"""Etapas de preprocesamiento para realzar los vasos antes de segmentar.

Cada función está aislada para que puedas activarla/desactivarla y JUSTIFICAR
en el video por qué la usas (el profe califica sobre todo el "por qué").
"""
import cv2
import numpy as np


def green_channel(rgb: np.ndarray) -> np.ndarray:
    """El canal verde es donde mejor contrastan los vasos en fondo de ojo.

    (El rojo suele estar saturado y el azul es oscuro/ruidoso.)
    """
    return rgb[:, :, 1]


def denoise(gray: np.ndarray, ksize: int = 5) -> np.ndarray:
    """Filtro de mediana: quita ruido preservando los bordes de los vasos."""
    if ksize and ksize >= 3:
        return cv2.medianBlur(gray, ksize | 1)  # | 1 asegura impar
    return gray


def clahe(gray: np.ndarray, clip: float = 2.0, grid: int = 8) -> np.ndarray:
    """Realce de contraste local adaptativo: hace resaltar los vasos finos."""
    op = cv2.createCLAHE(clipLimit=clip, tileGridSize=(grid, grid))
    return op.apply(gray)


def correct_illumination(gray: np.ndarray, kernel: int = 55) -> np.ndarray:
    """Corrige la iluminación dispareja y realza los vasos.

    Estima el fondo con un cierre morfológico grande (que "tapa" los vasos
    oscuros) y lo resta. Equivale a un black top-hat: los vasos (oscuros)
    quedan BRILLANTES sobre un fondo uniforme, y se atenúan el disco óptico
    y el gradiente de iluminación.
    """
    k = kernel | 1
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    background = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, se)
    return cv2.subtract(background, gray)
