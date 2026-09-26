# Problema 2 — Parte 6 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 6 (C6) — $U(Q_9)$

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

The same cube, settled completely. Determine $U(Q_9)$ exactly, with proof of both bounds.

*(Fine del problema 2. Punteggi: 1+2+3+5+8+13 = 32.)*

**Cosa consegniamo.** Problema aperto. Nessun contributo oltre la parte 5.

## 2. Dimostrazione
Vedi parte 5: il valore esatto richiede entrambi i bound; per il bound inferiore l'identità dell'eccesso $T=|E|+v+X$ (parte 2) è lo strumento, ma l'analisi dei casi non scala a 512 vertici senza un argomento strutturale.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- `problema-2/certificati/costruzione_88.py`
- `problema-2/certificati/q3_esaustivo.py`
- `problema-2/certificati/q3_verifica_indipendente.py`
- `problema-2/certificati/q4_branch_and_bound.py`
- `problema-2/certificati/q4_ricerca_locale.py`
- `problema-2/certificati/q4_verifica_etichettatura_indipendente.py`
- `problema-2/certificati/q5_stella_verifica_indipendente.py`
- `problema-2/certificati/verifica_dfs_88.py`
- `problema-2/certificati/verifica_etichettatura_q3.py`
- `problema-2/certificati/verifica_etichettatura_q4.py`
- `problema-2/certificati/verifica_q5_bipartita.py`
- `problema-2/certificati/verifica_q5_indipendenti.py`
- `problema-2/esperimenti/conta_cammini.py`
- `problema-2/esperimenti/costruzione_stelle.py`
- `problema-2/esperimenti/ricottura_controllo.py`

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:1412.3893v1 — The competition between simple and complex evolutionary trajectories in asexual populations (Ian E. Ochs, Michael M. Desai, 2014); solo abstract letto.
Nessuna.

## 5. Limiti e parti irrisolte
Tutto.
