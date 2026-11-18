"""Shared page frame (header, big title, footer) for project, Bio and Reflections pages."""

POSITION = ('<dl><dt>Artist</dt><dd></dd><dt>Lecturer</dt><dd>HTW Berlin</dd>'
            '<dt>Researcher, HCI</dt><dd>Speculative Realities Lab, Charité and Cluster of Excellence »Matters of Activity. Image Space Material«</dd>'
            '<dt>Ph.D. candidate</dt><dd>TU Berlin</dd></dl>')

def header(root):
    return f'''<header class="sh" id="top">
    <div class="sh__col sh__logo"><a href="{root}index.html">Paulina Greta Stefanovic</a></div>
    <div class="sh__col sh__intro"><p class="sh__label">Intro</p><p>Interaction / Embodied Cognition / Computational environments</p></div>
    <div class="sh__col sh__pos"><p class="sh__label">Position</p>
      {POSITION}
      <p class="sh__bio"><a href="{root}bio.html">Bio →</a><br><a href="{root}reflections.html">Reflections →</a></p></div>
  </header>'''

def title(root, n, word, href, sub=""):
    s = f'<p class="sw__proj">{sub}</p>' if sub else ""
    return f'<div class="sw"><h1><a href="{root}{href}"><span class="sw__n">({n})</span>{word}</a></h1>{s}</div>'

def footer():
    return '''<footer class="sf">
    <div class="sf__graphic"><svg viewBox="0 0 72 72" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="26" cy="36" r="20"/><circle cx="46" cy="36" r="20"/></svg></div>
    <div class="sf__about"><p class="sh__label">Contact</p><p>Open to interdisciplinary research conversations, evaluations and experimental collaborations.</p></div>
    <div class="sf__copy"><p>2026</p></div>
    <a class="sf__top" href="#top" aria-label="Back to top">↑</a>
  </footer>'''

CSS = '''
    .sh, .sw, .sf { --fr-ink: #202020; --fr-2: #767676; --fr-3: #b3b3b3; --fr-line: #ededed; --fr-gap: 8px;
      font-family: "UN_11ST_Regular", "Helvetica Neue", Arial, sans-serif; color: var(--fr-ink); }
    .sh { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: var(--fr-gap); padding: 13px var(--fr-gap) 12px; border-bottom: 1px solid var(--fr-line); font-size: 14px; line-height: 1.15; row-gap: 14px; }
    .sh p, .sh dl, .sh dd, .sf p { margin: 0; }
    .sh a, .sf a { color: inherit; text-decoration: none; }
    .sh__label { font-size: 10px; line-height: 1.6; text-transform: uppercase; color: var(--fr-3); }
    .sh__logo { grid-column: 1 / -1; font-size: 10px; line-height: 1.6; text-transform: uppercase; color: var(--fr-3); }
    .sh__intro, .sh__pos { grid-column: 1 / -1; }
    .sh__pos dl { display: grid; grid-template-columns: auto 1fr; column-gap: .9em; }
    .sh__pos dt { white-space: nowrap; } .sh__pos dd { color: var(--fr-2); }
    .sh__bio { margin-top: .6rem !important; } .sh__bio a { text-decoration: underline; text-underline-offset: .2em; }
    @media (min-width: 1024px) { .sh__logo { grid-column: 1 / span 2; } .sh__intro { grid-column: 3 / span 4; } .sh__pos { grid-column: 7 / span 6; } }
    .sw { padding: 18px var(--fr-gap) 0; }
    .sw h1 { margin: 0; font-family: "Helvetica Now Display", "Neue Haas Grotesk Display Pro", "Helvetica Neue", Helvetica, Arial, sans-serif; font-weight: 400;
      font-size: clamp(2.6rem, 6.9vw, 12rem); line-height: .86; letter-spacing: -.045em; margin-left: -.04em; padding: .06em 0 .2em; border-bottom: 1px solid var(--fr-ink); }
    .sw h1 a { color: inherit; text-decoration: none; }
    .sw__n { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace; font-size: .26em; letter-spacing: .3em; vertical-align: 2.3em; margin-right: .3em; }
    .sw__proj { font-size: 1.375rem; line-height: 1.15; letter-spacing: -.01em; padding: 14px 0 6px; margin: 0; }
    .sf { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: var(--fr-gap); padding: 14px var(--fr-gap) 90px; margin-top: 120px; border-top: 1px solid var(--fr-line); font-size: 14px; line-height: 1.15; position: relative; }
    .sf__graphic { grid-column: 1 / span 2; } .sf__graphic svg { width: 4.5rem; height: auto; }
    .sf__about { grid-column: 3 / span 4; } .sf__copy { grid-column: 10 / span 2; }
    .sf__top { position: absolute; right: var(--fr-gap); top: 14px; }
    @media (max-width: 1023px) { .sf__graphic { grid-column: 1 / -1; margin-bottom: 12px; } .sf__about { grid-column: 1 / span 8; } .sf__copy { grid-column: 9 / span 3; } }
'''
