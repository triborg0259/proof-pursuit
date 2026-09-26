"""Referee B — provenienza, fonti, evidenze computazionali, riproducibilità e regole.

Questo package contiene SOLO la parte B del sistema di referee, più i componenti condivisi
copiati senza modifiche dal progetto di riferimento (contracts, agent_common, provider, trust).
Perché: CLAUDE_CODE_B.md assegna a B i soli file `referee_b.py` e `prompts/b.md` e vieta di
toccare contratti, merge, provider, trust e Referee A; l'integratore aggiungerà il resto.

`adapter_b` è l'unico file nostro: fa da ponte fra i contratti dei referee (pydantic) e il
contratto JSON del repo in `shared/schemas/`. Non duplica logica, converte e basta.

Il verdetto ACCEPT non è mai prodotto da qui: resta una decisione umana.

Nessun import qui: `adapter_b` è anche un modulo eseguibile (`python -m referees.adapter_b`) e
importarlo in anticipo lo farebbe caricare due volte. Usare `from referees.adapter_b import ...`.
"""
