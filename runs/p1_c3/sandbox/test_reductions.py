"""Esplorazione numerica (float, NON prova) di riduzioni induttive per L(k).

Per la configurazione (x; x_1..x_k) e per ogni scelta dell'indice t da staccare:
  B_t = delta(x,x_t) + sum_{i!=t} delta(x_i,x_t) - [delta(x,U) - delta(x,U_t')]
  A_t = sum_i delta(x,x_i) - [delta(x,U) - delta(x_t,U_t')]
con U_t' = span degli altri. L(k) segue da L(k-1) se esiste t con B_t>=0 oppure A_t>=0.
Si cerca il minimo di max_t B_t, max_t A_t, e del massimo congiunto.
"""
import numpy as np
from scipy.optimize import minimize
from test_lemma_L import unit, delta_vec, delta_sub, rng

def margins(params, k, n):
    vs = [unit(params[i*n:(i+1)*n]) for i in range(k+1)]
    x, xs = vs[0], vs[1:]
    dU = delta_sub(x, xs)
    A, B = [], []
    for t in range(k):
        others = [xs[i] for i in range(k) if i != t]
        B.append(delta_vec(x, xs[t]) + sum(delta_vec(xi, xs[t]) for xi in others)
                 - (dU - delta_sub(x, others)))
        A.append(sum(delta_vec(x, xi) for xi in xs) - (dU - delta_sub(xs[t], others)))
    return max(B), max(A)

def search(which, k, n, trials):
    best, bestp = np.inf, None
    for _ in range(trials):
        p0 = rng.normal(size=(k+1)*n)
        fun = lambda p: margins(p, k, n)[which] if which < 2 else max(margins(p, k, n))
        res = minimize(fun, p0, method="Nelder-Mead",
                       options={"maxiter": 4000, "xatol": 1e-9, "fatol": 1e-12})
        if res.fun < best:
            best, bestp = res.fun, res.x
    return best, bestp

for k, n in [(2, 3), (3, 3), (3, 4), (4, 4), (4, 5)]:
    bB, pB = search(0, k, n, 40)
    bA, _ = search(1, k, n, 40)
    bAB, _ = search(2, k, n, 40)
    print(f"k={k} n={n}  min max_t B_t: {bB:+.5f}   min max_t A_t: {bA:+.5f}   min max(A,B): {bAB:+.5f}", flush=True)
    if bB < -1e-3:
        vs = [unit(pB[i*n:(i+1)*n]) for i in range(k+1)]
        np.set_printoptions(precision=3, suppress=True)
        print("   esempio B fallisce:", [v.round(3).tolist() for v in vs])
