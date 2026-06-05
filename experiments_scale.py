# -*- coding: utf-8 -*-
"""Prueba el flujo ganador a RESOLUCIÓN COMPLETA (SCALE=1.0), re-ajustando el
tamaño del kernel del top-hat y el min_size (que escalan con la resolución).
Compara contra el resultado a SCALE=0.5 (Dice ~0.70 en el subconjunto).
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import cv2
import numpy as np
import pandas as pd

from experiments import segment_cfg, pick_subset
from src import dataset, metrics

samples = dataset.list_samples()
subset = pick_subset(samples, 3)

# Precargar a resolución COMPLETA (sin reescalar)
cache = []
for s in subset:
    rgb = dataset.read_rgb(s.image_path)
    gt = dataset.read_binary(s.gt_path)
    fov = dataset.read_binary(s.mask_path) if s.mask_path else None
    cache.append((rgb, fov, gt))


def eval_cfg(cfg):
    ds, js = [], []
    for rgb, fov, gt in cache:
        pred = segment_cfg(rgb, fov, cfg)
        if pred.shape != gt.shape:
            pred = cv2.resize(pred, (gt.shape[1], gt.shape[0]),
                              interpolation=cv2.INTER_NEAREST)
        ds.append(metrics.dice(pred, gt, mask=fov))
        js.append(metrics.iou(pred, gt, mask=fov))
    return float(np.mean(ds)), float(np.mean(js))


# A resolución completa los tamaños escalan ~x2 (kernel) y ~x4 (área/min_size)
BASE = dict(median=5, clahe=True, illum=True, threshold="percentile",
            clahe_clip=2.0, pct=90)
rows = []
t0 = time.time()
for bg in [21, 31, 41]:
    for ms in [120, 240]:
        cfg = dict(BASE, bg_kernel=bg, min_size=ms)
        d, j = eval_cfg(cfg)
        rows.append({"config": f"bg{bg}_ms{ms}", "bg_kernel": bg, "min_size": ms,
                     "dice": round(d, 4), "jaccard": round(j, 4)})
        print(f"SCALE=1.0  bg{bg}_ms{ms}  Dice={d:.4f}  Jaccard={j:.4f}", flush=True)

df = pd.DataFrame(rows).sort_values("dice", ascending=False).reset_index(drop=True)
(ROOT / "results").mkdir(exist_ok=True)
df.to_csv(ROOT / "results" / "scale_full.csv", index=False)
print("\n=== TOP (SCALE=1.0) ===")
print(df.head().to_string(index=False))
print("\nReferencia SCALE=0.5 (subconjunto): Dice 0.702 / Jaccard 0.543")
print(f"Tiempo: {time.time() - t0:.1f}s")
