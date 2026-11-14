/* banco.c — banco di prova delle strutture dati per la mappa voxel (sciame-ottimizzazione, f7).
 * Compilare: gcc -O2 -o banco banco.c -lm
 * Uso: ./banco STRUTTURA RIS_CM SCENA W H FOTOGRAMMI [ombra=0|1] [arena=0|1] [tetto_blocchi]
 *   STRUTTURA: nulla | densa | densafix | hash | hashnc | octree | csr | pol3 | pol6 | ibr3 | ibr6
 *   SCENA: rada | densa
 * Regione 6 x 4 x 3 m, sensore fermo in (0, 2, 1.2) inclinato di 15 gradi in basso, campo 87 x 58 gradi.
 * Semi fissi. Un thread. Il tempo di generazione della profondita' e' escluso dalle misure.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <sys/resource.h>

typedef struct { int16_t L; uint8_t q; uint8_t nu; uint32_t tau; } Voxel; /* 8 byte: (L, q, nu, tau) */

static double now_ms(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec * 1e3 + ts.tv_nsec * 1e-6; }

/* ---------- generatore ---------- */
static uint64_t rs;
static inline uint64_t rnd(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 2685821657736338717ULL; }
static inline double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static double grand(void) { double u = urand() + 1e-300, v = urand(); return sqrt(-2 * log(u)) * cos(6.283185307179586 * v); }

/* ---------- geometria ---------- */
static const double SO[3] = { 0.001, 2.001, 1.201 }; /* sensore, coordinate della regione */
static int NX, NY, NZ; static double VS, IVS;
static int W, H, NR;
static float *dirs; static double *texit;
/* per le griglie polari */
#define NAZ 120
static int16_t *r_az; static float *r_cg, *r_sl;

typedef struct { double lo[3], hi[3]; double vy; } Box;
static Box sbox[64]; static int nsb; static Box mbox[16]; static int nmb;
static float *tstat;

static inline double ray_box(const float *d, const Box *b) {
    double t0 = 0, t1 = 1e30;
    for (int k = 0; k < 3; k++) {
        if (fabs(d[k]) < 1e-12) { if (SO[k] < b->lo[k] || SO[k] > b->hi[k]) return -1; }
        else { double inv = 1.0 / d[k], a = (b->lo[k] - SO[k]) * inv, c = (b->hi[k] - SO[k]) * inv;
               if (a > c) { double x = a; a = c; c = x; } if (a > t0) t0 = a; if (c < t1) t1 = c; if (t0 > t1) return -1; }
    }
    return t0 > 0 ? t0 : -1;
}
static void addbox(double x0, double y0, double z0, double x1, double y1, double z1) {
    Box *b = &sbox[nsb++]; b->lo[0] = x0; b->lo[1] = y0; b->lo[2] = z0; b->hi[0] = x1; b->hi[1] = y1; b->hi[2] = z1; b->vy = 0;
}
static void addmov(double x, double y, double vy) {
    Box *b = &mbox[nmb++]; b->lo[0] = x; b->hi[0] = x + 0.5; b->lo[1] = y; b->hi[1] = y + 0.5; b->lo[2] = 0; b->hi[2] = 1.75; b->vy = vy;
}
static void build_scene(int dense) {
    nsb = nmb = 0;
    addbox(-100, -100, -1, 100, 100, 0);       /* suolo */
    addbox(5.95, -100, 0, 6.2, 100, 10);       /* parete di fondo */
    if (!dense) { addmov(2.3, 0.5, 1.0); addmov(4.0, 3.0, -0.7); return; }
    addbox(-1, -1, 0, 100, 0.05, 10); addbox(-1, 3.95, 0, 100, 5, 10); /* pareti laterali */
    uint64_t keep = rs; rs = 0x9E3779B97F4A7C15ULL;
    for (int i = 0; i < 8; i++) { double x = 1.5 + 4 * urand(), y = 0.2 + 3.2 * urand(), s = 0.3 + 0.3 * urand(); addbox(x, y, 0, x + s, y + s, 0.15 + 0.35 * urand()); } /* bassi */
    for (int i = 0; i < 6; i++) { double x = 1.8 + 3.7 * urand(), y = 0.2 + 3.0 * urand(), s = 0.3 + 0.5 * urand(); addbox(x, y, 0, x + s, y + s, 1.5 + 1.0 * urand()); } /* pilastri e scaffali */
    for (int i = 0; i < 4; i++) { double x = 1.5 + 4 * urand(), y = 2.5 * urand(), l = 1.5 + 2.0 * urand(); if (y + l > 3.9) l = 3.9 - y; addbox(x, y, 1.8, x + 0.2, y + l, 2.1); } /* travi alla quota della testa */
    for (int i = 0; i < 5; i++) { double x = 1.5 + 4 * urand(), y = 0.2 + 3.0 * urand(); addbox(x, y, 0.70, x + 0.8, y + 0.6, 0.78); } /* piani sospesi */
    addbox(2.0, 1.5, 0, 2.05, 2.5, 1.8); /* pannello largo 1 m a 2 m */
    rs = keep;
    addmov(1.8, 0.4, 1.2); addmov(2.3, 3.0, -1.0); addmov(3.0, 1.0, 0.8); addmov(3.5, 2.5, -1.5); addmov(4.2, 0.6, 0.5); addmov(5.0, 3.2, -0.9);
}
static void build_rays(void) {
    NR = W * H; dirs = malloc(sizeof(float) * 3 * NR); texit = malloc(sizeof(double) * NR); tstat = malloc(sizeof(float) * NR);
    r_az = malloc(sizeof(int16_t) * NR); r_cg = malloc(sizeof(float) * NR); r_sl = malloc(sizeof(float) * NR);
    double th = tan(87.0 * M_PI / 360), tv = tan(58.0 * M_PI / 360), p = 15.0 * M_PI / 180, cp = cos(p), sp = sin(p);
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        double x = 1, y = -th * (2 * (u + 0.5) / W - 1), z = -tv * (2 * (v + 0.5) / H - 1);
        double xr = x * cp + z * sp, zr = -x * sp + z * cp, n = sqrt(xr * xr + y * y + zr * zr);
        int r = v * W + u; float *d = &dirs[3 * r]; d[0] = xr / n; d[1] = y / n; d[2] = zr / n;
        double roi[3] = { 6.0, 4.0, 3.0 }, te = 1e30;
        for (int k = 0; k < 3; k++) { if (d[k] > 0) { double t = (roi[k] - SO[k]) / d[k]; if (t < te) te = t; } else if (d[k] < 0) { double t = (0 - SO[k]) / d[k]; if (t < te) te = t; } }
        texit[r] = te - 1e-7;
        double az = atan2(d[1], d[0]) * 180 / M_PI; int a = (int)floor(az + 60.0); r_az[r] = (a < 0 || a >= NAZ) ? -1 : a;
        double cg = sqrt((double)d[0] * d[0] + (double)d[1] * d[1]); r_cg[r] = cg; r_sl[r] = d[2] / cg;
        double t = 1e30; for (int i = 0; i < nsb; i++) { double tt = ray_box(d, &sbox[i]); if (tt > 0 && tt < t) t = tt; } tstat[r] = t;
    }
}
static void gen_depth(float *depth) {
    for (int i = 0; i < nmb; i++) { Box *b = &mbox[i]; double y = b->lo[1] + b->vy / 15.0; if (y < 0.2 || y > 3.3) { b->vy = -b->vy; y = b->lo[1] + b->vy / 15.0; } b->lo[1] = y; b->hi[1] = y + 0.5; }
    for (int r = 0; r < NR; r++) {
        double t = tstat[r]; const float *d = &dirs[3 * r];
        for (int i = 0; i < nmb; i++) { double tt = ray_box(d, &mbox[i]); if (tt > 0 && tt < t) t = tt; }
        double g = grand(), dr = urand();
        t += g * 0.00375 * t * t;
        depth[r] = (t > 8.0 || t < 0.2 || dr < 0.02) ? 0.0f : (float)t;
    }
}

/* ---------- A: densa ---------- */
static Voxel *dense; int g_rox = 0, g_roy = 0, g_roz = 0;
static inline Voxel *dget_ring(int ix, int iy, int iz) {
    int a = ix + g_rox; if (a >= NX) a -= NX; int b = iy + g_roy; if (b >= NY) b -= NY; int c = iz + g_roz; if (c >= NZ) c -= NZ;
    return &dense[((size_t)a * NY + b) * NZ + c];
}
static inline Voxel *dget_fix(int ix, int iy, int iz) { return &dense[((size_t)ix * NY + iy) * NZ + iz]; }

/* ---------- B: hash di blocchi 8x8x8 ---------- */
typedef struct { uint32_t key, idx; } HEnt;
static HEnt *htab; static uint32_t hcap, hmask; static int hshift;
static Voxel **hblk; static uint32_t nblk, nlive, blkcap; static Voxel *harena;
static uint32_t h_lastkey, hc_lastkey; static Voxel *h_lastblk; static const Voxel *hc_lastblk;
static int g_nocache, g_arena; static uint64_t ndrop;
static inline uint32_t hhome(uint32_t key) { return (key * 2654435761u) >> hshift; }
static Voxel *h_find(uint32_t key) {
    uint32_t i = hhome(key);
    for (;;) { HEnt e = htab[i]; if (e.key == key) return hblk[e.idx]; if (!e.key) return NULL; i = (i + 1) & hmask; }
}
static Voxel *h_find_or_alloc(uint32_t key) {
    uint32_t i = hhome(key);
    for (;;) {
        HEnt e = htab[i]; if (e.key == key) return hblk[e.idx];
        if (!e.key) {
            if (nlive >= blkcap) return NULL;
            Voxel *b; if (g_arena) { b = harena + (size_t)nblk * 512; memset(b, 0, 512 * sizeof(Voxel)); } else b = calloc(512, sizeof(Voxel));
            hblk[nblk] = b; htab[i].key = key; htab[i].idx = nblk; nblk++; nlive++; return b;
        }
        i = (i + 1) & hmask;
    }
}
static void h_delete(uint32_t key) {
    uint32_t i = hhome(key);
    for (;;) { if (htab[i].key == key) break; if (!htab[i].key) return; i = (i + 1) & hmask; }
    if (!g_arena) free(hblk[htab[i].idx]);
    hblk[htab[i].idx] = NULL; nlive--; h_lastkey = 0; hc_lastkey = 0;
    uint32_t j = i;
    for (;;) {
        j = (j + 1) & hmask; if (!htab[j].key) break;
        uint32_t k = hhome(htab[j].key);
        if ((i <= j) ? (i < k && k <= j) : (i < k || k <= j)) continue;
        htab[i] = htab[j]; i = j;
    }
    htab[i].key = 0;
}
static inline uint32_t hkey(int ix, int iy, int iz) { return (uint32_t)((ix >> 3) | ((iy >> 3) << 10) | ((iz >> 3) << 20)) + 1u; }
static inline Voxel *hget(int ix, int iy, int iz) {
    uint32_t key = hkey(ix, iy, iz); Voxel *b;
    if (!g_nocache && key == h_lastkey) b = h_lastblk;
    else { b = h_find_or_alloc(key); if (!b) return NULL; h_lastkey = key; h_lastblk = b; }
    return &b[((ix & 7) << 6) | ((iy & 7) << 3) | (iz & 7)];
}
static inline const Voxel *hcget(int ix, int iy, int iz) {
    uint32_t key = hkey(ix, iy, iz); const Voxel *b;
    if (!g_nocache && key == hc_lastkey) b = hc_lastblk; else { b = h_find(key); hc_lastkey = key; hc_lastblk = b; }
    return b ? &b[((ix & 7) << 6) | ((iy & 7) << 3) | (iz & 7)] : NULL;
}

/* ---------- C: octree a indici, senza potatura; foglie = mattoni 2x2x2 ---------- */
static uint32_t (*onode)[8]; static uint32_t nnode, capnode; static Voxel (*obrick)[8]; static uint32_t nbrick, capbrick; static int OD;
static inline Voxel *oget(int ix, int iy, int iz) {
    uint32_t n = 0;
    for (int lv = OD - 1;; lv--) {
        int c = (((ix >> lv) & 1) << 2) | (((iy >> lv) & 1) << 1) | ((iz >> lv) & 1);
        uint32_t ch = onode[n][c];
        if (lv == 1) {
            if (!ch) { if (nbrick == capbrick) { capbrick *= 2; obrick = realloc(obrick, (size_t)capbrick * sizeof(*obrick)); }
                       memset(obrick[nbrick], 0, sizeof(*obrick)); ch = ++nbrick; onode[n][c] = ch; }
            return &obrick[ch - 1][((ix & 1) << 2) | ((iy & 1) << 1) | (iz & 1)];
        }
        if (!ch) { if (nnode == capnode) { capnode *= 2; onode = realloc(onode, (size_t)capnode * sizeof(*onode)); }
                   memset(onode[nnode], 0, sizeof(*onode)); ch = nnode++; onode[n][c] = ch; }
        n = ch;
    }
}
static inline const Voxel *ocget(int ix, int iy, int iz) {
    uint32_t n = 0;
    for (int lv = OD - 1;; lv--) {
        int c = (((ix >> lv) & 1) << 2) | (((iy >> lv) & 1) << 1) | ((iz >> lv) & 1);
        uint32_t ch = onode[n][c]; if (!ch) return NULL;
        if (lv == 1) return &obrick[ch - 1][((ix & 1) << 2) | ((iy & 1) << 1) | (iz & 1)];
        n = ch;
    }
}

/* ---------- F: vettore ordinato (chiave lineare), tipo CSR/COO ordinato ---------- */
static uint32_t *skey; static Voxel *sval; static uint32_t sn;
static inline uint32_t s_lb(uint32_t key) { uint32_t lo = 0, hi = sn; while (lo < hi) { uint32_t m = (lo + hi) >> 1; if (skey[m] < key) lo = m + 1; else hi = m; } return lo; }
static inline Voxel *sget(int ix, int iy, int iz) {
    uint32_t key = ((uint32_t)ix * NY + iy) * NZ + iz, i = s_lb(key);
    if (i < sn && skey[i] == key) return &sval[i];
    memmove(&skey[i + 1], &skey[i], (size_t)(sn - i) * 4); memmove(&sval[i + 1], &sval[i], (size_t)(sn - i) * sizeof(Voxel));
    skey[i] = key; memset(&sval[i], 0, sizeof(Voxel)); sn++; return &sval[i];
}
static inline const Voxel *scget(int ix, int iy, int iz) {
    uint32_t key = ((uint32_t)ix * NY + iy) * NZ + iz, i = s_lb(key); return (i < sn && skey[i] == key) ? &sval[i] : NULL;
}

/* ---------- lancio dei raggi (Amanatides-Woo), uguale per A, B, C, F ---------- */
static int g_shadow;
#define MISS(v) do { int l_ = (v)->L - 40; (v)->L = l_ < -200 ? -200 : l_; (v)->tau = frame; (v)->nu = 1; } while (0)
#define DEF_INTEGRATE(NAME, GET) \
static uint64_t NAME(const float *depth, uint32_t frame) { \
    uint64_t steps = 0; const double ox = SO[0], oy = SO[1], oz = SO[2]; \
    const int ix0 = (int)(ox * IVS), iy0 = (int)(oy * IVS), iz0 = (int)(oz * IVS); \
    for (int r = 0; r < NR; r++) { \
        double t = depth[r]; if (t <= 0) continue; \
        const float *d = &dirs[3 * r]; double tex = texit[r]; int hit = t < tex; double tend = hit ? t : tex; \
        int ix = ix0, iy = iy0, iz = iz0; \
        int sx = d[0] > 0 ? 1 : -1, sy = d[1] > 0 ? 1 : -1, sz = d[2] > 0 ? 1 : -1; \
        double tdx = d[0] != 0 ? VS / fabs(d[0]) : 1e30, tdy = d[1] != 0 ? VS / fabs(d[1]) : 1e30, tdz = d[2] != 0 ? VS / fabs(d[2]) : 1e30; \
        double tmx = d[0] > 0 ? ((ix + 1) * VS - ox) / d[0] : d[0] < 0 ? (ix * VS - ox) / d[0] : 1e30; \
        double tmy = d[1] > 0 ? ((iy + 1) * VS - oy) / d[1] : d[1] < 0 ? (iy * VS - oy) / d[1] : 1e30; \
        double tmz = d[2] > 0 ? ((iz + 1) * VS - oz) / d[2] : d[2] < 0 ? (iz * VS - oz) / d[2] : 1e30; \
        int ok = 1; \
        for (;;) { \
            double tn = tmx < tmy ? (tmx < tmz ? tmx : tmz) : (tmy < tmz ? tmy : tmz); \
            if (tn >= tend) break; \
            Voxel *v = GET(ix, iy, iz); steps++; if (v) MISS(v); else ndrop++; \
            if (tmx <= tmy && tmx <= tmz) { ix += sx; tmx += tdx; if ((unsigned)ix >= (unsigned)NX) { ok = 0; break; } } \
            else if (tmy <= tmz) { iy += sy; tmy += tdy; if ((unsigned)iy >= (unsigned)NY) { ok = 0; break; } } \
            else { iz += sz; tmz += tdz; if ((unsigned)iz >= (unsigned)NZ) { ok = 0; break; } } \
        } \
        if (!ok) continue; \
        { Voxel *v = GET(ix, iy, iz); steps++; \
          if (!v) ndrop++; else if (hit) { int l_ = v->L + 85; v->L = l_ > 350 ? 350 : l_; v->tau = frame; v->nu = 1; v->q = 1; } else MISS(v); } \
        if (hit && g_shadow) for (;;) { \
            if (tmx <= tmy && tmx <= tmz) { ix += sx; tmx += tdx; if ((unsigned)ix >= (unsigned)NX) break; } \
            else if (tmy <= tmz) { iy += sy; tmy += tdy; if ((unsigned)iy >= (unsigned)NY) break; } \
            else { iz += sz; tmz += tdz; if ((unsigned)iz >= (unsigned)NZ) break; } \
            Voxel *v = GET(ix, iy, iz); steps++; if (v) { if (v->tau != frame) v->nu = 2; } else ndrop++; \
        } \
    } \
    return steps; \
}
DEF_INTEGRATE(integ_dring, dget_ring)
DEF_INTEGRATE(integ_dfix, dget_fix)
DEF_INTEGRATE(integ_hash, hget)
DEF_INTEGRATE(integ_oct, oget)
DEF_INTEGRATE(integ_csr, sget)

/* ---------- interrogazione per settori ---------- */
#define NSEC 9
#define NRB 64
#define F_OCC 1
#define F_UNK 2
#define F_FREE 4
typedef struct { float near_occ; int nfree, nunk, nocc; } SecOut;
static int8_t *lut_sec; static uint8_t *lut_rb; static int ZB0, ZB1;
static void build_lut(void) {
    lut_sec = malloc((size_t)NX * NY); lut_rb = malloc((size_t)NX * NY);
    for (int ix = 0; ix < NX; ix++) for (int iy = 0; iy < NY; iy++) {
        double x = (ix + 0.5) * VS - SO[0], y = (iy + 0.5) * VS - SO[1], az = atan2(y, x) * 180 / M_PI;
        int s = (int)floor((az + 43.5) / 87.0 * NSEC); if (az < -43.5 || s < 0 || s >= NSEC) s = -1;
        int rb = (int)(sqrt(x * x + y * y) * 10); if (rb > NRB - 1) rb = NRB - 1;
        lut_sec[ix * NY + iy] = s; lut_rb[ix * NY + iy] = rb;
    }
    ZB0 = (int)ceil(0.10 * IVS - 1e-9); ZB1 = (int)floor(2.0 * IVS + 1e-9) - 1;
}
static void finalize(uint8_t fl[NSEC][NRB], SecOut *out) {
    for (int s = 0; s < NSEC; s++) {
        SecOut o = { -1, 0, 0, 0 };
        for (int rb = 0; rb < NRB; rb++) { uint8_t f = fl[s][rb]; if (!f) continue;
            if (f & F_OCC) { o.nocc++; if (o.near_occ < 0) o.near_occ = rb * 0.1f; } else if (f & F_UNK) o.nunk++; else o.nfree++; }
        out[s] = o;
    }
}
#define DEF_QUERY(NAME, CGET) \
static void NAME(uint32_t frame, SecOut *out) { \
    uint8_t fl[NSEC][NRB]; memset(fl, 0, sizeof fl); \
    for (int ix = 0; ix < NX; ix++) for (int iy = 0; iy < NY; iy++) { \
        int s = lut_sec[ix * NY + iy]; if (s < 0) continue; uint8_t f = 0; \
        for (int iz = ZB0; iz <= ZB1; iz++) { const Voxel *v = CGET(ix, iy, iz); \
            if (!v || v->tau == 0) f |= F_UNK; else if (v->L > 0) f |= F_OCC; else if (v->tau + 2 >= frame) f |= F_FREE; else f |= F_UNK; } \
        fl[s][lut_rb[ix * NY + iy]] |= f; \
    } \
    finalize(fl, out); \
}
DEF_QUERY(query_dring, dget_ring)
DEF_QUERY(query_dfix, dget_fix)
DEF_QUERY(query_hash, hcget)
DEF_QUERY(query_oct, ocget)
DEF_QUERY(query_csr, scget)

/* ---------- E: griglia polare sul piano del nucleo (1 grado x 0,1 m, quattro stati) ---------- */
enum { S_UNOBS = 0, S_FREE = 1, S_OCC = 2, S_SHADOW = 3 };
typedef struct { uint8_t state, hist, age, pad; } PCell;
static PCell *pcell; static uint8_t *p_obst, *p_gnd; static int NRAD; static double RMAX;
static int8_t az_sec[NAZ];
static uint64_t integ_pol(const float *depth, uint32_t frame) {
    (void)frame; memset(p_obst, 0, (size_t)NAZ * NRAD); memset(p_gnd, 0, (size_t)NAZ * NRAD);
    for (int r = 0; r < NR; r++) {
        float t = depth[r]; if (t <= 0) continue; int a = r_az[r]; if (a < 0) continue;
        float g = t * r_cg[r]; int j = (int)(g * 10.0f); if (j >= NRAD) continue;
        float z = (float)SO[2] + g * r_sl[r];
        if (z >= 0.07f) { if (z <= 2.0f) p_obst[a * NRAD + j] = 1; } else p_gnd[a * NRAD + j] = 1;
    }
    for (int a = 0; a < NAZ; a++) {
        PCell *c = &pcell[a * NRAD]; const uint8_t *ob = &p_obst[a * NRAD], *gn = &p_gnd[a * NRAD]; int j = 0;
        for (; j < NRAD && !ob[j]; j++) { c[j].hist = ((c[j].hist << 1) | gn[j]) & 7; c[j].state = c[j].hist ? S_FREE : S_UNOBS; c[j].age = gn[j] ? 0 : (c[j].age < 255 ? c[j].age + 1 : 255); }
        if (j < NRAD) { c[j].state = S_OCC; c[j].hist = 0; c[j].age = 0; j++; }
        for (; j < NRAD; j++) { c[j].state = S_SHADOW; c[j].hist = 0; if (c[j].age < 255) c[j].age++; }
    }
    return (uint64_t)NR + NAZ * NRAD;
}
static void query_pol(uint32_t frame, SecOut *out) {
    (void)frame; uint8_t fl[NSEC][NRB]; memset(fl, 0, sizeof fl);
    for (int a = 0; a < NAZ; a++) { int s = az_sec[a]; if (s < 0) continue; const PCell *c = &pcell[a * NRAD];
        for (int j = 0; j < NRAD; j++) fl[s][j] |= c[j].state == S_FREE ? F_FREE : c[j].state == S_OCC ? F_OCC : F_UNK; }
    finalize(fl, out);
}

/* ---------- D: polare sul piano + colonna di bit di quota per cella ---------- */
typedef struct { uint64_t fr[3], occ_now, occ_mem; uint32_t tau, pad; } HCell; /* 48 byte */
static HCell *hcell; static int NZL; static double ZR;
static inline uint64_t bitrange(int lo, int hi) { /* bit lo..hi, gia' ritagliati in 0..63 */
    uint64_t m = hi >= 63 ? ~0ULL : ((1ULL << (hi + 1)) - 1); return m & ~((1ULL << lo) - 1);
}
static uint64_t integ_ibr(const float *depth, uint32_t frame) {
    uint64_t steps = 0; int k = frame % 3; const float oz = (float)SO[2], izr = (float)(1.0 / ZR);
    for (int i = 0; i < NAZ * NRAD; i++) { hcell[i].fr[k] = 0; hcell[i].occ_now = 0; }
    for (int r = 0; r < NR; r++) {
        float t = depth[r]; if (t <= 0) continue; int a = r_az[r]; if (a < 0) continue;
        float gh = t * r_cg[r], s = r_sl[r]; int hit = gh < (float)RMAX; float gend = hit ? gh : (float)RMAX - 1e-4f;
        int jend = (int)(gend * 10.0f); HCell *col = &hcell[a * NRAD]; float z0 = oz;
        for (int j = 0; j <= jend; j++) {
            float z1 = oz + s * (j < jend ? (j + 1) * 0.1f : gend);
            float za = z0 < z1 ? z0 : z1, zb = z0 < z1 ? z1 : z0;
            int lo = za < 0 ? -1 : (int)(za * izr), hi = zb < 0 ? -1 : (int)(zb * izr); /* senza floorf: a -O2 e' una chiamata di libreria */
            if (hi >= 0 && lo < NZL) { if (lo < 0) lo = 0; if (hi >= NZL) hi = NZL - 1; col[j].fr[k] |= bitrange(lo, hi); col[j].tau = frame; }
            z0 = z1; steps++;
        }
        if (hit) { int zl = z0 < 0 ? -1 : (int)(z0 * izr); if (zl >= 0 && zl < NZL) col[jend].occ_now |= 1ULL << zl; }
    }
    for (int i = 0; i < NAZ * NRAD; i++) { HCell *c = &hcell[i]; c->fr[k] &= ~c->occ_now; c->occ_mem = (c->occ_mem & ~c->fr[k]) | c->occ_now; }
    return steps + 2 * (uint64_t)NAZ * NRAD;
}
static uint64_t BAND;
static void query_ibr(uint32_t frame, SecOut *out) {
    (void)frame; uint8_t fl[NSEC][NRB]; memset(fl, 0, sizeof fl);
    for (int a = 0; a < NAZ; a++) { int s = az_sec[a]; if (s < 0) continue; const HCell *c = &hcell[a * NRAD];
        for (int j = 0; j < NRAD; j++) { uint64_t occ = (c[j].occ_now | c[j].occ_mem) & BAND, fre = (c[j].fr[0] | c[j].fr[1] | c[j].fr[2]) & ~occ & BAND;
            uint8_t f = 0; if (occ) f |= F_OCC; if ((occ | fre) != BAND) f |= F_UNK; if (fre) f |= F_FREE; fl[s][j] |= f; } }
    finalize(fl, out);
}

/* ---------- statistiche ---------- */
static int cmpd(const void *a, const void *b) { double x = *(const double *)a, y = *(const double *)b; return (x > y) - (x < y); }
static void stats(double *v, int n, double *mean, double *p95, double *mx) {
    double s = 0; for (int i = 0; i < n; i++) s += v[i]; *mean = s / n;
    double *c = malloc(sizeof(double) * n); memcpy(c, v, sizeof(double) * n); qsort(c, n, sizeof(double), cmpd);
    int i95 = (int)ceil(0.95 * n) - 1; *p95 = c[i95]; *mx = c[n - 1]; free(c);
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "uso: %s STRUTTURA RIS_CM SCENA W H FOTOGRAMMI [ombra] [arena] [tetto_blocchi]\n", argv[0]); return 2; }
    const char *st = argv[1]; int res = atoi(argv[2]); const char *scn = argv[3]; W = atoi(argv[4]); H = atoi(argv[5]); int F = atoi(argv[6]);
    g_shadow = argc > 7 ? atoi(argv[7]) : 0; g_arena = argc > 8 ? atoi(argv[8]) : 0; long cap_arg = argc > 9 ? atol(argv[9]) : 0;
    VS = res / 100.0; IVS = 1.0 / VS; NX = (int)lround(6.0 / VS); NY = (int)lround(4.0 / VS); NZ = (int)lround(3.0 / VS);
    size_t NV = (size_t)NX * NY * NZ;
    rs = 12345; build_scene(!strcmp(scn, "densa")); build_rays(); build_lut();
    for (int a = 0; a < NAZ; a++) { double az = a - 60 + 0.5; int s = (int)floor((az + 43.5) / 87.0 * NSEC); az_sec[a] = (az < -43.5 || s < 0 || s >= NSEC) ? -1 : s; }
    enum { K_NONE, K_DRING, K_DFIX, K_HASH, K_OCT, K_CSR, K_POL, K_IBR } kind = K_NONE;
    size_t reserved = 0;
    if (!strcmp(st, "densa")) { kind = K_DRING; dense = calloc(NV, sizeof(Voxel)); memset(dense, 0, NV * sizeof(Voxel)); reserved = NV * sizeof(Voxel); }
    else if (!strcmp(st, "densafix")) { kind = K_DFIX; dense = calloc(NV, sizeof(Voxel)); memset(dense, 0, NV * sizeof(Voxel)); reserved = NV * sizeof(Voxel); }
    else if (!strcmp(st, "hash") || !strcmp(st, "hashnc")) {
        kind = K_HASH; g_nocache = !strcmp(st, "hashnc");
        uint32_t tot = (uint32_t)(((NX + 7) / 8) * ((NY + 7) / 8) * ((NZ + 7) / 8)); blkcap = cap_arg > 0 ? (uint32_t)cap_arg : tot;
        hcap = 1; hshift = 32; while (hcap < 2 * tot) { hcap <<= 1; hshift--; } hmask = hcap - 1;
        htab = calloc(hcap, sizeof(HEnt)); hblk = calloc(tot + 64, sizeof(Voxel *));
        if (g_arena) harena = malloc((size_t)blkcap * 512 * sizeof(Voxel));
        reserved = (size_t)hcap * sizeof(HEnt) + (size_t)(tot + 64) * sizeof(Voxel *) + (g_arena ? (size_t)blkcap * 4096 : 0);
    }
    else if (!strcmp(st, "octree")) { kind = K_OCT; OD = 1; while ((1 << OD) < NX) OD++; capnode = 1024; capbrick = 1024;
        onode = malloc((size_t)capnode * sizeof(*onode)); obrick = malloc((size_t)capbrick * sizeof(*obrick)); memset(onode[0], 0, sizeof(*onode)); nnode = 1; }
    else if (!strcmp(st, "csr")) { kind = K_CSR; skey = malloc((NV + 1) * 4); sval = malloc((NV + 1) * sizeof(Voxel)); reserved = (NV + 1) * 12; }
    else if (!strncmp(st, "pol", 3)) { kind = K_POL; RMAX = atof(st + 3); NRAD = (int)lround(RMAX * 10);
        pcell = calloc((size_t)NAZ * NRAD, sizeof(PCell)); p_obst = malloc((size_t)NAZ * NRAD); p_gnd = malloc((size_t)NAZ * NRAD); reserved = (size_t)NAZ * NRAD * (sizeof(PCell) + 2); }
    else if (!strncmp(st, "ibr", 3)) { kind = K_IBR; RMAX = atof(st + 3); NRAD = (int)lround(RMAX * 10); ZR = VS; NZL = NZ;
        hcell = calloc((size_t)NAZ * NRAD, sizeof(HCell)); reserved = (size_t)NAZ * NRAD * sizeof(HCell); BAND = bitrange(ZB0, ZB1); }
    else if (strcmp(st, "nulla")) { fprintf(stderr, "struttura sconosciuta\n"); return 2; }

    float *depth = malloc(sizeof(float) * NR); double *tu = malloc(sizeof(double) * F), *tq = malloc(sizeof(double) * F);
    uint64_t steps_tot = 0, steps_max = 0; double sink = 0; SecOut out[NSEC]; memset(out, 0, sizeof out);
    for (int f = 1; f <= F; f++) {
        gen_depth(depth);
        double t0 = now_ms(); uint64_t stp = 0;
        switch (kind) {
            case K_DRING: stp = integ_dring(depth, f); break; case K_DFIX: stp = integ_dfix(depth, f); break;
            case K_HASH: stp = integ_hash(depth, f); break; case K_OCT: stp = integ_oct(depth, f); break;
            case K_CSR: stp = integ_csr(depth, f); break; case K_POL: stp = integ_pol(depth, f); break;
            case K_IBR: stp = integ_ibr(depth, f); break; default: break;
        }
        double t1 = now_ms();
        switch (kind) {
            case K_DRING: query_dring(f, out); break; case K_DFIX: query_dfix(f, out); break;
            case K_HASH: query_hash(f, out); break; case K_OCT: query_oct(f, out); break;
            case K_CSR: query_csr(f, out); break; case K_POL: query_pol(f, out); break;
            case K_IBR: query_ibr(f, out); break; default: break;
        }
        double t2 = now_ms();
        tu[f - 1] = t1 - t0; tq[f - 1] = t2 - t1; steps_tot += stp; if (stp > steps_max) steps_max = stp;
        for (int s = 0; s < NSEC; s++) sink += out[s].near_occ + out[s].nfree;
    }
    double um, u95, ux, qm, q95, qx; stats(tu, F, &um, &u95, &ux); stats(tq, F, &qm, &q95, &qx);
    /* regime: senza il primo fotogramma */
    double um2, u952, ux2; if (F > 1) stats(tu + 1, F - 1, &um2, &u952, &ux2); else { um2 = um; u952 = u95; ux2 = ux; }

    /* memoria usata, somma di controllo, conteggi (fuori dal tempo) */
    size_t used = 0, alloc_vox = 0, touched = 0, nocc = 0, nfreenow = 0; uint64_t ck = 1469598103934665603ULL;
    if (kind >= K_DRING && kind <= K_CSR) {
        for (int ix = 0; ix < NX; ix++) for (int iy = 0; iy < NY; iy++) for (int iz = 0; iz < NZ; iz++) {
            const Voxel *v = kind == K_DRING ? dget_ring(ix, iy, iz) : kind == K_DFIX ? dget_fix(ix, iy, iz) : kind == K_HASH ? hcget(ix, iy, iz) : kind == K_OCT ? ocget(ix, iy, iz) : scget(ix, iy, iz);
            Voxel z = { 0, 0, 0, 0 }; if (v) { z = *v; alloc_vox++; }
            if (z.tau == (uint32_t)F) touched++;
            if (z.L > 0) nocc++; else if (z.tau && z.tau + 2 >= (uint32_t)F) nfreenow++;
            uint64_t w = (uint16_t)z.L | ((uint64_t)z.nu << 16) | ((uint64_t)z.q << 24) | ((uint64_t)z.tau << 32);
            for (int b = 0; b < 8; b++) { ck ^= (w >> (8 * b)) & 0xff; ck *= 1099511628211ULL; }
        }
    }
    switch (kind) {
        case K_DRING: case K_DFIX: used = NV * sizeof(Voxel); break;
        case K_HASH: used = (size_t)hcap * sizeof(HEnt) + (size_t)nblk * sizeof(Voxel *) + (size_t)nblk * (4096 + (g_arena ? 0 : 16)); break;
        case K_OCT: used = (size_t)capnode * sizeof(*onode) + (size_t)capbrick * sizeof(*obrick); reserved = used; break;
        case K_CSR: used = (size_t)sn * 12; break;
        default: used = reserved; break;
    }
    /* scorrimento di un voxel lungo x, 64 volte (solo densa ad anello e hash) */
    double shm = 0, shx = 0;
    if (kind == K_DRING || kind == K_HASH) {
        double ts[64];
        for (int i = 0; i < 64; i++) {
            double a = now_ms();
            if (kind == K_DRING) { memset(&dense[(size_t)g_rox * NY * NZ], 0, (size_t)NY * NZ * sizeof(Voxel)); g_rox = (g_rox + 1) % NX; }
            else if ((i & 7) == 7) { int bx = i >> 3; for (int by = 0; by < (NY + 7) / 8; by++) for (int bz = 0; bz < (NZ + 7) / 8; bz++) h_delete(hkey(bx * 8, by * 8, bz * 8)); }
            ts[i] = now_ms() - a;
        }
        double p; stats(ts, 64, &shm, &p, &shx);
    }
    struct rusage ru; getrusage(RUSAGE_SELF, &ru);
    int sf = 0, su = 0, so = 0; for (int s = 0; s < NSEC; s++) { sf += out[s].nfree; su += out[s].nunk; so += out[s].nocc; }
    printf("%-8s ris=%2dcm scena=%-5s raggi=%6d fot=%d ombra=%d arena=%d | agg_ms media=%.3f p95=%.3f max=%.3f primo=%.3f regime(media=%.3f p95=%.3f max=%.3f) | "
           "interr_ms media=%.4f p95=%.4f max=%.4f | passi/fot media=%.0f max=%llu | mem usata=%zu riservata=%zu B | "
           "voxel teorici=%zu allocati=%zu toccati_ultimo=%zu occ=%zu liberi_ora=%zu | blocchi=%u nodi=%u mattoni=%u scartati=%llu | "
           "settori ultimo: liberi=%d ignoti=%d occupati=%d | scorr_ms media=%.4f max=%.4f | rss_max=%ld kB | somma=%016llx sink=%.1f\n",
           st, res, scn, NR, F, g_shadow, g_arena, um, u95, ux, tu[0], um2, u952, ux2, qm, q95, qx,
           (double)steps_tot / F, (unsigned long long)steps_max, used, reserved, NV, alloc_vox, touched, nocc, nfreenow,
           nblk, nnode, nbrick, (unsigned long long)ndrop, sf, su, so, shm, shx, ru.ru_maxrss, (unsigned long long)ck, sink);
    return 0;
}
