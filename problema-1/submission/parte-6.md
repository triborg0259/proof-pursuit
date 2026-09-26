# Problem 1 — Part 6 — submission (PARTIAL)

**Declared status: PARTIAL.** The cell is not solved. What follows is the intermediate progress actually established,
as judged by the automatic Referee (verdict `REJECT`: The only declared claim is `main` (Fejes Tóth's bound for all N, d). The submission explicitly states in §8 that no non-trivial infinite family is proved and that cell 6 remains open; Lemmas 0–4 and Corollaries 5–6 are conditional transfer statements (FT(N,d) ⇒ FT(N+1,d) for s=d−1; FT(N+1,d) ⇒ FT(N,d) for d | N; FT(N+q',d) ⇒ FT(N,d−1)) whose hypotheses are themselves the unproved conjecture. None ).
The author's own declared status was `LEMMA_CANDIDATE`.

## 1. Result and scope
Rigorous, self-contained proofs of: (i) exact identities for M(N,d); (ii) the trivial infinite family N ≤ d (and d = 1), not covered by cells 1–5 but of no depth; (iii) three transfer lemmas: FT(N,d) ⟹ FT(N+1,d) when N ≡ −1 (mod d); FT(N+1,d) ⟹ FT(N,d) when d | N; FT(N+q,d) ⟹ FT(N,d−1) with q = ⌊N/(d−1)⌋ (finite-N analogue of Bilyk–Matzke's continuous dimension reduction); (iv) conditional corollary: cell 4's (5,3) implies S ≤ 6π for six lines in R^3. Float search in R^3..R^6 (13 pairs) found no counterexample. No non-trivial infinite family is settled; cell 6 remains open.

## 2. Proof
# Cell 6 — transfer lemmas, the trivial family, and a counterexample search

## 0. Notation
Lines are lines through the origin of $\mathbb R^d$, spanned by unit vectors; $\theta(\ell,\ell')=\arccos|\langle x,x'\rangle|\in[0,\pi/2]$; $S=\sum_{i<j}\theta(\ell_i,\ell_j)$. For integers $N\ge1$, $d\ge1$ write $N=qd+s$ with $q=\lfloor N/d\rfloor$, $0\le s<d$, and
$$M(N,d)=s\binom{q+1}{2}+(d-s)\binom{q}{2},\qquad B(N,d)=\Big(\binom N2-M(N,d)\Big)\frac{\pi}{2}.$$
**Definition.** $\mathrm{FT}(N,d)$ is the statement: *every $N$ lines in $\mathbb R^d$ satisfy $S\le B(N,d)$.* Cell 6 asks whether $\mathrm{FT}(N,d)$ holds for all $N,d$.

Throughout, $\binom{0}{2}=\binom{1}{2}=0$.

## 1. Exact identities for $M$
**Lemma 0.** Let $N=qd+s$, $0\le s<d$.
(a) $2M(N,d)=q\,(N+s-d)$.
(b) $M(N+1,d)=M(N,d)+q$.
(c) If $d\ge2$ and $N=q'(d-1)+s'$ with $0\le s'<d-1$ (so $q'=\lfloor N/(d-1)\rfloor$), then $M(N+q',d)=M(N,d-1)+\binom{q'}{2}$.

*Proof.* (a) $M=s\frac{q(q+1)}2+(d-s)\frac{q(q-1)}2=\frac q2\big[s(q+1)+(d-s)(q-1)\big]=\frac q2\big[dq+2s-d\big]=\frac q2(N+s-d)$, using $dq+s=N$.

(b) If $s\le d-2$, then $N+1=qd+(s+1)$ with $0\le s+1<d$ is the canonical representation, and $M(N+1,d)-M(N,d)=\binom{q+1}2-\binom q2=q$. If $s=d-1$, then $N+1=(q+1)d+0$, so $M(N+1,d)=d\binom{q+1}2$, while $M(N,d)=(d-1)\binom{q+1}2+\binom q2$; the difference is again $\binom{q+1}2-\binom q2=q$.

(c) $N+q'=q'(d-1)+s'+q'=q'd+s'$ with $0\le s'<d-1<d$, so this is the canonical representation of $N+q'$ modulo $d$, and
$M(N+q',d)=s'\binom{q'+1}2+(d-s')\binom{q'}2=\Big[s'\binom{q'+1}2+(d-1-s')\binom{q'}2\Big]+\binom{q'}2=M(N,d-1)+\binom{q'}2.$ $\square$

(These identities were also checked by exact integer arithmetic for all $1\le d\le40$, $1\le N\le400$ — file `verifica_identita_M.py`; the proof above does not depend on that check.)

## 2. The trivial infinite family $N\le d$ (and $d=1$)
**Lemma 1.** $\mathrm{FT}(N,d)$ holds whenever $N\le d$, and whenever $d=1$.

*Proof.* If $N\le d$ then $q=0$, $s=N$, so $M(N,d)=N\binom12+(d-N)\binom02=0$ and $B(N,d)=\binom N2\frac\pi2$. Since every $\theta\le\pi/2$, $S\le\binom N2\frac\pi2$. If $d=1$, all lines equal $\mathbb R^1$, so $S=0$; here $N=N\cdot1+0$, $M(N,1)=\binom N2$, $B(N,1)=0$, and $S\le0$ holds. $\square$

*Honest remark.* This family is not covered by cells 1–5 (cell 3 starts at $N=d+1$) but it is trivial; I list it only for completeness, not as substantive progress.

## 3. Adding a line when $N\equiv-1\pmod d$
**Lemma 2.** Let $d\ge1$, $N\ge2$, $N=qd+s$ with $s=d-1$ (i.e. $N\equiv-1\pmod d$). If $\mathrm{FT}(N,d)$ holds, then $\mathrm{FT}(N+1,d)$ holds.

*Proof.* Let $\ell_1,\dots,\ell_{N+1}$ be lines in $\mathbb R^d$ and $S$ their angle sum. For $k=1,\dots,N+1$ let $S_k$ be the angle sum of the $N$ lines obtained by deleting $\ell_k$. A pair $\{i,j\}$ contributes $\theta(\ell_i,\ell_j)$ to $S_k$ exactly for the $N+1-2=N-1$ indices $k\notin\{i,j\}$, hence
$$\sum_{k=1}^{N+1}S_k=(N-1)\,S.$$
By $\mathrm{FT}(N,d)$, $S_k\le B(N,d)$ for each $k$, so $(N-1)S\le(N+1)B(N,d)$, i.e. $S\le\frac{N+1}{N-1}B(N,d)$ (here $N-1\ge1$). It remains to show $\frac{N+1}{N-1}B(N,d)\le B(N+1,d)$, i.e.
$$(N+1)\Big(\binom N2-M(N,d)\Big)\le(N-1)\Big(\binom{N+1}2-M(N+1,d)\Big).\tag{1}$$
Since $(N+1)\binom N2=\frac{(N+1)N(N-1)}2=(N-1)\binom{N+1}2$, and $M(N+1,d)=M(N,d)+q$ by Lemma 0(b), (1) is equivalent to $-(N+1)M(N,d)\le-(N-1)M(N,d)-(N-1)q$, i.e. to $(N-1)q\le2M(N,d)$. By Lemma 0(a), $2M(N,d)=q(N+s-d)=q(N-1)$ because $s=d-1$. So (1) holds with equality, and $S\le B(N+1,d)$. $\square$

*Remark.* If $s\ne d-1$ and $q\ge1$, the inequality $(N-1)q\le q(N+s-d)$ fails, so this averaging argument gives exactly the residue class $s=d-1$ and nothing else (exact check in `verifica_identita_M.py`, item (d)).

## 4. Removing a line when $d\mid N$
**Lemma 3.** Let $d\ge1$, $N=qd$ with $q\ge1$. If $\mathrm{FT}(N+1,d)$ holds, then $\mathrm{FT}(N,d)$ holds.

*Proof.* If $N=1$ then $S=0\le B(1,d)$. Let $N\ge2$ and let $\ell_1,\dots,\ell_N$ be lines in $\mathbb R^d$ with angle sum $S$. For each $k$ put $A_k=\sum_{j\ne k}\theta(\ell_k,\ell_j)$. Each unordered pair $\{i,j\}$ appears in exactly $A_i$ and $A_j$, so $\sum_kA_k=2S$ and some index $k$ satisfies $A_k\ge2S/N$. Consider the $N+1$ lines $\ell_1,\dots,\ell_N,\ell_{N+1}$ with $\ell_{N+1}=\ell_k$ (a repeated line, allowed by the problem). Its angle sum is $S'=S+\sum_{j\le N}\theta(\ell_{N+1},\ell_j)=S+A_k+\theta(\ell_k,\ell_k)=S+A_k\ge S\,(1+\tfrac2N)=\tfrac{N+2}{N}S$, since $\theta(\ell_k,\ell_k)=\arccos1=0$. By $\mathrm{FT}(N+1,d)$, $S'\le B(N+1,d)$, hence $S\le\frac{N}{N+2}B(N+1,d)$. It remains to show $\frac N{N+2}B(N+1,d)\le B(N,d)$, i.e.
$$N\Big(\binom{N+1}2-M(N+1,d)\Big)\le(N+2)\Big(\binom N2-M(N,d)\Big).\tag{2}$$
Compute $N\binom{N+1}2-(N+2)\binom N2=\frac{N}{2}\big[(N^2+N)-(N^2+N-2)\big]=N$. With Lemma 0(b), (2) is equivalent to $N\le N\,(M(N,d)+q)-(N+2)M(N,d)=Nq-2M(N,d)$, and by Lemma 0(a) with $s=0$: $Nq-2M(N,d)=Nq-q(N-d)=qd=N$. So (2) holds with equality and $S\le B(N,d)$. $\square$

*Remark.* For $s\ne0$ one gets $Nq-2M=q(d-s)<qd+s=N$, so the argument works exactly when $d\mid N$ (exact check, item (e)).

## 5. Dropping one dimension
**Lemma 4.** Let $d\ge2$, $N\ge1$, $q'=\lfloor N/(d-1)\rfloor$. If $\mathrm{FT}(N+q',d)$ holds, then $\mathrm{FT}(N,d-1)$ holds.

*Proof.* Let $\ell_1,\dots,\ell_N$ be lines in $\mathbb R^{d-1}$ spanned by unit vectors $x_1,\dots,x_N$, with angle sum $S$. Embed $\iota:\mathbb R^{d-1}\to\mathbb R^d$, $\iota(x)=(x,0)$; this is a linear isometry, so $\langle\iota x_i,\iota x_j\rangle=\langle x_i,x_j\rangle$ and all angles $\theta$ are preserved. Let $e_d=(0,\dots,0,1)$ and consider the $N+q'$ lines in $\mathbb R^d$ spanned by $\iota x_1,\dots,\iota x_N$ and $q'$ copies of $e_d$. Their angle sum is
$$S'=S+\sum_{i=1}^{N}q'\,\theta(\iota x_i,e_d)+\binom{q'}2\theta(e_d,e_d)=S+q'N\frac\pi2+0,$$
because $\langle\iota x_i,e_d\rangle=0$ gives $\theta=\arccos0=\pi/2$ and $\theta(e_d,e_d)=0$. By $\mathrm{FT}(N+q',d)$,
$$S\le\Big(\binom{N+q'}2-M(N+q',d)-q'N\Big)\frac\pi2.$$
Now $\binom{N+q'}2-q'N=\frac{(N+q')(N+q'-1)}2-q'N=\frac{N^2-N+q'^2-q'}2=\binom N2+\binom{q'}2$, and $M(N+q',d)=M(N,d-1)+\binom{q'}2$ by Lemma 0(c). Therefore $S\le\big(\binom N2-M(N,d-1)\big)\frac\pi2=B(N,d-1)$. $\square$

## 6. Consequences
**Corollary 5 (conditional).** If cell 4's statement for five lines in $\mathbb R^3$ holds ($\mathrm{FT}(5,3)$, i.e. $S\le4\pi$), then every six lines in $\mathbb R^3$ satisfy $S\le6\pi$, i.e. $\mathrm{FT}(6,3)$.
*Proof.* $N=5=1\cdot3+2$, so $s=2=d-1$ and $N\ge2$; Lemma 2 gives $\mathrm{FT}(6,3)$. Here $B(6,3)=(15-3)\frac\pi2=6\pi$ since $6=2\cdot3+0$ and $M(6,3)=3\binom22=3$. $\square$
(This recovers, conditionally on cell 4, the range $N\le6$ in $\mathbb R^3$ attributed by Bilyk–Matzke to Fejes Tóth 1959; cell 4 itself is not proved here.)

**Corollary 6.** In the plane, Lemma 2 with $d=2$ says $\mathrm{FT}(N,2)\Rightarrow\mathrm{FT}(N+1,2)$ for odd $N\ge3$, and Lemma 3 says $\mathrm{FT}(N+1,2)\Rightarrow\mathrm{FT}(N,2)$ for even $N$. (Consistent with cell 1, which is already proved by the team; not needed.)

**What the lemmas do not give.** Starting from the families of cells 3–5 ($N=d+1$, $N=d+2$), Lemma 2 applies only when $d+2\equiv-1\pmod d$, i.e. $d\mid3$, and Lemma 4 maps $(d+2,d)$ to $(d+1,d-1)$, the same family. So no new *infinite* family follows from cells 1–5 plus these lemmas; they are transfer tools for future attempts (e.g. any proof of $\mathrm{FT}(2d-1,d)$ would yield $\mathrm{FT}(2d,d)$ by Lemma 2, and $\mathrm{FT}(2d,d)$ for all $d$ would yield $\mathrm{FT}(2d-2,d-1)$ by Lemma 4).

## 7. Counterexample search (float, exploration only — proves nothing)
Using the team's hill-climbing harness (`tools/autoloop.py` on `problema-1/esperimenti/lines_Rd.py`; Gaussian perturbations plus structured moves: copy a vector, orthogonalise against a random subset, random jump; 3 seeds × 8 restarts × 5 s per pair), the best $S$ found versus $B(N,d)$ for $(d,N)\in\{(3,6),(3,7),(3,8),(3,9),(4,7),(4,8),(4,9),(4,10),(5,8),(5,9),(5,11),(6,10),(6,13)\}$ (each $\approx5$ s wall, $\approx2.3$–$3.2\cdot10^5$ iterations):
- in 12 of 13 cases the best value agrees with $B(N,d)$ to within $2\cdot10^{-7}$; the sign of the residual is negative ($\approx-10^{-7}$) in these cases, which is the expected floating-point artefact of `arccos` at arguments clipped to $1-\varepsilon$ ($\arccos(1-\varepsilon)\approx\sqrt{2\varepsilon}$), **not** evidence of a violation; 
- for $(3,6)$ the search did not converge (best $18.8287<6\pi=18.8496$).
No configuration exceeding the conjectured bound was found. This is float arithmetic on a finite random sample: it supports "prove" over "disprove" heuristically and settles nothing.

## 8. Summary of status
- Proved (rigorously, self-contained): Lemma 0 (identities), Lemma 1 (trivial family $N\le d$ and $d=1$), Lemmas 2–4 (transfer implications), Corollaries 5–6.
- Not proved: any non-trivial infinite family; cell 6 remains open. Nothing here is claimed as a solution of the cell.

## 3. Verification: instructions, dependencies, timings
Python 3 standard library. Scripts (re-run by the orchestrator, see `runs/p1_c6/verifica/`):
- code_1 (python, rigor `exact`): Exact integer check of the identities of Lemma 0 and of the equality/inequality conditions in Lemmas 2–3, for 1≤d≤40, 1≤N≤400 (0.1 s). Saved as runs/p1_c6/sandbox/verifica_identita_M.py. The proofs do not depend on it.
- code_2 (bash, rigor `float_exploration_only`): Float-only hill-climbing search for configurations exceeding the conjectured bound in R^3..R^6 (13 pairs (d,N), 3 seeds x 8 restarts x 5 s each, ~70 s total), using the team's existing harness tools/autoloop.py with objective problema-1/esperimenti/lines_Rd.py; ledger saved in runs/p1_c6/sandbox/esplora_Rd.jsonl. Proves nothing.

## 4. Sources and contribution
- arXiv:1801.07837 (Bilyk–Matzke) — context only: Prop. 3.1 (dimension reduction for the continuous energy) motivates Lemma 4; the 'only settled case is d=1' statement; nothing cited as a proof step
- problema-1/fonti/README.md (team reading notes on Bilyk–Matzke; attribution of N≤6 in R^3 to Fejes Tóth 1959, unread original)
- Position with respect to the literature: [1801.07837] Bilyk–Matzke (read in full by the team earlier, see problema-1/fonti/README.md): the only settled case is the plane; they give a general non-sharp energy bound π/2 − 69/(50(d+1)) via the frame potential and, for the continuous (measure) version, a dimension-reduction Prop. 3.1 (conjecture in S^d ⟹ conjecture in S^{d−1}). Lemma 4 below is the finite-N analogue of that reduction, proved from scratch by embedding and adding q copies of a new orthogonal axis; the exact identity M(N+q,d) = M(N,d−1) + C(q,2) is what makes it sharp for finite N. Lemmas 2–3 (averaging over deleting/duplicating a line) do not appear in the abstracts and are our own. [2007.08698] Lim–McCann (abstract only): deformation to α-powers, optimality for α = ∞; not used. [1204.3850] is irrelevant (polygon mapping). Nothing in the literature I have settles any new infinite family; my approach departs from the energy method (known non-sharp) and instead builds exact transfer lemmas.

## 5. Limits and unresolved parts
Referee's blocking point: The only declared claim is `main` (Fejes Tóth's bound for all N, d). The submission explicitly states in §8 that no non-trivial infinite family is proved and that cell 6 remains open; Lemmas 0–4 and Corollaries 5–6 are conditional transfer statements (FT(N,d) ⇒ FT(N+1,d) for s=d−1; FT(N+1,d) ⇒ FT(N,d) for d | N; FT(N+q',d) ⇒ FT(N,d−1)) whose hypotheses are themselves the unproved conjecture. None of them, alone or combined with cells 1–5 (which are moreover not verified in the state: highest_verified_cell = 0), yields FT(N,d) for any family beyond the trivial N ≤ d / d = 1 case. Hence the declared target is not established, and no other declared claim exists to accept. The float search of §7 is exploration only and proves nothing (correctly acknowledged by the author).
Next step required: Address the stated blocking obligation without silently changing the target
Gaps declared by the author:
- No non-trivial infinite family is settled; the only 'family' proved outright (N ≤ d, d = 1) is trivial and should not be scored as substantive progress on cell 6.
- Corollary 5 (six lines in R^3) is conditional on cell 4 (five lines in R^3), which is not proved in this attempt and is not among the verified claims.
- Section 7 is floating-point hill climbing on a finite random sample: it is exploration only and proves nothing; the (3,6) run did not even converge to the conjectured value.
- The transfer lemmas, combined with cells 1–5, do not yield any new infinite family (shown in §6); their value is as reusable tools for later attempts.
