"""Paquete del flujo de procesamiento de segmentación de vasos retinales (Grupo 3 - dataset HRF).

Módulos:
    config         -> rutas y parámetros del proyecto
    dataset        -> carga de imágenes, ground truth y máscaras FOV (HRF)
    preprocessing  -> canal verde, denoise, CLAHE, corrección de iluminación
    segmentation   -> realce de vasos (Frangi) y binarización
    metrics        -> Dice, IoU y otras métricas
    pipeline       -> orquesta todo y evalúa sobre el dataset
"""
