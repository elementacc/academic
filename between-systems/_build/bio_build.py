"""Build bio.html (Opal-style spec list). Usage: python3 -I _build/bio_build.py <between-systems dir>"""
import os, sys, re
OUT = sys.argv[1]
LINE = os.path.join(OUT, "figures", "line")
def drawing(name):
    s = open(os.path.join(LINE, name + "-black.svg")).read()
    s = s.replace(' xmlns="http://www.w3.org/2000/svg"', "").replace('stroke="#111111"', 'stroke="currentColor"')
    return s.replace("<svg ", '<svg aria-hidden="true" ', 1)

ROWS = [
  dict(title="Profile", draw="01-headset",
       a=("Position", [("Artist", ""), ("Lecturer", "HTW Berlin"), ("Researcher, HCI", "Speculative Realities Lab"), ("Ph.D. candidate", "TU Berlin")]),
       b=("Based in", "Berlin, Germany"),
       text="I study how interactive technologies shape the ways we perceive, think and move. My starting point is the body: perception, cognition and action form one continuous way of meeting the world, and every interface intervenes in that loop. Trained in psychology and interaction design, I work between first-person inquiry and empirical study, and I build the interfaces I study. My doctoral research follows how people learn to draw in immersive space, without a page to lean on, and how they form spatial references through their own movement. With clinicians, designers and data scientists I develop navigational interfaces for complex neurosurgical imaging, where what an interface makes visible changes what can be understood. Alongside research I teach, run practice-based workshops and make creative technology projects. Increasingly I ask how systems that take part in thinking and making, AI among them, change the conditions under which we perceive, reason and come to know."),
  dict(title="Focus", draw="06-motion-figure",
       a=("Fields", [("Embodied cognition", ""), ("Immersive sketching", ""), ("Scientific visualization", ""), ("Non-normative interfaces", "")]),
       b=("Methods", "Phenomenologically informed inquiry, longitudinal studies, bodystorming, experimental interfaces"),
       text="I explore the relationship between technology, art, design, space and human perception, both in theory and in practice. My focus is on immersive and movement-based interfaces, and on interaction design that questions assumptions about perception, cognition and bodily ability."),
  dict(title="Practice", draw="05-gaze-drawing",
       a=("Ongoing reflection", [("Dialogues", "")]),
       b=("Through", "Senses, interactive objects, environments"),
       text="An ongoing reflection upon “Dialogues” as conversations embracing senses, interactive objects and environments. An intent of reasoning and creating different types of dialogues, in various declinations and forms. Confronting constraints and opening channels. <a href=\"reflections.html\">Read the reflections</a>"),
  dict(title="Exhibitions", draw="04-stylus-in-air",
       a=("Selected", [("2025", "<a href=\"https://dst-tud.de/new-science-exhibition-at-cosmo-invisible-how-data-visualization-helps-us-understand-the-world/\" target=\"_blank\" rel=\"noopener\">TU Dresden, [in]visible, COSMO Dresden ↗</a>"), ("2025", "<a href=\"https://www.soiree-xd.com/\" target=\"_blank\" rel=\"noopener\">Already Possible by Soirée XD &amp; masumi, Berlin ↗</a>"), ("2024", "<a href=\"https://pq.cz/symposium-technologies/researching-embodied-interactions/\" target=\"_blank\" rel=\"noopener\">Prague Quadrennial symposium: Researching Embodied Interactions, Prague ↗</a>")]),
       b=("Venues", "International venues and multimedia festivals"),
       text="My work has been shown at international venues and multimedia festivals."),
  dict(title="Teaching", draw="02-controller",
       a=("Courses", [("Natural User Interfaces", "HTW Berlin, current"), ("Technological Arts", "European academies")]),
       b=("Role", "Lecturer"),
       text="I have taught Technological Arts at several European academies. At present I teach the “Natural User Interfaces” course at HTW Berlin."),
  dict(title="Research lab", draw="03-depth-sensor",
       a=("Speculative Realities Lab", [("Since", "2023"), ("Neurosurgery", ""), ("Anthropology", ""), ("Immersive arts", "")]),
       b=("Collaboration", "Charité and the Cluster of Excellence »Matters of Activity. Image Space Material«"),
       text="Since 2023 I have been a researcher at the Speculative Realities Lab, a space connecting neurosurgery, anthropology and the immersive arts, run by Charité with the Cluster of Excellence »Matters of Activity. Image Space Material«."),
  dict(title="Education", draw="06-motion-figure",
       a=("Degrees", [("Ph.D., Human–Computer Interaction", "TU Berlin, expected 2027"), ("MSc, Psychology of Communication", "Sapienza University of Rome, 2015"), ("BA/BFA, Video Direction and Non-Linear Installation Arts", "IED Milan, 2013")]),
       b=("Doctoral topic", "Spatial reference formation in immersive 3D sketching"),
       text="My MSc thesis examined the sense of agency in gesture-controlled interactive storytelling through a phenomenological approach. My doctoral research continues that thread with a longitudinal study of drawing in immersive space."),
  dict(title="Publication", draw="05-gaze-drawing",
       a=("Chapter", [("“The Navigational Technè: From Static Frames to Perpetual Motion”", "")]),
       b=("In", "Matters of Activity: Rethinking Materiality, Rethinking Knowledge"),
       text="My chapter “The Navigational Technè: From Static Frames to Perpetual Motion” appears in the volume <em>Matters of Activity: Rethinking Materiality, Rethinking Knowledge</em>."),
]

def row(i, r):
    n = f"{i+1:02d}"
    open_ = i == 0
    kv = "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in r["a"][1])
    return f'''
      <li class="spec{' is-open' if open_ else ''}">
        <button class="spec__row" aria-expanded="{'true' if open_ else 'false'}" aria-controls="spec-{n}">
          <span class="spec__num">{n}</span><span class="spec__title">{r["title"]}</span>
          <span class="spec__icon" aria-hidden="true"></span>
        </button>
        <div class="spec__panel" id="spec-{n}"><div><div class="spec__inner">
          <div class="spec__a"><p class="spec__label">{r["a"][0]}</p><dl class="spec__kv">{kv}</dl></div>
          <div class="spec__b"><p class="spec__label">{r["b"][0]}</p><p class="muted">{r["b"][1]}</p></div>
          <p class="spec__text">{r["text"]}</p>
          <figure class="spec__draw">{drawing(r["draw"])}</figure>
        </div></div></div>
      </li>'''

N = len(ROWS)
HTML = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Bio | Research / Teaching / Practice</title>
  <meta name="description" content="Bio — artist and HCI researcher working on immersive and movement-based interfaces." />
  <link rel="preload" href="fonts/UN_11ST_Regular.woff2" as="font" type="font/woff2" crossorigin />
  <style>
    @font-face {{ font-family: UN_11ST_Regular; src: url(fonts/UN_11ST_Regular.woff2) format("woff2"), url(fonts/UN_11ST_Regular.woff) format("woff"); font-display: swap; }}
    *, *::before, *::after {{ box-sizing: border-box; }} * {{ margin: 0; }}
    ul, ol {{ list-style: none; padding: 0; }} button {{ font: inherit; color: inherit; }} svg {{ display: block; }}
    body, body.light {{ --bg: #ffffff; --fg: #202020; --fg2: #767676; --fg3: #b3b3b3; --line: #e6e6e6; --pillBg: #202020; --pillFg: #fff; }}
    body.dark {{ --bg: #141414; --fg: #f2f2f2; --fg2: #9a9a9a; --fg3: #5c5c5c; --line: #2c2c2c; --pillBg: #f2f2f2; --pillFg: #141414; }}
    body.mood {{ --bg: #f5f0fe; --fg: #342d42; --fg2: rgba(52,45,66,.75); --fg3: rgba(52,45,66,.45); --line: #e2d8fb; --pillBg: #342d42; --pillFg: #f5f0fe; }}
    html {{ background: var(--bg, #141414); }}
    body {{
      background: var(--bg); color: var(--fg);
      font-family: "UN_11ST_Regular", "Helvetica Neue", Arial, sans-serif; font-feature-settings: "ss01" on;
      font-size: 14px; line-height: 1.3; -webkit-font-smoothing: antialiased;
      transition: background-color .4s, color .4s; overflow-x: hidden;
    }}
    a {{ color: inherit; text-decoration: none; }} a:hover {{ color: var(--fg2); }}
    :focus-visible {{ outline: 1px solid var(--fg2); outline-offset: 3px; }}
    .muted {{ color: var(--fg2); }}
    .wrap {{ padding: 0 16px; }}
    .g {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); column-gap: 16px; }}
    @media (min-width: 900px) {{ .g {{ grid-template-columns: repeat(12, minmax(0, 1fr)); }} }}

    /* header */
    .top {{ padding: 14px 0 64px; align-items: start; border-bottom: 1px solid var(--line); }}
    .logo {{ grid-column: 1 / -1; font-size: 16px; letter-spacing: -.01em; white-space: nowrap; margin-bottom: 12px; }}
    .top__meta {{ display: none; font-size: 12px; }}
    .top__meta p {{ display: flex; align-items: center; gap: 6px; }}
    .bullet {{ width: 9px; height: 9px; border-radius: 50%; background: var(--fg3); display: inline-block; }}
    .top__pill {{ grid-column: 1 / span 3; justify-self: start; white-space: nowrap; background: var(--pillBg); color: var(--pillFg); border-radius: 999px; padding: 5px 16px; font-size: 12px; }}
    .top__pill:hover {{ color: var(--pillFg); opacity: .85; }}
    .lights {{ grid-column: 4 / span 1; justify-self: end; display: flex; gap: 6px; }}
    .lights button {{ width: 18px; height: 18px; border-radius: 50%; border: 1px solid var(--fg3); padding: 0; cursor: pointer; background: transparent; }}
    .lights [data-theme=light] {{ background: #fff; }} .lights [data-theme=dark] {{ background: #141414; }} .lights [data-theme=mood] {{ background: #ebe3fd; }}
    .lights button[aria-pressed=true] {{ outline: 1px solid var(--fg); outline-offset: 2px; }}
    @media (min-width: 900px) {{
      .top__meta {{ display: block; }}
      .logo {{ grid-column: 1 / span 3; margin-bottom: 0; }}
      .top__meta--a {{ grid-column: 4 / span 2; }} .top__meta--b {{ grid-column: 6 / span 3; }}
      .top__pill {{ grid-column: 9 / span 2; }} .lights {{ grid-column: 12 / span 1; }}
    }}

    /* title */
    .head {{ padding: 16px 0 120px; align-items: start; }}
    .head h1 {{ grid-column: 1 / span 3; font-size: clamp(36px, 4.4vw, 64px); line-height: 1; letter-spacing: -.02em; font-weight: 400; }}
    .head__count {{ grid-column: 4 / span 1; justify-self: end; font-size: 12px; text-align: right; }}
    .head__code {{ color: var(--fg3); }}
    .head__count span {{ display: block; }}
    @media (min-width: 900px) {{
      .head {{ padding-bottom: 180px; }}
      .head h1 {{ grid-column: 1 / span 6; }} .head__count {{ grid-column: 9 / span 2; justify-self: start; text-align: left; display: contents; }}
      .head__count span:first-child {{ grid-column: 9 / span 2; }} .head__code {{ grid-column: 11 / span 2; }}
    }}

    /* spec list */
    .specs {{ border-top: 1px solid var(--line); }}
    .spec {{ border-bottom: 1px solid var(--line); }}
    .spec__row {{
      width: 100%; background: none; border: 0; padding: 12px 0; cursor: pointer; text-align: left;
      display: grid; grid-template-columns: 3rem minmax(0, 1fr) 20px; column-gap: 16px; align-items: center; font-size: 15px;
    }}
    @media (min-width: 900px) {{ .spec__row {{ grid-template-columns: repeat(12, minmax(0, 1fr)); }} .spec__num {{ grid-column: 1; }} .spec__title {{ grid-column: 2 / span 4; }} .spec__icon {{ grid-column: 12; justify-self: end; }} }}
    .spec__row:hover .spec__title {{ color: var(--fg2); }}
    .spec__icon {{ position: relative; width: 18px; height: 18px; border-radius: 50%; background: var(--fg3); transition: background-color .3s; }}
    .spec.is-open .spec__icon {{ background: var(--fg); }}
    .spec__icon::before, .spec__icon::after {{ content: ""; position: absolute; left: 5px; right: 5px; top: 50%; height: 1.4px; margin-top: -.7px; background: var(--bg); transition: transform .3s; }}
    .spec__icon::after {{ transform: rotate(90deg); }}
    .spec.is-open .spec__icon::after {{ transform: rotate(0); }}
    .spec__panel {{ display: grid; grid-template-rows: 0fr; transition: grid-template-rows .5s cubic-bezier(.65,0,.35,1); }}
    .spec.is-open .spec__panel {{ grid-template-rows: 1fr; }}
    .spec__panel > div {{ overflow: hidden; }}
    .spec__inner {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); column-gap: 16px; row-gap: 18px; padding: 4px 0 28px; font-size: 12px; }}
    .spec__a {{ grid-column: 1 / span 2; }} .spec__b {{ grid-column: 3 / span 2; }}
    .spec__text {{ grid-column: 1 / -1; font-size: 14px; max-width: 52ch; }}
    .spec__draw {{ grid-column: 1 / -1; margin: 0; max-width: 300px; color: var(--fg); }}
    .spec__draw svg {{ width: 100%; height: auto; }}
    .spec__label {{ margin-bottom: 4px; }}
    .spec__kv {{ display: grid; grid-template-columns: auto 1fr; column-gap: 14px; color: var(--fg2); }}
    .spec__inner a {{ text-decoration: underline; text-underline-offset: .2em; }}
    .spec__kv dt {{ color: var(--fg2); }} .spec__kv dd {{ margin: 0; color: var(--fg3); }}
    @media (min-width: 900px) {{
      .spec__inner {{ grid-template-columns: repeat(12, minmax(0, 1fr)); }}
      .spec__a {{ grid-column: 7 / span 3; grid-row: 1; }} .spec__b {{ grid-column: 10 / span 2; grid-row: 1; }}
      .spec__text {{ grid-column: 2 / span 4; grid-row: 1; }}
      .spec__draw {{ grid-column: 7 / span 4; grid-row: 2; max-width: 380px; }}
      .spec__inner {{ padding-bottom: 36px; }}

    }}

    /* footer */
    .foot {{ padding: 20px 0 16px; font-size: 15px; }}
    .foot__block {{ row-gap: 6px; margin-bottom: 26px; }}
    .foot__label {{ grid-column: 1 / span 2; color: var(--fg2); }}
    .foot__val {{ grid-column: 3 / span 2; }}
    .foot__val a {{ display: block; }}
    @media (min-width: 900px) {{ .foot__label {{ grid-column: 1 / span 2; }} .foot__val {{ grid-column: 7 / span 4; }} .foot__val--mid {{ grid-column: 3 / span 4; }} }}
    .foot__base {{ border-top: 1px solid var(--line); padding-top: 14px; margin-top: 120px; }}
    .foot__base p:nth-child(1) {{ grid-column: 1 / span 2; }} .foot__base p:nth-child(2) {{ grid-column: 3 / span 1; }} .foot__base p:nth-child(3) {{ grid-column: 1 / -1; color: var(--fg2); margin-top: 6px; }}
    @media (min-width: 900px) {{ .foot__base p:nth-child(2) {{ grid-column: 7 / span 3; }} .foot__base p:nth-child(3) {{ grid-column: 10 / span 3; margin-top: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .spec__panel, .spec__icon::after {{ transition: none; }} }}
  </style>
</head>
<body class="dark">
  <div class="wrap">
    <header class="top g">
      <a class="logo" href="index.html">Research / Teaching / Practice</a>
      <div class="top__meta top__meta--a"><p>Bio</p><p class="muted">Research practice</p></div>
      <div class="top__meta top__meta--b"><p><span class="bullet"></span>Berlin</p><p><span class="bullet"></span>HCI · Immersive arts</p></div>
      <a class="top__pill" href="index.html#research">Selected work</a>
      <div class="lights" role="group" aria-label="Switch lights">
        <button data-theme="light" aria-label="Lights on"></button><button data-theme="dark" aria-label="Lights off"></button><button data-theme="mood" aria-label="Mood"></button>
      </div>
    </header>

    <section class="head g">
      <h1>Bio &amp;<br>Practice</h1>
      <p class="head__count"><span>01→{N:02d}</span><span class="head__code">RTP-BIO</span></p>
    </section>

    <ol class="specs">{"".join(row(i, r) for i, r in enumerate(ROWS))}
    </ol>

    <footer class="foot">
      <div class="g foot__block" style="margin-top:16px">
        <p class="foot__label">Based in</p><p class="foot__val foot__val--mid">Berlin<br>Germany</p>
      </div>
      <div class="g foot__block" style="margin-top:60px">
        <p class="foot__label">Contact</p><p class="foot__val foot__val--mid muted">Contact details to be added before publication.</p>
      </div>
      <div class="g foot__block">
        <p class="foot__label">Index</p>
        <p class="foot__val foot__val--mid"><a href="index.html#research">Research</a><a href="index.html#about">About</a><a href="index.html#students">Teaching</a><a href="reflections.html">Reflections</a></p>
      </div>
      <div class="g foot__base"><p>Research / Teaching / Practice</p><p>© 2026</p><p>An independent research archive</p></div>
    </footer>
  </div>
  <script>
    (function () {{
      var b = document.body, btns = document.querySelectorAll('[data-theme]');
      function set(t) {{
        b.classList.remove('light', 'dark', 'mood'); b.classList.add(t);
        btns.forEach(function (x) {{ x.setAttribute('aria-pressed', x.getAttribute('data-theme') === t ? 'true' : 'false'); }});
        try {{ localStorage.setItem('bs-lights', t); }} catch (e) {{}}
      }}
      var s = null; try {{ s = localStorage.getItem('bs-lights'); }} catch (e) {{}}
      set(s === 'light' || s === 'mood' || s === 'dark' ? s : 'dark');
      btns.forEach(function (x) {{ x.addEventListener('click', function () {{ set(x.getAttribute('data-theme')); }}); }});
      document.querySelectorAll('.spec__row').forEach(function (r) {{
        r.addEventListener('click', function () {{
          var it = r.closest('.spec'), open = !it.classList.contains('is-open');
          it.classList.toggle('is-open', open); r.setAttribute('aria-expanded', open ? 'true' : 'false');
        }});
      }});
    }})();
  </script>
</body>
</html>
'''
open(os.path.join(OUT, "bio.html"), "w").write(HTML)
print("wrote bio.html")
