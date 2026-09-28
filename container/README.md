# Container del Researcher

Isola il Researcher a livello di sistema: dentro il container esistono solo la sandbox della cella (`/work`),
`tools/` e la cartella del problema (`/repo/...`, sola lettura). Il Referee, i suoi prompt, gli schemi e gli
altri run non sono montati, quindi non sono leggibili né modificabili.

## Una tantum
```
docker build -t proof-pursuit-researcher container/
mkdir -p ~/.proof-pursuit/claude && chmod 700 ~/.proof-pursuit/claude
security find-generic-password -s "Claude Code-credentials" -w > ~/.proof-pursuit/claude/.credentials.json
chmod 600 ~/.proof-pursuit/claude/.credentials.json
```
Il secondo blocco esporta il token dell'abbonamento dal portachiavi di macOS in un file FUORI dal repo.
È un segreto della tua sessione: non copiarlo altrove, non versionarlo. Se la CLI lo rifiuta nel container,
l'alternativa è `ANTHROPIC_API_KEY` passata con `-e` (spesa a consumo).

## Prova che l'autenticazione funziona
```
container/lancia_researcher.sh /tmp problema-1 -p "rispondi solo: ok" --output-format json
```

## Uso dal loop
```
researcher/loop.py --workdir runs/p3_c3 --shell container ...
```
In modalità `container` il Researcher lavora in `/work`; nel prompt i percorsi sono quelli del container.
