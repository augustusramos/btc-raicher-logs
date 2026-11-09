"""Gráfico no estilo dos prints do Raicher/Dollynho: fundo preto, médias coloridas, RSI com níveis e StochRSI."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

MA_COLORS = {
    7: "#2ecc40", 21: "#ff4136", 49: "#b10dc9", 77: "#ff851b", 200: "#ff2d55", 231: "#cccccc",
    343: "#ffdc00", 539: "#39cccc", 686: "#f012be", 777: "#c71585", 1372: "#0074d9", 1617: "#ffffff",
}


def plot(tf: str, df, state: dict, path, bars: int = 200, log_scale: bool = False) -> None:
    d = df.iloc[-bars:]
    x = np.arange(len(d))
    plt.style.use("dark_background")
    fig, (ax, ar, ak) = plt.subplots(3, 1, figsize=(14, 10), sharex=True,
                                     gridspec_kw={"height_ratios": [3.2, 1.3, 1]})
    fig.patch.set_facecolor("black")
    for a in (ax, ar, ak):
        a.set_facecolor("black")
        a.grid(alpha=0.08)
        a.yaxis.tick_right()

    up = d["close"] >= d["open"]
    col = np.where(up, "#26ff7a", "#ff3c8e")
    ax.vlines(x, d["low"], d["high"], color=col, linewidth=0.8)
    ax.bar(x, (d["close"] - d["open"]).abs().clip(lower=d["close"] * 1e-4), bottom=np.minimum(d["open"], d["close"]),
           color=col, width=0.7)

    lo, hi = d["low"].min(), d["high"].max()
    for n, c in MA_COLORS.items():
        name = f"ma{n}"
        if name not in d or d[name].isna().all():
            continue
        last = d[name].iloc[-1]
        ls = "--" if n == 200 else "-"
        ax.plot(x, d[name], color=c, linewidth=1.3 if n in (7, 21, 49, 77, 343) else 1.0, linestyle=ls)
        if lo * 0.7 <= last <= hi * 1.3:
            ax.annotate(f"MA{n} {last:,.0f}", (x[-1], last), xytext=(6, 0), textcoords="offset points",
                        color=c, fontsize=8, va="center")
    for e in ("ema7", "ema77", "ema343"):
        if e in d and not d[e].isna().all():
            ax.plot(x, d[e], color=MA_COLORS[int(e[3:])], linewidth=0.7, linestyle=":")
    pad = (hi - lo) * 0.12
    ax.set_ylim((lo * 0.92, hi * 1.08) if log_scale else (lo - pad, hi + pad))
    if log_scale:
        ax.set_yscale("log")
    ax.set_title(f"BTCUSD {tf}  |  fechamento {state['bar_close'][:16]} UTC  |  {state['close']:,.0f}",
                 color="white", fontsize=12, loc="left")

    # RSI
    ar.axhspan(43.6, 70, color="#3d1a5b", alpha=0.45)
    ar.axhspan(40.54, 43.6, color="#ff851b", alpha=0.10)
    ar.plot(x, d["rsi"], color="#f5d76e", linewidth=1.1)
    ar.plot(x, d["rsi_ma"], color="#ff4136", linewidth=1.0)
    ar.axhline(50, color="white", alpha=0.35, linestyle=":")
    for L in state["rsi"]["levels_auto"]:
        ar.axhline(L["value"], color="#7fdbff", alpha=0.18, linewidth=0.6)
    for name, val in state["rsi"]["levels_known"].items():
        c = "#ff851b" if "Traps" in name else "#ffdc00" if name in ("BBB", "Fim de bull") else "#bbbbbb"
        ar.axhline(val, color=c, alpha=0.8, linewidth=0.9, linestyle="--")
        ar.annotate(f"{name} {val}", (x[-1], val), xytext=(-150, 2), textcoords="offset points", color=c, fontsize=7)
    ar.set_ylim(5, 100)
    ar.set_ylabel("RSI", color="white")

    # Stoch
    ak.axhspan(20, 80, color="#3d1a5b", alpha=0.35)
    ak.plot(x, d["stoch_k"], color="#0a84ff", linewidth=1.0)
    ak.plot(x, d["stoch_d"], color="#ff851b", linewidth=1.0)
    for name, val in {"Suporte Inferior": 20, "Suporte Superior": 50, "Resistencia Superior": 80}.items():
        ak.axhline(val, color="white", alpha=0.35, linestyle=":")
        ak.annotate(name, (x[-1], val), xytext=(-90, 2), textcoords="offset points", color="#7fdbff", fontsize=7)
    ak.set_ylim(-5, 105)
    ak.set_ylabel("Stoch RSI", color="white")

    step = max(1, len(d) // 10)
    ak.set_xticks(x[::step])
    fmt = "%d/%m %Hh" if tf.endswith("m") else "%d/%m/%y"
    ak.set_xticklabels([t.strftime(fmt) for t in d.index[::step]], fontsize=8, rotation=0)
    fig.tight_layout()
    fig.savefig(path, dpi=110, facecolor="black")
    plt.close(fig)
