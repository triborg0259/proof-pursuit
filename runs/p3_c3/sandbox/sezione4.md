## §4. The partitions of $T_k-1$ attaining the maximum

Throughout this section $n=T_k-1$ (so $r=k-1$), $D:=k^2-2k-1$ and $\ell:=k^2-3k-1$. Define
$$\nu_k:=(k-1,\,k-1,\,k-1,\,k-3,\,k-4,\,\dots,\,3,\,2)$$
(three parts equal to $k-1$ followed by one part of each size $k-3,k-4,\dots,2$; for $k=4$ this is $(3,3,3)$, for $k=5$ it is $(4,4,4,2)$). It has $k-1$ parts and size $3(k-1)+(T_{k-3}-1)=3k-4+T_k-(3k-3)=T_k-1$.

**Theorem 4.1.** Let $k\ge4$ and $\lambda\vdash T_k-1$. Then $d_B(\lambda)=k^2-2k-1$ if and only if $B^{k^2-3k-1}(\lambda)=\nu_k$. Hence the set of partitions of $T_k-1$ attaining $D_B(T_k-1)$ is exactly the preimage $B^{-(k^2-3k-1)}(\nu_k)$; it contains $\lambda^*_k$ of §3.

The proof uses three lemmas. For a partition $\mu$ write $c_u(\mu):=s(B^{u-1}(\mu))$ ($u\ge1$) for its part-count sequence (the sequence $(c_u)$ of Lemma 0.3 started at $\mu$).

**Lemma 4.2 (the future part counts determine the partition).** For every partition $\mu$ and every $i\ge0$,
$$\mu'_{i+1}=c_{i+1}(\mu)-\#\{u\in[1,i]:\ c_u(\mu)\ge i-u+1\},$$
where $\mu'_{i+1}=\#\{j:\mu_j\ge i+1\}$ is the $(i+1)$-st part of the conjugate. Consequently two partitions with the same sequence $(c_u)_{u\ge1}$ are equal.
*Proof.* By Lemma 0.3, $c_{i+1}(\mu)$ is the number of piles alive at time $i$. These are: the initial piles (the parts of $\mu$) of size $\ge i+1$, whose number is $\mu'_{i+1}$; and the piles $u\in[1,i]$ (created at time $u$ with size $c_u$), pile $u$ being alive at time $i$ iff $c_u\ge i-u+1$. This gives the formula. A partition is determined by its conjugate. $\square$

**Lemma 4.3 (the orbit of $\nu_k$).** Let $k\ge4$ and $c_u:=c_u(\nu_k)$. Then
$$c_1=k-1;\quad c_u=k\ (2\le u\le k-2);\quad c_{k-1}=k+1;\quad c_k=k-1;\quad c_{k+1}=k-1;\quad c_{k+1+i}=k\ (1\le i\le k-1);\quad c_{u+k}=c_u\ (u\ge k+1).$$
Moreover $B^k(\nu_k)=(k,k-1,\dots,2)$ is staircase-like, $B^{k-1}(\nu_k)=(k+1,k-1,k-2,\dots,3,1)$ is not, and $d_B(\nu_k)=k$.
*Proof.* The initial piles are three piles of size $k-1$ and one pile of each size $m\in[2,k-3]$ (none if $k=4$). We count the piles alive at time $\tau$ (Lemma 0.3), using $c_{\tau+1}=\#\{\text{alive at }\tau\}$ and "pile $u$ alive at $\tau$ iff $c_u\ge\tau-u+1$".
*$\tau=0$:* all $3+(k-4)=k-1$ initial piles: $c_1=k-1$.
*$1\le\tau\le k-2$* (induction on $\tau$, assuming $c_1,\dots,c_\tau\ge k-1$, which holds by the values already established): initial piles of size $\ge\tau+1$: the three of size $k-1$ (as $\tau+1\le k-1$) and the $\max(0,k-3-\tau)$ piles of size $m\in[\tau+1,k-3]$; new piles $u\in[1,\tau]$: all alive, since $c_u\ge k-1\ge\tau\ge\tau-u+1$. So $c_{\tau+1}=3+\max(0,k-3-\tau)+\tau$, i.e. $c_{\tau+1}=k$ for $1\le\tau\le k-3$ and $c_{k-1}=k+1$ ($\tau=k-2$).
*$\tau=k-1$:* no initial pile has size $\ge k$. Pile $u\in[1,k-1]$ is alive iff $c_u\ge k-u$: $u=1$: $k-1\ge k-1$; $2\le u\le k-2$: $k\ge k-u$; $u=k-1$: $k+1\ge1$. So $c_k=k-1$.
*$\tau=k$:* pile $u\in[1,k]$ alive iff $c_u\ge k+1-u$: $u=1$: $k-1\ge k$ fails; $2\le u\le k-2$: $k\ge k+1-u$ holds; $u=k-1$: $k+1\ge2$; $u=k$: $k-1\ge1$. So $c_{k+1}=k-1$, and the piles alive at time $k$ are $u=2,\dots,k$ with sizes $c_u-(k-u)$: $u\in[2,k-2]\mapsto u$, $u=k-1\mapsto k$, $u=k\mapsto k-1$. Hence $B^k(\nu_k)=(k,k-1,k-2,\dots,2)$. Its cell set is $\Delta_{k-1}\cup(D_k\setminus\{(k,1)\})$ (row $i\le k-1$ has $k+1-i=(k-i)+1$ cells, the extra one being $(i,k+1-i)\in D_k$; row $k$ is empty), so it is staircase-like with occupancy $\varepsilon=(1,\dots,1,0)$, and Lemma 1.1 gives $c_{k+1+i}=k-1+\varepsilon_{k-i\bmod k}$: $k-1$ for $i=0$, $k$ for $1\le i\le k-1$, and $k$-periodicity for $u\ge k+1$.
*$\tau=k-1$, the partition:* the alive piles are $u=1,\dots,k-1$ with sizes $c_u-(k-1-u)$: $u=1\mapsto1$, $u\in[2,k-2]\mapsto u+1$, $u=k-1\mapsto k+1$. So $B^{k-1}(\nu_k)=(k+1,k-1,\dots,3,1)$, which contains the cell $(1,k+1)\in D_{k+1}$, hence is not staircase-like, hence (Theorem 1.2) not cyclic.
Finally, cyclic partitions are forward-closed (if $B^i(\mu)=\mu$ then $B^i(B(\mu))=B(\mu)$), so if some $B^j(\nu_k)$ with $j\le k-1$ were cyclic then $B^{k-1}(\nu_k)$ would be; it is not. $B^k(\nu_k)$ is cyclic (Lemma 1.1). So $d_B(\nu_k)=k$. $\square$

**Lemma 4.4.** If $d_B(B^j(\mu))=m\ge1$ then $d_B(\mu)=j+m$.
*Proof.* $B^{j+m}(\mu)$ is cyclic. If $B^i(\mu)$ were cyclic for some $i<j+m$, forward-closure would make $B^{j+m-1}(\mu)=B^{m-1}(B^j\mu)$ cyclic, contradicting $d_B(B^j\mu)=m$. $\square$

**Proof of Theorem 4.1.**
($\Leftarrow$) If $B^\ell(\lambda)=\nu_k$ then, by Lemmas 4.3 and 4.4, $d_B(\lambda)=\ell+k=k^2-2k-1$.

($\Rightarrow$), $k\ge5$. Let $d_B(\lambda)=D$ and let $t$ be as in §2 ("Choice of $t$"). Since $B^{t-1}(\lambda)$ is cyclic, $t-1\ge d_B(\lambda)=D$, so $t\ge k^2-2k\ge k+1$, and Lemma 2.1 applies. We go through the cases of the proof of Theorem 2.6.
*Case A* gives $d_B(\lambda)\le n-1=T_k-2<D$ (as $k^2-5k+2>0$ for $k\ge5$): impossible.
*Case C* is impossible.
*Case B*, pattern (ii): there $p\ge t-k+1$, so $t\le p+k-1\le(q-p-1)k+k-1\le(k-3)k+k-1=D<t$ (Lemma 2.5): impossible.
So pattern (i) holds: $(c_p,\dots,c_q)=(k-1,k,\dots,k,k+1)$ with $t-k\le p<q\le t-1$, $2\le q-p\le k-2$, and Lemma 2.5 (with $x=k$) gives
$$k^2-2k\le t\le p+k\le(q-p-1)k+k\le(k-2)k=k^2-2k .$$
Hence all are equalities: $t=k^2-2k$, $p=t-k$, $q-p=k-2$, $q=t-2$; that is,
$$c_{t-k}=k-1,\qquad c_{t-k+i}=k\ (1\le i\le k-3),\qquad c_{t-2}=k+1 .\tag{4.1}$$
*The value $c_{t-1}$.* Lemma 0.4 with $i=t-k$: $c_{t-k+1}+\dots+c_t\le k(k-1)+(k-1)=k^2-1$. By (4.1) and $c_t=k-1$ the left side is $(k-3)k+(k+1)+c_{t-1}+(k-1)=k^2-k+c_{t-1}$, so $c_{t-1}\le k-1$. Conversely the following $k-1$ piles are alive at time $t-2$: pile $t-k$ (size $k-1\ge(t-2)-(t-k)+1=k-1$), the piles $t-k+i$, $1\le i\le k-3$ (size $k\ge(t-2)-(t-k+i)+1=k-1-i$), and pile $t-2$ (size $k+1\ge1$). So $c_{t-1}\ge k-1$, and $c_{t-1}=k-1$.
*The values $c_u$, $u\ge t$.* $B^{t-1}(\lambda)$ is staircase-like with $(c_t,c_{t+1})=(k-1,k)$; by Lemma 1.1 (with $r=k-1$) $c_u\in\{k-1,k\}$ for $u\ge t$, $c_{u+k}=c_u$, and $c_t+\dots+c_{t+k-1}=k(k-1)+(k-1)=k^2-1$. Among $k$ terms $\le k$ summing to $k^2-1$ exactly one equals $k-1$, and it is $c_t$; so $c_{t+i}=k$ for $1\le i\le k-1$.
*Conclusion.* Put $\mu:=B^{t-k-1}(\lambda)=B^{\ell}(\lambda)$ (note $t-k-1=k^2-3k-1=\ell$). Then $c_u(\mu)=s(B^{u-1+\ell}(\lambda))=c_{u+\ell}(\lambda)=c_{u+t-k-1}(\lambda)$, and the values just established read: $c_1(\mu)=k-1$, $c_u(\mu)=k$ for $2\le u\le k-2$, $c_{k-1}(\mu)=k+1$, $c_k(\mu)=k-1$, $c_{k+1}(\mu)=k-1$, $c_{k+1+i}(\mu)=k$ for $1\le i\le k-1$, and $k$-periodicity from index $k+1$ on. This is exactly the sequence of $\nu_k$ (Lemma 4.3). By Lemma 4.2, $\mu=\nu_k$.

($\Rightarrow$), $k=4$: exhaustive computation (script `verifica_estremali.py`, line $k=4$; exact integer arithmetic over all $30$ partitions of $9$): the only $\lambda\vdash9$ with $d_B(\lambda)=7$ is $(3,2,2,1,1)$, and $B^3((3,2,2,1,1))=(3,3,3)=\nu_4$ (indeed $(3,2,2,1,1)\mapsto(5,2,1,1)\mapsto(4,4,1)\mapsto(3,3,3)$).

*$\lambda^*_k$ is extremal, directly.* In the Claim of §3, $j:=k^2-3k-1\le k^2-2k-2$, $j\equiv-1\pmod k$ and $j=(k+1)(k-4)+3\equiv3\pmod{k+1}$; so $X_j$ has the two holes of $D_k$ at rows $k$ and $1$ and the extra cell at $(3,k-1)$: rows $1,2,3$ have $k-1$ cells each, row $i\in[4,k-1]$ has $k+1-i$, row $k$ is empty. Thus $B^{\ell}(\lambda^*_k)=\nu_k$, consistent with §3. $\square$

**Remarks.** (1) The extremal set is large: its cardinalities for $k=4,\dots,10$ are $1,6,34,175,831,3911,18163$ (exact computation), so a description as an explicit list is not to be expected; Theorem 4.1 determines it as the finite backward tree $B^{-\ell}(\nu_k)$, and $\lambda^*_k$ is an explicit member. (2) The proof shows more: every extremal orbit has $t=k^2-2k$ and passes through $\nu_k$ at time $\ell$, through $B^{k-1}(\nu_k)=(k+1,k-1,\dots,3,1)$ at time $k^2-2k-2$, and enters the cycle at $(k,k-1,\dots,2)$ at time $k^2-2k-1$. (3) Sanity check (not part of the proof): `verifica_estremali.py` confirms $\{\lambda:d_B(\lambda)=k^2-2k-1\}=\{\lambda:B^{\ell}(\lambda)=\nu_k\}$, $d_B(\nu_k)=k$ and $\lambda^*_k$ extremal over all partitions of $T_k-1$ for $4\le k\le10$ ($386155$ partitions at $k=10$; $15$ s in total).
