# Referee rapido — versione 0.2, senza Lean

Usate questa guida per le cinque ore rimaste. La revisione matematica è generale:
non dipende dall'ipercubo e funziona anche senza alcun controllo numerico allegato.

## Avvio immediato

Python 3.11+. Dalla directory del progetto:

```bash
python -m pip install -e ".[claude]"
python -m unittest discover -s tests -q
python check_examples.py
```

Impostate ANTHROPIC_API_KEY e ANTHROPIC_MODEL nell'ambiente. Non mettete chiavi
nelle prove, nella repository o nei file condivisi. ANTHROPIC_MODEL_B è opzionale.

```bash
python -m referees run examples/fast-input.json > packet.json
```

Per il vostro problema copiate fast-input.json e inserite testo originale,
cella, prova e claim numerati. Sono gli unici dati matematici indispensabili;
fonti e codice possono restare vuoti. Inserite le vere regole della competizione.
Il file d'esempio non contiene le regole ufficiali.

Due richieste Claude partono in parallelo: A cerca il primo errore matematico,
B controlla evidenze e regole. Default: timeout 60 secondi per richiesta, massimo
2500 token di output ciascuna, nessun retry automatico. Non è una garanzia di
latenza del servizio. --timeout e --max-tokens consentono di cambiare i limiti.
Per prove lunghe aumentate i token; un rapporto troncato resta non verificato.

Il risultato è un pacchetto con i due rapporti, il primo blocker, i claim proposti
e uno stato READY_FOR_HUMAN / NEEDS_WORK / INCOMPLETE. **READY_FOR_HUMAN non è
ACCEPT.** Il modello non può approvare la soluzione né modificare lo stato.

La funzione Python da integrare è:

```python
from referees.hackathon import prepare_review
packet = await prepare_review(job, backend, checks=[], timeout=60)
```

`job` è ReviewInput; `backend` è ClaudeBackend. Potete usare model_a/model_b diversi.
Questo non garantisce che gli errori dei modelli siano indipendenti.

## Controlli esatti opzionali e separati dalla prova generale

```bash
python -m referees run vostro-input.json --checks vostri-controlli.json > packet.json
```

Ogni controllo indica un claim_id dichiarato nella prova. Esempi di strutture:
examples/checks-multidomain.json. Non usate questo file insieme a fast-input.json:
contengono claim ID diversi. `python check_examples.py` esegue gli esempi da solo.

| Controllo | Cosa verifica realmente |
|---|---|
| rational_vectors | Norme e prodotti scalari esatti di vettori razionali; adatto a configurazioni geometriche finite |
| hypercube_paths | Conteggio dei cammini di UNA etichettatura, quindi eventuale limite superiore |
| hypercube_minimum | Enumerazione completa solo per d<=3; nessuna generalizzazione automatica |
| unrestricted_partitions_allowed_parts | Partizioni non ordinate con parti nell'insieme dato e ripetizioni illimitate, per i soli n richiesti |
| residue_classes | Disgiunzione delle classi fornite, gcd e testimone intero delle intersezioni |

Non abbiamo il testo di geometria, partizioni o classi di resto. Non è quindi
corretto affermare che i controlli generici risolvano esattamente quelle celle.
In particolare **D_B(n) non è stato definito**: adattate la funzione dopo aver letto
la sua definizione; non rinominate il contatore generico come se fosse già D_B.
I vettori razionali non coprono automaticamente coordinate trigonometriche o
irrazionali. Nessun supporto implicito ad aritmetica a intervalli è dichiarato.

Interi Python e Fraction evitano arrotondamenti. I float non vengono convertiti
silenziosamente in dati esatti. Esperimenti float restano utilizzabili come
esplorazione; non invalidano una prova indipendente corretta.

Il codice candidato in artifacts/code_used non viene eseguito sul vostro computer.
I controlli eseguono implementazioni possedute dal referee sui dati consegnati.
Questo evita di far certificare il proprio risultato allo script del Researcher.
Per nuovi algoritmi create un piccolo checker approvato dal team. Se volete
eseguire codice arbitrario, serve un worker isolato e un controllo di correttezza
indipendente: una semplice ricerca della parola float non basta.

## ACCEPT umano, senza Lean

Un revisore umano legge prova e rapporti e decide quali claim approvare. La
policy protetta deve avere require_machine_verification=false se la gara consente
prove scritte revisionate: il software non cambia questa regola autonomamente.

Per impedire che il modello fabbrichi un'approvazione, la ricevuta è firmata HMAC.
In un terminale/processo riservato alla persona, generate la chiave una volta:

macOS/Linux:
```bash
export REFEREE_APPROVAL_SECRET="$(python -c 'import secrets; print(secrets.token_hex(32))')"
```

PowerShell:
```powershell
$env:REFEREE_APPROVAL_SECRET = python -c "import secrets; print(secrets.token_hex(32))"
```

Non date questa variabile al processo del Researcher o a shell controllate dagli
agenti. La firma certifica un'azione del revisore, NON la verità matematica.

Nel terminale umano:
```bash
python -m referees approve packet.json --reviewer Gabriele --claims main --reason "Ho controllato prova, ipotesi e rapporti" > approval.json
```

Il comando richiede di digitare una frase contenente il digest del pacchetto.
Non ha --yes. Per più claim usate --claims lemma1,lemma2,main. Poi:

```bash
python -m referees finalize packet.json approval.json --current-input examples/fast-input.json > final.json
```

Usate il vostro input attuale al posto dell'esempio. Modificare prova, rapporti,
regole o stato invalida la ricevuta. Dipendenze mancanti restano bloccanti anche
con firma umana. L'orchestratore legge final.json e gestisce highest_verified_cell;
il referee restituisce lo snapshot senza incrementarlo.

Un ACCEPT in questa modalità significa **revisione umana con controlli di supporto**,
non prova formalizzata in Lean. Anche una persona può sbagliare.

## Test di non vacuità sul modello reale

```bash
python -m referees.adversarial_eval > live-eval.json
```

Esegue 7 chiamate pagate, massimo 3 contemporanee: due prove corrette e cinque
difettose (divisione per zero, quantificatori, esempi, circolarità, istruzioni
ostili). Restituisce falsi PASS, prove corrette non approvate e astensioni.
Le risposte attese non vengono mostrate al modello. Non ho eseguito questo test
live: serve la vostra chiave. Superarlo non garantisce affidabilità su prove nuove.

## Come dividervi oggi

- Persona A: prompt a.md, qualità dei blocker e test live su prove corrette/errate.
- Persona B: prompt b.md, controllo delle fonti e adattamento dei checker alle vere
  definizioni delle celle. Usare solo log prodotti realmente dal vostro sistema.
- Contratti e flusso umano restano condivisi; nominatene un integratore unico.

Non installate Lean per usare questa versione. I vecchi moduli runner.py e merge.py
rimangono come componenti interni/compatibilità: il percorso operativo attuale è
hackathon.prepare_review, sign_human_approval e finalize_review.
