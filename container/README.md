# Container del Researcher

Isola il Researcher a livello di sistema: dentro il container esistono solo la sandbox della cella (`/work`),
`tools/` e la cartella del problema (`/repo/...`, sola lettura). Il Referee, i suoi prompt, gli schemi e gli
altri run non sono montati, quindi non sono leggibili né modificabili.

## Una tantum
```
docker build -t proof-pursuit-researcher container/
mkdir -p ~/.proof-pursuit/claude && chmod 700 ~/.proof-pursuit/claude
docker run --rm -it -v ~/.proof-pursuit/claude:/home/researcher/.claude -e HOME=/home/researcher proof-pursuit-researcher claude
```
Nell'ultima riga la CLI parte dentro il container con la cartella delle credenziali montata in scrittura:
scrivi `/login`, completa il login nel browser, poi `/exit`. Da quel momento il container ha una sessione
propria in `~/.proof-pursuit/claude`, FUORI dal repo, che si rinnova da sola. Copiare il token dal portachiavi
di macOS non funziona: la CLI ruota i token e la copia risulta revocata (provato il 2026-09-29).
Se il login nel container non fosse possibile, l'alternativa è `ANTHROPIC_API_KEY` passata con `-e` (spesa a consumo).

## Prova che l'autenticazione funziona
```
container/lancia_researcher.sh /tmp problema-1 -p "rispondi solo: ok" --output-format json
```

## Uso dal loop
```
researcher/loop.py --workdir runs/p3_c3 --shell container ...
```
In modalità `container` il Researcher lavora in `/work`; nel prompt i percorsi sono quelli del container.
