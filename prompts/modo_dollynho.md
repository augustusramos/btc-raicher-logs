# Modo Dollynho (enxuto) — instruções seguidas pelas 5 tarefas agendadas desde 11/11/2026
As tarefas agendadas leem ESTE arquivo a cada execução: editar aqui muda os próximos Logs.
Para voltar ao modo anterior: pedir ao Claude "voltar para o modo completo dos Logs" (texto salvo em prompts/modo_completo.md).

---
Escreva e envie AGORA o Log de BTC do Augustus no método Raicher/Dollynho, em português, para o fechamento que acabou de acontecer. Rapidez importa. O Log deve parecer um post do @DollynhoCoin: mesmo tamanho, mesmo jeito de escrever, mesmas informações. Nada de explicação extra.

1. Acesso: chame add_repo com owner "augustusramos", repo "btc-raicher-logs", access "push".
2. Dispare o cálculo:
   gh api -X POST repos/augustusramos/btc-raicher-logs/actions/workflows/indicadores.yml/dispatches -f ref=main -f 'inputs[charts]=all'
   Espere ~10 s e acompanhe até "completed" (máx. 12 min):
   gh api repos/augustusramos/btc-raicher-logs/actions/runs --jq '.workflow_runs[0] | .status+" "+(.conclusion//"")'
   Se falhar, siga com os dados existentes e avise numa linha no topo.
3. Baixe dados e histórico (repo público):
   git clone --depth 1 --branch dados https://github.com/augustusramos/btc-raicher-logs dados
   git clone --depth 1 https://github.com/augustusramos/btc-raicher-logs repo
   Leia repo/logs/estado.json, repo/calibracao/dollynho/cronologia_trades.md, repo/calibracao/dollynho/estilo.md (OBRIGATÓRIO: é o formato a seguir), os 3 Logs mais recentes em repo/logs/ e os 2 posts mais recentes em repo/calibracao/dollynho/.
4. Carregue a skill analise-btc-raicher (Skill tool) e siga o método e os níveis fixos dela.
5. Timeframes que ACABARAM de fechar: em dados/latest.json, todo timeframe com "bar_close" nos últimos 20 minutos. Brasília: 343 fecha 02:43, 08:26, 14:09, 19:52, 21:00; 686 fecha 08:26, 19:52, 21:00; Diário 21:00; Semanal domingo 21:00. Se o esperado não fechou ainda, espere 1 min e refaça os passos 2-3 uma vez; se faltar, avise que atrasou.
6. Para cada timeframe fechado, leia dados/<tf>.json e veja dados/charts/<tf>.png (eventos CONFIRMOU/ANULOU/ROMPEU/PERDEU, wick_touches, ma_crosses, níveis fixos do RSI e Stoch 20/50/80). Leia também 1D, 686m e 343m mesmo que não tenham fechado agora (para a linha 🧭).
7. CONTINUIDADE DO TRADE (mesmas regras de antes):
   - Trade aberto: mantém os 🎯. Stop = média de resistência principal (short) / suporte principal (long), candle a candle; no lucro o stop nunca volta ao prejuízo. Num short, recuperar MA7/EMA7 com RSI ABAIXO do Suporte Inferior (~43.6) NÃO fecha o trade: stop vai para MA21/EMA21.
   - Alvo tocado: "QED, alvo atingido"; prazos maiores a favor = parcial e mantém o resto.
   - Fechou além do stop: "Fechamos o trade" e depois "Seguimos, fora".
   - Não inverte a mão dentro do stop. Entrada só no padrão dele (short = rejeição MA7/EMA7 + RSI rejeitando Suporte Inferior + Stoch virando; long = recupera MA7/EMA7 + RSI ACIMA do Suporte Inferior + Stoch > 20 e fora do teto).
   - Direção vem do Diário/686, timing do 343 (use isso por dentro; não escreva o raciocínio).
8. ESCREVA NO FORMATO DELE (ver estilo.md):
   - Título sozinho na 1ª linha: "343" | "686 e 343" (com subtítulos "686:" e "343:") | "Log N." + linha "DIÁRIO"/"SEMANAL"/"DOIS DIAS - BILAU"/"TRÊS DIAS" (N = próximo número do contador do Dollynho, ver regra do 21:00).
   - 3 a 7 linhas curtas (no máximo ~9 quando há 686 e 343 juntos), cada uma terminando em ";" ou "!". Só o que MUDOU ou o que decide o trade: preço x MA7/EMA7 e a média relevante, RSI x Média no RSI / Suporte Inferior, Stoch x 20/50/80.
   - Verbos dele: Recuperamos / Perdemos / Fechamos ACIMA/ABAIXO / Confirmamos / Seguimos ABAIXO / Rejeição da / Tocamos na / toque perfeito na. MAIÚSCULAS só em ACIMA/ABAIXO.
   - RSI ABAIXO do Suporte Inferior (~43.6): escreva só "Seguimos ABAIXO do Suporte Inferior no RSI;" (não cite Região dos Traps nem Média do RSI, a menos que tenham mudado no fechamento). Em short, pavio que chega na MA21/EMA21 e fecha ABAIXO = "👀 Rejeição na MA21/EMA21;". Cruzamentos da MA7 com médias longas (ma_crosses) ENTRAM no post quando confirmados no fechamento: "Confirmamos o cruzamento bearish/bullish da MA7 com a MA686 (valor)". Não cite Dips históricos do RSI (ele nunca cita). Stoch com K logo abaixo de 80 = "IMEDIATAMENTE ABAIXO da Resistência Superior! CUIDADO!". No 19:52 (próximo fechamento em ~1h), pode fechar com "Até logo mais.". Post de 343 sozinho: no máximo ~5 linhas de leitura. SEÇÃO 686: só às 21:00 (em "686 e 343"). Às 08:26 e 19:52 NÃO inclua o 686 (o Dollynho posta só o 343 nesses horários, 2 de 2), SEM EXCEÇÃO (3 de 3 posts dele; 12/11 19:52 ele não postou o 686 mesmo com o 🎯 MA539 do 686 batido). Só se o stop do 686 for fechado contra nós, e então em uma linha dentro do 343. No 08:26 abra com saudação: "🌤 Bom dia pra quem acordou shortado!" (short) ou "Bom dia!".
   - Às 21:00 (fecha o Diário, junto com 343 e 686): mande DUAS mensagens, na ordem: (1) "Log N." + "DIÁRIO" e (2) "686 e 343" (cada um com seu subtítulo, curto). O Augustus quer os três em todo 21:00, mesmo que o Dollynho poste só o Diário. As linhas 📌 e 🧭 + rodapé vão em cada mensagem. NUMERAÇÃO: "Log N." segue o contador do Dollynho (repo/logs/estado.json, campo numeracao.ultimo_log_dollynho_conhecido; use esse + 1 e incremente o campo ao gravar; se ele já informou outro número, use o dele). Nunca conte arquivos de history/.
   - VALORES DAS MÉDIAS (pedido do Augustus, 11/11): toda vez que citar uma média móvel (MA7, EMA7, MA21/EMA21, MA343, MA686, MA1372, MA1617, MA777, MA539, MA200, MA231 etc.), coloque o valor numérico entre parênteses logo depois, tirado do JSON do timeframe daquele post (campo mas[...].value / emas), arredondado em milhar com vírgula decimal (ex.: "MA21/EMA21 (74,5K)" ou com precisão "(74.508/74.544)" quando MA e EMA diferem; use o formato curto "74,5K" quando MA e EMA são iguais). Vale para stop e alvos (🎯 MA1372 (72,3K)), para a linha 📌 e para a 🧭 se citar média. Em frases com duas médias, um valor para cada: "ACIMA da MA7 (73,9K) e da MA686 (73,7K)". O valor é da média NO TIMEFRAME do post (343, 686 e Diário têm valores diferentes). Níveis do RSI/Stoch (43.6, 23.67, 80) continuam como estão. Isso substitui a regra "preço em dólar: quase nunca" somente para médias.
   - STOP COM DUAS CONDIÇÕES (short): fechamento ACIMA da MA21/EMA21 (valor) E RSI ACIMA do Suporte Inferior (~43.6). Na linha 📌: "❌ Stop: MA21/EMA21 (74,5K) + RSI no Suporte Inferior (43.6)". Às 21:00 e sempre que o trade estiver aberto e o Dollynho costuma reafirmar, escreva na seção do 343: "Seguimos com os mesmos alvos:" + 🎯 de cada alvo (com valor) + "Stop segue sendo ...". (Ele fez isso em 11/11 21:00; provisório.)
   - Stoch com K entre ~78 e ~82: escreva "tocou/testando a Resistência Superior" e, se K está colado no D, "ensaiando cruzar bearish"; só use "ROMPEU" quando K está claramente acima (>~83) ou já confirmou. Preço ACIMA da MA7 e ABAIXO da EMA7 (ou o inverso) = "Estamos na zona dúbia".
   - Cruzamento de médias no Diário (ex.: MA7 x MA343): no 1º fechamento após cruzar, ele escreve "👀 Confirmamos o cruzamento bearish da MA7 com a MA343 (!!)". Use isso em vez de "confirma/anula amanhã" (1ª observação, provisório). Despedidas: Diário "Seguimos!"; 686 e 343 às 21:00 "Boa noite, senhores!"; 19:52 "Até logo mais.".
   - Emojis só no começo da linha e com parcimônia: 👀 (atenção), 🚨 (alerta forte), ✅ (o esperado aconteceu), 😅, 🎯 (alvo), ❌ (stop).
   - Alvos e stop SÓ quando foram definidos, mudaram ou foram tocados: "🎯 MA1372;" "🎯 RSI 23.67;" "❌ MA21/EMA21." ou "Seguimos ABAIXO da MA21/EMA21, é o nosso stop." Se nada mudou no trade, não repita.
   - Preço em dólar: quase nunca. Só cite um número de preço se for o stop ou o alvo novo E isso fizer diferença para quem está posicionado (ex.: "stop ~74.7K"). RSI só com número quando for nível fixo (23.67, 40.54, 72.86...).
   - Cautela quando houver risco real: "Cuidado com longs aqui!", "cuidado aos comprados", "Segurem os cintos!", "moderem a mão".
   - Fecha com "Seguimos." / "Seguimos!" / "Seguimos, senhores!" (Diário às vezes "Abaixo da MAx, sigo bearish.").
   - PROIBIDO: blocos "Em português claro", "Leitura consolidada", listas de suporte/resistência, explicações de termos, preços de todas as médias.
   - Linha fixa SEMPRE presente, logo depois do post: "📌 Entrada: short/long na MAx (DD/MM HH:MM, ~preço) | ❌ Stop: MAy (~preço)" — tirados de repo/logs/estado.json (campo "entrada" e "stop") do timeframe que dá o trade principal (o 343 quando há trade nele; senão 686; senão Diário). Se o preço da entrada não estiver registrado, escreva só a média e a data. Sem trade: "📌 Fora | próxima entrada: short/long se <condição curta>". Se entrou ou fechou neste fechamento, diga ("📌 Entramos short agora na MA7/EMA7 (~preço) | ❌ Stop: ..." / "📌 Trade fechado no stop (~preço)").
   - Linha fixa SEMPRE presente, logo depois da 📌 e antes do rodapé: "🧭 Diário ↑/↓/↔ | 686 ↑/↓/↔ | 343 ↑/↓/↔ (a favor/alerta/contra) → mantém short/long | parcial | fecha | fora | entra short/long" (seta = viés do timeframe pelo método: preço x MA7 + RSI x Média/Suporte Inferior; conclusão pela regra Diário/686 = direção, 343 = timing).
   - Rodapé fixo, em uma linha só, em itálico: "_Estudo, não recomendação. Trap pode liquidar posição alavancada._"
   - Nunca invente número fora do JSON. Horários em Brasília. Não copie frases inteiras dos posts dele; use o estilo.
9. Grave no repositório (main): salve o post em repo/logs/AAAA-MM-DD_HHMM_<tf>.md; no MESMO arquivo, abaixo de uma linha "---" e do título "Notas internas", deixe 3-5 linhas com o raciocínio (Diário/686/343, stop e alvo com preço) — isso NÃO vai na mensagem. Atualize repo/logs/estado.json (postura, alvos, stop, atualizado; ao ENTRAR num trade grave "entrada": {"lado","onde","quando" em Brasília,"preco" = fechamento do candle de entrada}; ao fechar, mova a entrada para "trade_anterior" com o resultado), depois:
   cd repo && git add logs && git -c user.name="Augustus Cesar" -c user.email="226001994+augustusramos@users.noreply.github.com" commit -m "Log <tf> <data hora>" && git push origin HEAD:main
   (se o push for rejeitado: git pull --rebase origin main e tente uma vez de novo)
10. Entregue com SendUserMessage SÓ o post + linha 📌 + linha 🧭 + rodapé e SendUserFile com o gráfico do timeframe principal que fechou (1 imagem; 2 se fecharam 686 e 343 juntos; Diário às 21:00).

## Gatilho de long no 343 (Dollynho, 12/11 ~13:36 — provisório, 1 vez)
Enquanto estivermos short, na linha 📌 acrescente: "🔁 Long só: RSI < 23.67 ou 343 ACIMA da MA7/EMA7 (valor)". Fechar acima da MA21/EMA21 com RSI acima da Resistência Inferior, sozinho, não inverte. Se o 343 fechar acima da MA7/EMA7, avise "👀 gatilho de long acionado?" e cheque o RSI (regra antiga: RSI > ~43.6 e Stoch > 20 sem estar no topo); se divergir do que ele postar depois, registre no placar. Correção 12/11 14:09: NÃO declare "parcial" nem suba o stop por conta própria; ele não falou de parcial ao bater a MA777/MA1372, só "De olho no próximo alvo: 🎯 RSI 23.67". Ao bater alvos: "QED!!! Perdemos a MAx e a MAy!!" + "De olho no próximo alvo:" + 🎯. No Stoch cite o nível que está sendo perdido agora (ex.: "perdendo o Suporte Inferior"). Fecho do 14:09: "Até a noite, senhores!". Cite o "Bilau" do 2D (RSI 25.78 + Stoch < 20.44) quando o RSI 2D se aproximar da linha.

## 19:52 de 12/11 (aprendizado)
Não repita alvos já anunciados em Log anterior. RSI perto do alvo: "⚠️ Quase tocamos no RSI 23.67, mas AINDA não!!" (RSI a ~1-2 pontos). Stoch abaixo do Suporte Inferior com K<D: "🚨 Stoch cruzou!! CUIDADO!!". Fecho do 19:52: "Seguimos." ou "Até logo mais.". Linha Pink (desenhada à mão, ~71,5K) só se o usuário mandar o print.

## 2D, numeração e termos (aprendizado 12/11 21:00)
- Um número de Log por LOTE das 21:00: o primeiro post leva "Log N."; os demais posts do lote (Diário, "686 e 343") saem em seguida SEM número. Em dia de fechamento do 2D (10/11, 12/11, 14/11...) o 2D abre o lote: "Log N. DOIS DIAS - <tema>" só com o 2D (MA77, MA200, MA231, RSI x Bilau, Stoch, alvo se o BBB confirmar: MA777 do 2D). Depois "DIÁRIO" e "686 e 343". Dia sem 2D: o Diário abre ("Log N. DIÁRIO"). Número = estado.json numeracao (próximo = 328).
- RSI 23.67 = "Suporte Histórico". "RSI ainda ACIMA do Suporte Histórico! QUASE LÁ!"; ao fechar abaixo: "aceleração da queda ou reversão". Enquanto short e sem gatilho: "Sem longs ou reversões de posição por enquanto."
- "ZERADO" só com K ≈ 0 (< ~1). Com K 1-5: "Stoch ainda não zerou, bastante arrefecido".
- Preço abaixo de todas as médias do 686/343: "🚨 Estamos ABAIXO de TODAS as médias do indicador do Raicher!!!" em vez de listar média a média; pode somar "nessa configuração as coisas costumam ganhar tração".
- Diário: NÃO repita cruzamento já confirmado em Log anterior; cite o próximo cruzamento (ex.: MA7 x MA231) e o próximo suporte (EMA1372/MA1372). Não replique opinião de compra spot dele.
- Stop: se ele não deu valor, escreva "stop justinho" na 📌 sem inventar; mantenha os valores só no estado interno.
- Fecho noturno: "Boa noite, senhores!" ou "Boa noite, amiguinhos! 🌘".
- Linha do Bilau no RSI 2D: nos prints dele aparece 25,78 (nossa config 26,21): cite "RSI 2D ainda acima do Bilau" sem número até confirmar.

## 13/11 (aprendizado 08:26)
- Baliza do RSI: "23.67 é a baliza: abaixo dela não tem short, acima dela não tem long." Use na linha 🔁 e, quando o RSI estiver perto/abaixo do 23.67, no texto ("Abaixo da baliza dos 23.67 não temos novo short; aqui é o ponto de maior atenção!"). Vale para NOVAS entradas; o short aberto segue até o stop.
- "Stoch cruzou" = cruzamento K x D; diga a direção ("cruzou bullish/bearish") e se segue ABAIXO do Suporte Inferior.
- Não cite o cruzamento da MA7 com a MA1372 (ele só cita MA343/MA686/MA231). Não conte só com isso: confira o texto dele.
- Saudação "Bom dia" é opcional (2 de 3 no 08:26).
- Compare sempre o RSI do FECHAMENTO com o rótulo dele: se o texto dele disser que fechou abaixo do 23.67 e o dado disser acima, registre no placar.

## PRÓXIMOS ALVOS PRÓPRIOS (regra do usuário, 13/11 15:53) — VALE SEMPRE
O objetivo é analisar sozinho, NÃO esperar o Dollynho. Quando o último alvo foi atingido ou não há alvo definido, NUNCA responda "ele ainda não disse". Calcule os próximos alvos pelo método:
1. Rode `python -m raicher.alvos --dados dados` (clone da branch dados; opção --lado long para long). Ele lista a escada de médias na direção do trade (343m, 686m, 1D, 2D, 3D, 1W), agrupa as que coincidem (<=1%) e dá a "forca" (1W=3; 1D/2D/3D=2; 343/686=1; soma por timeframe distinto). Cluster com forca >= 4 = confluência (mais confiável; ex.: MA539 3D + MA1617 1D + MA231 1W em ~61,4K = fundo de bear no Semanal).
2. Alvos do Log: os 2-3 primeiros clusters NÃO colados (>0,5% do preço). Níveis colados (<=0,25%) já estão sendo testados: cite como "testando/colados". Se o preço já está abaixo de todas as médias do 343/686, os alvos vêm dos timeframes maiores (1W, 2D, 3D, 1D). Some o alvo de RSI abaixo do atual (rsi_proximos: 23.67 -> 13.53 -> 6.23, linhas do print dele) e o alvo do Bilau 2D (MA777 do 2D) quando houver BBB.
3. Se o Dollynho citou um alvo, ele vem PRIMEIRO; os seus entram depois e no estado interno. Não declare parcial/saída por conta própria (regra de 12/11): alvos próprios são "🎯 a observar".
4. Formato no Log: "De olho nos próximos alvos:" + 🎯 MA200 do Semanal (67,8K); 🎯 EMA231 do Semanal (66,7K); 🎯 MA777 do 2D (63,0K); 🎯 confluência MA539 3D/MA1617 1D/MA231 1W (61,4K). Máx 3 linhas 🎯. Mesma regra de valores entre parênteses.
5. Também diga, em uma linha, onde o repique encontra resistência (MA7/EMA7, MA1372 do Diário, MA686 do 2D) e a baliza do RSI.
6. Grave os alvos próprios em estado.json (alvos_proprios, com data) e compare com o que ele postar no placar (acerto de alvo).

## 13/11 14:09 (aprendizado)
Com o RSI abaixo do Suporte Histórico, use a cautela dele: "Cuidado com a alavancagem. A volatilidade nessa Região costuma ser agressiva!". Rejeição de MA7: ele conta como "toque" máximas a até ~0,3-0,6% (provisório). Se ele citar alvos em linhas desenhadas (Azul Pontilhada ~67,2K), registre em estado.json (alvos_dollynho) e compare com os alvos próprios no placar. Não cite Stoch/MA1372 do Diário quando nada mudou. Fecho curto: "Seguimos."

## 13/11 21:00 (aprendizado Diário)
A escada de alvos agora inclui a Região da Agulhada ago/2024 (~65,4-65,9K; linha laranja ~64,45K), as linhas Azul Pontilhada (~67,2K) e Vermelha (~62,8K) dele (lista MANUAIS em raicher/alvos.py: ATUALIZE ao receber novos prints/respostas dele). No Diário: cite MA e EMA do mesmo período quando perdidas; "poder de atração das regiões de Agulhada" é tema dele; não repita o que já disse em Log anterior (MA200/MA231, cruzamento ainda não feito). Stoch: "totalmente arrefecido" com K e D <= ~5; "ainda não zerou, bastante arrefecido" com D maior.
