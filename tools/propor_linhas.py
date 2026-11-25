"""Propõe linhas no estilo do Dollynho (retas em log ligando dois cruzamentos de médias do 343)
e escolhe as que o preço mais respeitou. Testa contra as linhas dele em cada print medido."""
import json, glob, math, sys, datetime as dt
import numpy as np, pandas as pd
sys.path.insert(0, 'tools')
from ancoras_cruzamentos import cruzamentos

TIPOS = None  # todos

def candidatas(P, T_D, janela2=365, janela1=3*365):
    """retorna arrays (s, a, tipo_idx) de retas ln p = a + s t"""
    S, A = [], []
    por = {}
    for p in P:
        if p['t'] < T_D - 86400: por.setdefault(p['tipo'], []).append(p)
    for tipo, Q in por.items():
        t = np.array([q['t'] for q in Q]); y = np.array([q['y'] for q in Q])
        i2 = np.where(t > T_D - janela2 * 86400)[0]
        for j in i2:
            i1 = np.where((t < t[j] - 86400) & (t > t[j] - janela1 * 86400))[0]
            if not len(i1): continue
            s = (y[j] - y[i1]) / (t[j] - t[i1]); a = y[j] - s * t[j]
            S.append(s); A.append(a)
    return np.concatenate(S), np.concatenate(A)

def pontua(s, a, bars, T_D, preco, faixa=0.08):
    v = a + s * T_D
    ok = np.abs(v - math.log(preco)) < faixa
    s, a = s[ok], a[ok]
    t = bars['t'].values; lo = np.log(bars.low.values); hi = np.log(bars.high.values); cl = np.log(bars.close.values)
    score = np.zeros(len(s))
    for k in range(0, len(s), 20000):
        L = a[k:k+20000, None] + s[k:k+20000, None] * t[None, :]
        rej = ((hi >= L - 0.001) & (cl < L) & (hi <= L + 0.004)) | ((lo <= L + 0.001) & (cl > L) & (lo >= L - 0.004))
        cruz = np.abs(np.diff(np.sign(cl[None, :] - L), axis=1)) > 0
        score[k:k+20000] = rej.sum(1) - float(sys.argv[3] if len(sys.argv)>3 else 0.5) * cruz.sum(1)
    return s, a, score

def escolhe(s, a, score, T_D, K, sep=0.003):
    v = a + s * T_D; esc = []
    for i in np.argsort(-score):
        if all(abs(v[i] - v[j]) > sep for j in esc): esc.append(i)
        if len(esc) == K: break
    return esc

def avalia(K=10, tol=0.003, seed=1):
    h = pd.read_csv('/tmp/h343.csv', index_col=0, parse_dates=True)
    h['t'] = (h.index - pd.Timestamp('1970-01-01', tz='UTC')).total_seconds() + 343 * 60
    P = cruzamentos(h, 343 * 60)
    rng = np.random.default_rng(seed)
    res = []
    for f in sorted(glob.glob('calibracao/linhas_prints/2*_343.json')):
        d = json.load(open(f)); quando = d['quando']
        T_D = dt.datetime.fromisoformat(quando).timestamp() + 3 * 3600
        bars = h[(h.t <= T_D) & (h.t > T_D - int(sys.argv[2] if len(sys.argv)>2 else 90) * 86400)]
        if len(bars) < 100: continue
        preco = float(bars.close.iloc[-1])
        s, a = candidatas(P, T_D)
        s, a, sc = pontua(s, a, bars, T_D, preco)
        esc = escolhe(s, a, sc, T_D, K)
        v_sis = (a + s * T_D)[esc]; s_sis = s[esc]
        dele = []
        for n, L in d['linhas'].items():
            (t1, p1), (t2, p2) = L['p1'], L['p2']
            ta, tb = [dt.datetime.fromisoformat(x).timestamp() + 3*3600 for x in (t1, t2)]
            sl = math.log(p2 / p1) / (tb - ta); vd = math.log(p1) + sl * (T_D - ta)
            if abs(vd - math.log(preco)) < 0.08: dele.append((n, vd, sl))
        if not dele: continue
        def acertos(vs, ss):
            return sum(any(abs(vd - vv) < tol and np.sign(sl) == np.sign(sv) for vv, sv in zip(vs, ss)) for _, vd, sl in dele)
        hit = acertos(v_sis, s_sis)
        base = []
        for _ in range(30):
            idx = escolhe(s, a, rng.random(len(s)), T_D, K)
            base.append(acertos((a + s * T_D)[idx], s[idx]))
        res.append(dict(print=f.split('/')[-1][:15], dele=len(dele), sistema=hit, acaso=round(float(np.mean(base)), 2), candidatas=len(s)))
        print(res[-1], flush=True)
    tot = sum(r['dele'] for r in res)
    print(f"K={K}: sistema acerta {sum(r['sistema'] for r in res)}/{tot} linhas dele; ao acaso {sum(r['acaso'] for r in res):.1f}/{tot}")
    json.dump(res, open(f'calibracao/teste_propor_K{K}.json', 'w'), indent=1)

if __name__ == '__main__':
    avalia(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
