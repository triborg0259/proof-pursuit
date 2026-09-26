#!/bin/bash
# Esegue TUTTE le suite del repo in un colpo: nostre (tests/), Referee (referee/tests), Creative (creative/tests).
# Nessuna chiamata a modelli: tutto offline o con backend finti. Uso: tools/run_tests.sh
set -e
cd "$(dirname "$0")/.."
PY=.venv/bin/python
for t in tests/test_researcher.py tests/test_bridge_referee.py tests/test_loop.py tests/test_b_referee.py; do
  echo "== $t"; $PY "$t" | grep -c '^ok' | sed 's/^/   test ok: /'
done
echo "== referee/tests";  (cd referee && ../$PY -m unittest discover -s tests -q 2>&1 | tail -1)
echo "== creative/tests"; $PY -m unittest discover -s creative/tests -p 'test_*.py' -q 2>&1 | tail -1
