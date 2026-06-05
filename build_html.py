# -*- coding: utf-8 -*-
"""Genera index.html autocontenible (figuras embebidas en base64), versión
explicativa para público no técnico."""
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
body{margin:0;font-family:'Segoe UI',Roboto,Arial,sans-serif;color:var(--d);background:var(--bg);line-height:1.6}
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
.tech{background:#f0f7f6;border-left:4px solid #2a9d8f;padding:12px 16px;border-radius:6px;margin:10px 0}
.tech h4{margin:0 0 4px;color:#264653}
.note{background:#fff8e6;border-left:4px solid #e9c46a;padding:12px 16px;border-radius:6px;margin:14px 0}
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
  <h2>1. ¿De qué trata el trabajo? (en simple)</h2>
  <p>Una foto del fondo del ojo (retina) muestra una red de <b>vasos sanguíneos</b>. Los
  médicos los analizan para detectar enfermedades como retinopatía diabética, glaucoma o
  hipertensión. El primer paso —y el objetivo de este trabajo— es <b>"dibujar" solo los
  vasos</b> separándolos del resto de la imagen. A eso se le llama <b>segmentar</b>.</p>
  <p>Lo hicimos con <b>técnicas clásicas de procesamiento de imágenes</b> (no usamos
  inteligencia artificial que "aprenda"), y medimos qué tan bien quedó comparándolo con el
  dibujo hecho por un experto.</p>
  <div class="kpi">
    <div><b>0.716</b>Dice (parecido al experto)</div>
    <div><b>0.560</b>Jaccard</div>
    <div><b>45</b>imágenes</div>
    <div><b>0</b>uso de IA / ML</div>
  </div>
</section>

<section>
  <h2>2. ¿Cómo se mide si está bien? (Dice y Jaccard)</h2>
  <p>Comparamos nuestro dibujo de vasos con el del experto <b>pixel por pixel</b>. De esa
  comparación salen tres cosas:</p>
  <ul>
    <li>🟢 <b>Aciertos:</b> pixeles que ambos marcaron como vaso.</li>
    <li>🔴 <b>Falsos positivos:</b> marcamos vaso donde no había.</li>
    <li>🔵 <b>Perdidos:</b> vasos reales que se nos escaparon.</li>
  </ul>
  <p>Las dos métricas miden el <b>solapamiento</b> (qué tanto coinciden los dos dibujos) y
  van de <b>0 a 1</b> — mientras más cerca de 1, mejor:</p>
  <div class="tech"><h4>Coeficiente de Dice</h4>Mide el parecido dándole doble peso a los
  aciertos. Es la métrica principal del trabajo.</div>
  <div class="tech"><h4>Índice de Jaccard (IoU)</h4>La parte que coincide dividida entre todo
  lo marcado por ambos. Siempre sale un poco menor que el Dice, pero "sube y baja" con él.</div>
  <div class="note">💡 En palabras simples: un Dice de <b>0.72</b> significa que nuestro dibujo
  de vasos <b>se parece bastante</b> al del experto. Si fuera 1.0, sería idéntico.</div>
</section>

<section>
  <h2>3. El dataset HRF</h2>
  <p>Base pública de la Universidad FAU (Alemania): <b>45 imágenes</b> (15 de ojos sanos, 15
  con retinopatía diabética y 15 con glaucoma). Cada una trae la foto, el <i>ground truth</i>
  (el dibujo correcto de los vasos, hecho a mano) y la máscara FOV (el círculo válido de la retina).</p>
  <div class="links">
    <a href="{FAU_URL}" target="_blank">⬇️ Descarga oficial (FAU)</a>
    <a href="{DRIVE_HRF}" target="_blank">⬇️ Carpeta del curso (Google Drive)</a>
  </div>
  <p style="color:var(--mut);font-size:.85rem">El dataset no se incluye en el repositorio (es
  público y pesado); usa los enlaces de descarga.</p>
</section>

<section>
  <h2>4. El flujo paso a paso: ¿qué hace cada técnica?</h2>
  <figure><img src="{F['02_flujo_pasos.png']}" alt="Flujo paso a paso">
  <figcaption>La misma imagen transformándose en cada etapa, hasta quedar solo los vasos.</figcaption></figure>
  <div class="tech"><h4>1. Canal verde</h4>Una foto a color tiene 3 capas: roja, verde y azul.
  Usamos <b>solo la verde</b> porque es donde los vasos se ven más nítidos; en la roja casi no
  se distinguen y en la azul hay mucho ruido.</div>
  <div class="tech"><h4>2. Filtro de mediana</h4>Quita el "granito"/ruido de la foto
  (reemplaza cada punto por el valor del medio de sus vecinos) <b>sin difuminar</b> los bordes
  de los vasos.</div>
  <div class="tech"><h4>3. CLAHE (realce de contraste)</h4>Sube el contraste <b>por zonas
  pequeñas</b>: hace que los vasos finos resalten del fondo, sin "quemar" la imagen.</div>
  <div class="tech"><h4>4. Corrección de iluminación / top-hat — ⭐ la clave</h4>La retina sale
  más iluminada en el centro y el disco óptico brilla mucho. Esta técnica <b>aplana la
  iluminación</b> y deja los vasos como <b>líneas claras sobre un fondo negro uniforme</b>.
  Fue la técnica que <b>más mejoró</b> el resultado.</div>
  <div class="tech"><h4>5. Umbral por percentil</h4>Hay que decidir, pixel por pixel, si es
  vaso o no. Marcamos como vaso el <b>~10% más brillante</b> del realce anterior. Es como poner
  una "línea de corte" que separa los vasos del fondo.</div>
  <div class="tech"><h4>6. Limpieza + recorte (FOV)</h4>Borramos manchitas sueltas (ruido que
  sobró) y recortamos al círculo de la retina, ignorando el borde negro.</div>
</section>

<section>
  <h2>5. ¿Por qué elegimos estas técnicas? (análisis con datos)</h2>
  <p>No elegimos las técnicas "por costumbre": las probamos <b>una por una</b>, midiendo el
  Dice cada vez, para ver cuánto aporta cada una. Eso se llama <b>estudio de ablación</b>.</p>
  <figure><img src="{F['01_ablacion.png']}" alt="Ablación">
  <figcaption>Dice de cada configuración (en verde, la ganadora).</figcaption></figure>
  <table>
    <tr><th>Configuración</th><th class="n">Dice</th><th class="n">Jaccard</th></tr>
    <tr><td>1. Solo canal verde + umbral</td><td class="n">0.121</td><td class="n">0.066</td></tr>
    <tr><td>2. + Mediana + CLAHE</td><td class="n">0.386</td><td class="n">0.245</td></tr>
    <tr><td><b>3. + Corrección de iluminación (top-hat)</b></td><td class="n"><b>0.643</b></td><td class="n"><b>0.480</b></td></tr>
    <tr><td>4. Frangi + Otsu</td><td class="n">0.161</td><td class="n">0.090</td></tr>
    <tr><td>5. Frangi + percentil</td><td class="n">0.551</td><td class="n">0.410</td></tr>
    <tr><td>6. Frangi + adaptativo</td><td class="n">0.355</td><td class="n">0.232</td></tr>
  </table>
  <div class="note">💡 <b>Análisis de la tabla:</b>
    <ul>
      <li>Con <b>solo el canal verde</b> apenas detectamos vasos (Dice 0.12): insuficiente.</li>
      <li>Al añadir <b>contraste (CLAHE)</b> ya <b>triplicamos</b> (0.39).</li>
      <li>La <b>corrección de iluminación</b> da el <b>mayor salto</b> (0.64): es la técnica estrella.</li>
      <li><b>Frangi</b> (un detector de "tubos" muy famoso) en vez de ayudar, <b>empeora</b>
      (0.16–0.55). Por eso lo <b>descartamos</b>. Tomar esta decisión con datos —y no porque sea
      una técnica popular— es parte del valor del trabajo.</li>
    </ul>
  </div>
  <h3>Ajuste fino (refinamiento)</h3>
  <p>Después afinamos dos "perillas": el <b>tamaño</b> del top-hat y el punto de corte del
  umbral. El mejor ajuste subió el Dice de <b>0.64 a 0.70</b>. También probamos la
  <b>resolución completa</b>: <b>no mejoró</b> (mismo Dice) y era 4× más lenta, así que
  mantuvimos media resolución.</p>
</section>

<section>
  <h2>6. Resultados y análisis (45 imágenes)</h2>
  <table>
    <tr><th>Grupo</th><th class="n">Dice</th><th class="n">Jaccard</th></tr>
    <tr><td><b>Global (las 45)</b></td><td class="n"><b>0.716</b></td><td class="n"><b>0.560</b></td></tr>
    <tr><td>Ojos sanos</td><td class="n">0.777</td><td class="n">0.635</td></tr>
    <tr><td>Glaucoma</td><td class="n">0.707</td><td class="n">0.547</td></tr>
    <tr><td>Retinopatía diabética</td><td class="n">0.664</td><td class="n">0.498</td></tr>
  </table>
  <figure><img src="{F['04_por_categoria.png']}" alt="Por categoría"></figure>
  <figure><img src="{F['05_boxplot_dice.png']}" alt="Boxplot">
  <figcaption>Distribución del Dice por grupo (cada caja muestra el rango de resultados).</figcaption></figure>
  <div class="note">💡 <b>Análisis por tipo de imagen:</b>
    <ul>
      <li><b>Sanos (0.78):</b> los mejores — no hay lesiones que confundan al método.</li>
      <li><b>Glaucoma (0.71):</b> intermedio.</li>
      <li><b>Retinopatía diabética (0.66):</b> los más difíciles, porque tienen <b>lesiones</b>
      (manchas claras y oscuras) que el método a veces confunde con vasos.</li>
    </ul>
    El boxplot muestra que los resultados son <b>consistentes</b> (poca variación), sobre todo
    en los ojos sanos.
  </div>
  <h3>La mejora lograda</h3>
  <table>
    <tr><th>Etapa</th><th class="n">Dice</th><th class="n">Sensibilidad</th><th class="n">Tiempo (45)</th></tr>
    <tr><td>Punto de partida (con Frangi)</td><td class="n">0.22</td><td class="n">0.13</td><td class="n">316 s</td></tr>
    <tr><td>Tras la ablación (con top-hat)</td><td class="n">0.64</td><td class="n">—</td><td class="n">—</td></tr>
    <tr><td><b>Versión final (ajustada)</b></td><td class="n"><b>0.716</b></td><td class="n"><b>0.746</b></td><td class="n"><b>16.5 s</b></td></tr>
  </table>
  <div class="note">💡 <b>¿Qué tanto mejoramos?</b> Pasamos de 0.22 a <b>0.716</b> (más del
  <b>triple</b>). La "sensibilidad" (cuántos vasos reales detectamos) subió de 13% a <b>75%</b>
  (casi 6 veces). Y como quitamos Frangi, el método es <b>20× más rápido</b>.</div>
</section>

<section>
  <h2>7. Análisis visual: ¿dónde acierta y dónde falla?</h2>
  <figure><img src="{F['03_overlay_aciertos_errores.png']}" alt="Overlay">
  <figcaption>Izquierda: foto original · Centro: dibujo del experto · Derecha: comparación a color.</figcaption></figure>
  <div class="note">💡 <b>Cómo leer la imagen de la derecha:</b>
    🟢 <b>verde</b> = acertamos · 🔴 <b>rojo</b> = marcamos de más · 🔵 <b>azul</b> = se nos escapó.
    <br><br>Hay <b>mucho verde y muy poco rojo</b> → el método es <b>preciso</b> (casi no inventa
    vasos). El <b>azul</b> aparece en los vasos <b>más finos</b> de la periferia → eso es lo que
    todavía se nos escapa, y sería la mejora a futuro.</div>
</section>

<section>
  <h2>8. Cómo ejecutar (reproducir el trabajo)</h2>
  <ol>
    <li><b>Descargar/clonar</b> el repositorio.</li>
    <li><b>Descargar el dataset HRF</b> (no viene incluido) y colocarlo en <code>data/HRF/</code>:
      <pre>data/HRF/
- images/    (45 fotos: 01_h.jpg, 01_dr.JPG, ...)
- manual1/   (ground truth: 01_h.tif, ...)
- mask/      (mascaras FOV: 01_h_mask.tif, ...)</pre>
      Las carpetas ya vienen creadas (vacías) en el repo; solo pega los archivos descargados.</li>
    <li><b>Instalar dependencias:</b> <code>pip install -r requirements.txt</code></li>
    <li><b>Ejecutar:</b>
      <pre>python run_baseline.py     # corre las 45 -&gt; predicted_masks/ + metricas
python experiments.py      # estudio de ablacion
python make_figures.py     # genera las figuras</pre></li>
    <li>O abre el notebook <code>notebooks/01_pipeline_HRF.ipynb</code> y ejecútalo celda por
      celda (Shift+Enter) para ver el proceso paso a paso.</li>
  </ol>
</section>

<section>
  <h2>9. Componentes del proyecto</h2>
  <div class="links">
    <a href="{REPO_URL}" target="_blank">📦 Repositorio</a>
    <a href="{REPO_URL}/blob/main/notebooks/01_pipeline_HRF.ipynb" target="_blank">📓 Notebook</a>
    <a href="{REPO_URL}/tree/main/src" target="_blank">🧩 Código (src/)</a>
    <a href="{REPO_URL}/blob/main/docs/Antecedentes.md" target="_blank">📄 Antecedentes</a>
    <a href="{REPO_URL}/blob/main/docs/Metodologia_y_Resultados.md" target="_blank">📄 Metodología y Resultados</a>
    <a href="{REPO_URL}/tree/main/predicted_masks" target="_blank">🖼️ predicted_masks</a>
  </div>
</section>

<section>
  <h2>10. Conclusiones</h2>
  <ul>
    <li>La mejor solución determinística fue <b>realce morfológico (top-hat) + umbral por
    percentil</b>: <b>Dice 0.716 / Jaccard 0.560</b>.</li>
    <li><b>Cada decisión se tomó con datos</b> (ablación y refinamiento), no por intuición.</li>
    <li>Descartamos <b>Frangi</b> y la <b>resolución completa</b> porque la evidencia mostró que
    no aportaban.</li>
    <li>Lo que falta mejorar: los <b>vasos más finos</b> (visibles en azul en el análisis visual).</li>
  </ul>
</section>

</main>
<footer>Grupo 3 · Sección B — Segmentación de vasos retinales (HRF) · Técnicas determinísticas</footer>
</body></html>"""

(ROOT / "index.html").write_text(HTML, encoding="utf-8")
print("index.html generado:", (ROOT / "index.html").stat().st_size, "bytes")
