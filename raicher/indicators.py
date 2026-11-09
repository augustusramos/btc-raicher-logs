"""Indicadores com as mesmas fórmulas do TradingView (ta.sma, ta.ema, ta.rma, ta.rsi, ta.stoch)."""
import numpy as np
import pandas as pd


def sma(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n, min_periods=n).mean()


def _seeded(s: pd.Series, n: int, alpha: float) -> pd.Series:
    """Média exponencial semeada com a SMA dos n primeiros valores (como o TradingView)."""
    v = s.to_numpy(dtype=float)
    out = np.full(len(v), np.nan)
    first = np.argmax(~np.isnan(v)) if np.any(~np.isnan(v)) else len(v)
    if len(v) - first < n:
        return pd.Series(out, index=s.index)
    i0 = first + n - 1
    out[i0] = np.nanmean(v[first:i0 + 1])
    for i in range(i0 + 1, len(v)):
        x = v[i]
        out[i] = out[i - 1] if np.isnan(x) else alpha * x + (1 - alpha) * out[i - 1]
    return pd.Series(out, index=s.index)


def ema(s: pd.Series, n: int) -> pd.Series:
    return _seeded(s, n, 2.0 / (n + 1))


def rma(s: pd.Series, n: int) -> pd.Series:
    return _seeded(s, n, 1.0 / n)


def rsi(close: pd.Series, n: int = 14) -> pd.Series:
    ch = close.diff()
    up = rma(ch.clip(lower=0), n)
    dn = rma((-ch).clip(lower=0), n)
    rs = up / dn
    out = 100 - 100 / (1 + rs)
    out[dn == 0] = 100
    out[(up == 0) & (dn == 0)] = np.nan
    return out


def stoch_rsi(r: pd.Series, stoch_len: int = 14, k: int = 3, d: int = 3):
    lo = r.rolling(stoch_len, min_periods=stoch_len).min()
    hi = r.rolling(stoch_len, min_periods=stoch_len).max()
    raw = 100 * (r - lo) / (hi - lo)
    kk = sma(raw, k)
    dd = sma(kk, d)
    return kk, dd


def add_all(df: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    out = df.copy()
    c = out["close"]
    for n in cfg["mas"]:
        out[f"ma{n}"] = sma(c, n)
    for n in cfg["emas"]:
        out[f"ema{n}"] = ema(c, n)
    out["rsi"] = rsi(c, cfg["rsi_length"])
    ma_fn = ema if cfg.get("rsi_ma_type", "SMA").upper() == "EMA" else sma
    out["rsi_ma"] = ma_fn(out["rsi"], cfg["rsi_ma_length"])
    st = cfg["stoch"]
    out["stoch_k"], out["stoch_d"] = stoch_rsi(out["rsi"], st["stoch_length"], st["k"], st["d"])
    if len(out) >= 700:
        out["pi_111"] = sma(c, 111)
        out["pi_350x2"] = 2 * sma(c, 350)
    return out
