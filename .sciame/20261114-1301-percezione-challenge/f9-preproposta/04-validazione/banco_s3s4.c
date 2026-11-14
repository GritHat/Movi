// banco_s3s4.c — sciame-validazione, estensione f9.
// Banco indipendente per S3 (inseguitore a due ipotesi) + S4 (ritaglio con l'informazione negativa)
// della preproposta esterna, implementate come scritte, e per la regola attuale del nucleo
// (cerchio al 95 % ritagliato sul cuneo, «perso» a meta' cuneo) sulla stessa scena.
// Scritto da zero: non usa codice di altri ruoli. Solo libreria standard C.
// Compilare: gcc -O2 -o banco banco_s3s4.c -lm
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>

#define DT (1.0/15.0)
#define CS 0.05
#define GX0 (-4.0)
#define GZ0 0.0
#define NX 160
#define NZ 96
#define NC (NX*NZ)
enum { LIB = 0, OCC = 1, OMB = 2, NOS = 3 };
#define RB 0.20
#define FOVH (43.5*M_PI/180.0)
#define RMIN 1.24
#define FASCIA 0.40
#define GATE 9.21
#define NBEH 9
#define NBIN 6
#define MAXP 4000
static const char *BNAME[NBEH] = {"prosegue", "rallenta", "ferma-riparte", "torna", "lato-lontano",
                                  "uno-due", "tripla", "ferma-meta", "ferma-caso"};
static const int BINK[NBIN] = {8, 15, 23, 30, 38, 45}; // 0,5 ... 3,0 s a 15 Hz

// ---- configurazione
static double Zp = 1.8, HW = 0.5, ZA = 2.3, RMAX = 3.0, XS = 1.9;
static double PD = 1.0, SIGM = 0.03, QQ = 0.2, MASKE = 0.0, VFIX = -1, SEFFMAX = 0.8;
static int WMODE = 1, LMODE = 1, NMODE = 0, CLAMP = 1, NPASS = 400, PANEL = 1;
static uint64_t SEED = 20261114;
static int TRACE = 0, TRACEP = 0, FALSO = 0;

// ---- generatore
static uint64_t rs;
static uint64_t splitmix(void) { uint64_t z = (rs += 0x9E3779B97F4A7C15ULL); z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ULL; z = (z ^ (z >> 27)) * 0x94D049BB133111EBULL; return z ^ (z >> 31); }
static double ru(void) { return (splitmix() >> 11) * (1.0 / 9007199254740992.0); }
static double rg(void) { double u = ru(), v = ru(); if (u < 1e-300) u = 1e-300; return sqrt(-2 * log(u)) * cos(2 * M_PI * v); }
static double runi(double a, double b) { return a + (b - a) * ru(); }

// ---- mappe
static unsigned char st_true[NC], st_est[NC], mp_true[NC], mp_est[NC];
static int wedge_cells; static double WCX, WCZ; static double tm_sum = 0, tm_max = 0; static long tm_n = 0;
static inline double cxi(int i) { return GX0 + (i + 0.5) * CS; }
static inline double czj(int j) { return GZ0 + (j + 0.5) * CS; }
static void build_static(unsigned char *m, double hw) {
    for (int j = 0; j < NZ; j++) for (int i = 0; i < NX; i++) {
        double x = cxi(i), z = czj(j), r = hypot(x, z), th = atan2(x, z);
        unsigned char s;
        if (fabs(th) > FOVH || r > RMAX || r < RMIN) s = NOS;
        else if (z > Zp - CS / 2 && fabs(x * Zp / z) <= hw) s = (z <= Zp + CS / 2) ? OCC : OMB;
        else s = LIB;
        m[j * NX + i] = s;
    }
}
// visibilita' di un disco: 2 tutto visibile, 1 tagliato, 0 nascosto o fuori
static int visib(double bx, double bz) {
    double r = hypot(bx, bz), th = atan2(bx, bz), a = asin(RB / r), ap = atan(HW / Zp);
    if (r - RB > RMAX || fabs(th) - a > FOVH) return 0;
    int full = 1;
    if (r + RB > RMAX || r - RB < RMIN || fabs(th) + a > FOVH) full = 0;
    if (bz - RB > Zp) {
        if (th - a >= -ap && th + a <= ap) return 0;
        if (!(th - a >= ap || th + a <= -ap)) full = 0;
    }
    return full ? 2 : 1;
}
static void overlay(unsigned char *dst, const unsigned char *src, const double *bx, const double *bz, int nb) {
    memcpy(dst, src, NC);
    for (int b = 0; b < nb; b++) {
        if (visib(bx[b], bz[b]) == 0) continue;
        int j0 = (int)floor((bz[b] - RB - CS - GZ0) / CS); if (j0 < 0) j0 = 0;
        for (int j = j0; j < NZ; j++) for (int i = 0; i < NX; i++) {
            int c = j * NX + i; if (dst[c] != LIB) continue;
            double x = cxi(i), z = czj(j), r = hypot(x, z);
            double pr = (x * bx[b] + z * bz[b]) / r, d = fabs(x * bz[b] - z * bx[b]) / r;
            if (pr <= 0 || d >= RB) continue;
            double tin = pr - sqrt(RB * RB - d * d);
            if (r >= tin - CS / 2) dst[c] = (r <= tin + CS / 2) ? OCC : OMB;
        }
    }
}
static double dist_wedge(double x, double z, double hw) { return fabs(x) - hw * z / Zp; } // >0 fuori dal cuneo

// ---- filtro
static void kf_pred(double *x, double *v, double *P) {
    *x += *v * DT; double a = P[0], b = P[1], c = P[2];
    P[0] = a + 2 * DT * b + DT * DT * c + QQ * DT * DT * DT / 3; P[1] = b + DT * c + QQ * DT * DT / 2; P[2] = c + QQ * DT;
}
static void h2_pred(double *x, double *v, double *P, double al) {
    *v *= al; *x += *v * DT; double a = P[0], b = P[1], c = P[2];
    P[0] = a + 2 * al * DT * b + al * al * DT * DT * c + QQ * DT * DT * DT / 3; P[1] = al * b + al * al * DT * c + QQ * DT * DT / 2; P[2] = al * al * c + QQ * DT;
}
static void kf_upd(double *x, double *v, double *P, double z, double R) {
    double S = P[0] + R, k1 = P[0] / S, k2 = P[1] / S, nu = z - *x; *x += k1 * nu; *v += k2 * nu;
    double a = P[0], b = P[1], c = P[2]; P[0] = (1 - k1) * a; P[1] = (1 - k1) * b; P[2] = c - k2 * b;
}

typedef struct {
    int valid; double shx, shz, seff, f1, f2, M, mu1, mu2, err; int in1, in2, in173, inhdr;
    double wfrac; int hdr_estlib, hdr_truelib, disc_n, disc_lib, mean_lib;
} Disp;
typedef struct {
    int alive, id, src, status, hits, age, miss_open, born; // status 0 tentativa, 1 vista, 2 in occlusione
    double x[4], PX[3], PZ[3], lmx, lmz;
    double x2[4], P2X[3], P2Z[3], alpha, mu1, mu2; int kocc, perso, perso_reason, strato1, was_hidden;
    int nuc_perso, nuc_shown, nuc_cont; double ent_x, ent_v; int tdom;
    Disp d, dprev; int has_prev, nuc_shown_prev;
} Track;

static double Phi(double u) { return 0.5 * erfc(-u * M_SQRT1_2); }
static void colmass(double m, double s, double g0, int n, int *lo, int *hi, double *out) {
    int a = (int)floor((m - 6.0 * s - g0) / CS), b = (int)floor((m + 6.0 * s - g0) / CS);
    if (a < 0) a = 0; if (b > n - 1) b = n - 1; *lo = a; *hi = b; if (a > b) return;
    double prev = Phi((g0 + a * CS - m) / s);
    for (int i = a; i <= b; i++) { double nx = Phi((g0 + (i + 1) * CS - m) / s); out[i] = nx - prev; prev = nx; }
}
static double dens[NC];
// calcola cio' che la preproposta mostra per una traccia in occlusione; aggiorna i pesi
static void display(Track *t, double tx, double tz) {
    Disp *o = &t->d; memset(o, 0, sizeof(*o));
    static double a1x[NX], a1z[NZ], a2x[NX], a2z[NZ];
    memset(a1x, 0, sizeof a1x); memset(a1z, 0, sizeof a1z); memset(a2x, 0, sizeof a2x); memset(a2z, 0, sizeof a2z);
    int l1, h1, l2, h2, m1, n1, m2, n2;
    colmass(t->x[0], sqrt(t->PX[0]), GX0, NX, &l1, &h1, a1x); colmass(t->x[2], sqrt(t->PZ[0]), GZ0, NZ, &m1, &n1, a1z);
    colmass(t->x2[0], sqrt(t->P2X[0]), GX0, NX, &l2, &h2, a2x); colmass(t->x2[2], sqrt(t->P2Z[0]), GZ0, NZ, &m2, &n2, a2z);
    int il = l1 < l2 ? l1 : l2, ih = h1 > h2 ? h1 : h2, jl = m1 < m2 ? m1 : m2, jh = n1 > n2 ? n1 : n2;
    double p1 = (WMODE == 1) ? t->mu1 : 0.8, p2 = (WMODE == 1) ? t->mu2 : 0.2;
    double na1 = 0, na2 = 0, al1 = 0, al2 = 0, T = 0, Sx = 0, Sz = 0, Sxx = 0, Szz = 0, dmax = 0;
    for (int j = jl; j <= jh; j++) for (int i = il; i <= ih; i++) {
        int c = j * NX + i; double q1 = a1x[i] * a1z[j], q2 = a2x[i] * a2z[j]; unsigned char s = mp_est[c];
        int ok = !CLAMP ? 1 : (NMODE == 0 ? (s >= OMB) : (s == OMB));
        if (ok) { al1 += q1; al2 += q2; double d = p1 * q1 + p2 * q2; dens[c] = d; T += d; double x = cxi(i), z = czj(j); Sx += d * x; Sz += d * z; Sxx += d * x * x; Szz += d * z * z; if (d > dmax) dmax = d; }
        else { na1 += q1; na2 += q2; dens[c] = 0; }
    }
    if (!CLAMP) { o->f1 = o->f2 = 1; } else if (NMODE == 0) { o->f1 = 1 - na1; o->f2 = 1 - na2; } else { o->f1 = al1; o->f2 = al2; }
    if (o->f1 < 0) o->f1 = 0; if (o->f2 < 0) o->f2 = 0;
    o->M = 0.8 * o->f1 + 0.2 * o->f2;
    double w1 = p1 * o->f1, w2 = p2 * o->f2, ws = w1 + w2;
    if (ws > 1e-280) { t->mu1 = w1 / ws; t->mu2 = w2 / ws; }
    o->mu1 = t->mu1; o->mu2 = t->mu2;
    if (T < 1e-12) { o->valid = 0; return; }
    o->valid = 1; o->shx = Sx / T; o->shz = Sz / T;
    double vx = Sxx / T - o->shx * o->shx, vz = Szz / T - o->shz * o->shz; if (vx < 0) vx = 0; if (vz < 0) vz = 0;
    o->seff = sqrt(vx + vz + CS * CS / 6);
    o->err = hypot(o->shx - tx, o->shz - tz);
    o->in1 = o->err <= o->seff; o->in2 = o->err <= 2 * o->seff; o->in173 = o->err <= 1.7308 * o->seff;
    // regione di massima densita' al 95 %
    int ti = (int)floor((tx - GX0) / CS), tj = (int)floor((tz - GZ0) / CS); double dt = -1;
    if (ti >= il && ti <= ih && tj >= jl && tj <= jh) dt = dens[tj * NX + ti];
    static double hist[512]; memset(hist, 0, sizeof hist); double above = 0;
    for (int j = jl; j <= jh; j++) for (int i = il; i <= ih; i++) {
        double d = dens[j * NX + i]; if (d <= 0) continue; if (d > dt) above += d;
        int e; double mnt = frexp(d / dmax, &e); int b = (-e) * 8 + (int)((1.0 - mnt) * 16.0); if (b < 0) b = 0; if (b > 511) b = 511; hist[b] += d;
    }
    o->inhdr = (dt > 0) && (above / T < 0.95);
    double cum = 0; int bt = 511; for (int b = 0; b < 512; b++) { cum += hist[b]; if (cum >= 0.95 * T) { bt = b; break; } }
    int nw = 0;
    for (int j = jl; j <= jh; j++) for (int i = il; i <= ih; i++) {
        int c = j * NX + i; double d = dens[c]; if (d <= 0) continue;
        int e; double mnt = frexp(d / dmax, &e); int b = (-e) * 8 + (int)((1.0 - mnt) * 16.0); if (b < 0) b = 0;
        if (b > bt) continue;
        if (mp_est[c] == LIB) o->hdr_estlib++; if (mp_true[c] == LIB) o->hdr_truelib++; if (st_est[c] == OMB) nw++;
    }
    o->wfrac = (double)nw / wedge_cells;
    // disco di raggio sigma_eff attorno alla posizione mostrata
    int i0 = (int)floor((o->shx - o->seff - GX0) / CS), i1 = (int)floor((o->shx + o->seff - GX0) / CS), j0 = (int)floor((o->shz - o->seff - GZ0) / CS), j1 = (int)floor((o->shz + o->seff - GZ0) / CS);
    for (int j = j0; j <= j1; j++) for (int i = i0; i <= i1; i++) {
        if (i < 0 || i >= NX || j < 0 || j >= NZ) continue; if (hypot(cxi(i) - o->shx, czj(j) - o->shz) > o->seff) continue;
        o->disc_n++; if (mp_est[j * NX + i] == LIB) o->disc_lib++;
    }
    int si = (int)floor((o->shx - GX0) / CS), sj = (int)floor((o->shz - GZ0) / CS);
    if (si >= 0 && si < NX && sj >= 0 && sj < NZ) o->mean_lib = (mp_est[sj * NX + si] == LIB);
}
// regola del nucleo: cerchio al 95 % sul cuneo, «perso» quando copre meta' del cuneo
static void nucleo(Track *t, double tx, double tz) {
    double r95 = sqrt(5.99 * (t->PX[0] > t->PZ[0] ? t->PX[0] : t->PZ[0]));
    int n = 0;
    int i0 = (int)floor((t->x[0] - r95 - GX0) / CS), i1 = (int)floor((t->x[0] + r95 - GX0) / CS), j0 = (int)floor((t->x[2] - r95 - GZ0) / CS), j1 = (int)floor((t->x[2] + r95 - GZ0) / CS);
    if (i0 < 0) i0 = 0; if (i1 > NX - 1) i1 = NX - 1; if (j0 < 0) j0 = 0; if (j1 > NZ - 1) j1 = NZ - 1;
    for (int j = j0; j <= j1; j++) for (int i = i0; i <= i1; i++) if (st_est[j * NX + i] == OMB && hypot(cxi(i) - t->x[0], czj(j) - t->x[2]) <= r95) n++;
    if (n >= 0.5 * wedge_cells) t->nuc_perso = 1;
    t->nuc_shown = !t->nuc_perso && n > 0;
    t->nuc_cont = t->nuc_shown && hypot(tx - t->x[0], tz - t->x[2]) <= r95 && dist_wedge(tx, tz, HW + MASKE) <= FASCIA && tz >= Zp - FASCIA;
}

// ---- soggetti
typedef struct { double x, z, v, phi, phi2, par, xp; int beh, phase, done, vis, seen; double tph, dx, dz; } Subj;
static void step_subj(Subj *s, double t, int isB, double tstartB) {
    double g = 1 + 0.08 * sin(2 * M_PI * 1.8 * t + s->phi);
    double st = s->v * g * DT;
    if (isB) { if (t >= tstartB) s->x += st; return; }
    switch (s->beh) {
    case 0: case 5: s->x += st; break;
    case 1: if (s->phase == 0 && s->seen && s->vis == 0) { s->phase = 1; s->tph = t; }
        { double m = 1; if (s->phase) { m = 1 - 0.5 * (t - s->tph) / 0.4; if (m < 0.5) m = 0.5; } s->x += st * m; } break;
    case 2: case 7: case 8:
        if (s->phase == 0) { if (s->x + st >= s->xp) { s->x = s->xp; s->phase = 1; s->tph = t; } else s->x += st; }
        else if (s->phase == 1) { if (s->par >= 0 && t - s->tph >= s->par) s->phase = 2; }
        else s->x += st;
        break;
    case 3: if (s->phase == 0) { s->x += st; if (s->x >= s->xp) s->phase = 1; } else s->x -= st; break;
    case 4: if (s->phase == 0) { s->x += st; if (s->x >= s->xp) { s->phase = 1; double r = hypot(s->x, s->z); s->dx = s->x / r; s->dz = s->z / r; } }
        else if (hypot(s->x, s->z) < RMAX + 1.2) { s->x += s->dx * st; s->z += s->dz * st; } break;
    case 6: if (s->phase == 0 && s->seen && s->vis == 0) s->phase = 1; s->x += st * (s->phase ? 3 : 1); break;
    }
    if (s->beh != 4) s->z = ZA + 0.02 * sin(2 * M_PI * 0.9 * t + s->phi2);
    if (s->x >= XS || (s->beh == 3 && s->phase == 1 && s->x <= -XS)) s->done = 1;
}

// ---- statistiche
typedef struct {
    long npass, ntrk; // passaggi, passaggi con la traccia entrata in occlusione
    long b_tot[NBIN], b_est[NBIN], b_perso[NBIN], b_notrk[NBIN], b_in1[NBIN], b_in2[NBIN], b_in173[NBIN], b_hdr[NBIN], b_w50[NBIN], b_nuc[NBIN], b_nucc[NBIN], b_mlow[NBIN];
    double b_wf[NBIN]; float *b_err[NBIN], *b_se[NBIN], *b_eh[NBIN], *b_ec[NBIN];
    long fr_occ, fr_est, fr_perso, fr_notrk, fr_nuc, pass_full, pass_nucfull, perso_sig, perso_coll; double perso_t;
    long fr_estlib, fr_truelib, pass_truelib, fr_disclib, fr_est15, fr_disclib15, fr_meanlib, fr_w50_15; double disc_frac;
    long fr_e30, fr_mlow30, fr_mlow;
    long n_dom, n_nodom; float *tdom_fv, *tdom_ed, *tdom_abs;
    long re_n, re_notrk, re_perso, re_in1, re_in2, re_in173, re_hdr, re_p1, re_p2, re_phdr, re_sosta, re_gate, re_kf95, re_nucgeo, re_nucshown; float *re_err, *re_se, *re_tocc;
    long gate_viol, ghost_end, ghost_pass; long b_first, swap_mute, pp_lost_pass, pp_lost_fr, a_split;
    long fin_n, fin_same;
} Stat;
static Stat S[NBEH];
static int cmpf(const void *a, const void *b) { float x = *(const float *)a, y = *(const float *)b; return (x > y) - (x < y); }
static double pct(float *a, long n, double p) { if (n <= 0) return NAN; qsort(a, n, sizeof(float), cmpf); double k = p * (n - 1); long i = (long)k; double f = k - i; return i + 1 < n ? a[i] * (1 - f) + a[i + 1] * f : a[i]; }
static void wilson(long k, long n, double *lo, double *hi) { if (n == 0) { *lo = *hi = NAN; return; } double z = 1.96, p = (double)k / n, d = 1 + z * z / n, c = p + z * z / (2 * n), h = z * sqrt(p * (1 - p) / n + z * z / (4.0 * n * n)); *lo = (c - h) / d; *hi = (c + h) / d; }
static double P100(long k, long n) { return n ? 100.0 * k / n : NAN; }

static void run_pass(int beh, int ip) {
    Stat *q = &S[beh];
    rs = SEED * 1000003ULL + (uint64_t)beh * 7919ULL + (uint64_t)ip * 104729ULL + 17; for (int i = 0; i < 4; i++) splitmix();
    double xsc = HW * ZA / Zp; // semilarghezza dell'ombra sulla linea del soggetto
    Subj A; memset(&A, 0, sizeof A); A.beh = beh; A.x = -XS; A.z = ZA; A.v = runi(0.3, 1.8); A.phi = runi(0, 2 * M_PI); A.phi2 = runi(0, 2 * M_PI);
    double u1 = ru(), u2 = ru(), u3 = ru(), u4 = ru(), u5 = ru();
    if (VFIX > 0) A.v = VFIX;
    A.par = -1; A.xp = 0;
    if (beh == 2) { A.par = 1.0 + 2.0 * u1; A.xp = 0; }
    if (beh == 7) A.xp = 0;
    if (beh == 8) A.xp = (2 * u1 - 1) * 0.6 * xsc;
    if (beh == 3 || beh == 4) A.xp = (2 * u1 - 1) * 0.45 * xsc;
    Subj B; memset(&B, 0, sizeof B); B.x = (-0.3 + 0.7 * u2) * xsc; B.z = ZA - 0.25; B.v = 0.6 + 1.0 * u3; B.phi = 2 * M_PI * u4; double delayB = 1.0 * u5, tstartB = 1e9;
    int nsub = (beh == 5) ? 2 : 1;
    Track T[8]; memset(T, 0, sizeof T); int nextid = 1, idA = -1;
    int ep0 = -1, kre = -1, kcap = 100000, tdom_done = 0; int had_ta = 0; int lastA = -1;
    long fr_occ = 0, fr_est = 0, fr_nuc = 0; int truelib_pass = 0, pp_lost = 0, ghost = 0, ghost_k = -1, bfirst = -1;
    double R = SIGM * SIGM;
    q->npass++;
    for (int k = 0; k < 1200; k++) {
        double t = k * DT;
        // verita'
        step_subj(&A, t, 0, 0); if (nsub == 2) step_subj(&B, t, 1, tstartB);
        A.vis = visib(A.x, A.z); if (A.vis == 2) A.seen = 1;
        if (nsub == 2) B.vis = visib(B.x, B.z);
        if (ep0 < 0 && A.seen && A.vis < 2) { ep0 = k; tstartB = t + delayB; kcap = k + ((beh == 4 || beh == 7 || beh == 8) ? 120 : 200); }
        // rilevamenti (le estrazioni non dipendono dalla variante)
        double detx[2], detz[2]; int dsrc[2], nd = 0, used[2] = {0, 0};
        for (int sidx = 0; sidx < 2; sidx++) {
            double u = ru(), g1 = rg(), g2 = rg(); Subj *s = sidx ? &B : &A;
            if (sidx >= nsub) continue;
            if (s->vis == 2 && u < PD) { detx[nd] = s->x + SIGM * g1; detz[nd] = s->z + SIGM * g2; dsrc[nd] = sidx; nd++; }
        }
        int detA = -1; for (int d = 0; d < nd; d++) if (dsrc[d] == 0) detA = d;
        // mappe del fotogramma
        double bx[2] = {A.x, B.x}, bz[2] = {A.z, B.z};
        overlay(mp_true, st_true, bx, bz, nsub); overlay(mp_est, st_est, bx, bz, nsub);
        // braccio «falso libero»: per FALSO fotogrammi da 0,53 s il cuneo stimato risulta suolo visto (buco riempito dal sensore)
        if (FALSO > 0 && ep0 >= 0 && k - ep0 >= 8 && k - ep0 < 8 + FALSO) for (int c = 0; c < NC; c++) if (st_est[c] == OMB) mp_est[c] = LIB;
        // predizione
        for (int i = 0; i < 8; i++) if (T[i].alive) {
            Track *tr = &T[i]; kf_pred(&tr->x[0], &tr->x[1], tr->PX); kf_pred(&tr->x[2], &tr->x[3], tr->PZ);
            if (tr->status == 2) { h2_pred(&tr->x2[0], &tr->x2[1], tr->P2X, tr->alpha); h2_pred(&tr->x2[2], &tr->x2[3], tr->P2Z, tr->alpha); tr->kocc++; }
        }
        // associazione delle tracce viste e tentative (prima le confermate)
        for (int i = 0; i < 8; i++) if (T[i].alive && T[i].status == 1) {
            Track *tr = &T[i]; int best = -1; double bd = GATE;
            for (int d = 0; d < nd; d++) if (!used[d]) { double ex = detx[d] - tr->x[0], ez = detz[d] - tr->x[2]; double d2 = ex * ex / (tr->PX[0] + R) + ez * ez / (tr->PZ[0] + R); if (d2 <= bd) { bd = d2; best = d; } }
            tr->age++;
            if (best >= 0) {
                used[best] = 1; kf_upd(&tr->x[0], &tr->x[1], tr->PX, detx[best], R); kf_upd(&tr->x[2], &tr->x[3], tr->PZ, detz[best], R);
                tr->lmx = detx[best]; tr->lmz = detz[best]; tr->hits++; tr->miss_open = 0; tr->src = dsrc[best]; if (dsrc[best] == 0) lastA = tr->id;
            } else {
                if (dist_wedge(tr->lmx, tr->lmz, HW + MASKE) <= FASCIA && tr->lmz > Zp) { // entra in occlusione
                    tr->status = 2; tr->kocc = 0; memcpy(tr->x2, tr->x, sizeof tr->x); memcpy(tr->P2X, tr->PX, sizeof tr->PX); memcpy(tr->P2Z, tr->PZ, sizeof tr->PZ);
                    tr->mu1 = 0.8; tr->mu2 = 0.2; tr->perso = 0; tr->perso_reason = 0; tr->nuc_perso = 0; tr->strato1 = 1; tr->was_hidden = 0; tr->has_prev = 0; tr->tdom = -1;
                    double d = fabs(0.0 - tr->x[0]), vv = fabs(tr->x[1]);
                    tr->alpha = 0.90;
                    if (LMODE == 1 && vv * DT > 1e-6 && (0.0 - tr->x[0]) * tr->x[1] > 0) { double al = d / (d + vv * DT); if (al < 0.5) al = 0.5; if (al > 0.995) al = 0.995; tr->alpha = al; }
                    tr->ent_x = tr->x[0]; tr->ent_v = tr->x[1];
                } else { tr->miss_open++; if (tr->miss_open > 3) tr->alive = 0; }
            }
        }
        // tracce in occlusione: che cosa si mostra (prima dell'associazione)
        Track *ta = NULL;
        for (int i = 0; i < 8; i++) if (T[i].alive && T[i].status == 2) {
            Track *tr = &T[i]; Subj *s = tr->src ? &B : &A;
            if (s->vis == 0) tr->was_hidden = 1;
            tr->dprev = tr->d; tr->nuc_shown_prev = tr->nuc_shown; if (tr->kocc > 0) tr->has_prev = 1;
            { struct timespec t0, t1; clock_gettime(CLOCK_MONOTONIC, &t0); display(tr, s->x, s->z); clock_gettime(CLOCK_MONOTONIC, &t1); double us = (t1.tv_sec - t0.tv_sec) * 1e6 + (t1.tv_nsec - t0.tv_nsec) / 1e3; tm_sum += us; tm_n++; if (us > tm_max) tm_max = us; }
            nucleo(tr, s->x, s->z);
            if (!tr->perso) {
                if (!tr->d.valid) { tr->perso = 1; tr->perso_reason = 2; if (tr->src == 0) { q->perso_coll++; q->perso_t += tr->kocc * DT; } }
                else if (tr->d.seff > SEFFMAX) { tr->perso = 1; tr->perso_reason = 1; if (TRACE && TRACEP < 0) printf("PERSO beh %d pass %d k %d kocc %d v %.2f A (%+.2f,%.2f) vis %d | H1 (%+.2f,%.2f) s %.2f | H2 (%+.2f,%.2f) s %.2f | mu1 %.3f f1 %.3f f2 %.3f | mostrata (%+.2f,%.2f) sig_eff %.3f\n", beh, ip, k, tr->kocc, A.v, A.x, A.z, A.vis, tr->x[0], tr->x[2], sqrt(tr->PX[0]), tr->x2[0], tr->x2[2], sqrt(tr->P2X[0]), tr->mu1, tr->d.f1, tr->d.f2, tr->d.shx, tr->d.shz, tr->d.seff); if (tr->src == 0) { q->perso_sig++; q->perso_t += tr->kocc * DT; } }
            }
            if (tr->tdom < 0 && tr->mu2 > 0.5) tr->tdom = tr->kocc;
            if (tr->src == 0 && !ta) ta = tr;
        }
        if (ta && ta->was_hidden && !had_ta) { had_ta = 1; q->ntrk++; }
        if (TRACE && ip == TRACEP && ep0 >= 0) printf("T k %3d t_occ %5.2f vis %d det %d | A (%+.2f, %.2f) | " , k, (k - ep0) * DT, A.vis, detA >= 0, A.x, A.z), ta ? printf("H1 x %+.2f sx %.2f  H2 x %+.2f sx %.2f a %.3f | f1 %.3f f2 %.3f mu1 %.3f | mostrata (%+.2f, %.2f) sig_eff %.2f err %.2f M %.3f perso %d wf %.2f nuc %d\n", ta->x[0], sqrt(ta->PX[0]), ta->x2[0], sqrt(ta->P2X[0]), ta->alpha, ta->d.f1, ta->d.f2, ta->mu1, ta->d.shx, ta->d.shz, ta->d.seff, ta->d.err, ta->d.M, ta->perso, ta->d.wfrac, ta->nuc_shown) : printf("nessuna traccia in occlusione\n");
        // statistiche per fotogramma dell'episodio di occlusione di A
        if (ep0 >= 0 && kre < 0 && detA < 0 && A.vis < 2) {
            int kt = k - ep0; fr_occ++; q->fr_occ++;
            int est = ta && !ta->perso && ta->d.valid;
            if (est) { fr_est++; q->fr_est++; } else if (ta) q->fr_perso++; else q->fr_notrk++;
            if (ta && ta->nuc_shown) { fr_nuc++; q->fr_nuc++; }
            if (est) {
                Disp *d = &ta->d;
                if (d->hdr_estlib) q->fr_estlib++; if (d->hdr_truelib) { q->fr_truelib++; truelib_pass = 1; }
                if (d->disc_lib) q->fr_disclib++; if (d->mean_lib) q->fr_meanlib++; q->disc_frac += d->disc_n ? (double)d->disc_lib / d->disc_n : 0;
                if (kt >= 15) { q->fr_est15++; if (d->disc_lib) q->fr_disclib15++; if (d->wfrac > 0.5) q->fr_w50_15++; }
                if (d->M < 0.05) q->fr_mlow++;
                if (kt >= 30) { q->fr_e30++; if (d->M < 0.05) q->fr_mlow30++; }
            }
            for (int b = 0; b < NBIN; b++) if (kt == BINK[b]) {
                q->b_tot[b]++;
                if (est) { Disp *d = &ta->d; long n = q->b_est[b]; if (n < MAXP) { q->b_err[b][n] = d->err; q->b_se[b][n] = d->seff; q->b_eh[b][n] = hypot(ta->x[0] - A.x, ta->x[2] - A.z); q->b_ec[b][n] = hypot(WCX - A.x, WCZ - A.z); }
                    q->b_est[b]++; q->b_in1[b] += d->in1; q->b_in2[b] += d->in2; q->b_in173[b] += d->in173; q->b_hdr[b] += d->inhdr; q->b_wf[b] += d->wfrac; q->b_w50[b] += d->wfrac > 0.5; q->b_mlow[b] += d->M < 0.05; }
                else if (ta) q->b_perso[b]++; else q->b_notrk[b]++;
                if (ta && ta->nuc_shown) { q->b_nuc[b]++; q->b_nucc[b] += ta->nuc_cont; }
            }
            if (beh == 5 && A.vis == 0) { int pp = 0; for (int i = 0; i < 8; i++) if (T[i].alive && T[i].status == 2 && T[i].strato1) pp = 1; if (!pp && idA >= 0) { pp_lost = 1; q->pp_lost_fr++; } }
        }
        // tempo di dominanza della sosta (una volta per passaggio, sulla traccia di A)
        if (ta && !tdom_done && ta->tdom >= 0 && ta->was_hidden) {
            tdom_done = 1; double v = fabs(ta->ent_v); if (v < 0.05) v = 0.05;
            double xfv = xsc + 0.02; while (visib(xfv, ZA) != 2 && xfv < 5) xfv += 0.005;
            long n = q->n_dom; if (n < MAXP) { q->tdom_abs[n] = ta->tdom * DT; q->tdom_fv[n] = ta->tdom * DT - (xfv - ta->ent_x) / v; q->tdom_ed[n] = ta->tdom * DT - (xsc - ta->ent_x) / v; } q->n_dom++;
        }
        // associazione delle tracce in occlusione: porta chi-quadro contro H1 o H2
        for (int d = 0; d < nd; d++) if (!used[d]) {
            int best = -1, bh = 0; double bd = GATE, d1best = 1e9;
            for (int i = 0; i < 8; i++) if (T[i].alive && T[i].status == 2 && T[i].kocc > 0) {
                Track *tr = &T[i];
                double ex = detx[d] - tr->x[0], ez = detz[d] - tr->x[2], d1 = ex * ex / (tr->PX[0] + R) + ez * ez / (tr->PZ[0] + R);
                ex = detx[d] - tr->x2[0]; ez = detz[d] - tr->x2[2]; double d2 = ex * ex / (tr->P2X[0] + R) + ez * ez / (tr->P2Z[0] + R);
                double dm = d1 < d2 ? d1 : d2; if (dm <= bd) { bd = dm; best = i; bh = d1 <= d2 ? 1 : 2; d1best = d1; }
            }
            // la ricomparsa di A: misura prima dell'associazione
            if (dsrc[d] == 0 && kre < 0 && ep0 >= 0) {
                kre = k;
                if (ta && ta->was_hidden) {
                    long n = q->re_n; Disp *dd = &ta->d;
                    if (ta->perso || !dd->valid) q->re_perso++;
                    else { if (n < MAXP) { q->re_err[n] = dd->err; q->re_se[n] = dd->seff; q->re_tocc[n] = (k - ep0) * DT; }
                        q->re_in1 += dd->in1; q->re_in2 += dd->in2; q->re_in173 += dd->in173; q->re_hdr += dd->inhdr;
                        if (ta->has_prev) { q->re_p1 += ta->dprev.in1; q->re_p2 += ta->dprev.in2; q->re_phdr += ta->dprev.inhdr; q->re_sosta += ta->dprev.mu2 > 0.5; q->re_nucshown += ta->nuc_shown_prev; }
                        q->re_n++; }
                    double ex = detx[d] - ta->x[0], ez = detz[d] - ta->x[2], d1 = ex * ex / (ta->PX[0] + R) + ez * ez / (ta->PZ[0] + R);
                    q->re_kf95 += d1 <= 5.99;
                    if (best >= 0 && &T[best] == ta) q->re_gate++; else { q->gate_viol++; ghost = 1; ghost_k = k; }
                    int npend = 0; for (int i = 0; i < 8; i++) if (T[i].alive && T[i].status == 2) npend++;
                    double dw = dist_wedge(detx[d], detz[d], HW + MASKE), rr = hypot(detx[d], detz[d]), fovd = rr * sin(FOVH - fabs(atan2(detx[d], detz[d])));
                    if (npend == 1 && dw <= FASCIA && RMAX - rr > FASCIA && fovd > FASCIA) q->re_nucgeo++;
                } else if (ta == NULL || !ta->was_hidden) { if (A.seen) q->re_notrk++; }
            }
            if (dsrc[d] == 1 && bfirst < 0) { bfirst = (kre < 0); if (bfirst) q->b_first++; }
            if (best >= 0) {
                Track *tr = &T[best]; used[d] = 1;
                if (dsrc[d] != tr->src) { q->swap_mute++; }
                if (bh == 2) { memcpy(tr->x, tr->x2, sizeof tr->x); memcpy(tr->PX, tr->P2X, sizeof tr->PX); memcpy(tr->PZ, tr->P2Z, sizeof tr->PZ); }
                kf_upd(&tr->x[0], &tr->x[1], tr->PX, detx[d], R); kf_upd(&tr->x[2], &tr->x[3], tr->PZ, detz[d], R);
                tr->status = 1; tr->strato1 = 0; tr->src = dsrc[d]; if (dsrc[d] == 0) lastA = tr->id; tr->lmx = detx[d]; tr->lmz = detz[d]; tr->miss_open = 0; tr->hits++;
            }
            (void)d1best;
        }
        // tracce tentative: dopo le confermate e dopo quelle in occlusione
        for (int i = 0; i < 8; i++) if (T[i].alive && T[i].status == 0 && T[i].born != k) {
            Track *tr = &T[i]; int best = -1; double bd = GATE;
            for (int d = 0; d < nd; d++) if (!used[d]) { double ex = detx[d] - tr->x[0], ez = detz[d] - tr->x[2]; double d2 = ex * ex / (tr->PX[0] + R) + ez * ez / (tr->PZ[0] + R); if (d2 <= bd) { bd = d2; best = d; } }
            tr->age++;
            if (best >= 0) {
                used[best] = 1; kf_upd(&tr->x[0], &tr->x[1], tr->PX, detx[best], R); kf_upd(&tr->x[2], &tr->x[3], tr->PZ, detz[best], R);
                tr->lmx = detx[best]; tr->lmz = detz[best]; tr->hits++; tr->src = dsrc[best]; if (dsrc[best] == 0) lastA = tr->id;
                if (tr->hits >= 3) { tr->status = 1; tr->miss_open = 0; if (tr->src == 0 && idA < 0) idA = tr->id; }
            } else if (tr->age >= 5) tr->alive = 0;
        }
        // rilevamenti rimasti: tracce nuove
        for (int d = 0; d < nd; d++) if (!used[d]) {
            for (int i = 0; i < 8; i++) if (!T[i].alive) {
                Track *tr = &T[i]; memset(tr, 0, sizeof *tr); tr->alive = 1; tr->id = nextid++; tr->src = dsrc[d]; tr->status = 0; tr->hits = 1; tr->age = 0; tr->born = k; if (dsrc[d] == 0) lastA = tr->id;
                tr->x[0] = detx[d]; tr->x[2] = detz[d]; tr->PX[0] = tr->PZ[0] = R; tr->PX[2] = tr->PZ[2] = 9.0; tr->lmx = detx[d]; tr->lmz = detz[d];
                if (dsrc[d] == 0 && idA >= 0 && kre == k) q->a_split++;
                break;
            }
        }
        if (detA >= 0 && ep0 >= 0 && kre < 0) kre = k;
        if (TRACE && ip == TRACEP && ep0 >= 0 && kre >= 0 && k <= kre + 12) { printf("TT k %d A (%+.2f,%.2f) vis %d det %d:", k, A.x, A.z, A.vis, detA >= 0); for (int i = 0; i < 8; i++) if (T[i].alive) printf(" [id %d st %d x %+.2f v %+.2f z %.2f vz %+.2f sx %.3f kocc %d]", T[i].id, T[i].status, T[i].x[0], T[i].x[1], T[i].x[2], T[i].x[3], sqrt(T[i].PX[0]), T[i].kocc); printf("\n"); }
        if (A.done || k >= kcap) break;
    }
    // fine passaggio
    if (ep0 >= 0 && fr_occ > 0) { if (fr_est == fr_occ) q->pass_full++; if (fr_nuc == fr_occ) q->pass_nucfull++; }
    if (truelib_pass) q->pass_truelib++;
    if (kre >= 0 && idA >= 0) { q->fin_n++; if (lastA == idA) q->fin_same++; }
    if (TRACE && TRACEP < 0 && kre >= 0 && idA >= 0 && lastA != idA) printf("IDPERSA beh %d pass %d v %.2f kre %d ep0 %d\n", beh, ip, A.v, kre, ep0);
    if (pp_lost) q->pp_lost_pass++;
    if (ghost) { q->ghost_pass++; for (int i = 0; i < 8; i++) if (T[i].alive && T[i].status == 2 && T[i].src == 0 && !T[i].perso && T[i].d.valid) { q->ghost_end++; break; } }
    (void)ghost_k;
}

int main(int argc, char **argv) {
    int behsel = -1;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-panel")) PANEL = atoi(argv[++i]); else if (!strcmp(argv[i], "-pd")) PD = atof(argv[++i]);
        else if (!strcmp(argv[i], "-w")) WMODE = atoi(argv[++i]); else if (!strcmp(argv[i], "-l")) LMODE = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-n")) NMODE = atoi(argv[++i]); else if (!strcmp(argv[i], "-clamp")) CLAMP = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-np")) NPASS = atoi(argv[++i]); else if (!strcmp(argv[i], "-seed")) SEED = strtoull(argv[++i], 0, 10);
        else if (!strcmp(argv[i], "-mask")) MASKE = atof(argv[++i]); else if (!strcmp(argv[i], "-v")) VFIX = atof(argv[++i]);
        else if (!strcmp(argv[i], "-sig")) SIGM = atof(argv[++i]); else if (!strcmp(argv[i], "-q")) QQ = atof(argv[++i]);
        else if (!strcmp(argv[i], "-beh")) behsel = atoi(argv[++i]); else if (!strcmp(argv[i], "-falso")) FALSO = atoi(argv[++i]); else if (!strcmp(argv[i], "-trace")) { TRACE = 1; TRACEP = atoi(argv[++i]); } else if (!strcmp(argv[i], "-seffmax")) SEFFMAX = atof(argv[++i]);
        else { fprintf(stderr, "opzione ignota %s\n", argv[i]); return 2; }
    }
    if (NPASS > MAXP) NPASS = MAXP;
    if (PANEL == 2) { Zp = 2.2; HW = 1.0; ZA = 2.6; RMAX = 3.8; XS = 2.25; }
    build_static(st_true, HW); build_static(st_est, HW + MASKE);
    wedge_cells = 0; for (int c = 0; c < NC; c++) if (st_est[c] == OMB) { wedge_cells++; WCX += cxi(c % NX); WCZ += czj(c / NX); }
    WCX /= wedge_cells; WCZ /= wedge_cells;
    for (int b = 0; b < NBEH; b++) {
        for (int j = 0; j < NBIN; j++) { S[b].b_err[j] = malloc(sizeof(float) * MAXP); S[b].b_se[j] = malloc(sizeof(float) * MAXP); S[b].b_eh[j] = malloc(sizeof(float) * MAXP); S[b].b_ec[j] = malloc(sizeof(float) * MAXP); }
        S[b].tdom_fv = malloc(sizeof(float) * MAXP); S[b].tdom_ed = malloc(sizeof(float) * MAXP); S[b].tdom_abs = malloc(sizeof(float) * MAXP);
        S[b].re_err = malloc(sizeof(float) * MAXP); S[b].re_se = malloc(sizeof(float) * MAXP); S[b].re_tocc = malloc(sizeof(float) * MAXP);
    }
    printf("# banco_s3s4: pannello %d m (Zp %.2f, soggetto a Z %.2f, portata %.1f), Pd %.2f, sigma misura %.3f m, q %.2f, pesi W%d, alfa L%d, ammesse N%s, ritaglio %d, errore ombra %+.2f m, v %s, N %d, seme %llu\n",
           PANEL, Zp, ZA, RMAX, PD, SIGM, QQ, WMODE, LMODE, NMODE ? "b" : "a", CLAMP, MASKE, VFIX > 0 ? "fissa" : "U(0.3,1.8)", NPASS, (unsigned long long)SEED);
    if (FALSO) printf("# braccio falso libero: %d fotogrammi da 0,53 s\n", FALSO);
    printf("# cuneo: %d celle = %.2f m2; semilarghezza ombra sulla linea %.3f m\n", wedge_cells, wedge_cells * CS * CS, HW * ZA / Zp);
    for (int b = 0; b < NBEH; b++) { if (behsel >= 0 && b != behsel) continue; for (int p = 0; p < NPASS; p++) run_pass(b, p); }
    for (int b = 0; b < NBEH; b++) {
        if (behsel >= 0 && b != behsel) continue; Stat *q = &S[b]; double lo, hi;
        printf("\n== %s: passaggi %ld, traccia entrata in occlusione %ld (%.1f %%)\n", BNAME[b], q->npass, q->ntrk, P100(q->ntrk, q->npass));
        printf("(e) fotogrammi d'occlusione %ld: stima mostrata %.1f %%, «perso» %.1f %%, nessuna traccia %.1f %% | passaggi con stima per tutta l'occlusione %.1f %% | nucleo: area mostrata %.1f %% dei fotogrammi, tutta l'occlusione %.1f %% dei passaggi\n",
               q->fr_occ, P100(q->fr_est, q->fr_occ), P100(q->fr_perso, q->fr_occ), P100(q->fr_notrk, q->fr_occ), P100(q->pass_full, q->npass), P100(q->fr_nuc, q->fr_occ), P100(q->pass_nucfull, q->npass));
        printf("    passaggi a «perso»: per sigma_eff %ld, per massa nulla %ld, tempo medio %.2f s\n", q->perso_sig, q->perso_coll, (q->perso_sig + q->perso_coll) ? q->perso_t / (q->perso_sig + q->perso_coll) : NAN);
        printf("(a) fotogrammi con stima %ld: regione 95%% su celle «libero» stimate %ld, su celle davvero libere %ld (passaggi %ld); disco ±sigma_eff che tocca «libero» %.1f %% (da 1 s: %.1f %%), quota media del disco su «libero» %.1f %%; posizione mostrata su «libero» %ld; regione 95%% oltre meta' cuneo da 1 s: %.1f %%\n",
               q->fr_est, q->fr_estlib, q->fr_truelib, q->pass_truelib, P100(q->fr_disclib, q->fr_est), P100(q->fr_disclib15, q->fr_est15), q->fr_est ? 100 * q->disc_frac / q->fr_est : NAN, q->fr_meanlib, P100(q->fr_w50_15, q->fr_est15));
        printf("    massa grezza < 0,05 con stima mostrata: %.1f %% dei fotogrammi (oltre 2 s: %.1f %%, n %ld)\n", P100(q->fr_mlow, q->fr_est), P100(q->fr_mlow30, q->fr_e30), q->fr_e30);
        long nd = q->n_dom < MAXP ? q->n_dom : MAXP;
        printf("    sosta dominante in %ld passaggi su %ld con traccia; t assoluto mediano %.2f s; rispetto a «tutto visibile»: mediana %+.2f s (5%% %+.2f, 95%% %+.2f); rispetto al bordo dell'ombra: mediana %+.2f s\n",
               q->n_dom, q->ntrk, pct(q->tdom_abs, nd, 0.5), pct(q->tdom_fv, nd, 0.5), pct(q->tdom_fv, nd, 0.05), pct(q->tdom_fv, nd, 0.95), pct(q->tdom_ed, nd, 0.5));
        printf("(b) t_occ:   n   stima%% perso%% senza%% | err med  err p95 | sig_eff med | dentro 1sig  2sig  1,73sig  reg95 | reg95/cuneo  >meta'%% | M<0,05%% | nucleo: mostrata%% contiene%%\n");
        for (int j = 0; j < NBIN; j++) {
            long n = q->b_est[j] < MAXP ? q->b_est[j] : MAXP;
            printf("    %.1f s %5ld  %5.1f %5.1f %5.1f | %6.3f %7.3f | %6.3f | %5.1f %5.1f %5.1f %5.1f | %5.2f %5.1f | %5.1f | %5.1f %5.1f\n", BINK[j] * DT, q->b_tot[j], P100(q->b_est[j], q->b_tot[j]), P100(q->b_perso[j], q->b_tot[j]), P100(q->b_notrk[j], q->b_tot[j]),
                   pct(q->b_err[j], n, 0.5), pct(q->b_err[j], n, 0.95), pct(q->b_se[j], n, 0.5), P100(q->b_in1[j], q->b_est[j]), P100(q->b_in2[j], q->b_est[j]), P100(q->b_in173[j], q->b_est[j]), P100(q->b_hdr[j], q->b_est[j]),
                   q->b_est[j] ? q->b_wf[j] / q->b_est[j] : NAN, P100(q->b_w50[j], q->b_est[j]), P100(q->b_mlow[j], q->b_est[j]), P100(q->b_nuc[j], q->b_tot[j]), P100(q->b_nucc[j], q->b_nuc[j]));
            printf("        confronto %.1f s: errore mediano del solo filtro (H1, senza ritaglio) %.3f m; del punto fisso «centro del cuneo» %.3f m\n", BINK[j] * DT, pct(q->b_eh[j], n, 0.5), pct(q->b_ec[j], n, 0.5));
        }
        long n = q->re_n < MAXP ? q->re_n : MAXP;
        printf("(c) ricomparse con stima %ld (senza traccia %ld, gia' «perso» %ld); t_occ mediano %.2f s; errore mediano %.3f m (p95 %.3f), sigma_eff mediana %.3f m\n", q->re_n, q->re_notrk, q->re_perso, pct(q->re_tocc, n, 0.5), pct(q->re_err, n, 0.5), pct(q->re_err, n, 0.95), pct(q->re_se, n, 0.5));
        wilson(q->re_in1, q->re_n, &lo, &hi); printf("    al fotogramma della ricomparsa: dentro 1 sigma_eff %.1f %% [%.1f; %.1f]", P100(q->re_in1, q->re_n), 100 * lo, 100 * hi);
        wilson(q->re_in2, q->re_n, &lo, &hi); printf("; dentro 2 sigma_eff %.1f %% [%.1f; %.1f]", P100(q->re_in2, q->re_n), 100 * lo, 100 * hi);
        wilson(q->re_in173, q->re_n, &lo, &hi); printf("; dentro 1,73 sigma_eff %.1f %% [%.1f; %.1f]", P100(q->re_in173, q->re_n), 100 * lo, 100 * hi);
        wilson(q->re_hdr, q->re_n, &lo, &hi); printf("; dentro la regione al 95 %% %.1f %% [%.1f; %.1f]\n", P100(q->re_hdr, q->re_n), 100 * lo, 100 * hi);
        wilson(q->re_p2, q->re_n, &lo, &hi); printf("    al fotogramma prima (ultimo «previsto» mostrato): 1 sigma_eff %.1f %%; 2 sigma_eff %.1f %% [%.1f; %.1f]; regione al 95 %% %.1f %%; sosta dominante %.1f %%; area del nucleo ancora mostrata %.1f %%\n",
               P100(q->re_p1, q->re_n), P100(q->re_p2, q->re_n), 100 * lo, 100 * hi, P100(q->re_phdr, q->re_n), P100(q->re_sosta, q->re_n), P100(q->re_nucshown, q->re_n));
        long nre = q->re_n + q->re_perso;
        wilson(q->re_kf95, nre, &lo, &hi);
        printf("(d) porta: dentro (stessa identita') %ld su %ld (%.1f %%), violata %ld (%.1f %%); ellisse 95%% del solo filtro contiene la misura %.1f %% [%.1f; %.1f]; riaggancio geometrico del nucleo ammesso %.1f %%\n",
               q->re_gate, nre, P100(q->re_gate, nre), q->gate_viol, P100(q->gate_viol, nre), P100(q->re_kf95, nre), 100 * lo, 100 * hi, P100(q->re_nucgeo, nre));
        printf("    dopo porta violata: traccia vecchia ancora «previsto» a fine prova %ld su %ld; tracce nuove per A alla ricomparsa %ld; identita' di A a fine prova uguale a quella iniziale: %ld su %ld (%.1f %%)\n", q->ghost_end, q->ghost_pass, q->a_split, q->fin_same, q->fin_n, P100(q->fin_same, q->fin_n));
        if (b == 5) printf("    uno-due: il mai visto esce per primo in %ld passaggi; identita' passata a lui senza segnale %ld; possibile presenza caduta con A nascosto: %ld passaggi, %ld fotogrammi\n", q->b_first, q->swap_mute, q->pp_lost_pass, q->pp_lost_fr);
    }
    printf("\n# costo di calcolo della stima mostrata (ritaglio, pesi, momenti, regione al 95 %%): %ld chiamate, media %.1f microsecondi, massimo %.1f microsecondi (C, -O2, un nucleo; altri processi attivi)\n", tm_n, tm_n ? tm_sum / tm_n : NAN, tm_max);
    return 0;
}
