# Proof Pursuit — referee rapido, versione 0.2

Leggere [HACKATHON_START.md](HACKATHON_START.md) per installazione, uso e integrazione.

La versione attuale usa due revisioni parallele, controlli esatti opzionali e approvazione finale umana. Non richiede Lean. Il flusso è generale e non dipende dall’ipercubo.

Punti di ingresso: `python -m referees run`, `approve`, `finalize`; API Python in `referees/hackathon.py`.

Test software: `python -m unittest discover -s tests -q`.
Esempi esatti nei quattro ambiti: `python check_examples.py`.
Test di non vacuità del modello reale (7 chiamate pagate): `python -m referees.adversarial_eval`.

Istruzioni per le due persone: CLAUDE_CODE_A.md e CLAUDE_CODE_B.md. Schemi in schemas/.

Limiti: nessuna chiamata Claude live eseguita qui; verifiche del modello da valutare sul vostro account. Il contatore di partizioni è generico: serve la definizione originale di D_B(n). Non vengono eseguiti programmi arbitrari del candidato.
