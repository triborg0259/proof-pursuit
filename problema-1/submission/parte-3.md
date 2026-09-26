# Problema 1 — Parte 3 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 3 — $d+1$ lines in $\mathbb{R}^d$

**Punteggio:** 3 points · **Valutazione:** Judged

The first case in every dimension: one line more than the dimension, $N = d+1$, where the conjectured optimum
repeats exactly one of the $d$ coordinate axes. Let $d \ge 1$. Prove that any $d+1$ lines in $\mathbb{R}^d$ satisfy
$$
S \;\le\; \left( \binom{d+1}{2} - 1 \right) \cdot \frac{\pi}{2}.
$$

**Cosa consegniamo.** Riduzione dell'enunciato a una disuguaglianza sui deficit $\delta_{ij}=\pi/2-\theta_{ij}$: la tesi equivale a $\sum_{i<j}\delta_{ij}\ge\pi/2$ per $d+1$ versori in $\mathbb R^d$. Il lemma della parte 2 (dimostrato e approvato) fornisce esattamente un deficit totale $\ge\pi/2$ lungo una catena. Il caso $d=1$ è banale (due rette coincidenti, $S=0$).

## 2. Dimostrazione
**Fatto 1 (dimostrato, parte 2).** Una catena di $m$ versori in $\mathbb R^{m-1}$ ha $\sum\theta(x_i,x_{i+1})\le(m-2)\pi/2$, cioè deficit totale sui passi consecutivi $\ge\pi/2$.

**Fatto 2 (dimostrato).** $d+1$ versori in $\mathbb R^d$ sono linearmente dipendenti; esiste un circuito minimale $x_{i_1},\dots,x_{i_m}$ ($m\le d+1$) con $\sum a_j x_{i_j}=0$, $a_j\ne0$, e ogni $m-1$ di essi indipendenti.

**Strategia (non completata).** Costruire dal circuito una catena di $m$ versori in uno spazio di dimensione $m-1$ (proiezioni successive sugli ortogonali di $\mathrm{span}(x_{i_1},\dots,x_{i_k})$) e confrontare gli angoli della catena con quelli originali tramite la disuguaglianza triangolare sferica; il confronto diretto perde un termine $\sum_i\delta_i$ per ogni proiezione e non basta: serve una scelta migliore dell'ordine del circuito o una stima più fine. Verifica numerica (harness, `problema-1/esperimenti`): nessuna configurazione trovata supera il bound per $d\le6$.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- `problema-1/esperimenti/lines_Rd.py`
- `problema-1/esperimenti/p1_somma_angoli.py`

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); solo abstract letto.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); solo abstract letto.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); solo abstract letto.
Bilyk–Matzke [1801.07837] dichiarano risolto solo il caso del piano; Lim–McCann [2007.08698] trattano una deformazione a un parametro: il caso $N=d+1$ non risulta noto, coerente con il fatto che la gara fornisce il lemma della parte 2 come mattone.

## 5. Limiti e parti irrisolte
Manca il passaggio da rette generiche a una catena senza perdita di deficit. Le parti 1–2 approvate restano utilizzabili come ipotesi.
