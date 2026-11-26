"""RSI/Stoch do 2D ABERTO (intracandle) na mínima, no fechamento e na máxima do dia.

Uso: python tools/bilau_intracandle.py --dados dados
Na véspera do fechamento do 2D (21:00 de dia sem fechamento do 2D), o 2D aberto = o candle diário que acabou
de fechar (abriu às 21:00 de ontem). Diz se o BBB foi tocado durante o dia (Dollynho 25/11: "quem aproveitou
conseguiu comprar o BBB durante o dia"). BBB = preço < MA200 2D + RSI 2D < 25,78 + Stoch K 2D < 20,44.
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from raicher.indicators import rsi, sma, stoch_rsi  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", default="dados")
    a = ap.parse_args()
    dados = Path(a.dados)
    cfg = json.loads((Path(__file__).resolve().parents[1] / "raicher" / "config.json").read_text())["bbb"]
    df = pd.read_csv(dados / "ohlc" / "2D.csv.gz")
    df["time"] = pd.to_datetime(df["time"], utc=True)
    d1 = json.loads((dados / "1D.json").read_text())
    aberto = pd.to_datetime(d1["bar_open"], utc=True)  # início do candle diário que fechou
    fechados = df[df["time"] < aberto]
    if len(fechados) and fechados["time"].iloc[-1] + pd.Timedelta(days=2) != aberto:
        print("AVISO: o 2D não abriu junto com este Diário (hoje é dia de FECHAMENTO do 2D?) — use 2D.json.")
    c = fechados["close"].astype(float).reset_index(drop=True)
    ma200 = sma(pd.concat([c, pd.Series([d1["close"]])], ignore_index=True), cfg["ma"]).iloc[-1]
    out = {}
    for nome in ("low", "close", "high"):
        px = float(d1[nome])
        s = pd.concat([c, pd.Series([px])], ignore_index=True)
        r = rsi(s)
        k, dd = stoch_rsi(r)
        bbb = px < ma200 and r.iloc[-1] < cfg["rsi"] and k.iloc[-1] < cfg["stoch_k"]
        out[nome] = {"preco": round(px), "rsi_2d": round(float(r.iloc[-1]), 2), "stoch_k_2d": round(float(k.iloc[-1]), 2),
                     "stoch_d_2d": round(float(dd.iloc[-1]), 2), "bbb": bool(bbb)}
    out["ma200_2d"] = round(float(ma200))
    out["bbb_durante_o_dia"] = out["low"]["bbb"]
    out["fecha_2d"] = str((aberto + pd.Timedelta(days=2)).tz_convert("America/Sao_Paulo"))
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
