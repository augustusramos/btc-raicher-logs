"""Leitura objetiva: cada dado do fechamento classificado como BULLISH / BEARISH / NEUTRO
pelas regras do método Raicher/Dollynho. Sem trade, sem stop, sem opinião.

Uso: python -m raicher.leitura --dados dados --tf 343m 686m 1D
"""
import argparse, json, os

MEDIAS = ["ma7", "ema7", "ma21", "ema21", "ma49", "ma77", "ma200", "ma231", "ma343",
          "ma539", "ma686", "ma777", "ma1372", "ma1617"]
NOME_TF = {"343m": "343", "686m": "686", "1D": "DIÁRIO", "2D": "DOIS DIAS", "3D": "TRÊS DIAS",
           "1W": "SEMANAL", "2W": "DUAS SEMANAS", "1M": "MENSAL"}


def k(v):
    return f"{v/1000:,.1f}K".replace(",", "X").replace(".", ",").replace("X", ".")


def ler_tf(t):
    out = []  # (classe, grupo, texto)
    mas = t.get("mas", {})
    emas = t.get("emas", {})
    todas = {**mas, **emas}
    # 1) Preço x médias (tendência)
    for m in MEDIAS:
        d = todas.get(m)
        if not d:
            continue
        ev = (d.get("event") or "")
        pos = d.get("pos")
        if "RECUPER" in ev or "ROMPEU" in ev:
            out.append(("BULLISH", "tendência", f"Recuperamos a {m.upper()} ({k(d['value'])})"))
        elif "PERDEU" in ev:
            out.append(("BEARISH", "tendência", f"Perdemos a {m.upper()} ({k(d['value'])})"))
        elif "CONFIRM" in ev:
            cl = "BULLISH" if pos == "ACIMA" else "BEARISH"
            out.append((cl, "tendência", f"Confirmamos {pos} da {m.upper()} ({k(d['value'])})"))
    acima = [m for m in MEDIAS if todas.get(m, {}).get("pos") == "ACIMA"]
    abaixo = [m for m in MEDIAS if todas.get(m, {}).get("pos") == "ABAIXO"]
    if abaixo and not acima:
        out.append(("BEARISH", "tendência", "Preço ABAIXO de todas as médias"))
    elif acima and not abaixo:
        out.append(("BULLISH", "tendência", "Preço ACIMA de todas as médias"))
    else:
        for m in ("ma7", "ma21"):
            d = todas.get(m)
            if d and not d.get("event"):
                cl = "BULLISH" if d["pos"] == "ACIMA" else "BEARISH"
                out.append((cl, "tendência", f"Preço {d['pos']} da {m.upper()} ({k(d['value'])})"))
    for w in t.get("wick_touches", []) or []:
        nome = w if isinstance(w, str) else (w.get("ma") or w.get("name") or str(w))
        out.append(("NEUTRO", "tendência", f"Toque de pavio na {str(nome).upper()}"))
    # 2) Cruzamentos da MA7
    for c in t.get("ma_crosses", []) or []:
        cl = "BULLISH" if c.get("direcao") == "bullish" else "BEARISH"
        verbo = "cruzando" if c.get("cruzando") else "cruzou"
        out.append((cl, "tendência", f"MA7 {verbo} {c.get('direcao')} a {c['par'].split(' x ')[1]}"))
    # 3) RSI
    r = t.get("rsi", {})
    if r:
        v, mm = r["value"], r["ma"]
        ev = r.get("vs_ma", {}).get("event") or ""
        pos = r.get("vs_ma", {}).get("pos")
        txt = f"RSI ({v:.1f}) {pos} da Média ({mm:.1f})" + (f" — {ev.split(' ')[0].lower()}" if ev else "")
        out.append(("BULLISH" if pos == "ACIMA" else "BEARISH", "tendência", txt))
        if v < 23.67:
            out.append(("BULLISH", "exaustão", f"RSI ABAIXO do Suporte Histórico 23.67 (sobrevenda extrema; no método: abaixo dele não tem short)"))
        elif v < 30:
            out.append(("BULLISH", "exaustão", "RSI abaixo de 30 (sobrevenda)"))
        elif v > 72.86:
            out.append(("BEARISH", "exaustão", "RSI acima de 72.86 (sobrecompra extrema)"))
        elif v > 70:
            out.append(("BEARISH", "exaustão", "RSI acima da Resistência Superior 70 (sobrecompra)"))
        elif 40.54 <= v <= 43.6:
            out.append(("NEUTRO", "tendência", "RSI na Região dos Traps (40.54–43.6): sinal pouco confiável"))
        elif v < 43.6:
            out.append(("BEARISH", "tendência", "RSI ABAIXO do Suporte Inferior (~43.6)"))
        elif v >= 50:
            out.append(("BULLISH", "tendência", "RSI ACIMA da linha 50"))
    # 4) Stoch
    s = t.get("stoch", {})
    if s:
        kk, dd = s["k"], s["d"]
        ev = s.get("k_vs_d", {}).get("event") or ""
        if kk <= 1 and dd <= 1:
            pass
        elif ev:
            cl = "BULLISH" if s["k_vs_d"]["pos"] == "ACIMA" else "BEARISH"
            out.append((cl, "tendência", f"Stoch cruzou {'bullish' if cl=='BULLISH' else 'bearish'} (K {kk:.1f} / D {dd:.1f})"))
        else:
            cl = "BULLISH" if kk > dd else "BEARISH" if kk < dd else "NEUTRO"
            out.append((cl, "tendência", f"Stoch K {'acima' if kk>dd else 'abaixo' if kk<dd else 'igual'} do D (K {kk:.1f} / D {dd:.1f})"))
        if kk <= 1 and dd <= 1:
            out.append(("BULLISH", "exaustão", "Stoch ZERADO (K e D em 0)"))
        elif kk < 20:
            out.append(("BULLISH", "exaustão", "Stoch abaixo do Suporte Inferior 20 (sobrevenda)"))
        elif kk > 80:
            out.append(("BEARISH", "exaustão", "Stoch acima da Resistência Superior 80 (sobrecompra)"))
    return out


SETUP_CLASSE = {"BBB (2D)": ("BULLISH", "BILAU 2D confirmado: região histórica de fundo"),
                "Agulhada 1D (7/21/343)": ("BULLISH", "Agulhada no Diário"),
                "Agulhada 1W (7/21/77)": ("BULLISH", "Agulhada no Semanal"),
                "BTFD MA343 1D": ("BULLISH", "MonkeyStrategy: preço na MA343 do Diário (BTFD)"),
                "BTFD MA49 1W": ("BULLISH", "MonkeyStrategy: preço na MA49 do Semanal (BTFD)")}


def setups(lat, tfs):
    out = []
    for s in lat.get("setups", []):
        nome = s["setup"]
        if nome == "2D MA77 x MA200":
            ev = s["detail"].get("event")
            if ev:
                cl = "BEARISH" if s["detail"]["ma77_vs_ma200"] == "ABAIXO" else "BULLISH"
                out.append((cl, "setup", f"2D: MA77 cruzou a MA200 ({ev})"))
            continue
        if nome in SETUP_CLASSE and s.get("active") and s["tf"] in tfs:
            cl, txt = SETUP_CLASSE[nome]
            out.append((cl, "setup", txt))
        elif nome == "BBB (2D)" and s.get("near") and not s.get("active") and "2D" in tfs:
            out.append(("NEUTRO", "setup", "Bilau 2D perto (2 de 3 condições)"))
    return out


EMO = {"BULLISH": "🟢", "BEARISH": "🔴", "NEUTRO": "⚪"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", default="dados")
    ap.add_argument("--tf", nargs="+", default=["343m"])
    a = ap.parse_args()
    lat = json.load(open(os.path.join(a.dados, "latest.json")))
    total = {"BULLISH": 0, "BEARISH": 0, "NEUTRO": 0}
    for tf in a.tf:
        t = lat["timeframes"].get(tf)
        if not t:
            continue
        linhas = ler_tf(t) + setups(lat, [tf])
        print(f"\n{NOME_TF.get(tf, tf)} — fechou {t['close']:,.0f} ({t['change_pct']:+.2f}%)".replace(",", "."))
        c = {"BULLISH": 0, "BEARISH": 0, "NEUTRO": 0}
        tend = {"BULLISH": 0, "BEARISH": 0}
        exa = {"BULLISH": 0, "BEARISH": 0}
        for cl, g, txt in linhas:
            print(f"{EMO[cl]} {cl}: {txt}")
            c[cl] += 1; total[cl] += 1
            if g == "tendência" and cl in tend: tend[cl] += 1
            if g in ("exaustão", "setup") and cl in exa: exa[cl] += 1
        print(f"Placar {NOME_TF.get(tf, tf)}: {c['BULLISH']} bullish x {c['BEARISH']} bearish"
              f" | tendência {tend['BULLISH']}🟢/{tend['BEARISH']}🔴 | exaustão/setups {exa['BULLISH']}🟢/{exa['BEARISH']}🔴")
    print(f"\nTOTAL: {total['BULLISH']} bullish x {total['BEARISH']} bearish")


if __name__ == "__main__":
    main()
