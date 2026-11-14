// sim3d.c — sciame-nuvole-punti, f7. Confronto fra il cuneo del nucleo (griglia polare 2D),
// le fasce di quota, il voxel 3D (DDA di Amanatides e Woo), l'interrogazione nello spazio
// dell'immagine e il "profilo" a due numeri per cella. Un fotogramma, sensore fermo.
// Compila: gcc -O2 -o sim3d sim3d.c -lm      Lancia: timeout 120 ./sim3d scene | sweep | rumore
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

#define W 848
#define H 480
#define PI 3.14159265358979323846
enum { SEEN = 0, HID = 1, OUTF = 2, SOL = 3 };
enum { FREE = 0, OCC = 1, SHD = 2, UNK = 3 };
enum { mT = 1, mE = 2, mG = 4, mH = 8 };
static const double HS = 1.2, RMAX = 3.0, ZTOP = 2.0, ZG = 0.07;
static double TX, TY, FX, FY, CP, SP; // tan dei semicampi, focali, cos e sin dell'inclinazione

typedef struct { double x0, x1, y0, y1, z0, z1; } Box;
typedef struct { double cx, cy, r, z0, z1; } Cyl;
static Box box[4]; static int nbox;
static Cyl cyl[4]; static int ncyl;
static int subj; // identificativo del solido "soggetto": 10+i cassa, 20+i cilindro, 0 nessuno

static float D[H][W], Dmin[H][W], Dmax[H][W];
static int ID[H][W];
static int noise = 0, trunc3 = 1, zona = 0;
static uint64_t rs = 20261114ULL;
static double urand(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
static double grand(void) { double u = urand() + 1e-300, v = urand(); return sqrt(-2 * log(u)) * cos(2 * PI * v); }
static double sig(double z) { return 0.00375 * z * z; }
static double marg(double z) { return noise ? (trunc3 ? 3 * sig(z) : 0.0) : 0.02; }
static double now(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e3 + t.tv_nsec * 1e-6; }

static void raydir(int u, int v, double *d) { // direzione nel mondo con profondita' unitaria lungo l'asse ottico
    double xc = (u + 0.5 - W / 2.0) / FX, yc = (v + 0.5 - H / 2.0) / FY;
    d[0] = xc; d[1] = CP - yc * SP; d[2] = -SP - yc * CP;
}
static void tocam(const double *p, double *c) {
    double y = p[1], z = p[2] - HS;
    c[0] = p[0]; c[1] = -SP * y - CP * z; c[2] = CP * y - SP * z;
}
static int infov(const double *p) {
    double c[3]; tocam(p, c);
    return c[2] > 1e-9 && fabs(c[0]) < TX * c[2] && fabs(c[1]) < TY * c[2];
}
static double hitbox(const Box *b, const double *o, const double *d) {
    double t0 = -1e30, t1 = 1e30, lo[3] = { b->x0, b->y0, b->z0 }, hi[3] = { b->x1, b->y1, b->z1 };
    for (int i = 0; i < 3; i++) {
        if (fabs(d[i]) < 1e-15) { if (o[i] < lo[i] || o[i] > hi[i]) return 1e30; continue; }
        double a = (lo[i] - o[i]) / d[i], c = (hi[i] - o[i]) / d[i];
        if (a > c) { double s = a; a = c; c = s; }
        if (a > t0) t0 = a;
        if (c < t1) t1 = c;
    }
    return (t0 <= t1 && t0 > 1e-9) ? t0 : 1e30;
}
static double hitcyl(const Cyl *c, const double *o, const double *d) {
    double best = 1e30, ox = o[0] - c->cx, oy = o[1] - c->cy;
    double A = d[0] * d[0] + d[1] * d[1], B = 2 * (ox * d[0] + oy * d[1]), C = ox * ox + oy * oy - c->r * c->r;
    if (A > 1e-15) {
        double q = B * B - 4 * A * C;
        if (q >= 0) {
            double t = (-B - sqrt(q)) / (2 * A), z = o[2] + t * d[2];
            if (t > 1e-9 && z >= c->z0 && z <= c->z1) best = t;
        }
    }
    if (fabs(d[2]) > 1e-15) {
        double zc[2] = { c->z0, c->z1 };
        for (int i = 0; i < 2; i++) {
            double t = (zc[i] - o[2]) / d[2], x = ox + t * d[0], y = oy + t * d[1];
            if (t > 1e-9 && t < best && x * x + y * y <= c->r * c->r) best = t;
        }
    }
    return best;
}
static double cast(const double *o, const double *d, int *id, int solidsonly) {
    double best = 1e30; int bid = 0;
    if (!solidsonly) {
        double t;
        if (d[2] < 0) { t = -o[2] / d[2]; if (t < best) { best = t; bid = 1; } }
        if (d[2] > 0) { t = (3.0 - o[2]) / d[2]; if (t < best) { best = t; bid = 2; } }
        if (d[1] > 0) { t = (4.5 - o[1]) / d[1]; if (t < best) { best = t; bid = 2; } }
        if (d[0] > 0) { t = (5.0 - o[0]) / d[0]; if (t < best) { best = t; bid = 2; } }
        if (d[0] < 0) { t = (-5.0 - o[0]) / d[0]; if (t < best) { best = t; bid = 2; } }
    }
    for (int i = 0; i < nbox; i++) { double t = hitbox(&box[i], o, d); if (t < best) { best = t; bid = 10 + i; } }
    for (int i = 0; i < ncyl; i++) { double t = hitcyl(&cyl[i], o, d); if (t < best) { best = t; bid = 20 + i; } }
    if (id) *id = bid;
    return best;
}
static int truth(const double *p, int *sid) {
    *sid = 0;
    for (int i = 0; i < nbox; i++)
        if (p[0] >= box[i].x0 && p[0] <= box[i].x1 && p[1] >= box[i].y0 && p[1] <= box[i].y1 && p[2] >= box[i].z0 && p[2] <= box[i].z1) { *sid = 10 + i; return SOL; }
    for (int i = 0; i < ncyl; i++) {
        double dx = p[0] - cyl[i].cx, dy = p[1] - cyl[i].cy;
        if (dx * dx + dy * dy <= cyl[i].r * cyl[i].r && p[2] >= cyl[i].z0 && p[2] <= cyl[i].z1) { *sid = 20 + i; return SOL; }
    }
    if (!infov(p)) return OUTF;
    double o[3] = { 0, 0, HS }, d[3] = { p[0], p[1], p[2] - HS };
    return cast(o, d, NULL, 1) < 1 - 1e-7 ? HID : SEEN;
}

static long subjpix;
static void render(void) {
    double o[3] = { 0, 0, HS }, d[3]; subjpix = 0;
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        raydir(u, v, d); int id; double t = cast(o, d, &id, 0);
        if (noise) t += grand() * sig(t);
        D[v][u] = (float)t; ID[v][u] = id; if (id == subj && subj) subjpix++;
    }
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        float a = 1e30f, b = -1e30f;
        for (int j = -1; j <= 1; j++) for (int i = -1; i <= 1; i++) {
            int vv = v + j, uu = u + i; if (vv < 0 || vv >= H || uu < 0 || uu >= W) continue;
            float x = D[vv][uu]; if (x < a) a = x; if (x > b) b = x;
        }
        Dmin[v][u] = a; Dmax[v][u] = b;
    }
}

// ---------- Q: interrogazione nello spazio dell'immagine, senza memoria ----------
static int qclass(const double *p) {
    double c[3]; tocam(p, c);
    if (c[2] <= 1e-9) return UNK;
    double uf = c[0] / c[2] * FX + W / 2.0, vf = c[1] / c[2] * FY + H / 2.0;
    int u = (int)floor(uf), v = (int)floor(vf);
    if (u < 1 || u > W - 2 || v < 1 || v > H - 2) return UNK;
    double m = marg(Dmin[v][u]);
    if (c[2] < Dmin[v][u] - m) return FREE;
    if (c[2] > Dmax[v][u] + marg(Dmax[v][u])) return SHD;
    return OCC; // superficie o bordo: ne' libero ne' nascosto
}

// ---------- N: griglia polare del nucleo ----------
#define NA 88
#define NR 30
static int gnd[NA][NR], obs[NA][NR];
static uint8_t NL[NA][NR], NG[NA][NR];
static int azbin(double x, double y) { int a = (int)floor(atan2(x, y) * 180 / PI + 44.0); return (a < 0 || a >= NA) ? -1 : a; }
static void buildN(void) {
    memset(gnd, 0, sizeof gnd); memset(obs, 0, sizeof obs);
    double d[3];
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        raydir(u, v, d); double t = D[v][u], x = t * d[0], y = t * d[1], z = HS + t * d[2], r = hypot(x, y);
        int a = azbin(x, y); if (a < 0 || r >= RMAX) continue;
        int ri = (int)(r / 0.1);
        if (z < ZG) gnd[a][ri]++; else if (z <= ZTOP) obs[a][ri]++;
    }
    for (int a = 0; a < NA; a++) {
        int r1 = NR;
        for (int ri = 0; ri < NR; ri++) if (obs[a][ri] >= 3) { r1 = ri; break; }
        for (int ri = 0; ri < NR; ri++) {
            int g = gnd[a][ri] >= 3, o = obs[a][ri] >= 3;
            NL[a][ri] = ri < r1 ? (g ? FREE : UNK) : ri == r1 ? OCC : SHD;
            NG[a][ri] = o ? OCC : g ? FREE : ri > r1 ? SHD : UNK;
        }
    }
}

// ---------- B: fasce di quota per cella polare ----------
static uint8_t Bm[2][NA][NR][8], Bc[2][NA][NR][8];
static const int BK[2] = { 4, 8 };
static uint8_t Bin[2][NA][NR][8]; static int Bin_ok = 0;
static void markband(int b, int a, int ri, double za, double zb, uint8_t m) {
    double lo = za < zb ? za : zb, hi = za < zb ? zb : za, hb = ZTOP / BK[b];
    if (hi < 0 || lo >= ZTOP) return;
    int k0 = (int)floor(lo / hb), k1 = (int)floor(hi / hb);
    if (k0 < 0) k0 = 0; if (k1 > BK[b] - 1) k1 = BK[b] - 1;
    for (int k = k0; k <= k1; k++) Bm[b][a][ri][k] |= m;
}
static long bsteps;
static void buildB(void) {
    memset(Bm, 0, sizeof Bm); bsteps = 0;
    if (!Bin_ok) {
        for (int b = 0; b < 2; b++) for (int a = 0; a < NA; a++) for (int ri = 0; ri < NR; ri++) for (int k = 0; k < BK[b]; k++) {
            int ok = 1; double hb = ZTOP / BK[b];
            for (int c = 0; c < 8 && ok; c++) {
                double az = (a - 44 + (c & 1)) * PI / 180, r = (ri + ((c >> 1) & 1)) * 0.1, z = (k + ((c >> 2) & 1)) * hb;
                double p[3] = { r * sin(az), r * cos(az), z }; ok = infov(p);
            }
            Bin[b][a][ri][k] = ok;
        }
        Bin_ok = 1;
    }
    double d[3];
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        raydir(u, v, d); int a = azbin(d[0], d[1]); if (a < 0) continue;
        double t = D[v][u], hr = hypot(d[0], d[1]), ze = HS + t * d[2], re = t * hr, n = sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2]);
        double m = marg(t) / n, tT = t - m, tH = t + m; int ground = ze < ZG;
        for (int ri = 0; ri < NR; ri++) {
            double tA = ri * 0.1 / hr, tB = (ri + 1) * 0.1 / hr; bsteps++;
            double e = tB < tT ? tB : tT;
            if (e > tA) for (int b = 0; b < 2; b++) markband(b, a, ri, HS + tA * d[2], HS + e * d[2], mT);
            double s = tA > tH ? tA : tH;
            if (!ground && tB > s) for (int b = 0; b < 2; b++) markband(b, a, ri, HS + s * d[2], HS + tB * d[2], mH);
        }
        if (re < RMAX && ze < ZTOP) {
            double zz = ze < 0 ? 0 : ze; int ri = (int)(re / 0.1);
            for (int b = 0; b < 2; b++) markband(b, a, ri, zz, zz, ground ? mG : mE);
        }
    }
    for (int b = 0; b < 2; b++) for (int a = 0; a < NA; a++) for (int ri = 0; ri < NR; ri++) for (int k = 0; k < BK[b]; k++) {
        uint8_t m = Bm[b][a][ri][k];
        Bc[b][a][ri][k] = (m & mE) ? OCC : (m & mH) ? SHD : ((m & (mT | mG)) && Bin[b][a][ri][k]) ? FREE : UNK;
    }
}

// ---------- V: voxel cartesiani, DDA di Amanatides e Woo ----------
typedef struct { double vs; int nx, ny, nz; uint8_t *m, *in; long steps; } Vox;
static Vox V[2];
static const double GX0 = -3, GY0 = 0, GZ0 = 0;
static void initV(Vox *g, double vs) {
    g->vs = vs; g->nx = (int)lround(6 / vs); g->ny = (int)lround(4 / vs); g->nz = (int)lround(3 / vs);
    long n = (long)g->nx * g->ny * g->nz; g->m = malloc(n); g->in = malloc(n);
    for (int k = 0; k < g->nz; k++) for (int j = 0; j < g->ny; j++) for (int i = 0; i < g->nx; i++) {
        int ok = 1;
        for (int c = 0; c < 8 && ok; c++) {
            double p[3] = { GX0 + (i + (c & 1)) * vs, GY0 + (j + ((c >> 1) & 1)) * vs, GZ0 + (k + ((c >> 2) & 1)) * vs }; ok = infov(p);
        }
        g->in[((long)k * g->ny + j) * g->nx + i] = ok;
    }
}
static void buildV(Vox *g) {
    long n = (long)g->nx * g->ny * g->nz; memset(g->m, 0, n); g->steps = 0;
    double d[3], o[3] = { (0 - GX0) / g->vs, (0 - GY0) / g->vs, (HS - GZ0) / g->vs };
    int dim[3] = { g->nx, g->ny, g->nz };
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        raydir(u, v, d);
        double t = D[v][u], nn = sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2]), m = marg(t) / nn, tT = t - m, tH = t + m;
        double ze = HS + t * d[2]; int ground = ze < ZG;
        int ix[3], st[3]; double tM[3], tD[3];
        for (int a = 0; a < 3; a++) {
            double da = d[a] / g->vs; ix[a] = (int)floor(o[a]); if (ix[a] >= dim[a]) ix[a] = dim[a] - 1;
            if (da > 1e-15) { st[a] = 1; tM[a] = (ix[a] + 1 - o[a]) / da; tD[a] = 1 / da; }
            else if (da < -1e-15) { st[a] = -1; tM[a] = (ix[a] - o[a]) / da; tD[a] = -1 / da; }
            else { st[a] = 0; tM[a] = 1e30; tD[a] = 1e30; }
        }
        double t0 = 0;
        for (;;) {
            int a = tM[0] < tM[1] ? (tM[0] < tM[2] ? 0 : 2) : (tM[1] < tM[2] ? 1 : 2);
            double t1 = tM[a]; g->steps++;
            if (t1 > t0 + 1e-12) {
                uint8_t *c = &g->m[((long)ix[2] * g->ny + ix[1]) * g->nx + ix[0]];
                if (t0 < tT) *c |= mT;
                if (!ground && t1 > tH) *c |= mH;
                if (zona && !ground && t1 > tT && t0 < tH) *c |= mE; // dopo le previsioni: la zona morta attorno al punto misurato non resta senza marca
            }
            if (ground && t1 >= tT) break;
            ix[a] += st[a]; if (ix[a] < 0 || ix[a] >= dim[a]) break;
            t0 = t1; tM[a] += tD[a];
        }
        double p[3] = { t * d[0], t * d[1], ze < 0 ? 0 : ze };
        int i = (int)floor((p[0] - GX0) / g->vs), j = (int)floor((p[1] - GY0) / g->vs), k = (int)floor((p[2] - GZ0) / g->vs);
        if (i >= 0 && i < g->nx && j >= 0 && j < g->ny && k >= 0 && k < g->nz) g->m[((long)k * g->ny + j) * g->nx + i] |= ground ? mG : mE;
    }
}
static int vclass(const Vox *g, const double *p, int cons) {
    int i = (int)floor((p[0] - GX0) / g->vs), j = (int)floor((p[1] - GY0) / g->vs), k = (int)floor((p[2] - GZ0) / g->vs);
    if (i < 0 || i >= g->nx || j < 0 || j >= g->ny || k < 0 || k >= g->nz) return UNK;
    long q = ((long)k * g->ny + j) * g->nx + i; uint8_t m = g->m[q];
    if (m & mE) return OCC;
    if (cons) return (m & mH) ? SHD : ((m & (mT | mG)) && g->in[q]) ? FREE : UNK;
    return (m & (mT | mG)) ? FREE : (m & mH) ? SHD : UNK;
}

// ---------- P: profilo, due numeri per cella polare ----------
#define NS 41
static float Plo[NA][NR], Phi[NA][NR]; // quota sotto cui non si vede; quota fino a cui si vede (Plo<0: nessun tratto libero)
static void buildP(void) {
    for (int a = 0; a < NA; a++) for (int ri = 0; ri < NR; ri++) {
        uint8_t s[5][NS];
        for (int c = 0; c < 5; c++) {
            double az = (a - 44 + (c == 4 ? 0.5 : (c & 1))) * PI / 180, r = (ri + (c == 4 ? 0.5 : ((c >> 1) & 1))) * 0.1;
            for (int j = 0; j < NS; j++) { double p[3] = { r * sin(az), r * cos(az), j * 0.05 }; s[c][j] = qclass(p); }
        }
        int lo = -1, hi = -1;
        for (int j = 0; j < NS - 1; j++) {
            int ok = 1;
            for (int c = 0; c < 5 && ok; c++) ok = s[c][j + 1] == FREE && (s[c][j] == FREE || (j == 0 && s[c][0] == OCC));
            if (ok) { if (lo < 0) lo = j; hi = j + 1; } else if (lo >= 0) break;
        }
        Plo[a][ri] = lo < 0 ? -1 : lo * 0.05f; Phi[a][ri] = lo < 0 ? -1 : hi * 0.05f;
    }
}

// ---------- valutazione ----------
#define NREP 10
static const char *RN[NREP] = { "N-L", "N-G", "B4", "B8", "V10-O", "V10-C", "V5-O", "V5-C", "Q", "P" };
static long cnt[NREP][4][4], subjN, subjD[NREP][4];
static double tms[8];
static const double LS = 0.025;
static void declare(const double *p, int *dc) {
    double r = hypot(p[0], p[1]); int a = azbin(p[0], p[1]), ri = (int)(r / 0.1); if (ri >= NR) ri = NR - 1; if (a < 0) a = 0;
    dc[0] = NL[a][ri]; dc[1] = NG[a][ri];
    dc[2] = Bc[0][a][ri][(int)(p[2] / 0.5)]; dc[3] = Bc[1][a][ri][(int)(p[2] / 0.25)];
    dc[4] = vclass(&V[1], p, 0); dc[5] = vclass(&V[1], p, 1); dc[6] = vclass(&V[0], p, 0); dc[7] = vclass(&V[0], p, 1);
    dc[8] = qclass(p);
    dc[9] = Plo[a][ri] < 0 ? UNK : p[2] < Plo[a][ri] ? SHD : p[2] < Phi[a][ri] ? FREE : UNK;
}
static void build_all(void) {
    double t = now(); render(); tms[0] = now() - t;
    t = now(); buildN(); tms[1] = now() - t;
    t = now(); buildB(); tms[2] = now() - t;
    t = now(); buildV(&V[1]); tms[3] = now() - t;
    t = now(); buildV(&V[0]); tms[4] = now() - t;
    t = now(); buildP(); tms[5] = now() - t;
    // aggiornamento proiettivo dei centri di V5 (solo tempo)
    t = now(); long f = 0; Vox *g = &V[0];
    for (int k = 0; k < g->nz; k++) for (int j = 0; j < g->ny; j++) for (int i = 0; i < g->nx; i++) {
        double p[3] = { GX0 + (i + 0.5) * g->vs, GY0 + (j + 0.5) * g->vs, GZ0 + (k + 0.5) * g->vs }; f += qclass(p) == FREE;
    }
    tms[6] = now() - t; tms[7] = (double)f;
}
static void evaluate(void) {
    memset(cnt, 0, sizeof cnt); memset(subjD, 0, sizeof subjD); subjN = 0;
    for (double z = LS / 2; z < ZTOP; z += LS) for (double y = LS / 2; y < RMAX; y += LS) for (double x = -2.2 + LS / 2; x < 2.2; x += LS) {
        double r = hypot(x, y); if (r > RMAX || fabs(atan2(x, y)) > 43.5 * PI / 180) continue;
        double p[3] = { x, y, z }; int sid, tr = truth(p, &sid), dc[NREP]; declare(p, dc);
        for (int k = 0; k < NREP; k++) cnt[k][tr][dc[k]]++;
        if (subj && sid == subj) { subjN++; for (int k = 0; k < NREP; k++) subjD[k][dc[k]]++; }
    }
}
static void report(const char *name) {
    double lv = LS * LS * LS * 1000; long tv[4] = { 0, 0, 0, 0 };
    for (int t = 0; t < 4; t++) for (int d = 0; d < 4; d++) tv[t] += cnt[0][t][d];
    long nonseen = tv[HID] + tv[OUTF] + tv[SOL];
    printf("\n## %s\n", name);
    printf("verita' (litri): visto %.0f | nascosto %.0f | fuori campo %.0f | solidi %.0f | totale %.0f ; pixel sul soggetto %ld ; punti del soggetto %ld\n",
           tv[SEEN] * lv, tv[HID] * lv, tv[OUTF] * lv, tv[SOL] * lv, (tv[0] + tv[1] + tv[2] + tv[3]) * lv, subjpix, subjN);
    printf("%-6s | %9s %7s (nasc/fuori/solido L) | %9s %8s %8s | %6s | %s\n", "rappr", "f.lib L", "%nonvis", "f.nasc L", "%dich.omb", "%visto", "resa%", "soggetto: %libero %occ %ombra %sconosc");
    for (int k = 0; k < NREP; k++) {
        long ff = cnt[k][HID][FREE] + cnt[k][OUTF][FREE] + cnt[k][SOL][FREE];
        long ds = cnt[k][SEEN][SHD] + cnt[k][HID][SHD] + cnt[k][OUTF][SHD] + cnt[k][SOL][SHD];
        printf("%-6s | %9.1f %6.2f%% (%.1f/%.1f/%.1f) | %9.1f %7.1f%% %7.2f%% | %5.1f%% |", RN[k], ff * lv, 100.0 * ff / (nonseen ? nonseen : 1),
               cnt[k][HID][FREE] * lv, cnt[k][OUTF][FREE] * lv, cnt[k][SOL][FREE] * lv,
               cnt[k][SEEN][SHD] * lv, ds ? 100.0 * cnt[k][SEEN][SHD] / ds : 0.0, 100.0 * cnt[k][SEEN][SHD] / tv[SEEN], 100.0 * cnt[k][SEEN][FREE] / tv[SEEN]);
        if (subjN) printf(" %6.2f %6.2f %6.2f %6.2f\n", 100.0 * subjD[k][FREE] / subjN, 100.0 * subjD[k][OCC] / subjN, 100.0 * subjD[k][SHD] / subjN, 100.0 * subjD[k][UNK] / subjN);
        else printf(" -\n");
    }
}
static void report_cost(void) {
    Vox *g = &V[0]; long n = (long)g->nx * g->ny * g->nz, teg = 0, honly = 0, any = 0;
    int bx = (g->nx + 7) / 8, by = (g->ny + 7) / 8, bz = (g->nz + 7) / 8; uint8_t *bl = calloc((long)bx * by * bz, 1);
    for (int k = 0; k < g->nz; k++) for (int j = 0; j < g->ny; j++) for (int i = 0; i < g->nx; i++) {
        uint8_t m = g->m[((long)k * g->ny + j) * g->nx + i]; if (!m) continue; any++;
        if (m & (mT | mE | mG)) { teg++; bl[((long)(k / 8) * by + j / 8) * bx + i / 8] |= 1; } else honly++;
        bl[((long)(k / 8) * by + j / 8) * bx + i / 8] |= 2;
    }
    long b1 = 0, b2 = 0; for (long q = 0; q < (long)bx * by * bz; q++) { b1 += bl[q] & 1; b2 += (bl[q] >> 1) & 1; }
    free(bl);
    printf("costo (un filo, ms): immagine sintetica %.1f | N %.1f | fasce B4+B8 %.1f (%ld visite) | DDA V10 %.1f (%ld passi) | DDA V5 %.1f (%ld passi) | profilo P %.1f | proiettivo sui %ld centri di V5 %.1f\n",
           tms[0], tms[1], tms[2], bsteps, tms[3], V[1].steps, tms[4], V[0].steps, tms[5], n, tms[6]);
    printf("V5 (6x4x3 m, %ld voxel): toccati %ld (%.1f%%), di cui attraversati/colpiti %ld e solo-ombra %ld ; blocchi 8^3: %d totali, %ld con attraversati/colpiti (%.1f%%), %ld contando anche l'ombra (%.1f%%)\n",
           n, any, 100.0 * any / n, teg, honly, bx * by * bz, b1, 100.0 * b1 / (bx * by * bz), b2, 100.0 * b2 / (bx * by * bz));
}
static int cellNL(double x, double y, int g) { int a = azbin(x, y), ri = (int)(hypot(x, y) / 0.1); return g ? NG[a][ri] : NL[a][ri]; }
static const char *CN[4] = { "libero", "occupato", "in ombra", "non osservato" };

static void scene(int s, double sx, double sy) {
    nbox = ncyl = 0; subj = 0;
    if (s == 1 || s == 2) { // S1: cassa alta 1 m; soggetto adulto (1) o accovacciato (2)
        box[nbox++] = (Box){ -0.4, 0.4, 1.5, 1.9, 0, 1.0 };
        cyl[ncyl++] = s == 1 ? (Cyl){ sx, sy, 0.22, 0, 1.7 } : (Cyl){ sx, sy, 0.25, 0, 0.8 }; subj = 20;
    } else if (s == 3) { // S2a: trave sospesa non vista
        box[nbox++] = (Box){ -1.0, 1.0, 1.5, 1.7, 1.7, 1.9 }; subj = 10;
    } else if (s == 4) { // S2b: trave vista, adulto dietro in pianta
        box[nbox++] = (Box){ -1.0, 1.0, 2.2, 2.4, 1.7, 1.9 };
        cyl[ncyl++] = (Cyl){ sx, sy, 0.22, 0, 1.7 }; subj = 20;
    } else if (s == 5) { // S3: pedana bassa, oggetto basso dietro
        box[nbox++] = (Box){ -0.4, 0.4, 1.3, 1.7, 0, 0.4 };
        cyl[ncyl++] = (Cyl){ sx, sy, 0.10, 0, 0.2 }; subj = 20;
    } else if (s == 6) { // S2c: trave sospesa non vista, soggetto = la trave, nessun altro
        box[nbox++] = (Box){ -1.0, 1.0, 1.0, 1.2, 1.7, 1.9 }; subj = 10;
    }
}

int main(int argc, char **argv) {
    const char *mode = argc > 1 ? argv[1] : "scene";
    TX = tan(43.5 * PI / 180); TY = tan(29 * PI / 180); FX = (W / 2.0) / TX; FY = (H / 2.0) / TY; CP = cos(15 * PI / 180); SP = sin(15 * PI / 180);
    initV(&V[0], 0.05); initV(&V[1], 0.10);
    if (argc > 2 && !strcmp(argv[2], "zona")) zona = 1;
    printf("# zona morta marcata=%d\n", zona);
    printf("# sim3d modo=%s seme=20261114 sensore 1,2 m, 15 gradi, 87x58 gradi, %dx%d ; reticolo di verita' %.3f m ; margine %s\n", mode, W, H, LS, "0,02 m (senza rumore) oppure 3 sigma / 0 (con rumore)");
    if (!strcmp(mode, "scene")) {
        struct { int s; double x, y; const char *n; } L[] = {
            { 1, 0.0, 2.4, "S1a cassa 1 m (1,5-1,9 m), adulto in piedi 1,7 m a (0; 2,4)" },
            { 2, 0.0, 2.4, "S1b cassa 1 m, soggetto accovacciato 0,8 m a (0; 2,4)" },
            { 3, 0, 0, "S2a trave 1,7-1,9 m di quota a 1,5-1,7 m (sopra il campo): soggetto = trave" },
            { 4, 0.0, 2.7, "S2b trave a 2,2-2,4 m (vista), adulto in piedi a (0; 2,7)" },
            { 5, 0.0, 1.9, "S3 pedana 0,4 m (1,3-1,7 m), oggetto alto 0,2 m a (0; 1,9)" } };
        for (int i = 0; i < 5; i++) {
            scene(L[i].s, L[i].x, L[i].y); build_all(); evaluate(); report(L[i].n);
            if (L[i].s != 3 && L[i].s != 6) printf("cella del centro del soggetto: N-L = %s ; N-G = %s\n", CN[cellNL(L[i].x, L[i].y, 0)], CN[cellNL(L[i].x, L[i].y, 1)]);
            if (i == 0 || i == 4) report_cost();
        }
    } else if (!strcmp(mode, "sweep")) {
        for (int pass = 0; pass < 2; pass++) {
            int s = pass ? 5 : 2; double mx[NREP] = { 0 }, mxh[NREP] = { 0 }; int nh = 0, np = 0;
            printf("\n## sweep %s: %% del corpo del soggetto in regione dichiarata libera, per posizione\n", pass ? "S3 (pedana 0,4 m, oggetto 0,2 m)" : "S1 (cassa 1 m, accovacciato 0,8 m)");
            printf("%6s %6s %7s |", "x", "y", "pixel"); for (int k = 0; k < NREP; k++) printf(" %6s", RN[k]); printf("\n");
            double xs1[] = { -0.45, -0.3, -0.15, 0, 0.15, 0.3, 0.45 }, ys1[] = { 2.2, 2.45, 2.7 };
            double xs3[] = { -0.2, 0, 0.2 }, ys3[] = { 1.85, 1.95, 2.1, 2.3, 2.6 };
            int nx = pass ? 3 : 7, ny = pass ? 5 : 3;
            for (int j = 0; j < ny; j++) for (int i = 0; i < nx; i++) {
                double x = pass ? xs3[i] : xs1[i], y = pass ? ys3[j] : ys1[j];
                scene(s, x, y); build_all(); evaluate(); np++; if (!subjpix) nh++;
                printf("%6.2f %6.2f %7ld |", x, y, subjpix);
                for (int k = 0; k < NREP; k++) {
                    double f = 100.0 * subjD[k][FREE] / subjN; printf(" %6.2f", f);
                    if (f > mx[k]) mx[k] = f; if (!subjpix && f > mxh[k]) mxh[k] = f;
                }
                printf("\n");
            }
            printf("posizioni %d, del tutto nascoste (0 pixel) %d\nmassimo, tutte      :", np, nh); for (int k = 0; k < NREP; k++) printf(" %s %.2f", RN[k], mx[k]);
            printf("\nmassimo, nascoste   :"); for (int k = 0; k < NREP; k++) printf(" %s %.2f", RN[k], mxh[k]); printf("\n");
        }
    } else if (!strcmp(mode, "rumore")) {
        noise = 1;
        for (trunc3 = 0; trunc3 <= 1; trunc3++) {
            rs = 20261114ULL; scene(2, 0.0, 2.4); build_all(); evaluate();
            report(trunc3 ? "S1b con rumore nominale, scavo troncato a 3 sigma" : "S1b con rumore nominale, scavo fino al punto misurato (nessun margine)");
            rs = 20261114ULL; scene(1, 0.0, 2.4); build_all(); evaluate();
            report(trunc3 ? "S1a con rumore nominale, scavo troncato a 3 sigma" : "S1a con rumore nominale, scavo fino al punto misurato (nessun margine)");
        }
    }
    return 0;
}
