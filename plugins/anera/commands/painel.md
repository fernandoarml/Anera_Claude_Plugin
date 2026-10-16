---
description: Painel do dia (ANERA) — prazos atrasados, de hoje e dos próximos dias, audiências e processos com andamentos novos, com o link da pasta de cada caso
argument-hint: [dias, padrão 7] [meus]
---
Monte o painel: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. `anera_status` (se não estiver conectado: "ANERA não conectado — rode /mcp e autentique o servidor anera" e encerre).
2. `anera_painel` com `dias` (padrão 7) e `apenas_meus` se o argumento "meus" for passado.
3. Apresente em blocos, nesta ordem:
   - **⚠️ Atrasados**;
   - **Hoje**;
   - **Próximos dias** (agrupados por data, com dia da semana);
   - **Andamentos não lidos** (processo e resumo do último andamento).
   Para cada item: tipo (prazo, audiência, reunião), título, processo/cliente e o **link da pasta do caso** (localize pelo `uuid ANERA` nas fichas ou pelo índice). Se o caso não tiver pasta, indique "sem pasta".
4. **Avisos:**
   - **Publicações não lidas** (`publicacoes_nao_lidas`): informe a quantidade e sugira `/novidades`.
   - **Criados pela IA aguardando validação** (`criado_pela_ia_aguardando_revisao`): liste e lembre: "valide no ANERA (botão Validar)".
5. Ao final, sugira em até 3 linhas as prioridades do dia. Não crie, conclua nem altere nada sem pedido.
