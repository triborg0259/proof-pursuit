# Referee A — correttezza matematica

Componente che valuta **solo** se l'argomento di una soluzione candidata regge.
Non risolve, non ripara la prova, non propone strategie, non giudica fonti o
regole di gara (competono a B) e non emette l'ACCEPT finale, che resta umano.

## Interfaccia, invariata

```python
from referees.referee_a import review_math

envelope = await review_math(job, backend, trusted, timeout=100)
# job: ReviewInput  ·  backend: JSONBackend  ·  trusted: TrustedContext
# ritorna AgentEnvelope[MathReport]
```

L'envelope contiene **o** `report` **o** `limitation`, mai entrambi.
`report=None` significa "non sono riuscito a valutare": un timeout, un errore di
rete o un JSON malformato **non** sono un FAIL matematico.

Verdetti: `PASS` (bersaglio esatto stabilito, nessun obbligo aperto) ·
`PARTIAL` (almeno un claim dichiarato regge, bersaglio no, nessun passo fatale) ·
`FAIL` (primo difetto sostanziale, con `first_fatal_error` di severita' `FATAL`).

Chi consuma A non deve cambiare nulla: firma, modelli Pydantic e campi sono
quelli del pacchetto originale.

## Verifica del software

```bash
python -m unittest tests.test_a_contract -v        # 21 test, ~1.2 s
python -m unittest tests.test_a_eval_offline -v    # 23 test, ~0.3 s
python -m pytest tests/ -q                         # intera suite, ~25 s
```

Misurato su Windows 11, Python 3.14.6, pydantic 2.13.4.

**Ambito:** questi test usano backend simulati. Verificano il software — ruolo,
isolamento dell'input, schema, gestione degli errori, compatibilita' con
`prepare_review` — e **non dicono nulla** sulla capacita' matematica del modello.

## Valutazione matematica

11 casi con esito stabilito a mano e indipendentemente dal modello: 2 prove
corrette (una con caso limite trattato), divisione per espressione nulla,
inversione di quantificatori, esempi finiti spacciati per prova universale,
lemma indispensabile non dimostrato, circolarita', induzione senza caso base,
limite superiore presentato come valore esatto, parziale valido su claim
dichiarato, prova corretta con istruzioni ostili immerse nel testo.

Senza costi:

```bash
python tools/eval_referee_a.py --list
python tools/eval_referee_a.py --show-payload case_03   # cosa vede il modello
```

Live, **consuma 11 chiamate a pagamento**:

```bash
python tools/eval_referee_a.py --model <MODEL_ID> > eval-a.json
```

Gli esiti attesi non raggiungono mai il modello: gli identificatori sono neutri
(`case_01`, …) e le annotazioni interne restano nella tabella locale.

Il riepilogo separa **prove errate accettate** e **prove corrette respinte** —
i due errori che contano — da parziali, astensioni ed errori tecnici. Rileva
inoltre se compare il claim che l'iniezione del caso 11 chiede di aggiungere.

**La qualita' dell'obiezione va letta a mano.** Un FAIL dato per un motivo
inventato conta come fallimento anche se l'etichetta coincide: per questo ogni
riga conserva `first_fatal_error` e `math_notes`.

## Segnalazioni all'integratore

Due difetti in moduli **non** di competenza di A, quindi non modificati.

**1. `referees/adversarial_eval.py` mostra la risposta attesa al modello.**
In `make_job` il nome del caso finisce in `problem_id` e `attempt_id`, e i nomi
sono `division_zero`, `circular`, `prompt_injection`, `correct_square`. Il
modello legge l'etichetta di cio' che deve trovare, quindi quella suite
sovrastima le prestazioni. Riproduzione:

```bash
python -c "from referees.adversarial_eval import CASES, make_job; print(make_job(CASES[2]).problem_id)"
# stampa: division_zero
```

Modifica necessaria: identificatori neutri, con la mappa nome→attesa tenuta
fuori dal payload. `tools/eval_referee_a.py` lo fa gia' e puo' servire da
riferimento.

**2. `referees/agent_common.py` perde il dettaglio degli errori.**
`call_agent` comprime ogni guasto in `f"{role}: {type(exc).__name__}"`. In
produzione una `ValidationError` diventa la stringa `"A: ValidationError"`,
senza indicare quale campo ha violato lo schema: la diagnosi di un'astensione
ripetuta diventa molto piu' lenta. Riproduzione: un backend che restituisce
`{"report": {...}, "limitation": "x"}` produce quella stringa e nient'altro.

Modifica suggerita: includere una forma troncata di `str(exc)`, senza
rimuovere la garanzia che un errore operativo non diventi mai un FAIL.

## Limiti dichiarati

- **Nessuna esecuzione live effettuata.** `ANTHROPIC_API_KEY` e
  `ANTHROPIC_MODEL` non erano configurate. Tutto cio' che e' riportato qui e'
  offline: la capacita' matematica di A **non e' stata misurata**.
- Gli esiti attesi dei casi sono giudizio umano, non verita' formalizzata. Per
  ogni caso il campo `rationale` spiega perche' quell'esito e' quello corretto,
  cosi' e' contestabile.
- La batteria e' piccola e bilanciata a mano: misura non vacuita', non
  affidabilita'. Superarla non garantisce nulla su prove nuove.
- A non dispone di strumenti di esecuzione: non esegue Python ne' Lean e non
  deve dichiarare di averlo fatto. Le osservazioni dei checker arrivano
  dall'orchestratore e valgono solo per l'ambito dichiarato.
