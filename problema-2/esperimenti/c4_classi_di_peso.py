"""P2 C4 - enumerazione esatta delle etichettature per classi di peso su Q_d.

IDEA. Due vertici di Q_d con lo stesso peso di Hamming differiscono in almeno
due coordinate, quindi non sono mai adiacenti. Di conseguenza, se l'etichettatura
assegna le etichette classe di peso per classe di peso, l'ordine INTERNO a una
classe non cambia l'orientazione di alcuno spigolo, e quindi non cambia il
conteggio. Conta solo la permutazione delle d+1 classi.

Inoltre ogni permutazione delle coordinate e' un automorfismo che preserva il
peso, quindi tutti i vertici dello stesso peso hanno lo stesso numero di cammini
in salita che vi terminano. Detto P_k quel valore comune:

    P_k = [k e' classe valle]
        + k     * P_{k-1}  se la classe k-1 precede la classe k
        + (d-k) * P_{k+1}  se la classe k+1 precede la classe k

    totale = somma su k di C(d,k) * P_k

perche' un vertice di peso k ha k vicini di peso k-1 e d-k vicini di peso k+1.
La classe k e' una classe valle quando entrambe le classi vicine la seguono.

Costo: O(d) per permutazione, (d+1)! permutazioni. Aritmetica intera esatta.

AMBITO. Questo enumera ESATTAMENTE una famiglia di etichettature, non tutte.
Il risultato e' quindi un LIMITE SUPERIORE per U(Q_d), esatto entro la famiglia.
Non e' una prova che U(Q_d) valga quel numero.

Uso:
    python c4_classi_di_peso.py            # d = 1..8, con autovalidazione
    python c4_classi_di_peso.py --dmax 9
"""
from __future__ import annotations

import argparse
import time
from itertools import permutations
from math import comb

# Valori gia' stabiliti dal team, usati solo come controllo del metodo.
NOTI = {1: 2, 2: 5, 3: 14, 4: 34, 5: 88}


def conta_per_ordine(d: int, posizione: tuple[int, ...]) -> int:
    """Numero di cammini in salita per l'etichettatura a classi di peso data.

    `posizione[k]` e' la posizione della classe di peso k nell'ordine delle
    etichette: 0 = classe etichettata per prima.
    """
    cammini_per_classe = [0] * (d + 1)
    # Le classi vanno elaborate in ordine di etichetta crescente: i predecessori
    # di una classe sono le classi vicine gia' elaborate.
    for k in sorted(range(d + 1), key=lambda c: posizione[c]):
        precedente_sotto = k >= 1 and posizione[k - 1] < posizione[k]
        precedente_sopra = k <= d - 1 and posizione[k + 1] < posizione[k]
        e_valle = not precedente_sotto and not precedente_sopra
        totale = 1 if e_valle else 0
        if precedente_sotto:
            totale += k * cammini_per_classe[k - 1]
        if precedente_sopra:
            totale += (d - k) * cammini_per_classe[k + 1]
        cammini_per_classe[k] = totale
    return sum(comb(d, k) * cammini_per_classe[k] for k in range(d + 1))


def migliore_ordine(d: int) -> tuple[int, tuple[int, ...]]:
    """Minimo esatto sulla famiglia: prova tutte le (d+1)! permutazioni."""
    migliore, argmin = None, None
    for ordine in permutations(range(d + 1)):
        # `ordine` elenca le classi in ordine di etichetta; lo converto in posizioni.
        posizione = [0] * (d + 1)
        for posto, classe in enumerate(ordine):
            posizione[classe] = posto
        valore = conta_per_ordine(d, tuple(posizione))
        if migliore is None or valore < migliore:
            migliore, argmin = valore, ordine
    return migliore, argmin


# --------------------------------------------------------------------------
# Verifica indipendente: conteggio diretto sul grafo, senza usare la simmetria.
# Serve a controllare che la formula compatta sopra non sia sbagliata.
# --------------------------------------------------------------------------

def conta_diretto(d: int, ordine: tuple[int, ...]) -> int:
    """Conta i cammini costruendo davvero il grafo e l'etichettatura.

    Metodo deliberatamente diverso: niente classi, niente binomiali. Assegna
    etichette vertice per vertice e propaga p(v) sul DAG indotto.
    """
    posizione = [0] * (d + 1)
    for posto, classe in enumerate(ordine):
        posizione[classe] = posto
    vertici = list(range(1 << d))
    # Ordina per (posizione della classe di peso, valore) e assegna 0,1,2,...
    vertici.sort(key=lambda v: (posizione[bin(v).count("1")], v))
    etichetta = {v: i for i, v in enumerate(vertici)}
    cammini = {}
    totale = 0
    for v in vertici:  # gia' in ordine di etichetta crescente = ordine topologico
        minori = [v ^ (1 << i) for i in range(d)
                  if etichetta[v ^ (1 << i)] < etichetta[v]]
        cammini[v] = 1 if not minori else sum(cammini[u] for u in minori)
        totale += cammini[v]
    return totale


def stringa_etichettatura(d: int, ordine: tuple[int, ...]) -> list[str]:
    """Lista dei 2^d vertici in ordine di etichetta crescente, come stringhe 0/1.

    Convenzione dichiarata: la coordinata 0 e' il bit meno significativo ed e'
    stampata a destra.
    """
    posizione = [0] * (d + 1)
    for posto, classe in enumerate(ordine):
        posizione[classe] = posto
    vertici = sorted(range(1 << d),
                     key=lambda v: (posizione[bin(v).count("1")], v))
    return [format(v, f"0{d}b") for v in vertici]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dmax", type=int, default=8)
    args = parser.parse_args()

    print(f"{'d':>2} {'|E|+1':>7} {'migliore':>9} {'eccesso':>8} "
          f"{'noto':>6} {'ordine classi':>22} {'sec':>7}")
    print("-" * 80)
    for d in range(1, args.dmax + 1):
        avvio = time.perf_counter()
        valore, ordine = migliore_ordine(d)
        durata = time.perf_counter() - avvio
        spigoli = d * (1 << (d - 1))
        noto = NOTI.get(d)
        esito = "" if noto is None else ("=" if noto == valore else f"!={noto}")
        print(f"{d:>2} {spigoli + 1:>7} {valore:>9} {valore - spigoli:>8} "
              f"{str(noto or '-'):>6} {str(ordine):>22} {durata:>7.2f} {esito}")

        # Autovalidazione: la formula compatta deve coincidere con il conteggio
        # diretto sul grafo, che usa un metodo diverso.
        if d <= 8:
            diretto = conta_diretto(d, ordine)
            assert diretto == valore, (
                f"d={d}: formula compatta {valore} != conteggio diretto {diretto}")

    print("\nControllo incrociato formula/grafo superato per ogni d stampato.")
    print("ATTENZIONE: questi sono limiti SUPERIORI (minimo entro la famiglia "
          "delle etichettature per classi di peso), non valori dimostrati.")


if __name__ == "__main__":
    main()
