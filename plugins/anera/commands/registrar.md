---
description: Registra na ficha do caso (e no ANERA) o que foi feito e decidido nesta sessão
argument-hint: [cliente / caso] [observação adicional]
---
Registre nas fichas o que foi tratado nesta sessão. $ARGUMENTS

> **Preferências do escritório:** antes de executar, aplique o que estiver em `CLAUDE.md` › Preferências do escritório (Geral e a subseção deste comando); elas prevalecem sobre os passos abaixo, exceto sigilo, confirmação antes de gravar e não inventar jurisprudência. Nunca edite este arquivo de comando: mudanças de padrão vão para o `CLAUDE.md` (`/anera:preferencias`).

1. **Identificar os casos.** Use o caso indicado nos argumentos ou, se não houver, os casos tratados nesta conversa. Se não estiver claro qual é o caso, pergunte. Leia o `PROCESSO.md` atual de cada um antes de alterar.
2. **Extrair da conversa** apenas o que for útil para uma sessão futura:
   - o que foi feito (peças, documentos, análises, buscas) e onde foi salvo;
   - **decisões** de estratégia e o que foi **combinado, aceito ou recusado** pelo cliente, com o motivo;
   - fatos novos sobre o caso;
   - pendências criadas e pendências resolvidas;
   - qualquer observação adicional passada nos argumentos.
3. **Atualizar o `PROCESSO.md`:**
   - **Histórico:** uma linha por evento, com data;
   - **Decisões e combinados:** uma linha por decisão (data, decisão, motivo, com quem);
   - **Pontos de atenção / Próximos passos:** acrescentar as pendências novas e remover as resolvidas;
   - **Dados do processo / Resumo dos fatos / Pedidos:** só se algo mudou.
4. **Atualizar também**, se for o caso: `CLIENTE.md` (contato, qualificação), `01_CLIENTES/_INDICE.md` (fase, status, número do processo) e `TESE.md` (aplicações).
5. **ANERA** (se conectado e a ficha tiver `uuid ANERA`):
   - proponha **anotações** no processo (ou atendimento) para o que for relevante à equipe, com prefixo de tipo: `[Decisão] …`, `[Pendência] …`, `[Histórico] …` — uma anotação objetiva por item, sem copiar a conversa;
   - se houve **movimentação** (ex.: protocolo, audiência realizada), proponha `anera_adicionar_andamento`;
   - se surgiu **prazo**, calcule com `anera_calcular_prazo` e proponha `anera_criar_prazo`; se um prazo foi cumprido, proponha `anera_concluir_prazo`;
   - se houver **documento** relacionado que o escritório queira no ANERA (peça, comprovante), ofereça anexá-lo à anotação: `anera_link_anexos` + `curl -F` (nunca base64);
   - não escreva o prefixo `IA:` (o servidor acrescenta);
   - **mostre a lista do que será gravado e só grave após o "sim"**.
6. **Regras:** escrever de forma objetiva, sem transcrever a conversa; não registrar nada que não tenha sido dito ou feito; não apagar registros anteriores (só corrigir se o advogado pedir).
7. **Confirmar** com um resumo curto do que foi gravado em cada ficha e no ANERA.
