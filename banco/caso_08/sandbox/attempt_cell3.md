# Problema 4, parte 3 — tentativo (Researcher)

Tesi: per ogni 3 <= k <= 8, k classi a due a due disgiunte hanno una coppia con gcd(m_i,m_j) >= k.

Struttura: Lemma 1 (riduzione ai moduli che dividono 420, gcd preservati) + ricerca esaustiva
delle k-clique nel grafo di compatibilita' su 1343 classi (nessuna potatura oltre la definizione),
0 sopravvissuti per k=3..8, conteggi riproducibili, controllo di non vacuita' (soglia k),
seconda implementazione indipendente concorde. Prove a mano per k=3 e k=4 incluse.

File: ricerca_clique_420.py (impl. 1), ricerca_moduli_residui.py (impl. 2),
run1.txt/run2.txt (conteggi), non_vacuita*.txt, impl2_*.txt.
Testo completo della prova: vedi output JSON del Researcher (campo proof_attempt).
