#!/usr/bin/env python3
"""Impede que o site publicado fique desatualizado.

O runner do GitHub Actions não tem R nem os pacotes do Epiverse, então o CI
publica reaproveitando o que está em `_freeze/` (perfil `ci`, `freeze: true`).
O efeito colateral, verificado na prática: se você editar só o TEXTO de uma
lição e der push sem renderizar localmente, o CI fica VERDE e publica a versão
antiga — o `freeze: true` reaproveita o resultado congelado e não regenera o
HTML daquele arquivo.

Este script grava a impressão digital de cada .qmd no momento em que o render
local roda (`--update`) e o CI confere se algum arquivo mudou depois (`--check`).
Assim a falha deixa de ser silenciosa e passa a dizer o que fazer.

Uso:
    python3 scripts/freshness.py --update   # depois de `quarto render`, antes do commit
    python3 scripts/freshness.py --check    # no CI
"""

import hashlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANIFEST = ROOT / ".freeze-sync.json"
IGNORAR = {".Rlib", "_site", "_work", "_source", ".quarto", ".git", "_freeze"}


def arquivos():
    for p in sorted(ROOT.rglob("*.qmd")):
        if any(parte in IGNORAR for parte in p.relative_to(ROOT).parts):
            continue
        yield p


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def atualizar():
    dados = {str(p.relative_to(ROOT)): digest(p) for p in arquivos()}
    MANIFEST.write_text(
        json.dumps(dados, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"{len(dados)} arquivo(s) registrados em {MANIFEST.name}")
    return 0


def conferir():
    if not MANIFEST.exists():
        print("erro: .freeze-sync.json não existe.")
        print("Rode: quarto render && python3 scripts/freshness.py --update")
        return 1

    registrado = json.loads(MANIFEST.read_text(encoding="utf-8"))
    atual = {str(p.relative_to(ROOT)): digest(p) for p in arquivos()}

    problemas = []
    for nome, d in sorted(atual.items()):
        if nome not in registrado:
            problemas.append(f"nunca renderizado localmente: {nome}")
        elif registrado[nome] != d:
            problemas.append(f"editado depois do último render: {nome}")
    for nome in sorted(set(registrado) - set(atual)):
        problemas.append(f"arquivo apagado: {nome}")

    if problemas:
        print("O site publicado ficaria desatualizado:\n")
        for x in problemas:
            print("  -", x)
        print("\nO CI não tem R e não consegue regerar estes arquivos.")
        print("Rode: quarto render && python3 scripts/freshness.py --update")
        return 1

    print("ok: os .qmd do site batem com o último render local")
    return 0


if __name__ == "__main__":
    if "--update" in sys.argv:
        sys.exit(atualizar())
    sys.exit(conferir())
