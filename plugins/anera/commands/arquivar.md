---
description: Encerra processo ou move cliente encerrado para 99_ARQUIVO
argument-hint: <cliente ou processo>
---
Arquive: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. Confirme com o advogado antes de mover qualquer pasta.
2. Processo encerrado: registre o resultado final em `PROCESSO.md` e nas `TESE.md` vinculadas (seção "Aplicações") e marque o status como "Encerrado" no índice.
3. Cliente sem processos ativos: mova a pasta inteira para `99_ARQUIVO/clientes/`, mantendo a estrutura.
4. Atualize o caminho e o status em `01_CLIENTES/_INDICE.md` e os links em `02_ESTRATEGICO/` que apontarem para o caminho antigo.
5. **ANERA:** caso pré-processual (atendimento) → com confirmação, `anera_arquivar_atendimento` com motivo e resultado (`contratacao`, `processo` + CNJ, `nenhum`, `outro`). **Processo judicial:** o conector ainda não arquiva processos. Com confirmação, registre `anera_criar_anotacao` (`[Histórico] Processo encerrado — resultado: …`) e lembre o advogado de **arquivar o processo no próprio ANERA**. Verifique com `anera_listar_prazos` se restaram prazos pendentes do processo e avise.
