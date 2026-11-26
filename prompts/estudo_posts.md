# Estudo automático dos posts do Dollynho e do Raicher (tarefa agendada, 4x por dia)
Objetivo: ler os posts novos deles no X pelo Chrome do Augustus, guardar no repositório e usar como estudo (placar e linhas). NÃO mude regras do método (prompts/modo_dollynho.md, seção PRINCÍPIO): só registre e proponha.

## Atenção: esta tarefa roda no computador do Augustus (exige o Chrome dele)
Por isso ela NÃO tem acesso de escrita ao repositório (add_repo pode falhar; o clone público funciona só para leitura).
Não tente git push. Para salvar, use o próprio Chrome do Augustus, que está logado no GitHub como augustusramos:
- monte UM arquivo JSON com tudo desta execução: {"gerado_em": "...", "posts": {"dollynho": [[id, ts_ms, texto, [imagens]], ...], "raicher": [...]}, "ultimo_lido": {...}, "placar": ["linha da tabela do placar", ...], "linhas": [{"acao": "atualizar"|"nova", "nome": ..., "tf": ..., "p1": [...], "p2": [...], "visto_em": ..., "fonte": ..., "papel": ...}], "pendencias": [...]};
- abra https://github.com/augustusramos/btc-raicher-logs/new/main?filename=calibracao/historico/novos/<AAAA-MM-DD_HHMM>.json ;
- coloque o conteúdo no editor (javascript_tool: copie com navigator.clipboard.writeText disparado por um clique na página e cole com ctrl+v no editor) e faça "Commit changes" direto na main.
Os Logs automáticos (que têm acesso ao repositório) juntam esses arquivos ao histórico, ao placar e às linhas no fechamento seguinte.

## Passos
1. Leia calibracao/historico/ultimo_lido.json (id e timestamp ms do último post lido de cada um).
2. Carregue as ferramentas do Claude in Chrome (ToolSearch, um único select) e a skill chrome-browser. Chame tabs_context_mcp com createIfEmpty e abra UMA aba nova.
   - Se o Chrome/extensão não responder (computador desligado ou Chrome fechado): termine sem mensagem e sem commit. A próxima execução pega o atraso, porque a busca é por data.
3. Para cada perfil (DollynhoCoin e raicher): navegue para
   https://x.com/search?q=from%3A<perfil>%20since%3A<data do ultimo_lido em AAAA-MM-DD>&src=typed_query&f=live
   e colete os posts com javascript_tool (rolagem curta, até ~15 rolagens; o eval do X é bloqueado por CSP, então escreva a função inline):
   - id do post pelo link /<perfil>/status/<id>; timestamp = (BigInt(id)>>22n)+1288834974657n (ms UTC);
   - texto = innerText do article (sem contadores); imagens = arquivos de pbs.twimg.com/media/<arquivo> (+ extensão do format=).
   Guarde só os posts com id MAIOR que o ultimo_id. Se aparecer "Algo deu errado" (limite do X), espere 60 s e tente uma vez.
4. Junte os posts novos (id maior que o ultimo_lido, considerando também os arquivos já existentes em calibracao/historico/novos/) e o novo ultimo_lido no JSON desta execução.
5. Antes, meça também as imagens PENDENTES de calibracao/linhas_pendentes.md (as que ainda não foram medidas), do jeito do item 5b; ao medir, escreva no JSON em "resolvidas" quais pendências foram resolvidas.
   Para cada post novo de análise (começa com 343, 686, "686 e 343", Log, Diário, Semanal, DOIS DIAS, ou tem gráfico):
   a. Placar: compare com o nosso Log do mesmo fechamento (logs/ e calibracao/placar.md) e escreva no JSON UMA linha de placar no formato das anteriores (igual / divergente / o que aprender). Não crie regra nova; 2ª ocorrência de algo = escreva "proposta ao Augustus" na linha.
   b. Linhas: a imagem NÃO chega ao ambiente da tarefa (pbs.twimg.com é bloqueado lá). Meça DENTRO do Chrome:
      - abra https://pbs.twimg.com/media/<arquivo>?format=jpg&name=orig numa aba;
      - cole o conteúdo de tools/medir_no_navegador.js num javascript_exec (cria window.L com fit, bands, eixoX);
      - veja a imagem com zoom (computer zoom em faixas: redimensione o <img> para 445 px de largura e role com style.top) para ler os rótulos de preço e datas e as cores das linhas;
      - leia por pixel: L.bands(...) nos rótulos do eixo de preço (pares [y_px, preço]), L.eixoX() nas datas (pares [x_px, data]) e L.fit(ponto_a, ponto_b, cor) em cada linha desenhada (m, c, res em px);
      - devolva esses números ao ambiente e converta com tools/linhas_print.py (spec com "y", "x", "checks" e "linhas"), igual a calibracao/linhas_prints/*.medidas.json. Só use a medição se a máxima/mínima marcada no print bater com os dados com erro <= 0,15%.
      - Linha que já existe em calibracao/linhas_ativas.json (mesma cor/nome e valor a até 0,5%): registre no JSON como "atualizar" (p1/p2 novos e visto_em).
      - Linha nova: registre como "nova" (nome pela cor/rótulo dele, autor, tf, p1, p2, visto_em, fonte, papel).
      - NUNCA remova linhas (regra de remoção ainda em discussão com o Augustus).
      - Médias móveis (MA/EMA rotuladas) não são linhas desenhadas: ignore.
      - Se a medição não for confiável, anote em "pendencias" (data, post, motivo) e siga.
6. Salve o JSON pelo GitHub no Chrome (ver "Atenção" acima) se houver post novo OU qualquer linha medida (inclusive das pendentes) OU pendência nova. Só termine sem salvar se não houve nada disso. Feche as abas que você abriu.
7. Se houve post novo de análise ou linhas medidas, mande ao Augustus com SendUserMessage um resumo de no máximo 4 linhas em português: quantos posts, se a posição dele bateu com a nossa, linhas atualizadas/novas. Sem post novo: não mande mensagem.
