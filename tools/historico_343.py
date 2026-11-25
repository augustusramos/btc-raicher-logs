"""Monta o histórico longo do 343m e 686m (desde 2021) a partir de candles de 1 min da Bitstamp.
Roda no GitHub Actions (o sandbox não acessa a Bitstamp). Saída: <dir>/343m.csv.gz e 686m.csv.gz."""
import sys, time
from pathlib import Path
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from raicher.fetch import _get, _to_df
from raicher.timeframes import intraday

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
inicio = pd.Timestamp(sys.argv[2] if len(sys.argv) > 2 else '2021-01-01', tz='UTC')
fim = pd.Timestamp.now(tz='UTC').floor('D')
partes = {343: [], 686: []}
mes = inicio
while mes < fim:
    prox = min(mes + pd.offsets.MonthBegin(1), fim)
    s, e = int(mes.timestamp()), int(prox.timestamp())
    rows = []
    while s < e:
        r = _get('btcusd', 60, s)
        if not r: break
        df = _to_df(r); rows.append(df)
        last = int(df.index[-1].timestamp())
        if last <= s: break
        s = last + 60; time.sleep(0.1)
    if rows:
        m = pd.concat(rows); m = m[~m.index.duplicated()].sort_index(); m = m[m.index < prox]
        for n in partes: partes[n].append(intraday(m, n, 'day'))
        print(mes.date(), len(m), flush=True)
    mes = prox
for n, ps in partes.items():
    d = pd.concat(ps); d = d[~d.index.duplicated(keep='last')].sort_index()
    d[['open', 'high', 'low', 'close', 'volume']].to_csv(out / f'{n}m.csv.gz', float_format='%.2f')
    print(n, len(d), d.index[0], d.index[-1])
