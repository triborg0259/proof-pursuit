Problem 3 — Part 5 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature and what remains open. Nothing is claimed as proven beyond what is written.

1. Result and scope

Official request.

Parte 5 (C5) — Two above a triangular number

Punteggio: 8 points · Valutazione: Judged

The next family: $n = T_{k-1} + 2$, that is $n = 3, 5, 8, 12, 17, 23, \ldots$ for $k = 2, 3, 4, 5, 6, 7, \ldots$.
Determine $D_B(T_{k-1} + 2)$ for every $k$, with proof of both bounds. State exactly for which $k$ your formula
holds, and give the remaining values separately. Your upper bound must be a single argument valid for all $k$ in
that range, not a separate treatment of each $k$, and you must give the extremal partitions explicitly as a
function of $k$.

Say also where the straightforward extension of the C3 argument stops: give the bound it does yield, show it is
strictly weaker than the truth, and identify precisely what your proof supplies in its place.

What we submit. No proof.

2. Proof

Same plan; the cell requires a single uniform argument and the analysis of where the extension of part 3 stops.

2b. Exact finite verification (computed 2026-09-26, integer arithmetic, 8 s for all n up to 56)

Script: problema-3/esperimenti/tabella_DB.py (functional graph on all partitions of $n$, cycles marked, $d_B$ by memoised orbit following); output in tabella_DB.txt. This is VERIFIED ON A FINITE RANGE, not a proof for general $k$.
For every rank $7\le k\le 10$ the exact value is $D_B(T_{k-1}+2)=k^2-5k+4=(k-1)(k-4)$ (values 18, 28, 40, 54). The formula fails for small $k$, where the residual values are $D_B(3)=$ see table ($k=2$), $D_B(5)=3$ ($k=3$), $D_B(8)=5$ ($k=4$), $D_B(12)=8$ ($k=5$), $D_B(17)=12$ ($k=6$). Conjectured: $D_B(T_{k-1}+2)=k^2-5k+4$ for all $k\ge7$, residual values as listed for $k\le6$. The straightforward extension of the cell-3 bound gives only $k^2-2k-1$, strictly weaker.

Values for the family $n=T_{k-1}+2$:
- k=4, n=8: D_B(n)=5; extremal partitions: 1, e.g. (1, 1, 1, 1, 1, 1, 1, 1)
- k=5, n=12: D_B(n)=8; extremal partitions: 2, e.g. (3, 3, 2, 2, 1, 1)
- k=6, n=17: D_B(n)=12; extremal partitions: 1, e.g. (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)
- k=7, n=23: D_B(n)=18; extremal partitions: 66, e.g. (5, 5, 4, 3, 3, 2, 1)
- k=8, n=30: D_B(n)=28; extremal partitions: 253, e.g. (6, 6, 5, 4, 3, 3, 2, 1)
- k=9, n=38: D_B(n)=40; extremal partitions: 1341, e.g. (7, 7, 6, 5, 4, 3, 3, 2, 1)
- k=10, n=47: D_B(n)=54; extremal partitions: 6335, e.g. (8, 8, 7, 6, 5, 4, 3, 3, 2, 1)

3. Verification: instructions, dependencies, timings

Available code (Python 3, standard library; every script runs in under a minute):
- No code yet.

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); abstract only read.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); abstract only read.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); abstract only read.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); abstract only read.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); abstract only read.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); abstract only read.
As in part 3.

5. Limits and unresolved parts

Everything.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022), found by query Bulgarian solitaire; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p3_c5.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp3_c5.tex&snip_name=p3_c5.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c5.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
