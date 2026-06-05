"""Orquesta el flujo de procesamiento completo: cargar -> preprocesar -> segmentar -> evaluar/guardar."""
import cv2
import numpy as np

from . import config, dataset
from . import preprocessing as pp
from . import segmentation as seg
from . import metrics


def segment(rgb, fov_mask=None, params=None) -> np.ndarray:
    """Aplica el flujo de procesamiento a UNA imagen (a la resolución recibida) -> máscara binaria {0,1}."""
    p = {**config.DEFAULT_PARAMS, **(params or {})}
    g = pp.green_channel(rgb)
    g = pp.denoise(g, p["median_ksize"])
    g = pp.clahe(g, p["clahe_clip"], p["clahe_grid"])
    g = pp.correct_illumination(g, p["bg_kernel"])  # black top-hat: vasos -> claros
    # Flujo ganador (ablación + refinamiento): top-hat con kernel pequeño +
    # umbral por percentil supera a Frangi y a Otsu en HRF (Dice ~0.70).
    # Frangi queda en segmentation.py solo para comparación.
    binary = seg.threshold_percentile(g, fov_mask=fov_mask, pct=p["pct"])
    binary = seg.clean(binary, fov_mask=fov_mask, min_size=p["min_size"])
    return binary


def _downscale(img, scale, interp):
    if scale == 1.0:
        return img
    h, w = img.shape[:2]
    return cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=interp)


def _save_png(path, img) -> bool:
    """Guarda una imagen como PNG soportando rutas Unicode (Windows).

    cv2.imwrite falla con rutas que tienen acentos; codificamos en memoria y
    escribimos los bytes con open().
    """
    ok, buf = cv2.imencode(".png", img)
    if ok:
        with open(path, "wb") as f:
            f.write(buf.tobytes())
    return ok


def run(samples=None, params=None, scale=None, save=True, verbose=True):
    """Corre el flujo de procesamiento sobre todo el dataset.

    - Guarda cada predicción en /predicted_masks (resolución original).
    - Devuelve una lista de dicts con las métricas por imagen (las que tienen GT).
    """
    samples = samples if samples is not None else dataset.list_samples()
    scale = config.SCALE if scale is None else scale
    config.PREDICTED_MASKS_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for i, s in enumerate(samples, 1):
        rgb = dataset.read_rgb(s.image_path)
        fov = dataset.read_binary(s.mask_path) if s.mask_path else None
        H, W = rgb.shape[:2]

        # Procesar (opcionalmente a menor resolución para acelerar)
        rgb_s = _downscale(rgb, scale, cv2.INTER_AREA)
        fov_s = _downscale(fov, scale, cv2.INTER_NEAREST) if fov is not None else None
        pred_s = segment(rgb_s, fov_mask=fov_s, params=params)

        # Devolver a resolución original (para guardar y comparar con el GT)
        pred = pred_s if scale == 1.0 else cv2.resize(
            pred_s, (W, H), interpolation=cv2.INTER_NEAREST)

        if save:
            _save_png(config.PREDICTED_MASKS_DIR / f"{s.name}.png", pred * 255)

        if s.gt_path:
            gt = dataset.read_binary(s.gt_path)
            pred_eval = pred
            fov_eval = fov
            if pred_eval.shape != gt.shape:
                pred_eval = cv2.resize(pred_eval, (gt.shape[1], gt.shape[0]),
                                       interpolation=cv2.INTER_NEAREST)
            if fov is not None and fov.shape != gt.shape:
                fov_eval = cv2.resize(fov, (gt.shape[1], gt.shape[0]),
                                      interpolation=cv2.INTER_NEAREST)
            m = metrics.all_metrics(pred_eval, gt, mask=fov_eval)
            m["name"] = s.name
            rows.append(m)
            if verbose:
                print(f"[{i:>2}/{len(samples)}] {s.name:<10} "
                      f"Dice={m['dice']:.4f}  IoU={m['iou']:.4f}")
        elif verbose:
            print(f"[{i:>2}/{len(samples)}] {s.name:<10} (sin ground truth, solo se guardó)")
    return rows


def summary(rows) -> dict:
    """Promedio de cada métrica sobre todas las imágenes evaluadas."""
    if not rows:
        return {}
    keys = ["dice", "iou", "sensitivity", "specificity", "accuracy"]
    return {k: float(np.mean([r[k] for r in rows])) for k in keys}
