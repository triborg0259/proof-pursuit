"""Verifica indipendente delle etichettature prodotte per P2 C4.

Legge i file JSON degli esperimenti e ricontrolla da zero, senza riusare nulla
del codice di ricerca:
  1. l'etichettatura e' una biiezione sui 2^d vertici;
  2. il conteggio dei cammini in salita, ricalcolato dalle stringhe 0/1;
  3. quando il file dichiara un insieme I: che sia indipendente e che Q_d - I
     sia una foresta (spigoli == vertici - componenti);
  4. che valga 2^d + (d-1)|I|.

Uso:  python c4_verifica_etichettature.py <file.json> [...]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def da_stringa(s: str) -> int:
    """Converte la stringa 0/1 nell'intero, bit meno significativo a destra."""
    return int(s, 2)


def conta_cammini(d: int, ordine: list[int]) -> int:
    """Ricorrenza p(v) = 1 se valle, altrimenti somma dei p dei vicini minori."""
    etichetta = {v: i for i, v in enumerate(ordine)}
    p, totale = {}, 0
    for v in ordine:
        minori = [v ^ (1 << i) for i in range(d) if etichetta[v ^ (1 << i)] < etichetta[v]]
        p[v] = sum(p[u] for u in minori) if minori else 1
        totale += p[v]
    return totale


def e_foresta_senza(d: int, insieme: set[int]) -> bool:
    """Q_d - insieme e' una foresta? Union-find, nessuna ricorsione."""
    padre = {v: v for v in range(1 << d) if v not in insieme}

    def trova(x: int) -> int:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    spigoli = 0
    for v in list(padre):
        for i in range(d):
            u = v ^ (1 << i)
            if u in padre and u > v:
                spigoli += 1
                ra, rb = trova(v), trova(u)
                if ra != rb:
                    padre[ra] = rb
    componenti = len({trova(v) for v in padre})
    return spigoli == len(padre) - componenti


def verifica(percorso: Path) -> bool:
    dati = json.loads(percorso.read_text())
    d = dati["d"]
    ordine = [da_stringa(s) for s in dati["etichettatura"]]
    esito = []

    biiettiva = sorted(ordine) == list(range(1 << d))
    esito.append(("etichettatura biiettiva su 2^d vertici", biiettiva))

    contati = conta_cammini(d, ordine)
    atteso = dati["cammini"]
    esito.append((f"conteggio cammini = {contati} (atteso {atteso})", contati == atteso))

    if "insieme_I" in dati:
        insieme = {da_stringa(s) for s in dati["insieme_I"]}
        taglia = dati["taglia_I"]
        esito.append((f"|I| = {len(insieme)} (atteso {taglia})", len(insieme) == taglia))
        indip = not any((v ^ (1 << i)) in insieme for v in insieme for i in range(d))
        esito.append(("I indipendente", indip))
        esito.append(("Q_d - I e' una foresta", e_foresta_senza(d, insieme)))
        formula = (1 << d) + (d - 1) * len(insieme)
        esito.append((f"2^d + (d-1)|I| = {formula}", formula == contati))

    print(f"\n{percorso.name}  (d = {d})")
    for testo, ok in esito:
        print(f"  [{'OK ' if ok else 'NO '}] {testo}")
    return all(ok for _, ok in esito)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    tutti_ok = True
    for arg in sys.argv[1:]:
        tutti_ok &= verifica(Path(arg))
    print("\n" + ("TUTTE LE VERIFICHE SUPERATE" if tutti_ok else "ALMENO UNA VERIFICA FALLITA"))
    return 0 if tutti_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
