"""Hipótese (Raicher 22/11 e 06/12/2025; Dollynho 31/01/2026): as linhas ligam AGULHADAS do 343
(MA7, MA21 e MA77 se encontrando num ponto). Testa quais pares de agulhadas ele liga."""
import json, math, glob, sys, datetime as dt
import numpy as np, pandas as pd

def agulhadas(h, ps=(7, 21, 77), typ='ma', lim=0.003):
    t = ((h.index - pd.Timestamp('1970-01-01', tz='UTC')).total_seconds() + 343 * 60).values
    X = np.array([(h.close.rolling(p).mean() if typ == 'ma' else h.close.ewm(span=p, adjust=False).mean()).values for p in ps])
    mid = X.mean(0); spr = (X.max(0) - X.min(0)) / mid
    low = (spr < lim) & (spr == pd.Series(spr).rolling(15, center=True, min_periods=1).min().values)
    idx = np.where(low)[0]
    # agrupa agulhadas a menos de 2 dias (mesmo evento)
    ev = []
    for i in idx:
        if ev and t[i] - ev[-1][0] < 2 * 86400:
            if spr[i] < ev[-1][2]: ev[-1] = (t[i], math.log(mid[i]), spr[i], h.index[i])
        else: ev.append((t[i], math.log(mid[i]), spr[i], h.index[i]))
    return ev

def linhas_dele():
    out = []
    for f in sorted(glob.glob('calibracao/linhas_prints/2*_343.json')):
        d = json.load(open(f)); T = dt.datetime.fromisoformat(d['quando']).timestamp() + 3 * 3600
        for n, L in d['linhas'].items():
            (t1, p1), (t2, p2) = L['p1'], L['p2']
            ta, tb = [dt.datetime.fromisoformat(x).timestamp() + 3 * 3600 for x in (t1, t2)]
            s = math.log(p2 / p1) / (tb - ta)
            out.append((f.split('/')[-1][:15], n, T, math.log(p1) + s * (T - ta), s))
    return out

def testa(ev, maxgap, tol=0.003):
    D = linhas_dele(); hit = 0; ncand = []
    for pr, n, T, v, s in D:
        E = [e for e in ev if e[0] < T - 86400]
        cands = []
        for i in range(len(E)):
            for j in range(i + 1, min(len(E), i + 1 + maxgap)):
                sl = (E[j][1] - E[i][1]) / (E[j][0] - E[i][0]); vv = E[i][1] + sl * (T - E[i][0])
                cands.append((vv, sl, i, j))
        near = [c for c in cands if abs(c[0] - v) < 0.08]
        ncand.append(len([c for c in cands if abs(c[0] - v) < 0.08]))
        if any(abs(c[0] - v) < tol and np.sign(c[1]) == np.sign(s) for c in cands): hit += 1
    return hit, len(D), float(np.mean(ncand))

if __name__ == '__main__':
    h = pd.read_csv('/tmp/h343.csv', index_col=0, parse_dates=True)
    for typ in ('ma', 'ema'):
        for lim in (0.002, 0.003, 0.005):
            ev = agulhadas(h, typ=typ, lim=lim)
            for g in (1, 2, 3, 99):
                hit, tot, nc = testa(ev, g)
                # acaso: fração da faixa ±8% coberta por nc linhas com tolerância ±0,3% (aprox.)
                acaso = 1 - (1 - 0.006 / 0.16) ** (nc / 2)
                print(f'{typ} lim {lim*100:.1f}% agulhadas={len(ev):3d} pares até {g:2d} vizinhas: acerta {hit}/{tot} ({hit/tot:.0%}) | candidatas na faixa {nc:.1f} | acaso ~{acaso:.0%}')
