Problem 4 — Part 2 — submission draft

Declared status: SOLVED (approved). Complete proof written by the team; automatic Referee READY_FOR_HUMAN
(judge A mathematics PASS, judge B evidence PASS); human approval recorded in runs/p4_c2/approval.json.

1. Result and scope

Four disjoint classes: the statement of the part is proved in full, in the generality required (see the proof for the
exact hypotheses). No computer calculation is needed.

2. Proof

Cell 2: four pairwise disjoint classes have a pair of moduli with $\gcd\ge4$

Target. If $a_i\ (\mathrm{mod}\ m_i)$, $i=1,2,3,4$, are pairwise disjoint congruence classes ($m_i\ge1$), then $\gcd(m_i,m_j)\ge4$ for some $i<j$.

Lemma 0

Let $g=\gcd(m,m')$. If $g\mid a-a'$ then the classes $a\ (\mathrm{mod}\ m)$ and $a'\ (\mathrm{mod}\ m')$ meet; equivalently, disjoint classes satisfy $g\nmid a-a'$.
Proof. Write $m=g\mu$, $m'=g\mu'$ with $\gcd(\mu,\mu')=1$ and $a-a'=g\delta$. The element $a+g\mu t$ of the first class lies in the second iff $g\mu'\mid g(\delta+\mu t)$ iff $\mu'\mid\delta+\mu t$, which has the solution $t\equiv-\delta\mu^{-1}\pmod{\mu'}$ since $\mu$ is invertible modulo $\mu'$. $\square$

Proof of the cell

Write $g_{ij}=\gcd(m_i,m_j)$ for $i\ne j$. Suppose, for a contradiction, that $g_{ij}\le3$ for all pairs. By Lemma 0, $g_{ij}=1$ is impossible for disjoint classes ($1\mid a_i-a_j$), hence
$$g_{ij}\in\{2,3\}\quad\text{for all } i\ne j.\qquad(1)$$
Two consequences of (1) and Lemma 0, for $i\ne j$:
- (E) if $2\mid m_i$ and $2\mid m_j$, then $2\mid g_{ij}$, so by (1) $g_{ij}=2$, and disjointness gives $2\nmid a_i-a_j$, i.e. $a_i\not\equiv a_j\pmod2$;
- (T) if $3\mid m_i$ and $3\mid m_j$, then $3\mid g_{ij}$, so $g_{ij}=3$, and disjointness gives $a_i\not\equiv a_j\pmod3$.

Let $E=\{i: 2\mid m_i\}$ and $T=\{i:3\mid m_i\}$.
Claim 1: $|E|\le2$ and $|T|\le3$. By (E) the residues $a_i\bmod2$, $i\in E$, are pairwise distinct, and there are only $2$ residues; by (T) the residues $a_i\bmod3$, $i\in T$, are pairwise distinct, and there are only $3$ residues.
Claim 2: $E\cup T=\{1,2,3,4\}$. Given $i$, pick any $j\ne i$; by (1) $g_{ij}\in\{2,3\}$ and $g_{ij}\mid m_i$, so $2\mid m_i$ or $3\mid m_i$.
Claim 3: $|T|\ge2$. By Claims 1–2, $|T|\ge4-|E|\ge2$.

We now rule out the remaining sizes of $T$.
- $|T|=4$. Then all four residues $a_i\bmod 3$ are pairwise distinct by (T), impossible with three residues.
- $|T|=3$. Say $T=\{1,2,3\}$ after relabelling, so $3\nmid m_4$. For $j\in T$: $g_{4j}\in\{2,3\}$ and $3\nmid g_{4j}$ (because $g_{4j}\mid m_4$), hence $g_{4j}=2$, so $2\mid m_j$. Thus $2\mid m_1,m_2,m_3$; also $2\mid m_4$ by Claim 2 (as $3\nmid m_4$). So $|E|=4$, contradicting Claim 1.
- $|T|=2$. By Claim 2 the two indices outside $T$ lie in $E$, so $|E|\ge2$, hence $|E|=2$ by Claim 1 and $E$ is exactly the complement of $T$; in particular $E\cap T=\emptyset$. Take $i\in E$ and $j\in T$. Then $g_{ij}\in\{2,3\}$ by (1). But $j\notin E$ means $2\nmid m_j$, so $2\nmid g_{ij}$ and $g_{ij}\ne2$; and $i\notin T$ means $3\nmid m_i$, so $3\nmid g_{ij}$ and $g_{ij}\ne3$. Contradiction.

Since $|T|\ge2$ is forced by Claim 3, all cases lead to a contradiction. Hence some pair satisfies $g_{ij}\ge4$. $\blacksquare$

Remark (not needed). The case $|T|=3$ shows more generally the mechanism used: an index whose modulus misses a prime $p$ forces all its gcds to avoid $p$.

3. Verification: instructions, dependencies, timings

Proof by hand, no dependencies. Mechanical verification not needed; the automatic Referee (two independent judges,
runs/p4_c2/attempts/packet_001.json) found no unjustified steps.

4. Sources and contribution

- arXiv:2607.24655 Fornal, Sun, On the problem of large gcd for disjoint residue classes (context only: asymptotic result, not used)
- Position with respect to the state of the art: Fornal-Sun [2607.24655] use a gcd-coloured complete graph in the asymptotic regime; the same graph viewpoint underlies our finite argument, but the proof here is elementary and self-contained.
- Contribution: the proof written here is the team's own, in full.

5. Limits and unresolved parts

None: the part is proved. Declared gaps: none.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family direct_proof, subgoal: Prove the case k=4 by the 'prime cliques' argument: indices whose moduli share a prime p form a set on which residues mod p are pairwise distinct, so |E|<=2 for p=2 and |T|<=3 for p=3; a case analysis on |T| closes.; declared CELL_SOLVED_CANDIDATE.
  - Why this approach: With all gcds in {2,3}, each modulus is divisible by 2 or 3, and the indices divisible by a common prime p must carry pairwise distinct residues mod p; counting these residues bounds the sizes of the two 'prime cliques' and the remaining case analysis on their sizes is short and exhaustive.
  - Position w.r.t. the literature: Fornal-Sun [2607.24655] use a gcd-coloured complete graph in the asymptotic regime; the same graph viewpoint underlies our finite argument, but the proof here is elementary and self-contained.
  - Referee: UNKNOWN_STATUS / READY_FOR_HUMAN; next: Human reviews the exact target, proof and evidence, then approves explicit claims
- Human approval: Thomas Tumini (human) at 2026-09-26T14:53:05 (READY_FOR_HUMAN → ACCEPT).

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015), found by query disjoint covering systems; abstract read, full text not relied upon.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026), found by query disjoint residue classes; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c2.tex and in the repository.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c2.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
