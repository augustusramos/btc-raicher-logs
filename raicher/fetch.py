"""Download e cache de candles da Bitstamp (mesma fonte dos gráficos do Raicher/Dollynho)."""
import time
from pathlib import Path

import pandas as pd
import requests

API = "https://www.bitstamp.net/api/v2/ohlc/{pair}/"
LIMIT = 1000
BITSTAMP_START = pd.Timestamp("2011-08-18", tz="UTC")


def _get(pair: str, step: int, start: int) -> list:
    for attempt in range(5):
        try:
            r = requests.get(
                API.format(pair=pair),
                params={"step": step, "limit": LIMIT, "start": start},
                timeout=30,
                headers={"User-Agent": "btc-raicher-logs"},
            )
            r.raise_for_status()
            return r.json()["data"]["ohlc"]
        except Exception:  # noqa: BLE001
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))
    return []


def _to_df(rows: list) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])
    df = pd.DataFrame(rows)
    df["time"] = pd.to_datetime(df["timestamp"].astype(int), unit="s", utc=True)
    df = df.set_index("time")[["open", "high", "low", "close", "volume"]].astype(float)
    return df


def fetch(pair: str, step: int, since: pd.Timestamp, cache: Path) -> pd.DataFrame:
    """Baixa candles de `step` segundos desde `since`, reaproveitando o cache em disco."""
    cached = None
    if cache.exists():
        cached = pd.read_csv(cache, index_col=0, parse_dates=True)
        cached.index = pd.to_datetime(cached.index, utc=True)
        cached = cached[cached.index >= since]
        if not cached.empty and cached.index[0] > since + pd.Timedelta(days=2):
            cached = None  # histórico pedido aumentou: baixa tudo de novo
    start = since if cached is None or cached.empty else cached.index[-2]  # refaz a última vela (pode estar aberta)
    start_s = int(start.timestamp())
    now_s = int(time.time())
    parts = []
    while start_s < now_s:
        rows = _get(pair, step, start_s)
        if not rows:
            break
        part = _to_df(rows)
        parts.append(part)
        last = int(part.index[-1].timestamp())
        if last <= start_s:
            break
        start_s = last + step
        time.sleep(0.15)
    frames = [f for f in [cached, *parts] if f is not None and not f.empty]
    df = pd.concat(frames)
    df = df[~df.index.duplicated(keep="last")].sort_index()
    cache.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache, compression="gzip" if cache.suffix == ".gz" else None)
    return df


def load_all(pair: str, minute_days: int, data_dir: Path) -> dict:
    daily = fetch(pair, 86400, BITSTAMP_START, data_dir / "daily.csv.gz")
    since_min = pd.Timestamp.now(tz="UTC").floor("D") - pd.Timedelta(days=minute_days)
    minute = fetch(pair, 60, since_min, data_dir / "minute.csv.gz")
    return {"daily": daily, "minute": minute}
