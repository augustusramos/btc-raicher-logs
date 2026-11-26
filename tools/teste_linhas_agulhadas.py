"""Backtest: o preço respeita as linhas de agulhadas (343, MA 7/21/77) mais do que linhas quaisquer?
Mede, em cada toque (vela cujo range atravessa a linha), se a vela fechou do lado de onde veio (rejeição)."""
import math, sys
import numpy as np, pandas as pd
sys.path.insert(0, 'tools')
from agulhadas_consecutivas import agulhadas

h = pd.read_csv('/tmp/h343.csv', index_col=0, parse_dates=True)
t = ((h.index - pd.Timestamp('1970-01-01', tz='UTC')).total_seconds() + 343 * 60).values
lo, hi, cl = np.log(h.low.values), np.log(h.high.values), np.log(h.close.values)

def toques(t1, y1, t2, y2, ate_dias=365):
    s = (y2 - y1) / (t2 - t1)
    m = (t > t2 + 86400) & (t < t2 + ate_dias * 86400)
    idx = np.where(m)[0]
    if len(idx) < 3: return 0, 0
    L = y1 + s * (t - t1)
    lado_prev = np.sign(cl[idx - 1] - L[idx - 1])
    toque = (lo[idx] <= L[idx]) & (hi[idx] >= L[idx]) & (lado_prev != 0)
    rej = toque & (np.sign(cl[idx] - L[idx]) == lado_prev)
    return int(toque.sum()), int(rej.sum())

rng = np.random.default_rng(0)
for viz in (1, 2, 3):
    ev = agulhadas(h, lim=0.003)
    T = R = Tc = Rc = 0; nl = 0
    for i in range(len(ev)):
        for j in range(i + 1, min(len(ev), i + 1 + viz)):
            (t1, y1, *_), (t2, y2, *_) = ev[i], ev[j]
            a, b = toques(t1, y1, t2, y2); T += a; R += b; nl += 1
            for _ in range(10):  # controle: mesma inclinação, deslocada ±1-8%
                d = rng.choice([-1, 1]) * rng.uniform(0.01, 0.08)
                a, b = toques(t1, y1 + d, t2, y2 + d); Tc += a; Rc += b
    print(f'pares até {viz} vizinhas: {nl} linhas | toques {T}, rejeição {R/T:.0%} | controle: toques/linha {Tc/nl/10:.1f}, rejeição {Rc/max(Tc,1):.0%}')
