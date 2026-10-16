---
name: ajuda
description: Tutorial e central de dúvidas do plugin ANERA para escritórios de advocacia. Use quando o usuário pedir ajuda, tutorial, "como faço para...", "o que o plugin faz", primeiros passos, quais comandos existem, como conectar o ANERA, como personalizar modelos, ou parecer perdido no uso do plugin.
argument-hint: "[dúvida] — ou sem nada para o tutorial"
---
# Ajuda do plugin ANERA

Material de apoio (leia o que for necessário para responder):
- `${CLAUDE_PLUGIN_ROOT}/skills/ajuda/TUTORIAL.md` — roteiro do tutorial dos primeiros dias;
- `${CLAUDE_PLUGIN_ROOT}/skills/ajuda/FAQ.md` — perguntas frequentes;
- `${CLAUDE_PLUGIN_ROOT}/docs/COMO-USAR.md` — manual completo;
- `${CLAUDE_PLUGIN_ROOT}/docs/CONECTOR-MCP-ANERA.md` — detalhes técnicos do conector (só se a dúvida for técnica);
- `${CLAUDE_PLUGIN_ROOT}/TERMOS-DE-USO.md` — termos de uso (licença, uso dos modelos, privacidade).

## Sem pergunta (`$ARGUMENTS` vazio): tutorial personalizado
1. Faça um diagnóstico rápido, sem expor dados de clientes:
   - existe `.claude/escritorio.json`? (escritório configurado)
   - existe `03_MODELOS/_base/timbrado.docx`? há modelos em `03_MODELOS/contratos/` e peças próprias em `03_MODELOS/pecas/`?
   - quantos clientes há em `01_CLIENTES/_INDICE.md`?
   - o ANERA responde (`anera_status`)? Se sim e houver `03_MODELOS/_versao-modelos.json`, compare com `anera_listar_modelos`: versão maior no ANERA → próximo passo é atualizar os modelos (`/anera:configurar-escritorio modelos`).
2. Mostre **"Seu progresso"** como checklist (✅/⬜): configurar escritório · conectar ANERA · timbrado · modelos próprios · primeiro cliente · primeiro contrato gerado · primeira peça · `/anera:registrar` usado · primeira preferência registrada.
3. Indique **o próximo passo** (um só) com o comando exato, e ofereça o tour pelo tutorial (`TUTORIAL.md`), em lições curtas: o usuário escolhe a lição ou segue em ordem.
4. Termine com: "Pode me perguntar qualquer coisa — por exemplo: `/anera:ajuda como gerar um contrato?`".

## Com pergunta: responda a dúvida
- Responda de forma **curta e prática**: o que fazer, o comando exato e um exemplo. Use o FAQ e o manual; não invente funcionalidades que o plugin não tem.
- Se a resposta envolver uma ação, ofereça fazê-la agora.
- Se a dúvida for sobre algo que **depende do ANERA** (prazos, intimações, andamentos, cadastro, anotações, honorários) e ele não estiver conectado, explique o ganho concreto e como conectar (`/mcp` → anera → autenticar).

## Sempre
- **Estimule o uso com o ANERA**: quando fizer sentido, mostre o que a mesma tarefa ganha com o ANERA conectado (ex.: "com o ANERA, o `/anera:painel` mostra seus prazos da semana e as intimações não lidas"). Sem exagero: uma frase objetiva.
- Lembre, quando pertinente, das garantias: o Claude **pede confirmação antes de gravar** no ANERA, **nada é excluído**, tudo fica **auditado** e o que a IA cria recebe a etiqueta **IA** para validação.
- Os comandos do plugin aparecem com o prefixo `anera:` (ex.: `/anera:buscar`); ao digitar `/` o Claude Code mostra a lista.
