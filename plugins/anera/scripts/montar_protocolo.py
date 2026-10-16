"""Monta a pasta de protocolo de um caso a partir de um plano (JSON), copiando e convertendo os arquivos para PDF.

Uso:
    python montar_protocolo.py --plano <plano.json>

plano.json:
{
  "destino": "<caminho da pasta do caso>/protocolo-inicial",
  "itens": [
    {"nome": "00_peticao_inicial",  "origens": ["<caso>/pecas/2026-10-07_peticao-inicial_v3.docx"]},
    {"nome": "01_procuracao",       "origens": ["<caso>/contrato-procuracao/procuracao_assinada.pdf"]},
    {"nome": "doc_1_nota_fiscal",   "origens": ["<caso>/documentos-caso/NFE.pdf"]},
    {"nome": "doc_5_fotos_veiculo", "origens": ["foto1.jpeg", "foto2.jpeg"]}
  ]
}
- Cada item vira UM PDF com o nome indicado (várias origens são unidas na ordem dada).
- Aceita PDF, DOCX/DOC (convertidos pelo Word) e imagens JPG/PNG.
- Os originais nunca são movidos nem alterados. Se a pasta de destino já existir, o script para (use outro nome).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

import fitz  # PyMuPDF

IMAGENS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
WORD = {".docx", ".doc"}


def docx_para_pdf(origem, destino_pdf):
    """Converte pelo Word usando caminhos temporários sem acentos (o Word falha com acentos via COM)."""
    tmp = tempfile.mkdtemp(prefix="prot_")
    try:
        ext = os.path.splitext(origem)[1].lower()
        src = os.path.join(tmp, "doc" + ext)
        out = os.path.join(tmp, "doc.pdf")
        shutil.copy(origem, src)
        ps = ("$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
              f"$d = $w.Documents.Open('{src}', $false, $true); "
              f"$d.SaveAs([ref]'{out}', [ref]17); $d.Close([ref]0); $w.Quit()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True, capture_output=True)
        shutil.copy(out, destino_pdf)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # cópias temporárias contêm dados do cliente


def anexar(pdf_final, origem, tmpdir):
    ext = os.path.splitext(origem)[1].lower()
    if ext == ".pdf":
        with fitz.open(origem) as src:
            pdf_final.insert_pdf(src)
    elif ext in WORD:
        convertido = os.path.join(tmpdir, f"conv_{len(os.listdir(tmpdir))}.pdf")
        docx_para_pdf(origem, convertido)
        with fitz.open(convertido) as src:
            pdf_final.insert_pdf(src)
    elif ext in IMAGENS:
        with fitz.open(origem) as img:
            pdf_bytes = img.convert_to_pdf()
        with fitz.open("pdf", pdf_bytes) as src:
            pdf_final.insert_pdf(src)
    else:
        raise ValueError(f"formato não suportado: {origem}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plano", required=True)
    a = ap.parse_args()
    with open(a.plano, encoding="utf-8") as f:
        plano = json.load(f)

    destino = plano["destino"]
    if os.path.exists(destino):
        sys.exit(f"ERRO: {destino} já existe. Use outro nome (ex.: protocolo-inicial_v2) em vez de sobrescrever.")
    faltando = [o for it in plano["itens"] for o in it["origens"] if not os.path.exists(o)]
    if faltando:
        sys.exit("ERRO: arquivos não encontrados:\n  " + "\n  ".join(faltando))

    os.makedirs(destino)
    tmpdir = tempfile.mkdtemp(prefix="prot_conv_")
    try:
        print(f"{'Arquivo':<55} {'Págs':>5} {'Tamanho':>10}")
        for it in plano["itens"]:
            final = fitz.open()
            for origem in it["origens"]:
                anexar(final, origem, tmpdir)
            caminho = os.path.join(destino, it["nome"] + ".pdf")
            final.save(caminho, garbage=3, deflate=True)
            paginas = final.page_count
            final.close()
            tam = os.path.getsize(caminho) / 1024 / 1024
            print(f"{it['nome'] + '.pdf':<55} {paginas:>5} {tam:>8.2f} MB")
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    print("Pasta criada:", destino)


if __name__ == "__main__":
    main()
