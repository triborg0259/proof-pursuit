# Problem 4 — Part 6 — PARTIAL submission draft

**Declared status: PARTIAL.** No complete solution: below is what has been established, the formalization,
the position with respect to the literature and what remains open. Nothing is declared proved beyond what is written.

## 1. Result and scope
**Official request.**
## Parte 6 (C6) — Beyond the boundary

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

Three directions beyond the certified range; any one of them counts. Any of the following.

(a) Decide a size $k \ge 25$.

(b) The asymptotic form. It is known that a pairwise disjoint family of size $k$ always has a pair with
$$
\gcd(m_i, m_j) \;\ge\; k \cdot \exp\!\left( -(2 + o(1)) \frac{\log k}{\log\log k} \right),
$$
which is $k^{1 - o(1)}$ but not linear in $k$. Prove the statement in full, or prove the weaker bound
$\gcd(m_i, m_j) \ge ck$ for some absolute constant $c > 0$, or improve the exponential factor above.

(c) The group form. Let $G$ be a group, let $G_1, \ldots, G_k$ be subgroups of finite index $n_i = [G : G_i]$,
and let $x_1 G_1, \ldots, x_k G_k$ be pairwise disjoint cosets. Is there a pair $i < j$ with
$\gcd(n_i, n_j) \ge k$? This is known for $k \le 5$ and open for every $k \ge 6$; settling $k = 6$ counts as
progress.

*(End of problem 4. Scores: 1+2+3+5+8+13 = 32.)*

**What we submit.** No proof. Relevant remark: the asymptotic bound quoted in the statement has already been improved in the literature.

## 2. Proof
Fornal–Sun [2607.24655] (July 2026) prove $\max\gcd(m_i,m_j)\gg k\exp(-(2+o(1))\sqrt{\log k/\log\log k})$, with a square root in the exponent: an improvement of the exponential factor requested in (b). Reproducing their proof in full (gcd graph, structural lemma, sieving partition, Möbius inversion, discrete Fourier transform) would count under the rules; not done.

## 3. Verification: instructions, dependencies, timings
Available code (Python 3, standard library; each script runs in under a minute):
- No code yet.

## 4. Sources and contribution
arXiv literature (deterministic search `tools/cerca_letteratura.sh`, abstracts read, not used as proof):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); abstract only read.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); abstract only read.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); abstract only read.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); abstract only read.
[2607.24655].

## 5. Limits and unresolved parts
Everything; route (b) via reproduction of the proof is the indicated one.
