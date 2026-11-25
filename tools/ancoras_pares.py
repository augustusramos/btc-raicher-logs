"""Para cada linha do gabarito, procura PARES de pontos no Diário (cruzamentos de médias, topos e fundos)
cuja reta (em escala log) reproduz a linha medida nos prints dele."""
import json, math, datetime as dt, itertools
import numpy as np, pandas as pd

def pontos(df):
    t0 = ((df.index - pd.Timestamp('1970-01-01', tz=df.index.tz)).total_seconds()).values
    P = []  # (t, log p, tipo)
    per = (7, 21, 49, 77, 200, 231, 343)
    for typ in ('ma', 'ema'):
        M = {p: (df.close.rolling(p).mean() if typ == 'ma' else df.close.ewm(span=p, adjust=False).mean()).values for p in per}
        for a, b in itertools.combinations(per, 2):
            d = M[a] - M[b]
            for i in np.where(np.sign(d[1:]) != np.sign(d[:-1]))[0] + 1:
                if np.isnan(d[i-1]) or np.isnan(M[b][i-1]): continue
                f = d[i-1] / (d[i-1] - d[i])  # interpolação entre fechamentos
                t = t0[i-1] + 86400 + f * 86400  # fechamento da vela i-1 = abertura + 1 dia
                v = M[a][i-1] + f * (M[a][i] - M[a][i-1])
                P.append((t, math.log(v), f'{typ}{a}x{b}', df.index[i].strftime('%Y-%m-%d')))
    for col, kind in (('high', 'topo'), ('low', 'fundo')):
        x = df[col].values
        r = pd.Series(x).rolling(11, center=True)
        piv = x == (r.max().values if kind == 'topo' else r.min().values)
        for i in np.where(piv)[0]:
            P.append((t0[i] + 43200, math.log(x[i]), kind, df.index[i].strftime('%Y-%m-%d')))
    return P

def busca(L, P, tol=0.0012, tol_s=0.06):
    tm = (L['t_ini'] + L['t_fim']) / 2; ym = L['a'] + L['s'] * tm
    Q = [p for p in P if p[0] < L['t_ini'] - 3 * 86400]
    T = np.array([q[0] for q in Q]); Y = np.array([q[1] for q in Q])
    achados = []
    for i in range(len(Q)):
        s = (ym - Y[i]) / (tm - T[i])
        if abs(s - L['s']) > abs(L['s']) * tol_s + 2e-10: continue
        pred = Y[i] + s * (T - T[i])
        ok = np.where((np.abs(pred - Y) < tol) & (T > T[i] + 5 * 86400))[0]
        for j in ok:
            s2 = (Y[j] - Y[i]) / (T[j] - T[i])
            err = abs((Y[i] + s2 * (tm - T[i])) - ym)
            achados.append((round(err * 1e4, 1), Q[i][3], Q[i][2], Q[j][3], Q[j][2]))
    achados.sort()
    return achados

if __name__ == '__main__':
    df = pd.read_csv('/tmp/1D.csv', index_col=0, parse_dates=True)
    P = pontos(df)
    G = json.load(open('calibracao/gabarito_linhas.json'))
    res = {}
    for L in G:
        a = busca(L, P)
        res[L['nome']] = a[:8]
        print(f"{L['nome']:28s} n={L['n_prints']:2d} achados={len(a):3d}", a[:3])
    json.dump(res, open('/tmp/pares.json', 'w'), ensure_ascii=False)
