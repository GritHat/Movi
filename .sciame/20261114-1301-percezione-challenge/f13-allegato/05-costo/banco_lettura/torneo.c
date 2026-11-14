// torneo.c — banco dell'avversario per l'estensione f7 (torneo dei falsificatori).
// Autore: sciame-avversario. Nessuna riga presa dai sorgenti delle corsie.
// Compilare: gcc -O2 -o torneo torneo.c -lm      Uso: ./torneo <prova> [argomenti]   (semi fissi)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>

#define W 320
#define H 240
#define NPIX (W * H)
#define CAMH 1.2
#define ZMAX 6.0
#define RG 3.0
#define NA 87
#define NR 30
#define DEG (M_PI / 180.0)
enum { UNK = 0, LIB = 1, OCC = 2, OMB = 3 };

// ---------- casuale ----------
static uint64_t rs = 88172645463325252ULL;
static void seme(uint64_t s) { rs = s * 2654435761ULL + 88172645463325252ULL; }
static double uni(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
static double gau(void) { double u = uni() + 1e-300, v = uni(); return sqrt(-2 * log(u)) * cos(2 * M_PI * v); }
static double adesso(void) { struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t); return t.tv_sec * 1e3 + t.tv_nsec * 1e-6; }

// ---------- scena ----------
typedef struct { double lo[3], hi[3]; int kind, on; } Box; // kind 0 fisso, 1 soggetto, 2 vetro
#define MAXB 40
static Box B[MAXB];
static int nb = 0, stanza = 1;
static void box(int i, double x0, double x1, double y0, double y1, double z0, double z1, int kind) {
    B[i].lo[0] = x0; B[i].hi[0] = x1; B[i].lo[1] = y0; B[i].hi[1] = y1; B[i].lo[2] = z0; B[i].hi[2] = z1; B[i].kind = kind; B[i].on = 1;
    if (i >= nb) nb = i + 1;
}
static void centro(int i, double cx, double cy, double w, double d, double h, int kind) { box(i, cx - w / 2, cx + w / 2, cy - d / 2, cy + d / 2, 0, h, kind); }

// ---------- camera ----------
static const double cpos[3] = {0, 0, CAMH};
static double tf[3], tr[3], tu[3]; // assi veri
static double ef[3], er[3], eu[3]; // assi stimati (imbardata 0)
static double THX, THY, txs[W], tys[H];
static double SP, CP;
static void assi(double yaw, double f[3], double r[3], double u[3]) {
    f[0] = sin(yaw) * CP; f[1] = cos(yaw) * CP; f[2] = -SP;
    r[0] = cos(yaw); r[1] = -sin(yaw); r[2] = 0;
    u[0] = sin(yaw) * SP; u[1] = cos(yaw) * SP; u[2] = CP;
}
static void initcam(void) {
    SP = sin(15 * DEG); CP = cos(15 * DEG); THX = tan(43.5 * DEG); THY = tan(29 * DEG);
    for (int i = 0; i < W; i++) txs[i] = ((i + 0.5) - W / 2.0) / (W / 2.0) * THX;
    for (int j = 0; j < H; j++) tys[j] = (H / 2.0 - (j + 0.5)) / (H / 2.0) * THY;
    assi(0, tf, tr, tu); assi(0, ef, er, eu);
}
// raggio contro la scena; t e' la profondita' lungo l'asse ottico se d = f + tx r + ty u
static double cast(const double o[3], const double d[3], int *id) {
    double best = 1e30; int bid = -1; double t;
    if (d[2] < -1e-12) { t = -o[2] / d[2]; if (t > 0 && t < best) { best = t; bid = -2; } }
    if (stanza) {
        if (d[0] > 1e-12) { t = (3 - o[0]) / d[0]; if (t > 0 && t < best) { best = t; bid = -3; } }
        if (d[0] < -1e-12) { t = (-3 - o[0]) / d[0]; if (t > 0 && t < best) { best = t; bid = -3; } }
        if (d[1] > 1e-12) { t = (4 - o[1]) / d[1]; if (t > 0 && t < best) { best = t; bid = -3; } }
        if (d[2] > 1e-12) { t = (3 - o[2]) / d[2]; if (t > 0 && t < best) { best = t; bid = -3; } }
    }
    for (int b = 0; b < nb; b++) {
        if (!B[b].on || B[b].kind == 2) continue;
        double t0 = 0, t1 = 1e30; int miss = 0;
        for (int a = 0; a < 3; a++) {
            if (fabs(d[a]) < 1e-12) { if (o[a] < B[b].lo[a] || o[a] > B[b].hi[a]) { miss = 1; break; } continue; }
            double ta = (B[b].lo[a] - o[a]) / d[a], tb = (B[b].hi[a] - o[a]) / d[a];
            if (ta > tb) { double s = ta; ta = tb; tb = s; }
            if (ta > t0) t0 = ta;
            if (tb < t1) t1 = tb;
            if (t0 > t1) { miss = 1; break; }
        }
        if (!miss && t0 > 1e-9 && t0 < best) { best = t0; bid = b; }
    }
    *id = bid; return best;
}
static double sig(double z) { return 0.004 * z * z; }
static double marg(double z) { return 0.03 + 3 * sig(z); }

// ---------- fotogrammi ----------
static float DD[3][NPIX]; // anello di 3
static int ID[NPIX];
static float *cur, *pr1, *pr2;
static int nfr = 0;
static int rumore = 1;
static double p_rado = 0, f_chiazze = 0; // quota di pixel non validi
static int nero = -1; // indice di una scatola i cui pixel non tornano
static int coperto = 0; // 1 tutto non valido, 2 valido a 2 cm, 3 congelato
static void render(void) {
    float *nw = DD[nfr % 3];
    if (coperto == 3) { memcpy(nw, cur, sizeof(float) * NPIX); pr2 = pr1; pr1 = cur; cur = nw; nfr++;
        // gli ID seguono la verita' (servono solo ai contatori)
        for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) { double d[3]; for (int a = 0; a < 3; a++) d[a] = tf[a] + txs[i] * tr[a] + tys[j] * tu[a]; int id; cast(cpos, d, &id); ID[j * W + i] = id; }
        return; }
    for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) {
        double d[3]; for (int a = 0; a < 3; a++) d[a] = tf[a] + txs[i] * tr[a] + tys[j] * tu[a];
        int id; double t = cast(cpos, d, &id); float v = 0;
        if (id != -1 && t <= ZMAX && t > 0.05) { v = (float)(t + (rumore ? sig(t) * gau() : 0)); if (v < 0.02f) v = 0.02f; }
        if (coperto == 1) v = 0;
        if (coperto == 2) { v = 0.02f; id = -4; }
        if (p_rado > 0 && uni() < p_rado) v = 0;
        if (id == nero) v = 0;
        nw[j * W + i] = v; ID[j * W + i] = id;
    }
    if (f_chiazze > 0) { long tgt = (long)(f_chiazze * NPIX), n = 0; int guard = 0;
        while (n < tgt && guard++ < 100000) { int ci = (int)(uni() * W), cj = (int)(uni() * H);
            for (int j = cj; j < cj + 20 && j < H; j++) for (int i = ci; i < ci + 20 && i < W; i++) if (nw[j * W + i] != 0) { nw[j * W + i] = 0; n++; } } }
    pr2 = pr1; pr1 = cur; cur = nw; nfr++;
}
static void azzera(void) { memset(DD, 0, sizeof(DD)); cur = DD[0]; pr1 = DD[1]; pr2 = DD[2]; nfr = 0; }
static int pixval(int b) { int n = 0; for (int k = 0; k < NPIX; k++) if (ID[k] == b && cur[k] != 0) n++; return n; }

// proiezione con la posa stimata
static int proj(const double p[3], double *zc, double *fu, double *fv) {
    double v[3] = {p[0] - cpos[0], p[1] - cpos[1], p[2] - cpos[2]};
    double z = v[0] * ef[0] + v[1] * ef[1] + v[2] * ef[2]; if (z < 0.05) return 0;
    double x = v[0] * er[0] + v[1] * er[1] + v[2] * er[2], y = v[0] * eu[0] + v[1] * eu[1] + v[2] * eu[2];
    *zc = z; *fu = (x / z) / THX * (W / 2.0) + W / 2.0; *fv = H / 2.0 - (y / z) / THY * (H / 2.0);
    return (*fu >= 0 && *fu < W && *fv >= 0 && *fv < H);
}
static double quota_pix(int i, int j, double d) { (void)i; return CAMH + d * (-SP + tys[j] * CP); }

// ---------- Q: stato di un punto letto nell'immagine ----------
static long nq = 0;
// modo 0: Q1 (3x3, margine). modo 1: braccio ingenuo (solo centro, margine 0). modo 2: ingenuo «non valido = libero»
static int q1m(const float *D, const double p[3], int modo, int *suolo) {
    double zc, fu, fv; nq++; if (suolo) *suolo = 0;
    if (!proj(p, &zc, &fu, &fv)) return UNK;
    int i = (int)fu, j = (int)fv;
    if (modo) { float d = D[j * W + i]; if (d == 0) return modo == 2 ? LIB : UNK; return zc < d ? LIB : OMB; }
    if (i < 1 || j < 1 || i >= W - 1 || j >= H - 1) return UNK;
    float dmin = 1e9f, dmax = 0; int allfloor = 1;
    for (int b = -1; b <= 1; b++) for (int a = -1; a <= 1; a++) { float d = D[(j + b) * W + i + a]; if (d == 0) return UNK; if (d < dmin) dmin = d; if (d > dmax) dmax = d; if (quota_pix(i + a, j + b, d) > 0.07) allfloor = 0; }
    double m = marg(zc);
    if (zc < dmin - m) return LIB;
    if (zc > dmax + m) return OMB;
    if (suolo && allfloor) *suolo = 1;
    return OCC;
}
static int q1(const double p[3]) { return q1m(cur, p, 0, NULL); }
static int contraddetto(const double p[3], int *centro_valido) {
    double zc, fu, fv; *centro_valido = 0; if (!proj(p, &zc, &fu, &fv)) return 1;
    int i = (int)fu, j = (int)fv; if (i < 1 || j < 1 || i >= W - 1 || j >= H - 1) return 1;
    double m = marg(zc); *centro_valido = cur[j * W + i] != 0;
    for (int b = -1; b <= 1; b++) for (int a = -1; a <= 1; a++) { float d = cur[(j + b) * W + i + a]; if (d != 0 && d < zc + m) return 1; }
    return 0;
}
// clausola: 1 = «non contraddetto ora»; 2 = anche «pixel centrale valido ora»; 0 = nessuna
static int q3(const double p[3], int clausola) {
    int s = q1m(cur, p, 0, NULL); if (s == LIB) return LIB;
    int h = (q1m(pr1, p, 0, NULL) == LIB) || (q1m(pr2, p, 0, NULL) == LIB);
    if (!h) return s;
    if (clausola == 0) return LIB;
    int cv; if (contraddetto(p, &cv)) return s;
    if (clausola == 2 && !cv) return s;
    return LIB;
}

// ---------- N: griglia polare del nucleo ----------
static int Nocc[NA][NR], Nflo[NA][NR], Neta[NA][NR], Nr0[NA];
static uint8_t N0s[NA][NR], N1s[NA][NR], Nany[NA][NR];
static void Nreset(void) { for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) Neta[a][r] = 99; }
static int cella(const double p[3], int *ia, int *ir) {
    double r = hypot(p[0], p[1]), az = atan2(p[0], p[1]) / DEG + 43.5;
    if (r >= RG || az < 0 || az >= NA || p[1] <= 0) return 0;
    *ia = (int)az; *ir = (int)(r / 0.1); return 1;
}
static void Nupdate(void) {
    memset(Nocc, 0, sizeof(Nocc)); memset(Nflo, 0, sizeof(Nflo));
    for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) {
        float d = cur[j * W + i]; if (d == 0) continue;
        double p[3]; for (int a = 0; a < 3; a++) p[a] = cpos[a] + d * (ef[a] + txs[i] * er[a] + tys[j] * eu[a]);
        int ia, ir; if (!cella(p, &ia, &ir)) continue;
        if (p[2] >= 0.07 && p[2] <= 2.0) Nocc[ia][ir]++; else if (p[2] < 0.07 && p[2] > -0.15) Nflo[ia][ir]++;
    }
    for (int a = 0; a < NA; a++) {
        int r0 = NR; for (int r = 0; r < NR; r++) if (Nocc[a][r] >= 3) { r0 = r; break; }
        Nr0[a] = r0;
        for (int r = 0; r < NR; r++) {
            int now = (r == r0) ? OCC : (r > r0 ? OMB : (Nflo[a][r] >= 1 ? LIB : UNK));
            if (now == LIB) Neta[a][r] = 0; else if (Neta[a][r] < 99) Neta[a][r]++;
            N1s[a][r] = (now == OCC || now == OMB) ? now : (Neta[a][r] <= 2 ? LIB : UNK);
            N0s[a][r] = (now == OCC) ? OCC : (Neta[a][r] <= 2 ? LIB : now);
            Nany[a][r] = (Nocc[a][r] >= 3);
        }
    }
}

// ---------- P (profilo) e S10 (tre fasce), da Q1 ----------
static uint64_t Lfree[NA][NR], Locc[NA][NR];
static int Pfonte = 0; // 0: Q1 ; 1: Q3c dove Q1 non sa
static float Pzv[NA][NR];
#define BASSA 0x0000000000000FF8ULL // livelli 3..11  (0,175-0,575 m)
#define MEDIA 0x00000000FFFFF000ULL // livelli 12..31 (0,625-1,575 m)
#define ALTA  0x000000FF00000000ULL // livelli 32..39 (1,625-1,975 m)
static void Pupdate(void) {
    for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) {
        double azc = (a + 0.5 - 43.5) * DEG, rc = (r + 0.5) * 0.1;
        double vx[3] = {rc * sin(azc), (rc - 0.04) * sin(azc - 0.4 * DEG), (rc + 0.04) * sin(azc + 0.4 * DEG)};
        double vy[3] = {rc * cos(azc), (rc - 0.04) * cos(azc - 0.4 * DEG), (rc + 0.04) * cos(azc + 0.4 * DEG)};
        uint64_t fr = 0, oc = 0;
        for (int k = 0; k < 40; k++) { int ok = 1, occ = 0;
            for (int v = 0; v < 3; v++) { double p[3] = {vx[v], vy[v], 0.025 + 0.05 * k}; int su; int s = q1m(cur, p, 0, &su); if (Pfonte && s == UNK && q3(p, 2) == LIB) s = LIB; if (!(s == LIB || (s == OCC && su))) ok = 0; if (s == OCC && !su) occ = 1; }
            if (ok) fr |= 1ULL << k; if (occ) oc |= 1ULL << k; }
        Lfree[a][r] = fr; Locc[a][r] = oc;
        int k = 0; while (k < 40 && (fr >> k & 1)) k++; Pzv[a][r] = 0.05f * k;
    }
}
static int S10lib(int a, int r, uint64_t pert) { return (Lfree[a][r] & pert) == pert; }
// S10 alla lettera: proiezione dei punti, «attraversato = osservato»
static uint8_t Sp_occ[NA][NR], Sp_obs[NA][NR];
static int fascia(double z) { return z < 0.15 ? -1 : (z < 0.60 ? 0 : (z < 1.60 ? 1 : (z <= 2.0 ? 2 : -1))); }
static void S10pupdate(void) {
    memset(Sp_occ, 0, sizeof(Sp_occ)); memset(Sp_obs, 0, sizeof(Sp_obs));
    for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) {
        float d = cur[j * W + i]; if (d == 0) continue;
        double dir[3]; for (int a = 0; a < 3; a++) dir[a] = ef[a] + txs[i] * er[a] + tys[j] * eu[a];
        double p[3]; int ia, ir, f;
        for (int a = 0; a < 3; a++) p[a] = cpos[a] + d * dir[a];
        if (cella(p, &ia, &ir) && (f = fascia(p[2])) >= 0) Sp_occ[ia][ir] |= 1 << f;
        for (double s = 0.3; s < d - 0.05; s += 0.05) { for (int a = 0; a < 3; a++) p[a] = cpos[a] + s * dir[a];
            if (cella(p, &ia, &ir) && (f = fascia(p[2])) >= 0) Sp_obs[ia][ir] |= 1 << f; }
    }
}

// ---------- VO: voxel densi 10 cm, log-odds ----------
#define VX 60
#define VY 40
#define VZ 30
#define NV (VX * VY * VZ)
typedef struct { float L[NV]; int tr[NV], hit[NV], sh[NV]; uint8_t known[NV]; int ombre, decad; long passi; } Vox;
static Vox *vo, *voa;
static uint8_t Vinfov[NV];
static int vidx(const double p[3]) { int x = (int)floor((p[0] + 3) * 10), y = (int)floor(p[1] * 10), z = (int)floor(p[2] * 10); if (x < 0 || x >= VX || y < 0 || y >= VY || z < 0 || z >= VZ) return -1; return (z * VY + y) * VX + x; }
static void Vreset(Vox *v) { memset(v->L, 0, sizeof(v->L)); memset(v->known, 0, NV); for (int i = 0; i < NV; i++) v->tr[i] = v->hit[i] = v->sh[i] = -9; v->passi = 0; }
static void Vupdate(Vox *v) {
    const float lo = 0.8473f, lf = -0.4055f, cmin = -2.0f, cmax = 3.5f;
    for (int j = 0; j < H; j += 2) for (int i = 0; i < W; i += 2) {
        float d = cur[j * W + i]; if (d == 0) continue;
        double dir[3]; for (int a = 0; a < 3; a++) dir[a] = ef[a] + txs[i] * er[a] + tys[j] * eu[a];
        double p[3]; int k;
        for (double s = 0.05; s < d - 0.05; s += 0.05) { for (int a = 0; a < 3; a++) p[a] = cpos[a] + s * dir[a]; k = vidx(p); v->passi++; if (k >= 0) v->tr[k] = nfr; }
        for (int a = 0; a < 3; a++) p[a] = cpos[a] + d * dir[a]; k = vidx(p); if (k >= 0) v->hit[k] = nfr;
        if (v->ombre) for (double s = d + 0.05; s < 7.5; s += 0.05) { for (int a = 0; a < 3; a++) p[a] = cpos[a] + s * dir[a]; k = vidx(p); v->passi++; if (k < 0) { if (p[1] > 4 || fabs(p[0]) > 3 || p[2] < 0 || p[2] > 3) break; continue; } if (v->hit[k] != nfr) v->sh[k] = nfr; }
    }
    for (int k = 0; k < NV; k++) {
        if (v->hit[k] == nfr) { v->L[k] += lo; v->known[k] = 1; }
        else if (v->tr[k] == nfr) { v->L[k] += lf; v->known[k] = 1; }
        else if (v->decad == 1) v->L[k] *= 0.98f;            // oblio verso il priore
        else if (v->decad == 2 && v->known[k]) v->L[k] -= 0.05f; // «pulizia dinamica» verso il libero
        if (v->L[k] > cmax) v->L[k] = cmax; if (v->L[k] < cmin) v->L[k] = cmin;
    }
}
static int VOq(const Vox *v, const double p[3]) { int k = vidx(p); if (k < 0 || !v->known[k]) return UNK; return v->L[k] > 0 ? OCC : (v->L[k] < 0 ? LIB : UNK); }
static int VOaq(const Vox *v, const double p[3]) {
    int k = vidx(p); if (k < 0 || !v->known[k]) return UNK;
    if (v->hit[k] == nfr) return OCC; if (v->L[k] > 0) return OCC; // «ricordato»: non libero
    if (v->L[k] < 0 && v->tr[k] >= nfr - 2 && v->sh[k] != nfr && Vinfov[k]) return LIB;
    return UNK;
}
static void Vinitfov(void) { for (int z = 0; z < VZ; z++) for (int y = 0; y < VY; y++) for (int x = 0; x < VX; x++) { int ok = 1;
            for (int c = 0; c < 8 && ok; c++) { double p[3] = {-3 + 0.1 * (x + (c & 1)), 0.1 * (y + (c >> 1 & 1)), 0.1 * (z + (c >> 2 & 1))}, zc, fu, fv; if (!proj(p, &zc, &fu, &fv) || fu < 1 || fv < 1 || fu >= W - 1 || fv >= H - 1) ok = 0; }
            Vinfov[(z * VY + y) * VX + x] = ok; } }

// ---------- VH: blocchi 8^3 da 5 cm con tetto ----------
#define HBX 15
#define HBY 10
#define HBZ 8
#define NHB (HBX * HBY * HBZ)
typedef struct { int8_t L[512]; uint8_t pp[512]; int tocco; int npp; } Blocco;
static Blocco *HB[NHB];
static int Hn = 0, Htetto = 1 << 30, Hpin = 0, Hpol = 0; // pol 0: meno recente; 1: piu' lontano
static long Hperse = 0, Hespulsi = 0, Halloc = 0;
static int hbidx(const double p[3], int *vi) {
    int x = (int)floor((p[0] + 3) * 20), y = (int)floor(p[1] * 20), z = (int)floor(p[2] * 20);
    if (x < 0 || x >= HBX * 8 || y < 0 || y >= HBY * 8 || z < 0 || z >= HBZ * 8) return -1;
    *vi = ((z & 7) * 8 + (y & 7)) * 8 + (x & 7); return ((z >> 3) * HBY + (y >> 3)) * HBX + (x >> 3);
}
static void Hreset(void) { for (int i = 0; i < NHB; i++) { free(HB[i]); HB[i] = NULL; } Hn = 0; Hperse = Hespulsi = Halloc = 0; }
static double hbdist(int b) { int x = b % HBX, y = b / HBX % HBY; return hypot((x + 0.5) * 0.4 - 3, (y + 0.5) * 0.4); }
static Blocco *Hget(int b) {
    if (HB[b]) return HB[b];
    if (Hn >= Htetto) { int vitt = -1; double best = 1e30;
        for (int i = 0; i < NHB; i++) if (HB[i] && !(Hpin && HB[i]->npp > 0)) { double key = Hpol ? -hbdist(i) : HB[i]->tocco; if (key < best) { best = key; vitt = i; } }
        if (vitt < 0) return NULL;
        Hperse += HB[vitt]->npp; Hespulsi++; free(HB[vitt]); HB[vitt] = NULL; Hn--; }
    HB[b] = calloc(1, sizeof(Blocco)); HB[b]->tocco = nfr; Hn++; Halloc++; return HB[b];
}
static void Hupdate(void) {
    for (int j = 0; j < H; j += 2) for (int i = 0; i < W; i += 2) {
        float d = cur[j * W + i]; if (d == 0) continue;
        double dir[3]; for (int a = 0; a < 3; a++) dir[a] = ef[a] + txs[i] * er[a] + tys[j] * eu[a];
        double p[3]; int vi, b;
        for (double s = 0.05; s < d - 0.025; s += 0.025) { for (int a = 0; a < 3; a++) p[a] = cpos[a] + s * dir[a]; b = hbidx(p, &vi); if (b < 0) continue; Blocco *q = Hget(b); if (!q) continue; q->tocco = nfr; if (q->L[vi] > -20) q->L[vi]--; }
        for (int a = 0; a < 3; a++) p[a] = cpos[a] + d * dir[a]; b = hbidx(p, &vi); if (b >= 0) { Blocco *q = Hget(b); if (q) { q->tocco = nfr; if (q->L[vi] < 30) q->L[vi] += 3; } }
    }
}

// ---------- reticolo di prova e verita' ----------
static double (*LP)[3]; static int nl = 0; static int *Tocc; static uint8_t *Tdeep, *Tobs; static int8_t *Thd;
static double LS = 0.05;
static void reticolo(double s) {
    LS = s; int cap = (int)(6 / s * 3 / s * 2 / s) + 10; LP = malloc(sizeof(double[3]) * cap); nl = 0;
    for (double z = s / 2; z < 2.0; z += s) for (double y = s / 2; y < 3.0; y += s) for (double x = -3 + s / 2; x < 3; x += s) {
        double r = hypot(x, y), az = fabs(atan2(x, y)) / DEG; if (r < 0.3 || r > 3.0 || az > 60) continue; LP[nl][0] = x; LP[nl][1] = y; LP[nl][2] = z; nl++; }
    Tocc = malloc(sizeof(int) * nl); Tdeep = malloc(nl); Tobs = malloc(nl); Thd = malloc(nl);
}
static int osservabile(const double p[3]) {
    double v[3] = {p[0], p[1], p[2] - CAMH};
    double z = v[0] * tf[0] + v[1] * tf[1] + v[2] * tf[2]; if (z < 0.05) return 0;
    double x = v[0] * tr[0] + v[1] * tr[1] + v[2] * tr[2], y = v[0] * tu[0] + v[1] * tu[1] + v[2] * tu[2];
    if (fabs(x / z) >= THX || fabs(y / z) >= THY) return 0;
    double d[3] = {v[0] / z, v[1] / z, v[2] / z}; int id; double t = cast(cpos, d, &id);
    return id != -1 && t <= ZMAX && z < t - 1e-9;
}
static int dentro(const double p[3], int *deep) {
    for (int b = 0; b < nb; b++) { if (!B[b].on) continue; int in = 1, dp = 1;
        for (int a = 0; a < 3; a++) { if (p[a] < B[b].lo[a] || p[a] > B[b].hi[a]) { in = 0; break; } if (p[a] < B[b].lo[a] + 0.05 || p[a] > B[b].hi[a] - 0.05) dp = 0; }
        if (in) { if (B[b].lo[2] <= 0 && p[2] < B[b].hi[2] - 0.05 && p[0] >= B[b].lo[0] + 0.05 && p[0] <= B[b].hi[0] - 0.05 && p[1] >= B[b].lo[1] + 0.05 && p[1] <= B[b].hi[1] - 0.05) dp = 1; *deep = dp; return b; } }
    *deep = 0; return -1;
}
static void verita(void) { for (int n = 0; n < nl; n++) { int dp; Tocc[n] = dentro(LP[n], &dp); Tdeep[n] = dp; Tobs[n] = osservabile(LP[n]); Thd[n] = -1; } }
static int nascosto_profondo(int n) { // non osservabile anche spostando il punto di 3 cm
    if (Thd[n] >= 0) return Thd[n];
    int h = 1; static const double o[4][3] = {{0.03, 0, 0}, {-0.03, 0, 0}, {0, 0, 0.03}, {0, 0, -0.03}};
    for (int k = 0; k < 4 && h; k++) { double p[3] = {LP[n][0] + o[k][0], LP[n][1] + o[k][1], LP[n][2] + o[k][2]}; if (osservabile(p)) h = 0; }
    return Thd[n] = h;
}

// ---------- candidate ----------
enum { cN0, cN1, cN1col, cQ1, cQ3, cQ3c, cP, cS10, cS10p, cVO, cVOa, NC };
static const char *CN[NC] = {"N0-suolo", "N1-suolo", "N1-colonna", "Q1", "Q3", "Q3c", "P", "S10(B+M)", "S10p(B+M)", "VO", "VOa"};
static int attiva[NC] = {1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
static int claim(int c, const double p[3]) {
    int ia, ir;
    switch (c) {
    case cN0: return (p[2] < 0.07 && cella(p, &ia, &ir)) ? N0s[ia][ir] : UNK;
    case cN1: return (p[2] < 0.07 && cella(p, &ia, &ir)) ? N1s[ia][ir] : UNK;
    case cN1col: return cella(p, &ia, &ir) ? N1s[ia][ir] : UNK;
    case cQ1: return q1(p);
    case cQ3: return q3(p, 1);
    case cQ3c: return q3(p, 2);
    case cP: return (cella(p, &ia, &ir) && p[2] < Pzv[ia][ir]) ? LIB : UNK;
    case cS10: return (p[2] >= 0.15 && p[2] < 1.6 && cella(p, &ia, &ir) && S10lib(ia, ir, BASSA | MEDIA)) ? LIB : UNK;
    case cS10p: return (p[2] >= 0.15 && p[2] < 1.6 && cella(p, &ia, &ir) && (Sp_obs[ia][ir] & 3) == 3 && !(Sp_occ[ia][ir] & 3)) ? LIB : UNK;
    case cVO: return VOq(vo, p);
    case cVOa: return VOaq(voa, p);
    }
    return UNK;
}
typedef struct { long fr, Fany, Fprof, pany, pocc, pnas, pdeep, lib, ok, den, Shid, Sany; double tsum, tmax; double tt[2000]; int nt; } Stat;
static Stat ST[NC];
static long Nomb_tot, Nomb_vis;
static void Sreset(void) { memset(ST, 0, sizeof(ST)); Nomb_tot = Nomb_vis = 0; }
static void aggiorna_tutte(void) {
    double t0;
    t0 = adesso(); Nupdate(); double tn = adesso() - t0;
    t0 = adesso(); Pupdate(); double tp = adesso() - t0;
    t0 = adesso(); if (attiva[cS10p]) S10pupdate(); double ts = adesso() - t0;
    t0 = adesso(); if (attiva[cVO]) Vupdate(vo); double tv = adesso() - t0;
    t0 = adesso(); if (attiva[cVOa]) Vupdate(voa); double tva = adesso() - t0;
    double tt[NC] = {tn, tn, tn, 0, 0, 0, tp, tp, ts, tv, tva};
    for (int c = 0; c < NC; c++) { ST[c].tsum += tt[c]; if (tt[c] > ST[c].tmax) ST[c].tmax = tt[c]; if (ST[c].nt < 2000) ST[c].tt[ST[c].nt++] = tt[c]; }
}
static void valuta(void) {
    verita();
    for (int n = 0; n < nl; n++) if (LP[n][2] < 0.07 && Tocc[n] < 0 && claim(cN1, LP[n]) == OMB) { Nomb_tot++; if (Tobs[n]) Nomb_vis++; }
    int vis[MAXB]; for (int b = 0; b < nb; b++) vis[b] = (B[b].on && B[b].kind == 1) ? pixval(b) : -1;
    for (int c = 0; c < NC; c++) { if (!attiva[c]) continue;
        long any = 0, prof = 0; int sh[MAXB] = {0}, sa[MAXB] = {0};
        double t0 = adesso();
        static uint8_t *cl = NULL; static int ncl = 0; if (ncl < nl) { cl = realloc(cl, nl); ncl = nl; }
        for (int n = 0; n < nl; n++) cl[n] = (uint8_t)claim(c, LP[n]);
        double dt = adesso() - t0;
        if (c == cQ1 || c == cQ3 || c == cQ3c) { ST[c].tsum += dt; if (dt > ST[c].tmax) ST[c].tmax = dt; ST[c].tt[ST[c].nt - 1] = dt; }
        for (int n = 0; n < nl; n++) {
            int dom = (c <= cN1) ? (LP[n][2] < 0.07) : (LP[n][2] >= 0.15);
            if (dom && Tocc[n] < 0 && Tobs[n] && hypot(LP[n][0], LP[n][1]) < RG && fabs(atan2(LP[n][0], LP[n][1])) < 43.5 * DEG) { ST[c].den++; if (cl[n] == LIB) ST[c].ok++; }
            if (cl[n] != LIB) continue;
            ST[c].lib++;
            if (Tocc[n] >= 0) { any++; ST[c].pocc++; if (Tdeep[n]) { prof++; ST[c].pdeep++; } int b = Tocc[n]; if (B[b].kind == 1) { sa[b] = 1; if (vis[b] == 0) sh[b] = 1; } }
            else if (!Tobs[n]) { any++; ST[c].pnas++; if (nascosto_profondo(n)) { prof++; ST[c].pdeep++; } }
        }
        ST[c].fr++; ST[c].pany += any; if (any) ST[c].Fany++; if (prof) ST[c].Fprof++;
        for (int b = 0; b < nb; b++) { ST[c].Shid += sh[b]; ST[c].Sany += sa[b]; }
    }
}
static int cmpd(const void *a, const void *b) { double x = *(double *)a, y = *(double *)b; return x < y ? -1 : x > y; }
static void stampa(const char *tit) {
    printf("## %s  (reticolo %.0f cm, %d punti)\n", tit, LS * 100, nl);
    printf("%-11s %5s %5s %6s %9s %8s %8s %8s %5s %5s %7s %7s %7s\n", "candidata", "fot", "F_ogni", "F_prof", "punti_FL", "occupati", "nascosti", "profondi", "S_nas", "S_ogni", "resa%", "t_med", "t_max");
    for (int c = 0; c < NC; c++) { if (!attiva[c]) continue; Stat *s = &ST[c]; double med = 0;
        if (s->nt) { qsort(s->tt, s->nt, sizeof(double), cmpd); med = s->tt[s->nt / 2]; }
        printf("%-11s %5ld %5ld %6ld %9ld %8ld %8ld %8ld %5ld %5ld %7.1f %7.2f %7.2f\n", CN[c], s->fr, s->Fany, s->Fprof, s->pany, s->pocc, s->pnas, s->pdeep, s->Shid, s->Sany, s->den ? 100.0 * s->ok / s->den : 0.0, med, s->tmax); }
    fflush(stdout);
}
static void tutto_reset(void) { azzera(); Nreset(); Vreset(vo); Vreset(voa); Sreset(); p_rado = f_chiazze = 0; coperto = 0; nero = -1; assi(0, tf, tr, tu); nb = 0; for (int i = 0; i < MAXB; i++) B[i].on = 0; }

// ---------- scene ----------
enum { bCASSA = 0, bPANN, bPED, bM1, bM2, bM3, bEXTRA };
static void scena_B_fissi(void) { box(bCASSA, -1.7, -0.9, 1.95, 2.25, 0, 1.0, 0); box(bPANN, 0.6, 1.6, 1.95, 2.0, 0, 2.0, 0); box(bPED, -0.3, 0.3, 1.25, 1.45, 0, 0.5, 0); }
static void scena_B(int k) { // tre mobili
    double t = k / 15.0; scena_B_fissi();
    double x1 = 2.4 - 1.2 * t; if (x1 < -2.4) x1 = -2.4; centro(bM1, x1, 2.55, 0.4, 0.3, 1.7, 1);
    double x2 = -2.0 + 0.6 * t; if (x2 > 2.0) x2 = 2.0; centro(bM2, x2, 1.70, 0.3, 0.3, 0.25, 1);
    double t3 = t - 3.0; double x3 = 2.2 - 1.4 * (t3 > 0 ? t3 : 0); if (x3 < -0.3) x3 = -0.3; centro(bM3, x3, 2.2, 0.3, 0.3, 1.0, 1);
}
static void scena_ferma(int barra) {
    box(bCASSA, -1.4, -0.8, 1.8, 2.3, 0, 1.0, 0); box(bPANN, 0.3, 1.3, 1.9, 1.95, 0, 2.0, 0); box(bPED, -0.45, 0.15, 1.3, 1.5, 0, 0.5, 0);
    centro(bM1, 0.8, 2.5, 0.4, 0.3, 1.7, 1); // persona nascosta dietro il pannello
    if (barra == 1) box(bEXTRA, -1.5, 1.5, 1.45, 1.55, 1.7, 1.9, 0);
    if (barra == 2) box(bEXTRA, -1.5, 1.5, 1.27, 1.33, 1.52, 1.58, 0);
}

// ====================== prove ======================
static void prova_statica(void) { // A11, A1 (Q, N), bracci ingenui
    tutto_reset(); reticolo(0.05); seme(1); scena_ferma(0);
    for (int k = 0; k < 12; k++) { render(); aggiorna_tutte(); }
    valuta(); stampa("A11/A1 scena ferma, dopo 12 fotogrammi (un fotogramma valutato)");
    long l1 = 0, f1 = 0, l2 = 0, f2 = 0;
    for (int n = 0; n < nl; n++) { int s = q1m(cur, LP[n], 1, NULL); if (s == LIB) { l1++; if (Tocc[n] >= 0 || !Tobs[n]) f1++; } }
    p_rado = 0.05; render(); verita();
    for (int n = 0; n < nl; n++) { int s = q1m(cur, LP[n], 2, NULL); if (s == LIB) { l2++; if (Tocc[n] >= 0 || !Tobs[n]) f2++; } }
    printf("braccio Q senza 3x3 e senza margine: liberi %ld, falsi %ld\nbraccio Q «non valido = libero» (5%% di buchi): liberi %ld, falsi %ld\n", l1, f1, l2, f2);
    for (int c = 0; c < NC; c++) if (ST[c].lib) printf("  %-11s falsi/liberi = %.2f %%  (profondi %.2f %%)\n", CN[c], 100.0 * ST[c].pany / ST[c].lib, 100.0 * ST[c].pdeep / ST[c].lib);
}
static void prova_A1_hash(void) {
    tutto_reset(); reticolo(0.05); seme(1); scena_ferma(0); Hreset(); Htetto = 1 << 30;
    for (int k = 0; k < 12; k++) { render(); Hupdate(); }
    verita(); long tre = 0, due = 0, nonall = 0, falsi2 = 0;
    for (int n = 0; n < nl; n++) { int vi, b = hbidx(LP[n], &vi); if (b < 0) continue;
        if (!HB[b]) { nonall++; due++; if (Tocc[n] >= 0 || !Tobs[n]) falsi2++; } // due vie: «non occupato» => libero ; tre vie: sconosciuto
        else { int8_t L = HB[b]->L[vi]; if (L < 0) { tre++; due++; } else if (L == 0) { due++; if (Tocc[n] >= 0 || !Tobs[n]) falsi2++; } } }
    printf("## A1 VH (blocchi 8^3 da 5 cm): blocchi allocati %d su %d\n", Hn, NHB);
    printf("punti del reticolo in blocchi non allocati: %ld ; dati «libero» a tre vie: 0 di questi (liberi totali %ld) ; a due vie («non occupato => libero»): liberi %ld, di cui falsi %ld\n", nonall, tre, due, falsi2);
}
static void prova_S10(void) {
    for (int sc = 0; sc < 6; sc++) {
        tutto_reset(); seme(2); attiva[cVO] = attiva[cVOa] = 0;
        if (sc == 0) { /* stanza vuota */ } else if (sc == 1) scena_ferma(1); else if (sc == 2) scena_ferma(2); else if (sc == 3) box(0, -0.2, 0.2, 1.9, 2.2, 0, 0.10, 0); else if (sc == 4) box(0, -1.5, 1.5, 1.95, 2.05, 1.7, 1.9, 0); else box(0, -1.5, 1.5, 2.45, 2.55, 1.7, 1.9, 0);
        for (int k = 0; k < 3; k++) { render(); aggiorna_tutte(); }
        long nLMH = 0, nLM = 0, nN = 0, nP = 0, bLM = 0, bN = 0, bSp = 0, bSi = 0, bP = 0, nSp = 0, n1_124_161 = 0; double zvmax_b = 0;
        for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) {
            double azc = (a + 0.5 - 43.5) * DEG, rc = (r + 0.5) * 0.1, x = rc * sin(azc), y = rc * cos(azc); int ogg = 0;
            for (int b = 0; b < nb; b++) if (B[b].on && x >= B[b].lo[0] && x <= B[b].hi[0] && y >= B[b].lo[1] && y <= B[b].hi[1] && B[b].lo[2] < 2.0) ogg = 1;
            int lmh = S10lib(a, r, BASSA | MEDIA | ALTA), lm = S10lib(a, r, BASSA | MEDIA), sp = (Sp_obs[a][r] & 3) == 3 && !(Sp_occ[a][r] & 3), si = !(Sp_occ[a][r] & 3);
            nLMH += lmh; nLM += lm; nN += N1s[a][r] == LIB; nP += Pzv[a][r] > 0; nSp += sp;
            if (lm && rc > 1.24 && rc < 1.61) n1_124_161++;
            if (ogg) { bLM += lm; bN += N1s[a][r] == LIB; bSp += sp; bSi += si; if (Pzv[a][r] > 0) { bP++; if (Pzv[a][r] > zvmax_b) zvmax_b = Pzv[a][r]; } }
        }
        static const char *nm[6] = {"stanza vuota", "barra 1,7-1,9 m a 1,5 m", "barra 1,52-1,58 m a 1,3 m", "scatola alta 0,10 m a 2 m", "[dopo] barra 1,7-1,9 m a 2,0 m", "[dopo] barra 1,7-1,9 m a 2,5 m"};
        if (sc >= 4) { int pv = 0; for (int k2 = 0; k2 < NPIX; k2++) if (ID[k2] == 0 && cur[k2] != 0) pv++; printf("   (pixel validi sulla barra: %d)\n", pv); }
        printf("## S10 scena %d (%s): celle «libero» su %d: S10(B+M+A) %ld ; S10(B+M) %ld (fra 1,24 e 1,61 m: %ld) ; S10p alla lettera %ld ; N1 %ld ; P (libero fino a una quota>0) %ld\n", sc, nm[sc], NA * NR, nLMH, nLM, n1_124_161, nSp, nN, nP);
        printf("   celle «libero» con un oggetto nella colonna 0-2 m: S10(B+M) %ld ; S10p %ld ; S10i (bit a zero = libero) %ld ; N1 %ld ; P %ld (quota massima dichiarata %.2f m)\n", bLM, bSp, bSi, bN, bP, zvmax_b);
    }
    attiva[cVO] = attiva[cVOa] = 1;
}
static void prova_A5a(void) {
    tutto_reset(); reticolo(0.05); seme(3); long perfr[NC][8] = {{0}}; int ck[8] = {59, 60, 61, 62, 63, 70, 90, 99};
    long q3nc[8] = {0};
    for (int k = 0; k < 100; k++) {
        if (k >= 60) box(0, -0.4, 0.4, 1.8, 2.4, 0, 1.5, 0);
        render(); aggiorna_tutte();
        for (int j = 0; j < 8; j++) if (k == ck[j]) { verita();
                for (int c = 0; c < NC; c++) for (int n = 0; n < nl; n++) if (claim(c, LP[n]) == LIB && (Tocc[n] >= 0 ? Tdeep[n] : (!Tobs[n] && nascosto_profondo(n)))) perfr[c][j]++;
                for (int n = 0; n < nl; n++) if (q3(LP[n], 0) == LIB && (Tocc[n] >= 0 ? Tdeep[n] : (!Tobs[n] && nascosto_profondo(n)))) q3nc[j]++; }
    }
    printf("## A5a scatola che compare al fotogramma 60 su zona vista libera: falsi liberi profondi per fotogramma\n%-12s", "candidata"); for (int j = 0; j < 8; j++) printf(" f%-5d", ck[j]); printf("\n");
    for (int c = 0; c < NC; c++) { printf("%-12s", CN[c]); for (int j = 0; j < 8; j++) printf(" %6ld", perfr[c][j]); printf("\n"); }
    printf("%-12s", "Q3 no claus."); for (int j = 0; j < 8; j++) printf(" %6ld", q3nc[j]); printf("\n");
}
static void prova_A5b(double pr, double fc) {
    tutto_reset(); reticolo(0.05); seme(4); attiva[cS10p] = 0;
    for (int k = 0; k < 90; k++) { centro(bM1, -2.4 + 1.4 * k / 15.0, 2.2, 0.4, 0.3, 1.7, 1); p_rado = pr; f_chiazze = fc; render(); aggiorna_tutte(); if (k >= 3) valuta(); }
    char t[200]; snprintf(t, sizeof t, "A5b mobile a 1,4 m/s, non validi: sparsi %.0f %%, a chiazze %.0f %%", pr * 100, fc * 100); stampa(t); attiva[cS10p] = 1;
}
static void prova_A5c(void) {
    tutto_reset(); reticolo(0.05); seme(41); attiva[cS10p] = 0; nero = bM1;
    for (int k = 0; k < 90; k++) { centro(bM1, -2.4 + 1.4 * k / 15.0, 2.2, 0.4, 0.3, 1.7, 1); render(); aggiorna_tutte(); if (k >= 3) valuta(); }
    stampa("A5c soggetto nero (nessun ritorno dal corpo) a 1,4 m/s"); attiva[cS10p] = 1;
}
static void prova_A6(void) {
    tutto_reset(); reticolo(0.05); seme(5); scena_ferma(0); int ck[6] = {29, 30, 31, 32, 40, 59}; long pf[NC][6] = {{0}}, pa[NC][6] = {{0}}, n0[6] = {0};
    for (int k = 0; k < 60; k++) { if (k >= 30) assi(1 * DEG, tf, tr, tu); render(); aggiorna_tutte();
        for (int j = 0; j < 6; j++) if (k == ck[j]) { verita(); for (int c = 0; c < NC; c++) for (int n = 0; n < nl; n++) if (claim(c, LP[n]) == LIB) { if (Tocc[n] >= 0 || !Tobs[n]) pa[c][j]++; if (Tocc[n] >= 0 ? Tdeep[n] : (!Tobs[n] && nascosto_profondo(n))) pf[c][j]++; } } }
    (void)n0;
    printf("## A6 imbardata vera di 1 grado dal fotogramma 30, posa creduta ferma; falsi liberi nel riferimento del mondo: ogni (profondi)\n%-12s", "candidata"); for (int j = 0; j < 6; j++) printf("      f%-7d", ck[j]); printf("\n");
    for (int c = 0; c < NC; c++) { printf("%-12s", CN[c]); for (int j = 0; j < 6; j++) printf(" %6ld (%5ld)", pa[c][j], pf[c][j]); printf("\n"); }
}
static void prova_A8(double yv) {
    tutto_reset(); reticolo(0.05); seme(6); box(0, -0.5, 0.5, yv, yv + 0.05, 0, 2.0, 2); centro(bM1, 0, yv + 0.9, 0.4, 0.3, 1.7, 1);
    for (int k = 0; k < 5; k++) { render(); aggiorna_tutte(); } verita();
    printf("## A8 lastra di vetro 1 x 2 m a %.1f m (invisibile alla profondita'): punti della lastra dati «libero»\n", yv);
    long tot = 0; for (int n = 0; n < nl; n++) if (Tocc[n] == 0) tot++;
    for (int c = 0; c < NC; c++) { long f = 0; for (int n = 0; n < nl; n++) if (Tocc[n] == 0 && claim(c, LP[n]) == LIB) f++; printf("  %-11s %ld su %ld\n", CN[c], f, tot); }
    int cl = 0; for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) { double azc = (a + 0.5 - 43.5) * DEG, rc = (r + 0.5) * 0.1, x = rc * sin(azc), y = rc * cos(azc); if (x > -0.5 && x < 0.5 && y > yv && y < yv + 0.05 && N1s[a][r] == LIB) cl++; }
    printf("  celle N1 «libero» sotto la lastra: %d\n", cl);
}
static void prova_A9(int modo) {
    tutto_reset(); reticolo(0.05); seme(7); scena_B_fissi(); int ck[7] = {29, 30, 31, 32, 33, 40, 59}; long lib[NC][7] = {{0}}, fal[NC][7] = {{0}};
    for (int k = 0; k < 60; k++) { centro(bM1, -2.0 + 1.4 * k / 15.0, 1.7, 0.4, 0.3, 1.7, 1); if (k >= 30) coperto = modo; render(); aggiorna_tutte();
        for (int j = 0; j < 7; j++) if (k == ck[j]) { verita(); for (int c = 0; c < NC; c++) for (int n = 0; n < nl; n++) if (claim(c, LP[n]) == LIB) { lib[c][j]++; if (Tocc[n] >= 0 && Tdeep[n]) fal[c][j]++; } } }
    static const char *nm[4] = {"", "tutto non valido", "valido a 2 cm ovunque", "fotogramma congelato"};
    printf("## A9 sensore coperto dal fotogramma 30 (%s), un mobile a 1,4 m/s: punti «libero» (di cui dentro un corpo, profondi)\n%-12s", nm[modo], "candidata"); for (int j = 0; j < 7; j++) printf("      f%-8d", ck[j]); printf("\n");
    for (int c = 0; c < NC; c++) { printf("%-12s", CN[c]); for (int j = 0; j < 7; j++) printf(" %7ld (%5ld)", lib[c][j], fal[c][j]); printf("\n"); }
}
static void prova_A2(int variante) { // 0: pannello fermo, il soggetto ci passa dietro e si ferma; 1: pannello che scorre davanti a un soggetto fermo e visto
    static Vox *v[3]; for (int i = 0; i < 3; i++) { if (!v[i]) v[i] = malloc(sizeof(Vox)); Vreset(v[i]); v[i]->ombre = 0; v[i]->decad = i; }
    tutto_reset(); seme(8); long fr_lib[3] = {0}, fr_unk[3] = {0}, fr_occ[3] = {0}, nasc = 0, qlib[3] = {0}; int primo[3] = {-1, -1, -1};
    for (int k = 0; k < 960; k++) { double t = k / 15.0;
        if (variante == 0) { box(bPANN, -0.5, 0.5, 1.8, 1.85, 0, 2.0, 0); double x = -1.6 + 1.2 * t; if (x > 0) x = 0; centro(bM1, x, 2.3, 0.4, 0.3, 1.7, 1); }
        else { centro(bM1, 0, 2.3, 0.4, 0.3, 1.7, 1); double px = -2.5 + 1.0 * (t - 2 > 0 ? t - 2 : 0); if (px > 0) px = 0; box(bPANN, px - 0.5, px + 0.5, 1.8, 1.85, 0, 2.0, 0); }
        render(); Nupdate(); for (int i = 0; i < 3; i++) Vupdate(v[i]);
        if (pixval(bM1) == 0) { nasc++;
            for (int i = 0; i < 3; i++) { int nl_ = 0, nu = 0, no = 0, tot = 0;
                for (double z = 0.15; z < 1.6; z += 0.1) for (double x = B[bM1].lo[0] + 0.1; x < B[bM1].hi[0] - 0.05; x += 0.1) { double p[3] = {x, B[bM1].lo[1] + 0.03, z}; /* faccia anteriore: i voxel interni non sono mai visti */ int s = VOq(v[i], p); tot++; nl_ += s == LIB; nu += s == UNK; no += s == OCC; }
                if (nl_) { fr_lib[i]++; if (primo[i] < 0) primo[i] = k; } else if (no) fr_occ[i]++; else fr_unk[i]++; }
            for (double z = 0.15; z < 1.6; z += 0.1) { double p[3] = {B[bM1].lo[0] + 0.2, 2.3, z}; if (q1(p) == LIB) qlib[0]++; if (q3(p, 1) == LIB) qlib[1]++; }
            { double p[3] = {B[bM1].lo[0] + 0.2, 2.3, 0.02}; if (claim(cN1, p) == LIB) qlib[2]++; }
        }
    }
    printf("## A2 variante %d (%s): fotogrammi col soggetto del tutto nascosto: %ld\n", variante, variante ? "pannello che scorre davanti a un soggetto fermo gia' visto" : "pannello fermo, il soggetto ci va dietro e si ferma 60 s", nasc);
    static const char *dn[3] = {"VO senza decadimento", "VO oblio verso il priore", "VO decadimento verso il libero"};
    for (int i = 0; i < 3; i++) printf("  %-32s fotogrammi con un voxel del corpo «libero»: %ld (primo: %d) ; tutto «occupato ricordato»: %ld ; «sconosciuto»: %ld\n", dn[i], fr_lib[i], primo[i], fr_occ[i], fr_unk[i]);
    printf("  punti del corpo dati «libero»: Q1 %ld ; Q3 %ld ; N1 (cella al suolo) %ld\n", qlib[0], qlib[1], qlib[2]);
}

// ---------- regioni di possibile presenza, sul piano (celle da 10 cm) ----------
#define GX 72
#define GY 36
#define NG (GX * GY)
static void gxy(int g, double *x, double *y) { *x = -3.6 + 0.1 * (g % GX + 0.5); *y = 0.1 * (g / GX + 0.5); }
static int gdi(double x, double y) { int i = (int)floor((x + 3.6) * 10), j = (int)floor(y * 10); if (i < 0 || i >= GX || j < 0 || j >= GY) return -1; return j * GX + i; }
static void dilata(const uint8_t *in, uint8_t *out, double rad) { int R = (int)ceil(rad * 10 - 1e-9); memset(out, 0, NG);
    for (int g = 0; g < NG; g++) if (in[g]) { int i0 = g % GX, j0 = g / GX; for (int dj = -R; dj <= R; dj++) for (int di = -R; di <= R; di++) { if (di * di + dj * dj > R * R) continue; int i = i0 + di, j = j0 + dj; if (i < 0 || i >= GX || j < 0 || j >= GY) continue; out[j * GX + i] = 1; } } }
static void erodi(const uint8_t *in, uint8_t *out, double rad) { uint8_t nin[NG], d[NG]; for (int g = 0; g < NG; g++) nin[g] = !in[g]; dilata(nin, d, rad); for (int g = 0; g < NG; g++) out[g] = in[g] && !d[g]; }
static int in_griglia(double x, double y) { double r = hypot(x, y); return r < RG && fabs(atan2(x, y)) < 43.5 * DEG; }
typedef struct { int vivo; uint8_t cuneo_core[NG]; int streak[NG]; float sil[NPIX]; uint8_t silstreak[NPIX]; uint8_t rec[NG]; int t0; } Reg;
static Reg RGN;
static int nascosto_da(double x, double y, double z, int occ) { // verita': il segmento camera-punto taglia la scatola occ
    double d[3] = {x, y, z - CAMH}; double t0 = 0, t1 = 1; for (int a = 0; a < 3; a++) { if (fabs(d[a]) < 1e-12) { if (cpos[a] < B[occ].lo[a] || cpos[a] > B[occ].hi[a]) return 0; continue; }
        double ta = (B[occ].lo[a] - cpos[a]) / d[a], tb = (B[occ].hi[a] - cpos[a]) / d[a]; if (ta > tb) { double s = ta; ta = tb; tb = s; } if (ta > t0) t0 = ta; if (tb < t1) t1 = tb; if (t0 > t1) return 0; } return 1; }
static int libero_ora(double x, double y) { double p[3] = {x, y, 0.10}; int su; int s = q1m(cur, p, 0, &su); return s == LIB || (s == OCC && su); }
static void reg_ingresso(int occ, double ex, double ey) {
    memset(&RGN, 0, sizeof(RGN)); RGN.vivo = 1; RGN.t0 = nfr;
    for (int g = 0; g < NG; g++) { double x, y; gxy(g, &x, &y); double p[3] = {x, y, 0.02}; int ia, ir; if (!cella(p, &ia, &ir)) continue;
        int r0 = Nr0[ia]; if (r0 >= NR || ir <= r0) continue; double azc = (ia + 0.5 - 43.5) * DEG, rc = (r0 + 0.5) * 0.1, ox = rc * sin(azc), oy = rc * cos(azc);
        if (ox > B[occ].lo[0] - 0.15 && ox < B[occ].hi[0] + 0.15 && oy > B[occ].lo[1] - 0.15 && oy < B[occ].hi[1] + 0.15) RGN.cuneo_core[g] = 1; }
    for (int k = 0; k < NPIX; k++) RGN.sil[k] = (ID[k] == occ && cur[k] != 0) ? cur[k] : 0;
    for (int g = 0; g < NG; g++) { double x, y; gxy(g, &x, &y); if (hypot(x - ex, y - ey) <= 0.4 && !libero_ora(x, y)) RGN.rec[g] = 1; }
}
static void reg_passo(int passi_rec) {
    if (!RGN.vivo) return;
    for (int g = 0; g < NG; g++) if (RGN.cuneo_core[g]) { double x, y; gxy(g, &x, &y); double p[3] = {x, y, 0.02}; int ia, ir; if (cella(p, &ia, &ir) && N1s[ia][ir] == LIB && Neta[ia][ir] == 0) { if (++RGN.streak[g] >= 3) RGN.cuneo_core[g] = 0; } else RGN.streak[g] = 0; }
    for (int j = 0; j < H; j++) for (int i = 0; i < W; i++) { int k = j * W + i; if (RGN.sil[k] == 0) continue; float d = cur[k];
        if (d != 0 && d > RGN.sil[k] + marg(d) && quota_pix(i, j, d) < 0.07) { if (++RGN.silstreak[k] >= 3) RGN.sil[k] = 0; } else RGN.silstreak[k] = 0; }
    for (int s = 0; s < passi_rec; s++) { uint8_t d[NG]; dilata(RGN.rec, d, 0.1); for (int g = 0; g < NG; g++) { int i0 = g % GX, j0 = g / GX; uint8_t v = d[g]; // dilatazione a 8 vicini
                for (int dj = -1; dj <= 1 && !v; dj++) for (int di = -1; di <= 1 && !v; di++) { int i = i0 + di, j = j0 + dj; if (i >= 0 && i < GX && j >= 0 && j < GY && RGN.rec[j * GX + i]) v = 1; }
                d[g] = v; }
        for (int g = 0; g < NG; g++) { double x, y; gxy(g, &x, &y); RGN.rec[g] = d[g] && !(coperto != 1 && libero_ora(x, y)); } }
}
static void v12_core(uint8_t *out) { for (int g = 0; g < NG; g++) { double x, y, zc, fu, fv; gxy(g, &x, &y); double p[3] = {x, y, 0.10}; out[g] = 0; if (!proj(p, &zc, &fu, &fv)) continue; float s = RGN.sil[(int)fv * W + (int)fu]; if (s != 0 && zc > s - marg(zc)) out[g] = 1; } }
static void prova_PP(int quale) {
    tutto_reset(); seme(20 + quale); attiva[cVO] = attiva[cVOa] = 0;
    int sogg = bM1, occ = -1, prima_vis = 0, K = 0; double lx = 0, ly = 0;
    long nasc = 0, fuori[5] = {0}; // cuneo, V12, rec, timer 10 s, V12 ristretta 20 cm
    long area_vera = 0, area[3] = {0}; int chiusaV12 = -1, chiusa_vera = -1; long residuo[3] = {-1, -1, -1}; int rimosso = -1; long fuori_dopo[3] = {0}; long nasc_dopo = 0; int v12_chiusa_dopo = -1;
    if (quale == 1) K = 14 + 900 + 15; if (quale == 2) K = 150; if (quale == 3 || quale == 5 || quale == 6) K = 60 + 30 + 30 + 60; if (quale == 4) K = 200;
    for (int k = 0; k < K; k++) { double t = k / 15.0; coperto = 0;
        if (quale == 1) { if (k < 914) box(bPANN, -0.5, 0.5, 1.8, 1.85, 0, 2.0, 0); else { B[bPANN].on = 0; if (rimosso < 0) rimosso = k; } double x = -1.6 + 1.2 * t; if (x > -0.505) x = -0.505; centro(bM1, x, 2.3, 0.2, 0.2, 1.7, 1); }
        if (quale == 2 || quale == 3 || quale == 5 || quale == 6) { box(bPED, -0.3, 0.3, 1.25, 1.45, 0, 0.5, 0); box(bPANN, 0.6, 1.6, 1.95, 2.0, 0, 2.0, 0);
            double x = -2.0 + 0.6 * t, y = 1.70; if (x > 0) x = 0;
            if (quale == 3) { double tb = t - 6.0; if (tb > 0) { double f = tb / 2.0; if (f > 1) f = 1; x = 1.2 * f; y = 1.70 + 0.6 * f; } if (k >= 90 && k < 120) coperto = 1; }
            if (quale == 6) { if (k >= 90) { x = 1.2; y = 2.3; } if (k == 90) coperto = 1; }
            if (quale == 5) { double tb = t - 6.0; if (tb > 0) { double f = tb / 0.45; if (f > 1) f = 1; x = 1.2 * f; y = 1.70 + 0.6 * f; } if (k >= 90 && k < 98) coperto = 1; }
            centro(bM1, x, y, 0.3, 0.3, 0.25, 1); }
        if (quale == 4) { double sx = -0.8 + 0.5 * (t - 2.0 > 0 ? t - 2.0 : 0); if (sx > 0.8) sx = 0.8; box(bPANN, sx - 0.5, sx + 0.5, 1.8, 1.9, 0, 2.0, 0);
            double x = -2.0 + 1.2 * t; if (x > -0.8) x = sx; centro(bM1, x, 2.3, 0.3, 0.3, 1.7, 1); }
        render(); Nupdate();
        int vis = pixval(sogg); double cx = (B[sogg].lo[0] + B[sogg].hi[0]) / 2, cy = (B[sogg].lo[1] + B[sogg].hi[1]) / 2;
        if (quale == 1 && rimosso >= 0) { reg_passo(1); } /* dopo la rimozione: niente riaggancio, si guarda solo il rilascio per suolo visto */
        else if (vis > 0) { prima_vis = 1; lx = cx; ly = cy; if (RGN.vivo && coperto == 0) { RGN.vivo = 0; } }
        else if (prima_vis && !RGN.vivo && coperto == 0) { occ = -1; for (int b = 0; b < nb; b++) if (B[b].on && B[b].kind == 0 && nascosto_da(cx, cy, B[sogg].hi[2] / 2, b)) occ = b; if (occ >= 0) reg_ingresso(occ, lx, ly); }
        else if (RGN.vivo) reg_passo(1);
        if (RGN.vivo && vis == 0) { nasc++; uint8_t c[NG], d[NG], e[NG]; int g = gdi(cx, cy);
            dilata(RGN.cuneo_core, d, 0.4); if (!d[g]) fuori[0]++;
            int f3 = !(d[g] && (nfr - RGN.t0) < 150); fuori[3] += f3;
            v12_core(c); dilata(c, d, 0.4); if (!d[g]) fuori[1]++;
            erodi(c, e, 0.2); if (!e[g]) fuori[4]++;
            if (!RGN.rec[g]) fuori[2]++;
            if ((quale == 3 && k >= 120) || (quale == 5 && k >= 98) || (quale == 6 && k >= 91)) { nasc_dopo++; dilata(RGN.cuneo_core, d, 0.4); fuori_dopo[0] += !d[g]; v12_core(c); dilata(c, d, 0.4); fuori_dopo[1] += !d[g]; fuori_dopo[2] += !RGN.rec[g];
                int ch = 1; for (int q = 0; q < NG; q++) if (c[q]) { double x, y; gxy(q, &x, &y); if (hypot(x, y) > 2.9) ch = 0; } v12_chiusa_dopo = ch; }
            if ((quale == 2 && k == 140) || (quale == 1 && k == 500) || (quale == 4 && k == 60)) { area_vera = area[0] = area[1] = area[2] = 0; int ch = 1, chv = 1;
                for (int q = 0; q < NG; q++) { double x, y; gxy(q, &x, &y); if (!in_griglia(x, y)) continue; int vera = nascosto_da(x, y, 0.10, occ); area_vera += vera; area[0] += RGN.cuneo_core[q]; area[1] += c[q]; area[2] += RGN.rec[q];
                    if (c[q] && hypot(x, y) > 2.9) ch = 0; if (vera && hypot(x, y) > 2.9) chv = 0; }
                chiusaV12 = ch; chiusa_vera = chv; }
        }
        if (quale == 1 && rimosso >= 0 && k == rimosso + 5) { uint8_t c[NG]; v12_core(c); residuo[0] = residuo[1] = residuo[2] = 0;
            for (int q = 0; q < NG; q++) { double x, y; gxy(q, &x, &y); double p[3] = {x, y, 0.10}; if (!in_griglia(x, y) || hypot(x - cx, y - cy) < 0.5 || !osservabile(p)) continue; residuo[0] += RGN.cuneo_core[q]; residuo[1] += c[q]; residuo[2] += RGN.rec[q]; }
            printf("   (PP1) 5 fotogrammi dopo la rimozione del pannello: il soggetto ha %d pixel validi (riaggancio disattivato per vedere il solo rilascio)\n", vis); }
    }
    static const char *nm[7] = {"", "PP1 sosta 60 s dietro il pannello alto, poi pannello tolto", "PP2 carrello da 0,25 m dietro la pedana da 0,5 m", "PP3 sensore coperto 2 s: il carrello passa dalla pedana al pannello", "PP4 occlusore mobile a 0,5 m/s col soggetto dietro", "PP5 braccio per rec: carrello a 3 m/s, sensore coperto 8 fotogrammi", "PP6 braccio per rec: salto del carrello in un solo fotogramma coperto"};
    printf("## %s\n   fotogrammi col soggetto del tutto nascosto e regione viva: %ld ; fuori regione: cuneo %ld, V12 %ld, rec %ld ; bracci: timer 10 s %ld, sagoma ristretta 20 cm %ld\n", nm[quale], nasc, fuori[0], fuori[1], fuori[2], fuori[3], fuori[4]);
    if (area_vera) printf("   aree in celle da 10 cm (entro la griglia): ombra vera a 10 cm di quota %ld ; cuneo %ld ; V12 %ld ; rec %ld ; ombra vera chiusa entro 2,9 m: %d ; V12 la dice chiusa: %d\n", area_vera, area[0], area[1], area[2], chiusa_vera, chiusaV12);
    if (quale == 1) printf("   celle di regione rimaste su suolo tornato visibile, a piu' di 0,5 m dal soggetto, 5 fotogrammi dopo la rimozione: cuneo %ld, V12 %ld, rec %ld\n", residuo[0], residuo[1], residuo[2]);
    if (quale == 3 || quale == 5 || quale == 6) printf("   dopo la copertura: fotogrammi nascosto %ld ; fuori regione: cuneo %ld, V12 %ld, rec %ld ; V12 dice ancora «ombra chiusa»: %d\n", nasc_dopo, fuori_dopo[0], fuori_dopo[1], fuori_dopo[2], v12_chiusa_dopo);
    attiva[cVO] = attiva[cVOa] = 1;
}
static void prova_A3(int tetto_pct, int pin, int pol) {
    tutto_reset(); seme(30); Hreset(); Htetto = 1 << 30; Hpin = pin; Hpol = pol; int entrato = 0; long pp0 = 0, fuori = 0, nasc = 0; int primo = -1, dom = 0;
    for (int k = 0; k < 150; k++) { double t = k / 15.0;
        box(bPANN, -0.5, 0.5, 1.8, 1.85, 0, 2.0, 0); double x = -1.6 + 1.2 * t; if (x > 0) x = 0; centro(bM1, x, 2.3, 0.4, 0.3, 1.7, 1);
        centro(bM2, 1.4 + 0.7 * sin(t * 1.3), 1.6 + 0.25 * cos(t * 0.9), 0.4, 0.3, 1.7, 1); // secondo mobile, sempre in vista
        render(); Hupdate();
        if (!entrato && k > 5 && pixval(bM1) == 0) { entrato = 1; dom = Hn; Htetto = (tetto_pct > 0) ? dom * tetto_pct / 100 : 1 << 30; Hperse = 0; /* il tetto e' fissato PRIMA di scrivere la possibile presenza */
            for (double z = 0.025; z < 2.0; z += 0.05) for (double y = 1.9; y < 3.0; y += 0.05) for (double xx = -1.2; xx < 1.2; xx += 0.05) { if (!nascosto_da(xx, y, z, bPANN) || hypot(xx, y) > 3) continue; double p[3] = {xx, y, z}; int vi, b = hbidx(p, &vi); if (b < 0) continue; Blocco *q = Hget(b); if (q && !q->pp[vi]) { q->pp[vi] = 1; q->npp++; pp0++; } }
            printf("   ingresso al fotogramma %d: blocchi dei raggi %d, con la possibile presenza %d, tetto %d\n", k, dom, Hn, Htetto > 100000 ? -1 : Htetto); }
        if (entrato && pixval(bM1) == 0) { nasc++; double p[3] = {x, 2.3, 0.85}; int vi, b = hbidx(p, &vi); int in = b >= 0 && HB[b] && HB[b]->pp[vi]; if (!in) { fuori++; if (primo < 0) primo = k; } }
    }
    printf("## A3 VH tetto %d %% dei blocchi dei raggi all'ingresso, pin %d, espulsione %s: voxel di possibile presenza scritti %ld, persi %ld ; blocchi espulsi %ld ; fotogrammi col soggetto nascosto %ld, fuori regione %ld (primo %d) ; blocchi alla fine %d\n", tetto_pct, pin, pol ? "piu' lontano" : "meno recente", pp0, Hperse, Hespulsi, nasc, fuori, primo, Hn);
}
static void prova_A4(void) { // K-102 e «oggetto nascosto osservato»
    tutto_reset(); seme(40); attiva[cS10p] = 0; long vf = 0, nlett = 0, nany = 0, ncuneo = 0, nq = 0, np = 0; long hf = 0, hN = 0, hQ = 0; long fant = 0, fantfr = 0, scia = 0, fr = 0;
    for (int k = 0; k < 150; k++) { scena_B(k); render(); aggiorna_tutte(); fr++;
        for (int s = bM1; s <= bM3; s++) { int vis = pixval(s); double cx = (B[s].lo[0] + B[s].hi[0]) / 2, cy = (B[s].lo[1] + B[s].hi[1]) / 2, h = B[s].hi[2];
            int ia, ir; double pg[3] = {cx, cy, 0.02}; int inc = cella(pg, &ia, &ir);
            if (s == bM1 && vis > 500 && nascosto_da(cx, cy, 0.3, bCASSA) && inc) { vf++;
                int lett = 0, any = 0, cun = 1; for (double dx = -0.15; dx <= 0.15; dx += 0.05) for (double dy = -0.15; dy <= 0.15; dy += 0.05) { double q[3] = {cx + dx, cy + dy, 0.02}; int a, r; if (!cella(q, &a, &r)) continue; if (N1s[a][r] == OCC) lett = 1; if (Nany[a][r]) { any = 1; if (r <= Nr0[a]) cun = 0; } }
                nlett += lett; nany += any; if (any && cun) ncuneo++;
                int oq = 0; for (double z = 0.1; z < h; z += 0.1) { double q[3] = {cx, B[s].lo[1], z}; if (q1(q) == OCC) oq++; } if (oq >= 3) nq++;
                if (Locc[ia][ir] >> 20) np++; }
            if (vis == 0 && inc) { hf++; int n1 = 0; for (double dx = -0.1; dx <= 0.1; dx += 0.05) { double q[3] = {cx + dx, cy, 0.02}; int a, r; if (cella(q, &a, &r) && N1s[a][r] == OCC) n1 = 1; } hN += n1;
                int oq = 0; for (double z = 0.05; z < h; z += 0.05) { double q[3] = {cx, B[s].lo[1], z}; if (q1(q) == OCC) oq++; } if (oq) hQ++; } }
        long f = 0; for (int z = 0; z < 20; z++) for (int y = 0; y < 30; y++) for (int x = 2; x < VX - 2; x++) { int i = (z * VY + y) * VX + x; if (vo->L[i] <= 0 || !vo->known[i]) continue; double p[3] = {-3 + 0.1 * (x + 0.5), 0.1 * (y + 0.5), 0.1 * (z + 0.5)}; int dp; if (dentro(p, &dp) >= 0) continue;
                    int vuoto_vicino = 1; for (int b = 0; b < nb; b++) if (B[b].on) { int near = 1; for (int a = 0; a < 3; a++) if (p[a] < B[b].lo[a] - 0.12 || p[a] > B[b].hi[a] + 0.12) near = 0; if (near) vuoto_vicino = 0; }
                    if (!vuoto_vicino || p[2] < 0.15) continue; if (osservabile(p)) scia++; else f++; }
        fant += f; if (f) fantfr++;
    }
    printf("## A4 / K-102 (scenario B, 150 fotogrammi)\n   adulto dietro la cassa da 1 m con piu' di 500 pixel validi: %ld fotogrammi ; «occupato osservato» nella sua impronta: N alla lettera %ld ; N «ogni ritorno» %ld (di cui tutto nel cuneo della cassa: %ld) ; Q1 (>= 3 punti della faccia) %ld ; P (livelli occupati sopra 1 m) %ld\n", vf, nlett, nany, ncuneo, nq, np);
    printf("   soggetti del tutto nascosti dentro la griglia: %ld soggetto-fotogrammi ; dati «osservato»: N1 %ld ; Q1 %ld\n", hf, hN, hQ);
    printf("   VO: voxel «occupato» vuoti, lontani oltre 12 cm da ogni corpo: in ombra %ld (in %ld fotogrammi su %ld) ; in vista (scia) %ld\n", fant, fantfr, fr, scia);
    attiva[cS10p] = 1;
}
static void prova_K102(void) {
    tutto_reset(); seme(42); long vf = 0, nlett = 0, nany = 0, ncuneo = 0, nq = 0, np = 0, pix = 0;
    for (int k = 0; k < 100; k++) { box(bCASSA, -0.5, 0.5, 1.7, 2.0, 0, 1.0, 0); double cx = -1.6 + 0.5 * k / 15.0, cy = 2.4; centro(bM1, cx, cy, 0.4, 0.3, 1.7, 1);
        render(); Nupdate(); Pupdate(); int vis = pixval(bM1);
        if (!(vis > 500 && nascosto_da(cx - 0.2, cy, 0.05, bCASSA) && nascosto_da(cx + 0.2, cy, 0.05, bCASSA))) continue;
        vf++; pix += vis; int lett = 0, any = 0, cun = 1, ia, ir;
        for (double dx = -0.15; dx <= 0.15; dx += 0.05) for (double dy = -0.15; dy <= 0.15; dy += 0.05) { double q[3] = {cx + dx, cy + dy, 0.02}; int a, r; if (!cella(q, &a, &r)) continue; if (N1s[a][r] == OCC) lett = 1; if (Nany[a][r]) { any = 1; if (r <= Nr0[a]) cun = 0; } }
        nlett += lett; nany += any; if (any && cun) ncuneo++;
        int oq = 0; for (double z = 0.1; z < 1.7; z += 0.1) { double q[3] = {cx, B[bM1].lo[1], z}; if (q1(q) == OCC) oq++; } if (oq >= 3) nq++;
        int pp_ = 0; for (double dx = -0.15; dx <= 0.15; dx += 0.05) for (double dy = -0.15; dy <= 0.15; dy += 0.05) { double pg[3] = {cx + dx, cy + dy, 0.02}; if (cella(pg, &ia, &ir) && (Locc[ia][ir] >> 20)) pp_ = 1; } np += pp_; }
    printf("## K-102 dedicata: adulto (1,7 m) a 0,5 m/s dietro una cassa da 1 m; fotogrammi con tutta l'impronta nell'ombra al suolo e piu' di 500 pixel validi: %ld (pixel validi medi %ld)\n   «occupato osservato» nella sua impronta: N alla lettera %ld ; N «ogni ritorno» %ld (di cui tutto dentro il cuneo: %ld) ; Q1 %ld ; P (livelli occupati sopra 1 m) %ld\n", vf, vf ? pix / vf : 0, nlett, nany, ncuneo, nq, np);
}
static void scenario(char quale, double pr, double fc, int stampa_si) {
    tutto_reset(); reticolo(0.10); seme(50 + quale);
    if (quale == 'B') { for (int k = 0; k < 150; k++) { scena_B(k); p_rado = pr; f_chiazze = fc; render(); aggiorna_tutte(); if (k >= 3) valuta(); } }
    if (quale == 'A') { for (int k = 0; k < 60; k++) { scena_B(k); p_rado = pr; f_chiazze = fc; render(); aggiorna_tutte(); if (k >= 3) valuta(); } }
    if (quale == 'C') { double ox[10], oy[10], w[10], h[10], vx[10], vy[10]; box(bCASSA, -1.7, -0.9, 1.95, 2.25, 0, 1.0, 0); box(bPANN, 0.6, 1.6, 1.95, 2.0, 0, 2.0, 0);
        for (int i = 0; i < 10; i++) { double r = 1.4 + 1.5 * uni(), a = (uni() * 76 - 38) * DEG; ox[i] = r * sin(a); oy[i] = r * cos(a); w[i] = 0.3 + 0.3 * uni(); h[i] = 0.3 + 1.4 * uni(); double v = 0.5 + 0.9 * uni(), d = uni() * 2 * M_PI; vx[i] = v * cos(d); vy[i] = v * sin(d); }
        for (int k = 0; k < 90; k++) { p_rado = f_chiazze = 0;
            if (k >= 30) { for (int i = 0; i < 10; i++) { double t = (k - 30) / 15.0, x = ox[i] + vx[i] * t, y = oy[i] + vy[i] * t; if (y < 1.3) y = 1.3; centro(10 + i, x, y, w[i], w[i], h[i], 1); } if (k < 45) { p_rado = pr; f_chiazze = fc; } }
            render(); aggiorna_tutte(); if (k >= 3) valuta(); } }
    if (stampa_si) printf("   [N1] punti al suolo in celle «in ombra»: %ld, di cui in verita' visibili: %ld (%.1f %%)\n", Nomb_tot, Nomb_vis, Nomb_tot ? 100.0 * Nomb_vis / Nomb_tot : 0.0);
    if (stampa_si) { char t[200]; snprintf(t, sizeof t, "Scenario %c, non validi: sparsi %.0f %%, a chiazze %.0f %%", quale, pr * 100, fc * 100); stampa(t); }
}
static void scenario_A(int chiazze) {
    printf("## Scenario A (azzeramento progressivo, %s): per quota di pixel validi, 57 fotogrammi dello scenario B\n", chiazze ? "a chiazze 20x20" : "sparso");
    printf("%-7s", "validi%"); for (int c = 0; c < NC; c++) if (c != cS10p && c != cN1col) printf(" | %-10s", CN[c]); printf("\n        (per candidata: fotogrammi con falso libero profondo / resa %% del libero vero)\n");
    for (int v = 100; v >= 0; v -= 10) { attiva[cS10p] = 0; attiva[cN1col] = 0; double f = 1 - v / 100.0; scenario('A', chiazze ? 0 : f, chiazze ? f : 0, 0);
        int valide = 0; for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) if (N1s[a][r] != UNK) valide++;
        printf("%-7d", v); for (int c = 0; c < NC; c++) if (c != cS10p && c != cN1col) printf(" | %3ld %5.1f ", ST[c].Fprof, ST[c].den ? 100.0 * ST[c].ok / ST[c].den : 0.0); printf(" | celle N note %d\n", valide); fflush(stdout); }
    attiva[cS10p] = attiva[cN1col] = 1;
}
static void prova_K106(void) {
    printf("## K-106 resa del libero vero (volume, quota >= 15 cm), scena B, 57 fotogrammi ; P e S10 costruiti su %s\n", Pfonte ? "Q3c" : "Q1");
    double cfg[5][2] = {{0, 0}, {0.05, 0}, {0, 0.05}, {0.20, 0}, {0, 0.20}};
    for (int i = 0; i < 5; i++) { attiva[cS10p] = attiva[cVO] = attiva[cVOa] = 0; scenario('A', cfg[i][0], cfg[i][1], 0);
        printf("  buchi sparsi %2.0f %%, a chiazze %2.0f %%: Q1 %.1f %% ; Q3 %.1f %% ; Q3c %.1f %% ; P %.1f %% ; S10 %.1f %% ; N1 (suolo) %.1f %%   | falsi profondi (fotogrammi): Q1 %ld, Q3 %ld, Q3c %ld\n", cfg[i][0] * 100, cfg[i][1] * 100,
               100.0 * ST[cQ1].ok / ST[cQ1].den, 100.0 * ST[cQ3].ok / ST[cQ3].den, 100.0 * ST[cQ3c].ok / ST[cQ3c].den, 100.0 * ST[cP].ok / ST[cP].den, 100.0 * ST[cS10].ok / ST[cS10].den, 100.0 * ST[cN1].ok / ST[cN1].den, ST[cQ1].Fprof, ST[cQ3].Fprof, ST[cQ3c].Fprof); printf("      P: fotogrammi con falso profondo %ld, punti falsi %ld (profondi %ld) ; S10: %ld, %ld (%ld)\n", ST[cP].Fprof, ST[cP].pany, ST[cP].pdeep, ST[cS10].Fprof, ST[cS10].pany, ST[cS10].pdeep); }
    attiva[cS10p] = attiva[cVO] = attiva[cVOa] = 1;
}
static void prova_K105(void) {
    tutto_reset(); seme(60); static uint8_t stor[4][NA][NR]; static int visst[4][MAXB]; static uint8_t marg_ok[4][2][NA][NR];
    long nasc = 0, ogni = 0, m14 = 0, m25 = 0, lib = 0, lib14 = 0, lib25 = 0; double D[2] = {1.4 * 0.2 + 0.05, 2.5 * 0.2 + 0.05};
    static double cxs[NA][NR], cys[NA][NR]; for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) { double azc = (a + 0.5 - 43.5) * DEG, rc = (r + 0.5) * 0.1; cxs[a][r] = rc * sin(azc); cys[a][r] = rc * cos(azc); }
    for (int k = 0; k < 150; k++) { scena_B(k); render(); Nupdate(); int sl = k % 4;
        memcpy(stor[sl], N1s, sizeof(N1s)); for (int b = 0; b < nb; b++) visst[sl][b] = (B[b].on && B[b].kind == 1) ? pixval(b) : -1;
        for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) { marg_ok[sl][0][a][r] = marg_ok[sl][1][a][r] = 0; if (N1s[a][r] != LIB) continue; lib++;
            double dmin = 1e9, x = cxs[a][r], y = cys[a][r], rr = hypot(x, y), az = fabs(atan2(x, y));
            double db = RG - rr; if (db < dmin) dmin = db; db = rr * sin(43.5 * DEG - az); if (db < dmin) dmin = db;
            for (int a2 = 0; a2 < NA; a2++) for (int r2 = 0; r2 < NR; r2++) if (N1s[a2][r2] == OMB || N1s[a2][r2] == UNK) { double d = hypot(x - cxs[a2][r2], y - cys[a2][r2]) - 0.07; if (d < dmin) dmin = d; }
            if (dmin > D[0]) { marg_ok[sl][0][a][r] = 1; lib14++; } if (dmin > D[1]) { marg_ok[sl][1][a][r] = 1; lib25++; } }
        for (int j = 1; j <= 3 && j <= k; j++) { int ps = (k - j) % 4;
            for (int b = 0; b < nb; b++) { if (!(B[b].on && B[b].kind == 1)) continue;
                for (int a = 0; a < NA; a++) for (int r = 0; r < NR; r++) { if (stor[ps][a][r] != LIB) continue; double x = cxs[a][r], y = cys[a][r]; if (x < B[b].lo[0] || x > B[b].hi[0] || y < B[b].lo[1] || y > B[b].hi[1]) continue;
                    ogni++; if (visst[ps][b] == 0) { nasc++; m14 += marg_ok[ps][0][a][r]; m25 += marg_ok[ps][1][a][r]; } } } }
    }
    printf("## K-105 (N1, scenario B, 150 fotogrammi; finestra d'uso 3 fotogrammi = 0,20 s)\n   celle-fotogramma «libero» poi occupate entro la finestra: da un soggetto qualsiasi %ld ; da un soggetto che al momento della dichiarazione non aveva alcun pixel valido %ld\n", ogni, nasc);
    printf("   con il margine attorno a ombra, non osservato e bordo: 0,33 m (1,4 m/s) %ld ; 0,55 m (2,5 m/s) %ld\n   libero conservato col margine: %.1f %% (0,33 m) ; %.1f %% (0,55 m)   [celle-fotogramma libere %ld]\n", m14, m25, 100.0 * lib14 / lib, 100.0 * lib25 / lib, lib);
}
static void prova_A10(void) { // tempi: scenario C sparso, tre ripetizioni; VH con allocazione
    printf("## A10 tempi per fotogramma nello scenario C (ms): mediana / p95 / massimo / (massimo:mediana), per ripetizione\n");
    for (int rep = 0; rep < 3; rep++) { scenario('C', 0.5, 0, 0);
        printf("  rip. %d:", rep); for (int c = 0; c < NC; c++) { if (c == cN0 || c == cN1col || c == cS10) continue; Stat *s = &ST[c]; qsort(s->tt, s->nt, sizeof(double), cmpd); double med = s->tt[s->nt / 2], p95 = s->tt[(int)(s->nt * 0.95)]; printf(" %s %.2f/%.2f/%.2f(%.2f)", CN[c], med, p95, s->tmax, s->tmax / (med > 1e-9 ? med : 1e-9)); } printf("\n"); }
    printf("   (Q: %d punti interrogati per fotogramma; P: %d interrogazioni; N, S10p, VO: aggiornamento)\n", nl, NA * NR * 120);
    for (int tetto = 0; tetto < 2; tetto++) { tutto_reset(); seme(99); Hreset(); Htetto = tetto ? 300 : 1 << 30; Hpin = 0; Hpol = 0; double tt[90]; long al[90]; double ox[10], oy[10], w[10], h[10];
        for (int i = 0; i < 10; i++) { double r = 1.4 + 1.5 * uni(), a = (uni() * 76 - 38) * DEG; ox[i] = r * sin(a); oy[i] = r * cos(a); w[i] = 0.3 + 0.3 * uni(); h[i] = 0.3 + 1.4 * uni(); }
        for (int k = 0; k < 90; k++) { if (k >= 30) for (int i = 0; i < 10; i++) centro(10 + i, ox[i] + 0.5 * (k - 30) / 15.0, oy[i], w[i], w[i], h[i], 1); p_rado = (k >= 30 && k < 45) ? 0.5 : 0; render(); long a0 = Halloc; double t0 = adesso(); Hupdate(); tt[k] = adesso() - t0; al[k] = Halloc - a0; }
        double s[90]; memcpy(s, tt, sizeof s); qsort(s, 90, sizeof(double), cmpd);
        printf("  VH (5 cm, raggi 1 su 4) tetto %s: mediana %.2f ms, p95 %.2f, massimo %.2f (fotogramma 0: %.2f ms con %ld allocazioni; fotogramma 30: %.2f ms con %ld) ; blocchi alla fine %d ; espulsi %ld\n", tetto ? "300 blocchi" : "nessuno", s[45], s[85], s[89], tt[0], al[0], tt[30], al[30], Hn, Hespulsi); }
    { tutto_reset(); seme(98); scena_ferma(0); for (int k = 0; k < 20; k++) { render(); Vupdate(vo); Vupdate(voa); } printf("  passi di raggio per fotogramma (10 cm, raggi 1 su 4): VO %ld ; VOa con le ombre %ld (+%.0f %%)\n", vo->passi / 20, voa->passi / 20, 100.0 * (voa->passi - vo->passi) / vo->passi); }
}

int main(int argc, char **argv) {
    initcam(); vo = malloc(sizeof(Vox)); voa = malloc(sizeof(Vox)); vo->ombre = 0; vo->decad = 0; voa->ombre = 1; voa->decad = 0; Vinitfov(); reticolo(0.05);
    const char *p = argc > 1 ? argv[1] : "";
    if (!strcmp(p, "statica")) { prova_statica(); prova_A1_hash(); }
    else if (!strcmp(p, "s10")) prova_S10();
    else if (!strcmp(p, "a5")) { prova_A5a(); prova_A5b(0.30, 0); prova_A5b(0, 0.30); prova_A5b(0, 0); }
    else if (!strcmp(p, "a5c")) prova_A5c();
    else if (!strcmp(p, "a5a")) prova_A5a();
    else if (!strcmp(p, "a6")) prova_A6();
    else if (!strcmp(p, "a8")) { prova_A8(1.5); prova_A8(2.0); }
    else if (!strcmp(p, "a9")) { prova_A9(1); prova_A9(2); prova_A9(3); }
    else if (!strcmp(p, "a2")) { prova_A2(0); prova_A2(1); }
    else if (!strcmp(p, "pp")) { for (int q = 1; q <= 6; q++) prova_PP(q); }
    else if (!strcmp(p, "a3")) { prova_A3(0, 0, 0); prova_A3(100, 0, 0); prova_A3(100, 0, 1); prova_A3(100, 1, 0); prova_A3(108, 0, 0); prova_A3(110, 0, 0); prova_A3(113, 0, 0); }
    else if (!strcmp(p, "a4")) prova_A4();
    else if (!strcmp(p, "k102")) prova_K102();
    else if (!strcmp(p, "scenB")) scenario('B', 0, 0, 1);
    else if (!strcmp(p, "scenC")) { scenario('C', 0.5, 0, 1); scenario('C', 0, 0.5, 1); }
    else if (!strcmp(p, "scenA")) { scenario_A(0); scenario_A(1); }
    else if (!strcmp(p, "k106")) { Pfonte = (argc > 2); prova_K106(); }
    else if (!strcmp(p, "k105")) prova_K105();
    else if (!strcmp(p, "a10")) prova_A10();
    else { fprintf(stderr, "prove: statica s10 a5 a6 a8 a9 a2 pp a3 a4 scenB scenC scenA k106 k105 a10\n"); return 2; }
    return 0;
}
