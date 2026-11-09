"""Ponto de entrada: baixa dados, calcula tudo e grava out/ (JSON + gráficos + alertas).

Uso:
  python -m raicher.run                 # dados reais da Bitstamp
  python -m raicher.run --synthetic     # dados falsos, só para testar o código
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import analyze, chart, indicators, timeframes

ROOT = Path(__file__).resolve().parent.parent


def synthetic(now: pd.Timestamp) -> dict:
    rng = np.random.default_rng(7)
    days = pd.date_range(pd.Timestamp("2011-08-18", tz="UTC"), now.floor("D"), freq="D")
    lr = rng.normal(0.0018, 0.04, len(days))
    close = 10 * np.exp(np.cumsum(lr))
    op = np.r_[close[0], close[:-1]]
    hi = np.maximum(op, close) * (1 + rng.uniform(0, 0.03, len(days)))
    lo = np.minimum(op, close) * (1 - rng.uniform(0, 0.03, len(days)))
    daily = pd.DataFrame({"open": op, "high": hi, "low": lo, "close": close, "volume": 1.0}, index=days)
    mins = pd.date_range(now.floor("D") - pd.Timedelta(days=200), now.floor("min"), freq="min")
    mlr = rng.normal(0, 0.0008, len(mins))
    mc = close[-200] * np.exp(np.cumsum(mlr))
    mo = np.r_[mc[0], mc[:-1]]
    minute = pd.DataFrame({"open": mo, "high": np.maximum(mo, mc) * 1.0003, "low": np.minimum(mo, mc) * 0.9997,
                           "close": mc, "volume": 1.0}, index=mins)
    return {"daily": daily, "minute": minute}


def clean(o):
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if np.isnan(o) else round(float(o), 4)
    return o


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--synthetic", action="store_true")
    ap.add_argument("--out", default=str(ROOT / "out"))
    ap.add_argument("--data", default=str(ROOT / "data"))
    ap.add_argument("--charts", default="changed", choices=["changed", "all", "none"])
    args = ap.parse_args()

    cfg = json.loads((Path(__file__).parent / "config.json").read_text())
    now = pd.Timestamp.now(tz="UTC")
    out = Path(args.out)
    (out / "charts").mkdir(parents=True, exist_ok=True)

    if args.synthetic:
        raw = synthetic(now)
    else:
        from . import fetch
        raw = fetch.load_all(cfg["pair"], cfg["minute_history_days"], Path(args.data))

    tfs_raw = timeframes.build(raw, cfg.get("intraday_anchor", "day"))
    prev_state = {}
    latest_path = out / "latest.json"
    if latest_path.exists():
        prev_state = json.loads(latest_path.read_text()).get("timeframes", {})

    tfs, states, changed = {}, {}, []
    for tf, df in tfs_raw.items():
        df = timeframes.closed_only(df, now)
        if len(df) < 30:
            continue
        df = indicators.add_all(df, cfg)
        tfs[tf] = df
        st = analyze.tf_state(tf, df, cfg)
        states[tf] = st
        if prev_state.get(tf, {}).get("bar_open") != st["bar_open"]:
            changed.append(tf)
        (out / f"{tf}.json").write_text(json.dumps(clean(st), ensure_ascii=False, indent=1))

    for tf in tfs:
        if args.charts == "all" or (args.charts == "changed" and tf in changed):
            t = cfg["timeframes"][tf]
            chart.plot(tf, tfs[tf], states[tf], out / "charts" / f"{tf}.png", t["chart_bars"], t["log_scale"])

    sets = analyze.setups(tfs, states, cfg)
    latest = {
        "generated_at": now.isoformat(),
        "source": "synthetic" if args.synthetic else "bitstamp btcusd",
        "new_closes": changed,
        "setups": sets,
        "timeframes": states,
    }
    latest_path.write_text(json.dumps(clean(latest), ensure_ascii=False, indent=1))

    # Alertas novos (dedupe por timeframe + setup + vela)
    state_path = out / "alerts_state.json"
    seen = set(json.loads(state_path.read_text())) if state_path.exists() else set()
    new = []
    for s in sets:
        if not (s["active"] or s.get("near")):
            continue
        bar = states[s["tf"]]["bar_open"]
        key = f"{s['setup']}|{'ATIVO' if s['active'] else 'PERTO'}|{bar}"
        if key not in seen:
            seen.add(key)
            new.append({"key": key, **s})
    state_path.write_text(json.dumps(sorted(seen)[-500:], indent=0))
    (out / "alerts_new.json").write_text(json.dumps(clean(new), ensure_ascii=False, indent=1))

    if (out / "history").exists() or "1D" in changed:
        (out / "history").mkdir(exist_ok=True)
        if "1D" in changed:
            day = states["1D"]["bar_open"][:10]
            (out / "history" / f"{day}.json").write_text(json.dumps(clean(latest), ensure_ascii=False))

    if not args.synthetic and (Path(args.data) / "daily.csv.gz").exists():
        import shutil
        shutil.copy(Path(args.data) / "daily.csv.gz", out / "daily.csv.gz")

    print(f"ok | fechamentos novos: {changed} | alertas novos: {len(new)}")


if __name__ == "__main__":
    main()
