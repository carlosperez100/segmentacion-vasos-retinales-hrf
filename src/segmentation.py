"""Realce tubular (Frangi) y binarización de los vasos.

Incluye varias opciones de umbralización para que experimentes y compares Dice.
"""
import warnings

import cv2
import numpy as np
from skimage.filters import frangi
from skimage.morphology import remove_small_objects

# Silencia un FutureWarning de skimage (remove_small_objects) para una salida limpia
warnings.filterwarnings("ignore", message=".*min_size.*", category=FutureWarning)


def frangi_vesselness(gray: np.ndarray, sigmas=(1, 6),
                      black_ridges: bool = False) -> np.ndarray:
    """Filtro de Frangi: resalta estructuras tubulares (vasos) a varias escalas.

    Espera vasos *claros* (black_ridges=False) porque venimos de
    correct_illumination. Devuelve un mapa de 'vesselness' en uint8 [0,255].
    """
    img = gray.astype(np.float64) / 255.0
    smin, smax = sigmas
    scales = np.arange(smin, smax + 1)
    v = frangi(img, sigmas=scales, black_ridges=black_ridges)
    v = cv2.normalize(v, None, 0, 255, cv2.NORM_MINMAX)
    return v.astype(np.uint8)


def threshold_otsu(gray: np.ndarray) -> np.ndarray:
    """Umbral global automático de Otsu."""
    _, b = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return (b > 0).astype(np.uint8)


def threshold_adaptive(gray: np.ndarray, block: int = 51, c: int = -2) -> np.ndarray:
    """Umbral adaptativo (local): útil si la iluminación aún varía."""
    b = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY, block | 1, c)
    return (b > 0).astype(np.uint8)


def threshold_percentile(feat: np.ndarray, fov_mask=None, pct: float = 92) -> np.ndarray:
    """Conserva el pct% superior de la respuesta (dentro del FOV).

    Útil para el mapa de Frangi (muy sesgado): Otsu suele cortar demasiado alto
    y pierde vasos finos; fijar un percentil controla mejor la sensibilidad.
    """
    vals = feat[fov_mask > 0] if fov_mask is not None else feat.ravel()
    if vals.size == 0:
        return np.zeros_like(feat, dtype=np.uint8)
    thr = np.percentile(vals, pct)
    return (feat >= thr).astype(np.uint8)


def clean(binary: np.ndarray, fov_mask=None, min_size: int = 60) -> np.ndarray:
    """Quita componentes pequeños (ruido) y recorta el resultado al FOV."""
    b = remove_small_objects(binary.astype(bool), min_size=min_size).astype(np.uint8)
    if fov_mask is not None:
        b = b * (fov_mask > 0).astype(np.uint8)
    return b
