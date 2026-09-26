#!/usr/bin/env python3
"""
autoloop.py — harness di ricerca "proponi / valuta / tieni se migliora" (pattern autoresearch), v2.

Uso:
    .venv/bin/python tools/autoloop.py <obiettivo.py> [--budget SEC] [--seeds K] [--workers W]
                                        [--restarts R] [--ledger FILE] [--tag T] [-- args...]

Il modulo obiettivo deve esporre:
    setup(argv) -> ctx
    random_candidate(rng, ctx) -> x
    mutate(x, rng, ctx, temp) -> x'          (mosse locali + mosse strutturate; temp decresce 1 -> 0)
    score(x, ctx) -> float                    (da MASSIMIZZARE, float)
    describe(x, ctx) -> obj serializzabile
    target(ctx) -> float | None               (valore congetturato, solo per confronto)
  opzionali:
    certify(x, ctx) -> dict                   (ricalcolo ad alta precisione / struttura del candidato)

Cosa fa:
  1. lancia K seed indipendenti in parallelo (multiprocessing), ciascuno con hill climbing a restart
     e budget di tempo fisso; regola: un candidato sostituisce il corrente SOLO se il punteggio migliora;
  2. prende il migliore fra i seed, lo ricertifica con certify() (es. mpmath a 40 cifre);
  3. appende una riga JSON al ledger con: tag, argomenti, seed, budget, iterazioni, best, target, gap,
     candidato, certificazione, timestamp. Il ledger è l'unica fonte per le tabelle nei README.

Aritmetica float nella ricerca: i risultati sono SOLO indicativi, mai una prova.
"""
import argparse, importlib.util, json, math, os, random, sys, time
from multiprocessing import Pool


def load_module(path):
    spec = importlib.util.spec_from_file_location("objective", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def climb(args):
    path, argv, seed, budget, restarts = args
    mod = load_module(path)
    ctx = mod.setup(argv)
    rng = random.Random(seed)
    t0 = time.time()
    best_x, best_s, it = None, -math.inf, 0
    per = budget / max(1, restarts)
    for r in range(restarts):
        if time.time() - t0 >= budget:
            break
        x = mod.random_candidate(rng, ctx); s = mod.score(x, ctx)
        tr0 = time.time()
        while time.time() - tr0 < per and time.time() - t0 < budget:
            it += 1
            temp = max(1e-3, 1.0 - (time.time() - tr0) / per)
            y = mod.mutate(x, rng, ctx, temp); sy = mod.score(y, ctx)
            if sy > s:
                x, s = y, sy
        if s > best_s:
            best_x, best_s = x, s
    return {"seed": seed, "iters": it, "score": best_s, "x": best_x, "elapsed": round(time.time() - t0, 2)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("objective")
    ap.add_argument("--budget", type=float, default=20.0, help="secondi per seed")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=1)
    ap.add_argument("--workers", type=int, default=min(8, os.cpu_count() or 1))
    ap.add_argument("--restarts", type=int, default=10)
    ap.add_argument("--ledger", default="ledger.jsonl")
    ap.add_argument("--tag", default="")
    a, argv = ap.parse_known_args()
    argv = [t for t in argv if t != "--"]

    mod = load_module(a.objective)
    ctx = mod.setup(argv)
    tgt = mod.target(ctx) if hasattr(mod, "target") else None

    jobs = [(a.objective, argv, a.seed0 + k, a.budget, a.restarts) for k in range(a.seeds)]
    t0 = time.time()
    with Pool(min(a.workers, a.seeds)) as pool:
        runs = pool.map(climb, jobs)
    wall = round(time.time() - t0, 2)
    best = max(runs, key=lambda r: r["score"])
    cert = mod.certify(best["x"], ctx) if hasattr(mod, "certify") else None

    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "tag": a.tag, "objective": os.path.basename(a.objective),
           "args": argv, "seeds": [r["seed"] for r in runs], "budget_per_seed_s": a.budget,
           "restarts": a.restarts, "wall_s": wall, "iters_total": sum(r["iters"] for r in runs),
           "per_seed_scores": [round(r["score"], 9) for r in runs],
           "best_score": best["score"], "target": tgt,
           "gap_target_minus_best": (None if tgt is None else tgt - best["score"]),
           "best": mod.describe(best["x"], ctx), "certify": cert}
    with open(a.ledger, "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
