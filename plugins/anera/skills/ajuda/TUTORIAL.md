# Tutorial — primeiros dias com o plugin ANERA

Lições curtas. Cada uma termina com algo feito de verdade no escritório.

## Lição 1 — Configurar o escritório (10 min)
`/anera:configurar-escritorio`
O Claude cria as pastas, pergunta os dados do advogado e do escritório, recebe o **timbrado** e uma **petição sua** para aprender a formatação, e — com o ANERA conectado — baixa e instala contratos e procurações já com seus dados.
**Resultado:** pasta organizada, `CLAUDE.md` com as regras do escritório e modelos prontos em `03_MODELOS/`.

## Lição 2 — Conectar o ANERA (2 min)
Digite `/mcp`, escolha **anera** e clique em autenticar. Faça login no ANERA e marque as permissões.
**Por que vale a pena:** o Claude passa a enxergar seus prazos, intimações e andamentos, preenche documentos com o cadastro do cliente e registra anotações e prazos no ANERA — sempre com sua confirmação.
**Teste:** `/anera:painel`.

## Lição 3 — Trazer um cliente para a pasta (1 min)
`/anera:buscar <nome do cliente>`
Se o cliente estiver no ANERA e ainda não tiver pasta, o Claude **cria a pasta do cliente e de cada caso ativo**, com as fichas preenchidas.
Sem ANERA: `/anera:novo-cliente <nome>` — arraste o RG/CNH para o chat e o Claude extrai a qualificação.

## Lição 4 — Gerar contrato e procuração (3 min)
`/anera:documentos-cliente <cliente> <caso>`
Escolha o modelo (entrada + êxito, só êxito ou valor fixo), informe os valores e receba Word + PDF na pasta do caso. Com o ANERA, a qualificação vem do cadastro e os honorários são gravados no sistema.

## Lição 5 — Redigir uma peça
`/anera:peca <tipo> <cliente> <caso>`
O Claude lê a ficha, os documentos, os andamentos (ANERA) e as teses, e redige no **seu padrão de formatação**. Citações não confirmadas vêm marcadas `[VERIFICAR]`.

## Lição 6 — Preparar o protocolo
`/anera:preparar-documentos <cliente> <caso>`
Peça + procuração + documentos pessoais + `doc_1`, `doc_2`... em PDF, na ordem certa, com um índice. Depois do protocolo, o Claude oferece registrar no ANERA e concluir o prazo.

## Lição 7 — Rotina diária com o ANERA
- **Manhã:** `/anera:painel` — atrasados, hoje, semana, intimações não lidas.
- **Intimações:** `/anera:novidades` — o Claude explica cada publicação, calcula o prazo com a calculadora do ANERA (feriados e recesso) e cria o prazo vinculado, com sua confirmação.
- **Valide** no ANERA o que a IA criou (etiqueta **IA** → botão **Validar**).

## Lição 8 — Memória do caso
Antes de fechar uma sessão: `/anera:registrar`. O que foi feito e decidido vai para a ficha do caso (e, se você aprovar, para as anotações do ANERA). Na próxima sessão, "abra o caso X" retoma de onde parou.

## Lição 9 — Ensinar seu estilo ao Claude
Mande peças que você já aprovou: `/anera:configurar-escritorio modelos`. Elas são anonimizadas e guardadas por área; daí em diante, as peças saem no estilo do escritório.

## Lição 10 — Deixar o Claude do seu jeito
Sempre que algo puder ser diferente, diga **"a partir de agora…"**. Exemplos:
- "a partir de agora, no contrato, gere também a declaração";
- "no painel, mostre 15 dias".

Para ver tudo o que já foi ajustado: `/anera:preferencias`. As preferências ficam no `CLAUDE.md` do escritório e **não se perdem** quando o plugin atualiza. Teve uma ideia boa para todos? `/anera:preferencias sugerir …`.
