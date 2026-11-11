# Modo completo (salvo em 11/11/2026) — prompt das 5 tarefas agendadas
Para voltar a este modo: pedir ao Claude "voltar para o modo completo dos Logs"; ele recoloca este texto nas 5 tarefas.

---
Escreva e envie AGORA o Log de BTC do Augustus no método Raicher/Dollynho, em português, para o fechamento que acabou de acontecer. Rapidez importa. O objetivo é soar e raciocinar como o @DollynhoCoin: mesmas leituras, mesmo jeito de dar alvos (🎯), stop e invalidação, e continuidade do trade de um Log para o outro.

1. Acesso: chame add_repo com owner "augustusramos", repo "btc-raicher-logs", access "push".
2. Dispare o cálculo:
   gh api -X POST repos/augustusramos/btc-raicher-logs/actions/workflows/indicadores.yml/dispatches -f ref=main -f 'inputs[charts]=all'
   Espere ~10 s e acompanhe até "completed" (máx. 12 min):
   gh api repos/augustusramos/btc-raicher-logs/actions/runs --jq '.workflow_runs[0] | .status+" "+(.conclusion//"")'
   Se falhar, siga com os dados existentes e avise no topo.
3. Baixe dados e histórico (repo público):
   git clone --depth 1 --branch dados https://github.com/augustusramos/btc-raicher-logs dados
   git clone --depth 1 https://github.com/augustusramos/btc-raicher-logs repo
   Leia repo/logs/estado.json (trade em andamento por timeframe), repo/calibracao/dollynho/cronologia_trades.md (como ele entra, sai e mexe no stop, regras aprendidas), os 3 Logs mais recentes em repo/logs/ e os 2 posts mais recentes em repo/calibracao/dollynho/.
4. Carregue a skill analise-btc-raicher (Skill tool) e siga o método, níveis fixos e formato dela, especialmente a seção "Estilo Dollynho".
5. Timeframes que ACABARAM de fechar: em dados/latest.json, todo timeframe com "bar_close" nos últimos 20 minutos (não use "new_closes"). Brasília: 343 fecha 02:43, 08:26, 14:09, 19:52, 21:00; 686 fecha 08:26, 19:52, 21:00; Diário 21:00; Semanal domingo 21:00. Se o esperado não fechou ainda, espere 1 min e refaça os passos 2-3 uma vez; se faltar, avise que atrasou.
6. Para cada timeframe fechado, leia dados/<tf>.json e veja dados/charts/<tf>.png. Use: eventos CONFIRMOU/ANULOU/ROMPEU/PERDEU, "wick_touches" (= "toque perfeito na MAx"), "ma_crosses" (MA7 cruzando médias longas), "ladder_below"/"ladder_above" (escada de médias), níveis fixos do RSI (inclui 72.86 e 23.67) e Stoch (20/50/80).
7. CONTINUIDADE DO TRADE (estado.json + cronologia_trades.md):
   - Trade aberto: mantenha os alvos (🎯) e diga se o fechamento confirma a tese. Stop = a média que é a resistência principal (short) ou o suporte principal (long), decidido candle a candle como ele faz; com o trade no lucro o stop nunca volta ao prejuízo. Num short, recuperar a MA7/EMA7 com RSI ainda ABAIXO do Suporte Inferior (~43.6) NÃO fecha o trade: o stop passa para a MA21/EMA21.
   - Alvo tocado: "QED, alvo atingido"; se os prazos maiores seguem a favor, parcial e mantém o restante com stop ajustado; liquidar tudo só no último alvo ou se o prazo maior virou contra.
   - Fechamento além do stop: "Fechamos o trade"; depois "Seguimos, fora", dizendo onde seria o novo ponto de entrada.
   - Não inverta a mão dentro do stop. Sem trade: entrada só no padrão dele (short = rejeição da MA7/EMA7 + RSI rejeitando o Suporte Inferior + Stoch virando para baixo; long = recupera MA7/EMA7 + RSI ACIMA do Suporte Inferior + Stoch acima de 20 e fora do teto). Stoch na máxima/zerado = cautela.
8. Escreva o Log no estilo do Dollynho (curto, linhas terminadas em ";", MAIÚSCULAS em ACIMA/ABAIXO, "Seguimos:" seguido da lista 🎯 de alvos, e o stop). 343 e 686: 4 a 8 linhas. Diário: Log completo numerado pela quantidade de arquivos em dados/history/. Semanal/2D/3D quando fecharem: seção própria. Nunca invente número fora do JSON. Horários em Brasília.
9. Depois do Log, um bloco "Em português claro:" (3 a 6 linhas, sem jargão, explicando termos como MA, RSI, Stoch quando aparecerem) dizendo: o que aconteceu neste fechamento; pelo método, a tese agora e por quê; pelo método, o que faria a entrada acontecer (condição de fechamento com preço), onde o método realiza (alvos com preço) e onde admite que errou (stop/invalidação com preço); o que vigiar no próximo fechamento e em que horário.
9b. Ao FINAL de tudo (depois do bloco "Em português claro", sem remover nem resumir nenhuma análise acima), um bloco "Leitura consolidada (um trade só):" com 4 a 6 linhas:
   - Direção (prazo maior): o que o Diário e o 686 dizem juntos (alta, queda ou indefinido) e o que sustenta isso;
   - Gatilho (343): o que o 343 está dizendo agora (a favor, alerta contra ou virou contra);
   - Posição única pelo método: manter / realizar parcial / apertar stop / fechar / ficar de fora / entrar, seguindo: 343+686+Diário a favor = manter ou entrar; 343 contra com 686 e Diário a favor = alerta, parcial ou stop mais curto, tese mantida; 686 também contra = tese de médio prazo enfraqueceu, sair; Diário contra = mudança de tendência, lado oposto só com confirmação;
   - Stop e alvo dessa posição única, com preço, e de qual timeframe vêm;
   - O que mudaria essa leitura no próximo fechamento (horário em Brasília).
   Escreva sempre como "pelo método…", nunca como ordem ("compre/venda agora"); não fale de tamanho de posição nem de alavancagem. Termine com: estudo, não recomendação; trap pode liquidar posição alavancada.
10. Grave no repositório (main): salve o Log + blocos em repo/logs/AAAA-MM-DD_HHMM_<tf>.md e atualize repo/logs/estado.json (postura, alvos, stop, atualizado), depois:
    cd repo && git add logs && git -c user.name="Augustus Cesar" -c user.email="226001994+augustusramos@users.noreply.github.com" commit -m "Log <tf> <data hora>" && git push origin HEAD:main
    (se o push for rejeitado: git pull --rebase origin main e tente uma vez de novo)
11. Entregue com SendUserMessage (o Log + "Em português claro" + "Leitura consolidada") e SendUserFile com os gráficos dos timeframes que fecharam.
