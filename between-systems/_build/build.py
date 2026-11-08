"""Generate Between Systems single-project pages (mosaic layout).

Usage: python3 -I build.py <between-systems dir>
"""
import json, math, os, random, sys, html

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SVGS = json.load(open(os.path.join(HERE, "svgs.json")))
FIG_DIR = os.path.join(HERE, "figures")
# figure shown in the right-hand column of each project page: (file, number, caption)
PROJECT_FIGS = [("01-drawing-in-air", 1, "Drawing in air"), ("03-signal", 3, "Signal"),
                ("04-spatial-cube", 4, "Spatial cube"), ("02-headset", 2, "Headset")]
def fig(i):
    f, n, cap = PROJECT_FIGS[i]
    svg = open(os.path.join(FIG_DIR, f + ".svg")).read()
    return f'{svg}<p class="doodle__cap">Fig {n}: {cap}</p>' 

PROJECTS = [
    dict(slug="01-drawing-without-a-page", no="01", title="Drawing without a page",
         area="VR Sketching", type="Longitudinal study",
         filters=["Spatial interaction", "Methods & interfaces"],
         lead="How are spatial relationships made when there is no surface to draw on?",
         short="Immersive 3D sketching examined through interaction traces, construction sequences, movement, and participants’ reflections.",
         detail="A longitudinal study of spatial drawing in immersive VR. The research follows how people establish relationships between shapes, viewpoints and body movement when sketching without a physical page or fixed construction procedure.",
         status="Illustrative study / 01. Current graphic is not a research artifact."),
    dict(slug="02-subcortical-matters", no="02", title="Subcortical Matters",
         area="Visualization", type="Collaborative work",
         filters=["Visualization", "Methods & interfaces"],
         lead="Making complex anatomical information more navigable and interpretable.",
         short="Interdisciplinary work on visual interaction with complex scientific and neuroanatomical material across immersive and screen-based contexts.",
         detail="An interdisciplinary exploration of complex neuroanatomical representations and the different demands placed on immersive and screen-based visualization, navigation, and interaction.",
         status="Illustrative study / 02. Current graphic is a conceptual illustration."),
    dict(slug="03-topovox", no="03", title="TopoVox",
         area="Interfaces", type="Experimental",
         filters=["Spatial interaction", "Visualization"],
         lead="Interfaces for seeing and exploring complex spatial data.",
         short="An exploration of visual organization, spatial navigation, and interaction with three-dimensional representations.",
         detail="Design inquiry into how interactive spatial representations may support exploration, comparison, and interpretation of complex digital material.",
         status="Conceptual / 03. Current graphic uses coordinate axes and concentric forms."),
    dict(slug="04-speculative-realities-lab", no="04", title="Speculative Realities Lab",
         area="Experiments", type="Research practice",
         filters=["Methods & interfaces"],
         lead="Prototypes, methods, and experiments at the edges of emerging interfaces.",
         short="Exploring how speculative approaches can make unfamiliar technological possibilities tangible and discussable.",
         detail="Explorations through prototypes and speculative practices to develop questions about emerging computational environments and their relationships to human experience.",
         status="Illustrative study / 04. Current graphic is illustrative imagery."),
]

def crop(svg, vb, extra=""):
    return svg.replace('viewBox="0 0 400 400"', f'viewBox="{vb}"', 1).replace("<svg ", f"<svg {extra} ", 1)

def doodle(seed):
    """One continuous closed line, drawn like a hand scribble."""
    r = random.Random(seed)
    n = 9
    pts = []
    for i in range(n):
        a = i / n * math.tau
        rad = 60 + r.random() * 40
        pts.append((100 + math.cos(a) * rad, 100 + math.sin(a) * rad))
    # inner loop
    for i in range(5):
        a = -i / 5 * math.tau + 1.2
        rad = 18 + r.random() * 22
        pts.append((100 + math.cos(a) * rad + r.uniform(-8, 8), 95 + math.sin(a) * rad))
    pts.append(pts[0])
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(1, len(pts)):
        p0 = pts[i - 1]; p1 = pts[i]
        mx = (p0[0] + p1[0]) / 2; my = (p0[1] + p1[1]) / 2
        d += f" Q{p0[0]:.1f} {p0[1]:.1f} {mx:.1f} {my:.1f}"
    return (f'<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="1.6" '
            f'stroke-linecap="round" aria-hidden="true"><path d="{d}"/></svg>')

def texture(kind, seed):
    r = random.Random(seed)
    parts = []
    if kind == "dots":
        for y in range(10, 400, 18):
            for x in range(10, 400, 18):
                d = math.hypot(x - 230, y - 180)
                rad = max(0.4, 5.5 - d / 45 + r.uniform(-.6, .6))
                parts.append(f'<circle cx="{x}" cy="{y}" r="{rad:.2f}" fill="currentColor"/>')
    elif kind == "contour":
        for k in range(1, 26):
            pts = []
            for i in range(0, 73):
                a = i / 72 * math.tau
                rad = k * 9 + 10 * math.sin(a * 3 + k * .35) + 6 * math.cos(a * 2 - k * .2)
                pts.append(f"{200 + math.cos(a) * rad:.1f},{200 + math.sin(a) * rad * .8:.1f}")
            parts.append(f'<polyline points="{" ".join(pts)}" stroke="currentColor" stroke-width=".8" fill="none" opacity="{1 - k / 30:.2f}"/>')
    elif kind == "hatch":
        for i in range(-400, 800, 7):
            wob = r.uniform(-3, 3)
            parts.append(f'<line x1="{i}" y1="0" x2="{i + 400 + wob}" y2="400" stroke="currentColor" stroke-width=".7"/>')
        parts.append('<circle cx="200" cy="200" r="120" fill="var(--layer1Color)"/>')
        for i in range(-400, 800, 7):
            parts.append(f'<line x1="{i}" y1="400" x2="{i + 400}" y2="0" stroke="currentColor" stroke-width=".5" opacity=".5" clip-path="url(#c{seed})"/>')
        parts.insert(0, f'<defs><clipPath id="c{seed}"><circle cx="200" cy="200" r="120"/></clipPath></defs>')
    elif kind == "field":
        for y in range(14, 400, 22):
            for x in range(14, 400, 22):
                a = math.sin(x * .013 + seed) * 2 + math.cos(y * .017) * 2
                dx, dy = math.cos(a) * 8, math.sin(a) * 8
                parts.append(f'<line x1="{x - dx:.1f}" y1="{y - dy:.1f}" x2="{x + dx:.1f}" y2="{y + dy:.1f}" stroke="currentColor" stroke-width=".9"/>')
    return (f'<svg viewBox="0 0 400 400" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            + "".join(parts) + "</svg>")

TEXTURES = [("contour", "dots"), ("contour", "field"), ("dots", "hatch"), ("field", "hatch")]
CROPS = ["60 60 200 200", "160 120 180 180", "110 200 160 160"]

CSS = open(os.path.join(HERE, "project.css")).read()
JS = open(os.path.join(HERE, "project.js")).read()

def esc(t):
    return html.escape(t, quote=False)

def page(i, p):
    svg = SVGS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    t1, t2 = TEXTURES[i]
    proj_nav = "".join(
        f'<a href="{q["slug"]}.html" class="sel__item{" is-active" if q is p else ""}"'
        f'{" aria-current=\"page\"" if q is p else ""} title="{esc(q["title"])}">{q["no"]}</a>'
        for q in PROJECTS)
    thumbs = "".join(
        f'<button class="thumb tile" data-view="{c}" aria-label="Show detail {k + 1}">'
        f'{crop(svg, c)}</button>'
        for k, c in enumerate(CROPS))
    spine = "".join(f"<span>{esc(x)}</span>" for x in [
        p["title"], p["area"] + " — " + p["type"], " + ".join(p["filters"]),
        "№" + p["no"], "Between Systems", "Research / Practice / Archive"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(p["title"])} | Between Systems</title>
  <meta name="description" content="{html.escape(p["short"])}" />
  <meta property="og:title" content="{html.escape(p["title"])} — Between Systems" />
  <meta property="og:description" content="{html.escape(p["lead"])}" />
  <link rel="preload" href="../fonts/UN_11ST_Regular.woff2" as="font" type="font/woff2" crossorigin />
  <style>
{CSS}
  </style>
</head>
<body class="light">
  <div class="mosaic">

    <!-- ============ Left half ============ -->
    <div class="half half--left">
      <div class="row row--top">
        <a class="logo" href="../index.html">○ Between Systems</a>
        <div class="figure" aria-hidden="true">{crop(svg, "0 0 400 400", 'class="figure__svg"')}</div>
        <div class="thumbs">{thumbs}</div>
      </div>

      <div class="spine tile" aria-label="Project specification">
        <span class="spine__cap" aria-hidden="true"></span>
        <div class="spine__label">{spine}</div>
        <span class="spine__end" aria-hidden="true"></span>
      </div>

      <div class="row row--info">
        <div class="tile tile--tall texture" aria-hidden="true">{texture(t1, i * 7 + 1)}</div>
        <div class="info">
          <section class="block">
            <h1 class="bar">{esc(p["title"])}</h1>
            <div class="block__body">
              <p>{esc(p["area"])}<br>{esc(p["type"])}<br>{esc(" + ".join(p["filters"]))}</p>
              <p class="muted">№{p["no"]} / 04 &nbsp;·&nbsp; 01 Research</p>
            </div>
          </section>
          <div class="info__pair">
            <section class="block">
              <h2 class="bar">Lead</h2>
              <div class="block__body"><p>{esc(p["lead"])}</p></div>
            </section>
            <section class="block">
              <h2 class="bar">Short description</h2>
              <div class="block__body"><p>{esc(p["short"])}</p></div>
            </section>
          </div>
        </div>
      </div>
    </div>

    <!-- ============ Right half ============ -->
    <div class="half half--right">
      <div class="row row--top">
        <div class="stage-col">
          <div class="sel">
            <div class="sel__dots" role="group" aria-label="Switch lights">
              <button class="dot dot--light" data-theme="light" aria-label="Lights on"><i></i></button>
              <button class="dot dot--dark" data-theme="dark" aria-label="Lights off"><i></i></button>
              <button class="dot dot--mood" data-theme="mood" aria-label="Mood"><i></i></button>
            </div>
            <span class="sel__label">Project</span>
            <nav class="sel__items" aria-label="Projects">{proj_nav}</nav>
          </div>
          <div class="stage tile">
            <p class="stage__caption">{esc(p["title"])} — illustrative study {p["no"]}</p>
            <div class="stage__svg" id="stage">{crop(svg, "0 0 400 400")}</div>
          </div>
        </div>
        <div class="side">
          <a class="pill" href="../index.html#research"><span>Index</span><span>0{len(PROJECTS)}</span></a>
          <figure class="doodle">{fig(i)}</figure>
          <div class="tile side__small" aria-hidden="true">{crop(svg, "140 140 120 120")}</div>
        </div>
      </div>

      <div class="row row--details">
        <div class="details">
          <section class="block">
            <h2 class="bar">About the study</h2>
            <div class="block__body"><p>{esc(p["detail"])}</p></div>
          </section>
          <section class="block">
            <h2 class="bar">Visual status</h2>
            <div class="block__body"><p class="muted">{esc(p["status"])}</p></div>
          </section>
        </div>
        <div class="tile texture texture--a" aria-hidden="true">{texture(t2, i * 7 + 2)}</div>
        <div class="tile texture texture--b" aria-hidden="true">{crop(svg, "40 40 320 320")}</div>
      </div>
    </div>
  </div>

  <!-- ============ Sticky action bar ============ -->
  <div class="dock">
    <a class="dock__bar" href="{nxt["slug"]}.html">
      <span>Next project — {esc(nxt["title"])}</span><span>№{nxt["no"]} →</span>
    </a>
    <a class="dock__back" href="../index.html#research">← All research</a>
  </div>

  <script>
{JS}
  </script>
</body>
</html>
"""

os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)
for i, p in enumerate(PROJECTS):
    path = os.path.join(OUT, "projects", p["slug"] + ".html")
    open(path, "w").write(page(i, p))
    print("wrote", path)
