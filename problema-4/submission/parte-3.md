# Problema 4 — Parte 3 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 3 (C3) — Every $k$ up to 8

**Punteggio:** 3 points · **Valutazione:** Judged

A first range of sizes: after C1 and C2, the sizes $k = 5, 6, 7$ and $8$ remain. Prove the statement for every
$k \le 8$.

**Cosa consegniamo.** Riduzione dimostrata a un insieme finito: in un controesempio di taglia $k$ si può supporre che ogni modulo divida $L_k=\mathrm{lcm}(2,\dots,k-1)$; certificato di esaustività non completato.

## 2. Dimostrazione
**Lemma di riduzione (dimostrato).** Siano $g_{ij}=\gcd(m_i,m_j)$ e $m_i'=\mathrm{lcm}_{j\ne i}g_{ij}$. Allora $m_i'\mid m_i$, $\gcd(m_i',m_j')=g_{ij}$ (è diviso da $g_{ij}$ e divide $\gcd(m_i,m_j)$), e le classi $a_i \pmod{m_i'}$ restano a due a due disgiunte per il criterio $(*)$, che dipende solo da $g_{ij}$ e da $a_i-a_j\bmod g_{ij}$. In un controesempio ogni $g_{ij}\le k-1$, quindi $m_i'\mid L_k$: l'insieme dei moduli è finito. Vale anche $\sum1/m_i\le1$. **Ricerca (impostata):** moduli = multinsiemi di $k$ divisori di $L_k$ con gcd a coppie in $[2,k-1]$, ciascuno uguale al lcm dei propri gcd; residui = CSP con vincoli $a_i\not\equiv a_j\pmod{g_{ij}}$, normalizzazione $a_1=0$; seconda implementazione per enumerazione delle famiglie di gcd ammissibili. Il Researcher (run `runs/p4_c3`) ha prodotto un tentativo, in valutazione.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- Researcher attempt_001, code_1 (python, exact): Implementation 1 (certificate): exhaustive enumeration of all k-cliques in G_k on the 1343 classes (a,m), m|420, m>=2; n
- Researcher attempt_001, code_2 (python, exact): Implementation 2 (independent cross-check, different method): enumerate non-decreasing k-tuples of moduli dividing 420 w

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); solo abstract letto.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); solo abstract letto.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); solo abstract letto.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); solo abstract letto.
Fornal–Sun [2607.24655] (2026) trattano il regime asintotico con un grafo dei gcd: stesso oggetto della nostra riduzione; i casi $k\le8$ non vi compaiono.

## 5. Limiti e parti irrisolte
Esecuzione certificata (conteggi, tempi, rerun, sopravvissuti) per $k=5,\dots,8$.
