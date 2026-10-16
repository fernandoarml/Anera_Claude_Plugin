# Changelog — plugin anera

## 0.3.1 — prévia (16/10/2026)
- Referência do conector atualizada para o servidor 1.6.0: anera_listar_modelos e anera_link_modelos disponíveis (modelos liberados para escritórios com conta ativa).

## 0.3.0 — prévia (16/10/2026)
- Distribuição pelo GitHub: /plugin marketplace add https://github.com/fernandoarml/Anera_Claude_Plugin.git (o Claude Code não aceita catálogo hospedado fora de um repositório git nesta configuração).
- Aviso de versão nova passa a consultar o versao.json do repositório.

## 0.2.1 — prévia (16/10/2026)
- Endereço de download definitivo: https://app.anera.com.br/backend/download/plugins/claude/ (arquivo novo para não esbarrar em cache do servidor).

## 0.2.0 — prévia (16/10/2026)
- Modelos de contrato, procuração e declaração passam a vir pelo conector do ANERA (anera_link_modelos), conferidos por sha256, em vez de acompanhar o plugin.
- Aviso de versão nova ao abrir a sessão, com o comando de atualização.
- Distribuição por link: https://app.anera.com.br/backend/download/plugins/claude/marketplace.json.
- Termos de uso do plugin (TERMOS-DE-USO.md).
- Camadas separadas: regras gerais no plugin (regras/REGRAS-BASE.md, injetadas em toda sessão, inclusive após /clear e compactação); o CLAUDE.md do escritório fica enxuto, com áreas, padrões e Preferências do escritório, e nunca é alterado por atualizações.
- Novo /anera:preferencias: ajustes do escritório que valem sobre o padrão dos comandos e sugestões de melhoria (06_PROCEDIMENTOS/SUGESTOES-PLUGIN.md).
- Modelos alterados pelo escritório são preservados nas atualizações (a versão nova vem ao lado para comparar).
- /anera:configurar-escritorio migrar: converte CLAUDE.md de formato anterior.
- Comandos sem áreas fixas: usam as áreas configuradas pelo escritório.

## 0.1.0 — prévia (15/10/2026)
- Estrutura de escritório: pastas, fichas `CLIENTE.md`/`PROCESSO.md`/`TESE.md`, índices e `CLAUDE.md`-modelo.
- Skills: `/anera:configurar-escritorio` (configuração guiada, com recebimento de timbrado, peça de formatação e modelos próprios) e `/anera:ajuda` (tutorial, progresso e dúvidas).
- Hook de boas-vindas (`SessionStart`): detecta pasta não configurada e orienta a configuração.
- Comandos: `buscar` (cria pasta a partir do ANERA), `novo-cliente`, `novo-processo`, `documentos-cliente`, `peca`, `preparar-documentos`, `registrar`, `arquivar`, `nova-tese`, `painel`, `novidades`.
- Modelos de referência com campos do escritório: 5 contratos de honorários (autor/defesa), 4 procurações, declaração de hipossuficiência; instalador `scripts/instalar_modelos.py` (aplica timbrado, dados e cor do escritório).
- Conector MCP remoto do ANERA (`.mcp.json`, OAuth) — servidor v1.5.0.
