# De onde saem as linhas do Dollynho (estudo de 25/11/2026)

Base: 51 prints medidos (calibracao/linhas_prints), juntados em 61 linhas distintas (calibracao/gabarito_linhas.json, gerado por tools/gabarito_linhas.py).

## Confirmado
- Escala LOG: em escala linear as linhas estendidas para trás dariam preços negativos; em log batem com pontos reais.
- Ele mantém as linhas por meses (Amarela Tracejada dez/2025 → ago/2026; Ciano abr → out/2026), com erro de medição de 1 a 3 bp entre prints.
- Âncoras em cruzamentos de médias, e o rótulo dele diz quais:
  - magenta "7,21,343 – 2024-ABR e 2024-JUL" = cruzamentos MA7×MA77 do Diário em 30/04/2024 e 20/07/2024 (erro 0,03–0,05%).
  - dourada pontilhada "7,21,77 – 2025-JUL e 2025-DEZ" = agulhadas MA 7/21/77 do 343 em 26/07 e 28/12/2025 (erro 0,02%).
  - laranja "EMAs 7,21,77 – 2025-JUN e 2025-DEZ" = agulhadas EMA 7/21/77 do 343 em 16/06 e 05/12/2025 (erro 0,2%).

## Não resolvido
- Nenhuma regra única reproduz a maioria das linhas: pares de agulhadas do 343 explicam 11 de 61 (vários por coincidência).
- Linhas com âncoras antigas (2014–2023) têm dezenas de pares candidatos no Diário que passam igualmente perto: não dá para saber quais ele usou sem o rótulo ou sem histórico de 343 desses anos (o projeto só tem 343 desde dez/2024).

## Próximo passo
1. Histórico do 343 desde 2022 (dados de minuto da Bitstamp via GitHub Actions) para testar as agulhadas antigas.
2. Ler os rótulos de cada linha nos prints (ele escreve as médias e as datas) e usar como gabarito das âncoras.
3. Só depois treinar a escolha automática.
