Versione 0.2: leggere prima HACKATHON_START.md. Non serve Lean. Il verdetto ACCEPT è umano; il modello fornisce una revisione.

# Persona A — Mathematical Correctness

Lavora sul componente A di questo progetto esistente, senza ricostruire l'intero
referee. Leggi prima README.md, referees/contracts.py e referees/prompts/a.md.

File di tua proprietà:
- referees/referee_a.py
- referees/prompts/a.md
- tests/test_a_*.py, da creare per i tuoi casi

Non modificare contratti, merge, provider, trust, referee B o stato condiviso.
Se serve un cambiamento di interfaccia, proponilo all'integratore con un esempio
di input/output; non aggirare il contratto per far passare un test.

Il tuo componente riceve ReviewInput e restituisce AgentEnvelope[MathReport].
La matematica deve essere valutata indipendentemente da B. Usa claim ID già
dichiarati e identifica il primo errore sostanziale. Non riparare la prova.
Non certificare fonti, non eseguire codice e non decidere il verdetto finale.
Un rapporto assente per incapacità deve avere report=null e limitation esplicita.

Obiettivo del tuo lavoro: migliorare e valutare il controllo dei passaggi logici,
ipotesi, quantificatori, domini, casi limite, circolarità, limiti superiore/inferiore
e corrispondenza con il target. Nessun punteggio di fiducia equivale a una prova.

Costruisci casi con prova corretta, divisione per zero, lemma non dimostrato,
induzione incompleta e test numerici presentati come prova generale. Includi prove
corrette difficili: non premiare un referee che rifiuta tutto.

Esegui: python -m unittest discover -s tests -v
Non usare chiavi API nei test. Per test live usa l'ambiente del team e contabilizza
il costo. Distingui nel report test del codice, test del modello e formalizzazione.

Consegna diff, test e limiti osservati. Branch suggerito: feature/referee-a.
