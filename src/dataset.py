"""Carga del dataset HRF: empareja cada imagen con su ground truth y su máscara FOV.

Soporta dos organizaciones de carpeta:
  A) Estándar HRF:  data/HRF/images, data/HRF/manual1, data/HRF/mask
  B) Plana:         data/HRF/ con todos los archivos juntos
     (imágenes = .jpg/.JPG/.png ; máscaras = *_mask.tif ; ground truth = resto de *.tif)
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np

from . import config

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".ppm"}
LABEL_EXTS = {".tif", ".tiff", ".png", ".gif"}


@dataclass
class Sample:
    """Una muestra del dataset: imagen + (opcional) ground truth + (opcional) máscara FOV."""
    name: str
    image_path: Path
    gt_path: Optional[Path] = None
    mask_path: Optional[Path] = None


def list_samples() -> List[Sample]:
    """Devuelve la lista de muestras, detectando el layout automáticamente."""
    if config.IMAGES_DIR.exists():
        return _list_structured()
    if config.DATA_DIR.exists():
        return _list_flat()
    raise FileNotFoundError(
        f"No encuentro los datos. Coloca el dataset HRF en: {config.DATA_DIR}"
    )


def _list_structured() -> List[Sample]:
    samples = []
    for img in sorted(config.IMAGES_DIR.iterdir()):
        if img.suffix.lower() not in IMAGE_EXTS:
            continue
        stem = img.stem
        gt = _first_existing(config.GT_DIR,
                             [f"{stem}.tif", f"{stem}.tiff", f"{stem}.png", f"{stem}.gif"])
        mask = _first_existing(config.MASK_DIR,
                               [f"{stem}_mask.tif", f"{stem}_mask.tiff",
                                f"{stem}.tif", f"{stem}_mask.png"])
        samples.append(Sample(stem, img, gt, mask))
    return samples


def _list_flat() -> List[Sample]:
    files = [p for p in config.DATA_DIR.iterdir() if p.is_file()]
    images = [p for p in files if p.suffix.lower() in IMAGE_EXTS]
    masks = {p.stem[:-5]: p for p in files
             if p.suffix.lower() in LABEL_EXTS and p.stem.endswith("_mask")}
    gts = {p.stem: p for p in files
           if p.suffix.lower() in LABEL_EXTS and not p.stem.endswith("_mask")}
    samples = []
    for img in sorted(images):
        stem = img.stem
        samples.append(Sample(stem, img, gts.get(stem), masks.get(stem)))
    return samples


def _first_existing(folder: Path, candidates) -> Optional[Path]:
    if not folder.exists():
        return None
    for c in candidates:
        p = folder / c
        if p.exists():
            return p
    return None


def _imread_unicode(path: Path, flag: int):
    """Lee una imagen soportando rutas con caracteres no-ASCII (Windows).

    cv2.imread NO maneja rutas Unicode en Windows (p. ej. 'Visión'); leemos los
    bytes con open() —que sí las maneja— y decodificamos con cv2.imdecode.
    """
    with open(path, "rb") as f:
        buf = np.frombuffer(f.read(), dtype=np.uint8)
    return cv2.imdecode(buf, flag)


def read_rgb(path: Path) -> np.ndarray:
    """Lee una imagen a color en formato RGB."""
    bgr = _imread_unicode(path, cv2.IMREAD_COLOR)
    if bgr is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {path}")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def read_binary(path: Path) -> np.ndarray:
    """Lee una imagen como máscara binaria {0,1}."""
    img = _imread_unicode(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer: {path}")
    return (img > 127).astype(np.uint8)
