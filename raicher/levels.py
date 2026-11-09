"""Linhas horizontais do RSI calculadas automaticamente.

O Raicher desenha níveis onde o RSI virou várias vezes na história. Aqui: acha os pivôs (topos e fundos
locais) do RSI, faz uma densidade dos valores e pega os picos mais fortes, com distância mínima entre eles.
"""
import numpy as np
import pandas as pd


def pivots(r: pd.Series, w: int) -> np.ndarray:
    v = r.to_numpy(dtype=float)
    vals = []
    for i in range(w, len(v) - w):
        win = v[i - w:i + w + 1]
        if np.isnan(win).any():
            continue
        if v[i] == win.max() or v[i] == win.min():
            vals.append(v[i])
    return np.array(vals)


def auto_levels(r: pd.Series, k: int = 6, bandwidth: float = 1.0, min_gap: float = 4.0) -> list:
    r = r.dropna()
    if len(r) < 60:
        return []
    w = 3 if len(r) < 300 else 5
    p = pivots(r, w)
    if len(p) < 8:
        return []
    grid = np.arange(5, 95.01, 0.05)
    dens = np.exp(-0.5 * ((grid[:, None] - p[None, :]) / bandwidth) ** 2).sum(axis=1)
    peaks = [i for i in range(1, len(grid) - 1) if dens[i] >= dens[i - 1] and dens[i] >= dens[i + 1]]
    peaks.sort(key=lambda i: dens[i], reverse=True)
    chosen = []
    for i in peaks:
        if all(abs(grid[i] - grid[j]) >= min_gap for j in chosen):
            chosen.append(i)
        if len(chosen) == k:
            break
    total = dens[chosen].sum() if chosen else 1
    return sorted(
        ({"value": round(float(grid[i]), 2), "strength": round(float(dens[i] / total), 3)} for i in chosen),
        key=lambda x: x["value"],
    )


def label(levels: list, rsi_now: float) -> list:
    """Nomeia no estilo do método: acima do RSI atual = resistência, abaixo = suporte; >50 Superior, <50 Inferior."""
    out = []
    for lv in levels:
        side = "Resistencia" if lv["value"] > rsi_now else "Suporte"
        zone = "Superior" if lv["value"] >= 50 else "Inferior"
        out.append({**lv, "name": f"{side} {zone}"})
    return out


def calibration(levels: list, known: dict) -> list:
    """Compara os níveis automáticos com os valores citados nos posts."""
    res = []
    for name, val in known.items():
        if not levels:
            res.append({"known": name, "value": val, "nearest_auto": None, "diff": None})
            continue
        near = min(levels, key=lambda x: abs(x["value"] - val))
        res.append({"known": name, "value": val, "nearest_auto": near["value"], "diff": round(near["value"] - val, 2)})
    return res
