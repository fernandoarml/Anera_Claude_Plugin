"""Preenche um modelo .docx do escritório (campos {{CAMPO}}) e, opcionalmente, gera o PDF pelo Word.

Uso:
    python preencher_modelo.py --modelo <modelo.docx> --saida <arquivo.docx> --dados <dados.json> [--pdf]

dados.json: {"NOME_CONTRATANTE": "MARIA DA SILVA", "CPF": "000.000.000-00", ...}
Ao final, lista os campos que ficaram sem preencher (o arquivo é gerado mesmo assim, para revisão).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape

CAMPO = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
PARTES_TEXTO = re.compile(r"word/(document|header\d*|footer\d*)\.xml$")


def preencher(modelo, saida, dados):
    restantes = set()
    zin = zipfile.ZipFile(modelo)
    os.makedirs(os.path.dirname(os.path.abspath(saida)), exist_ok=True)
    zout = zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED)
    for info in zin.infolist():
        data = zin.read(info.filename)
        if PARTES_TEXTO.match(info.filename):
            x = data.decode("utf-8")
            x = CAMPO.sub(lambda m: escape(str(dados[m.group(1)])) if m.group(1) in dados else m.group(0), x)
            restantes.update(CAMPO.findall(x))
            data = x.encode("utf-8")
        zout.writestr(info, data)
    zout.close()
    return sorted(restantes)


def gerar_pdf(docx):
    """Converte pelo Word usando cópia temporária em caminho sem acentos (o Word falha com acentos via COM)."""
    tmp = tempfile.mkdtemp(prefix="doc_")
    try:
        origem = os.path.join(tmp, "doc.docx")
        destino = os.path.join(tmp, "doc.pdf")
        shutil.copy(docx, origem)
        ps = ("$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
              f"$d = $w.Documents.Open('{origem}', $false, $true); "
              f"$d.SaveAs([ref]'{destino}', [ref]17); $d.Close([ref]0); $w.Quit()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
        pdf = os.path.splitext(docx)[0] + ".pdf"
        shutil.copy(destino, pdf)
        return pdf
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # a cópia temporária contém dados do cliente


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--dados", required=True)
    ap.add_argument("--pdf", action="store_true")
    a = ap.parse_args()
    with open(a.dados, encoding="utf-8") as f:
        dados = json.load(f)
    if os.path.exists(a.saida):
        sys.exit(f"ERRO: {a.saida} já existe. Use a próxima versão (_v2, _v3...) em vez de sobrescrever.")
    restantes = preencher(a.modelo, a.saida, dados)
    print("Gerado:", a.saida)
    if a.pdf:
        print("PDF:", gerar_pdf(a.saida))
    print("Campos sem preencher:", ", ".join(restantes) if restantes else "nenhum")


if __name__ == "__main__":
    main()
