Problem 2 — Part 4 — submission draft (value by construction)

Declared status: PARTIAL. Upper bound by explicit construction, counted exactly; the lower bound
(minimality) is NOT proved. The cell is graded on the value: if the value is the true minimum, it counts; we declare it
as a candidate, not as a theorem.

1. Result and scope

$Q_7$: candidate value $464$ ($=|E|+16$)

Labelling (increasing order of label, position $i$ = coordinate $i$):

0000000,1111000,1100110,0011110,1010101,0101101,0110011,1001011,0110100,1001100,1010010,0101010,1100001,0011001,0000111,1111111,1000000,0100000,0010000,1110000,0001000,1101000,1011000,0111000,0000100,1100100,1010100,0101100,0011100,1111100,0000010,1100010,0110010,1001010,0011010,1111010,1000110,0100110,0010110,1110110,0001110,1101110,1011110,0111110,0000001,1010001,0110001,1001001,0101001,1111001,1000101,0100101,0010101,1110101,0001101,1101101,1011101,0111101,1000011,0100011,0010011,1110011,0001011,1101011,1011011,0111011,1100111,1010111,0110111,1001111,0101111,0011111,1100000,1010000,0110000,1001000,0101000,0011000,1000100,0100100,0010100,1110100,0001100,1101100,1011100,0111100,1000010,0100010,0010010,1110010,0001010,1101010,1011010,0111010,0000110,1010110,0110110,1001110,0101110,1111110,1000001,0100001,0010001,1110001,0001001,1101001,1011001,0111001,0000101,1100101,0110101,1001101,0011101,1111101,0000011,1100011,1010011,0101011,0011011,1111011,1000111,0100111,0010111,1110111,0001111,1101111,1011111,0111111

$Q_8$: candidate value $1040$ ($=|E|+16$)

Labelling (increasing order of label, position $i$ = coordinate $i$):

00000000,11110000,11001100,00111100,10101010,01011010,01100110,10010110,01101001,10011001,10100101,01010101,11000011,00110011,00001111,11111111,10000000,01000000,00100000,11100000,00010000,11010000,10110000,01110000,00001000,11001000,10101000,01101000,10011000,01011000,00111000,11111000,00000100,11000100,10100100,01100100,10010100,01010100,00110100,11110100,10001100,01001100,00101100,11101100,00011100,11011100,10111100,01111100,00000010,11000010,10100010,01100010,10010010,01010010,00110010,11110010,10001010,01001010,00101010,11101010,00011010,11011010,10111010,01111010,10000110,01000110,00100110,11100110,00010110,11010110,10110110,01110110,00001110,11001110,10101110,01101110,10011110,01011110,00111110,11111110,00000001,11000001,10100001,01100001,10010001,01010001,00110001,11110001,10001001,01001001,00101001,11101001,00011001,11011001,10111001,01111001,10000101,01000101,00100101,11100101,00010101,11010101,10110101,01110101,00001101,11001101,10101101,01101101,10011101,01011101,00111101,11111101,10000011,01000011,00100011,11100011,00010011,11010011,10110011,01110011,00001011,11001011,10101011,01101011,10011011,01011011,00111011,11111011,00000111,11000111,10100111,01100111,10010111,01010111,00110111,11110111,10001111,01001111,00101111,11101111,00011111,11011111,10111111,01111111,11000000,10100000,01100000,10010000,01010000,00110000,10001000,01001000,00101000,11101000,00011000,11011000,10111000,01111000,10000100,01000100,00100100,11100100,00010100,11010100,10110100,01110100,00001100,10101100,01101100,10011100,01011100,11111100,10000010,01000010,00100010,11100010,00010010,11010010,10110010,01110010,00001010,11001010,01101010,10011010,00111010,11111010,00000110,11000110,10100110,01010110,00110110,11110110,10001110,01001110,00101110,11101110,00011110,11011110,10111110,01111110,10000001,01000001,00100001,11100001,00010001,11010001,10110001,01110001,00001001,11001001,10101001,01011001,00111001,11111001,00000101,11000101,01100101,10010101,00110101,11110101,10001101,01001101,00101101,11101101,00011101,11011101,10111101,01111101,00000011,10100011,01100011,10010011,01010011,11110011,10001011,01001011,00101011,11101011,00011011,11011011,10111011,01111011,10000111,01000111,00100111,11100111,00010111,11010111,10110111,01110111,11001111,10101111,01101111,10011111,01011111,00111111

2. Proof

"Star" construction. Let $R$ be a set of even-weight vertices pairwise at Hamming distance $\ge4$
(a distance-4 code among the even-weight words; here the lexicode). Non-peaks $=R\cup\{\text{odd weight}\}$,
peaks $=$ even vertices outside $R$. Labels: first $R$ and the odd vertices not adjacent to $R$ (valleys), then the odd
vertices adjacent to a root (each has exactly one neighbouring root, because two roots are at distance $\ge4$), finally the peaks.
Every non-peak has $p=1$ (a valley, or a single root as its only smaller neighbour); every peak has all its $d$ smaller
neighbours with $p=1$, hence $p=d$. Total $=(d+1)2^{d-1}-(d-1)|R|$: for $d=3,4,5$ this gives $14,34,88$, i.e. exactly the
minima proved in parts 1–2; for $d=6,7,8$ it gives $204,464,1040$ with $|R|=4,8,16$ (optimal codes: $A(5,3)=4$,
$A(6,3)=8$, $A(7,3)=16$, Hamming).

Optimality within the family (proved). For a labelling of this type (independent peaks, complement
a forest, $p=1$ on all non-peaks) the total is $|E|+c$ with $c$ = number of components of the forest, and
$c=(d-1)|P|-2^{d-1}(d-2)$ with $P$ the set of peaks. Reducing $c$ requires a smaller independent set $P$
with acyclic complement. An independent set of $Q_d$ of size $2^{d-1}-s$ with $s$ small contains at most one
vertex of the minority class (if $B$ is the set of odd vertices of $P$, $|N(B)|\ge 2d-2$ for $|B|\ge2$ and the size
does not add up); if $P$ is entirely even, the complement is acyclic only if the $2^{d-1}-|P|$ even vertices outside $P$ are
pairwise at distance $\ge4$ (two even vertices at distance 2 have two common odd neighbours: a 4-cycle), i.e. they form an
even distance-4 code, of size at most $A(d-1,3)$; if $P$ contains an odd vertex $o$, the complement contains the $d$
even neighbours of $o$ and the vertices $o\oplus e_i\oplus e_j$, which form 6-cycles. Hence within the family the minimum of $c$ is
$2^{d-1}-(d-1)A(d-1,3)$: $12,16,16$ for $d=6,7,8$. What is missing: ruling out labellings outside the family
(excess $X>0$), as was done for $d=5$ in part 2 with the case analysis.

3. Verification: instructions, dependencies, timings
Counting with conta_cammini.py (exact integers). Control annealing (ricottura_controllo.py): see ricottura_q*.log.

4. Sources and contribution

Construction and argument entirely ours; standard distance-4 codes (lexicode/Hamming). No citation used.

5. Limits and unresolved parts

General lower bound not proved: the value is a motivated candidate (it coincides with the known minima for $d\le5$ and,
for $d=9$, with $|R|=20$ the same formula gives $2400$, the upper bound known to the organisers).

6. How this result was obtained (multi-agent trace)

Pipeline: formalised statement → Researcher (Claude, real shell) → orchestrator re-runs every script → two independent Referee judges (mathematics / evidence) → human approval. Trace:
- No agent run on this cell; the text was written by the team from its notes.

6b. Tokens used by the agents

- Token counts not recorded for this run (older harness version; only cost and turns were logged).

7. arXiv literature consulted

- arXiv:1412.3893v1 — The competition between simple and complex evolutionary trajectories in asexual populations (Ian E. Ochs, Michael M. Desai, 2014), found by query uphill paths; abstract read, full text not relied upon.

8. Code

The complete code, with the orchestrator's trusted re-runs, is in the write-up https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c4.tex and in the repository.

Full write-up (LaTeX, all resources): https://github.com/triborg0259/proof-pursuit/blob/main/report/cells/p2_c4.tex · Repository: https://github.com/triborg0259/proof-pursuit/blob/main/
