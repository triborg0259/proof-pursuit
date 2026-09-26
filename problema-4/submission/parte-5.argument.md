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
- attempt_001 — Researcher: family contradiction, subgoal: Prove the "two isolated sizes" half of cell 5: if the statement holds for every size s < k, then it holds for k = 24 and for k = 30 (so neither is the least size at which it can fail). Full hand proof, no computer search needed.; declared LEMMA_CANDIDATE.
  - Why this approach: No blocker and no failed attempts are recorded. Cell 5 has two independent halves: (A) a strengthened computational certificate for a contiguous range, and (B) deciding the isolated sizes 24 and 30. Half (B) is a pure-mathematics statement with a short complete proof, so it is the natural first subgoal: it is checkable by a hostile reader with no code, it is reusable (Lemmas 1, 3, 4, 6 are exactly the proved pruning rules the range search will need), and it also settles the "compare with the source" duty, since I found that O'Bryant's published argument for k=30 (arXiv:math/0604347v2, Lemma 6 item 8) has a step that does not follow as written and I replace it. The colleague loop on cell 4 already has a modulus-stage search that finishes k≤13 but times out at k=14 (runs/p4_c4/sandbox), so the range half needs a new search design; that is the next iteration, not this one.
  - Position w.r.t. the literature: The listed abstracts do not touch this cell directly: [2607.24655] (Fornal–Sun) is the asymptotic bound max gcd ≫ k·exp(−(2+o(1))√(log k/log log k)) — relevant to C6(b) only; [2608.15873] (Menon) is the group form C6(c); [2603.26043] and [1511.04293] are about disjoint covering systems with a repeated modulus. Not listed by the search but found and READ IN FULL (downloaded from arxiv.org/pdf/math/0604347v2, text extracted): K. O'Bryant, "On Z.-W. Sun's disjoint congruence classes conjecture" (2006), Theorem 3: "The DCCC holds for k ≤ 20. Moreover, a counterexample to the DCCC with minimal k does not have k ∈ {24, 30}." His route for 24 and 30 is: item 5 (a minimal counterexample has ≥3 multiples of k−1) contradicts item 8 (for 7 ≤ k ≤ 30 a prime p ≥ k/2 divides exactly 0 or 2 moduli). My proof FOLLOWS his overall strategy (items 4, 5, 8 re-proved here from scratch, with our own Lemma 3/4 replacing his pigeonhole-on-residues paragraph) but DEPARTS at the k=30 end-game: his text says "each of the 27 possible values of ω must actually occur: |P1|=|P2|=|P3|=3. Thus two of the four primes 17, 19, 23, 29 are in separate Pi's" — with p=29 the three primes 17,19,23 could all lie in the same P_j, so that sentence does not follow from what precedes it. I close the gap with a different argument (cross products of primes from different P_j must be ≤ 29, forcing seven primes into one 3-element set). Also, unlike his Lemma 6 I never use minimality of Σm_i. Nothing from the paper is used as a hypothesis; the whole proof is written out. His k ≤ 20 claim (a week of Mathematica in 2006) is CITED only, not used and not reproduced.
  - Referee: REJECT / NEEDS_WORK; fatal error: The declared target 'main' is the whole of cell 5: (A) determine and certify the largest contiguous range k ≤ K with the strengthened certificate (i)–(v) [non-vacuity demonstration, individual survivor decisions with minimal forcing part, exact survivor lists, all pruning rules proved and tested off, second independent implementation compared elementwise], and (B) show that neither k=24 nor k=30 is the least failing size. The submission addresses only (B): it proves 'S(s) for all 2≤s<k ⇒ S(k)' for k∈{24,30}. Nothing in the submission determines a contiguous certified range, and no certificate components (i)–(v) are present; the state also carries no previously verified claims (highest_verified_cell=0) that the argument could lean on. The only declared claim is 'main', so no declared claim is established and PARTIAL is unavailable. The argument for (B) contains no invalid inference (see math_notes) and should be re-declared as its own claim.; next: Address the stated blocking obligation without silently changing the target

6b. Tokens used by the agents

- Researcher attempt_001: input 781,965 · output (incl. reasoning) 39,242
- Referee judge A: input 37,838 · output (incl. reasoning) 4,568
- Referee judge B: input 38,346 · output (incl. reasoning) 4,239
- Total: input 858,149 · output 48,049 tokens

7. arXiv literature consulted

- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p4_c5.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp4_c5.tex&snip_name=p4_c5.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c5.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
