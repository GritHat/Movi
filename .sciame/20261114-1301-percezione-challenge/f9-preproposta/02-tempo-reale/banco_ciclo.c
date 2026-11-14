/* Bilancio del ciclo con i moduli della preproposta accesi: ordini di grandezza su CPU, un filo.
 *
 * (a) moduli della preproposta, per 10 tracce: due ipotesi per traccia (previsione 4 stati), ritaglio della gaussiana
 *     sulla griglia polare (probabilita' zero sulle celle «libero»), massa rimasta in ombra, aggiornamento dei pesi,
 *     raggio efficace dopo il ritaglio, punto di massimo avvicinamento, quota di massa nel volume protetto,
 *     macchina a stati (confronti).  Caso peggiore: tutta la griglia per ogni ipotesi.  Variante: solo il riquadro a 3 sigma.
 * (b) riferimento: proiezione di un'immagine di profondita' 848x480 sulla griglia polare (stadio del nucleo).
 *
 * Compilare:  gcc -O2 -o /tmp/banco_ciclo banco_ciclo.c -lm
 * Rifare:     timeout 120 /tmp/banco_ciclo > risultati_banco_c.txt
 * Dati sintetici, seme fisso (12345). NON e' la macchina di destinazione.
 */
#define _POSIX_C_SOURCE 199309L
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define NA 88
#define NR 30
#define NT 10
#define W 848
#define H 480

enum { LIBERO = 0, OCCUPATO = 1, OMBRA = 2, NONOSS = 3 };

static uint8_t stato[NA][NR], protetto[NA][NR];
static float cx[NA][NR], cz[NA][NR], carea[NA][NR];

static uint32_t rs = 12345u;
static double rnd(void) { rs = rs * 1664525u + 1013904223u; return (rs >> 8) / 16777216.0; }

static double adesso(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec * 1e-6;
}
static int cmp(const void *a, const void *b) { double x = *(const double *)a, y = *(const double *)b; return (x > y) - (x < y); }
static void stat(const char *nome, double *v, int n) {
    qsort(v, n, sizeof(double), cmp);
    printf("%-58s mediana %8.4f ms   99o perc. %8.4f ms   massimo %8.4f ms   (n = %d)\n", nome, v[n / 2], v[(int)(0.99 * n)], v[n - 1], n);
}

typedef struct { float x, z, vx, vz, sxx, sxz, szz; } Ipotesi;
typedef struct { Ipotesi h[2]; float mu[2]; int fsm; float sig_eff, t_cpa, d_cpa, p_intr; } Traccia;

/* ritaglio di una ipotesi sulla griglia; ritorna la quota di massa in celle non libere */
static float ritaglio(const Ipotesi *h, int riquadro, float *m_x, float *m_z, float *m_xx, float *m_zz, float *m_prot) {
    float det = h->sxx * h->szz - h->sxz * h->sxz;
    float ixx = h->szz / det, ixz = -h->sxz / det, izz = h->sxx / det;
    float tot = 0, omb = 0, sx = 0, sz = 0, sxx = 0, szz = 0, pr = 0;
    int a0 = 0, a1 = NA, r0 = 0, r1 = NR;
    if (riquadro) {
        float s = 3.0f * sqrtf(h->sxx > h->szz ? h->sxx : h->szz);
        float r = sqrtf(h->x * h->x + h->z * h->z), a = atan2f(h->x, h->z) * 57.29578f;
        float da = (r > s) ? asinf(s / r) * 57.29578f : 90.0f;
        a0 = (int)floorf(a - da + 44.0f); a1 = (int)ceilf(a + da + 44.0f);
        r0 = (int)floorf((r - s) * 10.0f); r1 = (int)ceilf((r + s) * 10.0f);
        if (a0 < 0) a0 = 0; if (a1 > NA) a1 = NA; if (r0 < 0) r0 = 0; if (r1 > NR) r1 = NR;
    }
    for (int i = a0; i < a1; i++)
        for (int j = r0; j < r1; j++) {
            float dx = cx[i][j] - h->x, dz = cz[i][j] - h->z;
            float w = expf(-0.5f * (dx * dx * ixx + 2 * dx * dz * ixz + dz * dz * izz)) * carea[i][j];
            tot += w;
            if (stato[i][j] != LIBERO) {
                omb += w; sx += w * cx[i][j]; sz += w * cz[i][j];
                sxx += w * cx[i][j] * cx[i][j]; szz += w * cz[i][j] * cz[i][j];
                if (protetto[i][j]) pr += w;
            }
        }
    *m_x = sx; *m_z = sz; *m_xx = sxx; *m_zz = szz; *m_prot = pr;
    (void)tot;
    return (tot > 0) ? omb / tot : 0.0f;
}

static void ciclo_tracce(Traccia *tr, float dt, int riquadro) {
    const float q = 0.2f, alfa = 0.9f;
    for (int t = 0; t < NT; t++) {
        Traccia *T = &tr[t];
        float f[2], mass = 0, mx = 0, mz = 0, mxx = 0, mzz = 0, mp = 0;
        for (int k = 0; k < 2; k++) {
            Ipotesi *h = &T->h[k];
            if (k == 1) { h->vx *= alfa; h->vz *= alfa; }           /* sosta: velocita' smorzata */
            h->x += h->vx * dt; h->z += h->vz * dt;
            float g = q * dt * dt * dt / 3 + 0.01f * dt;             /* crescita della covarianza (semplificata a 2x2) */
            h->sxx += g; h->szz += g;
            float a, b, c, d, e;
            f[k] = ritaglio(h, riquadro, &a, &b, &c, &d, &e);
            float w = T->mu[k] * f[k];
            mass += w; mx += T->mu[k] * a; mz += T->mu[k] * b; mxx += T->mu[k] * c; mzz += T->mu[k] * d; mp += T->mu[k] * e;
        }
        /* pesi con l'informazione negativa */
        float s = T->mu[0] * f[0] + T->mu[1] * f[1];
        if (s > 1e-9f) { T->mu[0] = T->mu[0] * f[0] / s; T->mu[1] = 1.0f - T->mu[0]; }
        if (T->mu[0] < 1e-3f) T->mu[0] = 1e-3f; if (T->mu[0] > 0.999f) T->mu[0] = 0.999f; T->mu[1] = 1.0f - T->mu[0];
        /* raggio efficace dopo il ritaglio (dai momenti accumulati; normalizzazione approssimata) */
        float n = mass > 1e-9f ? mass : 1e-9f; (void)n;
        float wsum = mx * mx + mz * mz > 0 ? 1.0f : 1.0f; (void)wsum;
        T->sig_eff = sqrtf(fabsf(mxx + mzz) + 1e-9f);
        T->p_intr = mp;
        /* punto di massimo avvicinamento per le due ipotesi, pesato */
        float tc = 0, dc = 0;
        for (int k = 0; k < 2; k++) {
            Ipotesi *h = &T->h[k];
            float v2 = h->vx * h->vx + h->vz * h->vz;
            float tk = v2 > 1e-6f ? -(h->x * h->vx + h->z * h->vz) / v2 : 0.0f; if (tk < 0) tk = 0;
            float px = h->x + h->vx * tk, pz = h->z + h->vz * tk;
            tc += T->mu[k] * tk; dc += T->mu[k] * sqrtf(px * px + pz * pz);
        }
        T->t_cpa = tc; T->d_cpa = dc;
        /* indice di rotta convergente e macchina a stati: pochi confronti */
        float r2 = T->h[0].x * T->h[0].x + T->h[0].z * T->h[0].z;
        float tdot = (T->h[0].z * T->h[0].vx - T->h[0].x * T->h[0].vz) / (r2 + 1e-6f);
        float rdot = (T->h[0].x * T->h[0].vx + T->h[0].z * T->h[0].vz) / sqrtf(r2 + 1e-6f);
        if (T->mu[1] > 0.7f) T->fsm = 4; else if (fabsf(tdot) < 0.05f && rdot < 0) T->fsm = 2; else T->fsm = 1;
    }
}

static void prepara_griglia(void) {
    for (int i = 0; i < NA; i++)
        for (int j = 0; j < NR; j++) {
            float a = (-44.0f + i + 0.5f) * 0.01745329f, r = (j + 0.5f) * 0.1f;
            cx[i][j] = r * sinf(a); cz[i][j] = r * cosf(a); carea[i][j] = r * 0.1f * 0.01745329f;
            /* pannello fra -18 e +29 gradi a 1,15 m: ombra dietro; il resto libero; bordo campo non osservato */
            int inombra = (i >= 26 && i <= 73 && r > 1.2f);
            stato[i][j] = inombra ? OMBRA : (r < 1.24f ? NONOSS : LIBERO);
            protetto[i][j] = (fabsf(cx[i][j]) < 0.5f && cz[i][j] < 2.0f);
        }
}

static void prepara_tracce(Traccia *tr, float sigma) {
    for (int t = 0; t < NT; t++)
        for (int k = 0; k < 2; k++) {
            Ipotesi *h = &tr[t].h[k];
            h->x = (float)(rnd() * 2.0 - 1.0); h->z = (float)(1.5 + rnd() * 1.2);
            h->vx = (float)(rnd() * 2.8 - 1.4); h->vz = (float)(rnd() * 0.6 - 0.3);
            h->sxx = sigma * sigma; h->szz = sigma * sigma; h->sxz = 0.2f * sigma * sigma;
            tr[t].mu[0] = 0.8f; tr[t].mu[1] = 0.2f; tr[t].fsm = 0;
        }
}

/* (b) proiezione dell'immagine di profondita' sulla griglia polare */
static uint16_t prof[H][W];
static float rx[W], ry[H];
static uint16_t n_suolo[NA][NR], n_ost[NA][NR];
static float primo[NA];

static void prepara_immagine(void) {
    float fx = W / (2.0f * tanf(0.5f * 87.0f * 0.01745329f)), fy = H / (2.0f * tanf(0.5f * 58.0f * 0.01745329f));
    for (int u = 0; u < W; u++) rx[u] = (u - W / 2 + 0.5f) / fx;
    for (int v = 0; v < H; v++) ry[v] = (v - H / 2 + 0.5f) / fy;
    float st = sinf(15 * 0.01745329f), ct = cosf(15 * 0.01745329f);
    for (int v = 0; v < H; v++)
        for (int u = 0; u < W; u++) {
            /* suolo a 1,2 m sotto la camera inclinata di 15 gradi; parete a 4 m; un ostacolo; 5 % di buchi */
            float den = ry[v] * ct + st;                      /* componente verso il basso del raggio */
            float d = den > 0.02f ? 1.2f / den : 4.0f;
            if (d > 4.0f) d = 4.0f;
            if (u > 300 && u < 520 && d > 1.3f) d = 1.3f;     /* pannello */
            if (rnd() < 0.05) d = 0.0f;
            prof[v][u] = (uint16_t)(d * 1000.0f);
        }
}

static int proietta(void) {
    const float st = 0.2588190f, ct = 0.9659258f;
    memset(n_suolo, 0, sizeof n_suolo); memset(n_ost, 0, sizeof n_ost);
    for (int i = 0; i < NA; i++) primo[i] = 1e9f;
    int buchi = 0;
    for (int v = 0; v < H; v++)
        for (int u = 0; u < W; u++) {
            uint16_t p = prof[v][u];
            if (!p) { buchi++; continue; }
            float d = p * 0.001f, xc = rx[u] * d, yc = ry[v] * d;
            float zw = d * ct - yc * st, quota = 1.2f - (yc * ct + d * st);
            float r = sqrtf(xc * xc + zw * zw);
            int i = (int)(atan2f(xc, zw) * 57.29578f + 44.0f), j = (int)(r * 10.0f);
            if (i < 0 || i >= NA || j < 0 || j >= NR) continue;
            if (quota > 0.07f && quota < 2.0f) { n_ost[i][j]++; if (r < primo[i]) primo[i] = r; }
            else if (fabsf(quota) <= 0.07f) n_suolo[i][j]++;
        }
    int occ = 0;
    for (int i = 0; i < NA; i++)
        for (int j = 0; j < NR; j++) {
            float r = (j + 0.5f) * 0.1f;
            uint8_t s = n_ost[i][j] >= 3 ? OCCUPATO : (r > primo[i] ? OMBRA : (n_suolo[i][j] >= 3 ? LIBERO : NONOSS));
            occ += s;
        }
    return occ + buchi;
}

int main(void) {
    static double t[20000];
    Traccia tr[NT];
    volatile float pozzo = 0; volatile int pozzo_i = 0;
    prepara_griglia();
    printf("# Banco del ciclo, C -O2, un filo. Griglia %d x %d = %d celle; %d tracce x 2 ipotesi.\n", NA, NR, NA * NR, NT);

    const float sig[2] = {0.8f, 0.3f};
    for (int riq = 0; riq < 2; riq++)
        for (int s = 0; s < 2; s++) {
            int n = 5000;
            for (int it = 0; it < n; it++) {
                if (it % 20 == 0) prepara_tracce(tr, sig[s]);       /* fuori dal tempo misurato */
                double a = adesso();
                ciclo_tracce(tr, 1.0f / 15.0f, riq);
                t[it] = adesso() - a;
                pozzo += tr[it % NT].sig_eff + tr[it % NT].d_cpa + tr[it % NT].mu[0];
            }
            char nome[128];
            snprintf(nome, sizeof nome, "(a) moduli preproposta, %s, sigma %.1f m", riq ? "riquadro a 3 sigma" : "griglia intera     ", sig[s]);
            stat(nome, t, n);
        }

    prepara_immagine();
    int n = 500;
    for (int it = 0; it < n; it++) {
        double a = adesso();
        pozzo_i += proietta();
        t[it] = adesso() - a;
    }
    stat("(b) proiezione 848x480 -> griglia polare (atan2f per pixel)", t, n);
    fprintf(stderr, "pozzo %f %d\n", (double)pozzo, pozzo_i);
    return 0;
}
