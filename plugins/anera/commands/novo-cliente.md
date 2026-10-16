---
description: Cria a pasta e a ficha de um novo cliente (e o cadastro no ANERA, se necessário)
argument-hint: <nome do cliente> [PF|PJ]
---
Crie um novo cliente em `01_CLIENTES/` para: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. **Verificar se já existe:** consulte `01_CLIENTES/_INDICE.md` (inclusive arquivados) e, com o ANERA conectado, `anera_buscar_clientes` por nome e por CPF/CNPJ.
2. **Pasta:** crie `NOME COMPLETO - MM-AAAA` (nome completo em caixa alta, como no documento de identidade, com acentos; mês e ano de entrada), com a subpasta `documentos-pessoais/` (contrato e procuração ficam na pasta de cada caso). Se o cliente enviar fotos/PDF de documentos, salve-os em `documentos-pessoais/` e extraia deles a qualificação (pedindo conferência ao advogado).
3. **Ficha:** copie `${CLAUDE_PLUGIN_ROOT}/templates/CLIENTE.md` e preencha. Se o cliente já existir no ANERA, use `anera_obter_cliente` como fonte da qualificação (campos ausentes → pergunte ou extraia dos documentos; não invente).
4. **ANERA:**
   - cliente **não cadastrado** → mostre os dados e, após o "sim", `anera_cadastrar_cliente`;
   - cliente cadastrado com dados faltando/desatualizados que estão nos documentos → **ofereça** `anera_atualizar_cliente`;
   - grave o `uuid ANERA` na ficha.
5. Acrescente o cliente em `01_CLIENTES/_INDICE.md`.
6. Pergunte os dados de qualificação que ainda faltarem.
