# program.md — protocollo per il harness di ricerca numerica

Analogo del `program.md` di autoresearch, adattato: qui l'agente (Claude o un subagente) propone esperimenti,
il harness li esegue con budget fisso e li registra in un ledger; si tiene solo ciò che migliora.

## Ciclo
1. Scegli un'ipotesi numerica precisa (es. "per d=3, N=5 il massimo di S è il valore congetturato").
2. Esegui:
   `.venv/bin/python tools/autoloop.py <obiettivo> --budget B --seeds K --ledger <problema>/esperimenti/ledger.jsonl --tag <T> -- <args>`
   Limiti: B·K/workers < 2 min per esperimento salvo motivo dichiarato. Parti da casi piccoli.
3. Leggi `gap_target_minus_best` e `certify.summary`:
   - gap ≈ 0 (< 1e-6) e struttura coerente ⇒ evidenza a favore del target (NON prova);
   - gap < 0 oltre l'errore float (< -1e-6, confermato da `S_mp40` > target) ⇒ **controesempio candidato**:
     ricontrolla con seed diversi, poi tenta una versione esatta (coordinate algebriche);
   - gap > 1e-3 ⇒ ricerca non convergente: aumenta budget/seeds una volta; se persiste, annota e fermati.
4. Aggiorna il README degli esperimenti con la tabella generata da `tools/ledger_table.py`.
5. Ogni run è registrato: non cancellare righe del ledger, semmai aggiungi un tag "scartato".

## Cosa NON fare
- Non presentare massimi numerici come prova. Non scrivere "risolto" in STATUS su questa base.
- Non ottimizzare il harness oltre il necessario per le celle in corso.
