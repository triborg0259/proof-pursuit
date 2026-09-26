# Problem 2 — Part 3 — submission draft (value by construction)

**Declared status: PARTIAL.** Upper bound by explicit construction, counted exactly; the lower bound
(minimality) is NOT proved. The cell is graded on the value: if the value is the true minimum, it counts; we declare it
as a candidate, not as a theorem.

## 1. Result and scope
### $Q_6$: candidate value $204$ ($=|E|+12$)
Labelling (increasing label order, position $i$ = coordinate $i$):

`000000,111100,110011,001111,101010,011010,100110,010110,101001,011001,100101,010101,100000,010000,001000,111000,000100,110100,101100,011100,000010,110010,001110,111110,000001,110001,001101,111101,100011,010011,001011,111011,000111,110111,101111,011111,110000,101000,011000,100100,010100,001100,100010,010010,001010,111010,000110,110110,101110,011110,100001,010001,001001,111001,000101,110101,101101,011101,000011,101011,011011,100111,010111,111111`

## 2. Proof
**"Star" construction.** Let $R$ be a set of even-weight vertices pairwise at Hamming distance $\ge4$
(a distance-4 code among the even-weight words; here the lexicode). Non-peaks $=R\cup\{\text{odd weight}\}$,
peaks $=$ even vertices outside $R$. Labels: first $R$ and the odd vertices not adjacent to $R$ (valleys), then the odd
vertices adjacent to a root (each has exactly one neighbouring root, because two roots are at distance $\ge4$), finally the peaks.
Every non-peak has $p=1$ (a valley, or a single root as its only smaller neighbour); every peak has all $d$ smaller
neighbours with $p=1$, hence $p=d$. Total $=(d+1)2^{d-1}-(d-1)|R|$: for $d=3,4,5$ this gives $14,34,88$, i.e. exactly the
minima proved in parts 1–2; for $d=6,7,8$ it gives $204,464,1040$ with $|R|=4,8,16$ (optimal codes: $A(5,3)=4$,
$A(6,3)=8$, $A(7,3)=16$, Hamming).

**Optimality within the family (proved).** For a labelling of this type (independent peaks, complement
a forest, $p=1$ on all non-peaks) the total is $|E|+c$ with $c$ = number of components of the forest, and
$c=(d-1)|P|-2^{d-1}(d-2)$ with $P$ the set of peaks. Reducing $c$ requires a smaller independent set $P$
with acyclic complement. An independent set of $Q_d$ of size $2^{d-1}-s$ with $s$ small contains at most one
vertex of the minority class (if $B$ are the odd vertices of $P$, $|N(B)|\ge 2d-2$ for $|B|\ge2$ and the size
does not add up); if $P$ is entirely even, the complement is acyclic only if the $2^{d-1}-|P|$ even vertices outside $P$ are
pairwise at distance $\ge4$ (two even vertices at distance 2 have two common odd neighbours: a 4-cycle), i.e. they form an
even distance-4 code, of size at most $A(d-1,3)$; if $P$ contains an odd vertex $o$, the complement contains the $d$
even neighbours of $o$ and the vertices $o\oplus e_i\oplus e_j$, which form 6-cycles. Hence within the family the minimum of $c$ is
$2^{d-1}-(d-1)A(d-1,3)$: $12,16,16$ for $d=6,7,8$. **What is missing:** ruling out labellings outside the family
(excess $X>0$), as done for $d=5$ in part 2 with the case analysis.

## 3. Verification: instructions, dependencies, timings
```
cd problema-2/esperimenti && python3 costruzione_stelle.py 6   # ricostruisce e conta (< 1 s ciascuno)
```
Counting with `conta_cammini.py` (exact integers). Control annealing (`ricottura_controllo.py`): see `ricottura_q*.log`.

## 4. Sources and contribution
Construction and argument entirely ours; standard distance-4 codes (lexicode/Hamming). No citation used.

## 5. Limits and unresolved parts
General lower bound not proved: the value is a motivated candidate (it coincides with the known minima for $d\le5$ and,
for $d=9$, with $|R|=20$ the same formula gives $2400$, the upper bound known to the organisers).


## 6. How this result was obtained (multi-agent trace)
Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- **attempt_001** — Researcher: family `reduction`, subgoal: Determine U(Q_6) = 204: explicit labelling with 204 uphill paths, and a lower-bound proof (hand reduction to a finite statement about induced forests of Q_6, refuted by exact enumeration in seconds).; declared `CELL_SOLVED_CANDIDATE`.
  - Why this approach: No prior attempt on this cell. The Q_5 proof (accepted READY_FOR_HUMAN) reduces the lower bound to a small finite statement; the same lemmas hold verbatim for Q_6 and the bound 204 = |E|+12 is exactly where the resulting finite statement becomes false, while simulated annealing (5 of 6 seeds) never beat 204. The construction generalises the Q_3/Q_4/Q_5 optima (peaks = one parity class minus a distance-4 code), consistent with Pike's characterisation of decycling numbers of hypercubes.
  - Position w.r.t. the literature: The deterministic arXiv search returned only 1412.3893v1 (evolutionary biology, "uphill" in a fitness-landscape sense) — irrelevant. I searched the web for the related notion that my reduction produces: decycling (feedback vertex) sets of hypercubes. D. A. Pike, "Decycling hypercubes", Graphs and Combinatorics 19 (2003) 547–550 (abstract read on link.springer.com/article/10.1007/s00373-003-0529-9, paper NOT read): "∇(Q_n) = 2^{n-1} − A(n,4) if and only if Q_n has a minimum decycling set that consists of pairwise non-adjacent vertices". This is CITED for context only: it explains why the optimal construction takes peaks = a parity class minus a distance-4 code (A(6,4)=4 gives 28 peaks), and it is consistent with our computed fact that Q_6 has no independent-plus-≤2 decycling set of size ≤ 27. No statement from the literature is used in the proof; every finite fact is established by our own exact enumeration.
  - Referee: `UNKNOWN_STATUS` / `READY_FOR_HUMAN`; next: Human reviews the exact target, proof and evidence, then approves explicit claims

## 7. arXiv literature consulted
- arXiv:1412.3893v1 — *The competition between simple and complex evolutionary trajectories in asexual populations* (Ian E. Ochs, Michael M. Desai, 2014), found by query `uphill paths`; abstract read, full text not relied upon.

## 8. Code
**attempt_001 / code_1** (python, rigor `exact`): Shared exact utilities for Q_6 (parity classes, neighbour bitmasks, union-find forest test).

```python
"""Utilita' esatte (interi/bitmask) per Q_6: classi di parita', vicini, foreste."""
D = 6
N = 1 << D
PARI = [v for v in range(N) if bin(v).count("1") % 2 == 0]
DISPARI = [v for v in range(N) if bin(v).count("1") % 2 == 1]

def vicini(v):
    return [v ^ (1 << i) for i in range(D)]

def maschera_vicini(v):
    m = 0
    for u in vicini(v):
        m |= 1 << u
    return m

MASCHERA_VICINI = [maschera_vicini(v) for v in range(N)]

def bit_a_lista(m):
    return [v for v in range(N) if (m >> v) & 1]

def e_foresta(maschera_vertici):
    """True se il sottografo indotto e' aciclico (union-find esatto)."""
    genitore = {}
    def trova(x):
        while genitore[x] != x:
            genitore[x] = genitore[genitore[x]]
            x = genitore[x]
        return x
    vertici = bit_a_lista(maschera_vertici)
    for v in vertici:
        genitore[v] = v
    for v in vertici:
        for u in vicini(v):
            if u > v and (maschera_vertici >> u) & 1:
                ru, rv = trova(u), trova(v)
                if ru == rv:
                    return False
                genitore[ru] = rv
    return True

def stringa(v):
    return "".join(str((v >> i) & 1) for i in range(D))

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_1.py (python3, clean copy of the researcher sandbox): exit 0 in 0.0s; stdout: ''; stderr: ''`

**attempt_001 / code_2** (python, rigor `exact`): Computation 3: refutes (★₀) (all peaks in one class) by pruned DFS over R' (every distance-2 pair of R' must lie in N(o) for some o in H_O) plus union-find; covers h=0,1,2, H_O ∋ 100000 (WLOG by translation), all R' of size 5+h. Output: 0 forests, 0.6 s.

```python
import itertools, time
from cubo6 import DISPARI, MASCHERA_VICINI, PARI, e_foresta
MASCHERA_O = sum(1 << o for o in DISPARI)
E1 = 1

def coppia_coperta(a, b, H_O):
    return any((MASCHERA_VICINI[o] >> a) & 1 and (MASCHERA_VICINI[o] >> b) & 1 for o in H_O)

def compatibile(v, R, H_O):
    return all(bin(v ^ r).count("1") != 2 or coppia_coperta(v, r, H_O) for r in R)

def dfs(R, idx, taglia, H_O, contatori):
    if len(R) == taglia:
        contatori["candidati"] += 1
        m = sum(1 << r for r in R) | (MASCHERA_O & ~sum(1 << o for o in H_O))
        if e_foresta(m):
            contatori["foreste"] += 1
            print("FORESTA TROVATA", R, H_O)
        return
    for k in range(idx, len(PARI)):
        if compatibile(PARI[k], R, H_O):
            R.append(PARI[k])
            dfs(R, k + 1, taglia, H_O, contatori)
            R.pop()

def main():
    inizio = time.time()
    altri = [o for o in DISPARI if o != E1]
    scelte_H = {0: [()], 1: [(E1,)], 2: [(E1, o) for o in altri]}
    for h in (0, 1, 2):
        contatori = {"candidati": 0, "foreste": 0}
        for H_O in scelte_H[h]:
            dfs([], 0, 5 + h, list(H_O), contatori)
        print(f"h={h}: insiemi H_O {len(scelte_H[h])}, candidati R' sopravvissuti alla potatura "
              f"{contatori['candidati']}, foreste {contatori['foreste']}, tempo {time.time()-inizio:.1f}s")

if __name__ == "__main__":
    main()

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_2.py (python3, clean copy of the researcher sandbox): exit 0 in 0.6s; stdout: "h=0: insiemi H_O 1, candidati R' sopravvissuti alla potatura 0, foreste 0, tempo 0.0s\nh=1: insiemi H_O 1, candidati R' sopravvissuti alla potatura 37, foreste 0, tempo 0.0s\nh=2: insiemi H_O 31, `

**attempt_001 / code_3** (c, rigor `exact`): Computation 2 (independent, brute force): refutes (★₀) by testing with union-find every R' of size 5+h for h=0 (201376 sets), h=1 with H_O={100000} (906192 sets), h=2 with H_O={100000,o} for all 31 other odd o (104,341,536 pairs). Output: 0 forests; 10.3 s wall-clock (cc -O2).

```c
#include <stdio.h>
#include <stdint.h>
static int genitore[64];
static int trova(int x) { while (genitore[x] != x) x = genitore[x] = genitore[genitore[x]]; return x; }
static int e_foresta(uint64_t m) {
    for (int v = 0; v < 64; v++) genitore[v] = v;
    for (int v = 0; v < 64; v++) {
        if (!((m >> v) & 1)) continue;
        for (int i = 0; i < 6; i++) {
            int u = v ^ (1 << i);
            if (u < v || !((m >> u) & 1)) continue;
            int a = trova(u), b = trova(v);
            if (a == b) return 0;
            genitore[a] = b;
        }
    }
    return 1;
}
static int pari[32], n_pari = 0;
static uint64_t maschera_O = 0;
static long esaminati = 0, foreste = 0;
static void combinazioni(int da, int k, uint64_t m) {
    if (k == 0) {
        esaminati++;
        if (e_foresta(m)) { foreste++; printf("FORESTA TROVATA maschera %llx\n", (unsigned long long)m); }
        return;
    }
    for (int i = da; i <= n_pari - k; i++) combinazioni(i + 1, k - 1, m | (1ULL << pari[i]));
}
int main(void) {
    for (int v = 0; v < 64; v++) {
        if (__builtin_popcount(v) % 2 == 0) pari[n_pari++] = v; else maschera_O |= 1ULL << v;
    }
    combinazioni(0, 5, maschera_O);
    printf("h=0: R' di taglia 5 esaminati %ld, foreste %ld\n", esaminati, foreste);
    esaminati = foreste = 0;
    combinazioni(0, 6, maschera_O & ~(1ULL << 1));
    printf("h=1: R' di taglia 6 esaminati %ld, foreste %ld\n", esaminati, foreste);
    esaminati = foreste = 0;
    for (int o = 0; o < 64; o++) {
        if (o == 1 || __builtin_popcount(o) % 2 == 0) continue;
        combinazioni(0, 7, maschera_O & ~(1ULL << 1) & ~(1ULL << o));
    }
    printf("h=2: coppie (H_O, R') di taglia 7 esaminate %ld, foreste %ld\n", esaminati, foreste);
    return 0;
}

```
Trusted re-run by the orchestrator: `code_3: not re-run (language 'c' not supported by the orchestrator)`

**attempt_001 / code_4** (python, rigor `exact`): Computations 1a/1b (mixed parity classes): part A enumerates all B ⊆ O with 100000 ∈ B and |N(B)| ≤ 20 by DFS (18878 nodes) and finds no B with 2 ≤ |B| ≤ 13 and |N(B)| ≤ 7+|B|; part B (b=1) tests all R = N(100000) ∪ (≤2 extra even) and all H of allowed size with union-find: 254840 pairs, 0 forests. 3.6 s.

```python
import itertools, time
from cubo6 import DISPARI, MASCHERA_VICINI, PARI, e_foresta
MASCHERA_O = sum(1 << o for o in DISPARI)
E1 = 1

def conta(m):
    return bin(m).count("1")

def parte_A():
    trovati, contatore = [], [0]
    altri = [o for o in DISPARI if o != E1]
    def dfs(B, mN, idx):
        contatore[0] += 1
        b = len(B)
        if 2 <= b <= 13 and conta(mN) <= 7 + b:
            trovati.append(list(B))
        if b == 13:
            return
        for k in range(idx, len(altri)):
            mN2 = mN | MASCHERA_VICINI[altri[k]]
            if conta(mN2) <= 20:
                B.append(altri[k])
                dfs(B, mN2, k + 1)
                B.pop()
    dfs([E1], MASCHERA_VICINI[E1], 0)
    print(f"parte A: nodi DFS visitati {contatore[0]}, insiemi B con |N(B)| <= 7+|B| trovati: {len(trovati)}")
    return trovati

def parte_B():
    mNB = MASCHERA_VICINI[E1]
    base = [v for v in PARI if (mNB >> v) & 1]
    extra_pari = [v for v in PARI if not (mNB >> v) & 1]
    esaminati, foreste = 0, 0
    for k in range(0, 3):
        for extra in itertools.combinations(extra_pari, k):
            R = base + list(extra)
            mR = sum(1 << r for r in R)
            base_m = (mR | MASCHERA_O) & ~(1 << E1)
            cand = [v for v in range(64) if (base_m >> v) & 1]
            for h in range(0, k + 1):
                for H in itertools.combinations(cand, h):
                    esaminati += 1
                    if e_foresta(base_m & ~sum(1 << x for x in H)):
                        foreste += 1
                        print("FORESTA TROVATA", R, H)
    print(f"parte B: coppie (R,H) esaminate {esaminati}, foreste trovate {foreste}")

if __name__ == "__main__":
    t = time.time()
    parte_A()
    parte_B()
    print(f"tempo {time.time()-t:.1f}s")

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_4.py (python3, clean copy of the researcher sandbox): exit 0 in 3.6s; stdout: 'parte A: nodi DFS visitati 18878, insiemi B con |N(B)| <= 7+|B| trovati: 0\nparte B: coppie (R,H) esaminate 254840, foreste trovate 0\ntempo 3.6s'; stderr: ''`

**attempt_001 / code_5** (python, rigor `exact`): Upper bound: builds the 204-path labelling (peaks = even vertices minus the distance-4 code {000000,111100,001111,110011}) and counts exactly with the Lemma 1 recursion (conta_cammini.py from the Q_5 certificate): prints 204, 12 valleys, and the 64-vertex order.

```python
from conta_cammini import conta_cammini, stringa
from cubo6 import DISPARI, MASCHERA_VICINI, PARI
D = 6
R = [0b000000, 0b001111, 0b110011, 0b111100]  # bit i = coordinata i+1

def costruisci():
    m_foglie = 0
    for r in R:
        m_foglie |= MASCHERA_VICINI[r]
    foglie = [o for o in DISPARI if (m_foglie >> o) & 1]
    isolati = [o for o in DISPARI if not (m_foglie >> o) & 1]
    picchi = [v for v in PARI if v not in R]
    assert len(foglie) == 24 and len(isolati) == 8 and len(picchi) == 28
    return R + isolati + foglie + picchi

if __name__ == "__main__":
    ordine = costruisci()
    totale, p, valli = conta_cammini(ordine, D)
    print("cammini in salita:", totale, "valli:", len(valli))
    print("ordine:", ",".join(stringa(v, D) for v in ordine))

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_5.py (python3, clean copy of the researcher sandbox): exit 0 in 0.0s; stdout: 'cammini in salita: 204 valli: 12\nordine: 000000,111100,110011,001111,101010,011010,100110,010110,101001,011001,100101,010101,100000,010000,001000,111000,000100,110100,101100,011100,000010,110010,`

**attempt_001 / code_6** (python, rigor `exact`): Independent verification of the submitted labelling (string-based, no shared code): reads the 64 strings from stdin and enumerates every uphill path by DFS from each valley. Prints 204, 12 valleys.

```python
import sys

def vicini_stringa(s):
    return [s[:i] + ("1" if s[i] == "0" else "0") + s[i + 1:] for i in range(len(s))]

def conta(ordine):
    etichetta = {s: i + 1 for i, s in enumerate(ordine)}
    assert len(etichetta) == 64 and all(len(s) == 6 for s in ordine)
    valli = [s for s in ordine if all(etichetta[t] > etichetta[s] for t in vicini_stringa(s))]
    def cammini_da(s):
        return 1 + sum(cammini_da(t) for t in vicini_stringa(s) if etichetta[t] > etichetta[s])
    return sum(cammini_da(v) for v in valli), len(valli)

if __name__ == "__main__":
    ordine = sys.stdin.read().replace("\n", "").replace(" ", "").split(",")
    totale, n_valli = conta(ordine)
    print("cammini in salita (DFS):", totale, "valli:", n_valli)

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_6.py (python3, clean copy of the researcher sandbox): exit 1 in 0.0s; stdout: ''; stderr: '(ordine)\n                      ~~~~~^^^^^^^^\n  File "/Users/thomastumini/proof-pursuit/runs/p2_c3/verifica/attempt_001/code_6.py", line 8, in conta\n    assert len(etichetta) == 64 a`

**attempt_001 / code_7** (python, rigor `exact`): Sanity check (evidence only): T = 192 + #valleys + X and X ∈ {0} ∪ [4,∞) on 20000 random labellings (all asserts pass; smallest positive X seen: 238).

```python
import random
from conta_cammini import conta_cammini, vicini
D, N = 6, 64
rng = random.Random(0)
minimo_X_positivo = None
for _ in range(20000):
    ordine = list(range(N)); rng.shuffle(ordine)
    etichetta = {v: i for i, v in enumerate(ordine)}
    totale, p, valli = conta_cammini(ordine, D)
    X = sum(p[u] - 1 for u in range(N) for w in vicini(u, D) if etichetta[u] < etichetta[w])
    assert totale == 192 + len(valli) + X
    assert X == 0 or X >= 4
    if X > 0 and (minimo_X_positivo is None or X < minimo_X_positivo):
        minimo_X_positivo = X
print("20000 etichettature casuali: identita' verificata; minimo X positivo osservato:", minimo_X_positivo)

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_7.py (python3, clean copy of the researcher sandbox): exit 0 in 2.9s; stdout: "20000 etichettature casuali: identita' verificata; minimo X positivo osservato: 238"; stderr: ''`

**attempt_001 / code_8** (python, rigor `float_exploration_only`): Simulated annealing over labellings of Q_6 (exploration only, 300k swap moves per seed, exact integer scoring): seeds 0,1,2,3,5 reached 204 with 12 valleys, seed 4 stuck at 253; never below 204.

```python
import random, sys, time
from conta_cammini import conta_cammini, stringa
D = 6
N = 1 << D

def ricottura(seed, passi, t0=3.0, t1=0.05):
    rng = random.Random(seed)
    ordine = list(range(N)); rng.shuffle(ordine)
    val = conta_cammini(ordine, D)[0]
    migliore, miglior_ordine = val, ordine[:]
    for k in range(passi):
        t = t0 * (t1 / t0) ** (k / passi)
        i, j = rng.randrange(N), rng.randrange(N)
        ordine[i], ordine[j] = ordine[j], ordine[i]
        nuovo = conta_cammini(ordine, D)[0]
        if nuovo <= val or rng.random() < 2.718 ** ((val - nuovo) / t):
            val = nuovo
            if val < migliore:
                migliore, miglior_ordine = val, ordine[:]
        else:
            ordine[i], ordine[j] = ordine[j], ordine[i]
    return migliore, miglior_ordine

if __name__ == "__main__":
    seed = int(sys.argv[1]); passi = int(sys.argv[2]) if len(sys.argv) > 2 else 300000
    v, o = ricottura(seed, passi)
    tot, p, valli = conta_cammini(o, D)
    print(f"seed {seed}: migliore {v}, valli {len(valli)}")
    print("ordine:", ",".join(stringa(x, D) for x in o))

```
Trusted re-run by the orchestrator: `orchestrator re-ran code_8.py (python3, clean copy of the researcher sandbox): exit 1 in 0.0s; stdout: ''; stderr: 'Traceback (most recent call last):\n  File "/Users/thomastumini/proof-pursuit/runs/p2_c3/verifica/attempt_001/code_8.py", line 25, in <module>\n    seed = int(sys.argv[1]); passi = int`


---
Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c3.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
