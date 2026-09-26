Problem 4 — Part 4 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is claimed as proved beyond what is written.

1. Result and scope

Official request.

Parte 4 (C4) — Every $k$ up to 12

Punteggio: 5 points · Valutazione: Judged

A longer range, and a precise account of your method at the sizes just beyond it. Prove the statement for every
$k \le 12$. Then, for each $k$ from $9$ to $16$ in turn, report exactly what your method leaves undecided at that
$k$: if nothing, say so and prove it; if something, exhibit it in full. If that disagrees with any source you
consulted, say which of the two is right and why. An answer that reports agreement with a source it did not test
will be marked wrong.

What we deliver. As in part 3, extended to $k\le12$ ($L_{12}=27720$, 96 divisors); not executed.

2. Proof

Same reduction and same search scheme; the report on the cases $9\le k\le16$ requires listing the survivors of the pruning without deciding them by unproved rules.

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

Everything except the reduction.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family exact_computation, subgoal: Prove the statement for every k ≤ 12 (and k = 13) by a certified finite search: reduction lemma (moduli = lcm of gcds, no minimality needed) + Huhn–Megyesi density criterion with all admissible M + residue stage; report exactly what is left undecided for k = 9..16.; declared CELL_SOLVED_CANDIDATE.
  - Why this approach: First natural subgoal of the cell (no blocker). Cell 3's approved method (clique search on classes mod 420) does not scale to L_12 = 27720 (112 320 classes). The modulus-level density criterion is far stronger: with all admissible M it kills everything at k ≤ 12 in 15 s and leaves one tuple at k = 13, which the residue stage decides. No minimality of k is assumed for k ≤ 13.
  - Position w.r.t. the literature: Fornal–Sun arXiv:2607.24655 (read in full via the PDF): asymptotic bound max gcd ≫ k·exp(−(2+o(1))√(log k/log log k)); their Lemma 4.1 is asymptotic and gives nothing at fixed small k; they cite O'Bryant for k ≤ 20. O'Bryant, arXiv:math/0604347v2 (read in full): proves the statement for k ≤ 20 and that a minimal counterexample has k ∉ {24,30}, using a modulus-only method: Lemma 5 (= our Lemma B, stated with the Huhn–Megyesi reference), Lemma 6 (items 1–8, several requiring minimality of k and of Σm_i) and a week-long Mathematica search 'Grow' for k ≤ 19 applying Lemma 5 only with M = lcm of the gcds of each subset. Our method ADAPTS his: (i) Lemma A gives his items 1 and 3 without any minimality assumption; (ii) Lemma B is applied with ALL divisors M of L_k that are multiples of the gcd-lcm (strictly stronger pruning; his whole k ≤ 19 search is replaced by seconds); (iii) we add a residue stage, which is needed: at k = 13 the modulus-only rules (R1)–(R3) leave one tuple, and so do the rules with his items 4–5 added (tested: 669 090 nodes, same single survivor). Tested agreement with O'Bryant: k ≤ 12 both give 'no counterexample'; at k = 13 we could not reproduce a modulus-only refutation of (10,10,10,10,10,12,12,12,12,24,36,40,45) from his paper (we did not run his code), but our stage B decides it, so nothing we claim depends on him. Abstracts 2603.26043, 1511.04293 (disjoint covering systems) and 2608.15873 (group form, tuple (6,6,6,10,15)) are not relevant to this cell.
  - Referee: UNKNOWN_STATUS / INCOMPLETE; next: Provide the missing review or independently checked evidence

6b. Tokens used by the agents

- Referee judge B: input 41,396 · output (incl. reasoning) 4,612
- Referee judge A: input 40,888 · output (incl. reasoning) 7,105
- Total: input 82,284 · output 11,717 tokens

7. arXiv literature consulted

- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p4_c4.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp4_c4.tex&snip_name=p4_c4.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c4.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
