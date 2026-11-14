// banco.c — micro-banco di sciame-tempo-reale (estensione f7, corsia A).
// Misura il costo per fotogramma dell'aggiornamento di una mappa voxel (lancio dei raggi su matrice densa,
// su blocchi con hash, proiezione dei voxel) e della griglia polare del nucleo, su profondità sintetica.
// Compilazione: gcc -O2 -o banco banco.c -lm -lpthread
// Uso:
//   banco tempo <scena> <D|H|P|Q|G> <lato_cm> <k> <margine_sigma> [tetto_blocchi] [lasco]
//   banco sicurezza <scena> <lato_cm> <k>
//   banco interf <scena> <cpuA> <cpuB> <conB>
//   banco vecchi <lato_cm> <Q|P|D>
// scena: vuota | tipica | perturbazione. Seme fisso: ogni lancio dà gli stessi fotogrammi.
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
#include <sched.h>
#include <pthread.h>

#define W 640
#define H 480
#define NF 120
#define NPASS 2
#define PERT_F 60
#define HS 1.2
#define RY0 (-2.0)
#define ROI_X 6.0
#define ROI_Y 4.0
#define ROI_Z 3.0
#define LOCC 17
#define LFREE 8
#define LMAX 70
#define LMIN (-40)

static double fx, fy, cx0, cy0, ct, st;
static float dwx_v[H], dwz_v[H], dwy_u[W];
static uint16_t *frames, *clean;

static double now_ms(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e3 + t.tv_nsec * 1e-6; }
static inline double sigma_z(double z) { return 0.00375 * z * z; }

// ---------- generatore ----------
static uint64_t rs;
static inline uint64_t xr(void) { rs ^= rs >> 12; rs ^= rs << 25; rs ^= rs >> 27; return rs * 0x2545F4914F6CDD1DULL; }
static inline double ur(void) { return (xr() >> 11) * (1.0 / 9007199254740992.0); }
static double gr(void) { double a = 0; for (int i = 0; i < 12; i++) a += ur(); return a - 6.0; }

// ---------- scena ----------
typedef struct { double x0, y0, z0, x1, y1, z1, ay, wy, ph; int from; } Box;
static Box boxes[64]; static int nbox; static double wall_x; static double drop_p; static int drop_from;

static void add_box(double xc, double yc, double z0, double sx, double sy, double sz, double ay, double ph, int from) {
    Box *b = &boxes[nbox++]; b->x0 = xc - sx / 2; b->x1 = xc + sx / 2; b->y0 = yc - sy / 2; b->y1 = yc + sy / 2;
    b->z0 = z0; b->z1 = z0 + sz; b->ay = ay; b->wy = 2 * M_PI / 60.0; b->ph = ph; b->from = from;
}
static void scena(const char *nome) {
    nbox = 0; drop_p = 0; drop_from = 1 << 30; rs = 0x9E3779B97F4A7C15ULL;
    if (!strcmp(nome, "vuota")) { wall_x = 8.0; return; }
    wall_x = 5.5;
    double xs[6] = {1.5, 2.2, 3.0, 3.6, 4.2, 5.0}, ys[6] = {-1.0, 0.8, -0.3, 1.2, 0.0, -1.4};
    for (int i = 0; i < 6; i++) add_box(xs[i], ys[i], 0, 0.3, 0.5, 1.7, 0.6, i * 1.1, 0);
    add_box(4.01, 0.51, 0, 0.02, 0.02, 2.0, 0, 0, 0);            // palo di 2 cm
    if (!strcmp(nome, "perturbazione")) {
        for (int i = 0; i < 40; i++) {
            double sx = 0.15 + 0.25 * ur(), sy = 0.15 + 0.25 * ur(), sz = 0.15 + 0.25 * ur();
            add_box(1.0 + 4.3 * ur(), -1.9 + 3.8 * ur(), 0.2 + 2.4 * ur(), sx, sy, sz, 0.3, 6.28 * ur(), PERT_F);
        }
        drop_p = 0.05; drop_from = PERT_F;
    } else if (strcmp(nome, "tipica")) { fprintf(stderr, "scena sconosciuta\n"); exit(2); }
}
static void geometria(void) {
    fx = (W / 2.0) / tan(87.0 / 2 * M_PI / 180); fy = (H / 2.0) / tan(58.0 / 2 * M_PI / 180);
    cx0 = (W - 1) / 2.0; cy0 = (H - 1) / 2.0; ct = cos(15 * M_PI / 180); st = sin(15 * M_PI / 180);
    for (int v = 0; v < H; v++) { double b = (v - cy0) / fy; dwx_v[v] = ct - st * b; dwz_v[v] = -ct * b - st; }
    for (int u = 0; u < W; u++) dwy_u[u] = -(u - cx0) / fx;
}
static void rendi(void) {
    frames = malloc((size_t)NF * W * H * 2); clean = malloc((size_t)NF * W * H * 2);
    for (int f = 0; f < NF; f++) {
        double by0[64], by1[64]; int act[64], na = 0;
        for (int i = 0; i < nbox; i++) if (f >= boxes[i].from) {
            double dy = boxes[i].ay * sin(boxes[i].wy * f + boxes[i].ph);
            by0[na] = boxes[i].y0 + dy; by1[na] = boxes[i].y1 + dy; act[na++] = i;
        }
        uint16_t *fr = frames + (size_t)f * W * H, *cl = clean + (size_t)f * W * H;
        for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
            double dx = dwx_v[v], dy = dwy_u[u], dz = dwz_v[v], t = wall_x / dx;
            if (dz < 0) { double q = -HS / dz; if (q < t) t = q; } else if (dz > 0) { double q = (4 - HS) / dz; if (q < t) t = q; }
            if (dy > 0) { double q = 6 / dy; if (q < t) t = q; } else if (dy < 0) { double q = -6 / dy; if (q < t) t = q; }
            for (int j = 0; j < na; j++) {
                Box *b = &boxes[act[j]];
                double t0 = b->x0 / dx, t1 = b->x1 / dx; if (t0 >= t) continue;
                if (dy != 0) { double a = by0[j] / dy, c = by1[j] / dy; if (a > c) { double w = a; a = c; c = w; } if (a > t0) t0 = a; if (c < t1) t1 = c; }
                else if (by0[j] > 0 || by1[j] < 0) continue;
                if (dz != 0) { double a = (b->z0 - HS) / dz, c = (b->z1 - HS) / dz; if (a > c) { double w = a; a = c; c = w; } if (a > t0) t0 = a; if (c < t1) t1 = c; }
                else if (b->z0 > HS || b->z1 < HS) continue;
                if (t0 <= t1 && t0 > 0 && t0 < t) t = t0;
            }
            double zn = t + sigma_z(t) * gr(); int bad = (zn < 0.4 || zn > 10.0);
            if (f >= drop_from && ur() < drop_p) bad = 1;
            cl[v * W + u] = (uint16_t)(t * 1000 + 0.5); fr[v * W + u] = bad ? 0 : (uint16_t)(zn * 1000 + 0.5);
        }
    }
}

// ---------- mappa ----------
typedef struct { int8_t L; uint8_t fl; uint16_t sf, sh, ep; } Vox;   // 8 byte
static int nx, ny, nz; static double vs; static Vox *dg;
// blocchi con hash
static int maxblk, capblk, usedblk; static Vox *pool; static int32_t *htk, *hti; static uint32_t hmask; static int hshift;
static long n_alloc_fallite;
static Vox *hlookup(uint32_t key, int alloc) {
    uint32_t h = (key * 2654435761u) >> hshift;
    for (;;) {
        if (htk[h] == (int32_t)key) return pool + (size_t)hti[h] * 512;
        if (htk[h] < 0) {
            if (!alloc) return NULL;
            if (usedblk >= capblk) { n_alloc_fallite++; return NULL; }
            htk[h] = key; hti[h] = usedblk; memset(pool + (size_t)usedblk * 512, 0, 512 * sizeof(Vox)); return pool + (size_t)(usedblk++) * 512;
        }
        h = (h + 1) & hmask;
    }
}
typedef struct { uint32_t k; Vox *b; } HC;
static inline Vox *hget(int ix, int iy, int iz, HC *c) {
    uint32_t key = (uint32_t)(ix >> 3) | ((uint32_t)(iy >> 3) << 8) | ((uint32_t)(iz >> 3) << 16);
    if (key != c->k) { c->b = hlookup(key, 1); c->k = key; }
    return c->b ? c->b + ((ix & 7) | ((iy & 7) << 3) | ((iz & 7) << 6)) : NULL;
}
static void mappa_init(double lato) {
    vs = lato; nx = (int)(ROI_X / vs + 0.5); ny = (int)(ROI_Y / vs + 0.5); nz = (int)(ROI_Z / vs + 0.5);
    dg = calloc((size_t)nx * ny * nz, sizeof(Vox));
    maxblk = ((nx + 7) / 8) * ((ny + 7) / 8) * ((nz + 7) / 8); capblk = maxblk; usedblk = 0;
    pool = malloc((size_t)maxblk * 512 * sizeof(Vox)); memset(pool, 0, (size_t)maxblk * 512 * sizeof(Vox));
    int hs = 1, sh = 0; while (hs < maxblk * 3) { hs <<= 1; sh++; } hmask = hs - 1; hshift = 32 - sh;
    htk = malloc(hs * 4); hti = malloc(hs * 4); for (int i = 0; i < hs; i++) htk[i] = -1;
}

// attraversamento di Amanatides e Woo: t è la profondità Z lungo il raggio (la direzione ha componente ottica 1)
#define DDA(DX, DY, DZ, TEND, VISIT) do { \
    double gx_ = 1e-4 * (DX) / vs, gy_ = (-RY0 + 1e-4 * (DY)) / vs, gz_ = (HS + 1e-4 * (DZ)) / vs; \
    int ix = (int)gx_, iy = (int)floor(gy_), iz = (int)floor(gz_); \
    double ddx = (DX) / vs, ddy = (DY) / vs, ddz = (DZ) / vs; \
    int sx_ = 1, sy_ = ddy > 0 ? 1 : -1, sz_ = ddz > 0 ? 1 : -1; \
    double tdx = 1.0 / ddx, tdy = ddy != 0 ? fabs(1.0 / ddy) : 1e30, tdz = ddz != 0 ? fabs(1.0 / ddz) : 1e30; \
    double tmx = 1e-4 + (ix + 1 - gx_) * tdx; \
    double tmy = ddy != 0 ? 1e-4 + (sy_ > 0 ? (iy + 1 - gy_) : (gy_ - iy)) * tdy : 1e30; \
    double tmz = ddz != 0 ? 1e-4 + (sz_ > 0 ? (iz + 1 - gz_) : (gz_ - iz)) * tdz : 1e30; \
    double te_ = (TEND); \
    if (te_ > 1e-4) for (;;) { \
        VISIT; \
        if (tmx < tmy) { \
            if (tmx < tmz) { if (tmx >= te_) break; ix += sx_; tmx += tdx; if (ix >= nx) break; } \
            else { if (tmz >= te_) break; iz += sz_; tmz += tdz; if ((unsigned)iz >= (unsigned)nz) break; } \
        } else { \
            if (tmy < tmz) { if (tmy >= te_) break; iy += sy_; tmy += tdy; if ((unsigned)iy >= (unsigned)ny) break; } \
            else { if (tmz >= te_) break; iz += sz_; tmz += tdz; if ((unsigned)iz >= (unsigned)nz) break; } \
        } \
    } } while (0)

static inline int vox_of(double z, double dx, double dy, double dz) {   // indice del voxel del punto, o -1
    double x = z * dx, y = z * dy - RY0, zz = HS + z * dz;
    if (x < 0 || y < 0 || zz < 0) return -1;
    int ix = (int)(x / vs), iy = (int)(y / vs), iz = (int)(zz / vs);
    if (ix >= nx || iy >= ny || iz >= nz) return -1;
    return ix + nx * (iy + ny * iz);
}

static long g_steps, g_rays, g_hits;

// passo 1: i colpi a piena risoluzione (sempre prima dei liberi)
static void colpi_densa(const uint16_t *fr, uint16_t stamp) {
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        uint16_t mm = fr[v * W + u]; if (!mm) continue;
        int id = vox_of(mm * 1e-3, dwx_v[v], dwy_u[u], dwz_v[v]); if (id < 0) continue;
        Vox *q = &dg[id]; q->sh = stamp; int l = q->L + LOCC; q->L = l > LMAX ? LMAX : l; g_hits++;
    }
}
static void colpi_hash(const uint16_t *fr, uint16_t stamp) {
    HC c = {0xffffffffu, NULL};
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        uint16_t mm = fr[v * W + u]; if (!mm) continue;
        double z = mm * 1e-3, x = z * dwx_v[v], y = z * dwy_u[u] - RY0, zz = HS + z * dwz_v[v];
        if (y < 0 || zz < 0) continue; int ix = (int)(x / vs), iy = (int)(y / vs), iz = (int)(zz / vs);
        if (ix >= nx || iy >= ny || iz >= nz) continue;
        Vox *q = hget(ix, iy, iz, &c); if (!q) continue; q->sh = stamp; int l = q->L + LOCC; q->L = l > LMAX ? LMAX : l; g_hits++;
    }
}
// minimo del blocco k×k; rigido: un solo pixel non valido annulla il blocco; lasco: minimo dei validi
static inline double zmin_blocco(const uint16_t *fr, int u0, int v0, int k, int lasco) {
    unsigned m = 65535; int inval = 0;
    for (int v = v0; v < v0 + k; v++) for (int u = u0; u < u0 + k; u++) { unsigned mm = fr[v * W + u]; if (!mm) inval = 1; else if (mm < m) m = mm; }
    if (m == 65535 || (inval && !lasco)) return -1; return m * 1e-3;
}
static inline double tclip(double dx, double dy, double dz) {
    double t = ROI_X / dx;
    if (dy > 0) { double q = (ROI_Y + RY0) / dy; if (q < t) t = q; } else if (dy < 0) { double q = RY0 / dy; if (q < t) t = q; }
    if (dz > 0) { double q = (ROI_Z - HS) / dz; if (q < t) t = q; } else if (dz < 0) { double q = -HS / dz; if (q < t) t = q; }
    return t;
}
// passo 2: lo scavo dei liberi, un raggio per blocco k×k, fino al minimo del blocco meno il margine
static void liberi_densa(const uint16_t *fr, uint16_t stamp, int k, double marg, int lasco) {
    long steps = 0, rays = 0;
    for (int v0 = 0; v0 < H; v0 += k) for (int u0 = 0; u0 < W; u0 += k) {
        double z = zmin_blocco(fr, u0, v0, k, lasco); if (z < 0) continue;
        double a = (u0 + (k - 1) * 0.5 - cx0) / fx, b = (v0 + (k - 1) * 0.5 - cy0) / fy;
        double dx = ct - st * b, dy = -a, dz = -ct * b - st, te = z - marg * sigma_z(z), tc = tclip(dx, dy, dz);
        if (tc < te) te = tc; rays++;
        DDA(dx, dy, dz, te, { Vox *q = &dg[ix + nx * (iy + ny * iz)]; if (q->sh != stamp) { q->sf = stamp; int l = q->L - LFREE; q->L = l < LMIN ? LMIN : l; } steps++; });
    }
    g_steps += steps; g_rays += rays;
}
static void liberi_hash(const uint16_t *fr, uint16_t stamp, int k, double marg, int lasco) {
    long steps = 0, rays = 0; HC c = {0xffffffffu, NULL};
    for (int v0 = 0; v0 < H; v0 += k) for (int u0 = 0; u0 < W; u0 += k) {
        double z = zmin_blocco(fr, u0, v0, k, lasco); if (z < 0) continue;
        double a = (u0 + (k - 1) * 0.5 - cx0) / fx, b = (v0 + (k - 1) * 0.5 - cy0) / fy;
        double dx = ct - st * b, dy = -a, dz = -ct * b - st, te = z - marg * sigma_z(z), tc = tclip(dx, dy, dz);
        if (tc < te) te = tc; rays++;
        DDA(dx, dy, dz, te, { Vox *q = hget(ix, iy, iz, &c); if (q && q->sh != stamp) { q->sf = stamp; int l = q->L - LFREE; q->L = l < LMIN ? LMIN : l; } steps++; });
    }
    g_steps += steps; g_rays += rays;
}

// ---------- proiezione dei voxel con piramide dei minimi ----------
#define NL 7
static uint16_t *pyr[NL]; static int pw[NL], ph[NL];
static void pyr_init(void) { pw[0] = W; ph[0] = H; for (int l = 1; l < NL; l++) { pw[l] = (pw[l - 1] + 1) / 2; ph[l] = (ph[l - 1] + 1) / 2; pyr[l] = malloc((size_t)pw[l] * ph[l] * 2); } }
static void pyr_build(const uint16_t *fr) {
    pyr[0] = (uint16_t *)fr;
    for (int l = 1; l < NL; l++) for (int y = 0; y < ph[l]; y++) for (int x = 0; x < pw[l]; x++) {
        int x0 = 2 * x, y0 = 2 * y, x1 = x0 + 1 < pw[l - 1] ? x0 + 1 : x0, y1 = y0 + 1 < ph[l - 1] ? y0 + 1 : y0;
        const uint16_t *p = pyr[l - 1]; int w = pw[l - 1];
        uint16_t m = p[y0 * w + x0], q = p[y0 * w + x1]; if (q < m) m = q; q = p[y1 * w + x0]; if (q < m) m = q; q = p[y1 * w + x1]; if (q < m) m = q;
        pyr[l][y * pw[l] + x] = m;       // un pixel non valido vale 0: il minimo diventa 0 e blocca il «libero»
    }
}
static uint16_t *lev0v;
static void pyr_build_validi(const uint16_t *fr) {            // minimo dei soli pixel validi: il non valido vale 65535
    if (!lev0v) lev0v = malloc((size_t)W * H * 2);
    for (int i = 0; i < W * H; i++) lev0v[i] = fr[i] ? fr[i] : 65535;
    pyr_build(lev0v);
}
static void liberi_proiezione(const uint16_t *fr, uint16_t stamp, double marg, int lasco) {
    if (lasco) pyr_build_validi(fr); else pyr_build(fr);
    double rho = vs * 0.8660254; long steps = 0;
    for (int iz = 0; iz < nz; iz++) for (int ix = 0; ix < nx; ix++) {
        double rx = (ix + 0.5) * vs, rz = (iz + 0.5) * vs - HS, Zc = ct * rx - st * rz, Yc = -st * rx - ct * rz;
        if (Zc - rho < 0.4) continue;
        double v = cy0 + fy * Yc / Zc, rv = fy * rho / (Zc - rho), ru = fx * rho / (Zc - rho);
        if (v - rv < 0 || v + rv > H - 1) continue;
        double ext = 2 * (ru > rv ? ru : rv); int l = 0; while (ext / (1 << l) > 2 && l < NL - 1) l++;
        int y0 = (int)(v - rv) >> l, y1 = ((int)(v + rv) + 1); if (y1 > H - 1) y1 = H - 1; y1 >>= l;
        double zf = Zc + rho; unsigned thr = (unsigned)((zf + marg * sigma_z(zf)) * 1000 + 1);
        const uint16_t *p = pyr[l]; int w = pw[l]; double fz = fx / Zc;
        Vox *row = &dg[ix + nx * ny * iz];
        for (int iy = 0; iy < ny; iy++) {
            double u = cx0 - fz * ((iy + 0.5) * vs + RY0);
            if (u - ru < 0 || u + ru > W - 1) continue;
            int x0 = (int)(u - ru) >> l, x1 = (int)(u + ru) + 1; if (x1 > W - 1) x1 = W - 1; x1 >>= l;
            unsigned m = 65535; for (int y = y0; y <= y1; y++) for (int x = x0; x <= x1; x++) { unsigned q = p[y * w + x]; if (q < m) m = q; }
            steps++;
            if (m > thr && m != 65535) { Vox *q = row + (size_t)nx * iy; if (q->sh != stamp) { q->sf = stamp; int ll = q->L - LFREE; q->L = ll < LMIN ? LMIN : ll; } }
            else if (m != 65535) row[(size_t)nx * iy].ep = stamp;      // contraddetto ora: una profondita' valida sta davanti al lato lontano del voxel
        }
    }
    g_steps += steps;
}

// ---------- griglia polare del nucleo: 1° × 0,1 m fino a 3 m ----------
#define NAZ 87
#define NRB 30
static int16_t *az_lut; static float *kr_lut, *kh_lut; static uint16_t ground[NAZ * NRB]; static uint8_t cell[NAZ * NRB]; static float first_r[NAZ];
static void polare_init(void) {
    az_lut = malloc(W * H * 2); kr_lut = malloc(W * H * 4); kh_lut = malloc(W * H * 4);
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        double dx = dwx_v[v], dy = dwy_u[u]; int a = (int)floor(atan2(dy, dx) * 180 / M_PI + 43.5);
        az_lut[v * W + u] = (a < 0 || a >= NAZ) ? -1 : a; kr_lut[v * W + u] = hypot(dx, dy); kh_lut[v * W + u] = dwz_v[v];
    }
}
static void polare(const uint16_t *fr, uint16_t stamp) {
    for (int a = 0; a < NAZ; a++) first_r[a] = 1e9f;
    for (int i = 0; i < W * H; i++) {
        unsigned mm = fr[i]; int a = az_lut[i]; if (!mm || a < 0) continue;
        float z = mm * 1e-3f, rho = z * kr_lut[i], h = (float)HS + z * kh_lut[i];
        if (h > 0.07f && h < 2.0f) { if (rho < first_r[a]) first_r[a] = rho; }
        else if (h <= 0.07f && h >= -0.07f) { int rb = (int)(rho * 10); if (rb < NRB) ground[a * NRB + rb] = stamp; }
    }
    for (int a = 0; a < NAZ; a++) {
        int fb = first_r[a] < 3.0f ? (int)(first_r[a] * 10) : NRB;
        for (int rb = 0; rb < NRB; rb++) {
            uint8_t s;                                             // 0 non osservato, 1 libero, 2 occupato, 3 in ombra
            if (rb < fb) s = (ground[a * NRB + rb] && (uint16_t)(stamp - ground[a * NRB + rb]) < 3) ? 1 : 0;
            else if (rb == fb) s = 2; else s = 3;
            cell[a * NRB + rb] = s;
        }
    }
}

// ---------- statistiche ----------
static int cmpd(const void *a, const void *b) { double x = *(double *)a, y = *(double *)b; return x < y ? -1 : x > y; }
static void stat(double *t, int n, double *mean, double *p50, double *p95, double *p99, double *mx) {
    double *s = malloc(n * sizeof(double)); memcpy(s, t, n * sizeof(double)); qsort(s, n, sizeof(double), cmpd);
    double a = 0; for (int i = 0; i < n; i++) a += s[i]; *mean = a / n; *p50 = s[n / 2];
    *p95 = s[(int)ceil(0.95 * n) - 1]; *p99 = s[(int)ceil(0.99 * n) - 1]; *mx = s[n - 1]; free(s);
}
static double mediana(double *t, int n) { double m, a, b, c, d; stat(t, n, &m, &a, &b, &c, &d); return a; }

static int modo_tempo(int argc, char **argv) {
    const char *sc = argv[2]; char met = argv[3][0]; double lato = atof(argv[4]) / 100.0; int k = atoi(argv[5]); double marg = atof(argv[6]);
    int tetto = argc > 7 ? atoi(argv[7]) : 0, lasco = argc > 8 ? atoi(argv[8]) : 0;
    geometria(); scena(sc); rendi(); mappa_init(lato); if (tetto > 0) capblk = tetto; pyr_init(); polare_init();
    static double tt[NPASS * NF]; int n = 0; g_steps = g_rays = g_hits = 0;
    for (int p = 0; p < NPASS; p++) for (int f = 0; f < NF; f++) {
        const uint16_t *fr = frames + (size_t)f * W * H; uint16_t stamp = (uint16_t)(p * NF + f + 1);
        double t0 = now_ms();
        if (met == 'G') polare(fr, stamp);
        else if (met == 'D') { colpi_densa(fr, stamp); liberi_densa(fr, stamp, k, marg, lasco); }
        else if (met == 'H') { colpi_hash(fr, stamp); liberi_hash(fr, stamp, k, marg, lasco); }
        else if (met == 'P') { colpi_densa(fr, stamp); liberi_proiezione(fr, stamp, marg, 0); }
        else if (met == 'Q') { colpi_densa(fr, stamp); liberi_proiezione(fr, stamp, marg, 1); }
        tt[n++] = now_ms() - t0;
    }
    double mean, p50, p95, p99, mx; stat(tt, n, &mean, &p50, &p95, &p99, &mx);
    uint16_t last = (uint16_t)(NPASS * NF); long nfree = 0, nocc = 0, tot = (long)nx * ny * nz;
    if (met == 'H') { for (long i = 0; i < (long)usedblk * 512; i++) { if (pool[i].sh == last) nocc++; else if (pool[i].sf == last) nfree++; } }
    else if (met != 'G') { for (long i = 0; i < tot; i++) { if (dg[i].sh == last) nocc++; else if (dg[i].sf == last) nfree++; } }
    else { for (int i = 0; i < NAZ * NRB; i++) { if (cell[i] == 1) nfree++; else if (cell[i] == 2) nocc++; } tot = NAZ * NRB; }
    printf("scena=%s metodo=%c lato_cm=%g k=%d margine=%g lasco=%d cpu=%d | N=%d media=%.3f p50=%.3f p95=%.3f p99=%.3f max=%.3f primo=%.3f ms",
           sc, met, lato * 100, k, marg, lasco, sched_getcpu(), n, mean, p50, p95, p99, mx, tt[0]);
    if (met != 'G') printf(" | raggi/fot=%.0f passi/raggio=%.1f passi/fot=%.0f colpi/fot=%.0f", (double)g_rays / n, g_rays ? (double)g_steps / g_rays : 0.0, (double)g_steps / n, (double)g_hits / n);
    printf(" | celle=%ld liberi=%ld occupati=%ld (ultimo fot.)", tot, nfree, nocc);
    printf(" | f%d: giro1=%.3f (mediana f30-59 %.3f) giro2=%.3f (mediana %.3f)", PERT_F, tt[PERT_F], mediana(tt + 30, 30), tt[NF + PERT_F], mediana(tt + NF + 30, 30));
    if (met == 'H') printf(" | blocchi=%d/%d tetto=%d alloc_fallite=%ld mem_MB=%.2f", usedblk, maxblk, capblk, n_alloc_fallite, usedblk * 512.0 * 8 / 1e6);
    else if (met != 'G') printf(" | mem_MB=%.2f", tot * 8.0 / 1e6);
    printf("\n"); return 0;
}

// ---------- modo sicurezza: falsi «libero» in un fotogramma, mappa azzerata ----------
static void conta(const char *nome, const uint8_t *lib, const uint8_t *gt1, const uint8_t *gt2, long tot, long *acc) {
    long nl = 0, f1 = 0, f2 = 0, f3 = 0; int izmin = (int)(0.10 / vs + 0.5);   // f3: come f2, esclusi i voxel con il centro sotto 0,10 m
    for (long i = 0; i < tot; i++) if (lib[i]) { nl++; if (gt1[i]) f1++; if (gt2[i]) { f2++; if (i / ((long)nx * ny) >= izmin) f3++; } }
    acc[0] += nl; acc[1] += f1; acc[2] += f2; acc[3] += f3; (void)nome;
}
static int modo_sicurezza(int argc, char **argv) {
    (void)argc; const char *sc = argv[2]; double lato = atof(argv[3]) / 100.0; int k = atoi(argv[4]);
    geometria(); scena(sc); rendi(); mappa_init(lato); pyr_init();
    long tot = (long)nx * ny * nz; uint8_t *gt1 = malloc(tot), *gt2 = malloc(tot), *lib = malloc(tot); int16_t *acc = malloc(tot * 2);
    enum { NV = 11 }; const char *nomi[NV] = {
        "a  k=1, somma dei log-odds, senza priorita'", "b  k=1, priorita' al colpo, margine 0", "b3 k=1, priorita' al colpo, margine 3 sigma",
        "c  decimazione k (colpi e liberi solo sui campioni)", "d  minimo del blocco k, colpo sul raggio centrale", "e  colpi pieni + liberi a blocchi (rigido), margine 0",
        "e3 colpi pieni + liberi a blocchi (rigido), margine 3 sigma", "eL colpi pieni + liberi a blocchi (lasco), margine 3 sigma", "p  proiezione dei voxel, margine 0", "p3 proiezione dei voxel, margine 3 sigma", "q3 proiezione lasca (minimo dei validi), margine 3 sigma"};
    long A[NV][4]; memset(A, 0, sizeof A); long ngt1 = 0, ngt2 = 0, ngt3 = 0; int nfr = 0;
    for (int f = 5; f < NF; f += 10) {
        const uint16_t *fr = frames + (size_t)f * W * H, *cl = clean + (size_t)f * W * H; nfr++;
        memset(gt1, 0, tot); memset(gt2, 0, tot);
        for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
            int id; if (fr[v * W + u]) { id = vox_of(fr[v * W + u] * 1e-3, dwx_v[v], dwy_u[u], dwz_v[v]); if (id >= 0) gt1[id] = 1; }
            id = vox_of(cl[v * W + u] * 1e-3, dwx_v[v], dwy_u[u], dwz_v[v]); if (id >= 0) gt2[id] = 1;
        }
        for (long i = 0; i < tot; i++) { ngt1 += gt1[i]; ngt2 += gt2[i]; if (gt2[i] && i / ((long)nx * ny) >= (int)(0.10 / vs + 0.5)) ngt3++; }
        // a: somma
        memset(acc, 0, tot * 2); memset(lib, 0, tot);
        for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
            uint16_t mm = fr[v * W + u]; if (!mm) continue; double z = mm * 1e-3, dx = dwx_v[v], dy = dwy_u[u], dz = dwz_v[v];
            int eid = vox_of(z, dx, dy, dz); double te = z, tc = tclip(dx, dy, dz); if (tc < te) te = tc;
            DDA(dx, dy, dz, te, { int id = ix + nx * (iy + ny * iz); if (id != eid) acc[id] -= LFREE; });
            if (eid >= 0) acc[eid] += LOCC;
        }
        for (long i = 0; i < tot; i++) lib[i] = acc[i] < 0; conta(nomi[0], lib, gt1, gt2, tot, A[0]);
        for (int var = 1; var < NV; var++) {
            memset(dg, 0, tot * sizeof(Vox)); uint16_t stamp = 1;
            if (var == 1) { colpi_densa(fr, stamp); liberi_densa(fr, stamp, 1, 0, 0); }
            else if (var == 2) { colpi_densa(fr, stamp); liberi_densa(fr, stamp, 1, 3, 0); }
            else if (var == 3) {            // decimazione: un pixel ogni k, colpi e liberi solo da quello
                for (int v = k / 2; v < H; v += k) for (int u = k / 2; u < W; u += k) { uint16_t mm = fr[v * W + u]; if (!mm) continue; int id = vox_of(mm * 1e-3, dwx_v[v], dwy_u[u], dwz_v[v]); if (id >= 0) dg[id].sh = stamp; }
                for (int v = k / 2; v < H; v += k) for (int u = k / 2; u < W; u += k) {
                    uint16_t mm = fr[v * W + u]; if (!mm) continue; double z = mm * 1e-3, dx = dwx_v[v], dy = dwy_u[u], dz = dwz_v[v], te = z, tc = tclip(dx, dy, dz); if (tc < te) te = tc;
                    DDA(dx, dy, dz, te, { Vox *q = &dg[ix + nx * (iy + ny * iz)]; if (q->sh != stamp) q->sf = stamp; });
                }
            } else if (var == 4) {          // minimo del blocco, colpo sul raggio centrale
                for (int pass = 0; pass < 2; pass++) for (int v0 = 0; v0 < H; v0 += k) for (int u0 = 0; u0 < W; u0 += k) {
                    double z = zmin_blocco(fr, u0, v0, k, 1); if (z < 0) continue;
                    double a = (u0 + (k - 1) * 0.5 - cx0) / fx, b = (v0 + (k - 1) * 0.5 - cy0) / fy, dx = ct - st * b, dy = -a, dz = -ct * b - st;
                    if (pass == 0) { int id = vox_of(z, dx, dy, dz); if (id >= 0) dg[id].sh = stamp; }
                    else { double te = z, tc = tclip(dx, dy, dz); if (tc < te) te = tc; DDA(dx, dy, dz, te, { Vox *q = &dg[ix + nx * (iy + ny * iz)]; if (q->sh != stamp) q->sf = stamp; }); }
                }
            } else if (var == 5) { colpi_densa(fr, stamp); liberi_densa(fr, stamp, k, 0, 0); }
            else if (var == 6) { colpi_densa(fr, stamp); liberi_densa(fr, stamp, k, 3, 0); }
            else if (var == 7) { colpi_densa(fr, stamp); liberi_densa(fr, stamp, k, 3, 1); }
            else if (var == 8) { colpi_densa(fr, stamp); liberi_proiezione(fr, stamp, 0, 0); }
            else if (var == 9) { colpi_densa(fr, stamp); liberi_proiezione(fr, stamp, 3, 0); }
            else if (var == 10) { colpi_densa(fr, stamp); liberi_proiezione(fr, stamp, 3, 1); }
            for (long i = 0; i < tot; i++) lib[i] = (dg[i].sf == stamp && dg[i].sh != stamp); conta(nomi[var], lib, gt1, gt2, tot, A[var]);
        }
    }
    printf("scena=%s lato_cm=%g k=%d fotogrammi=%d voxel=%ld | voxel con superficie misurata (rif.1)=%.0f/fot, con superficie vera (rif.2)=%.0f/fot, di cui sopra 0,10 m (rif.3)=%.0f/fot\n", sc, lato * 100, k, nfr, tot, (double)ngt1 / nfr, (double)ngt2 / nfr, (double)ngt3 / nfr);
    for (int i = 0; i < NV; i++) printf("  %-62s liberi/fot=%8.0f  falsi su rif.1=%7ld  falsi su rif.2=%7ld  su rif.3=%7ld  (somma su %d fot.)\n", nomi[i], (double)A[i][0] / nfr, A[i][1], A[i][2], A[i][3], nfr);
    return 0;
}

// ---------- modo interferenza ----------
static volatile int stopB; static int cpuB_g;
static void pin(int cpu) { cpu_set_t s; CPU_ZERO(&s); CPU_SET(cpu, &s); pthread_setaffinity_np(pthread_self(), sizeof s, &s); }
static void *threadB(void *arg) {
    (void)arg; pin(cpuB_g); uint16_t stamp = 1;
    while (!stopB) for (int f = 0; f < NF && !stopB; f++) { const uint16_t *fr = frames + (size_t)f * W * H; colpi_densa(fr, stamp); liberi_densa(fr, stamp, 1, 0, 0); stamp++; if (!stamp) stamp = 1; }
    return NULL;
}
static int modo_interf(int argc, char **argv) {
    (void)argc; const char *sc = argv[2]; int cpuA = atoi(argv[3]); cpuB_g = atoi(argv[4]); int conB = atoi(argv[5]);
    geometria(); scena(sc); rendi(); mappa_init(0.05); polare_init(); pthread_t tb;
    if (conB) pthread_create(&tb, NULL, threadB, NULL);
    pin(cpuA); static double tt[2 * NF]; int n = 0; struct timespec nx_t; clock_gettime(CLOCK_MONOTONIC, &nx_t); double rit_max = 0;
    for (int p = 0; p < 2; p++) for (int f = 0; f < NF; f++) {
        nx_t.tv_nsec += 66666667; if (nx_t.tv_nsec >= 1000000000) { nx_t.tv_nsec -= 1000000000; nx_t.tv_sec++; }
        clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &nx_t, NULL);
        double t0 = now_ms(), rit = t0 - (nx_t.tv_sec * 1e3 + nx_t.tv_nsec * 1e-6); if (rit > rit_max) rit_max = rit;
        polare(frames + (size_t)f * W * H, (uint16_t)(p * NF + f + 1)); tt[n++] = now_ms() - t0;
    }
    stopB = 1; if (conB) pthread_join(tb, NULL);
    double mean, p50, p95, p99, mx; stat(tt, n, &mean, &p50, &p95, &p99, &mx);
    printf("interferenza scena=%s G a 15 Hz su cpu %d, D 5 cm k=1 su cpu %d: %s | N=%d media=%.3f p50=%.3f p95=%.3f p99=%.3f max=%.3f ms | ritardo massimo del risveglio=%.3f ms\n",
           sc, cpuA, cpuB_g, conB ? "ATTIVO" : "spento", n, mean, p50, p95, p99, mx, rit_max);
    return 0;
}

// ---------- modo vecchi: dati vecchi contro occlusione nuova (prove 2 e 5) ----------
static int dentro_scatola(double x, double y, double z, int f) {
    for (int i = 0; i < nbox; i++) if (f >= boxes[i].from) {
        double dy = boxes[i].ay * sin(boxes[i].wy * f + boxes[i].ph);
        if (x >= boxes[i].x0 && x <= boxes[i].x1 && y >= boxes[i].y0 + dy && y <= boxes[i].y1 + dy && z >= boxes[i].z0 && z <= boxes[i].z1) return 1;
    }
    return 0;
}
static int modo_vecchi(int argc, char **argv) {
    (void)argc; double lato = atof(argv[2]) / 100.0; char met = argv[3][0];
    geometria(); scena("perturbazione"); rendi(); mappa_init(lato); pyr_init(); long tot = (long)nx * ny * nz;
    for (int fermo = 0; fermo < 2; fermo++) {
        memset(dg, 0, tot * sizeof(Vox));
        printf("vecchi lato_cm=%g metodo=%c mappa=%s | per fotogramma: voxel con il centro in una scatola; falsi liberi nelle letture L (log-odds<0), M3 (ultimi 3 fot.), M1 (solo fot. corrente)\n", lato * 100, met, fermo ? "FERMA dal fot. 60" : "che integra");
        for (int f = 0; f < 75; f++) {
            const uint16_t *fr = frames + (size_t)f * W * H; uint16_t stamp = (uint16_t)(f + 1);
            if (!(fermo && f >= PERT_F)) { colpi_densa(fr, stamp); if (met == 'D') liberi_densa(fr, stamp, 4, 3, 0); else liberi_proiezione(fr, stamp, 3, met == 'Q'); }
            if (f < 58 || (f > 64 && f != 74)) continue;
            long nin = 0, fl = 0, f3 = 0, f1 = 0, f3c = 0;
            for (int iz = 0; iz < nz; iz++) for (int iy = 0; iy < ny; iy++) for (int ix = 0; ix < nx; ix++) {
                if (!dentro_scatola((ix + 0.5) * vs, (iy + 0.5) * vs + RY0, (iz + 0.5) * vs, f)) continue;
                Vox *q = &dg[ix + nx * (iy + ny * iz)]; nin++;
                if (q->L < 0) fl++;
                if (q->sh != stamp && q->sf && (uint16_t)(stamp - q->sf) < 3) { f3++; if (q->ep != stamp) f3c++; }
                if (q->sh != stamp && q->sf == stamp) f1++;
            }
            printf("  f=%2d  dentro=%6ld  L=%6ld  M3=%6ld  M1=%6ld  M3c=%6ld\n", f, nin, fl, f3, f1, f3c);
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc >= 7 && !strcmp(argv[1], "tempo")) return modo_tempo(argc, argv);
    if (argc >= 5 && !strcmp(argv[1], "sicurezza")) return modo_sicurezza(argc, argv);
    if (argc >= 6 && !strcmp(argv[1], "interf")) return modo_interf(argc, argv);
    if (argc >= 4 && !strcmp(argv[1], "vecchi")) return modo_vecchi(argc, argv);
    fprintf(stderr, "uso: vedi l'intestazione di banco.c\n"); return 2;
}
