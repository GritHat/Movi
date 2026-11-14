/* sciame-avversario, f8 (continuita visiva), torneo dei falsificatori.
 * Simulatore MIO (scena, generatore, sensore, ciclo di vita, predittori riscritti dal testo delle candidate).
 * Compila:  gcc -O2 -o torneo torneo.c -lm
 * Uso:      timeout 120 ./torneo -scene T -beh 0,1,2,3,4,5,6 -n 200 -seed 9000 -tab tab_D.txt,tab_T.txt [opzioni]
 * Candidate: 0 C-004 fronte+scia | 1 C-001 particelle con sosta | 2 C-005W raggio da tabella, comportamento peggiore
 *            3 C-005P raggio da tabella tarata solo su «prosegue» | 4 C-EST lettura A | 5 C-EST lettura B
 * Limiti esterni: REACH = disco raggiungibile (v_max) ∩ non visto libero oltre la fascia 0,20; S1 = cuneo + 0,40 (strato 1).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <stdint.h>

#define DT (1.0/15.0)
#define CELL 0.10
#define C2 0.25
#define MAXC 16000
#define MAXC2 4000
#define FOVH (43.5*M_PI/180.0)
#define NCAND 6
#define NB 15
#define NTAU 8
#define NPT 5
#define MAXK 700
#define NMAXT 400
#define QKF 0.2
#define SIGM 0.05
#define VMAX 2.5
#define PDM 0.9
static const int TAUK[NTAU] = {8, 15, 30, 45, 75, 150, 300, 450};
static const char *BN[NB] = {"prosegue", "rallenta", "sosta", "torna", "svolta", "lontano", "sostalunga", "sosta30", "fermasubito",
                             "tripla", "tornatardi", "versosens", "accelera", "sostameta", "riserva"};
static const char *CN[NCAND] = {"C004", "C001", "C005W", "C005P", "ESTA", "ESTB"};

typedef struct { uint64_t s; } Rng;
static inline uint64_t rnext(Rng *r) { uint64_t z = (r->s += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static inline double runi(Rng *r) { return (rnext(r) >> 11) * (1.0 / 9007199254740992.0); }
static double rgau(Rng *r) { double u1 = runi(r), u2 = runi(r); if (u1 < 1e-300) u1 = 1e-300; return sqrt(-2 * log(u1)) * cos(2 * M_PI * u2); }
static double ru(Rng *r, double a, double b) { return a + (b - a) * runi(r); }

/* ---------- scena ---------- */
static double YP = 2.0, YS = 4.0, W = 1.0, RMAX = 6.0, GX0, DW = 0.0, PD = 0.9, BODY = 0.0, C6 = 0.22, VLO = 0.3, VHI = 1.8, VP = 0.0;
static int NX, NY, NC, NX2, NY2, CAP = 78, FOLLOW = 0, FREEZE = 0, MISS = 0, STRANGER = 0, CALMODE = 0;
static double DROP = -1;
typedef struct { uint8_t st[MAXC], fg[MAXC], s1[MAXC], call[MAXC2]; int ash; double px; } Masks;
static Masks MC, MF;   /* correnti, congelate all'ingresso */
static inline int cidx(double x, double y) { int i = (int)floor((x - GX0) / CELL), j = (int)floor(y / CELL); if (i < 0 || i >= NX || j < 0 || j >= NY) return -1; return j * NX + i; }
static int vis_pt(double x, double y, double px, double w) {   /* 1 visibile, 0 in ombra, -1 fuori campo o portata */
    if (y <= 0.0 || hypot(x, y) > RMAX || fabs(atan2(x, y)) > FOVH) return -1;
    if (y > YP) { double xs = x * YP / y; if (xs >= px - w / 2 && xs <= px + w / 2) return 0; }
    return 1;
}
static void compute_masks(Masks *m, double px, double w) {
    m->px = px; m->ash = 0;
    for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
        double x = GX0 + (i + .5) * CELL, y = (j + .5) * CELL; int v = vis_pt(x, y, px, w), c = j * NX + i;
        uint8_t s = v < 0 ? 0 : (v == 0 ? 1 : 2);
        if (fabs(y - YP) <= CELL * 0.5 && x >= px - w / 2 && x <= px + w / 2) s = 3;
        m->st[c] = s; if (s == 1) m->ash++;
    }
    memset(m->s1, 0, NC);
    for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) {
        int c = j * NX + i; uint8_t f = (m->st[c] == 2);
        if (f) for (int dj = -2; dj <= 2 && f; dj++) for (int di = -2; di <= 2; di++) {
            if (di * di + dj * dj > 4) continue; int a = i + di, b = j + dj;
            if (a < 0 || a >= NX || b < 0 || b >= NY || m->st[b * NX + a] != 2) { f = 0; break; }
        }
        m->fg[c] = f;
        if (m->st[c] == 1) for (int dj = -4; dj <= 4; dj++) for (int di = -4; di <= 4; di++) {
            if (di * di + dj * dj > 16) continue; int a = i + di, b = j + dj;
            if (a >= 0 && a < NX && b >= 0 && b < NY) m->s1[b * NX + a] = 1;
        }
    }
    memset(m->call, 0, NX2 * NY2);
    for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) if (!m->fg[j * NX + i]) {
        int ci = (int)(((i + .5) * CELL) / C2), cj = (int)(((j + .5) * CELL) / C2); if (ci < NX2 && cj < NY2) m->call[cj * NX2 + ci] = 1;
    }
}

/* ---------- regioni ---------- */
typedef struct { uint8_t m[MAXC]; int list[MAXC]; int n, n50, nsh, nsh50; int has; double px, py; int haspt; } Reg;
static Reg RG[NCAND];
static void reg_clear(Reg *r) { for (int i = 0; i < r->n; i++) r->m[r->list[i]] = 0; r->n = 0; r->n50 = 0; r->nsh = 0; r->nsh50 = 0; r->has = 0; r->haspt = 0; }
static inline void reg_add(Reg *r, int c, int bits) { if (!r->m[c]) r->list[r->n++] = c; if ((bits & 2) && !(r->m[c] & 2)) r->n50++; r->m[c] |= bits; }
static void mark_coarse(Reg *r, int cc, int bits, const Masks *m) {
    int ci = cc % NX2, cj = cc / NX2;
    int i0 = (int)ceil(ci * C2 / CELL - 0.5 - 1e-9), i1 = (int)ceil((ci + 1) * C2 / CELL - 0.5 - 1e-9) - 1;
    int j0 = (int)ceil(cj * C2 / CELL - 0.5 - 1e-9), j1 = (int)ceil((cj + 1) * C2 / CELL - 0.5 - 1e-9) - 1;
    for (int j = j0; j <= j1; j++) for (int i = i0; i <= i1; i++) { if (i < 0 || i >= NX || j < 0 || j >= NY) continue; int c = j * NX + i; if (!m->fg[c]) reg_add(r, c, bits); }
}
static double cden[MAXC2]; static int ctouch[MAXC2], nct;
static int SMOOTH1 = 0, FIXENTRY = 0; static double MIXW[7] = {.60, .10, .10, .10, .05, .05, 0};
static inline void splat(double x, double y, double w, const Masks *m, int sm) {
    int ci = (int)floor((x - GX0) / C2), cj = (int)floor(y / C2); if (ci < 0 || ci >= NX2 || cj < 0 || cj >= NY2) return;
    int c = cj * NX2 + ci; if (cden[c] == 0) ctouch[nct++] = c; if (!sm) { cden[c] += w; return; } cden[c] += 0.5 * w;
    static const int D[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
    for (int k = 0; k < 4; k++) { int a = ci + D[k][0], b = cj + D[k][1]; if (a < 0 || a >= NX2 || b < 0 || b >= NY2) continue; int c2 = b * NX2 + a; if (!m->call[c2]) continue; if (cden[c2] == 0) ctouch[nct++] = c2; cden[c2] += 0.125 * w; }
}
static int cmp_den(const void *a, const void *b) { double x = cden[*(const int *)a], y = cden[*(const int *)b]; return x < y ? 1 : (x > y ? -1 : 0); }
static void hpd_coarse(Reg *r, const Masks *m) {   /* massima densita al 50 e al 90 % sulle celle grosse toccate; poi azzera */
    double tot = 0; for (int i = 0; i < nct; i++) tot += cden[ctouch[i]];
    if (tot > 0) { qsort(ctouch, nct, sizeof(int), cmp_den); double cum = 0;
        for (int i = 0; i < nct; i++) { int c = ctouch[i]; if (cum < 0.9 * tot) mark_coarse(r, c, cum < 0.5 * tot ? 3 : 1, m); cum += cden[c]; } r->has = 1; }
    for (int i = 0; i < nct; i++) cden[ctouch[i]] = 0; nct = 0;
}

/* ---------- filtro ---------- */
typedef struct { double x, y, vx, vy, a, b, c; } KF;
static void kf_predict(KF *k) { k->x += k->vx * DT; k->y += k->vy * DT; double a = k->a + 2 * k->b * DT + k->c * DT * DT + QKF * DT * DT * DT / 3, b = k->b + k->c * DT + QKF * DT * DT / 2, c = k->c + QKF * DT; k->a = a; k->b = b; k->c = c; }
static void kf_update(KF *k, double zx, double zy) { double R = SIGM * SIGM, s = k->a + R, k1 = k->a / s, k2 = k->b / s; double rx = zx - k->x, ry = zy - k->y;
    k->x += k1 * rx; k->vx += k2 * rx; k->y += k1 * ry; k->vy += k2 * ry; double a = (1 - k1) * k->a, b = (1 - k1) * k->b, c = k->c - k2 * k->b; k->a = a; k->b = b; k->c = c; }

/* ---------- generatore delle traiettorie (mio) ---------- */
static double TX[MAXK], TY[MAXK]; static int KMID, KMAN; static double VNOM, SEXIT;
static void walk_noise(Rng *r, double *ux, double *uy) { *ux = *ux * (1 - 0.5 * DT) + 0.12 * sqrt(DT) * rgau(r); *uy = *uy * (1 - 0.5 * DT) + 0.12 * sqrt(DT) * rgau(r); }
static void gen_truth(int beh, Rng *r) {
    double v = ru(r, VLO, VHI), th = ru(r, -15, 15) * M_PI / 180, c = cos(th), s = sin(th); VNOM = v;
    double xe = -(W / 2) * YS / YP, sexit = (W * YS / YP) / (c - (W / 2) * s / YP); SEXIT = sexit;
    double tv = 2.0, x0, y0;
    for (;;) { x0 = xe - v * tv * c; y0 = YS - v * tv * s; if (tv <= 0.27 || (hypot(x0, y0) < RMAX - 0.10 && fabs(atan2(x0, y0)) < FOVH - 0.03)) break; tv -= 0.05; }
    double sm = ru(r, 0.05, 0.95) * sexit;
    if (beh == 8) sm = ru(r, 0.03, 0.25) / c; if (beh == 10) sm = ru(r, 0.85, 0.98) * sexit; if (beh == 13) sm = 0.5 * sexit;
    double fslow = ru(r, 0.3, 0.6), ramp = (runi(r) < 0.3) ? 0.2 : ru(r, 0.2, 0.6), hold = ru(r, 2, 4), wait = ru(r, 0.3, 1.0), ang = (runi(r) < 0.5 ? -1 : 1) * ru(r, 45, 90) * M_PI / 180, facc = ru(r, 1.5, 2.0);
    if (beh == 6) hold = ru(r, 6, 10); if (beh == 7) hold = 30; if (beh == 8) { hold = 6; ramp = 0.1; } if (beh == 13) { hold = 6; ramp = 2 * DT; }
    double x = x0, y = y0, dx = c, dy = s, f = 1.0, ux = 0, uy = 0, arc = -v * tv, tm = -1; int ph = 0; KMID = -1; KMAN = -1;
    for (int k = 0; k < MAXK; k++) {
        TX[k] = x; TY[k] = y; if (KMID < 0 && arc >= 0.5 * sexit) KMID = k;
        if (ph == 0 && arc >= sm && beh != 0) { ph = 1; tm = 0; KMAN = k;
            if (beh == 4) { double c2 = cos(ang), s2 = sin(ang), nx = c2 * dx - s2 * dy, ny = s2 * dx + c2 * dy; dx = nx; dy = ny; }
            if (beh == 5) { double h = hypot(x, y); dx = x / h; dy = y / h; }
            if (beh == 11) { double h = hypot(x, y); dx = -x / h; dy = -y / h; } }
        if (ph >= 1) { tm += DT;
            switch (beh) {
            case 1: f = 1 + (fslow - 1) * fmin(1.0, tm / 0.5); break;
            case 2: case 6: case 7: case 8: case 13:
                if (tm <= ramp) f = 1 - tm / ramp; else if (tm <= ramp + hold) f = 0; else f = fmin(1.0, (tm - ramp - hold) / 0.5); break;
            case 3: case 10:
                if (tm <= 0.3) f = 1 - tm / 0.3; else if (tm <= 0.3 + wait) f = 0; else { if (ph == 1) { dx = -dx; dy = -dy; ph = 2; } f = fmin(1.0, (tm - 0.3 - wait) / 0.4); } break;
            case 9: f = 1 + 2 * fmin(1.0, tm / 0.3); break;
            case 11: if (y < YP + 0.35) f = 0; break;
            case 12: f = 1 + (facc - 1) * fmin(1.0, tm / 0.3); break;
            default: break; } }
        walk_noise(r, &ux, &uy); double g = f < 1 ? f : 1.0;
        double vx = v * f * dx + g * ux, vy = v * f * dy + g * uy; x += vx * DT; y += vy * DT; arc += v * f * DT * (ph == 2 ? -1 : 1);
    }
    if (KMID < 0) KMID = MAXK - 1;
}

/* ---------- libreria di percorsi per C-004 ---------- */
#define NLIB 200
static float LDX[NLIB][MAXK], LDY[NLIB][MAXK];
static void make_lib(void) {
    Rng r = {777001};
    for (int l = 0; l < NLIB; l++) { double v = ru(&r, 0.5, 1.6), x = 0, y = 0, ux = 0, uy = 0;
        for (int k = 0; k < MAXK; k++) { LDX[l][k] = (float)(x / v); LDY[l][k] = (float)(y / v); walk_noise(&r, &ux, &uy); x += (v + ux) * DT; y += uy * DT; } }
}

/* ---------- C-004: fronte + scia ---------- */
#define NM 400
typedef struct { double w[NM], x0[NM], y0[NM], a[NM], b[NM]; int li[NM], tf[NM]; int j; double gx, gy; } Cono;
static Cono CO;
static inline void cono_pos(const Cono *s, int i, int j, double *x, double *y) { int jj = (s->tf[i] >= 0 && j > s->tf[i]) ? s->tf[i] : j; if (jj >= MAXK) jj = MAXK - 1;
    double p = LDX[s->li[i]][jj], q = LDY[s->li[i]][jj]; *x = s->x0[i] + s->a[i] * p - s->b[i] * q; *y = s->y0[i] + s->b[i] * p + s->a[i] * q; }
static void cono_init(Cono *s, const KF *kf, Rng *r, const Masks *m) {
    double sa = sqrt(kf->a), sc = sqrt(kf->c); int perm[NM / 2]; for (int i = 0; i < NM / 2; i++) perm[i] = i;
    for (int i = NM / 2 - 1; i > 0; i--) { int j = (int)(runi(r) * (i + 1)); int t = perm[i]; perm[i] = perm[j]; perm[j] = t; }
    for (int i = 0; i < NM; i++) { s->w[i] = 1; s->li[i] = i % NLIB; s->x0[i] = kf->x + sa * rgau(r); s->y0[i] = kf->y + sa * rgau(r);
        s->a[i] = kf->vx + sc * rgau(r); s->b[i] = kf->vy + sc * rgau(r); s->tf[i] = -1;
        if (i >= NM / 2) { int J = 90; for (int j = 1; j <= 90; j++) { double x, y; cono_pos(s, i, j, &x, &y); int c = cidx(x, y); if (c >= 0 && m->fg[c]) { J = j; break; } }
            s->tf[i] = (int)(((perm[i - NM / 2] + .5) / (NM / 2)) * J); } }
    s->j = 0; s->gx = kf->x; s->gy = kf->y;
}
static double sortv[NM]; static int cmp_idx(const void *a, const void *b) { double x = sortv[*(const int *)a], y = sortv[*(const int *)b]; return x < y ? -1 : (x > y ? 1 : 0); }
static void cono_step(Cono *s, Reg *r, const Masks *m) {
    static double mx[NM], my[NM], mw[NM]; int j = s->j++; double Stot = 0;
    for (int sc = 0; sc < 2; sc++) { double pw = (sc == 0 ? 0.60 : 0.25) / (NM / 2);
        for (int i = sc * NM / 2; i < (sc + 1) * NM / 2; i++) { mw[i] = 0; if (s->w[i] < 1e-4) continue; double x, y; cono_pos(s, i, j, &x, &y); int c = cidx(x, y);
            if (c >= 0 && m->fg[c]) { s->w[i] *= (1 - PDM); if (s->w[i] < 1e-4) continue; }
            mx[i] = x; my[i] = y; mw[i] = s->w[i] * pw; Stot += mw[i]; splat(x, y, s->w[i], m, 1); }
        hpd_coarse(r, m); }
    r->has = 1;   /* per costruzione emette sempre: se tutti i membri sono estinti la regione e vuota (contata come area 0) */
    double tx = s->gx, ty = s->gy;
    if (Stot >= 0.02) { int id[NM], n = 0; double med[2];
        for (int ax = 0; ax < 2; ax++) { n = 0; for (int i = 0; i < NM; i++) if (mw[i] > 0) { id[n++] = i; sortv[i] = ax ? my[i] : mx[i]; }
            qsort(id, n, sizeof(int), cmp_idx); double acc = 0; med[ax] = sortv[id[n - 1]]; for (int q = 0; q < n; q++) { acc += mw[id[q]]; if (acc >= Stot / 2) { med[ax] = sortv[id[q]]; break; } } }
        double best = 1e18; for (int i = 0; i < NM; i++) if (mw[i] > 1e-9) { double d = (mx[i] - med[0]) * (mx[i] - med[0]) + (my[i] - med[1]) * (my[i] - med[1]); if (d < best) { best = d; tx = mx[i]; ty = my[i]; } } }
    double ex = 0.5 * (tx - s->gx), ey = 0.5 * (ty - s->gy), e = hypot(ex, ey), mxs = VMAX * DT; if (e > mxs) { ex *= mxs / e; ey *= mxs / e; }
    s->gx += ex; s->gy += ey; r->px = s->gx; r->py = s->gy; r->haspt = 1;
}

/* ---------- C-001: particelle con modo «sosta» ---------- */
#define NP 2000
typedef struct { double x[NP], y[NP], vx[NP], vy[NP], w[NP]; uint8_t md[NP]; int j; } Part;
static Part PA;
static void part_init(Part *p, const KF *kf, Rng *r) { double sa = sqrt(kf->a), g = kf->b / kf->a, sr = sqrt(fmax(1e-9, kf->c - kf->b * kf->b / kf->a));
    for (int i = 0; i < NP; i++) { double ex = sa * rgau(r), ey = sa * rgau(r); p->x[i] = kf->x + ex; p->y[i] = kf->y + ey; p->vx[i] = kf->vx + g * ex + sr * rgau(r); p->vy[i] = kf->vy + g * ey + sr * rgau(r); p->w[i] = 1.0 / NP; p->md[i] = 0; } p->j = 0; }
static void part_step(Part *p, Reg *r, const Masks *m, Rng *g) {
    static double nx[NP], ny[NP], nvx[NP], nvy[NP]; static uint8_t nmd[NP];
    double ps = 1 - exp(-0.25 * DT), pr = 1 - exp(-0.4 * DT), sq = sqrt(QKF * DT), W1 = 0, W2 = 0, sx = 0, sy = 0;
    int first = (p->j++ == 0);
    for (int i = 0; i < NP; i++) {
        if (!first) { if (p->md[i] == 0) { if (runi(g) < ps) p->md[i] = 1; } else if (runi(g) < pr) p->md[i] = 0;
            if (p->md[i] == 0) { p->vx[i] += sq * rgau(g); p->vy[i] += sq * rgau(g); p->x[i] += p->vx[i] * DT; p->y[i] += p->vy[i] * DT; } }
        int c = cidx(p->x[i], p->y[i]); if (c >= 0 && m->fg[c]) p->w[i] *= (1 - PDM);
        W1 += p->w[i]; }
    if (W1 <= 0) { r->has = 0; return; }
    for (int i = 0; i < NP; i++) { p->w[i] /= W1; W2 += p->w[i] * p->w[i]; sx += p->w[i] * p->x[i]; sy += p->w[i] * p->y[i]; splat(p->x[i], p->y[i], p->w[i], m, SMOOTH1); }
    hpd_coarse(r, m); r->px = sx; r->py = sy; r->haspt = 1;
    if (1.0 / W2 < NP / 2) { double u = runi(g) / NP, cum = p->w[0]; int k = 0;
        for (int i = 0; i < NP; i++) { double t = u + (double)i / NP; while (cum < t && k < NP - 1) cum += p->w[++k]; nx[i] = p->x[k]; ny[i] = p->y[k]; nvx[i] = p->vx[k]; nvy[i] = p->vy[k]; nmd[i] = p->md[k]; }
        memcpy(p->x, nx, sizeof nx); memcpy(p->y, ny, sizeof ny); memcpy(p->vx, nvx, sizeof nvx); memcpy(p->vy, nvy, sizeof nvy); memcpy(p->md, nmd, sizeof nmd); for (int i = 0; i < NP; i++) p->w[i] = 1.0 / NP; }
}

/* ---------- C-005: disco da tabella ---------- */
static double TABW[MAXK], TABP[MAXK], TAB50[MAXK]; static int HAVETAB = 0;
static void disc_region(Reg *r, double cx, double cy, double r90, double r50, const Masks *m) {
    int i0 = (int)floor((cx - r90 - GX0) / CELL), i1 = (int)floor((cx + r90 - GX0) / CELL), j0 = (int)floor((cy - r90) / CELL), j1 = (int)floor((cy + r90) / CELL);
    if (i0 < 0) i0 = 0; if (j0 < 0) j0 = 0; if (i1 >= NX) i1 = NX - 1; if (j1 >= NY) j1 = NY - 1;
    for (int j = j0; j <= j1; j++) for (int i = i0; i <= i1; i++) { double x = GX0 + (i + .5) * CELL - cx, y = (j + .5) * CELL - cy, d2 = x * x + y * y; int c = j * NX + i;
        if (d2 <= (r90 + 0.07) * (r90 + 0.07) && !m->fg[c]) reg_add(r, c, d2 <= (r50 + 0.07) * (r50 + 0.07) ? 3 : 1); }
    r->has = 1; r->px = cx; r->py = cy; r->haspt = 1;
}

/* ---------- C-EST: due ipotesi, ritaglio, sigma_eff ---------- */
typedef struct { double mx[2], my[2], vx[2], vy[2], a[2], b[2], c[2], mu[2]; double alpha; int cumul, perso, j, jexit, dom; double sig, ex, ey, cxx, cyy, cxy, mu1; } Est;
static Est ES[2];
static void est_init(Est *e, const KF *kf, double alpha, int cumul) { for (int h = 0; h < 2; h++) { e->mx[h] = kf->x; e->my[h] = kf->y; e->vx[h] = kf->vx; e->vy[h] = kf->vy; e->a[h] = kf->a; e->b[h] = kf->b; e->c[h] = kf->c; }
    e->mu[0] = 0.8; e->mu[1] = 0.2; e->alpha = alpha; e->cumul = cumul; e->perso = 0; e->j = 0; e->jexit = -1; e->dom = 0; e->mu1 = 0.8; }
static double dbuf[MAXC]; static int dtouch[MAXC], ndt; static double GXA[2][400], GYA[2][400];
static void est_step(Est *e, Reg *r, const Masks *m) {
    int I0[2], I1[2], J0[2], J1[2]; double f[2];
    if (e->j++ > 0) for (int h = 0; h < 2; h++) { double al = h ? e->alpha : 1.0; e->mx[h] += e->vx[h] * DT; e->my[h] += e->vy[h] * DT; e->vx[h] *= al; e->vy[h] *= al;
        double a = e->a[h] + 2 * e->b[h] * DT + e->c[h] * DT * DT + QKF * DT * DT * DT / 3, b = al * (e->b[h] + e->c[h] * DT) + QKF * DT * DT / 2, c = al * al * e->c[h] + QKF * DT; e->a[h] = a; e->b[h] = b; e->c[h] = c; }
    for (int h = 0; h < 2; h++) { double s = sqrt(e->a[h]), is = 1.0 / (s * M_SQRT2);
        int i0 = (int)floor((e->mx[h] - 4 * s - GX0) / CELL), i1 = (int)floor((e->mx[h] + 4 * s - GX0) / CELL), j0 = (int)floor((e->my[h] - 4 * s) / CELL), j1 = (int)floor((e->my[h] + 4 * s) / CELL);
        if (i0 < 0) i0 = 0; if (j0 < 0) j0 = 0; if (i1 >= NX) i1 = NX - 1; if (j1 >= NY) j1 = NY - 1; I0[h] = i0; I1[h] = i1; J0[h] = j0; J1[h] = j1;
        for (int i = i0; i <= i1; i++) { double xa = GX0 + i * CELL - e->mx[h]; GXA[h][i] = 0.5 * (erf((xa + CELL) * is) - erf(xa * is)); }
        for (int j = j0; j <= j1; j++) { double ya = j * CELL - e->my[h]; GYA[h][j] = 0.5 * (erf((ya + CELL) * is) - erf(ya * is)); }
        double fm = 0; for (int j = j0; j <= j1; j++) { const uint8_t *fg = m->fg + j * NX; double acc = 0; for (int i = i0; i <= i1; i++) if (fg[i]) acc += GXA[h][i]; fm += acc * GYA[h][j]; }
        f[h] = 1 - fm; if (f[h] < 0) f[h] = 0; }
    double w0, w1; if (e->cumul) { w0 = e->mu[0] * f[0]; w1 = e->mu[1] * f[1]; } else { w0 = 0.8 * f[0]; w1 = 0.2 * f[1]; }
    double ws = w0 + w1; if (ws > 1e-300) { e->mu[0] = w0 / ws; e->mu[1] = w1 / ws; } e->mu1 = e->mu[0];
    { int c = cidx(e->mx[0], e->my[0]); if (e->jexit < 0 && e->j > 1 && (c < 0 || m->fg[c])) e->jexit = e->j; if (e->jexit >= 0 && e->j >= e->jexit + 8 && e->mu1 > 0.5 && e->dom == 0) e->dom = 1; }
    ndt = 0; double Z = 0, dmax = 0;
    for (int h = 0; h < 2; h++) { if (f[h] < 1e-9 || e->mu[h] < 1e-12) continue; double k = e->mu[h] / f[h];
        for (int j = J0[h]; j <= J1[h]; j++) { double gy = GYA[h][j] * k; if (gy < 1e-14) continue; for (int i = I0[h]; i <= I1[h]; i++) { int c = j * NX + i; if (m->fg[c]) continue; double d = GXA[h][i] * gy; if (d < 1e-13) continue; if (dbuf[c] == 0) dtouch[ndt++] = c; dbuf[c] += d; } } }
    double sx = 0, sy = 0, sxx = 0, syy = 0, sxy = 0;
    for (int q = 0; q < ndt; q++) { int c = dtouch[q]; double d = dbuf[c], x = GX0 + (c % NX + .5) * CELL, y = (c / NX + .5) * CELL; Z += d; sx += d * x; sy += d * y; sxx += d * x * x; syy += d * y * y; sxy += d * x * y; if (d > dmax) dmax = d; }
    if (Z <= 1e-12) { r->has = 0; e->sig = 99; for (int q = 0; q < ndt; q++) dbuf[dtouch[q]] = 0; return; }
    e->ex = sx / Z; e->ey = sy / Z; e->cxx = sxx / Z - e->ex * e->ex; e->cyy = syy / Z - e->ey * e->ey; e->cxy = sxy / Z - e->ex * e->ey; e->sig = sqrt(fmax(0, (e->cxx + e->cyy) / 2));
    if (e->sig > 0.8) e->perso = 1;
    static double bins[2049]; memset(bins, 0, sizeof bins);
    for (int q = 0; q < ndt; q++) { double d = dbuf[dtouch[q]]; bins[(int)(2048 * d / dmax)] += d; }
    double cum = 0, t90 = 0, t50 = -1; for (int b = 2048; b >= 0; b--) { cum += bins[b]; if (t50 < 0 && cum >= 0.5 * Z) t50 = b * dmax / 2048; if (cum >= 0.9 * Z) { t90 = b * dmax / 2048; break; } }
    if (!e->perso) { for (int q = 0; q < ndt; q++) { int c = dtouch[q]; if (dbuf[c] >= t90) reg_add(r, c, dbuf[c] >= t50 ? 3 : 1); } r->has = 1; }
    r->px = e->ex; r->py = e->ey; r->haspt = 0;
    for (int q = 0; q < ndt; q++) dbuf[dtouch[q]] = 0;
}

/* ---------- statistiche ---------- */
static struct {
    long n[NB][NTAU], in90[NB][NTAU][NCAND], in50[NB][NTAU][NCAND], noreg[NB][NTAU][NCAND], reach[NB][NTAU], s1[NB][NTAU], s1f[NB][NTAU];
    double area[NB][NTAU][NCAND], a50[NB][NTAU][NCAND];
    long hid[NB], cnoreg[NB][NCAND], cfg[NB][NCAND], cfree[NB][NCAND], ccw[NB][NCAND], cptfg[NB][NCAND], cempty[NB][NCAND];
    long pas[NB], pocc[NB], pnoreg[NB][NCAND], pfg[NB][NCAND], pcw[NB][NCAND], preach[NB], ps1[NB], ps1f[NB], creach[NB], cs1[NB], cs1f[NB];
    long vu[NB], vu90[NB][NCAND], vureach[NB], vus1[NB];
    long re[NB], re45[NB][NCAND], re30[NB][NCAND], rein[NB][NCAND], reell[NB][2], reellp[NB][2], reperso[NB][2], half[NB][NCAND], eighty[NB][NCAND], nucleo[NB];
    long nopend[NB], closed[NB], unconf[NB], chidnp[NB], fixed[NB];
    long mu1dom[NB][2], esperso[NB][NTAU][2]; double essig[NB][NTAU][2], esmu[NB][NTAU][2];
    long st_n, st_first, st_nuc, st_gate[NCAND], st_ell[2];
    int nvr[NB], nperr[NB][NTAU], njump[NB];
    double dark[NB];
} S;
static float VR[NB][NMAXT], PERR[NB][NTAU][NPT][NMAXT], JUMP[NB][NPT][NMAXT];
static float CALE[7][80][NMAXT]; static int CALN[7][80];
static double tns[NCAND]; static long tcn[NCAND]; static double tmax[NCAND];
static int cmpf(const void *a, const void *b) { float x = *(const float *)a, y = *(const float *)b; return x < y ? -1 : (x > y ? 1 : 0); }
static double quant(float *v, int n, double q) { if (n <= 0) return NAN; qsort(v, n, sizeof(float), cmpf); int i = (int)(q * n); if (i >= n) i = n - 1; return v[i]; }
static double nowns(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e9 + t.tv_nsec; }

static int sense(double x, double y, double px, Rng *r, double *zx, double *zy, int forced_miss) {
    double cxm = x;
    if (vis_pt(x, y, px, W) == -1) return 0;
    if (y > YP) { double sl = (px - W / 2) * y / YP, sr = (px + W / 2) * y / YP;
        if (BODY > 0) { double a = x - BODY / 2, b = x + BODY / 2, lL = fmax(0, fmin(b, sl) - a), lR = fmax(0, b - fmax(a, sr)), vl = lL + lR;
            if (vl < BODY - 1e-9) { if (C6 > 0) return 0; if (vl < 0.10) return 0; cxm = (lL * (a + lL / 2) + lR * (b - lR / 2)) / vl; } }
        else { if (x >= sl && x <= sr) return 0; double d = x < sl ? sl - x : x - sr; if (d < C6) return 0; } }
    if (forced_miss) return 0;
    if (runi(r) >= PD) return 0;
    *zx = cxm + SIGM * rgau(r); *zy = y + SIGM * rgau(r); return 1;
}
static double dist_reg(const Reg *r, double x, double y) { double best = 1e18; for (int i = 0; i < r->n; i++) { int c = r->list[i]; double dx = GX0 + (c % NX + .5) * CELL - x, dy = (c / NX + .5) * CELL - y, d = dx * dx + dy * dy; if (d < best) best = d; } return r->n ? sqrt(best) : 1e9; }

static void run_trial(int beh, uint64_t seed) {
    Rng rt = {seed * 1000003ULL + beh * 7919ULL}, rs = {(seed * 1000003ULL + beh * 7919ULL) ^ 0xABCDEF12345ULL}, rp = {(seed * 1000003ULL + beh * 7919ULL) ^ 0x1234567ULL};
    gen_truth(beh, &rt);
    double px = 0; compute_masks(&MC, 0, W + DW);
    KF kf; int trk = 0, ndet = 0, kp = 0, klast = -1, occl = 0, hidden_seen = 0, kinit = 0, missleft = 0, was_hidden = 0, everclosed = 0;
    double zpx = 0, zpy = 0, zlx = 0, zly = 0; KF kf0; int flag_noreg[NCAND] = {0}, flag_fg[NCAND] = {0}, flag_cw[NCAND] = {0}, flag_half[NCAND] = {0}, flag_80[NCAND] = {0}, f_reach = 0, f_s1 = 0, f_s1f = 0, f_nopend = 0, nuc_on = 1;
    /* estraneo */ double sx0 = 0, sy0 = 0, sdir = 1, sv = 1; int sk0 = -1, dropk = -1;
    S.pas[beh]++;
    for (int k = 0; k < MAXK; k++) {
        double x = TX[k], y = TY[k];
        if (cidx(x, y) < 0) break;
        if (VP != 0 || FOLLOW) { double npx = px;
            if (FOLLOW) { if (k >= KMID) npx = x * YP / y; } else if (KMAN >= 0 && k >= KMAN) npx = -VP * (k - KMAN) * DT;
            if (npx != px) { px = npx; compute_masks(&MC, px, W + DW); } }
        const Masks *mp = (FREEZE && occl) ? &MF : &MC;
        int v = vis_pt(x, y, px, W), hid = (v != 1);
        if (v == 1 && was_hidden && MISS > 0 && missleft == 0) missleft = MISS + 1;
        if (hid) was_hidden = 1;
        if (DROP >= 0 && dropk < 0 && v == 1 && !was_hidden && y > YP) { double sl = (px - W / 2) * y / YP; if (sl - x <= DROP) dropk = k; }
        int fm = (missleft > 1) || (dropk >= 0 && k - dropk < 5); if (missleft > 1) missleft--;
        double zx = 0, zy = 0; int det = sense(x, y, px, &rs, &zx, &zy, fm);
        if (det) {
            if (trk == 0) { zpx = zx; zpy = zy; kp = k; trk = 1; ndet = 1; }
            else if (trk == 1) { double dtk = (k - kp) * DT; kf.x = zx; kf.y = zy; kf.vx = (zx - zpx) / dtk; kf.vy = (zy - zpy) / dtk; kf.a = SIGM * SIGM; kf.b = kf.a / dtk; kf.c = 2 * kf.a / (dtk * dtk); trk = 2; ndet = 2; }
            else { kf_predict(&kf); if (occl && hidden_seen) {
                    /* ricomparsa */
                    S.re[beh]++; S.dark[beh] += (k - klast) * DT; int nj = S.njump[beh];
                    for (int c = 0; c < NCAND; c++) { double d = RG[c].has ? dist_reg(&RG[c], zx, zy) : 1e9; if (d <= 0.45) S.re45[beh][c]++; if (d <= 0.30) S.re30[beh][c]++; if (d <= 0.075) S.rein[beh][c]++; if (flag_half[c]) S.half[beh][c]++; if (flag_80[c]) S.eighty[beh][c]++; }
                    for (int e = 0; e < 2; e++) { Est *E = &ES[e]; double dx = zx - E->ex, dy = zy - E->ey, det2 = E->cxx * E->cyy - E->cxy * E->cxy; double m2 = det2 > 1e-12 ? (E->cyy * dx * dx - 2 * E->cxy * dx * dy + E->cxx * dy * dy) / det2 : 1e9; if (m2 <= 5.99) S.reell[beh][e]++; if (m2 <= 5.99 && !E->perso) S.reellp[beh][e]++; if (E->perso) S.reperso[beh][e]++; }
                    if (nj < NMAXT) { JUMP[beh][0][nj] = hypot(RG[0].px - zx, RG[0].py - zy); JUMP[beh][1][nj] = hypot(RG[1].px - zx, RG[1].py - zy); JUMP[beh][2][nj] = hypot(kf.x - zx, kf.y - zy); JUMP[beh][3][nj] = hypot(ES[0].ex - zx, ES[0].ey - zy); JUMP[beh][4][nj] = hypot(zlx - zx, zly - zy); S.njump[beh]++; }
                    if (nuc_on) S.nucleo[beh]++;
                    break; }
                kf_update(&kf, zx, zy); ndet++; occl = 0; }
            klast = k; zlx = zx; zly = zy;
        } else {
            if (trk == 1 && k - kp > 3) trk = 0;
            if (trk == 2) { kf_predict(&kf);
                if (!occl) { int c = cidx(zlx, zly);
                    if (c >= 0 && MC.s1[c]) { if (ndet >= 4) { occl = 1; hidden_seen = 0; kinit = k; kf0 = kf; S.pocc[beh]++; if (FREEZE) memcpy(&MF, &MC, sizeof(Masks)); mp = (FREEZE) ? &MF : &MC;
                            if (S.nvr[beh] < NMAXT) VR[beh][S.nvr[beh]++] = (float)(hypot(kf.vx, kf.vy) / VNOM);
                            if (!CALMODE) { cono_init(&CO, &kf, &rp, mp); part_init(&PA, &kf, &rp); est_init(&ES[0], &kf, 0.90, 1); est_init(&ES[1], &kf, 0.95, 0); }
                            if (STRANGER) { double sl = (-W / 2) * YS / YP, sr = (W / 2) * YS / YP; sx0 = ru(&rt, sl + 0.2 * (sr - sl), sr - 0.2 * (sr - sl)); sy0 = YS + ru(&rt, -0.3, 0.3); sdir = runi(&rt) < 0.5 ? -1 : 1; sv = ru(&rt, 0.8, 1.5); sk0 = k + (int)(ru(&rt, 0.3, 4.0) / DT); } }
                        else { trk = 0; ndet = 0; S.unconf[beh]++; } }
                    else if (k - klast > 3 || FIXENTRY == 2) { int pc = cidx(kf.x, kf.y); if (FIXENTRY && ndet >= 4 && pc >= 0 && (MC.s1[pc] || MC.st[pc] == 1)) { occl = 1; hidden_seen = 0; kinit = k; kf0 = kf; S.pocc[beh]++; S.fixed[beh]++; if (FREEZE) memcpy(&MF, &MC, sizeof(Masks)); mp = (FREEZE) ? &MF : &MC; if (!CALMODE) { cono_init(&CO, &kf, &rp, mp); part_init(&PA, &kf, &rp); est_init(&ES[0], &kf, 0.90, 1); est_init(&ES[1], &kf, 0.95, 0); } } else if (k - klast > 3) { trk = 0; ndet = 0; if (!everclosed) { S.closed[beh]++; everclosed = 1; } } } } }
        }
        if (hid && !occl) { S.chidnp[beh]++; if (!f_nopend) { f_nopend = 1; S.nopend[beh]++; } }
        if (occl && !det) {
            if (hid) hidden_seen = 1;
            int j = k - kinit, kk = k - klast; double tau_i = -1; int ti = -1; for (int q = 0; q < NTAU; q++) if (TAUK[q] == kk) ti = q; (void)tau_i;
            if (CALMODE) { double cx = kf0.x + kf0.vx * j * DT, cy = kf0.y + kf0.vy * j * DT; if (hid && beh < 7 && kk < 80 && CALN[beh][kk] < NMAXT) CALE[beh][kk][CALN[beh][kk]++] = (float)hypot(cx - x, cy - y); if (kk >= CAP) break; continue; }
            double t0;
            reg_clear(&RG[0]); t0 = nowns(); cono_step(&CO, &RG[0], mp); t0 = nowns() - t0; tns[0] += t0; tcn[0]++; if (t0 > tmax[0]) tmax[0] = t0;
            reg_clear(&RG[1]); t0 = nowns(); part_step(&PA, &RG[1], mp, &rp); t0 = nowns() - t0; tns[1] += t0; tcn[1]++; if (t0 > tmax[1]) tmax[1] = t0;
            { double cx = kf0.x + kf0.vx * j * DT, cy = kf0.y + kf0.vy * j * DT; int q = kk < MAXK ? kk : MAXK - 1;
              reg_clear(&RG[2]); t0 = nowns(); disc_region(&RG[2], cx, cy, TABW[q], TAB50[q], mp); t0 = nowns() - t0; tns[2] += t0; tcn[2]++; if (t0 > tmax[2]) tmax[2] = t0;
              reg_clear(&RG[3]); disc_region(&RG[3], cx, cy, TABP[q], 0.5 * TABP[q], mp); }
            for (int e = 0; e < 2; e++) { reg_clear(&RG[4 + e]); t0 = nowns(); est_step(&ES[e], &RG[4 + e], mp); t0 = nowns() - t0; tns[4 + e] += t0; tcn[4 + e]++; if (t0 > tmax[4 + e]) tmax[4 + e] = t0; }
            int tc = cidx(x, y); double ash = MC.ash > 0 ? MC.ash : 1;
            /* limiti esterni */
            double rr = VMAX * kk * DT + 0.30; int in_reach = (tc >= 0) && !mp->fg[tc] && hypot(x - zlx, y - zly) <= rr;
            int in_s1 = (tc >= 0) && (MC.st[tc] != 2 || MC.s1[tc]), in_s1f = FREEZE ? ((tc >= 0) && (MF.st[tc] == 0 || MF.s1[tc])) : in_s1;
            { /* regola del nucleo: cerchio al 95 % (2,45 sigma) ritagliato sull'ombra, mostrato finche < meta del cuneo */
              if (nuc_on) { double rad = 2.45 * sqrt(kf.a); int cnt = 0; int i0 = (int)floor((kf.x - rad - GX0) / CELL), i1 = (int)floor((kf.x + rad - GX0) / CELL), j0 = (int)floor((kf.y - rad) / CELL), j1 = (int)floor((kf.y + rad) / CELL);
                  if (i0 < 0) i0 = 0; if (j0 < 0) j0 = 0; if (i1 >= NX) i1 = NX - 1; if (j1 >= NY) j1 = NY - 1;
                  for (int jj = j0; jj <= j1; jj++) for (int ii = i0; ii <= i1; ii++) { double ddx = GX0 + (ii + .5) * CELL - kf.x, ddy = (jj + .5) * CELL - kf.y; if (ddx * ddx + ddy * ddy <= rad * rad && MC.st[jj * NX + ii] == 1) cnt++; }
                  if (cnt >= 0.5 * ash) nuc_on = 0; } }
            for (int c = 0; c < NCAND; c++) { Reg *r = &RG[c]; r->nsh = 0; r->nsh50 = 0; for (int q = 0; q < r->n; q++) if (MC.st[r->list[q]] == 1) { r->nsh++; if (r->m[r->list[q]] & 2) r->nsh50++; } if (r->nsh > 0.5 * ash) flag_half[c] = 1; if (r->nsh > 0.8 * ash) flag_80[c] = 1; }
            if (hid) {
                S.hid[beh]++;
                if (!in_reach) { S.creach[beh]++; if (!f_reach) { f_reach = 1; S.preach[beh]++; } }
                if (!in_s1) { S.cs1[beh]++; if (!f_s1) { f_s1 = 1; S.ps1[beh]++; } }
                if (!in_s1f) { S.cs1f[beh]++; if (!f_s1f) { f_s1f = 1; S.ps1f[beh]++; } }
                if (ti >= 0) { S.n[beh][ti]++; S.reach[beh][ti] += in_reach; S.s1[beh][ti] += in_s1; S.s1f[beh][ti] += in_s1f;
                    int np = S.nperr[beh][ti]; if (np < NMAXT) { PERR[beh][ti][0][np] = hypot(RG[0].px - x, RG[0].py - y); PERR[beh][ti][1][np] = RG[1].has ? hypot(RG[1].px - x, RG[1].py - y) : 9; PERR[beh][ti][2][np] = hypot(kf.x - x, kf.y - y); PERR[beh][ti][3][np] = hypot(ES[0].ex - x, ES[0].ey - y); PERR[beh][ti][4][np] = hypot(zlx - x, zly - y); S.nperr[beh][ti]++; }
                    for (int e = 0; e < 2; e++) { S.esperso[beh][ti][e] += ES[e].perso; S.essig[beh][ti][e] += ES[e].sig; S.esmu[beh][ti][e] += ES[e].mu1; } }
                for (int c = 0; c < NCAND; c++) { Reg *r = &RG[c]; int in9 = r->has && tc >= 0 && (r->m[tc] & 1), in5 = r->has && tc >= 0 && (r->m[tc] & 2);
                    if (ti >= 0) { S.in90[beh][ti][c] += in9; S.in50[beh][ti][c] += in5; S.noreg[beh][ti][c] += !r->has; S.area[beh][ti][c] += r->has ? r->nsh / ash : 0; S.a50[beh][ti][c] += r->has ? r->nsh50 / ash : 0; }
                    if (!r->has) { S.cnoreg[beh][c]++; if (!flag_noreg[c]) { flag_noreg[c] = 1; S.pnoreg[beh][c]++; } }
                    else { if (r->n == 0) S.cempty[beh][c]++;
                        int onfg = 0, onfree = 0; for (int q = 0; q < r->n; q++) { int cc = r->list[q]; if (MC.fg[cc]) onfg = 1; if (MC.st[cc] == 2) onfree = 1; }
                        if (onfg) { S.cfg[beh][c]++; if (!flag_fg[c]) { flag_fg[c] = 1; S.pfg[beh][c]++; } } if (onfree) S.cfree[beh][c]++;
                        if (!in9 && r->nsh <= 0.25 * ash && dist_reg(r, x, y) > 0.5) { S.ccw[beh][c]++; if (!flag_cw[c]) { flag_cw[c] = 1; S.pcw[beh][c]++; } }
                        if (r->haspt) { int pc = cidx(r->px, r->py); if (pc >= 0 && MC.fg[pc]) S.cptfg[beh][c]++; } } }
            } else if (v == 1) { double sl = (px - W / 2) * y / YP, sr = (px + W / 2) * y / YP, d = (y > YP) ? (x < sl ? sl - x : x - sr) : 1;
                if (d >= C6 || BODY > 0) { S.vu[beh]++; S.vureach[beh] += in_reach; S.vus1[beh] += in_s1; for (int c = 0; c < NCAND; c++) S.vu90[beh][c] += (RG[c].has && tc >= 0 && (RG[c].m[tc] & 1)); } }
            for (int e = 0; e < 2; e++) if (ES[e].dom == 1) { S.mu1dom[beh][e]++; ES[e].dom = 2; }
            /* estraneo che esce dalla stessa ombra */
            if (STRANGER && sk0 >= 0 && k >= sk0) { double sx = sx0 + sdir * sv * (k - sk0) * DT, szx, szy;
                if (sense(sx, sy0, px, &rs, &szx, &szy, 0)) { S.st_n++; int c = cidx(szx, szy); if (hid) { S.st_first++; if (c >= 0 && MC.s1[c]) S.st_nuc++;
                        for (int q = 0; q < NCAND; q++) if (RG[q].has && dist_reg(&RG[q], szx, szy) <= 0.45) S.st_gate[q]++;
                        for (int e = 0; e < 2; e++) { Est *E = &ES[e]; double dx = szx - E->ex, dy = szy - E->ey, det2 = E->cxx * E->cyy - E->cxy * E->cxy; if (!E->perso && det2 > 1e-12 && (E->cyy * dx * dx - 2 * E->cxy * dx * dy + E->cxx * dy * dy) / det2 <= 5.99) S.st_ell[e]++; } }
                    break; } }
            if (kk >= CAP) break;
        }
    }
}

static void load_tab(const char *list) {
    char buf[512]; strncpy(buf, list, 511); buf[511] = 0; for (int k = 0; k < MAXK; k++) { TABW[k] = 0; TAB50[k] = 0; TABP[k] = -1; }
    int nf = 0; for (char *tok = strtok(buf, ","); tok; tok = strtok(NULL, ","), nf++) { FILE *f = fopen(tok, "r"); if (!f) { fprintf(stderr, "manca %s\n", tok); exit(2); } char line[1024];
        while (fgets(line, sizeof line, f)) { if (line[0] == '#') continue; int k; double q[7], p50, p90; if (sscanf(line, "%d %lf %lf %lf %lf %lf %lf %lf %lf %lf", &k, &q[0], &q[1], &q[2], &q[3], &q[4], &q[5], &q[6], &p50, &p90) != 10) continue;
            if (nf < 2) { for (int b = 0; b < 7; b++) if (q[b] > TABW[k]) TABW[k] = q[b]; if (p50 > TAB50[k]) TAB50[k] = p50; } else TABP[k] = q[0]; }
        fclose(f); }
    for (int k = 1; k < MAXK; k++) { if (TABW[k] < TABW[k - 1]) TABW[k] = (k < 80) ? TABW[k - 1] : TABW[k - 1] + VMAX * DT; if (TAB50[k] < TAB50[k - 1]) TAB50[k] = (k < 80) ? TAB50[k - 1] : TAB50[k - 1] + VMAX * DT; }
    if (nf < 3) for (int k = 0; k < MAXK; k++) TABP[k] = TABW[k]; else { if (TABP[0] < 0) TABP[0] = 0.1; for (int k = 1; k < MAXK; k++) if (TABP[k] < TABP[k - 1]) TABP[k] = TABP[k - 1]; }
    HAVETAB = 1;
}

int main(int argc, char **argv) {
    int behs[NB], nb = 0, N = 200; long seed0 = 9000; const char *scene = "T", *tab = NULL, *calout = NULL; char behs_s[256] = "0,1,2,3,4,5,6";
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-scene")) scene = argv[++i]; else if (!strcmp(argv[i], "-beh")) strncpy(behs_s, argv[++i], 255); else if (!strcmp(argv[i], "-n")) N = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-seed")) seed0 = atol(argv[++i]); else if (!strcmp(argv[i], "-tab")) tab = argv[++i]; else if (!strcmp(argv[i], "-cal")) { calout = argv[++i]; CALMODE = 1; }
        else if (!strcmp(argv[i], "-dw")) DW = atof(argv[++i]); else if (!strcmp(argv[i], "-pd")) PD = atof(argv[++i]); else if (!strcmp(argv[i], "-body")) BODY = atof(argv[++i]);
        else if (!strcmp(argv[i], "-c6")) C6 = atof(argv[++i]); else if (!strcmp(argv[i], "-vlo")) VLO = atof(argv[++i]); else if (!strcmp(argv[i], "-vhi")) VHI = atof(argv[++i]);
        else if (!strcmp(argv[i], "-cap")) CAP = atoi(argv[++i]); else if (!strcmp(argv[i], "-vp")) VP = atof(argv[++i]); else if (!strcmp(argv[i], "-follow")) FOLLOW = 1;
        else if (!strcmp(argv[i], "-freeze")) FREEZE = 1; else if (!strcmp(argv[i], "-miss")) MISS = atoi(argv[++i]); else if (!strcmp(argv[i], "-stranger")) STRANGER = 1; else if (!strcmp(argv[i], "-drop")) DROP = atof(argv[++i]); else if (!strcmp(argv[i], "-smooth1")) SMOOTH1 = 1; else if (!strcmp(argv[i], "-fixentry")) FIXENTRY = 1; else if (!strcmp(argv[i], "-fixentry2")) FIXENTRY = 2;
        else if (!strcmp(argv[i], "-mix")) { char mb[256]; strncpy(mb, argv[++i], 255); mb[255] = 0; int q = 0; for (char *t2 = strtok(mb, ","); t2 && q < 7; t2 = strtok(NULL, ",")) MIXW[q++] = atof(t2); for (; q < 7; q++) MIXW[q] = 0; }
        else { fprintf(stderr, "opzione ignota %s\n", argv[i]); return 2; } }
    if (!strcmp(scene, "D")) { YP = 1.9; YS = 2.3; W = 1.0; RMAX = 3.0; } else if (!strcmp(scene, "T")) { YP = 2.0; YS = 4.0; W = 1.0; RMAX = 6.0; } else if (!strcmp(scene, "L")) { YP = 2.0; YS = 4.0; W = 2.0; RMAX = 6.0; } else { fprintf(stderr, "scena?\n"); return 2; }
    GX0 = -(RMAX + 1.5); NX = (int)ceil(2 * (RMAX + 1.5) / CELL); NY = (int)ceil((RMAX + 2.0) / CELL); NC = NX * NY; NX2 = (int)ceil(NX * CELL / C2); NY2 = (int)ceil(NY * CELL / C2);
    if (NC > MAXC || NX2 * NY2 > MAXC2 || NX > 400 || NY > 400) { fprintf(stderr, "griglia troppo grande\n"); return 2; }
    for (char *tok = strtok(behs_s, ","); tok; tok = strtok(NULL, ",")) behs[nb++] = atoi(tok);
    if (N > NMAXT) N = NMAXT;
    make_lib(); if (tab) load_tab(tab); else if (!CALMODE) { fprintf(stderr, "serve -tab\n"); return 2; }
    printf("# torneo.c scena=%s yp=%.1f ys=%.1f w=%.1f portata=%.1f | N=%d seme=%ld | dw=%+.2f pd=%.2f corpo=%.2f c6=%.2f v=%.2f-%.2f cap=%d vp=%.2f segue=%d congela=%d mancati=%d estraneo=%d vuoto=%.2f\n", scene, YP, YS, W, RMAX, N, seed0, DW, PD, BODY, C6, VLO, VHI, CAP, VP, FOLLOW, FREEZE, MISS, STRANGER, DROP);
    for (int b = 0; b < nb; b++) for (int t = 0; t < N; t++) run_trial(behs[b], (uint64_t)(seed0 + t));
    if (CALMODE) { FILE *f = fopen(calout, "w"); fprintf(f, "# taratura scena=%s N=%d seme=%ld v=%.2f-%.2f: k, q90 per comportamento 0..6 (-1 se n<30), q50 e q90 dell'insieme\n", scene, N, seed0, VLO, VHI);
        static float pool[7 * NMAXT]; for (int k = 0; k < 80; k++) { fprintf(f, "%d", k); int np = 0; for (int b = 0; b < 7; b++) { for (int i = 0; i < CALN[b][k]; i++) pool[np++] = CALE[b][k][i]; fprintf(f, " %.3f", CALN[b][k] >= 30 ? quant(CALE[b][k], CALN[b][k], 0.90) : -1.0); }
            fprintf(f, " %.3f %.3f\n", np >= 30 ? quant(pool, np, 0.5) : -1.0, np >= 30 ? quant(pool, np, 0.9) : -1.0); } fclose(f); printf("scritta %s\n", calout); return 0; }
    printf("\n## 1. copertura per comportamento e tau (cicli a soggetto NON visibile). Per candidata: c90 c50 area90/ombra senzaRegione%%\n");
    printf("%-11s tau    n |", "comport."); for (int c = 0; c < NCAND; c++) printf(" %-22s|", CN[c]); printf(" REACH   S1  S1congelato\n");
    for (int b = 0; b < nb; b++) { int B = behs[b]; for (int t = 0; t < NTAU; t++) { long n = S.n[B][t]; if (n < 1) continue; printf("%-11s %4.1f %4ld |", BN[B], TAUK[t] * DT, n);
            for (int c = 0; c < NCAND; c++) printf(" %5.3f %5.3f %4.2f %5.1f |", (double)S.in90[B][t][c] / n, (double)S.in50[B][t][c] / n, S.area[B][t][c] / n, 100.0 * S.noreg[B][t][c] / n);
            printf(" %5.3f %5.3f %5.3f\n", (double)S.reach[B][t] / n, (double)S.s1[B][t] / n, (double)S.s1f[B][t] / n); } }
    printf("\n## 2. per ciclo nascosto e per passaggio. Per candidata: cicli senza regione %% (passaggi) | regione vuota %% | cicli R90 su libero oltre fascia %% (passaggi) | cicli R90 su libero stretto %% | cicli 'piccola e sbagliata' %% (passaggi) | punto su libero oltre fascia %%\n");
    for (int b = 0; b < nb; b++) { int B = behs[b]; double h = S.hid[B] > 0 ? S.hid[B] : 1; printf("%-11s passaggi %ld, con occlusione %ld, cicli nascosti %ld | fuori REACH: cicli %ld passaggi %ld | fuori S1: %ld / %ld | fuori S1 congelato: %ld / %ld\n", BN[B], S.pas[B], S.pocc[B], S.hid[B], S.creach[B], S.preach[B], S.cs1[B], S.ps1[B], S.cs1f[B], S.ps1f[B]);
        for (int c = 0; c < NCAND; c++) printf("   %-6s senza %5.1f (%ld) | vuota %5.1f | suFG %5.1f (%ld) | suLibero %5.1f | piccolaSbagliata %5.1f (%ld) | puntoFG %5.1f\n", CN[c], 100 * S.cnoreg[B][c] / h, S.pnoreg[B][c], 100 * S.cempty[B][c] / h, 100 * S.cfg[B][c] / h, S.pfg[B][c], 100 * S.cfree[B][c] / h, 100 * S.ccw[B][c] / h, S.pcw[B][c], 100 * S.cptfg[B][c] / h); }
    printf("\n## 3. cicli a soggetto VISIBILE ma non rilevato durante l'occlusione dichiarata (fuori dalla fascia C6): n | contenuto da R90 per candidata | REACH | S1\n");
    for (int b = 0; b < nb; b++) { int B = behs[b]; long n = S.vu[B]; if (!n) continue; printf("%-11s %5ld |", BN[B], n); for (int c = 0; c < NCAND; c++) printf(" %5.3f", (double)S.vu90[B][c] / n); printf(" | %5.3f | %5.3f\n", (double)S.vureach[B] / n, (double)S.vus1[B] / n); }
    printf("\n## 4. ricomparsa: n, buio medio s | per candidata: prima misura entro 0,45 / entro 0,30 / dentro R90 | ellisse 95%% ESTA ESTB: calcolata [dichiarata, cioe non perso] (perso a quel punto) | R90 > meta ombra prima della ricomparsa, per candidata | > 80%% | nucleo ancora mostrato\n");
    for (int b = 0; b < nb; b++) { int B = behs[b]; long n = S.re[B]; if (!n) { printf("%-11s 0\n", BN[B]); continue; } printf("%-11s %4ld %4.2f |", BN[B], n, S.dark[B] / n);
        for (int c = 0; c < NCAND; c++) printf(" %4.2f/%4.2f/%4.2f", (double)S.re45[B][c] / n, (double)S.re30[B][c] / n, (double)S.rein[B][c] / n);
        printf(" | %5.3f [%5.3f] (%4.2f) %5.3f [%5.3f] (%4.2f) | meta:", (double)S.reell[B][0] / n, (double)S.reellp[B][0] / n, (double)S.reperso[B][0] / n, (double)S.reell[B][1] / n, (double)S.reellp[B][1] / n, (double)S.reperso[B][1] / n);
        for (int c = 0; c < NCAND; c++) printf(" %4.2f", (double)S.half[B][c] / n); printf(" | 80:"); for (int c = 0; c < NCAND; c++) printf(" %4.2f", (double)S.eighty[B][c] / n); printf(" | nucleo %4.2f\n", (double)S.nucleo[B] / n);
        printf("            salto mediano / p90 (m): C004 %.2f/%.2f  C001 %.2f/%.2f  vel.cost %.2f/%.2f  EST-A media %.2f/%.2f  fermo %.2f/%.2f\n", quant(JUMP[B][0], S.njump[B], .5), quant(JUMP[B][0], S.njump[B], .9), quant(JUMP[B][1], S.njump[B], .5), quant(JUMP[B][1], S.njump[B], .9), quant(JUMP[B][2], S.njump[B], .5), quant(JUMP[B][2], S.njump[B], .9), quant(JUMP[B][3], S.njump[B], .5), quant(JUMP[B][3], S.njump[B], .9), quant(JUMP[B][4], S.njump[B], .5), quant(JUMP[B][4], S.njump[B], .9)); }
    printf("\n## 5. ciclo di vita: passaggi | con un ciclo nascosto senza traccia pendente (cicli) | traccia chiusa in campo aperto | entrata non confermata | velocita stimata/vera all'ingresso: mediana p10 p90\n");
    for (int b = 0; b < nb; b++) { int B = behs[b]; printf("%-11s %4ld | %4ld (%ld) | %4ld | %4ld | corrette %ld | %.2f %.2f %.2f\n", BN[B], S.pas[B], S.nopend[B], S.chidnp[B], S.closed[B], S.unconf[B], S.fixed[B], quant(VR[B], S.nvr[B], .5), quant(VR[B], S.nvr[B], .1), quant(VR[B], S.nvr[B], .9)); }
    printf("\n## 6. C-EST: passaggi con mu1 > 0,5 oltre 0,5 s dopo l'uscita attesa (A, B) | per tau: perso%% A B, sigma_eff medio A B, mu1 medio A B\n");
    for (int b = 0; b < nb; b++) { int B = behs[b]; printf("%-11s mu1 dominante: A %ld  B %ld su %ld occlusioni\n", BN[B], S.mu1dom[B][0], S.mu1dom[B][1], S.pocc[B]);
        for (int t = 0; t < NTAU; t++) { long n = S.n[B][t]; if (n < 1) continue; printf("     tau %4.1f n %4ld | perso %5.1f %5.1f | sigma %4.2f %4.2f | mu1 %4.2f %4.2f\n", TAUK[t] * DT, n, 100.0 * S.esperso[B][t][0] / n, 100.0 * S.esperso[B][t][1] / n, S.essig[B][t][0] / n, S.essig[B][t][1] / n, S.esmu[B][t][0] / n, S.esmu[B][t][1] / n); } }
    printf("\n## 7. miscele per ripesatura: 'squadra' = pesi di -mix (predefiniti 60/10/10/10/5/5), giurato 30/10/20/20/10/10: tau | per candidata c90 c50\n");
    { double WM[2][7] = {{0}, {.30, .10, .20, .20, .10, .10, 0}}; for (int q = 0; q < 7; q++) WM[0][q] = MIXW[q]; static const char *MN[2] = {"squadra", "giurato"};
      for (int mi = 0; mi < 2; mi++) for (int t = 0; t < 5; t++) { double den = 0, num9[NCAND] = {0}, num5[NCAND] = {0}; int ok = 1;
              for (int B = 0; B < 7; B++) { if (WM[mi][B] <= 0) continue; if (S.pas[B] == 0) { ok = 0; break; } double wq = WM[mi][B] / S.pas[B]; den += wq * S.n[B][t]; for (int c = 0; c < NCAND; c++) { num9[c] += wq * S.in90[B][t][c]; num5[c] += wq * S.in50[B][t][c]; } }
              if (!ok || den <= 0) continue; printf("%-8s %4.1f n.eff %5.1f |", MN[mi], TAUK[t] * DT, den * 200); for (int c = 0; c < NCAND; c++) printf(" %s %5.3f %5.3f |", CN[c], num9[c] / den, num5[c] / den); printf("\n"); } }
    printf("\n## 8. errore mediano del punto (m) per comportamento e tau: C004 fantasma | C001 media | vel.cost | EST-A media ritagliata | fermo\n");
    for (int b = 0; b < nb; b++) { int B = behs[b]; for (int t = 0; t < NTAU; t++) { int n = S.nperr[B][t]; if (n < 30) continue; printf("%-11s %4.1f %4d | %.2f | %.2f | %.2f | %.2f | %.2f\n", BN[B], TAUK[t] * DT, n, quant(PERR[B][t][0], n, .5), quant(PERR[B][t][1], n, .5), quant(PERR[B][t][2], n, .5), quant(PERR[B][t][3], n, .5), quant(PERR[B][t][4], n, .5)); } }
    if (STRANGER) { printf("\n## 9. estraneo: rilevato durante l'occlusione %ld | con il primo ancora nascosto %ld | riagganciato dalla regola del nucleo (entro 0,40 dall'ombra) %ld | dalla porta R90+0,45 per candidata:", S.st_n, S.st_first, S.st_nuc); for (int c = 0; c < NCAND; c++) printf(" %s %ld", CN[c], S.st_gate[c]); printf(" | ellisse 95%% ESTA %ld ESTB %ld\n", S.st_ell[0], S.st_ell[1]); }
    printf("\n## 10. costo per ciclo e traccia (C, -O2, macchina condivisa): media / massimo in microsecondi\n");
    for (int c = 0; c < NCAND; c++) if (tcn[c]) printf("%-6s %8.1f / %8.1f  (n %ld)\n", CN[c], tns[c] / tcn[c] / 1000, tmax[c] / 1000, tcn[c]);
    return 0;
}
