#!/usr/bin/env python3
"""
Garante linha em branco ANTES de cada cerca de div (`:::` / `::: {.callout-...}`),
fora de blocos de código. Sem isso o pandoc não reconhece o div e deixa `:::` literal no HTML.

Uso: python3 scripts/normalizar_divs.py [dir ...]
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent


def normalizar(texto: str) -> str:
    linhas = texto.split("\n")
    saida, dentro = [], False
    for linha in linhas:
        if linha.startswith("```"):
            dentro = not dentro
            saida.append(linha)
            continue
        if not dentro and linha.startswith(":::") and saida and saida[-1].strip():
            if not saida[-1].startswith(":::"):
                saida.append("")
        saida.append(linha)
    return "\n".join(saida)


def main() -> None:
    alvos = sys.argv[1:] or ["_source/en-quarto"]
    total = 0
    for alvo in alvos:
        for p in sorted((RAIZ / alvo).rglob("*.qmd")):
            txt = p.read_text(encoding="utf-8")
            novo = normalizar(txt)
            if novo != txt:
                p.write_text(novo, encoding="utf-8")
                total += 1
                print(f"ajustado: {p.relative_to(RAIZ)}")
    print(f"{total} arquivo(s) ajustado(s).")


if __name__ == "__main__":
    main()
