#!/usr/bin/env python3
"""
Verifica a integridade da tradução comparando cada lição em inglês (já convertida para Quarto,
em `_source/en-quarto/`) com a versão em português.

Checa:
  1. blocos de código: o código R normalizado (sem comentários, sem espaços) tem de ser idêntico
  2. quantidade de linhas de cerca ``` aberta/fechada
  3. quantidade de callouts `::: {.callout-...}` e fechamentos `:::`
  4. links para arquivos locais existentes
  5. imagens referenciadas existentes
  6. parágrafos que continuam em inglês (heurística)

Uso: python3 scripts/verificar_traducao.py
"""
import pathlib
import re
import sys
import difflib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PARES = [
    ("_source/en-quarto/episodios/01-acessar-atrasos.qmd", "episodios/01-acessar-atrasos.qmd"),
    ("_source/en-quarto/episodios/02-quantificar-transmissibilidade.qmd",
     "episodios/02-quantificar-transmissibilidade.qmd"),
    ("_source/en-quarto/episodios/03-funcoes-de-atraso.qmd", "episodios/03-funcoes-de-atraso.qmd"),
    ("_source/en-quarto/episodios/04-criar-previsoes.qmd", "episodios/04-criar-previsoes.qmd"),
    ("_source/en-quarto/episodios/05-severidade-estatica.qmd", "episodios/05-severidade-estatica.qmd"),
    ("_source/en-quarto/episodios/06-superspreading-estimar.qmd",
     "episodios/06-superspreading-estimar.qmd"),
    ("_source/en-quarto/episodios/07-superspreading-simular.qmd",
     "episodios/07-superspreading-simular.qmd"),
    ("_source/en-quarto/setup.qmd", "setup.qmd"),
    ("_source/en-quarto/glossario.qmd", "glossario.qmd"),
    ("_source/en-quarto/notas/equacao-de-renovacao.qmd", "notas/equacao-de-renovacao.qmd"),
    ("_source/en-quarto/notas/ajuste-cfr-atrasos.qmd", "notas/ajuste-cfr-atrasos.qmd"),
    ("_source/en-quarto/perfis.qmd", "perfis.qmd"),
]

# Linhas extras no bloco de código do PT que são correções documentadas do material original
# (registradas em licenca.qmd). Qualquer outra diferença continua sendo erro.
ADICOES_DOCUMENTADAS = {"sudo apt install libglpk40"}

# arquivos cujo texto legitimamente contém muitos termos em inglês (heurística desligada)
SEM_HEURISTICA = {"glossario.qmd", "setup.qmd"}


def blocos_codigo(texto: str):
    blocos, atual, dentro = [], [], False
    for linha in texto.split("\n"):
        if linha.startswith("```"):
            if dentro:
                blocos.append("\n".join(atual))
                atual, dentro = [], False
            else:
                dentro = True
            continue
        if dentro:
            atual.append(linha)
    return blocos


def normalizar(codigo: str) -> str:
    limpas = []
    for linha in codigo.split("\n"):
        linha = re.sub(r"#.*$", "", linha)
        linha = re.sub(r"\s+", " ", linha).strip()
        if linha:
            limpas.append(linha)
    return "\n".join(limpas)


def checar(en_rel: str, pt_rel: str) -> list:
    en_p, pt_p = ROOT / en_rel, ROOT / pt_rel
    problemas = []
    if not pt_p.exists():
        return [f"ARQUIVO AUSENTE: {pt_rel}"]

    # o arquivo PT pode ter caixas "No Brasil" a mais: compara só até o fim do EN
    en_txt = en_p.read_text(encoding="utf-8")
    pt_txt = pt_p.read_text(encoding="utf-8")

    # 1. código — alinhamento por conteúdo (difflib), não por índice, para que
    #    blocos novos documentados (caixas desta adaptação) não desloquem a comparação
    en_blocos, pt_blocos = blocos_codigo(en_txt), blocos_codigo(pt_txt)
    en_norm = [normalizar(b) for b in en_blocos]
    pt_norm = [normalizar(b) for b in pt_blocos]
    sm = difflib.SequenceMatcher(a=en_norm, b=pt_norm, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "insert":
            for j in range(j1, j2):
                so_pt = [x for x in pt_norm[j].split("\n") if x]
                if so_pt and all(any(y in x for y in ADICOES_DOCUMENTADAS) for x in so_pt):
                    continue
                problemas.append(f"bloco de código {j + 1} só existe no PT "
                                 f"(não é adição documentada): {so_pt[:1]}")
            continue
        if tag in ("delete", "replace"):
            for i in range(i1, i2):
                problemas.append(f"bloco de código {i + 1} do original não tem equivalente no PT")
            for j in range(j1, j2):
                na = en_norm[i1].split("\n") if i1 < len(en_norm) else []
                nb = pt_norm[j].split("\n")
                problemas.append(f"bloco de código {j + 1} diferente do original")
                for la, lb in zip(na, nb):
                    if la != lb:
                        problemas.append(f"    EN: {la[:110]}\n    PT: {lb[:110]}")
                        break

    # 2. cercas de código
    for nome, txt in (("EN", en_txt), ("PT", pt_txt)):
        n = len(re.findall(r"^```", txt, re.M))
        if n % 2:
            problemas.append(f"cercas de código ímpares em {nome} ({n})")

    # 3. callouts
    for nome, txt in (("EN", en_txt), ("PT", pt_txt)):
        abre = len(re.findall(r"^::: \{", txt, re.M))
        fecha = len(re.findall(r"^:::\s*$", txt, re.M))
        if abre != fecha:
            problemas.append(f"callouts desbalanceados em {nome}: {abre} abre / {fecha} fecha")
    ab_en = len(re.findall(r"^::: \{", en_txt, re.M))
    ab_pt = len(re.findall(r"^::: \{", pt_txt, re.M))
    if ab_pt < ab_en:
        problemas.append(f"callouts: EN={ab_en} PT={ab_pt} (perdidos {ab_en - ab_pt})")

    # 4. links internos existentes
    for link in re.findall(r"\]\((?!https?:|#|mailto:)([^)#]+)", pt_txt):
        if not (pt_p.parent / link).resolve().exists():
            problemas.append(f"link local quebrado: {link}")

    # 5. imagens
    for img in re.findall(r"!\[[^\]]*\]\((?!https?:)([^)]+)\)", pt_txt):
        if not (pt_p.parent / img).resolve().exists():
            problemas.append(f"imagem ausente: {img}")

    # 6. parágrafos que continuam em inglês
    if pt_rel in SEM_HEURISTICA:
        return problemas

    # linhas dentro de comentários HTML não são renderizadas: não entram na heurística
    em_comentario, dentro_comentario = set(), False
    for n, linha in enumerate(pt_txt.split("\n"), 1):
        if "<!--" in linha and "-->" not in linha:
            dentro_comentario = True
            em_comentario.add(n)
            continue
        if dentro_comentario:
            em_comentario.add(n)
            if "-->" in linha:
                dentro_comentario = False
            continue
        if "<!--" in linha and "-->" in linha:
            em_comentario.add(n)

    en_words = re.compile(
        r"\b(the|and|of|with|from|that|this|which|are|is|you can|we can|"
        r"should be|data set|column names|outbreak|dataset)\b", re.I)
    dentro = False
    for n, linha in enumerate(pt_txt.split("\n"), 1):
        if linha.startswith("```"):
            dentro = not dentro
            continue
        if dentro or len(linha) < 60 or n in em_comentario:
            continue
        limpa = re.sub(r"\(\*[^*]*\*\)", "", linha)
        limpa = re.sub(r"\*\*[^*]+\*\*", "", limpa)        # negrito: nomes próprios e rótulos
        limpa = re.sub(r"\*[^*]+\*", "", limpa)            # itálico: idem
        limpa = re.sub(r"`[^`]*`", "", limpa)              # nomes de função/pacote
        limpa = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", limpa)  # alvos de link
        palavras = len(re.findall(r"\w+", limpa))
        if palavras and len(en_words.findall(limpa)) / palavras > 0.10:
            problemas.append(f"L{n}: linha possivelmente ainda em inglês -> {linha[:90]}")
    return problemas


def main() -> int:
    total = 0
    for en_rel, pt_rel in PARES:
        probs = checar(en_rel, pt_rel)
        total += len(probs)
        marca = "OK  " if not probs else "ERRO"
        print(f"[{marca}] {pt_rel}")
        for p in probs:
            print(f"       {p}")
    print(f"\n{total} problema(s) encontrado(s).")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
