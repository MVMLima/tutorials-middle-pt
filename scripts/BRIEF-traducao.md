# BRIEF — Tradução e adaptação PT-BR do tutorial Epiverse-TRACE "Middle tasks"

## Fonte
- Original (EN): https://epiverse-trace.github.io/tutorials-middle/ (Epiverse-TRACE, CC-BY 4.0)
- Repositório: https://github.com/epiverse-trace/tutorials-middle
- Arquivos de trabalho (já convertidos de Carpentries → Quarto): `_source/en-quarto/`

## Objetivo
Produzir a versão em português brasileiro do curso *Real-time analysis and forecasting for
outbreak analytics with R* (análise em tempo real e previsão para análise de surtos), para uso em
oficinas presenciais com epidemiologistas de vigilância.

## Regras invioláveis

1. **Não alterar código.** Nenhum token de código R pode mudar: funções, argumentos, nomes de
   objetos, strings, números, caminhos de arquivo, nomes de colunas. Só é permitido traduzir
   **comentários R** (linhas cujo conteúdo, ignorando espaços, começa com `#`).
2. **Não alterar saídas pré-impressas.** Blocos de saída de console, mensagens de erro e avisos do
   R permanecem em inglês, exatamente como o R os emite.
3. **Não alterar estrutura Quarto.** Mantenha todas as linhas `::: {.callout-...}` / `:::` como
   estão (os títulos já estão em português). Não crie, funda ou remova callouts. Mantenha uma
   linha em branco antes e depois de cada cerca `:::`.
4. **Não inventar.** Não acrescente números, datas, referências, DOIs, links, nomes de portarias
   ou dados que não estejam no original. Se algo estiver ambíguo, traduza literalmente e marque
   com `<!-- [verificar] -->` logo depois.
5. **Manter em inglês** (nome técnico, não se traduz): nomes de pacotes (`{EpiNow2}`,
   `{epiparameter}`, `{incidence2}`, `{cfr}`, `{outbreaks}`, `{epicontacts}`, `{superspreading}`,
   `{epichains}`, `{fitdistrplus}`, `{tidyverse}`), nomes de funções (`EpiNow2::epinow()`), nomes
   de colunas e valores de colunas, URLs, caminhos de arquivo, e os termos **linelist**, **Stan**,
   **MCMC**, **Rt**, **R0**, **CFR**, **IFR**, **delay**, **epiweek**.
6. **Escrita matemática intacta**: não toque em nada entre `$...$`, `$$...$$`, `\\(...\\)` nem
   nos identificadores de âncora `{#algumacoisa}`.
7. **Tom.** Português brasileiro técnico, direto, como um epidemiologista explicando para outro.
   Sem floreio, sem "vamos mergulhar", sem "poderoso". Trate o leitor por "você".
8. **Links internos**: mantenha os destinos como estão (já apontam para os arquivos do site PT).

## Termbase (use consistentemente)

| Inglês | Português |
|---|---|
| outbreak | surto |
| outbreak analytics | análise de surtos |
| real-time analysis | análise em tempo real |
| delay distribution | distribuição de atraso |
| generation time | tempo de geração |
| serial interval | intervalo serial |
| incubation period | período de incubação |
| infectious period | período de infecciosidade |
| latent period | período latente |
| presymptomatic | pré-sintomático |
| reporting delay | atraso de notificação |
| right-truncation / right-censoring | truncamento à direita / censura à direita |
| double censoring | dupla censura |
| discretised | discretizada |
| parameterised / non-parameterised | parametrizada / não parametrizada |
| summary statistics | estatísticas resumo |
| distribution parameters | parâmetros da distribuição |
| probability distribution | distribuição de probabilidade |
| credible interval | intervalo de credibilidade |
| confidence interval | intervalo de confiança |
| prior / posterior / likelihood | priori / posteriori / verossimilhança |
| reproduction number | número de reprodução |
| effective reproduction number | número de reprodução efetivo |
| basic reproduction number | número de reprodução básico |
| growth rate | taxa de crescimento |
| doubling time | tempo de duplicação |
| case fatality risk (CFR) | risco de letalidade (CFR) |
| infection fatality ratio (IFR) | razão de letalidade por infecção (IFR) |
| severity | gravidade |
| hospitalisation | internação |
| superspreading | superspreading |
| superspreading event (SSE) | evento de superdisseminação (SSE) |
| offspring distribution | distribuição de casos secundários |
| transmission chain | cadeia de transmissão |
| secondary cases | casos secundários |
| contact tracing | rastreamento de contatos |
| backward / forward tracing | rastreamento retrospectivo / prospectivo |
| cluster | aglomerado |
| forecast | previsão |
| short-term forecast | previsão de curto prazo |
| nowcast | nowcast (estimativa do presente) |
| projection | projeção |
| renewal equation | equação de renovação |
| delay-adjusted | ajustado pelo atraso |
| naive estimate | estimativa ingênua |
| case data | dados de casos |
| linelist | linelist |
| to estimate | estimar |
| estimate (substantivo) | estimativa |
| uncertainty | incerteza |
| to account for / to adjust for | levar em conta / corrigir para |
| to inform | orientar |
| schedule / timing | cronograma / momento |
| workshop | oficina |
| Challenge | Desafio |
| Solution | Solução |
| Hint | Dica |
| Key points | Pontos-chave |
| checklist | checklist |
| you can | você pode |

## Ambiente (adaptação ao contexto brasileiro)
- Onde o original diz **RStudio**, escreva **Positron (ou RStudio, se preferir)** na primeira
  menção de cada arquivo e apenas **Positron** nas seguintes. Não reescreva capturas de tela nem
  menus que só existem no RStudio — nesses casos mantenha RStudio e não invente equivalente.
- Onde o original ensina a instalar pacotes, você pode acrescentar a menção ao espelho brasileiro
  do CRAN — use **exatamente** esta linha, sem alterar o resto:
  `options(repos = c(CRAN = "https://cran-r.c3sl.ufpr.br/"))`.
- **Não** crie blocos de contexto brasileiro por conta própria. Quando perceber um ponto onde
  caberia uma ligação com a prática brasileira (SINAN, SIVEP-Gripe, DATASUS, e-SUS, semana
  epidemiológica, rotina de vigilância), deixe um comentário na linha exata, neste formato:
  `<!-- CONTEXTO-BR: sugestão curta do que caberia aqui -->`
  O revisor (agente pai) decide e escreve o texto final desses boxes.

## Entrega
- Arquivo de saída no caminho indicado no prompt do seu agente, em UTF-8.
- Ao terminar, informe: caminho absoluto, número de linhas (`wc -l`) e a lista de marcações
  `<!-- [verificar] -->` e `<!-- CONTEXTO-BR: ... -->` que você deixou.
