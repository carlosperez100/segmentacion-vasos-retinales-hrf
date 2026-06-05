# -*- coding: utf-8 -*-
"""Genera index.html autocontenible (figuras embebidas en base64) para publicar."""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "results" / "figuras"

OWNER = "carlosperez100"
REPO = "segmentacion-vasos-retinales-hrf"
REPO_URL = f"https://github.com/{OWNER}/{REPO}"
DRIVE_HRF = "https://drive.google.com/drive/folders/1Jy8XiGUqX5oGJCFKK18Osj48eETJ3f66"
FAU_URL = "https://www5.cs.fau.de/research/data/fundus-images/"


def img64(name):
    p = FIG / name
    if not p.exists():
        return ""
    b = base64.b64encode(p.read_bytes()).decode()
    return f"data:image/png;base64,{b}"


F = {n: img64(n) for n in ["01_ablacion.png", "02_flujo_pasos.png",
                           "03_overlay_aciertos_errores.png",
                           "04_por_categoria.png", "05_boxplot_dice.png"]}

CSS = """
:root{--t:#2a9d8f;--d:#264653;--bg:#f6f8f9;--card:#fff;--mut:#5b6b73}
*{box-sizing:border-box}
body{margin:0;font-family:'Segoe UI',Roboto,Arial,sans-serif;color:var(--d);background:var(--bg);line-height:1.55}
header{background:linear-gradient(135deg,#264653,#2a9d8f);color:#fff;padding:48px 24px;text-align:center}
header h1{margin:0 0 8px;font-size:1.9rem}
header p{margin:4px 0;opacity:.95}
.team{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:16px}
.team span{background:rgba(255,255,255,.18);padding:6px 12px;border-radius:20px;font-size:.9rem}
main{max-width:980px;margin:0 auto;padding:24px}
section{background:var(--card);border-radius:12px;padding:22px 26px;margin:18px 0;box-shadow:0 1px 4px rgba(0,0,0,.07)}
h2{color:var(--t);border-bottom:2px solid #e7eef0;padding-bottom:8px;margin-top:0}
h3{color:var(--d);margin-bottom:6px}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:.93rem}
th,td{border:1px solid #e2e8ea;padding:8px 10px;text-align:left}
th{background:#eef5f4;color:var(--d)}
td.n,th.n{text-align:center}
img{max-width:100%;border-radius:8px;border:1px solid #e2e8ea;margin:8px 0}
figcaption{color:var(--mut);font-size:.85rem;margin-bottom:14px}
.kpi{display:flex;flex-wrap:wrap;gap:14px;margin:8px 0}
.kpi div{flex:1;min-width:130px;background:#eef5f4;border-radius:10px;padding:14px;text-align:center}
.kpi b{display:block;font-size:1.6rem;color:var(--t)}
.badge{display:inline-block;background:var(--t);color:#fff;padding:3px 10px;border-radius:6px;font-size:.8rem}
a{color:var(--t)}
.links a{display:inline-block;margin:6px 10px 6px 0;background:#eef5f4;padding:8px 14px;border-radius:8px;text-decoration:none}
footer{text-align:center;color:var(--mut);padding:24px;font-size:.85rem}
code{background:#eef5f4;padding:1px 6px;border-radius:4px}
pre{background:#0f172a;color:#e6edf3;padding:12px 14px;border-radius:8px;overflow:auto;font-size:.84rem;line-height:1.45}
ol li{margin:8px 0}
"""

HTML = f"""<!DOCTYPE html>
<html lang="es"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Segmentación de vasos retinales — Grupo 3 (HRF)</title>
<style>{CSS}</style></head>
<body>
<header>
  <h1>Segmentación de vasos sanguíneos en imágenes de fondo de ojo</h1>
  <p><b>Dataset HRF</b> · Técnicas determinísticas (sin Machine Learning) · Métricas: Dice y Jaccard</p>
  <p>Curso de Visión por Computador — Maestría en Inteligencia Artificial (UNI)</p>
  <div class="team">
    <span>👥 Grupo 3 · Sección B</span>
    <span>Josemanuel Rossy Cañari Palante</span>
    <span>Kenny Asto Hinostroza</span>
    <span>Melissa Dessire Aylas Barranca</span>
    <span>Carlos Pérez Pérez</span>
  </div>
</header>
<main>

<section>
  <h2>1. Objetivo</h2>
  <p>Segmentar los <b>vasos sanguíneos</b> de las 45 imágenes del dataset <b>HRF</b>
  (15 sanas, 15 con retinopatía diabética, 15 con glaucoma) usando <b>solo técnicas
  clásicas de procesamiento de imágenes</b> (sin aprendizaje de máquina), maximizando
  el <b>coeficiente de Dice</b> y el <b>índice de Jaccard (IoU)</b>.</p>
  <div class="kpi">
    <div><b>0.716</b>Dice (45 img)</div>
    <div><b>0.560</b>Jaccard (45 img)</div>
    <div><b>0.746</b>Sensibilidad</div>
    <div><b>45</b>imágenes</div>
  </div>
</section>

<section>
  <h2>2. Dataset HRF</h2>
  <p>Base pública del <i>Pattern Recognition Lab</i> (Universidad FAU Erlangen). Cada
  imagen (3504×2336) trae su foto, la máscara FOV y el <i>ground truth</i> de vasos
  segmentado a mano.</p>
  <div class="links">
    <a href="{FAU_URL}" target="_blank">⬇️ Descarga oficial (FAU)</a>
    <a href="{DRIVE_HRF}" target="_blank">⬇️ Carpeta del curso (Google Drive)</a>
  </div>
  <p style="color:var(--mut);font-size:.85rem">Nota: el dataset no se incluye en el
  repositorio (es público y pesado); usa los enlaces de descarga.</p>
</section>

<section>
  <h2>3. Flujo de procesamiento (propuesta ganadora)</h2>
  <figure><img src="{F['02_flujo_pasos.png']}" alt="Flujo paso a paso">
  <figcaption>Transformación de la imagen en cada etapa del flujo.</figcaption></figure>
  <table>
    <tr><th class="n">#</th><th>Etapa</th><th>Técnica</th><th>Por qué</th></tr>
    <tr><td class="n">1</td><td>Selección de canal</td><td>Canal verde</td><td>Donde más contrastan los vasos</td></tr>
    <tr><td class="n">2</td><td>Reducción de ruido</td><td>Filtro de mediana</td><td>Quita ruido sin borrar bordes</td></tr>
    <tr><td class="n">3</td><td>Realce de contraste</td><td>CLAHE</td><td>Resalta vasos finos por zonas</td></tr>
    <tr><td class="n">4</td><td>Corrección de iluminación</td><td>Black top-hat (kernel 15)</td><td>Vasos claros sobre fondo uniforme</td></tr>
    <tr><td class="n">5</td><td>Binarización</td><td>Umbral por percentil (P90)</td><td>Mejor sensibilidad que Otsu</td></tr>
    <tr><td class="n">6</td><td>Post-proceso</td><td>Limpieza + recorte FOV</td><td>Quita ruido y borde de la retina</td></tr>
  </table>
</section>

<section>
  <h2>4. Metodología experimental (decisiones con datos)</h2>
  <h3>Estudio de ablación</h3>
  <figure><img src="{F['01_ablacion.png']}" alt="Ablación">
  <figcaption>Dice por configuración; cada técnica añadida y su aporte.</figcaption></figure>
  <table>
    <tr><th>Configuración</th><th class="n">Dice</th><th class="n">Jaccard</th></tr>
    <tr><td>1. Canal verde + Otsu</td><td class="n">0.121</td><td class="n">0.066</td></tr>
    <tr><td>2. + Mediana + CLAHE</td><td class="n">0.386</td><td class="n">0.245</td></tr>
    <tr><td><b>3. + Corrección de iluminación (top-hat)</b></td><td class="n"><b>0.643</b></td><td class="n"><b>0.480</b></td></tr>
    <tr><td>4. Frangi + Otsu</td><td class="n">0.161</td><td class="n">0.090</td></tr>
    <tr><td>5. Frangi + percentil</td><td class="n">0.551</td><td class="n">0.410</td></tr>
    <tr><td>6. Frangi + adaptativo</td><td class="n">0.355</td><td class="n">0.232</td></tr>
  </table>
  <p>👉 La corrección de iluminación es la de mayor aporte. <b>Frangi no mejora</b> en
  este dataset, por eso <b>se descartó</b> (decisión respaldada por los datos).</p>
  <h3>Refinamiento</h3>
  <p>Ajustando el kernel del top-hat y el umbral, la mejor configuración fue
  <b>kernel=15 + percentil 90 + CLAHE 2.0</b> → Dice 0.70 en el subconjunto.</p>
</section>

<section>
  <h2>5. Resultados (45 imágenes)</h2>
  <table>
    <tr><th>Métrica</th><th class="n">Dice</th><th class="n">Jaccard</th></tr>
    <tr><td>Global</td><td class="n"><b>0.716</b></td><td class="n"><b>0.560</b></td></tr>
    <tr><td>Sano</td><td class="n">0.777</td><td class="n">0.635</td></tr>
    <tr><td>Glaucoma</td><td class="n">0.707</td><td class="n">0.547</td></tr>
    <tr><td>Retinopatía diabética</td><td class="n">0.664</td><td class="n">0.498</td></tr>
  </table>
  <figure><img src="{F['04_por_categoria.png']}" alt="Por categoría"></figure>
  <figure><img src="{F['05_boxplot_dice.png']}" alt="Boxplot">
  <figcaption>Distribución del Dice por categoría (los sanos, más altos y consistentes).</figcaption></figure>
  <h3>Evolución</h3>
  <table>
    <tr><th>Etapa</th><th class="n">Dice</th><th class="n">Sensibilidad</th><th class="n">Tiempo (45)</th></tr>
    <tr><td>Baseline (Frangi+Otsu)</td><td class="n">0.22</td><td class="n">0.13</td><td class="n">316 s</td></tr>
    <tr><td>Ablación (top-hat+Otsu)</td><td class="n">0.64</td><td class="n">—</td><td class="n">—</td></tr>
    <tr><td><b>Final (refinado)</b></td><td class="n"><b>0.716</b></td><td class="n"><b>0.746</b></td><td class="n"><b>16.5 s</b></td></tr>
  </table>
</section>

<section>
  <h2>6. Análisis visual</h2>
  <figure><img src="{F['03_overlay_aciertos_errores.png']}" alt="Overlay">
  <figcaption>🟢 verde = aciertos · 🔴 rojo = falsos positivos · 🔵 azul = vasos perdidos.
  Alta precisión (poco rojo); lo que falta son los vasos más finos (azul).</figcaption></figure>
</section>

<section>
  <h2>7. Cómo ejecutar (reproducir el trabajo)</h2>
  <ol>
    <li><b>Descargar/clonar</b> el repositorio.</li>
    <li><b>Descargar el dataset HRF</b> (no viene incluido) y colocarlo en <code>data/HRF/</code>
      con esta estructura:
      <pre>data/HRF/
├─ images/    (45 fotos: 01_h.jpg, 01_dr.JPG, ...)
├─ manual1/   (ground truth: 01_h.tif, ...)
└─ mask/      (mascaras FOV: 01_h_mask.tif, ...)</pre>
      Las carpetas ya vienen creadas (vacias) en el repo; solo pega los archivos descargados.</li>
    <li><b>Instalar dependencias:</b> <code>pip install -r requirements.txt</code></li>
    <li><b>Ejecutar:</b>
      <pre>python run_baseline.py     # corre las 45 -&gt; predicted_masks/ + metricas
python experiments.py      # estudio de ablacion
python make_figures.py     # genera las figuras</pre></li>
    <li>O abre el notebook <code>notebooks/01_pipeline_HRF.ipynb</code> y ejecuta celda por celda
      (Shift+Enter) para ver el proceso paso a paso.</li>
  </ol>
</section>

<section>
  <h2>8. Componentes del proyecto</h2>
  <div class="links">
    <a href="{REPO_URL}" target="_blank">📦 Repositorio</a>
    <a href="{REPO_URL}/blob/main/notebooks/01_pipeline_HRF.ipynb" target="_blank">📓 Notebook</a>
    <a href="{REPO_URL}/tree/main/src" target="_blank">🧩 Código (src/)</a>
    <a href="{REPO_URL}/blob/main/docs/Antecedentes.md" target="_blank">📄 Antecedentes</a>
    <a href="{REPO_URL}/blob/main/docs/Metodologia_y_Resultados.md" target="_blank">📄 Metodología y Resultados</a>
    <a href="{REPO_URL}/tree/main/predicted_masks" target="_blank">🖼️ predicted_masks</a>
  </div>
</section>

</main>
<footer>Grupo 3 · Sección B — Segmentación de vasos retinales (HRF) · Técnicas determinísticas</footer>
</body></html>"""

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print("index.html generado:", (ROOT / "index.html").stat().st_size, "bytes")
