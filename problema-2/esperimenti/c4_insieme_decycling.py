"""P2 C4 - ricerca di insiemi indipendenti che rendono Q_d una foresta.

MOTIVAZIONE. Sia I un insieme indipendente di vertici di Q_d tale che Q_d - I
sia una foresta. L'etichettatura che mette PRIMA i vertici della foresta, ogni
albero ordinato dalla radice verso le foglie, e I per ULTIMO, produce
esattamente

    2^d + (d-1)|I|

cammini in salita. Infatti ogni vertice della foresta ha al piu' un vicino di
etichetta minore (il padre nel suo albero; i vicini in I vengono dopo), quindi
p = 1 per tutti; ogni vertice di I ha tutti e d i vicini nella foresta e quindi
con etichetta minore, e p = d. Il totale e' (2^d - |I|)*1 + |I|*d.

Quindi   U(Q_d) <= 2^d + (d-1) * (minimo |I| ammissibile).

I valori noti sono tutti di questa forma:
    d=3: 8 + 2*3  = 14    d=5: 32 + 4*14 = 88
    d=4: 16 + 3*6 = 34    d=6: 64 + 5*28 = 204  (trovato dalla ricerca locale)

Il programma cerca I piccoli con ricottura simulata e VERIFICA sempre il
risultato in due modi indipendenti: (a) controllo diretto di indipendenza e
aciclicita'; (b) costruzione dell'etichettatura e conteggio dei cammini.

AMBITO. Produce LIMITI SUPERIORI per U(Q_d). Nessuna prova di minimalita'.

Uso:
    python c4_insieme_decycling.py --d 6 --secondi 60
    python c4_insieme_decycling.py --d 7 --secondi 600 --salva q7_set.json
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

NOTI = {3: 14, 4: 34, 5: 88}


def vicini_di(d: int) -> list[tuple[int, ...]]:
    return [tuple(v ^ (1 << i) for i in range(d)) for v in range(1 << d)]


def componenti_e_spigoli(d: int, dentro: list[bool],
                         vicini: list[tuple[int, ...]]) -> tuple[int, int, int]:
    """Su Q_d - I: restituisce (numero vertici, numero spigoli, componenti).

    Union-find senza ricorsione. Q_d - I e' una foresta se e solo se
    spigoli == vertici - componenti.
    """
    padre = list(range(1 << d))

    def trova(x: int) -> int:
        while padre[x] != x:
            padre[x] = padre[padre[x]]
            x = padre[x]
        return x

    n_vertici = sum(dentro)
    n_spigoli = 0
    for v in range(1 << d):
        if not dentro[v]:
            continue
        for u in vicini[v]:
            if u > v and dentro[u]:
                n_spigoli += 1
                ra, rb = trova(v), trova(u)
                if ra != rb:
                    padre[ra] = rb
    radici = {trova(v) for v in range(1 << d) if dentro[v]}
    return n_vertici, n_spigoli, len(radici)


def eccesso_cicli(d: int, insieme: set[int], vicini: list[tuple[int, ...]]) -> int:
    """Quanti spigoli di troppo rispetto a una foresta. Zero = e' una foresta."""
    dentro = [v not in insieme for v in range(1 << d)]
    n_v, n_e, comp = componenti_e_spigoli(d, dentro, vicini)
    return n_e - (n_v - comp)


def coppie_adiacenti(insieme: set[int], vicini: list[tuple[int, ...]]) -> int:
    """Quante coppie adiacenti dentro I. Zero = I e' indipendente."""
    return sum(1 for v in insieme for u in vicini[v] if u in insieme and u > v)


def costo(d, insieme, vicini, peso=60):
    """Vogliamo I piccolo, indipendente e che spezzi tutti i cicli."""
    return (len(insieme)
            + peso * eccesso_cicli(d, insieme, vicini)
            + peso * coppie_adiacenti(insieme, vicini))


def cerca(d: int, secondi: float, seme: int) -> tuple[set[int], int]:
    """Ricottura simulata su sottoinsiemi di vertici."""
    rng = random.Random(seme)
    n = 1 << d
    vicini = vicini_di(d)
    # Partenza: una classe di peso alternata, tipicamente gia' indipendente.
    insieme = {v for v in range(n) if bin(v).count("1") % 2 == 0 and rng.random() < 0.6}
    corrente = costo(d, insieme, vicini)
    migliore_valido, taglia_migliore = None, None

    avvio = time.perf_counter()
    while time.perf_counter() - avvio < secondi:
        frazione = ((time.perf_counter() - avvio) / secondi * 8) % 1.0
        temperatura = 4.0 * (1 - frazione) ** 2 + 0.02
        for _ in range(60):
            v = rng.randrange(n)
            if v in insieme:
                insieme.discard(v)
                annulla = ("aggiungi", v)
            else:
                insieme.add(v)
                annulla = ("togli", v)
            nuovo = costo(d, insieme, vicini)
            if nuovo <= corrente or rng.random() < pow(2.718281828,
                                                       -(nuovo - corrente) / temperatura):
                corrente = nuovo
                if (eccesso_cicli(d, insieme, vicini) == 0
                        and coppie_adiacenti(insieme, vicini) == 0):
                    if taglia_migliore is None or len(insieme) < taglia_migliore:
                        taglia_migliore = len(insieme)
                        migliore_valido = set(insieme)
            else:
                azione, w = annulla
                if azione == "aggiungi":
                    insieme.add(w)
                else:
                    insieme.discard(w)
    return migliore_valido, taglia_migliore


def etichettatura_da_insieme(d: int, insieme: set[int],
                             vicini: list[tuple[int, ...]]) -> list[int]:
    """Foresta prima (ogni albero dalla radice in giu'), poi I."""
    resto = [v for v in range(1 << d) if v not in insieme]
    visitati, ordine = set(), []
    for radice in resto:
        if radice in visitati:
            continue
        coda = [radice]
        visitati.add(radice)
        while coda:  # visita in ampiezza: il padre precede sempre il figlio
            v = coda.pop(0)
            ordine.append(v)
            for u in vicini[v]:
                if u not in insieme and u not in visitati:
                    visitati.add(u)
                    coda.append(u)
    return ordine + sorted(insieme)


def conta_cammini(d: int, ordine: list[int]) -> int:
    """Conteggio esatto indipendente, sulla etichettatura costruita."""
    etichetta = {v: i for i, v in enumerate(ordine)}
    p, totale = {}, 0
    for v in ordine:
        minori = [v ^ (1 << i) for i in range(d)
                  if etichetta[v ^ (1 << i)] < etichetta[v]]
        p[v] = sum(p[u] for u in minori) if minori else 1
        totale += p[v]
    return totale


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--d", type=int, required=True)
    parser.add_argument("--secondi", type=float, default=120)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--salva", type=Path)
    args = parser.parse_args()

    d = args.d
    vicini = vicini_di(d)
    insieme, taglia = cerca(d, args.secondi, args.seed)
    if insieme is None:
        print("Nessun insieme ammissibile trovato nel tempo dato.")
        return

    # Verifica 1: le due proprieta' richieste, controllate direttamente.
    assert coppie_adiacenti(insieme, vicini) == 0, "I non e' indipendente"
    assert eccesso_cicli(d, insieme, vicini) == 0, "Q_d - I non e' una foresta"

    # Verifica 2: costruisco davvero l'etichettatura e conto i cammini.
    ordine = etichettatura_da_insieme(d, insieme, vicini)
    assert sorted(ordine) == list(range(1 << d)), "etichettatura non biiettiva"
    contati = conta_cammini(d, ordine)
    previsti = (1 << d) + (d - 1) * taglia

    print(f"d = {d}   vertici = {1 << d}   |E| = {d * (1 << (d - 1))}")
    print(f"|I| trovato = {taglia}   (I indipendente, Q_d - I foresta: verificati)")
    print(f"formula 2^d + (d-1)|I| = {previsti}")
    print(f"conteggio diretto dei cammini = {contati}   "
          f"{'CONCORDE' if contati == previsti else 'DISCORDE!'}")
    if d in NOTI:
        print(f"valore noto U(Q_{d}) = {NOTI[d]}   -> "
              f"{'ritrovato' if contati == NOTI[d] else 'NON ritrovato'}")
    print(f"\n==> U(Q_{d}) <= {contati}    (limite superiore, non dimostrato minimo)")

    if args.salva:
        args.salva.write_text(json.dumps({
            "d": d, "taglia_I": taglia, "cammini": contati,
            "limite_superiore": contati, "seed": args.seed,
            "insieme_I": [format(v, f"0{d}b") for v in sorted(insieme)],
            "etichettatura": [format(v, f"0{d}b") for v in ordine],
            "convenzione": "coordinata 0 = bit meno significativo, a destra",
            "ambito": "limite superiore; I indipendente e Q_d-I foresta verificati",
        }, indent=2))
        print(f"salvato in {args.salva}")


if __name__ == "__main__":
    main()
