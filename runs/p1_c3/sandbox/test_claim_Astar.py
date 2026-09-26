"""Esplorazione numerica (float, NON prova) del Lemma A*(k):
   sum_i delta(x,x_i) + angolo(x,U) >= min_t angolo(x_t, span(x_i: i!=t)),
con U = span(x_1..x_k). Minimizza il margine su configurazioni casuali (Powell).
"""
import numpy as np
from scipy.optimize import minimize
from test_lemma_L import unit, delta_vec, delta_sub, rng

def margin_Astar(params, k, n):
    vs = [unit(params[i*n:(i+1)*n]) for i in range(k+1)]
    x, xs = vs[0], vs[1:]
    angle_x_U = np.pi/2 - delta_sub(x, xs)
    mu = min(np.pi/2 - delta_sub(xs[t], [xs[i] for i in range(k) if i != t]) for t in range(k))
    return sum(delta_vec(x, xi) for xi in xs) + angle_x_U - mu

for k, n in [(2, 3), (3, 3), (3, 4), (4, 4), (4, 5), (5, 5)]:
    worst = np.inf
    for _ in range(25):
        res = minimize(margin_Astar, rng.normal(size=(k+1)*n), args=(k, n), method="Powell",
                       options={"maxiter": 2000, "xtol": 1e-8, "ftol": 1e-12})
        worst = min(worst, res.fun)
    print(f"k={k} n={n}: min margine A* = {worst:+.6f}", flush=True)
