---
description: Cria a pasta e a ficha de um novo processo (ou caso pré-processual) dentro de um cliente, vinculando ao ANERA
argument-hint: <cliente> <sigla da área (tabela do CLAUDE.md)> <parte contrária> <número CNJ ou PRE>
---
Crie um novo processo para: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. Localize o cliente em `01_CLIENTES/_INDICE.md` (pergunte se houver ambiguidade).
2. Padronize o nome da parte contrária conforme a lista em `01_CLIENTES/_INDICE.md`; se for recorrente e nova, acrescente-a lá.
3. Crie, **diretamente na pasta do cliente**, `AREA_PARTE-CONTRARIA_NUMERO/` (ou `..._PRE-identificador` se ainda não ajuizado), com subpastas `contrato-procuracao/` (contrato de honorários, procuração e declarações deste caso), `documentos-caso/` (apólice, negativa, contratos, comunicações, documentos do benefício etc.), `autos/`, `pecas/` e `pesquisa/`.
4. Copie `${CLAUDE_PLUGIN_ROOT}/templates/PROCESSO.md`, preencha o que for conhecido, apague as seções que não se aplicam à área e adicione o processo à tabela de `CLIENTE.md` e de `01_CLIENTES/_INDICE.md`.
5. Se houver documentos fornecidos, leia-os e preencha os dados do caso, o resumo dos fatos e os pedidos.
6. **ANERA:**
   - procure o processo (`anera_buscar_processos` por CNJ ou nome do caso) ou o atendimento (`anera_buscar_atendimentos`, para caso ainda não ajuizado);
   - se **já existir**, grave o `uuid ANERA` na ficha;
   - caso **ainda não ajuizado** e sem atendimento no ANERA → ofereça `anera_cadastrar_atendimento` (título = assunto do caso; descrição = resumo dos fatos) e grave o uuid do atendimento na ficha;
   - processo ajuizado que **não existir** → ofereça cadastrar: use `anera_opcoes_processo` para os valores aceitos, mostre o resumo e, após o "sim", `anera_cadastrar_processo` (sem `numerocnj` se ainda não ajuizado); grave o uuid na ficha.
7. Consulte `02_ESTRATEGICO/_INDICE.md` e sugira teses da mesma área que se apliquem (em seguros, as que combatam o motivo da negativa, inclusive as de `comum/`).
