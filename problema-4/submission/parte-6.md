# Problema 4 — Parte 6 — bozza di consegna PARZIALE

**Stato dichiarato: PARZIALE.** Nessuna soluzione completa: qui sotto ciò che è stabilito, la formalizzazione,
la posizione rispetto alla letteratura e ciò che resta aperto. Nulla è dichiarato dimostrato oltre quanto scritto.

## 1. Risultato e ambito
**Richiesta ufficiale.**
## Parte 6 (C6) — Beyond the boundary

**Punteggio:** 13 points · **Valutazione:** Judged · **Open question**

Three directions beyond the certified range; any one of them counts. Any of the following.

(a) Decide a size $k \ge 25$.

(b) The asymptotic form. It is known that a pairwise disjoint family of size $k$ always has a pair with
$$
\gcd(m_i, m_j) \;\ge\; k \cdot \exp\!\left( -(2 + o(1)) \frac{\log k}{\log\log k} \right),
$$
which is $k^{1 - o(1)}$ but not linear in $k$. Prove the statement in full, or prove the weaker bound
$\gcd(m_i, m_j) \ge ck$ for some absolute constant $c > 0$, or improve the exponential factor above.

(c) The group form. Let $G$ be a group, let $G_1, \ldots, G_k$ be subgroups of finite index $n_i = [G : G_i]$,
and let $x_1 G_1, \ldots, x_k G_k$ be pairwise disjoint cosets. Is there a pair $i < j$ with
$\gcd(n_i, n_j) \ge k$? This is known for $k \le 5$ and open for every $k \ge 6$; settling $k = 6$ counts as
progress.

*(Fine del problema 4. Punteggi: 1+2+3+5+8+13 = 32.)*

**Cosa consegniamo.** Nessuna prova. Segnalazione rilevante: il bound asintotico citato nell'enunciato è già stato migliorato in letteratura.

## 2. Dimostrazione
Fornal–Sun [2607.24655] (luglio 2026) dimostrano $\max\gcd(m_i,m_j)\gg k\exp(-(2+o(1))\sqrt{\log k/\log\log k})$, con radice quadrata all'esponente: un miglioramento del fattore esponenziale richiesto in (b). Riprodurre la loro prova per esteso (grafo dei gcd, lemma strutturale, partizione crivellante, inversione di Möbius, trasformata di Fourier discreta) conterebbe secondo le regole; non fatto.

## 3. Verifica: istruzioni, dipendenze, tempi
Codice disponibile (Python 3, libreria standard; ogni script gira in meno di un minuto):
- Nessun codice ancora.

## 4. Fonti e contributo
Letteratura arXiv (ricerca deterministica `tools/cerca_letteratura.sh`, abstract letti, non usata come prova):
- arXiv:2603.26043v1 — Finiteness of Disjoint Covering Systems with Precisely One Repeated Modulus (Yu Hashimoto, 2026); solo abstract letto.
- arXiv:1511.04293v1 — Searching for Disjoint Covering Systems with Precisely One Repeated Modulus (Shalosh B. Ekhad, Aviezri S. Fraenkel, Doron Zeilberger, 2015); solo abstract letto.
- arXiv:2607.24655v1 — On the problem of large gcd for disjoint residue classes (Jan Fornal, Yu-Chen Sun, 2026); solo abstract letto.
- arXiv:2608.15873v1 — Two Questions on $G$-harmonic Tuples (Murali Menon, 2026); solo abstract letto.
[2607.24655].

## 5. Limiti e parti irrisolte
Tutto; la via (b) via riproduzione della prova è quella indicata.
