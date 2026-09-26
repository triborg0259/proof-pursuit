"""Certificato per la caratterizzazione delle partizioni estremali di n = T_k - 1.

Cosa fa: per ogni k in [4, KMAX] calcola d_B su TUTTE le partizioni di n = T_k - 1 (interi
esatti) e verifica:
  (1) D_B(n) = k^2 - 2k - 1;
  (2) {lam : d_B(lam) = D_B(n)} == {lam : B^{k^2-3k-1}(lam) = nu_k},
      con nu_k = (k-1, k-1, k-1, k-3, k-4, ..., 2);
  (3) d_B(nu_k) = k  e  lambda*_k = (k-1, k-2, k-2, ..., 1, 1) e' estremale.
Perche': la cella 3 chiede quali partizioni raggiungono il massimo; per k = 4 questo
calcolo e' parte della prova (caso non coperto dall'argomento generale), per k >= 5 e' solo
un controllo indipendente della dimostrazione.
Insieme finito coperto: tutte le partizioni di T_k - 1 per 4 <= k <= KMAX.
"""
import sys
import time
from db_table import distanze_dal_ciclo, shift


def nu(k):
    """La partizione collo di bottiglia nu_k = (k-1, k-1, k-1, k-3, ..., 2)."""
    return tuple([k - 1] * 3 + list(range(k - 3, 1, -1)))


def lambda_star(k):
    """La partizione estremale esplicita di Griggs-Ho (k-1, k-2, k-2, ..., 1, 1)."""
    return tuple([k - 1, k - 2] + list(range(k - 2, 0, -1)) + [1])


def potenza_shift(lam, j):
    for _ in range(j):
        lam = shift(lam)
    return lam


def verifica(k):
    n, t0 = k * (k + 1) // 2 - 1, time.time()
    d = distanze_dal_ciclo(n)
    D = max(d.values())
    estremali = {lam for lam, v in d.items() if v == D}
    j = k * k - 3 * k - 1
    preimmagini = {lam for lam in d if potenza_shift(lam, j) == nu(k)}
    ok = (D == k * k - 2 * k - 1 and estremali == preimmagini
          and d[nu(k)] == k and lambda_star(k) in estremali)
    print(f"k={k} n={n} #partizioni={len(d)} D_B={D} #estremali={len(estremali)} "
          f"nu_k={nu(k)} d_B(nu_k)={d[nu(k)]} j={j} caratterizzazione_ok={ok} "
          f"t={time.time()-t0:.1f}s", flush=True)
    return ok


if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print("tutto ok:", all([verifica(k) for k in range(4, kmax + 1)]))
