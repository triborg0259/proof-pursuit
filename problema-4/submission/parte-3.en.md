# Problem 4 — Part 3 — PARTIAL submission draft

**Declared status: PARTIAL.** No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is declared proven beyond what is written.

## 1. Result and scope
**Official request.**
## Parte 3 (C3) — Every $k$ up to 8

**Punteggio:** 3 points · **Valutazione:** Judged

A first range of sizes: after C1 and C2, the sizes $k = 5, 6, 7$ and $8$ remain. Prove the statement for every
$k \le 8$.

**What we deliver.** Proven reduction to a finite set: in a counterexample of size $k$ one may assume that every modulus divides $L_k=\mathrm{lcm}(2,\dots,k-1)$; exhaustiveness certificate not completed.

## 2. Proof
**Reduction lemma (proven).** Let $g_{ij}=\gcd(m_i,m_j)$ and $m_i'=\mathrm{lcm}_{j\ne i}g_{ij}$. Then $m_i'\mid m_i$, $\gcd(m_i',m_j')=g_{ij}$ (it is divisible by $g_{ij}$ and divides $\gcd(m_i,m_j)$), and the classes $a_i \pmod{m_i'}$ remain pairwise disjoint by criterion $(*)$, which depends only on $g_{ij}$ and on $a_i-a_j\bmod g_{ij}$. In a counterexample every $g_{ij}\le k-1$, hence $m_i'\mid L_k$: the set of moduli is finite. Also $\sum1/m_i\le1$ holds. **Search (set up):** moduli = multisets of $k$ divisors of $L_k$ with pairwise gcd in $[2,k-1]$, each equal to the lcm of its own gcds; residues = CSP with constraints $a_i\not\equiv a_j\pmod{g_{ij}}$, normalization $a_1=0$; second implementation by enumeration of the admissible gcd families. The Researcher (run `runs/p4_c3`) produced an attempt, under evaluation.

## 3. Verification: instructions, dependencies, timings
Code available (Python 3, standard library; each script runs in under one minute):
- Researcher attempt_001, code_1 (python, exact): Implementation 1 (certificate): exhaustive enumeration of all k-cliques in G_k on the 1343 classes (a,m), m|420, m>=2; n
- Researcher attempt_001, code_2 (python, exact): Implementation 2 (independent cross-check, different method): enumerate non-decreasing k-tuples of moduli dividing 420 w

## 4. Sources and contribution
arXiv literature (deterministic search `tools/cerca_letteratura.sh`, abstracts read, not used as proof):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); abstract only read.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); abstract only read.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); abstract only read.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); abstract only read.
Fornal–Sun [2607.24655] (2026) treat the asymptotic regime with a gcd graph: the same object as our reduction; the cases $k\le8$ do not appear there.

## 5. Limits and unresolved parts
Certified execution (counts, timings, reruns, survivors) for $k=5,\dots,8$.
