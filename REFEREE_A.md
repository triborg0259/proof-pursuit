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

Tutti i comandi si lanciano **dalla cartella `referee/`**, che e' la radice del
pacchetto dopo l'integrazione fatta da Thomas:

```bash
cd referee
set PYTHONPATH=%CD%                                # su Windows
python -m unittest tests.test_a_contract -v        # 21 test, ~1.2 s
python -m unittest tests.test_a_eval_offline -v    # 23 test, ~0.3 s
python -m unittest discover -s tests -q            # 94 test, ~6.2 s
```

Suite di radice del repository (Researcher, ponte, Referee B), dalla radice:

```bash
python -m pytest tests/ -q                         # ~30 s
```

Misurato su Windows 11, Python 3.14.6, pydantic 2.13.4, pytest 9.0.3.

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

Senza costi, dalla cartella `referee/`:

```bash
python eval_referee_a.py --list
python eval_referee_a.py --show-payload case_03   # cosa vede il modello
```

Live, **consuma 11 chiamate a pagamento**:

```bash
python eval_referee_a.py --model <MODEL_ID> > eval-a.json
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

Tre punti in moduli **non** di competenza di A, quindi non modificati.

**0. I moduli condivisi esistono in due copie, e questo rompe l'integrazione.**
Le stesse classi vivono sia in `referee/referees/` (copia canonica, portata da
Thomas su `main`) sia in `referees/` al primo livello (copia di
`feature/referee-b`). I file sono byte per byte identici, quindi il rischio
sembra estetico, ma non lo e': Python li importa come moduli distinti e crea
**classi diverse con lo stesso nome**. Riproduzione, su un albero in cui
entrambe le copie sono presenti:

```python
import sys
sys.path.insert(0, 'referee'); sys.path.insert(0, '.')
from referees.contracts import MathReport as B_side
del sys.modules['referees'], sys.modules['referees.contracts']
sys.path.remove('.')
from referees.contracts import MathReport as A_side
print(A_side is B_side)                 # False
report = A_side(mathematical_verdict='PASS', first_fatal_error=None,
                accepted_mathematical_claims=['main'], unproved_claims=[],
                missing_cases=[], math_notes='x')
print(isinstance(report, B_side))       # False
```

Conseguenza pratica: un `MathReport` prodotto da A non e' riconosciuto come
`MathReport` da B. Qualunque composizione dei due rapporti (per esempio
`ReviewPacket`, che contiene entrambi gli envelope) fallisce la validazione.

Modifica necessaria, che spetta all'integratore: **una sola copia** dei moduli
condivisi. Poiche' `main` porta gia' il pacchetto in `referee/referees/`, la
strada piu' corta e' spostare li' `adapter_b.py` e il resto del lavoro di B ed
eliminare `referees/` di primo livello. Referee A e' gia' allineato a quella
collocazione. Verificato su un branch locale `integration-a-b`: con le due
copie presenti le suite passano comunque (94 test nel pacchetto, 19 alla
radice), perche' nessun test fa attraversare un oggetto da una copia all'altra.
I test verdi **non** dimostrano quindi che l'integrazione regga.

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
