# Perguntas frequentes — plugin ANERA

## Primeiros passos
**O que o plugin faz?**
Transforma uma pasta do computador em um escritório organizado no Claude: uma pasta por cliente e por caso, fichas que funcionam como memória de cada caso, contratos e procurações preenchidos automaticamente, peças no padrão do escritório, montagem dos documentos para protocolo e — com o ANERA — prazos, intimações, andamentos e anotações integrados.

**Por onde começo?**
`/anera:configurar-escritorio`. Depois `/anera:ajuda` mostra seu progresso e o próximo passo.

**Preciso saber programar?**
Não. Tudo é pedido em português, por comando (`/anera:...`) ou em conversa ("gere o contrato da Maria").

**Quais comandos existem?**
| Comando | Para quê |
|---|---|
| `/anera:configurar-escritorio` | Configurar ou ajustar o escritório, timbrado e modelos |
| `/anera:ajuda` | Tutorial e dúvidas |
| `/anera:buscar` | Achar cliente ou caso (pasta + ANERA); cria a pasta se só existir no ANERA |
| `/anera:novo-cliente` · `/anera:novo-processo` | Cadastrar cliente e caso |
| `/anera:documentos-cliente` | Contrato, procuração e declaração preenchidos (Word + PDF) |
| `/anera:peca` | Rascunho de peça no padrão do escritório |
| `/anera:preparar-documentos` | Pasta de protocolo numerada |
| `/anera:registrar` | Gravar na ficha (e no ANERA) o que foi feito e decidido |
| `/anera:painel` | Prazos e intimações do dia/semana (ANERA) |
| `/anera:novidades` | Tratar intimações e andamentos novos (ANERA) |
| `/anera:nova-tese` · `/anera:arquivar` | Teses do escritório; encerrar casos |
| `/anera:preferencias` | Ajustar o jeito de trabalhar do escritório; registrar sugestões |

## ANERA
**Preciso do ANERA?**
O plugin funciona só com a pasta, mas foi feito para trabalhar **junto com o ANERA**. Sem ele, você perde: os **modelos prontos de contrato, procuração e declaração** (vêm pelo conector), painel de prazos, tratamento de intimações com cálculo de prazo, andamentos nas peças, cadastro automático de clientes e casos, honorários e anotações no sistema.

**Como conecto?**
`/mcp` → **anera** → autenticar → login no ANERA → marcar permissões. Para desconectar: ANERA › Configurações › Integrações com IA.

**O Claude pode bagunçar meus dados no ANERA?**
Não sem você ver. Toda gravação é mostrada antes e só acontece com o seu "sim"; **nenhuma ferramenta exclui registros**; tudo fica no histórico com origem "claude"; anotações começam com `IA:`; prazos, processos e atendimentos criados pela IA recebem a etiqueta **IA** até você clicar em **Validar**.

**O Claude calcula prazos?**
Sim, mas **nunca de cabeça**: usa a calculadora do ANERA (CPC, CLT, dias úteis, feriados nacionais e estaduais, recesso). Ainda assim, o controle oficial é seu — confira e valide.

**Apareceu "falta permissão".**
A conexão foi feita sem aquela permissão (ou a permissão é nova). Desconecte no ANERA (Configurações › Integrações com IA) e conecte de novo marcando-a.

## Modelos e documentos
**Posso usar meu próprio timbrado?**
Sim — `/anera:configurar-escritorio timbrado`. Envie um Word em branco com cabeçalho e rodapé.

**Posso usar meus próprios contratos e peças?**
Sim — `/anera:configurar-escritorio modelos`. Peças aprovadas viram referência de estilo (anonimizadas). Seu contrato pode ser comparado com o do ANERA para apontar lacunas.

**De onde vêm os modelos de contrato e procuração?**
Do ANERA, pelo conector: `/anera:configurar-escritorio modelos` baixa o pacote (link temporário, conferido por sha256) e instala com seus dados e seu timbrado, no seu computador. Quando o ANERA publicar modelos novos, o mesmo comando oferece atualizar (as versões anteriores vão para `_historico/`). Os modelos são para uso do seu escritório — não repasse a terceiros.

**As regras dos contratos (percentuais, multas) são obrigatórias?**
Não. São padrões de referência. O conteúdo jurídico e comercial é do escritório — revise e ajuste.

**Onde ficam os documentos gerados?**
Na pasta do caso: `01_CLIENTES/<CLIENTE>/<CASO>/contrato-procuracao/`, `pecas/`, `protocolo-inicial/`. Nada é sobrescrito: cada ajuste gera `_v2`, `_v3`...

**O PDF não foi gerado.**
O PDF é feito pelo Microsoft Word. Verifique se o Word está instalado e se o arquivo não está aberto.

**Como atualizo o plugin?**
Ao abrir a sessão, o plugin avisa quando há versão nova. Para atualizar: `/plugin marketplace update anera-marketplace` e depois `/reload-plugins` (ou abra uma sessão nova). Para não precisar fazer isso: `/plugin` › Marketplaces › anera-marketplace › **Enable auto-update**.

## Personalizar
**Posso mudar o jeito como um comando trabalha?**
Sim. Diga "a partir de agora…" ou use `/anera:preferencias`. O Claude grava a preferência no `CLAUDE.md` do escritório (seção **Preferências do escritório**), que prevalece sobre o padrão do plugin. As regras de segurança são a exceção: sigilo, confirmação antes de gravar no ANERA e jurisprudência verificável.

**Minhas personalizações se perdem quando o plugin atualiza?**
Não. A atualização troca só os arquivos do plugin. Ficam intactos:
- o `CLAUDE.md`;
- as preferências;
- os dados do escritório;
- os modelos em `03_MODELOS/`;
- as fichas.

Se um modelo novo do ANERA chegar e você tiver alterado o seu, o seu é mantido e o novo vem ao lado para comparar.

**Tive uma ideia que serviria para todo mundo.**
`/anera:preferencias sugerir <ideia>`. Ela fica em `06_PROCEDIMENTOS/SUGESTOES-PLUGIN.md`, sem dados de clientes, para enviar ao ANERA.

## Organização
**Como os clientes ficam organizados?**
`01_CLIENTES/NOME COMPLETO - MM-AAAA/` com `CLIENTE.md`, `documentos-pessoais/` e uma pasta por caso (`AREA_PARTE_NUMERO/`), cada uma com `PROCESSO.md`, `contrato-procuracao/`, `documentos-caso/`, `autos/`, `pecas/` e `pesquisa/`. O índice geral é `01_CLIENTES/_INDICE.md`.

**Como o Claude "lembra" de um caso numa conversa nova?**
Pela ficha `PROCESSO.md` (e pelas anotações do ANERA). Use `/anera:registrar` antes de fechar a sessão.

## Privacidade
**Meus dados vão para onde?**
Os arquivos ficam no seu computador. O conteúdo que o Claude lê é processado pela Anthropic conforme o plano contratado (confira as configurações de privacidade da sua conta). O ANERA só recebe o que você autorizar (anotações, prazos, cadastro e, se você quiser, anexos). O Claude não envia dados de clientes a sites ou serviços externos sem pedido expresso.

**E golpes contra meus clientes?**
Os contratos têm um quadro antigolpe com os telefones oficiais do escritório e a regra "na dúvida, ligue você mesmo".

## Problemas comuns
| Situação | Solução |
|---|---|
| Os comandos `/anera:` não aparecem | Confira se o plugin está habilitado (`/plugin`) e abra uma sessão nova |
| "ANERA não conectado" | `/mcp` → anera → autenticar |
| Não consigo mover/renomear uma pasta | Algum arquivo está aberto no Word ou no Explorer |
| Link de arquivo não abre | Peça para refazer o link (espaços viram `%20`) |

**Não resolveu?** Suporte do plugin: **suporte.claude@anera.com.br** ou WhatsApp **(27) 99751-6427**. Mande o comando usado, o que esperava e o que aconteceu, **sem dados de clientes**.
| Sessão longa e lenta | Abra uma sessão nova — o Claude retoma pelas fichas |
