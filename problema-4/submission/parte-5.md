# Problema 4 — Parte 5 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 5 (C5) — The certified boundary

**Punteggio:** 8 points · **Valutazione:** Judged

The main certification cell: an initial range of sizes as long as you can make it, plus two isolated sizes
further out. Determine the largest $k$ for which you can certify the statement for all sizes up to and including
$k$, and certify it. The range you claim must be contiguous, and if your argument at a given size assumes that
all smaller sizes have already been settled you must say so. Then decide the two isolated sizes $k = 24$ and
$k = 30$: show that neither is the least size at which the statement can fail.

For this cell the exhaustiveness certificate of the hand-in rules is not enough on its own. Add:

(i) a demonstration that your method is not vacuous. Construct a case in which an admissible configuration
genuinely exists, run your machinery on it unmodified, and show it returns that configuration. A method that
reports "nothing survives" at every size it is pointed at is indistinguishable from a method with a bug, and will
be graded as one;

(ii) for every object your pruning leaves undecided, at every $k$ you claim — not a sample — an individual
decision, plus the smallest part of that object which already forces the decision, plus a proof that no smaller
part does;

(iii) the exact list, not merely the count, of what survives at each $k$;

(iv) every pruning rule you use beyond those you have proved, proved. If your search needs a rule you invented
to finish a size, that rule is part of your claim: state it, prove it, and show the survivor list is unchanged
when you switch it off. A size that only closes with an unproved rule is not certified;

(v) a second implementation, written independently of your first, that differs in method — not the same
algorithm twice — and the two survivor lists compared elementwise at every $k$ you claim. Report any difference
rather than reconciling it silently: a disagreement means one of them is wrong, and finding which is part of the
cell.

**Cosa consegniamo.** Nessun certificato. Osservazione: per $k=24,30$ la forza bruta su $L_k$ è impraticabile; serve un argomento di riduzione di taglia (se un controesempio esiste a $k$, ne esiste uno a un $k'<k$).

## 2. Dimostrazione
Non sviluppato.

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
Tutto.
