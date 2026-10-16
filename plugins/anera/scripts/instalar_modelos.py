"""Instala no escritório os modelos de contrato, procuração e declaração do ANERA, personalizados.

Uso:
    python instalar_modelos.py --origem <pacote.zip | pasta> --config <escritorio.json> --destino <pasta 03_MODELOS>
                               [--timbrado <timbrado.docx>] [--substituir] [--pdf]

- Origem: o pacote baixado pelo conector do ANERA (anera_link_modelos), conferido pelo manifesto (sha256 de cada
  arquivo), ou uma pasta com os modelos genéricos (contratos/ e procuracoes/), para manutenção.

- Aplica o timbrado do escritório (cabeçalho, rodapé, margens) aos contratos e procurações.
  A declaração de hipossuficiência é sempre documento branco (sem timbrado).
- Preenche os campos do ESCRITÓRIO ({{ADVOGADO_NOME}}, {{TELEFONES_OFICIAIS}}...). Os campos do CLIENTE
  ({{NOME_CONTRATANTE}}, {{CPF}}...) ficam intactos para o comando de documentos preencher depois.
- Troca a cor principal (padrão 16304D) pela cor do escritório, se configurada.
- Nunca sobrescreve sem --substituir; com --substituir, a versão anterior vai para <pasta>/_historico/.
- Protege modelos alterados pelo escritório: <destino>/_versao-modelos.json guarda o sha256 de cada arquivo instalado.
  Com --substituir, um arquivo diferente do registrado (ou sem registro) é MANTIDO e a versão nova é gravada ao lado,
  como <nome>_novo-<versao>.docx, para comparar. --incluir-alterados substitui também esses (anterior → _historico/).
"""
import argparse
import datetime
import glob
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE_NEUTRA = os.path.normpath(os.path.join(AQUI, "..", "modelos", "_base", "base-neutra.docx"))
COR_PADRAO = "16304D"
CAMPO = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
CAMPOS_ESCRITORIO = {"ADVOGADO_NOME", "ADVOGADO_OAB_UF", "ADVOGADO_OAB_NUMERO", "ADVOGADO_CPF", "ESCRITORIO_ENDERECO",
                     "ESCRITORIO_CIDADE_UF", "ESCRITORIO_CEP", "EMAIL_OFICIAL", "TELEFONE_PRINCIPAL",
                     "TELEFONES_OFICIAIS", "TELEFONES_OFICIAIS_RESUMO"}


def campos(cfg):
    adv, esc = cfg["advogado"], cfg["escritorio"]
    tels = esc.get("telefones_oficiais") or []
    return {
        "ADVOGADO_NOME": adv["nome"].upper(),
        "ADVOGADO_OAB_UF": adv["oab_uf"],
        "ADVOGADO_OAB_NUMERO": adv["oab_numero"],
        "ADVOGADO_CPF": adv.get("cpf", ""),
        "ESCRITORIO_ENDERECO": esc["endereco"],
        "ESCRITORIO_CIDADE_UF": esc["cidade_uf"],
        "ESCRITORIO_CEP": esc["cep"],
        "EMAIL_OFICIAL": esc["email"],
        "TELEFONE_PRINCIPAL": esc.get("telefone_principal") or (tels[0] if tels else ""),
        "TELEFONES_OFICIAIS": "   |   ".join(tels),
        "TELEFONES_OFICIAIS_RESUMO": "  |  ".join(tels),
    }


def corpo(docx):
    x = zipfile.ZipFile(io.BytesIO(docx)).read("word/document.xml").decode("utf-8")
    ini = x.index("<w:body>") + len("<w:body>")
    return x[ini:x.index("<w:sectPr")]


def montar(base, body, destino, valores, cor):
    zin = zipfile.ZipFile(io.BytesIO(base) if isinstance(base, bytes) else base)
    zout = zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED)
    restantes = set()
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == "word/document.xml":
            x = data.decode("utf-8")
            ini = x.index("<w:body>") + len("<w:body>")
            fim = x.index("<w:sectPr")
            b = CAMPO.sub(lambda m: escape(valores[m.group(1)]) if m.group(1) in valores else m.group(0), body)
            if cor and cor.upper() != COR_PADRAO:
                b = b.replace(COR_PADRAO, cor.upper())
            restantes = {c for c in CAMPO.findall(b) if c in CAMPOS_ESCRITORIO}
            data = (x[:ini] + b + x[fim:]).encode("utf-8")
        zout.writestr(info, data)
    zout.close()
    return restantes


def gerar_pdf(docx):
    tmp = tempfile.mkdtemp(prefix="mod_")
    try:
        origem, destino = os.path.join(tmp, "doc.docx"), os.path.join(tmp, "doc.pdf")
        shutil.copy(docx, origem)
        ps = ("$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
              f"$d = $w.Documents.Open('{origem}', $false, $true); "
              f"$d.SaveAs([ref]'{destino}', [ref]17); $d.Close([ref]0); $w.Quit()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, capture_output=True)
        shutil.copy(destino, os.path.splitext(docx)[0] + ".pdf")
        return True
    except Exception as e:  # sem Word: o .docx continua válido
        print("   (PDF não gerado:", e, ")")
        return False
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def guardar_anterior(caminho):
    hist = os.path.join(os.path.dirname(caminho), "_historico")
    os.makedirs(hist, exist_ok=True)
    data = datetime.date.today().isoformat()
    for ext in (".docx", ".pdf"):
        atual = os.path.splitext(caminho)[0] + ext
        if os.path.exists(atual):
            alvo = os.path.join(hist, f"{data}_{os.path.basename(atual)}")
            n = 2
            while os.path.exists(alvo):
                alvo = os.path.join(hist, f"{data}_{n}_{os.path.basename(atual)}")
                n += 1
            shutil.move(atual, alvo)


def pasta_de(nome):
    return "contratos" if nome.startswith("contrato") else "procuracoes"


def carregar_origem(origem):
    """Devolve (versao_pacote, [(pasta, nome, bytes)]). Pacote zip é conferido pelo manifesto."""
    if os.path.isdir(origem):
        itens = []
        for pasta in ("contratos", "procuracoes"):
            for f in sorted(glob.glob(os.path.join(origem, pasta, "*.docx"))):
                with open(f, "rb") as h:
                    itens.append((pasta, os.path.basename(f), h.read()))
        versao = None
        cat = os.path.join(origem, "catalogo.json")
        if os.path.exists(cat):
            with open(cat, encoding="utf-8") as h:
                versao = json.load(h).get("versao_pacote")
        return versao, itens
    z = zipfile.ZipFile(origem)
    try:
        manifesto = json.loads(z.read("manifesto.json").decode("utf-8"))
    except KeyError:
        sys.exit("ERRO: pacote sem manifesto.json — baixe de novo pelo conector do ANERA.")
    itens = []
    for m in manifesto["modelos"]:
        dados = z.read(m["arquivo"])
        if hashlib.sha256(dados).hexdigest() != m["sha256"].lower():
            sys.exit(f"ERRO: {m['arquivo']} não confere com o manifesto (arquivo alterado ou corrompido). Nada foi instalado.")
        nome = os.path.basename(m["arquivo"])
        itens.append((pasta_de(nome), nome, dados))
    return manifesto.get("versao_pacote"), itens


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--origem", required=True, help="pacote .zip baixado do ANERA ou pasta com os modelos")
    ap.add_argument("--config", required=True)
    ap.add_argument("--destino", required=True, help="pasta 03_MODELOS do escritório")
    ap.add_argument("--timbrado", help="timbrado .docx do escritório (sem ele, usa base neutra)")
    ap.add_argument("--substituir", action="store_true")
    ap.add_argument("--incluir-alterados", action="store_true",
                    help="com --substituir, substitui também modelos alterados pelo escritório")
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    with open(a.config, encoding="utf-8") as f:
        cfg = json.load(f)
    valores = campos(cfg)
    cor = (cfg.get("visual") or {}).get("cor_principal", "").lstrip("#")
    if a.timbrado and not os.path.exists(a.timbrado):
        sys.exit(f"ERRO: timbrado não encontrado: {a.timbrado}")
    versao, itens = carregar_origem(a.origem)
    if not itens:
        sys.exit("ERRO: nenhum modelo encontrado na origem.")
    caminho_registro = os.path.join(a.destino, "_versao-modelos.json")
    registro = {}
    if os.path.exists(caminho_registro):
        with open(caminho_registro, encoding="utf-8") as h:
            registro = json.load(h)
    hashes = dict(registro.get("arquivos") or {})
    avisos, instalados, mantidos = [], [], []
    for pasta, nome, modelo in itens:
        os.makedirs(os.path.join(a.destino, pasta), exist_ok=True)
        rel = f"{pasta}/{nome}"
        destino = os.path.join(a.destino, pasta, nome)
        if os.path.exists(destino):
            if not a.substituir:
                print("pulado (já existe):", os.path.join(pasta, nome))
                continue
            with open(destino, "rb") as h:
                alterado = hashes.get(rel) != hashlib.sha256(h.read()).hexdigest()
            if alterado and not a.incluir_alterados:
                destino = os.path.join(a.destino, pasta, f"{os.path.splitext(nome)[0]}_novo-{versao or 'atual'}.docx")
                mantidos.append((rel, os.path.relpath(destino, a.destino)))
            else:
                guardar_anterior(destino)
        declaracao = nome.startswith("declaracao")
        if declaracao:
            base = modelo
        elif a.timbrado:
            base = a.timbrado
        else:
            base = BASE_NEUTRA
        faltando = montar(base, corpo(modelo), destino, valores, None if declaracao else cor)
        if faltando:
            avisos.append((nome, sorted(faltando)))
        if os.path.basename(destino) == nome:
            with open(destino, "rb") as h:
                hashes[rel] = hashlib.sha256(h.read()).hexdigest()
            instalados.append(rel)
            print("instalado:", os.path.join(pasta, nome))
        else:
            print("mantido (alterado pelo escritório):", rel, "→ versão nova ao lado:", os.path.basename(destino))
        if a.pdf:
            gerar_pdf(destino)
    if instalados or mantidos:
        pendentes = sorted(set(registro.get("pendentes_comparacao") or []) - set(instalados) | {m for m, _ in mantidos})
        with open(caminho_registro, "w", encoding="utf-8") as h:
            json.dump({"versao_pacote": versao, "instalado_em": datetime.date.today().isoformat(),
                       "arquivos": hashes, "pendentes_comparacao": pendentes}, h, ensure_ascii=False, indent=2)
    if mantidos:
        print("ATENÇÃO — modelos alterados pelo escritório foram mantidos; compare com a versão nova:")
        for rel, novo in mantidos:
            print(f"   {rel}  ×  {novo}")
    for nome, f in avisos:
        print("AVISO — campos do escritório sem valor em", nome, ":", ", ".join(f))
    vazios = [k for k, v in valores.items() if not v]
    if vazios:
        print("AVISO — dados do escritório vazios na configuração:", ", ".join(vazios))


if __name__ == "__main__":
    main()
