# Problema 2 — note di triage

## Definizioni
- Etichettatura $f:V\to\{1..n\}$ biiettiva. Valle = minimo locale (tutti i vicini con etichetta maggiore).
- Cammino in salita = cammino da una valle con etichette strettamente crescenti (lunghezza $\ge1$; la valle sola conta).
- $U(G)=\min_f \#\{\text{cammini in salita}\}$. $Q_d$: $2^d$ vertici, $d2^{d-1}$ spigoli.

**Osservazione strutturale.** Il conteggio dipende solo dall'orientazione aciclica indotta da $f$ (spigolo
orientato dal minore al maggiore). Posto $p(v)$ = numero di cammini in salita che terminano in $v$:
$$p(v)=[v\text{ valle}]+\sum_{u\to v}p(u),\qquad \#\text{cammini}=\sum_v p(v).$$
Calcolo esatto in $O(|E|)$ con interi (nessun problema numerico). Perfetto per ricerca locale sulle etichettature.

## Richieste per parte
| Parte | Richiesta | Punti | Tipo |
|---|---|---|---|
| C1 | $U(Q_3)$, $U(Q_4)$ + etichettatura esplicita | 1 | Checked instantly |
| C2 | $U(Q_5)$ + etichettatura | 2 | Checked instantly |
| C3 | $U(Q_6)$ + etichettatura | 3 | Checked instantly |
| C4 | $U(Q_7)$, $U(Q_8)$ + etichettature | 5 | Checked instantly |
| C5 | Migliorare $2368\le U(Q_9)\le2400$: etichettatura con $\le2399$ oppure prova $\ge2369$ | 8 | Judged |
| C6 | $U(Q_9)$ esatto con prova di entrambi i bound | 13 | Judged · Open |

**Formato di consegna:** lista dei $2^d$ vertici in ordine crescente di etichetta, come stringhe 0/1.
Prove computer-assisted ammesse (< 10 min, codice incluso, spiegazione del perché il calcolo prova il bound).

## Ambiguità / dati mancanti
1. Convenzione delle stringhe 0/1 (coordinata 1 a sinistra o a destra?): irrilevante per il conteggio (simmetria
   di $Q_d$), ma va dichiarata nella consegna.
2. "Checked instantly" su C1–C4: il valore viene confrontato con quello degli organizzatori. Un valore sbagliato
   per difetto di ricerca (minimo locale) costa la cella: serve o una prova di minimalità o ricerca esaustiva.
3. C5: "lower bound unpublished" ⇒ gli organizzatori hanno un argomento non in letteratura; non possiamo leggerlo.

## Fatti dimostrabili subito (sanity)
- **Bound IMO generalizzato:** ogni vertice è fine di almeno un cammino in salita ($p(v)\ge1$, seguendo vicini
  decrescenti si arriva a una valle). Quindi $p(v)\ge\max(1,\deg^-(v))$ (i $\deg^-$ vicini minori hanno ciascuno
  $p\ge1$ e danno cammini distinti). Sommando: $\#\ge|E|+\#\text{valli}\ge|E|+1$.
  Per la griglia questo è esatto ($2n^2-2n+1=|E|+1$). Per $Q_d$: $U(Q_d)\ge d2^{d-1}+1$; per $Q_9$: $\ge2305$,
  ma il bound noto è $2368$: **il cubo NON raggiunge $|E|+1$**, l'eccesso è tra 64 e 96. Il cuore del problema è
  capire perché e quantificare l'eccesso.
- Uguaglianza in $p(v)=\deg^-(v)$ richiede $p(u)=1$ per ogni vicino minore $u$, cioè $\deg^-(u)\le1$: in un grafo
  regolare di grado $d$ questo è impossibile per tutti i vertici "alti": l'eccesso viene dai vertici con molti
  vicini minori che a loro volta hanno molti vicini minori.
- Piccolo caso: $Q_1$ (uno spigolo): 1 valle, cammini: valle sola + spigolo = 2 = $|E|+1$. $Q_2$ (4-ciclo):
  etichette 1,2,4,3 attorno: valle 1; cammini: (1),(1,2),(1,3),(1,2,4),(1,3,4) = 5 = $|E|+1$. Per $Q_3$ da calcolare.

## Approcci
- **A. Calcolo esatto per $Q_3$**: $8!=40320$ etichettature, brute force in secondi. Anche via orientazioni acicliche.
- **B. $Q_4$ esatto**: $16!$ troppo; ma si può fare branch-and-bound sulle orientazioni acicliche / etichettature
  con bound inferiore parziale, oppure ricerca esaustiva sulle orientazioni acicliche modulo simmetria
  (gruppo di $Q_4$ ha ordine $2^4\cdot4!=384$). Alternativa: SA per il valore + prova di minimalità dedicata.
- **C. Ricerca locale (harness discreto)** per $Q_4..Q_9$: stato = permutazione; mosse = scambio di due etichette,
  spostamento di un'etichetta, mosse strutturate (rispettare la simmetria del cubo, es. etichettare per
  sottocubi ricorsivamente); punteggio = $-\#$cammini (intero esatto). È IL caso d'uso del harness (obiettivo
  discreto). Rischio: minimi locali ⇒ molti seed, riavvii, mosse grandi.
- **D. Costruzioni ricorsive**: $Q_d=Q_{d-1}\square K_2$; etichettare una copia con $1..2^{d-1}$ e l'altra sopra?
  Contare l'eccesso in funzione di $d$ e cercare una formula (l'eccesso 64–96 per $d=9$ suggerisce $\sim 2^{d-3}$).
  Confrontare con i valori esatti di $Q_3,Q_4$.
- **E. Bound inferiori migliori**: raffinare $p(v)\ge\max(1,\deg^-(v))$ con un'analisi dei vertici a
  $\deg^-\ge2$ i cui predecessori hanno $\deg^-\ge2$; oppure LP/ILP sul DAG; oppure prova computer-assisted per C6
  (dubbio: $Q_9$ ha 512 vertici, lo spazio è enorme; serve un argomento strutturale, non una enumerazione).
- **F. Letteratura**: cercare "uphill paths hypercube", generalizzazioni di IMO 2022 P6 (es. arXiv 2023–2026),
  OEIS per la sequenza $U(Q_d)$.

## Priorità
C1 (esatto, quasi gratis) → C2–C4 con harness discreto + costruzione ricorsiva → C5 solo se la costruzione
scala a $\le2399$ (upper bound è la via più realistica; il lower bound $\ge2369$ è "unpublished" e difficile).
