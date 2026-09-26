# Problema 4 — Parte 4 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 4 (C4) — Every $k$ up to 12

**Punteggio:** 5 points · **Valutazione:** Judged

A longer range, and a precise account of your method at the sizes just beyond it. Prove the statement for every
$k \le 12$. Then, for each $k$ from $9$ to $16$ in turn, report exactly what your method leaves undecided at that
$k$: if nothing, say so and prove it; if something, exhibit it in full. If that disagrees with any source you
consulted, say which of the two is right and why. An answer that reports agreement with a source it did not test
will be marked wrong.

**Cosa consegniamo.** Come parte 3, esteso a $k\le12$ ($L_{12}=27720$, 96 divisori); non eseguito.

## 2. Dimostrazione
Stessa riduzione e stesso schema di ricerca; il rapporto sui casi $9\le k\le16$ richiede di elencare i sopravvissuti alla potatura senza deciderli con regole non dimostrate.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- Nessun codice ancora.

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); solo abstract letto.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); solo abstract letto.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); solo abstract letto.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); solo abstract letto.
Come parte 3.

## 5. Limiti e parti irrisolte
Tutto tranne la riduzione.
