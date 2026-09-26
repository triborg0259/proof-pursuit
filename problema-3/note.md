# Problema 3 — note di triage

## Definizioni
- Partizione $\lambda$ di $n$; shift $B$: togli 1 da ogni parte, scarta le nulle, aggiungi una parte $=s$ (numero di parti).
- Cyclic: $B^i(\lambda)=\lambda$ per qualche $i\ge1$. $d_B(\lambda)$ = passi per entrare in un ciclo; $D_B(n)=\max_\lambda d_B$.
- $T_k=k(k+1)/2$, $\delta_k=(k,\dots,1)$, rango $k$ di $n$: $T_{k-1}<n\le T_k$.
- Esempio dato: $d_B((2,1,1,1,1))=3$ (verificabile a mano: coerente con la definizione).

## Richieste per parte
| Parte | Richiesta | Punti |
|---|---|---|
| C1 | $n=T_k$: tutti convergono a $\delta_k$, unica ciclica. $n=T_{k-1}+r$: tutte le partizioni cicliche + numero di cicli. Prove. | 1 |
| C2 | $D_B(T_k)$ esatto per ogni $k$, entrambi i bound | 2 |
| C3 | $k\ge4$, $n$ non triangolare di rango $k$: $D_B(n)\le k^2-2k-1$; $D_B(T_k-1)$ esatto + partizioni estremali | 3 |
| C4 | $D_B(T_{k-1}+1)$ per $k\ge5$, entrambi i bound | 5 |
| C5 | $D_B(T_{k-1}+2)$ per ogni $k$: formula + range di validità + valori residui; upper bound con UN argomento uniforme; estremali esplicite in $k$; discussione di dove si ferma l'estensione dell'argomento C3 | 8 |
| C6 | $D_B(n)$ per ogni $n$ (aperto) | 13 |

**Consegna:** prove scritte. Calcolo ammesso solo se esaustivo su un insieme finito a cui l'argomento riduce il
problema (< 10 min, codice incluso). Valori come formule in $k$; partizioni estremali esplicite in $k$.
Citazione non vale; una prova scritta per esteso sì, "whatever its source" (⇒ possiamo riprodurre prove note
per esteso, dichiarando la fonte).

## Ambiguità / dati mancanti
1. C1: "number of distinct cycles" — atteso un conteggio in funzione di $(k,r)$; chiarire se conta anche
   i cicli di lunghezza 1 (sì, un punto fisso è un ciclo).
2. C3: "for that $n$" = $n=T_k-1$. Partizioni estremali: quelle con $d_B=D_B$.
3. C5: "for every $k$" ma $k=2$ dà $n=3$, $k=3$ dà $n=5$: casi piccoli con comportamento anomalo; il testo chiede
   di dichiarare il range e i valori residui separatamente.
4. C6: "Open question" — ma per C6 non è chiaro se esista una congettura formulata; da cercare in letteratura.

## Contesto — letteratura (DA VERIFICARE prima di citare; ricordi, non letture)
- Brandt (1982): per $n=T_k$ convergenza a $\delta_k$; per $n$ generico caratterizzazione dei cicli.
- Igusa (1985), Etienne (1991): $D_B(T_k)=k(k-1)$ (bound $k^2-k$ raggiunto).
- Griggs–Ho (1998) "The cycling of partitions and compositions under repeated shifts": bound generale e congetture
  su $D_B(n)$ per $n$ non triangolare; potrebbe contenere proprio $k^2-2k-1$ e valori per $T_k-1$.
- Drensky (2015?) survey "The Bulgarian solitaire and the mathematics around it".
- Hopkins–Jones, Hopkins–Sellers (cicli, Gardner, "necklaces").
Il problema sembra costruito su Griggs–Ho: C3 = loro teorema?, C4/C5 = famiglie forse parzialmente aperte, C6 = congettura.

## Approcci
- **C1.** Struttura nota: rappresentare $\lambda$ come diagramma e $B$ come "spostamento sulla diagonale". Cicliche
  di $n=T_{k-1}+r$: $\delta_{k-1}$ più $r$ "carte extra" su $r$ delle $k$ posizioni $0..k-1$ (posizione 0 = nuova
  parte 1). $B$ agisce su queste come rotazione ciclica dell'indicatore in $\mathbb{Z}_k$ ⇒ cicli = collane binarie
  con $k$ perle e $r$ nere: $\frac1k\sum_{d\mid\gcd(k,r)}\varphi(d)\binom{k/d}{r/d}$. **Da dimostrare per esteso**
  (che ogni partizione entra in questo insieme e che nessun'altra è ciclica): argomento standard con la
  "somma degli scarti dalla scala" che decresce.
- **C2.** $D_B(T_k)=k^2-k$: costruzione (es. $(T_k)$ o $(k-1,k-1,\dots)$? da calcolare) + bound superiore (argomento
  di Igusa/Etienne, da riscrivere). Calcolo esatto per $k\le 9$ per confermare.
- **C3–C5.** Calcolare $D_B(n)$ per ogni $n\le 60$–$70$ ($p(70)\approx4\cdot10^6$, fattibile in Python/C in minuti):
  tabella esatta, estremali, formule congetturali per $T_k-1$, $T_{k-1}+1$, $T_{k-1}+2$. Poi prove: la struttura
  "potenziale" (distanza dalla scala) dà upper bound; le estremali danno lower bound.
- **C6.** Tabella completa + congettura; non attesa una prova.

## Esperimento E1 (da fare per primo, ~minuti): $D_B(n)$ esatto per $n\le 60$
Grafo funzionale sulle partizioni; $d_B$ via ricerca dei cicli (Floyd/marcatura); registrare per ogni $n$:
$D_B(n)$, numero di cicli, partizioni estremali. Interi esatti: nessun problema numerico.
Verifica indipendente: due implementazioni (una su partizioni come tuple, una su "diagramma/insieme di carte
in posizione") per C-cell che richiedono calcolo esaustivo.

## Letteratura arXiv (ricerca deterministica 2026-09-26, abstract letti)
- [1503.00885] V. Drensky, "The Bulgarian solitaire and the mathematics around it" (2015): survey storico; conferma la
  convergenza a $\delta_k$ per $n=T_k$. [2607.17194] R. Meštrović, survey (2026): cita Brandt 1982 per la
  caratterizzazione delle partizioni cicliche (nostra C1). Da leggere per le fonti di $D_B$ (Igusa, Etienne, Griggs–Ho).
- Rumore scartato: [math/0401385] random Bulgarian solitaire, [1101.1546] prova di Toom, [1703.07102], [2208.14496].
