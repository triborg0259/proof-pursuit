# lean/ — Lean 4 + Mathlib per Proof Pursuit

Progetto Lake che fissa la versione di Lean e Mathlib usata per verificare le prove formali dei tentativi
(`lean-toolchain`, `lake-manifest.json`). La cartella `.lake/` (Mathlib compilata, circa 7 GB) non è versionata.

Installazione: `brew install elan-init`, poi qui dentro `lake exe cache get` (scarica Mathlib già compilata; non
compilarla da sorgente). Verifica di un file: `python3 tools/verifica_lean.py FILE.lean --teorema NOME` dalla radice del
repo. Dettagli nel README principale, sezione 10.
