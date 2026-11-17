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
- Linha do Bilau no RSI 2D: 25,78 (confirmada 3x nos prints dele; config corrigida em 14/11; 26,21 = referência Raicher). Pode citar o número: "RSI 2D (28,x) a ~2 pontos do Bilau (25,78)".

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

## 14/11 08:26 (aprendizado — IMPORTANTE)
- O STOP do short agora é a MA7/EMA7 do 343 (ajuste dele em 14/11 08:26), com alvo na Linha Vermelha (~62,4-62,8K). Na 📌: "❌ Stop: fechamento ACIMA da MA7/EMA7 (valor)". Ele só aperta o stop; o stop em lucro nunca volta a prejuízo. Ler estado.json: o campo stop é a verdade.
- RSI abaixo de 23.67: o 23.67 é "a principal Resistência local". Acompanhe a MÉDIA do RSI: se a Média vier para baixo de 23.67, "nova aceleração, aí sim marcando o fundo". Use: "A Média do RSI (27,2) já se aproxima dos 23.67".
- Antes do fechamento Semanal (domingo 21:00): "Amanhã temos fechamento Semanal, volatilidade!" e a cautela "Não alavanque! Modere a mão e cuidado com a ganância."
- Saudação do 08:26: "Bom dia, amiguinhos!" é aceitável (3 de 4).

## 14/11 (Bilau)
O Dollynho avisa "LATEJANDO" (🍆) quando o BBB do 2D está perto: preço abaixo da MA200 do 2D + Stoch 2D < 20,44 + RSI 2D chegando em 25,78. No Log do 2D das 21:00 (14/11): diga qual condição falta e o alvo se confirmar (MA777 do 2D ~63K), e se o RSI 2D fechou abaixo de 25,78 diga "BILAU CONFIRMADO" (QED).

## 14/11 14:28 (stop duplo)
Stop do short 343 = fechamento ACIMA da MA7/EMA7 E RSI acima do Suporte Histórico (23,67). Citar "Média do RSI = nova resistência" quando ela alcançar o RSI. Alvo: Linha Vermelha.

## 14/11 21:00 (pós-Bilau)
Bilau 2D confirmado pelo post dele. Tom: "daqui pra baixo só long, sem novo short"; short existente: zerar na Linha Vermelha ou stop MA7/EMA7. 686 pode sair separado do 343. Alvo de capitulação ("rosquinha") = MA77 Mensal ~53,2K; Linha Laranja ~59K = suporte do 686; MA1617 1D = suporte do fundo dos 58K. Stoch "absolutamente zerado" quando K=D=0. Rodar alvos.py (agora com 1M).

## CORREÇÃO 14/11 23:37 (viés após Bilau)
Erro do Log 329: concluímos "mantém short / sigo bearish" quando ele concluiu "daqui pra baixo só long". Regra: com Bilau 2D confirmado, a conclusão dos Logs é VIÉS DE COMPRA ("daqui pra baixo não tem short"); o short existente só é mantido até o alvo (Linha Vermelha) ou stop (MA7/EMA7) e o Log diz isso como "zerar o trade", nunca como "sigo bearish". Não abrir short novo. Não escrever "cuidado com shorts atrasados" E "mantém short" no mesmo Log. Entrada long só quando ele avisar ou a regra de long (343 acima da MA7/EMA7) disparar.

## REGRA PRINCIPAL (Augustus, 14/11 23:42): DADOS, NÃO ADIVINHAÇÃO
Mesmos dados (Bitstamp, mesmos indicadores) = mesmas conclusões. A conclusão de cada Log sai SÓ da aplicação das regras abaixo aos números do JSON. Nunca escrever o que "o Dollynho deve dizer", nunca esperar ou supor um post dele, nunca suavizar ou inverter uma conclusão para "parecer" com ele. Se as regras apontam algo, escreva com firmeza.
Tabela de decisão (aplicar em ordem, a primeira que valer decide a conclusão do Log):
1. Bilau 2D confirmado (fechamento 2D: preço < MA200 2D, RSI 2D < 25.78, Stoch 2D < 20.44) → conclusão: "daqui pra baixo só long, sem short novo". Short aberto só vai até o alvo atual ou o stop ("zerar o trade"), nunca "sigo bearish". Vale até o RSI 2D voltar acima da Média do RSI 2D.
2. RSI do timeframe < 23.67 (Suporte Histórico) → "sem short novo aqui"; short aberto mantido até alvo/stop.
3. Stoch cruzou bullish abaixo de 20 com RSI < 30 → "sinal de esgotamento da queda" (cuidado com shorts).
4. Long só dispara com 343 fechando ACIMA da MA7/EMA7 E RSI acima de 23.67 (ou o setup BTFD/Agulhada do método).
5. Nada acima → seguir o viés de tendência (preço x MA7 + RSI x Média).
Linha 🧭 e "Seguimos..." devem bater com esta tabela. Proibido no mesmo Log: "mantém short / sigo bearish" junto com regra 1 ativa.

## DECISÃO DE POSIÇÃO (obrigatória em todo Log, Augustus 14/11 23:48)
Logo depois da linha 🧭, escreva uma linha:
"⚖️ Posição pelos dados: MANTER <lado> | ZERAR <lado> | ZERAR e ABRIR <outro lado> | FICAR DE FORA | ABRIR <lado> — porque <regra que decidiu, em poucas palavras com os números>"
Como decidir (só com os números do JSON e estado.json, nesta ordem):
A. Fechou além do stop do trade aberto (ex.: short: 343 ACIMA da MA7/EMA7 E RSI acima de 23.67) → ZERAR. Abrir o lado oposto só se a condição de entrada desse lado também fechou (long: 343 ACIMA da MA7/EMA7 + RSI acima de 23.67 + Stoch > 20 e não no topo; short: rejeição da MA7/EMA7 + RSI rejeitando o Suporte Inferior + Stoch virando para baixo). Senão, FICAR DE FORA.
B. Alvo final do trade atingido → ZERAR. Se a regra 1 (Bilau) ou 2 (RSI < 23.67) da tabela estiver ativa, não abrir short novo; long só quando A disparar para long.
C. Regra 1 (Bilau 2D) ativa com short aberto → MANTER só até o alvo atual/stop, escrito como "manter até zerar na <alvo>"; nunca abrir short novo.
D. Trade aberto, nem stop nem alvo final → MANTER.
E. Sem trade → ABRIR só se a condição de entrada de A fechou neste candle; senão FICAR DE FORA e dizer a condição que falta.
O que valer aqui atualiza logs/estado.json (entrada/stop/trade_anterior). A linha ⚖️, a 🧭 e o texto do post não podem se contradizer.
Toda divergência entre nossa ⚖️ e a decisão dele vai para o placar com a regra que faltou.

## 15/11 09:42 (provisório, 1x): long no pullback com divergência
Depois de zerar no alvo e com Bilau ativo: se o 343 dispara o gatilho de long (acima da MA7/EMA7) com Stoch K > ~80, a ⚖️ é FICAR DE FORA ("Stoch nas máximas, cuidado; long no pullback"). Long preferencial: pullback do RSI à sua Média / ao 23.67 formando divergência de alta (preço faz fundo igual ou menor, RSI faz fundo mais alto e segura acima de 23.67) + Stoch voltando a cruzar para cima. Avisar "👀 possível divergência se formando" quando acontecer.

## Consolidação 15/11 (ver calibracao/decisoes_dollynho.md)
Antes de escrever a ⚖️, leia calibracao/decisoes_dollynho.md e decida como os padrões 1-6 de lá mandam: direção pelos prazos maiores, timing pelo 343; candle contra não fecha trade (só o stop); no lucro aperta stop e parcial no alvo intermediário com prazos maiores a favor; zera no alvo final ou quando Bilau 2D + RSI < 23,67 + Stoch cruzando para cima aparecem juntos; não vira a mão no candle em que zera; Stoch no teto = não compra, Stoch zerado = não vende.

## 15/11 21:00 (Semanal): fundos de bear
Log Semanal com preço abaixo da MA49 1W: citar as médias de fundo de bear do Semanal com valor — MA231, EMA343 e MA343 1W — como "nos ciclos anteriores o fundo tocou a EMA343 ou a MA343; não descarto visita". Zona ~52,6–56,9K (EMA343/MA343 1W + MA77 1M) é o destino de capitulação; não muda a decisão do 343, mas entra nos níveis de invalidação do long ("se perder 61,9K e a MA231 1W, próximo destino EMA343 1W").

## 15/11 21:00 (Diário): faixa imediata primeiro
No Diário, cite primeiro a faixa onde o preço está preso (suporte e resistência mais próximos, incluindo os níveis manuais do alvos.py: linha laranja ~64,45K e Agulhada 2024 ~65,4-65,9K) antes de médias distantes. Cruzamento da MA7 já anunciado em Log anterior não se repete (2ª ocorrência: regra firme).

## 15/11 21:00 (686 e 343): alinhamento
Long (ou short) no 343 só quando o 686 também está do mesmo lado da MA7. 343 acima da MA7/EMA7 com 686 abaixo da MA7 = "inconsistência entre 686 e 343" → ⚖️ FICAR DE FORA, aguardando. Próxima resistência do RSI do 343 acima de 30 = Suporte Inferior (~43,6).

## 16/11 19:52 (aprendizado, provisório 1x)
- 343 voltando ACIMA da MA7/EMA7 após rejeições: "De volta ACIMA da MA7/EMA7;".
- Stoch K x D bullish no teto / voltando a subir: "E o Stoch volta a mirar a Máxima!" (neutro, sem 🚨 nem "cuidado com longs"). "🚨 Stoch cruzou!! CUIDADO!!" fica para o cruzamento bearish a partir do teto (ou K perdendo 20). A ⚖️ continua FICAR DE FORA com Stoch no teto.
- RSI do 343 abaixo do Suporte Inferior em repique: "Seguimos atentos ao Suporte Inferior no RSI, deve atuar como Resistência!!" (2ª vez, regra firme).
- Fecho do 19:52 pode ser "Seguimos, até o fechamento do Diário."

## 16/11 21:00: dois horizontes
Depois do Bilau, o Log do 2D separa: (1) TRADE 343/686 — baliza MA7/EMA7 nos dois; abaixo, fora e esperar divergência no RSI; short arriscado; (2) POSIÇÃO DE LONGO PRAZO — abaixo da EMA777 do 2D é zona de compra ("promoção"), alvo longo MA200 do 2D. A linha ⚖️ continua sendo do trade; a zona de longo prazo vai numa linha do texto do 2D, sem tamanho de posição. Lembrar: em 2018 e 2022 houve 2º dip depois do BBB.
