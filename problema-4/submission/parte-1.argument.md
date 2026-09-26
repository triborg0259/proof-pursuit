Problem 4 — Part 1 — submission draft

Declared status: SOLVED (approved). Complete proof written by the team; automatic Referee READY_FOR_HUMAN
(judge A mathematics PASS, judge B evidence PASS); human approval recorded in runs/p4_c1/approval.json.

1. Result and scope

Three disjoint classes: the statement of the part is proved in full, in the required generality (see the proof for the
exact hypotheses). No computer calculation is needed.

2. Proof

Cell 1: three pairwise disjoint classes have a pair of moduli with $\gcd\ge3$

Target. If $a_1\ (\mathrm{mod}\ m_1)$, $a_2\ (\mathrm{mod}\ m_2)$, $a_3\ (\mathrm{mod}\ m_3)$ are pairwise disjoint congruence classes ($m_i\ge1$), then $\gcd(m_i,m_j)\ge3$ for some $i<j$.

Lemma 0 (the direction of $(*)$ that we use)

Let $g=\gcd(m,m')$. If $g\mid a-a'$ then the classes $a\ (\mathrm{mod}\ m)$ and $a'\ (\mathrm{mod}\ m')$ have a common element. Equivalently: if the two classes are disjoint then $g\nmid a-a'$.
Proof. Write $m=g\mu$, $m'=g\mu'$ with $\gcd(\mu,\mu')=1$, and $a-a'=g\delta$ with $\delta\in\mathbb Z$. An element of the first class has the form $a+mt=a+g\mu t$, $t\in\mathbb Z$; it lies in the second class iff $m'\mid a+g\mu t-a'$, i.e. $g\mu'\mid g(\delta+\mu t)$, i.e. $\mu'\mid\delta+\mu t$. Since $\gcd(\mu,\mu')=1$, $\mu$ is invertible modulo $\mu'$, so $t\equiv-\delta\mu^{-1}\pmod{\mu'}$ solves it. $\square$
(This is the statement $(*)$ quoted in the problem; we include the short proof so that the argument is self-contained.)

Proof of the cell

Let the three classes be pairwise disjoint and suppose, for a contradiction, that $\gcd(m_i,m_j)\le2$ for all three pairs.
1. Every pairwise gcd equals $2$. If $\gcd(m_i,m_j)=1$ then $1\mid a_i-a_j$, so by Lemma 0 the classes $i$ and $j$ meet, contradicting disjointness. Hence $\gcd(m_i,m_j)=2$ for all $i<j$.
2. The residues are pairwise of different parity. For $i<j$, disjointness and Lemma 0 give $\gcd(m_i,m_j)=2\nmid a_i-a_j$, i.e. $a_i\not\equiv a_j\pmod 2$.
3. Contradiction. $a_1,a_2,a_3$ would be three integers with pairwise different residues modulo $2$; but there are only two residues modulo $2$, so two of them coincide (pigeonhole). 

Hence the assumption fails: some pair satisfies $\gcd(m_i,m_j)\ge3$. $\blacksquare$

Remark. Step 1 is the first "trivial bound" of the problem statement; it is re-derived here only because the argument needs the exact value $2$ of every gcd, not merely $\ge2$.

3. Verification: instructions, dependencies, timings

Hand-written proof, no dependencies. Mechanical verification not needed; the automatic Referee (two independent judges,
runs/p4_c1/attempts/packet_001.json) found no unjustified steps.

4. Sources and contribution

- arXiv:2607.24655 Fornal, Sun, On the problem of large gcd for disjoint residue classes (context only: asymptotic result, not used)
- Position with respect to the state of the art: Fornal-Sun [2607.24655] prove an asymptotic lower bound for the largest gcd; the small cases k=3,4 are elementary and are not treated there. Our proof is independent.
- Contribution: the proof written here is the team's, in full.

5. Limits and unresolved parts

None: the part is proved. Declared gaps: none.

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- attempt_001 — Researcher: family direct_proof, subgoal: Prove the case k=3 by parity: all gcds would be 2, forcing pairwise distinct parities of three residues.; declared CELL_SOLVED_CANDIDATE.
  - Why this approach: For three classes the only escape from the conclusion is that every gcd equals 2; the disjointness criterion () then forces three pairwise different parities, which is impossible. The criterion () is re-proved in one paragraph so that the argument is self-contained.
  - Position w.r.t. the literature: Fornal-Sun [2607.24655] prove an asymptotic lower bound for the largest gcd; the small cases k=3,4 are elementary and are not treated there. Our proof is independent.
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

The complete code, with the orchestrator's trusted re-runs, is in the write-up: https://triborg0259.github.io/proof-pursuit/cells/p4_c1.html (rendered), https://www.overleaf.com/docs?snip_uri=https://raw.githubusercontent.com/triborg0259/proof-pursuit/main/report/cells/p4_c1.tex (open in Overleaf), source in the repository https://github.com/triborg0259/proof-pursuit/blob/main/.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c1.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
