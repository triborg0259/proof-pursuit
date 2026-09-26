"""Esplorazione numerica (float, NON prova) di due enunciati candidati.

L(k):  per versori x, x_1..x_k:  sum_i delta(x,x_i) + sum_{i<j} delta(x_i,x_j) >= delta(x, span(x_i))
A'(k): se x_k e' il piu' vicino a x (|<x,x_k>| massimo):
       sum_i delta(x,x_i) >= delta(x, U) - delta(x_k, span(altri))
dove delta(x,y)=arcsin|<x,y>| e delta(x,W)=arcsin ||P_W x||.
Cerca il minimo del margine con ottimizzazione locale casuale.
"""
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(1)

def unit(v):
    return v / np.linalg.norm(v)

def delta_vec(x, y):
    return np.arcsin(min(1.0, abs(x @ y)))

def delta_sub(x, basis_vectors):
    """arcsin della norma della proiezione di x su span(basis_vectors)."""
    if len(basis_vectors) == 0:
        return 0.0
    M = np.array(basis_vectors).T
    q, _ = np.linalg.qr(M)
    r = np.linalg.matrix_rank(M, tol=1e-9)
    q = q[:, :r]
    return np.arcsin(min(1.0, np.linalg.norm(q.T @ x)))

def margin_L(params, k, n):
    vs = [unit(params[i*n:(i+1)*n]) for i in range(k+1)]
    x, xs = vs[0], vs[1:]
    lhs = sum(delta_vec(x, xi) for xi in xs)
    lhs += sum(delta_vec(xs[i], xs[j]) for i in range(k) for j in range(i+1, k))
    return lhs - delta_sub(x, xs)

def margin_A(params, k, n):
    vs = [unit(params[i*n:(i+1)*n]) for i in range(k+1)]
    x, xs = vs[0], vs[1:]
    kk = int(np.argmax([abs(x @ xi) for xi in xs]))
    others = [xs[i] for i in range(k) if i != kk]
    lhs = sum(delta_vec(x, xi) for xi in xs)
    return lhs - (delta_sub(x, xs) - delta_sub(xs[kk], others))

def search(fun, k, n, trials):
    best = np.inf
    for _ in range(trials):
        p0 = rng.normal(size=(k+1)*n)
        res = minimize(fun, p0, args=(k, n), method="Nelder-Mead",
                       options={"maxiter": 4000, "xatol": 1e-9, "fatol": 1e-12})
        best = min(best, res.fun)
    return best

for k, n in [(2, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)]:
    print(f"k={k} n={n}  min margine L: {search(margin_L, k, n, 60):+.5f}"
          f"   min margine A': {search(margin_A, k, n, 60):+.5f}", flush=True)
