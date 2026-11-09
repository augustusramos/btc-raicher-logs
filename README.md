# btc-raicher-logs

Indicadores automáticos de BTC no método do @raicher / @DollynhoCoin, para o Claude escrever o Log a cada fechamento.

## O que roda
O GitHub Action `indicadores` roda logo após os fechamentos (horários em UTC no workflow):
1. Baixa candles da Bitstamp (BTCUSD, histórico desde 2011 no diário; últimos 200 dias em 1 min).
2. Monta os timeframes: 343m, 686m, 1D, 2D, 3D, 1W, 2W, 1M, 2M, 4M (alinhamento explicado em `raicher/timeframes.py`).
3. Calcula médias (7, 21, 49, 77, 200, 231, 343, 539, 686, 777, 1372 + EMAs), RSI 14 com média, StochRSI.
4. Calcula as linhas horizontais do RSI automaticamente (pivôs históricos) e compara com os níveis citados nos posts.
5. Detecta setups: BBB no 2D, Agulhada (1D 7/21/343, 1W 7/21/77), BTFD (MA343 1D, MA49 1W), toque na MA343 (343m/686m/1D), cruzamento 77x200 no 2D, reset do RSI semanal < 30.
6. Gera gráficos no estilo dos prints e publica tudo na branch `dados`.
7. Abre uma issue quando aparece alerta novo (o GitHub avisa por e-mail/app).

## Branch `dados`
- `latest.json` — estado de todos os timeframes + setups (é o que o Claude lê para escrever o Log)
- `<tf>.json` — estado de cada timeframe
- `charts/<tf>.png` — gráficos
- `history/AAAA-MM-DD.json` — foto diária no fechamento do 1D
- `calibracao.txt` — valores calculados x valores citados nos posts

## Rodar local
```
pip install -r requirements.txt
python -m raicher.run --charts all      # dados reais
python -m raicher.run --synthetic       # teste sem internet
```

Ajustes ficam em `raicher/config.json`. Isto é ferramenta de estudo, não recomendação de investimento.
