"""P2 C4 - ricerca locale sullo spazio completo delle etichettature di Q_d.

MOTIVAZIONE. La famiglia delle etichettature per classi di peso
(c4_classi_di_peso.py) riproduce U(Q_d) per d <= 4 ma fallisce a d = 5: da 92
contro il valore vero 88. Serve quindi cercare fuori da quella famiglia.

METODO. Ricottura simulata sulle permutazioni dei 2^d vertici.
- stato: ordine dei vertici per etichetta crescente;
- mosse: scambio di due etichette, oppure spostamento di un'etichetta altrove;
- punteggio: numero esatto di cammini in salita, in aritmetica intera.

Il conteggio sfrutta il fatto che l'ordine per etichetta e' gia' un ordine
topologico del DAG indotto, quindi una sola passata basta:

    p(v) = 1 se v non ha vicini con etichetta minore (v e' una valle)
    p(v) = somma di p(u) sui vicini u con etichetta minore, altrimenti

CALIBRAZIONE. d = 5 ha risposta nota (88). Se la ricerca non la ritrova, i
valori prodotti per d = 6,7,8 non sono affidabili e vanno dichiarati deboli.

AMBITO. Produce LIMITI SUPERIORI. Nessun valore qui e' dimostrato minimo.

Uso:
    python c4_ricerca_locale.py --d 5 --secondi 60
    python c4_ricerca_locale.py --d 7 --secondi 600 --seed 1
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

NOTI = {1: 2, 2: 5, 3: 14, 4: 34, 5: 88}


def vicini_di(d: int) -> list[tuple[int, ...]]:
    """Lista di adiacenza di Q_d: due vertici adiacenti se differiscono di un bit."""
    return [tuple(v ^ (1 << i) for i in range(d)) for v in range(1 << d)]


def conta(ordine: list[int], vicini: list[tuple[int, ...]],
          rango: list[int], cammini: list[int]) -> int:
    """Numero esatto di cammini in salita. `rango` e `cammini` sono buffer riusati."""
    for posto, v in enumerate(ordine):
        rango[v] = posto
    totale = 0
    for v in ordine:  # ordine di etichetta crescente = ordine topologico
        somma = 0
        mio_rango = rango[v]
        for u in vicini[v]:
            if rango[u] < mio_rango:
                somma += cammini[u]
        cammini[v] = somma if somma else 1
        totale += cammini[v]
    return totale


def ordine_per_classi_di_peso(d: int) -> list[int]:
    """Punto di partenza ragionevole: il miglior ordine di classi noto per d<=8."""
    migliori = {1: (0, 1), 2: (0, 1, 2), 3: (0, 1, 3, 2), 4: (0, 1, 4, 3, 2),
                5: (0, 1, 3, 2, 5, 4), 6: (0, 1, 3, 2, 6, 5, 4),
                7: (0, 1, 3, 2, 5, 4, 7, 6), 8: (0, 1, 3, 2, 5, 4, 8, 7, 6)}
    classi = migliori.get(d, tuple(range(d + 1)))
    posizione = {classe: posto for posto, classe in enumerate(classi)}
    return sorted(range(1 << d), key=lambda v: (posizione[bin(v).count("1")], v))


def ricottura(d: int, secondi: float, seme: int,
              partenza: list[int] | None = None) -> tuple[int, list[int]]:
    """Ricottura simulata con riavvii impliciti tramite riscaldamento periodico."""
    rng = random.Random(seme)
    n = 1 << d
    vicini = vicini_di(d)
    rango = [0] * n
    cammini = [0] * n

    ordine = list(partenza) if partenza else list(range(n))
    if partenza is None:
        rng.shuffle(ordine)
    corrente = conta(ordine, vicini, rango, cammini)
    migliore, ordine_migliore = corrente, list(ordine)

    avvio = time.perf_counter()
    temperatura_iniziale = max(2.0, corrente * 0.01)
    passi = 0
    while True:
        trascorso = time.perf_counter() - avvio
        if trascorso >= secondi:
            break
        # Raffreddamento ciclico: scende, poi riparte caldo. Evita di restare
        # bloccati in un minimo locale senza buttare via il migliore trovato.
        frazione = (trascorso / secondi * 6) % 1.0
        temperatura = temperatura_iniziale * (1 - frazione) ** 3 + 0.01

        for _ in range(200):  # blocco di mosse fra due letture dell'orologio
            passi += 1
            i, j = rng.randrange(n), rng.randrange(n)
            if i == j:
                continue
            if rng.random() < 0.7:
                ordine[i], ordine[j] = ordine[j], ordine[i]
                annulla = ("scambio", i, j)
            else:
                v = ordine.pop(i)
                ordine.insert(j, v)
                annulla = ("sposta", j, i)
            candidato = conta(ordine, vicini, rango, cammini)
            delta = candidato - corrente
            if delta <= 0 or rng.random() < pow(2.718281828, -delta / temperatura):
                corrente = candidato
                if candidato < migliore:
                    migliore, ordine_migliore = candidato, list(ordine)
            else:
                tipo, a, b = annulla
                if tipo == "scambio":
                    ordine[a], ordine[b] = ordine[b], ordine[a]
                else:
                    v = ordine.pop(a)
                    ordine.insert(b, v)
    return migliore, ordine_migliore, passi


def verifica_indipendente(d: int, ordine: list[int]) -> int:
    """Riconta con strutture diverse (dizionari, nessun buffer riusato).

    Serve a escludere che il conteggio veloce sia falsato da un buffer sporco.
    """
    etichetta = {v: i for i, v in enumerate(ordine)}
    p = {}
    totale = 0
    for v in ordine:
        minori = [v ^ (1 << i) for i in range(d)
                  if etichetta[v ^ (1 << i)] < etichetta[v]]
        p[v] = sum(p[u] for u in minori) if minori else 1
        totale += p[v]
    return totale


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--d", type=int, required=True)
    parser.add_argument("--secondi", type=float, default=60)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--salva", type=Path)
    args = parser.parse_args()

    d = args.d
    spigoli = d * (1 << (d - 1))
    valore, ordine, passi = ricottura(d, args.secondi, args.seed,
                                      ordine_per_classi_di_peso(d))
    controllo = verifica_indipendente(d, ordine)
    assert controllo == valore, f"conteggio veloce {valore} != controllo {controllo}"

    noto = NOTI.get(d)
    print(f"d = {d}   vertici = {1 << d}   |E| = {spigoli}   |E|+1 = {spigoli + 1}")
    print(f"mosse valutate: {passi}")
    print(f"migliore trovato: {valore}   (eccesso su |E|: {valore - spigoli})")
    print(f"ricontrollato con metodo indipendente: {controllo} OK")
    if noto is not None:
        stato = "RITROVATO" if valore == noto else f"NON ritrovato (vero {noto})"
        print(f"valore noto per d={d}: {noto} -> {stato}")
    print("\nATTENZIONE: limite SUPERIORE. Nessuna prova di minimalita'.")

    if args.salva:
        args.salva.write_text(json.dumps({
            "d": d, "cammini": valore, "spigoli": spigoli, "seed": args.seed,
            "secondi": args.secondi, "mosse": passi,
            "etichettatura": [format(v, f"0{d}b") for v in ordine],
            "convenzione": "coordinata 0 = bit meno significativo, stampato a destra",
            "ambito": "limite superiore da ricerca locale, non dimostrato minimo",
        }, indent=2))
        print(f"salvato in {args.salva}")


if __name__ == "__main__":
    main()
