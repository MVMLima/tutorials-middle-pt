# Biblioteca R local do projeto (criada por `pak::pkg_install(..., lib = ".Rlib")`).
# Assim os pacotes do curso não se misturam com a biblioteca global do R.
local({
  lib <- file.path(getwd(), ".Rlib")
  if (dir.exists(lib)) .libPaths(c(lib, .libPaths()))
})
