/* banco.c — banco di prova indipendente di sciame-prestazioni (estensione f7).
 * Scritto da capo il 14 novembre 2026, senza leggere il codice degli altri ruoli.
 * Una rappresentazione per eseguibile:  gcc -O2 -DREP=R_xxx banco.c -lm
 * Uso: ./banco_xxx scena(vuota|rada|densa|carico) res_cm(10|5) passo(1|2|4|8) fotogrammi [fasce] [portata_polare_m]
 * Il tempo misurato comprende: deproiezione dei pixel, lancio dei raggi, scritture, potatura.
 * NON comprende la generazione dell'immagine di profondita' (e' il sensore simulato).
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <sys/prctl.h>

#define R_POLARE 1
#define R_IMMAGINE 2
#define R_FASCE 3
#define R_DENSA 4
#define R_HASH 5
#define R_HASHOCC 6
#define R_OCTREE 7
#define R_OCTPOT 8
#define R_COLBIT 9   /* aggiunta dopo il primo giro di misure: colonne di bit di quota (vedi BENCHMARK_INDIPENDENTE.md) */
#ifndef REP
#error "manca -DREP=R_xxx"
#endif
#define E_VOXEL (REP==R_DENSA||REP==R_HASH||REP==R_HASHOCC||REP==R_OCTREE||REP==R_OCTPOT)

/* ---------- camera e regione ---------- */
#define W 640
#define H 480
#define HFOV_G 87.0
#define VFOV_G 58.0
#define CAMZ 1.2f
#define TILT_G 15.0
#define ZMAX_MM 6000
#define ROIX 6.0f
#define HY 2.0f
#define ROIZ 3.0f
#define DT (1.0f/15.0f)
#define NSET 18
#define NRQ 60          /* distanze della tabella dei settori: 60 x 0,1 m */
#define QZ0 0.10f       /* quote interrogate: 0,10-2,00 m */
#define QZ1 2.00f

static float FX, FY, CXc, CYc, CT, ST;
static float ca[W];            /* (u-cx)/fx */
static float dirx[H], dirz[H]; /* componenti x e z della direzione per riga (profondita' z unitaria) */
static uint16_t D[W * H];      /* immagine di profondita' in mm, 0 = non valido */
static float zb[W * H], zbase[W * H];

static float RES, INV;
static int NX, NY, NZ, PASSO = 1, NFASCE = 3;
static float PORTATA = 3.0f;
static uint64_t n_raggi, n_passi;
static size_t mem_struttura, mem_indice, mem_tabelle;

static inline uint64_t ora(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}
static long leggi_stato(const char *chiave) {
    FILE *f = fopen("/proc/self/status", "r"); char r[256]; long v = -1; size_t n = strlen(chiave);
    if (!f) return -1;
    while (fgets(r, sizeof r, f)) if (!strncmp(r, chiave, n)) { v = atol(r + n + 1); break; }
    fclose(f); return v;
}

/* ---------- scene ---------- */
typedef struct { float c[3], h[3], v[3], lo[3], hi[3]; } ogg_t;
#define MAXOGG 256
static ogg_t ogg[MAXOGG]; static int nogg, nogg_prima; /* nogg_prima: oggetti prima del fotogramma 150 (scena carico) */
static uint64_t seme = 0x9E3779B97F4A7C15ull;
static inline uint64_t xs(void) { seme ^= seme << 13; seme ^= seme >> 7; seme ^= seme << 17; return seme; }
static inline float unif(float a, float b) { return a + (b - a) * (float)((xs() >> 11) * (1.0 / 9007199254740992.0)); }

static void agg(float cx, float cy, float cz, float hx, float hy, float hz, float vx, float vy, float vz) {
    ogg_t *o = &ogg[nogg++];
    o->c[0] = cx; o->c[1] = cy; o->c[2] = cz; o->h[0] = hx; o->h[1] = hy; o->h[2] = hz;
    o->v[0] = vx; o->v[1] = vy; o->v[2] = vz;
    o->lo[0] = 1.0f + hx; o->hi[0] = 5.8f - hx; o->lo[1] = -1.9f + hy; o->hi[1] = 1.9f - hy;
    o->lo[2] = hz; o->hi[2] = 2.6f - hz;
}
static void scena_rada(void) {
    agg(2.5f, 0.0f, 0.85f, 0.20f, 0.25f, 0.85f, 0, 1.0f, 0);   /* persona che attraversa */
    agg(3.2f, -1.0f, 0.5f, 0.5f, 0.5f, 0.5f, 0, 0, 0);          /* cassa da 1 m */
    agg(2.0f, 0.8f, 1.0f, 0.025f, 0.5f, 1.0f, 0, 0, 0);         /* pannello largo 1 m, alto 2 m */
}
static void scaffale(float cx, float cy, int lungo_x) {
    float hl = 1.0f, hp = 0.25f;
    for (int i = 0; i < 4; i++) { float z = 0.4f + 0.5f * i;
        if (lungo_x) agg(cx, cy, z, hl, hp, 0.02f, 0, 0, 0); else agg(cx, cy, z, hp, hl, 0.02f, 0, 0, 0); }
    if (lungo_x) { agg(cx - hl, cy, 1.0f, 0.02f, hp, 1.0f, 0, 0, 0); agg(cx + hl, cy, 1.0f, 0.02f, hp, 1.0f, 0, 0, 0); }
    else { agg(cx, cy - hl, 1.0f, hp, 0.02f, 1.0f, 0, 0, 0); agg(cx, cy + hl, 1.0f, hp, 0.02f, 1.0f, 0, 0, 0); }
}
static void scena_densa(void) {
    agg(5.95f, 0, 1.5f, 0.05f, 2.0f, 1.5f, 0, 0, 0);            /* parete di fondo */
    scaffale(2.6f, 1.7f, 1); scaffale(3.6f, -1.7f, 1); scaffale(5.4f, 0.0f, 0);
    for (int i = 0; i < 20; i++) {
        float hx = unif(0.10f, 0.30f), hy = unif(0.10f, 0.30f), hz = unif(0.10f, 0.45f);
        float x = unif(1.5f, 5.3f), y = unif(-1.6f, 1.6f);
        float z = (i % 4 == 3) ? unif(0.6f, 2.0f) : hz;        /* uno su quattro e' sospeso */
        float vx = 0, vy = 0;
        if (i < 8) { vx = unif(-1.2f, 1.2f); vy = unif(-1.2f, 1.2f); }
        agg(x, y, z, hx, hy, hz, vx, vy, 0);
    }
}
static void scena_carico(void) {
    scena_rada(); nogg_prima = nogg;
    while (nogg < 200) {
        float h = unif(0.05f, 0.20f);
        agg(unif(1.0f, 5.8f), unif(-1.9f, 1.9f), unif(0.1f, 2.5f), h, unif(0.05f, 0.20f), unif(0.05f, 0.20f),
            unif(-1, 1), unif(-1, 1), unif(-0.5f, 0.5f));
    }
}
static inline float rimbalza(float p, float lo, float hi) {
    float L = hi - lo; if (L <= 0) return p;
    float m = fmodf(p - lo, 2 * L); if (m < 0) m += 2 * L;
    return lo + (m < L ? m : 2 * L - m);
}

/* ---------- sensore simulato: immagine di profondita' ---------- */
static void camera_init(void) {
    FX = (W / 2.0) / tan(HFOV_G * M_PI / 360.0); FY = (H / 2.0) / tan(VFOV_G * M_PI / 360.0);
    CXc = W / 2.0f; CYc = H / 2.0f; CT = cos(TILT_G * M_PI / 180.0); ST = sin(TILT_G * M_PI / 180.0);
    for (int u = 0; u < W; u++) ca[u] = (u + 0.5f - CXc) / FX;
    for (int v = 0; v < H; v++) { float b = (v + 0.5f - CYc) / FY; dirx[v] = CT - b * ST; dirz[v] = -ST - b * CT;
        float zf = dirz[v] < -1e-6f ? CAMZ / (-dirz[v]) : INFINITY;
        for (int u = 0; u < W; u++) zbase[v * W + u] = zf; }
}
static void genera(int k) {
    float t = k * DT; int n = (nogg_prima && k < 150) ? nogg_prima : nogg;
    memcpy(zb, zbase, sizeof zb);
    for (int i = 0; i < n; i++) {
        ogg_t *o = &ogg[i]; float c[3];
        for (int a = 0; a < 3; a++) c[a] = o->v[a] != 0 ? rimbalza(o->c[a] + o->v[a] * t, o->lo[a], o->hi[a]) : o->c[a];
        float b0[3] = { c[0] - o->h[0], c[1] - o->h[1], c[2] - o->h[2] }, b1[3] = { c[0] + o->h[0], c[1] + o->h[1], c[2] + o->h[2] };
        int u0 = W, u1 = -1, v0 = H, v1 = -1, tutto = 0;
        for (int q = 0; q < 8; q++) {
            float x = (q & 1) ? b1[0] : b0[0], y = (q & 2) ? b1[1] : b0[1], z = ((q & 4) ? b1[2] : b0[2]) - CAMZ;
            float zc = x * CT - z * ST; if (zc < 0.1f) { tutto = 1; break; }
            float uu = CXc + FX * (-y) / zc, vv = CYc + FY * (-x * ST - z * CT) / zc;
            int iu = (int)floorf(uu), iv = (int)floorf(vv);
            if (iu - 1 < u0) u0 = iu - 1; if (iu + 1 > u1) u1 = iu + 1; if (iv - 1 < v0) v0 = iv - 1; if (iv + 1 > v1) v1 = iv + 1;
        }
        if (tutto) { u0 = 0; u1 = W - 1; v0 = 0; v1 = H - 1; }
        if (u0 < 0) u0 = 0; if (v0 < 0) v0 = 0; if (u1 > W - 1) u1 = W - 1; if (v1 > H - 1) v1 = H - 1;
        for (int v = v0; v <= v1; v++) {
            float dx = dirx[v], dz = dirz[v];
            float tx0 = b0[0] / dx, tx1 = b1[0] / dx;                      /* dx > 0 sempre */
            float tz0 = (b0[2] - CAMZ) / dz, tz1 = (b1[2] - CAMZ) / dz; if (tz0 > tz1) { float s = tz0; tz0 = tz1; tz1 = s; }
            float ta = tx0 > tz0 ? tx0 : tz0, tb = tx1 < tz1 ? tx1 : tz1; if (ta > tb) continue;
            for (int u = u0; u <= u1; u++) {
                float dy = -ca[u]; float ty0 = b0[1] / dy, ty1 = b1[1] / dy; if (ty0 > ty1) { float s = ty0; ty0 = ty1; ty1 = s; }
                float t0 = ta > ty0 ? ta : ty0, t1 = tb < ty1 ? tb : ty1;
                if (t0 <= t1 && t0 > 0.05f && t0 < zb[v * W + u]) zb[v * W + u] = t0;
            }
        }
    }
    uint64_t s = 0xD1B54A32D192ED03ull * (uint64_t)(k + 1) + 0x12345;
    for (int i = 0; i < W * H; i++) {
        s ^= s << 13; s ^= s >> 7; s ^= s << 17;
        float z = zb[i];
        if (!(z < 1e9f) || (s & 0xFF) < 3) { D[i] = 0; continue; }              /* senza ritorno, o buco (1,2 %) */
        float g = ((float)((s >> 8) & 0xFFFF) + (float)((s >> 24) & 0xFFFF) + (float)((s >> 40) & 0xFFFF) - 98302.5f) * (1.0f / 32767.5f);
        z += 0.0025f * z * z * g;                                              /* rumore ~ z^2: 1 cm a 2 m, 4 cm a 4 m */
        int mm = (int)(z * 1000.0f + 0.5f);
        D[i] = (mm <= 0 || mm > ZMAX_MM) ? 0 : (uint16_t)mm;
    }
}

/* ---------- voxel comune (4 byte) ---------- */
typedef struct { int8_t lo; uint8_t occ; uint16_t seen; } vox_t;
static inline void w_free(vox_t *v, uint16_t f) { if (v->seen == f) return; v->seen = f; v->occ = 0; if (v->lo > -8) v->lo--; }
static inline void w_occ(vox_t *v, uint16_t f) { if (v->seen == f && v->occ) return; v->seen = f; v->occ = 1; v->lo = v->lo > 4 ? 7 : (int8_t)(v->lo + 3); }

/* ---------- strutture ---------- */
#if REP == R_DENSA
static vox_t *G;
static void st_init(void) { size_t n = (size_t)NX * NY * NZ; G = calloc(n, sizeof(vox_t)); mem_struttura = n * sizeof(vox_t); }
static inline vox_t *acc_w(int x, int y, int z) { return &G[((size_t)z * NY + y) * NX + x]; }
static inline const vox_t *acc_r(int x, int y, int z) { return &G[((size_t)z * NY + y) * NX + x]; }
static void st_fine_fotogramma(void) {}
static size_t st_mem(void) { return mem_struttura; }
static uint32_t st_unita(void) { return (uint32_t)(NX * NY * NZ); }

#elif REP == R_HASH || REP == R_HASHOCC
static uint32_t *hk, *hv, hmask, nblk, maxblk; static int hshift;
static vox_t *bpool, *c_blk; static uint32_t c_key = 0xFFFFFFFFu;
static void st_init(void) {
    maxblk = (uint32_t)(((NX + 7) / 8) * ((NY + 7) / 8) * ((NZ + 7) / 8));
    uint32_t ts = 1; int lg = 0; while (ts < 2 * maxblk) { ts <<= 1; lg++; }
    hmask = ts - 1; hshift = 32 - lg; hk = calloc(ts, 4); hv = calloc(ts, 4); mem_indice = (size_t)ts * 8;
    bpool = calloc((size_t)maxblk * 512, sizeof(vox_t));   /* riservato: le pagine non toccate non sono residenti */
}
static inline vox_t *blk_find(uint32_t key, int crea) {
    uint32_t h = (key * 2654435761u) >> hshift;
    for (;;) { uint32_t k = hk[h];
        if (k == key + 1) return bpool + (size_t)hv[h] * 512;
        if (!k) { if (!crea) return NULL; hk[h] = key + 1; hv[h] = nblk; return bpool + (size_t)(nblk++) * 512; }
        h = (h + 1) & hmask; }
}
static inline vox_t *acc_w(int x, int y, int z) {
    uint32_t key = (uint32_t)(x >> 3) | ((uint32_t)(y >> 3) << 8) | ((uint32_t)(z >> 3) << 16);
    if (key != c_key || !c_blk) { c_key = key; c_blk = blk_find(key, 1); }
    return c_blk + (((z & 7) << 6) | ((y & 7) << 3) | (x & 7));
}
static inline const vox_t *acc_r(int x, int y, int z) {
    uint32_t key = (uint32_t)(x >> 3) | ((uint32_t)(y >> 3) << 8) | ((uint32_t)(z >> 3) << 16);
    if (key != c_key) { c_key = key; c_blk = blk_find(key, 0); }
    return c_blk ? c_blk + (((z & 7) << 6) | ((y & 7) << 3) | (x & 7)) : NULL;
}
static void st_fine_fotogramma(void) {}
static size_t st_mem(void) { return (size_t)nblk * 512 * sizeof(vox_t) + mem_indice; }
static uint32_t st_unita(void) { return nblk; }

#elif REP == R_OCTREE || REP == R_OCTPOT
typedef struct { uint32_t child; vox_t val; } nodo_t;    /* 8 byte; i figli si allocano a otto a otto */
static nodo_t *pool; static uint32_t prossimo = 8, alto = 8, *liberi, nliberi, in_uso = 1; static int PROF;
static uint32_t picco_in_uso = 1; static uint64_t somma_fine; static uint32_t nfine;
static void st_init(void) {
    int m = NX > NY ? NX : NY; if (NZ > m) m = NZ; PROF = 0; while ((1 << PROF) < m) PROF++;
    size_t cap = 8; for (int l = 1; l <= PROF; l++) cap += (size_t)1 << (3 * l);
    pool = calloc(cap, sizeof(nodo_t)); liberi = calloc(cap / 8 + 1, 4);
}
static inline uint32_t alloc8(void) {
    uint32_t c; if (nliberi) c = liberi[--nliberi]; else { c = prossimo; prossimo += 8; if (prossimo > alto) alto = prossimo; }
    in_uso += 8; if (in_uso > picco_in_uso) picco_in_uso = in_uso; return c;
}
static inline vox_t *acc_w(int x, int y, int z) {
    uint32_t n = 0;
    for (int l = PROF - 1; l >= 0; l--) {
        nodo_t *p = &pool[n];
        if (!p->child) { uint32_t c = alloc8(); for (int i = 0; i < 8; i++) { pool[c + i].child = 0; pool[c + i].val = p->val; } p->child = c; }
        n = p->child + (uint32_t)(((x >> l) & 1) | (((y >> l) & 1) << 1) | (((z >> l) & 1) << 2));
    }
    return &pool[n].val;
}
static inline const vox_t *acc_r(int x, int y, int z) {
    uint32_t n = 0;
    for (int l = PROF - 1; l >= 0; l--) { const nodo_t *p = &pool[n]; if (!p->child) break;
        n = p->child + (uint32_t)(((x >> l) & 1) | (((y >> l) & 1) << 1) | (((z >> l) & 1) << 2)); }
    return pool[n].val.seen ? &pool[n].val : NULL;
}
#if REP == R_OCTPOT
static int pota(uint32_t n) {
    nodo_t *p = &pool[n]; if (!p->child) return 1;
    int tutte = 1; uint32_t c = p->child;
    for (int i = 0; i < 8; i++) tutte &= pota(c + i);
    if (!tutte) return 0;
    for (int i = 1; i < 8; i++) if (memcmp(&pool[c].val, &pool[c + i].val, sizeof(vox_t))) return 0;
    p->val = pool[c].val; p->child = 0; liberi[nliberi++] = c; in_uso -= 8; return 1;
}
static void st_fine_fotogramma(void) { pota(0); somma_fine += in_uso; nfine++; }
#else
static void st_fine_fotogramma(void) { somma_fine += in_uso; nfine++; }
#endif
/* memoria: alto livello del serbatoio dei nodi + lista dei blocchi liberi */
static size_t st_mem(void) { return (size_t)alto * sizeof(nodo_t) + (REP == R_OCTPOT ? (size_t)(alto / 8) * 4 : 0); }
static uint32_t st_unita(void) { return in_uso; }

#elif REP == R_FASCE
typedef struct { uint16_t seen, occ_seen; uint8_t zlo, zhi; } fascia_t;   /* 6 byte */
static fascia_t *Fz; static uint16_t *suolo; static float bordo[64];
static void st_init(void) {
    size_t n = (size_t)NX * NY; Fz = calloc(n * NFASCE, sizeof(fascia_t)); suolo = calloc(n, 2);
    mem_struttura = n * NFASCE * sizeof(fascia_t) + n * 2;
    if (NFASCE == 3) { bordo[0] = 0.15f; bordo[1] = 0.60f; bordo[2] = 1.60f; bordo[3] = ROIZ; }
    else for (int i = 0; i <= NFASCE; i++) bordo[i] = ROIZ * i / NFASCE;
}
static inline int banda(float z) {
    if (NFASCE == 3) return z < 0.15f ? -1 : z < 0.60f ? 0 : z < 1.60f ? 1 : 2;
    int b = (int)(z * (NFASCE / ROIZ)); return b >= NFASCE ? NFASCE - 1 : b;
}
static inline uint8_t quant(float z) { int q = (int)(z * (255.0f / ROIZ)); return (uint8_t)(q < 0 ? 0 : q > 255 ? 255 : q); }
static inline void segna(int cella, float z0, float z1, uint16_t f) {
    float zl = z0 < z1 ? z0 : z1, zh = z0 < z1 ? z1 : z0; int b0 = banda(zl), b1 = banda(zh);
    for (int b = b0 < 0 ? 0 : b0; b <= b1; b++) {
        fascia_t *p = &Fz[(size_t)cella * NFASCE + b];
        if (p->seen != f) { p->seen = f; p->zlo = 255; p->zhi = 0; }
        uint8_t ql = quant(zl > bordo[b] ? zl : bordo[b]), qh = quant(zh < bordo[b + 1] ? zh : bordo[b + 1]);
        if (ql < p->zlo) p->zlo = ql; if (qh > p->zhi) p->zhi = qh;
    }
}
static void st_fine_fotogramma(void) {}
static size_t st_mem(void) { return mem_struttura; }
static uint32_t st_unita(void) { return (uint32_t)(NX * NY * NFASCE); }

#elif REP == R_COLBIT
typedef struct { uint32_t lib, occ; uint16_t seen, pad; } col_t;   /* 12 byte: 30 livelli di quota da 10 cm in due maschere di bit */
static col_t *Cb;
static void st_init(void) { size_t n = (size_t)NX * NY; Cb = calloc(n, sizeof(col_t)); mem_struttura = n * sizeof(col_t); }
static inline void segna(int cella, float z0, float z1, uint16_t f) {
    float zl = z0 < z1 ? z0 : z1, zh = z0 < z1 ? z1 : z0; int lo = (int)(zl * 10.0f), hi = (int)(zh * 10.0f);
    if (lo < 0) lo = 0; if (hi > 29) hi = 29;
    col_t *c = &Cb[cella]; if (c->seen != f) { c->seen = f; c->lib = 0; c->occ = 0; }
    c->lib |= (0xFFFFFFFFu >> (31 - hi)) & (0xFFFFFFFFu << lo);
}
static void st_fine_fotogramma(void) {}
static size_t st_mem(void) { return mem_struttura; }
static uint32_t st_unita(void) { return (uint32_t)(NX * NY); }

#elif REP == R_POLARE
#define NA 87
static int NR; typedef struct { uint16_t suolo_seen; uint8_t stato, pad; } cella_t;   /* 4 byte */
static cella_t *P; static float rmin[NA]; static uint8_t *azlut; static float *rhlut;
static void st_init(void) {
    NR = (int)(PORTATA * 10.0f + 0.5f); P = calloc((size_t)NA * NR, sizeof(cella_t));
    mem_struttura = (size_t)NA * NR * sizeof(cella_t) + sizeof rmin;
    azlut = malloc(W * H); rhlut = malloc(sizeof(float) * W * H); mem_tabelle = (size_t)W * H * 5;
    for (int v = 0; v < H; v++) for (int u = 0; u < W; u++) {
        float x = dirx[v], y = -ca[u]; float az = atan2f(y, x) * (180.0f / (float)M_PI) + 43.5f;
        azlut[v * W + u] = (az < 0 || az >= NA) ? 255 : (uint8_t)az; rhlut[v * W + u] = sqrtf(x * x + y * y);
    }
}
static void st_fine_fotogramma(void) {}
static size_t st_mem(void) { return mem_struttura; }
static uint32_t st_unita(void) { return (uint32_t)(NA * NR); }

#elif REP == R_IMMAGINE
static uint16_t *Dmin, *Dmax, *tmpa, *tmpb;
static void st_init(void) { Dmin = calloc(W * H, 2); Dmax = calloc(W * H, 2); tmpa = calloc(W * H, 2); tmpb = calloc(W * H, 2);
    mem_struttura = (size_t)W * H * 2 * 4; }
static void st_fine_fotogramma(void) {}
static size_t st_mem(void) { return mem_struttura; }
static uint32_t st_unita(void) { return W * H; }
#endif

/* ---------- aggiornamento ---------- */
#if E_VOXEL && REP != R_HASHOCC
static inline void lancia(float px, float py, float pz, uint16_t f) {
    const float ox = 1e-4f, oy = 1e-4f, oz = CAMZ + 1e-4f;
    if (pz < 0.001f) pz = 0.001f;
    float dx = px - ox, dy = py - oy, dz = pz - oz, te = 1.0f; int dentro = 1;
    if (px >= ROIX) { float t = (ROIX - ox) / dx; if (t < te) te = t; dentro = 0; }
    if (py >= HY) { float t = (HY - oy) / dy; if (t < te) te = t; dentro = 0; }
    else if (py <= -HY) { float t = (-HY - oy) / dy; if (t < te) te = t; dentro = 0; }
    if (pz >= ROIZ) { float t = (ROIZ - oz) / dz; if (t < te) te = t; dentro = 0; }
    if (!dentro) { te *= 0.9999f; px = ox + dx * te; py = oy + dy * te; pz = oz + dz * te; }
    float gx0 = ox * INV, gy0 = (oy + HY) * INV, gz0 = oz * INV, gx1 = px * INV, gy1 = (py + HY) * INV, gz1 = pz * INV;
    int ix = (int)gx0, iy = (int)gy0, iz = (int)gz0, ex = (int)gx1, ey = (int)gy1, ez = (int)gz1;
    if (ex < 0) ex = 0; if (ex >= NX) ex = NX - 1; if (ey < 0) ey = 0; if (ey >= NY) ey = NY - 1; if (ez < 0) ez = 0; if (ez >= NZ) ez = NZ - 1;
    float gdx = gx1 - gx0, gdy = gy1 - gy0, gdz = gz1 - gz0;
    int nx = abs(ex - ix), ny = abs(ey - iy), nz = abs(ez - iz);
    int sx = ex > ix ? 1 : -1, sy = ey > iy ? 1 : -1, sz = ez > iz ? 1 : -1;
    float tdx = nx ? fabsf(1.0f / gdx) : INFINITY, tdy = ny ? fabsf(1.0f / gdy) : INFINITY, tdz = nz ? fabsf(1.0f / gdz) : INFINITY;
    float tmx = nx ? (sx > 0 ? (ix + 1 - gx0) : (gx0 - ix)) * tdx : INFINITY;
    float tmy = ny ? (sy > 0 ? (iy + 1 - gy0) : (gy0 - iy)) * tdy : INFINITY;
    float tmz = nz ? (sz > 0 ? (iz + 1 - gz0) : (gz0 - iz)) * tdz : INFINITY;
    int n = nx + ny + nz; n_passi += (uint64_t)n;
    for (int k = 0; k < n; k++) {
        w_free(acc_w(ix, iy, iz), f);
        if (tmx <= tmy && tmx <= tmz) { ix += sx; tmx = --nx ? tmx + tdx : INFINITY; }
        else if (tmy <= tmz) { iy += sy; tmy = --ny ? tmy + tdy : INFINITY; }
        else { iz += sz; tmz = --nz ? tmz + tdz : INFINITY; }
    }
    vox_t *e = acc_w(ix, iy, iz); if (dentro) w_occ(e, f); else w_free(e, f);
}
#endif
#if REP == R_FASCE || REP == R_COLBIT
static inline void lancia(float px, float py, float pz, uint16_t f) {
    const float ox = 1e-4f, oy = 1e-4f, oz = CAMZ + 1e-4f;
    if (pz < 0.001f) pz = 0.001f;
    float dx = px - ox, dy = py - oy, dz = pz - oz, te = 1.0f; int dentro = 1;
    if (px >= ROIX) { float t = (ROIX - ox) / dx; if (t < te) te = t; dentro = 0; }
    if (py >= HY) { float t = (HY - oy) / dy; if (t < te) te = t; dentro = 0; }
    else if (py <= -HY) { float t = (-HY - oy) / dy; if (t < te) te = t; dentro = 0; }
    if (pz >= ROIZ) { float t = (ROIZ - oz) / dz; if (t < te) te = t; dentro = 0; }
    if (!dentro) { te *= 0.9999f; px = ox + dx * te; py = oy + dy * te; pz = oz + dz * te; dz = pz - oz; }
    float gx0 = ox * INV, gy0 = (oy + HY) * INV, gx1 = px * INV, gy1 = (py + HY) * INV;
    int ix = (int)gx0, iy = (int)gy0, ex = (int)gx1, ey = (int)gy1;
    if (ex < 0) ex = 0; if (ex >= NX) ex = NX - 1; if (ey < 0) ey = 0; if (ey >= NY) ey = NY - 1;
    float gdx = gx1 - gx0, gdy = gy1 - gy0;
    int nx = abs(ex - ix), ny = abs(ey - iy), sx = ex > ix ? 1 : -1, sy = ey > iy ? 1 : -1;
    float tdx = nx ? fabsf(1.0f / gdx) : INFINITY, tdy = ny ? fabsf(1.0f / gdy) : INFINITY;
    float tmx = nx ? (sx > 0 ? (ix + 1 - gx0) : (gx0 - ix)) * tdx : INFINITY;
    float tmy = ny ? (sy > 0 ? (iy + 1 - gy0) : (gy0 - iy)) * tdy : INFINITY;
    int n = nx + ny; n_passi += (uint64_t)n; float t = 0, z0 = oz;
    for (int k = 0; k < n; k++) {
        int cella = iy * NX + ix;
        if (tmx <= tmy) { t = tmx; ix += sx; tmx = --nx ? tmx + tdx : INFINITY; }
        else { t = tmy; iy += sy; tmy = --ny ? tmy + tdy : INFINITY; }
        float z1 = oz + t * dz; segna(cella, z0, z1, f); z0 = z1;
    }
    int cella = iy * NX + ix; segna(cella, z0, pz, f);
#if REP == R_FASCE
    if (dentro) { int b = banda(pz); if (b < 0) suolo[cella] = f; else Fz[(size_t)cella * NFASCE + b].occ_seen = f; }
#else
    if (dentro) { int l = (int)(pz * 10.0f); if (l > 29) l = 29; Cb[cella].occ |= 1u << l; }
#endif
}
#endif

static void aggiorna(uint16_t f) {
#if REP == R_POLARE
    for (int a = 0; a < NA; a++) rmin[a] = 1e9f;
    for (int v = PASSO / 2; v < H; v += PASSO) {
        float ddz = dirz[v]; const uint16_t *riga = D + v * W; const uint8_t *az = azlut + v * W; const float *rh = rhlut + v * W;
        for (int u = PASSO / 2; u < W; u += PASSO) {
            uint16_t d = riga[u]; if (!d) continue; int a = az[u]; if (a == 255) continue;
            float z = d * 0.001f, h = CAMZ + z * ddz, r = z * rh[u]; n_raggi++;
            if (r >= PORTATA) continue;
            if (h >= 0.07f) { if (h <= 2.0f && r < rmin[a]) rmin[a] = r; }
            else if (h > -0.07f) { int rb = (int)(r * 10.0f); if (rb >= NR) rb = NR - 1; P[a * NR + rb].suolo_seen = f; }
        }
    }
    for (int a = 0; a < NA; a++) {
        int ro = rmin[a] < PORTATA ? (int)(rmin[a] * 10.0f) : NR; cella_t *c = P + a * NR;
        for (int r = 0; r < NR; r++)
            c[r].stato = r < ro ? ((c[r].suolo_seen && c[r].suolo_seen + 2 >= f) ? 1 : 0) : r == ro ? 2 : 3;   /* 0 non oss., 1 libero, 2 occupato, 3 ombra */
    }
#elif REP == R_IMMAGINE
    (void)f;   /* minimo e massimo 3x3, separabili, sull'immagine intera (non dipende dal passo); 0 = non valido si propaga nel minimo */
    for (int v = 0; v < H; v++) { const uint16_t *r = D + v * W; uint16_t *a = tmpa + v * W, *b = tmpb + v * W;
        for (int u = 0; u < W; u++) { int ul = u ? u - 1 : 0, ur = u < W - 1 ? u + 1 : u; uint16_t x = r[ul], y = r[u], z = r[ur];
            uint16_t mn = x < y ? x : y; if (z < mn) mn = z; uint16_t mx = x > y ? x : y; if (z > mx) mx = z; a[u] = mn; b[u] = mx; } }
    for (int v = 0; v < H; v++) { int vu = v ? v - 1 : 0, vd = v < H - 1 ? v + 1 : v;
        const uint16_t *a0 = tmpa + vu * W, *a1 = tmpa + v * W, *a2 = tmpa + vd * W, *b0 = tmpb + vu * W, *b1 = tmpb + v * W, *b2 = tmpb + vd * W;
        uint16_t *o = Dmin + v * W, *p = Dmax + v * W;
        for (int u = 0; u < W; u++) { uint16_t mn = a0[u] < a1[u] ? a0[u] : a1[u]; if (a2[u] < mn) mn = a2[u];
            uint16_t mx = b0[u] > b1[u] ? b0[u] : b1[u]; if (b2[u] > mx) mx = b2[u]; o[u] = mn; p[u] = mx; } }
    n_raggi += W * H;
#elif REP == R_HASHOCC
    for (int v = PASSO / 2; v < H; v += PASSO) {
        float ddx = dirx[v], ddz = dirz[v]; const uint16_t *riga = D + v * W;
        for (int u = PASSO / 2; u < W; u += PASSO) {
            uint16_t d = riga[u]; if (!d) continue; float z = d * 0.001f, px = z * ddx, py = -z * ca[u], pz = CAMZ + z * ddz; n_raggi++;
            if (pz < 0.07f || pz >= ROIZ || px >= ROIX || py >= HY || py <= -HY) continue;      /* solo l'occupato sopra il suolo */
            w_occ(acc_w((int)(px * INV), (int)((py + HY) * INV), (int)(pz * INV)), f);
        }
    }
#else
    for (int v = PASSO / 2; v < H; v += PASSO) {
        float ddx = dirx[v], ddz = dirz[v]; const uint16_t *riga = D + v * W;
        for (int u = PASSO / 2; u < W; u += PASSO) {
            uint16_t d = riga[u]; if (!d) continue; float z = d * 0.001f; n_raggi++;
            lancia(z * ddx, -z * ca[u], CAMZ + z * ddz, f);
        }
    }
#endif
    st_fine_fotogramma();
}

/* ---------- interrogazione: 18 settori da 5 gradi ---------- */
static uint8_t tab[NSET * NRQ]; static int32_t *colsec; static float d_occ[NSET], d_lib[NSET];
static void q_init(void) {
#if E_VOXEL || REP == R_FASCE || REP == R_COLBIT
    colsec = malloc(sizeof(int32_t) * NX * NY);
    for (int iy = 0; iy < NY; iy++) for (int ix = 0; ix < NX; ix++) {
        float x = (ix + 0.5f) * RES, y = (iy + 0.5f) * RES - HY, az = atan2f(y, x) * (180.0f / (float)M_PI) + 45.0f, r = sqrtf(x * x + y * y);
        int s = (int)(az / 5.0f), rb = (int)(r * 10.0f);
        colsec[iy * NX + ix] = (az < 0 || s >= NSET || rb >= NRQ) ? -1 : s * NRQ + rb;
    }
#endif
}
/* bit della tabella: 1 = c'e' del non osservato, 2 = c'e' dell'occupato, 4 = toccata */
static double interroga(uint16_t f) {
    memset(tab, 0, sizeof tab);
#if E_VOXEL
    int z0 = (int)(QZ0 * INV + 0.5f), z1 = (int)(QZ1 * INV + 0.5f);
    for (int iy = 0; iy < NY; iy++) for (int ix = 0; ix < NX; ix++) {
        int idx = colsec[iy * NX + ix]; if (idx < 0) continue; uint8_t b = 4;
        for (int iz = z0; iz < z1; iz++) { const vox_t *v = acc_r(ix, iy, iz);
            if (!v || (uint16_t)(v->seen + 2) < f || !v->seen) b |= 1; else if (v->occ && v->seen == f) b |= 2; }
        tab[idx] |= b;
    }
#elif REP == R_FASCE
    for (int iy = 0; iy < NY; iy++) for (int ix = 0; ix < NX; ix++) {
        int cella = iy * NX + ix, idx = colsec[cella]; if (idx < 0) continue; uint8_t b = 4;
        for (int k = 0; k < NFASCE; k++) { if (bordo[k + 1] <= QZ0 || bordo[k] >= QZ1) continue;
            const fascia_t *p = &Fz[(size_t)cella * NFASCE + k];
            if (p->occ_seen == f) { b |= 2; continue; }
            float hi = bordo[k + 1] < QZ1 ? bordo[k + 1] : QZ1;
            if (p->seen != f || p->zlo > quant(bordo[k]) + 2 || p->zhi + 2 < quant(hi)) b |= 1; }
        tab[idx] |= b;
    }
#elif REP == R_COLBIT
    const uint32_t BANDA = 0x000FFFFEu;   /* livelli 1..19: quote 0,1-2,0 m */
    for (int i = 0; i < NX * NY; i++) { int idx = colsec[i]; if (idx < 0) continue; const col_t *c = &Cb[i]; uint8_t b = 4;
        if (c->seen != f) b |= 1; else if (c->occ & BANDA) b |= 2; else if ((c->lib & BANDA) != BANDA) b |= 1;
        tab[idx] |= b; }
#elif REP == R_POLARE
    for (int s = 0; s < NSET; s++) for (int k = 0; k < 5; k++) { int a = s * 5 + k - 1; if (a < 0 || a >= NA) continue;   /* 87 gradi dentro 90 */
        const cella_t *c = P + a * NR;
        for (int r = 0; r < NR && r < NRQ; r++) tab[s * NRQ + r] |= (uint8_t)(4 | (c[r].stato == 2 ? 2 : c[r].stato == 1 ? 0 : 1)); }
#elif REP == R_IMMAGINE
    (void)f;
    for (int s = 0; s < NSET; s++) for (int k = 0; k < 5; k++) {
        float az = (s * 5 + k + 0.5f - 45.0f) * ((float)M_PI / 180.0f), cz = cosf(az), sz = sinf(az);
        for (int r = 0; r < NRQ; r++) { float rr = (r + 0.5f) * 0.1f, x = rr * cz, y = rr * sz; uint8_t b = 4;
            for (int q = 0; q < 20; q++) { float zz = QZ0 + 0.05f + 0.095f * q - CAMZ;
                float zc = x * CT - zz * ST; if (zc < 0.1f) { b |= 1; continue; }
                float iz = 1.0f / zc; int u = (int)(CXc + FX * (-y) * iz), v = (int)(CYc + FY * (-x * ST - zz * CT) * iz);
                if ((unsigned)u >= W || (unsigned)v >= H) { b |= 1; continue; }
                uint16_t mn = Dmin[v * W + u], mx = Dmax[v * W + u]; if (!mn) { b |= 1; continue; }
                float m = 0.05f + 0.0075f * zc * zc, lo = mn * 0.001f - m, hi = mx * 0.001f + m;
                if (zc < lo) continue; if (zc <= hi) b |= 2; else b |= 1; }
            tab[s * NRQ + r] |= b; }
    }
#endif
    double somma = 0;
    for (int s = 0; s < NSET; s++) { d_occ[s] = -1; d_lib[s] = -1; int libero = 1;
        for (int r = 13; r < NRQ; r++) { uint8_t b = tab[s * NRQ + r];
            if ((b & 2) && d_occ[s] < 0) d_occ[s] = r * 0.1f;
            if (libero && (b != 4)) { libero = 0; d_lib[s] = r * 0.1f; } }
        if (libero) d_lib[s] = NRQ * 0.1f;
        somma += d_occ[s] + 10.0 * d_lib[s]; }
    return somma;
}

/* ---------- statistiche ---------- */
static int cmp64(const void *a, const void *b) { uint64_t x = *(const uint64_t *)a, y = *(const uint64_t *)b; return x < y ? -1 : x > y; }
typedef struct { double media, p50, p95, p99, max; } stat_t;
static stat_t stat(const uint64_t *t, int da, int a) {
    stat_t s = { 0, 0, 0, 0, 0 }; int n = a - da; if (n <= 0) return s;
    uint64_t *c = malloc(sizeof(uint64_t) * n); memcpy(c, t + da, sizeof(uint64_t) * n); qsort(c, n, sizeof(uint64_t), cmp64);
    double sm = 0; for (int i = 0; i < n; i++) sm += c[i];
    s.media = sm / n; s.p50 = c[(n - 1) / 2]; s.p95 = c[(int)ceil(0.95 * n) - 1]; s.p99 = c[(int)ceil(0.99 * n) - 1]; s.max = c[n - 1];
    free(c); return s;
}

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "uso: %s scena res_cm passo fotogrammi [fasce] [portata_polare]\n", argv[0]); return 2; }
    const char *scena = argv[1]; int res_cm = atoi(argv[2]); PASSO = atoi(argv[3]); int nf = atoi(argv[4]);
    if (argc > 5) NFASCE = atoi(argv[5]); if (argc > 6) PORTATA = atof(argv[6]);
    RES = res_cm * 0.01f; INV = 1.0f / RES; NX = (int)(ROIX * INV + 0.5f); NY = (int)(2 * HY * INV + 0.5f); NZ = (int)(ROIZ * INV + 0.5f);
    if (!getenv("BANCO_THP")) prctl(PR_SET_THP_DISABLE, 1, 0, 0, 0);   /* pagine da 4 kB: la memoria residente misura cio' che si tocca */
    camera_init();
    if (!strcmp(scena, "rada")) scena_rada(); else if (!strcmp(scena, "densa")) scena_densa(); else if (!strcmp(scena, "carico")) scena_carico();
    else if (strcmp(scena, "vuota")) { fprintf(stderr, "scena ignota\n"); return 2; }
    uint64_t *ta = malloc(sizeof(uint64_t) * nf), *tq = malloc(sizeof(uint64_t) * nf); memset(ta, 1, sizeof(uint64_t) * nf); memset(tq, 1, sizeof(uint64_t) * nf);
    uint32_t *un = malloc(4 * nf); memset(un, 0, 4 * nf);
    genera(0);
    long rss0 = leggi_stato("VmRSS:");
    st_init(); q_init();
    double somma = 0; uint64_t passi150 = 0, raggi150 = 0;
    for (int k = 0; k < nf; k++) {
        genera(k); uint16_t f = (uint16_t)(k + 1);
        uint64_t p0 = n_passi, r0 = n_raggi;
        uint64_t t0 = ora(); aggiorna(f); uint64_t t1 = ora(); somma += interroga(f); uint64_t t2 = ora();
        ta[k] = t1 - t0; tq[k] = t2 - t1; un[k] = st_unita();
        if (k == 150) { passi150 = n_passi - p0; raggi150 = n_raggi - r0; }
    }
    long hwm = leggi_stato("VmHWM:");
    int caldo = nf > 20 ? 5 : 0; stat_t sa = stat(ta, caldo, nf), sq = stat(tq, caldo, nf);
    static const char *nomi[] = { "", "polare", "immagine", "fasce", "densa", "hash8", "hash8_solo_occ", "octree", "octree_pot" };
#if REP == R_COLBIT
    printf("rep=colonne_bit scena=%s res_cm=%d passo=%d fotogrammi=%d", scena, res_cm, PASSO, nf);
#else
    printf("rep=%s scena=%s res_cm=%d passo=%d fotogrammi=%d", nomi[REP], scena, res_cm, PASSO, nf);
#endif
#if REP == R_FASCE
    printf(" fasce=%d", NFASCE);
#endif
#if REP == R_POLARE
    printf(" portata=%.0f", PORTATA);
#endif
    printf(" raggi_f=%.0f passi_f=%.0f", (double)n_raggi / nf, (double)n_passi / nf);
    printf(" agg_media_ms=%.4f agg_p50_ms=%.4f agg_p95_ms=%.4f agg_p99_ms=%.4f agg_max_ms=%.4f agg_primo_ms=%.4f",
           sa.media / 1e6, sa.p50 / 1e6, sa.p95 / 1e6, sa.p99 / 1e6, sa.max / 1e6, ta[0] / 1e6);
    if (n_passi) printf(" ns_passo=%.3f", sa.media * nf / (double)n_passi);
    printf(" int_media_us=%.3f int_p95_us=%.3f int_max_us=%.3f", sq.media / 1e3, sq.p95 / 1e3, sq.max / 1e3);
    printf(" mem_B=%zu mem_indice_B=%zu mem_tabelle_B=%zu unita=%u rss_delta_kB=%ld", st_mem(), mem_indice, mem_tabelle, st_unita(), hwm - rss0);
#if REP == R_OCTREE || REP == R_OCTPOT
    printf(" nodi_picco=%u nodi_fine_media=%.0f", picco_in_uso, (double)somma_fine / nfine);
#endif
    if (!strcmp(scena, "carico") && nf > 160) {
        stat_t pr = stat(ta, 5, 150), do_ = stat(ta, 151, nf);
        printf(" prima_p50_ms=%.4f prima_max_ms=%.4f t150_ms=%.4f dopo_p50_ms=%.4f dopo_max_ms=%.4f unita_149=%u unita_150=%u unita_fine=%u raggi150=%llu passi150=%llu",
               pr.p50 / 1e6, pr.max / 1e6, ta[150] / 1e6, do_.p50 / 1e6, do_.max / 1e6, un[149], un[150], un[nf - 1],
               (unsigned long long)raggi150, (unsigned long long)passi150);
    }
    printf(" somma=%.1f\n", somma);
    return 0;
}
