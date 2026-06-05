"""Configuración central del proyecto (rutas y parámetros).

Edita aquí si tu carpeta de datos está organizada distinto.
"""
from pathlib import Path

# Raíz del proyecto = carpeta que contiene /src, /data, /predicted_masks
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# --- Dataset (Grupo 3 = HRF) ---
DATASET_NAME = "HRF"
DATA_DIR = PROJECT_ROOT / "data" / DATASET_NAME

# Layout estándar de HRF (subcarpetas). Si tu copia de Drive viene "plana"
# (todos los archivos juntos en data/HRF/), el cargador lo detecta solo.
IMAGES_DIR = DATA_DIR / "images"   # fotos: 01_h.jpg, 01_dr.JPG, 01_g.jpg, ...
GT_DIR = DATA_DIR / "manual1"      # ground truth: 01_h.tif, ...
MASK_DIR = DATA_DIR / "mask"       # máscaras FOV: 01_h_mask.tif, ...

# --- Salidas ---
PREDICTED_MASKS_DIR = PROJECT_ROOT / "predicted_masks"   # EXIGIDO por el enunciado
RESULTS_DIR = PROJECT_ROOT / "results"

# --- Parámetros de procesamiento (punto de partida; hay que experimentar) ---
# HRF es 3504x2336 (pesado). Factor de reescalado para procesar:
#   0.5 = mitad de resolución -> rápido para iterar
#   1.0 = resolución completa -> úsalo para el resultado FINAL (mejor Dice)
SCALE = 0.5

# Parámetros por defecto del flujo de procesamiento (se pueden sobreescribir por experimento)
DEFAULT_PARAMS = {
    "median_ksize": 5,       # suavizado (mediana, impar)
    "clahe_clip": 2.0,       # límite de contraste de CLAHE
    "clahe_grid": 8,         # tamaño de tile de CLAHE
    "bg_kernel": 15,         # kernel del top-hat (refinamiento: chico capta vasos finos)
    "pct": 90,               # percentil del umbral sobre el realce top-hat
    "frangi_sigmas": (1, 6), # (solo para experimentos de comparación; no en el flujo final)
    "min_size": 60,          # eliminar componentes conectados < min_size px
}
