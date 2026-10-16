# Modelos de procuração e declaração

| Modelo | Uso |
|---|---|
| **A – novas ações** | Ações em geral (indenizatórias etc.), com poderes judiciais e a fórmula discreta "podendo agir em juízo ou fora dele". |
| **B – INSS** | Representação administrativa perante o INSS (inclusive Meu INSS) e o CRPS, e ações judiciais contra o INSS (inclusive Juizados Especiais Federais). |
| **C – defesa em processo** | Defesa em processo já ajuizado, com o número do processo, juízo e parte contrária. |
| **D – seguros** | Igual à A + representação perante **seguradoras e outras pessoas jurídicas e órgãos públicos ou privados**, restrita aos assuntos das demandas objeto do mandato. |

Status: **modelos de referência do ANERA** (versão em `03_MODELOS/_versao-modelos.json`) — revisar e aprovar antes do primeiro uso. Arquivos para uso, nesta pasta, em Word e PDF: `procuracao-A-novas-acoes`, `procuracao-B-inss`, `procuracao-C-defesa-processo`, `procuracao-D-seguros`. Versões anteriores ficam em `_historico/`. Uma página cada, timbrado oficial, Century Gothic, espaço ampliado para assinatura digital.

## Poderes especiais (art. 105 do CPC) — todos os modelos
- desistir, transigir, firmar acordos e compromissos e renunciar ao direito sobre o qual se funda a ação;
- receber valores e dar quitação, inclusive **requerer, levantar, receber e sacar alvarás judiciais**, por transferência eletrônica para conta do advogado, e valores de RPV e precatórios;
- assinar declaração de hipossuficiência econômica;
- **B:** também renunciar aos valores que excederem o limite de alçada dos Juizados Especiais Federais.

O modelo B **não** inclui poder para receber o benefício mensal do cliente junto ao INSS (apenas valores judiciais).

**Excluídos de propósito nos modelos de referência:** receber citação, confessar e reconhecer a procedência do pedido. Também foi retirada a representação extrajudicial ampla (pessoas físicas/jurídicas, órgãos reguladores, recursos administrativos), por abrir margem a questionamentos.

## Campos a preencher
- Todos: `{{NOME_OUTORGANTE}}`, `{{NACIONALIDADE}}`, `{{ESTADO_CIVIL}}`, `{{PROFISSAO}}`, `{{CPF}}`, `{{RG}}`, `{{ENDERECO_COMPLETO}}`, `{{CEP}}`, `{{CIDADE}}`, `{{UF}}` (cidade do outorgante, onde assina).
- C: `{{NUMERO_PROCESSO}}`, `{{JUIZO}}` (ex.: "a 2ª Vara Cível da Comarca de Campinas/SP"), `{{PARTE_CONTRARIA}}`.

## Declaração de hipossuficiência econômica
Arquivo: `declaracao-hipossuficiencia` (Word e PDF). **Documento branco, sem timbrado, Arial 12**, uma página.
- Base legal atualizada: art. 5º, LXXIV, da CF e arts. 98 e 99 do CPC (a Lei 1.060/50, art. 4º, foi revogada pelo CPC/2015).
- Campos: `{{NOME_DECLARANTE}}`, `{{NACIONALIDADE}}`, `{{ESTADO_CIVIL}}`, `{{PROFISSAO}}`, `{{NATURALIDADE}}`, `{{CPF}}`, `{{RG}}`, `{{ENDERECO_COMPLETO}}`, `{{CEP}}`, `{{CIDADE}}`, `{{UF}}`.

## Para alterar os modelos
Peça ao Claude o ajuste; ele gera a nova versão para revisão e, aprovada, substitui o modelo (a anterior vai para `_historico/`).
