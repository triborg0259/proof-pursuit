/* Verifica indipendente (C, interi) della parte 'una classe' del certificato per U(Q_6) >= 204.
 *
 * Enunciato finito da confutare (S0'): esistono h in {0,1,2}, un insieme H_O di h vertici dispari
 * e un insieme R' di 5+h vertici pari tali che R' ∪ (O \ H_O) induce una foresta in Q_6.
 * (Equivalente a (S0): togliere vertici pari da R rimpicciolisce solo R'; un sottografo indotto di
 *  una foresta e' una foresta, quindi basta |R'| = 5 + h.)
 * WLOG e_1 = 000001 (intero 1) ∈ H_O se h ≥ 1: le traslazioni pari sono transitive sui dispari.
 * Metodo: per ogni H_O e ogni R' (combinazioni), union-find sul sottografo indotto.
 */
#include <stdio.h>
#include <stdint.h>

static int genitore[64];
static int trova(int x) { while (genitore[x] != x) x = genitore[x] = genitore[genitore[x]]; return x; }

/* 1 se il sottografo indotto dalla maschera e' aciclico */
static int e_foresta(uint64_t m) {
    for (int v = 0; v < 64; v++) genitore[v] = v;
    for (int v = 0; v < 64; v++) {
        if (!((m >> v) & 1)) continue;
        for (int i = 0; i < 6; i++) {
            int u = v ^ (1 << i);
            if (u < v || !((m >> u) & 1)) continue;
            int a = trova(u), b = trova(v);
            if (a == b) return 0;
            genitore[a] = b;
        }
    }
    return 1;
}

static int pari[32], n_pari = 0;
static uint64_t maschera_O = 0;
static long esaminati = 0, foreste = 0;

/* enumera i sottoinsiemi di 'k' vertici pari a partire dall'indice 'da' e li testa */
static void combinazioni(int da, int k, uint64_t m) {
    if (k == 0) {
        esaminati++;
        if (e_foresta(m)) { foreste++; printf("FORESTA TROVATA maschera %llx\n", (unsigned long long)m); }
        return;
    }
    for (int i = da; i <= n_pari - k; i++) combinazioni(i + 1, k - 1, m | (1ULL << pari[i]));
}

int main(void) {
    for (int v = 0; v < 64; v++) {
        if (__builtin_popcount(v) % 2 == 0) pari[n_pari++] = v; else maschera_O |= 1ULL << v;
    }
    /* h = 0 */
    combinazioni(0, 5, maschera_O);
    printf("h=0: R' di taglia 5 esaminati %ld, foreste %ld\n", esaminati, foreste);
    /* h = 1: H_O = {1} */
    esaminati = foreste = 0;
    combinazioni(0, 6, maschera_O & ~(1ULL << 1));
    printf("h=1: R' di taglia 6 esaminati %ld, foreste %ld\n", esaminati, foreste);
    /* h = 2: H_O = {1, o} per ogni altro dispari o */
    esaminati = foreste = 0;
    for (int o = 0; o < 64; o++) {
        if (o == 1 || __builtin_popcount(o) % 2 == 0) continue;
        combinazioni(0, 7, maschera_O & ~(1ULL << 1) & ~(1ULL << o));
    }
    printf("h=2: coppie (H_O, R') di taglia 7 esaminate %ld, foreste %ld\n", esaminati, foreste);
    return 0;
}
