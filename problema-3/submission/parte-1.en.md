# Problem 3 — Part 1 — PARTIAL submission draft

**Declared status: PARTIAL.** No complete solution: below is what has been established, the formalisation,
the position with respect to the literature and what remains open. Nothing is claimed as proved beyond what is written.

## 1. Result and scope
**Official request.**
## Parte 1 (C1) — Cyclic partitions and cycles

**Punteggio:** 1 point · **Valutazione:** Judged

First, the long-run behaviour: which partitions repeat under the shift, and how they fall into cycles.
Let $n = T_k$. Prove that for every partition $\lambda$ of $n$ there is an $i$ with $B^i(\lambda) = \delta_k$,
and that $\delta_k$ is the only cyclic partition of $n$. Then let $n$ be arbitrary of rank $k$, say
$n = T_{k-1} + r$ with $1 \le r \le k$: determine all cyclic partitions of $n$, and determine the number of
distinct cycles of $B$ on the partitions of $n$. Prove both.

**What we deliver.** Complete description of the structure (proof currently being written up by the Researcher): cyclic partitions = staircase $\delta_{k-1}$ plus $r$ extra cards on $r$ of the $k$ positions $0,\dots,k-1$; the cycles correspond to binary necklaces with $k$ beads of which $r$ are black; number of cycles $\frac1k\sum_{d\mid\gcd(k,r)}\varphi(d)\binom{k/d}{r/d}$.

## 2. Proof
**Representation.** A partition of $n=T_{k-1}+r$ is written as a Young diagram; the operation $B$ moves each cell along a diagonal. The partitions of the form $\delta_{k-1}$ + indicator $\varepsilon\in\{0,1\}^k$ (an extra card in position $i$ means part $i+1$ instead of $i$, with position $0$ = new part 1) are closed under $B$, which acts on $\varepsilon$ as a cyclic rotation in $\mathbb Z_k$; hence they are all cyclic and the cycles are the orbits of the rotation, i.e. the necklaces, counted by Burnside's lemma. **To be completed:** (i) that every partition enters this set (potential = sum of the deviations from the staircase, strictly decreasing outside the set); (ii) that no other partition is cyclic (follows from (i)). For $n=T_k$ ($r=k$ or $r=0$) the only necklace is all black/all white: unique cyclic partition $\delta_k$.

## 3. Verification: instructions, dependencies, timings
Available code (Python 3, standard library; each script runs in under a minute):
- Researcher attempt_001, code_1 (python, exact): Sanity check (not part of the proof): exact brute-force enumeration of all partitions of n for n = 1..60, computing the 
- Researcher attempt_002, code_1 (python, exact): Exact brute-force check for n=1..40: cyclic partitions equal S_{k,r}; number of cycles equals the necklace formula; for 

## 4. Sources and contribution
arXiv literature (deterministic search `tools/cerca_letteratura.sh`, abstracts read, not used as proof):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); abstract only read.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); abstract only read.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); abstract only read.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); abstract only read.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); abstract only read.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); abstract only read.
Brandt (1982) characterises the cyclic partitions (cited in the surveys by Drensky [1503.00885] and Meštrović [2607.17194]); we reproduce the argument in full, as permitted by the rules.

## 5. Limits and unresolved parts
Complete write-up of points (i)–(ii).
