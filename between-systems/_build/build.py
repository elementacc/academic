"""Generate Research / Teaching / Practice single-project pages (mosaic layout).

Usage: python3 -I build.py <between-systems dir>
"""
import json, math, os, random, sys, html

OUT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SVGS = json.load(open(os.path.join(HERE, "svgs.json")))
FIG_DIR = os.path.join(HERE, "figures")
# figure shown in the right-hand column of each project page: (file, number, caption)
PROJECT_FIGS = [("01-drawing-in-air", 1, "Drawing in air"), ("02-headset", 2, "Headset"),
                ("05-axes", 5, "Perception, action, interface")]
def fig(i):
    f, n, cap = PROJECTS[i].get("fig") or PROJECT_FIGS[i]
    svg = open(os.path.join(FIG_DIR, f + ".svg")).read()
    return f'{svg}<p class="doodle__cap">Fig {n}: {cap}</p>' 

PROJECTS = [
    dict(slug="01-vr-sketching", no="01", title="VR Sketching", svg=0,
         area="Drawing without a page", type="Longitudinal study",
         filters=["Spatial interaction", "Methods & interfaces"],
         lead="How are spatial relationships made when there is no surface to draw on?",
         short="Immersive 3D sketching examined through interaction traces, construction sequences, movement, and participants’ reflections.",
         detail="A longitudinal study of spatial drawing in immersive VR. The research follows how people establish relationships between shapes, viewpoints and body movement when sketching without a physical page or fixed construction procedure.",
         status="Illustrative study / 01. Current graphic is not a research artifact."),
    dict(slug="02-speculative-realities-lab", no="02", svg=3, title="Speculative Realities Lab",
         area="Experiments", type="Research practice",
         filters=["Methods & interfaces"],
         lead="Prototypes, methods, and experiments at the edges of emerging interfaces.",
         short="Exploring how speculative approaches can make unfamiliar technological possibilities tangible and discussable.",
         detail="Explorations through prototypes and speculative practices to develop questions about emerging computational environments and their relationships to human experience.",
         status="Illustrative study / 02. Current graphic is illustrative imagery."),
    dict(slug="03-movement-based-research", no="03", title="Movement-based research",
         area="Software research", type="Ongoing, 2023–present",
         filters=["Spatial interaction", "Methods & interfaces"],
         lead="Translating continuous movement qualities into discrete, programmable functions for an immersive drawing interface.",
         short="Most XR, CAVE and sensor-based software makes the body central as a perceiving subject, but not as an active agent: movement qualities, position and different body parts are left out of input design, which mostly relies on hand controllers.",
         detail="Body-Sketch is an ongoing system development that creates a working software application for an immersive 3D drawing interface. Users interact through a wide range of motion inputs, from subtle hand gestures to full-body interaction. This broadens input modalities and the accessibility of 3D drawing technology across fields.",
         status="Project documentation / 03. Interface screenshots, posters and reference material.",
         fig=("05-axes", 5, "Perception, action, interface"),
         media=dict(
             dir="media/movement",
             figure=("ref-laban.jpg", "Effort diagram after Rudolf Laban"),
             thumbs=[("ui-finger-drawing.png", "Body-Sketch UI: setting countdowns for finger drawing"),
                     ("dynamic-brushes.png", "Dynamic brushes: width and colour follow movement velocity"),
                     ("eye-drawing.png", "Eye drawing: gaze as a drawing cursor")],
             stage=("ui-finger-drawing.png", "Body-Sketch UI — draw with your fingers"),
             strip=("input-modalities.jpg", "Input modalities: foot, eye, full body, head, hand"),
             side=("ref-boxall.png", "L. E. Boxall, “Printing with magnetic inks”"),
             tall=("poster-concept.jpg", "Body/Sketch poster: concept and development"),
             tex_a=("poster-features.jpg", "Body/Sketch poster: features"),
             tex_b=("ref-trisha-brown.jpg", "Trisha Brown, “It’s a Draw/Live Feed” (2003)"),
         ),
         detail_blocks=[
             ("About the study", None),
             ("Objectives", "The software translates continuous movement qualities into discrete coded functions for an immersive drawing interface. Though the applied use case is drawing, the concept can be expanded to other applications."),
             ("Eye drawing — an inclusive feature", "Eye drawing introduces gaze as an input modality for immersive sketching: the system translates eye movements into a drawing cursor instead of moving controllers. This enables hands-free or hybrid workflows, reduces reliance on controllers and extends embodied interaction beyond the hand — opening tool design towards inclusivity while keeping a user-centred path at its core."),
         ],
         info_blocks=[
             ("References", "Rudolf Laban (1879–1958)<br>Trisha Brown, “It’s a Draw/Live Feed” (2003)<br>L. E. Boxall, “Printing with magnetic inks”"),
             ("Credits", "Designed and developed by students of HTW University of Applied Sciences Berlin, IKG (Informatik in Kultur und Gesundheit), 2023–2026. Concept and supervision by the author of this archive."),
         ]),
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
    M = p.get("media")
    svg = SVGS[p["svg"]] if "svg" in p else ""
    def img(key, cap=True, fit=""):
        f, alt = M[key]
        c = f'<span class="tile__cap">{esc(alt)}</span>' if cap else ""
        return f'<img src="{M["dir"]}/{f}" alt="{html.escape(alt)}" loading="lazy"{fit}>{c}' 
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    t1, t2 = TEXTURES[p.get("svg", i) % len(TEXTURES)]
    proj_nav = "".join(
        f'<a href="{q["slug"]}.html" class="sel__item{" is-active" if q is p else ""}"'
        f'{" aria-current=\"page\"" if q is p else ""} title="{esc(q["title"])}">{q["no"]}</a>'
        for q in PROJECTS)
    if M:
        thumbs = "".join(
            f'<button class="thumb tile" data-src="{M["dir"]}/{f}" data-alt="{html.escape(alt)}" aria-label="Show: {html.escape(alt)}">'
            f'<img src="{M["dir"]}/{f}" alt="" loading="lazy"></button>'
            for f, alt in M["thumbs"])
    else:
        thumbs = "".join(
            f'<button class="thumb tile" data-view="{c}" aria-label="Show detail {k + 1}">'
            f'{crop(svg, c)}</button>'
            for k, c in enumerate(CROPS))
    total = len(PROJECTS)
    if M:
        figure_html = f'<div class="figure figure--img">{img("figure", cap=False)}<p class="figure__cap">{esc(M["figure"][1])}</p></div>'
        stage_html = f'<p class="stage__caption">{esc(M["stage"][1])}</p><div class="stage__img" id="stage">{img("stage", cap=False)}</div>'
        strip_html = f'<div class="tile strip">{img("strip")}</div>'
        side_html = f'<div class="tile side__small">{img("side")}</div>'
        tall_html = f'<div class="tile tile--tall texture">{img("tall")}</div>'
        texa_html = f'<div class="tile texture texture--a">{img("tex_a")}</div>'
        texb_html = f'<div class="tile texture texture--b">{img("tex_b")}</div>'
    else:
        figure_html = f'<div class="figure" aria-hidden="true">{crop(svg, "0 0 400 400", 'class="figure__svg"')}</div>'
        stage_html = f'<p class="stage__caption">{esc(p["title"])} — illustrative study {p["no"]}</p><div class="stage__svg" id="stage">{crop(svg, "0 0 400 400")}</div>'
        strip_html = ""
        side_html = f'<div class="tile side__small" aria-hidden="true">{crop(svg, "140 140 120 120")}</div>'
        tall_html = f'<div class="tile tile--tall texture" aria-hidden="true">{texture(t1, p.get("svg", i) * 7 + 1)}</div>'
        texa_html = f'<div class="tile texture texture--a" aria-hidden="true">{texture(t2, p.get("svg", i) * 7 + 2)}</div>'
        texb_html = f'<div class="tile texture texture--b" aria-hidden="true">{crop(svg, "40 40 320 320")}</div>'
    blocks = p.get("detail_blocks") or [("About the study", None), ("Visual status", "__status__")]
    def block(h, body):
        if body is None: body = esc(p["detail"])
        elif body == "__status__": body = f'<span class="muted">{esc(p["status"])}</span>'
        return f'<section class="block"><h2 class="bar">{esc(h)}</h2><div class="block__body"><p>{body}</p></div></section>'
    details_html = "\n          ".join(block(h, b) for h, b in blocks)
    extra = p.get("info_blocks")
    info_extra = ('<div class="info__pair">' + "".join(block(h, b) for h, b in extra) + '</div>') if extra else ""
    spine = "".join(f"<span>{esc(x)}</span>" for x in [
        p["title"], p["area"] + " — " + p["type"], " + ".join(p["filters"]),
        "№" + p["no"], "Research / Teaching / Practice", "Independent research archive"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(p["title"])} | Research / Teaching / Practice</title>
  <meta name="description" content="{html.escape(p["short"])}" />
  <meta property="og:title" content="{html.escape(p["title"])} — Research / Teaching / Practice" />
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
        <a class="logo" href="../index.html">○ Research / Teaching / Practice</a>
        {figure_html}
        <div class="thumbs">{thumbs}</div>
      </div>

      <div class="spine tile" aria-label="Project specification">
        <span class="spine__cap" aria-hidden="true"></span>
        <div class="spine__label">{spine}</div>
        <span class="spine__end" aria-hidden="true"></span>
      </div>
      {strip_html}

      <div class="row row--info">
        {tall_html}
        <div class="info">
          <section class="block">
            <h1 class="bar">{esc(p["title"])}</h1>
            <div class="block__body">
              <p>{esc(p["area"])}<br>{esc(p["type"])}<br>{esc(" + ".join(p["filters"]))}</p>
              <p class="muted">№{p["no"]} / {total:02d} &nbsp;·&nbsp; 01 Research</p>
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
          {info_extra}
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
            {stage_html}
          </div>
        </div>
        <div class="side">
          <a class="pill" href="../index.html#research"><span>Index</span><span>{total:02d}</span></a>
          <figure class="doodle">{fig(i)}</figure>
          {side_html}
        </div>
      </div>

      <div class="row row--details">
        <div class="details">
          {details_html}
        </div>
        {texa_html}
        {texb_html}
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
