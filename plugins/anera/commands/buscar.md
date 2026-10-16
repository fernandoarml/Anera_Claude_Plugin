---
description: Localiza cliente ou caso (pasta + ANERA); se só existir no ANERA, cria automaticamente a pasta e as fichas do cliente e do caso
argument-hint: <nome, CPF/CNPJ, nº do processo, sinistro, apólice ou parte contrária>
---
Localize: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

## 1. Buscar na pasta
- Procure em `01_CLIENTES/_INDICE.md` (busca parcial e sem acentos; em números, ignore pontos, traços e barras). Se não achar, busque nas fichas `CLIENTE.md` e `PROCESSO.md` de `01_CLIENTES/` e `99_ARQUIVO/clientes/`.

## 2. Buscar no ANERA
Sempre que o ANERA estiver conectado (`anera_status`):
- `anera_buscar_clientes`, `anera_buscar_processos` e `anera_buscar_atendimentos` com o termo (situação `todos`, para incluir arquivados).
- Para cada processo encontrado, `anera_obter_processo` (próximo prazo e último andamento).
- Sem conexão: siga só com a pasta e avise ("ANERA não conectado — rode /mcp e autentique o servidor anera").

## 3. Resultado
**Encontrado na pasta:** mostre cliente, área, parte contrária, nº do processo, status, **próximo prazo e último andamento (ANERA)** e o link da pasta. Se a ficha estiver sem `uuid ANERA` e o registro existir no ANERA, grave o uuid na ficha. Aponte divergências (ex.: processo do cliente que existe no ANERA mas não tem pasta → trate como no item 4, só para esse processo).

**Encontrado só no ANERA → criar a estrutura automaticamente** (é só criação local de pastas e fichas; nada é gravado no ANERA):

a) **Cliente** (se ainda não tiver pasta) — `anera_obter_cliente`:
   - pasta `01_CLIENTES/NOME COMPLETO - MM-AAAA`: nome em caixa alta como no cadastro; `MM-AAAA` = mês e ano de `data_cadastro` (se não vier, use o mês/ano atual e avise);
   - subpasta `documentos-pessoais/`;
   - `CLIENTE.md` a partir de `${CLAUDE_PLUGIN_ROOT}/templates/CLIENTE.md`, com a qualificação do ANERA e o `uuid ANERA`. Campos que não vierem ficam em branco (não invente) e são listados no final como "faltando no cadastro".

b) **Casos** — quais criar:
   - busca por **processo/caso** → só esse processo (ou atendimento);
   - busca por **cliente** → todos os processos **ativos** e atendimentos **ativos** do cliente (os arquivados só são listados).
   Para cada um, `anera_obter_processo` (ou `anera_obter_atendimento`):
   - pasta `AREA_PARTE-CONTRARIA_NUMERO` diretamente na pasta do cliente, com `contrato-procuracao/`, `documentos-caso/`, `autos/`, `pecas/` e `pesquisa/`:
     - `AREA`: sigla da tabela de áreas do `CLAUDE.md`, deduzida de natureza, caso e partes (ex.: seguradora + equipamento → `SEG-EQUIP`; condomínio cobrando → `CIVEL`). **Se não der para deduzir com segurança, pergunte a área antes de criar essa pasta**;
     - `PARTE-CONTRARIA`: nome curto padronizado (lista do `_INDICE.md`; empresa nova recorrente → acrescente à lista; pessoa física → `SOBRENOME-Nome`);
     - `NUMERO`: número CNJ; atendimento ou processo sem CNJ → `PRE-<número do atendimento ou AAAA-MM-DD>`.
   - `PROCESSO.md` a partir de `${CLAUDE_PLUGIN_ROOT}/templates/PROCESSO.md`, com o `uuid ANERA` e o que o ANERA traz: dados do processo (CNJ, juízo/comarca/vara, sistema, valor da causa, polo, partes contrárias, fase atual) e, de atendimento, o título e o relato (em "Resumo dos fatos"). **Não copie prazos nem a lista de andamentos** (ficam no ANERA); registre no Histórico: "DD/MM/AAAA — pasta criada a partir do ANERA".
   - Apague da ficha as seções que não se aplicam à área.

c) **Índice:** acrescente o cliente e cada caso em `01_CLIENTES/_INDICE.md`.

d) **Mostre o que foi criado**, com links, e o que ficou faltando (campos de qualificação, área a confirmar, documentos a colocar em `documentos-pessoais/` e `documentos-caso/`).

**Não encontrado em nenhum dos dois:** informe e ofereça `/novo-cliente`.
