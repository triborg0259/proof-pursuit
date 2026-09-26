# Problema 1 — Parte 5 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 5 — $d+2$ lines in $\mathbb{R}^d$

**Punteggio:** 8 points · **Valutazione:** Judged

The case $N = d+2$ in every dimension, with the same conjectured optimum: the $d$ coordinate axes, two of them
repeated. Prove that for every $d \ge 2$, any $d+2$ lines in $\mathbb{R}^d$ satisfy
$$
S \;\le\; \left( \binom{d+2}{2} - 2 \right) \frac{\pi}{2}.
$$

**Cosa consegniamo.** Nessuna prova. Riformulazione in termini di deficit ($\sum\delta_{ij}\ge\pi$) e sanity check dei valori.

## 2. Dimostrazione
La tesi equivale a: $d+2$ versori in $\mathbb R^d$ hanno deficit totale $\ge\pi$. Se la parte 3 si ottiene per riduzione a una catena (deficit $\ge\pi/2$), la via naturale è iterare la riduzione su due circuiti indipendenti della dipendenza lineare (rango $\le d$ fra $d+2$ vettori: lo spazio delle relazioni ha dimensione $\ge2$). Non sviluppato.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- `problema-1/esperimenti/lines_Rd.py`
- `problema-1/esperimenti/p1_somma_angoli.py`

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); solo abstract letto.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); solo abstract letto.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); solo abstract letto.
Non risulta noto (Bilyk–Matzke [1801.07837]; Lim–McCann [2007.08698]).

## 5. Limiti e parti irrisolte
Dipende dalla parte 3.
