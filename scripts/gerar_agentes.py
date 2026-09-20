#!/usr/bin/env python3
"""Gera os prompts e os scripts de execução dos agentes tradutores (agy / Antigravity CLI)."""
import pathlib

ROOT = pathlib.Path("/home/marc/Documentos/Projetos/tutorials-middle-pt")
AG = ROOT / "_work" / "agents"
AG.mkdir(parents=True, exist_ok=True)

AGENTES = [
    ("01", "episodios/01-acessar-atrasos.qmd",
     "Episódio 1 — Acessar distribuições de atraso (Access epidemiological delay distributions): "
     "uso do pacote {epiparameter} para obter distribuições de tempo de geração e intervalo serial "
     "da literatura, estatísticas resumo, parâmetros de distribuição, tabelas de parâmetros e "
     "citações dos estudos."),
    ("02", "episodios/02-quantificar-transmissibilidade.qmd",
     "Episódio 2 — Quantificar transmissibilidade (Quantifying transmission): uso do {EpiNow2} para "
     "estimar o número de reprodução efetivo Rt e o tempo de duplicação a partir de dados de casos, "
     "inferência bayesiana com Stan, opções de atraso, truncamento à direita, efeito de dia da semana "
     "e sobreposição."),
    ("03", "episodios/03-funcoes-de-atraso.qmd",
     "Episódio 3 — Usar distribuições de atraso na análise (Use delay distributions in analysis): "
     "combinar distribuições com EpiNow2::delay_opts(), gerar atrasos com simulate_delays(), comparar "
     "atrasos fixos e variáveis, discretizar distribuições, plotar PMF/CDF e usar atrasos em epinow()."),
    ("04", "episodios/04-criar-previsoes.qmd",
     "Episódio 4 — Criar previsão de curto prazo (Create a short-term forecast): previsão de casos e "
     "óbitos com epinow(), modelo de observação com obs_opts() e subnotificação, integração com "
     "{epiparameter}, previsão de óbitos a partir de casos e escolha do horizonte de previsão."),
    ("05", "episodios/05-severidade-estatica.qmd",
     "Episódio 5 — Estimar a gravidade de um surto (Estimation of outbreak severity): risco de "
     "letalidade (CFR) bruto e ajustado pelo atraso com o pacote {cfr}, estimativa de CFR e IFR, "
     "viés temporal, censura à direita, estratificação por idade e uso de {outbreaks}."),
    ("06", "episodios/06-superspreading-estimar.qmd",
     "Episódio 6 — Levar em conta o superspreading (Account for superspreading): transmissão em "
     "cadeias com {epicontacts}, estimativa empírica da distribuição de casos secundários com "
     "{fitdistrplus}, ajuste de distribuições negativa binomial e Poisson, e uso do {superspreading} "
     "para probabilidade de aglomerados e de extinção."),
    ("07", "episodios/07-superspreading-simular.qmd",
     "Episódio 7 — Simular cadeias de transmissão (Simulate transmission chains): uso do {epichains} "
     "para simular o potencial de surtos grandes e de extinção a partir de distribuições de casos "
     "secundários superdispersas, tamanho e duração de cadeias, número de casos e cenários de "
     "intervenção."),
    ("08", "setup.qmd + glossario.qmd",
     "Página de Setup (instalação de R, ferramentas de compilação, pacotes do Epiverse, projeto do R, "
     "GitHub) e o Glossário de Termos. São DOIS arquivos de saída. No glossário, mantenha as seções de "
     "letra (`## A`, `## B`, ...) e reordene as entradas de cada seção na ordem alfabética do português; "
     "preserve integralmente as âncoras `{#algumacoisa}` e os links internos `(#algumacoisa)`, porque os "
     "episódios apontam para elas."),
    ("09", "notas/equacao-de-renovacao.qmd + notas/ajuste-cfr-atrasos.qmd",
     "Duas notas teóricas de apoio: (a) Introdução à equação de renovação (Introduction to the Renewal "
     "equation) — como os atrasos entram na estimativa de Rt; (b) Como ajustar o CFR pelo atraso "
     "(How to adjust the CFR for delays) — CFR bruto versus corrigido, atraso entre caso e óbito. "
     "São DOIS arquivos de saída."),
]

PROMPT = """Você é um tradutor técnico-científico de epidemiologia. Trabalhe no diretório
{root}

## Passo 1 — Leia as regras
Leia o arquivo `scripts/BRIEF-traducao.md` (caminho absoluto: {root}/scripts/BRIEF-traducao.md)
e siga TODAS as regras invioláveis e o termbase. Ele é a fonte de verdade.

## Passo 2 — Tarefa
{descricao}

ENTRADA (leia o arquivo inteiro antes de começar):
{entradas}

SAÍDA (crie/sobrescreva):
{saidas}

O texto de entrada é uma aula de análise de surtos em R, já convertida do formato
Carpentries/The Carpentries Workbench para o formato Quarto (callouts `::: {{.callout-...}}`).
Os títulos dos callouts já estão em português: não os altere.

## Regras extras para este trabalho
- No cabeçalho YAML (entre `---`), mantenha APENAS a linha `title:` traduzida. Remova
  `teaching:`, `exercises:`, `editor_options:` e qualquer outra linha.
- O arquivo de saída deve conter SOMENTE o conteúdo da aula traduzido. Não acrescente
  comentários seus, nem relatórios, nem blocos de código novos.
- Preserve exatamente a quantidade, a ordem e a indentação dos blocos de código e dos
  `::: {{.callout-...}}` do original. Mantenha uma linha em branco antes e depois de cada `:::`.
- NÃO traduza o conteúdo dentro dos blocos de código, exceto comentários que começam com `#`.

## Como escrever o arquivo
Use a ferramenta de escrita de arquivo para criar o arquivo de saída completo, com caminho absoluto.
Se o arquivo for grande, escreva em partes (primeira parte criando o arquivo, o restante com
`cat >> arquivo << 'EOF'` no shell), sempre com caminho absoluto e fechando o heredoc corretamente.

## Checklist antes de terminar
1. Nenhum token de código R alterado (exceto comentários `#`).
2. Todos os blocos `::: {{.callout-...}}` preservados, com os mesmos títulos.
3. Saídas de console/erros do R preservados em inglês.
4. Nenhum número, link, referência ou dado inventado.
5. `wc -l` do arquivo de saída conferido e comparável ao da entrada.
6. Marcações `<!-- [verificar] -->` e `<!-- CONTEXTO-BR: ... -->` deixadas onde couber.

## Relatório final (texto curto)
- Caminhos absolutos dos arquivos escritos + número de linhas de cada um
- Lista das marcações `[verificar]` (linha e motivo)
- Lista das sugestões `CONTEXTO-BR` (linha e sugestão)
"""

for num, saida_rel, desc in AGENTES:
    entradas = "\n".join(f"  - {ROOT}/_source/en-quarto/{s.strip()}" for s in saida_rel.split(" + "))
    saidas = "\n".join(f"  - {ROOT}/{s.strip()}" for s in saida_rel.split(" + "))
    txt = PROMPT.format(root=ROOT, descricao=desc, entradas=entradas, saidas=saidas)
    (AG / f"prompt-{num}.md").write_text(txt, encoding="utf-8")

    sh = f"""#!/usr/bin/env bash
# Agente tradutor {num}
cd "{ROOT}" || exit 1
LOG="{AG}/log-{num}.txt"
agy --dangerously-skip-permissions --print-timeout 40m --print="$(cat '{AG}/prompt-{num}.md')" > "$LOG" 2>&1
echo "EXIT_AGENTE{num}=$?" >> "$LOG"
"""
    p = AG / f"run-{num}.sh"
    p.write_text(sh, encoding="utf-8")
    p.chmod(0o755)

print("Prompts e scripts gerados em", AG)
for f in sorted(AG.iterdir()):
    print(" ", f.name, f.stat().st_size, "bytes")
