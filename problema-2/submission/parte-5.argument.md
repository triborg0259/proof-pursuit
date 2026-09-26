Problem 2 — Part 5 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalisation,
the position with respect to the literature and what remains open. Nothing is declared proven beyond what is written.

1. Result and scope

Official request.

Parte 5 (C5) — Bounds for $U(Q_9)$

Punteggio: 8 points · Valutazione: Judged

$Q_9$ has $512$ vertices and $2304$ edges. The best bounds known to the organisers are
$$2368 \le U(Q_9) \le 2400;$$
the lower bound is unpublished. Improve either one: prove that $U(Q_9) \ge 2369$, or exhibit a labelling of $Q_9$
with at most $2399$ uphill paths.

What we submit. No improvement of the known bounds. Contribution: the star construction with an even code of distance 4 and size 20 gives exactly the known upper bound; proof that within this family one cannot go lower.

2. Proof

Star construction (see part 3): total $=(d+1)2^{d-1}-(d-1)|R|$ with $R$ an even code of distance 4. For $d=9$, $|R|\le A(8,3)=20$ and the minimum total of the family is $2560-160=2400$, i.e. the organisers' upper bound. Hence the known bound is (in all likelihood) precisely this construction, and improving it requires a forest of non-peaks that is not made of stars (larger trees, reducing the number of components below 96). Set up: search for independent sets $P$ of $Q_9$ with $|P|<236$ and acyclic complement; not executed.

3. Verification: instructions, dependencies, timings

Available code (Python 3, standard library; every script runs in under a minute):
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

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:1412.3893v1 — The competition between simple and complex evolutionary trajectories in asexual populations (Ian E. Ochs, Michael M. Desai, 2014); abstract only read.
No arXiv work on uphill paths on the hypercube: the problem appears to be unpublished.

5. Limits and unresolved parts

Both the lower and the upper bound.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:1412.3893v1 — The competition between simple and complex evolutionary trajectories in asexual populations (Ian E. Ochs, Michael M. Desai, 2014), found by query uphill paths; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c5.tex and in the repository.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c5.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
