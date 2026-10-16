<!-- anera:claude-md v2 — as regras gerais vêm do plugin (regras/REGRAS-BASE.md) e são atualizadas com ele; este arquivo guarda só o que é do escritório e nunca é alterado por atualizações do plugin. -->
# {{ESCRITORIO_NOME}} — {{ADVOGADO_NOME}} (OAB/{{ADVOGADO_OAB_UF}} {{ADVOGADO_OAB_NUMERO}})

Base de trabalho do escritório, organizada pelo plugin ANERA. As **regras gerais** (estrutura, memória do caso, ANERA, sigilo, links) vêm do plugin em toda sessão. Este arquivo guarda **o que é do escritório** e **prevalece** sobre o padrão do plugin. Exceções: sigilo, confirmação antes de gravar no ANERA e não inventar jurisprudência.

- **Dados do escritório:** `.claude/escritorio.json`.
- **Dúvidas:** `/anera:ajuda`.
- **Preferências:** `/anera:preferencias`.

## Áreas de atuação

| Área | Sigla nos nomes de processo | Pasta (`<area>`) |
|---|---|---|
{{TABELA_AREAS}}

## Padrões do escritório
- **Peças:** conforme `03_MODELOS/_base/PADRAO-FORMATACAO.md`.
- **Contratos e procurações:** conforme os modelos instalados em `03_MODELOS/` (ver os `LEIA-ME.md`).
- _Acrescente aqui padrões próprios: tom das peças, estrutura preferida, partes contrárias recorrentes etc._

## Preferências do escritório
Ajustes pedidos pelo escritório durante o uso. Valem sobre o padrão do plugin e dos comandos. Registre um item por linha, com a data. O Claude registra aqui quando você diz "a partir de agora…", sempre pedindo confirmação.

### Geral
_(nenhuma ainda — ex.: "2026-11-03: sempre tratar o cliente por Sr./Sra. nas peças")_

### /anera:documentos-cliente
_(nenhuma ainda)_

### /anera:peca
_(nenhuma ainda)_

### /anera:preparar-documentos
_(nenhuma ainda)_

### /anera:novidades e /anera:painel
_(nenhuma ainda)_
