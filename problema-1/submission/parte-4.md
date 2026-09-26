# Problema 1 — Parte 4 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 4 — Five lines in $\mathbb{R}^3$, six in $\mathbb{R}^4$

**Punteggio:** 5 points · **Valutazione:** Judged

Two concrete instances of the next case, $N = d+2$: five lines in three dimensions and six lines in four.
In each, the conjectured optimum repeats two of the coordinate axes. Prove that any $5$ lines in $\mathbb{R}^3$
satisfy $S \le 4\pi$, and that any $6$ lines in $\mathbb{R}^4$ satisfy $S \le 13\pi/2$.

**Cosa consegniamo.** Nessuna prova. Riformulazione: entrambe le istanze sono il caso $N=d+2$, equivalente a deficit totale $\ge\pi$. Verifica numerica (non prova) del bound su entrambe le istanze.

## 2. Dimostrazione
Le due disuguaglianze richieste sono i casi $(d,N)=(3,5)$ e $(4,6)$ della parte 5. Con $\delta_{ij}=\pi/2-\theta_{ij}=\arcsin|\langle x_i,x_j\rangle|$ le tesi diventano $\sum_{i<j}\delta_{ij}\ge\pi$. Via computazionale ammessa dalla cella: massimizzazione rigorosa di $S$ su $(S^2)^5$ e $(S^3)^6$ con aritmetica a intervalli e branch-and-bound; parametri liberi 7 e 12 dopo le simmetrie, con massimi non lisci (coppie ortogonali o coincidenti), quindi serve un argomento locale attorno agli ottimi. Impostato, non eseguito: il caso in $\mathbb R^4$ è al limite dei 10 minuti.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- `problema-1/esperimenti/lines_Rd.py`
- `problema-1/esperimenti/p1_somma_angoli.py`

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:1801.07837v1 — On the Fejes Tóth Problem about the Sum of Angles Between Lines (Dmitriy Bilyk, Ryan W Matzke, 2018); solo abstract letto.
- arXiv:2007.08698v2 — On Fejes Tóth's conjectured maximizer for the sum of angles between lines (Tongseok Lim, Robert J. McCann, 2020); solo abstract letto.
- arXiv:1204.3850v1 — Simple Agents Learn to Find Their Way: An Introduction on Mapping Polygons (Jérémie Chalopin, Shantanu Das, Yann Disser, 2012); solo abstract letto.
Fejes Tóth (1959) copre $\mathbb R^3$ con $N\le6$ secondo Bilyk–Matzke [1801.07837]: la prima istanza è nota in letteratura, ma la citazione non vale come prova.

## 5. Limiti e parti irrisolte
Entrambe le istanze: prova mancante. Strada realistica: dedurle dalla parte 5 oppure completare il branch-and-bound a intervalli per $\mathbb R^3$.
