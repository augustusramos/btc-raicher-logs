"""Testa a hipótese: as linhas do Dollynho ligam duas AGULHADAS do gráfico de 343
(momentos em que MA/EMA 7, 21 e 77 se encontram num ponto)."""
import json, math, itertools, sys
import numpy as np, pandas as pd

def eventos(df, combos=((7, 21, 77), (7, 21, 343), (7, 77, 231)), lim=0.004):
    t = ((df.index - pd.Timestamp('1970-01-01', tz='UTC')).total_seconds() + df.attrs.get('dur', 343 * 60)).values
    E = []
    for ps in combos:
        for typ in ('ma', 'ema'):
            M = pd.concat([(df.close.rolling(p).mean() if typ == 'ma' else df.close.ewm(span=p, adjust=False).mean()) for p in ps], axis=1)
            mid = M.mean(axis=1).values; spr = ((M.max(axis=1) - M.min(axis=1)) / M.mean(axis=1)).values
            low = (spr < lim) & (spr == pd.Series(spr).rolling(9, center=True, min_periods=1).min().values)
            for i in np.where(low)[0]:
                E.append(dict(t=t[i], y=math.log(mid[i]), tipo=f"{typ}{','.join(map(str, ps))}", quando=df.index[i].tz_convert('America/Sao_Paulo').strftime('%Y-%m-%d %H:%M'), spr=round(spr[i] * 100, 2)))
    return E

def testa(L, E, tol_bp=15):
    tm = (L['t_ini'] + L['t_fim']) / 2; ym = L['a'] + L['s'] * tm
    Q = [e for e in E if e['t'] < L['t_ini'] - 86400]
    r = []
    for a, b in itertools.combinations(Q, 2):
        if a['tipo'] != b['tipo'] or b['t'] - a['t'] < 2 * 86400: continue
        s = (b['y'] - a['y']) / (b['t'] - a['t'])
        err = (a['y'] + s * (tm - a['t']) - ym) * 1e4
        if abs(err) < tol_bp and abs(s - L['s']) < abs(L['s']) * 0.1 + 3e-10:
            r.append((round(abs(err), 1), a['tipo'], a['quando'], b['quando']))
    return sorted(r)

if __name__ == '__main__':
    df = pd.read_csv(sys.argv[1] if len(sys.argv)>1 else '/tmp/343m.csv', index_col=0, parse_dates=True)
    E = eventos(df)
    print('agulhadas no 343 desde', df.index[0].date(), ':', len(E))
    G = json.load(open('calibracao/gabarito_linhas.json'))
    tot = ok = 0; out = {}
    for L in G:
        if L['t_ini'] < df.index[0].timestamp() + 120 * 86400: continue
        r = testa(L, E); tot += 1; ok += bool(r); out[L['nome']] = r[:5]
        print(f"{L['nome']:28s} {len(r):3d}", r[:2])
    print(f'linhas com par de agulhadas que reproduz: {ok}/{tot}')
    json.dump(out, open('/tmp/agulhadas_res.json', 'w'), ensure_ascii=False)
