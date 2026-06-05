# -*- coding: utf-8 -*-
"""Refinamiento: parte del flujo ganador (top-hat + umbral) y busca los mejores
parámetros (tamaño del kernel del top-hat, tipo de umbral, clip de CLAHE).

Precarga el subconjunto una vez para ir rápido. Guarda results/refinamiento.csv.
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import cv2
import numpy as np
import pandas as pd

from experiments import segment_cfg, pick_subset, SCALE
from src import dataset, metrics

samples = dataset.list_samples()
subset = pick_subset(samples, 3)

# Precargar imágenes del subconjunto (a escala) una sola vez
cache = []
for s in subset:
    rgb = dataset.read_rgb(s.image_path)
    gt = dataset.read_binary(s.gt_path)
    fov = dataset.read_binary(s.mask_path) if s.mask_path else None
    rgb_s = cv2.resize(rgb, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_AREA)
    fov_s = (cv2.resize(fov, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_NEAREST)
             if fov is not None else None)
    cache.append((rgb_s, fov_s, gt, fov))


def eval_cfg(cfg):
    ds, js = [], []
    for rgb_s, fov_s, gt, fov in cache:
        pred = segment_cfg(rgb_s, fov_s, cfg)
        pred = cv2.resize(pred, (gt.shape[1], gt.shape[0]), interpolation=cv2.INTER_NEAREST)
        ds.append(metrics.dice(pred, gt, mask=fov))
        js.append(metrics.iou(pred, gt, mask=fov))
    return float(np.mean(ds)), float(np.mean(js))


# Flujo ganador como base; variamos kernel del top-hat, umbral y clip de CLAHE
# Ronda 2: el top-hat con kernel pequeño rinde más -> exploramos kernels chicos,
# el percentil del umbral y el tamaño mínimo de objeto (para no perder vasos finos).
BASE = dict(median=5, clahe=True, illum=True, threshold="percentile", clahe_clip=2.0)
rows = []
t0 = time.time()
for bg in [11, 15, 21, 25, 31, 35]:
    for pct in [88, 90, 92]:
        for ms in [30, 60]:
            cfg = dict(BASE, bg_kernel=bg, pct=pct, min_size=ms)
            d, j = eval_cfg(cfg)
            label = f"bg{bg}_pct{pct}_ms{ms}"
            rows.append({"config": label, "bg_kernel": bg, "pct": pct,
                         "min_size": ms, "dice": round(d, 4), "jaccard": round(j, 4)})
            print(f"{label:20s}  Dice={d:.4f}  Jaccard={j:.4f}", flush=True)

df = pd.DataFrame(rows).sort_values("dice", ascending=False).reset_index(drop=True)
(ROOT / "results").mkdir(exist_ok=True)
df.to_csv(ROOT / "results" / "refinamiento.csv", index=False)
print("\n=== TOP 5 ===")
print(df[["config", "dice", "jaccard"]].head().to_string(index=False))
best = df.iloc[0]
print(f"\nMEJOR: {best['config']}  Dice={best['dice']}  Jaccard={best['jaccard']}")
print(f"Tiempo: {time.time() - t0:.1f}s")
