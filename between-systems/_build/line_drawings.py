import math, os
C30, S30 = math.cos(math.pi/6), 0.5
ACC = "#ff5a1f"
class D:
    def __init__(s, cx=200, cy=210, k=1.0):
        s.cx, s.cy, s.k, s.out = cx, cy, k, []
    def P(s, x, y, z):
        return (s.cx + (x - y) * C30 * s.k, s.cy + (x + y) * S30 * s.k - z * s.k)
    def line(s, a, b, **kw): s.poly([a, b], **kw)
    def poly(s, pts, close=False, w=None, color=None, dash=None, fill=None):
        q = [s.P(*p) for p in pts]
        a = []
        if w: a.append(f'stroke-width="{w}"')
        if color: a.append(f'stroke="{color}"')
        if dash: a.append(f'stroke-dasharray="{dash}"')
        a.append(f'fill="{fill}"' if fill else "")
        s.out.append(("path", q, close, a))
    def circle(s, c, r, axis, n=72, **kw):
        x, y, z = c; pts = []
        for i in range(n + 1):
            t = i / n * 2 * math.pi; u, v = r * math.cos(t), r * math.sin(t)
            pts.append((x, y + u, z + v) if axis == "x" else (x + u, y, z + v) if axis == "y" else (x + u, y + v, z))
        s.poly(pts, **kw)
    def dot(s, c, r=2.2, color=ACC):
        s.out.append(("dot", [s.P(*c)], r, color))
    def box(s, x0, y0, z0, x1, y1, z1, **kw):
        L = s.line
        for a, b in [((x0,y0,z1),(x1,y0,z1)),((x1,y0,z1),(x1,y1,z1)),((x1,y1,z1),(x0,y1,z1)),((x0,y1,z1),(x0,y0,z1)),
                     ((x1,y0,z0),(x1,y0,z1)),((x1,y1,z0),(x1,y1,z1)),((x0,y1,z0),(x0,y1,z1)),
                     ((x1,y0,z0),(x1,y1,z0)),((x1,y1,z0),(x0,y1,z0))]:
            L(a, b, **kw)
    def vcyl(s, c, r, h, n=72, **kw):
        x, y, z = c
        s.circle((x, y, z + h), r, "z", **kw)
        pts = [(x + r*math.cos(t), y + r*math.sin(t), z) for t in [i/n*2*math.pi for i in range(n+1)]]
        front = [p for p in pts if (p[0] + p[1]) >= (x + y) - 1e-6]
        front.sort(key=lambda p: math.atan2(p[1]-y, p[0]-x))
        s.poly(front, **kw)
        # silhouette: tangent points where x - y extreme
        a = (x + r*math.cos(-math.pi/4), y + r*math.sin(-math.pi/4)); b = (x + r*math.cos(3*math.pi/4), y + r*math.sin(3*math.pi/4))
        s.line((a[0], a[1], z), (a[0], a[1], z + h), **kw); s.line((b[0], b[1], z), (b[0], b[1], z + h), **kw)
    def svg(s, stroke, pad=34):
        xs = [x for o in s.out for x, _ in o[1]]; ys = [y for o in s.out for _, y in o[1]]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        sc = (400 - 2*pad) / max(x1 - x0, y1 - y0)
        ox = 200 - (x0 + x1) / 2 * sc; oy = 200 - (y0 + y1) / 2 * sc
        T = lambda x, y: (x*sc + ox, y*sc + oy)
        parts = []
        for o in s.out:
            if o[0] == "path":
                _, q, close, a = o
                d = "M" + " L".join("%.2f %.2f" % T(x, y) for x, y in q) + (" Z" if close else "")
                parts.append(f'<path d="{d}" {" ".join(a)}/>')
            else:
                _, q, r, color = o; x, y = T(*q[0])
                parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r*1.6:.2f}" fill="{color}" stroke="none"/>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" fill="none" stroke="{stroke}" '
                f'stroke-width=".9" stroke-linecap="round" stroke-linejoin="round">' + "".join(parts) + "</svg>")

def headset():
    d = D(k=1.0)
    # visor body: depth x 0..44, width y -70..70, height z -30..30; front face x=44 visible
    d.box(0, -70, -30, 44, 70, 30)
    # chamfer lines on front face
    d.poly([(44, -62, 30), (44, -70, 22)], w=.6); d.poly([(44, 62, 30), (44, 70, 22)], w=.6)
    # tracking cameras on front face (normal +x)
    for yy, zz in ((-50, 16), (50, 16), (-50, -16), (50, -16)):
        d.circle((44, yy, zz), 5, "x", w=.7)
    d.circle((44, 0, 0), 9, "x"); d.circle((44, 0, 0), 4, "x", w=.6); d.dot((44, 0, 0))
    # side face y=70: button + vents
    d.circle((22, 70, 8), 3.5, "y", w=.6)
    for xx in range(8, 38, 5): d.line((xx, 70, -18), (xx, 70, -8), w=.5)
    # face cushion behind (x<0)
    d.poly([(0, 70, 26), (-12, 66, 24), (-12, 66, -24), (0, 70, -26)], w=.6)
    # head strap: loop going back
    d.poly([(-12, 66, 8), (-60, 72, 12), (-110, 52, 14), (-132, 0, 14)], w=.9)
    d.poly([(-12, 66, -6), (-60, 72, -2), (-110, 52, 0), (-132, 0, 0)], w=.9)
    d.poly([(4, 0, 30), (-40, 0, 46), (-100, 0, 40), (-132, 0, 14)], w=.9)
    d.poly([(4, 8, 30), (-40, 8, 46), (-100, 8, 40), (-132, 8, 14)], w=.5)
    return d
def controller():
    d = D(cy=250, k=1.3)
    d.vcyl((0, 0, -60), 14, 75)
    d.circle((0, 0, 15), 32, "z"); d.circle((0, 0, 15), 26, "z", w=.6)
    d.circle((0, 0, 9), 32, "z", w=.5, dash="1 3")
    for t in range(0, 360, 30):
        a = math.radians(t); d.dot((32*math.cos(a), 32*math.sin(a), 15), r=1.2, color=None if t else ACC) if False else None
    for t in range(0, 360, 45):
        a = math.radians(t); x, y = 29*math.cos(a), 29*math.sin(a); d.line((x, y, 15), (x, y, 12), w=.6)
    d.circle((0, 0, 15), 5, "z"); d.dot((0, 0, 15), r=1.8)
    d.circle((14, 0, -20), 4, "x", w=.6)
    d.line((-12, 7, -60), (-12, 7, -64), w=.5)
    return d
def sensor():
    d = D(cy=200, k=1.15)
    d.box(-90, -14, 0, 90, 14, 22)
    for x, r in ((-55, 7), (0, 9), (40, 5), (62, 5)):
        d.circle((x, 14, 11), r, "y"); d.circle((x, 14, 11), r*.45, "y", w=.6)
    d.dot((0, 14, 11))
    for i in range(-80, -66, 3): d.line((i, 14, 4), (i, 14, 18), w=.5)
    d.vcyl((0, 0, -40), 8, 40); d.box(-30, -22, -48, 30, 22, -40)
    return d
def stylus():
    d = D(cy=230, k=1.1)
    # pen along axis tilted: build as sequence of circles along a direction
    import math as m
    dirv = (0.55, -0.35, 0.76); L = sum(v*v for v in dirv) ** .5; dirv = tuple(v/L for v in dirv)
    tip = (-70, 40, -40)
    def at(t): return tuple(tip[i] + dirv[i]*t for i in range(3))
    # body as two long lines + rings (approximate)
    perp = (0.6, 0.8, 0)
    for t in (22, 40, 120, 150):
        c = at(t); pts = []
        for i in range(37):
            a = i/36*2*m.pi; u = (perp[0]*m.cos(a)*7, perp[1]*m.cos(a)*7, m.sin(a)*7)
            pts.append((c[0]+u[0], c[1]+u[1], c[2]+u[2]))
        d.poly(pts, w=.8)
    for sgn in (1, -1):
        d.line(tuple(at(22)[i] + sgn*perp[i]*7 for i in range(3)), tuple(at(150)[i] + sgn*perp[i]*7 for i in range(3)))
        d.line(tip, tuple(at(22)[i] + sgn*perp[i]*7 for i in range(3)))
    d.dot(tip, r=2.4)
    # 3D stroke trailing from tip
    pts = []
    for i in range(160):
        t = i/159; a = t*4.2*m.pi
        pts.append((-70 - 120*t + 25*m.sin(a), 40 + 30*m.cos(a)*(1-t) - 20*t, -40 + 18*m.sin(a*0.5) - 10*t))
    d.poly(pts, w=.7)
    # floor grid
    for g in range(-150, 31, 30): d.line((g, -60, -95), (g, 90, -95), w=.35)
    for g in range(-60, 91, 30): d.line((-150, g, -95), (30, g, -95), w=.35)
    return d
def eye():
    d = D(cy=200, k=1.2)
    # eye as sphere-ish: circle front + iris on face
    d.circle((-70, 0, 40), 26, "x"); d.circle((-70, 0, 40), 11, "x"); d.dot((-70, 0, 40), r=2)
    d.poly([(-70, -38, 40), (-70, -12, 58), (-70, 12, 58), (-70, 38, 40), (-70, 12, 22), (-70, -12, 22)], close=True, w=.6)
    # gaze rays to plane
    target = (70, 10, 10)
    for dy, dz in ((-6, 4), (0, 0), (6, -4)):
        d.line((-70, dy*.5, 40 + dz*.5), (target[0], target[1] + dy*4, target[2] + dz*4), w=.5, dash="2 4")
    # screen plane
    d.poly([(70, -60, -40), (70, 70, -40), (70, 70, 60), (70, -60, 60)], close=True)
    for g in range(-40, 70, 20): d.line((70, g, -40), (70, g, 60), w=.3)
    for g in range(-20, 60, 20): d.line((70, -60, g), (70, 70, g), w=.3)
    d.circle((70, 10, 10), 10, "x", w=.7); d.dot((70, 10, 10), r=2.4)
    # drawn path on plane
    d.poly([(70, -40, 40), (70, -20, 30), (70, -5, 36), (70, 10, 10), (70, 30, 0), (70, 50, 20)], w=.9)
    return d
def body():
    d = D(cy=215, k=1.15)
    J = dict(head=(0, 0, 120), neck=(0, 0, 100), sl=(0, -24, 96), sr=(0, 24, 96), el=(10, -44, 70), er=(18, 40, 118),
             hl=(22, -50, 46), hr=(30, 50, 140), pel=(0, 0, 40), kl=(8, -14, 0), kr=(-6, 16, 2), fl=(14, -18, -40), fr=(-14, 20, -38),
             hipl=(0, -12, 40), hipr=(0, 12, 40))
    bones = [("neck","sl"),("neck","sr"),("sl","el"),("el","hl"),("sr","er"),("er","hr"),("neck","pel"),("hipl","hipr"),
             ("hipl","kl"),("kl","fl"),("hipr","kr"),("kr","fr")]
    for a, b in bones: d.line(J[a], J[b])
    d.circle(J["head"], 11, "x")
    for k, v in J.items():
        if k != "head": d.circle(v, 3, "x", w=.6)
    d.dot(J["hr"], r=2.6)
    # movement trace of right hand
    pts = [(30 + 25*math.sin(t/8), 50 + 30*math.cos(t/10), 140 - t*1.2 + 10*math.sin(t/5)) for t in range(0, 60)]
    d.poly(pts, w=.6, dash="1 3")
    # floor ellipse
    d.circle((0, 0, -42), 70, "z", w=.4); d.circle((0, 0, -42), 45, "z", w=.3, dash="2 4")
    return d
ITEMS = {"01-headset": headset, "02-controller": controller, "03-depth-sensor": sensor,
         "04-stylus-in-air": stylus, "05-gaze-drawing": eye, "06-motion-figure": body}
os.makedirs("svg", exist_ok=True)
for k, f in ITEMS.items():
    d = f()
    open(f"svg/{k}-black.svg", "w").write(d.svg("#111111"))
    open(f"svg/{k}-white.svg", "w").write(d.svg("#f2f2f2"))
print("ok")
