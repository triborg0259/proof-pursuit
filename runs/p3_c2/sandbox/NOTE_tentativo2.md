# p3_c2 — tentativo 2 (Researcher)
- Trovata la fonte primaria: Griggs & Ho, "The cycling of partitions and compositions under repeated shifts",
  Adv. Appl. Math. 21 (1998) 205-227, PDF dalla homepage dell'autore (people.math.sc.edu/griggs/cycling.pdf,
  salvato come griggs_ho_cycling.pdf / .txt, LETTO: Sezioni 2-3).
- La stima superiore D_B(T_k) <= k^2-k e' il loro Teorema 3.7, via la successione c_i = numero di parti di
  B^{i-1}(lambda) e il pattern (x-1, x, ..., x, x+1) (Lemmi 3.3-3.6). Prova riscritta per intero e con i passi
  omessi nell'originale esplicitati (induzione "continue this process" del Lemma 3.5; conteggio finale
  p <= x(q-p-1)).
- verifica_lemmi_sequenza.py: controllo esaustivo esatto delle NOSTRE riformulazioni dei lemmi su tutte le
  partizioni di n <= 24 e del Lemma 3.3 per k = 3..7 (8.6 s). Non e' una prova: serve contro errori di trascrizione.
- Convergenza a delta_k e unicita' della partizione ciclica: dimostrate con la regola delle celle (Lemma 1 del
  tentativo 1), il potenziale W e l'argomento CRT buco/cella (come nel Teorema 2.1 di Griggs-Ho).
