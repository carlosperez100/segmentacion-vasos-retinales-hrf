# -*- coding: utf-8 -*-
"""Genera los gráficos para el informe/video en results/figuras/.

- 01 ablación (barras)            <- results/ablacion.csv
- 02 flujo paso a paso            <- imagen 01_h con el flujo ganador
- 03 overlay aciertos/errores     <- imagen 01_h
- 04 Dice/Jaccard por categoría   <- results/baseline_metrics.csv (corrida de las 45)
- 05 boxplot del Dice             <- results/baseline_metrics.csv
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd

from src import dataset, config, metrics, pipeline
from src import preprocessing as pp

OUT = ROOT / "results" / "figuras"
OUT.mkdir(parents=True, exist_ok=True)
SCALE = config.SCALE
P = config.DEFAULT_PARAMS

# ---------- 1) Barras de la ablación ----------
abl_path = ROOT / "results" / "ablacion.csv"
if abl_path.exists():
    abl = pd.read_csv(abl_path)
    best_i = int(abl["dice"].idxmax())
    colors = ["#9aa0a6"] * len(abl)
    colors[best_i] = "#2a9d8f"
    plt.figure(figsize=(9, 4.8))
    plt.bar(range(len(abl)), abl["dice"], color=colors)
    plt.xticks(range(len(abl)), abl["config"], rotation=30, ha="right", fontsize=8)
    plt.ylabel("Dice"); plt.ylim(0, 1)
    plt.title("Estudio de ablación — Dice por configuración")
    for i, v in enumerate(abl["dice"]):
        plt.text(i, v + 0.015, f"{v:.2f}", ha="center", fontsize=8)
    plt.tight_layout(); plt.savefig(OUT / "01_ablacion.png", dpi=130); plt.close()

# ---------- Procesar una imagen sana con el FLUJO GANADOR ----------
sample = next(s for s in dataset.list_samples() if s.name == "01_h")
rgb = dataset.read_rgb(sample.image_path)
gt = dataset.read_binary(sample.gt_path)
fov = dataset.read_binary(sample.mask_path)
rgb_s = cv2.resize(rgb, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_AREA)
fov_s = cv2.resize(fov, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_NEAREST)

g0 = pp.green_channel(rgb_s)
g1 = pp.denoise(g0, P["median_ksize"])
g2 = pp.clahe(g1, P["clahe_clip"], P["clahe_grid"])
g3 = pp.correct_illumination(g2, P["bg_kernel"])
pred_s = pipeline.segment(rgb_s, fov_mask=fov_s)   # flujo ganador completo

# ---------- 2) Montaje paso a paso ----------
fig, ax = plt.subplots(1, 5, figsize=(20, 4.6))
panels = [(g0, "1. Canal verde"), (g1, "2. Mediana"), (g2, "3. CLAHE"),
          (g3, "4. Top-hat (iluminacion)"), (pred_s * 255, "5. Umbral percentil + limpieza")]
for a, (im, t) in zip(ax, panels):
    a.imshow(im, cmap="gray"); a.set_title(t); a.axis("off")
plt.suptitle(f"Flujo de procesamiento ganador — imagen {sample.name}", fontsize=13)
plt.tight_layout(); plt.savefig(OUT / "02_flujo_pasos.png", dpi=130); plt.close()

# ---------- 3) Overlay aciertos/errores (TP/FP/FN) ----------
pred = cv2.resize(pred_s, (gt.shape[1], gt.shape[0]),
                  interpolation=cv2.INTER_NEAREST).astype(bool)
gtb = gt.astype(bool) & (fov > 0)
predb = pred & (fov > 0)
ov = np.zeros((*gt.shape, 3), np.uint8)
ov[predb & gtb] = (0, 200, 0)
ov[predb & ~gtb] = (220, 0, 0)
ov[~predb & gtb] = (0, 90, 255)
m = metrics.all_metrics(predb.astype(np.uint8), gt, mask=fov)
fig, ax = plt.subplots(1, 3, figsize=(18, 7))
ax[0].imshow(rgb); ax[0].set_title("Original")
ax[1].imshow(gt, cmap="gray"); ax[1].set_title("Ground truth (experto)")
ax[2].imshow(ov)
ax[2].set_title(f"Verde=acierto · Rojo=falso+ · Azul=perdido\nDice={m['dice']:.3f} · Jaccard={m['iou']:.3f}")
for a in ax:
    a.axis("off")
plt.tight_layout(); plt.savefig(OUT / "03_overlay_aciertos_errores.png", dpi=130); plt.close()

# ---------- 4) y 5) desde las métricas de las 45 ----------
mpath = ROOT / "results" / "baseline_metrics.csv"
if mpath.exists():
    dfm = pd.read_csv(mpath)
    order = ["sano", "retinopatia", "glaucoma"]
    g = dfm.groupby("categoria")[["dice", "iou"]].mean().reindex(order)

    x = np.arange(len(order)); w = 0.35
    plt.figure(figsize=(7, 4.8))
    plt.bar(x - w / 2, g["dice"], w, label="Dice", color="#2a9d8f")
    plt.bar(x + w / 2, g["iou"], w, label="Jaccard", color="#e9c46a")
    plt.xticks(x, order); plt.ylim(0, 1); plt.ylabel("valor"); plt.legend()
    plt.title("Dice / Jaccard por categoría (45 imágenes)")
    for i, (d, j) in enumerate(zip(g["dice"], g["iou"])):
        plt.text(i - w / 2, d + 0.01, f"{d:.2f}", ha="center", fontsize=8)
        plt.text(i + w / 2, j + 0.01, f"{j:.2f}", ha="center", fontsize=8)
    plt.tight_layout(); plt.savefig(OUT / "04_por_categoria.png", dpi=130); plt.close()

    plt.figure(figsize=(7, 4.8))
    data = [dfm[dfm["categoria"] == c]["dice"].values for c in order]
    plt.boxplot(data, labels=order, showmeans=True)
    plt.ylabel("Dice"); plt.ylim(0, 1)
    plt.title("Distribución del Dice por categoría (45 imágenes)")
    plt.tight_layout(); plt.savefig(OUT / "05_boxplot_dice.png", dpi=130); plt.close()

print("Figuras guardadas en results/figuras/:")
for p in sorted(OUT.glob("*.png")):
    print("  ", p.name)
