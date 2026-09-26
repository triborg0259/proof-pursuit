# Stato dell'arte sui harness per ricerca matematica con AI (ricerca web, 2026-09-26)

## Tre famiglie
1. **Ricerca evolutiva di programmi** (AlphaEvolve, DeepMind 2025; ShinkaEvolve, Sakana, ICLR 2026;
   OpenEvolve/CodeEvolve open source). Un LLM muta codice, un evaluatore scalare decide, un archivio/isole
   mantiene diversità. Georgiev–Gómez-Serrano–Tao–Wagner (arXiv:2511.02864) l'hanno applicato a 67 problemi:
   ottimo per **costruzioni** (impacchettamenti, insiemi in campi finiti, disuguaglianze variazionali),
   inutile dove serve un'idea nuova; Tao insiste su evaluatori **non sfruttabili** (aritmetica esatta/intervalli,
   niente tolleranze lasche) e sulla verifica umana indipendente dell'output.
   ShinkaEvolve si installa in 10–15 min (`pip install shinka-evolve`), problema = `initial.py` con
   EVOLVE-BLOCK + `evaluate.py` che restituisce `combined_score`; supporta Claude Code come modello di
   mutazione ("headless/claude").
2. **Loop con verificatore formale** (AlphaProof Nexus, DeepMind 2026; Aristotle/Harmonic; AxiomProver; Gauss).
   Il "judge" è Lean: feedback affidabile ma richiede Lean+Mathlib (non installati qui) e la formalizzazione di
   geometria sferica/angoli fra rette: ore di lavoro solo per gli enunciati. Non fattibile in gara.
3. **LLM come giudice di prove in linguaggio naturale.** Evidenza 2025–2026: accuratezza alta su benchmark
   (ProofBench >90%) ma inaffidabile in selezione: GPT-5 (thinking high) ha giudicato corrette 7 prove su 48
   tutte con errori critici (USAMO 2025); RAND: nessun giudice uniformemente affidabile; bias >50% nei test
   avversariali. ⇒ un modello-giudice serve come **critico avversario**, mai come oracolo.

## Cosa implica per Proof Pursuit (7 ore, 24 celle quasi tutte "prove", giudizio umano)
- Ricerca evolutiva: utile solo per celle con **costruzione/controesempio** (P1 parte 6 "disprove"; altri
  problemi da vedere). Il nostro `tools/autoloop.py` copre lo spazio continuo di P1; ShinkaEvolve avrebbe senso
  se un problema richiedesse di evolvere *programmi* (algoritmi, costruzioni combinatorie strutturate).
  Decisione: rinviare finché non abbiamo i problemi 2–4.
- Verifica: per calcoli a supporto di prove usare aritmetica esatta (Fraction/sympy) o a intervalli (mpmath.iv),
  con due implementazioni realmente diverse quando richiesto. Da aggiungere al harness: fase `certify` esatta.
- Giudizio delle prove: loop generatore/critico con subagenti indipendenti (prompt: "trova l'errore", checklist
  del protocollo), poi revisione umana. Nessuna infrastruttura: Agent tool + `tools/review_checklist.md`.
