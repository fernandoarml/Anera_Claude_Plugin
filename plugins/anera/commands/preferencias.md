---
description: Mostra, inclui ou remove preferências do escritório (padrões que valem sobre o plugin e sobrevivem às atualizações) e registra sugestões de melhoria do plugin
argument-hint: "[nova preferência em texto livre | remover <item> | sugerir <melhoria>] — ou nada para listar"
---
Preferências do escritório: $ARGUMENTS

As preferências ficam em `CLAUDE.md` › **Preferências do escritório**: são do escritório e **não são alteradas por atualizações do plugin**. Nunca edite arquivos do plugin.

**Sem argumento — listar:** mostre as preferências atuais agrupadas (Geral e por comando) e dê 3 exemplos do que dá para ajustar (ex.: "no contrato, sempre gerar também o PDF da procuração assinável", "nas peças, usar 'Excelentíssimo(a)' no endereçamento", "no painel, mostrar 15 dias").

**Nova preferência:**
1. Entenda o pedido e identifique onde ele vale: Geral ou um comando específico.
2. Se conflitar com uma preferência existente, mostre as duas e pergunte qual fica.
3. Se tocar em regra de segurança (sigilo, confirmação antes de gravar no ANERA, jurisprudência verificável), explique que essas regras não podem ser afrouxadas e proponha uma alternativa.
4. Mostre a linha exata, no formato `- AAAA-MM-DD: <preferência>`, com a subseção de destino, e grave só depois do "sim". Crie a subseção do comando se ainda não existir.
5. Se a melhoria servir a qualquer escritório, ofereça registrá-la também como sugestão (abaixo).

**remover / alterar:** mostre o item, confirme e edite a linha. Itens removidos não precisam de histórico.

**sugerir:** acrescente em `06_PROCEDIMENTOS/SUGESTOES-PLUGIN.md` (crie a partir de `${CLAUDE_PLUGIN_ROOT}/templates/SUGESTOES-PLUGIN.md` se não existir) uma linha com data, comando, sugestão e motivo, **sem nenhum dado de cliente**. Lembre que o arquivo pode ser enviado ao ANERA como retorno.
