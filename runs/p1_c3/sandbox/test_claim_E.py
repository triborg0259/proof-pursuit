"""Esplorazione numerica (float, NON prova) della "Claim E(m)":
per m versori in R^{m-1} esistono a != b tali che, con R = gli altri m-2,
   sum_{i in R} delta(x_a,x_i) + delta(x_a,x_b) >= angolo(x_b, span R) = pi/2 - delta(x_b, span R).
Si minimizza max_{a!=b} margine su configurazioni casuali con ottimizzazione locale.
"""
import sys
import numpy as np
from scipy.optimize import minimize
from test_lemma_L import unit, delta_vec, delta_sub, rng

def margin_E(params, m):
    n = m - 1
    xs = [unit(params[i*n:(i+1)*n]) for i in range(m)]
    best = -np.inf
    for a in range(m):
        for b in range(m):
            if a == b:
                continue
            R = [xs[i] for i in range(m) if i not in (a, b)]
            lhs = sum(delta_vec(xs[a], xi) for xi in R) + delta_vec(xs[a], xs[b])
            rhs = np.pi/2 - delta_sub(xs[b], R)
            best = max(best, lhs - rhs)
    return best

def search(m, trials):
    worst, worstp = np.inf, None
    for _ in range(trials):
        p0 = rng.normal(size=m*(m-1))
        res = minimize(margin_E, p0, args=(m,), method="Powell",
                       options={"maxiter": 3000, "xtol": 1e-8, "ftol": 1e-12})
        if res.fun < worst:
            worst, worstp = res.fun, res.x
    return worst, worstp

for m in [3, 4, 5, 6]:
    w, p = search(m, 30)
    print(f"m={m}: min over configs of max_(a,b) margin = {w:+.5f}", flush=True)
    if w < -1e-4:
        n = m - 1
        print("  esempio:", [unit(p[i*n:(i+1)*n]).round(3).tolist() for i in range(m)])
