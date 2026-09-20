#!/usr/bin/env bash
# Dispara os 9 agentes tradutores em paralelo e espera todos terminarem.
cd "$(dirname "$0")/.." || exit 1
for n in 01 02 03 04 05 06 07 08 09; do
  bash "_work/agents/run-${n}.sh" &
done
wait
echo "=== todos os agentes terminaram ==="
for n in 01 02 03 04 05 06 07 08 09; do
  printf "%s: " "$n"; tail -1 "_work/agents/log-${n}.txt" 2>/dev/null || echo "sem log"
done
