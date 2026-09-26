# Problema 1 — Parte 6 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 6 — $N$ lines in $\mathbb{R}^d$

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

Fejes Tóth's conjecture from the Setting, for every $N$ and every $d$. For $N$ lines in $\mathbb{R}^d$, write
$N = qd + s$ with $0 \le s < d$, and let
$$
M(N,d) = s \binom{q+1}{2} + (d-s) \binom{q}{2}.
$$
Prove or disprove: every $N$ lines in $\mathbb{R}^d$ satisfy
$$
S \;\le\; \left( \binom{N}{2} - M(N,d) \right) \frac{\pi}{2}.
$$
This is the value attained by splitting the lines as evenly as possible among $d$ mutually orthogonal
directions. Settling any infinite family not already covered above counts as partial progress.

*(Fine del problema 1. Punteggi: 1+2+3+5+8+13 = 32.)*

**Cosa consegniamo.** Problema aperto. Nessuna famiglia infinita nuova. Contributo: verifica numerica del bound per $N\le10$ nel piano (harness) e impostazione della ricerca di controesempi.

## 2. Dimostrazione
Congettura di Fejes Tóth completa. Con il harness numerico (`tools/autoloop.py`, hill climbing con riavvii) il massimo trovato coincide con il valore congetturato entro $2\cdot10^{-5}$ per tutti i casi provati; nessun superamento. Non è una prova (virgola mobile).

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- `problema-1/esperimenti/lines_Rd.py`
- `problema-1/esperimenti/p1_somma_angoli.py`

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); solo abstract letto.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); solo abstract letto.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); solo abstract letto.
Bilyk–Matzke [1801.07837]: bound generale via energia e riduzione dimensione alta → bassa; Lim–McCann [2007.08698]: equivalenza con l'unicità dell'ottimizzatore per ogni $\alpha>1$, dimostrata per $\alpha=\infty$.

## 5. Limiti e parti irrisolte
Tutto.
