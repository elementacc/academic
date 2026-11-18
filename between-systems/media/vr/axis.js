/* Axis / Space — minimal line figure for the VR Sketching page.
   Isometric thin-line cube of space, one reference plane, a hand-drawn pyramid
   drawn in with a doubled line, and a single orange point at the pen tip.
   Drag to turn the view. */
(function () {
  const cv = document.getElementById('axis-canvas');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const INK = '#222', ACCENT = '#f26a3d';
  let W = 0, H = 0, DPR = 1;

  function size() {
    const r = cv.getBoundingClientRect();
    DPR = Math.min(2, window.devicePixelRatio || 1);
    W = r.width; H = r.height;
    cv.width = Math.round(W * DPR); cv.height = Math.round(H * DPR);
  }

  // isometric start: yaw 45°, pitch ~35°
  let yaw = -Math.PI / 4, pitch = 0.6155, tYaw = yaw, tPitch = pitch, drag = null, t0 = performance.now();

  function project(p) {
    const cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
    const x = p[0] * cy - p[2] * sy, z0 = p[0] * sy + p[2] * cy;
    const y = p[1] * cp - z0 * sp, z = p[1] * sp + z0 * cp;
    const s = Math.min(W / 4.2, H / 3.6);
    return [W / 2 + x * s, H * 0.52 - y * s, z];
  }

  function line(a, b) {
    const p = project(a), q = project(b);
    ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
  }

  // cube of space: a long box like the reference, slightly stretched on x
  const X = 1.35, Y = 0.8, Z = 0.8;
  const corners = [];
  for (const x of [-X, X]) for (const y of [-Y, Y]) for (const z of [-Z, Z]) corners.push([x, y, z]);
  const edges = [];
  corners.forEach((a, i) => corners.forEach((b, j) => {
    if (j > i && (a[0] !== b[0]) + (a[1] !== b[1]) + (a[2] !== b[2]) === 1) edges.push([a, b]);
  }));

  // hand-drawn pyramid (slightly wobbly), plus a second, offset pass of the same line
  function wob(a, b, n, k) {
    const out = [], ph = k * 1.7;
    for (let i = 0; i <= n; i++) {
      const t = i / n, env = Math.sin(t * Math.PI) * 0.02;
      out.push([a[0] + (b[0] - a[0]) * t + env * Math.sin(t * 3.1 + ph),
                a[1] + (b[1] - a[1]) * t + env * Math.sin(t * 2.7 + ph * 1.3),
                a[2] + (b[2] - a[2]) * t + env * Math.cos(t * 2.3 + ph)]);
    }
    return out;
  }
  const b = -Y, r = 0.55;
  const A = [-r, b, -r], B = [r, b, -r], C = [r, b, r], D = [-r, b, r], T = [0.04, 0.55, 0.02];
  const strokes = [[A, B], [B, C], [C, D], [D, A], [A, T], [B, T], [C, T], [D, T]]
    .map((s, k) => wob(s[0], s[1], 30, k * 31 + 3));
  const total = strokes.reduce((n, s) => n + s.length, 0);

  function draw(now) {
    if (!drag && !reduce) tYaw += 0.0009;
    yaw += (tYaw - yaw) * 0.08; pitch += (tPitch - pitch) * 0.08;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.lineCap = 'round'; ctx.lineJoin = 'round';

    // box
    ctx.strokeStyle = INK; ctx.lineWidth = 1.1;
    edges.forEach(([a, c]) => line(a, c));

    // one reference plane (floor at mid-height), hairline
    ctx.lineWidth = 0.6;
    const m = 0;
    [[[-X, m, -Z], [X, m, -Z]], [[X, m, -Z], [X, m, Z]], [[X, m, Z], [-X, m, Z]], [[-X, m, Z], [-X, m, -Z]]].forEach(([a, c]) => line(a, c));

    // pyramid drawn in, with a thin second pass
    const prog = reduce ? 1 : Math.min(1, ((now - t0) / 8000) % 1.3);
    let budget = Math.floor(prog * total), tip = null;
    for (const s of strokes) {
      if (budget <= 1) break;
      const n = Math.min(s.length, budget); budget -= n;
      ctx.beginPath();
      for (let i = 0; i < n; i++) { const p = project(s[i]); i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1]); }
      ctx.lineWidth = 1.1; ctx.stroke();
      ctx.beginPath();
      for (let i = 0; i < n; i++) { const p = project(s[i]); i ? ctx.lineTo(p[0] + 3, p[1] - 2) : ctx.moveTo(p[0] + 3, p[1] - 2); }
      ctx.lineWidth = 0.5; ctx.stroke();
      tip = project(s[n - 1]);
    }

    // pen tip: the single accent
    if (!tip || prog >= 1) tip = project(T);
    ctx.lineWidth = 1.1; ctx.strokeStyle = INK;
    ctx.beginPath(); ctx.ellipse(tip[0], tip[1], 11, 13, -0.5, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = ACCENT;
    ctx.beginPath(); ctx.arc(tip[0], tip[1], 4.5, 0, Math.PI * 2); ctx.fill();

    // small hatch marks on one face, like the reference
    ctx.lineWidth = 0.8; ctx.strokeStyle = INK;
    for (let i = 0; i < 6; i++) {
      const z = -Z * 0.55 + i * 0.09;
      line([-X, -Y * 0.15, z], [-X, -Y * 0.5, z]);
    }

    requestAnimationFrame(draw);
  }

  cv.addEventListener('pointerdown', e => { drag = { x: e.clientX, y: e.clientY, yaw: tYaw, pitch: tPitch }; cv.setPointerCapture(e.pointerId); });
  cv.addEventListener('pointermove', e => {
    if (!drag) return;
    tYaw = drag.yaw + (e.clientX - drag.x) * 0.008;
    tPitch = Math.max(-1.2, Math.min(1.2, drag.pitch + (e.clientY - drag.y) * 0.006));
  });
  const end = () => { drag = null; };
  cv.addEventListener('pointerup', end); cv.addEventListener('pointercancel', end);
  cv.addEventListener('dblclick', () => { t0 = performance.now(); });

  size(); addEventListener('resize', size);
  requestAnimationFrame(draw);
})();
