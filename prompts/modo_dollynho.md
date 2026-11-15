# Modo DADOS — instruções seguidas pelas 5 tarefas agendadas (desde 14/11/2026 23:39)
Pedido do Augustus: NÃO tentar adivinhar o que o Dollynho vai dizer. Mostrar os dados do fechamento (mesma fonte e mesmos indicadores dele) e dizer, dado por dado, se é BULLISH ou BEARISH pelas regras do método. Sem trade, sem entrada, sem stop, sem "mantém short", sem postura, sem imitar o estilo dele.
(O modo antigo, que imitava os posts, está em prompts/modo_dollynho_antigo.md.)

1. Acesso: add_repo owner "augustusramos", repo "btc-raicher-logs", access "push".
2. Dispare o cálculo:
   gh api -X POST repos/augustusramos/btc-raicher-logs/actions/workflows/indicadores.yml/dispatches -f ref=main -f 'inputs[charts]=all'
   Espere ~10 s e acompanhe até "completed" (máx. 12 min):
   gh api repos/augustusramos/btc-raicher-logs/actions/runs --jq '.workflow_runs[0] | .status+" "+(.conclusion//"")'
   Se falhar, siga com os dados existentes e avise numa linha no topo.
3. git clone --depth 1 --branch dados https://github.com/augustusramos/btc-raicher-logs dados
   git clone --depth 1 https://github.com/augustusramos/btc-raicher-logs repo
4. Timeframes que ACABARAM de fechar (Brasília): 343 às 02:43, 08:26, 14:09, 19:52, 21:00; 686 às 08:26, 19:52, 21:00; Diário 21:00; 2D às 21:00 nos dias de fechamento do 2D; Semanal domingo 21:00. Confirme pelo "bar_close" em dados/latest.json (últimos 20 min). Se o esperado não fechou, espere 1 min e refaça 2-3 uma vez.
5. Rode: cd repo && python -m raicher.leitura --dados ../dados --tf <timeframes que fecharam, do maior para o menor>
   Essa saída É o Log. Copie as linhas como estão (podem ser levemente encurtadas, nunca reinterpretadas). Não acrescente classificação que o script não deu. Não invente número fora do JSON.
6. Acrescente no fim, só se existir no JSON, uma linha "Níveis próximos:" com a média logo acima e a logo abaixo do preço no menor timeframe que fechou (ladder_above[0] e ladder_below[0], com valor). Isto é informação, não alvo.
7. Formato da mensagem:
   Título: "Leitura <timeframes> — DD/MM HH:MM"
   Blocos por timeframe (🟢 BULLISH / 🔴 BEARISH / ⚪ NEUTRO + placar do timeframe).
   Linha final: "Total: X bullish x Y bearish (tendência: ...; exaustão/setups: ...)" — sem conclusão de compra ou venda.
   Rodapé em itálico: "_Dados classificados pelas regras do método. Não é recomendação; alavancagem pode liquidar._"
   PROIBIDO: linhas 📌/🧭, entrada, stop, alvo, "mantém short/long", "sigo bearish", "daqui pra baixo só long", previsões, imitar o Dollynho.
8. Grave em repo/logs/AAAA-MM-DD_HHMM_<tfs>.md e faça commit:
   cd repo && git add logs && git -c user.name="Augustus Cesar" -c user.email="226001994+augustusramos@users.noreply.github.com" commit -m "Leitura <tfs> <data hora>" && git push origin HEAD:main
   (se rejeitado: git pull --rebase origin main e tente uma vez de novo)
9. Entregue com SendUserMessage a mensagem e com SendUserFile o gráfico do maior timeframe que fechou (dados/charts/<tf>.png).

## Regras de classificação (resumo do que o script aplica)
- Preço ACIMA de uma média / recuperou = BULLISH; ABAIXO / perdeu = BEARISH (MA7, EMA7, MA21, EMA21, MA49, MA77, MA200, MA231, MA343, MA539, MA686, MA777, MA1372, MA1617).
- MA7 cruzando para cima uma média longa = BULLISH; para baixo = BEARISH.
- RSI acima da Média do RSI = BULLISH; abaixo = BEARISH. RSI ≥ 50 = BULLISH; abaixo do Suporte Inferior (~43.6) = BEARISH; Região dos Traps (40.54–43.6) = NEUTRO.
- Exaustão: RSI < 30 e < 23.67 (Suporte Histórico) = BULLISH (sobrevenda; no método "abaixo de 23.67 não tem short"); RSI > 70 / 72.86 = BEARISH.
- Stoch K cruzou acima do D = BULLISH; abaixo = BEARISH; K < 20 ou zerado = BULLISH (sobrevenda); K > 80 = BEARISH (sobrecompra).
- Setups: Bilau 2D confirmado, Agulhada, BTFD MA343 1D / MA49 1W = BULLISH; MA77 cruzando abaixo da MA200 no 2D = BEARISH.
- Tendência (médias, RSI x Média, Stoch K x D) e exaustão/setups aparecem separados no placar, porque podem apontar em sentidos opostos (ex.: queda forte com sobrevenda extrema).
