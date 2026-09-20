# Análise em tempo real e previsão para surtos com R — adaptação PT-BR

Site do curso **Análise em tempo real e previsão para surtos com R: atrasos, número de reprodução,
previsão, gravidade e superspreading**, adaptação para o português brasileiro do tutorial
*Epiverse-TRACE Tutorials Middle*.

**Site publicado:** https://mvmlima.github.io/tutorials-middle-pt/

## O que tem aqui

| Arquivo | Conteúdo |
|---|---|
| `index.qmd` | Página inicial: sobre o curso, público, pré-requisitos |
| `setup.qmd` | Preparação do ambiente (R, ferramentas de compilação, pacotes, projeto do R) |
| `episodios/01-acessar-atrasos.qmd` | Buscar distribuições de atraso na literatura com `{epiparameter}` |
| `episodios/02-quantificar-transmissibilidade.qmd` | Estimar $R_t$ e taxa de crescimento com `{EpiNow2}` |
| `episodios/03-funcoes-de-atraso.qmd` | Combinar, discretizar e comparar distribuições de atraso |
| `episodios/04-criar-previsoes.qmd` | Previsão de curto prazo de casos e óbitos |
| `episodios/05-severidade-estatica.qmd` | Risco de letalidade (CFR) bruto e corrigido pelo atraso |
| `episodios/06-superspreading-estimar.qmd` | Distribuição de casos secundários e risco de aglomerados |
| `episodios/07-superspreading-simular.qmd` | Simulação de cadeias de transmissão com `{epichains}` |
| `notas/equacao-de-renovacao.qmd` | Nota teórica: como os atrasos entram na estimativa de $R_t$ |
| `notas/ajuste-cfr-atrasos.qmd` | Nota teórica: por que o CFR bruto engana no meio do surto |
| `glossario.qmd` | Glossário de termos |
| `perfis.qmd` | Personas de aprendiz do treinamento |
| `instrutor.qmd` | Notas e plano de aula para quem conduz a oficina |
| `licenca.qmd` | Licença e créditos |
| `data/` | Arquivos de dados usados no curso (também baixáveis pelo site) |
| `img/` | Figuras do material original |
| `_source/` | Arquivos originais em inglês (formato Carpentries), mantidos para conferência |

## Como renderizar localmente

Requisitos: [Quarto](https://quarto.org/) 1.8+ e R 4.2+.

```bash
# 1. pacotes do curso numa biblioteca local do projeto (não mexe na biblioteca global do R)
Rscript scripts/instalar_pacotes.R

# 2. renderizar
quarto render
```

O site sai em `_site/`. Para pré-visualizar com recarregamento automático: `quarto preview`.

O `_quarto.yml` usa `execute: freeze: auto`, então os resultados dos blocos de código ficam
guardados em `_freeze/` e o build no GitHub Actions **não precisa do R nem dos pacotes**. Se
você alterar o **código** de um `.qmd`, renderize localmente de novo e commite o `_freeze/`
atualizado junto com o arquivo.

> **Tempo de execução:** os episódios que rodam `EpiNow2::epinow()` fazem inferência bayesiana por
> MCMC. Espere alguns minutos por ajuste; o render completo é demorado por isso.

## Publicação

O workflow `.github/workflows/publish.yml` renderiza o site e publica na branch `gh-pages` a
cada push na `main`. O GitHub Pages serve a partir dessa branch.

## Verificação da tradução

```bash
python3 scripts/verificar_traducao.py
```

Compara cada episódio traduzido com o original convertido (`_source/en-quarto/`) e aponta: blocos
de código que foram alterados, callouts perdidos, links internos quebrados e imagens ausentes.

## Como a versão PT-BR foi produzida

1. `scripts/convert_carpentries.py` converte as lições do formato Carpentries Workbench (divs
   cercados com `::::`) para o formato Quarto (callouts), ajustando caminhos de dados, imagens e
   links internos.
2. Nove agentes tradutores (CLI `agy`) traduzem e adaptam cada episódio seguindo
   `scripts/BRIEF-traducao.md` (termbase e regras: código intocado, nada inventado).
3. `scripts/passada_editorial.py` insere as caixas de contexto brasileiro e remove os marcadores
   de trabalho.
4. `scripts/verificar_traducao.py` confere a integridade do código.

## Licença

O material original é publicado sob [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Esta adaptação é publicada sob a **mesma licença**. Créditos completos em `licenca.qmd`.

Citação do original:

> Valle-Campos A, Minter A, Degoot A, Gruson H, Bah B, Eggo R, Funk S, Kucharski A (2026).
> *Epiverse-TRACE Tutorials Middle: Real-time analysis and forecasting for outbreak analytics
> with R.* DOI: [10.5281/zenodo.21512003](https://doi.org/10.5281/zenodo.21512003)
