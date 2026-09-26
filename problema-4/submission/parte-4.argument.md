# Problem 4 — Part 4 — PARTIAL submission draft

**Declared status: PARTIAL.** No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is claimed as proved beyond what is written.

## 1. Result and scope
**Official request.**
## Parte 4 (C4) — Every $k$ up to 12

**Punteggio:** 5 points · **Valutazione:** Judged

A longer range, and a precise account of your method at the sizes just beyond it. Prove the statement for every
$k \le 12$. Then, for each $k$ from $9$ to $16$ in turn, report exactly what your method leaves undecided at that
$k$: if nothing, say so and prove it; if something, exhibit it in full. If that disagrees with any source you
consulted, say which of the two is right and why. An answer that reports agreement with a source it did not test
will be marked wrong.

**What we deliver.** As in part 3, extended to $k\le12$ ($L_{12}=27720$, 96 divisors); not executed.

## 2. Proof
Same reduction and same search scheme; the report on the cases $9\le k\le16$ requires listing the survivors of the pruning without deciding them by unproved rules.

## 3. Verification: instructions, dependencies, timings
Available code (Python 3, standard library; each script runs in under a minute):
- No code yet.

## 4. Sources and contribution
arXiv literature (deterministic search `tools/cerca_letteratura.sh`, abstracts read, not used as proof):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); abstract only read.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); abstract only read.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); abstract only read.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); abstract only read.
As in part 3.

## 5. Limits and unresolved parts
Everything except the reduction.


## 6. How this result was obtained (multi-agent trace)
Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

## 7. arXiv literature consulted
- arXiv:2603.26043v1 — *Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus* (Yu Hashimoto, 2026), found by query `disjoint covering systems`; abstract read, full text not relied upon.
- arXiv:1511.04293v1 — *Searching for Disjoint Covering Systems with Precisely One Repeated Modulus* (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015), found by query `disjoint covering systems`; abstract read, full text not relied upon.
- arXiv:2607.24655v1 — *On the problem of large gcd for disjoint residue classes* (Jan Fornal, Yu-Chen Sun, 2026), found by query `disjoint residue classes`; abstract read, full text not relied upon.
- arXiv:2608.15873v1 — *Two Questions on $G$-harmonic Tuples* (Murali Menon, 2026), found by query `disjoint residue classes`; abstract read, full text not relied upon.

## 8. Code
See the certificates listed in section 3.

---
Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p4_c4.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
