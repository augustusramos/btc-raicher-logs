# Estudo 26/11: "Stoch cruzando" e "stop na MA7 após martelo"
Base: 1.772 posts do Dollynho e 174 do Raicher (dez/2025–nov/2026) + Stoch RSI calculado no 343/686/Diário (histórico desde 2021).

## 1. Stoch "cruzando" (tools/teste_stoch_cruzando.py, resultado em teste_stoch_cruzando.json)
Dollynho, 123 frases sobre cruzamento K x D (excluídas as de "cruzar um nível"):
| Como ele escreve | n | K x D já cruzado no fechamento |
|---|---|---|
| "cruzou" / "confirmou o cruzamento" | 52 | 94% |
| "cruzando" | 46 | 72% (os outros: K a até ~4 pontos da D e virando) |
| "ensaiando / ameaçando / querendo cruzar" | 25 | 28% |
Raicher: só 5 frases, sem conclusão.
Leitura: ele usa vocabulário diferente para cada caso. "Cruzou" = confirmado. Antes de cruzar, quase sempre "ensaiando/ameaçando cruzar". "Cruzando" é na maioria confirmado, às vezes iminente.
Proposta: manter a regra de 26/11 e acrescentar: K ainda não cruzou, mas está a até ~4 pontos da D e indo em direção a ela → "Stoch ensaiando um cruzamento bearish/bullish" (em vez de "segue no teto").

## 2. Stop na MA7 depois de candle forte contra o short
Ele nunca escreveu "martelo" (0 de 1.772 posts). "Stop na MA7" aparece 8 vezes: é o stop padrão dele em short curto e no trailing depois de alvo atingido.
Candle bullish forte fechando colado abaixo da MA7 durante um short:
- Subiu/deixou o stop na MA7: 28/06 (trade no lucro), 13/07 (alvo atingido), 03/10, 14/11 ("trade impecável"), 25/11 (MA7 abaixo da entrada).
- Manteve stop mais largo (MA21/EMA77): 22/06, 24/09 (2x), 25/09, 28/09 — trades recém-abertos, ainda sem lucro.
Leitura: o gatilho não é o martelo, é o trade estar no lucro (MA7 já do lado do ganho). É a regra que já existe ("no lucro, aperta o stop e garante ganho"), aplicada com a MA7.
Proposta: em vez de "martelo = stop na MA7", usar "short no lucro com a MA7 abaixo da entrada (ou alvo já atingido) → stop na MA7; trade recém-aberto/sem lucro → stop segue na MA21 mesmo com candle forte contra".
