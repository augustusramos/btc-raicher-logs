# Documento-mestre do projeto btc-raicher-logs

Atualizado em 23/11/2026. Este arquivo explica o projeto inteiro para qualquer sessão nova do Claude (ou pessoa) se situar sem depender de conversa anterior. Ferramenta de estudo, não recomendação de investimento.

## 1. Objetivo

Gerar, a cada fechamento de candle, um Log de BTC no método do @raicher / @DollynhoCoin, com a mesma leitura e a mesma decisão de posição que o Dollynho tomaria com os mesmos dados. Os posts dele são o gabarito: não se copia o texto dele; compara-se o próximo passo (manter, zerar, virar, entrar, ficar de fora, alvos e stop) e ajusta-se a regra quando a diferença se repete.

Meta de longo prazo (Augustus): transformar os Logs numa plataforma própria (página automática, canal, assinatura) e medir se as decisões dão resultado.

## 2. Onde está cada coisa

| Caminho | O que é |
| --- | --- |
| `raicher/` | Código: busca de candles (Bitstamp), timeframes, médias, RSI, StochRSI, setups, gráficos, alvos próprios |
| `raicher/config.json` | Médias, EMAs, níveis fixos do RSI, parâmetros do Bilau |
| `raicher/alvos.py` | Escada de alvos próprios (clusters de médias de vários timeframes + níveis manuais dele) |
| `.github/workflows/indicadores.yml` | Calcula tudo e publica na branch `dados` |
| `.github/workflows/ao_vivo.yml` | Foto do candle em formação, na branch `ao-vivo` (`ao_vivo.json`) |
| branch `dados` | `latest.json`, `<tf>.json`, `charts/<tf>.png`, `history/` |
| `prompts/modo_dollynho.md` | Instruções que as tarefas agendadas seguem a cada fechamento (editar aqui muda os próximos Logs) |
| `logs/AAAA-MM-DD_HHMM_<tf>.md` | Cada Log enviado + "Notas internas" (raciocínio, 📌, 🧭, ⚖️) |
| `logs/estado.json` | Estado dos trades (postura, entrada, stop, alvos, histórico), numeração dos Logs, Bilau, compras de longo prazo dele |
| `calibracao/placar.md` | Uma linha por post dele comparado: o que bateu, o que divergiu, regra ajustada |
| `calibracao/decisoes_dollynho.md` | Como ele decide a posição, trade a trade, com os dados de cada fechamento |
| `calibracao/dollynho/` | Resumo parafraseado de cada post dele + `estilo.md` + `cronologia_trades.md` |
| `docs/METODO.md` | Este arquivo |

## 3. Automação

Cinco tarefas agendadas na conta claude.ai do Augustus (fuso America/Sao_Paulo), cada uma abre uma sessão nova e executa `prompts/modo_dollynho.md`:

| Horário | Fecha |
| --- | --- |
| 02:44 | 343 |
| 08:27 | 343 e 686 |
| 14:10 | 343 |
| 19:53 | 343 e 686 |
| 21:01 | 343, 686, Diário (+ 2D nos dias de 2D, Semanal no domingo, 3D quando fecha) |

Elas não dependem de nenhuma conversa. Se uma conversa for apagada, os Logs continuam.

Limites conhecidos: a sessão não acessa a Bitstamp direto (proxy); os dados vêm sempre do workflow. Criar tarefas novas pelo chat foi bloqueado pelo classificador de permissões duas vezes (alerta de RSI e leitura automática do X).

## 4. Fonte e indicadores

- Fonte: Bitstamp BTCUSD (a mesma dos prints dele). Fechamentos batem com os dele em menos de 0,1%; médias em menos de 0,3%; RSI idêntico.
- Médias (SMA) 7, 21, 49, 77, 200, 231, 343, 539, 686, 777, 1372, 1617, 2744; EMAs 7, 21, 49, 77, 231, 343, 686, 777, 1372, 1617.
- Timeframes: 343 min, 686 min, Diário, 2D, 3D, Semanal, 2 Semanas, Mensal, 2M, 4M.
- Horários de fechamento (Brasília): 343 às 02:43, 08:26, 14:09, 19:52, 21:00; 686 às 08:26, 19:52, 21:00; Diário 21:00; Semanal domingo 21:00; 2D e 3D ancorados no início do ano.
- RSI 14 com Média (SMA 14) e níveis fixos: 72,86; 70 (Resistência Superior); 50 (Resistência Inferior); ~43,6 (Suporte Inferior); 40,54 (Região dos Traps); 35,74; 30; 23,67 (Suporte Histórico); 13,53.
- StochRSI 3,3,14,14: 20 (Suporte Inferior), 50, 80 (Resistência Superior), 0 (zerado), 100 (máxima).
- Nível fixo: Fundo 2025-NOV 80.537.

## 5. Setups com nome

- **Bilau (BBB) no 2D:** preço abaixo da MA200 do 2D + RSI 2D abaixo de 25,78 + Stoch 2D abaixo de 20,44. Confirmação só no fechamento do 2D. Historicamente região de fundo de ciclo (11 ocorrências). Confirmado em 14/11 e 18/11/2026 ("Bilau duplo").
- **Agulhada:** cruzamento triplo para cima (Diário 7/21/343; Semanal 7/21/77). As regiões das Agulhadas antigas viram suporte/resistência (Agulhada ago/2024 ~65,4–65,9K; linha laranja ago/2026 ~64,45K).
- **MonkeyStrategy (BTFD):** compra na MA343 do Diário e na MA49 do Semanal.
- **2D 77x200:** cruzamento para baixo confirma bear; para cima, bull.
- **Fundos de bear no Semanal:** MA231, EMA343, MA343. **Rosquinha:** MA77 do Mensal (~53,2–53,5K), compra ideal dele.

## 6. Tabela de decisão (o que decide a posição)

Aplicada só aos números do JSON e ao `estado.json`, nesta ordem:

1. ~~Bilau 2D ativo = sem short novo~~ — ENCERRADO em 26/11 (Augustus: o Bilau foi um ponto de compra, não um regime). Só volta a ser citado se um novo BBB se formar no 2D.
2. **RSI do timeframe abaixo de 23,67:** sem short novo.
3. **Stoch cruzando para cima abaixo de 20 com RSI abaixo de 30:** esgotamento da queda.
4. **Long:** 343 fechando acima da MA7/EMA7 com RSI acima do Suporte Inferior (~43,6), Stoch fora do teto e 686 do mesmo lado da MA7. Alternativa preferida: recuo do RSI à Média/23,67 com divergência de alta. Com a MA21 do 343 a menos de ~2% acima, exige fechar acima da MA21.
5. **Exceção de reversão com Bilau (18/11, provisória):** candle forte de reversão no 343 recuperando a linha perdida, RSI acima da Média e de 23,67, Stoch virando no 20, divergência de alta: compra no fechamento mesmo com o 686 contra; stop abaixo da linha recuperada.
6. **Short:** rejeição da MA7/EMA7 + RSI rejeitando o Suporte Inferior + Stoch virando para baixo. Ordem tática permitida na EMA21 do 343 com stop curto, mesmo com Bilau, nunca a mercado.
7. **Nada acima:** segue a tendência (preço x MA7 + RSI x Média).

Gestão do trade (padrões dele):

- A direção vem dos prazos maiores (Diário, 2D); o 343 dá o momento.
- Um candle contra não fecha o trade; só o stop fecha. Stop = média de resistência/suporte principal + condição no RSI.
- No lucro, aperta o stop no próprio fechamento que confirma (MA21 → MA7/EMA7) e nunca devolve o lucro.
- Zera no alvo final, ou quando Bilau + RSI abaixo de 23,67 + Stoch cruzando para cima aparecem juntos.
- Não vira a mão no candle em que zera. Stoch no teto = não compra; Stoch zerado = não vende.
- Nunca declarar parcial nem mexer no stop sem a regra mandar.
- Dois horizontes: trade alavancado no 343/686 e compras de longo prazo dele à vista (abaixo da EMA777 do 2D = "promoção"; ordens em degraus até a rosquinha).

### 6.x Abaixo de todas as médias (24/11)
Só projeta mais queda ("testar o fundo") se ainda há espaço: Stoch > ~30 e caindo, RSI abaixo da Média, sem divergência. Stoch zerado, RSI sobrevendido, divergência ou Traps segurando = perto do fundo, aguardar MA7/Média do RSI. Teste em 33 posts dele: 76% (83% fora de trade aberto). Detalhes em prompts/modo_dollynho.md.

## 7. Alvos

- Alvos são as próximas médias/níveis na direção do trade, pulando as intermediárias quando há confluência forte adiante.
- `raicher/alvos.py` monta a escada (pesos por timeframe; níveis manuais dele: Agulhada 2024, linha laranja, Linha Vermelha, Azul Pontilhada, Linha Laranja do 686 ~59K). Rodar: `python -m raicher.alvos --dados dados [--lado short|long]`.
- Linhas desenhadas por ele e equivalentes nos dados: Azul Pontilhada ~67,2K ≈ MA200/EMA231 do Semanal; Linha Vermelha ~62,3–62,8K (descendente) ≈ MA777 do 2D; Linha Branca ~57,7K ≈ MA686/EMA777 do 3D; Ciano ~61,4K; Verde Tracejada ~55,6K.

## 8. Formato da mensagem (desde 23/11/2026)

- Um bloco por timeframe que fechou; às 21:00 o primeiro traz "Log N." (N = último número dele + 1, corrigido quando ele postar).
- 3 a 5 linhas: evento do candle → preço x média-chave → RSI x nível-chave → Stoch → posição.
- Cada linha de dado termina com ⬆️ (bullish), ⬇️ (bearish) ou ↔️ (neutro). Posição numa frase, sem seta.
- Fecho do bloco: "<TF>: BULLISH ⬆️ / BEARISH ⬇️ / NEUTRO ↔️" pela tendência, com ressalva curta entre parênteses.
- Números só em entrada, stop, alvo e suporte/resistência imediatos. Stoch sem K/D. Sem a palavra "pavio" (tocamos / rejeição / martelo).
- 📌, 🧭 e ⚖️ ficam nas Notas internas do arquivo, não na mensagem. Rodapé: "_Estudo, não recomendação._"

## 9. Calibração (como o projeto aprende)

Para cada post dele (enviado pelo Augustus ou lido no X pelo Chrome dele):

1. Resumo parafraseado em `calibracao/dollynho/AAAA-MM-DD_HHMM_<tf>.md`.
2. Comparar com o nosso Log do mesmo fechamento: dados, decisão de posição, alvos, stop, sentimento.
3. Linha no `calibracao/placar.md`.
4. Regra nova em `prompts/modo_dollynho.md` como provisória na 1ª vez; fixa quando a mesma diferença se repetir.
5. Atualizar `logs/estado.json` se ele mudou trade, alvo ou stop.

Placar de 09/11 a 23/11/2026: posição igual em 64 de 69 fechamentos (93%); 88% antes das regras de decisão, 95% depois. Relatório: "Revisão dos Logs x Dollynho" (doc no claude.ai).

## 10. Histórico de trades dele no período

| Trade | Entrada | Saída |
| --- | --- | --- |
| Short 343 | 03/11 à noite, MA7/EMA7 | Alvo Linha Vermelha, 15/11 ~02:43 (alvos intermediários MA777/MA1372, RSI 23,67, Azul Pontilhada) |
| Short tático | Ordem na EMA21 do 343 (~65,8K), 17/11 | Não executou |
| Long 343 | 18/11 21:00, ~63,0K, stop Linha Vermelha → MA7 | Stop na MA7, 19/11 14:09 (62.389) |
| Compras à vista | Ordens 58K–53K (19–20/11); executou ~57K e ~55K (21/11) | Em aberto (alvo semanal 53K) |

## 11. Origem da série dele

Primeiro post no formato atual: 21/12/2025 (SEMANAL, domingo). "Log 7" em 27/12/2025 é o primeiro com número. Antes disso, um post isolado em 02/11/2025 ("Plantão dominical"). Em 22/11/2026 ele estava no Log 336.

## 12. Pendências

- Detector de linhas (`raicher/linhas.py`, gabarito em `calibracao/linhas_dollynho.json`). Achado de 23/11: as linhas dele no 343 são linhas de tendência longas, em escala log, que ligam pivôs do Diário de meses ou anos atrás (Verde Tracejada: 6 pivôs desde jul/2025; Azul Pontilhada: topos jun–ago/2026; Branca: fundos jul–ago/2026). Com pivôs de 3 dias e tolerância de 0,6%, as 9 linhas dele aparecem entre ~127 candidatas, a até 0,2% do valor de hoje. Falta o critério de escolha: no top 15 do ranking atual só 2 batem. Próximo passo: mais exemplos (prints antigos dele) para aprender a seleção.
- Varredura completa do histórico dele e do Raicher (texto + gráficos) desde 21/12/2025.
- Registro de resultado (% de cada entrada/saída, dele e nossa) para medir lucratividade, não só concordância.
- Detecção de divergência menos rígida (ele viu 10 que o nosso cálculo não marcou entre 21 e 23/11).
- Plataforma: página automática no GitHub, Logs gerados via API, canal no Telegram; marca própria e consulta jurídica (CVM) antes de cobrar.


### Atualização 26/11
- Stoch: "cruzou/cruzando" só com cruzamento no fechamento; quase encostando (≤ ~4 pontos e convergindo) = "ensaiando um cruzamento".
- Stop: no lucro (MA7 além da entrada ou alvo atingido) → stop na MA7; trade sem lucro → stop segue na MA21 mesmo com candle forte contra.
