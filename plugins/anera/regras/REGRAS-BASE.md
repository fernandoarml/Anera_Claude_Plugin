# Regras-base do plugin ANERA (escritório de advocacia)

Valem em toda sessão numa pasta de escritório configurada. Vêm do plugin e são atualizadas com ele. O que é **do escritório** fica no `CLAUDE.md` da pasta (áreas, padrões e **Preferências do escritório**), que **prevalece** sobre estas regras e sobre o padrão dos comandos. Exceções: sigilo, confirmação antes de gravar no ANERA e não inventar jurisprudência.

## Camadas: nunca editar o plugin
- **Nunca edite arquivos do plugin** (`${CLAUDE_PLUGIN_ROOT}`, pasta de plugins do Claude). Eles são substituídos a cada atualização.
- Quando o usuário pedir uma mudança de padrão ("a partir de agora…", "sempre…", "nunca mais…", "no contrato, faça…"):
  1. registre em `CLAUDE.md` › **Preferências do escritório** (em "Geral" ou na subseção do comando);
  2. mostre o texto e peça confirmação antes de gravar.
- Se a melhoria servir a qualquer escritório, ofereça registrar também em `06_PROCEDIMENTOS/SUGESTOES-PLUGIN.md`: data, comando, sugestão e motivo, **sem dados de clientes**.
- Modelos e textos-base copiados para a pasta (`03_MODELOS/`, `.claude/templates/`) são do escritório e podem ser editados.

## Estrutura da pasta
| Pasta | Conteúdo |
|---|---|
| `00_INTEGRACOES/` | Integrações. Prazos e financeiro ficam no ANERA, nunca aqui. |
| `01_CLIENTES/` | Uma pasta por cliente (`CLIENTE.md`) e uma subpasta por caso (`PROCESSO.md`). Índice: `01_CLIENTES/_INDICE.md`. |
| `02_ESTRATEGICO/<area>/` | Teses, uma subpasta por tese com `TESE.md`. Índice: `02_ESTRATEGICO/_INDICE.md`. |
| `03_MODELOS/` | `_base/` (timbrado, peça de referência, `PADRAO-FORMATACAO.md`), `pecas/<area>/` (só peças próprias aprovadas), `contratos/`, `procuracoes/`. |
| `04_PESQUISA/` | `jurisprudencia/<area>/`, `legislacao/`, `doutrina/`, `pecas-referencia/` (peças de terceiros). |
| `05_ADMINISTRATIVO/` · `06_PROCEDIMENTOS/` · `99_ARQUIVO/clientes/` | Interno · manual e sugestões · clientes encerrados |

**Cliente:** `NOME COMPLETO - MM-AAAA` (caixa alta, como no documento, com acentos; PJ: razão social). Dentro: `CLIENTE.md`, `documentos-pessoais/` e uma pasta por caso `AREA_PARTE-CONTRARIA_NUMERO`. A `AREA` é a sigla da tabela do `CLAUDE.md`. O `NUMERO` é o CNJ completo ou, antes do ajuizamento, `PRE-<sinistro|protocolo|data>`; renomear ao ajuizar.
**Caso:** `PROCESSO.md`, `contrato-procuracao/`, `documentos-caso/`, `autos/`, `pecas/`, `pesquisa/`, `protocolo-inicial/`.
**Arquivos:** `AAAA-MM-DD_tipo_vN.ext`. Nunca sobrescrever, criar `vN+1`. Sem acentos ou espaços em nomes criados pelo Claude, exceto a pasta do cliente.
**Índice:** atualizar `01_CLIENTES/_INDICE.md` ao criar, renomear, encerrar ou arquivar. Para localizar: índice → fichas → ANERA (`/anera:buscar` cria a pasta do que só existir no ANERA).
**Documentos Word:** partir de `03_MODELOS/_base/timbrado.docx` e seguir `PADRAO-FORMATACAO.md`. Declarações assinadas pelo cliente: página branca.

## Regras de trabalho
1. **Contexto primeiro:** ler `CLIENTE.md`, `PROCESSO.md` e as `TESE.md` vinculadas (e, com o ANERA, os andamentos recentes).
2. **Estilo:** peças seguem `03_MODELOS/`; peças de terceiros só como fonte de argumentos.
3. **Teses:** registrar o vínculo em `PROCESSO.md` e em `TESE.md`; atualizar o índice de teses.
4. **Jurisprudência:** nunca inventar julgados, números, ementas ou dispositivos. Sem fonte verificável, marcar `[VERIFICAR]`.
5. **Rascunhos:** tudo o que o Claude produz é rascunho até a revisão do advogado.
6. **Promoção a modelo:** só a pedido, e **anonimizado** (inclusive metadados e links internos).
7. **Encerramento:** cliente sem casos ativos vai para `99_ARQUIVO/clientes/`, com o índice atualizado.
8. **Memória do caso:** ao concluir qualquer trabalho num caso, atualizar `PROCESSO.md` sem esperar pedido:
   - Histórico, com data;
   - Decisões e combinados, com o motivo;
   - Pontos de atenção / Próximos passos.

   Informar em uma linha o que foi registrado.

## ANERA (conector MCP `anera`)
1. **Comece com `anera_status`** em tarefas com prazos, andamentos, cadastro ou anotações. Sem conexão: seguir só com a pasta, avisar "ANERA não conectado — /mcp › anera › autenticar" e dizer em uma frase o que a tarefa ganharia.
2. **Fonte oficial:** prazos, andamentos e financeiro vêm do ANERA. Consultar, não copiar para as fichas.
3. **Confirme antes de gravar:** mostrar exatamente o que será gravado e esperar o "sim". Buscar antes de criar.
4. **Prazos:** sempre `anera_calcular_prazo` antes de `anera_criar_prazo`, nunca de cabeça.
5. **Vínculo:** campo `uuid ANERA` nas fichas.
6. **Anotações:** usar os marcadores `[Decisão]`, `[Pendência]`, `[Histórico]`; o servidor acrescenta `IA: ` sozinho.
7. **Arquivos:** o original fica na pasta. Anexar ao ANERA com `anera_link_anexos` + `curl -F`, nunca em base64.
8. **Intimações:** fluxo listar → obter → vincular → calcular → `anera_criar_prazo` com `publicacao_uuid` → marcar lida. Cada gravação com confirmação.
9. **Etiqueta IA:** o que o Claude cria aguarda **Validar** pelo advogado no ANERA. O Claude nunca valida o próprio trabalho; lembrar de validar.
10. **Honorários:** após o contrato, `anera_definir_honorarios`. **Atendimentos:** casos não judicializados; ao ajuizar, arquivar o atendimento e cadastrar o processo.
11. **Modelos:** vêm por `anera_link_modelos` (ver `/anera:configurar-escritorio modelos`). São de uso do escritório: não enviar a terceiros.

## Links e sigilo
- **Links para arquivos:** caminho relativo à raiz do escritório, com **cada espaço como `%20`** no endereço (o formato `< >` não funciona). O texto visível pode ter espaços.
- **Sigilo:** dados de clientes são sigilosos e dados de saúde são sensíveis.
  - Nunca enviar dados, documentos ou trechos de autos a sites ou serviços externos sem pedido expresso. O ANERA é o sistema do próprio escritório.
  - Na web, pesquisar só com termos jurídicos genéricos.
