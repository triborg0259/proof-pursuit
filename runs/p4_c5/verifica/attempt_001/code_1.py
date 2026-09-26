"""Verifica esatta (enumerazione finita) della tabella usata nella prova per k=24 e k=30.

Per ogni l (numero di moduli multipli di p=k-1) calcola il massimo prodotto di l interi
positivi con somma <= n (n = numero di primi < k diversi da p) e lo confronta con k-l.
Perche': la mappa omega e' iniettiva, quindi k-l <= prodotto; se k-l > massimo prodotto
la configurazione e' impossibile. Aritmetica intera esatta.
"""
from itertools import product


def prodotto_massimo(numero_fattori, somma_massima):
    """Massimo prodotto di numero_fattori interi >=1 con somma <= somma_massima (forza bruta)."""
    migliore = 0
    for fattori in product(range(1, somma_massima + 1), repeat=numero_fattori):
        if sum(fattori) <= somma_massima:
            prodotto = 1
            for f in fattori:
                prodotto *= f
            migliore = max(migliore, prodotto)
    return migliore


def tabella(k, numero_primi):
    """Stampa, per l = 3..numero_primi, k-l e il massimo prodotto; segnala i casi non esclusi."""
    for l in range(3, numero_primi + 1):
        massimo = prodotto_massimo(l, numero_primi)
        esito = "escluso (k-l > max)" if k - l > massimo else "NON escluso dal solo pigeonhole"
        print(f"k={k} l={l} k-l={k-l} max_prodotto={massimo} -> {esito}")


tabella(24, 8)   # primi < 24 diversi da 23: 2,3,5,7,11,13,17,19
tabella(30, 9)   # primi < 30 diversi da 29: 2,3,5,7,11,13,17,19,23
