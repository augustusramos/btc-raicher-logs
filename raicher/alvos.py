"""Próximos alvos pelo método (sem esperar o Dollynho).

Lê os <tf>.json da branch `dados` e lista os níveis na direção do trade (short: abaixo do preço;
long: acima), agrupa os que coincidem (<= 1%) entre timeframes e ordena do mais perto ao mais longe.
Uso: python -m raicher.alvos --dados dados [--lado short|long] [--preco 68750]
Não é recomendação: é a escada de médias do método. Só vale no fechamento.
"""
import argparse
import json
from pathlib import Path

TFS = ["343m", "686m", "1D", "2D", "3D", "1W"]
PESO = {"manual": 2, "343m": 1, "686m": 1, "1D": 2, "2D": 2, "3D": 2, "1W": 3}
RSI_LINHAS = [23.67, 13.53, 6.23]  # 23.67 Suporte Histórico; 13.53 (2022) e 6.23 (2023 ATL) = linhas do print dele
MANUAIS = [  # níveis desenhados/citados por ele (valor, nome); manter atualizado ao receber prints
    (65900, "Região da Agulhada ago/2024 (topo)"), (65400, "Região da Agulhada ago/2024 (base)"),
    (64450, "Linha laranja da Agulhada ago/2024"), (62800, "Linha Vermelha (dele, 13/11)"), (67200, "Linha Azul Pontilhada (dele)"),
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
