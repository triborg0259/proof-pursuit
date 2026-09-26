#!/bin/sh
# Rende in HTML (con formule via MathJax) tutti i .md del progetto, in _html/ (stessa struttura).
# Uso: sh tools/render.sh   → poi apri _html/index.html nel browser
set -e
cd "$(dirname "$0")/.."
mkdir -p _html
: > _html/index.md
find . -name '*.md' -not -path './_html/*' -not -name 'CLAUDE.md' | sort | while read f; do
  rel="${f#./}"; out="_html/${rel%.md}.html"; mkdir -p "$(dirname "$out")"
  pandoc "$f" -s --mathjax -o "$out" --metadata title="$rel" 2>/dev/null
  echo "- [$rel](${rel%.md}.html)" >> _html/index.md
done
pandoc _html/index.md -s -o _html/index.html --metadata title="Proof Pursuit"
rm _html/index.md
echo "ok → _html/index.html"
