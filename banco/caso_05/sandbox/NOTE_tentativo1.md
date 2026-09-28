# p3_c2 — tentativo 1 (Researcher)
- Valori esatti: D_B(T_k) = k^2-k per k<=9 (calcola_DB_triangolari.py, esaustivo, 0.5 s).
- Estremale di Igusa gamma_k=(k-1,k-1,k-2,...,2,1,1) (Hopkins, CMJ 43 (2012), letto): dimostrata d_B(gamma_k)=k^2-k
  tramite la "regola delle celle": con s = numero di pile, celle (i,1)->(1,i), (i,h)->(i+1,h-1) per 2<=h<=s+1,
  (i,h)->(i,h-1) per h>=s+2. Tracce diagonali d=i+h-1 ruotano; le celle sopra altezza s+1 scendono di una diagonale.
- Bound superiore generale: NON dimostrato. Nessuna fonte accessibile con la prova (Igusa/Etienne/Griggs-Ho paywall;
  Hopkins, Drensky, Mestrovic, Pham, Jonsson: solo citazioni).
- Dati: dopo t_stab = T_{k-1}-(k-2) il numero di pile e' in {k-1,k,k+1} (k<=8, esplora_m.py).
