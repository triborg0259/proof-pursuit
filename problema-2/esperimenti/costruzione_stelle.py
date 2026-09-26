"""
costruzione_stelle.py — etichettatura "a stelle" di Q_d e conteggio esatto dei cammini in salita.

Idea (generalizza la costruzione ottima trovata per d=3,4,5): scegli un insieme R di vertici di peso pari a due a due
a distanza >= 4 (un codice a distanza 4 fra le parole di peso pari). Non-picchi = R + tutti i vertici di peso dispari;
picchi = i vertici pari fuori da R. Ordine delle etichette: radici R e dispari isolati (valli), poi i dispari adiacenti
a una radice (foglie: un solo vicino minore), poi i picchi (tutti i vicini minori, ciascuno con p=1).
Totale = (d+1) 2^{d-1} - (d-1)|R|: piu' grande e' R, meglio e'. R = lexicode a distanza 4 (ottimo per d <= 8).
Questo e' un UPPER BOUND per costruzione; non dimostra la minimalita'. Aritmetica intera esatta.
Uso: python3 costruzione_stelle.py 6 7 8
"""
import sys
from conta_cammini import conta_cammini, stringa

peso = lambda v: bin(v).count("1")


def lexicode_pari(d):
    """Parole di peso pari, in ordine lessicografico, tenendo quelle a distanza >= 4 da tutte le precedenti."""
    codice = []
    for v in range(1 << d):
        if peso(v) % 2 == 0 and all(peso(v ^ c) >= 4 for c in codice):
            codice.append(v)
    return codice


def ordine_stelle(d, radici):
    """Lista dei 2^d vertici in ordine crescente di etichetta: valli, foglie, picchi."""
    dispari = [v for v in range(1 << d) if peso(v) % 2 == 1]
    vicini_radici = {r ^ (1 << i) for r in radici for i in range(d)}
    foglie = [v for v in dispari if v in vicini_radici]
    isolati = [v for v in dispari if v not in vicini_radici]
    picchi = [v for v in range(1 << d) if peso(v) % 2 == 0 and v not in radici]
    return radici + isolati + foglie + picchi


if __name__ == "__main__":
    for d in map(int, sys.argv[1:] or ["3", "4", "5", "6", "7", "8"]):
        radici = lexicode_pari(d)
        ordine = ordine_stelle(d, radici)
        totale, p, valli = conta_cammini(ordine, d)
        spigoli = d << (d - 1)
        print(f"d={d}: |R|={len(radici)} totale={totale} = |E|+{totale - spigoli}  valli={len(valli)}  "
              f"formula={(d + 1) * (1 << (d - 1)) - (d - 1) * len(radici)}")
        with open(f"etichettatura_q{d}.txt", "w") as f:
            f.write(",".join(stringa(v, d) for v in ordine) + "\n")
