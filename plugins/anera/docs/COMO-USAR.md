# Como usar o plugin ANERA no Claude

Manual do dia a dia. Para um tour guiado: `/anera:ajuda`.

## 1. Instalar e configurar (uma vez)
1. No Claude Code, adicione o marketplace do ANERA e instale o plugin `anera` (comandos em `README.md` do marketplace).
2. Abra uma **sessão nova** na pasta que será o escritório (pode ser uma pasta vazia, ou sincronizada com o OneDrive/Google Drive em modo "espelhar").
3. Rode **`/anera:configurar-escritorio`**. Em cerca de 10 minutos o Claude:
   - conecta o ANERA (recomendado);
   - pergunta os dados do advogado e do escritório, inclusive os **telefones oficiais** (usados no quadro antigolpe);
   - cria as pastas e o `CLAUDE.md` com as regras do escritório;
   - recebe o **timbrado** e uma **petição sua** para aprender a formatação;
   - instala contratos, procurações e a declaração de hipossuficiência personalizados;
   - pede suas **peças-modelo** para escrever no estilo do escritório.

## 2. Conectar o ANERA
`/mcp` → **anera** → autenticar → login no ANERA → marcar as permissões (leitura, anotações, prazos, publicações, cadastro, financeiro).
Com o ANERA, o Claude consulta **prazos, intimações e andamentos**, preenche documentos com o **cadastro** e registra **anotações, prazos e honorários** — sempre com sua confirmação, sem excluir nada, com etiqueta **IA** para você validar.
Desconectar: ANERA › Configurações › Integrações com IA.

## 3. Comandos
| Comando | O que faz |
|---|---|
| `/anera:ajuda [dúvida]` | Tutorial, seu progresso e respostas a dúvidas |
| `/anera:configurar-escritorio [parte]` | Configuração completa ou só uma parte: `dados`, `timbrado`, `modelos`, `anera`, `estrutura`, `migrar` |
| `/anera:preferencias [texto]` | Lista, inclui ou remove preferências do escritório (valem sobre o padrão do plugin e não se perdem nas atualizações); `sugerir` registra ideias para o ANERA |
| `/anera:buscar <termo>` | Acha cliente/caso na pasta e no ANERA; se só existir no ANERA, cria a pasta e as fichas |
| `/anera:novo-cliente <nome>` | Cria cliente (pasta + ficha + cadastro no ANERA) |
| `/anera:novo-processo ...` | Cria caso (pasta + ficha + processo/atendimento no ANERA) |
| `/anera:documentos-cliente <cliente> <caso>` | Contrato, procuração e declaração preenchidos (Word + PDF) |
| `/anera:peca <tipo> <cliente> <caso>` | Rascunho de peça no padrão do escritório |
| `/anera:preparar-documentos <cliente> <caso>` | Pasta de protocolo numerada (00_peça, 01_procuração... doc_1, doc_2...) |
| `/anera:registrar` | Grava na ficha (e no ANERA) o que foi feito e decidido |
| `/anera:painel` | Prazos atrasados/hoje/semana e intimações não lidas |
| `/anera:novidades` | Trata intimações e andamentos novos, com prazo calculado pelo ANERA |
| `/anera:nova-tese` · `/anera:arquivar` | Teses do escritório · encerrar casos |

Também dá para pedir em conversa: "gere o contrato da Maria, modelo A, entrada de R$ 1.500 e 20%".

## 4. Rotina sugerida
- **Ao começar o dia:** `/anera:painel`.
- **Chegou intimação:** `/anera:novidades`.
- **Cliente novo:** `/anera:buscar <nome>` (ou `/anera:novo-cliente`) → `/anera:documentos-cliente`.
- **Peça:** `/anera:peca` → revisar → `/anera:preparar-documentos` → protocolar.
- **Ao fechar a sessão:** `/anera:registrar`.
- **No ANERA:** validar o que tiver a etiqueta **IA**.

## 5. Onde fica cada coisa
```
ESCRITÓRIO/
├── CLAUDE.md               ← regras do escritório (o Claude lê sozinho)
├── .claude/escritorio.json ← dados do escritório
├── 01_CLIENTES/            ← um cliente por pasta; um caso por subpasta (índice em _INDICE.md)
├── 02_ESTRATEGICO/         ← teses do escritório
├── 03_MODELOS/             ← timbrado, padrão de formatação, contratos, procurações, peças próprias
├── 04_PESQUISA/            ← jurisprudência, legislação, peças de terceiros
├── 06_PROCEDIMENTOS/       ← este manual
└── 99_ARQUIVO/             ← clientes encerrados
```

## 6. Regras de ouro
1. **Revise sempre** — tudo que o Claude produz é rascunho até sua revisão.
2. **Prazos:** o Claude calcula com a calculadora do ANERA, mas o controle é seu — valide.
3. **Sigilo:** o Claude não envia dados de clientes a sites ou serviços externos sem pedido expresso.
4. **Versões não se sobrescrevem** (`_v2`, `_v3`...).
5. **Registre antes de sair** (`/anera:registrar`).

## 7. Privacidade
O plugin acessa os dados do seu escritório no ANERA pelo conector oficial, com as permissões que você escolheu ao conectar. O conteúdo que o Claude lê (fichas, documentos da pasta e dados do ANERA) é processado pela Anthropic conforme o plano que você contratou: confira as configurações de privacidade e de uso de dados da sua conta. O ANERA não recebe os arquivos da sua pasta (só anexos que você autorizar). Nenhuma ferramenta do conector exclui registros, e toda gravação feita pelo Claude fica registrada no histórico do ANERA. Você pode desconectar a qualquer momento em **Configurações › Integrações com IA**.

## 8. Requisitos
- Claude Code (aplicativo desktop ou terminal), versão 2.1.224 ou mais recente.
- **ANERA** com o conector autorizado, para os modelos de contrato e procuração e para prazos, intimações e cadastro.
- **Git** (o Claude Code usa para baixar e atualizar o plugin; no Windows, instale o Git for Windows).
- **Python 3** (para preencher modelos e montar protocolos).
- **Microsoft Word** (para gerar PDF; sem ele, os documentos saem só em Word).
