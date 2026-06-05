# -*- coding: utf-8 -*-
"""Estudio de ablación: añade/varía técnicas y mide Dice y Jaccard.

Corre sobre un subconjunto representativo (N por categoría) para iterar rápido.
Guarda results/ablacion.csv.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import cv2
import numpy as np
import pandas as pd

from src import dataset, metrics
from src import preprocessing as pp
from src import segmentation as seg

SCALE = 0.5
SUBSET_PER_CAT = 3   # imágenes por categoría (sano/retinopatía/glaucoma)


def categoria(n):
    if n.endswith("_h"):
        return "sano"
    if n.endswith("_dr"):
        return "retinopatia"
    return "glaucoma"


def pick_subset(samples, per_cat):
    by = {}
    for s in samples:
        by.setdefault(categoria(s.name), []).append(s)
    sub = []
    for _, lst in by.items():
        sub += sorted(lst, key=lambda s: s.name)[:per_cat]
    return sub


def segment_cfg(rgb, fov, cfg):
    """Segmenta UNA imagen según la configuración (flags) dada."""
    g = pp.green_channel(rgb)
    if cfg.get("median"):
        g = pp.denoise(g, cfg["median"])
    if cfg.get("clahe"):
        g = pp.clahe(g, cfg.get("clahe_clip", 2.0), cfg.get("clahe_grid", 8))
    used_illum = False
    if cfg.get("illum"):
        g = pp.correct_illumination(g, cfg.get("bg_kernel", 55))
        used_illum = True

    if cfg.get("frangi"):
        feat = seg.frangi_vesselness(g, sigmas=cfg.get("sigmas", (1, 6)),
                                     black_ridges=False)
    else:
        # sin Frangi: si hubo corrección de iluminación los vasos ya son claros;
        # si no, invertimos (vasos oscuros -> claros) para poder umbralizar.
        feat = g if used_illum else (255 - g)

    th = cfg.get("threshold", "otsu")
    if th == "otsu":
        b = seg.threshold_otsu(feat)
    elif th == "adaptive":
        b = seg.threshold_adaptive(feat, cfg.get("block", 51), cfg.get("C", -2))
    elif th == "percentile":
        b = seg.threshold_percentile(feat, fov_mask=fov, pct=cfg.get("pct", 92))
    else:
        raise ValueError(th)

    return seg.clean(b, fov_mask=fov, min_size=cfg.get("min_size", 60))


def evaluate(cfg, subset):
    ds, js = [], []
    for s in subset:
        rgb = dataset.read_rgb(s.image_path)
        gt = dataset.read_binary(s.gt_path)
        fov = dataset.read_binary(s.mask_path) if s.mask_path else None
        rgb_s = cv2.resize(rgb, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_AREA)
        fov_s = (cv2.resize(fov, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_NEAREST)
                 if fov is not None else None)
        pred = segment_cfg(rgb_s, fov_s, cfg)
        pred = cv2.resize(pred, (gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_NEAREST)
        ds.append(metrics.dice(pred, gt, mask=fov))
        js.append(metrics.iou(pred, gt, mask=fov))
    return float(np.mean(ds)), float(np.mean(js))


# Cada paso AÑADE una técnica respecto al anterior (ablación), y al final se
# comparan variantes de umbral sobre el flujo completo.
CONFIGS = [
    ("1. Canal verde + Otsu",        dict()),
    ("2. + Mediana + CLAHE",         dict(median=5, clahe=True)),
    ("3. + Correccion iluminacion",  dict(median=5, clahe=True, illum=True)),
    ("4. + Frangi (umbral Otsu)",    dict(median=5, clahe=True, illum=True, frangi=True, threshold="otsu")),
    ("5. Frangi + umbral percentil", dict(median=5, clahe=True, illum=True, frangi=True, threshold="percentile", pct=92)),
    ("6. Frangi + umbral adaptativo", dict(median=5, clahe=True, illum=True, frangi=True, threshold="adaptive")),
]


if __name__ == "__main__":
    t0 = time.time()
    samples = dataset.list_samples()
    subset = pick_subset(samples, SUBSET_PER_CAT)
    print(f"Subset ({len(subset)} imgs): {[s.name for s in subset]}\n", flush=True)

    rows = []
    for label, cfg in CONFIGS:
        d, j = evaluate(cfg, subset)
        rows.append({"config": label, "dice": round(d, 4), "jaccard": round(j, 4)})
        print(f"{label:34s}  Dice={d:.4f}  Jaccard={j:.4f}", flush=True)

    df = pd.DataFrame(rows)
    (ROOT / "results").mkdir(exist_ok=True)
    df.to_csv(ROOT / "results" / "ablacion.csv", index=False)
    best = df.loc[df["dice"].idxmax()]
    print(f"\nMEJOR: {best['config']}  Dice={best['dice']}  Jaccard={best['jaccard']}")
    print(f"Tiempo: {time.time() - t0:.1f}s")
