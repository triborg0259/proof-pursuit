Versione 0.2: leggere prima HACKATHON_START.md. Non serve Lean. Il verdetto ACCEPT è umano; il modello fornisce una revisione.

# Persona B — Evidence, Sources, Computation and Rules

Lavora sul componente B di questo progetto esistente. Leggi prima README.md,
referees/contracts.py, referees/trust.py e referees/prompts/b.md.

File di tua proprietà:
- referees/referee_b.py
- referees/prompts/b.md
- tests/test_b_*.py, da creare per i tuoi casi

Non modificare contratti, merge, provider, trust, referee A o stato condiviso.
Eventuali integrazioni con lettura fonti o verificatori vanno concordate con
l'integratore: non assegnare al modello accesso arbitrario a shell o rete.

Il componente riceve ReviewInput e restituisce AgentEnvelope[EvidenceReport].
Lavora senza leggere il rapporto di A. Non rifare la prova, inventare passaggi
matematici o sostituire una prova mancante con una citazione vietata.

Controlla applicabilità delle fonti, attribuzione, uso consentito, codice incluso,
riproducibilità, esaustività, aritmetica e certificati. Non presentare mai un log
del candidato come una verifica effettuata da voi. Se non hai accesso alla fonte
o all'esecuzione, dichiara MISSING; non fingere un controllo né una frode.

Un risultato noto in letteratura può essere dimostrato indipendentemente: separa
provenienza e dipendenza effettiva. Classifica ogni claim dichiarato e segnala
quali mancanze bloccano la cella o soltanto uno specifico lemma.

Casi richiesti: prova autonoma senza citazioni; fonte valida ma vietata; citazione
non verificata; log falso; campionamento spacciato per enumerazione; floating point
senza controllo; computazione esatta corretta con certificato autentico.

Esegui: python -m unittest discover -s tests -v
Non creare VerifiedRecord da affermazioni del modello. Solo l'orchestratore può
popolare il contesto di fiducia dopo verifica reale, separata e documentata.

Consegna diff, test e limiti osservati. Branch suggerito: feature/referee-b.
