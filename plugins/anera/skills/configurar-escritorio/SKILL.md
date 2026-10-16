---
name: configurar-escritorio
description: Configuração guiada do escritório no plugin ANERA — cria a estrutura de pastas, coleta os dados do advogado e do escritório, recebe o timbrado e os modelos do escritório, instala contratos e procurações personalizados e conecta o ANERA. Use no primeiro uso do plugin numa pasta, quando o usuário pedir para configurar, reconfigurar, trocar timbrado, atualizar dados do escritório ou incluir modelos.
argument-hint: "[parte específica: dados | timbrado | modelos | anera | estrutura | migrar]"
---
# Configurar o escritório

Conduza a configuração **em etapas curtas, uma de cada vez**, em português, com tom acolhedor e objetivo. Mostre no início o roteiro (as 7 etapas abaixo) e, a cada etapa concluída, um ✅. Se o usuário pedir só uma parte (`$ARGUMENTS`), vá direto a ela.

Arquivos do plugin: `${CLAUDE_PLUGIN_ROOT}` (scripts em `scripts/`, fichas e textos-base em `templates/`, base neutra em `modelos/_base/`, manual em `docs/`). Os modelos de contrato, procuração e declaração **não vêm no plugin**: são baixados pelo conector do ANERA na etapa 6.

**Regras gerais:**
- **Camadas:** o que vem do plugin (regras-base, comandos, scripts) é atualizado com ele e **nunca é editado**; o que é do escritório (`CLAUDE.md`, `.claude/escritorio.json`, `03_MODELOS/`, fichas) fica na pasta e nenhuma atualização mexe. Ajustes de padrão vão para `CLAUDE.md` › Preferências do escritório (`/anera:preferencias`).
- **Nunca apagar nem sobrescrever** nada que já exista na pasta. Se já houver estrutura, `CLAUDE.md` ou modelos, mostre o que existe e pergunte antes de mudar (versão anterior vai para `_historico/`).
- Dados pessoais e de clientes nunca saem do computador, exceto para o ANERA, com a autorização do usuário.
- Requisitos: **Python 3** (scripts) e, para gerar PDF, **Microsoft Word**. Verifique no início (`python --version`); se faltar o Python, explique como instalar e continue o que for possível.

## Etapa 1 — Boas-vindas e diagnóstico
- Explique em 3 linhas o que o plugin faz e que a configuração leva cerca de 10 minutos.
- Verifique: existe `.claude/escritorio.json`? existe `01_CLIENTES/`? o ANERA está conectado (`anera_status`)?
- Mostre um quadro "o que já está pronto / o que falta".

## Etapa 2 — Conectar o ANERA (recomendado fortemente)
- Explique o ganho em linguagem simples: com o ANERA, o Claude **consulta prazos, intimações e andamentos, preenche contratos com o cadastro do cliente e registra anotações e prazos no sistema** — sempre pedindo confirmação, sem excluir nada, com tudo auditado e marcado com a etiqueta **IA** para validação. É também pelo ANERA que chegam os **modelos prontos de contrato, procuração e declaração** (etapa 6).
- Se `anera_status` não responder: oriente digitar `/mcp`, escolher **anera**, autenticar (login do ANERA → tela de permissões) e marcar as permissões: leitura, anotações, prazos, publicações, cadastro e financeiro. Depois peça para avisar e teste com `anera_status`.
- Se o usuário não tiver ANERA, siga normalmente (o plugin funciona só com a pasta, com os modelos próprios do escritório) e diga em uma linha como contratar/ativar depois.
- Com o ANERA conectado, use `anera_listar_responsaveis` para **pré-preencher** nome e OAB do advogado na etapa 3.

## Etapa 3 — Dados do escritório
Pergunte (em blocos, mostrando o que já foi pré-preenchido):
- **Advogado responsável:** nome completo, OAB (UF e número), CPF.
- **Escritório:** nome, endereço, cidade/UF, CEP, e-mail oficial, site.
- **Telefones oficiais** (1 a 3): são os números que aparecerão no **quadro antigolpe** dos contratos — o cliente será orientado a desconfiar de qualquer outro número.
- **Áreas de atuação** e uma sigla curta para cada (ex.: Previdenciário → `PREV`; Cível → `CIVEL`; seguros → `SEG-VIDA`, `SEG-VEIC`...).
- **Cor principal** dos contratos (padrão azul-marinho `16304D`; ofereça usar a cor predominante do timbrado).
Grave em `.claude/escritorio.json` no formato de `${CLAUDE_PLUGIN_ROOT}/templates/escritorio.exemplo.json`. Mostre o resumo e peça confirmação.

## Etapa 4 — Estrutura de pastas e regras
- Crie (sem apagar nada): `00_INTEGRACOES/` (só com o `LEIA-ME.md` de `templates/LEIA-ME-integracoes.md` — endereço do conector e como conectar; nada além do necessário para usar o ANERA), `01_CLIENTES/` (com `_INDICE.md` de `templates/INDICE-CLIENTES.md`), `02_ESTRATEGICO/<area>/` para cada área (com `_INDICE.md` de `templates/INDICE-TESES.md`), `03_MODELOS/_base/`, `03_MODELOS/pecas/<area>/`, `03_MODELOS/contratos/`, `03_MODELOS/procuracoes/`, `04_PESQUISA/` (`jurisprudencia/<area>/`, `legislacao/`, `doutrina/`, `pecas-referencia/`), `05_ADMINISTRATIVO/`, `06_PROCEDIMENTOS/`, `99_ARQUIVO/clientes/`.
- Gere o `CLAUDE.md` do escritório a partir de `${CLAUDE_PLUGIN_ROOT}/templates/CLAUDE.template.md`, substituindo os campos `{{...}}` (nome do escritório, advogado, OAB, tabela de áreas). Ele é **enxuto de propósito**: as regras gerais vêm do plugin em toda sessão (`regras/REGRAS-BASE.md`) e se atualizam sozinhas; o `CLAUDE.md` guarda só áreas, padrões e **Preferências do escritório**. Se já existir um `CLAUDE.md`, **não substitua**: siga a parte **migrar** abaixo.
- Crie `06_PROCEDIMENTOS/SUGESTOES-PLUGIN.md` a partir de `templates/SUGESTOES-PLUGIN.md`.
- Copie `templates/CLIENTE.md`, `PROCESSO.md` e `TESE.md` para `.claude/templates/` (o comando `/anera:novo-cliente` usa a versão do plugin se não houver cópia local).
- Copie `${CLAUDE_PLUGIN_ROOT}/docs/COMO-USAR.md` para `06_PROCEDIMENTOS/`.

## Etapa 5 — Timbrado e modelo de formatação (peça o arquivo ao usuário)
Peça, explicando para que serve cada um:
1. **Timbrado** — "um documento Word **em branco** com o cabeçalho e o rodapé do escritório (logo, endereço, contatos)". Será a base de todo documento gerado.
2. **Modelo de formatação de peças** — "uma petição sua já pronta, de preferência uma inicial, que mostre a fonte, o espaçamento, os títulos e as citações que você usa".

Como entregar: **arrastar o arquivo para o chat** ou salvar numa pasta e informar o caminho. Ao receber:
- **Timbrado:** copie para `03_MODELOS/_base/timbrado.docx`. Confira se tem cabeçalho/rodapé; se vier com texto no corpo, avise e pergunte se pode usar só cabeçalho/rodapé.
- **Peça de formatação:** **anonimize** (nomes, CPF, RG, endereços, números de processo, apólices, valores, dados de saúde, inclusive metadados e links internos do arquivo — confira tudo com uma varredura) e salve como `03_MODELOS/_base/padrao-formatacao-pecas.docx`. Extraia o padrão (fonte, tamanho, alinhamento, entrelinhas, recuo, títulos, citações, listas, fecho) e grave `03_MODELOS/_base/PADRAO-FORMATACAO.md`. Mostre o padrão extraído e peça confirmação.
- Sem timbrado: os documentos saem em página branca (dá para incluir depois com `/anera:configurar-escritorio timbrado`).

## Etapa 6 — Modelos de contrato, procuração e declaração (pelo ANERA)
- **Sem ANERA conectado** (ou sem as ferramentas `anera_listar_modelos`/`anera_link_modelos`, em servidor anterior à 1.6.0): explique em duas linhas que os modelos prontos vêm pelo conector do ANERA, para assinantes, e siga para a etapa 7 (modelos próprios). Não procure modelos em outro lugar.
- **Com ANERA:** chame `anera_listar_modelos`. Se `disponivel` for `false`, mostre o `motivo` e siga para a etapa 7.
- **Sugira os modelos do ANERA** como ponto de partida: vêm **sem dados de nenhum escritório e sem timbrado** e recebem os dados e o timbrado deste escritório na instalação, no próprio computador. Mostre o que vem pronto (abaixo) e pergunte: usar os modelos do ANERA, trazer os do escritório (etapa 7) ou os dois (instalar os do ANERA e comparar com os próprios).
- Se o usuário aceitar:
  1. `anera_link_modelos` (todos, ou `ids` escolhidos). O link vale 15 minutos e serve uma vez.
  2. Baixe direto para o disco, sem passar o conteúdo pela conversa: `curl -fsSL -o .claude/modelos-anera.zip "<url>"`.
  3. Confira o `sha256` devolvido pela ferramenta: `python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" .claude/modelos-anera.zip`. Se não conferir, apague o arquivo, avise e peça um link novo.
  4. Instale com os dados e o timbrado do escritório:
     `python "${CLAUDE_PLUGIN_ROOT}/scripts/instalar_modelos.py" --origem .claude/modelos-anera.zip --config .claude/escritorio.json --destino 03_MODELOS --timbrado 03_MODELOS/_base/timbrado.docx --pdf`
     (sem timbrado, omita `--timbrado`; para reinstalar depois de mudar dados ou receber versão nova, acrescente `--substituir`). O instalador confere cada arquivo pelo manifesto do pacote e não instala nada se algum não conferir.
     **Modelos que o escritório alterou** são mantidos: a versão nova sai ao lado como `<nome>_novo-<versao>.docx`. Para cada um, mostre as diferenças de texto e pergunte: manter o do escritório (apague o `_novo`), adotar o novo (rode de novo com `--substituir --incluir-alterados`; o anterior vai para `_historico/`) ou juntar os dois (proponha a versão combinada e grave como modelo do escritório depois do "sim").
  5. Apague `.claude/modelos-anera.zip`. A versão instalada fica registrada em `03_MODELOS/_versao-modelos.json`.
- **Modelos novos no ANERA:** se a `versao_pacote` de `anera_listar_modelos` for maior que a de `03_MODELOS/_versao-modelos.json`, ofereça atualizar (mesmo fluxo, com `--substituir`; as versões anteriores vão para `_historico/`).
- Os modelos são de uso do escritório assinante (ver `${CLAUDE_PLUGIN_ROOT}/TERMOS-DE-USO.md`): não os envie a terceiros nem os copie para fora de `03_MODELOS/`.
- Copie `templates/LEIA-ME-contratos.md` e `templates/LEIA-ME-procuracoes.md` para as pastas correspondentes, preenchendo o nome do advogado.
- **Explique o que vem pronto:** 5 contratos (autor: entrada + êxito, só êxito, valor fixo; defesa: entrada + êxito, valor fixo), 4 procurações (novas ações, INSS, defesa em processo, seguros) e a declaração de hipossuficiência — com legal design, quadro antigolpe e regras de desistência.
- **Deixe claro:** as regras comerciais dos contratos (percentuais por fase, multas em salários mínimos, prazos de repasse, renúncia) são **padrões de referência**; o conteúdo jurídico e comercial é de responsabilidade do escritório e deve ser revisado. Ofereça revisar juntos agora ou depois.
- Abra (link) um contrato em PDF para o usuário ver o resultado.

## Etapa 7 — Seus próprios modelos (guie o usuário a entregar)
Explique que o Claude escreve **no estilo do escritório** quando tem peças próprias como referência, e peça, por área de atuação:
- **Peças que o escritório já usa e aprova:** iniciais, contestações, réplicas, recursos, petições simples (juntada, cumprimento). Sugira começar com 2 ou 3 das mais frequentes.
- **Contrato e procuração próprios**, se o escritório preferir os seus: o Claude compara com os modelos do plugin, aponta lacunas (ex.: base de cálculo do êxito, desistência, repasse, LGPD, antigolpe) e propõe uma versão.
- **Outros documentos recorrentes:** notificações extrajudiciais, declarações, substabelecimentos.
Para cada arquivo recebido: **anonimize** (como na etapa 5), salve em `03_MODELOS/pecas/<area>/` com nome `tipo_assunto.docx` (ex.: `inicial_negativa-seguro-vida.docx`), e registre no índice da pasta. Peças de **outros escritórios** vão para `04_PESQUISA/pecas-referencia/` (servem de argumento, não de estilo). Diga que dá para mandar mais modelos a qualquer momento com `/anera:configurar-escritorio modelos`.

## Parte `migrar` — CLAUDE.md de formato anterior
Use quando o `CLAUDE.md` não tiver a marca `anera:claude-md v2`, ou seja, quando ele repete regras gerais que agora vêm do plugin.
1. Guarde uma cópia em `.claude/_historico/CLAUDE-AAAA-MM-DD.md`.
2. Separe o conteúdo em dois grupos:
   - **regras gerais**, iguais ou equivalentes a `${CLAUDE_PLUGIN_ROOT}/regras/REGRAS-BASE.md`. Saem do arquivo;
   - **o que é do escritório**: áreas, padrões próprios, exceções e regras que o escritório acrescentou. Fica.
3. Na dúvida, o trecho **fica**, em "Padrões do escritório".
4. Monte o novo `CLAUDE.md` no formato do template, com o que é do escritório em "Padrões do escritório" ou "Preferências do escritório".
5. Mostre ao usuário as duas listas e o novo arquivo, e grave só depois do "sim".
6. Avise que vale a partir da próxima sessão.

## Encerramento
- Mostre o checklist final (✅/⬜) e os links para `CLAUDE.md`, `.claude/escritorio.json`, os modelos e o manual.
- Sugira os **primeiros passos**: `/anera:buscar <nome de um cliente>` (com o ANERA, cria a pasta do cliente automaticamente), `/anera:painel` e `/anera:ajuda`.
- Explique em uma frase que o escritório pode ajustar o jeito de trabalhar a qualquer momento ("a partir de agora, faça…" ou `/anera:preferencias`), e que esses ajustes **não se perdem** nas atualizações do plugin.
- Avise que as mudanças no `CLAUDE.md` valem a partir da **próxima sessão**.
