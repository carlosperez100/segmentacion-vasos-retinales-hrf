# -*- coding: utf-8 -*-
"""Corre el flujo de procesamiento base sobre el HRF y reporta Dice/IoU (global y por categoría)."""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import pandas as pd
from src import pipeline, config

print("Dataset:", config.DATA_DIR, "| SCALE:", config.SCALE, flush=True)

t0 = time.time()
rows = pipeline.run(save=True, verbose=True)
df = pd.DataFrame(rows)

print("\n=== PROMEDIOS (todas) ===")
print(pd.Series(pipeline.summary(rows)).round(4))


def categoria(n):
    if n.endswith("_h"):
        return "sano"
    if n.endswith("_dr"):
        return "retinopatia"
    if n.endswith("_g"):
        return "glaucoma"
    return "otro"


if not df.empty:
    df["categoria"] = df["name"].map(categoria)
    print("\n=== POR CATEGORIA ===")
    print(df.groupby("categoria")[["dice", "iou"]].mean().round(4))
    (ROOT / "results").mkdir(exist_ok=True)
    df.to_csv(ROOT / "results" / "baseline_metrics.csv", index=False)
    print("\nGuardado: results/baseline_metrics.csv")

print(f"\nTiempo total: {time.time() - t0:.1f}s ({len(rows)} imagenes)")
