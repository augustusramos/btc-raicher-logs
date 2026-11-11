"""Lê o estado de cada timeframe e detecta os eventos/setups do método."""
import math

import numpy as np
import pandas as pd

from . import levels as lv


def _f(x, nd=2):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    return round(float(x), nd)


def _side(a, b):
    if a is None or b is None or np.isnan(a) or np.isnan(b):
        return 0
    return 1 if a > b else -1


def cross_event(x: pd.Series, y) -> dict:
    """Evento da última vela fechada de x contra y (série ou número), no vocabulário do método."""
    yy = y if isinstance(y, pd.Series) else pd.Series(y, index=x.index)
    if len(x) < 3:
        return {"pos": None, "event": None}
    s = [_side(x.iloc[i], yy.iloc[i]) for i in (-3, -2, -1)]
    pos = "ACIMA" if s[2] > 0 else "ABAIXO" if s[2] < 0 else None
    if 0 in s:
        return {"pos": pos, "event": None}
    if s[2] != s[1] and s[1] != s[0]:
        ev = "ANULOU (voltou " + pos + ")"
    elif s[2] != s[1]:
        ev = "ROMPEU PRA CIMA (confirma/anula na proxima vela)" if s[2] > 0 else "PERDEU (confirma/anula na proxima vela)"
    elif s[1] != s[0]:
        ev = "CONFIRMOU " + pos
    else:
        ev = None
    return {"pos": pos, "event": ev}


def bars_since(mask: pd.Series):
    idx = np.flatnonzero(mask.to_numpy())
    return None if len(idx) == 0 else int(len(mask) - 1 - idx[-1])


def tf_state(tf: str, df: pd.DataFrame, cfg: dict) -> dict:
    last = df.iloc[-1]
    prev = df.iloc[-2]
    close = float(last["close"])
    st = {
        "tf": tf,
        "bar_open": df.index[-1].isoformat(),
        "bar_close": pd.Timestamp(last["end"]).isoformat(),
        "open": _f(last["open"]), "high": _f(last["high"]), "low": _f(last["low"]), "close": _f(close),
        "change_pct": _f((close / prev["close"] - 1) * 100),
        "bars_available": int(len(df)),
    }

    # Médias
    mas = {}
    for col in [c for c in df.columns if c.startswith(("ma", "ema"))]:
        val = last[col]
        if pd.isna(val):
            continue
        ev = cross_event(df["close"], df[col])
        tol = val * 0.0015  # "toque perfeito": pavio a até 0,15% da média conta como toque
        touched = bool(last["low"] - tol <= val <= last["high"] + tol)
        mas[col] = {"value": _f(val), "dist_pct": _f((close / val - 1) * 100), "touched_wick": touched, **ev}
    st["mas"] = mas
    below = {k: v for k, v in mas.items() if v["value"] < close}
    above = {k: v for k, v in mas.items() if v["value"] > close}
    st["support_mas"] = sorted(below, key=lambda k: -below[k]["value"])[:3]
    st["resistance_mas"] = sorted(above, key=lambda k: above[k]["value"])[:3]
    # Escada completa (para alvos e stops no estilo do Dollynho: alvo = média mais à frente, stop = média logo atrás)
    st["ladder_below"] = [[k, below[k]["value"]] for k in sorted(below, key=lambda k: -below[k]["value"])]
    st["ladder_above"] = [[k, above[k]["value"]] for k in sorted(above, key=lambda k: above[k]["value"])]
    st["wick_touches"] = [k for k, v in mas.items() if v["touched_wick"]]

    # Cruzamentos da MA7 com as médias que o Dollynho/Raicher citam ("MA7 cruzando bearish a MA343", "7x21", "7x343")
    crosses = []
    if "ma7" in df:
        m7 = df["ma7"]
        for n in (21, 49, 77, 200, 231, 343, 539, 686, 1372, 1617):
            col = f"ma{n}"
            if col not in df or pd.isna(df[col].iloc[-1]):
                continue
            ev = cross_event(m7, df[col])
            gap = (m7 - df[col]) / df[col] * 100
            g_now, g_prev = float(gap.iloc[-1]), float(gap.iloc[-4]) if len(gap) > 4 else float("nan")
            converging = (not math.isnan(g_prev)) and abs(g_now) < abs(g_prev)
            near = abs(g_now) <= 1.0 and converging
            if ev["event"] or near:
                if ev["event"]:
                    direction = "bullish" if ev["pos"] == "ACIMA" else "bearish"
                else:  # ainda não cruzou: MA7 acima e se aproximando = cruzando para baixo
                    direction = "bearish" if g_now > 0 else "bullish"
                crosses.append({"par": f"MA7 x MA{n}", "event": ev["event"], "ma7_pos": ev["pos"],
                                "gap_pct": _f(g_now), "cruzando": near and not ev["event"],
                                "direcao": direction})
    st["ma_crosses"] = crosses

    # RSI
    r = df["rsi"]
    rnow = float(r.iloc[-1])
    auto = lv.auto_levels(r)
    known = {**cfg.get("rsi_template", {}), **cfg["known_rsi_levels"].get(tf, {})}
    labeled = lv.label(auto, rnow)
    lowest_inf = min((x["value"] for x in auto if x["value"] < 50), default=30.0)
    st["rsi"] = {
        "value": _f(rnow), "ma": _f(df["rsi_ma"].iloc[-1]),
        "vs_ma": cross_event(r, df["rsi_ma"]),
        "vs_50": cross_event(r, 50.0),
        "levels_auto": labeled,
        "levels_known": known,
        "level_events": {f"{x['value']}": cross_event(r, x["value"]) for x in auto},
        "nearest_above": min((x for x in labeled if x["value"] > rnow), key=lambda x: x["value"], default=None),
        "nearest_below": max((x for x in labeled if x["value"] < rnow), key=lambda x: x["value"], default=None),
        "reset_level": lowest_inf,
        "bars_since_reset": bars_since(r <= lowest_inf),
        "calibration": lv.calibration(auto, cfg["known_rsi_levels"].get(tf, {})),
        "known_level_events": {name: cross_event(r, val) for name, val in known.items()},
        "known_nearest_above": min(((n, v) for n, v in known.items() if v > rnow), key=lambda x: x[1], default=None),
        "known_nearest_below": max(((n, v) for n, v in known.items() if v < rnow), key=lambda x: x[1], default=None),
        "in_traps_zone": bool(cfg["traps_zone"][0] <= rnow <= cfg["traps_zone"][1]) if "traps_zone" in cfg else None,
    }
    # Divergência simples: preço fez low menor e RSI low maior nas últimas 30 velas (ou o contrário)
    win = df.iloc[-30:]
    if len(win) >= 30:
        a, b = win.iloc[:15], win.iloc[15:]
        bull = b["low"].min() < a["low"].min() and b["rsi"].min() > a["rsi"].min()
        bear = b["high"].max() > a["high"].max() and b["rsi"].max() < a["rsi"].max()
        st["rsi"]["divergence"] = "bullish" if bull else "bearish" if bear else None

    # StochRSI
    k, d = df["stoch_k"], df["stoch_d"]
    kn, dn = float(k.iloc[-1]), float(d.iloc[-1])
    kc = cross_event(k, d)
    st["stoch"] = {
        "k": _f(kn), "d": _f(dn),
        "cross": ("bullish" if kc["pos"] == "ACIMA" else "bearish") if kc["event"] and kc["event"].startswith(("ROMPEU", "PERDEU")) else None,
        "k_vs_d": kc,
        "zone": "ZERADO" if kn <= 5 else "abaixo de 20" if kn < 20 else "TETO" if kn >= 95 else "acima de 80" if kn > 80 else "range 20-80",
        "levels": {name: cross_event(k, val) for name, val in cfg.get("stoch_levels", {"20": 20.0, "80": 80.0}).items()},
    }
    st["horizontal_levels"] = {n: {"value": v, "dist_pct": _f((close / v - 1) * 100), **cross_event(df["close"], float(v))}
                               for n, v in cfg.get("horizontal_levels", {}).items()}
    if "pi_111" in df and not pd.isna(last.get("pi_111", np.nan)):
        st["picycle_ratio_pct"] = _f(last["pi_111"] / last["pi_350x2"] * 100)
    return st


def setups(tfs: dict, states: dict, cfg: dict) -> list:
    out = []
    a = cfg["alerts"]

    # BBB no 2D
    if "2D" in tfs:
        d2 = tfs["2D"].iloc[-1]
        b = cfg["bbb"]
        ma = d2.get(f"ma{b['ma']}")
        c1 = bool(d2["close"] < ma) if not pd.isna(ma) else False
        c2 = bool(d2["rsi"] < b["rsi"])
        c3 = bool(d2["stoch_k"] < b["stoch_k"])
        out.append({"tf": "2D", "setup": "BBB (2D)", "active": c1 and c2 and c3,
                    "near": bool(c1 and d2["rsi"] < b["rsi"] + 5 and d2["stoch_k"] < 30),
                    "detail": {"abaixo_ma200": c1, "rsi": _f(d2["rsi"]), "rsi_lt_26_21": c2,
                               "stoch_k": _f(d2["stoch_k"]), "stoch_lt_20_44": c3}})
        x77 = cross_event(tfs["2D"]["ma77"], tfs["2D"]["ma200"])
        out.append({"tf": "2D", "setup": "2D MA77 x MA200", "active": bool(x77["event"]), "near": False,
                    "detail": {"ma77_vs_ma200": x77["pos"], "event": x77["event"]}})

    # Agulhada
    for tf, trio in cfg["agulhada"].items():
        if tf not in tfs:
            continue
        df = tfs[tf]
        f, m, s = (df[f"ma{n}"] for n in trio)
        ok = (f > m) & (m > s)
        recent = bool(ok.iloc[-1] and not ok.iloc[-4:-1].all())
        trio_now = [float(x.iloc[-1]) for x in (f, m, s)]
        spread = (max(trio_now) - min(trio_now)) / float(df["close"].iloc[-1]) * 100
        det = {"medias": trio, "ordem_7_21_longa": bool(ok.iloc[-1]), "squeeze_pct": _f(spread)}
        starts = np.flatnonzero((ok & ~ok.shift(1, fill_value=False)).to_numpy())
        if len(starts):
            i0 = starts[-1]
            det["ultima_agulhada"] = df.index[i0].date().isoformat()
            c0 = float(df["close"].iloc[i0])
            det["drawdown_desde_pct"] = _f((float(df["low"].iloc[i0:].min()) / c0 - 1) * 100)
        out.append({"tf": tf, "setup": f"Agulhada {tf} ({'/'.join(map(str, trio))})", "active": recent,
                    "near": (not ok.iloc[-1]) and spread < a["agulhada_squeeze_pct"], "detail": det})

    # BTFD (MonkeyStrategy)
    for tf, n in cfg["btfd"].items():
        m = states.get(tf, {}).get("mas", {}).get(f"ma{n}")
        if not m:
            continue
        near = abs(m["dist_pct"]) <= a["ma343_touch_pct"] * 2
        out.append({"tf": tf, "setup": f"BTFD MA{n} {tf}", "active": m["touched_wick"] or near, "near": abs(m["dist_pct"]) <= 4,
                    "detail": m})

    # Matrix do 343
    for tf in a["timeframes_ma343"]:
        m = states.get(tf, {}).get("mas", {}).get("ma343")
        if not m:
            continue
        hit = m["touched_wick"] or abs(m["dist_pct"]) <= a["ma343_touch_pct"]
        out.append({"tf": tf, "setup": f"MA343 {tf}", "active": hit, "near": abs(m["dist_pct"]) <= 3 * a["ma343_touch_pct"],
                    "detail": m})

    # Ciclo do Semanal: resets do RSI abaixo de 30
    if "1W" in tfs:
        r = tfs["1W"]["rsi"]
        below = r < 30
        entries = int((below & ~below.shift(1, fill_value=False)).sum())
        out.append({"tf": "1W", "setup": "Reset RSI < 30 (1W)", "active": bool(below.iloc[-1] and not below.iloc[-2]),
                    "near": float(r.iloc[-1]) < 35, "detail": {"rsi": _f(r.iloc[-1]), "resets_na_historia": entries}})
    return out
