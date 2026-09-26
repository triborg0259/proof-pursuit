PROBLEM 2 — PART 6 — PARTIAL SUBMISSION DRAFT

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is claimed as proved beyond what is written.

1. RESULT AND SCOPE

Official request.

PART 6 (C6) — $U(Q_9)$

Score: 13 points · Evaluation: Judged · Open question

The same cube, settled completely. Determine $U(Q_9)$ exactly, with proof of both bounds.

(End of problem 2. Scores: 1+2+3+5+8+13 = 32.)

What we submit. Open problem. No contribution beyond part 5.

2. PROOF

See part 5: the exact value requires both bounds; for the lower bound the excess identity $T=|E|+v+X$ (part 2) is the tool, but the case analysis does not scale to 512 vertices without a structural argument.

3. VERIFICATION: INSTRUCTIONS, DEPENDENCIES, TIMINGS

Available code (Python 3, standard library; every script runs in under one minute):
- problema-2/certificati/costruzione_88.py
- problema-2/certificati/q3_esaustivo.py
- problema-2/certificati/q3_verifica_indipendente.py
- problema-2/certificati/q4_branch_and_bound.py
- problema-2/certificati/q4_ricerca_locale.py
- problema-2/certificati/q4_verifica_etichettatura_indipendente.py
- problema-2/certificati/q5_stella_verifica_indipendente.py
- problema-2/certificati/verifica_dfs_88.py
- problema-2/certificati/verifica_etichettatura_q3.py
- problema-2/certificati/verifica_etichettatura_q4.py
- problema-2/certificati/verifica_q5_bipartita.py
- problema-2/certificati/verifica_q5_indipendenti.py
- problema-2/esperimenti/conta_cammini.py
- problema-2/esperimenti/costruzione_stelle.py
- problema-2/esperimenti/ricottura_controllo.py

4. SOURCES AND CONTRIBUTION

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:1412.3893v1 — The competition between simple and complex evolutionary trajectories in asexual populations (Ian E. Ochs, Michael M. Desai, 2014); abstract only read.
None.

5. LIMITS AND UNRESOLVED PARTS

Everything.

6. HOW THIS RESULT WAS OBTAINED (MULTI-AGENT TRACE)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

6B. TOKENS USED BY THE AGENTS

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. ARXIV LITERATURE CONSULTED

- arXiv:1412.3893v1 — The competition between simple and complex evolutionary trajectories in asexual populations (Ian E. Ochs, Michael M. Desai, 2014), found by query uphill paths; abstract read, full text not relied upon.

8. CODE

The complete code, with the orchestrator's trusted re-runs, is in the write-up https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c6.tex and in the repository.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c6.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
