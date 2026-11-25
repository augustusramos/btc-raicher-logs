"""Junta as medições dos prints numa lista única de linhas (uma por linha real) e procura as âncoras no histórico diário."""
import json, glob, math, datetime as dt, collections
import numpy as np, pandas as pd

def ts(s): return dt.datetime.fromisoformat(s).timestamp()

def junta():
    med = collections.defaultdict(list)
    for f in sorted(glob.glob('calibracao/linhas_prints/2*_343.json')):
        d = json.load(open(f))
        for n, l in d['linhas'].items():
            (a, pa), (b, pb) = l['p1'], l['p2']
            med[n].append(dict(print=f.split('/')[-1][:15], t1=ts(a) - 3*3600, p1=pa, t2=ts(b) - 3*3600, p2=pb, cor=l.get('cor'), estilo=l.get('estilo'), nota=l.get('nota')))
    linhas = []
    for n, ms in med.items():
        grupos = []
        for m in ms:  # mesma "cor/nome" pode ser linhas diferentes: agrupa pelo valor no meio do intervalo
            s = math.log(m['p2'] / m['p1']) / (m['t2'] - m['t1'])
            tm = (m['t1'] + m['t2']) / 2
            for g in grupos:
                v = g['a'] + g['s'] * (tm - g['t0'])
                if abs(v - (math.log(m['p1']) + s * (tm - m['t1']))) < 0.004 and abs(s - g['s']) < abs(g['s']) * 0.15 + 1e-11:
                    g['ms'].append(m); break
            else:
                grupos.append(dict(ms=[m], t0=m['t1'], a=math.log(m['p1']), s=s))
        for k, g in enumerate(grupos):
            T, Y = [], []
            for m in g['ms']:
                for t in np.linspace(m['t1'], m['t2'], 5):
                    T.append(t); Y.append(math.log(m['p1']) + math.log(m['p2']/m['p1']) * (t - m['t1']) / (m['t2'] - m['t1']))
            s, a = np.polyfit(T, Y, 1)
            res = float(np.std(np.array(Y) - (s * np.array(T) + a)))
            ms = g['ms']
            linhas.append(dict(nome=n + (f'_{k+1}' if len(grupos) > 1 else ''), s=s, a=a, res_bp=round(res * 1e4, 1),
                               n_prints=len(ms), primeiro=ms[0]['print'][:10], ultimo=ms[-1]['print'][:10],
                               cor=ms[0]['cor'], estilo=ms[0]['estilo'], notas=[m['nota'] for m in ms if m['nota']][:3],
                               t_ini=min(m['t1'] for m in ms), t_fim=max(m['t2'] for m in ms)))
    return linhas

def valor(L, t): return math.exp(L['a'] + L['s'] * t)

def ancoras(L, df, tol=0.0025):
    out = []
    t = ((df.index - pd.Timestamp('1970-01-01', tz=df.index.tz)).total_seconds() + 12*3600).values
    v = np.exp(L['a'] + L['s'] * t)
    for col, kind in (('high', 'topo'), ('low', 'fundo')):
        x = df[col].values
        piv = (x == pd.Series(x).rolling(11, center=True).max().values) if kind == 'topo' else (x == pd.Series(x).rolling(11, center=True).min().values)
        d = x / v - 1
        for i in np.where(piv & (np.abs(d) < tol))[0]:
            out.append((df.index[i].strftime('%Y-%m-%d'), kind, round(float(d[i]) * 100, 2)))
    for p1, p2 in ((7, 21), (7, 77), (21, 77), (7, 231), (7, 343)):
        for typ in ('ma', 'ema'):
            f = (lambda s, p: s.rolling(p).mean()) if typ == 'ma' else (lambda s, p: s.ewm(span=p, adjust=False).mean())
            m1, m2 = f(df.close, p1).values, f(df.close, p2).values
            cr = np.where(np.sign(m1[1:] - m2[1:]) != np.sign(m1[:-1] - m2[:-1]))[0] + 1
            for i in cr:
                if np.isnan(m2[i]): continue
                d = m1[i] / v[i] - 1
                if abs(d) < tol: out.append((df.index[i].strftime('%Y-%m-%d'), f'{typ}{p1}x{p2}', round(float(d) * 100, 2)))
    return sorted(out)

if __name__ == '__main__':
    df = pd.read_csv('/tmp/1D.csv', index_col=0, parse_dates=True)
    linhas = junta()
    for L in linhas:
        L['ancoras'] = ancoras(L, df.loc[:dt.datetime.fromtimestamp(L['t_ini']).strftime('%Y-%m-%d')])
        L['inclin_pct_dia'] = round(L['s'] * 86400 * 100, 4)
    json.dump(linhas, open('calibracao/gabarito_linhas.json', 'w'), ensure_ascii=False, indent=1, default=float)
    for L in linhas:
        print(f"{L['nome']:28s} n={L['n_prints']:2d} {L['primeiro']} {L['inclin_pct_dia']:+.3f}%/d res={L['res_bp']}bp anc={len(L['ancoras'])} {L['ancoras'][:6]}")
