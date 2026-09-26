/*
 * clique_moduli.c — Implementazione 2 (indipendente) per il problema 4, parte 5.
 *
 * COSA: enumera i multinsiemi di k moduli (divisori >= 2 di L = lcm(1..soglia))
 * come multi-clique del grafo di compatibilita' H: arco d-d' se 2 <= gcd(d,d') <= soglia,
 * cappio in d se d <= soglia (un modulo puo' ripetersi solo se gcd(d,d)=d <= soglia).
 * Le sequenze sono NON CRESCENTI e gli insiemi di candidati sono bitset intersecati
 * ad ogni passo (stile Bron-Kerbosch), cosi' ogni multinsieme e' visitato una sola volta.
 * Potatura interna: (R2) criterio di densita' di Huhn-Megyesi sulla famiglia parziale,
 * ricalcolato da zero per ogni M | L multiplo di g = lcm dei gcd a coppie.
 * Alle foglie: (R3) ogni potenza di primo di un modulo divide un altro modulo;
 * (R2) su OGNI sotto-multinsieme (somme precalcolate per maschera).
 * Stadio B (residui): CSP con forward checking e variabile a dominio minimo (MRV);
 * il primo residuo assegnato e' 0 (traslazione).
 * PERCHE': serve una seconda implementazione con metodo diverso da ricerca_moduli_hm.py
 * (sequenze non decrescenti, somme incrementali, backtracking statico sui residui).
 * Aritmetica: solo interi esatti a 64 bit (i valori restano < 2^40).
 *
 * Uso: ./clique_moduli ricerca|nonvacuita k [k ...]
 *      ./clique_moduli parti_minime m1 m2 ... mk
 *      ./clique_moduli residui m1 m2 ... mk
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAX_DIV 256          /* divisori di L (L <= 360360 ha 192 divisori) */
#define MAX_K 16
#define WORDS 4              /* bitset da 256 bit */
#define BUDGET_B 50000000L   /* limite nodi dello stadio B (onesta': NON_DECISO) */

typedef struct { uint64_t w[WORDS]; } Bits;

static long gcdl(long a, long b) { while (b) { long t = a % b; a = b; b = t; } return a; }
static long lcml(long a, long b) { return a / gcdl(a, b) * b; }

/* ---------- stato globale della ricerca sui moduli ---------- */
static int k_glob, soglia_glob;
static long L_glob;
static long divs[MAX_DIV]; static int n_divs;        /* tutti i divisori di L */
static long cand[MAX_DIV]; static int n_cand;        /* divisori >= 2 (candidati) */
static long gtab[MAX_DIV][MAX_DIV];                  /* gcd fra candidati */
static long peso[MAX_DIV][MAX_DIV];                  /* peso[i][m] = M/gcd(cand[i],M) */
static Bits adj[MAX_DIV];                            /* vicini di indice <= i (cappio incluso) */
static int parziale[MAX_K];
static long nodi, foglie, n_sopr;
static int sopravvissuti[100000][MAX_K];
static int32_t *somma_maschera;                      /* [maschera][m] somme per sottoinsieme */
static long g_maschera[1 << MAX_K];

static void bits_set(Bits *b, int i) { b->w[i >> 6] |= (uint64_t)1 << (i & 63); }
static int bits_test(const Bits *b, int i) { return (b->w[i >> 6] >> (i & 63)) & 1; }
static Bits bits_and(Bits a, Bits b) { Bits r; for (int t = 0; t < WORDS; t++) r.w[t] = a.w[t] & b.w[t]; return r; }

/* Prepara divisori, candidati, tabelle dei gcd e dei pesi, adiacenze. */
static void prepara(int k, int soglia) {
    k_glob = k; soglia_glob = soglia;
    L_glob = 1; for (int t = 1; t <= soglia; t++) L_glob = lcml(L_glob, t);
    n_divs = 0; for (long d = 1; d <= L_glob; d++) if (L_glob % d == 0) divs[n_divs++] = d;
    n_cand = 0; for (int i = 0; i < n_divs; i++) if (divs[i] >= 2) cand[n_cand++] = divs[i];
    for (int i = 0; i < n_cand; i++) for (int j = 0; j < n_cand; j++) gtab[i][j] = gcdl(cand[i], cand[j]);
    for (int i = 0; i < n_cand; i++) for (int m = 0; m < n_divs; m++) peso[i][m] = divs[m] / gcdl(cand[i], divs[m]);
    for (int i = 0; i < n_cand; i++) {
        memset(&adj[i], 0, sizeof(Bits));
        for (int j = 0; j < i; j++) if (gtab[i][j] >= 2 && gtab[i][j] <= soglia) bits_set(&adj[i], j);
        if (cand[i] <= soglia) bits_set(&adj[i], i);           /* cappio: ripetizione ammessa */
    }
}

/* (R2) sulla famiglia parziale piu' il candidato j: per ogni M multiplo di g, somma <= M. */
static int densita_ok(int prof, int j, long g) {
    for (int m = 0; m < n_divs; m++) {
        if (divs[m] % g) continue;
        long s = peso[j][m];
        for (int t = 0; t < prof; t++) s += peso[parziale[t]][m];
        if (s > divs[m]) return 0;
    }
    return 1;
}

/* (R3): ogni potenza di primo massima di ciascun modulo divide un altro modulo della famiglia. */
static int famiglia_ridotta(void) {
    for (int i = 0; i < k_glob; i++) {
        long n = cand[parziale[i]];
        for (long p = 2; n > 1; p++) {
            if (n % p) continue;
            long q = 1; while (n % p == 0) { n /= p; q *= p; }
            int trovato = 0;
            for (int j = 0; j < k_glob && !trovato; j++) if (j != i && cand[parziale[j]] % q == 0) trovato = 1;
            if (!trovato) return 0;
        }
    }
    return 1;
}

/* (R2) su ogni sotto-multinsieme (maschere con almeno 2 elementi), somme e lcm incrementali. */
static int tutti_i_sottoinsiemi_ok(void) {
    int K = k_glob; long nm = 1L << K;
    g_maschera[0] = 1; memset(somma_maschera, 0, sizeof(int32_t) * n_divs);
    for (long mask = 1; mask < nm; mask++) {
        int basso = __builtin_ctzl(mask); long resto = mask & (mask - 1);
        long g = g_maschera[resto];
        for (int t = 0; t < K; t++) if ((resto >> t) & 1) g = lcml(g, gtab[parziale[basso]][parziale[t]]);
        g_maschera[mask] = g;
        int32_t *s = somma_maschera + mask * n_divs, *s0 = somma_maschera + resto * n_divs;
        for (int m = 0; m < n_divs; m++) s[m] = s0[m] + (int32_t)peso[parziale[basso]][m];
        if (__builtin_popcountl(mask) < 2) continue;
        for (int m = 0; m < n_divs; m++) if (divs[m] % g == 0 && s[m] > divs[m]) return 0;
    }
    return 1;
}

/* Foglia: applica (R3) e (R2)-sottoinsiemi; registra il sopravvissuto in ordine non decrescente. */
static void foglia(void) {
    foglie++;
    if (!famiglia_ridotta() || !tutti_i_sottoinsiemi_ok()) return;
    for (int t = 0; t < k_glob; t++) sopravvissuti[n_sopr][t] = parziale[k_glob - 1 - t];
    n_sopr++;
}

/* Nodo: estende la sequenza non crescente con ogni candidato del bitset che passa (R2). */
static void estendi(int prof, Bits cands, long g) {
    nodi++;
    if (prof == k_glob) { foglia(); return; }
    for (int j = n_cand - 1; j >= 0; j--) {
        if (!bits_test(&cands, j)) continue;
        long g2 = g;
        for (int t = 0; t < prof; t++) g2 = lcml(g2, gtab[j][parziale[t]]);
        if (!densita_ok(prof, j, g2)) continue;
        parziale[prof] = j;
        estendi(prof + 1, bits_and(cands, adj[j]), g2);
    }
}

/* Esegue lo stadio A per (k, soglia) e stampa conteggi e sopravvissuti. */
static void stadio_a(int k, int soglia) {
    prepara(k, soglia);
    somma_maschera = malloc(sizeof(int32_t) * n_divs * (1L << k));
    nodi = foglie = n_sopr = 0;
    Bits tutti; memset(&tutti, 0, sizeof tutti);
    for (int i = 0; i < n_cand; i++) bits_set(&tutti, i);
    clock_t t0 = clock();
    estendi(0, tutti, 1);
    double dt = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("k=%d soglia=%d L=%ld candidati=%d nodi=%ld foglie=%ld sopravvissuti=%ld tempo=%.2fs\n",
           k, soglia, L_glob, n_cand, nodi, foglie, n_sopr, dt);
    for (long s = 0; s < n_sopr; s++) {
        printf("   sopravvissuto: (");
        for (int t = 0; t < k; t++) printf("%ld%s", cand[sopravvissuti[s][t]], t + 1 < k ? ", " : ")\n");
    }
    fflush(stdout);
    free(somma_maschera);
}

/* ---------- stadio B: residui con forward checking ---------- */
static long modB[MAX_K], gB[MAX_K][MAX_K]; static int kB;
static long nodiB, budget_superato;
static long testimone[MAX_K];

/* Dominio = bitset dei residui ammessi modulo m_i; copiato per livello di ricorsione. */
typedef struct { uint64_t *bits; long conta; } Dominio;

static void dominio_rimuovi(Dominio *d, long r, long passo, long m) {
    for (long x = r; x < m; x += passo)
        if ((d->bits[x >> 6] >> (x & 63)) & 1) { d->bits[x >> 6] &= ~((uint64_t)1 << (x & 63)); d->conta--; }
}

/* Ricorsione: sceglie la variabile non assegnata con dominio minimo; il primo valore e' 0. */
static int cerca_residui(int assegnati, int *fatto, Dominio *dom) {
    nodiB++;
    if (nodiB > BUDGET_B) { budget_superato = 1; return 0; }
    if (assegnati == kB) return 1;
    int v = -1;
    for (int i = 0; i < kB; i++) if (!fatto[i] && (v < 0 || dom[i].conta < dom[v].conta)) v = i;
    if (dom[v].conta == 0) return 0;
    long nw_tot = 0; for (int i = 0; i < kB; i++) nw_tot += (modB[i] + 63) / 64;
    uint64_t *copia = malloc(sizeof(uint64_t) * nw_tot);
    Dominio dom2[MAX_K]; long off = 0;
    for (int i = 0; i < kB; i++) { dom2[i].bits = copia + off; off += (modB[i] + 63) / 64; }
    for (long a = 0; a < modB[v]; a++) {
        if (!((dom[v].bits[a >> 6] >> (a & 63)) & 1)) continue;
        if (assegnati == 0 && a != 0) break;                    /* traslazione: primo residuo 0 */
        memcpy(copia, dom[0].bits, sizeof(uint64_t) * nw_tot);
        for (int i = 0; i < kB; i++) dom2[i].conta = dom[i].conta;
        fatto[v] = 1; testimone[v] = a;
        for (int i = 0; i < kB; i++) if (!fatto[i]) dominio_rimuovi(&dom2[i], a % gB[v][i], gB[v][i], modB[i]);
        if (cerca_residui(assegnati + 1, fatto, dom2)) { free(copia); return 1; }
        fatto[v] = 0;
        if (budget_superato) break;
    }
    free(copia);
    return 0;
}

/* Decide un multinsieme di moduli: stampa FATTIBILE (con testimone riverificato), INFATTIBILE o NON_DECISO. */
static const char *decidi(const long *mod, int k, int stampa) {
    kB = k; nodiB = 0; budget_superato = 0;
    long nw_tot = 0;
    for (int i = 0; i < k; i++) { modB[i] = mod[i]; nw_tot += (mod[i] + 63) / 64; }
    for (int i = 0; i < k; i++) for (int j = 0; j < k; j++) gB[i][j] = gcdl(mod[i], mod[j]);
    uint64_t *bits = malloc(sizeof(uint64_t) * nw_tot); Dominio dom[MAX_K]; long off = 0;
    for (int i = 0; i < k; i++) {
        dom[i].bits = bits + off; off += (mod[i] + 63) / 64; dom[i].conta = mod[i];
        memset(dom[i].bits, 0, sizeof(uint64_t) * ((mod[i] + 63) / 64));
        for (long x = 0; x < mod[i]; x++) dom[i].bits[x >> 6] |= (uint64_t)1 << (x & 63);
    }
    int fatto[MAX_K] = {0};
    int ok = cerca_residui(0, fatto, dom);
    free(bits);
    const char *esito = ok ? "FATTIBILE" : (budget_superato ? "NON_DECISO" : "INFATTIBILE");
    if (ok) for (int i = 0; i < k; i++) for (int j = i + 1; j < k; j++)     /* riverifica con (*) */
        if (((testimone[i] - testimone[j]) % gB[i][j] + gB[i][j]) % gB[i][j] == 0) { printf("ERRORE testimone\n"); exit(1); }
    if (stampa) {
        printf("   %s moduli=(", esito);
        for (int i = 0; i < k; i++) printf("%ld%s", mod[i], i + 1 < k ? ", " : ")");
        printf(" nodi_B=%ld testimone=", nodiB);
        if (ok) { printf("("); for (int i = 0; i < k; i++) printf("(%ld, %ld)%s", testimone[i], mod[i], i + 1 < k ? ", " : ")"); }
        else printf("None");
        printf("\n"); fflush(stdout);
    }
    return esito;
}

/* Parti minime: sotto-multinsiemi (per indici) infattibili senza sottoinsieme proprio infattibile. */
static void parti_minime(const long *mod, int k) {
    long minimi[100000]; int n_min = 0;
    decidi(mod, k, 1);
    for (int r = 2; r <= k; r++) for (long mask = 0; mask < (1L << k); mask++) {
        if (__builtin_popcountl(mask) != r) continue;
        int contenuto = 0; for (int t = 0; t < n_min; t++) if ((minimi[t] & mask) == minimi[t]) contenuto = 1;
        if (contenuto) continue;
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
    if (strcmp(argv[1], "parti_minime") == 0 || strcmp(argv[1], "residui") == 0) {
        for (int i = 2; i < argc; i++) mod[n++] = atol(argv[i]);
        if (argv[1][0] == 'p') parti_minime(mod, n); else decidi(mod, n, 1);
        return 0;
    }
    int nonvac = strcmp(argv[1], "nonvacuita") == 0;
    for (int i = 2; i < argc; i++) {
        int k = atoi(argv[i]);
        stadio_a(k, nonvac ? k : k - 1);
        for (long s = 0; s < n_sopr; s++) {
            for (int t = 0; t < k; t++) mod[t] = cand[sopravvissuti[s][t]];
            decidi(mod, k, 1);
        }
    }
    return 0;
}
