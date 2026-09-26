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
