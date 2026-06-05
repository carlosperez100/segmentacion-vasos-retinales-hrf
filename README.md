# Segmentación de vasos sanguíneos en imágenes de fondo de ojo (HRF)

Trabajo parcial — **Visión por Computador**, Maestría en Inteligencia Artificial (UNI).
Segmentación de vasos retinales en el dataset **HRF** usando **técnicas determinísticas
(sin Machine Learning)**, evaluada con **coeficiente de Dice** e **índice de Jaccard (IoU)**.

**Grupo 3 (Sección B):** Josemanuel Rossy Cañari Palante · Kenny Asto Hinostroza ·
Melissa Dessire Aylas Barranca · Carlos Pérez Pérez

## 🏆 Resultado

**Dice 0.716 · Jaccard 0.560** sobre las 45 imágenes.
Flujo ganador: `canal verde → mediana → CLAHE → corrección de iluminación (black top-hat)
→ umbral por percentil → limpieza + recorte al FOV`.

📊 **Reporte visual (HTML):** abre `index.html` o visítalo en
**https://carlosperez100.github.io/segmentacion-vasos-retinales-hrf/**

## 📁 Estructura

```
src/                     código en módulos (config, dataset, preprocessing,
                         segmentation, metrics, pipeline)
notebooks/               01_pipeline_HRF.ipynb (demo + evaluación)
docs/                    Antecedentes.md · Metodologia_y_Resultados.md
results/                 figuras/ (gráficos) · *.csv (métricas, ablación)
predicted_masks/         máscaras resultantes (salida exigida)
run_baseline.py          corre el flujo sobre las 45 imágenes
experiments.py           estudio de ablación
experiments_refine.py    búsqueda de parámetros (refinamiento)
make_figures.py          genera las figuras
build_html.py            genera index.html
```

## 📥 Dataset (no incluido en el repositorio)

Descárgalo y colócalo en `data/HRF/` (subcarpetas `images/`, `manual1/`, `mask/`):

- **Oficial (FAU):** https://www5.cs.fau.de/research/data/fundus-images/
- **Carpeta del curso (Google Drive):** https://drive.google.com/drive/folders/1Jy8XiGUqX5oGJCFKK18Osj48eETJ3f66

## ▶️ Cómo ejecutar

```bash
pip install -r requirements.txt
python run_baseline.py     # corre las 45 -> predicted_masks/ + results/baseline_metrics.csv
python experiments.py      # estudio de ablación
python make_figures.py     # regenera las figuras
```

## 📄 Documentos

- [Antecedentes](docs/Antecedentes.md) — contexto, dataset y comparación de fuentes.
- [Metodología y Resultados](docs/Metodologia_y_Resultados.md) — flujo, experimentos, resultados y fórmulas.

> Método 100% determinístico (sin aprendizaje de máquina). Selección del mejor flujo por Dice y Jaccard.
