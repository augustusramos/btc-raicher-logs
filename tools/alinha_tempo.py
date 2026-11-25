"""Ajusta o deslocamento do eixo de datas de um print usando linhas já medidas em prints confiáveis.
Uso: python tools/alinha_tempo.py ARQUIVO REF1,REF2 DATA_COMPARACAO"""
import json, math, sys, subprocess, datetime as dt
nome, refs, t = sys.argv[1], sys.argv[2].split(','), sys.argv[3]
base = f'calibracao/linhas_prints/{nome}'
d = json.load(open(base + '.medidas.json'))
def val(L, t):
    (a, pa), (b, pb) = L['p1'], L['p2']; ta, tb, tt = [dt.datetime.fromisoformat(x).timestamp() for x in (a, b, t)]
    return pa * math.exp(math.log(pb / pa) * (tt - ta) / (tb - ta))
R = {}
for r in refs:
    for n, L in json.load(open(f'calibracao/linhas_prints/{r}.json'))['linhas'].items(): R.setdefault(n, []).append(val(L, t))
dx = d['x'][1][0] - d['x'][0][0]; best = None
for k in range(-40, 41):
    sh = k * dx / 40
    d2 = dict(d); d2['x'] = [[x + sh, dd] for x, dd in d['x']]; json.dump(d2, open('/tmp/al.json', 'w'))
    subprocess.run(['python3', 'tools/linhas_print.py', '/tmp/al.json', '/tmp/al_o.json'], capture_output=True)
    o = json.load(open('/tmp/al_o.json'))['linhas']
    e = [val(o[n], t) / (sum(R[n]) / len(R[n])) - 1 for n in o if n in R]
    if e:
        m = sum(abs(x) for x in e) / len(e)
        if not best or m < best[0]: best = (m, sh, [round(x * 1e4, 1) for x in e])
print('desloc px', round(best[1], 1), 'erro médio bp', round(best[0] * 1e4, 1), best[2])
if len(sys.argv) > 4:
    d['x'] = [[round(x + best[1], 1), dd] for x, dd in d['x']]; d['nota_tempo'] = f'eixo de datas alinhado por {sys.argv[2]} (desloc {best[1]:.1f}px)'
    json.dump(d, open(base + '.medidas.json', 'w'), ensure_ascii=False)
    subprocess.run(['python3', 'tools/linhas_print.py', base + '.medidas.json', base + '.json'], capture_output=True)
