# Cell 2: $D_B(T_k)=k^2-k$ for every $k\ge 1$

Throughout, $n=T_k=k(k+1)/2$, $\delta_k=(k,k-1,\dots,1)$, and for a partition $\lambda$ we write $\ell(\lambda)$ for its number of parts. The result is

**Theorem.** For every $k\ge1$, $D_B(T_k)=k^2-k$. The maximum is attained by $\gamma_k=(k-1,k-1,k-2,\dots,2,1,1)$ for $k\ge2$ (and by $\gamma_1=(1)$).

The proof has three parts: (I) the cell rule for $B$, convergence to $\delta_k$ and uniqueness of the cyclic partition (so that $d_B(\lambda)=\min\{m: B^m(\lambda)=\delta_k\}$); (II) the lower bound via $\gamma_k$; (III) the upper bound via the sequence of pile counts. Part III follows the method of Griggs–Ho (Adv. Appl. Math. 21 (1998), Thm. 3.7), which we read in full and rewrite here completely, with the inductions that the paper only sketches written out.

---

## Part I. Cells, diagonals, convergence

### Conventions
Draw $\lambda=(\lambda_1\ge\dots\ge\lambda_s)$ as the set of **cells** $(i,h)$ with $1\le i\le s$, $1\le h\le\lambda_i$ (column $i$ = pile $i$, $h$ = height). The **diagonal** of $(i,h)$ is $d(i,h)=i+h-1$; diagonal $d$ consists of the $d$ **slots** $(p,d+1-p)$, $p=1,\dots,d$ (we call $p$ the slot number). A set of cells is the diagram of a partition iff its column heights are weakly decreasing and each column is an initial segment of heights. $\delta_k$ is the diagram in which diagonals $1,\dots,k$ are full (all slots occupied) and all others are empty.

### Lemma 1 (cell rule)
Let $\lambda$ have $s$ parts and define, on the cells of $\lambda$,
1. $\varphi(i,1)=(1,i)$ for $1\le i\le s$;
2. $\varphi(i,h)=(i+1,h-1)$ if $2\le h\le s+1$;
3. $\varphi(i,h)=(i,h-1)$ if $h\ge s+2$.

Then $\varphi$ is injective and its image is exactly the diagram of $B(\lambda)$. Cells of type 1–2 stay on their diagonal, their slot number changing by the cyclic shift $\rho_d:p\mapsto p+1$ ($p<d$), $d\mapsto 1$; cells of type 3 move from diagonal $d$ to diagonal $d-1$, keeping their column.

*Proof.* Let $q=\#\{i:\lambda_i\ge s+2\}$; since $\lambda$ is sorted these are $i=1,\dots,q$. The parts of $B(\lambda)$ are $s$ together with $\lambda_i-1$ for $\lambda_i\ge 2$; since $\lambda_i-1\ge s+1>s$ exactly for $i\le q$, the sorted $B(\lambda)$ has column heights
$$\lambda_1-1,\dots,\lambda_q-1,\ s,\ \lambda_{q+1}-1,\ \lambda_{q+2}-1,\dots$$
(columns of height $0$ discarded). Now list the image of $\varphi$ column by column. Column 1 receives heights $1,\dots,s$ from rule 1 and, if $q\ge1$, heights $s+1,\dots,\lambda_1-1$ from rule 3 with $i=1$: total height $\lambda_1-1$ if $q\ge1$, $s$ if $q=0$. For $2\le c\le q$, column $c$ receives heights $1,\dots,\min(\lambda_{c-1},s+1)-1=1,\dots,s$ from rule 2 with $i=c-1$ (as $\lambda_{c-1}\ge s+2$) and heights $s+1,\dots,\lambda_c-1$ from rule 3 with $i=c$: total $\lambda_c-1$. If $q\ge1$, column $q+1$ receives heights $1,\dots,s$ from rule 2 with $i=q$ and nothing from rule 3: height $s$. For $c\ge q+2$, column $c$ receives heights $1,\dots,\lambda_{c-1}-1$ from rule 2 with $i=c-1$ (as $\lambda_{c-1}\le s+1$) and nothing else. In every column the received heights are contiguous from $1$ and the contributions of the three rules are disjoint, so $\varphi$ is injective and its image is precisely the diagram of $B(\lambda)$ listed above. The statements about diagonals and slots are read off from the formulas: $d(1,i)=i=d(i,1)$ and slot $i=d\mapsto 1$; $d(i+1,h-1)=d(i,h)$ and slot $i\mapsto i+1$; $d(i,h-1)=d(i,h)-1$. $\square$

**Consequences.** (a) *Rotation.* If $\lambda_1\le s+1$ (no cell of type 3), then for every $d$ the set of occupied slots of diagonal $d$ in $B(\lambda)$ is the image under $\rho_d$ of the set of occupied slots of diagonal $d$ in $\lambda$; the same holds for the set of empty slots ("holes").
(b) *Potential.* Let $W(\lambda)=\sum_{\text{cells}}d(i,h)\ (\ge 0)$. Then $W(B(\lambda))=W(\lambda)-\#\{(i,h)\in\lambda:h\ge s+2\}$; in particular $W(B(\lambda))\le W(\lambda)$, with equality iff $\lambda_1\le s+1$.

### Lemma 2 (convergence and uniqueness)
Let $|\lambda|=T_k$. Then $B^m(\lambda)=\delta_k$ for some $m\ge0$; $B(\delta_k)=\delta_k$; and $\delta_k$ is the only cyclic partition of $T_k$. Consequently $d_B(\lambda)=\min\{m\ge0:B^m(\lambda)=\delta_k\}$.

*Proof.* $B(\delta_k)$ has parts $k-1,\dots,1$ and the new part $k$, so $B(\delta_k)=\delta_k$.

*Claim: if $\mu\vdash T_k$ and $\mu\ne\delta_k$, there is a diagonal $w$ with an empty slot such that diagonal $w+1$ contains a cell.* Let $D$ be the largest occupied diagonal. If diagonals $1,\dots,D-1$ are all full, then $T_{D-1}<|\mu|\le T_D$, so $D=k$ and diagonal $k$ is full ($|\mu|=T_k=T_{k-1}+k$), i.e. $\mu=\delta_k$. Otherwise let $w\le D-1$ be the largest diagonal with an empty slot; diagonal $w+1\le D$ is full (if $w+1<D$) or equals $D$ (nonempty); either way it contains a cell.

Now take any $\lambda\vdash T_k$. By (b), $W(B^m(\lambda))$ is a non-increasing sequence of non-negative integers, so only finitely many steps have $W$ strictly decreasing; let $m_0$ be such that no step from time $m_0$ on decreases $W$, i.e. by (b) every $B^m(\lambda)$, $m\ge m_0$, satisfies $\lambda^{(m)}_1\le s_m+1$ ($s_m$ = number of parts). Suppose $\mu=B^{m_0}(\lambda)\ne\delta_k$ and take $w$ as in the claim: a hole at slot $p_0$ of diagonal $w$ and a cell at slot $p_1$ of diagonal $w+1$. By (a), applied at each step $m\ge m_0$, at time $m_0+u$ diagonal $w$ has a hole at the slot $\equiv p_0+u\pmod w$ and diagonal $w+1$ has a cell at the slot $\equiv p_1+u\pmod{w+1}$ (representatives in $\{1,\dots,w\}$, $\{1,\dots,w+1\}$). Since $\gcd(w,w+1)=1$, by the Chinese remainder theorem there is $u\ge0$ with $p_0+u\equiv w\pmod w$ and $p_1+u\equiv1\pmod{w+1}$. At time $m=m_0+u$: slot $w$ of diagonal $w$ is the position $(w,1)$, and it is empty, so column $w$ is empty and $s_m\le w-1$; slot $1$ of diagonal $w+1$ is the position $(1,w+1)$, and it is a cell, so $\lambda^{(m)}_1\ge w+1\ge s_m+2$. This contradicts $\lambda^{(m)}_1\le s_m+1$. Hence $B^{m_0}(\lambda)=\delta_k$, and $B^m(\lambda)=\delta_k$ for all $m\ge m_0$.

If $\mu$ is cyclic, $B^P(\mu)=\mu$ with $P\ge1$, choose $m$ with $B^m(\mu)=\delta_k$; then $\mu=B^{P\lceil m/P\rceil}(\mu)=\delta_k$ because $P\lceil m/P\rceil\ge m$ and $\delta_k$ is fixed. So $\delta_k$ is the unique cyclic partition, and by definition $d_B(\lambda)=\min\{m:B^m(\lambda)=\delta_k\}$. $\square$

---

## Part II. Lower bound: $d_B(\gamma_k)=k^2-k$

**Theorem A.** For every $k\ge1$, $D_B(T_k)\ge k^2-k$, attained by $\gamma_k=(k-1,k-1,k-2,\dots,2,1,1)$ ($k\ge2$), $\gamma_1=(1)$.

*Proof.* For $k=1$, $D_B(1)=0=k^2-k$. Let $k\ge2$. For $p_H\in\{1,\dots,k\}$ and $p_X\in\{1,\dots,k+1\}$ let $S(p_H,p_X)$ be the set of cells of $\delta_k$ with the cell $(p_H,k+1-p_H)$ removed (a hole in slot $p_H$ of diagonal $k$) and the cell $(p_X,k+2-p_X)$ added (an extra cell in slot $p_X$ of diagonal $k+1$). Its column heights are $k+1-p$ for $p\notin\{p_H,p_X\}$, $k-p_H$ for $p=p_H$, $k+2-p_X$ for $p=p_X$ (column $k+1$ exists iff $p_X=k+1$). It is a partition diagram iff $p_X\ne p_H$ and $p_X\ne p_H+1$: if $p_X=p_H$ the added cell sits above a missing one; if $p_X=p_H+1$ column $p_X$ would be taller than column $p_H$; otherwise heights are weakly decreasing, since column $p_X$ has the height of column $p_X-1$ and column $p_H$ has the height of column $p_H+1$. Note $\gamma_k=S(1,k+1)$ (columns $k-1,k-1,k-2,\dots,2,1,1$), and every $S(p_H,p_X)$ has $|S|=T_k$ and $S\ne\delta_k$.

Number of columns of $S(p_H,p_X)$: $s=k+1$ if $p_X=k+1$; $s=k-1$ if $p_H=k$ (then $p_X\le k$... indeed $p_X\ne k+1=p_H+1$); $s=k$ otherwise. All columns have height $\le k$ except column $p_X$ of height $k+2-p_X\le k+1$, with equality iff $p_X=1$. Hence a cell of height $\ge s+2$ exists only when $s=k-1$ and $p_X=1$, i.e. only in $S(k,1)$, where it is the single cell $(1,k+1)$.

*Case $S(k,1)$.* Here $s=k-1$ and $S(k,1)=(k+1,k-1,k-2,\dots,2)$; by Lemma 1: rule 1 sends the bottom row to column 1 with heights $1,\dots,k-1$; rule 2 sends every other cell $(i,h)$, $2\le h\le k$, to $(i+1,h-1)$, giving columns $2,\dots,k$ of heights $k-1,\dots,1$; rule 3 sends $(1,k+1)$ to $(1,k)$, completing column 1 to height $k$. So $B(S(k,1))=\delta_k$.

*Other cases.* No cell of type 3, so by Consequence (a) every diagonal rotates by $\rho_d$, holes included: $B(S(p_H,p_X))=S(p_H',p_X')$ with $p_H'\equiv p_H+1\pmod k$, $p_X'\equiv p_X+1\pmod{k+1}$ (Lemma 1 guarantees the result is a partition diagram).

Starting from $\gamma_k=S(1,k+1)$, as long as the orbit has not visited $S(k,1)$ we have $B^t(\gamma_k)=S(p_H(t),p_X(t))$ with $p_H(t)\equiv1+t\pmod k$, $p_X(t)\equiv t\pmod{k+1}$, none of which is $\delta_k$. The first $t\ge0$ with $(p_H(t),p_X(t))=(k,1)$ satisfies $t\equiv k-1\pmod k$, $t\equiv1\pmod{k+1}$; writing $t=k-1+ak$, $k-1+ak\equiv-2-a\equiv1\pmod{k+1}$, so $a\equiv k-2\pmod{k+1}$ and the least $a\ge0$ is $a=k-2$. Thus $t_0=k-1+(k-2)k=k^2-k-1$, $B^t(\gamma_k)\ne\delta_k$ for $0\le t\le k^2-k-1$, and $B^{k^2-k}(\gamma_k)=B(S(k,1))=\delta_k$. By Lemma 2, $d_B(\gamma_k)=k^2-k$. $\square$

---

## Part III. Upper bound: $d_B(\lambda)\le k^2-k$ for every $\lambda\vdash T_k$

### The pile-count sequence and the bookkeeping lemma
Fix a partition $\lambda=(\lambda_1,\dots,\lambda_s)\vdash n$ (any $n\ge1$ in this subsection). For $i\ge1$ put
$$c_i:=\ell\big(B^{i-1}(\lambda)\big)\ \ (\ge1).$$
The step $B^{i-1}(\lambda)\to B^{i}(\lambda)$ creates a new part of size $c_i$; call it the pile $P_i$.

**Lemma 3 (bookkeeping).** For every $m\ge0$ the parts of $B^m(\lambda)$ are exactly
$$\{\lambda_j-m:\ \lambda_j>m\}\ \cup\ \{c_i-(m-i):\ 1\le i\le m,\ c_i>m-i\}$$
(as a multiset). Consequently
$$c_{m+1}=\#\{j:\lambda_j\ge m+1\}+\#\{i\in[1,m]:\ c_i\ge m+1-i\}.\tag{3.1}$$

*Proof.* Induction on $m$. For $m=0$ the parts are the $\lambda_j$. If the statement holds for $m$, then $B^{m+1}(\lambda)$ consists of each listed part decreased by $1$, dropping those that become $0$—giving $\lambda_j-(m+1)$ for $\lambda_j>m+1$ and $c_i-(m+1-i)$ for $i\le m$, $c_i>m+1-i$—together with one new part equal to $\ell(B^m(\lambda))=c_{m+1}=c_{m+1}-((m+1)-(m+1))$, which is the term $i=m+1$ (present since $c_{m+1}\ge1>0$). Formula (3.1) counts the parts. $\square$

We encode (3.1) with the indicators ("$P_j$ is alive at time $i-1$", "$\lambda_j$ is alive at time $i-1$"):
$$e_{i,j}:=[\,c_j\ge i-j\,]\ (1\le j<i),\qquad f_{i,j}:=[\,\lambda_j\ge i\,],\qquad\text{so}\qquad c_i=\sum_{j}f_{i,j}+\sum_{j=1}^{i-1}e_{i,j}.\tag{3.2}$$
Two facts are used constantly: $e_{i,i-1}=1$ (as $c_{i-1}\ge1$), and, for fixed $j$, $e_{i,j}=1$ exactly for $j+1\le i\le j+c_j$ (a column of $c_j$ ones followed by zeros); likewise $f_{i,j}=1$ exactly for $i\le\lambda_j$.

**Lemma 4 (deaths).** For $i\ge1$ let $\delta_i:=c_i+1-c_{i+1}$. Then $\delta_i$ is the number of parts equal to $1$ in $B^{i-1}(\lambda)$; hence $c_{i+1}\le c_i+1$. Moreover
$$\delta_i=\sum_j (f_{i,j}-f_{i+1,j})+\sum_{j=1}^{i-1}(e_{i,j}-e_{i+1,j}),$$
where every summand is $0$ or $1$. In particular: if $\delta_i=0$ then $e_{i+1,j}=e_{i,j}$ for all $j<i$; if $\delta_i=1$ and $j_0<i$ satisfies $e_{i,j_0}=1$, $e_{i+1,j_0}=0$, then $e_{i+1,j}=e_{i,j}$ for all $j<i$, $j\ne j_0$.

*Proof.* $B^{i}(\lambda)$ has one new part and one part for each part $\ge2$ of $B^{i-1}(\lambda)$, so $c_{i+1}=1+c_i-\#\{\text{parts }=1\}$. By Lemma 3 the parts equal to $1$ of $B^{i-1}(\lambda)$ are $\lambda_j-(i-1)=1$, i.e. $\lambda_j=i$, i.e. $f_{i,j}-f_{i+1,j}=1$, and $c_j-(i-1-j)=1$, i.e. $c_j=i-j$, i.e. $e_{i,j}-e_{i+1,j}=1$; all other summands are $0$ by the monotonicity of the columns. The two particular statements follow since the summands are non-negative. $\square$

**Definition.** For integers $x$ and $p<q$ with $q\ge p+2$ we say that the sequence has an **$x$-pattern on $[p,q]$** if
$$(c_p,c_{p+1},\dots,c_{q-1},c_q)=(x-1,x,\dots,x,x+1).$$
Since $c_p\ge1$, an $x$-pattern forces $x\ge2$; and $\delta_p=0$, $\delta_{q-1}=0$, $\delta_i=1$ for $p<i<q-1$.

**Lemma 5 (sandwich).** If $i<j$ and $c_i<x<c_j$, then there is an $x$-pattern on some $[p,q]$ with $i\le p<q\le j$.

*Proof.* Let $p$ be the largest index in $[i,j)$ with $c_p\le x-1$ (it exists since $c_i\le x-1$). Then $c_{p+1}\ge x$: by maximality if $p+1<j$, and because $c_j>x$ if $p+1=j$. By Lemma 4, $c_{p+1}\le c_p+1\le x$, so $c_p=x-1$, $c_{p+1}=x$. Every $m\in(p,j]$ has $c_m\ge x$ (maximality for $m<j$, hypothesis for $m=j$). Let $q$ be the least index $>p$ with $c_q\ne x$; $q\le j$ since $c_j\ne x$, and $q\ge p+2$. Then $c_q\ge x+1$ and $c_q\le c_{q-1}+1=x+1$. $\square$

### The end of the orbit when $n=T_k$
**Lemma 6.** Let $n=T_k$, $k\ge1$, $\lambda\vdash n$, $t=d_B(\lambda)$ (finite by Lemma 2).
1. $c_i=k$ for all $i\ge t+1$, and if $t\ge1$ then $c_t=k-1$.
2. If $t\ge k+1$, then at least one of the following holds:
   * (i) there is a $k$-pattern on some $[p,q]$ with $t-k\le p<q\le t-1$;
   * (ii) there is a $(k-1)$-pattern on some $[p,q]$ with $t-k+1\le p<q\le t+1$.

*Proof.* (1) $B^m(\lambda)=\delta_k$ for $m\ge t$, so $c_{m+1}=k$. Let $t\ge1$ and $\mu=B^{t-1}(\lambda)$, so $\mu\ne\delta_k$, $B(\mu)=\delta_k$, $\ell(\mu)=c_t$. The new part $c_t$ of $B(\mu)$ is a part of $\delta_k$, so $c_t\le k$. If $c_t=k$, the remaining parts $\mu_j-1$ ($\mu_j\ge2$) form $\{k-1,\dots,1\}$, so $\mu$ has the parts $k,k-1,\dots,2$ and, having $c_t=k$ parts in total, exactly one part $1$: $\mu=\delta_k$, a contradiction. Also $c_t\ge c_{t+1}-1=k-1$ by Lemma 4. Hence $c_t=k-1$.

(2) Let $t\ge k+1$, so $t-k\ge1$. Row $t$ of (3.2) has $c_t=k-1$ ones. The $k$ columns $P_{t-k},\dots,P_{t-1}$ cannot all have $e_{t,j}=1$; since $e_{t,t-1}=1$, there is $i\in[t-k,t-2]$ with $e_{t,i}=0$; take the largest such $i$. Then $e_{t,j}=1$ for $j\in[i+1,t-1]$. As $\delta_t=c_t+1-c_{t+1}=0$, Lemma 4 gives $e_{t+1,i+1}=1$, i.e. $c_{i+1}\ge t-i$. From $e_{t,i}=0$, $c_i\le t-i-1$, and by Lemma 4 $c_i\ge c_{i+1}-1\ge t-i-1$. Hence
$$c_i=t-i-1,\qquad c_{i+1}=t-i.\tag{6.1}$$

*Case A: $i\ge t-k+1$.* Then $c_i\le k-2<k-1<k=c_{t+1}$ and $i<t+1$; Lemma 5 with $x=k-1$ gives a $(k-1)$-pattern on $[p,q]$ with $t-k+1\le i\le p<q\le t+1$: (ii) holds.

*Case B: $i=t-k$.* Then $c_{t-k}=k-1$ and $c_{t-k+1}=k$ by (6.1). If some $j\in[t-k+2,t-1]$ has $c_j\le k-2$, Lemma 5 ($x=k-1$, indices $j<t+1$) gives a $(k-1)$-pattern on $[p,q]$ with $t-k+2\le p<q\le t+1$: (ii) holds. If some $j\in[t-k+2,t-1]$ has $c_j\ge k+1$, Lemma 5 ($x=k$, indices $t-k<j$) gives a $k$-pattern on $[p,q]$ with $t-k\le p<q\le j\le t-1$: (i) holds. Otherwise $c_j\in\{k-1,k\}$ for all $j\in[t-k+2,t-1]$, and we derive a contradiction by counting cards. Row $t$ has its $k-1$ ones at the columns $P_{t-k+1},\dots,P_{t-1}$, hence all other entries of row $t$ vanish: $f_{t,j}=0$ for all $j$ and $e_{t,j}=0$ for $j\le t-k$. By Lemma 3 the parts of $B^{t-1}(\lambda)$ are therefore exactly $c_j-(t-1-j)$ for $j=t-k+1,\dots,t-1$. For $j=t-k+1$ this part is $k-(k-2)=2$; for $j=t-k+m$ with $2\le m\le k-1$ it is $c_j-(k-1-m)\le k-(k-1-m)=m+1$. So
$$T_k=|B^{t-1}(\lambda)|\le 2+\sum_{m=2}^{k-1}(m+1)=2+\sum_{u=3}^{k}u=2+(T_k-3)=T_k-1,$$
a contradiction. (For $k=2$ the sum is empty and the bound reads $2=T_2-1$; for $k=1$ case (2) cannot occur since $c_t=k-1=0$ is impossible.) $\square$

**Lemma 7.** Let $\lambda\vdash n$, $k\ge3$, and suppose $(c_p,c_{p+1},\dots,c_{p+k})=(k-2,k-1,\dots,k-1,k)$ for some $p\ge1$ (a $(k-1)$-pattern on $[p,p+k]$). Then $p+k\le n+1$.

*Proof.* For $j\in[p+1,p+k-1]$: $e_{p+k,j}=[k-1\ge p+k-j]=1$. Also $e_{p+k,p}=[k-2\ge k]=0$. Row $p+k$ has $c_{p+k}=k$ ones, so besides these $k-1$ there is exactly one more one, either some $f_{p+k,j}=1$, whence $p+k\le\lambda_j\le n$ and we are done, or some $e_{p+k,j}=1$ with $j\le p-1$. Suppose in the latter case $j\ge2$. Then $e_{p+k,j-1}=0$ (the extra one is unique and $j-1\notin\{p\}\cup[p+1,p+k-1]$). Since $\delta_{p+k-1}=c_{p+k-1}+1-c_{p+k}=0$, Lemma 4 gives $e_{p+k-1,j-1}=0$. Since $k\ge3$, $c_{p+k-2}=k-1$ and $\delta_{p+k-2}=1$; the column $P_p$ dies there ($e_{p+k-2,p}=[k-2\ge k-2]=1$, $e_{p+k-1,p}=[k-2\ge k-1]=0$), so Lemma 4 with $j_0=p\ne j-1$ gives $e_{p+k-2,j-1}=e_{p+k-1,j-1}=0$, i.e. $c_{j-1}<p+k-2-(j-1)$, i.e. $c_{j-1}\le p+k-j-2$. But $e_{p+k,j}=1$ means $c_j\ge p+k-j\ge c_{j-1}+2$, contradicting Lemma 4. Hence $j=1$, so $c_1\ge p+k-1$; as $c_1=\ell(\lambda)\le n$, $p+k\le n+1$. $\square$

**Lemma 8.** If there is an $x$-pattern on $[p,p+2]$, then $p\le x$.

*Proof.* Suppose $p\ge x+1$, so $c_p=x-1\le p-2$. Row $p$ has at most $x-1\le p-2$ ones among the $p-1$ columns $P_1,\dots,P_{p-1}$, so some $e_{p,i}=0$ with $i\le p-1$, and $i\le p-2$ because $e_{p,p-1}=1$; take $i$ largest, so $e_{p,i+1}=1$. Since $\delta_p=\delta_{p+1}=0$, Lemma 4 gives $e_{p+2,i+1}=e_{p+1,i+1}=e_{p,i+1}=1$, i.e. $c_{i+1}\ge p-i+1$; but $e_{p,i}=0$ gives $c_i\le p-i-1$, so $c_{i+1}\ge c_i+2$, contradicting Lemma 4. $\square$

**Lemma 9.** Suppose there is an $x$-pattern on $[p,q]$ with $q\ge p+3$ and $p\ge x+1$. Then there are $x',p',q'$ with an $x'$-pattern on $[p',q']$ and
$$x'\le x,\qquad p'\ge p-x,\qquad 2\le q'-p'\le q-p-1.$$

*Proof.* Since $p\ge x+1$, the $x$ columns $P_{p-x},\dots,P_{p-1}$ exist. Row $p$ has $c_p=x-1$ ones, so some $e_{p,p'}=0$ with $p'\in[p-x,p-1]$, and $p'\le p-2$ because $e_{p,p-1}=1$ (note $x\ge2$). Take $p'$ largest; then $e_{p,j}=1$ for $j\in[p'+1,p-1]$. As $\delta_p=0$, Lemma 4 gives $e_{p+1,j}=1$ for $j\in[p'+1,p-1]$, and $e_{p+1,p}=1$ anyway; so
$$e_{p+1,j}=1\quad\text{for all }j\in[p'+1,p].\tag{9.1}$$
From $e_{p+1,p'+1}=1$: $c_{p'+1}\ge p-p'$; from $e_{p,p'}=0$: $c_{p'}\le p-p'-1$; from Lemma 4: $c_{p'}\ge c_{p'+1}-1$. Hence
$$c_{p'}=p-p'-1,\qquad c_{p'+1}=p-p'.\tag{9.2}$$
Put $y:=p-p'$ ($2\le y\le x$) and $M:=q-p-1\ge2$.

*Claim.* For $1\le m\le M$: if $c_{p'+u}=y$ for all $1\le u\le m-1$, then $e_{p+m,j}=1$ for all $j\in[p'+m,p+m-1]$, and consequently $c_{p'+m}\ge y$.

Induction on $m$. For $m=1$ this is (9.1). Let $2\le m\le M$ and assume $c_{p'+u}=y$ for $u\le m-1$. By the induction hypothesis (whose hypothesis holds a fortiori), $e_{p+m-1,j}=1$ for $j\in[p'+m-1,p+m-2]$. Since $p+m\le q-1$ and $p+m-1\ge p+1$, both $c_{p+m-1}$ and $c_{p+m}$ equal $x$, so $\delta_{p+m-1}=1$: exactly one pile alive at time $p+m-2$ dies. The column $P_{p'+m-1}$ has $c_{p'+m-1}=y$, so it has ones exactly in rows $p'+m,\dots,p'+m-1+y=p+m-1$; thus $e_{p+m-1,p'+m-1}=1$, $e_{p+m,p'+m-1}=0$, and this is the unique death. By Lemma 4 every other one of row $p+m-1$ persists: $e_{p+m,j}=1$ for $j\in[p'+m,p+m-2]$; and $e_{p+m,p+m-1}=1$. Finally $e_{p+m,p'+m}=1$ means $c_{p'+m}\ge p+m-(p'+m)=y$. This proves the claim.

Let $U:=\{m\in[1,M]:c_{p'+m}\ne y\}$. *$U$ is nonempty:* otherwise the claim applies with $m=M$ and gives $e_{q-1,p'+M}=1$ (indeed $p+M-1=q-2\ge p'+M$); since $c_q=x+1=c_{q-1}+1$, $\delta_{q-1}=0$ and Lemma 4 gives $e_{q,p'+M}=1$, i.e. $c_{p'+M}\ge q-p'-M=y+1\ne y$, a contradiction. Let $m^*=\min U$; by (9.2), $m^*\ge2$. The claim applies to $m^*$ and gives $c_{p'+m^*}\ge y$, hence $c_{p'+m^*}\ge y+1$, while Lemma 4 gives $c_{p'+m^*}\le c_{p'+m^*-1}+1=y+1$. Therefore
$$(c_{p'},c_{p'+1},\dots,c_{p'+m^*-1},c_{p'+m^*})=(y-1,y,\dots,y,y+1),$$
a $y$-pattern on $[p',p'+m^*]$ with $x'=y\le x$, $p'\ge p-x$, and $2\le m^*\le M=q-p-1$. $\square$

**Lemma 10 (iteration).** If there is an $x$-pattern on $[p,q]$, then $p\le x\,(q-p-1)$.

*Proof.* Put $(x_0,p_0,q_0)=(x,p,q)$. As long as $q_j-p_j\ge3$ and $p_j\ge x_j+1$, Lemma 9 yields an $x_{j+1}$-pattern on $[p_{j+1},q_{j+1}]$ with $x_{j+1}\le x_j\le x$, $p_{j+1}\ge p_j-x_j\ge p_j-x$ and $2\le q_{j+1}-p_{j+1}\le q_j-p_j-1$. The lengths $q_j-p_j$ are integers $\ge2$ that strictly decrease, so the procedure stops after $J\le (q-p)-2$ applications, at a pattern $(x_J,p_J,q_J)$ for which either $p_J\le x_J\le x$, or $q_J-p_J=2$ and then $p_J\le x_J\le x$ by Lemma 8. Hence $p=p_0\le p_J+Jx\le x+(q-p-2)x=x(q-p-1)$. $\square$

### Theorem B (upper bound)
**Theorem B.** Let $n=T_k$. For every $\lambda\vdash n$, $d_B(\lambda)\le k^2-k$.

*Proof.* For $k=1$ the only partition is $\delta_1$ and $d_B=0$. For $k=2$, $n=3$: $d_B((2,1))=0$, $d_B((3))=1$ ($B(3)=(2,1)$), $d_B((1,1,1))=2$ ($(1,1,1)\to(3)\to(2,1)$); all $\le2=k^2-k$. Let $k\ge3$, $\lambda\vdash T_k$, $t=d_B(\lambda)$. If $t\le k$ then $t\le k\le k^2-k$. Assume $t\ge k+1$; by Lemma 6(2), (i) or (ii) holds.

*Case 1: (ii) holds with $q-p=k$.* From $t-k+1\le p$ and $q\le t+1$ we get $p=t-k+1$, $q=t+1$, and the $(k-1)$-pattern on $[p,p+k]$ reads $(c_p,\dots,c_{p+k})=(k-2,k-1,\dots,k-1,k)$. Lemma 7 gives $p+k\le n+1$, so
$$t=p+k-1\le n=\tfrac{k(k+1)}2\le k^2-k,$$
the last inequality because $k+1\le 2(k-1)$ for $k\ge3$.

*Case 2: otherwise.* Then there is an $x$-pattern on $[p,q]$ with $x\in\{k,k-1\}$ and $q-p\le k-1$: in (i), $q-p\le (t-1)-(t-k)=k-1$; in (ii) with $q-p\ne k$, $q-p\le (t+1)-(t-k+1)-1=k-1$. By Lemma 10, $p\le x(q-p-1)\le k(k-2)=k^2-2k$. In (i), $t\le p+k\le k^2-k$. In (ii), $t\le p+k-1\le k^2-k-1$. $\square$

### Conclusion
By Theorem A, $D_B(T_k)\ge k^2-k$ with the explicit extremal $\gamma_k$; by Theorem B, $D_B(T_k)\le k^2-k$. Hence $D_B(T_k)=k^2-k$ for every $k\ge1$. $\blacksquare$

---

## Computational sanity checks (exact integer arithmetic; not part of the proof)
* `calcola_DB_triangolari.py`: exhaustive computation of $d_B$ over all partitions of $T_k$, $k\le 9$: $D_B(T_k)=k^2-k$ and $\gamma_k$ is extremal (0.5 s).
* `verifica_lemmi_sequenza.py`: exhaustive check of Lemmas 4, 7, 8, 9, 10 exactly as stated above (every $x$-pattern with $p<60$, $q-p<40$ in the first 400 terms) for all partitions of every $n\le24$, and of Lemma 6 and Theorem B for $k=3,\dots,7$ (8.6 s). This guards against transcription errors in the statements; the proofs above are self-contained.
