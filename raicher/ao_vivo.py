"""Leitura AO VIVO (candle em formação) do 343m, 686m e 1D.

Só para consulta durante o candle. NÃO é fechamento: o método só vale no fechamento,
e nada aqui altera a branch dados nem os Logs.
Uso: python -m raicher.ao_vivo --out ao_vivo.json
"""
import argparse
import json
import math
from pathlib import Path

import pandas as pd

from . import fetch, indicators, timeframes

ROOT = Path(__file__).resolve().parent.parent
CAMPOS = ["ma7", "ema7", "ma21", "ema21", "ma77", "ma539", "ma686", "ma777", "ma1372", "ma1617", "ma343", "ma200"]


def _f(x):
    try:
        x = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) else round(x, 2)


def linha(row) -> dict:
    d = {k: _f(row.get(k)) for k in ["open", "high", "low", "close", "rsi", "rsi_ma", "stoch_k", "stoch_d"]}
    d["mas"] = {k: _f(row.get(k)) for k in CAMPOS if k in row}
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ao_vivo.json")
    ap.add_argument("--data", default=str(ROOT / "data"))
    args = ap.parse_args()

    cfg = json.loads((Path(__file__).parent / "config.json").read_text())
    now = pd.Timestamp.now(tz="UTC")
    raw = fetch.load_all(cfg["pair"], cfg["minute_history_days"], Path(args.data))
    tfs = timeframes.build(raw, cfg.get("intraday_anchor", "day"))

    out = {"gerado_em_utc": now.isoformat(), "fonte": "bitstamp btcusd",
           "aviso": "candle EM FORMAÇÃO: não é fechamento", "timeframes": {}}
    for tf in ["343m", "686m", "1D", "2D"]:
        df = indicators.add_all(tfs[tf], cfg)
        aberto = df.iloc[-1]
        fechado = df[df["end"] <= now].iloc[-1]
        out["timeframes"][tf] = {
            "candle_abre": str(df.index[-1]), "candle_fecha": str(aberto["end"]),
            "em_formacao": bool(aberto["end"] > now),
            "agora": linha(aberto),
            "ultimo_fechado": {"fechou": str(fechado["end"]), **linha(fechado)},
        }
    txt = json.dumps(out, ensure_ascii=False, indent=1)
    Path(args.out).write_text(txt)
    print(txt)


if __name__ == "__main__":
    main()
