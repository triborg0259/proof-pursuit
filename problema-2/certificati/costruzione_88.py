"""Costruzione esplicita con 88 cammini in salita su Q_5 e verifica esatta.

Idea: picchi = tutti i vertici di peso pari tranne 00000 e 11110 (14 picchi, indipendenti);
il complemento (2 pari + 16 dispari) e' una foresta con 10 spigoli e 8 componenti:
etichettiamo prima le 8 radici (valli), poi le foglie, poi i picchi. Ogni non-picco ha p = 1,
ogni picco ha p = 5: totale 18 + 14*5 = 88.
"""
from conta_cammini import conta_cammini, stringa, da_stringa

D = 5
N = 1 << D
peso = lambda v: bin(v).count("1")
radici = [da_stringa("00000"), da_stringa("11110")]
dispari = [v for v in range(N) if peso(v) % 2 == 1]
foglie = [v for v in dispari if any(v ^ r in [1 << i for i in range(D)] for r in radici)]
isolati = [v for v in dispari if v not in foglie]
picchi = [v for v in range(N) if peso(v) % 2 == 0 and v not in radici]
ordine = radici + isolati + foglie + picchi

if __name__ == "__main__":
    tot, p, valli = conta_cammini(ordine, D)
    print("totale cammini:", tot)
    print("valli:", [stringa(v, D) for v in valli])
    print("ordine:", ",".join(stringa(v, D) for v in ordine))
