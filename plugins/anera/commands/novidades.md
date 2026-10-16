---
description: Intimações/publicações e andamentos novos (ANERA), com a providência sugerida, criação de prazo vinculado e baixa da publicação — tudo com confirmação
argument-hint: [desde AAAA-MM-DD — sem data, traz os não lidos]
---
Verifique as novidades: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. `anera_status` (se não estiver conectado, avise e encerre). Verifique as permissões: sem `prazos:escrita` ou `publicacoes:escrita`, faça só a análise e oriente a reconectar com a permissão.

2. **Publicações/intimações** (primeiro, porque geram prazo):
   - `anera_listar_publicacoes` (não lidas; com `desde`, filtre por `de`). Consultar **não** marca como lida.
   - Para cada uma: `anera_obter_publicacao` (texto completo) e a ficha `PROCESSO.md` do caso (pelo `uuid ANERA` ou pelo índice).
   - Se vier `processo_sugerido` e a publicação não estiver vinculada → proponha `anera_vincular_publicacao`.
   - Explique **o que foi publicado** em linguagem simples e **a providência** (ex.: "contrarrazões em 10 dias", "ciência, sem providência").
   - **Prazo:** `anera_calcular_prazo` (data de início = data da intimação; regra e UF aplicáveis — nunca conte de cabeça; mostre a regra e os dias não contados). Confira em `anera_listar_prazos` se já existe. Se não existir, mostre título, data, tipo e responsável e, após o "sim", `anera_criar_prazo` **com `publicacao_uuid`**.
   - Depois de tratada: `anera_marcar_publicacao_lida`; se não houver providência, proponha `anera_arquivar_publicacao`.

3. **Andamentos** (`anera_novidades`, com `desde` se informado; não marca como lido): para cada processo, traga o texto completo dos relevantes (`anera_listar_andamentos` com `texto_completo`), explique e sugira a providência. Se gerar prazo que não tenha vindo por publicação, siga o mesmo cálculo e confirmação.

4. Ofereça registrar na ficha de cada caso o que for relevante (regra 8 do `CLAUDE.md` do escritório).

5. **Resumo final:** publicações tratadas, prazos criados (lembrando que nascem com a etiqueta **IA** e precisam ser **validados no ANERA**) e itens que pedem atenção do advogado.
