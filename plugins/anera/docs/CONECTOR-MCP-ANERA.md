# Conector ANERA — referência de uso

> Usado pelo plugin `anera` para o Claude se conectar ao ANERA. Servidor v1.5.0.
> Endereço: `https://app.anera.com.br/backend/mcp` (remoto, OAuth 2.1 — não há token para copiar nem nada para instalar).

## Conectar
1. Digite `/mcp`, escolha **anera** e clique em autenticar.
2. Faça login no ANERA e marque as permissões na tela de consentimento.
3. Teste: peça "rode o anera_status".

Sem conexão, as ferramentas `anera_*` não aparecem e o trabalho segue só com a pasta. Para desconectar: ANERA › **Configurações › Integrações com IA**.

## 1. Permissões

| Escopo | Libera | Ferramentas |
|---|---|---|
| `leitura` *(sempre concedido)* | Consultas gerais, inclusive publicações | todas as de §3.1 e as de consulta de §3.4, exceto `anera_honorarios` |
| `financeiro:leitura` | Honorários e faturas | `anera_honorarios` |
| `financeiro:escrita` | Definir honorários do processo | `anera_definir_honorarios` |
| `publicacoes:escrita` | Tratar publicações/intimações | `anera_marcar_publicacao_lida`, `anera_arquivar_publicacao`, `anera_vincular_publicacao` |
| `anotacoes:escrita` | Comentários e seus anexos | `anera_criar_anotacao`, `anera_link_anexos` |
| `prazos:escrita` | Prazos e compromissos | `anera_criar_prazo`, `anera_concluir_prazo` |
| `cadastro:escrita` | Clientes, atendimentos, processos, andamentos | `anera_cadastrar_cliente`, `anera_atualizar_cliente`, `anera_cadastrar_atendimento`, `anera_atualizar_atendimento`, `anera_arquivar_atendimento`, `anera_reativar_atendimento`, `anera_cadastrar_processo`, `anera_atualizar_processo`, `anera_adicionar_andamento` |

**Comportamento quando falta permissão:**
- `tools/list` só lista as ferramentas cobertas pelos escopos concedidos. Para o modelo, a ferramenta
  "não existe".
- Se mesmo assim uma ferramenta for chamada, ela devolve erro com a orientação: *"Esta conexão não tem a
  permissão X. Para usá-la, desconecte o ANERA neste aplicativo, conecte de novo e autorize essa
  permissão."*
- **No plugin:** quando um comando precisa de escrita e a ferramenta não está disponível, explique ao
  usuário que é preciso reconectar e marcar a permissão.

**Identidade:**
- A conexão age **como o usuário que autorizou**. Prazos, anotações e andamentos ficam no nome dele.
  Prazos do tipo `Pessoal` de outros usuários não aparecem.
- Cada pessoa do escritório (inclusive subcontas) conecta a própria conta.
- **Sessões independentes:** logar no ANERA pelo navegador **não** derruba a conexão do Claude.

**Validade:**
- O access token vale 1 h e o refresh token 30 dias, renovado a cada uso.
- O usuário pode desconectar a qualquer momento em **Configurações › Integrações com IA**. A conta
  principal vê e desconecta as conexões de todo o escritório.

---

## 2. Convenções das respostas

- **Formato:** cada ferramenta devolve **um bloco de texto com JSON** (`content[0].text`).
  `isError: true` indica erro de validação ou de regra, com mensagem em português que pode ser mostrada
  ao usuário.
- **Identificadores:** sempre `uuid`. Para obter um uuid, use as ferramentas de busca.
- **Datas:**
  - Parâmetros de data usam `AAAA-MM-DD`.
  - `data_limite` de prazo aceita `AAAA-MM-DD` ou `AAAA-MM-DD HH:MM`.
  - Prazo **sem horário** é gravado como `00:00` e devolvido só como `AAAA-MM-DD`.
  - O fuso é `America/Sao_Paulo` (-03:00). Para saber "hoje", use `anera_status`.
- **Respostas enxutas:** campos vazios ou nulos são **omitidos**, e textos longos de andamento vêm
  resumidos (600 caracteres), salvo pedido de `texto_completo`.
- **Limites:** padrão de 20 itens (máximo 100). Em prazos o padrão é 50 e em andamentos 30.
- **Taxa:** 120 chamadas por minuto por conexão. Acima disso, a resposta é HTTP 429.
- **Instruções do servidor:** o `initialize` devolve instruções que o Claude recebe automaticamente:
  - sigilo profissional;
  - identificar registros por uuid;
  - usar a calculadora para prazos;
  - **confirmar com o usuário antes de gravar**;
  - nenhuma ferramenta exclui registros.

---

## 3. Referência das ferramentas

`*` = obrigatório.

### 3.1 Consulta

#### `anera_status` — `leitura`
Sem parâmetros. Devolve `usuario {nome, email}`, `escritorio`, `conta_principal`, `permissoes[]`,
`agora` (ISO com fuso), `hoje`, `dia_da_semana`. **Use no início dos comandos** para saber se o ANERA
está conectado, quais permissões existem e qual é a data de hoje.

#### `anera_painel` — `leitura`
| Parâmetro | Tipo | Observação |
|---|---|---|
| `dias` | int 1–60 | padrão 7 |
| `apenas_meus` | bool | só prazos do usuário conectado |

Devolve:
- `prazos_atrasados[]`, `prazos_hoje[]` e `prazos_proximos_dias[]`, já incluindo audiências e
  reuniões;
- `processos_com_andamentos_nao_lidos[] {uuid, caso, numero_cnj, nao_lidos, ultimo_andamento}`;
- `publicacoes_nao_lidas`: quantas publicações/intimações aguardam leitura na caixa de entrada.

#### `anera_buscar_clientes` — `leitura`
`busca` (nome, empresa, e-mail ou CPF/CNPJ, com ou sem pontuação) · `status` `ativos|inativos|todos`
(padrão ativos) · `limite`.
Devolve `clientes[] {uuid, nome, empresa, cpf_cnpj, email, celular, cidade, estado, status}`.

#### `anera_obter_cliente` — `leitura`
`cliente_uuid*`. Devolve a **qualificação completa**, que é a base de contrato, procuração e
declaração:
- **Qualificação:** `nome, empresa, cpf_cnpj, rg_ie, data_nascimento, estado_civil, nome_conjuge,
  cpf_conjuge, nacionalidade, profissao`.
- **Contato e endereço:** `email, celular, telefone, cep, endereco, numero, bairro, cidade, estado`.
- **Outros dados:** `status, observacoes, data_cadastro`.
- **Listas:** `campos_adicionais[] {rotulo, valor}`, `contatos[]`,
  `processos[] {uuid, caso, numero_cnj, situacao, natureza, comarca, vara}` e
  `atendimentos[] {uuid, numero, titulo, situacao}`.

Valores-lixo herdados do sistema antigo (CPF, RG ou CEP zerados, data `0000-00-00`) são omitidos. Se um
campo não vier, ele **não está cadastrado**: o comando deve perguntar ao usuário em vez de inventar.

#### `anera_buscar_processos` — `leitura`
`busca` (CNJ com ou sem pontuação, nome do caso ou do cliente) · `cliente_uuid` · `situacao`
`Ativo|Arquivado|todos` (padrão Ativo) · `limite`.
Devolve `processos[] {uuid, numero_interno, caso, numero_cnj, natureza, comarca, vara, situacao,
cliente{uuid,nome}, andamentos_nao_lidos}`.

#### `anera_obter_processo` — `leitura`
`processo_uuid*`. Devolve:
- **Identificação:** `numero_interno, caso, pasta, posicao_cliente`.
- **Classificação:** `natureza, procedimento(+_descricao), competencia(+_descricao)`.
- **Tramitação:** `judicializado, eletronico, sistema, numero_cnj, instancia, comarca, vara`.
- **Situação:** `valor_causa, situacao, observacoes, ultima_movimentacao`.
- **Pessoas:** `cliente{}`, `partes_contrarias[] {nome, posicao, documento, telefone, email}`,
  `representados[]`.
- **Andamento do caso:** `historico_status[]`, `prazos_pendentes[]` (até 10), `ultimo_andamento`,
  `andamentos_nao_lidos`.

#### `anera_listar_prazos` — `leitura`
| Parâmetro | Observação |
|---|---|
| `de`, `ate` | `AAAA-MM-DD` |
| `status` | `Pendente` (padrão), `Concluido`, `todos` |
| `tipo` | `Prazo`, `Audiencia`, `Petição Inicial`, `Reuniao`, `Manifestacao`, `Recurso`, `Pessoal`, `Outro` |
| `responsavel` | `"meus"` ou uuid de usuário |
| `processo_uuid`, `cliente_uuid`, `atendimento_uuid` | filtros |
| `busca` | trecho do título |
| `limite` | padrão 50 |

Cada prazo traz `{uuid, titulo, tipo, status, data_limite, atrasado, observacao, concluido_em,
responsavel{}, processo{}, atendimento{}, cliente{}}`. **Não há tabela separada de audiências:**
audiência, reunião etc. são prazos com `tipo`.

#### `anera_listar_andamentos` — `leitura`
`processo_uuid*` · `desde` · `texto_completo` (bool) · `limite` (padrão 30).
Devolve `andamentos[] {data, origem: tribunal|manual, texto, sigiloso, nao_lido, lancado_por}`.
**Não marca andamentos como lidos no ANERA** (os avisos de "novo" dos usuários continuam).

#### `anera_novidades` — `leitura`
`desde` (opcional: sem ele, traz os **não lidos**; com ele, tudo desde a data) · `limite` (processos,
padrão 20).
Devolve `processos[] {processo{}, cliente{}, total_andamentos, andamentos[] (até 10, resumidos)}`.
Também não marca como lido.

#### `anera_listar_anotacoes` — `leitura`
`referencia*` (`processos|prazos|atendimentos`) · `uuid*` · `limite`.
Devolve `anotacoes[] {uuid, texto, autor, criado_em, anexos[]}`, da mais recente para a mais antiga.

#### `anera_buscar_atendimentos` / `anera_obter_atendimento` — `leitura`
- **`anera_buscar_atendimentos`:** recebe `busca`, `cliente_uuid`, `situacao` e `limite`.
- **`anera_obter_atendimento`:** recebe `atendimento_uuid*` e devolve:
  - `numero, titulo, descricao, pasta, situacao, numero_cnj, cliente{}`;
  - `motivo_arquivamento` e `resultado_arquivamento`, **só quando arquivado**;
  - `prazos_pendentes[]` e `ultimas_anotacoes[]` (as 5 mais recentes);
  - `criado_pela_ia_aguardando_revisao`, quando for o caso.
- **Uso:** atendimento é a consulta ou caso ainda não judicializado. É o "caso pré-processual".

#### `anera_listar_responsaveis` — `leitura`
Sem parâmetros. Devolve `usuarios[] {uuid, nome, funcao, oab, voce}`. Use para escolher o responsável
de um prazo e para preencher OAB e nome de advogados nos documentos.

#### `anera_opcoes_processo` — `leitura`
Sem parâmetros. Devolve os valores aceitos em `anera_cadastrar_processo`:
- `posicao_cliente[]`;
- `natureza[]`, `procedimento[]` e `competencia[]`, cada um como `{valor, descricao}`.

Envie o **`valor`**.

#### `anera_calcular_prazo` — `leitura`
`data_inicio*` (data da intimação, não contada) · `dias*` · `regra`
(`cpc` padrão, `clt`, `uteis`, `cpp`, `civil`, `corridos`) · `uf` (feriados estaduais).
Devolve `data_final, regra, base_legal, prorrogado, motivo_prorrogacao, dias_nao_contados[]`.
**Regra para o plugin:** *nunca* conte prazo no próprio modelo. Sempre use esta ferramenta, que
considera feriados nacionais e estaduais, recesso forense (CPC) e prorrogação.

#### `anera_honorarios` — `financeiro:leitura`
`processo_uuid` **ou** `cliente_uuid`. Devolve:
- `honorarios_processo`, só com processo:
  - `valor_causa`;
  - `contratuais {valor_fixo, percentual_exito, exito_estimado}`;
  - `sucumbencia {percentual, valor_estimado, exigibilidade_suspensa, motivo}`.
- `faturas_em_aberto[] {uuid, numero, vencimento, valor, valor_pago, parcela, vencida}`.
- `total_em_aberto`.

### 3.2 Escrita

Todas as ferramentas de escrita:
- **pedem confirmação** na descrição: o modelo deve mostrar o que vai gravar e esperar o "ok";
- **nunca excluem** registros e nunca alteram a data de um prazo existente;
- são **auditadas** no log de atividades do ANERA com `origem = claude`, usuário e conexão;
- aplicam as mesmas regras das telas do ANERA: seguidores, notificações, trava do CNJ.

#### `anera_criar_anotacao` — `anotacoes:escrita`
`referencia*` (`processos|prazos|atendimentos`) · `uuid*` · `texto*` ·
`anexos[] {nome*, conteudo_base64*}` (opcional, até 5 arquivos de até 2 MB cada).
- **Anexos em base64:** só para arquivos **pequenos** cujo conteúdo o Claude já tem (ex.: um resumo que
  ele mesmo gerou). O base64 passa pela conversa e consome contexto. Para arquivos da pasta local, use
  `anera_link_anexos` (abaixo).
- **Validação antes de gravar:** extensão não permitida, base64 inválido ou arquivo acima de 2 MB
  recusam a chamada inteira, e a anotação **não** é criada.
- **Prefixo:** o servidor grava o texto com **`IA: `** no início, automaticamente (se o texto já começar
  com `IA:`, não duplica). Não inclua o prefixo no comando; ele serve para distinguir no ANERA o que veio
  da IA do que foi escrito à mão.
- **Efeito:** o autor passa a seguir o item e quem já segue é notificado.
- **Retorno:** `{uuid, anexos[] {uuid, nome, tamanho}}`. Guarde o `uuid` para anexar arquivos depois.
- **Correspondência com o `/registrar`:** o ANERA **não tem tipos de anotação** (histórico, decisão,
  pendência). Use um marcador no texto: `"[Decisão] …"`, `"[Pendência] …"`, `"[Histórico] …"`. No
  ANERA fica `IA: [Decisão] …`.

#### `anera_link_anexos` — `anotacoes:escrita`
`anotacao_uuid*` · `max_arquivos` (1–20, padrão 10).
- **Para que serve:** anexar arquivos da **pasta local** (PDF da petição, contrato, comprovante) a uma
  anotação. O arquivo vai direto do disco para o ANERA por HTTP, sem passar pela conversa.
- **Retorno:** `{url, expira_em, max_arquivos, tamanho_maximo_mb, extensoes[], como_enviar,
  varios_arquivos}`.
- **Validade:** o link vale **15 minutos**, só para **aquela anotação** e só até `max_arquivos`
  arquivos. Também deixa de valer se a conexão for desconectada.
- **Quem pode anexar:** só em anotações **criadas pelo próprio usuário** conectado.
- **Envio (Claude Code / Cowork, via Bash):**
  ```bash
  curl -sS -F "arquivo=@/caminho/peticao-inicial.pdf" "<url>"
  # vários de uma vez:
  curl -sS -F "arquivo[]=@/caminho/a.pdf" -F "arquivo[]=@/caminho/b.docx" "<url>"
  ```
- **Resposta do envio (JSON):** `{mensagem, anotacao_uuid, anexos[] {uuid, nome, tamanho}, erros[]
  {arquivo, erro}}`. Num envio com vários arquivos, os válidos entram e os recusados aparecem em
  `erros`, sem gastar o limite do link.
- **Códigos HTTP:**
  - `200`: pelo menos um arquivo anexado;
  - `422`: nenhum arquivo aceito;
  - `409`: o limite de arquivos do link acabou;
  - `410`: o link expirou;
  - `404`: link inválido ou revogado.
- **Restrições:** extensões `txt, doc, docx, xls, xlsx, pdf, ppt, pptx, jpg, jpeg, png, webp` (as
  mesmas do ANERA), até **10 MB por arquivo**.
- **Fluxo típico:** `anera_criar_anotacao` (texto) → `anera_link_anexos` (uuid devolvido) → `curl -F`
  para cada arquivo → conferir a resposta. Os anexos aparecem na anotação dentro do ANERA e podem ser
  baixados normalmente.

#### `anera_criar_prazo` — `prazos:escrita`
`titulo*` · `data_limite*` · `tipo` (padrão `Prazo`) · `processo_uuid` · `atendimento_uuid` ·
`publicacao_uuid` · `responsavel_uuid` (padrão: o usuário conectado) · `observacao`.
- **Vínculo com a intimação:** com `publicacao_uuid`, o prazo aparece vinculado à publicação no ANERA.
  Se a publicação já estiver ligada a um processo e `processo_uuid` não for enviado, o prazo herda esse
  processo.
- **Status inicial:** entra como **Pendente**.
- **Notificação:** se o responsável for outra pessoa, ela é notificada.
- **Deduplicação:** se já existir um prazo com mesmo título, data e processo criado nas últimas 24h,
  devolve `{duplicado: true, uuid}` sem criar outro.
- **Restrição:** prazo `Pessoal` só pode ter o próprio usuário como responsável.

#### `anera_concluir_prazo` — `prazos:escrita`
`prazo_uuid*` · `observacao` (vira anotação no prazo, também com o prefixo `IA:`, ex.: "Contestação
protocolada em 14/10").
Se o prazo já estiver concluído, apenas informa.

#### `anera_adicionar_andamento` — `cadastro:escrita`
`processo_uuid*` · `texto*`. Lança um andamento **manual**, já marcado como lido.

#### `anera_cadastrar_cliente` — `cadastro:escrita`
`nome*` e, opcionalmente, todos os campos de qualificação de `anera_obter_cliente`.
- **Formatos aceitos:** `estado` deve ser a UF com 2 letras, `data_nascimento` no formato `AAAA-MM-DD`
  e `email` precisa ser válido.
- **CPF/CNPJ já cadastrado:** não cria outro e devolve `{duplicado: true, uuid, nome}`. Nesse caso,
  use `anera_atualizar_cliente`.

#### `anera_atualizar_cliente` — `cadastro:escrita`
`cliente_uuid*` e os campos que mudam. **Campos vazios são ignorados** (não apagam o valor atual). Se o
CPF/CNPJ informado pertencer a outro cliente, a ferramenta recusa.

#### `anera_cadastrar_atendimento` — `cadastro:escrita`
`cliente_uuid*` · `titulo*` (assunto) · `descricao` (relato).
- **Uso:** abre um atendimento (consulta ou caso ainda não judicializado) para um cliente **já
  cadastrado**. Se o cliente for novo, cadastre-o antes com `anera_cadastrar_cliente`.
- **Deduplicação:** se já existir atendimento com o mesmo título para o mesmo cliente criado nas
  últimas 24h, devolve `{duplicado: true, uuid, numero}` sem criar outro.
- **Retorno:** `{uuid, numero}`. O número segue a sequência anual do ANERA (ex.: `2026-00003`).
- **Revisão:** o atendimento nasce marcado como criado pela IA (§3.3).

#### `anera_atualizar_atendimento` — `cadastro:escrita`
`atendimento_uuid*` · `titulo` · `descricao`.
- **Alteração parcial:** envie só o que muda. Campos vazios são ignorados. A `descricao` enviada
  **substitui** o relato atual.
- **Descrição ou anotação:** a descrição é o resumo do caso. O que foi conversado em cada contato vai em
  anotação (`anera_criar_anotacao` com `referencia: "atendimentos"`), que guarda o histórico com data e
  autor e aceita anexos.

#### `anera_arquivar_atendimento` — `cadastro:escrita`
`atendimento_uuid*` · `motivo*` · `resultado*` (`contratacao`, `processo`, `nenhum`, `outro`) ·
`numerocnj` (obrigatório quando `resultado = processo`).
- **Mesma regra da tela:** com resultado `processo`, só é possível arquivar com o número CNJ, ou seja,
  depois da distribuição.
- **Dica no retorno:** quando o resultado é `processo`, a resposta lembra de cadastrar o processo com
  `anera_cadastrar_processo` usando o mesmo CNJ.
- **Repetição:** arquivar um atendimento já arquivado só informa, sem erro.

#### `anera_reativar_atendimento` — `cadastro:escrita`
`atendimento_uuid*`. Reabre um atendimento arquivado (volta a `Ativo`).

#### `anera_cadastrar_processo` — `cadastro:escrita`
`cliente_uuid*` · `posicao_cliente*` · `natureza*` · `procedimento*` (valores de
`anera_opcoes_processo`) · `competencia` · `caso` · `numerocnj` · `comarca` · `vara` · `sistema` ·
`valor_causa` (número) · `observacoes` · `partes_contrarias[] {nome*, posicao, documento}`.
- **Cliente:** precisa existir. Cadastre-o antes, se for o caso.
- **CNJ já cadastrado:** devolve `{duplicado: true, uuid}` sem criar outro.
- **Caso ainda não ajuizado:** cadastre sem `numerocnj`.

#### `anera_definir_honorarios` — `financeiro:escrita`
`processo_uuid*` · `valor_fixo` (R$, ≥ 0) · `percentual_exito` (0–100) · `sucumbencia_percentual`
(0–100) · `sucumbencia_suspensa` (bool) · `sucumbencia_motivo`.
- **Alteração parcial:** envie só o que muda. O que não for enviado mantém o valor atual (o servidor
  mescla antes de gravar).
- **Suspensão:** `sucumbencia_motivo` só é guardado quando `sucumbencia_suspensa = true`. Ao tirar a
  suspensão, o motivo é apagado.
- **Retorno:** `{honorarios {valor_fixo, percentual_exito, sucumbencia_percentual, sucumbencia_suspensa,
  sucumbencia_motivo}, alteracoes {campo: {de, para}}}`. Se nada mudou, a resposta diz isso e não há
  `alteracoes`.
- **Auditoria:** registra o "de → para" de cada campo.
- **Leitura:** os valores atuais e as estimativas (êxito e sucumbência sobre o valor da causa) vêm de
  `anera_honorarios`.
- **Uso típico:** no `/documentos-cliente`, depois de gerar o contrato, gravar o valor fixo e o
  percentual de êxito contratados.

#### `anera_atualizar_processo` — `cadastro:escrita`
`processo_uuid*` · `caso` · `numerocnj` · `comarca` · `vara` · `sistema` · `instancia` · `valor_causa`
· `observacoes`.
- **`numerocnj`:** só é aceito se o processo ainda não tiver número. É o fluxo "após o ajuizamento".
- **Partes contrárias:** não são alteradas por aqui.

### 3.3 Marcação "criado pela IA" e validação

Prazos (`anera_criar_prazo`), processos (`anera_cadastrar_processo`) e atendimentos
(`anera_cadastrar_atendimento`) criados pelo conector nascem **marcados como criados pela IA**.

- **No ANERA:** aparece uma etiqueta discreta **IA** nas listas (Tarefas & Prazos, Agenda, Processos,
  Atendimentos, Quadro de Atividades). Nas telas de detalhe aparece **IA · Validar**. Depois de revisar
  os dados, o usuário clica em **Validar** e a etiqueta some de todas as telas. Quem validou e quando
  fica registrado no histórico.
- **Nas ferramentas de leitura:** registros ainda não validados trazem
  `criado_pela_ia_aguardando_revisao: true` (em `anera_listar_prazos`, `anera_painel`,
  `anera_obter_processo` e `anera_obter_atendimento`). O plugin pode lembrar o usuário de revisar,
  por exemplo no `/painel`: *"Há 3 prazos criados pela IA aguardando sua validação no ANERA"*.
- **Limites:** a validação é feita **só no ANERA**, nunca pelo MCP. A IA não pode "aprovar" o próprio
  trabalho. Clientes cadastrados e edições feitas pela IA não recebem a marcação. Edições ficam
  registradas no histórico com `origem = claude`.

### 3.4 Publicações e intimações

Publicações capturadas dos diários oficiais (DJEN etc.) pelo monitoramento do ANERA. **Consultar pelo
Claude nunca marca como lida.** Marcar como lida é sempre uma ação explícita, feita depois de tratar a
intimação.

#### `anera_listar_publicacoes` — `leitura`
`leitura` (`nao_lidas` padrão, `lidas`, `todas`) · `caixa` (`entrada` padrão, `arquivadas`) ·
`processo_uuid` · `busca` (número do processo com ou sem pontuação, tribunal, órgão, caso, cliente) ·
`de` / `ate` (data de disponibilização) · `limite`.
Devolve `publicacoes[] {uuid, data_disponibilizacao, tribunal, orgao, numero_processo, meio, lida,
arquivada, processo{}, processo_sugerido{}, cliente{}, prazos_criados, resumo}`.
- `processo_sugerido` aparece quando a publicação ainda não está vinculada, mas existe no ANERA um
  processo com o mesmo número CNJ.

#### `anera_obter_publicacao` — `leitura`
`publicacao_uuid*`. Devolve:
- os mesmos campos da listagem, com o **texto completo** (`texto`, já sem HTML);
- `link_inteiro_teor` e `link`;
- `prazos_vinculados[]`, os prazos já criados a partir da publicação.

#### `anera_marcar_publicacao_lida` — `publicacoes:escrita`
`publicacao_uuid*` · `lida` (padrão `true`; `false` volta para não lida).
- O ANERA guarda a data da primeira leitura. Voltar para não lida não apaga essa data (mesmo
  comportamento da tela).

#### `anera_arquivar_publicacao` — `publicacoes:escrita`
`publicacao_uuid*` · `arquivar` (padrão `true`; `false` devolve à caixa de entrada). Não exclui.

#### `anera_vincular_publicacao` — `publicacoes:escrita`
`publicacao_uuid*` · `processo_uuid*`. Normalmente usado com o `processo_sugerido`. Se a publicação já
estava ligada a outro processo, ela é transferida e a resposta avisa.

#### Fluxo recomendado: "trate as intimações novas"
1. `anera_listar_publicacoes` (não lidas).
2. Para cada uma, `anera_obter_publicacao` e leitura do texto.
3. Se houver `processo_sugerido`, propor `anera_vincular_publicacao`.
4. Identificar a providência e o prazo, depois `anera_calcular_prazo` (data de início = data da
   intimação, conforme a regra aplicável).
5. Mostrar o resumo ao usuário e, com confirmação, `anera_criar_prazo` com `publicacao_uuid`. O prazo
   nasce com a etiqueta IA para revisão.
6. `anera_marcar_publicacao_lida`. Se não houver providência, `anera_arquivar_publicacao`.

O `initialize` do servidor já instrui o Claude nessa ordem.

### 3.5 Modelos de documentos *(servidor 1.6.0 — em implementação)*

#### `anera_listar_modelos` — `leitura`
Sem parâmetros. **Retorno:** `{versao_pacote, atualizado_em, disponivel, motivo?, modelos[] {id, tipo, titulo, usa_timbrado}}`.
Com `disponivel: false`, mostre o `motivo` ao usuário (os modelos são para assinantes).

#### `anera_link_modelos` — `leitura`
`ids` (opcional; sem ele, pacote completo). **Retorno:** `{url, expira_em, arquivo, tamanho, sha256, versao_pacote, como_baixar}`.
- Link de **15 minutos**, uso único, só para a conexão que pediu.
- Baixe direto para o disco (`curl -fsSL -o .claude/modelos-anera.zip "<url>"`), confira o `sha256` e instale com
  `scripts/instalar_modelos.py --origem .claude/modelos-anera.zip ...` (confere cada arquivo pelo `manifesto.json`).
  Nunca peça o conteúdo dos modelos na conversa.
- Fluxo completo: `/anera:configurar-escritorio`, etapa 6.

---

## 4. Regras de uso

1. **Comece com `anera_status`.** Ele diz se há conexão, quais permissões existem e a data de hoje. Sem
   conexão, siga no modo só pasta.
2. **Confirme antes de gravar.** Mostre um resumo do que será enviado (campos e valores) e só chame a
   ferramenta de escrita após o "sim" do usuário.
3. **Busque antes de criar.** Use `anera_buscar_clientes` e `anera_buscar_processos` antes de
   `cadastrar_*`. A deduplicação do servidor é a última barreira, não a primeira.
4. **Prazos processuais:** primeiro `anera_calcular_prazo`, depois `anera_criar_prazo` com a
   `data_final` devolvida.
5. **Não invente dados de qualificação.** Se `anera_obter_cliente` não trouxer um campo, pergunte ao
   usuário ou extraia de um documento da pasta e **ofereça** `anera_atualizar_cliente`.
6. **O vínculo com a pasta é pelo uuid.** Grave na ficha (`CLIENTE.md` / `PROCESSO.md`) o campo
   `uuid ANERA: …` devolvido pelas ferramentas. O ANERA ainda **não** guarda o caminho da pasta (§6).
7. **Anotações já saem marcadas.** O servidor prefixa `IA: ` em toda anotação. Não repita o prefixo no
   texto enviado.
8. **Arquivos vão como anexo de anotação, e só quando fizer sentido.** O original fica na pasta. Quando o
   escritório quiser o arquivo também no ANERA (petição protocolada, contrato assinado, comprovante),
   crie a anotação e anexe com `anera_link_anexos` + `curl`. Nunca use base64 para arquivos da pasta.
9. **Sigilo.** Não copie dados de clientes para dentro do plugin, de exemplos ou de logs.

---

## 5. Comandos × ferramentas

| Comando | Com o ANERA conectado |
|---|---|
| `/configurar-escritorio` | `anera_status` para testar a conexão e mostrar as permissões. Também `anera_listar_responsaveis` para pré-preencher advogados e OAB, e `anera_listar_modelos` → `anera_link_modelos` + `curl` para baixar e instalar os modelos. |
| `/buscar` | `anera_buscar_clientes` / `anera_buscar_processos`, seguidos de `anera_obter_processo` (próximo prazo e último andamento) |
| `/novo-cliente` | `anera_buscar_clientes` (CPF), depois `anera_cadastrar_cliente` ou `anera_atualizar_cliente` com dados extraídos de RG, CNH e comprovante. Grava o uuid na `CLIENTE.md`. |
| `/novo-processo` | `anera_opcoes_processo`, depois `anera_cadastrar_processo`. Grava o uuid na `PROCESSO.md`. |
| `/documentos-cliente` | `anera_obter_cliente` (qualificação) e `anera_listar_responsaveis` (advogados). Ao final, com confirmação: `anera_definir_honorarios` (valor fixo e % de êxito do contrato) e `anera_criar_anotacao` registrando os documentos gerados. |
| `/peca` | `anera_obter_processo`, `anera_listar_andamentos` (`texto_completo` para decisões) e `anera_listar_anotacoes` |
| `/registrar` | `anera_criar_anotacao` (com marcador de tipo) e, se for movimentação, `anera_adicionar_andamento`. Se houver documento relacionado, `anera_link_anexos` + `curl`. |
| `/preparar-documentos` | `anera_criar_anotacao` registrando o protocolo, com a peça e os documentos protocolados anexados via `anera_link_anexos` + `curl`. Opcionalmente `anera_concluir_prazo` do prazo cumprido. |
| `/arquivar` | Ainda não há ferramenta para arquivar processo (§6). Registrar com `anera_criar_anotacao`. |
| Atendimento (consultas ainda não judicializadas) | `anera_buscar_atendimentos` → `anera_obter_atendimento` (relato + últimas anotações) → `anera_criar_anotacao` (`referencia: "atendimentos"`, com anexos se houver) / `anera_atualizar_atendimento` → ao final, `anera_arquivar_atendimento` |
| `/painel` | `anera_painel`. Destaque os itens com `criado_pela_ia_aguardando_revisao` e lembre de validá-los no ANERA. |
| `/novidades` | `anera_novidades` (andamentos) e `anera_listar_publicacoes` (intimações). Por item, sugestão de providência e, com confirmação, o fluxo de §3.4: `anera_calcular_prazo` → `anera_criar_prazo` (com `publicacao_uuid`) → `anera_marcar_publicacao_lida` |

---

## 6. O que o conector ainda não faz

| Item | Situação |
|---|---|
| Guardar no ANERA o caminho da pasta do cliente | não existe (o vínculo é o `uuid ANERA` na ficha) |
| Arquivar processo / alterar situação | não exposto |
| Tipos de anotação (histórico/decisão/pendência, resolver pendência) | não existe; usar prefixo |
| Marcar prazo fatal, responsável do processo e fase | não existe |
| Avisos em tempo real | não existe (o Claude consulta quando você pede, ex.: `/anera:painel`) |

Nesses casos, faça direto no ANERA.

## 7. Privacidade

O plugin acessa os dados do seu escritório no ANERA pelo conector oficial, com as permissões que você
escolheu ao conectar. O conteúdo que o Claude lê (fichas, documentos da pasta e dados do ANERA) é
processado pela Anthropic conforme o plano que você contratou: confira as configurações de
privacidade e de uso de dados da sua conta. O ANERA não recebe os arquivos da sua pasta. Nenhuma
ferramenta do conector exclui registros, e toda gravação feita pelo Claude fica registrada no
histórico do ANERA. Você pode desconectar a qualquer momento em **Configurações › Integrações com
IA**.
