# Placar: nosso Log x Dollynho

| Data/hora (Brasília) | TF | Leituras batidas | Diferenças | Ajuste feito |
|---|---|---|---|---|
| 09/11/2026 14:09 | 343 | fechamento 74.782; abaixo MA7/EMA7; recuperou MA1617; recuperou Média do RSI; abaixo do Suporte Inferior; Stoch acima de 50 | toque na MA21 (pavio a 0,04%); alvos MA1372 + RSI 23.67 e stop EMA21 (trade contínuo); Linha Verde (manual) | tolerância de toque 0,15%; linha 72,86; escada de médias; estado de trade entre Logs |
| 09/11/2026 (cronologia) | 343/686/1D | — | não sabíamos do short aberto desde 03/11 | estado.json reconstruído com a cronologia; regra de stop corrigida (ele reposiciona candle a candle) |
| 09/11/2026 19:52 | 343 | fechamento 75.139 idêntico; ACIMA da MA7/EMA7; RSI no Suporte Inferior (42,3 x 43,6); Stoch indo para a Resistência Superior (cautela); stop MA21/EMA21; acima da MA1617 e MA686; abaixo da MA21 | Stoch dele ~1 vela à frente (print na vela nova); ele não repetiu alvos no texto; Linha Verde (manual) | nenhum (bateu) |
| 09/11/2026 21:00 | 1D/686/343 | Diário ABAIXO da MA343 e da Média do RSI, Stoch abaixo de 20; 686/343 ACIMA da MA7/EMA7; 343 RSI no Suporte Inferior; Stoch na máxima; short mantido | ele não citou alvos do 686 | nenhum |
| 10/11/2026 08:26 | 343 | rejeição; ABAIXO da MA7/EMA7, MA1617 e Média do RSI; Stoch abaixo de 80; short mantido | ele leu "rejeição da MA21"; nós lemos rejeição da MA7/EMA7 | nenhum (1ª vez) |
| 10/11/2026 14:09 | 343 | perdeu MA686; 🎯 MA777/MA1372 perto; RSI perto de 23.67 | nós apertamos o stop para a MA7 (ele não informou) | nenhum |
| 10/11/2026 21:00 | 1D | tocou MA231 (QED); abaixo da MA343 e da Média do RSI | **nós liquidamos o trade; ele realizou parciais e manteve**; não narramos a MA7 cruzando a MA343 | regra de parcial + `ma_crosses` nos dados |
| 10/11/2026 21:00 | 2D | pavio na MA77 do 2D, fechou acima; Stoch zerado; BBB 2 de 3 | — | nenhum (bateu) |
| 10/11/2026 21:00 | 686/343 | 686 abaixo da MA7 e da Média do RSI, Stoch bearish; 343 acima da MA686 e da Média do RSI, Stoch bullish, abaixo da MA7; 🎯 MA1372 e RSI 23.67; stop MA7/EMA7 | — | nenhum (bateu) |
| 11/11/2026 08:26 | 343 | — | **nós fechamos o short ao recuperar a MA7; ele manteve** | regra: recuperar a MA7 com RSI abaixo do Suporte Inferior não fecha o short |
| 11/11/2026 14:09 | 343 | recuperou MA7/EMA7; RSI abaixo do Suporte Inferior; stop MA21/EMA21; Stoch testando 80 | **nós abrimos long; ele seguiu short e alertou contra longs** (corrigido no próprio Log) | regra: não inverter dentro do stop; long exige RSI acima de ~43,6 |
