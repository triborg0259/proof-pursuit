# Problema 1 — note di triage

## Definizioni (estratte dal testo ricevuto)
- $N$ rette $\ell_1,\ldots,\ell_N$ in $\mathbb{R}^2$ (parte 1; il preambolo menziona un $d$ generale,
  quindi le parti successive riguarderanno presumibilmente $\mathbb{R}^d$).
- **Definizione ufficiale (preambolo ricevuto):** rette per l'origine di $\mathbb{R}^d$, ripetizioni ammesse;
  $\theta(\ell,\ell')=\arccos|\langle x,x'\rangle|\in[0,\pi/2]$ con $x,x'$ versori;
  $S=\sum_{i<j}\theta(\ell_i,\ell_j)$. **Coincide con l'ipotesi di lavoro usata in E1 e nell'approccio E.**
- Congettura di Fejes Tóth (1959): $S$ massima con $d$ rette ortogonali usate $\lfloor N/d\rfloor$ o $\lceil N/d\rceil$ volte.
  Per $N=d+k$, $0\le k\le d$: valore $\big(\binom{N}{2}-k\big)\frac{\pi}{2}$.
- Il problema (nome ufficiale "Angles between lines") è esplicitamente il problema di Fejes Tóth.

## Richieste per parte
| Parte | Richiesta | Punti | Tipo |
|---|---|---|---|
| 1 | Dimostrare $S \le \frac{\pi}{2}\lfloor N^2/4\rfloor$ per rette in $\mathbb{R}^2$ | 1 | Judged (prova) |
| 2 | Lemma di ortogonalità: catena $x_1..x_m$ di versori in $\mathbb{R}^{m-1}$, $x_i\perp x_j$ per $|i-j|\ge2$ ⇒ $\sum_{i=1}^{m-1}\theta(x_i,x_{i+1})\le(m-2)\frac{\pi}{2}$ | 2 | Judged (prova) |
| 3 | $N=d+1$ in $\mathbb{R}^d$, $d\ge1$: $S\le(\binom{d+1}{2}-1)\frac{\pi}{2}$ | 3 | Judged (prova) |
| 4 | $5$ rette in $\mathbb{R}^3$: $S\le4\pi$; $6$ rette in $\mathbb{R}^4$: $S\le13\pi/2$ | 5 | Judged (prova; calcolo rigoroso ammesso) |
| 5 | $N=d+2$ in $\mathbb{R}^d$, $d\ge2$: $S\le(\binom{d+2}{2}-2)\frac{\pi}{2}$ | 8 | Judged (prova) |
| 6 | Congettura completa (prove or disprove); famiglie infinite nuove = progresso parziale | 13 | Judged · Open |

**Requisiti di consegna (preambolo):** prova scritta per ogni cella tentata. Computer ammesso per esplorare;
una prova può dipendere da un calcolo solo se: codice incluso, < 10 minuti su portatile, rigoroso (aritmetica
esatta o a intervalli, oppure errore numerico limitato con argomento). Dichiarare quali celle sono risolte
e quali parziali. Citare un risultato pubblicato per l'enunciato richiesto NON conta.

## Ambiguità / dati mancanti
1. ~~Definizione di $S$ assente~~ → risolta dal preambolo.
2. ~~Rette coincidenti~~ → ripetizioni esplicitamente ammesse (angolo 0). La prova deve gestirle.
3. "Conjectured optimum": in $d=2$ la disuguaglianza è da dimostrare; la congettura aperta riguarda $d\ge3$.
4. Parte 3 con $d=1$: due rette in $\mathbb{R}^1$ coincidono, $S=0=(1-1)\pi/2$. Banale ma va incluso.
5. Parte 6: "disprove" ammesso ⇒ una ricerca di controesempi (numerica poi esatta) è legittima. Parti 3–5
   invece chiedono prove: se la ricerca numerica trovasse un controesempio a una di esse, la cella sarebbe
   mal posta; improbabile ma va tenuto a mente.
6. Parte 4 ammette esplicitamente calcolo rigoroso (aritmetica esatta/a intervalli, < 10 min): unica cella
   dove un approccio computer-assisted (branch-and-bound) è una strada concreta.

## Contesto — letteratura (vedi fonti/README.md per i dettagli)
**Letto [BM18] Bilyk–Matzke 2018/2019.** Convenzione: loro $S^d$ = nostro $\mathbb{R}^{d+1}$. Dichiarano: unico
caso risolto = piano (Fodor–Vígh–Zarnócz 2016; BM18 danno tre prove alternative, una — "Stolarsky per quadranti" —
coincide in sostanza col nostro approccio E); $\mathbb{R}^3$ con $N\le6$ confermato da Fejes Tóth 1959 (copre
"5 rette in $\mathbb{R}^3$" di P4); bound generale $\frac{\pi}{2}-\frac{69}{50(d+1)}$ (energia continua);
Prop. 3.1: congettura in dim. alta ⇒ dim. bassa. **Conseguenza:** P3, P5, P6 e "6 in $\mathbb{R}^4$" non risultano
noti (al 2018): il lemma P2 suggerisce che gli autori della gara abbiano in mente una via elementare per P3.
Da controllare: Lim–McCann (2020, non letto) e lavori 2019–2026.

## Contesto (precedente, mantenuto per storico)
Confermato dal preambolo: è il problema di L. Fejes Tóth (1959). Letteratura candidata da controllare prima
di citarla (utile per capire quali casi speciali sono noti e con quali tecniche, NON per sostituire prove):
- L. Fejes Tóth, 1959 (articolo originale, in tedesco, probabilmente su Acta Math. Acad. Sci. Hungar.).
- D. Bilyk, R. Matzke, "On the Fejes Tóth problem about the sum of angles between lines", Proc. AMS (~2019):
  risultati parziali in $d\ge3$ (da verificare: forse il caso $N=d+1$? e un bound generale via energia).
- Possibili lavori successivi (Bilyk–Glazyrin–Matzke–Park–Vlasiuk? Fodor–Vígh–Zarnócz?) — da verificare.
**Non citare finché non verificati.** Per le celle la citazione comunque non vale come prova.

## Approcci plausibili per la parte 1 (sotto l'ipotesi di lavoro su $S$)
- **A. Ordinamento angolare + accoppiamento.** Parametrizzare le rette con direzioni $\theta_i\in[0,\pi)$.
  Per ogni retta $\ell_i$ e ogni retta $\ell_j$, l'angolo $\angle(\ell_i,\ell_j)\le\pi/2$ e vale
  $\angle(\ell_i,\ell_j)+\angle(\ell_i,\ell_j^\perp)=\pi/2$ dove $\ell_j^\perp$ è la perpendicolare.
  Idea: mostrare che per ogni coppia di rette $\ell_j,\ell_k$ vale, per ogni $\ell_i$,
  $\angle(\ell_i,\ell_j)+\angle(\ell_i,\ell_k)\le \pi/2 + \angle(\ell_j,\ell_k)$?? (da verificare: potrebbe
  essere falso; controllare su esempi).
- **B. Argomento alla Turán/bipartizione.** Definire il grafo delle coppie con angolo "grande" e mostrare
  che un vincolo geometrico (es. tre rette a due a due con angolo $>\pi/3$ è impossibile in $\mathbb{R}^2$…
  falso in generale, da controllare) limita la somma. Più promettente: disuguaglianza per triple.
  Per tre rette in $\mathbb{R}^2$ con angoli a due a due $a,b,c\in[0,\pi/2]$: si ha
  $a+b+c\le\pi$ (le tre direzioni in $[0,\pi)$; il massimo è $\pi$ con angoli $\pi/3$). Sommando su tutte le
  triple: $(N-2)\,S\le\pi\binom{N}{3}$ ⇒ $S\le \pi N(N-1)/6$, che è più debole di $\frac{\pi}{2}\lfloor N^2/4\rfloor \approx \pi N^2/8$.
  Serve quindi un'idea più fine (es. induzione rimuovendo una coppia di rette perpendicolari o quasi).
- **C. Induzione su $N$ togliendo due rette.** Se esistono due rette $\ell_a,\ell_b$ con angolo $\phi$,
  per ogni altra $\ell_i$: $\angle(\ell_i,\ell_a)+\angle(\ell_i,\ell_b)\le \pi/2 + $ (qualcosa)? Se si scelgono
  $\ell_a,\ell_b$ opportune (es. le due con angolo massimo) e si mostra
  $\angle(\ell_i,\ell_a)+\angle(\ell_i,\ell_b)\le\pi/2+\phi'$ con termini che si compensano, si ottiene
  $S(N)\le S(N-2)+\frac{\pi}{2}(N-2)+\frac{\pi}{2}$, e $\lfloor N^2/4\rfloor=\lfloor (N-2)^2/4\rfloor+N-1$ chiude
  l'induzione. Da verificare con cura: questo schema è il candidato principale.
- **E. Argomento integrale-geometrico (Crofton) — CANDIDATO PRINCIPALE, prova completa abbozzata.**
  Direzioni $\theta_i\in[0,\pi)$. Per $\psi$ uniforme in $[0,\pi)$ sia $A_\psi=\{\theta: (\theta-\psi)\bmod\pi\in[0,\pi/2)\}$
  (un "semifascio" di direzioni). Fatto chiave (da verificare con cura, incluso il caso $\theta_i=\theta_j$):
  $$\Pr\big[\text{esattamente una fra }\theta_i,\theta_j\text{ sta in }A_\psi\big] = \frac{2}{\pi}\,\angle(\ell_i,\ell_j).$$
  Equivalente: con la mappa $\theta\mapsto 2\theta$ le rette diventano punti sulla circonferenza, l'angolo fra rette
  diventa metà della distanza geodetica, e un diametro casuale separa due punti con probabilità (distanza)/$\pi$.
  Allora, detto $k_\psi=|\{i:\theta_i\in A_\psi\}|$,
  $$S=\frac{\pi}{2}\,\mathbb{E}\big[k_\psi (N-k_\psi)\big]\le \frac{\pi}{2}\left\lfloor\frac{N^2}{4}\right\rfloor,$$
  perché $k(N-k)\le\lfloor N^2/4\rfloor$ per ogni intero $k$. Uguaglianza sse per quasi ogni $\psi$ il taglio è
  bilanciato ($k_\psi\in\{\lfloor N/2\rfloor,\lceil N/2\rceil\}$): spiega i massimizzatori "piatti" visti in E1.
  Gestisce rette parallele/coincidenti (mai separate, angolo 0). Nessuna citazione necessaria: è autocontenuto.
  Da fare: (1) dimostrare il fatto chiave con un calcolo esplicito di misura; (2) scrivere la prova completa;
  (3) revisione critica; (4) bozza di submission.
- **D. Verifica numerica su piccoli $N$** (solo come sanity check, non prova): ottimizzazione casuale /
  griglia su $N\le 8$ per confermare che il massimo è $\frac{\pi}{2}\lfloor N^2/4\rfloor$ sotto l'ipotesi su $S$.

## Parte 2 — triage

**Affermazione da stabilire.** Se $m\ge2$, $x_1,\dots,x_m$ versori in $\mathbb{R}^{m-1}$ con $x_i\perp x_j$ per $|i-j|\ge2$,
allora $\sum_{i=1}^{m-1}\theta(x_i,x_{i+1})\le(m-2)\pi/2$. Equivalente: la somma dei "deficit"
$\sum_i(\pi/2-\theta_i)\ge\pi/2$. Intuizione: se tutti gli angoli consecutivi fossero $\pi/2$ i vettori sarebbero
$m$ versori ortogonali in $\mathbb{R}^{m-1}$, impossibile; il lemma quantifica di quanto si deve deviare.

**Casi piccoli.** $m=2$: $x_2=\pm x_1$ in $\mathbb{R}^1$, somma $0\le0$. $m=3$: in $\mathbb{R}^2$, $x_3=\pm x_1^\perp$,
quindi $\theta_1+\theta_2=\theta_1+(\pi/2-\theta_1)=\pi/2$: **uguaglianza sempre**. Con $c_i=\langle x_i,x_{i+1}\rangle=\sin\alpha_i$
il determinante di Gram (tridiagonale) è $D_3=\cos(\alpha_1+\alpha_2)\cos(\alpha_1-\alpha_2)$, coerente.

**Approccio F — induzione su $m$ per proiezione (CANDIDATO PRINCIPALE, prova completa abbozzata).**
Passo $m-1\to m$ ($m\ge3$). Sia $U=x_m^\perp\cong\mathbb{R}^{m-2}$. I vettori $x_1,\dots,x_{m-2}$ stanno in $U$.
- Se $x_{m-1}\ne\pm x_m$: sia $y$ il versore di $x_{m-1}-\langle x_{m-1},x_m\rangle x_m\in U$. Allora $y\perp x_j$ per $j\le m-3$,
  quindi $x_1,\dots,x_{m-2},y$ è una catena di $m-1$ versori in $U\cong\mathbb{R}^{m-2}$: per ipotesi induttiva
  $\sum_{i\le m-3}\theta_i+\theta(x_{m-2},y)\le(m-3)\pi/2$.
  Scrivendo $x_{m-1}=\sin\varphi\, y+\cos\varphi\, x_m$ (a meno di segni) con $\varphi=\theta(x_{m-1},x_m)$ e usando $x_{m-2}\perp x_m$:
  $|\langle x_{m-2},x_{m-1}\rangle|=\sin\varphi\cos\psi$ con $\psi=\theta(x_{m-2},y)$. Posto $\beta=\pi/2-\varphi$:
  $\theta_{m-2}=\arccos(\cos\beta\cos\psi)\le\beta+\psi$ (perché $\cos(\beta+\psi)\le\cos\beta\cos\psi$ e $\beta+\psi\le\pi$;
  è la disuguaglianza triangolare sferica per il triangolo rettangolo). Quindi
  $\theta_{m-2}+\theta_{m-1}\le\psi+\beta+\varphi=\psi+\pi/2$, e sommando: $\sum\theta_i\le(m-3)\pi/2+\pi/2=(m-2)\pi/2$.
- Se $x_{m-1}=\pm x_m$: allora $\theta_{m-1}=0$ e $\theta_{m-2}=\pi/2$ (poiché $x_{m-2}\perp x_m$). Si sceglie un versore
  $y\in U$ ortogonale a $x_1,\dots,x_{m-3}$ (esiste: $\dim U=m-2>m-3$), si applica l'ipotesi induttiva alla catena
  $x_1,\dots,x_{m-2},y$ e si usa $\theta_{m-2}+\theta_{m-1}=\pi/2\le\theta(x_{m-2},y)+\pi/2$.
Base $m=2$: somma $0$. **Da fare:** scrivere la prova completa con i segni espliciti, revisione critica, bozza.

**Approccio G (alternativo, di riserva).** Gram tridiagonale $G$ con $1$ sulla diagonale e $c_i$ fuori: $\det G=0$
(rango $\le m-1$). Mostrare che $\sum\arcsin|c_i|<\pi/2\Rightarrow G$ definita positiva tramite i continuanti
$D_k=D_{k-1}-c_{k-1}^2D_{k-2}$. Non sviluppato; F è più diretto.

**Collegamento probabile con le parti successive.** Il lemma quantifica un deficit totale $\ge\pi/2$ lungo una
catena: plausibilmente serve per il caso $N=d+1$ (bound $(\binom{N}{2}-1)\pi/2$, cioè deficit totale $\ge\pi/2$).

## Parti 3–6 — triage

**Struttura comune.** Deficit $\delta_{ij}=\pi/2-\theta_{ij}=\arcsin|\langle x_i,x_j\rangle|$. Le tesi diventano:
- P3: $d+1$ versori in $\mathbb{R}^d$ ⇒ $\sum_{i<j}\delta_{ij}\ge\pi/2$.
- P5: $d+2$ versori in $\mathbb{R}^d$ ⇒ $\sum\delta_{ij}\ge\pi$. P4 = P5 per $(d,N)=(3,5),(4,6)$.
- P6: $N$ versori in $\mathbb{R}^d$ ⇒ $\sum\delta_{ij}\ge M(N,d)\,\pi/2$.
Sanity check dei valori: P4: $(10-2)\pi/2=4\pi$ ✓, $(15-2)\pi/2=13\pi/2$ ✓.

**Parte 3 (3 pt).** Il lemma della parte 2 è chiaramente il mattone: dà deficit $\ge\pi/2$ per una catena.
Ostacolo: $d+1$ versori generici non formano una catena. Idee:
- (a) Riduzione a catena: da una dipendenza lineare minimale $\sum a_ix_i=0$ (circuito, $m\le d+1$ vettori in
  posizione generale di dimensione $m-1$) costruire una catena $y_1..y_m$ con $\theta(y_i,y_{i+1})$ legata alle
  $\theta(x_i,x_j)$ (es. proiezioni successive / sottospazi $\mathrm{span}(x_1..x_k)$). Da esplorare.
- (b) Induzione diretta su $d$ per proiezione su $x_{d+1}^\perp$ (come in F): la disuguaglianza triangolare
  sferica dà solo $\delta_{ij}\ge\delta(y_i,y_j)-\delta_i-\delta_j$, che sommata perde un fattore $(d-2)\sum_i\delta_i$.
  **Non basta così**; serve una scelta migliore del vettore su cui proiettare o una stima più fine.
- (c) Letteratura: verificare se $N=d+1$ è già dimostrato (Fodor–Vígh–Zarnócz 2016? Bilyk–Matzke 2019?) e con
  quale tecnica; la prova va comunque riscritta in modo autonomo.
- (d) Sanity check numerico con il harness: $d=3..6$, $N=d+1$.

**Parte 4 (5 pt).** Due istanze concrete di $d+2$. Strade: (i) dedurle da un argomento generale (P5);
(ii) prova computer-assisted: massimizzazione di $S$ su $(S^2)^5$ e $(S^3)^6$ con branch-and-bound a intervalli.
Difficoltà: il massimo è in punti "a spigolo" (coppie ortogonali/coincidenti) e la funzione non è liscia lì;
serve un argomento locale attorno agli ottimi + copertura rigorosa del resto. Dimensione: $5\cdot2-3=7$ e
$6\cdot3-6=12$ parametri dopo le simmetrie: il caso $\mathbb{R}^4$ è pesante per il limite di 10 minuti.
Prima esplorare (i).

**Parte 5 (8 pt).** Generalizzazione di P3 con deficit $\ge\pi$. Se P3 si fa con una riduzione strutturale,
tentare di iterarla (due "circuiti" indipendenti?). Da aprire solo dopo P3.

**Parte 6 (13 pt, aperta).** Nessuna prova attesa. Contributi parziali realistici: (i) ricerca numerica sistematica
di controesempi per $N\le 2d$, $d\le 6$ (harness); (ii) una famiglia infinita nuova (es. $N=d+3$? o $N=2d$?)
solo se emerge un metodo da P3/P5. Punteggio alto ma probabilità bassa: budget limitato.

## Esperimenti
- E1 (esperimenti/README.md): hill climbing su $N=2..10$, massimo numerico = target entro $2\cdot10^{-5}$,
  nessun superamento. Massimizzatori non unici (insieme piatto).

## Stato
Parte 1: approccio E promettente, prova da scrivere e revisionare.
Parte 2: approccio F, prova abbozzata per induzione, da scrivere e revisionare.
Parti 3–6: solo triage. Ordine naturale: 1 → 2 → 3 → (5 → 4) → 6. In attesa delle parti 2–6 e della
definizione ufficiale di $S$ (se diversa dall'ipotesi, l'approccio E va riadattato).

## Letteratura arXiv (ricerca deterministica 2026-09-26)
- [1801.07837] Bilyk–Matzke (letto integralmente, vedi fonti/README.md). [2007.08698] T. Lim, R. McCann (2020), abstract:
  immergono la congettura in una famiglia a un parametro $\alpha$ (potenze degli angoli rinormalizzati); congettura
  equivalente all'unicità dell'ottimizzatore per ogni $\alpha>1$; dimostrano ottimalità e unicità per $\alpha=\infty$.
  Non dà i casi $N=d+1$, $d+2$ (P3–P5): restano non coperti in letteratura, coerente con BM18.
