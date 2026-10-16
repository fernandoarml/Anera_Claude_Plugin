# Modelos de contrato de honorários

Modelos-base com cláusulas comuns idênticas; mudam a cláusula 2 (honorários), o objeto (autor ou réu) e os trechos que dependem deles (resumo, acordos e desistência). Os modelos-base atendem bem **seguros e indenizatórias**; outros nichos terão adaptações próprias (ver "Próximos modelos").

| Modelo | Honorários | Uso típico |
|---|---|---|
| **A – entrada + êxito** | Entrada + `{{PERCENTUAL_EXITO}}`% do proveito econômico | Entrada + 20% ou entrada + 30% |
| **B – êxito** | `{{PERCENTUAL_EXITO}}`% do proveito econômico, sem entrada | 30% no final |
| **C – valor fixo** | Valor fixo à vista ou parcelado | Casos sem proveito econômico mensurável |
| **D – defesa: entrada + êxito** | Entrada + `{{PERCENTUAL_EXITO}}`% do proveito econômico da defesa | Cliente réu em ação já ajuizada |
| **E – defesa: valor fixo** | Valor fixo à vista ou parcelado | Cliente réu em ação já ajuizada |

Status: **modelos de referência do ANERA** (versão em `03_MODELOS/_versao-modelos.json`) — revisar e aprovar antes do primeiro uso. Arquivos para uso, nesta pasta, em Word e PDF:
- `contrato-honorarios-A-entrada-exito` · `contrato-honorarios-B-exito` · `contrato-honorarios-C-valor-fixo`
- `contrato-honorarios-D-defesa-entrada-exito` · `contrato-honorarios-E-defesa-valor-fixo`

Versões anteriores ficam em `_historico/`.

Formato: legal design — máximo de 5 páginas (hoje todos com 5), resumo no topo, cláusulas com ícones, partes chamadas de CLIENTE e ADVOGADO, tabela de desistência e quadro de alerta contra golpes. Cores do timbrado (azul #16304D).

## Regras fixas (decididas pelo escritório)
- Contratação em nome de **{{ADVOGADO_NOME}}** (dados em `.claude/escritorio.json`).
- Abrangência: fase administrativa + judicial até o trânsito em julgado, com recursos e cumprimento de sentença. Sustentação oral nos tribunais superiores: negociada à parte.
- Mesmo percentual de êxito na fase administrativa e na judicial (sem desconto).
- Proveito econômico inclui o que o cliente **recebe** e o que **deixa de pagar** (ex.: declaratória de inexistência de débito).
- Entrada não é devolvida: remunera o trabalho integralmente feito antes do ajuizamento (estudo do caso, análise documental, pesquisa, estratégia e preparação do processo). Única exceção: renúncia do advogado sem justo motivo antes do ajuizamento (cláusula 8.9).
- Repasse ao cliente e pagamento de honorários recebidos diretamente pelo cliente: até 3 dias úteis.
- Sem cláusula de desistência livre em 7 dias.
- Foro: **domicílio do cliente**.
- **Renúncia do advogado** (cláusula 8.9): antes do ajuizamento e sem motivo, o advogado **devolve a entrada** (modelo A) ou os valores recebidos (modelo C); se motivada (ex.: atraso no pagamento), não devolve. Depois do ajuizamento, percentuais da tabela. Comunicação por e-mail ou aplicativo de mensagens basta com prova de envio; sem confirmação de leitura, ciência presumida 5 dias após o envio (8.10). Os 10 dias legais de representação contam da ciência.
- **Informação falsa, omissão relevante ou depoimento divergente** do relato inicial (cláusula 6.2): o advogado pode rescindir de imediato (observados os 10 dias legais de representação). Devidos 100% dos honorários de êxito sobre o **valor da causa**; no modelo C, 100% dos honorários fixos com vencimento antecipado.

### Encerramento antecipado pelo cliente (revogação ou encerramento sem justa causa)
Redação neutra: a cláusula 8 começa por "Se o CLIENTE revogar a procuração ou encerrar o contrato...", sem afirmar que ele pode sair a qualquer tempo (para não induzir).

**Antes de entrar com a ação** não há honorários de êxito nem de sucumbência:
- **Modelo A (com entrada):** o cliente perde apenas a entrada, que não é devolvida (remunera estudo do caso, análise documental e preparação do processo).
- **Modelo B (sem entrada):** multa fixa = 5 salários mínimos (escrita em reais), paga em 10 dias.
- **Modelo C (valor fixo):** multa fixa = 5 salários mínimos (em reais), descontados os valores já pagos, que não são devolvidos.

**Depois do ajuizamento:**

| Fase na data da desistência | Êxito (ou honorários fixos no modelo C) | Sucumbência |
|---|---|---|
| Ajuizada, antes do encerramento da instrução | 60% | 60% |
| Após a instrução, antes da sentença | 75% | 75% |
| Após a sentença | 100% | 100% |

- Êxito: percentual da tabela × honorários de êxito × proveito econômico (valor atualizado da condenação ou do acordo).
- Sucumbência: percentual da tabela × valor integral da sucumbência fixada no processo; devida quando fixada e exigível. Divisão diferente fixada pelo juízo → o cliente indeniza a diferença.
- Vencimento: êxito e sucumbência após o trânsito em julgado ou acordo, conforme o cliente receber. Multa fixa e honorários fixos (modelo C): 10 dias.
- O advogado pode juntar o contrato aos autos para destaque mesmo após o encerramento, como terceiro interessado.
- **Desistência do processo** (extinção sem resolução de mérito): pedido por escrito ao advogado, que protocola. Honorários pelos mesmos percentuais da tabela, mas sobre o **valor da causa** (soma dos pedidos); vencem em 10 dias da homologação. Cliente é avisado do risco de pagar custas e honorários à parte contrária (art. 90 do CPC). No modelo C: percentuais da tabela sobre os honorários fixos.

### Segurança e canais oficiais (cláusula 11)
- Resumo do topo: linha **SEGURANÇA** em destaque amarelo, com os telefones oficiais e o aviso de leitura obrigatória da cláusula 11.
- 11.1: declaração do cliente de que leu e compreendeu a cláusula 11 (leitura obrigatória).
- Quadro de alerta (redação neutra: golpistas podem se passar por membros da Justiça ou pelo escritório): o escritório **nunca** faz cobranças para liberação de valores ou alvarás, nem pede senhas/códigos/dados bancários. Boletos de honorários e custas **são** enviados por mensagem, por isso não há proibição de boletos/links.
- **Confirmação por ligação feita pelo próprio cliente** (spoofing só afeta chamadas e mensagens recebidas).
- Pagamentos ao advogado só valem para conta **de titularidade do advogado** (conta não indicada no contrato, por decisão do escritório); pagamento a terceiro não quita.
- Repasses só para conta de titularidade do cliente.
- Responsabilidade afastada por culpa exclusiva de terceiro/titular (art. 43, III, LGPD).
- **Sem palavra de segurança** (decisão do escritório: risco de vazamento). Atenção: nada sigiloso deve constar no contrato, pois ele pode ser juntado aos autos.
- **Pendente:** cartilha de segurança (1 página, legal design) para entregar junto com o contrato.

### Modelos de defesa (D e E)
- Objeto: contestação, reconvenção e pedido contraposto (incluídos), acompanhamento até o trânsito em julgado, recursos, cumprimento de sentença e acordo. Sem fase extrajudicial.
- **Prazo da defesa (1.3):** cliente entrega documentos imediatamente; advogado não responde por contratação com prazo reduzido ou atraso do cliente, inclusive revelia.
- **Proveito econômico (D):** valor pedido pelo autor (valor atualizado da causa) − condenação final ou acordo (improcedência = valor integral pedido) + o que o cliente receber em reconvenção/pedido contraposto.
- Acordo (D): êxito sobre a economia obtida (pedido − valor acordado).
- Desistência: marco é a **apresentação da contestação** (não o ajuizamento).
  - **D:** antes da contestação, perde só a entrada; depois, tabela 60/75/100% para êxito e sucumbência.
  - **E:** antes da contestação, **multa fixa de 7 salários mínimos** (em reais), descontado o que já pagou; depois, **valor integral** dos honorários fixos (sem percentuais) + sucumbência pela tabela 60/75/100%.
  - Renúncia do advogado após a contestação no E: honorários fixos **proporcionais** (60/75/100%), por boa-fé.
- Sem a subcláusula de "desistência do processo" (não se aplica ao réu): numeração da cláusula 8 vai até 8.9 (renúncia = 8.8; comunicação = 8.9; divisão da sucumbência = 8.4).

## Próximos modelos
- **Possessórias (reintegração de posse):** modelos próprios para **autor** e **réu**, nas versões valor fixo e entrada + êxito de 5% ou 10% **sobre o valor atualizado do imóvel (IPCA)**, fixado desde logo no contrato; cláusulas de conservação do bem e de não alteração das características do imóvel.
- Demais nichos (previdenciário, trabalhista, família): a construir a partir dos modelos-base.

## Campos a preencher
- Todos: `{{NOME_CONTRATANTE}}`, `{{NACIONALIDADE}}`, `{{ESTADO_CIVIL}}`, `{{PROFISSAO}}`, `{{CPF}}`, `{{RG}}`, `{{ENDERECO_COMPLETO}}`, `{{CEP}}`, `{{TELEFONE}}`, `{{EMAIL}}`, `{{DESCRICAO_DO_CASO}}`, `{{PARTE_CONTRARIA}}`.
- B e C: `{{VALOR_MULTA_PRE_ACAO}}` e `{{VALOR_MULTA_PRE_ACAO_EXTENSO}}` = **5 × salário mínimo vigente na data do contrato**. Confirmar o valor do salário mínimo sempre que gerar um contrato novo e escrever o valor em reais (nunca "salários mínimos").
- A e B: `{{PERCENTUAL_EXITO}}` e `{{PERCENTUAL_EXITO_EXTENSO}}`.
- A: `{{VALOR_ENTRADA}}`, `{{VALOR_ENTRADA_EXTENSO}}`, `{{FORMA_PAGAMENTO_ENTRADA}}`.
- C e E: `{{VALOR_TOTAL}}`, `{{VALOR_TOTAL_EXTENSO}}`, `{{FORMA_PAGAMENTO}}`.
- D: mesmos campos do A (entrada e êxito).
- E: `{{VALOR_MULTA_PRE_CONTESTACAO}}` e `{{VALOR_MULTA_PRE_CONTESTACAO_EXTENSO}}` = **7 × salário mínimo vigente** (confirmar a cada contrato; escrever em reais).
- D e E: `{{NUMERO_PROCESSO}}`; `{{DESCRICAO_DO_CASO}}` completa "na ação ___" (ex.: "de indenização por danos morais").

`{{DESCRICAO_DO_CASO}}` completa a frase "para a defesa de seus interesses ___". Exemplos:
- "relativos à negativa de cobertura do sinistro nº ___, referente ao seguro de vida (apólice nº ___)"
- "na ação de reintegração de posse do imóvel situado na ___"
- "na ação declaratória de inexistência do débito de R$ ___ cobrado por ___"

## Para alterar os modelos
- Ajustes de texto: peça ao Claude (ex.: "no modelo A, troque a multa de atraso para 2%"). Ele gera a nova versão, mostra para revisão e, aprovada, substitui o modelo (a anterior vai para `_historico/`).
- Dados do escritório (telefones, endereço, OAB, timbrado): `/anera:configurar-escritorio dados` e reinstalar os modelos (`/anera:configurar-escritorio modelos`).
