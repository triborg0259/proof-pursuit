# Problema 1 — fonti verificate

## [BM18] D. Bilyk, R. W. Matzke, "On the Fejes Tóth problem about the sum of angles between lines",
arXiv:1801.07837 (2018); versione pubblicata Proc. AMS 147 (2019). File: `BilykMatzke2018_arXiv1801.07837.pdf`
(+ estrazione testo `BilykMatzke2018.txt`). **Letto** (introduzione, §3, §4) il 2026-09-26.

**Convenzione:** loro $S^d\subset\mathbb{R}^{d+1}$; il nostro $d$ (dimensione ambiente) = loro $d+1$.
Energia normalizzata $E(Z)=\frac{1}{N^2}\sum_{i,j}\arccos|z_i\cdot z_j|$, quindi $S = \frac{N^2}{2}E(Z)$.

**Cosa dichiarano noto (con loro attribuzioni):**
- Caso $S^1$ (= nostre rette in $\mathbb{R}^2$, **parte 1**): dimostrato in [9] Fodor–Vígh–Zarnócz (2016) e [10];
  in §4 BM18 danno tre prove alternative: espansione in polinomi di Chebyshev (coefficienti $\tilde F_n\le0$),
  serie di Fourier, principio di Stolarsky per quadranti. Quest'ultimo è essenzialmente il nostro approccio E.
- $S^2$ (= $\mathbb{R}^3$): Fejes Tóth 1959 ha confermato la congettura per $N\le6$ ⇒ "5 rette in $\mathbb{R}^3$"
  (**metà della parte 4**) è un risultato del 1959. Non abbiamo letto l'articolo originale [8]; la prova va
  comunque prodotta da noi.
- Bound generali: Thm 1.3, $\max I(\mu)\le\frac{\pi}{2}-\frac{69}{50(d+1)}$ su $S^d$, $d\ge2$ (via "frame potential").
- Prop. 3.1 (riduzione dimensionale): se la congettura continua vale su $S^d$ vale anche su $S^{d-1}$.
- Frase chiave: "the only settled case of the conjecture: d = 1" (cioè solo il piano). ⇒ **Parti 3, 5, 6 e la
  metà "6 rette in $\mathbb{R}^4$" della parte 4 NON risultano dimostrate in letteratura a questa data (2018).**
  Da controllare se lavori 2019–2026 (Bilyk–Glazyrin–Matzke–Park–Vlasiuk; Lim–McCann) abbiano chiuso $N=d+1$.

## [LM20] Y. Lim, R. McCann, "On Fejes Tóth's conjectured maximizer for the sum of angles between lines"
(preprint, math.utoronto.ca/mccann/papers/LimMcCann20a.pdf). **NON ancora letto.** Titolo suggerisce
risultati di massimalità locale / caratterizzazione del massimizzatore congetturato.

## [FVZ16] G. Fodor, V. Vígh, T. Zarnócz, "On the angle sum of lines", Arch. Math. (2016?) — citato da BM18 come [9].
**NON letto.** Contiene la prova del caso planare e il bound $E\le 3\pi/8$ su $S^2$.
