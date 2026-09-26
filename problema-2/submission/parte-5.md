# Problema 2 — Parte 5 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 5 (C5) — Bounds for $U(Q_9)$

**Punteggio:** 8 points · **Valutazione:** Judged

$Q_9$ has $512$ vertices and $2304$ edges. The best bounds known to the organisers are
$$
2368 \le U(Q_9) \le 2400;
$$
the lower bound is unpublished. Improve either one: prove that $U(Q_9) \ge 2369$, or exhibit a labelling of $Q_9$
with at most $2399$ uphill paths.

**Cosa consegniamo.** Nessun miglioramento dei bound noti. Contributo: la costruzione a stelle con un codice pari a distanza 4 di taglia 20 dà esattamente il bound superiore noto; dimostrazione che dentro questa famiglia non si può scendere.

## 2. Dimostrazione
Costruzione a stelle (vedi parte 3): totale $=(d+1)2^{d-1}-(d-1)|R|$ con $R$ codice pari a distanza 4. Per $d=9$, $|R|\le A(8,3)=20$ e il totale minimo della famiglia è $2560-160=2400$, cioè il bound superiore degli organizzatori. Quindi il bound noto è (con ogni probabilità) proprio questa costruzione, e migliorarlo richiede una foresta di non-picchi non a stelle (alberi più grandi, che riducano il numero di componenti sotto 96). Impostato: cercare insiemi indipendenti $P$ di $Q_9$ con $|P|<236$ e complemento aciclico; non eseguito.

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
Nessun lavoro arXiv sui cammini in salita sull'ipercubo: il problema risulta inedito.

## 5. Limiti e parti irrisolte
Sia il bound inferiore sia quello superiore.
