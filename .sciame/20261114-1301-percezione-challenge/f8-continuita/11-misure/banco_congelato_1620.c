/* banco.c — BANCO DI PROVA INDIPENDENTE della continuita' visiva (sciame-validazione, f8, f4).
 * Predittori riscritti da capo dalle sole descrizioni a parole (triage, consegne, preproposta, SOLUZIONE_V2 B4-B5).
 * Uso:  banco tara                                  -> taratura.txt (semi 1000-1199, D e T)
 *       banco prova GEO PD E FASCIA CURVA SEME0 NSEMI COMPORTAMENTI ETICHETTA
 *       banco tempo GEO NTRACCE
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "gen.h"

#define CELL 0.10
#define HDIAG 0.0707
#define KH 76
#define NTAU 5
static const int TAUK[NTAU] = {8, 15, 30, 45, 75};       /* 0,53 / 1 / 2 / 3 / 5 s */
static const double TAUS[NTAU] = {0.5, 1, 2, 3, 5};
#define Q_NUC 0.2
#define RVAR 0.0025
#define VMAX 2.5
#define CHI50 1.386
#define CHI90 4.605
#define CHI95 5.991
#define NM 400      /* membri di C-004 */
#define NLIBMAX 200
#define NP 2000     /* particelle di C-001 */
static double BAND = 0.20;

enum { P_L0, P_L1, P_L2, P_L2R, P_L2Q, P_L3, P_C005, P_C005B, P_C004, P_C001, P_C009, P_ESTA, P_ESTB, P_ESTA0, P_ESTB0, P_C004M, NPRED };
static const char *PN[NPRED] = {"L0-nucleo", "L1-fermo", "L2-filtro", "L2r-filtro-ritagliato", "L2q-q0.01", "L3-raggiungibile",
    "C-005", "C-005b", "C-004", "C-001+C-008", "C-001+C-009", "C-EST-A", "C-EST-B", "C-EST-A-senzafascia", "C-EST-B-senzafascia", "C-004m"};

/* ---------------- griglia ---------------- */
typedef struct {
    int nx, ny, n, nA; double gx, areaShadow;
    float *cx, *cy, *dE; uint8_t *dom, *inA, *inA0, *in100, *cntA; int *A;
} Grid;
static Grid G;
static float *D1, *D2, *D3, *D4; static int *SIDX;
static int C4_SM = 3, ONLY_C004 = 0;   /* passate di lisciatura di C-004 (tarate); solo C-004 nei lanci di taratura */

static void grid_make(const Geo *g) {
    double gx = ceil((g->rmax * sin(HALF_FOV) + 0.05) * 10.0) / 10.0;
    G.nx = (int)lround(2 * gx / CELL); G.ny = (int)lround(g->rmax / CELL); G.n = G.nx * G.ny; G.gx = gx;
    G.cx = malloc(G.n * sizeof(float)); G.cy = malloc(G.n * sizeof(float)); G.dE = malloc(G.n * sizeof(float));
    G.dom = calloc(G.n, 1); G.inA = calloc(G.n, 1); G.inA0 = calloc(G.n, 1); G.in100 = calloc(G.n, 1); G.cntA = calloc(G.n, 1);
    G.A = malloc(G.n * sizeof(int)); G.nA = 0; int ns = 0;
    for (int j = 0; j < G.ny; j++) for (int i = 0; i < G.nx; i++) {
        int c = j * G.nx + i; double x = -gx + (i + 0.5) * CELL, y = (j + 0.5) * CELL;
        G.cx[c] = x; G.cy[c] = y; G.dom[c] = in_domain(g, x, y);
        double d = dist_wedge(x, y, g->yp, g->tAe); G.dE[c] = d;
        G.inA0[c] = G.dom[c] && d == 0.0;                    /* «in ombra» (stimata) */
        G.inA[c] = G.dom[c] && (d - HDIAG <= BAND);          /* non «visto libero oltre la fascia» */
        G.in100[c] = G.dom[c] && (d - HDIAG <= 0.40);        /* strato 1 del nucleo: cuneo + fascia 0,40 m */
        if (G.inA0[c]) ns++;
        if (G.inA[c]) G.A[G.nA++] = c;
    }
    G.areaShadow = ns * CELL * CELL;
    for (int a = 0; a < G.nA; a++) { int c = G.A[a], i = c % G.nx, j = c / G.nx, n = 0;
        for (int dj = -1; dj <= 1; dj++) for (int di = -1; di <= 1; di++) { int ii = i + di, jj = j + dj;
            if (ii >= 0 && ii < G.nx && jj >= 0 && jj < G.ny && G.inA[jj * G.nx + ii]) n++; }
        G.cntA[c] = n; }
    D1 = calloc(G.n, sizeof(float)); D2 = calloc(G.n, sizeof(float)); D3 = calloc(G.n, sizeof(float)); D4 = calloc(G.n, sizeof(float)); SIDX = malloc(G.n * sizeof(int));
}
static inline int cell_of(double x, double y) {
    int i = (int)floor((x + G.gx) / CELL), j = (int)floor(y / CELL);
    if (i < 0 || i >= G.nx || j < 0 || j >= G.ny) return -1;
    return j * G.nx + i;
}
/* 0 = fuori griglia o fuori campo («non osservato»); 1 = in A; 2 = visto libero oltre la fascia */
static inline int cls(double x, double y) { int c = cell_of(x, y); if (c < 0 || !G.dom[c]) return 0; return G.inA[c] ? 1 : 2; }

/* ---------------- uscita comune di un predittore ---------------- */
typedef struct { int has_pt, has_reg, alias; double px, py; uint8_t *reg; int i0, i1, j0, j1; } Out;
static void out_clear(Out *o) {
    if (!o->alias && o->i1 >= o->i0) for (int j = o->j0; j <= o->j1; j++) memset(o->reg + j * G.nx + o->i0, 0, o->i1 - o->i0 + 1);
    o->i0 = G.nx; o->i1 = -1; o->j0 = G.ny; o->j1 = -1; o->has_reg = 0;
}
static inline void out_mark(Out *o, int c, uint8_t lv) {
    if (o->reg[c] < lv) o->reg[c] = lv;
    int i = c % G.nx, j = c / G.nx;
    if (i < o->i0) o->i0 = i; if (i > o->i1) o->i1 = i; if (j < o->j0) o->j0 = j; if (j > o->j1) o->j1 = j;
    o->has_reg = 1;
}
/* celle (della maschera) entro r90 dal centro; livello 2 entro r50 (r50 < 0: nessuna R50) */
static int fill_disc(Out *o, double cx, double cy, double r90, double r50, const uint8_t *mask) {
    int i0 = (int)floor((cx - r90 + G.gx) / CELL), i1 = (int)floor((cx + r90 + G.gx) / CELL);
    int j0 = (int)floor((cy - r90) / CELL), j1 = (int)floor((cy + r90) / CELL), cnt = 0;
    if (i0 < 0) i0 = 0; if (j0 < 0) j0 = 0; if (i1 >= G.nx) i1 = G.nx - 1; if (j1 >= G.ny) j1 = G.ny - 1;
    double r2 = r90 * r90, q2 = r50 > 0 ? r50 * r50 : -1;
    for (int j = j0; j <= j1; j++) for (int i = i0; i <= i1; i++) { int c = j * G.nx + i;
        if (mask && !mask[c]) continue;
        double dx = G.cx[c] - cx, dy = G.cy[c] - cy, d2 = dx * dx + dy * dy;
        if (d2 <= r2) { out_mark(o, c, d2 <= q2 ? 2 : 1); cnt++; } }
    return cnt;
}
static const float *SORTKEY;
static int cmp_desc(const void *a, const void *b) { float x = SORTKEY[*(const int *)a], y = SORTKEY[*(const int *)b]; return (x < y) - (x > y); }
/* insieme di massima densita' sulle celle di A: livello 2 fino a p50, livello 1 fino a p90 */
static void hdr_mark(Out *o, const float *dens, double p90, double p50) {
    int m = 0; double tot = 0;
    for (int a = 0; a < G.nA; a++) { int c = G.A[a]; if (dens[c] > 0) { SIDX[m++] = c; tot += dens[c]; } }
    if (tot <= 0) return;
    SORTKEY = dens; qsort(SIDX, m, sizeof(int), cmp_desc);
    double cum = 0;
    for (int t = 0; t < m; t++) { int c = SIDX[t]; if (cum >= p90 * tot) break; out_mark(o, c, cum < p50 * tot ? 2 : 1); cum += dens[c]; }
}
/* lisciatura 3x3 dentro A, che conserva la massa */
static void smooth(const float *in, float *out) {
    for (int a = 0; a < G.nA; a++) out[G.A[a]] = 0;
    for (int a = 0; a < G.nA; a++) { int c = G.A[a]; if (in[c] <= 0) continue;
        float sh = in[c] / G.cntA[c]; int i = c % G.nx, j = c / G.nx;
        for (int dj = -1; dj <= 1; dj++) for (int di = -1; di <= 1; di++) { int ii = i + di, jj = j + dj;
            if (ii >= 0 && ii < G.nx && jj >= 0 && jj < G.ny) { int c2 = jj * G.nx + ii; if (G.inA[c2]) out[c2] += sh; } } }
}
static void clearA(float *d) { for (int a = 0; a < G.nA; a++) d[G.A[a]] = 0; }

/* ---------------- filtro di Kalman del nucleo (un asse) ---------------- */
typedef struct { double p, v, a, b, c; } K1;
static inline void k1_pred(K1 *s, double q) {
    s->p += s->v * DT; double a = s->a, b = s->b, c = s->c;
    s->a = a + 2 * DT * b + DT * DT * c + q * DT * DT * DT / 3; s->b = b + DT * c + q * DT * DT / 2; s->c = c + q * DT;
}
static inline void k1_upd(K1 *s, double z, double R) {
    double S = s->a + R, k1 = s->a / S, k2 = s->b / S, y = z - s->p, a = s->a, b = s->b;
    s->p += k1 * y; s->v += k2 * y; s->a = a - k1 * a; s->b = b - k1 * b; s->c = s->c - k2 * b;
}

/* ---------------- taratura (C-005, C-004) ---------------- */
static double TAB90[KH + 1], TAB50[KH + 1];
static int NLIB; static float LIBA[NLIBMAX][KH + 1], LIBC[NLIBMAX][KH + 1];

/* ---------------- stato di una traccia nascosta ---------------- */
typedef struct {
    K1 kx, ky, qx, qy; double p0x, p0y, v0x, v0y, ux, uy;
    int l0_lost;                                                    /* L0 */
    float c4w[NM]; short c4frz[NM]; double c4px, c4py, c4mx, c4my;              /* C-004 */
    float *pfx, *pfy, *pfvx, *pfvy, *pfw; uint8_t *pfm; Rng pr;     /* C-001 */
    double h9x, h9y; int h9free, h9sw;                              /* C-009 */
    double e2p[2][2], e2v[2][2]; K1 e2x[2], e2y[2];                 /* C-EST: H2 nelle letture A e B */
    double mu1[4], mu2[4], em[4][5]; int est_state[4], est_iexit, est_in;   /* 1 previsto, 0 perso, -1 regione vuota */
    Out out[NPRED];
} Trk;

static void trk_alloc(Trk *t) {
    memset(t, 0, sizeof(*t));
    t->pfx = malloc(NP * sizeof(float)); t->pfy = malloc(NP * sizeof(float)); t->pfvx = malloc(NP * sizeof(float));
    t->pfvy = malloc(NP * sizeof(float)); t->pfw = malloc(NP * sizeof(float)); t->pfm = malloc(NP);
    for (int p = 0; p < NPRED; p++) { t->out[p].reg = calloc(G.n, 1); t->out[p].i0 = G.nx; t->out[p].i1 = -1; t->out[p].j0 = G.ny; t->out[p].j1 = -1; }
    free(t->out[P_C005B].reg); t->out[P_C005B].reg = t->out[P_C005].reg; t->out[P_C005B].alias = 1;
    free(t->out[P_C009].reg); t->out[P_C009].reg = t->out[P_C001].reg; t->out[P_C009].alias = 1;
    free(t->out[P_C004M].reg); t->out[P_C004M].reg = t->out[P_C004].reg; t->out[P_C004M].alias = 1;
}
static inline void alias_copy(Out *dst, const Out *src) { dst->i0 = src->i0; dst->i1 = src->i1; dst->j0 = src->j0; dst->j1 = src->j1; dst->has_reg = src->has_reg; }

/* posizione del membro j di C-004 al passo i */
static inline void c4_pos(const Trk *t, int j, int i, double *x, double *y) {
    int lj = (j % (NM / 2)) % NLIB, ii = i;
    if (j >= NM / 2 && ii > t->c4frz[j]) ii = t->c4frz[j];
    double al = LIBA[lj][ii], cr = LIBC[lj][ii], bx = t->p0x + t->v0x * ii * DT, by = t->p0y + t->v0y * ii * DT;
    *x = bx + t->ux * al - t->uy * cr; *y = by + t->uy * al + t->ux * cr;
}

static void trk_init(Trk *t, K1 kx, K1 ky, K1 qx, K1 qy, uint64_t seed) {
    t->kx = kx; t->ky = ky; t->qx = qx; t->qy = qy;
    t->p0x = kx.p; t->p0y = ky.p; t->v0x = kx.v; t->v0y = ky.v;
    double sp = hypot(kx.v, ky.v); if (sp < 1e-6) { t->ux = 1; t->uy = 0; } else { t->ux = kx.v / sp; t->uy = ky.v / sp; }
    for (int p = 0; p < NPRED; p++) { out_clear(&t->out[p]); t->out[p].has_pt = 0; }
    t->l0_lost = 0;
    /*== C-004: istante di congelamento della scia, uniforme fra l'ingresso in A e l'uscita del membro ==*/
    if (NLIB > 0) for (int j = 0; j < NM; j++) {
        t->c4w[j] = 1.0f; t->c4frz[j] = KH + 1;
        if (j >= NM / 2) { int ien = -1, iex = KH; double x, y; t->c4frz[j] = KH;
            for (int i = 0; i <= KH; i++) { c4_pos(t, j, i, &x, &y); int cl = cls(x, y);
                if (ien < 0) { if (cl == 1) ien = i; } else if (cl != 1) { iex = i; break; } }
            if (ien < 0) ien = 0;
            double u = fmod((j - NM / 2 + 0.5) * 0.6180339887, 1.0);
            t->c4frz[j] = (short)(ien + (int)(u * (iex - ien))); }
    }
    t->c4px = t->p0x; t->c4py = t->p0y; t->c4mx = t->p0x; t->c4my = t->p0y;
    /*== C-001: particelle dalla distribuzione a posteriori del filtro ==*/
    rng_seed(&t->pr, seed, 77, 0, 9);
    for (int n = 0; n < NP; n++) {
        double dx = sqrt(kx.a) * rng_n(&t->pr), dy = sqrt(ky.a) * rng_n(&t->pr);
        double sx = kx.c - kx.b * kx.b / kx.a, sy = ky.c - ky.b * ky.b / ky.a; if (sx < 0) sx = 0; if (sy < 0) sy = 0;
        t->pfx[n] = kx.p + dx; t->pfy[n] = ky.p + dy;
        t->pfvx[n] = kx.v + kx.b / kx.a * dx + sqrt(sx) * rng_n(&t->pr); t->pfvy[n] = ky.v + ky.b / ky.a * dy + sqrt(sy) * rng_n(&t->pr);
        t->pfw[n] = 1.0f / NP; t->pfm[n] = 0; }
    t->h9x = kx.p; t->h9y = ky.p; t->h9free = 0; t->h9sw = 0;
    /*== C-EST ==*/
    for (int r = 0; r < 2; r++) { t->e2p[r][0] = kx.p; t->e2p[r][1] = ky.p; t->e2v[r][0] = kx.v; t->e2v[r][1] = ky.v; t->e2x[r] = kx; t->e2y[r] = ky; }
    for (int v = 0; v < 4; v++) { t->mu1[v] = 0.8; t->mu2[v] = 0.2; t->est_state[v] = 1; }
    t->est_iexit = -1; t->est_in = 0;
}

/*== PRED basi: L0 nucleo, L1 fermo, L2 filtro, L3 raggiungibile, C-005 tabella ==*/
static void step_basi(Trk *t, int i) {
    k1_pred(&t->kx, Q_NUC); k1_pred(&t->ky, Q_NUC); k1_pred(&t->qx, 0.01); k1_pred(&t->qy, 0.01);
    double mx = t->kx.p, my = t->ky.p, va = fmax(t->kx.a, t->ky.a);
    Out *o;
    /* L0: cerchio al 95 % ritagliato sul cuneo, finche' copre meno di meta' del cuneo; poi «perso», assorbente */
    o = &t->out[P_L0]; out_clear(o); o->has_pt = 0;
    if (!t->l0_lost) { int cnt = fill_disc(o, mx, my, sqrt(CHI95 * va), -1, G.inA0);
        if (cnt * CELL * CELL >= 0.5 * G.areaShadow) { t->l0_lost = 1; out_clear(o); } else { o->has_pt = 1; o->px = mx; o->py = my; } }
    /* L1 */
    o = &t->out[P_L1]; o->has_pt = 1; o->px = t->p0x; o->py = t->p0y;
    /* L2: cerchio del filtro al 90 % e al 50 %, non ritagliato; L2r ritagliato su A; L2q con q = 0,01 */
    o = &t->out[P_L2]; out_clear(o); fill_disc(o, mx, my, sqrt(CHI90 * va), sqrt(CHI50 * va), NULL); o->has_pt = 1; o->px = mx; o->py = my;
    o = &t->out[P_L2R]; out_clear(o); fill_disc(o, mx, my, sqrt(CHI90 * va), sqrt(CHI50 * va), G.inA); o->has_pt = 1; o->px = mx; o->py = my;
    double vq = fmax(t->qx.a, t->qy.a);
    o = &t->out[P_L2Q]; out_clear(o); fill_disc(o, t->qx.p, t->qy.p, sqrt(CHI90 * vq), sqrt(CHI50 * vq), NULL); o->has_pt = 1; o->px = t->qx.p; o->py = t->qy.p;
    /* L3: raggiungibile (v_max t + 0,30 m) e non visto libero; nessun punto, un solo livello */
    o = &t->out[P_L3]; out_clear(o); fill_disc(o, t->p0x, t->p0y, VMAX * i * DT + 0.30, -1, G.inA); o->has_pt = 0;
    /* C-005: centro a velocita' costante, raggi da tabella, ritagliato su A. C-005b: stesso, punto = baricentro di R50 */
    o = &t->out[P_C005]; out_clear(o); fill_disc(o, mx, my, TAB90[i], TAB50[i], G.inA); o->has_pt = 1; o->px = mx; o->py = my;
    Out *ob = &t->out[P_C005B]; alias_copy(ob, o); ob->has_pt = 0;
    if (o->has_reg) { double sx = 0, sy = 0; int n = 0, n1 = 0; double tx = 0, ty = 0;
        for (int j = o->j0; j <= o->j1; j++) for (int ii = o->i0; ii <= o->i1; ii++) { int c = j * G.nx + ii;
            if (o->reg[c] == 2) { sx += G.cx[c]; sy += G.cy[c]; n++; } else if (o->reg[c] == 1) { tx += G.cx[c]; ty += G.cy[c]; n1++; } }
        if (n) { ob->has_pt = 1; ob->px = sx / n; ob->py = sy / n; } else if (n1) { ob->has_pt = 1; ob->px = tx / n1; ob->py = ty / n1; } }
}

/*== PRED C-004: fronte + scia ==*/
static void step_c004(Trk *t, int i) {
    Out *o = &t->out[P_C004]; out_clear(o);
    if (NLIB <= 0) return;
    double S[2] = {0, 0}, sx[2] = {0, 0}, sy[2] = {0, 0};
    clearA(D1); clearA(D2);
    for (int j = 0; j < NM; j++) { double x, y; c4_pos(t, j, i, &x, &y); int c = cell_of(x, y), s = j >= NM / 2;
        if (c < 0 || !G.dom[c]) continue;                         /* non osservato: nessuna cella, peso invariato */
        if (!G.inA[c]) { t->c4w[j] *= 0.1f; continue; }           /* visto libero oltre la fascia: un decimo */
        float w = t->c4w[j]; (s ? D2 : D1)[c] += w; S[s] += w; sx[s] += w * x; sy[s] += w * y; }
    for (int sc = 0; sc < 2; sc++) if (S[sc] > 0) { float *src = sc ? D2 : D1, *dst = D3;
        for (int q = 0; q < C4_SM; q++) { dst = (src == D3) ? D4 : D3; smooth(src, dst); src = dst; }
        hdr_mark(o, src, 0.90, 0.50); }
    /* fantasma: media dello scenario piu' pesante, al piu' v_max per ciclo */
    int s = S[0] >= S[1] ? 0 : 1;
    if (S[s] > 0) { double tx = sx[s] / S[s], ty = sy[s] / S[s], dx = tx - t->c4px, dy = ty - t->c4py, d = hypot(dx, dy), lim = VMAX * DT;
        if (d > lim) { dx *= lim / d; dy *= lim / d; } t->c4px += dx; t->c4py += dy; }
    o->has_pt = 1; o->px = t->c4px; o->py = t->c4py;
    /* C-004m: altra lettura del fantasma, la media pesata di tutti i membri non visti liberi */
    Out *om = &t->out[P_C004M]; alias_copy(om, o); om->has_pt = 1;
    if (S[0] + S[1] > 0) { double tx = (sx[0] + sx[1]) / (S[0] + S[1]), ty = (sy[0] + sy[1]) / (S[0] + S[1]), dx = tx - t->c4mx, dy = ty - t->c4my, d = hypot(dx, dy), lim = VMAX * DT;
        if (d > lim) { dx *= lim / d; dy *= lim / d; } t->c4mx += dx; t->c4my += dy; }
    om->px = t->c4mx; om->py = t->c4my;
}

/*== PRED C-001: particelle con modo «sosta», evidenza negativa oltre la fascia; C-007 regioni; C-008 e C-009 punti ==*/
static void step_c001(Trk *t, int i) {
    Out *o = &t->out[P_C001]; out_clear(o); o->has_pt = 0;
    const double sv = sqrt(Q_NUC * DT), pstop = 0.25 * DT, pgo = 0.4 * DT;
    double W = 0, W2 = 0, WA = 0, sx = 0, sy = 0;
    clearA(D1);
    for (int n = 0; n < NP; n++) {
        if (t->pfm[n]) { if (rng_u(&t->pr) < pgo) t->pfm[n] = 0; }
        else if (rng_u(&t->pr) < pstop) t->pfm[n] = 1;
        if (!t->pfm[n]) { t->pfvx[n] += sv * rng_n(&t->pr); t->pfvy[n] += sv * rng_n(&t->pr);
            t->pfx[n] += t->pfvx[n] * DT; t->pfy[n] += t->pfvy[n] * DT; }
        int c = cell_of(t->pfx[n], t->pfy[n]);
        if (c >= 0 && G.dom[c]) { if (!G.inA[c]) t->pfw[n] *= 0.1f; else { D1[c] += t->pfw[n]; WA += t->pfw[n]; sx += t->pfw[n] * t->pfx[n]; sy += t->pfw[n] * t->pfy[n]; } }
        W += t->pfw[n]; W2 += (double)t->pfw[n] * t->pfw[n]; }
    if (WA > 0) { smooth(D1, D2); smooth(D2, D3); hdr_mark(o, D3, 0.90, 0.50); o->has_pt = 1; o->px = sx / WA; o->py = sy / WA; }
    /* ricampionamento sistematico sotto N/2 efficaci */
    if (W > 0 && W * W / W2 < NP / 2.0) {
        static float bx[NP], by[NP], bvx[NP], bvy[NP]; static uint8_t bm[NP];
        double step = W / NP, u = rng_u(&t->pr) * step, cum = t->pfw[0]; int m = 0;
        for (int n = 0; n < NP; n++) { double tgt = u + n * step; while (cum < tgt && m < NP - 1) cum += t->pfw[++m];
            bx[n] = t->pfx[m]; by[n] = t->pfy[m]; bvx[n] = t->pfvx[m]; bvy[n] = t->pfvy[m]; bm[n] = t->pfm[m]; }
        memcpy(t->pfx, bx, sizeof(bx)); memcpy(t->pfy, by, sizeof(by)); memcpy(t->pfvx, bvx, sizeof(bvx)); memcpy(t->pfvy, bvy, sizeof(bvy)); memcpy(t->pfm, bm, sizeof(bm));
        for (int n = 0; n < NP; n++) t->pfw[n] = (float)(W / NP);
    } else if (W > 0 && W < 1e-20) for (int n = 0; n < NP; n++) t->pfw[n] *= 1e20f;
    /* C-009: punto del filtro finche' non sta 3 cicli su celle viste libere, poi la media, al piu' v_max per ciclo */
    Out *o9 = &t->out[P_C009]; alias_copy(o9, o); o9->has_pt = 1;
    if (!t->h9sw) { if (cls(t->kx.p, t->ky.p) == 2) t->h9free++; else t->h9free = 0;
        if (t->h9free > 3) t->h9sw = 1; else { t->h9x = t->kx.p; t->h9y = t->ky.p; } }
    if (t->h9sw && o->has_pt) { double dx = o->px - t->h9x, dy = o->py - t->h9y, d = hypot(dx, dy), lim = VMAX * DT;
        if (d > lim) { dx *= lim / d; dy *= lim / d; } t->h9x += dx; t->h9y += dy; }
    o9->px = t->h9x; o9->py = t->h9y;
}

/*== PRED C-EST: due ipotesi (S3), ritaglio con l'informazione negativa (S4); letture A e B, con e senza fascia ==*/
static inline void k2_pred(K1 *s, double al, double q) { /* covarianza con velocita' smorzata */
    double a = s->a, b = s->b, c = s->c;
    s->a = a + 2 * DT * b + DT * DT * c + q * DT * DT * DT / 3; s->b = al * (b + DT * c) + q * DT * DT / 2; s->c = al * al * c + q * DT;
}
static void step_est(Trk *t, int i) {
    static const double ALPHA[2] = {0.90, 0.95};
    /* H1 = filtro del nucleo gia' propagato in step_basi (t->kx, t->ky) */
    for (int r = 0; r < 2; r++) { t->e2v[r][0] *= ALPHA[r]; t->e2v[r][1] *= ALPHA[r];
        t->e2p[r][0] += t->e2v[r][0] * DT; t->e2p[r][1] += t->e2v[r][1] * DT; k2_pred(&t->e2x[r], ALPHA[r], Q_NUC); k2_pred(&t->e2y[r], ALPHA[r], Q_NUC); }
    { int c = cls(t->kx.p, t->ky.p); if (c == 1) t->est_in = 1; else if (t->est_in && c == 2 && t->est_iexit < 0) t->est_iexit = i; }   /* uscita attesa del transito: il centro di H1 torna su celle viste libere dopo essere stato in A */
    /* densita' sulle celle di A: g1 (D1), g2 lettura A (D2), g2 lettura B (D3) */
    double f1[2] = {0, 0}, f2[2][2] = {{0, 0}, {0, 0}};  /* [fascia: 0 con, 1 senza] ; f2[lettura][fascia] */
    double n1 = CELL * CELL / (2 * M_PI * sqrt(t->kx.a * t->ky.a));
    double n2[2]; for (int r = 0; r < 2; r++) n2[r] = CELL * CELL / (2 * M_PI * sqrt(t->e2x[r].a * t->e2y[r].a));
    for (int a = 0; a < G.nA; a++) { int c = G.A[a]; double x = G.cx[c], y = G.cy[c], e, dx, dy; float g;
        dx = x - t->kx.p; dy = y - t->ky.p; e = 0.5 * (dx * dx / t->kx.a + dy * dy / t->ky.a); g = e < 40 ? (float)(n1 * exp(-e)) : 0; D1[c] = g; f1[0] += g; if (G.inA0[c]) f1[1] += g;
        dx = x - t->e2p[0][0]; dy = y - t->e2p[0][1]; e = 0.5 * (dx * dx / t->e2x[0].a + dy * dy / t->e2y[0].a); g = e < 40 ? (float)(n2[0] * exp(-e)) : 0; D2[c] = g; f2[0][0] += g; if (G.inA0[c]) f2[0][1] += g;
        dx = x - t->e2p[1][0]; dy = y - t->e2p[1][1]; e = 0.5 * (dx * dx / t->e2x[1].a + dy * dy / t->e2y[1].a); g = e < 40 ? (float)(n2[1] * exp(-e)) : 0; D3[c] = g; f2[1][1] += G.inA0[c] ? g : 0; f2[1][0] += g; }
    for (int v = 0; v < 4; v++) { int r = v & 1, nb = v >> 1; /* v: 0 A, 1 B, 2 A senza fascia, 3 B senza fascia */
        Out *o = &t->out[P_ESTA + v]; out_clear(o); o->has_pt = 0;
        double F1 = f1[nb], F2 = f2[r][nb]; const float *g2 = r ? D3 : D2; const uint8_t *mask = nb ? G.inA0 : G.inA;
        if (F1 <= 1e-30 && F2 <= 1e-30) { t->est_state[v] = -1; continue; }           /* regione vuota */
        double m1, m2;
        if (r == 0) { m1 = t->mu1[v] * F1; m2 = t->mu2[v] * F2; } else { m1 = 0.8 * F1; m2 = 0.2 * F2; }
        double s = m1 + m2; if (s <= 1e-300) { t->est_state[v] = -1; continue; }
        m1 /= s; m2 /= s; t->mu1[v] = m1; t->mu2[v] = m2;
        double w1 = F1 > 1e-30 ? m1 / F1 : 0, w2 = F2 > 1e-30 ? m2 / F2 : 0, M = 0, sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0;
        for (int a = 0; a < G.nA; a++) { int c = G.A[a]; if (!mask[c]) continue; double d = w1 * D1[c] + w2 * g2[c]; if (d <= 0) continue;
            double x = G.cx[c], y = G.cy[c]; M += d; sx += d * x; sy += d * y; sxx += d * x * x; syy += d * y * y; sxy += d * x * y; }
        if (M <= 0) { t->est_state[v] = -1; continue; }
        sx /= M; sy /= M; sxx = sxx / M - sx * sx + CELL * CELL / 12; syy = syy / M - sy * sy + CELL * CELL / 12; sxy = sxy / M - sx * sy;
        double seff = sqrt(0.5 * (sxx + syy));
        t->em[v][0] = sx; t->em[v][1] = sy; t->em[v][2] = sxx; t->em[v][3] = syy; t->em[v][4] = sxy;
        if (seff > 0.8) { t->est_state[v] = 0; continue; }                            /* «perso»: nessun inviluppo */
        t->est_state[v] = 1; o->has_pt = 1; o->px = sx; o->py = sy;
        double det = sxx * syy - sxy * sxy; if (det < 1e-12) det = 1e-12;
        double r95 = sqrt(CHI95 * fmax(sxx, syy)) + CELL;
        int i0 = (int)floor((sx - r95 + G.gx) / CELL), i1 = (int)floor((sx + r95 + G.gx) / CELL), j0 = (int)floor((sy - r95) / CELL), j1 = (int)floor((sy + r95) / CELL);
        if (i0 < 0) i0 = 0; if (j0 < 0) j0 = 0; if (i1 >= G.nx) i1 = G.nx - 1; if (j1 >= G.ny) j1 = G.ny - 1;
        for (int j = j0; j <= j1; j++) for (int ii = i0; ii <= i1; ii++) { int c = j * G.nx + ii; if (!mask[c]) continue;
            double dx = G.cx[c] - sx, dy = G.cy[c] - sy, d2 = (syy * dx * dx - 2 * sxy * dx * dy + sxx * dy * dy) / det;
            if (d2 <= CHI95) out_mark(o, c, d2 <= CHI50 ? 2 : 1); }
    }
}
/*== FINE PRED ==*/

static void step_all(Trk *t, int i) { step_basi(t, i); step_c004(t, i); if (ONLY_C004) return; step_c001(t, i); step_est(t, i); }

/* ---------------- misure ---------------- */
typedef struct { int n90, n50, nfree, nnot100; } RS;
static RS reg_stat(const Out *o) {
    RS r = {0, 0, 0, 0};
    if (!o->has_reg) return r;
    for (int j = o->j0; j <= o->j1; j++) for (int i = o->i0; i <= o->i1; i++) { int c = j * G.nx + i; uint8_t v = o->reg[c];
        if (v) { r.n90++; if (v == 2) r.n50++; if (G.dom[c] && !G.inA[c]) r.nfree++; if (G.dom[c] && !G.in100[c]) r.nnot100++; } }
    return r;
}
static double dist_reg(const Out *o, double x, double y) {
    double best = 1e9; if (!o->has_reg) return best;
    for (int j = o->j0; j <= o->j1; j++) for (int i = o->i0; i <= o->i1; i++) { int c = j * G.nx + i;
        if (o->reg[c]) { double d = hypot(G.cx[c] - x, G.cy[c] - y); if (d < best) best = d; } }
    return best;
}

#define CAP 1000
typedef struct { int n, nreg, npt, in50, in90, in100, nout, nsc; double a50, a90, sc, fr_free, fr_tot; int ne; float err[CAP]; } HC;
typedef struct {
    int npass, pgap, pgaplate, cyc, cycreg, cycpt, maxgap_sum, maxgap_max, stepc, stepp, backc, backp, freec, freep, fptc, fptp, n100c, n100p,
        w50, w80, w08, nre, re40, re30, gate95, ngate, cyc0530, in0530; double stepsum; int nstep;
    int nj; float jump[CAP], jratio[CAP];
} PC;
static HC H[NPRED][NBEH][NTAU];
static PC P[NPRED][NBEH];
static struct { int valid, invalid, outA, outA0, missopen, hidcyc, l0_n, l0_lostbefore, c1ok_n, c1ok; int nd; float l0dur[CAP];
    int est_prev[4], est_perso[4], est_vuoto[4], est_domlate[4], est_domcyc[4], est_passperso[4], est_passvuoto[4];
    int due_n, due_stranger, due_c1, due_r100gone; int due_gate[NPRED]; } GB[NBEH];
static int NVALID[NBEH];

static int cmpf(const void *a, const void *b) { float x = *(const float *)a, y = *(const float *)b; return (x > y) - (x < y); }
static double quant(float *v, int n, double q) { if (n <= 0) return NAN; qsort(v, n, sizeof(float), cmpf); int k = (int)ceil(q * n) - 1; if (k < 0) k = 0; if (k >= n) k = n - 1; return v[k]; }

static Trk TR[10];

/* un passaggio: ritorna 1 se valido. Se cal != NULL raccoglie i dati di taratura. */
typedef struct { int ok, klast, kre; double err[KH + 1]; int hid[KH + 1]; float la[KH + 1], lc[KH + 1]; } CalRec;

static int run_pass(const Geo *g, int beh, uint64_t seed, double pd, int curve, CalRec *cal) {
    static Traj T; traj_make(&T, g, beh, seed);
    Rng rm, rm2; rng_seed(&rm, seed, (uint64_t)g->name, (uint64_t)beh, 2); rng_seed(&rm2, seed, (uint64_t)g->name, (uint64_t)beh, 3);
    static int zok[MAXK], z2ok[MAXK]; static double zx[MAXK], zy[MAXK], z2x[MAXK], z2y[MAXK];
    for (int k = 0; k < T.n; k++) { double z[2]; zok[k] = measure(g, &rm, T.x[k], T.y[k], pd, curve, z); zx[k] = z[0]; zy[k] = z[1];
        z2ok[k] = 0; if (T.has2) { z2ok[k] = measure(g, &rm2, T.x2[k], T.y2[k], pd, curve, z); z2x[k] = z[0]; z2y[k] = z[1]; } }
    /* ingresso nel buio: primo ciclo non rilevabile dopo almeno un ciclo rilevabile */
    int khide = -1, seen = 0;
    for (int k = 0; k < T.n; k++) { int d = detectable(g, T.x[k], T.y[k]); if (d) seen = 1; else if (seen) { khide = k; break; } }
    if (khide < 0) return 0;
    /* filtro in vista (q = 0,2 e q = 0,01) */
    K1 kx, ky, qx, qy; int nm = 0, kfirst = -1, klast = -1; double fx = 0, fy = 0;
    for (int k = 0; k < khide; k++) {
        if (nm >= 2) { k1_pred(&kx, Q_NUC); k1_pred(&ky, Q_NUC); k1_pred(&qx, 0.01); k1_pred(&qy, 0.01); }
        if (!zok[k]) continue;
        if (nm == 0) { kfirst = k; fx = zx[k]; fy = zy[k]; }
        else if (nm == 1) { double dt = (k - kfirst) * DT;
            kx.p = zx[k]; kx.v = (zx[k] - fx) / dt; kx.a = RVAR; kx.b = RVAR / dt; kx.c = 2 * RVAR / (dt * dt); ky = kx; ky.p = zy[k]; ky.v = (zy[k] - fy) / dt; qx = kx; qy = ky; }
        else { k1_upd(&kx, zx[k], RVAR); k1_upd(&ky, zy[k], RVAR); k1_upd(&qx, zx[k], RVAR); k1_upd(&qy, zy[k], RVAR); }
        nm++; klast = k; }
    if (nm < 4) return 0;                                   /* traccia non confermata */
    /* lo stato dei filtri va riportato a klast: rifaccio il filtro fino a klast */
    { nm = 0; for (int k = 0; k <= klast; k++) {
        if (nm >= 2) { k1_pred(&kx, Q_NUC); k1_pred(&ky, Q_NUC); k1_pred(&qx, 0.01); k1_pred(&qy, 0.01); }
        if (!zok[k]) continue;
        if (nm == 0) { kfirst = k; fx = zx[k]; fy = zy[k]; }
        else if (nm == 1) { double dt = (k - kfirst) * DT;
            kx.p = zx[k]; kx.v = (zx[k] - fx) / dt; kx.a = RVAR; kx.b = RVAR / dt; kx.c = 2 * RVAR / (dt * dt); ky = kx; ky.p = zy[k]; ky.v = (zy[k] - fy) / dt; qx = kx; qy = ky; }
        else { k1_upd(&kx, zx[k], RVAR); k1_upd(&ky, zy[k], RVAR); k1_upd(&qx, zx[k], RVAR); k1_upd(&qy, zy[k], RVAR); }
        nm++; } }
    if (cal) { /* taratura: errore del centro a velocita' costante e percorso residuo, per ciclo */
        cal->ok = 1; cal->klast = klast; double th_c, th_s, sp = hypot(kx.v, ky.v); th_c = sp > 1e-6 ? kx.v / sp : 1; th_s = sp > 1e-6 ? ky.v / sp : 0;
        int open = 1;
        for (int i = 0; i <= KH; i++) { int k = klast + i; if (k >= T.n) { cal->hid[i] = 0; cal->la[i] = cal->lc[i] = 0; continue; }
            double ex = T.x[k] - (kx.p + kx.v * i * DT), ey = T.y[k] - (ky.p + ky.v * i * DT);
            cal->err[i] = hypot(ex, ey); cal->la[i] = (float)(ex * th_c + ey * th_s); cal->lc[i] = (float)(-ex * th_s + ey * th_c);
            if (i > 0 && k > khide && zok[k]) open = 0;
            cal->hid[i] = i > 0 && open && !zok[k] && !detectable(g, T.x[k], T.y[k]); }
        return 1; }
    Trk *t = &TR[0]; trk_init(t, kx, ky, qx, qy, seed);
    NVALID[beh]++; GB[beh].valid++;
    int gap[NPRED], maxgap[NPRED], anygap[NPRED], lategap[NPRED], anystep[NPRED], anyback[NPRED], anyfree[NPRED], anyfpt[NPRED], any100[NPRED];
    double lpx[NPRED], lpy[NPRED]; int lhas[NPRED]; RS last_rs[NPRED];
    for (int p = 0; p < NPRED; p++) { gap[p] = maxgap[p] = anygap[p] = lategap[p] = anystep[p] = anyback[p] = anyfree[p] = anyfpt[p] = any100[p] = 0; lhas[p] = 0; lpx[p] = lpy[p] = 0; last_rs[p] = (RS){0, 0, 0, 0}; }
    int anyoutA = 0, anyoutA0 = 0, kre = -1, l0lostk = -1, stranger = 0, estperso[4] = {0, 0, 0, 0}, estvuoto[4] = {0, 0, 0, 0}, estdom[4] = {0, 0, 0, 0};
    int kend = klast + KH; if (kend > T.n - 1) kend = T.n - 1;
    for (int k = klast + 1; k <= kend; k++) {
        int i = k - klast;
        if (k > khide && (zok[k] || z2ok[k])) { kre = k; stranger = !zok[k]; break; }
        step_all(t, i);
        int hidden = !detectable(g, T.x[k], T.y[k]);
        if (!hidden) GB[beh].missopen++; else GB[beh].hidcyc++;
        int ct = cell_of(T.x[k], T.y[k]); int tout = (ct < 0 || !G.dom[ct]);
        if (hidden && !tout) { if (!G.inA[ct]) anyoutA = 1; if (!G.inA0[ct]) anyoutA0 = 1; }
        if (t->l0_lost && l0lostk < 0) l0lostk = k;
        for (int v = 0; v < 4; v++) { if (t->est_state[v] == 1) GB[beh].est_prev[v]++; else if (t->est_state[v] == 0) { GB[beh].est_perso[v]++; estperso[v] = 1; } else { GB[beh].est_vuoto[v]++; estvuoto[v] = 1; }
            if (t->est_iexit >= 0 && i > t->est_iexit + 8 && t->mu1[v] > 0.5) { GB[beh].est_domcyc[v]++; estdom[v] = 1; } }
        int itau = -1; for (int q = 0; q < NTAU; q++) if (TAUK[q] == i) itau = q;
        for (int p = 0; p < NPRED; p++) { Out *o = &t->out[p]; PC *pc = &P[p][beh];
            RS rs = reg_stat(o); last_rs[p] = rs;
            pc->cyc++; if (o->has_reg) { pc->cycreg++; if (gap[p] > maxgap[p]) maxgap[p] = gap[p]; gap[p] = 0; }
            else { gap[p]++; anygap[p] = 1; if (i > 5) lategap[p] = 1; }
            if (o->has_pt) { pc->cycpt++;
                if (lhas[p]) { double dx = o->px - lpx[p], dy = o->py - lpy[p], d = hypot(dx, dy); pc->stepsum += d; pc->nstep++;
                    if (d > 0.1667 + 1e-6) { pc->stepc++; anystep[p] = 1; }
                    if (dx * t->ux + dy * t->uy < -0.05) { pc->backc++; anyback[p] = 1; } }
                if (cls(o->px, o->py) == 2) { pc->fptc++; anyfpt[p] = 1; }
                lpx[p] = o->px; lpy[p] = o->py; lhas[p] = 1; } else lhas[p] = 0;
            if (rs.nfree > 0) { pc->freec++; anyfree[p] = 1; }
            if (rs.nnot100 > 0) { pc->n100c++; any100[p] = 1; }
            double a90 = rs.n90 * CELL * CELL, a50 = rs.n50 * CELL * CELL;
            if (o->has_reg) { if (a90 > 0.5 * G.areaShadow) pc->w50++; if (a90 > 0.8 * G.areaShadow) pc->w80++; if (sqrt(a90 / M_PI) > 0.8) pc->w08++; }
            int t90 = !tout && o->has_reg && o->reg[ct] >= 1, t50 = !tout && o->has_reg && o->reg[ct] == 2;
            if (hidden && i >= 8 && i <= 45) { pc->cyc0530++; if (t90) pc->in0530++; }
            if (getenv("DEBUG_C004") && p == P_C004 && itau >= 3 && hidden && !t90 && (beh == B_SOSTA || beh == B_RALLENTA || beh == B_TORNA)) {
                double ex = T.x[k] - t->p0x, ey = T.y[k] - t->p0y; int nb = 0; if (ct >= 0) { int ci = ct % G.nx, cj = ct / G.nx; for (int dj = -1; dj <= 1; dj++) for (int di = -1; di <= 1; di++) { int c2 = (cj + dj) * G.nx + ci + di; if (c2 >= 0 && c2 < G.n && o->reg[c2]) nb++; } }
                fprintf(stderr, "DBG %s seme? tau=%.0f vero=(%.2f,%.2f) lungo=%.2f traverso=%.2f v0=%.2f dE=%.2f inA=%d fuori=%d n90=%d vicini_in_R90=%d\n", BEH_NAME[beh], TAUS[itau], T.x[k], T.y[k], ex * t->ux + ey * t->uy, -ex * t->uy + ey * t->ux, hypot(t->v0x, t->v0y), ct >= 0 ? G.dE[ct] : -1, ct >= 0 ? G.inA[ct] : -1, tout, rs.n90, nb); }
            if (itau >= 0 && hidden) { HC *h = &H[p][beh][itau];
                h->n++; if (o->has_reg) { h->nreg++; h->a50 += a50; h->a90 += a90; h->fr_free += rs.nfree; h->fr_tot += rs.n90; }
                if (o->has_pt) { h->npt++; if (h->ne < CAP) h->err[h->ne++] = (float)hypot(o->px - T.x[k], o->py - T.y[k]); }
                int t100 = tout || G.in100[ct];
                if (tout) h->nout++;
                if (t50) h->in50++; if (t90) h->in90++; if (t100) h->in100++;
                if (!tout) { /* punteggio logaritmico ad anelli: 0,5 / 0,4 / 0,1; fuori da R100: 9,21 */
                    int n100 = 0; for (int c = 0; c < G.n; c++) n100 += G.in100[c];
                    double A100 = n100 * CELL * CELL, s;
                    double ring = A100 - (rs.n90 - rs.nnot100) * CELL * CELL; if (ring < CELL * CELL) ring = CELL * CELL;
                    if (!o->has_reg) s = G.in100[ct] ? -log(1.0 / A100) : 9.21;
                    else if (rs.n50 > 0) { if (t50) s = -log(0.5 / a50); else if (t90) s = -log(0.4 / fmax(a90 - a50, CELL * CELL)); else if (G.in100[ct]) s = -log(0.1 / ring); else s = 9.21; }
                    else { if (t90) s = -log(0.9 / a90); else if (G.in100[ct]) s = -log(0.1 / ring); else s = 9.21; }
                    h->sc += s; h->nsc++; } }
        }
    }
    /* chiusura del passaggio */
    for (int p = 0; p < NPRED; p++) { PC *pc = &P[p][beh]; pc->npass++; if (gap[p] > maxgap[p]) maxgap[p] = gap[p];
        pc->pgap += anygap[p]; pc->pgaplate += lategap[p]; pc->maxgap_sum += maxgap[p]; if (maxgap[p] > pc->maxgap_max) pc->maxgap_max = maxgap[p];
        pc->stepp += anystep[p]; pc->backp += anyback[p]; pc->freep += anyfree[p]; pc->fptp += anyfpt[p]; pc->n100p += any100[p]; }
    GB[beh].outA += anyoutA; GB[beh].outA0 += anyoutA0;
    for (int v = 0; v < 4; v++) { GB[beh].est_passperso[v] += estperso[v]; GB[beh].est_passvuoto[v] += estvuoto[v]; GB[beh].est_domlate[v] += estdom[v]; }
    if (kre >= 0) { double z0 = stranger ? z2x[kre] : zx[kre], z1 = stranger ? z2y[kre] : zy[kre];
        /* regola del nucleo per il riaggancio (B5, «Ritorno»): geometrica, con una sola traccia pendente */
        double rr = hypot(z0, z1), th = fabs(atan2(z0, z1));
        int c1 = dist_wedge(z0, z1, g->yp, g->tAe) <= 0.40 && g->rmax - rr > 0.40 && rr * sin(fmax(HALF_FOV - th, 0.0)) > 0.40;
        GB[beh].c1ok_n++; GB[beh].c1ok += c1;
        if (beh == B_DUE) { GB[beh].due_n++; if (stranger) { GB[beh].due_stranger++; GB[beh].due_c1 += c1; if (c1 && !detectable(g, T.x[kre], T.y[kre])) GB[beh].due_r100gone++; } }
        GB[beh].l0_n++; if (l0lostk >= 0) GB[beh].l0_lostbefore++;
        if (GB[beh].nd < CAP) GB[beh].l0dur[GB[beh].nd++] = (float)(((l0lostk >= 0 ? l0lostk : kre) - (klast + 1)) * DT);
        for (int p = 0; p < NPRED; p++) { Out *o = &t->out[p]; PC *pc = &P[p][beh]; pc->nre++;
            double d = dist_reg(o, z0, z1); if (d <= 0.40) pc->re40++; if (d <= 0.30) pc->re30++;
            if (stranger && d <= 0.40) GB[beh].due_gate[p]++;
            if (lhas[p] && pc->nj < CAP) { double j = hypot(z0 - lpx[p], z1 - lpy[p]); pc->jump[pc->nj] = (float)j;
                pc->jratio[pc->nj] = last_rs[p].n90 > 0 ? (float)(j / sqrt(last_rs[p].n90 * CELL * CELL / M_PI)) : -1; pc->nj++; }
            /* porta al 95 %: L2 = innovazione normalizzata del filtro; C-EST = ellisse dichiarata (momenti ritagliati) */
            if (p == P_L2 || p == P_L2Q) { K1 ax = p == P_L2 ? t->kx : t->qx, ay = p == P_L2 ? t->ky : t->qy; double q = p == P_L2 ? Q_NUC : 0.01; k1_pred(&ax, q); k1_pred(&ay, q);
                double dx = z0 - ax.p, dy = z1 - ay.p; pc->ngate++; if (dx * dx / (ax.a + RVAR) + dy * dy / (ay.a + RVAR) <= CHI95) pc->gate95++; }
            if (p >= P_ESTA) { int v = p - P_ESTA; pc->ngate++;
                if (t->est_state[v] == 1) { double sxx = t->em[v][2], syy = t->em[v][3], sxy = t->em[v][4], det = sxx * syy - sxy * sxy, dx = z0 - t->em[v][0], dy = z1 - t->em[v][1];
                    if (det < 1e-12) det = 1e-12; if ((syy * dx * dx - 2 * sxy * dx * dy + sxx * dy * dy) / det <= CHI95) pc->gate95++; } }
        } }
    return 1;
}

/* ---------------- taratura ---------------- */
static const double W_SQ[7] = {60, 10, 10, 10, 5, 5, 0}, W_GI[7] = {30, 10, 20, 20, 10, 10, 0};
typedef struct { float e; float w; } EW;
static int cmpew(const void *a, const void *b) { float x = ((const EW *)a)->e, y = ((const EW *)b)->e; return (x > y) - (x < y); }
static double wquant(EW *v, int n, double q) { if (n <= 0) return NAN; qsort(v, n, sizeof(EW), cmpew); double tot = 0, cum = 0; for (int i = 0; i < n; i++) tot += v[i].w;
    for (int i = 0; i < n; i++) { cum += v[i].w; if (cum >= q * tot) return v[i].e; } return v[n - 1].e; }

static void do_tara(void) {
    FILE *f = fopen("taratura.txt", "w");
    const char gs[2] = {'D', 'T'};
    static CalRec R[7][200];
    for (int gi = 0; gi < 2; gi++) { Geo g = geo_make(gs[gi], 0.0);
        for (int b = 0; b < 7; b++) for (int s = 0; s < 200; s++) { R[b][s].ok = 0; run_pass(&g, b, 1000 + s, 0.9, 0, &R[b][s]); }
        double t90[KH + 1], t50[KH + 1]; t90[0] = t50[0] = 0.10;
        static float e[200]; static EW ew[1400];
        for (int i = 1; i <= KH; i++) { double mx = 0; const int onpath[5] = {0, 1, 2, 3, 6};
            for (int q = 0; q < 5; q++) { int b = onpath[q], n = 0; for (int s = 0; s < 200; s++) if (R[b][s].ok && R[b][s].hid[i]) e[n++] = (float)R[b][s].err[i];
                if (n >= 20) { qsort(e, n, sizeof(float), cmpf); int kq = (int)ceil(0.90 * (n + 1)) - 1; if (kq >= n) kq = n - 1; if (e[kq] > mx) mx = e[kq]; } }
            t90[i] = fmax(mx, t90[i - 1]);
            int n = 0; for (int b = 0; b < 6; b++) { int nb = 0; for (int s = 0; s < 200; s++) nb += R[b][s].ok; if (!nb) continue;
                for (int s = 0; s < 200; s++) if (R[b][s].ok && R[b][s].hid[i]) { ew[n].e = (float)R[b][s].err[i]; ew[n].w = (float)(W_SQ[b] / nb); n++; } }
            double md = n >= 20 ? wquant(ew, n, 0.50) : t50[i - 1]; t50[i] = fmin(md, t90[i]); if (t50[i] < 0.05) t50[i] = 0.05; }
        fprintf(f, "GEO %c\n", gs[gi]);
        for (int i = 0; i <= KH; i++) fprintf(f, "%.4f %.4f\n", t90[i], t50[i]);
        int nl = 0; for (int s = 0; s < 200; s++) nl += R[0][s].ok;
        fprintf(f, "LIB %d\n", nl);
        for (int s = 0; s < 200; s++) if (R[0][s].ok) { for (int i = 0; i <= KH; i++) fprintf(f, "%.4f %.4f ", R[0][s].la[i], R[0][s].lc[i]); fprintf(f, "\n"); }
        printf("taratura %c: percorsi di libreria %d; R90 a 0,5/1/2/3/5 s = %.2f %.2f %.2f %.2f %.2f m; R50 = %.2f %.2f %.2f %.2f %.2f m\n", gs[gi], nl,
               t90[8], t90[15], t90[30], t90[45], t90[75], t50[8], t50[15], t50[30], t50[45], t50[75]);
    }
    fclose(f);
}
static void load_tara(char gname) {
    FILE *f = fopen("taratura.txt", "r"); if (!f) { fprintf(stderr, "manca taratura.txt\n"); exit(2); }
    char want = gname == 'D' ? 'D' : 'T', tag[16], gc; int found = 0;
    while (fscanf(f, "%15s %c", tag, &gc) == 2) { double a90[KH + 1], a50[KH + 1];
        for (int i = 0; i <= KH; i++) if (fscanf(f, "%lf %lf", &a90[i], &a50[i]) != 2) exit(3);
        int nl; if (fscanf(f, "%15s %d", tag, &nl) != 2) exit(3);
        static float la[NLIBMAX][KH + 1], lc[NLIBMAX][KH + 1];
        for (int s = 0; s < nl; s++) for (int i = 0; i <= KH; i++) if (fscanf(f, "%f %f", &la[s][i], &lc[s][i]) != 2) exit(3);
        if (gc == want) { memcpy(TAB90, a90, sizeof(a90)); memcpy(TAB50, a50, sizeof(a50)); NLIB = nl; memcpy(LIBA, la, sizeof(la)); memcpy(LIBC, lc, sizeof(lc)); found = 1; } }
    fclose(f); if (!found) { fprintf(stderr, "taratura assente per %c\n", want); exit(2); }
}

static double now_ms(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec * 1e3 + ts.tv_nsec * 1e-6; }

int main(int argc, char **argv) {
    if (getenv("C4_SM")) C4_SM = atoi(getenv("C4_SM"));
    if (getenv("ONLY_C004")) ONLY_C004 = 1;
    if (argc >= 2 && !strcmp(argv[1], "tara")) { Geo g = geo_make('T', 0); grid_make(&g); do_tara(); return 0; }
    if (argc >= 4 && !strcmp(argv[1], "tempo")) {
        Geo g = geo_make(argv[2][0], 0.0); int nt = atoi(argv[3]); grid_make(&g); load_tara(g.name);
        for (int q = 0; q < nt; q++) trk_alloc(&TR[q]);
        static float tm[5][40000]; int n = 0; const char *gn[5] = {"basi(L0,L1,L2,L2r,L2q,L3,C-005)", "C-004", "C-001(2000 particelle)", "C-EST(4 varianti)", "tutti"};
        static float tinit[40000]; int ni = 0;
        for (int rep = 0; rep < 40; rep++) { double t0 = now_ms();
            for (int q = 0; q < nt; q++) { K1 kx = {-(g.tA * g.ys + 0.25) - 0.02 * q, 0.6 + 0.05 * q, 0.0008, 0.004, 0.04}, ky = {g.ys, 0.05, 0.0008, 0.004, 0.04}; trk_init(&TR[q], kx, ky, kx, ky, 7000 + rep * 10 + q); }
            tinit[ni++] = (float)(now_ms() - t0);
            for (int i = 1; i <= KH; i++) { double a, b, c, d, e;
                a = now_ms(); for (int q = 0; q < nt; q++) step_basi(&TR[q], i);
                b = now_ms(); for (int q = 0; q < nt; q++) step_c004(&TR[q], i);
                c = now_ms(); for (int q = 0; q < nt; q++) step_c001(&TR[q], i);
                d = now_ms(); for (int q = 0; q < nt; q++) step_est(&TR[q], i);
                e = now_ms(); tm[0][n] = (float)(b - a); tm[1][n] = (float)(c - b); tm[2][n] = (float)(d - c); tm[3][n] = (float)(e - d); tm[4][n] = (float)(e - a); n++; } }
        printf("# tempo per ciclo, %d tracce nascoste insieme, geometria %c (celle di A: %d), %d cicli; C, -O2, un filo\n", nt, g.name, G.nA, n);
        for (int q = 0; q < 5; q++) printf("T\t%c\t%d\t%s\tmediana %.4f ms\tp95 %.4f ms\tmax %.4f ms\n", g.name, nt, gn[q], quant(tm[q], n, 0.5), quant(tm[q], n, 0.95), quant(tm[q], n, 1.0));
        printf("T\t%c\t%d\tinizializzazione (all'ingresso)\tmediana %.4f ms\tmax %.4f ms\n", g.name, nt, quant(tinit, ni, 0.5), quant(tinit, ni, 1.0));
        return 0; }
    if (argc < 11 || strcmp(argv[1], "prova")) { fprintf(stderr, "uso: banco tara | banco prova GEO PD E FASCIA CURVA SEME0 NSEMI COMPORTAMENTI ETICHETTA | banco tempo GEO N\n"); return 1; }
    char gname = argv[2][0]; double pd = atof(argv[3]), e = atof(argv[4]); BAND = atof(argv[5]); int curve = atoi(argv[6]);
    long seed0 = atol(argv[7]); int ns = atoi(argv[8]); const char *behs = argv[9], *tag = argv[10];
    Geo g = geo_make(gname, e); grid_make(&g); load_tara(gname); trk_alloc(&TR[0]);
    int n100 = 0; for (int c = 0; c < G.n; c++) n100 += G.in100[c];
    printf("# banco prova geo=%c pd=%.2f e=%.2f fascia=%.2f curva=%d semi=%ld..%ld comportamenti=%s etichetta=%s\n", gname, pd, e, BAND, curve, seed0, seed0 + ns - 1, behs, tag);
    printf("# passate di lisciatura di C-004: %d\n", C4_SM);
    printf("# griglia %dx%d celle da 0,10 m; ombra stimata %.2f m2; A (ombra+fascia) %.2f m2; R100 %.2f m2\n", G.nx, G.ny, G.areaShadow, G.nA * CELL * CELL, n100 * CELL * CELL);
    double t0 = now_ms();
    for (int b = 0; b < NBEH; b++) { if (!strchr(behs, '0' + b)) continue;
        for (int s = 0; s < ns; s++) if (!run_pass(&g, b, (uint64_t)(seed0 + s), pd, curve, NULL)) GB[b].invalid++; }
    printf("# tempo del lancio %.1f s\n", (now_ms() - t0) / 1e3);
    /* uscita */
    for (int b = 0; b < NBEH; b++) { if (!strchr(behs, '0' + b)) continue;
        printf("G\t%s\t%s\tvalidi=%d\tscartati=%d\tpass_vero_fuori_A=%d\tpass_vero_fuori_ombra=%d\tcicli_nascosti=%d\tcicli_mancati_in_vista=%d\tricomparsi=%d\tL0_perso_prima=%d\tL0_durata_previsto_med=%.3f\tq25=%.3f\tq75=%.3f\tC1_riaggancio=%d/%d\n",
               tag, BEH_NAME[b], GB[b].valid, GB[b].invalid, GB[b].outA, GB[b].outA0, GB[b].hidcyc, GB[b].missopen, GB[b].l0_n, GB[b].l0_lostbefore,
               quant(GB[b].l0dur, GB[b].nd, 0.5), quant(GB[b].l0dur, GB[b].nd, 0.25), quant(GB[b].l0dur, GB[b].nd, 0.75), GB[b].c1ok, GB[b].c1ok_n);
        for (int v = 0; v < 4; v++) printf("E\t%s\t%s\t%s\tcicli_previsto=%d\tcicli_perso=%d\tcicli_vuoto=%d\tpass_perso=%d\tpass_vuoto=%d\tpass_transito_dominante_tardi=%d\tcicli_dominante_tardi=%d\n",
               tag, BEH_NAME[b], PN[P_ESTA + v], GB[b].est_prev[v], GB[b].est_perso[v], GB[b].est_vuoto[v], GB[b].est_passperso[v], GB[b].est_passvuoto[v], GB[b].est_domlate[v], GB[b].est_domcyc[v]);
        if (b == B_DUE) { printf("D\t%s\tdue\teventi=%d\tesce_prima_lo_sconosciuto=%d\tnucleo_riaggancia_lo_sconosciuto=%d\tR100_tolta_a_soggetto_nascosto=%d", tag, GB[b].due_n, GB[b].due_stranger, GB[b].due_c1, GB[b].due_r100gone);
            for (int p = 0; p < NPRED; p++) printf("\t%s=%d", PN[p], GB[b].due_gate[p]); printf("\n"); }
        for (int p = 0; p < NPRED; p++) { PC *pc = &P[p][b];
            printf("P\t%s\t%s\t%s\tnpass=%d\tpass_vuoto=%d\tpass_vuoto_dopo5=%d\tcicli=%d\tcicli_regione=%d\tcicli_punto=%d\tvuoto_max_medio=%.2f\tvuoto_max=%d\tpassi_oltre=%d\tpass_passi_oltre=%d\tindietro=%d\tpass_indietro=%d\tpasso_medio=%.4f\tR90_su_libero_cicli=%d\tpass=%d\tpunto_su_libero_cicli=%d\tpass=%d\tR90_fuori_R100_cicli=%d\tpass=%d\tampio50=%d\tampio80=%d\tampio08m=%d\tnre=%d\tre40=%d\tre30=%d\tsalto_med=%.3f\tsalto_p90=%.3f\tsalto_su_raggio_med=%.3f\tporta95=%d/%d\tcicli0530=%d\tdentro0530=%d\n",
                   tag, BEH_NAME[b], PN[p], pc->npass, pc->pgap, pc->pgaplate, pc->cyc, pc->cycreg, pc->cycpt, pc->npass ? (double)pc->maxgap_sum / pc->npass : 0, pc->maxgap_max,
                   pc->stepc, pc->stepp, pc->backc, pc->backp, pc->nstep ? pc->stepsum / pc->nstep : 0, pc->freec, pc->freep, pc->fptc, pc->fptp, pc->n100c, pc->n100p, pc->w50, pc->w80, pc->w08,
                   pc->nre, pc->re40, pc->re30, quant(pc->jump, pc->nj, 0.5), quant(pc->jump, pc->nj, 0.9), quant(pc->jratio, pc->nj, 0.5), pc->gate95, pc->ngate, pc->cyc0530, pc->in0530);
            for (int q = 0; q < NTAU; q++) { HC *h = &H[p][b][q]; static float tmp[CAP]; memcpy(tmp, h->err, h->ne * sizeof(float));
                printf("H\t%s\t%s\t%s\t%.1f\tn=%d\tnreg=%d\tnpt=%d\tin50=%d\tin90=%d\tin100=%d\tfuori_griglia=%d\tarea50=%.3f\tarea90=%.3f\tombra=%.3f\terr_med=%.3f\terr_p90=%.3f\tpunteggio=%.3f\tquota_su_libero=%.4f\n",
                       tag, BEH_NAME[b], PN[p], TAUS[q], h->n, h->nreg, h->npt, h->in50, h->in90, h->in100, h->nout, h->nreg ? h->a50 / h->nreg : 0, h->nreg ? h->a90 / h->nreg : 0, G.areaShadow,
                       quant(tmp, h->ne, 0.5), quant(tmp, h->ne, 0.9), h->nsc ? h->sc / h->nsc : NAN, h->fr_tot > 0 ? h->fr_free / h->fr_tot : 0); } } }
    /* errore del punto sulle miscele (quantili pesati sui passaggi) */
    for (int mix = 0; mix < 2; mix++) { const double *w = mix ? W_GI : W_SQ;
        for (int p = 0; p < NPRED; p++) for (int q = 0; q < NTAU; q++) { static EW ew[7 * CAP]; int n = 0;
            for (int b = 0; b < 7; b++) { if (!strchr(behs, '0' + b) || NVALID[b] == 0 || w[b] == 0) continue; HC *h = &H[p][b][q];
                for (int k = 0; k < h->ne; k++) { ew[n].e = h->err[k]; ew[n].w = (float)(w[b] / NVALID[b]); n++; } }
            if (n > 0) { double med = wquant(ew, n, 0.5), p90 = wquant(ew, n, 0.9); printf("M\t%s\t%s\t%s\t%.1f\tn=%d\terr_med=%.3f\terr_p90=%.3f\n", tag, mix ? "giurato" : "squadra", PN[p], TAUS[q], n, med, p90); } } }
    return 0;
}
