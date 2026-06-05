"""Métricas de evaluación de segmentación.

Las que califica el profe son **Dice** e **IoU (Jaccard)**; incluyo además
sensibilidad, especificidad y accuracy para tu análisis. Todo se evalúa solo
dentro de la máscara FOV (la región válida de la retina).
"""
import numpy as np

_EPS = 1e-7


def _counts(pred, gt, mask=None):
    """Cuenta TP, TN, FP, FN (restringido al FOV si se pasa máscara)."""
    pred = pred.astype(bool)
    gt = gt.astype(bool)
    if mask is not None:
        valid = mask.astype(bool)
        pred = pred & valid
        gt = gt & valid
    else:
        valid = np.ones_like(gt, dtype=bool)
    tp = int(np.sum(pred & gt))
    tn = int(np.sum((~pred) & (~gt) & valid))
    fp = int(np.sum(pred & (~gt)))
    fn = int(np.sum((~pred) & gt))
    return tp, tn, fp, fn


def dice(pred, gt, mask=None) -> float:
    """Coeficiente de Dice = 2*TP / (2*TP + FP + FN). Rango [0,1], 1 = perfecto."""
    tp, _, fp, fn = _counts(pred, gt, mask)
    return 2 * tp / (2 * tp + fp + fn + _EPS)


def iou(pred, gt, mask=None) -> float:
    """Índice de Jaccard (IoU) = TP / (TP + FP + FN). Rango [0,1], 1 = perfecto."""
    tp, _, fp, fn = _counts(pred, gt, mask)
    return tp / (tp + fp + fn + _EPS)


def all_metrics(pred, gt, mask=None) -> dict:
    """Devuelve un diccionario con todas las métricas."""
    tp, tn, fp, fn = _counts(pred, gt, mask)
    return {
        "dice": 2 * tp / (2 * tp + fp + fn + _EPS),
        "iou": tp / (tp + fp + fn + _EPS),
        "sensitivity": tp / (tp + fn + _EPS),
        "specificity": tn / (tn + fp + _EPS),
        "accuracy": (tp + tn) / (tp + tn + fp + fn + _EPS),
    }
