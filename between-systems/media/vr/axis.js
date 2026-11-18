/* Axis / Space — interactive figure for the VR Sketching page.
   Three grain-shaded orthogonal planes, a bounding cube marked with crosshairs,
   and a hand-drawn stroke that is redrawn in space. Drag (or move) to turn the view. */
(function () {
  const cv = document.getElementById('axis-canvas');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  const readout = document.getElementById('axis-readout');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let W = 0, H = 0, DPR = 1;
  const off = document.createElement('canvas'), oc = off.getContext('2d');

  // grain texture (stipple)
  const grain = document.createElement('canvas');
  grain.width = grain.height = 256;
  (function () {
    const g = grain.getContext('2d'), id = g.createImageData(256, 256);
    for (let i = 0; i < id.data.length; i += 4) {
      const v = Math.random();
      id.data[i] = id.data[i + 1] = id.data[i + 2] = 0;
      id.data[i + 3] = Math.round(255 * Math.pow(v, 1.6));
    }
    g.putImageData(id, 0, 0);
  })();

  function size() {
    const r = cv.getBoundingClientRect();
    DPR = Math.min(2, window.devicePixelRatio || 1);
    W = r.width; H = r.height;
    cv.width = off.width = Math.round(W * DPR);
    cv.height = off.height = Math.round(H * DPR);
  }

  // view state
  let yaw = -0.62, pitch = 0.42, tYaw = yaw, tPitch = pitch, drag = null, t0 = performance.now();

  function project(p) {
    const cy = Math.cos(yaw), sy = Math.sin(yaw), cp = Math.cos(pitch), sp = Math.sin(pitch);
    let x = p[0] * cy - p[2] * sy, z = p[0] * sy + p[2] * cy;
    let y = p[1] * cp - z * sp; z = p[1] * sp + z * cp;
    const s = Math.min(W, H) * 0.27, f = 4.2 / (4.2 + z);
    return [W / 2 + x * s * f, H * 0.5 - y * s * f, z];
  }

  // hand-drawn pyramid stroke in space (wobbly, like a first VR sketch)
  function wob(a, b, n, k) {
    const out = [], f1 = 1 + (k % 3), f2 = 2 + (k % 2), ph = k * 1.7;
    for (let i = 0; i <= n; i++) {
      const t = i / n, env = Math.sin(t * Math.PI) * 0.028;
      out.push([a[0] + (b[0] - a[0]) * t + env * Math.sin(t * f1 * 3.1 + ph),
                a[1] + (b[1] - a[1]) * t + env * Math.sin(t * f2 * 2.7 + ph * 1.3),
                a[2] + (b[2] - a[2]) * t + env * Math.cos(t * f1 * 2.3 + ph)]);
    }
    return out;
  }
  const A = [-0.7, -0.55, -0.7], B = [0.7, -0.55, -0.7], C = [0.7, -0.55, 0.7], D = [-0.7, -0.55, 0.7], T = [0.05, 0.75, 0.0];
  const strokes = [[A, B], [B, C], [C, D], [D, A], [A, T], [B, T], [C, T], [D, T],
    [[-0.35, -0.55, -0.7], [-0.35, -0.55, 0.7]], [[-0.7, -0.55, 0.05], [0.7, -0.55, 0.05]]]
    .map((s, k) => wob(s[0], s[1], 24, k * 31 + 3));
  const total = strokes.reduce((n, s) => n + s.length, 0);

  const planes = [
    { pts: [[-1, -1, 0], [1, -1, 0], [1, 1, 0], [-1, 1, 0]], tone: 0.8, label: 'XY' },
    { pts: [[0, -1, -1], [0, -1, 1], [0, 1, 1], [0, 1, -1]], tone: 1, label: 'YZ' },
    { pts: [[-1, 0, -1], [1, 0, -1], [1, 0, 1], [-1, 0, 1]], tone: 0.6, label: 'XZ' },
  ];
  const corners = [];
  for (const x of [-1, 1]) for (const y of [-1, 1]) for (const z of [-1, 1]) corners.push([x, y, z]);
  const edges = [];
  corners.forEach((a, i) => corners.forEach((b, j) => {
    if (j > i && (a[0] !== b[0]) + (a[1] !== b[1]) + (a[2] !== b[2]) === 1) edges.push([a, b]);
  }));

  function plane(pl) {
    const P = pl.pts.map(project);
    oc.setTransform(1, 0, 0, 1, 0, 0);
    oc.clearRect(0, 0, off.width, off.height);
    oc.setTransform(DPR, 0, 0, DPR, 0, 0);
    oc.beginPath(); P.forEach((p, i) => (i ? oc.lineTo(p[0], p[1]) : oc.moveTo(p[0], p[1]))); oc.closePath();
    const g = oc.createLinearGradient(P[0][0], P[0][1], P[2][0], P[2][1]);
    g.addColorStop(0, `rgba(0,0,0,${pl.tone})`);
    g.addColorStop(0.5, `rgba(0,0,0,${pl.tone * 0.35})`);
    g.addColorStop(1, `rgba(0,0,0,${pl.tone * 0.08})`);
    oc.fillStyle = g; oc.fill();
    oc.globalCompositeOperation = 'destination-in';
    oc.setTransform(1, 0, 0, 1, 0, 0);
    oc.fillStyle = oc.createPattern(grain, 'repeat');
    oc.fillRect(0, 0, off.width, off.height);
    oc.globalCompositeOperation = 'source-over';
    ctx.drawImage(off, 0, 0, W, H);
  }

  function cross(x, y, s) {
    ctx.beginPath(); ctx.moveTo(x - s, y); ctx.lineTo(x + s, y); ctx.moveTo(x, y - s); ctx.lineTo(x, y + s); ctx.stroke();
  }

  function draw(now) {
    if (!drag && !reduce) tYaw += 0.0012;
    yaw += (tYaw - yaw) * 0.08; pitch += (tPitch - pitch) * 0.08;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    ctx.clearRect(0, 0, W, H);

    // planes, far to near
    planes.map(pl => ({ pl, z: pl.pts.map(project).reduce((s, p) => s + p[2], 0) }))
      .sort((a, b) => b.z - a.z).forEach(o => plane(o.pl));

    // cube hairlines + crosshairs
    ctx.strokeStyle = 'rgba(0,0,0,.28)'; ctx.lineWidth = 0.6;
    edges.forEach(([a, b]) => { const p = project(a), q = project(b); ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke(); });
    ctx.strokeStyle = '#000'; ctx.lineWidth = 1;
    corners.forEach(c => { const p = project(c); cross(p[0], p[1], 6); });

    // stroke drawn in over time
    const prog = reduce ? 1 : Math.min(1, ((now - t0) / 7000) % 1.25);
    let budget = Math.floor(prog * total);
    ctx.strokeStyle = '#000'; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
    for (const s of strokes) {
      if (budget <= 1) break;
      const n = Math.min(s.length, budget); budget -= n;
      for (let i = 1; i < n; i++) {
        const p = project(s[i - 1]), q = project(s[i]);
        ctx.lineWidth = Math.max(1.2, 4.2 - (p[2] + 1.5) * 1);
        ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
      }
    }

    // axis gizmo, bottom left
    const o = [-1.35, -1.15, 1.25], L = 0.38;
    const po = project(o);
    [['X', [L, 0, 0]], ['Y', [0, 0, -L]], ['Z', [0, L, 0]]].forEach(([n, d]) => {
      const q = project([o[0] + d[0], o[1] + d[1], o[2] + d[2]]);
      ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(po[0], po[1]); ctx.lineTo(q[0], q[1]); ctx.stroke();
      ctx.font = '11px "Helvetica Neue", Helvetica, Arial, sans-serif'; ctx.fillStyle = '#000';
      ctx.fillText(n, q[0] + (q[0] >= po[0] ? 4 : -10), q[1] + (q[1] > po[1] ? 12 : -4));
    });

    if (readout) {
      const deg = v => Math.round(((v * 180 / Math.PI) % 360 + 540) % 360 - 180);
      readout.textContent = `yaw ${deg(yaw)}°  pitch ${deg(pitch)}°`;
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
