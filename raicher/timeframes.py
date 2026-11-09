"""Monta os timeframes do método a partir de candles de 1 min e 1 dia.

Alinhamento (conferido contra datas de fechamento citadas nos posts):
- 1D fecha 00:00 UTC (21h Brasília).
- 1W começa segunda 00:00 UTC.
- 2W: limite de vela em 2025-12-22 (post do Raicher de 20/12/2025 "daqui 47h").
- 2D / 3D: ancorados no início de cada ano (o 2D bate com fechamentos de 23/11/2025, 06/02/2026 e 06/06/2026).
- 2M / 4M: ancorados em janeiro (4M fecha fim de abr, ago, dez).
- 343m / 686m: ancorados no início de cada dia UTC. CONFERIDO com prints do Dollynho de 08-09/11/2026:
  343m fecha 05:43, 11:26, 17:09, 22:52, 00:00 UTC; 686m fecha 11:26, 22:52, 00:00 UTC.
"""
import pandas as pd

AGG = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}
TWO_WEEK_REF = pd.Timestamp("2025-12-22", tz="UTC")


def _ohlc(df: pd.DataFrame, start: pd.Series, end: pd.Series) -> pd.DataFrame:
    g = df.assign(_s=start, _e=end).groupby("_s")
    out = g.agg(AGG)
    out["end"] = g["_e"].max()
    out.index.name = "time"
    return out.dropna(subset=["close"])


def intraday(minute: pd.DataFrame, n_min: int, anchor: str = "day") -> pd.DataFrame:
    t = minute.index.to_series()
    if anchor == "day":
        day = t.dt.floor("D")
        k = ((t - day) // pd.Timedelta(minutes=n_min))
        start = day + k * pd.Timedelta(minutes=n_min)
        end = (start + pd.Timedelta(minutes=n_min)).where(
            start + pd.Timedelta(minutes=n_min) <= day + pd.Timedelta(days=1), day + pd.Timedelta(days=1)
        )
    else:
        ref = pd.Timestamp("1970-01-01", tz="UTC")
        start = ref + ((t - ref) // pd.Timedelta(minutes=n_min)) * pd.Timedelta(minutes=n_min)
        end = start + pd.Timedelta(minutes=n_min)
    return _ohlc(minute, start, end)


def daily(d: pd.DataFrame) -> pd.DataFrame:
    out = d.copy()
    out["end"] = out.index + pd.Timedelta(days=1)
    return out


def multi_day(d: pd.DataFrame, n: int) -> pd.DataFrame:
    t = d.index.to_series()
    year = pd.to_datetime(t.dt.year.astype(str) + "-01-01", utc=True)
    doy = (t - year).dt.days
    start = year + pd.to_timedelta((doy // n) * n, unit="D")
    next_year = year + pd.offsets.DateOffset(years=1)
    raw_end = start + pd.Timedelta(days=n)
    end = raw_end.where(raw_end <= next_year, next_year)
    return _ohlc(d, start, end)


def weeks(d: pd.DataFrame, n: int) -> pd.DataFrame:
    t = d.index.to_series()
    ref = TWO_WEEK_REF if n > 1 else pd.Timestamp("2024-01-01", tz="UTC")  # 2024-01-01 é segunda
    start = ref + ((t - ref) // pd.Timedelta(weeks=n)) * pd.Timedelta(weeks=n)
    end = start + pd.Timedelta(weeks=n)
    return _ohlc(d, start, end)


def months(d: pd.DataFrame, n: int) -> pd.DataFrame:
    t = d.index.to_series()
    y, m = t.dt.year, t.dt.month
    m0 = ((m - 1) // n) * n + 1
    start = pd.to_datetime(pd.DataFrame({"year": y, "month": m0, "day": 1})).dt.tz_localize("UTC")
    end = start + pd.offsets.DateOffset(months=n)
    return _ohlc(d, start, end)


def build(raw: dict, anchor: str = "day") -> dict:
    d = raw["daily"]
    m = raw["minute"]
    return {
        "343m": intraday(m, 343, anchor),
        "686m": intraday(m, 686, anchor),
        "1D": daily(d),
        "2D": multi_day(d, 2),
        "3D": multi_day(d, 3),
        "1W": weeks(d, 1),
        "2W": weeks(d, 2),
        "1M": months(d, 1),
        "2M": months(d, 2),
        "4M": months(d, 4),
    }


def closed_only(df: pd.DataFrame, now: pd.Timestamp) -> pd.DataFrame:
    """Remove a vela em formação: só fechamento conta."""
    return df[df["end"] <= now]
