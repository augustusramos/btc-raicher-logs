"""Converte linhas medidas num print (pixels) em preço x data.
Entrada: dict com eixos (y px -> preço; x px -> data) e linhas (m, c em pixels, y = m*x + c).
Escala de preço logarítmica (TradingView com L ativo)."""
import math, datetime as dt, json, sys
import numpy as np

def calibra(ylab, xlab):
    ys, ps = zip(*ylab); A = np.polyfit([math.log(p) for p in ps], ys, 1)  # y = a*ln(p)+b
    res = [y - (A[0]*math.log(p)+A[1]) for y, p in ylab]
    xs, ds = zip(*xlab); D = [dt.datetime.fromisoformat(d).timestamp() for d in ds]
    B = np.polyfit(xs, D, 1)  # t = b0*x + b1
    resx = [(B[0]*x+B[1]-t)/3600 for x, t in zip(xs, D)]
    return A, B, max(map(abs, res)), max(map(abs, resx))

def preco(A, y): return math.exp((y - A[1]) / A[0])
def data(B, x): return dt.datetime.fromtimestamp(B[0]*x+B[1])
def xpara(B, d): return (dt.datetime.fromisoformat(d).timestamp() - B[1]) / B[0]

def converte(spec):
    if 'candles' in spec:  # sem eixo de datas: última vela (abertura) + 5 velas por dia
        c = spec['candles']; t = dt.datetime.fromisoformat(c['ultima_abertura'])
        spec['x'] = [[c['ultima_x'] - c['sp'] * 5 * k, (t - dt.timedelta(days=k)).isoformat()] for k in range(12)]
    A, B, ry, rx = calibra(spec['y'], spec['x'])
    chk = [[e, round(preco(A, y))] for y, e in spec.get('checks', [])]
    out = {'print': spec['print'], 'quando': spec['quando'], 'erro_eixo_px': round(ry, 2), 'erro_tempo_h': round(rx, 2), 'conferencia_max_min': chk, 'linhas': {}}
    for nome, L in spec['linhas'].items():
        x0, x1 = L['x0'], L['x1']
        p0 = preco(A, L['m']*x0 + L['c']); p1 = preco(A, L['m']*x1 + L['c'])
        out['linhas'][nome] = {**{k: v for k, v in L.items() if k in ('cor', 'estilo', 'nota')},
            'p1': [data(B, x0).strftime('%Y-%m-%d %H:%M'), round(p0)], 'p2': [data(B, x1).strftime('%Y-%m-%d %H:%M'), round(p1)],
            'res_px': L.get('res')}
    return out

if __name__ == '__main__':
    spec = json.load(open(sys.argv[1])); r = converte(spec)
    if len(sys.argv) > 2: json.dump(r, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
    print(r['erro_eixo_px'], r['erro_tempo_h'], r['conferencia_max_min'])
    for k, v in r['linhas'].items(): print(k, v['p1'], v['p2'], v['res_px'])
