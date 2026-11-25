"""Hipótese (confirmada na Linha Branca e na Magenta): a linha liga dois CRUZAMENTOS do mesmo tipo
(ex.: MA7 x MA77) no gráfico de 343 ou no Diário. Para cada linha, lista os pares do mesmo tipo que a reproduzem."""
import json, math, itertools, sys
import numpy as np, pandas as pd

def cruzamentos(df, dur, pref=''):
    t0 = ((df.index - pd.Timestamp('1970-01-01', tz='UTC')).total_seconds()).values
    P = []
    for typ in ('ma', 'ema'):
        M = {p: (df.close.rolling(p).mean() if typ == 'ma' else df.close.ewm(span=p, adjust=False).mean()).values for p in (7, 21, 49, 77, 231, 343)}
        for a, b in itertools.combinations(M, 2):
            d = M[a] - M[b]
            for i in np.where(np.sign(d[1:]) != np.sign(d[:-1]))[0] + 1:
                if np.isnan(d[i-1]): continue
                f = d[i-1] / (d[i-1] - d[i])
                P.append(dict(t=t0[i-1] + dur + f * dur, y=math.log(M[a][i-1] + f * (M[a][i] - M[a][i-1])), tipo=f'{pref}{typ}{a}x{b}',
                              quando=df.index[i].tz_convert('America/Sao_Paulo').strftime('%Y-%m-%d %H:%M')))
    return P

def pares(L, P, tol_bp=10):
    tm = (L['t_ini'] + L['t_fim']) / 2; ym = L['a'] + L['s'] * tm
    por = {}
    for p in P:
        if p['t'] < L['t_ini'] - 86400: por.setdefault(p['tipo'], []).append(p)
    r = []
    for tipo, Q in por.items():
        T = np.array([q['t'] for q in Q]); Y = np.array([q['y'] for q in Q])
        for i in range(len(Q)):
            s = (Y[i+1:] - Y[i]) / (T[i+1:] - T[i])
            err = (Y[i] + s * (tm - T[i]) - ym) * 1e4
            ok = np.where((np.abs(err) < tol_bp) & (np.abs(s - L['s']) < abs(L['s']) * 0.08 + 3e-10) & (T[i+1:] - T[i] > 86400))[0]
            for j in ok: r.append((round(abs(float(err[j])), 1), tipo, Q[i]['quando'], Q[i+1+j]['quando']))
    return sorted(r)

if __name__ == '__main__':
    h = pd.read_csv('/tmp/h343.csv', index_col=0, parse_dates=True)
    d = pd.read_csv('/tmp/1D.csv', index_col=0, parse_dates=True)
    P = cruzamentos(h, 343 * 60, '343:') + cruzamentos(d.loc['2016':], 86400, 'D:')
    G = json.load(open('calibracao/gabarito_linhas.json'))
    out = {}; n1 = 0
    for L in G:
        r = pares(L, P); out[L['nome']] = r[:6]; n1 += len(r) == 1
        print(f"{L['nome']:28s} {len(r):3d}", r[:2])
    json.dump(out, open('calibracao/ancoras_candidatas.json', 'w'), ensure_ascii=False, indent=1)
    print('linhas com 1 único par:', n1, '/', len(G))
