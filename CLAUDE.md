# Proof Pursuit — protocollo persistente

Gara di ricerca matematica assistita da AI, durata 7 ore, 4 problemi × 6 celle di difficoltà crescente.
Contano prove e certificati verificabili. I risultati parziali valgono se descritti correttamente.
Ammessi: web, letteratura, AI, codice.

## Clean code (richiesta esplicita del team)
- Funzioni piccole, semplici, spiegabili; mai oltre ~30 righe.
- Commenti e docstring in italiano che dicono COSA fa il codice e PERCHÉ.
- Niente file o requirements nuovi per dipendenze già installate altrove (usare `.venv`).
- Codice e output leggibili: nomi parlanti, niente one-liner criptici.

## Vincoli assoluti
- NON accedere all'account della gara, NON inviare submission, NON pubblicare materiale. Tutto resta locale.
- Non dichiarare mai "risolto" sulla base di una bozza plausibile o di un esperimento favorevole.
- Il consenso di un altro modello non è una prova.
- Non inventare citazioni. Non presentare come letta una fonte non verificata.
- Nessuna dashboard, server, framework di orchestrazione o infrastruttura non necessaria.

## Struttura
- `CLAUDE.md` — questo protocollo.
- `STATUS.md` — stato delle 4 colonne e delle 24 celle, con evidenze concrete.
- `problema-N/` — una cartella per problema:
  - `enunciato.md` — testo originale, salvato fedelmente (mai corretto o completato in silenzio)
  - `note.md` — definizioni estratte, richieste per cella, punteggi, ambiguità, approcci
  - `esperimenti/` — codice di ricerca (trova risultati)
  - `certificati/` — oggetti da verificare + script di verifica (controlla risultati) — SEPARATI dalla ricerca
  - `submission/` — bozze delle consegne, una per cella
- `tools/autoloop.py` — harness "proponi / valuta / tieni se migliora" (pattern autoresearch, senza il repo): seed paralleli, budget fisso, restart, ricertificazione mpmath, ledger JSONL. Protocollo d’uso in `tools/program.md`; tabelle con `tools/ledger_table.py`. Ambiente: `.venv` (numpy, mpmath). Output float ⇒ MAI una prova.
- `shared/` — contratto JSON del sistema multi-agente (state, attempt, referee_report, creative_ideas); `researcher/` —
  agente Researcher (nostra parte del brief MVP); `runs/<problem>/` — cartelle di lavoro del loop; `tests/`.
  Il Researcher NON giudica e NON dichiara celle risolte: solo il Referee approva. Stati di cella ammessi:
  SOLVED · SOLVED_BY_COMPUTATION · PARTIAL_PROGRESS · UNRESOLVED · KNOWN_OPEN · FALSE.
- Creare altri file solo quando servono.

## Raccolta dei problemi
Quando arriva un problema:
1. Salvare fedelmente il testo in `problema-N/enunciato.md`.
2. Estrarre definizioni, richieste per cella, punteggi, requisiti di consegna → `note.md`.
3. Segnalare ambiguità o dati mancanti che cambiano il significato matematico.
4. Riassumere cosa viene chiesto e quali approcci sembrano plausibili.
5. Limitarsi a comprensione e triage; attendere il problema successivo prima di ricerche lunghe.
Con tutti e 4 i problemi: proporre una distribuzione del tempo che garantisca un primo passaggio su ciascuno.
Chiedere quanto tempo rimane se non è stato indicato.

## Protocollo di ricerca (per ogni cella)
- Scrivere esattamente quale affermazione si cerca di stabilire.
- Controllare definizioni, casi limite e piccoli esempi.
- Distinguere sempre: DIMOSTRATO / CITATO (con fonte) / VERIFICATO SU INTERVALLO FINITO / CONGETTURA.
- Fonti esterne: registrare riferimento preciso, enunciato usato e ipotesi.
- Se la cella richiede una prova, citare il risultato non sostituisce la dimostrazione.
- Valore ottimo: separare la costruzione che lo raggiunge dalla prova che non si può fare meglio.
- Approccio fallito: documentare l'ostacolo concreto e ciò che resta utilizzabile.

## Esperimenti e certificati
Prima di una ricerca costosa: descrivere spazio di ricerca, copertura, stima del costo, criterio di arresto.
Partire da casi piccoli con limiti espliciti.
Quando il calcolo sostiene una prova:
- giustificare matematicamente la riduzione a un insieme finito;
- dimostrare la validità di ogni regola che esclude casi;
- aritmetica esatta quando possibile; giustificare eventuali errori numerici;
- registrare parametri, versioni, seed, conteggi, tempi;
- conservare gli oggetti necessari alla verifica;
- fornire un comando riproducibile e misurare il tempo di verifica;
- rispettare il limite < 10 minuti su portatile e i requisiti specifici della cella.
Una ricerca interrotta è incompleta. L'assenza di controesempi non dimostra nulla oltre il dominio coperto.
Implementazioni indipendenti richieste ⇒ metodi realmente diversi, non riscritture dello stesso algoritmo.

## Revisione e consegna
Prima di dichiarare risolta una cella: revisione critica (ipotesi mancanti, circolarità, passaggi non giustificati,
discrepanze codice/enunciato).
Bozza di submission in `problema-N/submission/cella-K.md` con:
1. risultato esatto e ambito di validità;
2. dimostrazione completa oppure certificato + giustificazione;
3. istruzioni di verifica, dipendenze, tempi misurati;
4. fonti, con distinzione tra risultati esistenti e nostro contributo;
5. limiti e parti irrisolte.
Aggiornare `STATUS.md` con evidenze concrete.

## Stati ammessi in STATUS.md
`non iniziato` · `in analisi` · `in corso` · `parziale` (con cosa è stabilito) · `bozza pronta` (da revisionare) ·
`revisionato` (pronto per consegna) · `bloccato` (con ostacolo).
