#!/usr/bin/env python3
"""
Converte os episódios do Carpentries Workbench (sandpaper) do curso
"Real-time analysis and forecasting for outbreak analytics with R"
(Epiverse-TRACE tutorials-middle) para o formato Quarto usado no site PT-BR.

Uso: python3 scripts/convert_carpentries.py <entrada> <saida> [episodios|raiz|notas]
"""
import re
import sys

BLOCKS = {
    "questions":   ("note",      "Perguntas",           False),
    "objectives":  ("tip",       "Objetivos",           False),
    "prereq":      ("important", "Pré-requisitos",      False),
    "spoiler":     ("note",      "Detalhes",            True),
    "callout":     ("note",      None,                  False),
    "challenge":   ("tip",       "Desafio",             False),
    "hint":        ("note",      "Dica",                True),
    "solution":    ("note",      "Solução",             True),
    "checklist":   ("note",      "Checklist",           False),
    "caution":     ("warning",   "Atenção",             False),
    "discussion":  ("note",      "Discussão",           False),
    "keypoints":   ("note",      "Pontos-chave",        False),
    "instructor":  ("important", "Para o instrutor",    True),
    "checkpoint":  ("note",      "Checagem",            False),
    "testimonial": ("note",      "Para se aprofundar",  False),
    "tab":         ("panel-tabset", None,               False),
}

OPEN = re.compile(r"^(:{3,})\s*([A-Za-z][\w-]*)\s*$")
CLOSE = re.compile(r"^:{3,}\s*$")

# slug original -> nome do arquivo no site PT-BR
EPISODIOS = {
    "delays-access":             "01-acessar-atrasos",
    "quantify-transmissibility": "02-quantificar-transmissibilidade",
    "delays-functions":          "03-funcoes-de-atraso",
    "create-forecast":           "04-criar-previsoes",
    "severity-static":           "05-severidade-estatica",
    "superspreading-estimate":   "06-superspreading-estimar",
    "superspreading-simulate":   "07-superspreading-simular",
    "template":                  "template",
}
NOTAS = {
    "intro-renewal-equation":  "equacao-de-renovacao",
    "intro-cfr-adjust-delays": "ajuste-cfr-atrasos",
}

REWRITES = [
    (r"\(\.\./learners/setup\.md", "(../setup.qmd"),
    (r"\(\.\./learners/reference\.md", "(../glossario.qmd"),
    (r"\(\.\./learners/intro-renewal-equation\.md\)", "(../notas/equacao-de-renovacao.qmd)"),
    (r"\(\.\./learners/intro-cfr-adjust-delays\.md\)", "(../notas/ajuste-cfr-atrasos.qmd)"),
    (r"\(reference\.md", "(glossario.qmd"),
    (r"\(\./reference\.md", "(glossario.qmd"),
    (r"\(\.\./profiles/learner-profiles\.md\)", "(../perfis.qmd)"),
    (r"\(profiles/learner-profiles\.md\)", "(perfis.qmd)"),
    (r"\(\.\./instructors/instructor-notes\.md\)", "(../instrutor.qmd)"),
]
for slug, novo in EPISODIOS.items():
    REWRITES.append((rf"\(\.\./episodes/{re.escape(slug)}\.md(#[^)]*)?\)", rf"({novo}.qmd\1)"))
for slug, novo in NOTAS.items():
    REWRITES.append((rf"\((\.\./)?(learners/)?{re.escape(slug)}\.md\)", f"(../notas/{novo}.qmd)"))

DL = re.compile(r"https://epiverse-trace\.github\.io/tutorials-middle/data/")
IMG = re.compile(r"(\]\()(?P<p>(\.\./)?(episodes/)?fig/)(?P<f>[\w.\-]+\.(?:png|jpg|jpeg|svg))")
LINKDATA = re.compile(r"\]\((?:\.\./)?(?:episodes/)?data/")


def convert(text: str, destino: str) -> str:
    em_episodios = destino == "episodios"
    em_notas = destino == "notas"
    pref = "../" if (em_episodios or em_notas) else ""
    out, stack, in_code = [], [], False

    for line in text.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue

        m = OPEN.match(line)
        if m:
            cls = m.group(2).lower()
            if cls in BLOCKS:
                kind, title, collapse = BLOCKS[cls]
                if kind == "panel-tabset":
                    out.append("::: {.panel-tabset}")
                    stack.append("tab")
                else:
                    attrs = f".callout-{kind}"
                    if cls == "challenge":
                        attrs += " .desafio"
                    if cls == "solution":
                        attrs += " .solucao"
                    opts = f' title="{title}"' if title else ""
                    if collapse:
                        opts += ' collapse="true"'
                    out.append(f"::: {{{attrs}{opts}}}")
                    stack.append(cls)
                continue
            else:
                out.append(f"::: {{.{cls}}}")
                stack.append(cls)
                continue

        if CLOSE.match(line):
            if stack:
                stack.pop()
                out.append(":::")
            continue

        if stack and stack[-1] == "tab" and re.match(r"^#{3,4} ", line):
            line = line[1:]
        for pat, rep in REWRITES:
            line = re.sub(pat, rep, line)
        line = DL.sub(f"{pref}data/", line)
        line = LINKDATA.sub(f"]({pref}data/", line)
        line = IMG.sub(lambda mm: f"{mm.group(1)}{pref}img/{mm.group('f')}", line)
        out.append(line)

    return "\n".join(out)


def main():
    src, dst, tipo = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "raiz")
    text = open(src, encoding="utf-8").read()
    res = convert(text, tipo)
    open(dst, "w", encoding="utf-8").write(res)
    print(f"[{tipo}] {src} -> {dst}: {len(text.splitlines())} -> {len(res.splitlines())} linhas")
    for name, (kind, title, _) in BLOCKS.items():
        a = len(re.findall(rf"^:{{3,}}\s*{name}\s*$", text, re.M))
        needle = f'title="{title}"' if title else "{.callout-" + kind
        b = res.count(needle)
        if a and b < a:
            print(f"    ATENCAO: {a} blocos '{name}', {b} convertidos")


if __name__ == "__main__":
    main()
