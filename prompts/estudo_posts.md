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
5. Para cada post novo de análise (começa com 343, 686, "686 e 343", Log, Diário, Semanal, DOIS DIAS, ou tem gráfico):
   a. Placar: compare com o nosso Log do mesmo fechamento (logs/ e calibracao/placar.md) e escreva no JSON UMA linha de placar no formato das anteriores (igual / divergente / o que aprender). Não crie regra nova; 2ª ocorrência de algo = escreva "proposta ao Augustus" na linha.
   b. Linhas: abra a imagem original (https://pbs.twimg.com/media/<arquivo>?format=jpg&name=orig) e meça as linhas desenhadas por ele com o método de calibracao/linhas_prints (tools/linhas_print.py, tools/salva_print.py: escala de preço lida por pixel nos rótulos do eixo, datas lidas no eixo de baixo, reta ajustada por cor). Só use a medição se a máxima/mínima marcada no print bater com os dados com erro <= 0,15%.
      - Linha que já existe em calibracao/linhas_ativas.json (mesma cor/nome e valor a até 0,5%): registre no JSON como "atualizar" (p1/p2 novos e visto_em).
      - Linha nova: registre como "nova" (nome pela cor/rótulo dele, autor, tf, p1, p2, visto_em, fonte, papel).
      - NUNCA remova linhas (regra de remoção ainda em discussão com o Augustus).
      - Médias móveis (MA/EMA rotuladas) não são linhas desenhadas: ignore.
      - Se a medição não for confiável, anote em "pendencias" (data, post, motivo) e siga.
6. Salve o JSON pelo GitHub no Chrome (ver "Atenção" acima) — só se houver post novo. Feche as abas que você abriu.
7. Se houve post novo de análise, mande ao Augustus com SendUserMessage um resumo de no máximo 4 linhas em português: quantos posts, se a posição dele bateu com a nossa, linhas atualizadas/novas. Sem post novo: não mande mensagem.
