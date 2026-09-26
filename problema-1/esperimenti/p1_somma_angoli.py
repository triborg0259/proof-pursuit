"""
Obiettivo per tools/autoloop.py — Problema 1, sanity check numerico (NON una prova).

IPOTESI DI LAVORO (S non ancora definita nel testo ricevuto):
    S(l_1..l_N) = somma su coppie non ordinate {i,j} dell'angolo non orientato in [0, pi/2] fra l_i e l_j.
Rette parametrizzate dalla direzione theta in [0, pi). Angolo(theta_i, theta_j) = min(d, pi - d), d = |theta_i - theta_j|.

Valore congetturato del massimo: (pi/2) * floor(N^2/4).

Uso:
    python3 tools/autoloop.py problema-1/esperimenti/p1_somma_angoli.py --budget 5 --seed 1 -- N
"""
import math, random

PI = math.pi


def setup(argv):
    N = int(argv[0]) if argv else 6
    return {"N": N}


def target(ctx):
    N = ctx["N"]
    return (PI / 2) * (N * N // 4)


def random_candidate(rng, ctx):
    return [rng.uniform(0, PI) for _ in range(ctx["N"])]


def mutate(x, rng, ctx, temp):
    y = list(x)
    i = rng.randrange(len(y))
    if rng.random() < 0.15:
        y[i] = rng.uniform(0, PI)                  # salto globale
    else:
        y[i] = (y[i] + rng.gauss(0, 0.5 * temp)) % PI   # perturbazione locale
    return y


def score(x, ctx):
    s = 0.0
    n = len(x)
    for i in range(n):
        for j in range(i + 1, n):
            d = abs(x[i] - x[j])
            s += min(d, PI - d)
    return s


def describe(x, ctx):
    return [round(t, 4) for t in x]
