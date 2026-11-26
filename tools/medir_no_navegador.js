// Funções para medir linhas num print do X DENTRO do Chrome (javascript_tool), na página da imagem original
// https://pbs.twimg.com/media/<arquivo>?format=jpg&name=orig . Cole este arquivo inteiro num javascript_exec;
// depois use window.L.fit / bands / eixoX. Coordenadas em pixels da imagem original.
(function () {
  const I = document.querySelector('img'); const W = I.naturalWidth, H = I.naturalHeight;
  const c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d'); g.drawImage(I, 0, 0); const D = g.getImageData(0, 0, W, H).data;
  const px = (x, y) => { const o = (y * W + x) * 4; return [D[o], D[o + 1], D[o + 2]]; };
  // fit(a, b, cor, tol, janela, maxLarg, residuoMax): segue uma linha colorida entre a=[x,y] e b=[x,y] (palpites)
  // e devolve a reta y = m*x + c em pixels (res = erro em px). cor = [r,g,b] (null = detecta).
  function fit(a, b, col, tol, win, mw, rt) {
    win = win || 8; tol = tol || 70; mw = mw || 7; rt = rt || 2.5;
    if (!col) { let best = null; for (const f of [0.1, 0.3, 0.5, 0.7, 0.9]) { const x = Math.round(a[0] + (b[0] - a[0]) * f), ye = a[1] + (b[1] - a[1]) * f; for (let dy = -6; dy <= 6; dy++) { const d = px(x, Math.round(ye + dy)); const s = Math.max(...d) - Math.min(...d) + Math.max(...d) * 0.3; if (!best || s > best[0]) best = [s, d]; } } col = best[1]; }
    const pts = [];
    for (let x = Math.ceil(a[0]); x <= b[0]; x += 3) { const ye = a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]); const ys = []; for (let dy = -win; dy <= win; dy++) { const y = Math.round(ye + dy); const d = px(x, y); if (Math.abs(d[0] - col[0]) + Math.abs(d[1] - col[1]) + Math.abs(d[2] - col[2]) < tol) ys.push(y); } if (ys.length && ys.length < mw) pts.push([x, ys.reduce((s, v) => s + v, 0) / ys.length]); }
    const reg = P => { let n = P.length, sx = 0, sy = 0, sxx = 0, sxy = 0; P.forEach(p => { sx += p[0]; sy += p[1]; sxx += p[0] * p[0]; sxy += p[0] * p[1]; }); const m = (n * sxy - sx * sy) / (n * sxx - sx * sx); return [m, (sy - m * sx) / n]; };
    if (pts.length < 5) return { col, n: pts.length };
    let [m, cc] = reg(pts); let P2 = pts.filter(p => Math.abs(p[1] - (m * p[0] + cc)) < rt); if (P2.length >= 5) [m, cc] = reg(P2);
    const res = Math.sqrt(P2.reduce((s, p) => s + (p[1] - (m * p[0] + cc)) ** 2, 0) / P2.length);
    return { col, n: P2.length, m: +m.toFixed(5), c: +cc.toFixed(2), res: +res.toFixed(2), x0: P2[0][0], x1: P2[P2.length - 1][0] };
  }
  // bands(x0,x1,y0,y1,'y'): centros (y) dos rótulos claros do eixo de preço numa faixa de colunas.
  function bands(x0, x1, y0, y1, axis) { x0 = Math.round(x0); x1 = Math.round(x1); y0 = Math.round(y0); y1 = Math.round(y1); const out = []; let on = false, st = 0; const L = axis === 'y' ? y1 - y0 : x1 - x0; for (let k = 0; k <= L; k++) { let hit = false; if (axis === 'y') { for (let x = x0; x < x1; x++) { const d = px(x, y0 + k); if (d[0] + d[1] + d[2] > 330) { hit = true; break; } } } else { for (let y = y0; y < y1; y++) { const d = px(x0 + k, y); if (d[0] + d[1] + d[2] > 330) { hit = true; break; } } } if (hit && !on) { on = true; st = k; } if (!hit && on) { on = false; out.push(+(((st + k - 1) / 2) + (axis === 'y' ? y0 : x0)).toFixed(1)); } } return out; }
  // eixoX(): centros [x, largura] dos rótulos verdes do eixo de datas (números do dia ~5-25 px de largura).
  function eixoX() { let best = null; for (let y0 = H - 100; y0 < H - 30; y0 += 3) { let n = 0; for (let x = 0; x < W - 80; x++) { const d = px(x, y0); if (d[1] > 150 && d[0] < 180 && d[2] < 120) n++; } if (!best || n > best[1]) best = [y0, n]; } const y0 = best[0]; const cols = []; for (let x = 0; x < W - 80; x++) { let on = false; for (let y = y0 - 8; y < y0 + 8; y++) { const d = px(x, y); if (d[1] > 150 && d[0] < 180 && d[2] < 120) { on = true; break; } } cols.push(on); } const runs = []; let st = -1; cols.forEach((v, x) => { if (v && st < 0) st = x; if (!v && st >= 0) { runs.push([st, x - 1]); st = -1; } }); const gg = []; runs.forEach(r => { if (gg.length && r[0] - gg[gg.length - 1][1] < 10) gg[gg.length - 1][1] = r[1]; else gg.push([r[0], r[1]]); }); return gg.map(r => [(r[0] + r[1]) / 2, r[1] - r[0]]); }
  window.L = { fit, bands, eixoX, px, W, H };
  return 'ok ' + W + 'x' + H;
})();
