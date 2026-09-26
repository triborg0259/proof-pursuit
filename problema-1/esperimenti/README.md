# Problema 1 — esperimenti

## E1 — sanity check numerico del massimo congetturato (2026-09-26)

**Scopo:** verificare, sotto l'ipotesi di lavoro su $S$ (somma degli angoli in $[0,\pi/2]$ su coppie non ordinate),
che il massimo numerico di $S$ per $N$ rette nel piano coincida con $\frac{\pi}{2}\lfloor N^2/4\rfloor$.
**NON è una prova.** Aritmetica float, ricerca euristica (hill climbing con restart).

**Comando (riproducibile):**
```
for N in 2 3 4 5 6 7 8 9 10; do
  python3 tools/autoloop.py problema-1/esperimenti/p1_somma_angoli.py \
      --budget 3 --seed 1 --restarts 10 --log problema-1/esperimenti/p1_log_N$N.jsonl -- $N
done
```
Python 3.14.7, nessuna dipendenza. Tempo: 3 s per N, 27 s totali. Spazio: $\theta\in[0,\pi)^N$.

**Risultati (seed 1):**

| N | best trovato | target $\frac{\pi}{2}\lfloor N^2/4\rfloor$ | gap | iterazioni |
|---|---|---|---|---|
| 2 | 1.570796 | 1.570796 | 1.9e-08 | 4.0M |
| 3 | 3.141593 | 3.141593 | ~0 | 3.3M |
| 4 | 6.283185 | 6.283185 | 4.7e-08 | 2.4M |
| 5 | 9.424778 | 9.424778 | ~0 | 2.1M |
| 6 | 14.137166 | 14.137167 | 1.3e-06 | 1.7M |
| 7 | 18.849556 | 18.849556 | ~0 | 1.4M |
| 8 | 25.132737 | 25.132741 | 4.1e-06 | 1.1M |
| 9 | 31.415927 | 31.415927 | ~0 | 1.0M |
| 10 | 39.269889 | 39.269908 | 1.9e-05 | 0.8M |

Nessun valore supera il target (entro l'errore float). I gap positivi sono convergenza incompleta, non evidenza contro.

**Osservazione rilevante:** i massimizzatori trovati NON sono la configurazione "due direzioni perpendicolari".
Es. $N=3$: tre rette a $60°$ danno $\pi$, uguale al target. Il massimo è raggiunto su un insieme "piatto" di
configurazioni. Interpretazione (vedi note.md, approccio E): il massimo è raggiunto esattamente quando ogni
"taglio" del fascio di direzioni separa le rette il più equamente possibile. Utile se una parte successiva
chiede i casi di uguaglianza.
