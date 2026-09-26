Problem 3 — Part 3 — submission (PARTIAL)

Declared status: PARTIAL. The cell is not solved. What follows is the intermediate progress actually established,
as judged by the automatic Referee (verdict UNKNOWN_STATUS: Provide the missing review or independently checked evidence).
The author's own declared status was LEMMA_CANDIDATE.

1. Result and scope

Complete written proofs of: (1) Brandt's characterisation of cyclic partitions (Theorem 1.2, needed as a tool); (2) D_B(n) ≤ k^2−2k−1 for all k ≥ 5 and all non-triangular n of rank k (Theorem 2.6), with k = 4 (n = 7, 8, 9) settled by an exhaustive exact computation (D_B = 4, 5, 7); (3) D_B(T_k−1) = k^2−2k−1 for all k ≥ 4, the maximum being attained by λ*_k = (k−1, k−2, k−2, k−3, …, 2, 1, 1), whose orbit is described in closed form (§3). Exact data: number of extremal partitions of T_k−1 is 1, 6, 34, 175, 831, 3911 for k = 4..9; the table D_B(n), n ≤ 45, agrees with Griggs–Ho's Figure 1 for n ≤ 36. NOT done: the characterisation of all partitions of T_k−1 attaining the maximum (the last sub-question of the cell).

2. Proof

Cell 3 — full proof of the upper bound $D_B(n)\le k^2-2k-1$ and of $D_B(T_k-1)=k^2-2k-1$

What is proved here. (A) For every $k\ge 4$ and every $n$ with $T_{k-1}<n<T_k$: $D_B(n)\le k^2-2k-1$.
(B) For every $k\ge 4$: $D_B(T_k-1)=k^2-2k-1$, the lower bound being attained by
$$\lambda^_k=(k-1,\;k-2,\;k-2,\;k-3,\;\dots,\;2,\;1,\;1)\qquad(\lambda^_1=k-1,\ \lambda^_2=k-2,\ \lambda^_i=k-i+1\ (3\le i\le k),\ \lambda^*_{k+1}=1).$$
Not proved here: the description of all partitions of $T_k-1$ attaining the maximum (see gaps).
The argument follows Griggs–Ho (1998), rewritten in full in a "pile lifetime" language with every step justified; nothing is merely cited: Brandt's characterisation of cyclic partitions is re-proved in §1.

Throughout, $n=T_{k-1}+r$ with $1\le r\le k$ ($k$ = rank of $n$); "non-triangular" means $1\le r\le k-1$.

§0. Cells, diagonals, and the shift on cells

For a partition $\lambda=(\lambda_1\ge\dots\ge\lambda_s)$ let $C(\lambda)=\{(i,j):1\le i\le s,\ 1\le j\le\lambda_i\}$ (row $i$ = $i$-th part). A finite set $X\subset\mathbb Z_{\ge1}^2$ is of the form $C(\lambda)$ iff it is left-justified (row $i$ of $X$ is $\{1,\dots,r_i\}$) with $r_1\ge r_2\ge\cdots$; then $\lambda$ = the nonzero $r_i$. $C(\lambda)$ is determined by the multiset of its row lengths. The diagonal of a cell is $w(i,j)=i+j-1$; $D_w=\{(i,w+1-i):1\le i\le w\}$ has $w$ cells. $\Delta_m:=\bigcup_{w\le m}D_w=C(\delta_m)$, $|\Delta_m|=T_m$. Transposition $(i,j)\mapsto(j,i)$ maps $C(\lambda)$ to $C(\lambda')$ and preserves diagonals.

Rotation. For a cell set $X$ put $\rho(X)=\{(i+1,j-1):(i,j)\in X,\ j\ge2\}\cup\{(1,i):(i,1)\in X\}$. On each $D_w$, $\rho$ is the cyclic permutation of rows $i\mapsto i+1$ ($1\le i\le w-1$), $w\mapsto1$; so $\rho$ is a bijection of $\mathbb Z_{\ge1}^2$ preserving diagonals. For $s\ge1$ put $\sigma_s(X)=\{(i-[j\ge s+1],\,j):(i,j)\in X\}$.

Lemma 0.1 (shift on cells). Let $\lambda$ have $s$ parts. Then $C(B(\lambda))=\sigma_s(\rho(C(\lambda)))$. Moreover $\rho(C(\lambda))$ has no cell in a column $\ge s+1$ iff $\lambda_1\le s+1$; in that case $C(B(\lambda))=\rho(C(\lambda))$, and if $\lambda_1\ge s+2$ then $\sigma_s$ moves at least one cell of $\rho(C(\lambda))$ (namely $(2,s+1)$) up by one row.

Proof. Directly from the definition, $\rho(C(\lambda))=\{(1,i):1\le i\le s\}\cup\{(i+1,j):1\le i\le s,\ 1\le j\le\lambda_i-1\}$: a left-justified set with row lengths $r_1=s$, $r_{i+1}=\lambda_i-1$ ($1\le i\le s$). Its nonzero row lengths form exactly the multiset of parts of $B(\lambda)$ (the parts are $s$ and the positive $\lambda_i-1$). The largest column index occurring is $\max(s,\lambda_1-1)$, whence the second sentence.
Case $\lambda_1\le s+1$: $r_1=s\ge\lambda_1-1=r_2\ge r_3\ge\cdots$, so $\rho(C(\lambda))$ is the left-justified set with weakly decreasing row lengths equal to the parts of $B(\lambda)$, i.e. $\rho(C(\lambda))=C(B(\lambda))$, and $\sigma_s$ acts trivially on it.
Case $\lambda_1\ge s+2$: let $p=\#\{i:\lambda_i-1>s\}\ge1$. The parts of $B(\lambda)$ in decreasing order are $\lambda_1-1,\dots,\lambda_p-1,\,s,\,\lambda_{p+1}-1,\dots$, so
$C(B(\lambda))=\{(i,j):i\le p,\ j\le\lambda_i-1\}\cup\{(p+1,j):j\le s\}\cup\{(i+1,j):i\ge p+1,\ j\le\lambda_i-1\}$.
In $\rho(C(\lambda))$ the rows $\ge p+2$ are $\{(i+1,j):i\ge p+1,j\le\lambda_i-1\}$ and lie in columns $\le\lambda_{p+1}-1\le s$, so $\sigma_s$ fixes them, and they coincide with the third set above. Rows $1,\dots,p+1$ of $\rho(C(\lambda))$ consist of the full rectangle $\{1,\dots,p+1\}\times\{1,\dots,s\}$ (because $r_1=s$ and $r_{i+1}=\lambda_i-1>s$ for $i\le p$) together with $\{(i+1,j):i\le p,\ s+1\le j\le\lambda_i-1\}$. $\sigma_s$ fixes the rectangle and moves the second set to $\{(i,j):i\le p,\ s+1\le j\le\lambda_i-1\}$. The union is $\{(i,j):i\le p,\ j\le\lambda_i-1\}\cup\{(p+1,j):j\le s\}$, which is exactly the first two sets above. Since $\lambda_1-1\ge s+1$, the cell $(2,s+1)$ belongs to $\rho(C(\lambda))$ and is moved. $\square$

Corollary 0.2 (potential). Let $\Phi(\lambda)=\sum_{(i,j)\in C(\lambda)}(i+j-1)$. Then $\Phi(B(\lambda))\le\Phi(\lambda)$, with equality iff $\lambda_1\le s(\lambda)+1$. (Indeed $\rho$ preserves diagonals and each cell moved by $\sigma_s$ lowers its diagonal by exactly $1$.)

Lemma 0.3 (pile lifetimes). Fix $\lambda\vdash n$ and write $\lambda^{(\tau)}=B^{\tau}(\lambda)$, $c_u=$ number of parts of $\lambda^{(u-1)}$ ($u\ge1$). Call the "piles" the parts of $\lambda$ (initial piles, of sizes $\lambda_j$ at time $0$) and, for each $u\ge1$, the new part $c_u$ created by the $u$-th shift (pile $u$, of size $c_u$ at time $u$). A pile of size $m$ at time $\tau_0$ has size $m-(\tau-\tau_0)$ at time $\tau\ge\tau_0$ and is alive at $\tau$ iff this is $\ge1$; it dies at time $\tau_0+m$. Then for every $\tau\ge0$, $\lambda^{(\tau)}$ is the multiset of sizes of the piles alive at time $\tau$; in particular $c_{\tau+1}=\#\{\text{piles alive at time }\tau\}$, pile $u$ is alive at time $\tau\ge u$ iff $c_u\ge\tau-u+1$, and
$$c_{\tau+1}=c_\tau+1-\#\{\text{piles that die at time }\tau\}\qquad(\tau\ge1).\qquad(0.3)$$
Proof. Induction on $\tau$ using the definition of $B$: each part alive at time $\tau-1$ loses one card (and disappears iff it had size $1$, i.e. dies at time $\tau$), and one new part equal to the number of parts $c_\tau$ appears. $\square$

Two immediate consequences used constantly: (a) $c_{\tau+1}\le c_\tau+1$; (b) if $c_{\tau+1}=c_\tau+1$ then no pile dies at time $\tau$, so every pile alive at time $\tau-1$ is alive at time $\tau$; if $c_{\tau+1}=c_\tau$ then exactly one pile dies at time $\tau$.

Lemma 0.4 (window sum). For $n=T_{k-1}+r$ and every $i\ge0$: $c_{i+1}+\dots+c_{i+k}\le k(k-1)+r$.
Proof. The sum counts pairs (time $\tau\in[i,i+k-1]$, pile alive at $\tau$). A pile alive at time $i$ with size $m$ contributes $\min(m,k)\le m$; these sizes sum to $n$. Pile $i+j$ ($1\le j\le k-1$) is alive only at times $\ge i+j$, contributing $\le k-j$. Total $\le n+\sum_{j=1}^{k-1}(k-j)=n+T_{k-1}=k(k-1)+r$. $\square$

Lemma 0.5 (sandwich). If $i<j$ and $c_i<x<c_j$ then there are $p,q$ with $i\le p<q\le j$, $q\ge p+2$ and $(c_p,c_{p+1},\dots,c_q)=(x-1,x,\dots,x,x+1)$.
Proof. Let $p$ be the largest index in $[i,j)$ with $c_p\le x-1$ (exists: $c_i\le x-1$; $p<j$ as $c_j>x$). Then $c_{p+1}\ge x$ and, by (a), $c_{p+1}\le c_p+1\le x$: so $c_p=x-1$, $c_{p+1}=x$. Let $q$ be the least index $>p$ with $c_q\ne x$ ($q\le j$ since $c_j\ne x$; $q\ge p+2$). By maximality of $p$, $c_q\ge x$, so $c_q\ge x+1$, and by (a) $c_q\le c_{q-1}+1=x+1$. $\square$

§1. Staircase-like partitions

Call $\mu\vdash n=T_{k-1}+r$ staircase-like if $C(\mu)=\Delta_{k-1}\cup S$ with $S\subseteq D_k$ (then $|S|=r$). Equivalently $\mu=(k-1+\varepsilon_1,k-2+\varepsilon_2,\dots,1+\varepsilon_{k-1},\varepsilon_k)$ with $\varepsilon\in\{0,1\}^k$, $\sum\varepsilon_i=r$, where $\varepsilon_i=[(i,k+1-i)\in C(\mu)]$.

Lemma 1.1. Let $\mu$ be staircase-like with occupancy vector $\varepsilon$. Then $\mu_1\le s(\mu)+1$, $C(B(\mu))=\rho(C(\mu))$, $B(\mu)$ is staircase-like with occupancy $(\varepsilon_k,\varepsilon_1,\dots,\varepsilon_{k-1})$, $B^k(\mu)=\mu$ (so $\mu$ is cyclic), and the number of parts of $B^i(\mu)$ is $k-1+\varepsilon_{k-i \bmod k}$ (index taken in $\{1,\dots,k\}$). Consequently the sequence $i\mapsto s(B^i(\mu))$ is $k$-periodic with values in $\{k-1,k\}$, takes the value $k$ exactly $r$ times per period, and any $k$ consecutive values sum to $k(k-1)+r$; if $1\le r\le k-1$ both values occur.
Proof. $\mu_1\in\{k-1,k\}$ and $s(\mu)=k-1+\varepsilon_k\in\{k-1,k\}$, so $\mu_1\le s+1$ and Lemma 0.1 gives $C(B(\mu))=\rho(C(\mu))$. $\rho$ permutes each $D_w$, fixes the full diagonals $D_1,\dots,D_{k-1}$ setwise and rotates $D_k$ by one row; iterating $k$ times gives the identity on $D_k$. The count of parts is $k-1+[(k,1)\in C]$, and $(k,1)\in C(B^i(\mu))$ iff $\varepsilon_{k-i}=1$. $\square$

Theorem 1.2 (Brandt). $\mu\vdash n$ is cyclic iff $\mu$ is staircase-like.
Proof. ($\Leftarrow$) Lemma 1.1. ($\Rightarrow$) Let $\mu$ be cyclic, $B^m(\mu)=\mu$. By Corollary 0.2, $\Phi(\mu)\ge\Phi(B(\mu))\ge\dots\ge\Phi(B^m(\mu))=\Phi(\mu)$, so every $\nu$ on the cycle satisfies $\nu_1\le s(\nu)+1$ and $C(B(\nu))=\rho(C(\nu))$. Hence $C(B^m(\mu))=\rho^m(C(\mu))$ for all $m\ge0$: on $D_w$ the row indices are shifted by $m$ modulo $w$.
Suppose $\mu$ is not staircase-like. Then either some $D_w$ with $w\le k-1$ is not full (and, since $|C(\mu)|=n>T_{k-1}-1$, some $D_{w'}$ with $w'\ge k>w$ is nonempty), or some $D_{w'}$ with $w'\ge k+1$ is nonempty (and, since $n\le T_k$, some $D_w$ with $w\le k<w'$ is not full). In both cases take $w''=\max\{v\in[w,w'-1]:D_v\not\subseteq C(\mu)\}$; then $D_{w''+1}$ is nonempty (it is full if $w''<w'-1$, and it is $D_{w'}$ otherwise). So there are $w$, a row $h$ with $(h,w+1-h)\notin C(\mu)$ and a row $b$ with $(b,w+2-b)\in C(\mu)$. By the Chinese remainder theorem ($\gcd(w,w+1)=1$) there is $m\ge0$ with $h+m\equiv w\pmod w$ and $b+m\equiv1\pmod{w+1}$. For $\nu=B^m(\mu)$: $(w,1)\notin C(\nu)$, so $s(\nu)\le w-1$; and $(1,w+1)\in C(\nu)$, so $\nu_1\ge w+1\ge s(\nu)+2$. Then $\Phi(B(\nu))<\Phi(\nu)$ (Corollary 0.2), contradicting constancy of $\Phi$ on the cycle. $\square$

Lemma 1.3 (recognition). Let $\lambda\vdash n=T_{k-1}+r$, $t'\ge1$, and suppose $c_{t'},\dots,c_{t'+k-1}\in\{k-1,k\}$ and $c_{t'+k}=c_{t'}$. Then $\mu:=B^{t'-1}(\lambda)$ is staircase-like.
Proof. Let $0\le i\le k-1$. The piles alive at time $t'-1+i$ are: the piles of $\mu$ (alive at time $t'-1$) of size $\ge i+1$, whose number is $\mu'_{i+1}$; and the piles $u\in[t',t'+i-1]$, all alive since $c_u\ge k-1\ge i\ge (t'+i-1)-u+1$. So $\mu'_{i+1}=c_{t'+i}-i\in\{k-1-i,k-i\}$. For $i=k$: pile $u\in[t'+1,t'+k-1]$ is alive at time $t'+k-1$ ($c_u\ge k-1\ge t'+k-u$), pile $t'$ is alive iff $c_{t'}\ge k$; thus $\mu'_{k+1}=c_{t'+k}-(k-1)-[c_{t'}=k]=c_{t'}-(k-1)-[c_{t'}=k]=0$. Hence $C(\mu')=\Delta_{k-1}\cup S'$ with $S'\subseteq D_k$, and transposing, $C(\mu)=\Delta_{k-1}\cup S$ with $S\subseteq D_k$. $\square$

§2. The upper bound

Fix $k\ge5$, $n=T_{k-1}+r$ with $1\le r\le k-1$, $\lambda\vdash n$, and the sequence $(c_u)$ of Lemma 0.3.

Choice of $t$. By finiteness the orbit reaches a cyclic partition $B^{t_0-1}(\lambda)$, which is staircase-like (Thm 1.2); by Lemma 1.1 all later terms are staircase-like and $(c_u)_{u\ge t_0}$ is $k$-periodic with both values $k-1,k$ present, so some $u\in[t_0,t_0+k-1]$ has $(c_u,c_{u+1})=(k-1,k)$. Let
$$t:=\min\{u\ge1:\ B^{u-1}(\lambda)\text{ staircase-like and }(c_u,c_{u+1})=(k-1,k)\}.$$
Then $d_B(\lambda)\le t-1$, and from index $t$ on Lemma 1.1 applies: $c_{u}\in\{k-1,k\}$ for $u\ge t$, $c_{u+k}=c_u$, and $c_t+\dots+c_{t+k-1}=k(k-1)+r$.

If $t\le k$ then $d_B(\lambda)\le k-1\le k^2-2k-1$. Assume $t\ge k+1$.

Lemma 2.1 (a pattern before $t$). At least one of the following holds:
(i) $(c_p,\dots,c_q)=(k-1,k,\dots,k,k+1)$ for some $t-k\le p<q\le t-1$, $q\ge p+2$;
(ii) $(c_p,\dots,c_q)=(k-2,k-1,\dots,k-1,k)$ for some $t-k+1\le p<q\le t+1$, $q\ge p+2$.
Proof. The $k$ piles $t-k,\dots,t-1$ exist ($t-k\ge1$); pile $t-1$ is alive at time $t-1$ ($c_{t-1}\ge1$); only $c_t=k-1$ piles are alive at time $t-1$. So some pile $i\in[t-k,t-2]$ is dead at time $t-1$; take $i$ largest, so piles $i+1,\dots,t-1$ are alive at time $t-1$. As $c_{t+1}=c_t+1$, no pile dies at time $t$ (0.3(b)), so pile $i+1$ is alive at time $t$: $c_{i+1}\ge t-i$. Pile $i$ dead at $t-1$: $c_i\le t-1-i$. With (a): $c_{i+1}\le c_i+1\le t-i$. Hence $c_i=t-i-1$, $c_{i+1}=t-i$.
Case $i\ge t-k+1$. $c_i\le k-2<k-1<k=c_{t+1}$; Lemma 0.5 with $x=k-1$ on $[i,t+1]$ gives (ii) with $p\ge i\ge t-k+1$.
Case $i=t-k$. Then $c_{t-k}=k-1$, $c_{t-k+1}=k$. If some $j\in[t-k+2,t-1]$ has $c_j\le k-2$: Lemma 0.5 ($x=k-1$) on $[j,t+1]$ gives (ii) with $p\ge j$. If some such $j$ has $c_j\ge k+1$: Lemma 0.5 ($x=k$) on $[t-k,j]$ gives (i). Otherwise $c_{t-k},\dots,c_{t-1}\in\{k-1,k\}$ and $c_t=k-1=c_{t-k}$, so Lemma 1.3 (with $t'=t-k$) shows $B^{t-k-1}(\lambda)$ staircase-like with $(c_{t-k},c_{t-k+1})=(k-1,k)$, contradicting the minimality of $t$. $\square$

Lemma 2.2 (long pattern of type (ii)). If $k\ge3$ and $(c_p,\dots,c_{p+k})=(k-2,k-1,\dots,k-1,k)$ then $p+k\le n+1$.
Proof. By 0.3(b): no pile dies at time $p+k-1$ (as $c_{p+k}=c_{p+k-1}+1$) and exactly one pile dies at each time $\tau\in[p+1,p+k-2]$ (as $c_{\tau+1}=c_\tau$). Pile $p+j$ ($1\le j\le k-1$) has size $k-1\ge k-j$, hence is alive at time $p+k-1$: these are $k-1$ alive piles; $c_{p+k}=k$, so exactly one further pile $P$ is alive at time $p+k-1$. Pile $p$ (size $k-2$) dies at time $p+k-2$, so $P\ne p$. If $P$ is an initial pile of size $\lambda_j$, then $\lambda_j\ge p+k$, so $p+k\le n$. Otherwise $P=u$ with $u\le p-1$. Suppose $u\ge2$. Pile $u-1$ is not alive at time $p+k-1$, hence (no deaths at $p+k-1$) not alive at time $p+k-2$; the unique pile dying at time $p+k-2$ is pile $p\neq u-1$ (it is alive at $p+k-3\ge p$), hence pile $u-1$ is not alive at time $p+k-3$: $c_{u-1}\le p+k-3-(u-1)=p+k-u-2$. But $u$ alive at $p+k-1$ gives $c_u\ge p+k-u$, so $c_u\ge c_{u-1}+2$, contradicting (a). So $u=1$ and $c_1\ge p+k-1$; as $c_1=s(\lambda)\le n$, $p+k\le n+1$. $\square$

Lemma 2.3 (short pattern). If $(c_p,c_{p+1},c_{p+2})=(x-1,x,x+1)$ then $p\le x$.
Proof. Suppose $p\ge x+1$. $x\ge2$ (as $c_p\ge1$), so $p\ge3$. Pile $p-1$ is alive at time $p-1$ and only $c_p=x-1\le p-2$ piles are alive then, so some pile $i\in[1,p-2]$ is dead at time $p-1$; take $i$ largest, so pile $i+1$ is alive at time $p-1$. No pile dies at times $p$ and $p+1$ (0.3(b)), so pile $i+1$ is alive at time $p+1$: $c_{i+1}\ge p-i+1$. Pile $i$ dead at $p-1$: $c_i\le p-1-i$. Thus $c_{i+1}\ge c_i+2$, contradicting (a). $\square$

Lemma 2.4 (descent). Let $q\ge p+3$, $(c_p,\dots,c_q)=(x-1,x,\dots,x,x+1)$ and $p\ge x+1$. Then there are $p',q'$ with $p-x\le p'\le p-2$, $2\le q'-p'\le q-p-1$ and $(c_{p'},\dots,c_{q'})=(x'-1,x',\dots,x',x'+1)$ where $x'=p-p'\le x$.
Proof. By 0.3(b): no pile dies at time $p$ ($c_{p+1}=c_p+1$), exactly one pile dies at each time $\tau\in[p+1,q-2]$, and no pile dies at time $q-1$. The $x$ piles $p-x,\dots,p-1$ exist ($p-x\ge1$); pile $p-1$ is alive at time $p-1$ and only $x-1$ piles are, so some pile $p'\in[p-x,p-2]$ is dead at time $p-1$; take $p'$ largest. Then piles $p'+1,\dots,p-1$ are alive at time $p-1$, hence (no deaths at $p$) alive at time $p$, as is pile $p$. So $c_{p'+1}\ge p-p'$; $c_{p'}\le p-1-p'$; by (a), $c_{p'+1}=p-p'$ and $c_{p'}=p-p'-1$; pile $p'+1$ dies at time $p+1$.
We show by induction on $m=1,2,\dots,q-p-1$: (H$_m$) either the lemma's conclusion holds with $q'-p'=m'$ for some $2\le m'\le m$, or $c_{p'+m'}=p-p'$ for all $1\le m'\le m$ and the piles $p'+m,\dots,p+m-1$ are alive at time $p+m-1$. (H$_1$) was just shown. Assume (H$_m$) in its second alternative with $m\le q-p-2$. Pile $p'+m$ has size $p-p'$ and dies at time $p+m$; it is alive at time $p+m-1$; since exactly one pile dies at time $p+m$, all other piles alive at $p+m-1$, i.e. $p'+m+1,\dots,p+m-1$, and the new pile $p+m$, are alive at time $p+m$. Pile $p'+m+1$ alive at time $p+m$ gives $c_{p'+m+1}\ge p-p'$, and (a) gives $c_{p'+m+1}\le c_{p'+m}+1=p-p'+1$. If $c_{p'+m+1}=p-p'+1$, then $(c_{p'},\dots,c_{p'+m+1})=(x'-1,x',\dots,x',x'+1)$ with $x'=p-p'$, $q'-p'=m+1\ge2$: the conclusion with $m'=m+1$. Otherwise $c_{p'+m+1}=p-p'$ and (H$_{m+1}$) holds. Finally, the second alternative of (H$_{q-p-1}$) is impossible: pile $p'+q-p-1$ would have size $p-p'$, be alive at time $q-2$ and die at time $(p'+q-p-1)+(p-p')=q-1$, whereas no pile dies at time $q-1$. Hence the first alternative of (H$_{q-p-1}$) holds, which is the lemma's conclusion with $x'=p-p'\le x$ and $2\le q'-p'\le q-p-1$. $\square$

Lemma 2.5. If $(c_p,\dots,c_q)=(x-1,x,\dots,x,x+1)$ with $q\ge p+2$ and $x\le k$, then $p\le (q-p-1)\,k$.
Proof. Induction on $q-p$. If $q-p=2$: Lemma 2.3 gives $p\le x\le k$. If $q-p\ge3$: either $p\le x\le k\le(q-p-1)k$, or Lemma 2.4 gives a pattern at $p'\ge p-x\ge p-k$ with $x'\le x\le k$, $2\le q'-p'\le q-p-1$; by induction $p'\le(q'-p'-1)k\le(q-p-2)k$, so $p\le p'+k\le(q-p-1)k$. $\square$

Theorem 2.6. $D_B(n)\le k^2-2k-1$ for $k\ge5$, $1\le r\le k-1$.
Proof. With $t\ge k+1$, Lemma 2.1 gives (i) or (ii). In (i), $p\ge t-k$, $q\le t-1$ force $q-p\le k-1$; in (ii), $q-p\le k$.
Case A: (ii) with $q-p=k$. Then $p=t-k+1$, $q=t+1$; Lemma 2.2: $t+1\le n+1$, so $d_B(\lambda)\le t-1\le n-1\le T_k-2=\tfrac{k^2+k-4}{2}\le k^2-2k-1$, the last inequality being $k^2-5k+2\ge0$, true for $k\ge5$.
Case B: $q-p\le k-2$. Here $x\in\{k,k-1\}$; Lemma 2.5: $p\le(k-3)k$. Since $p\ge t-k$ in both (i),(ii): $t\le p+k\le k^2-2k$, so $d_B(\lambda)\le t-1\le k^2-2k-1$.
Case C: $q-p=k-1$ — impossible. In (i): $p=t-k$, $q=t-1$, so $c_{t-1}=k+1$. But Lemma 0.4 on $c_{t-1},\dots,c_{t+k-2}$ and $c_t+\dots+c_{t+k-1}=k(k-1)+r$ give $c_{t-1}\le c_{t+k-1}\le k$. Contradiction. In (ii): $p\in\{t-k+1,t-k+2\}$. If $p=t-k+1$ then $q=t$ and $c_t=k\ne k-1$. If $p=t-k+2$ then $c_{t-k+2}=k-2$: pile $t-k+2$ has size $1$ at time $t-1$, hence dies at time $t$, but $c_{t+1}=c_t+1$ means no pile dies at time $t$. Contradiction.
Since $2\le q-p\le k$, the cases are exhaustive. $\square$

Case $k=4$ (exhaustive computation, exact integer arithmetic). $n\in\{7,8,9\}$; the script verifica_k4.py enumerates all partitions ($15,22,30$ of them), computes $d_B$ for each by following orbits, and finds $D_B(7)=4$, $D_B(8)=5$, $D_B(9)=7$, all $\le 7=4^2-2\cdot4-1$ (wall-clock $<0.01$ s). This completes (A) for all $k\ge4$.

§3. The exact value $D_B(T_k-1)=k^2-2k-1$ ($k\ge4$)

Upper bound: §2 with $r=k-1$. Lower bound: $d_B(\lambda^_k)=k^2-2k-1$ where $C(\lambda^_k)=\Delta_{k-1}\cup\{(i,k+1-i):3\le i\le k\}\cup\{(k+1,1)\}$ (rows: $k-1,\,k-2,\,k-2,\dots,2,1,1$; size $T_{k-1}+(k-2)+1=T_k-1$).

Put $J=k^2-2k-2=1+(k-3)(k+1)$. For $j\ge0$ let $X_j=\rho^j(C(\lambda^*_k))$. Since $\rho$ rotates each diagonal by one row, $X_j=\Delta_{k-1}\cup\{(i,k+1-i):1\le i\le k,\ i\not\equiv j+1,j+2\ (\bmod k)\}\cup\{(a_j,k+2-a_j)\}$ with $a_j\in\{1,\dots,k+1\}$, $a_j\equiv j\pmod{k+1}$ (the two holes of $D_k$ start at rows $1,2$ and the extra cell of $D_{k+1}$ starts at row $k+1\equiv0$).

Claim. For $0\le j\le J$: $C(B^j(\lambda^_k))=X_j$. Proof by induction on $j$. $j=0$ is the definition. Let $0\le j\le J-1$ and $C(B^j(\lambda^_k))=X_j$; write $\nu=B^j(\lambda^_k)$. Rows $1,\dots,k-1$ of $\nu$ are nonempty; row $k+1$ nonempty implies row $k$ nonempty (it is a partition), so $s(\nu)=k-1+[(k,1)\in X_j]+[a_j=k+1]$ and $\nu_1=k-1+[(1,k)\in X_j]+[a_j=1]$. Thus $\nu_1\ge s(\nu)+2$ forces $a_j=1$, $(k,1)\notin X_j$, i.e. $j\equiv1\pmod{k+1}$ and $k\equiv j+1$ or $j+2\pmod k$, i.e. $j\equiv-1$ or $-2\pmod k$. Writing $j=1+m(k+1)$, $j\equiv 1+m\pmod k$, so $m\equiv k-2$ or $k-3\pmod k$; the least such $j\ge0$ are $1+(k-3)(k+1)=J$ and $1+(k-2)(k+1)>J$. Hence for $j\le J-1$ we have $\nu_1\le s(\nu)+1$, and Lemma 0.1 gives $C(B^{j+1}(\lambda^_k))=\rho(X_j)=X_{j+1}$. $\square$

Each $X_j$ ($0\le j\le J$) contains a cell of $D_{k+1}$, so $B^j(\lambda^_k)$ is not staircase-like, hence not cyclic (Theorem 1.2): $d_B(\lambda^_k)\ge J+1$. At $j=J$: $\nu=B^J(\lambda^_k)$ has $a_J=1$ (as $J\equiv1\pmod{k+1}$) and, as $J\equiv k-2\pmod k$, the holes of $D_k$ are at rows $k-1$ and $k$; so $(1,k)\in X_J$, $(k,1)\notin X_J$, $\nu_1=k+1$, $s(\nu)=k-1$, and Lemma 0.1 gives $C(B^{J+1}(\lambda^_k))=\sigma_{k-1}(\rho(X_J))$. Now $\rho(X_J)=\Delta_{k-1}\cup(D_k\setminus\{(k,1),(1,k)\})\cup\{(2,k)\}$ (the holes rotate to rows $k$ and $1$, the extra cell $(1,k+1)$ goes to $(2,k)$); its only cell in a column $\ge k$ is $(2,k)$, moved by $\sigma_{k-1}$ to $(1,k)$. Hence $C(B^{J+1}(\lambda^_k))=\Delta_{k-1}\cup(D_k\setminus\{(k,1)\})=C((k,k-1,\dots,2))$, which is staircase-like, hence cyclic. Therefore $d_B(\lambda^_k)=J+1=k^2-2k-1$, and with §2, $D_B(T_k-1)=k^2-2k-1$ for all $k\ge4$. (Check: $k=4$: $\lambda^=(3,2,2,1,1)$, $d_B=7$; the script confirms $d_B(\lambda^_k)=k^2-2k-1$ for $4\le k\le12$ and $D_B(T_k-1)=k^2-2k-1$ for $4\le k\le9$ — sanity checks only, not part of the proof.)

§4. On the extremal partitions of $T_k-1$ (not resolved here)

Exact computation gives the number of $\lambda\vdash T_k-1$ with $d_B(\lambda)=k^2-2k-1$: $1,6,34,175,831,3911$ for $k=4,\dots,9$ (e.g. $k=5$: $(4,3,3,2,1,1),(4,3,2,2,2,1),(4,3,2,2,1,1,1),(3,3,3,2,2,1),(3,3,3,2,1,1,1),(3,3,2,2,2,1,1)$). A structural description is left to a later iteration; the proof of Theorem 2.6 shows that any extremal $\lambda$ must fall in Case B with all inequalities tight ($t=k^2-2k$, pattern (i) with $p=t-k$, $q-p=k-2$, and every descent step of Lemma 2.4 losing exactly $k$), which is the natural starting point.

3. Verification: instructions, dependencies, timings

Python 3 standard library. Scripts (re-run by the orchestrator, see runs/p3_c3/verifica/):
- code_1 (python, rigor exact): Certificato esaustivo per il caso k=4 (n = 7, 8, 9: tutte le 15+22+30 partizioni, d_B calcolato seguendo l'orbita; verifica D_B(n) <= 7) e controlli di sanita' (d_B(lambda*_k) = k^2-2k-1 per k=4..12; D_B(T_k-1) = k^2-2k-1 per k=4..9). Aritmetica intera esatta; insieme finito coperto: tutte le partizioni di 7, 8, 9 (per la prova) e di 14,20,27,35,44 (solo controllo). Tempo totale misurato: 0.49 s. Eseguire: .venv/bin/python verifica_k4.py nella cartella runs/p3_c3/sandbox (importa db_table.py).
- code_2 (python, rigor exact): Modulo di supporto (db_table.py): enumerazione delle partizioni di n, shift B, calcolo di d_B per tutte le partizioni via esplorazione del grafo funzionale (colorazione dei cammini; un off-by-one nella prima versione — base = -1 — e' stato corretto in base = 0 dopo il confronto con la tabella di Griggs–Ho). Eseguito da solo stampa D_B(n) e le estremali per n <= NMAX (n <= 45 in ~2 s totali).
- code_3 (python, rigor exact): Esplorazione (non usata nella prova): stampa l'orbita di lambda*_k in forma diagonale (diagonali < k piene, buchi sulla diagonale k, cella extra sulla diagonale k+1); ha suggerito la forma chiusa X_j di §3.

4. Sources and contribution

- J. R. Griggs, C.-C. Ho, The cycling of partitions and compositions under repeated shifts, Adv. Appl. Math. 21 (1998) 205–227, doi:10.1006/aama.1998.0597 — READ in the authors' preprint version https://people.math.sc.edu/griggs/cycling.pdf (Mar. 2, 1998; 22 pp.). Used: overall strategy (Prop. 3.2, Lemmas 3.3–3.6, 4.3, Thm 4.4) and the extremal partition of Thm 4.4(2); every statement re-proved above; their Figure 1 (D_B(n), 4 ≤ n ≤ 36) used to cross-check my table.
- J. Brandt, Cycles of partitions, Proc. AMS 85 (1982) 483–486 — NOT read; cited by Griggs–Ho for the characterisation of cyclic partitions, which is re-proved in §1 (Theorem 1.2).
- arXiv:2607.17194 (Meštrović 2026), arXiv:1503.00885 (Drensky 2015) — abstracts only; context (surveys), not used in the proof.
- Position with respect to the literature: The arXiv abstracts listed (math/0401385, 1503.00885, 2607.17194, 1101.1546, 1703.07102, 2208.14496) do not treat D_B(n) for non-triangular n; 2607.17194 and 1503.00885 are surveys citing Brandt (1982) for the cyclic partitions, 1101.1546 concerns Toom's convergence proof. The relevant source is not on arXiv: J. R. Griggs, C.-C. Ho, 'The cycling of partitions and compositions under repeated shifts', Adv. Appl. Math. 21 (1998) 205–227 (doi:10.1006/aama.1998.0597); I downloaded and read the authors' preprint (people.math.sc.edu/griggs/cycling.pdf, dated Mar. 2, 1998). Its Theorem 4.4 states: '(1) D_B(n) ≤ k^2−2k−1 for k ≥ 4 [n = 1+…+(k−1)+r, 1 ≤ r < k]; (2) equality holds when k ≥ 4 and r = k−1', with the extremal partition λ_1=k−1, λ_2=k−2, λ_i=k−i+1 (3≤i≤k), λ_{k+1}=1 and the remark 'imitating the proof of Theorem 3.1, we can show d_B(λ)=k^2−2k−1' (no details). My attempt FOLLOWS Griggs–Ho's strategy but reproduces every proof in full (as required: citing does not count), in a 'pile lifetime' formalism equivalent to their diagram_B; it ADAPTS their Lemma 3.5 (dropping the constraint q' ≤ p+1, which their own proof does not establish and which is not needed) and their Theorem 2.1 proof (their CRT sketch is written out with the potential Φ), and SUPPLIES the omitted lower-bound orbit computation for λ*_k. Griggs–Ho give, for triangular n, only necessary conditions on extremal partitions (their Thm 3.8, converse false for k=8) and nothing for T_k−1, consistent with my leaving that sub-question open.

5. Limits and unresolved parts

Referee's blocking point: —
Next step required: Provide the missing review or independently checked evidence
Gaps declared by the author:
- The cell also asks 'which partitions attain the maximum' for n = T_k−1: not determined here. Computation shows the extremal set is large (1, 6, 34, 175, 831, 3911 partitions for k = 4..9), so a structural description is needed; only the explicit extremal family λ*_k and the necessary condition 'Case B with all inequalities tight' are given.
- The case k = 4 of the upper bound relies on an exhaustive computation over the partitions of 7, 8, 9 (code included, exact, < 0.01 s) rather than on the general argument (Case A of Theorem 2.6 needs k ≥ 5).
- Lemma 0.3 (pile-lifetime bookkeeping) is proved by a short induction stated in words; a hostile reader may want it spelled out formally (it is a direct restatement of the definition of B with parts tracked individually).
- In Lemma 1.1 the formula 'number of parts of B^i(μ) = k−1+ε_{k−i mod k}' uses that the occupancy vector is rotated by one position per step; this follows from ρ shifting rows by +1 on D_k, as stated, but the index bookkeeping (representatives in {1..k}) is compressed.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family direct_proof, subgoal: Prove the general upper bound D_B(n) ≤ k^2−2k−1 for every non-triangular n of rank k ≥ 4, and prove D_B(T_k−1) = k^2−2k−1 exactly (lower bound via an explicit partition λ*_k), as a single self-contained argument (Brandt's characterisation of cyclic partitions re-proved inside).; declared LEMMA_CANDIDATE.
  - Why this approach: No blocker and no verified claims: the natural first subgoal is the whole quantitative content of the cell (general bound + exact value at T_k−1). The literature (Griggs–Ho 1998) contains a proof sketch of exactly this bound; the rules allow a proof 'written out in full, whatever its source', so I fetched the preprint, reconstructed every lemma in a cleaner language, filled the gaps (their proof of Brandt's theorem is a sketch; their Lemma 3.5 statement contains an unused/incorrect constraint q' ≤ p+1 which I dropped; their Lemma 3.3 uses Theorem 2.1 in a way I replaced by an explicit recognition lemma), and verified numerically that the value is k^2−2k−1 (an off-by-one bug in my first table, which suggested k^2−2k−2, was found and fixed by comparing with Griggs–Ho's Figure 1). The characterisation of all extremal partitions of T_k−1 is deliberately left for a later iteration.
  - Position w.r.t. the literature: The arXiv abstracts listed (math/0401385, 1503.00885, 2607.17194, 1101.1546, 1703.07102, 2208.14496) do not treat D_B(n) for non-triangular n; 2607.17194 and 1503.00885 are surveys citing Brandt (1982) for the cyclic partitions, 1101.1546 concerns Toom's convergence proof. The relevant source is not on arXiv: J. R. Griggs, C.-C. Ho, 'The cycling of partitions and compositions under repeated shifts', Adv. Appl. Math. 21 (1998) 205–227 (doi:10.1006/aama.1998.0597); I downloaded and read the authors' preprint (people.math.sc.edu/griggs/cycling.pdf, dated Mar. 2, 1998). Its Theorem 4.4 states: '(1) D_B(n) ≤ k^2−2k−1 for k ≥ 4 [n = 1+…+(k−1)+r, 1 ≤ r < k]; (2) equality holds when k ≥ 4 and r = k−1', with the extremal partition λ_1=k−1, λ_2=k−2, λ_i=k−i+1 (3≤i≤k), λ_{k+1}=1 and the remark 'imitating the proof of Theorem 3.1, we can show d_B(λ)=k^2−2k−1' (no details). My attempt FOLLOWS Griggs–Ho's strategy but reproduces every proof in full (as required: citing does not count), in a 'pile lifetime' formalism equivalent to their diagram_B; it ADAPTS their Lemma 3.5 (dropping the constraint q' ≤ p+1, which their own proof does not establish and which is not needed) and their Theorem 2.1 proof (their CRT sketch is written out with the potential Φ), and SUPPLIES the omitted lower-bound orbit computation for λ*_k. Griggs–Ho give, for triangular n, only necessary conditions on extremal partitions (their Thm 3.8, converse false for k=8) and nothing for T_k−1, consistent with my leaving that sub-question open.
  - Referee: UNKNOWN_STATUS / INCOMPLETE; next: Provide the missing review or independently checked evidence

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

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p3_c3.html (rendered), https://www.overleaf.com/docs?snip_uri=https%3A%2F%2Fraw.githubusercontent.com%2Ftriborg0259%2Fproof-pursuit%2Fmain%2Freport%2Fcells%2Fp3_c3.tex&snip_name=p3_c3.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c3.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
