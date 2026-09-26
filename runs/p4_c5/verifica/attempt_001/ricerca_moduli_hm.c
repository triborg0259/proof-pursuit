/*
 * ricerca_moduli_hm.c — Implementazione 1 (porting in C di ricerca_moduli_hm.py + decidi_residui.py).
 *
 * COSA: stesso algoritmo della versione Python: k-uple NON DECRESCENTI di divisori >= 2 di
 * L = lcm(1..soglia), visitate in ordine crescente di candidato; ad ogni estensione
 * (R1) 2 <= gcd(m, q) <= soglia per ogni q gia' scelto e (R2) criterio di Huhn-Megyesi sul
 * prefisso, con le somme  sum_i M/gcd(m_i, M)  mantenute INCREMENTALMENTE per tutti i divisori M;
 * alle foglie (R3) famiglia ridotta e (R4) criterio (R2) su ogni sotto-multinsieme.
 * Stadio B: backtracking sui residui in ORDINE STATICO di indice, a_1 = 0, dominio Z/m_i,
 * controllo su tutte le coppie precedenti (nessuna propagazione).
 * PERCHE': la versione Python supera i 10 minuti da k = 14; questa versione ha per costruzione
 * gli stessi conteggi (nodi, foglie, sopravvissuti) e viene confrontata con essa per k <= 13.
 * Aritmetica: interi esatti a 64 bit.
 *
 * Uso: ./ricerca_moduli_hm ricerca|nonvacuita k [k ...]      (stadio A e poi stadio B)
 *      ./ricerca_moduli_hm parti_minime m1 ... mk
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAX_DIV 256
#define MAX_K 16
#define BUDGET_B 50000000L

static long gcdl(long a, long b) { while (b) { long t = a % b; a = b; b = t; } return a; }
static long lcml(long a, long b) { return a / gcdl(a, b) * b; }

static int K, SOGLIA; static long L;
static long divs[MAX_DIV]; static int n_divs;
static long cand[MAX_DIV]; static int n_cand;
static long peso[MAX_DIV][MAX_DIV];
static long nodi, foglie, n_sopr;
static long sopravvissuti[100000][MAX_K];
static long parziale[MAX_K];

static void prepara(int k, int soglia) {
    K = k; SOGLIA = soglia; L = 1;
    for (int t = 1; t <= soglia; t++) L = lcml(L, t);
    n_divs = 0; for (long d = 1; d <= L; d++) if (L % d == 0) divs[n_divs++] = d;
    n_cand = 0; for (int i = 0; i < n_divs; i++) if (divs[i] >= 2) cand[n_cand++] = divs[i];
    for (int i = 0; i < n_cand; i++) for (int m = 0; m < n_divs; m++) peso[i][m] = divs[m] / gcdl(cand[i], divs[m]);
}

/* Scomposizione in potenze di primo massime; restituisce il numero di fattori. */
static int potenze_di_primo(long n, long *out) {
    int c = 0;
    for (long p = 2; n > 1; p++) {
        if (n % p) continue;
        long q = 1; while (n % p == 0) { n /= p; q *= p; }
        out[c++] = q;
    }
    return c;
}

/* (R3): ogni potenza di primo di ciascun m_i divide un altro m_j. */
static int famiglia_ridotta(const long *mod, int k) {
    long q[16];
    for (int i = 0; i < k; i++) {
        int c = potenze_di_primo(mod[i], q);
        for (int t = 0; t < c; t++) {
            int ok = 0;
            for (int j = 0; j < k; j++) if (j != i && mod[j] % q[t] == 0) ok = 1;
            if (!ok) return 0;
        }
    }
    return 1;
}

/* (R2) su un sotto-multinsieme dato: True se passa per ogni M multiplo dell'lcm dei gcd. */
static int criterio_hm(const long *sotto, int r) {
    long g = 1;
    for (int a = 0; a < r; a++) for (int b = a + 1; b < r; b++) g = lcml(g, gcdl(sotto[a], sotto[b]));
    for (int m = 0; m < n_divs; m++) {
        if (divs[m] % g) continue;
        long s = 0; for (int a = 0; a < r; a++) s += divs[m] / gcdl(sotto[a], divs[m]);
        if (s > divs[m]) return 0;
    }
    return 1;
}

/* (R4): criterio HM su ogni sottoinsieme di dimensione >= 2, per dimensione crescente. */
static int tutti_i_sottoinsiemi_passano(const long *mod, int k) {
    for (int r = 2; r <= k; r++) for (long mask = 0; mask < (1L << k); mask++) {
        if (__builtin_popcountl(mask) != r) continue;
        long sotto[MAX_K]; int n = 0;
        for (int i = 0; i < k; i++) if ((mask >> i) & 1) sotto[n++] = mod[i];
        if (!criterio_hm(sotto, n)) return 0;
    }
    return 1;
}

static void foglia(void) {
    foglie++;
    if (famiglia_ridotta(parziale, K) && tutti_i_sottoinsiemi_passano(parziale, K)) {
        memcpy(sopravvissuti[n_sopr], parziale, sizeof(long) * K); n_sopr++;
    }
}

/* Nodo: parziale non decrescente, somme HM correnti (per ogni M), g = lcm dei gcd. */
static void estendi(int prof, const long *somme, long g) {
    nodi++;
    if (prof == K) { foglia(); return; }
    long somme2[MAX_DIV];
    for (int c = 0; c < n_cand; c++) {
        long m = cand[c];
        if (prof && m < parziale[prof - 1]) continue;
        long g2 = g; int ok = 1;
        for (int t = 0; t < prof && ok; t++) {
            long x = gcdl(m, parziale[t]);
            if (x < 2 || x > SOGLIA) ok = 0; else g2 = lcml(g2, x);
        }
        if (!ok) continue;
        for (int i = 0; i < n_divs; i++) somme2[i] = somme[i] + peso[c][i];
        for (int i = 0; i < n_divs && ok; i++) if (divs[i] % g2 == 0 && somme2[i] > divs[i]) ok = 0;
        if (!ok) continue;
        parziale[prof] = m;
        estendi(prof + 1, somme2, g2);
    }
}

static void stadio_a(int k, int soglia) {
    prepara(k, soglia);
    nodi = foglie = n_sopr = 0;
    long zero[MAX_DIV] = {0};
    clock_t t0 = clock();
    estendi(0, zero, 1);
    double dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("k=%d soglia=%d L=%ld candidati=%d nodi=%ld foglie=%ld sopravvissuti=%ld tempo=%.2fs\n",
           k, soglia, L, n_cand, nodi, foglie, n_sopr, dt);
    for (long s = 0; s < n_sopr; s++) {
        printf("   sopravvissuto: (");
        for (int t = 0; t < k; t++) printf("%ld%s", sopravvissuti[s][t], t + 1 < k ? ", " : ")\n");
    }
    fflush(stdout);
}

/* ---------- stadio B: backtracking statico sui residui ---------- */
static long modB[MAX_K], gB[MAX_K][MAX_K], res[MAX_K]; static int kB; static long nodiB; static int superato;

static int estendi_residui(int i) {
    nodiB++;
    if (nodiB > BUDGET_B) { superato = 1; return 0; }
    if (i == kB) return 1;
    for (long a = 0; a < (i == 0 ? 1 : modB[i]); a++) {
        int ok = 1;
        for (int j = 0; j < i && ok; j++) if (((a - res[j]) % gB[i][j] + gB[i][j]) % gB[i][j] == 0) ok = 0;
        if (!ok) continue;
        res[i] = a;
        if (estendi_residui(i + 1)) return 1;
        if (superato) return 0;
    }
    return 0;
}

static const char *decidi(const long *mod, int k, int stampa) {
    kB = k; nodiB = 0; superato = 0;
    for (int i = 0; i < k; i++) { modB[i] = mod[i]; for (int j = 0; j < k; j++) gB[i][j] = gcdl(mod[i], mod[j]); }
    int ok = estendi_residui(0);
    const char *esito = ok ? "FATTIBILE" : (superato ? "NON_DECISO" : "INFATTIBILE");
    if (ok) for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++)     /* riverifica con (*) */
        if (((res[i] - res[j]) % gB[i][j] + gB[i][j]) % gB[i][j] == 0) { printf("ERRORE testimone\n"); exit(1); }
    if (stampa) {
        printf("   %s moduli=(", esito);
        for (int i = 0; i < k; i++) printf("%ld%s", mod[i], i + 1 < k ? ", " : ")");
        printf(" nodi_B=%ld testimone=", nodiB);
        if (ok) { printf("("); for (int i = 0; i < k; i++) printf("(%ld, %ld)%s", res[i], mod[i], i + 1 < k ? ", " : ")"); }
        else printf("None");
        printf("\n"); fflush(stdout);
    }
    return esito;
}

/* Parti minime infattibili (stesso criterio di parte_minima.py: per dimensione crescente). */
static void parti_minime(const long *mod, int k) {
    long minimi[100000]; int n_min = 0;
    decidi(mod, k, 1);
    for (int r = 2; r <= k; r++) for (long mask = 0; mask < (1L << k); mask++) {
        if (__builtin_popcountl(mask) != r) continue;
        int cont = 0; for (int t = 0; t < n_min; t++) if ((minimi[t] & mask) == minimi[t]) cont = 1;
        if (cont) continue;
        long sub[MAX_K]; int n = 0; for (int i = 0; i < k; i++) if ((mask >> i) & 1) sub[n++] = mod[i];
        const char *e = decidi(sub, n, 0);
        if (strcmp(e, "NON_DECISO") == 0) printf("   NON_DECISO su maschera %ld\n", mask);
        if (strcmp(e, "INFATTIBILE") == 0) {
            minimi[n_min++] = mask;
            printf("   parte minima infattibile: indici ("); int primo = 1;
            for (int i = 0; i < k; i++) if ((mask >> i) & 1) { printf("%s%d", primo ? "" : ", ", i); primo = 0; }
            printf(") moduli ("); primo = 1;
            for (int i = 0; i < k; i++) if ((mask >> i) & 1) { printf("%s%ld", primo ? "" : ", ", mod[i]); primo = 0; }
            printf(")\n");
        }
    }
    fflush(stdout);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "uso: vedi intestazione\n"); return 1; }
    long mod[MAX_K]; int n = 0;
    if (strcmp(argv[1], "parti_minime") == 0) {
        for (int i = 2; i < argc; i++) mod[n++] = atol(argv[i]);
        parti_minime(mod, n); return 0;
    }
    int nonvac = strcmp(argv[1], "nonvacuita") == 0;
    for (int i = 2; i < argc; i++) {
        int k = atoi(argv[i]);
        stadio_a(k, nonvac ? k : k - 1);
        for (long s = 0; s < n_sopr; s++) decidi(sopravvissuti[s], k, 1);
    }
    return 0;
}
