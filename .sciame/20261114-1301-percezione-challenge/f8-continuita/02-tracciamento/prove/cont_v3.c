/* cont.c — sciame-tracciamento, f8 (continuita' visiva). Confronto dei predittori durante l'occlusione.
   Uso: ./cont <file traiettorie> <yp> <rmax> <dw> <guard> <seme> [np]
   Scena dell'avversario (scena_parte3.py): sensore in (0,0) verso +y, campo +-43,5 gradi, pannello a y=yp.
   Metodi: a = Kalman CV libero; b = lo stesso ritagliato sul non-libero (e regola del nucleo "meta' dell'ombra");
   c = IMM a 5 modi con pesi aggiornati dall'evidenza negativa; d0/d1/d2 = particelle (CV; +sosta; +sosta+svolta);
   e = insieme raggiungibile; f = fermo all'ultima misura. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define DT (1.0/15.0)
#define CELL 0.25
#define GX0 (-8.0)
#define GY0 (-2.0)
#define GNX 64
#define GNY 40
#define NC (GNX*GNY)
#define NB 7
#define NT 6
#define MAXN 1200
#define NPMAX 4000
enum {MA, MB, MC, MD0, MD1, MD2, MD3, MD3M, MD3W, ME, MF, NM};
#define NPF 4
static const char *MN[NM] = {"a KF libero ", "b KF ritagl.", "c IMM 5 modi", "d0 part. CV ", "d1 +sosta   ", "d2 +sosta+sv", "d3 nominale ", "d3 ibr. tar.", "d3 ibr. peg.", "e raggiung. ", "f fermo     "};
static const char *BN[NB + 1] = {"prosegue", "sosta", "torna", "lontano", "rallenta", "svolta", "sostalunga", "MISCELA"};
static const int EVK[NT] = {8, 15, 30, 45, 60, 75};
static const double EVT[NT] = {0.5, 1, 2, 3, 4, 5};

static double SIG = 0.05, PD = 0.9, Q = 0.2, VMAX = 2.5, YP = 2.0, RMAXS = 6.0, TANF;
static int NP = 500; static double LT = 0.5, LS = 0.25, LR = 0.3, PU = 0.5;
static const double C50 = 1.386, C90 = 4.605, C95 = 5.991, C99 = 9.21;

static inline int vis(double x, double y, double w) {
    if (y <= 0.05) return 0;
    if (x * x + y * y > RMAXS * RMAXS || fabs(x) > y * TANF) return 0;
    if (w > 0 && y > YP && fabs(x * YP / y) <= w / 2) return 2;
    return 1;
}
static inline int cidx(double x, double y) {
    int i = (int)floor((x - GX0) / CELL), j = (int)floor((y - GY0) / CELL);
    if (i < 0 || i >= GNX || j < 0 || j >= GNY) return -1;
    return j * GNX + i;
}
static inline double ccx(int c) { return GX0 + (c % GNX + 0.5) * CELL; }
static inline double ccy(int c) { return GY0 + (c / GNX + 0.5) * CELL; }
static unsigned char gt[NC], ge[NC];
static double ASH; static int NSHE;

/* ---------- rng ---------- */
static uint64_t rs;
static inline uint64_t rnext(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 2685821657736338717ULL; }
static inline double runi(void) { return (rnext() >> 11) * (1.0 / 9007199254740992.0); }
static int ghave = 0; static double gspare;
static inline double rgau(void) {
    if (ghave) { ghave = 0; return gspare; }
    double u, v, s; do { u = 2 * runi() - 1; v = 2 * runi() - 1; s = u * u + v * v; } while (s >= 1 || s == 0);
    s = sqrt(-2 * log(s) / s); gspare = v * s; ghave = 1; return u * s;
}
static void rseed(uint64_t s) { rs = s * 0x9E3779B97F4A7C15ULL + 0x1234567ULL; if (!rs) rs = 1; ghave = 0; for (int i = 0; i < 8; i++) rnext(); }

/* ---------- Kalman isotropo (come l'avversario) ---------- */
typedef struct { double x, y, vx, vy, a, b, c; } KF;
static void kf_init(KF *s, double z1x, double z1y, double z2x, double z2y, int dk) {
    double R = SIG * SIG, T = DT * dk; s->x = z2x; s->y = z2y; s->vx = (z2x - z1x) / T; s->vy = (z2y - z1y) / T;
    s->a = R; s->b = R / T; s->c = 2 * R / (T * T);
}
static void kf_predict(KF *s) {
    s->x += s->vx * DT; s->y += s->vy * DT; double a = s->a, b = s->b, c = s->c;
    s->a = a + 2 * b * DT + c * DT * DT + Q * DT * DT * DT / 3; s->b = b + c * DT + Q * DT * DT / 2; s->c = c + Q * DT;
}
static void kf_update(KF *s, double zx, double zy, double R) {
    double S = s->a + R, k1 = s->a / S, k2 = s->b / S, ex = zx - s->x, ey = zy - s->y;
    s->x += k1 * ex; s->y += k1 * ey; s->vx += k2 * ex; s->vy += k2 * ey;
    double a = s->a, b = s->b, c = s->c; s->a = (1 - k1) * a; s->b = (1 - k1) * b; s->c = c - k2 * b;
}

/* ---------- regione a massa piu' alta su celle ---------- */
static double cm[NC]; static int ord[NC]; static unsigned char in50[NC], in90[NC];
static int cmpd(const void *p, const void *q) { double a = cm[*(const int *)p], b = cm[*(const int *)q]; return a < b ? 1 : a > b ? -1 : 0; }
static double POUT = 0, HL50 = 0.5, HL90 = 0.9;
static void hpd(double *a50, double *a90) {   /* cm[] normalizzato a 1; POUT = massa gia' dichiarata "fuori area" */
    int n = 0; for (int c = 0; c < NC; c++) { in50[c] = in90[c] = 0; if (cm[c] > 0) ord[n++] = c; }
    qsort(ord, n, sizeof(int), cmpd);
    double acc = POUT; int n50 = 0, n90 = 0;
    for (int i = 0; i < n; i++) { int c = ord[i]; if (acc < HL50) { in50[c] = 1; n50++; } if (acc < HL90) { in90[c] = 1; n90++; } else break; acc += cm[c]; }
    *a50 = n50 * CELL * CELL; *a90 = n90 * CELL * CELL;
}
static double score(int tc) { if (tc < 0 || ge[tc] == 0) return 0; double a = POUT, m = cm[tc]; for (int c = 0; c < NC; c++) if (cm[c] > m) a += cm[c]; return a; }
static double EPS = 0.05, RZX, RZY, RRAD;
static void floor_mix(void) {   /* mescola eps di massa uniforme sulle celle d'ombra raggiungibili */
    int n = 0; for (int c = 0; c < NC; c++) if (ge[c] == 2) { double dx = ccx(c) - RZX, dy = ccy(c) - RZY; if (dx * dx + dy * dy <= RRAD * RRAD) n++; }
    if (!n) return; POUT *= 1 - EPS;
    for (int c = 0; c < NC; c++) { cm[c] *= 1 - EPS; if (ge[c] == 2) { double dx = ccx(c) - RZX, dy = ccy(c) - RZY; if (dx * dx + dy * dy <= RRAD * RRAD) cm[c] += EPS / n; } }
}
static double LV[4][NT] = {{.5, .5, .5, .5, .5, .5}, {.9, .9, .9, .9, .9, .9}, {.5, .5, .5, .5, .5, .5}, {.9, .9, .9, .9, .9, .9}};
static void project(double *px, double *py) {  /* se il punto cade su cella vista libera, va alla cella non libera piu' vicina */
    int c = cidx(*px, *py); if (c >= 0 && ge[c] != 1) return;
    double best = 1e18; int bc = -1;
    for (int k = 0; k < NC; k++) if (ge[k] != 1) { double dx = ccx(k) - *px, dy = ccy(k) - *py, d = dx * dx + dy * dy; if (d < best) { best = d; bc = k; } }
    if (bc >= 0) { *px = ccx(bc); *py = ccy(bc); }
}

/* ---------- IMM a 5 modi ---------- */
#define NMO 5
static const double AM[NMO][4] = {{1, 0, 0, 1}, {0, 0, 0, 0}, {-1, 0, 0, -1}, {0, -1, 1, 0}, {0, 1, -1, 0}};
typedef struct { double m[NMO][4], P[NMO][16], mu[NMO]; } IMM;
static double PI_[NMO][NMO];
static void imm_setup(void) {
    memset(PI_, 0, sizeof PI_);
    PI_[0][1] = 0.25 * DT; PI_[0][2] = 0.05 * DT; PI_[0][3] = 0.05 * DT; PI_[0][4] = 0.05 * DT;
    PI_[1][0] = 0.2 * DT; PI_[1][2] = 0.2 * DT; PI_[2][1] = 0.1 * DT;
    for (int i = 0; i < NMO; i++) { double s = 0; for (int j = 0; j < NMO; j++) if (j != i) s += PI_[i][j]; PI_[i][i] = 1 - s; }
}
static void imm_spawn(IMM *I, const KF *k) {
    static const double mu0[NMO] = {0.90, 0.04, 0.02, 0.02, 0.02};
    for (int j = 0; j < NMO; j++) {
        I->mu[j] = mu0[j]; I->m[j][0] = k->x; I->m[j][1] = k->y; I->m[j][2] = k->vx; I->m[j][3] = k->vy;
        double *P = I->P[j]; memset(P, 0, 16 * sizeof(double));
        P[0] = P[5] = k->a; P[10] = P[15] = k->c; P[2] = P[8] = k->b; P[7] = P[13] = k->b;
    }
}
static void imm_step(IMM *I) {
    double c[NMO], m0[NMO][4], P0[NMO][16];
    for (int j = 0; j < NMO; j++) { c[j] = 0; for (int i = 0; i < NMO; i++) c[j] += PI_[i][j] * I->mu[i]; }
    for (int j = 0; j < NMO; j++) {
        double w[NMO]; for (int i = 0; i < NMO; i++) w[i] = c[j] > 1e-300 ? PI_[i][j] * I->mu[i] / c[j] : (i == j);
        for (int a = 0; a < 4; a++) { m0[j][a] = 0; for (int i = 0; i < NMO; i++) m0[j][a] += w[i] * I->m[i][a]; }
        for (int a = 0; a < 16; a++) P0[j][a] = 0;
        for (int i = 0; i < NMO; i++) if (w[i] > 0) { double d[4]; for (int a = 0; a < 4; a++) d[a] = I->m[i][a] - m0[j][a];
            for (int a = 0; a < 4; a++) for (int b = 0; b < 4; b++) P0[j][4 * a + b] += w[i] * (I->P[i][4 * a + b] + d[a] * d[b]); }
    }
    for (int j = 0; j < NMO; j++) {
        double F[16] = {1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1}; const double *A = AM[j];
        F[2] = DT * A[0]; F[3] = DT * A[1]; F[6] = DT * A[2]; F[7] = DT * A[3];
        double t[16], *P = I->P[j], *m = I->m[j], mm[4];
        for (int a = 0; a < 4; a++) { mm[a] = 0; for (int b = 0; b < 4; b++) mm[a] += F[4 * a + b] * m0[j][b]; }
        for (int a = 0; a < 4; a++) m[a] = mm[a];
        for (int a = 0; a < 4; a++) for (int b = 0; b < 4; b++) { double s = 0; for (int k = 0; k < 4; k++) s += F[4 * a + k] * P0[j][4 * k + b]; t[4 * a + b] = s; }
        for (int a = 0; a < 4; a++) for (int b = 0; b < 4; b++) { double s = 0; for (int k = 0; k < 4; k++) s += t[4 * a + k] * F[4 * b + k]; P[4 * a + b] = s; }
        if (j == 1) { P[0] += 0.02 * DT; P[5] += 0.02 * DT; }
        else {
            double q3 = Q * DT * DT * DT / 3, q2 = Q * DT * DT / 2, q1 = Q * DT;
            P[0] += q3; P[5] += q3; P[10] += q1; P[15] += q1;
            /* blocco posizione-velocita': q2 * A */
            P[2] += q2 * A[0]; P[3] += q2 * A[1]; P[6] += q2 * A[2]; P[7] += q2 * A[3];
            P[8] += q2 * A[0]; P[12] += q2 * A[1]; P[9] += q2 * A[2]; P[13] += q2 * A[3];
        }
        I->mu[j] = c[j];
    }
}
static const double ZN[7] = {-2.4, -1.6, -0.8, 0, 0.8, 1.6, 2.4};
static void imm_neg(IMM *I, double west) {
    double zw[7], s = 0; for (int i = 0; i < 7; i++) { zw[i] = exp(-0.5 * ZN[i] * ZN[i]); s += zw[i]; } for (int i = 0; i < 7; i++) zw[i] /= s;
    double tot = 0;
    for (int j = 0; j < NMO; j++) {
        double *P = I->P[j]; double l11 = sqrt(fmax(P[0], 1e-12)), l21 = P[4] / l11, l22 = sqrt(fmax(P[5] - l21 * l21, 1e-12)), mf = 0;
        for (int a = 0; a < 7; a++) for (int b = 0; b < 7; b++) {
            double x = I->m[j][0] + l11 * ZN[a], y = I->m[j][1] + l21 * ZN[a] + l22 * ZN[b];
            if (vis(x, y, west) == 1) mf += zw[a] * zw[b];
        }
        I->mu[j] *= (1 - PD * mf); tot += I->mu[j];
    }
    if (tot > 0) for (int j = 0; j < NMO; j++) I->mu[j] /= tot;
}
static void imm_point(const IMM *I, double *x, double *y) { *x = *y = 0; for (int j = 0; j < NMO; j++) { *x += I->mu[j] * I->m[j][0]; *y += I->mu[j] * I->m[j][1]; } }
static void imm_cells(const IMM *I, int clip) {   /* riempie cm[] normalizzato */
    double tot = 0; double inv[NMO][3], nrm[NMO];
    for (int j = 0; j < NMO; j++) { const double *P = I->P[j]; double det = fmax(P[0] * P[5] - P[1] * P[4], 1e-12);
        inv[j][0] = P[5] / det; inv[j][1] = -P[1] / det; inv[j][2] = P[0] / det; nrm[j] = I->mu[j] / (2 * M_PI * sqrt(det)); }
    for (int c = 0; c < NC; c++) {
        cm[c] = 0; if (clip && ge[c] == 1) continue;
        double x = ccx(c), y = ccy(c), d = 0;
        for (int j = 0; j < NMO; j++) { if (I->mu[j] < 1e-4) continue; double dx = x - I->m[j][0], dy = y - I->m[j][1];
            double e = inv[j][0] * dx * dx + 2 * inv[j][1] * dx * dy + inv[j][2] * dy * dy; if (e < 40) d += nrm[j] * exp(-0.5 * e); }
        cm[c] = d; tot += d;
    }
    POUT = 0; if (tot > 0) for (int c = 0; c < NC; c++) { cm[c] /= tot; if (clip && ge[c] == 0) { POUT += cm[c]; cm[c] = 0; } }
}
static double imm_gate(const IMM *I, double zx, double zy) {  /* min Mahalanobis^2 sui modi con peso >= 1% */
    double best = 1e18, R = SIG * SIG;
    for (int j = 0; j < NMO; j++) { if (I->mu[j] < 0.01) continue; const double *P = I->P[j];
        double a = P[0] + R, b = P[1], d = P[5] + R, det = a * d - b * b, dx = zx - I->m[j][0], dy = zy - I->m[j][1];
        double e = (d * dx * dx - 2 * b * dx * dy + a * dy * dy) / det; if (e < best) best = e; }
    return best;
}

/* ---------- particelle ---------- */
typedef struct { double x[NPMAX], y[NPMAX], vx[NPMAX], vy[NPMAX], w[NPMAX]; unsigned char md[NPMAX]; int kind; } PF;
static void pf_spawn(PF *p, const KF *k, int kind) {
    double sa = sqrt(k->a), sc = sqrt(k->c); p->kind = kind;
    for (int i = 0; i < NP; i++) { p->x[i] = k->x + sa * rgau(); p->y[i] = k->y + sa * rgau(); p->vx[i] = k->vx + sc * rgau(); p->vy[i] = k->vy + sc * rgau(); p->md[i] = 0; p->w[i] = 1.0 / NP; }
}
static inline void rot(double *vx, double *vy, double ang) { double c = cos(ang), s = sin(ang), a = *vx * c - *vy * s, b = *vx * s + *vy * c; *vx = a; *vy = b; }
static void pf_move(PF *p) {
    double sq = sqrt(Q * DT);
    for (int i = 0; i < NP; i++) {
        if (p->kind == 1) { if (p->md[i] == 0) { if (runi() < 1 - exp(-0.25 * DT)) p->md[i] = 1; } else if (runi() < 1 - exp(-0.4 * DT)) p->md[i] = 0; }
        else if (p->kind == 2) {
            if (p->md[i] == 0) {
                double u = runi();
                if (u < 0.25 * DT) p->md[i] = 1;
                else if (u < 0.40 * DT) { if (runi() < 0.4) { p->vx[i] = -p->vx[i]; p->vy[i] = -p->vy[i]; } else rot(&p->vx[i], &p->vy[i], (runi() < 0.5 ? -1 : 1) * (M_PI / 4 + runi() * M_PI / 4)); }
            } else if (runi() < 0.3 * DT) {
                p->md[i] = 0; double u = runi();
                if (u < 0.25) { p->vx[i] = -p->vx[i]; p->vy[i] = -p->vy[i]; } else if (u < 0.40) rot(&p->vx[i], &p->vy[i], (runi() < 0.5 ? -1 : 1) * (M_PI / 4 + runi() * M_PI / 4));
            }
        }
        else if (p->kind == 3) {
            if (p->md[i] == 0) {
                double u = runi();
                if (u < LS * DT) p->md[i] = 1;
                else if (u < (LS + LT) * DT) rot(&p->vx[i], &p->vy[i], 2 * M_PI * runi());
            } else if (runi() < LR * DT) { p->md[i] = 0; if (runi() < PU) rot(&p->vx[i], &p->vy[i], 2 * M_PI * runi()); }
        }
        if (p->md[i] == 0) {
            p->vx[i] += sq * rgau(); p->vy[i] += sq * rgau();
            if (p->kind >= 2) { double s = hypot(p->vx[i], p->vy[i]); if (s > VMAX) { p->vx[i] *= VMAX / s; p->vy[i] *= VMAX / s; } }
            p->x[i] += p->vx[i] * DT; p->y[i] += p->vy[i] * DT;
        }
    }
}
static void pf_neg(PF *p, double west) {
    double tot = 0, s2 = 0;
    for (int i = 0; i < NP; i++) { if (vis(p->x[i], p->y[i], west) == 1) p->w[i] *= (1 - PD); tot += p->w[i]; }
    if (tot <= 0) { for (int i = 0; i < NP; i++) p->w[i] = 1.0 / NP; return; }
    for (int i = 0; i < NP; i++) { p->w[i] /= tot; s2 += p->w[i] * p->w[i]; }
    if (1.0 / s2 < NP / 2.0) {
        static double tx[NPMAX], ty[NPMAX], tvx[NPMAX], tvy[NPMAX]; static unsigned char tm[NPMAX];
        double u = runi() / NP, c = p->w[0]; int i = 0;
        for (int j = 0; j < NP; j++) { double t = u + (double)j / NP; while (c < t && i < NP - 1) { i++; c += p->w[i]; }
            tx[j] = p->x[i]; ty[j] = p->y[i]; tvx[j] = p->vx[i]; tvy[j] = p->vy[i]; tm[j] = p->md[i]; }
        memcpy(p->x, tx, NP * sizeof(double)); memcpy(p->y, ty, NP * sizeof(double)); memcpy(p->vx, tvx, NP * sizeof(double)); memcpy(p->vy, tvy, NP * sizeof(double)); memcpy(p->md, tm, NP);
        for (int j = 0; j < NP; j++) p->w[j] = 1.0 / NP;
    }
}
static void pf_point(const PF *p, double *x, double *y) { *x = *y = 0; for (int i = 0; i < NP; i++) { *x += p->w[i] * p->x[i]; *y += p->w[i] * p->y[i]; } }
static double pf_cells(const PF *p) {  /* cm[] ; ritorna la massa fuori griglia */
    memset(cm, 0, sizeof cm); double out = 0;
    for (int i = 0; i < NP; i++) { int c = cidx(p->x[i], p->y[i]); if (c >= 0 && ge[c] != 0) cm[c] += p->w[i]; else out += p->w[i]; }
    POUT = out; if (p->kind == 3) floor_mix(); return out;
}
static void pf_mode(const PF *p, double *x, double *y) {  /* media locale attorno alla cella (3x3) piu' pesante; lascia cm[] riempito */
    pf_cells(p); double best = -1; int bc = -1;
    for (int c = 0; c < NC; c++) if (cm[c] > 0) { int i = c % GNX, j = c / GNX; double s = 0;
        for (int dj = -1; dj <= 1; dj++) for (int di = -1; di <= 1; di++) { int ii = i + di, jj = j + dj; if (ii >= 0 && ii < GNX && jj >= 0 && jj < GNY) s += cm[jj * GNX + ii]; }
        if (s > best) { best = s; bc = c; } }
    if (bc < 0) { pf_point(p, x, y); return; }
    double sx = 0, sy = 0, sw = 0, cx = ccx(bc), cy = ccy(bc);
    for (int i = 0; i < NP; i++) { double dx = p->x[i] - cx, dy = p->y[i] - cy; if (dx * dx + dy * dy <= 0.4 * 0.4) { sx += p->w[i] * p->x[i]; sy += p->w[i] * p->y[i]; sw += p->w[i]; } }
    if (sw > 0) { *x = sx / sw; *y = sy / sw; } else { *x = cx; *y = cy; }
}
static int near90(double zx, double zy) { for (int c = 0; c < NC; c++) if (in90[c]) { double dx = ccx(c) - zx, dy = ccy(c) - zy; if (dx * dx + dy * dy <= 0.45 * 0.45) return 1; } return 0; }
static double pf_near(const PF *p, double zx, double zy, double d) { double s = 0; for (int i = 0; i < NP; i++) { double dx = p->x[i] - zx, dy = p->y[i] - zy; if (dx * dx + dy * dy <= d * d) s += p->w[i]; } return s; }
static double pf_massvis(const PF *p, double w, int code) { double s = 0; for (int i = 0; i < NP; i++) if (vis(p->x[i], p->y[i], w) == code) s += p->w[i]; return s; }

/* ---------- raccolta ---------- */
static float ERR[NB][NT][NM][MAXN]; static int NEV[NB][NT];
static double COV50[NB][NT][NM], COV90[NB][NT][NM], AR90[NB][NT][NM], AR50[NB][NT][NM], NLL[NB][NT][NM], FREE90[NB][NT][NM];
static float SC[NB][NT][MAXN]; static double MOUT[NB][NT], TOUT[NB][NT], RENEAR[NB][NM], PTFREE[NB][NT][NM];
static long SM_N[NB][NM + 1], SM_BIG[NB][NM + 1], SM_BACK[NB][NM + 1]; static double SM_MAX[NB][NM + 1];
static long HIDC[NB], NUCC[NB]; static double NUCDUR[NB]; static int NTR[NB];
static float JUMP[NB][NM][MAXN]; static int NRE[NB]; static double RE90[NB][NM], REID[NB][NM], RETAU[NB];
static double TNS = 0; static long TCY = 0;

static int cmpf(const void *a, const void *b) { float x = *(const float *)a, y = *(const float *)b; return x < y ? -1 : x > y; }
static double pct(float *v, int n, double p) { if (n == 0) return NAN; static float t[NB * MAXN]; memcpy(t, v, n * sizeof(float)); qsort(t, n, sizeof(float), cmpf); int i = (int)(p * (n - 1) + 0.5); return t[i]; }
static double gcellmass(double mx, double my, double var, int c) {
    double s = sqrt(2 * var), x0 = GX0 + (c % GNX) * CELL, y0 = GY0 + (c / GNX) * CELL;
    return 0.25 * (erf((x0 + CELL - mx) / s) - erf((x0 - mx) / s)) * (erf((y0 + CELL - my) / s) - erf((y0 - my) / s));
}
static inline double nowns(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e9 + t.tv_nsec; }

static PF pf[NPF]; static double TX[400], TY[400];

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "uso: cont file yp rmax dw guard seme [np]\n"); return 1; }
    FILE *f = fopen(argv[1], "r"); YP = atof(argv[2]); RMAXS = atof(argv[3]); double dw = atof(argv[4]), guard = atof(argv[5]); long seed = atol(argv[6]);
    if (argc > 7) NP = atoi(argv[7]);
    if (getenv("LT")) LT = atof(getenv("LT")); if (getenv("LS")) LS = atof(getenv("LS")); if (getenv("LR")) LR = atof(getenv("LR")); if (getenv("PU")) PU = atof(getenv("PU"));
    TANF = tan(43.5 * M_PI / 180); imm_setup();
    { const char *nm[4] = {"L50", "L90", "W50", "W90"}; for (int v = 0; v < 4; v++) if (getenv(nm[v])) sscanf(getenv(nm[v]), "%lf %lf %lf %lf %lf %lf", &LV[v][0], &LV[v][1], &LV[v][2], &LV[v][3], &LV[v][4], &LV[v][5]); }
    if (getenv("EPS")) EPS = atof(getenv("EPS"));
    int bi, n, trial = 0; double w, yped, wprev = -1, west = 0;
    while (fscanf(f, " T %d %lf %lf %d", &bi, &w, &yped, &n) == 4) {
        for (int k = 0; k < n; k++) if (fscanf(f, "%lf %lf", &TX[k], &TY[k]) != 2) return 2;
        if (w != wprev) { wprev = w; west = w + dw + guard; int ns = 0; NSHE = 0;
            for (int c = 0; c < NC; c++) { gt[c] = vis(ccx(c), ccy(c), w); ge[c] = vis(ccx(c), ccy(c), west); ns += gt[c] == 2; NSHE += ge[c] == 2; } ASH = ns * CELL * CELL; }
        rseed(seed * 1000003ULL + trial); trial++;
        KF kf; int havekf = 0, havez = 0, kp = 0, k0 = -1, kl = 0, seen = 0, alive = 0, nuc = 1, nucn = 0; double zpx = 0, zpy = 0, zlx = 0, zly = 0;
        IMM imm; double pp[NM + 1][2], pd[NM + 1][2]; int havep = 0, handed = 0, cntf = 0;
        NTR[bi]++;
        for (int k = 0; k < n; k++) {
            double x = TX[k], y = TY[k]; int vt = vis(x, y, w); int det = vt == 1 && runi() < PD;
            double zx = x + SIG * rgau(), zy = y + SIG * rgau();
            if (!havekf) { if (det) { if (!havez) { zpx = zx; zpy = zy; kp = k; havez = 1; } else { kf_init(&kf, zpx, zpy, zx, zy, k - kp); havekf = 1; zlx = zx; zly = zy; kl = k; } } continue; }
            kf_predict(&kf);
            if (k0 < 0 && vt != 1) k0 = k;
            if (k0 >= 0 && vt == 1) seen = 1;
            if (det) {
                if (k0 >= 0) {   /* ricomparsa */
                    if (!alive) break;
                    RZX = zlx; RZY = zly; RRAD = VMAX * (k - kl) * DT + 3 * SIG * 1.414; HL50 = 0.5; HL90 = 0.9;
                    int r = NRE[bi]; if (r >= MAXN) break; NRE[bi]++; RETAU[bi] += (k - kl) * DT; int zc = cidx(zx, zy); double a50, a90, px, py;
                    double rho90 = sqrt(C90 * (kf.a + SIG * SIG)), dk = hypot(kf.x - zx, kf.y - zy), d2 = dk * dk / (kf.a + SIG * SIG);
                    JUMP[bi][MA][r] = dk; RE90[bi][MA] += dk <= rho90; REID[bi][MA] += d2 <= C99;
                    px = kf.x; py = kf.y; project(&px, &py); JUMP[bi][MB][r] = hypot(px - zx, py - zy); RE90[bi][MB] += dk <= rho90; REID[bi][MB] += d2 <= C99;
                    imm_step(&imm); imm_point(&imm, &px, &py); JUMP[bi][MC][r] = hypot(px - zx, py - zy); imm_cells(&imm, 0); hpd(&a50, &a90);
                    RE90[bi][MC] += zc >= 0 && in90[zc]; RENEAR[bi][MC] += near90(zx, zy); REID[bi][MC] += imm_gate(&imm, zx, zy) <= C99;
                    for (int q = 0; q < NPF; q++) { pf_move(&pf[q]); pf_point(&pf[q], &px, &py); JUMP[bi][MD0 + q][r] = hypot(px - zx, py - zy); pf_cells(&pf[q]); hpd(&a50, &a90);
                        RE90[bi][MD0 + q] += zc >= 0 && in90[zc]; RENEAR[bi][MD0 + q] += near90(zx, zy); REID[bi][MD0 + q] += pf_near(&pf[q], zx, zy, 0.5) >= 0.01; }
                    JUMP[bi][MD3M][r] = JUMP[bi][MD3W][r] = hypot(pp[MD3M][0] - zx, pp[MD3M][1] - zy); REID[bi][MD3M] = REID[bi][MD3W] = REID[bi][MD3];
                    { int tq = 0; double tau = (k - k0) * DT; while (tq < NT - 1 && EVT[tq] < tau) tq++; pf_cells(&pf[3]); HL90 = LV[1][tq]; hpd(&a50, &a90); RE90[bi][MD3M] += zc >= 0 && in90[zc]; RENEAR[bi][MD3M] += near90(zx, zy); HL90 = LV[3][tq]; hpd(&a50, &a90); RE90[bi][MD3W] += zc >= 0 && in90[zc]; RENEAR[bi][MD3W] += near90(zx, zy); HL90 = 0.9; }
                    double rad = VMAX * (k - kl) * DT + 3 * SIG * 1.414; int in = hypot(zx - zlx, zy - zly) <= rad; RE90[bi][ME] += in; REID[bi][ME] += in; JUMP[bi][ME][r] = NAN;
                    JUMP[bi][MF][r] = hypot(zx - zlx, zy - zly); RE90[bi][MF] += 0; REID[bi][MF] += 0;
                    break;
                }
                kf_update(&kf, zx, zy, SIG * SIG); zlx = zx; zly = zy; kl = k; alive = 0; havep = 0; continue;
            }
            /* ciclo senza misura */
            if (!alive) { imm_spawn(&imm, &kf); for (int q = 0; q < NPF; q++) pf_spawn(&pf[q], &kf, q); alive = 1; }
            else { imm_step(&imm); pf_move(&pf[0]); pf_move(&pf[1]); pf_move(&pf[2]); double t0 = nowns(); pf_move(&pf[3]); TNS += nowns() - t0; }
            RZX = zlx; RZY = zly; RRAD = VMAX * (k - kl) * DT + 3 * SIG * 1.414; HL50 = 0.5; HL90 = 0.9;
            imm_neg(&imm, west); pf_neg(&pf[0], west); pf_neg(&pf[1], west); pf_neg(&pf[2], west);
            double t0 = nowns(); pf_neg(&pf[3], west); double p3x, p3y, m3x, m3y, a50, a90; pf_point(&pf[3], &p3x, &p3y); project(&p3x, &p3y); pf_mode(&pf[3], &m3x, &m3y); hpd(&a50, &a90); TNS += nowns() - t0; TCY++;
            if (k0 < 0) continue;
            /* punti mostrati */
            double pt[NM + 1][2];
            pt[MA][0] = kf.x; pt[MA][1] = kf.y; pt[MB][0] = kf.x; pt[MB][1] = kf.y; project(&pt[MB][0], &pt[MB][1]);
            imm_point(&imm, &pt[MC][0], &pt[MC][1]); project(&pt[MC][0], &pt[MC][1]);
            pf_point(&pf[0], &pt[MD0][0], &pt[MD0][1]); project(&pt[MD0][0], &pt[MD0][1]);
            pf_point(&pf[1], &pt[MD1][0], &pt[MD1][1]); project(&pt[MD1][0], &pt[MD1][1]);
            pf_point(&pf[2], &pt[MD2][0], &pt[MD2][1]); project(&pt[MD2][0], &pt[MD2][1]);
            pt[MD3][0] = p3x; pt[MD3][1] = p3y;
            { int kc = cidx(kf.x, kf.y); if (!havep) { handed = 0; cntf = 0; } if (kc < 0 || ge[kc] == 1) cntf++; else cntf = 0; if (cntf >= 3) handed = 1;
              double tx = handed ? p3x : kf.x, ty = handed ? p3y : kf.y; (void)m3x; (void)m3y;
              if (havep) { double dx = tx - pp[MD3M][0], dy = ty - pp[MD3M][1], d = hypot(dx, dy), lim = VMAX * DT; if (d > lim) { dx *= lim / d; dy *= lim / d; } pt[MD3M][0] = pp[MD3M][0] + dx; pt[MD3M][1] = pp[MD3M][1] + dy; }
              else { pt[MD3M][0] = tx; pt[MD3M][1] = ty; }
              pt[MD3W][0] = pt[MD3M][0]; pt[MD3W][1] = pt[MD3M][1]; }
            double rad = VMAX * (k - kl) * DT + 3 * SIG * 1.414; { double sx = 0, sy = 0; int nn = 0;
                for (int c = 0; c < NC; c++) if (ge[c] != 1) { double dx = ccx(c) - zlx, dy = ccy(c) - zly; if (dx * dx + dy * dy <= rad * rad) { sx += ccx(c); sy += ccy(c); nn++; } }
                if (nn) { pt[ME][0] = sx / nn; pt[ME][1] = sy / nn; } else { pt[ME][0] = zlx; pt[ME][1] = zly; } }
            pt[MF][0] = zlx; pt[MF][1] = zly;
            if (havep) { pt[NM][0] = pp[NM][0] + 0.3 * (pt[MD3][0] - pp[NM][0]); pt[NM][1] = pp[NM][1] + 0.3 * (pt[MD3][1] - pp[NM][1]); } else { pt[NM][0] = pt[MD3][0]; pt[NM][1] = pt[MD3][1]; }
            if (vt != 1 && !seen) {
                HIDC[bi]++;
                /* regola del nucleo: cerchio al 95% ritagliato sul cuneo < meta' del cuneo */
                if (nuc) { double r95 = sqrt(C95 * kf.a); int ns = 0; for (int c = 0; c < NC; c++) if (ge[c] == 2) { double dx = ccx(c) - kf.x, dy = ccy(c) - kf.y; if (dx * dx + dy * dy <= r95 * r95) ns++; }
                    if (ns >= 0.5 * NSHE) nuc = 0; else { NUCC[bi]++; nucn++; } }
                if (havep) for (int m = 0; m <= NM; m++) { double sx = pt[m][0] - pp[m][0], sy = pt[m][1] - pp[m][1], st = hypot(sx, sy);
                    SM_N[bi][m]++; if (st > VMAX * DT + 1e-9) SM_BIG[bi][m]++; if (st > SM_MAX[bi][m]) SM_MAX[bi][m] = st;
                    if (st > 0.03 && sx * pd[m][0] + sy * pd[m][1] < 0) SM_BACK[bi][m]++; pd[m][0] = sx; pd[m][1] = sy; }
                else for (int m = 0; m <= NM; m++) pd[m][0] = pd[m][1] = 0;
            }
            for (int m = 0; m <= NM; m++) { pp[m][0] = pt[m][0]; pp[m][1] = pt[m][1]; } havep = 1;
            /* valutazione */
            int ti = -1; for (int t = 0; t < NT; t++) if (k - k0 == EVK[t]) ti = t;
            if (ti >= 0 && vt != 1 && !seen && NEV[bi][ti] < MAXN) {
                int e = NEV[bi][ti]++, tc = cidx(x, y); double m;
                for (int mth = 0; mth < NM; mth++) { ERR[bi][ti][mth][e] = hypot(pt[mth][0] - x, pt[mth][1] - y); int pc = cidx(pt[mth][0], pt[mth][1]); PTFREE[bi][ti][mth] += pc >= 0 && gt[pc] == 1; }
                /* a, b */
                double r50 = sqrt(C50 * kf.a), r90 = sqrt(C90 * kf.a), d = hypot(kf.x - x, kf.y - y);
                COV50[bi][ti][MA] += d <= r50; COV90[bi][ti][MA] += d <= r90; AR50[bi][ti][MA] += M_PI * r50 * r50 / ASH; AR90[bi][ti][MA] += M_PI * r90 * r90 / ASH;
                m = tc >= 0 ? gcellmass(kf.x, kf.y, kf.a, tc) : 0; NLL[bi][ti][MA] += -log(fmax(m, 1e-4));
                { int n50 = 0, n90 = 0, nf = 0, na = 0; double tot = 0, mt = 0; for (int c = 0; c < NC; c++) { double dx = ccx(c) - kf.x, dy = ccy(c) - kf.y, dd = dx * dx + dy * dy;
                        if (dd <= r90 * r90) { na++; nf += gt[c] == 1; }
                        if (ge[c] == 1) continue; if (dd <= r50 * r50) n50++; if (dd <= r90 * r90) n90++; if (dd < 36 * kf.a + 1) { double g = gcellmass(kf.x, kf.y, kf.a, c); tot += g; if (c == tc) mt = g; } }
                    COV50[bi][ti][MB] += d <= r50; COV90[bi][ti][MB] += d <= r90; AR50[bi][ti][MB] += n50 * CELL * CELL / ASH; AR90[bi][ti][MB] += n90 * CELL * CELL / ASH;
                    NLL[bi][ti][MB] += -log(fmax(tot > 0 ? mt / tot : 0, 1e-4)); FREE90[bi][ti][MA] += na ? (double)nf / na : 0; }
                /* c */
                imm_cells(&imm, 1); hpd(&a50, &a90); { int tout = tc < 0 || ge[tc] == 0; COV50[bi][ti][MC] += tout || in50[tc]; COV90[bi][ti][MC] += tout || in90[tc]; } AR50[bi][ti][MC] += a50 / ASH; AR90[bi][ti][MC] += a90 / ASH;
                NLL[bi][ti][MC] += -log(fmax((tc < 0 || ge[tc] == 0) ? POUT : cm[tc], 1e-4));
                /* d */
                for (int q = 0; q < NPF; q++) { pf_cells(&pf[q]); hpd(&a50, &a90); int mth = MD0 + q; int tout = tc < 0 || ge[tc] == 0; COV50[bi][ti][mth] += tout || in50[tc]; COV90[bi][ti][mth] += tout || in90[tc];
                    AR50[bi][ti][mth] += a50 / ASH; AR90[bi][ti][mth] += a90 / ASH; NLL[bi][ti][mth] += -log(fmax(tout ? POUT : cm[tc], 1e-4));
                    int nf = 0, na = 0; for (int c = 0; c < NC; c++) if (in90[c]) { na++; nf += gt[c] == 1; } FREE90[bi][ti][mth] += na ? (double)nf / na : 0; }
                MOUT[bi][ti] += pf_massvis(&pf[3], w, 0); TOUT[bi][ti] += vt == 0;
                { pf_cells(&pf[3]); SC[bi][ti][e] = score(tc); int tout = tc < 0 || ge[tc] == 0;
                  for (int v = 0; v < 2; v++) { int mth = v ? MD3W : MD3M; HL50 = LV[2 * v][ti]; HL90 = LV[2 * v + 1][ti]; hpd(&a50, &a90);
                    COV50[bi][ti][mth] += tout || in50[tc]; COV90[bi][ti][mth] += tout || in90[tc]; AR50[bi][ti][mth] += a50 / ASH; AR90[bi][ti][mth] += a90 / ASH; NLL[bi][ti][mth] += -log(fmax(tout ? POUT : cm[tc], 1e-4));
                    int nf = 0, na = 0; for (int c = 0; c < NC; c++) if (in90[c]) { na++; nf += gt[c] == 1; } FREE90[bi][ti][mth] += na ? (double)nf / na : 0; }
                  HL50 = 0.5; HL90 = 0.9; }
                /* e */
                { int nn = 0; for (int c = 0; c < NC; c++) if (ge[c] == 2) { double dx = ccx(c) - zlx, dy = ccy(c) - zly; if (dx * dx + dy * dy <= rad * rad) nn++; }
                    int in = hypot(x - zlx, y - zly) <= rad; COV50[bi][ti][ME] += in; COV90[bi][ti][ME] += in; AR50[bi][ti][ME] += nn * CELL * CELL / ASH; AR90[bi][ti][ME] += nn * CELL * CELL / ASH; NLL[bi][ti][ME] += -log(fmax(in && nn ? 1.0 / nn : 0, 1e-4)); }
                NLL[bi][ti][MF] += -log(1e-4);
            }
            if (k - k0 >= 110) break;
        }
        NUCDUR[bi] += nucn * DT;
    }
    /* ---------- stampa ---------- */
    printf("# cont: %s yp %.2f rmax %.1f dw %+.2f guard %.2f seme %ld np %d; ombra %.2f m2; q %.2f Pd %.1f; d3: LT %.2f LS %.2f LR %.2f PU %.2f\n", argv[1], YP, RMAXS, dw, guard, seed, NP, ASH, Q, PD, LT, LS, LR, PU);
    static float pool[NB * MAXN];
    for (int b = 0; b <= NB; b++) {
        printf("\n== %s ==\n tau    n | metodo        err_med err_p90 | cop50  cop90 | area50 area90 (x ombra) | punteggio | punto su libero%% | reg90 su libere%%\n", BN[b]);
        for (int t = 0; t < NT; t++) {
            int nn = 0; if (b < NB) nn = NEV[b][t]; else for (int q = 0; q < NB; q++) nn += NEV[q][t];
            if (!nn) continue;
            for (int m = 0; m < NM; m++) {
                double c50 = 0, c90 = 0, a50 = 0, a90 = 0, nl = 0, pf_ = 0, fr = 0; int np = 0;
                for (int q = (b < NB ? b : 0); q < (b < NB ? b + 1 : NB); q++) { c50 += COV50[q][t][m]; c90 += COV90[q][t][m]; a50 += AR50[q][t][m]; a90 += AR90[q][t][m]; nl += NLL[q][t][m]; pf_ += PTFREE[q][t][m]; fr += FREE90[q][t][m];
                    memcpy(pool + np, ERR[q][t][m], NEV[q][t] * sizeof(float)); np += NEV[q][t]; }
                printf(" %.1f %4d | %s  %6.2f  %6.2f | %5.3f  %5.3f | %6.2f %6.2f          | %6.2f    | %5.1f | %5.1f\n", EVT[t], nn, MN[m], pct(pool, np, 0.5), pct(pool, np, 0.9), c50 / nn, c90 / nn, a50 / nn, a90 / nn, nl / nn, 100 * pf_ / nn, 100 * fr / nn);
            }
            if (b < NB) printf("          d3: massa fuori campo/portata %.2f; vero fuori campo/portata %.2f\n", MOUT[b][t] / nn, TOUT[b][t] / nn);
        }
    }
    printf("\n== punteggio conforme di d3 (livello al quale la cella del vero entra nella regione): quantile 50%% / 90%% (n) ==\n");
    for (int b = 0; b <= NB; b++) { printf("%-10s", BN[b]); for (int t = 0; t < NT; t++) { int np = 0; for (int q = (b < NB ? b : 0); q < (b < NB ? b + 1 : NB); q++) { memcpy(pool + np, SC[q][t], NEV[q][t] * sizeof(float)); np += NEV[q][t]; }
            if (np) { static float tt[NB * MAXN]; memcpy(tt, pool, np * sizeof(float)); qsort(tt, np, sizeof(float), cmpf); int i5 = (int)ceil(0.5 * (np + 1)) - 1, i9 = (int)ceil(0.9 * (np + 1)) - 1; if (i9 >= np) i9 = np - 1; if (i5 >= np) i5 = np - 1;
                printf(" | %.1fs %.3f/%.3f (%d)", EVT[t], tt[i5], tt[i9], np); } else printf(" | %.1fs n/d", EVT[t]); } printf("\n"); }
    printf("livelli usati: L50 L90 W50 W90 ="); for (int v = 0; v < 4; v++) { printf(" ["); for (int t = 0; t < NT; t++) printf("%.3f ", LV[v][t]); printf("]"); } printf(" eps %.2f\n", EPS);
    printf("\n== continuita', regolarita', ricomparsa (per comportamento) ==\n");
    for (int b = 0; b < NB; b++) {
        if (!NTR[b]) continue;
        printf("%s: cicli nascosti %ld; il NUCLEO (meta' dell'ombra) emette una stima nel %.1f%% dei cicli (durata media %.2f s su %.2f s nascosti)\n", BN[b], HIDC[b], 100.0 * NUCC[b] / fmax(HIDC[b], 1), NUCDUR[b] / NTR[b], HIDC[b] * DT / NTR[b]);
        printf("   regolarita' (passo>v_max*dt %% ; passo all'indietro>3cm %% ; passo max m):");
        for (int m = 0; m <= NM; m++) { if (m == ME || m == MF || m == MD0 || m == MD3W) continue; printf(" [%s %.2f ; %.2f ; %.2f]", m < NM ? MN[m] : "d3 media lisciata", 100.0 * SM_BIG[b][m] / fmax(SM_N[b][m], 1), 100.0 * SM_BACK[b][m] / fmax(SM_N[b][m], 1), SM_MAX[b][m]); }
        printf("\n   ricomparsa n=%d, tau medio %.2f s: salto mediano/p90 m ; prima misura in reg90 %% ; entro 0,3 m da reg90 %% ; identita' %%:", NRE[b], RETAU[b] / fmax(NRE[b], 1));
        for (int m = 0; m < NM; m++) { if (m == MF || m == ME || m == MD0 || m == MB) continue; printf(" [%s %.2f/%.2f ; %.1f ; %.1f ; %.1f]", MN[m], pct(JUMP[b][m], NRE[b], 0.5), pct(JUMP[b][m], NRE[b], 0.9), 100 * RE90[b][m] / fmax(NRE[b], 1), 100 * RENEAR[b][m] / fmax(NRE[b], 1), 100 * REID[b][m] / fmax(NRE[b], 1)); }
        printf("\n");
    }
    printf("\ncosto d3 (%d particelle; moto+evidenza negativa+ricampionamento+punto+regione): %.1f microsecondi per ciclo e per traccia (%ld cicli)\n", NP, TNS / fmax(TCY, 1) / 1000, TCY);
    return 0;
}
