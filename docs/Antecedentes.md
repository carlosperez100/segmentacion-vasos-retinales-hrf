# Antecedentes

**Trabajo parcial — Segmentación de vasos sanguíneos en imágenes de fondo de ojo**
**Curso:** Visión por Computador (Maestría en Inteligencia Artificial – UNI)
**Grupo 3 (Sección B):** Josemanuel Rossy Cañari Palante · Kenny Asto Hinostroza · Melissa Dessire Aylas Barranca · Carlos Pérez Pérez
**Dataset asignado:** HRF (High-Resolution Fundus)

---

## 1. Contexto del problema

La segmentación de los **vasos sanguíneos** en imágenes de fondo de ojo (retinografías)
es un paso fundamental y previo al diagnóstico asistido por computador de varias
enfermedades. Los oftalmólogos evalúan la **morfología vascular** (calibre, tortuosidad,
patrón de ramificación) para detectar **retinopatía diabética**, **glaucoma**,
**hipertensión** e incluso enfermedades **cardiovasculares**. Por ello, aislar la red
vascular de la imagen —separándola del disco óptico, la fóvea y el fondo— es el primer
problema a resolver, y es el objeto de este trabajo.

El reto técnico principal es resaltar los vasos (que se vuelven progresivamente más
finos hacia la periferia) sin perder información, mientras se atenúan elementos que
"estorban" como el disco óptico (brillante), la fóvea (oscura), la iluminación dispareja
y, en imágenes patológicas, las **lesiones** (exudados y hemorragias).

## 2. El dataset HRF (High-Resolution Fundus)

HRF es una base de datos pública creada por el *Pattern Recognition Lab* de la
**Universidad Friedrich-Alexander de Erlangen-Núremberg (FAU)**, Alemania, como
benchmark para la evaluación comparativa de algoritmos de segmentación vascular.

| Característica | Detalle |
|---|---|
| Nº de imágenes | **45** |
| Composición | 15 sanos (`_h`) · 15 retinopatía diabética (`_dr`) · 15 glaucoma (`_g`) |
| Resolución | **3504 × 2336** px (alta resolución) |
| Por cada imagen | foto a color (`.JPG`/`.jpg`), máscara FOV (*mask type 1*) y segmentación manual de vasos *gold standard* (*mask type 2*) |
| Organización | subcarpetas `images/`, `manual1/` (ground truth) y `mask/` (FOV) |
| Fuente oficial | https://www5.cs.fau.de/research/data/fundus-images/ (https://lme.tf.fau.de/) |

El *ground truth* fue segmentado manualmente píxel a píxel, lo que permite evaluar
objetivamente cualquier propuesta de segmentación contra una referencia experta.

## 3. Antecedentes en segmentación de vasos (métodos clásicos)

Como el trabajo exige **técnicas determinísticas (sin aprendizaje de máquina)**, se
toman como antecedentes los métodos clásicos de procesamiento de imágenes más robustos:

- **Filtros adaptados (*matched filters*)** — Chaudhuri et al. (1989): convolución con
  plantillas con forma de vaso en múltiples orientaciones.
- **Realce tubular por Hessiano (*vesselness*)** — Frangi et al. (1998): detección
  multiescala de estructuras alargadas mediante los autovalores del Hessiano.
- **Morfología matemática** — operadores *top-hat* con elementos estructurantes lineales
  para realzar estructuras delgadas y corregir iluminación.
- **Umbralización** global (Otsu) y **adaptativa/local**, y **crecimiento de regiones**.
- **Método de referencia del propio HRF** — Budai et al. (2013), segmentación vascular
  robusta multiescala.

La evaluación estándar en estas tareas (y la exigida en este trabajo) usa el
**coeficiente de Dice** y el **índice de Jaccard (IoU)**, ambos en el rango [0, 1].

## 4. Procedencia de los datos: dos fuentes obtenidas

Para garantizar la integridad de los datos de trabajo se obtuvieron **dos copias**
del dataset HRF y se compararon:

- **Fuente A — Drive de la profesora.** Carpeta `HRF` compartida por la docente
  (Elian Laura) en Google Drive, con subcarpetas `images/`, `manual1/` y `mask/`.
  Es la copia contra la que se realizará la **evaluación/calificación** del trabajo.
- **Fuente B — Sitio oficial de la FAU.** Archivo `all.zip` (~73 MB) descargado del
  repositorio oficial del *Pattern Recognition Lab* de la FAU.

> **Nota de obtención:** la descarga automatizada de la Fuente A (gdown) fue limitada
> por Google tras múltiples accesos, por lo que la copia de la profesora se obtuvo de
> forma manual; la Fuente B se descargó directamente del repositorio oficial.

## 5. Comparación de las dos fuentes (verificación de integridad)

Se compararon archivo por archivo ambas copias (nombres, conteos y **hash MD5** del
contenido):

| Subcarpeta | Archivos (Fuente A) | Archivos (Fuente B) | Idénticos (MD5) | Distintos |
|---|:--:|:--:|:--:|:--:|
| `images/`  | 45 | 45 | 45 | 0 |
| `manual1/` | 45 | 45 | 45 | 0 |
| `mask/`    | 45 | 45 | 45 | 0 |
| **Total**  | **135** | **135** | **135** | **0** |

**Resultado:** los **135 archivos son byte por byte idénticos**. Es decir, la copia de
la profesora **es exactamente el dataset HRF oficial de la FAU, sin modificación alguna**.

## 6. Diferencias encontradas y solución adoptada

- **Diferencias en el contenido:** *ninguna*. Imágenes, ground truth y máscaras FOV son
  idénticos entre ambas fuentes (verificado por MD5).
- **Aparente diferencia descartada:** en una primera revisión por API de Google Drive la
  carpeta de la profesora parecía **no incluir la subcarpeta `mask/`**; se comprobó que
  fue un **artefacto de indexación** de Drive, no una diferencia real: la carpeta `mask/`
  existe y contiene las 45 máscaras FOV.
- **Diferencias de empaquetado:** el sitio oficial de la FAU ofrece, además, recursos
  complementarios no requeridos para este trabajo (datasets de calidad de imagen,
  centros del disco óptico).

**Solución:** se trabaja con la **copia de la profesora** (`data/HRF/`) como fuente
única para el desarrollo y la evaluación, por ser la referencia de calificación; la
copia de la FAU se conserva como **respaldo y verificación de integridad**. Al ser
idénticas, los resultados son plenamente equivalentes al benchmark oficial.

## 7. Consideración técnica resuelta (reproducibilidad)

Durante la implementación se detectó que **OpenCV (`cv2.imread`/`imwrite`) no maneja
rutas con caracteres no ASCII en Windows** (la ruta del proyecto contiene la "í" de
*"Visión"*), lo que impedía leer las imágenes. Se resolvió leyendo/escribiendo los
bytes con `open()` y `cv2.imdecode`/`cv2.imencode`, de modo que el flujo de procesamiento funciona
independientemente de la ruta.

## 8. Referencias

1. Budai, A., Bock, R., Maier, A., Hornegger, J., & Michelson, G. (2013). *Robust Vessel
   Segmentation in Fundus Images*. International Journal of Biomedical Imaging.
2. Frangi, A. F., Niessen, W. J., Vincken, K. L., & Viergever, M. A. (1998). *Multiscale
   vessel enhancement filtering*. MICCAI.
3. Chaudhuri, S., Chatterjee, S., Katz, N., Nelson, M., & Goldbaum, M. (1989).
   *Detection of blood vessels in retinal images using two-dimensional matched filters*.
   IEEE Transactions on Medical Imaging.
4. HRF Database — Pattern Recognition Lab, FAU Erlangen.
   https://www5.cs.fau.de/research/data/fundus-images/
