/* audit_imm.c — sciame-rovesciatore, f9: audit delle ipotesi nascoste su S3 + S4
 * (inseguitore a due ipotesi + ritaglio con l'informazione negativa).
 * Scena a una dimensione sulla linea dell'attore. Nessuna profondita' simulata.
 * Compilare: gcc -O2 -o audit_imm audit_imm.c -lm
 * Lanciare:  timeout 120 ./audit_imm > risultati_audit_imm.txt
 * Seme fisso (20261114). Previsioni: PREVISIONI.md (scritte prima).
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
#include <string.h>

#define NP 1000
#define NRUN 1000
#define DT (1.0 / 15.0)
#define A_SH (-0.639)
#define B_SH (0.639)
#define SIGV 0.10
#define SIGP 0.03

static uint64_t rs[2];
static uint64_t splitmix(uint64_t *x) {
    uint64_t z = (*x += 0x9E3779B97F4A7C15ULL);
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL;
    z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL;
    return z ^ (z >> 31);
}
static void seed(uint64_t s) { rs[0] = splitmix(&s); rs[1] = splitmix(&s); }
static inline uint64_t rotl(uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t nexti(void) {
    uint64_t s0 = rs[0], s1 = rs[1], r = s0 + s1;
    s1 ^= s0; rs[0] = rotl(s0, 24) ^ s1 ^ (s1 << 16); rs[1] = rotl(s1, 37);
    return r;
}
static inline double unif(void) { return (nexti() >> 11) * (1.0 / 9007199254740992.0); }
static double gauss(void) {
    static int has = 0; static double keep;
    if (has) { has = 0; return keep; }
    double u1, u2;
    do { u1 = unif(); } while (u1 < 1e-300);
    u2 = unif();
    double r = sqrt(-2.0 * log(u1)), th = 6.283185307179586 * u2;
    keep = r * sin(th); has = 1;
    return r * cos(th);
}

typedef struct {
    const char *name;
    double v;      /* velocita' vera */
    int stop;      /* 0 transito, 1 sosta */
    double xstop;  /* centro alla sosta */
    int varA;      /* 1 = lettura A (alla lettera), 0 = lettura B (ritaglio vero) */
    int L2;        /* 1 = ammesse solo le celle in ombra */
    double w;      /* larghezza del corpo */
    double mask;   /* ombra stimata piu' stretta di mask per lato (striscia «libero» falsa) */
    double band;   /* fascia: l'insieme ammesso e' dilatato di band */
    double lat;    /* stato portato a t_now = t_cap + lat prima del ritaglio */
    double pd;
    double q;
} Cfg;

static int cmpd(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}
static double med(double *v, int n) {
    if (n == 0) return NAN;
    qsort(v, n, sizeof(double), cmpd);
    return v[n / 2];
}

typedef struct { double x[NP], u[NP]; int n; } Set; /* n = vive (lettura B) */

static int allowed(const Cfg *c, double x, double lo, double hi) {
    double es_lo = A_SH + c->mask - c->band, es_hi = B_SH - c->mask + c->band;
    if (x >= es_lo && x <= es_hi) return 1;
    if (!c->L2) { /* celle occupate dalla parte visibile del corpo */
        if (lo < A_SH) { double r = hi < A_SH ? hi : A_SH; if (x >= lo - c->band && x <= r) return 1; }
        if (hi > B_SH) { double l = lo > B_SH ? lo : B_SH; if (x >= l && x <= hi + c->band) return 1; }
    }
    return 0;
}
/* cella davvero vista libera: fuori dall'ombra vera e fuori dal corpo visibile */
static int truly_free(double x, double lo, double hi) {
    if (x >= A_SH && x <= B_SH) return 0;
    if (x >= lo && x <= hi) return 0;
    return 1;
}

static void run_cfg(const Cfg *c) {
    static Set h1, h2;
    static double mu1_re[NRUN], jump_re[NRUN], delay_s[NRUN], zdelay[NRUN], gap[NRUN];
    int n_re = 0, n_delay = 0, n_z = 0, n_gap = 0;
    int falsestop = 0, extinct = 0, zfalse = 0, within1s = 0, never_re = 0; (void)never_re;
    long cov1 = 0, cov2 = 0, covn = 0, freen = 0; double sig_acc = 0, free_acc = 0;
    double sqq = sqrt(c->q * DT);
    for (int r = 0; r < NRUN; r++) {
        double vest = c->v + SIGV * gauss(); if (vest < 0.1) vest = 0.1;
        double c0 = A_SH - c->w / 2, D = 0.0 - c0, alpha = D / (D + vest * DT);
        for (int i = 0; i < NP; i++) {
            h1.x[i] = c0 + SIGP * gauss(); h1.u[i] = vest + SIGV * gauss();
            h2.x[i] = c0 + SIGP * gauss(); h2.u[i] = vest + SIGV * gauss();
        }
        h1.n = h2.n = NP;
        double w1 = 0.8, w2 = 0.2, mu1 = 0.8;
        double tstop = c->stop ? (c->xstop - c0) / c->v : 1e9;
        double tout = (B_SH + c->w / 2 - c0) / fmax(vest - 2 * SIGV, 0.1) + 3 * DT; /* regola Z */
        int K = c->stop ? (int)((tstop + 3.2) / DT) : (int)(8.0 / DT);
        int fs = 0, ext = 0, dly = 0, zf = 0, re = 0;
        double mmean = c0, msig = SIGP;
        for (int k = 1; k <= K; k++) {
            double t = k * DT, cc = c0 + c->v * t;
            if (c->stop && cc > c->xstop) cc = c->xstop;
            double lo = cc - c->w / 2, hi = cc + c->w / 2;
            /* propagazione */
            for (int i = 0; i < NP; i++) {
                h1.u[i] += sqq * gauss(); h1.x[i] += h1.u[i] * DT;
                h2.u[i] = alpha * h2.u[i] + sqq * gauss(); h2.x[i] += h2.u[i] * DT;
            }
            /* riaggancio: corpo tutto fuori dall'ombra vera, Pd per fotogramma */
            if (lo >= B_SH && unif() < c->pd) {
                re = 1;
                mu1_re[n_re] = mu1; jump_re[n_re] = fabs(cc - mmean) / fmax(msig, 1e-6); n_re++;
                gap[n_gap++] = t;
                break;
            }
            if (!c->stop && t > tout) zf = 1;
            /* lettura L2: il ritaglio parte a corpo tutto nascosto */
            int do_clamp = !(c->L2 && lo < A_SH);
            double f1 = 1, f2 = 1;
            if (do_clamp) {
                Set *hs[2] = { &h1, &h2 }; double *fs_[2] = { &f1, &f2 };
                for (int h = 0; h < 2; h++) {
                    Set *s = hs[h]; int ns = 0;
                    if (c->varA) {
                        for (int i = 0; i < NP; i++) if (allowed(c, s->x[i] + s->u[i] * c->lat, lo, hi)) ns++;
                        *fs_[h] = (double)ns / NP;
                    } else {
                        if (s->n == 0) { *fs_[h] = 0; continue; }
                        for (int i = 0; i < NP; i++)
                            if (allowed(c, s->x[i] + s->u[i] * c->lat, lo, hi)) { s->x[ns] = s->x[i]; s->u[ns] = s->u[i]; ns++; }
                        *fs_[h] = (double)ns / NP;
                        if (ns == 0) s->n = 0;
                        else for (int i = ns; i < NP; i++) { int j = (int)(unif() * ns); s->x[i] = s->x[j]; s->u[i] = s->u[j]; }
                    }
                }
            }
            w1 *= f1; w2 *= f2;
            if (w1 / 0.8 < 0.05 && w2 / 0.2 < 0.05) ext = 1;
            if (w1 + w2 <= 0) break;
            mu1 = w1 / (w1 + w2);
            if (!c->stop && mu1 < 0.5) fs = 1;
            if (c->stop && t >= tstop && mu1 < 0.5 && !dly) { dly = 1; delay_s[n_delay++] = t - tstop; if (t - tstop <= 1.0) within1s++; }
            /* mistura mostrata (ritagliata): media, sigma, massa su celle davvero libere */
            double sw = 0, sx = 0, sxx = 0, sfree = 0;
            Set *hs2[2] = { &h1, &h2 }; double mu[2] = { mu1, 1 - mu1 };
            for (int h = 0; h < 2; h++) {
                Set *s = hs2[h]; if (mu[h] <= 0) continue;
                double a_ = 0, ax = 0, axx = 0, af = 0;
                for (int i = 0; i < NP; i++) {
                    double xe = s->x[i] + s->u[i] * c->lat;
                    if (c->varA && !allowed(c, xe, lo, hi)) continue;
                    if (!c->varA && s->n == 0) break;
                    a_ += 1; ax += xe; axx += xe * xe; if (truly_free(xe, lo, hi)) af += 1;
                }
                if (a_ > 0) { sw += mu[h]; sx += mu[h] * ax / a_; sxx += mu[h] * axx / a_; sfree += mu[h] * af / a_; }
            }
            if (sw > 0) {
                mmean = sx / sw; double var = sxx / sw - mmean * mmean; msig = sqrt(var > 0 ? var : 0);
                free_acc += sfree / sw; freen++;
                if (c->stop && t - tstop >= 0.5 && t - tstop <= 3.0) {
                    covn++; sig_acc += msig;
                    if (fabs(cc - mmean) <= msig) cov1++;
                    if (fabs(cc - mmean) <= 2 * msig) cov2++;
                }
            }
        }
        if (c->stop) zdelay[n_z++] = tout - tstop;
        if (!c->stop && !re) never_re++;
        falsestop += fs; extinct += ext; zfalse += zf;
    }
    printf("%-34s", c->name);
    if (!c->stop) {
        printf(" transito v=%.1f | sosta falsa %5.1f %% | estinte %5.1f %% | mu1 al riaggancio (mediana) %.2f | salto/sigma (mediana) %.2f | massa su libero vero %.1f %% | senza misura (mediana) %.2f s | regola Z: falsi %4.1f %% | n=%d\n",
               c->v, 100.0 * falsestop / NRUN, 100.0 * extinct / NRUN, med(mu1_re, n_re), med(jump_re, n_re),
               100.0 * free_acc / (freen ? freen : 1), med(gap, n_gap), 100.0 * zfalse / NRUN, NRUN);
    } else {
        printf(" sosta x=%+.2f v=%.1f | mu2>0,5 entro 1 s %5.1f %% | mai %5.1f %% | ritardo mediano %.2f s | estinte %5.1f %% | vero entro ±sigma %5.1f %% | entro ±2sigma %5.1f %% | sigma_eff medio %.2f m | massa su libero vero %.1f %% | regola Z: ritardo mediano %.2f s | n=%d\n",
               c->xstop, c->v, 100.0 * within1s / NRUN, 100.0 * (NRUN - n_delay) / NRUN, med(delay_s, n_delay),
               100.0 * extinct / NRUN, 100.0 * cov1 / (covn ? covn : 1), 100.0 * cov2 / (covn ? covn : 1),
               sig_acc / (covn ? covn : 1), 100.0 * free_acc / (freen ? freen : 1), med(zdelay, n_z), NRUN);
    }
    fflush(stdout);
}

int main(void) {
    seed(20261114ULL);
    /* name, v, stop, xstop, varA, L2, w, mask, band, lat, pd, q */
    Cfg cfgs[] = {
        { "C0 ideale B (punto, Pd 1)",        1.2, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0,   1.0, 0.2 },
        { "C0 ideale A (punto, Pd 1)",        1.2, 0, 0, 1, 0, 0.0, 0.0, 0.0, 0.0,   1.0, 0.2 },
        { "P1 nucleo B L1",                   1.2, 0, 0, 0, 0, 0.4, 0.0, 0.0, 0.0,   0.9, 0.2 },
        { "P2 nucleo A L1",                   1.2, 0, 0, 1, 0, 0.4, 0.0, 0.0, 0.0,   0.9, 0.2 },
        { "P3 nucleo B L2",                   1.2, 0, 0, 0, 1, 0.4, 0.0, 0.0, 0.0,   0.9, 0.2 },
        { "P4 lento B L1 q0.2",               0.5, 0, 0, 0, 0, 0.4, 0.0, 0.0, 0.0,   0.9, 0.2 },
        { "P4' lento B L1 q0.05",             0.5, 0, 0, 0, 0, 0.4, 0.0, 0.0, 0.0,   0.9, 0.05 },
        { "P4'' lento A L1 q0.2",             0.5, 0, 0, 1, 0, 0.4, 0.0, 0.0, 0.0,   0.9, 0.2 },
        { "P5 maschera -20 B L1",             1.2, 0, 0, 0, 0, 0.4, 0.2, 0.0, 0.0,   0.9, 0.2 },
        { "P5b maschera -20 + fascia 0.40",   1.2, 0, 0, 0, 0, 0.4, 0.2, 0.4, 0.0,   0.9, 0.2 },
        { "P5c fascia 0.40, maschera esatta", 1.2, 0, 0, 0, 0, 0.4, 0.0, 0.4, 0.0,   0.9, 0.2 },
        { "P10 latenza 155 ms B L1",          1.2, 0, 0, 0, 0, 0.4, 0.0, 0.0, 0.155, 0.9, 0.2 },
        { "P10' latenza 155 ms A L1",         1.2, 0, 0, 1, 0, 0.4, 0.0, 0.0, 0.155, 0.9, 0.2 },
        { "P1' nucleo B L1 Pd 0.7",           1.2, 0, 0, 0, 0, 0.4, 0.0, 0.0, 0.0,   0.7, 0.2 },
        { "P6 sosta meta' B L1",              1.2, 1, 0.0,   0, 0, 0.4, 0.0, 0.0, 0.0, 0.9, 0.2 },
        { "P6' sosta meta' A L1",             1.2, 1, 0.0,   1, 0, 0.4, 0.0, 0.0, 0.0, 0.9, 0.2 },
        { "P7 sosta ingresso B L1",           1.2, 1, -0.389, 0, 0, 0.4, 0.0, 0.0, 0.0, 0.9, 0.2 },
        { "P7 sosta uscita B L1",             1.2, 1, 0.389, 0, 0, 0.4, 0.0, 0.0, 0.0, 0.9, 0.2 },
        { "P7' sosta ingresso B + fascia",    1.2, 1, -0.389, 0, 0, 0.4, 0.0, 0.4, 0.0, 0.9, 0.2 },
        { "P6'' sosta meta' lento B L1",      0.5, 1, 0.0,   0, 0, 0.4, 0.0, 0.0, 0.0, 0.9, 0.2 },
        { "P6''' sosta meta' maschera -20",   1.2, 1, 0.0,   0, 0, 0.4, 0.2, 0.0, 0.0, 0.9, 0.2 },
        /* secondo lancio (P11, scritta dopo il primo): celle in coda, le precedenti non cambiano */
        { "P11 maschera -8 B L1",             1.2, 0, 0, 0, 0, 0.4, 0.08, 0.0, 0.0,  0.9, 0.2 },
        { "P11b maschera -4 B L1",            1.2, 0, 0, 0, 0, 0.4, 0.04, 0.0, 0.0,  0.9, 0.2 },
        { "P11c sosta meta' maschera -8",     1.2, 1, 0.0,   0, 0, 0.4, 0.08, 0.0, 0.0, 0.9, 0.2 },
    };
    int n = sizeof(cfgs) / sizeof(cfgs[0]);
    printf("# audit_imm: NP=%d per ipotesi, NRUN=%d, 15 Hz, ombra [%.3f, %.3f], sigma_v=%.2f, seme 20261114\n", NP, NRUN, A_SH, B_SH, SIGV);
    for (int i = 0; i < n; i++) run_cfg(&cfgs[i]);
    return 0;
}
