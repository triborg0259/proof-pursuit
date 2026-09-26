# Problem 4, cell 5 — the two isolated sizes: neither 24 nor 30 is the least size at which the statement can fail

Notation. For $k\ge2$ let $S(k)$ be the statement "every family of $k$ pairwise disjoint classes has a pair $i<j$ with $\gcd(m_i,m_j)\ge k$". A *counterexample of size $k$* is a pairwise disjoint family of $k$ classes with $g_{ij}:=\gcd(m_i,m_j)\le k-1$ for all $i<j$; $S(k)$ fails iff a counterexample of size $k$ exists. $L_k:=\operatorname{lcm}(1,\dots,k-1)$. We use only the definitions and the criterion $(*)$: two classes meet iff $\gcd(m_i,m_j)\mid a_i-a_j$.

**Theorem.** Let $k\in\{24,30\}$ and assume $S(s)$ holds for every $2\le s<k$. Then $S(k)$ holds. Consequently neither $24$ nor $30$ is the least size at which the statement fails.

(The proof is given in full below; see the JSON `proof_attempt` field of the attempt.)
