"""
Obiettivo per tools/autoloop.py — Problema 1 in R^d: massimizzare S = sum_{i<j} arccos|<x_i,x_j>|
su N rette per l'origine (versori x_i in R^d).  Uso:  ... lines_Rd.py -- d N

Mosse (mutate):
  - locale: perturbazione gaussiana di un versore, ampiezza ~ temp;
  - strutturate (utili perché l'ottimo congetturato è "a spigoli": coppie ortogonali o coincidenti):
      * copia: x_i <- ±x_j;
      * ortogonalizza: x_i <- componente di x_i ortogonale a un sottoinsieme casuale degli altri;
      * salto: x_i <- versore casuale.
Target: congettura di Fejes Tóth, d direzioni ortogonali usate floor(N/d) o ceil(N/d) volte:
  S* = (pi/2) * [ C(N,2) - sum_a C(n_a,2) ]  con n_a le molteplicità.
certify(): ricalcolo di S con mpmath a 40 cifre + matrice |<x_i,x_j>| arrotondata, per leggere la struttura.
"""
import math, random
import numpy as np

PI = math.pi


def setup(argv):
    d, N = int(argv[0]), int(argv[1])
    return {"d": d, "N": N}


def target(ctx):
    d, N = ctx["d"], ctx["N"]
    q, r = divmod(N, d)
    mult = [q + 1] * r + [q] * (d - r)
    return (PI / 2) * (N * (N - 1) // 2 - sum(n * (n - 1) // 2 for n in mult))


def _unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else None


def random_candidate(rng, ctx):
    d, N = ctx["d"], ctx["N"]
    X = np.array([[rng.gauss(0, 1) for _ in range(d)] for _ in range(N)])
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def mutate(x, rng, ctx, temp):
    d, N = ctx["d"], ctx["N"]
    Y = x.copy()
    i = rng.randrange(N)
    u = rng.random()
    if u < 0.6:
        v = _unit(Y[i] + np.array([rng.gauss(0, 0.6 * temp) for _ in range(d)]))
    elif u < 0.75 and N > 1:
        j = rng.randrange(N - 1); j += (j >= i)
        v = Y[j] * (1 if rng.random() < 0.5 else -1)
    elif u < 0.92:
        k = rng.randint(1, min(d - 1, N - 1)) if N > 1 and d > 1 else 0
        others = [j for j in range(N) if j != i]
        sub = rng.sample(others, k) if k else []
        v = Y[i].copy()
        if sub:
            B = Y[sub]
            Q, _ = np.linalg.qr(B.T)
            v = v - Q @ (Q.T @ v)
        v = _unit(v)
        if v is None:
            v = _unit(np.array([rng.gauss(0, 1) for _ in range(d)]))
    else:
        v = _unit(np.array([rng.gauss(0, 1) for _ in range(d)]))
    if v is not None:
        Y[i] = v
    return Y


def score(x, ctx):
    G = np.abs(x @ x.T)
    np.clip(G, 0.0, 1.0, out=G)
    iu = np.triu_indices(len(x), 1)
    return float(np.sum(np.arccos(G[iu])))


def describe(x, ctx):
    return [[round(float(t), 6) for t in row] for row in x]


def certify(x, ctx):
    import mpmath as mp
    mp.mp.dps = 40
    X = [[mp.mpf(float(t)) for t in row] for row in x]
    X = [[t / mp.sqrt(sum(s * s for s in row)) for t in row] for row in X]
    N = len(X)
    S = mp.mpf(0)
    G = [[0.0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            ip = abs(sum(X[i][k] * X[j][k] for k in range(len(X[i]))))
            G[i][j] = round(float(ip), 4)
            if j > i:
                S += mp.acos(min(ip, mp.mpf(1)))
    tgt = target(ctx)
    near0 = sum(1 for i in range(N) for j in range(i + 1, N) if G[i][j] < 1e-3)
    near1 = sum(1 for i in range(N) for j in range(i + 1, N) if G[i][j] > 1 - 1e-3)
    return {"S_mp40": mp.nstr(S, 20), "target": mp.nstr(mp.mpf(tgt), 20),
            "abs_gram_rounded": G,
            "summary": f"pairs ~orth={near0}, ~coinc={near1}, other={N*(N-1)//2-near0-near1}"}
