# Problema 4 — Parte 1 — bozza di consegna

**Stato dichiarato: RISOLTA (approvata).** Prova completa scritta dal team; Referee automatico READY_FOR_HUMAN
(giudice A matematica PASS, giudice B evidenze PASS); approvazione umana registrata in `runs/p4_c1/approval.json`.

## 1. Risultato e ambito
Tre classi disgiunte: l'enunciato della parte è dimostrato integralmente, nella generalità richiesta (vedi la prova per le
ipotesi esatte). Nessun calcolo al computer è necessario.

## 2. Dimostrazione
# Cell 1: three pairwise disjoint classes have a pair of moduli with $\gcd\ge3$

**Target.** If $a_1\ (\mathrm{mod}\ m_1)$, $a_2\ (\mathrm{mod}\ m_2)$, $a_3\ (\mathrm{mod}\ m_3)$ are pairwise disjoint congruence classes ($m_i\ge1$), then $\gcd(m_i,m_j)\ge3$ for some $i<j$.

## Lemma 0 (the direction of $(*)$ that we use)
Let $g=\gcd(m,m')$. If $g\mid a-a'$ then the classes $a\ (\mathrm{mod}\ m)$ and $a'\ (\mathrm{mod}\ m')$ have a common element. Equivalently: if the two classes are disjoint then $g\nmid a-a'$.
*Proof.* Write $m=g\mu$, $m'=g\mu'$ with $\gcd(\mu,\mu')=1$, and $a-a'=g\delta$ with $\delta\in\mathbb Z$. An element of the first class has the form $a+mt=a+g\mu t$, $t\in\mathbb Z$; it lies in the second class iff $m'\mid a+g\mu t-a'$, i.e. $g\mu'\mid g(\delta+\mu t)$, i.e. $\mu'\mid\delta+\mu t$. Since $\gcd(\mu,\mu')=1$, $\mu$ is invertible modulo $\mu'$, so $t\equiv-\delta\mu^{-1}\pmod{\mu'}$ solves it. $\square$
(This is the statement $(*)$ quoted in the problem; we include the short proof so that the argument is self-contained.)

## Proof of the cell
Let the three classes be pairwise disjoint and suppose, for a contradiction, that $\gcd(m_i,m_j)\le2$ for all three pairs.
1. *Every pairwise gcd equals $2$.* If $\gcd(m_i,m_j)=1$ then $1\mid a_i-a_j$, so by Lemma 0 the classes $i$ and $j$ meet, contradicting disjointness. Hence $\gcd(m_i,m_j)=2$ for all $i<j$.
2. *The residues are pairwise of different parity.* For $i<j$, disjointness and Lemma 0 give $\gcd(m_i,m_j)=2\nmid a_i-a_j$, i.e. $a_i\not\equiv a_j\pmod 2$.
3. *Contradiction.* $a_1,a_2,a_3$ would be three integers with pairwise different residues modulo $2$; but there are only two residues modulo $2$, so two of them coincide (pigeonhole). 

Hence the assumption fails: some pair satisfies $\gcd(m_i,m_j)\ge3$. $\blacksquare$

*Remark.* Step 1 is the first "trivial bound" of the problem statement; it is re-derived here only because the argument needs the exact value $2$ of every gcd, not merely $\ge2$.


## 3. Verifica: istruzioni, dipendenze, tempi
Prova a mano, nessuna dipendenza. Verifica meccanica non necessaria; il Referee automatico (due giudici indipendenti,
`runs/p4_c1/attempts/packet_001.json`) non ha trovato passaggi non giustificati.

## 4. Fonti e contributo
- arXiv:2607.24655 Fornal, Sun, On the problem of large gcd for disjoint residue classes (context only: asymptotic result, not used)
- Posizione rispetto allo stato dell'arte: Fornal-Sun [2607.24655] prove an asymptotic lower bound for the largest gcd; the small cases k=3,4 are elementary and are not treated there. Our proof is independent.
- Contributo: la prova qui scritta è del team, per esteso.

## 5. Limiti e parti irrisolte
Nessuna: la parte è dimostrata. Gap dichiarati: nessuno.
