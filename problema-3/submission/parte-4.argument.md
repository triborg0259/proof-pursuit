PROBLEM 3 — PART 4 — PARTIAL SUBMISSION DRAFT

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is declared proven beyond what is written.

1. RESULT AND SCOPE

Official request.

PART 4 (C4) — ONE ABOVE A TRIANGULAR NUMBER

Score: 5 points · Evaluation: Judged

The first family just above a triangular number: $n = T_{k-1} + 1$, that is $n = 11, 16, 22, 29, \ldots$ for
$k = 5, 6, 7, 8, \ldots$. Determine $D_B(T_{k-1} + 1)$ for every $k \ge 5$, with proof of both bounds.

What we deliver. No proof.

2. PROOF

Same plan as part 3 on the family $n=T_{k-1}+1$.

3. VERIFICATION: INSTRUCTIONS, DEPENDENCIES, TIMINGS

Available code (Python 3, standard library; each script runs in under a minute):
- No code yet.

4. SOURCES AND CONTRIBUTION

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); abstract only read.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); abstract only read.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); abstract only read.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); abstract only read.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); abstract only read.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); abstract only read.
As in part 3.

5. LIMITS AND UNRESOLVED PARTS

Everything.

6. HOW THIS RESULT WAS OBTAINED (MULTI-AGENT TRACE)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

6B. TOKENS USED BY THE AGENTS

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. ARXIV LITERATURE CONSULTED

- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022), found by query Bulgarian solitaire; abstract read, full text not relied upon.

8. CODE

The complete code, with the orchestrator's trusted re-runs, is in the write-up https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c4.tex and in the repository.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c4.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
