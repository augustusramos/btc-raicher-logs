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

## Atualização 25/11 (histórico do 343 desde 2021, branch `historico`)
- Linha Branca confirmada pelo rótulo dele ("7,77,231 – 2023-MAI-03 e MAI-08"): cruzamentos MA7×MA77 do 343 em 03/05/2023 14:09 e 08/05/2023 02:43 → reproduz a linha com 0,09% de erro (o 2º melhor par do mês erra 0,9%).
- Regra geral confirmada: as âncoras são CRUZAMENTOS DE MÉDIAS (sobretudo do 343; às vezes do Diário), e o rótulo dele diz quais médias e quais datas.
- Mas, sem o rótulo, os dados não dizem quais cruzamentos ele escolheu: para quase toda linha existem de 10 a 250 pares de cruzamentos do mesmo tipo que reproduzem a linha com erro < 0,1% (só 3 de 61 têm par único). tools/ancoras_cruzamentos.py, resultado em calibracao/ancoras_candidatas.json.
- Conclusão: reproduzir a ESCOLHA dele só com os dados não é viável hoje. Caminho prático: (1) manter as linhas dele registradas a partir dos prints (ele as mantém por meses); (2) para linhas novas, o sistema propõe candidatas com a mesma construção (cruzamentos do 343 que já foram tocados pelo preço) e ranqueia por toques; (3) ler os rótulos dos prints para ampliar o gabarito.
