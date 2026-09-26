# Problem 3 — Part 2 — submission (PARTIAL)

**Declared status: PARTIAL.** Lower bound proved in full with an explicit extremal partition; the upper bound is NOT proved
here (verified exhaustively for small k only, and known in the literature: Igusa 1985, Etienne 1991, whose proofs we could
not access in time). The automatic Referee rejected the attempt as a solution of the whole cell precisely for this reason
(verdict REJECT: "Theorem B (upper bound D_B(T_k) ≤ k^2−k for all k) is not proved; the submission itself marks it 'NOT PROVED HERE' and only cites Igusa/Etienne (statement not reproduced, sources not read) plus an exhaustive check for sm…"), and accepted the lower-bound part as a lemma candidate.

## 1. Result and scope
Complete proof that D_B(T_k) ≥ k^2 − k for all k ≥ 1 with the explicit extremal γ_k = (k−1,k−1,k−2,…,2,1,1) (Theorem A), resting on a new exact cell-motion lemma for B (Lemma 1) that is reusable for the other cells; exhaustive exact verification that D_B(T_k) = k^2 − k for k ≤ 9. The general upper bound D_B(T_k) ≤ k^2 − k is not proved.

## 2. Proof
## Conventions

Draw a partition $\lambda=(\lambda_1\ge\dots\ge\lambda_s)$ as a diagram whose **column** $i$ ($1\le i\le s$) consists of the cells $(i,h)$, $1\le h\le \lambda_i$ ($h$ = height). The *diagonal* of a cell is $d(i,h)=i+h-1$. Diagonal $d$ contains the $d$ *slots* $(p,\,d+1-p)$, $p=1,\dots,d$; a set of cells is the diagram of a partition iff the column heights are weakly decreasing. $\delta_k$ is the diagram whose diagonals $1,\dots,k$ are full and all others empty. Throughout $n=T_k$.

## Lemma 1 (exact cell rule for $B$)

Let $\lambda$ have $s$ columns. Then $B(\lambda)$ is the diagram obtained from $\lambda$ by moving every cell as follows:

1. $(i,1)\mapsto(1,i)$ for $1\le i\le s$;
2. $(i,h)\mapsto(i+1,h-1)$ if $2\le h\le s+1$;
3. $(i,h)\mapsto(i,h-1)$ if $h\ge s+2$.

In particular cells of type 1–2 stay on their diagonal (slot $p\mapsto p+1$, and slot $d\mapsto 1$: a cyclic rotation of the diagonal), while cells of type 3 move from diagonal $d$ to diagonal $d-1$ (same column).

*Proof.* By definition the columns of $B(\lambda)$ are the multiset $\{s\}\cup\{\lambda_i-1:\lambda_i\ge 2\}$. Consider first the "unsorted" diagram $U$: column 1 of height $s$, column $i+1$ of height $\lambda_i-1$ ($1\le i\le s$). Rules 1 and 2 applied to all cells with $h\le s+1$ produce exactly the cells of $U$ of height $\le s+1$ (the new column, and the old columns shifted right and lowered), and rule 2 without the restriction $h\le s+1$ would produce all of $U$. Let $q=\#\{i:\lambda_i-1\ge s+1\}=\#\{i:\lambda_i\ge s+2\}$; because $\lambda$ is sorted, these are $i=1,\dots,q$, so in $U$ exactly the columns $2,\dots,q+1$ have height $>s+1$ (column 1 has height $s$, columns $i+1$ with $i>q$ have height $\le s$). Now compare $U$ with the diagram $V$ obtained from $U$ by moving every cell of height $\ge s+1$ in columns $2,\dots,q+1$ one column to the left. Column heights of $V$: column 1 has the $s$ cells of the new column plus the cells of heights $s+1,\dots,\lambda_1-1$ received from column 2, hence height $\lambda_1-1$; column $i$ for $2\le i\le q$ keeps heights $1,\dots,s$ (from old column $i-1$, whose height $\lambda_{i-1}-1\ge s+1$), loses heights $s+1,\dots,\lambda_{i-1}-1$ and receives heights $s+1,\dots,\lambda_i-1$ from column $i+1$, hence height $\lambda_i-1$; column $q+1$ keeps heights $1,\dots,s$ and loses the rest, hence height $s$; columns $i+1>q+1$ are unchanged with height $\lambda_i-1\le s$. So the columns of $V$ are $\lambda_1-1\ge\dots\ge\lambda_q-1\ge s\ge \lambda_{q+1}-1\ge\dots$, i.e. $V$ is the sorted diagram of $B(\lambda)$ (columns of height 0 at the end are discarded). Finally, the cells moved in passing from $U$ to $V$ are exactly the images under rule 2 of the cells $(i,h)$ of $\lambda$ with $h-1\ge s+1$, i.e. $h\ge s+2$; composing "$(i,h)\mapsto(i+1,h-1)$ then one column left" gives rule 3. $\square$

## Lemma 2 (convergence to $\delta_k$; used only for context, not for the bound)

Let $W(\lambda)=\sum_{\text{cells}} d(i,h)$. By Lemma 1, $W(B(\lambda))=W(\lambda)-\#\{(i,h)\in\lambda: h\ge s+2\}\le W(\lambda)$. Since diagonal $d$ has only $d$ slots, among all sets of $T_k$ cells with at most $d$ cells on diagonal $d$ the minimum of $W$ is attained only by $\delta_k$ (fill diagonals $1,\dots,k$); hence $W(\lambda)\ge W(\delta_k)$ with equality iff $\lambda=\delta_k$. (Combined with the fact that a partition $\ne\delta_k$ of $T_k$ cannot be periodic with all steps of cost 0 — which is C1 material and not needed below — this gives convergence; we do not use it.)

## Theorem A (lower bound). For every $k\ge1$, $D_B(T_k)\ge k^2-k$, attained by
$$\gamma_k=(k-1,\,k-1,\,k-2,\,k-3,\dots,2,\,1,\,1)\quad(k\ge2),\qquad \gamma_1=(1).$$
($\gamma_k$ is $\delta_k$ with the part $k$ replaced by the two parts $k-1$ and $1$; $|\gamma_k|=T_k$.)

*Proof.* For $k=1$ the only partition is $\delta_1$ and $D_B(1)=0=k^2-k$. Let $k\ge2$. For $p_H\in\{1,\dots,k\}$ and $p_X\in\{1,\dots,k+1\}$ let $S(p_H,p_X)$ be the set of cells of $\delta_k$ with the cell $(p_H,\,k+1-p_H)$ removed (a *hole* in slot $p_H$ of diagonal $k$) and the cell $(p_X,\,k+2-p_X)$ added (an *extra cell* in slot $p_X$ of diagonal $k+1$). Its column heights are $k+1-p$ for $p\notin\{p_H,p_X\}$, $k-p_H$ for $p=p_H$, $k+2-p_X$ for $p=p_X$ (and column $k+1$ exists iff $p_X=k+1$). It is a partition diagram iff $p_X\ne p_H$ and $p_X\ne p_H+1$ (if $p_X=p_H$ the cell $(p_H,k+2-p_H)$ would sit above a missing cell; if $p_X=p_H+1$ column $p_X$ would be taller than column $p_H$; otherwise the heights are weakly decreasing because column $p_X$ has the same height as column $p_X-1$ and column $p_H$ has the same height as column $p_H+1$). Note $\gamma_k=S(1,k+1)$: columns $k-1,k-1,k-2,\dots,2,1,1$.

Number of columns of $S(p_H,p_X)$: $s=k+1$ if $p_X=k+1$; $s=k-1$ if $p_H=k$ (then $p_X\le k$); $s=k$ otherwise. Heights: every column has height $\le k$ except column $p_X$, of height $k+2-p_X\le k+1$, with equality iff $p_X=1$. Hence a cell of height $\ge s+2$ exists only when $s=k-1$ and $p_X=1$, i.e. only in $S(k,1)$, and then it is the single cell $(1,k+1)$.

*Case $S(k,1)$.* By Lemma 1 with $s=k-1$: the bottom row $(i,1)$, $i\le k-1$, becomes column 1 with heights $1,\dots,k-1$; the cells $(i,h)$ with $2\le h\le k$ (all remaining cells of $\delta_k$ minus the hole, since the hole is $(k,1)$ and column $k$ is empty) go to $(i+1,h-1)$, giving columns $2,\dots,k$ of heights $k-1,\dots,1$; the cell $(1,k+1)$ drops to $(1,k)$, completing column 1 to height $k$. So $B(S(k,1))=\delta_k$.

*Other cases.* No cell has height $\ge s+2$, so by Lemma 1 every cell rotates one slot along its diagonal; the same is true of the empty slot (hole) on diagonal $k$, because the cells of diagonal $k$ permute cyclically among its slots. Hence $B(S(p_H,p_X))=S(p_H',p_X')$ with $p_H'\equiv p_H+1\pmod k$, $p_X'\equiv p_X+1\pmod{k+1}$ (representatives in $\{1..k\}$, $\{1..k+1\}$). (Lemma 1 guarantees the result is a partition diagram, so the validity condition is automatically preserved.)

Therefore, starting from $\gamma_k=S(1,k+1)$, as long as no step has hit $S(k,1)$ we have $B^t(\gamma_k)=S(p_H(t),p_X(t))$ with $p_H(t)\equiv 1+t\pmod k$, $p_X(t)\equiv k+1+t\equiv t\pmod{k+1}$. None of these equals $\delta_k$ (they have a hole). The first $t\ge0$ with $S(p_H(t),p_X(t))=S(k,1)$ satisfies $t\equiv k-1\pmod k$ and $t\equiv1\pmod{k+1}$. Writing $t=k-1+ak$: $k-1+ak\equiv -2-a\equiv 1\pmod{k+1}$, so $a\equiv-3\equiv k-2\pmod{k+1}$, and the least $a\ge0$ is $a=k-2$ (valid since $k\ge2$). Thus $t_0=k-1+(k-2)k=k^2-k-1$, $B^{t}(\gamma_k)\ne\delta_k$ for $0\le t\le k^2-k-1$, and $B^{k^2-k}(\gamma_k)=B(S(k,1))=\delta_k$. Since $\delta_k$ is a fixed point and (by Lemma 2, or by C1) it is the only cyclic partition of $T_k$, $d_B(\gamma_k)=k^2-k$. $\square$

(Consistency check with the statement's example and data: $\gamma_3=(2,2,1,1)$, $d_B=6$; the exhaustive computation below gives $D_B(T_k)=k^2-k$ and confirms $\gamma_k$ among the extremals for $k\le9$.)

## Theorem B (upper bound) — NOT PROVED HERE

Claim: $d_B(\lambda)\le k^2-k$ for every partition $\lambda$ of $T_k$. This is the theorem of Igusa (1985) / Etienne (1991) (CITED, proof not reproduced). What is established:

* **Exhaustive verification for $k\le9$** (exact integer arithmetic, all $p(T_k)$ partitions, 0.5 s total): $D_B(T_k)=k^2-k$ for $k=1,\dots,9$. This proves the cell's statement only for $k\le 9$.
* Structural facts from Lemma 1 available for the next attempt: (i) $W$ strictly decreases exactly at steps where some pile has size $\ge s+2$, and $\gamma_k$ has $W(\gamma_k)-W(\delta_k)=1$, so the difficulty is bounding runs of "free" steps, not the number of costly steps; (ii) empirically (exhaustive, $k\le8$) the number of piles lies in $\{k-1,k,k+1\}$ for all $t\ge T_{k-1}-(k-2)$, which suggests the strategy: bound the time until the configuration becomes "near-staircase", then analyse the near-staircase dynamics as in Theorem A.

## Conclusion of this attempt

$D_B(T_k)\ge k^2-k$ for all $k\ge1$ (Theorem A, complete), with explicit extremal $\gamma_k$; $D_B(T_k)=k^2-k$ for $k\le9$ by exhaustive computation; the general inequality $D_B(T_k)\le k^2-k$ remains to be proved.

## 3. Verification: instructions, dependencies, timings
Python 3 standard library. Scripts (re-run by the orchestrator, see `runs/p3_c2/verifica/`):
- code_1 (python, rigor `exact`): Exhaustive exact computation of D_B(T_k) and of all extremal partitions for k ≤ 9 (all partitions of T_k, orbit followed to δ_k). Finite set covered: every partition of T_k for k=1..9 (up to 89134 partitions). Wall-clock 0.48 s. Confirms D_B(T_k)=k^2−k for k≤9; does not prove the general upper bound.
- code_2 (python, rigor `exact`): Exploration only: along every orbit for k ≤ 8, records the last time the pile count leaves {k−1,k,k+1} and the first time diagonals 1..k−1 are full; used to guide the (unfinished) upper-bound strategy. Exact integers, all partitions of T_k for k=3..8, ~1 min.

## 4. Sources and contribution
- B. Hopkins, 30 Years of Bulgarian Solitaire, College Math. J. 43 (2012) 135–140 (read in full; p.137 statement that Igusa proved γ_k=(k−1,k−1,k−2,…,2,1,1) is at maximal distance k(k−1)) — CITED for context only
- K. Igusa, Solution of the Bulgarian solitaire conjecture, Math. Mag. 58 (1985) 259–271 — NOT read (paywalled); statement cited via Hopkins/Drensky
- G. Etienne, Tableaux de Young et solitaire bulgare, J. Combin. Theory Ser. A 58 (1991) 181–197 — NOT read
- J. R. Griggs, C.-C. Ho, The cycling of partitions and compositions under repeated shifts, Adv. Appl. Math. 21 (1998) 205–227 — NOT read
- arXiv:1503.00885 (Drensky) and arXiv:2607.17194 (Meštrović) — read; both only cite Igusa/Etienne for the k(k−1) bound and name Toom's extremal τ=γ_k
- M. Jonsson, Processes on Integer Partitions and Their Limit Shapes, PhD thesis, Mälardalen Univ. 2017 (DiVA diva2:1082060) — read the relevant pages; cites Etienne for the game-tree height k^2−k
- Position with respect to the literature: The listed arXiv abstracts (math/0401385, 1703.07102: random variants; 1101.1546: Toom's convergence proof; 2208.14496: orbit growth; 1503.00885 and 2607.17194: surveys) do not prove the bound. I fetched and read (pdftotext) Drensky 1503.00885, Meštrović 2607.17194, Hopkins "30 years of Bulgarian solitaire" (College Math. J. 43 (2012) 135–140), Hopkins–Jones (EJC 13 (2006) R80), N. Pham's honors thesis and M. Jonsson's PhD thesis (DiVA 1082060). All state, CITED: Knuth conjectured and Igusa (Math. Mag. 58 (1985) 259–271) and Etienne (JCTA 58 (1991) 181–197) proved that for n=T_k the maximal number of moves is k(k−1), attained by γ_k=(k−1,k−1,k−2,…,2,1,1) (Hopkins 2012, p. 137: "Igusa [15] shows that the partition γ_k … is at distance k(k−1) from τ_k and that this distance is maximal"). None of the read sources reproduces the proof. My approach follows the classical "cards on diagonals" idea mentioned by Hopkins (p. 137) but makes it exact (Lemma 1) and uses it to prove the lower bound in full; the upper bound argument of Igusa/Etienne is not reproduced.

## 5. Limits and unresolved parts
- Upper bound D_B(T_k) ≤ k^2 − k for all k: not proved (only verified exhaustively for k ≤ 9 and cited from Igusa 1985 / Etienne 1991, whose proofs I could not access). This is the next blocker.
- Theorem A uses that δ_k is the only cyclic partition of T_k to conclude d_B(γ_k) = k^2−k rather than merely B^{k^2−k}(γ_k)=δ_k; this is the C1 statement, sketched via the potential W in Lemma 2 but not written out in full here (the strict-decrease/non-periodicity step is omitted).
- Lemma 1's proof treats ties (columns of equal height) implicitly: the sorted diagram is determined by the multiset of column heights, so ties do not affect the cell set, but the reader may want this stated explicitly.
