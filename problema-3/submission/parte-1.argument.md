Problem 3 — Part 1 — submission

Declared status: SOLVED (approved). Complete proof; automatic Referee READY_FOR_HUMAN (judge A, mathematics: PASS;
judge B, evidence: PASS; code re-run by the orchestrator); human approval recorded in runs/p3_c1/approval.json.

1. Result and scope

Full written proof of all parts of cell 1: (i) for n=T_k every partition reaches δ_k and δ_k is the unique cyclic partition; (ii) for n=T_{k-1}+r the cyclic partitions are exactly the C(k,r) partitions λ^ε (positive numbers among k-i+ε_i, ε∈{0,1}^k of weight r), on which B acts as cyclic rotation of ε; (iii) the number of cycles is (1/k)Σ_{d|gcd(k,r)} φ(d) C(k/d, r/d). The convergence step is proved via an ordered dynamics, a diagonal potential Φ with exact equality characterisation, and a hole-chasing lemma. Exact brute-force check agrees for all n≤40.

2. Proof

Notation

Throughout $n\ge 1$ has rank $k$, i.e. $n=T_{k-1}+r$ with $1\le r\le k$ (equivalently $T_{k-1}<n\le T_k$). For a $0/1$-word $\varepsilon=(\varepsilon_1,\dots,\varepsilon_k)$ of weight $|\varepsilon|=\sum\varepsilon_i=r$ put
$$\lambda^{\varepsilon}:=\text{the partition whose parts are the positive numbers among } k-i+\varepsilon_i,\quad i=1,\dots,k,$$
$$W_{k,r}:=\{\varepsilon\in\{0,1\}^k:|\varepsilon|=r\},\qquad S_{k,r}:=\{\lambda^{\varepsilon}:\varepsilon\in W_{k,r}\}.$$

Fact 0. $\lambda^\varepsilon$ is a partition of $n$; the sequence $(k-i+\varepsilon_i)_{i=1}^k$ is weakly decreasing, its first $k-1$ entries are $\ge1$, and the $k$-th is $\varepsilon_k$. Moreover $\varepsilon\mapsto\lambda^\varepsilon$ is injective on $W_{k,r}$, and $S_{k,k}=\{\delta_k\}$.

Proof. Sum: $\sum_i(k-i)+\sum_i\varepsilon_i=T_{k-1}+r=n$. Monotone: $(k-i+\varepsilon_i)-(k-i-1+\varepsilon_{i+1})=1+\varepsilon_i-\varepsilon_{i+1}\ge0$. For $i\le k-1$, $k-i+\varepsilon_i\ge1$. Injective: $\lambda^\varepsilon$ has $k-1$ or $k$ parts; pad it with zeros to length exactly $k$; the padded weakly decreasing sequence of a multiset is unique, and $(k-i+\varepsilon_i)_i$ is such a sequence, so the $i$-th padded part equals $k-i+\varepsilon_i$ and $\varepsilon_i$ is recovered. For $r=k$ the only word is $(1,\dots,1)$ and $\lambda^\varepsilon=(k,k-1,\dots,1)=\delta_k$. $\square$

Part I. $B$ acts on $S_{k,r}$ as a rotation

Lemma 1. For $\varepsilon\in W_{k,r}$, $B(\lambda^\varepsilon)=\lambda^{\sigma\varepsilon}$ where $\sigma\varepsilon:=(\varepsilon_k,\varepsilon_1,\varepsilon_2,\dots,\varepsilon_{k-1})$. In particular $S_{k,r}$ is $B$-invariant, $B^k$ is the identity on $S_{k,r}$, and every element of $S_{k,r}$ is cyclic.

Proof. By Fact 0, $\lambda^\varepsilon$ has $s=k-1+\varepsilon_k$ parts: the parts $k-i+\varepsilon_i$ for $i\le k-1$, plus the part $1$ (coming from $i=k$) iff $\varepsilon_k=1$. Applying $B$: each part $k-i+\varepsilon_i$ ($i\le k-1$) becomes $k-(i+1)+\varepsilon_i$, which is positive for $i\le k-2$ and equals $\varepsilon_{k-1}$ for $i=k-1$ (kept iff it is $1$); the part $1$ present when $\varepsilon_k=1$ becomes $0$ and is discarded; the new part is $s=k-1+\varepsilon_k$. Hence $B(\lambda^\varepsilon)$ has as parts the positive numbers among
$$k-1+\varepsilon_k\ \ (\text{index }i'=1),\qquad k-i'+\varepsilon_{i'-1}\ \ (i'=2,\dots,k),$$
which are exactly the numbers $k-i'+(\sigma\varepsilon)_{i'}$, $i'=1,\dots,k$. So $B(\lambda^\varepsilon)=\lambda^{\sigma\varepsilon}$. Since $\sigma$ preserves weight and $\sigma^k=\mathrm{id}$, $B^k(\lambda^\varepsilon)=\lambda^{\sigma^k\varepsilon}=\lambda^\varepsilon$ with $k\ge1$, so $\lambda^\varepsilon$ is cyclic. $\square$

Part II. Every partition of $n$ enters $S_{k,r}$

II.1 Ordered dynamics

A composition is a finite sequence $c=(c_1,\dots,c_s)$ of positive integers. Define
$$\tilde B(c):=\text{the sequence }(s,\ c_1-1,\ \dots,\ c_s-1)\text{ with all zero entries deleted}.$$
The multiset of entries of $\tilde B(c)$ is $\{s\}\cup\{c_i-1:c_i\ge2\}$, which is by definition the multiset of parts of $B(\mathrm{sort}(c))$. Hence, starting from $c^{(0)}:=\lambda$ (as a sequence) and putting $c^{(t+1)}:=\tilde B(c^{(t)})$, we have
$$B^t(\lambda)=\mathrm{sort}(c^{(t)})\quad\text{for all }t\ge0. \qquad(1)$$
Write $s_t$ for the length of $c^{(t)}$. The cell set of a composition is $C(c):=\{(i,j):1\le i\le s,\ 1\le j\le c_i\}\subset\mathbb Z_{\ge1}^2$; put $C_t:=C(c^{(t)})$. Cell $(i,j)$ lies on diagonal $i+j$. Two properties hold for every composition, by definition: (closed) if $(i,j)\in C(c)$ and $1\le j'\le j$ then $(i,j')\in C(c)$; (gap-free) if $(i,1)\in C(c)$ and $1\le i'\le i$ then $(i',1)\in C(c)$; and $(i,1)\notin C(c)$ iff $i>s$.

II.2 The potential

For a finite sequence $e=(e_1,\dots,e_m)$ of non-negative integers put $\Phi(e):=\sum_{i=1}^m\sum_{j=1}^{e_i}(i+j)\in\mathbb Z_{\ge0}$ (zero entries contribute nothing).

Lemma 2. For every composition $c$, $\Phi(\tilde B(c))\le\Phi(c)$, with equality if and only if the set $\{i: c_i=1\}$ is a terminal segment of $\{1,\dots,s\}$ (i.e. $c_i=1\Rightarrow c_j=1$ for all $j>i$).

Proof. Let $e:=(s,c_1-1,\dots,c_s-1)$ (length $s+1$, zeros allowed). Then
$$\Phi(e)=\sum_{j=1}^{s}(1+j)+\sum_{i=1}^{s}\sum_{j=1}^{c_i-1}(i+1+j)=\sum_{i=1}^{s}(i+1)+\sum_{i=1}^{s}\sum_{j'=2}^{c_i}(i+j')=\sum_{i=1}^{s}\sum_{j'=1}^{c_i}(i+j')=\Phi(c),$$
where we substituted $j'=j+1$ and used that the term $j'=1$ of column $i$ is $i+1$. Now $\tilde B(c)$ is obtained from $e$ by deleting its zero entries; an entry $e_q>0$ preceded by $z_q$ zeros moves to position $q-z_q$, so $\Phi$ decreases by $\sum_{q:e_q>0}z_q e_q\ge0$, with equality iff no positive entry is preceded by a zero, i.e. iff the zeros of $e$ form a terminal segment. Since $e_1=s\ge1$ and $e_{i+1}=0\iff c_i=1$, this says exactly that $\{i:c_i=1\}$ is terminal in $\{1,\dots,s\}$. $\square$

By Lemma 2, $(\Phi(c^{(t)}))_{t\ge0}$ is a non-increasing sequence of non-negative integers, hence eventually constant: there is $t_0$ with $\Phi(c^{(t+1)})=\Phi(c^{(t)})$ for all $t\ge t_0$. By the equality case of Lemma 2:
$$\text{for all }t\ge t_0:\quad \{i:c^{(t)}_i=1\}\text{ is a terminal segment of }\{1,\dots,s_t\}. \qquad(2)$$

II.3 Diagonal motion in the steady regime

Define $\rho:\mathbb Z_{\ge1}^2\to\mathbb Z_{\ge1}^2$ by $\rho(i,j)=(i+1,j-1)$ if $j\ge2$ and $\rho(i,1)=(1,i)$. Then $\rho$ preserves $i+j$, and $\rho$ is a bijection (inverse: $(i,j)\mapsto(i-1,j+1)$ for $i\ge2$, $(1,j)\mapsto(j,1)$). On diagonal $d\ge2$, whose cells are $(i,d-i)$, $1\le i\le d-1$, $\rho$ sends column $i$ to column $i+1$ for $i\le d-2$ and column $d-1$ to column $1$; hence $\rho^m$ sends the cell of diagonal $d$ in column $i$ to the cell in the unique column $\equiv i+m \pmod{d-1}$ in $\{1,\dots,d-1\}$.

Lemma 3. For all $t\ge t_0$: $C_{t+1}=\rho(C_t)$.

Proof. Let $c=c^{(t)}$, $e=(s,c_1-1,\dots,c_s-1)$ as in Lemma 2. The cells of $e$ (defined as for compositions, zero entries giving no cells) are $\{(1,j):1\le j\le s\}=\rho(\{(j,1):1\le j\le s\})$ together with $\{(i+1,j-1):2\le j\le c_i\}=\rho(\{(i,j)\in C_t: j\ge2\})$; so the cell set of $e$ is $\rho(C_t)$. By (2), the zeros of $e$ form a terminal segment, so deleting them does not move any positive entry, and $C_{t+1}=C(\tilde B(c))$ is the cell set of $e$. $\square$

Consequently, for $t\ge t_0$ and $m\ge0$, $C_{t+m}=\rho^m(C_t)$, and since $\rho^m$ is injective,
$$x\in C_t\iff\rho^m(x)\in C_{t+m}\qquad(x\in\mathbb Z_{\ge1}^2). \qquad(3)$$

II.4 The hole lemma

Lemma 4. Let $t\ge t_0$ and $d\ge2$. If some cell of diagonal $d$ is not in $C_t$ (a hole), then no cell of any diagonal $D>d$ lies in $C_t$.

Proof. Diagonal $2$ consists of the single cell $(1,1)\in C_t$ (as $n\ge1$, $s_t\ge1$), so $d\ge3$. Suppose $(p,d-p)\notin C_t$ and $(q,D-q)\in C_t$ with $D>d$. For $m\ge0$ let $h_m\in\{1,\dots,d-1\}$ be the column of $\rho^m(p,d-p)$ and $\kappa_m\in\{1,\dots,D-1\}$ the column of $\rho^m(q,D-q)$; by (3), $\rho^m(p,d-p)\notin C_{t+m}$ and $\rho^m(q,D-q)\in C_{t+m}$. By II.3, $h_{m+1}\equiv h_m+1\pmod{d-1}$ and $\kappa_{m+1}\equiv\kappa_m+1\pmod{D-1}$.

Constraint (ii). If $h_m=d-1$ then $\kappa_m\le d-2$. Indeed the hole is then the cell $(d-1,1)\notin C_{t+m}$, so $d-1>s_{t+m}$ (II.1), i.e. $s_{t+m}\le d-2$, and every cell of $C_{t+m}$ has column $\le d-2$.

Since $h_m$ runs cyclically through $1,\dots,d-1$, there are infinitely many $m$ with $h_m=d-1$. Take one such $m$ and put $u:=\kappa_m\in\{1,\dots,d-2\}$ (by (ii)). For $l=1,\dots,d-1$ we have $h_{m+l}=l$ (the hole goes from column $d-1$ to $1,2,\dots,d-1$), and $\kappa_{m+l}=u+l$ as long as $u+l\le D-1$.

Case A: $u\le D-d$. Then $u+(d-1)\le D-1$, so $\kappa_{m+d-1}=u+d-1\ge d$, while $h_{m+d-1}=d-1$: this contradicts (ii).

Case B: $u\ge D-d+1$. Then $D-u\le d-1$; the card is in column $D-1$ at $l=D-1-u$, in column $1$ at $l=D-u$, and in column $l-(D-u)+1$ for $D-u\le l\le d-1$ (no further wrap, since $l-(D-u)+1\le d-D+u\le u\le d-2<D-1$). At $l=d-1$ the hole is again in column $d-1$ and the card in column $u':=u-(D-d)$, with $1\le u'\le u-1$ because $D-d\ge1$ and $u\ge D-d+1$.

So each time the hole is in column $d-1$, either Case A gives a contradiction, or Case B occurs and at the next such time the card's column is a strictly smaller positive integer. Case B cannot occur forever (positive integers cannot decrease strictly infinitely often), so Case A occurs at some time — a contradiction. Hence no such card exists. $\square$

II.5 Conclusion of Part II

Theorem A. For every partition $\lambda$ of $n$ (rank $k$, $n=T_{k-1}+r$, $1\le r\le k$) there is $t$ with $B^t(\lambda)\in S_{k,r}$. In particular for $n=T_k$ there is $t$ with $B^t(\lambda)=\delta_k$.

Proof. Take $t=t_0$ and $C:=C_{t}$. Diagonal $2$ is full ($=\{(1,1)\}\subseteq C$); $C$ is finite, so $K:=\max\{m\ge2:\text{diagonals }2,\dots,m\text{ are all contained in }C\}$ exists, and diagonal $K+1$ has a hole. By Lemma 4 no cell of diagonal $\ge K+2$ is in $C$. Therefore
$$C=\{(i,j):i+j\le K\}\ \cup\ R,\qquad R\subseteq\{(i,K+1-i):1\le i\le K\},\quad r':=|R|\le K-1.$$
Set $\varepsilon_i:=1$ if $(i,K+1-i)\in R$ and $0$ otherwise ($1\le i\le K$). Column $i\le K$ of $C$ consists of $(i,1),\dots,(i,K-i)$ plus possibly $(i,K+1-i)$, so it has height $K-i+\varepsilon_i$; columns $>K$ are empty. Hence $c^{(t)}$ is the sequence of positive numbers among $K-i+\varepsilon_i$ ($i=1,\dots,K$), and $n=|C|=T_{K-1}+r'$ with $0\le r'\le K-1$.
If $r'\ge1$: then $T_{K-1}<n\le T_K$, so $K=k$, $r'=r$, and by (1) $B^t(\lambda)=\mathrm{sort}(c^{(t)})=\lambda^\varepsilon\in S_{k,r}$ (the sequence is already weakly decreasing by Fact 0).
If $r'=0$: then $n=T_{K-1}$, so $k=K-1$, $r=k$, and $c^{(t)}=(K-1,K-2,\dots,1)=\delta_k$, i.e. $B^t(\lambda)=\delta_k\in S_{k,k}$. $\square$

Part III. Cyclic partitions and cycles

Theorem B. The cyclic partitions of $n=T_{k-1}+r$ ($1\le r\le k$) are exactly the elements of $S_{k,r}$, i.e. the partitions $\lambda^\varepsilon$ with $\varepsilon\in\{0,1\}^k$ of weight $r$ — explicitly, the partitions whose parts are the positive numbers among $k-1+\varepsilon_1,\ k-2+\varepsilon_2,\ \dots,\ 1+\varepsilon_{k-1},\ \varepsilon_k$ with exactly $r$ of the $\varepsilon_i$ equal to $1$. There are $\binom kr$ of them. For $n=T_k$ ($r=k$) the only cyclic partition is $\delta_k$, and every partition of $T_k$ reaches $\delta_k$.

Proof. ($\supseteq$) Lemma 1. ($\subseteq$) Let $\lambda$ be cyclic, $B^i(\lambda)=\lambda$ with $i\ge1$. By Theorem A, $B^t(\lambda)\in S_{k,r}$ for some $t$. Choose an integer $q$ with $qi\ge t$. Then $\lambda=B^{qi}(\lambda)=B^{qi-t}\big(B^t(\lambda)\big)\in S_{k,r}$ by $B$-invariance of $S_{k,r}$ (Lemma 1). The count $\binom kr$ is Fact 0 (injectivity) and $|W_{k,r}|=\binom kr$. The triangular statements are the case $r=k$ ($S_{k,k}=\{\delta_k\}$) together with Theorem A. $\square$

Theorem C. The number of distinct cycles of $B$ on the partitions of $n=T_{k-1}+r$ is
$$N(k,r)=\frac1k\sum_{d\mid\gcd(k,r)}\varphi(d)\binom{k/d}{r/d},$$
where $\varphi$ is Euler's function. For $n=T_k$ this equals $1$.

Proof. Every cycle of $B$ consists of cyclic partitions, hence (Theorem B) lies in $S_{k,r}$, and every element of $S_{k,r}$ lies on a cycle (Lemma 1). By Lemma 1 and the injectivity of $\varepsilon\mapsto\lambda^\varepsilon$, the cycles of $B$ on $S_{k,r}$ correspond bijectively to the orbits of the cyclic group $G=\langle\sigma\rangle=\{\sigma^j:0\le j\le k-1\}$ (of order $k$) acting on $W_{k,r}$ by rotation.

Orbit count (Burnside, with proof). Count pairs $(g,\varepsilon)\in G\times W_{k,r}$ with $g\varepsilon=\varepsilon$ in two ways: $\sum_{g\in G}|\mathrm{Fix}(g)|=\sum_{\varepsilon}|\mathrm{Stab}(\varepsilon)|=\sum_{\varepsilon}\frac{|G|}{|G\varepsilon|}=|G|\cdot\#\text{orbits}$ (orbit–stabiliser; each orbit $O$ contributes $\sum_{\varepsilon\in O}|G|/|O|=|G|$). Hence $\#\text{orbits}=\frac1k\sum_{j=0}^{k-1}|\mathrm{Fix}(\sigma^j)|$.

Fixed points of $\sigma^j$. $\sigma^j$ shifts positions by $j$ modulo $k$; its cycles on $\{1,\dots,k\}\cong\mathbb Z_k$ are the cosets $i+g\mathbb Z_k$ where $g=\gcd(j,k)$ (because $\{jm\bmod k\}=g\mathbb Z_k$), so there are $g$ cycles each of length $k/g$. A word is fixed by $\sigma^j$ iff it is constant on each cycle; choosing $a$ cycles to carry $1$'s gives weight $a\,k/g$. So $|\mathrm{Fix}(\sigma^j)|=\binom{g}{rg/k}$ if $(k/g)\mid r$, and $0$ otherwise. The number of $j\in\{0,\dots,k-1\}$ with $\gcd(j,k)=g$ is $\varphi(k/g)$ (write $j=gj'$, $0\le j'<k/g$, $\gcd(j',k/g)=1$). Putting $d=k/g$ (so $d\mid k$, and the term is nonzero iff $d\mid r$):
$$N(k,r)=\frac1k\sum_{d\mid k,\ d\mid r}\varphi(d)\binom{k/d}{r/d}=\frac1k\sum_{d\mid\gcd(k,r)}\varphi(d)\binom{k/d}{r/d}.$$
For $r=k$: $\sum_{d\mid k}\varphi(d)\binom{k/d}{k/d}=\sum_{d\mid k}\varphi(d)=k$, so $N(k,k)=1$ (consistent with $S_{k,k}=\{\delta_k\}$, $B(\delta_k)=\delta_k$). $\square$

Summary of the answers to cell 1

* $n=T_k$: every partition reaches $\delta_k$ (Theorem A), and $\delta_k$ is the unique cyclic partition (Theorem B), forming the unique cycle (a fixed point).
* $n=T_{k-1}+r$, $1\le r\le k$: the cyclic partitions are exactly the $\binom kr$ partitions $\lambda^\varepsilon$, $\varepsilon\in\{0,1\}^k$ of weight $r$ (Theorem B); $B$ acts on them by the rotation $\varepsilon\mapsto(\varepsilon_k,\varepsilon_1,\dots,\varepsilon_{k-1})$ (Lemma 1); the number of cycles is $\frac1k\sum_{d\mid\gcd(k,r)}\varphi(d)\binom{k/d}{r/d}$ (Theorem C).

Examples. $n=8=T_3+2$ ($k=4,r=2$): cyclic partitions $\lambda^\varepsilon$ for $\varepsilon\in\{1100,1010,1001,0110,0101,0011\}$: $(4,3,1),(4,2,2),(4,2,1,1),(3,3,2),(3,3,1,1),(3,2,2,1)$; cycles: $\{1100,0110,0011,1001\}$ and $\{1010,0101\}$, so $N(4,2)=\frac14(\binom42+\varphi(2)\binom21)=2$.

Independent exact check (not part of the proof). The script verifica_cella1.py (exact integer arithmetic) enumerates all partitions of every $n\le40$, computes the cyclic partitions and the number of cycles by brute force, and confirms they equal $S_{k,r}$ and $N(k,r)$; it also checks Lemma 2 on all compositions of $n\le14$. Runtime 7.0 s.

3. Verification: instructions, dependencies, timings

Python 3 standard library only. Scripts (also saved in runs/p3_c1/sandbox/ and re-run in runs/p3_c1/verifica/):
- code_1 (python, rigor exact): Exact brute-force check for n=1..40: cyclic partitions equal S_{k,r}; number of cycles equals the necklace formula; for n=T_k the only cyclic partition is delta_k. Also checks the potential Lemma 2 (monotonicity and exact equality condition) on all compositions of n<=14. Finite set covered: all partitions of n<=40, all compositions of n<=14. Wall-clock 7.0 s. File: runs/p3_c1/sandbox/verifica_cella1.py

Trusted re-runs by the orchestrator (exit code, wall clock, output):
- orchestrator re-ran code_1.py (python3, clean copy of the researcher sandbox): exit 0 in 7.0s; stdout: 'OK: n=1..40 e potenziale su composizioni di n<=14, tempo 7.0s'; stderr: ''

4. Sources and contribution

- arXiv:1503.00885 (Drensky, survey; abstract only — context: attribution of the characterisation to Brandt 1982)
- arXiv:2607.17194 (Meštrović, survey; abstract only — context)
- arXiv:1101.1546 (Hart–Khan–Khan, exposition of Toom's proof; abstract only — context)
- arXiv:2208.14496 (Pham; abstract only — context: necklace parametrisation of orbits)
- Position with respect to the literature: The cell's statement is classical: 1503.00885 (Drensky) and 2607.17194 (Meštrović) survey it and attribute the characterisation of cyclic partitions and the necklace count of cycles to Brandt (1982); 1101.1546 (Hart–Khan–Khan) expounds Toom's proof of convergence to δ_k for triangular n; 2208.14496 (Pham) uses Brandt's necklace parametrisation of orbits. I have not read the full papers, only the abstracts; nothing from them is used as a hypothesis. My proof follows the general strategy of "diagonal invariant + monotone potential" but the hole-chasing lemma and all details are written out in full here, so the result is proved, not cited.
- Contribution: the proof above is written out in full by the team's Researcher and checked by two independent judges and by a human.

5. Limits and unresolved parts

Gaps declared by the author (all accepted by the judges):
- Lemma 4 (hole lemma) is the most delicate step; the case analysis A/B on the card's column is written out, but the referee should re-check the index bookkeeping (in particular that in Case B the card wraps exactly once before the hole returns to column d-1, and that u' = u-(D-d) is ≥ 1).
- Burnside's lemma and the orbit structure of a rotation on Z_k are proved briefly inline (orbit–stabiliser is used without proof); these are textbook facts.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family direct_proof, subgoal: Prove the complete statement of cell 1: (a) for n = T_k every partition reaches δ_k and δ_k is the only cyclic partition; (b) for n = T_{k-1}+r, 1 ≤ r ≤ k, the cyclic partitions are exactly δ_{k-1}+ε with ε ∈ {0,1}^k of weight r, and the number of cycles is the number of binary necklaces of length k with r black beads, (1/k) Σ_{d | gcd(k,r)} φ(d) C(k/d, r/d).; declared CELL_SOLVED_CANDIDATE.
  - Why this approach: No previous attempt or blocker; this is the first natural subgoal and it covers the whole cell. The potential + diagonal-rotation + CRT route is the shortest fully self-contained argument I know that handles all n at once (not only triangular n), and it yields the cyclic set and the cycle count with the same machinery. An exact brute-force enumeration for n ≤ 60 was run as a sanity check of the statement (not as part of the proof).
  - Position w.r.t. the literature: The abstracts say the cyclic partitions were characterized and counted by Brandt (1982), with orbits parametrized by necklaces of black and white beads (2208.14496v1, 2607.17194v1), and that for triangular n the process converges to the unique fixed point (1503.00885v1). 1101.1546v3 (Hart–Khan–Khan) states that Toom's proof of the triangular case can be generalized via the Chinese Remainder Theorem. I have NOT read the full papers; only the abstracts. My proof follows the spirit indicated in the abstract of 1101.1546v3 (CRT on diagonals of coprime lengths), combined with a potential-function argument to justify that B is a pure diagonal rotation along every cycle; every step is written out here in full, so nothing is cited as a proof. The necklace formula is Brandt's statement (CITED for context only); it is proved inline via Burnside's lemma, which is also proved inline.
  - Referee: (nessun verdetto) / None
- attempt_002 — Researcher: family direct_proof, subgoal: Complete proof of cell 1: (a) every partition of n eventually enters the B-invariant family S_{k,r}; (b) S_{k,r} is exactly the set of cyclic partitions (for n=T_k this is {δ_k}); (c) the number of cycles is the necklace number (1/k)Σ_{d|gcd(k,r)} φ(d) C(k/d,r/d).; declared CELL_SOLVED_CANDIDATE.
  - Why this approach: No blocker/failed attempts recorded; this is the first attempt. The diagonal-potential route (in the spirit of Akin–Davis/Toom) gives a single self-contained argument covering both the triangular and non-triangular case at once, with every step elementary and checkable; the cycle count then follows from the explicit rotation action.
  - Position w.r.t. the literature: The cell's statement is classical: 1503.00885 (Drensky) and 2607.17194 (Meštrović) survey it and attribute the characterisation of cyclic partitions and the necklace count of cycles to Brandt (1982); 1101.1546 (Hart–Khan–Khan) expounds Toom's proof of convergence to δ_k for triangular n; 2208.14496 (Pham) uses Brandt's necklace parametrisation of orbits. I have not read the full papers, only the abstracts; nothing from them is used as a hypothesis. My proof follows the general strategy of "diagonal invariant + monotone potential" but the hole-chasing lemma and all details are written out in full here, so the result is proved, not cited.
  - Referee: UNKNOWN_STATUS / READY_FOR_HUMAN; next: Human reviews the exact target, proof and evidence, then approves explicit claims
- Human approval: Thomas Tumini (human) at 2026-09-26T15:08:49 (READY_FOR_HUMAN → ACCEPT).

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017), found by query Bulgarian solitaire; abstract read, full text not relied upon.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022), found by query Bulgarian solitaire; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p3_c1.html (rendered), https://www.overleaf.com/docs?snip_uri=https://raw.githubusercontent.com/triborg0259/proof-pursuit/main/report/cells/p3_c1.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c1.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
