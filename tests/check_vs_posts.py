"""Confere os valores calculados contra números citados nos posts do Raicher/Dollynho.

Rodar depois de existir data/ (cache da Bitstamp):  python -m tests.check_vs_posts
Diferenças pequenas (< 1-2%) são normais: eles citam valores arredondados e a vela ainda pode estar aberta.
"""
import json
from pathlib import Path

import pandas as pd

from raicher import fetch, indicators, timeframes

# (timeframe, data da vela (abertura, UTC), coluna, valor citado, fonte)
CITED = [
    ("1W", "2026-09-21", "ma77", 88800, "Raicher 21/09/2026: MA77 nos 88.8K"),
    ("1W", "2026-09-21", "ma49", 77800, "Raicher 21/09/2026: MA49 nos 77.8K"),
    ("1W", "2026-02-23", "ma231", 57000, "Raicher 02/03/2026: MA231 nos 57K"),
    ("1W", "2026-02-23", "ma343", 45800, "Raicher 02/03/2026: MA343 nos 45.8K"),
    ("1W", "2026-09-07", "ma7", 74300, "Raicher 14/09/2026: MA7 nos 74.3K"),
    ("1W", "2026-09-07", "ma21", 70400, "Raicher 14/09/2026: MA21 nos 70.4K"),
    ("1D", "2026-10-26", "ma77", 79000, "Dollynho 27/10/2026: MA77 ~79k"),
    ("2D", "2026-09-19", "ma200", 83200, "Dollynho 20/09/2026: MA200 do 2D ~83200"),
]


def main() -> None:
    cfg = json.loads(Path("raicher/config.json").read_text())
    raw = {"daily": fetch.fetch(cfg["pair"], 86400, fetch.BITSTAMP_START, Path("data/daily.csv.gz")),
           "minute": pd.DataFrame(columns=["open", "high", "low", "close", "volume"],
                                  index=pd.DatetimeIndex([], tz="UTC"))}
    d = raw["daily"]
    tfs = {"1D": timeframes.daily(d), "2D": timeframes.multi_day(d, 2), "1W": timeframes.weeks(d, 1)}
    tfs = {k: indicators.add_all(v, cfg) for k, v in tfs.items()}
    for tf, day, col, cited, src in CITED:
        df = tfs[tf]
        ts = pd.Timestamp(day, tz="UTC")
        row = df[df.index <= ts].iloc[-1]
        val = float(row[col])
        print(f"{tf:3} {str(row.name)[:10]} {col:6} calc={val:>10,.0f} citado={cited:>8,} dif={val / cited - 1:+.2%}  ({src})")


if __name__ == "__main__":
    main()
