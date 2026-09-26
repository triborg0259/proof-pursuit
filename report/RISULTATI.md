---
title: "Proof Pursuit — risultati raggiunti"
subtitle: "Team: T. Tumini (Researcher), gabundos (Referee), M. Renzi (Creative), gio3r3gio · 26 settembre 2026"
lang: it
---

## In una riga

Su 24 celle, **10 chiuse** con prova completa, verdetto positivo di due giudici automatici indipendenti e approvazione umana (18 punti), **1 candidato** sul valore, **13 parziali** onesti, tutti pubblicati. Il sistema multi-agente ha funzionato end-to-end e ha chiuso da solo 5 celle; le altre 5 le ha chiuse con prove scritte a mano dal team e giudicate dallo stesso Referee.

## Cosa abbiamo chiuso

| Cella | Come | Punti |
|---|---|---|
| Problema 1, parte 1 | prova scritta dal team (semigiro casuale), giudicata dal Referee, approvata | 1 |
| Problema 1, parte 2 | prova scritta dal team (induzione con proiezione), giudicata, approvata | 2 |
| Problema 2, parte 1 | loop autonomo: Researcher con shell + Referee, revisione umana | 1 |
| Problema 2, parte 2 | loop autonomo, tre run del Referee, riduzione riletta a mano | 2 |
| Problema 2, parte 3 | loop autonomo, una iterazione: valore, etichettatura e bound inferiore | 3 |
| Problema 3, parte 1 | loop autonomo, una iterazione | 1 |
| Problema 3, parte 2 | loop autonomo, **due iterazioni**: REJECT motivato, poi prova completata | 2 |
| Problema 4, parte 1 | prova scritta dal team (parità), giudicata, approvata | 1 |
| Problema 4, parte 2 | prova scritta dal team (clique per primo), giudicata, approvata | 2 |
| Problema 4, parte 3 | loop autonomo: riduzione a insieme finito + ricerca certificata con due implementazioni | 3 |

Autonomamente (Researcher → Referee, senza intervento umano sul contenuto): problema 2 parti 1, 2, 3; problema 3 parti 1, 2; problema 4 parte 3. Con prova umana e giudizio automatico: problema 1 parti 1, 2; problema 4 parti 1, 2.

## Cosa è rimasto parziale, e cosa contiene

| Cella | Contenuto del parziale |
|---|---|
| Problema 1, parte 3–5 | formalizzazione, riduzione ai deficit, lemma della parte 2 come mattone, letteratura |
| Problema 1, parte 6 | lemmi di trasferimento fra dimensioni (dimostrati), nessuna famiglia infinita nuova; aperta dal 1959 |
| Problema 2, parte 4 | valore candidato per costruzione a stelle, ottimalità dimostrata dentro la famiglia; bound inferiore mancante |
| Problema 2, parte 5–6 | identità strutturale esatta e riduzione agli insiemi decycling; bound noti non migliorati |
| Problema 3, parte 3 | bound generale dimostrato per rango ≥ 5, tabella esatta fino a rango 11, valore della famiglia congetturato con estremali esplicite |
| Problema 3, parte 4–5 | tabella esatta, formule congetturate, valori residui, estremali; prova uniforme mancante |
| Problema 3, parte 6 | tabella come base per la congettura; aperta |
| Problema 4, parte 4 | certificato scritto e matematica giudicata PASS fino a taglia 13; riesecuzioni non riprodotte per argomenti mancanti negli script |
| Problema 4, parte 5 | prova a mano del punto sulle due taglie isolate; certificato rafforzato mancante |
| Problema 4, parte 6 | ricorsione e bound incondizionato più debole; segnalato il lavoro arXiv del luglio 2026 che migliora il bound citato |

## Perché parziali: il tempo

1. **Costruzione del sistema in gara.** Delle 7 ore, circa 3 sono andate a costruire e integrare il harness: Researcher, ponte, Referee di due giudici, Creative, loop, ricerca arXiv, pacchetti di consegna. I primi run reali sono partiti a metà pomeriggio.
2. **Latenza per tentativo.** Un tentativo del Researcher con shell dura 10–25 minuti, il Referee 4: un'iterazione vale 15–30 minuti, due iterazioni un'ora. La macchina aspetta il modello; più CPU non aiuta, il parallelismo era già a undici celle.
3. **Quattro difetti di contratto trovati dai run** (flag variadico che ingoiava il prompt; riserva del giudice che annullava un PASS; riesecuzioni fidate e regole ufficiali mancanti; provenienza dei claim non ammessa dal validatore). Ogni correzione è costata un run del Referee e 10–15 minuti; ma senza i run reali non sarebbero emersi.
4. **Un riavvio accidentale della sessione** a 35 minuti dalla fine ha ucciso sette loop in corso, di cui quattro già col tentativo scritto; sono stati recuperati come parziali, due seconde iterazioni sono andate perse.
5. **Difficoltà intrinseca.** Le parti 6 sono problemi aperti; le parti 5 richiedono argomenti uniformi o certificati rafforzati a ore di lavoro. Il piano dichiarava dall'inizio 14–18 punti realistici: siamo a 18 più il candidato.

## Cosa ha funzionato e va tenuto

- Referee a due giudici con merge deterministico: nessun falso positivo; i REJECT hanno sempre indicato il passo esatto mancante.
- Ciclo dell'errore: su problema 3 parte 2 il Researcher ha letto il rigetto, recuperato la fonte e completato la prova al secondo giro.
- Prove scritte a mano giudicate dal Referee: quattro celle chiuse in venti minuti.
- Costruzione esplicita più verifica esatta: per problema 2 il metodo della parte 2 si è esteso alla parte 3 in una iterazione.
- Tracciabilità: ogni consegna riporta le decisioni degli agenti, i token, le fonti arXiv e il codice rieseguito.

## Cosa cambiare la prossima volta

Harness pronto prima della gara; portfolio di Researcher paralleli per cella con famiglie diverse; Referee da subito sui tentativi umani; script con argomenti espliciti e limiti di tempo dichiarati; niente riavvii della sessione con loop attivi.

Repository e write-up: https://github.com/triborg0259/proof-pursuit · https://triborg0259.github.io/proof-pursuit/
