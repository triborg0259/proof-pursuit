# Problema 3 — Parte 2 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 2 (C2) — $D_B$ at triangular $n$

**Punteggio:** 2 points · **Valutazione:** Judged

Next, how long the process can take to reach a cycle, starting with the triangular numbers.
Determine $D_B(T_k)$ for every $k$, with proof of both bounds.

**Cosa consegniamo.** Valore atteso $D_B(T_k)=k^2-k$ (citato: Igusa 1985, Etienne 1991); costruzione e bound superiore da riprodurre per esteso.

## 2. Dimostrazione
Bound inferiore: esibire una partizione di $T_k$ con $d_B=k^2-k$ in funzione di $k$ (candidata: la partizione in una sola parte $(T_k)$ o $(k-1,\dots)$, da confermare col calcolo esatto per $k\le9$). Bound superiore: potenziale che decresce di almeno 1 ogni $k$ mosse dopo una fase iniziale. Non completato.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- Nessun codice ancora.

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:math/0401385v2 — Random Bulgarian solitaire (Serguei Popov, 2004); solo abstract letto.
- arXiv:1503.00885v1 — The Bulgarian solitaire and the mathematics around it (Vesselin Drensky, 2015); solo abstract letto.
- arXiv:2607.17194v1 — A short survey the game Bulgarian solitaire and related games (Romeo Meštrović, 2026); solo abstract letto.
- arXiv:1101.1546v3 — Revisiting Toom's proof of Bulgarian Solitaire (Therese A. Hart, Gabriel Khan, Mizan R. Khan, 2011); solo abstract letto.
- arXiv:1703.07102v1 — An exponential limit shape of random $q$-proportion Bulgarian solitaire (Kimmo Eriksson, Markus Jonsson abd Jonas Sjöstrand, 2017); solo abstract letto.
- arXiv:2208.14496v1 — Limiting behavior in growth of Bulgarian Solitaire orbits (Nhung Pham, 2022); solo abstract letto.
Igusa (1985), Etienne (1991): $D_B(T_k)=k(k-1)$; survey [1503.00885], [2607.17194].

## 5. Limiti e parti irrisolte
Riscrittura completa delle due direzioni.
