"""Próximos alvos pelo método (sem esperar o Dollynho).

Lê os <tf>.json da branch `dados` e lista os níveis na direção do trade (short: abaixo do preço;
long: acima), agrupa os que coincidem (<= 1%) entre timeframes e ordena do mais perto ao mais longe.
Uso: python -m raicher.alvos --dados dados [--lado short|long] [--preco 68750]
Não é recomendação: é a escada de médias do método. Só vale no fechamento.
"""
import argparse
import json
from pathlib import Path

TFS = ["343m", "686m", "1D", "2D", "3D", "1W", "1M"]
PESO = {"manual": 2, "343m": 1, "686m": 1, "1D": 2, "2D": 2, "3D": 2, "1W": 3, "1M": 4}
RSI_LINHAS = [23.67, 13.53, 6.23]  # 23.67 Suporte Histórico; 13.53 (2022) e 6.23 (2023 ATL) = linhas do print dele
MANUAIS = [  # níveis desenhados/citados por ele (valor, nome); manter atualizado ao receber prints
    (65900, "Região da Agulhada ago/2024 (topo)"), (65400, "Região da Agulhada ago/2024 (base)"),
    (64450, "Linha laranja da Agulhada ago/2024"), (62600, "Linha Vermelha (dele, descendente: 62,8K em 13/11; 62,4K em 14/11)"), (59200,"Linha Laranja (dele, ~59,2K em 19/11; fundo de jul/2025; 🎯 do 686)"),
    (61600, "Linha Ciano (dele, 343, descendente; ~61,6K em 19/11)"), (56902, "EMA2401 do Diário (print dele 19/11; não está nos dados)"),
    (67200, "Linha Azul Pontilhada (dele)"),
    (57600, "Linha Branca (dele, 343, descendente; ~57,7K em 20/11 19:52, tocada: mín 57.668; ~57,5-57,6K no print de 24/11 21:11; = MA686/EMA777 3D; 🎯 1 do short de 24/11 21:00; rebaixada a SUPORTE intermediário em 25/11 08:26: deve oferecer algum suporte)"),
    (57850, "Linha Vinho (dele, 686, ASCENDENTE: a linha roxa/vinho abaixo da amarela; 🍷 no print de 24/11 21:41 em ~57,8-57,9K; segurou o fundo de 20-21/11 no 686; destino dele nas próximas horas)"),
    (55300, "Linha Verde Tracejada (dele, 343, descendente; ~55,6K em 21/11, ~55,3K no print de 24/11 21:11; 🎯 2 do short de 24/11 21:00)"),
    (53950, "Linha Amarela Tracejada (dele, 343, descendente; ~53,9-54,0K no print de 25/11 08:31; 🍯 🎯 3 do short de 24/11 21:00)"),
    (50000, "MA42 do 2M (Raicher 19/11: '2 Month Double Bottom', ~50K, não tocada)"),
    (57500, "Trend das Agulhadas 03/03+16/10/2023 (Raicher 22/11, 686, ASCENDENTE ~+1,2K/mês; ~57,5K em 22/11; suporte do fundo)"),
    (55000, "Trend das Agulhadas 29/07+07/09/2025 (Raicher 22/11, 343, DESCENDENTE ~-80/dia; ~55,0K em 22/11; tocada no fundo 55.081)"),
]
COLADO = 0.25   # % -> nível "colado" no preço (já testando/perdido agora)
AGRUPA = 1.0    # % -> níveis a até 1% um do outro formam um cluster


def carregar(dados: Path):
    out = {}
    for tf in TFS:
        p = dados / f"{tf}.json"
        if p.exists():
            out[tf] = json.loads(p.read_text())
    return out


def niveis(d: dict, preco: float, lado: str):
    res = []
    for tf, j in d.items():
        for nome, v in j.get("mas", {}).items():
            val = v.get("value")
            if not val:
                continue
            dist = (val / preco - 1) * 100
            if (lado == "short" and dist < 0) or (lado == "long" and dist > 0):
                res.append({"tf": tf, "nome": nome.upper(), "valor": round(val), "dist_pct": round(dist, 2)})
    for val, nome in MANUAIS:
        dist = (val / preco - 1) * 100
        if (lado == "short" and dist < 0) or (lado == "long" and dist > 0):
            res.append({"tf": "manual", "nome": nome.upper(), "valor": val, "dist_pct": round(dist, 2)})
    res.sort(key=lambda x: abs(x["dist_pct"]))
    return res


def clusters(lv):
    cs = []
    for n in lv:
        for c in cs:
            if abs(n["valor"] / c["ref"] - 1) * 100 <= AGRUPA:
                c["itens"].append(n)
                break
        else:
            cs.append({"ref": n["valor"], "itens": [n]})
    out = []
    for c in cs:
        tfs = sorted({i["tf"] for i in c["itens"]})
        forca = sum(PESO[t] for t in tfs)
        valor = round(sum(i["valor"] for i in c["itens"]) / len(c["itens"]))
        out.append({"valor": valor, "dist_pct": c["itens"][0]["dist_pct"],
                    "forca": forca, "tfs": tfs,
                    "medias": [f'{i["nome"]} {i["tf"]} ({i["valor"]:,})'.replace(",", ".") for i in c["itens"]],
                    "colado": abs(c["itens"][0]["dist_pct"]) <= COLADO})
    out.sort(key=lambda x: abs(x["dist_pct"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dados", default="dados")
    ap.add_argument("--lado", default="short", choices=["short", "long"])
    ap.add_argument("--preco", type=float)
    a = ap.parse_args()
    d = carregar(Path(a.dados))
    preco = a.preco or d["343m"]["close"]
    cs = clusters(niveis(d, preco, a.lado))
    rsi = d["343m"]["rsi"]["value"]
    if a.lado == "short":
        rsi_alvos = [x for x in RSI_LINHAS if x < rsi - 0.3]
    else:
        rsi_alvos = [x for x in [30, 35.74, 40.54, 43.6, 50] if x > rsi + 0.3]
    print(json.dumps({"preco": preco, "lado": a.lado, "rsi_343": rsi, "rsi_proximos": rsi_alvos[:2],
                      "escada": cs[:8],
                      "como_ler": "Os 2-3 primeiros clusters NÃO colados (>0.5%) são os alvos; 'forca' >= 4 = confluência (mais confiável). Colado = já está testando. Parcial/stop só com a palavra dele."},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
