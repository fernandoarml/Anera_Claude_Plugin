---
description: Gera contrato de honorários, procuração e declaração de hipossuficiência preenchidos para um caso
argument-hint: <cliente> [caso] [contrato | procuracao | declaracao]
---
Gere os documentos de contratação para: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. **Localizar.** Encontre o cliente e o caso em `01_CLIENTES/_INDICE.md` e leia `CLIENTE.md` e `PROCESSO.md`. Se o cliente tiver mais de um caso e o caso não foi indicado, pergunte qual.
2. **Quais documentos.** Se não foram indicados, gere contrato + procuração e pergunte se precisa da declaração de hipossuficiência (gratuidade).
3. **Escolher os modelos** (ver `03_MODELOS/contratos/LEIA-ME.md` e `03_MODELOS/procuracoes/LEIA-ME.md`):
   - Contrato — pergunte a forma de cobrança combinada:
     - cliente **autor**: A (entrada + êxito), B (só êxito) ou C (valor fixo);
     - cliente **réu**: D (entrada + êxito) ou E (valor fixo).
   - Procuração — pela área e polo do caso: SEG-* → **D (seguros)**; PREV → **B (INSS)**; cliente réu → **C (defesa, com nº do processo)**; demais → **A (novas ações)**.
   - Declaração: modelo único (`declaracao-hipossuficiencia.docx`).
4. **Reunir os dados.**
   - Qualificação: da ficha `CLIENTE.md` e, com o ANERA conectado, de `anera_obter_cliente` (pelo `uuid ANERA`). Se as fontes divergirem, mostre a divergência e pergunte qual vale. Campo faltando nas duas → pergunte ou extraia dos documentos pessoais (não invente) e **ofereça** `anera_atualizar_cliente` com o dado novo.
   - Do caso: `{{DESCRICAO_DO_CASO}}`, `{{PARTE_CONTRARIA}}`, `{{NUMERO_PROCESSO}}`, `{{JUIZO}}` — proponha a partir do `PROCESSO.md` e peça confirmação. Exemplos de descrição no LEIA-ME dos contratos.
   - Valores: pergunte entrada, percentual, valor fixo e forma de pagamento (com `financeiro:leitura`, consulte antes `anera_honorarios` do processo e use como sugestão). Escreva valores e percentuais também por extenso.
   - Multa (contratos B e C: 5 salários mínimos; E: 7 salários mínimos): **pergunte o valor do salário mínimo vigente** e mostre o cálculo antes de usar. Escreva em reais.
   - Nomes em caixa alta como no documento de identidade.
   - Nenhum campo termina com ponto final (ex.: `SEGURADORA X S/A`, não `S.A.`), porque o modelo já pontua a frase.
5. **Gerar.** Para cada documento:
   - Grave os dados em um JSON **temporário no scratchpad** (nunca na pasta do escritório).
   - Rode: `python "${CLAUDE_PLUGIN_ROOT}/scripts/preencher_modelo.py" --modelo <modelo aprovado em 03_MODELOS> --saida "<caso>/contrato-procuracao/AAAA-MM-DD_<tipo>_v1.docx" --dados <json> --pdf`
     - `<tipo>`: `contrato-honorarios-A` … `-E`, `procuracao-A` … `-D`, `declaracao-hipossuficiencia`.
     - Se o arquivo já existir, use `_v2`, `_v3`… (o script não sobrescreve).
   - Apague o JSON temporário ao final.
6. **Conferir.** Informe os campos que ficaram sem preencher. Mostre um resumo do que foi gerado (modelo escolhido, valores, multa) para o advogado revisar antes de enviar ao cliente.
7. **Registrar.** No `PROCESSO.md`, preencha "Modelo de contrato / honorários" e acrescente uma linha no "Histórico". Com o ANERA conectado, proponha (e grave após o "sim") `anera_criar_anotacao` no processo/atendimento: `[Histórico] Contrato de honorários (modelo X, condições) e procuração (modelo Y) gerados em DD/MM — aguardam assinatura`. Proponha também `anera_definir_honorarios` com o valor fixo e/ou o % de êxito contratados (escopo `financeiro:escrita`; se faltar, oriente a reconectar com a permissão). Quando o contrato **assinado** voltar, ofereça anexá-lo a uma anotação (`anera_link_anexos` + `curl`).
8. **Não enviar.** Os documentos não são enviados a ninguém nem a plataformas de assinatura; o envio é feito pelo advogado.
