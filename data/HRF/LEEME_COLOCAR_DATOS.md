# Coloca aquí el dataset HRF

El dataset **no se incluye** en el repositorio (es público y pesado). Descárgalo y
colócalo en esta carpeta respetando la estructura:

```
data/HRF/
├─ images/    01_h.jpg, 01_dr.JPG, 01_g.jpg, ...   (45 imágenes)
├─ manual1/   01_h.tif, 01_dr.tif, ...             (ground truth)
└─ mask/      01_h_mask.tif, ...                    (máscaras FOV)
```

## Enlaces de descarga
- **Oficial (FAU):** https://www5.cs.fau.de/research/data/fundus-images/ (archivo `all.zip`)
- **Carpeta del curso (Google Drive):** https://drive.google.com/drive/folders/1Jy8XiGUqX5oGJCFKK18Osj48eETJ3f66

> El cargador (`src/dataset.py`) también detecta el dataset si lo dejas "plano"
> (todos los archivos juntos en `data/HRF/`).
