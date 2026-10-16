---
description: Cria uma nova tese em 02_ESTRATEGICO
argument-hint: <área> <nome da tese>
---
Crie uma nova tese: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. Crie `02_ESTRATEGICO/<area>/<nome-da-tese-em-kebab-case>/` com subpasta `anexos/`. Use a pasta da área conforme a tabela de áreas do `CLAUDE.md` (ou `areas` em `.claude/escritorio.json`); se a área não existir, pergunte se deve ser criada.
2. Copie `${CLAUDE_PLUGIN_ROOT}/templates/TESE.md` e preencha com o que foi informado. Status inicial: "Em teste", salvo indicação contrária.
3. Procure em `04_PESQUISA/` material relacionado e referencie na ficha.
4. Adicione a linha em `02_ESTRATEGICO/_INDICE.md`.
5. Nunca invente jurisprudência; o que não for verificável marque como `[VERIFICAR]`.
