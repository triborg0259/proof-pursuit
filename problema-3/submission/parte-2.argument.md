# Problem 3 — Part 2 — PARTIAL submission draft

**Declared status: PARTIAL.** No complete solution: below is what has been established, the formalization,
the position with respect to the literature, and what remains open. Nothing is claimed as proven beyond what is written.

## 1. Result and scope
**Official request.**
## Parte 2 (C2) — $D_B$ at triangular $n$

**Punteggio:** 2 points · **Valutazione:** Judged

Next, how long the process can take to reach a cycle, starting with the triangular numbers.
Determine $D_B(T_k)$ for every $k$, with proof of both bounds.

**What we deliver.** Expected value $D_B(T_k)=k^2-k$ (cited: Igusa 1985, Etienne 1991); construction and upper bound to be reproduced in full.

## 2. Proof
Lower bound: exhibit a partition of $T_k$ with $d_B=k^2-k$ as a function of $k$ (candidate: the single-part partition $(T_k)$ or $(k-1,\dots)$, to be confirmed by exact computation for $k\le9$). Upper bound: a potential that decreases by at least 1 every $k$ moves after an initial phase. Not completed.

## 3. Verification: instructions, dependencies, timings
Available code (Python 3, standard library; each script runs in under a minute):
- No code yet.

## 4. Sources and contribution
arXiv literature (deterministic search `tools/cerca_letteratura.sh`, abstracts read, not used as proof):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); abstract only read.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); abstract only read.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); abstract only read.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); abstract only read.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); abstract only read.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); abstract only read.
Igusa (1985), Etienne (1991): $D_B(T_k)=k(k-1)$; survey [1503.00885], [2607.17194].

## 5. Limits and unresolved parts
Complete rewrite of both directions.


## 6. How this result was obtained (multi-agent trace)
Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- **attempt_001** — Researcher: family `direct_proof`, subgoal: Establish the value D_B(T_k) = k^2 - k: prove the lower bound D_B(T_k) ≥ k^2 - k with an explicit extremal family and an exact cell-motion lemma for B; identify the general upper bound as the remaining blocker.; declared `LEMMA_CANDIDATE`.
  - Why this approach: First iteration, no blocker stated. The cell asks for the exact value with both bounds; the literature (read: Hopkins 2012 survey) fixes the answer k^2-k and Igusa's extremal γ_k, but no accessible source contains a written proof (Igusa 1985, Etienne 1991, Griggs–Ho 1998 are paywalled; the surveys and theses I read only cite them). I therefore built the proof from scratch. The lower bound and an exact structural lemma are complete; the general upper bound is not, and I say so.
  - Position w.r.t. the literature: The listed arXiv abstracts (math/0401385, 1703.07102: random variants; 1101.1546: Toom's convergence proof; 2208.14496: orbit growth; 1503.00885 and 2607.17194: surveys) do not prove the bound. I fetched and read (pdftotext) Drensky 1503.00885, Meštrović 2607.17194, Hopkins "30 years of Bulgarian solitaire" (College Math. J. 43 (2012) 135–140), Hopkins–Jones (EJC 13 (2006) R80), N. Pham's honors thesis and M. Jonsson's PhD thesis (DiVA 1082060). All state, CITED: Knuth conjectured and Igusa (Math. Mag. 58 (1985) 259–271) and Etienne (JCTA 58 (1991) 181–197) proved that for n=T_k the maximal number of moves is k(k−1), attained by γ_k=(k−1,k−1,k−2,…,2,1,1) (Hopkins 2012, p. 137: "Igusa [15] shows that the partition γ_k … is at distance k(k−1) from τ_k and that this distance is maximal"). None of the read sources reproduces the proof. My approach follows the classical "cards on diagonals" idea mentioned by Hopkins (p. 137) but makes it exact (Lemma 1) and uses it to prove the lower bound in full; the upper bound argument of Igusa/Etienne is not reproduced.
  - Referee: `(nessun verdetto)` / `None`

## 6b. Tokens used by the agents
- Token counts not recorded for this run (older harness version; only cost and turns were logged).

## 7. arXiv literature consulted
- arXiv:math/0401385v2 — *Random Bulgarian solitaire* (Serguei Popov, 2004), found by query `Bulgarian solitaire`; abstract read, full text not relied upon.
- arXiv:1503.00885v1 — *The Bulgarian solitaire and the mathematics around it* (Vesselin Drensky, 2015), found by query `Bulgarian solitaire`; abstract read, full text not relied upon.
- arXiv:2607.17194v1 — *A short survey the game Bulgarian solitaire and related games* (Romeo Meštrović, 2026), found by query `Bulgarian solitaire`; abstract read, full text not relied upon.
- arXiv:1101.1546v3 — *Revisiting Toom's proof of Bulgarian Solitaire* (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011), found by query `Bulgarian solitaire`; abstract read, full text not relied upon.
- arXiv:1703.07102v1 — *An exponential limit shape of random $q$-proportion Bulgarian solitaire* (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017), found by query `Bulgarian solitaire`; abstract read, full text not relied upon.
- arXiv:2208.14496v1 — *Limiting behavior in growth of Bulgarian Solitaire orbits* (Nhung Pham, 2022), found by query `Bulgarian solitaire`; abstract read, full text not relied upon.

## 8. Code
**attempt_001 / code_1** (python, rigor `exact`): Exhaustive exact computation of D_B(T_k) and of all extremal partitions for k ≤ 9 (all partitions of T_k, orbit followed to δ_k). Finite set covered: every partition of T_k for k=1..9 (up to 89134 partitions). Wall-clock 0.48 s. Confirms D_B(T_k)=k^2−k for k≤9; does not prove the general upper bound.

```python
"""Calcolo esatto di D_B(T_k) per k piccoli (esplorazione, aritmetica intera esatta).

Enumera tutte le partizioni di n = T_k, applica lo shift B fino a raggiungere
delta_k (unico punto fisso per n triangolare: verifichiamo anche questo)
e registra la distanza massima e le partizioni che la raggiungono.
"""
import sys


def shift(parti):
    """Applica lo shift B: togli 1 da ogni parte, aggiungi la parte s."""
    s = len(parti)
    nuove = [p - 1 for p in parti if p > 1] + [s]
    return tuple(sorted(nuove, reverse=True))


def partizioni(n, massimo=None):
    """Genera tutte le partizioni di n con parti <= massimo (ordine decrescente)."""
    if massimo is None:
        massimo = n
    if n == 0:
        yield ()
        return
    for prima in range(min(n, massimo), 0, -1):
        for resto in partizioni(n - prima, prima):
            yield (prima,) + resto


def distanze_al_punto_fisso(n, punto_fisso):
    """Restituisce dict partizione -> numero di shift per arrivare al punto fisso.

    Usa memoizzazione lungo le orbite; presuppone che ogni orbita finisca in punto_fisso
    (lo verifichiamo con un controllo di sicurezza sul numero di passi).
    """
    dist = {punto_fisso: 0}
    for lam in partizioni(n):
        cammino = []
        cur = lam
        while cur not in dist:
            cammino.append(cur)
            cur = shift(cur)
            assert len(cammino) <= 10 * n * n, "orbita troppo lunga: non converge?"
        base = dist[cur]
        for i, p in enumerate(reversed(cammino)):
            dist[p] = base + i + 1
    return dist


def main(k_max):
    for k in range(1, k_max + 1):
        n = k * (k + 1) // 2
        delta = tuple(range(k, 0, -1))
        dist = distanze_al_punto_fisso(n, delta)
        D = max(dist.values())
        estremali = sorted(p for p, d in dist.items() if d == D)
        print(f"k={k} n={n} #partizioni={len(dist)} D_B={D} k^2-k={k*k-k} "
              f"#estremali={len(estremali)}")
        for p in estremali[:12]:
            print("   ", p)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_1.py (python3, clean copy of the researcher sandbox): exit 0 in 0.1s; stdout: '1, 1)\n    (4, 4, 3, 3, 3, 3, 3, 3, 2)\n    (4, 4, 4, 3, 2, 2, 2, 2, 2, 1, 1, 1)\n    (4, 4, 4, 3, 2, 2, 2, 2, 2, 2, 1)\nk=8 n=36 #partizioni=17977 D_B=56 k^2-k=56 #estremali=1267\n    (5, 4, 4, 3`

**attempt_001 / code_2** (python, rigor `exact`): Exploration only: along every orbit for k ≤ 8, records the last time the pile count leaves {k−1,k,k+1} and the first time diagonals 1..k−1 are full; used to guide the (unfinished) upper-bound strategy. Exact integers, all partitions of T_k for k=3..8, ~1 min.

```python
"""Esplorazione: statistiche sulla successione m(t) = numero di pile lungo le orbite."""
import sys
from collections import Counter
from calcola_DB_triangolari import shift, partizioni


def conteggio_diagonali(parti):
    """c_d = numero di celle (i,j) del diagramma (righe = pile) con i+j-1 = d."""
    c = Counter()
    for i, p in enumerate(parti, start=1):
        for j in range(1, p + 1):
            c[i + j - 1] += 1
    return c


def diagonali_piene_fino(parti, d_max):
    """True se le diagonali 1..d_max sono tutte piene (c_d = d)."""
    c = conteggio_diagonali(parti)
    return all(c[d] == d for d in range(1, d_max + 1))


def main(k):
    n = k * (k + 1) // 2
    delta = tuple(range(k, 0, -1))
    peggio_stab = 0; peggio_pieno = 0; combinazioni = Counter()
    for lam in partizioni(n):
        orbita = [lam]
        while orbita[-1] != delta:
            orbita.append(shift(orbita[-1]))
        d = len(orbita) - 1
        m = [len(p) for p in orbita]
        t_stab = max([t + 1 for t in range(len(m)) if abs(m[t] - k) > 1] + [0])
        t_pieno = next(t for t, p in enumerate(orbita) if diagonali_piene_fino(p, k - 1))
        peggio_stab = max(peggio_stab, t_stab)
        peggio_pieno = max(peggio_pieno, t_pieno)
        combinazioni[(t_pieno, d - t_pieno)] += 1
    print(f"k={k}: max t_stab={peggio_stab}, max t_pieno={peggio_pieno}, k^2-k={k*k-k}")


if __name__ == "__main__":
    for k in range(3, int(sys.argv[1]) + 1):
        main(k)

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_2.py (python3, clean copy of the researcher sandbox): exit 1 in 0.1s; stdout: ''; stderr: 'Traceback (most recent call last):\n  File "/Users/thomastumini/proof-pursuit/runs/p3_c2/verifica/attempt_001/code_2.py", line 41, in <module>\n    for k in range(3, int(sys.argv[1]) +`


---
Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p3_c2.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
