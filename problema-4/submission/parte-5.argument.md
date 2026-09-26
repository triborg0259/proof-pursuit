Problem 4 — Part 5 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is declared proven beyond what is written.

1. Result and scope

Official request.

Parte 5 (C5) — The certified boundary

Punteggio: 8 points · Valutazione: Judged

The main certification cell: an initial range of sizes as long as you can make it, plus two isolated sizes
further out. Determine the largest $k$ for which you can certify the statement for all sizes up to and including
$k$, and certify it. The range you claim must be contiguous, and if your argument at a given size assumes that
all smaller sizes have already been settled you must say so. Then decide the two isolated sizes $k = 24$ and
$k = 30$: show that neither is the least size at which the statement can fail.

For this cell the exhaustiveness certificate of the hand-in rules is not enough on its own. Add:

(i) a demonstration that your method is not vacuous. Construct a case in which an admissible configuration
genuinely exists, run your machinery on it unmodified, and show it returns that configuration. A method that
reports "nothing survives" at every size it is pointed at is indistinguishable from a method with a bug, and will
be graded as one;

(ii) for every object your pruning leaves undecided, at every $k$ you claim — not a sample — an individual
decision, plus the smallest part of that object which already forces the decision, plus a proof that no smaller
part does;

(iii) the exact list, not merely the count, of what survives at each $k$;

(iv) every pruning rule you use beyond those you have proved, proved. If your search needs a rule you invented
to finish a size, that rule is part of your claim: state it, prove it, and show the survivor list is unchanged
when you switch it off. A size that only closes with an unproved rule is not certified;

(v) a second implementation, written independently of your first, that differs in method — not the same
algorithm twice — and the two survivor lists compared elementwise at every $k$ you claim. Report any difference
rather than reconciling it silently: a disagreement means one of them is wrong, and finding which is part of the
cell.

What we deliver. No certificate. Observation: for $k=24,30$ brute force on $L_k$ is impractical; a size-reduction argument is needed (if a counterexample exists at $k$, one exists at some $k'<k$).

2. Proof

Not developed.

3. Verification: instructions, dependencies, timings

Available code (Python 3, standard library; each script runs in under a minute):
- No code yet.

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); abstract only read.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); abstract only read.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); abstract only read.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); abstract only read.
As in part 3.

5. Limits and unresolved parts

Everything.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p4_c5.html (rendered), https://www.overleaf.com/docs?snip_uri=https://raw.githubusercontent.com/triborg0259/proof-pursuit/main/report/cells/p4_c5.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c5.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
