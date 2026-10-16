---
description: Redige o rascunho de uma peça para um processo
argument-hint: <tipo de peça> <processo ou cliente> [instruções]
---
Redija o rascunho da peça: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. Localize o caso em `01_CLIENTES/_INDICE.md`. Leia `CLIENTE.md`, `PROCESSO.md`, os documentos do caso, os autos relevantes e as `TESE.md` vinculadas.
2. **ANERA** (se conectado e a ficha tiver `uuid ANERA`): use `anera_obter_processo`, `anera_listar_andamentos` (com `texto_completo` para decisões, sentenças e intimações relevantes) e `anera_listar_anotacoes` para trazer o que aconteceu no processo desde a última atualização da ficha. Se a peça responde a uma intimação, identifique o prazo correspondente em `anera_listar_prazos`.
3. Use como padrão de estilo e estrutura o modelo correspondente em `03_MODELOS/pecas/<area>/`. Se não houver, avise e use a estrutura de `03_MODELOS/_base/padrao-formatacao-pecas.docx`.
4. Use `04_PESQUISA/` e as teses da mesma área como fonte de argumentos. Nunca invente julgados ou dispositivos; marque `[VERIFICAR]` quando não puder confirmar.
5. Gere o `.docx` a partir de `03_MODELOS/_base/timbrado.docx`, seguindo `03_MODELOS/_base/PADRAO-FORMATACAO.md`. Salve em `pecas/AAAA-MM-DD_tipo_vN.docx`, sem sobrescrever versões anteriores.
6. Atualize "Peças produzidas" e, se for o caso, "Teses aplicadas" em `PROCESSO.md` e "Aplicações" na `TESE.md`.
7. Ao final, liste pontos que exigem revisão do advogado.
