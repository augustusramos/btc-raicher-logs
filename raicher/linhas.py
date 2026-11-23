"""Detector de linhas de tendencia no estilo do Dollynho.

Achado da calibracao (23/11/2026): as linhas que ele desenha no 343 sao linhas de tendencia
LONGAS, em escala log, que ligam topos e fundos do Diario de meses (ate anos) atras e sao
estendidas ate hoje (ex.: Verde Tracejada toca 6 pivos desde jul/2025; Azul Pontilhada e o
teto dos topos de jun-ago/2026). Este modulo procura retas (em log do preco) que passam por
varios pivos do Diario e estao perto do preco atual.

Uso:
  python -m raicher.linhas --dados dados            # lista as linhas detectadas
  python -m raicher.linhas --dados dados --comparar calibracao/linhas_dollynho.json
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ORIGEM = pd.Timestamp("2026-01-01")


def _dias(ts) -> np.ndarray:
    ts = pd.DatetimeIndex(ts)
    if ts.tz is not None:
        ts = ts.tz_convert("America/Sao_Paulo").tz_localize(None)
    return np.asarray((ts - ORIGEM).total_seconds() / 86400.0)


def pivos(df: pd.DataFrame, janela: int) -> list:
    H, L = df["high"].values, df["low"].values
    n = len(df)
    out = []
    for i in range(janela, n - 1):
        lo, hi = max(0, i - janela), min(n, i + janela + 1)
        if H[i] == H[lo:hi].max():
            out.append((i, "H", H[i]))
        if L[i] == L[lo:hi].min():
            out.append((i, "L", L[i]))
    return out


def detectar(df: pd.DataFrame, agora: pd.Timestamp, preco: float, janela: int = 5,
             tol: float = 0.005, min_toques: int = 3, faixa: float = 0.2,
             min_dias: int = 20, max_linhas: int = 12) -> list:
    """Retas em log(preco) por pares de pivos, pontuadas pelo numero de pivos tocados."""
    t = _dias(df.index) + 0.875  # o Diario fecha 21:00 de Brasilia
    pv = pivos(df, janela)
    pt = np.array([t[i] for i, _, _ in pv])
    pp = np.log(np.array([p for _, _, p in pv]))
    tipo = np.array([k for _, k, _ in pv])
    x_now = float(_dias([agora])[0])
    cands = []
    for a in range(len(pv)):
        for b in range(a + 1, len(pv)):
            if pt[b] - pt[a] < min_dias:
                continue
            m = (pp[b] - pp[a]) / (pt[b] - pt[a])
            v_now = np.exp(pp[a] + m * (x_now - pt[a]))
            if abs(v_now / preco - 1) > faixa:
                continue
            dev = np.abs(pp - (pp[a] + m * (pt - pt[a])))
            hit = dev < np.log1p(tol)
            k = int(hit.sum())
            if k < min_toques:
                continue
            cands.append({
                "valor_hoje": float(v_now),
                "inclinacao_pct_dia": float(np.expm1(m) * 100),
                "toques": k,
                "toques_topo": int((hit & (tipo == "H")).sum()),
                "toques_fundo": int((hit & (tipo == "L")).sum()),
                "primeiro": str(df.index[pv[int(np.argmax(hit))][0]].date()),
                "ultimo": str(df.index[pv[len(hit) - 1 - int(np.argmax(hit[::-1]))][0]].date()),
                "_m": m, "_a": (pt[a], pp[a]),
            })
    cands.sort(key=lambda c: (-c["toques"], abs(c["valor_hoje"] / preco - 1)))
    escolhidas = []
    for c in cands:
        dup = any(abs(c["valor_hoje"] / e["valor_hoje"] - 1) < 0.006 and
                  abs(c["inclinacao_pct_dia"] - e["inclinacao_pct_dia"]) < 0.08 for e in escolhidas)
        if not dup:
            escolhidas.append(c)
        if len(escolhidas) >= max_linhas:
            break
    for e in escolhidas:
        e.pop("_m"); e.pop("_a")
    return sorted(escolhidas, key=lambda e: -e["valor_hoje"])


def valor_gabarito(linha: dict, agora: pd.Timestamp) -> tuple:
    (d1, p1), (d2, p2) = linha["p1"], linha["p2"]
    x1, x2 = _dias([pd.Timestamp(d1)])[0], _dias([pd.Timestamp(d2)])[0]
    m = (np.log(p2) - np.log(p1)) / (x2 - x1)
    x = _dias([agora])[0]
    return float(np.exp(np.log(p1) + m * (x - x1))), float(np.expm1(m) * 100)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", default="dados")
    ap.add_argument("--comparar")
    ap.add_argument("--janela", type=int, default=5)
    a = ap.parse_args()
    df = pd.read_csv(Path(a.dados) / "ohlc" / "1D.csv.gz", index_col=0, parse_dates=True)
    df = df[df.index >= df.index[-1] - pd.Timedelta(days=900)]
    m343 = pd.read_csv(Path(a.dados) / "ohlc" / "343m.csv.gz", index_col=0, parse_dates=True)
    agora = m343.index[-1].tz_convert("America/Sao_Paulo").tz_localize(None)
    preco = float(m343["close"].iloc[-1])
    linhas = detectar(df, agora, preco, janela=a.janela)
    out = {"agora": str(agora), "preco": preco, "linhas": linhas}
    if a.comparar:
        g = json.loads(Path(a.comparar).read_text())["linhas"]
        comp = {}
        for nome, ln in g.items():
            v, s = valor_gabarito(ln, agora)
            best = min(linhas, key=lambda e: abs(e["valor_hoje"] / v - 1) + abs(e["inclinacao_pct_dia"] - s) / 10) if linhas else None
            comp[nome] = {"dele_hoje": round(v), "dele_incl_pct_dia": round(s, 3),
                          "nossa_hoje": round(best["valor_hoje"]) if best else None,
                          "nossa_incl_pct_dia": round(best["inclinacao_pct_dia"], 3) if best else None,
                          "erro_pct": round((best["valor_hoje"] / v - 1) * 100, 2) if best else None,
                          "toques": best["toques"] if best else None}
        out["comparacao"] = comp
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
