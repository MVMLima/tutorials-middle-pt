#!/usr/bin/env Rscript
# Instala os pacotes do curso numa biblioteca LOCAL do projeto (.Rlib).
# Usa o Posit Package Manager (binários para Ubuntu noble) quando disponível.
P <- "/home/marc/Documentos/Projetos/tutorials-middle-pt"
lib <- file.path(P, ".Rlib")
dir.create(lib, showWarnings = FALSE)

options(
  repos = c(CRAN = "https://packagemanager.posit.co/cran/__linux__/noble/latest"),
  HTTPUserAgent = sprintf(
    "R/%s R (%s)", getRversion(),
    paste(getRversion(), R.version$platform, R.version$arch, R.version$os)
  ),
  Ncpus = max(1, parallel::detectCores() - 2)
)
cat("R:", R.version.string, "\nlib:", lib, "\nNcpus:", getOption("Ncpus"), "\n")

pkgs <- c(
  # núcleo
  "EpiNow2", "epiparameter", "incidence2", "tidyverse",
  # severidade / forecast
  "cfr", "outbreaks",
  # superspreading / cadeias
  "epicontacts", "fitdistrplus", "superspreading", "epichains",
  # utilidades usadas nos episódios
  "here", "gt", "cowplot", "scales", "latex2exp", "patchwork",
  "socialmixr", "visNetwork", "magrittr", "withr", "readr", "stringr",
  "tidyr", "purrr", "tibble", "dplyr", "ggplot2", "webshot"
)

install.packages(pkgs, lib = lib, dependencies = TRUE, quiet = FALSE)

cat("\n=== instalados em .Rlib:", length(list.files(lib)), "===\n")
faltando <- pkgs[!pkgs %in% rownames(installed.packages(lib.loc = lib))]
cat("FALTANDO:", if (length(faltando)) paste(faltando, collapse = ", ") else "nenhum", "\n")
