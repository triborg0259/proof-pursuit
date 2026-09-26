#!/bin/bash
# Traduce in inglese ogni bozza problema-N/submission/parte-K.md → parte-K.en.md con `claude -p` (nessuno strumento).
# Formule LaTeX, codice, numeri e struttura delle sezioni restano identici. Uso: tools/traduci_submission.sh [file...]
cd "$(dirname "$0")/.."
PROMPT='Translate the following Markdown document from Italian to English. Keep EXACTLY: all LaTeX/math, code blocks, inline code, numbers, file paths, section numbering and Markdown structure. Translate only the prose. Keep the labels of the five sections as: "## 1. Result and scope", "## 2. Proof", "## 3. Verification: instructions, dependencies, timings", "## 4. Sources and contribution", "## 5. Limits and unresolved parts". Return ONLY the translated Markdown, no preamble.'
FILES=${@:-$(ls problema-*/submission/parte-?.md)}
for f in $FILES; do
  out=${f%.md}.en.md
  ( claude -p --tools "" --no-session-persistence --output-format text --model claude-fable-5-1 --effort low --max-budget-usd 2 "$PROMPT

$(cat "$f")" > "$out.tmp" 2>/dev/null && mv "$out.tmp" "$out" && echo "ok $out" || echo "ERRORE $f" ) &
done
wait
