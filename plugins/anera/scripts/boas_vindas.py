"""Hook SessionStart do plugin anera: estado do escritório + regras-base do plugin.

Saída: texto factual (vai para o contexto da sessão). Não executa nada e não lê dados de clientes.
- Em toda abertura (startup, resume, clear, compact) de uma pasta configurada: injeta regras/REGRAS-BASE.md,
  para que as regras gerais venham sempre da versão instalada do plugin (o CLAUDE.md guarda só o que é do escritório).
- Só no startup: boas-vindas/orientação e aviso de versão nova.
Única rede: GET em versao_url (distribuicao.json: versao.json no repositório público do plugin), só no startup, sem enviar dados.
Desligar a consulta: variável de ambiente ANERA_SEM_VERIFICACAO=1.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_PLUGIN = os.path.normpath(os.path.join(AQUI, ".."))
LIMITE = 9500  # o Claude Code limita o texto que um hook injeta; acima disso, só aponta o arquivo

try:
    evento = json.loads(sys.stdin.read() or "{}")
except Exception:
    evento = {}
origem = evento.get("source", "startup")
projeto = os.environ.get("CLAUDE_PROJECT_DIR") or evento.get("cwd") or os.getcwd()
config = os.path.join(projeto, ".claude", "escritorio.json")
tem_config = os.path.exists(config)
tem_estrutura = os.path.isdir(os.path.join(projeto, "01_CLIENTES"))


def ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


def versao_nova():
    """Consulta versao.json no repositório do plugin (GET simples, 2 s). Falhou → silêncio."""
    if os.environ.get("ANERA_SEM_VERIFICACAO"):
        return None
    try:
        import urllib.request
        dist = json.loads(ler(os.path.join(AQUI, "distribuicao.json")))
        atual = json.loads(ler(os.path.join(RAIZ_PLUGIN, ".claude-plugin", "plugin.json")))["version"]
        with urllib.request.urlopen(dist["versao_url"], timeout=2) as r:
            pub = json.loads(r.read(65536).decode("utf-8"))

        def num(v):
            return tuple(int(x) for x in re.findall(r"\d+", v)[:3])

        if num(pub["versao"]) > num(atual):
            return atual, pub
    except Exception:
        return None
    return None


linhas = []
if origem == "startup":
    linhas.append("Plugin ANERA (escritório de advocacia) ativo nesta sessão.")
    if not tem_config:
        linhas += [
            "Estado: esta pasta AINDA NÃO FOI CONFIGURADA como escritório (não existe .claude/escritorio.json).",
            "Na primeira resposta ao usuário, o plugin prevê: dar boas-vindas em uma frase, explicar em duas linhas o que o "
            "plugin faz e oferecer a configuração guiada (/anera:configurar-escritorio) e o tutorial (/anera:ajuda). "
            "Se o usuário pedir outra coisa, atender e lembrar da configuração ao final.",
        ]
        if tem_estrutura:
            linhas.append("Observação: a pasta já tem 01_CLIENTES, então pode ser um escritório organizado antes do plugin; "
                          "a configuração deve preservar tudo o que existe.")
    else:
        try:
            cfg = json.loads(ler(config))
            nome = (cfg.get("escritorio") or {}).get("nome") or (cfg.get("advogado") or {}).get("nome") or ""
            linhas.append(f"Estado: escritório configurado ({nome}).".replace(" ()", ""))
        except Exception:
            linhas.append("Estado: existe .claude/escritorio.json, mas não foi possível lê-lo (arquivo inválido); "
                          "/anera:configurar-escritorio pode corrigir.")
        claude_md = os.path.join(projeto, "CLAUDE.md")
        if os.path.exists(claude_md) and "anera:claude-md v2" not in ler(claude_md):
            linhas.append("Observação: o CLAUDE.md desta pasta é de formato anterior (repete regras gerais que agora vêm do "
                          "plugin). Ofereça uma vez, sem insistir: /anera:configurar-escritorio migrar.")
        linhas.append("Dúvidas: /anera:ajuda. Visão do dia com o ANERA: /anera:painel. Preferências: /anera:preferencias.")
    linhas.append("O plugin funciona melhor com o ANERA conectado (prazos, intimações, andamentos, cadastro e "
                  "anotações; os modelos de contrato e procuração também vêm pelo conector); sem conexão, as "
                  "ferramentas anera_* não aparecem e o trabalho segue só com a pasta.")
    nova = versao_nova()
    if nova:
        atual, pub = nova
        resumo = "; ".join(pub.get("novidades") or [])[:400]
        linhas.append(f"ATUALIZAÇÃO DISPONÍVEL: plugin anera {pub['versao']} (instalada: {atual}). Na primeira resposta, "
                      f"avisar o usuário em uma linha e indicar o comando `{pub.get('atualizar')}` (depois, /reload-plugins "
                      "ou nova sessão) e a opção de ligar a atualização automática em /plugin › Marketplaces."
                      + (f" Novidades: {resumo}" if resumo else ""))

if tem_config:
    regras_path = os.path.join(RAIZ_PLUGIN, "regras", "REGRAS-BASE.md")
    regras = ler(regras_path).replace("${CLAUDE_PLUGIN_ROOT}", RAIZ_PLUGIN)
    texto = "\n".join(linhas)
    if len(texto) + len(regras) + 2 <= LIMITE:
        linhas.append("\n" + regras)
    else:
        linhas.append(f"REGRAS-BASE do plugin (leitura obrigatória antes da primeira tarefa): {regras_path}")

if linhas:
    sys.stdout.buffer.write(("\n".join(linhas) + "\n").encode("utf-8"))  # UTF-8 também no Windows
