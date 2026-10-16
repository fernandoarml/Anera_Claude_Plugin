---
description: Organiza em uma pasta, na ordem de protocolo, a peça e os documentos que serão juntados (procuração, documentos pessoais e doc_1, doc_2...)
argument-hint: <cliente> <caso> [peça: inicial (padrão) | réplica | contestação | ...]
---
Prepare os documentos para protocolo de: $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. **Localizar o caso** em `01_CLIENTES/_INDICE.md` e ler o `PROCESSO.md`. Identificar a peça (padrão: petição inicial) e a **versão final** dela em `pecas/` (a de maior número de versão; se houver dúvida, perguntar).

2. **Levantar o que pode ser juntado**:
   - a peça;
   - `contrato-procuracao/`: procuração (preferir a **versão assinada em PDF**; se só houver a não assinada, avisar) e declaração de hipossuficiência, se o caso pedir gratuidade;
   - `documentos-pessoais/`: documento de identidade e comprovante de residência;
   - `documentos-caso/`: provas e demais documentos.
   Ler a peça e extrair o **rol de documentos** citados ("doc. 1", "anexo", "conforme documento...") e os fatos que dependem de prova.

3. **Propor o plano** em uma tabela — **antes de copiar qualquer arquivo**:

   | Ordem | Nome no protocolo | Arquivo de origem | Por que entra |
   |---|---|---|---|

   Ordem e nomes:
   - `00_peticao_inicial` (ou `00_<peca>`): a peça;
   - `01_procuracao`;
   - `02_documento_pessoal`;
   - `03_comprovante_residencia`;
   - `04_declaracao_hipossuficiencia` (só se houver pedido de gratuidade);
   - demais documentos: `doc_1_<descricao>`, `doc_2_<descricao>`, ... na **ordem em que aparecem na peça** (cronológica, se a peça não definir).

   Regras:
   - `<descricao>` curta, minúscula, sem acentos e sem espaços (ex.: `doc_3_laudo_cautelar`).
   - **Fotos e arquivos do mesmo fato** viram um único PDF (ex.: `doc_5_fotos_portas_traseiras`).
   - Liste também, separadamente, **o que NÃO entra e por quê** (ex.: arquivo de referência, documento estratégico que não convém juntar, duplicado).
   - Aponte: documentos citados na peça que **não foram encontrados**; documentos encontrados que a peça **não cita**; divergência entre a numeração da peça e a do protocolo (a peça deve citar `doc_1`, `doc_2`... na mesma ordem — sugerir o ajuste na peça, sem alterá-la sozinho).

4. **Esperar a confirmação do advogado.** Ajustar a ordem, incluir ou excluir conforme a estratégia indicada.

5. **Montar a pasta** com o script:
   - Grave o plano confirmado em um JSON **temporário no scratchpad**, com caminhos absolutos e `"destino": "<caso>/protocolo-inicial"` (para outras peças: `protocolo-<peca>`, ex.: `protocolo-replica`).
   - Se a pasta já existir, use `_v2`, `_v3`... (o script não sobrescreve).
   - Rode: `python "${CLAUDE_PLUGIN_ROOT}/scripts/montar_protocolo.py" --plano <json>`
   - Apague o JSON temporário ao final.
   O script copia (nunca move) os originais, converte Word e imagens para PDF e une várias origens em um só arquivo.

6. **Gerar o `INDICE-PROTOCOLO.md`** dentro da pasta criada, com:
   - a tabela final (ordem, arquivo, origem, páginas, tamanho);
   - os documentos **não juntados** e o motivo;
   - pendências (documentos faltando, procuração sem assinatura, ajustes de numeração na peça).

7. **Conferir para o protocolo:**
   - apontar arquivos grandes (o limite por arquivo varia conforme o tribunal/sistema — o advogado confirma o limite aplicável);
   - lembrar que o protocolo é feito pelo advogado no sistema do tribunal.

8. **Registrar** no `PROCESSO.md` (Histórico e, se houver, pendências), conforme a regra 8 do `CLAUDE.md`. Com o ANERA conectado, proponha `anera_criar_anotacao` (`[Histórico] Pasta de protocolo montada: N documentos`). Depois do protocolo, ofereça uma anotação `[Histórico] Protocolado em DD/MM` com **a peça e os documentos protocolados anexados** (`anera_link_anexos` + `curl -F` com os PDFs de `protocolo-inicial/`; até 10 MB por arquivo e até 20 por link — se houver mais, gere outro link). Depois que o advogado informar que **protocolou**, ofereça: `anera_adicionar_andamento` (protocolo), `anera_concluir_prazo` do prazo correspondente e, na petição inicial, `anera_atualizar_processo` com o número CNJ recebido — sempre com confirmação.
