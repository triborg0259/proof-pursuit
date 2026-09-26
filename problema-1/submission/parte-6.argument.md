Problem 1 — Part 6 — PARTIAL submission draft

Declared status: PARTIAL. No complete solution: below is what has been established, the formalization,
the position with respect to the literature and what remains open. Nothing is declared proved beyond what is written.

1. Result and scope

Official request.

Parte 6 — $N$ lines in $\mathbb{R}^d$

Punteggio: 13 points · Valutazione: Judged · Open question

Fejes Tóth's conjecture from the Setting, for every $N$ and every $d$. For $N$ lines in $\mathbb{R}^d$, write
$N = qd + s$ with $0 \le s < d$, and let
$$M(N,d) = s \binom{q+1}{2} + (d-s) \binom{q}{2}.$$
Prove or disprove: every $N$ lines in $\mathbb{R}^d$ satisfy
$$S \;\le\; \left( \binom{N}{2} - M(N,d) \right) \frac{\pi}{2}.$$
This is the value attained by splitting the lines as evenly as possible among $d$ mutually orthogonal
directions. Settling any infinite family not already covered above counts as partial progress.

(End of problem 1. Scores: 1+2+3+5+8+13 = 32.)

What we submit. Open problem. No new infinite family. Contribution: numerical verification of the bound for $N\le10$ in the plane (harness) and setup of the counterexample search.

2. Proof

Full Fejes Tóth conjecture. With the numerical harness (tools/autoloop.py, hill climbing with restarts) the maximum found coincides with the conjectured value within $2\cdot10^{-5}$ for all cases tested; no exceedance. This is not a proof (floating point).

3. Verification: instructions, dependencies, timings

Code available (Python 3, standard library; each script runs in under one minute):
- problema-1/esperimenti/lines_Rd.py
- problema-1/esperimenti/p1_somma_angoli.py

4. Sources and contribution

arXiv literature (deterministic search tools/cerca_letteratura.sh, abstracts read, not used as proof):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); abstract only read.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); abstract only read.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); abstract only read.
Bilyk–Matzke [1801.07837]: general bound via energy and reduction from high to low dimension; Lim–McCann [2007.08698]: equivalence with the uniqueness of the optimizer for every $\alpha>1$, proved for $\alpha=\infty$.

5. Limits and unresolved parts

Everything.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family reduction, subgoal: Establish rigorous, reusable reduction lemmas between instances FT(N,d) of the conjecture (add a line, remove a line, drop one dimension), settle the (trivial) infinite family N ≤ d not covered by cells 1–5, and record a float-only counterexample search in R^3..R^6.; declared LEMMA_CANDIDATE.
  - Why this approach: No blocker and no verified claims exist for this cell; cell 6 is an open problem and asks for infinite families beyond cells 1–5. A frontal attack (e.g. N = 2d) is out of reach in one iteration, and the frame-potential/Gram approach is known (Bilyk–Matzke) to be non-sharp. The best first step is to build the exact 'transfer' machinery: which instances of the conjecture imply which others. These lemmas are cheap, fully rigorous, reusable by later iterations (any future family proved for N ≡ −1 mod d extends to N+1; any family in R^d transfers down a dimension), and they immediately give a new finite case ((6,3) from cell 4). I also record honestly the trivial family N ≤ d, and a float-only search giving no counterexample, since the cell says 'prove or disprove'.
  - Position w.r.t. the literature: [1801.07837] Bilyk–Matzke (read in full by the team earlier, see problema-1/fonti/README.md): the only settled case is the plane; they give a general non-sharp energy bound π/2 − 69/(50(d+1)) via the frame potential and, for the continuous (measure) version, a dimension-reduction Prop. 3.1 (conjecture in S^d ⟹ conjecture in S^{d−1}). Lemma 4 below is the finite-N analogue of that reduction, proved from scratch by embedding and adding q copies of a new orthogonal axis; the exact identity M(N+q,d) = M(N,d−1) + C(q,2) is what makes it sharp for finite N. Lemmas 2–3 (averaging over deleting/duplicating a line) do not appear in the abstracts and are our own. [2007.08698] Lim–McCann (abstract only): deformation to α-powers, optimality for α = ∞; not used. [1204.3850] is irrelevant (polygon mapping). Nothing in the literature I have settles any new infinite family; my approach departs from the energy method (known non-sharp) and instead builds exact transfer lemmas.
  - Referee: REJECT / NEEDS_WORK; fatal error: The only declared claim is main (Fejes Tóth's bound for all N, d). The submission explicitly states in §8 that no non-trivial infinite family is proved and that cell 6 remains open; Lemmas 0–4 and Corollaries 5–6 are conditional transfer statements (FT(N,d) ⇒ FT(N+1,d) for s=d−1; FT(N+1,d) ⇒ FT(N,d) for d | N; FT(N+q',d) ⇒ FT(N,d−1)) whose hypotheses are themselves the unproved conjecture. None of them, alone or combined with cells 1–5 (which are moreover not verified in the state: highest_verified_cell = 0), yields FT(N,d) for any family beyond the trivial N ≤ d / d = 1 case. Hence the declared target is not established, and no other declared claim exists to accept. The float search of §7 is exploration only and proves nothing (correctly acknowledged by the author).; next: Address the stated blocking obligation without silently changing the target

6b. Tokens used by the agents

- Researcher attempt_001: input 638,915 · output (incl. reasoning) 26,403
- Referee judge A: input 33,430 · output (incl. reasoning) 2,241
- Referee judge B: input 33,467 · output (incl. reasoning) 2,783
- Referee judge B: input 35,113 · output (incl. reasoning) 1,828
- Total: input 740,925 · output 33,255 tokens

7. arXiv literature consulted

- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018), found by query angles between lines; abstract read, full text not relied upon.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020), found by query angles between lines; abstract read, full text not relied upon.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012), found by query angles between lines; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p1_c6.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp1_c6.tex&snip_name=p1_c6.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p1_c6.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
