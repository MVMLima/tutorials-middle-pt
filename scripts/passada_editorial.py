#!/usr/bin/env python3
"""
Passada editorial final sobre os arquivos traduzidos:

1. substitui os marcadores `<!-- CONTEXTO-BR: ... -->` escolhidos por caixas "No Brasil"
   de verdade (conteúdo escrito pelo revisor, com fonte verificada);
2. remove os marcadores `CONTEXTO-BR` restantes e os `[verificar]` deixados pelos agentes;
3. corrige links relativos e inserções pontuais.

Para editar o conteúdo das caixas, mexa nas constantes abaixo.
"""
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent.parent

# Fontes usadas nas caixas (verificadas em 20/09/2026):
#  - Portal de Dados Abertos do SUS, conjunto SIVEP-Gripe (SRAG 2019-2026)
#  - SINAN, instrucional para download de microdados (dados preliminares x finais)
FONTE_SIVEP = ("[Portal de Dados Abertos do SUS — SIVEP-Gripe](https://dadosabertos.saude.gov.br/"
               "dataset/srag-2019-a-2026)")
FONTE_SINAN = ("[SINAN — instrucional para download de microdados]"
               "(http://portalsinan.saude.gov.br/images/documentos/Agravos/microdados/"
               "INSTRUCIONAL_PARA_DOWNLOAD_DE_MICRODADOS_DO_SINAN.pdf)")

CAIXAS = [
    # (arquivo, prefixo do marcador a substituir, caixa)
    ("episodios/01-acessar-atrasos.qmd",
     "<!-- CONTEXTO-BR: Na rotina de vigilância brasileira (SINAN e SIVEP-Gripe), registra-se",
     f"""::: {{.callout-note title="No Brasil: as datas que a vigilância registra"}}

Na rotina brasileira, o que se registra é a **data de primeiros sintomas** e a **data de
notificação/digitação** — não a data exata da infecção, que só costuma ser conhecida em
investigações específicas de surto. Para SRAG, o sistema oficial é o **SIVEP-Gripe**, cuja base é
publicada de forma aberta ({FONTE_SIVEP}).

É essa lacuna entre os dois momentos que faz o intervalo serial ser usado como aproximação do
tempo de geração.

:::"""),

    ("episodios/01-acessar-atrasos.qmd",
     "<!-- CONTEXTO-BR: No SUS, o tempo de permanência hospitalar",
     """::: {.callout-note title="No Brasil: tempo de permanência e desfecho"}

O tempo entre a internação e o desfecho alimenta diretamente o planejamento de leitos. No Brasil,
casos e óbitos por SRAG estão no **SIVEP-Gripe** e as internações em geral no **SIH/DATASUS**,
ambos com bases publicadas abertamente no [Portal de Dados Abertos do
SUS](https://dadosabertos.saude.gov.br/).

:::"""),

    ("episodios/02-quantificar-transmissibilidade.qmd",
     "<!-- CONTEXTO-BR: No Brasil, dados semelhantes de séries temporais de casos notificados",
     f"""::: {{.callout-note title="No Brasil: de onde vêm as séries de casos"}}

As séries usadas neste tipo de análise saem dos sistemas de notificação: o **SINAN** para os
agravos de notificação compulsória e o **SIVEP-Gripe** para casos e óbitos por SRAG. O SIVEP-Gripe
é o sistema oficial de registro da SRAG no país e tem base pública em {FONTE_SIVEP}.

Duas consequências práticas: os períodos mais recentes são **dados preliminares**, sujeitos a
revisão, e a consolidação leva tempo — é daí que vem a censura à direita nas últimas semanas da
série. Fonte sobre a diferença entre dados preliminares e finais: {FONTE_SINAN}.

:::"""),

    ("episodios/03-funcoes-de-atraso.qmd",
     "<!-- CONTEXTO-BR: No Brasil, o atraso de notificação pode ser calculado",
     f"""::: {{.callout-note title="No Brasil: medir o atraso de notificação"}}

Nas bases do SINAN e do SIVEP-Gripe, o atraso de notificação pode ser medido diretamente pela
diferença entre a data de primeiros sintomas e a data de notificação ou de digitação. Como as
últimas semanas ainda não foram consolidadas, esse atraso aparece como censura à direita — e é
exatamente o que este episódio ensina a representar como distribuição. Fonte: {FONTE_SINAN}.

:::"""),

    ("episodios/04-criar-previsoes.qmd",
     "<!-- CONTEXTO-BR: No Brasil, a subnotificação varia conforme o agravo",
     f"""::: {{.callout-note title="No Brasil: subnotificação e atraso de digitação"}}

A subnotificação varia muito conforme o agravo e o nível de atenção: casos leves podem passar fora
do sistema, enquanto internações por SRAG ficam registradas no SIVEP-Gripe ({FONTE_SIVEP}). Como a
base continua sendo atualizada, as semanas mais recentes ainda estão incompletas — e num modelo com
fator de escala isso se confunde facilmente com queda real de transmissão. Escolher o `scale` com
base em dados incompletos enviesa a previsão para baixo.

:::"""),

    ("episodios/04-criar-previsoes.qmd",
     "<!-- CONTEXTO-BR: O efeito de dia da semana é muito expressivo nas notificações",
     """::: {.callout-note title="No Brasil: efeito de dia da semana"}

Antes de ajustar o modelo, olhe o gráfico da sua série diária. Oscilação em "dente de serra" é
comum em bases de notificação e costuma vir de represamento de digitação em fins de semana e
feriados, seguido de concentração de lançamentos nos dias úteis.

O efeito de dia da semana do modelo existe justamente para absorver esse padrão. Conferir o
gráfico é o que diz se ele é necessário no seu caso — e um resíduo em dente de serra depois do
ajuste costuma indicar que o termo não foi suficiente.

:::"""),
]

# links/correções pontuais
SUBSTITUICOES = [
    # o agente deixou o caminho do glossário sem o ".." de subida de pasta
    ("episodios/01-acessar-atrasos.qmd", "](glossario.qmd#", "](../glossario.qmd#"),
]

# marcadores de trabalho dos agentes que saem no fim
MARCADOR_CONTEXTO = re.compile(r"[ \t]*<!--\s*CONTEXTO-BR:.*?-->\n?", re.S)
MARCADOR_VERIFICAR = re.compile(r"[ \t]*<!--\s*\[verificar[^>]*?-->\n?")
VERIFICAR_INLINE = re.compile(r"\s*<!--\s*\[verificar[^>]*?-->")


def main() -> None:
    for rel, prefixo, caixa in CAIXAS:
        p = P / rel
        txt = p.read_text(encoding="utf-8")
        linhas = txt.split("\n")
        achou = False
        for i, linha in enumerate(linhas):
            if linha.startswith(prefixo):
                linhas[i] = caixa
                achou = True
                break
        if not achou:
            print(f"FALHA: marcador nao encontrado em {rel}: {prefixo[:70]}")
            continue
        p.write_text("\n".join(linhas), encoding="utf-8")
        print(f"caixa inserida em {rel}")

    for rel, de, para in SUBSTITUICOES:
        p = P / rel
        txt = p.read_text(encoding="utf-8")
        if de not in txt:
            print(f"FALHA substituicao em {rel}: {de[:50]}")
            continue
        p.write_text(txt.replace(de, para), encoding="utf-8")
        print(f"substituicao aplicada em {rel}")

    alvos = sorted(P.glob("*.qmd")) + sorted(P.glob("episodios/*.qmd")) + sorted(P.glob("notas/*.qmd"))
    for p in alvos:
        txt = p.read_text(encoding="utf-8")
        novo = MARCADOR_CONTEXTO.sub("", txt)
        novo = MARCADOR_VERIFICAR.sub("", novo)
        novo = VERIFICAR_INLINE.sub("", novo)
        novo = re.sub(r"\n{3,}", "\n\n", novo)
        if novo != txt:
            p.write_text(novo, encoding="utf-8")
            print(f"marcadores removidos de {p.relative_to(P)}")


if __name__ == "__main__":
    main()
