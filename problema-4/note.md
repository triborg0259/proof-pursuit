# Problema 4 — note di triage

## Definizioni
- Classi $a_i \pmod{m_i}$ a due a due disgiunte $\iff \gcd(m_i,m_j)\nmid a_i-a_j$ per ogni $i<j$ (CRT, dato come $(*)$).
- Tesi$(k)$: ogni famiglia disgiunta di $k$ classi ha una coppia con $\gcd(m_i,m_j)\ge k$. Sharp: $1..k \pmod k$.
- Banali (non valgono nulla): ogni gcd $\ge2$; $\sum 1/m_i\le1$ ⇒ qualche $m_i\ge k$.
- Controesempio a Tesi$(k)$ := famiglia disgiunta con tutti i $\gcd\in[2,k-1]$.

## Richieste per parte
| Parte | Richiesta | Punti |
|---|---|---|
| C1 | Prova per $k=3$ | 1 |
| C2 | Prova per $k=4$ | 2 |
| C3 | Prova per ogni $k\le8$ | 3 |
| C4 | Prova per ogni $k\le12$; per $k=9..16$ report esatto di cosa il metodo lascia indeciso; confronto con fonti **testate** | 5 |
| C5 | Massimo $k$ certificato (range contiguo) + decidere $k=24$ e $k=30$; certificato rafforzato (i)–(v), incluse **due implementazioni indipendenti per metodo** | 8 |
| C6 | (a) decidere un $k\ge25$; (b) asintotica: $\ge ck$ o migliorare il fattore; (c) forma gruppale, $k=6$ | 13 |

**Consegna computazionale (rigidissima):** insieme finito + prova che nulla fuori è controesempio; ogni regola di
pruning dimostrata; conteggio nodi e tempo per ogni $k$; rerun; decisione individuale per ogni sopravvissuto con
"parte minima che forza la decisione" e prova di minimalità. Per C5 anche: test di non-vacuità (il metodo deve
ritrovare una configurazione ammissibile costruita apposta), lista esatta dei sopravvissuti, regole inventate
dimostrate e testate spente, seconda implementazione con metodo diverso e confronto elemento per elemento.

## Ambiguità / dati mancanti
1. Titolo della colonna assente nel testo incollato (irrilevante).
2. "Decide $k=24$ e $k=30$: show that neither is the least size at which the statement can fail": basta mostrare
   che se Tesi fallisce a $k$ allora fallisce anche a un $k'<k$ (riduzione), oppure provare Tesi$(k)$ direttamente.
   Suggerisce che esista un argomento "se c'è un controesempio di taglia $k$ ce n'è uno di taglia minore" per
   certi $k$ (es. $k$ non primo? $k$ con molti divisori?). Da capire.
3. C4: "what your method leaves undecided at $k=9..16$": si aspetta che il metodo lasci sopravvissuti per alcuni
   $k$ oltre 12; onestà richiesta.
4. C6(b): "It is known that ..." — la fonte non è indicata; da identificare (probabilmente Z.-W. Sun, oppure
   lavori su covering systems). Non affidarsi senza verifica.

## Riduzione a insieme finito (idea chiave, DA DIMOSTRARE con cura — è il fondamento di C3–C5)
Sia $g_{ij}=\gcd(m_i,m_j)$. La disgiunzione della coppia $(i,j)$ dipende solo da $g_{ij}$ e da $a_i-a_j \bmod g_{ij}$.
Poniamo $m_i'=\mathrm{lcm}_{j\ne i}\,g_{ij}$. Allora $m_i'\mid m_i$ e $g_{ij}\mid m_i', m_j'$, quindi
$\gcd(m_i',m_j')=g_{ij}$ esattamente (divide $g_{ij}$ perché $m_i'\mid m_i$; è diviso da $g_{ij}$). Le classi
$a_i \pmod{m_i'}$ restano disgiunte. Quindi **WLOG ogni $m_i$ è lcm dei suoi gcd con gli altri**; in un
controesempio ogni $g_{ij}\le k-1$, dunque $m_i\mid L_k:=\mathrm{lcm}(2,\dots,k-1)$: **insieme finito**.
Inoltre $\sum1/m_i\le1$ resta necessario. Conseguenze: primi $>k-1$ irrilevanti; per ogni primo $p$ gli esponenti
sono limitati da $\lfloor\log_p(k-1)\rfloor$.
Spazio: moduli = multiinsiemi di $k$ divisori di $L_k$ con gcd a coppie in $[2,k-1]$ e ogni $m_i$ = lcm dei suoi gcd;
residui: CSP su $\prod \mathbb{Z}_{m_i}$ con vincoli $a_i\not\equiv a_j \pmod{g_{ij}}$; normalizzazione $a_1=0$
e simmetrie (traslazione, permutazioni, automorfismi $x\mapsto ux$ con $u$ invertibile mod $L_k$).
$L_{12}=\mathrm{lcm}(2..11)=27720$ (96 divisori); $L_{24}$ e $L_{30}$ molto più grandi ⇒ per 24/30 servirà la
riduzione dell'ambiguità 2, non forza bruta.

## Approcci
- **C1 ($k=3$) a mano.** Controesempio: gcd tutti $=2$ ⇒ tutti i moduli pari, $a_i$ a due a due di parità
  diversa: impossibile con 3 classi (pigeonhole su $\mathbb{Z}_2$). Fatto. (Prova di 3 righe.)
- **C2 ($k=4$) a mano.** gcd $\in\{2,3\}$. Grafo dei gcd su 4 vertici colorato con 2 e 3; le coppie con gcd 2
  richiedono parità diverse, quelle con gcd 3 residui mod 3 diversi. Se il grafo "gcd=2" ha un triangolo ⇒
  contraddizione; altrimenti... pigeonhole combinato; inoltre struttura: se $2\mid m_i$ e $2\mid m_j$ allora
  $2\mid g_{ij}$, quindi l'insieme dei moduli pari forma una clique in gcd pari; gcd$\in\{2,3\}$ ⇒ clique con gcd
  esattamente 2 ⇒ al massimo 2 moduli pari; analogamente al massimo 2 moduli divisibili per 3; ma ogni modulo ha
  un fattore 2 o 3 (gcd $\ge2$ con qualcuno) — 4 moduli, ognuno pari o multiplo di 3, al più 2 per tipo, e i
  due pari devono avere gcd $\ge2$ con i due multipli di 3 ⇒ pari e multipli di 3 insieme ⇒ contraddizione col
  conteggio. Da scrivere con cura. Questo schema ("clique per primo") potrebbe scalare: per ogni primo $p$, i
  moduli divisibili per $p^e$ formano una clique con $p^e\mid g_{ij}$.
- **C3–C5: ricerca esaustiva certificata** sull'insieme finito sopra, con due implementazioni diverse:
  (1) backtracking sui moduli (divisori di $L_k$) + CSP sui residui con propagazione; (2) approccio per
  "struttura dei primi": costruzione per grafi di gcd + SAT/colorazione, o enumerazione delle famiglie di gcd
  ammissibili $\{g_{ij}\}$ e verifica di realizzabilità. Il vincolo di 10 minuti e i certificati (conteggi,
  survivors, minimal forcing part) rendono C5 costoso ma è la cella da 8 punti più "meccanica" della gara.
- **C6(b) asintotico**: solo se avanza tempo; identificare prima la fonte del bound noto.

## Contesto — letteratura (DA VERIFICARE; ricordi)
- La domanda è nota come congettura di Z.-W. Sun sulle classi (coset) disgiunte (~2004); Sun ha risultati su
  $\max\gcd$ e sulla forma gruppale per $k$ piccoli. Erdős Problems potrebbe averla catalogata. Cercare anche
  "disjoint residue classes gcd of moduli" e lavori 2020–2026 (es. su arXiv) con calcoli certificati.

## Letteratura arXiv (ricerca deterministica 2026-09-26, abstract letti; testo completo NON ancora letto)
- **[2607.24655] J. Fornal, Yu-Chen Sun, "On the problem of large gcd for disjoint residue classes" (lug. 2026).**
  Abstract: per $k$ classi disgiunte $\max\gcd(m_i,m_j)\gg k\exp\!\big(-(2+o(1))\sqrt{\log k/\log\log k}\big)$; metodo: grafo
  completo con archi colorati dai gcd + lemma strutturale + partizione crivellante + inversione di Möbius + DFT.
  **Conseguenza per C6(b):** il bound "noto" citato nell'enunciato ($\exp(-(2+o(1))\log k/\log\log k)$) è già stato
  migliorato (radice quadrata all'esponente). Citare non vale; riprodurre la prova per esteso sì ("whatever its source").
  Via realistica per C6(b): scaricare il paper (shell `full`) e riscrivere la dimostrazione completa, verificandola.
  Il "grafo dei gcd" è la stessa struttura del nostro schema "clique per primo" per C2–C5.
- [1511.04293], [2603.26043] (disjoint covering systems con un modulo ripetuto): contesto, non usati.
