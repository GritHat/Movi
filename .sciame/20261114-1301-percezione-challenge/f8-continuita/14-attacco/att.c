/* att.c — simulatore dell'attacco alle modifiche (sciame-avversario, f8, fase f4). Scritto da capo.
 * Regole prese da MODIFICHE_CONTINUITA.md (§2.1-2.6) e SOLUZIONE_V2.md (B3 C6, B5 «Ritorno»).
 * Mio: generatore di traiettorie, corpo esteso, C6 sulla maschera stimata, ciclo di vita, sessione.
 * Uso: att prova chiave=valore ...   |   att sessione chiave=valore ...   |   att tempo geo=T n=10
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define DT (1.0 / 15.0)
#define CELL 0.10
#define HD 0.0707
#define HFOV (43.5 * M_PI / 180.0)
#define KH 90
#define NM 400
#define NLIBMAX 400
#define VMAX 2.5
#define NK 420
#define T_PRE 2.5
#define QN 0.2
#define RV 0.0025
#define NB 10
enum { PROSEGUE, RALLENTA, SOSTA, TORNA, SVOLTA, LONTANO, SOSTALUNGA, SBIRCIA, FERMOVISTA, CURVA };
static const char *BN[NB] = {"prosegue", "rallenta", "sosta", "torna", "svolta", "lontano", "sostalunga", "sbircia", "fermo-in-vista", "curva"};

/* ---- parametri ---- */
static char GEO = 'T';
static double YP, W, YS, RMAX, TA, TAE, E_MASK = 0, PD = 0.9, RB = 0.225, C6ADJ = 0.10, BAND = 0.20;
static double YAWB = 0, YAWJ = 0, OMEGA = 0, VLO = 0.3, VHI = 1.8;
static int NLIB_WANT = 200, LIB_LIVELY = 0, TEST_LIVELY = 0, NSEED = 400, AMPIO_ON = 1, SMOOTH = 3;
static long SEED0 = 200000;
static const char *BEHS = "0123";
static double RH = 0.40, VMIN = 0.0; static int ASSORB = 1, M1N = 1, BORDO = 1; /* bracci di correzione, dopo la prova */

/* ---- casuali: xorshift64* ---- */
typedef struct { uint64_t s; } Rng;
static uint64_t r64(Rng *r) { uint64_t x = r->s; x ^= x >> 12; x ^= x << 25; x ^= x >> 27; r->s = x; return x * 0x2545F4914F6CDD1DULL; }
static double ru(Rng *r) { return (double)(r64(r) >> 11) / 9007199254740992.0; }
static double rn(Rng *r) { double u1 = ru(r), u2 = ru(r); if (u1 < 1e-300) u1 = 1e-300; return sqrt(-2 * log(u1)) * cos(2 * M_PI * u2); }
static double rr_(Rng *r, double a, double b) { return a + (b - a) * ru(r); }
static void rseed(Rng *r, uint64_t a, uint64_t b, uint64_t c) { r->s = (a + 1) * 0x9E3779B97F4A7C15ULL ^ (b + 7) * 0xC2B2AE3D27D4EB4FULL ^ (c + 13) * 0x165667B19E3779F9ULL; if (!r->s) r->s = 1; for (int i = 0; i < 8; i++) r64(r); }

/* ---- geometria ---- */
static void geo_set(void) {
    if (GEO == 'D') { YP = 1.9; W = 1.0; YS = 2.3; RMAX = 3.0; } else if (GEO == 'T') { YP = 2.0; W = 1.0; YS = 4.0; RMAX = 6.0; } else { YP = 2.0; W = 2.0; YS = 4.0; RMAX = 6.0; }
    TA = (W / 2) / YP; TAE = (TA * YS + E_MASK) / YS;
}
static double dwedge(double x, double y, double yp, double t) {
    double ax = fabs(x); if (y >= yp && ax <= y * t) return 0;
    double cx = yp * t, n = sqrt(1 + t * t), qx = ax - cx, qy = y - yp, al = (qx * t + qy) / n;
    double dray = al <= 0 ? hypot(qx, qy) : fabs(qx - qy * t) / n, dbot = ax <= cx ? fabs(yp - y) : hypot(qx, qy);
    return dray < dbot ? dray : dbot;
}
static double PSI = 0; /* errore d'imbardata della maschera stimata, in questo ciclo */
static inline double dest(double x, double y) { double c = cos(PSI), s = sin(PSI); return dwedge(c * x + s * y, -s * x + c * y, YP, TAE); }
static inline int intrue(double x, double y) { return y >= YP && fabs(x) <= y * TA; }
static inline int indom(double x, double y) { return y > 0 && hypot(x, y) <= RMAX && fabs(atan2(x, y)) <= HFOV; }

/* ---- griglia e maschere (ricalcolate quando PSI cambia) ---- */
static int NX, NY, NC, NA; static double GX, AREA_SH, SHCX, SHCY;
static float *CX, *CY, *DE; static uint8_t *DOM, *AM, *R100, *CNT; static int *AL, *SIDX; static float *D1, *D2, *D3, *D4;
static void grid_alloc(void) {
    GX = ceil((RMAX * sin(HFOV) + 0.05) * 10) / 10; NX = (int)lround(2 * GX / CELL); NY = (int)lround(RMAX / CELL); NC = NX * NY;
    CX = malloc(NC * sizeof(float)); CY = malloc(NC * sizeof(float)); DE = malloc(NC * sizeof(float));
    DOM = calloc(NC, 1); AM = calloc(NC, 1); R100 = calloc(NC, 1); CNT = calloc(NC, 1); AL = malloc(NC * sizeof(int)); SIDX = malloc(NC * sizeof(int));
    D1 = calloc(NC, sizeof(float)); D2 = calloc(NC, sizeof(float)); D3 = calloc(NC, sizeof(float)); D4 = calloc(NC, sizeof(float));
    for (int j = 0; j < NY; j++) for (int i = 0; i < NX; i++) { int c = j * NX + i; CX[c] = -GX + (i + 0.5) * CELL; CY[c] = (j + 0.5) * CELL; DOM[c] = indom(CX[c], CY[c]); }
}
static double PSI_MASK = 1e9;
static void masks(void) {
    if (PSI == PSI_MASK) return; PSI_MASK = PSI; NA = 0; int ns = 0; double sx = 0, sy = 0;
    for (int c = 0; c < NC; c++) { double d = dest(CX[c], CY[c]); DE[c] = d; AM[c] = DOM[c] && d - HD <= BAND; R100[c] = DOM[c] && d - HD <= 0.40;
        if (DOM[c] && d == 0) { ns++; sx += CX[c]; sy += CY[c]; } if (AM[c]) AL[NA++] = c; }
    AREA_SH = ns * CELL * CELL; SHCX = ns ? sx / ns : 0; SHCY = ns ? sy / ns : YS;
    for (int a = 0; a < NA; a++) { int c = AL[a], i = c % NX, j = c / NX, n = 0;
        for (int dj = -1; dj <= 1; dj++) for (int di = -1; di <= 1; di++) { int ii = i + di, jj = j + dj; if (ii >= 0 && ii < NX && jj >= 0 && jj < NY && AM[jj * NX + ii]) n++; }
        CNT[c] = n; }
}
static inline int cell_of(double x, double y) { int i = (int)floor((x + GX) / CELL), j = (int)floor(y / CELL); if (i < 0 || i >= NX || j < 0 || j >= NY) return -1; return j * NX + i; }
/* corpo visibile in questo ciclo: le sue celle sono «occupato osservato», quelle dietro sono la sua ombra: non «libero» */
static int BVIS = 0; static double BX, BY;
static inline int body_blocks(double x, double y) {
    if (!BVIS || RB <= 0) return 0; if (hypot(x - BX, y - BY) <= RB + HD) return 1;
    double rc = hypot(BX, BY), r = hypot(x, y); if (r < rc) return 0;
    double da = atan2(x, y) - atan2(BX, BY); return fabs(da) <= asin(fmin(1.0, RB / rc));
}
/* 0 non osservato; 1 in A (ombra stimata + fascia); 2 visto libero oltre la fascia; 3 occupato dal corpo o dietro di esso */
static inline int cls(double x, double y) { int c = cell_of(x, y); if (c < 0 || !DOM[c]) return 0; if (AM[c]) return 1; return body_blocks(x, y) ? 3 : 2; }

/* ---- traiettorie (generatore mio) ---- */
typedef struct { int n, beh; double x[NK], y[NK], v0, ex, ey; } Traj;
static void traj(Traj *T, int beh, uint64_t seed, int lively) {
    Rng r; rseed(&r, seed, (uint64_t)beh, (uint64_t)GEO); T->beh = beh;
    double v0 = rr_(&r, VLO, VHI), h = rr_(&r, -15, 15) * M_PI / 180, oy = rr_(&r, -0.10, 0.10); int mir = ru(&r) < 0.5;
    double yc = YS + oy, ch = cos(h), sh = sin(h), s_in = -TA * yc / (ch + TA * sh), s_out = TA * yc / (ch - TA * sh);
    double t_out = T_PRE + (s_out - s_in) / v0, tman = T_PRE + ru(&r) * (t_out - T_PRE);
    int sudden = ru(&r) < 0.5; double fslow = rr_(&r, 0.3, 0.6), asl = rr_(&r, 0.5, 1.5), ast = sudden ? 6.0 : rr_(&r, 1.0, 3.0);
    double hold = beh == SOSTA ? rr_(&r, 2, 4) : rr_(&r, 6, 8), pause = rr_(&r, 0.3, 1.0), fback = rr_(&r, 0.8, 1.2);
    double turn = rr_(&r, 45, 90) * M_PI / 180 * (ru(&r) < 0.5 ? -1 : 1), ph1 = rr_(&r, 0, 2 * M_PI), ph2 = rr_(&r, 0, 2 * M_PI);
    double sstop = 1e9; if (beh == SBIRCIA) { sstop = s_in + rr_(&r, -0.15, 0.15); hold = 5.0; ast = 6.0; } if (beh == FERMOVISTA) { sstop = s_in - rr_(&r, 0.33, 0.40); hold = 10.0; ast = 6.0; }
    double om = (beh == CURVA ? OMEGA * M_PI / 180 * (ru(&r) < 0.5 ? -1 : 1) : 0);
    double sway = lively ? 0.05 : 0.02, rip = lively ? 0.10 : 0.03, sv = lively ? 0.10 : 0.05, shd = (lively ? 5.0 : 2.0) * M_PI / 180, fstep = 1.4 + 0.5 * v0;
    const double hs = DT / 4; double px = s_in * ch, py = yc + s_in * sh;
    for (double u = 0; u < T_PRE - 1e-9; u += hs) { double hd = h + om * (-(u + hs / 2)); px -= v0 * cos(hd) * hs; py -= v0 * sin(hd) * hs; }
    T->ex = s_in * ch; T->ey = yc + s_in * sh; T->v0 = v0;
    double m = 1, mt = 1, acc = 1, gh = 0, ght = 0, ev = sv * rn(&r), eh = shd * rn(&r), t = 0, s = s_in - v0 * T_PRE, tstop = -1; int phase = 0;
    double tpost = (beh == SBIRCIA || beh == FERMOVISTA) ? 20.0 : 9.0; int nk = (int)((T_PRE + tpost) / DT) + 1; if (nk > NK) nk = NK; T->n = nk;
    for (int k = 0; k < nk; k++) {
        double hd = h + gh + eh + om * (t - T_PRE), lat = sway * sin(M_PI * fstep * t + ph2) * fmin(1.0, fabs(m));
        T->x[k] = px - sin(hd) * lat; T->y[k] = py + cos(hd) * lat;
        for (int q = 0; q < 4; q++) {
            double sp0 = v0 * m;
            if (beh == SBIRCIA || beh == FERMOVISTA) {
                if (phase == 0 && sstop - s <= sp0 * sp0 / (2 * ast)) { phase = 1; mt = 0; acc = ast; }
                if (phase == 1 && m <= 1e-6) { phase = 2; tstop = t; }
                if (phase == 2 && t - tstop >= hold) { phase = 3; mt = 1; acc = 1.0; }
            } else if (t >= tman) switch (beh) {
                case RALLENTA: mt = fslow; acc = asl; break;
                case SOSTA: case SOSTALUNGA: if (phase == 0) { mt = 0; acc = ast; if (m <= 1e-6) { phase = 1; tstop = t; } } else if (t - tstop >= hold) { mt = 1; acc = 1.0; } break;
                case TORNA: if (phase == 0) { mt = 0; acc = 3.0; if (m <= 1e-6) { phase = 1; tstop = t; } } else if (t - tstop >= pause) { mt = -fback; acc = 1.5; } break;
                case SVOLTA: ght = turn; break;
                case LONTANO: { double d = atan2(py, px) - h; while (d > M_PI) d -= 2 * M_PI; while (d < -M_PI) d += 2 * M_PI; ght = d; } break;
                default: break; }
            double dm = mt - m, lim = acc / v0 * hs; if (dm > lim) dm = lim; if (dm < -lim) dm = -lim; m += dm;
            double dg = ght - gh, gl = (90 * M_PI / 180) * hs; if (dg > gl) dg = gl; if (dg < -gl) dg = -gl; gh += dg;
            double av = exp(-hs / 1.5), ah = exp(-hs / 2.0); ev = av * ev + sv * sqrt(1 - av * av) * rn(&r); eh = ah * eh + shd * sqrt(1 - ah * ah) * rn(&r);
            double hh = h + gh + eh + om * (t - T_PRE), sp = v0 * m * (1 + ev) * (1 + rip * sin(2 * M_PI * fstep * t + ph1));
            double vx = sp * cos(hh), vy = sp * sin(hh);
            if (fabs(px) <= W / 2 + 0.1 && py >= YP && py < YP + 0.15 + RB && vy < 0) { vx = 0; vy = 0; }
            px += vx * hs; py += vy * hs; s += v0 * m * hs; t += hs; } }
    if (mir) { for (int k = 0; k < nk; k++) T->x[k] = -T->x[k]; T->ex = -T->ex; }
}

/* ---- sensore: corpo esteso, baricentro della parte visibile, C6 sulla maschera stimata ---- */
#define NSP 37
static double SPX[NSP], SPY[NSP];
static void sp_init(void) { int n = 0; SPX[n] = 0; SPY[n++] = 0; for (int ring = 1; ring <= 3; ring++) for (int q = 0; q < 6 * ring; q++) { double a = 2 * M_PI * q / (6 * ring), rr = ring / 3.0; SPX[n] = rr * cos(a); SPY[n++] = rr * sin(a); } }
typedef struct { int grp, cut, acc; double f, zx, zy; } Obs;
static Obs sense(double x, double y, Rng *rm) {
    Obs o = {0, 0, 0, 0, 0, 0}; double u = ru(rm), n1 = rn(rm), n2 = rn(rm);
    if (RB <= 0) { int vis = indom(x, y) && !intrue(x, y); o.f = vis; o.grp = vis; o.cut = vis && dest(x, y) <= C6ADJ; o.zx = x + 0.05 * n1; o.zy = y + 0.05 * n2; }
    else { int nv = 0; double sx = 0, sy = 0, dmin = 1e9;
        for (int q = 0; q < NSP; q++) { double qx = x + RB * SPX[q], qy = y + RB * SPY[q]; if (!indom(qx, qy) || intrue(qx, qy)) continue; nv++; sx += qx; sy += qy; double d = dest(qx, qy); if (d < dmin) dmin = d; }
        o.f = (double)nv / NSP; o.grp = o.f >= 0.15; if (nv) { o.zx = sx / nv + 0.05 * n1; o.zy = sy / nv + 0.05 * n2; } o.cut = o.grp && dmin <= C6ADJ; }
    o.acc = o.grp && !o.cut && u < PD; return o;
}

/* ---- filtro del nucleo, un asse ---- */
typedef struct { double p, v, a, b, c; } K1;
static void kpred(K1 *s) { s->p += s->v * DT; double a = s->a, b = s->b, c = s->c; s->a = a + 2 * DT * b + DT * DT * c + QN * DT * DT * DT / 3; s->b = b + DT * c + QN * DT * DT / 2; s->c = c + QN * DT; }
static void kupd(K1 *s, double z) { double S = s->a + RV, k1 = s->a / S, k2 = s->b / S, y = z - s->p, a = s->a, b = s->b; s->p += k1 * y; s->v += k2 * y; s->a = a - k1 * a; s->b = b - k1 * b; s->c -= k2 * b; }

/* ---- sd-1: C-004 fronte + scia, pavimento, soglia «ampio», punto ibrido con attesa ---- */
static int NLIB = 0; static float LA[NLIBMAX][KH + 1], LC[NLIBMAX][KH + 1];
typedef struct { double p0x, p0y, v0x, v0y, ux, uy; float w[NM]; short frz[NM]; int ampio, floor_, ent, sw, hold, tok; double ptx, pty, tx, ty, area0; uint8_t *raw, *reg; int nraw, nreg; } Pred;
static void mpos(const Pred *t, int j, int i, double *x, double *y) {
    int lj = (j % (NM / 2)) % NLIB, ii = i, ir; if (j >= NM / 2 && ii > t->frz[j]) ii = t->frz[j]; ir = ii > KH ? KH : ii;
    double al = LA[lj][ir], cr = LC[lj][ir], bx = t->p0x + t->v0x * ii * DT, by = t->p0y + t->v0y * ii * DT;
    *x = bx + t->ux * al - t->uy * cr; *y = by + t->uy * al + t->ux * cr;
}
static void pred_init(Pred *t, K1 kx, K1 ky) {
    t->p0x = kx.p; t->p0y = ky.p; t->v0x = kx.v; t->v0y = ky.v; double sp = hypot(kx.v, ky.v); if (sp < 1e-6) { t->ux = 1; t->uy = 0; } else { t->ux = kx.v / sp; t->uy = ky.v / sp; }
    for (int j = 0; j < NM; j++) { t->w[j] = 1; t->frz[j] = 32000;
        if (j >= NM / 2) { int ien = -1, iex = KH; double x, y; t->frz[j] = KH;
            for (int i = 0; i <= KH; i++) { mpos(t, j, i, &x, &y); int cl = cls(x, y); if (ien < 0) { if (cl == 1) ien = i; } else if (cl != 1) { iex = i; break; } }
            if (ien < 0) ien = 0; double u = fmod((j - NM / 2 + 0.5) * 0.6180339887, 1.0); t->frz[j] = (short)(ien + (int)(u * (iex - ien))); } }
    t->ampio = t->floor_ = t->ent = t->sw = t->hold = t->tok = 0; t->ptx = kx.p; t->pty = ky.p; t->nraw = t->nreg = 0;
    if (!t->raw) { t->raw = calloc(NC, 1); t->reg = calloc(NC, 1); } else { memset(t->raw, 0, NC); memset(t->reg, 0, NC); }
}
static void smooth(const float *in, float *out) {
    for (int a = 0; a < NA; a++) out[AL[a]] = 0;
    for (int a = 0; a < NA; a++) { int c = AL[a]; if (in[c] <= 0) continue; float sh = in[c] / CNT[c]; int i = c % NX, j = c / NX;
        for (int dj = -1; dj <= 1; dj++) for (int di = -1; di <= 1; di++) { int ii = i + di, jj = j + dj; if (ii >= 0 && ii < NX && jj >= 0 && jj < NY) { int c2 = jj * NX + ii; if (AM[c2]) out[c2] += sh; } } }
}
static const float *SK; static int cmpd(const void *a, const void *b) { float x = SK[*(const int *)a], y = SK[*(const int *)b]; return (x < y) - (x > y); }
static void hdr(Pred *t, const float *d) { int m = 0; double tot = 0, cum = 0; for (int a = 0; a < NA; a++) { int c = AL[a]; if (d[c] > 0) { SIDX[m++] = c; tot += d[c]; } }
    if (tot <= 0) return; SK = d; qsort(SIDX, m, sizeof(int), cmpd); for (int q = 0; q < m; q++) { if (cum >= 0.90 * tot) break; t->raw[SIDX[q]] = 1; cum += d[SIDX[q]]; } }
/* un ciclo: i = cicli dall'ultima misura; (fx, fy) = punto del filtro */
static void pred_step(Pred *t, int i, double fx, double fy) {
    double S[2] = {0, 0}, sx = 0, sy = 0; for (int a = 0; a < NA; a++) { D1[AL[a]] = 0; D2[AL[a]] = 0; }
    memset(t->raw, 0, NC);
    for (int j = 0; j < NM; j++) { double x, y; mpos(t, j, i, &x, &y); int cl = cls(x, y), s = j >= NM / 2; if (cl == 0 || cl == 3) continue; if (cl == 2) { t->w[j] *= 0.1f; continue; }
        int c = cell_of(x, y); float w = t->w[j]; (s ? D2 : D1)[c] += w; S[s] += w; sx += w * x; sy += w * y; }
    for (int sc = 0; sc < 2; sc++) if (S[sc] > 0) { float *src = sc ? D2 : D1, *dst = D3; for (int q = 0; q < SMOOTH; q++) { dst = (src == D3) ? D4 : D3; smooth(src, dst); src = dst; } hdr(t, src); }
    int n = 0; for (int a = 0; a < NA; a++) n += t->raw[AL[a]];
    if (n == 0) { for (int a = 0; a < NA; a++) t->raw[AL[a]] = 1; n = NA; t->floor_ = 1; if (AMPIO_ON) t->ampio = 1; } else t->floor_ = 0;
    t->nraw = n; t->area0 = n * CELL * CELL;
    if (AMPIO_ON && (t->area0 > 0.8 * AREA_SH || i > 45)) t->ampio = 1;
    if (t->ampio) { memset(t->reg, 0, NC); for (int a = 0; a < NA; a++) t->reg[AL[a]] = 1; t->nreg = NA; } else { memcpy(t->reg, t->raw, NC); t->nreg = n; }
    t->tok = S[0] + S[1] > 0; if (t->tok) { t->tx = sx / (S[0] + S[1]); t->ty = sy / (S[0] + S[1]); }
    int c = cls(fx, fy);
    if (!t->sw) { if (c != 2) { t->ent = 1; t->ptx = fx; t->pty = fy; } else if (!t->ent && i <= 8) { t->ptx = fx; t->pty = fy; } else { t->sw = 1; t->hold = 0; } }
    if (t->sw) { t->hold++; if (t->hold > 8 && t->tok) { double dx = t->tx - t->ptx, dy = t->ty - t->pty, d = hypot(dx, dy), lim = VMAX * DT; if (d > lim) { dx *= lim / d; dy *= lim / d; }
            if (cls(t->ptx + dx, t->pty + dy) != 2) { t->ptx += dx; t->pty += dy; } } }
}
static double dist_reg(const uint8_t *reg, double x, double y) { double best = 1e9; for (int a = 0; a < NA; a++) { int c = AL[a]; if (reg[c]) { double d = hypot(CX[c] - x, CY[c] - y); if (d < best) best = d; } } return best; }

/* ---- statistiche ---- */
#define NTAU 4
static const int TK[NTAU] = {15, 30, 45, 75};
#define CAP 4000
typedef struct {
    int valid, invalid, scoperti, cyc_scop, fuori100, fuoriA, ricomp, riagg, amb_c1, amb_m7, amb_both, falsa_p, falsa_c, falsa_floor, ampio_prima, n_ep, back_p, ptfree_c, ptfree_p, gapc, cut_cyc, cut_oss, hidcyc, floorc;
    int n[NTAU], in_raw[NTAU], in_shown[NTAU], nT[NTAU], inT[NTAU]; double ar[NTAU]; int falsa_dopo, cut_altro, f_dist, f_bordo, shT[NTAU]; int nta; float ta[CAP];
    int nch; float ch[CAP]; int nal; float al[CAP]; int nce; float ce[CAP], fe[CAP]; int ng; float gd[CAP];
} St;
static St S_[NB];
static int cmpf(const void *a, const void *b) { float x = *(const float *)a, y = *(const float *)b; return (x > y) - (x < y); }
static double med(float *v, int n) { if (n <= 0) return NAN; qsort(v, n, sizeof(float), cmpf); return v[n / 2]; }

static Pred PR; static int GHOSTS = 0;
/* un passaggio con il ciclo di vita com'e' scritto. lib != NULL: registra un percorso residuo e ritorna. esito: 0 nessuna ricomparsa, 1 riagganciato, 2 ambiguo */
static int pass(int beh, uint64_t seed, int lively, float *la, float *lc, int *esito) {
    static Traj T; traj(&T, beh, seed, lively); Rng rm, ry; rseed(&rm, seed, 1000 + beh, (uint64_t)GEO); rseed(&ry, seed, 2000 + beh, (uint64_t)GEO);
    St *st = &S_[beh]; K1 kx = {0}, ky = {0}, sx_ = {0}, sy_ = {0}; int state = 0, nme = 0, miss = 0, klast = -1, kfirst = -1; double f1x = 0, f1y = 0, lzx = 0, lzy = 0;
    int everconf = 0, anyscop = 0, any100 = 0, anyA = 0, nchange = 0, falsa = 0, back = 0, ptfree = 0, ep_real = 0, ep_ampio = 0, first_out = 0, valid = 0, everhid = 0, done_lib = 0;
    double lpx = 0, lpy = 0, eux = 1, euy = 0, last_area = 0; int t_amp = -1; int lhas = 0; if (esito) *esito = 0;
    for (int k = 0; k < T.n; k++) {
        PSI = (YAWB + YAWJ * rn(&ry)) * M_PI / 180; if (YAWJ == 0) PSI = YAWB * M_PI / 180; masks();
        double x = T.x[k], y = T.y[k]; Obs o = sense(x, y, &rm); BVIS = o.f > 0; BX = x; BY = y;
        int tuttonasc = (o.f == 0) && indom(x, y), hid = !(o.grp && !o.cut);
        if (tuttonasc && !everhid) { everhid = 1; valid = everconf; if (!valid && !la) { st->invalid++; return 0; } if (!la) st->valid++; }
        int ct = cell_of(x, y); int tin = ct >= 0 && DOM[ct];
        if (!la && tuttonasc && tin) { if (!R100[ct]) any100 = 1; if (!AM[ct]) anyA = 1; }
        if (state == 1 && nme >= 2) { kpred(&kx); kpred(&ky); }
        if (state == 2) { kpred(&kx); kpred(&ky); }
        if (state == 0 || state == 3) { if (o.acc) { state = 1; nme = 1; miss = 0; kfirst = k; f1x = o.zx; f1y = o.zy; klast = k; lzx = o.zx; lzy = o.zy; nchange++; } }
        else if (state == 1) {
            if (o.acc) { if (nme == 1) { double dt = (k - kfirst) * DT; kx.p = o.zx; kx.v = (o.zx - f1x) / dt; kx.a = RV; kx.b = RV / dt; kx.c = 2 * RV / (dt * dt); ky = kx; ky.p = o.zy; ky.v = (o.zy - f1y) / dt; }
                else { kupd(&kx, o.zx); kupd(&ky, o.zy); }
                nme++; if (nme >= 4) everconf = 1; miss = 0; klast = k; lzx = o.zx; lzy = o.zy; sx_ = kx; sy_ = ky; }
            else { miss++;
                if (nme >= 4) { int ent = dest(lzx, lzy) < 0.40 || dest(kx.p, ky.p) <= 0.40;      /* M1 com'e' scritta */
                    if (ent && !la && !(o.grp && o.cut) && miss < M1N) ent = 0;
                    if (ent) { if (la) { /* taratura: percorso residuo dal punto dell'ultima misura */
                            double sp = hypot(sx_.v, sy_.v), c = sp > 1e-6 ? sx_.v / sp : 1, s = sp > 1e-6 ? sx_.v * 0 + sy_.v / sp : 0;
                            for (int i = 0; i <= KH; i++) { int kk = klast + i; if (kk >= T.n) kk = T.n - 1; double ex = T.x[kk] - (sx_.p + sx_.v * i * DT), ey = T.y[kk] - (sy_.p + sy_.v * i * DT); la[i] = (float)(ex * c + ey * s); lc[i] = (float)(-ex * s + ey * c); }
                            done_lib = 1; return 1; }
                        state = 2; nchange++; pred_init(&PR, sx_, sy_); if (hypot(sx_.v, sy_.v) < VMIN) PR.ampio = 1; t_amp = -1; eux = PR.ux; euy = PR.uy; lhas = 0; ep_real = 0; ep_ampio = 0;
                        if (!hid) { falsa++; st->falsa_c++; if (everhid) st->falsa_dopo++; }
                        for (int i = 1; i < k - klast; i++) pred_step(&PR, i, sx_.p + sx_.v * i * DT, sy_.p + sy_.v * i * DT); }
                    else if (miss >= 3) { state = 3; nchange++; } }
                else if (miss >= 3) { state = 0; nme = 0; } } }
        if (state == 2) { int i = k - klast;
            if (o.acc && i > 0 && PR.nreg > 0 && k > klast) { /* ricomparsa: «Ritorno» del nucleo E porta M7 */
                double r = hypot(o.zx, o.zy), th = fabs(atan2(o.zx, o.zy));
                int c1d = dest(o.zx, o.zy) <= RH, c1b = !BORDO || (RMAX - r > 0.40 && r * sin(fmax(HFOV - th, 0.0)) > 0.40), c1 = c1d && c1b && (GHOSTS == 0 || !ASSORB);
                double dg = dist_reg(PR.reg, o.zx, o.zy); int m7 = dg <= 0.40;
                if (ep_real && !first_out) { first_out = 1; st->ricomp++; if (st->ng < CAP) st->gd[st->ng++] = (float)dg;
                    if (!c1d) st->f_dist++; if (!c1b) st->f_bordo++; if (c1 && m7) st->riagg++; else if (!c1 && !m7) st->amb_both++; else if (!c1) st->amb_c1++; else st->amb_m7++;
                    if (ep_ampio) st->ampio_prima++; if (st->nta < CAP) st->ta[st->nta++] = (float)((t_amp >= 0 ? t_amp : i) * DT); if (st->nal < CAP) st->al[st->nal++] = (float)(last_area / AREA_SH); st->n_ep++; if (esito) *esito = (c1 && m7) ? 1 : 2; }
                if (c1 && m7) { kupd(&kx, o.zx); kupd(&ky, o.zy); state = 1; nme++; miss = 0; klast = k; lzx = o.zx; lzy = o.zy; sx_ = kx; sy_ = ky; nchange++; }
                else { GHOSTS++; state = 1; nme = 1; miss = 0; kfirst = k; f1x = o.zx; f1y = o.zy; klast = k; lzx = o.zx; lzy = o.zy; nchange++; }
            } else if (i > 0) {
                pred_step(&PR, i, kx.p, ky.p); st->hidcyc++; if (PR.floor_) st->floorc++; if (PR.nreg == 0) st->gapc++;
                if (tuttonasc) ep_real = 1; if (PR.ampio && hid) ep_ampio = 1; if (PR.ampio && t_amp < 0) t_amp = i; if (hid) last_area = PR.area0;
                if (PR.floor_ && falsa && i <= 2) st->falsa_floor++;
                if (o.grp && o.cut) { st->cut_cyc++; }
                if (lhas) { double dx = PR.ptx - lpx, dy = PR.pty - lpy; if (dx * eux + dy * euy < -0.05) back = 1; }
                lpx = PR.ptx; lpy = PR.pty; lhas = 1;
                if (i > 5 && cls(PR.ptx, PR.pty) == 2) { st->ptfree_c++; ptfree = 1; }
                if (PR.ampio && hid && st->nce < CAP && (k % 5) == 0) { st->ce[st->nce] = (float)hypot(PR.ptx - x, PR.pty - y); st->fe[st->nce] = (float)hypot(SHCX - x, SHCY - y); st->nce++; }
                for (int q = 0; q < NTAU; q++) if (TK[q] == i && hid) { st->n[q]++; if (tin && PR.raw[ct]) st->in_raw[q]++; if (tin && PR.reg[ct]) st->in_shown[q]++; st->ar[q] += PR.area0 / AREA_SH; if (tuttonasc) { st->nT[q]++; if (tin && PR.raw[ct]) st->inT[q]++; if (tin && PR.reg[ct]) st->shT[q]++; } } } }
        if (!la && tuttonasc && state != 2 && GHOSTS == 0) { anyscop = 1; st->cyc_scop++; }
        if (!la && o.grp && o.cut && state != 2) st->cut_altro++;
    }
    (void)done_lib;
    if (la) return 0;
    if (!everhid) { if (beh == FERMOVISTA || beh == SBIRCIA) st->valid++; else { st->invalid++; return 0; } }
    st->scoperti += anyscop; st->fuori100 += any100; st->fuoriA += anyA; st->falsa_p += falsa > 0; st->back_p += back; st->ptfree_p += ptfree;
    if (st->nch < CAP) st->ch[st->nch++] = (float)nchange;
    return 1;
}

static void build_lib(void) {
    double e = E_MASK, pd = PD, yb = YAWB, yj = YAWJ; char g = GEO; E_MASK = 0; PD = 0.9; YAWB = YAWJ = 0; if (GEO == 'L') GEO = 'T'; geo_set(); PSI = 0; PSI_MASK = 1e9; masks();
    NLIB = 0; for (long s = 100000; NLIB < NLIB_WANT && s < 100000 + 20 * NLIB_WANT; s++) if (pass(PROSEGUE, (uint64_t)s, LIB_LIVELY, LA[NLIB], LC[NLIB], NULL)) NLIB++;
    E_MASK = e; PD = pd; YAWB = yb; YAWJ = yj; GEO = g; geo_set(); PSI_MASK = 1e9; memset(S_, 0, sizeof(S_));
}
static double now_ms(void) { struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts); return ts.tv_sec * 1e3 + ts.tv_nsec * 1e-6; }
static void args(int argc, char **argv) {
    for (int a = 2; a < argc; a++) { char *eq = strchr(argv[a], '='); if (!eq) continue; *eq = 0; const char *k = argv[a], *v = eq + 1;
        if (!strcmp(k, "geo")) GEO = v[0]; else if (!strcmp(k, "e")) E_MASK = atof(v); else if (!strcmp(k, "pd")) PD = atof(v); else if (!strcmp(k, "rb")) RB = atof(v);
        else if (!strcmp(k, "c6")) C6ADJ = atof(v); else if (!strcmp(k, "yawb")) YAWB = atof(v); else if (!strcmp(k, "yawj")) YAWJ = atof(v); else if (!strcmp(k, "omega")) OMEGA = atof(v);
        else if (!strcmp(k, "vlo")) VLO = atof(v); else if (!strcmp(k, "vhi")) VHI = atof(v); else if (!strcmp(k, "nlib")) NLIB_WANT = atoi(v); else if (!strcmp(k, "libviv")) LIB_LIVELY = atoi(v);
        else if (!strcmp(k, "viv")) TEST_LIVELY = atoi(v); else if (!strcmp(k, "n")) NSEED = atoi(v); else if (!strcmp(k, "seme")) SEED0 = atol(v); else if (!strcmp(k, "beh")) BEHS = v;
        else if (!strcmp(k, "rh")) RH = atof(v); else if (!strcmp(k, "vmin")) VMIN = atof(v); else if (!strcmp(k, "assorb")) ASSORB = atoi(v); else if (!strcmp(k, "m1n")) M1N = atoi(v); else if (!strcmp(k, "bordo")) BORDO = atoi(v);
        else if (!strcmp(k, "ampio")) AMPIO_ON = atoi(v); else if (!strcmp(k, "lisc")) SMOOTH = atoi(v); else { fprintf(stderr, "chiave ignota %s\n", k); exit(1); } *eq = '='; }
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "uso: att prova|sessione|tempo chiave=valore...\n"); return 1; }
    args(argc, argv); geo_set(); grid_alloc(); sp_init(); build_lib();
    printf("#"); for (int a = 1; a < argc; a++) printf(" %s", argv[a]); printf("\n# geo=%c e=%.2f pd=%.2f rb=%.3f c6=%.2f imbardata fissa=%.1f tremolio=%.1f gradi; libreria %d percorsi (vivaci=%d); prova vivaci=%d; curva=%.1f gradi/s; v=%.1f-%.1f\n", GEO, E_MASK, PD, RB, C6ADJ, YAWB, YAWJ, NLIB, LIB_LIVELY, TEST_LIVELY, OMEGA, VLO, VHI);
    if (!strcmp(argv[1], "tempo")) { int nt = NSEED; Pred *P = calloc(nt, sizeof(Pred)); PSI = 0; masks(); static float tm[8000]; int n = 0;
        for (int rep = 0; rep < 20; rep++) { for (int q = 0; q < nt; q++) { K1 kx = {-(TA * YS + 0.3) - 0.01 * (q % 20), 0.6 + 0.04 * (q % 25), 0.0008, 0.004, 0.04}, ky = {YS, 0.05, 0.0008, 0.004, 0.04}; pred_init(&P[q], kx, ky); }
            for (int i = 1; i <= 75; i++) { double a = now_ms(); for (int q = 0; q < nt; q++) pred_step(&P[q], i, P[q].p0x + P[q].v0x * i * DT, P[q].p0y); tm[n++] = (float)(now_ms() - a); } }
        qsort(tm, n, sizeof(float), cmpf); printf("TEMPO geo=%c tracce=%d celle_A=%d cicli=%d mediana=%.3f ms p95=%.3f ms max=%.3f ms\n", GEO, nt, NA, n, tm[n / 2], tm[(int)(0.95 * n)], tm[n - 1]); return 0; }
    if (!strcmp(argv[1], "sessione")) { /* 120 passaggi di fila, 30 per comportamento di BEHS, mescolati; le pendenti restano (regola 2 del §2.5) */
        int nb = (int)strlen(BEHS), np = 30 * nb, ord[400]; Rng r; rseed(&r, (uint64_t)SEED0, 5, 5); for (int p = 0; p < np; p++) ord[p] = BEHS[p % nb] - '0';
        for (int p = np - 1; p > 0; p--) { int q = (int)(ru(&r) * (p + 1)); int t = ord[p]; ord[p] = ord[q]; ord[q] = t; }
        int first = -1, riagg_dopo = 0, ric_dopo = 0, riagg = 0, ric = 0; GHOSTS = 0;
        for (int p = 0; p < np; p++) { int es = 0, g0 = GHOSTS; pass(ord[p], (uint64_t)(SEED0 + p), TEST_LIVELY, NULL, NULL, &es);
            if (es) { ric++; if (es == 1) riagg++; if (first >= 0) { ric_dopo++; if (es == 1) riagg_dopo++; } }
            if (first < 0 && GHOSTS > g0) first = p + 1; }
        printf("SESSIONE geo=%c passaggi=%d ricomparse=%d riagganciate=%d prima_ambigua_al_passaggio=%d ricomparse_dopo=%d riagganciate_dopo=%d pendenti_alla_fine=%d\n", GEO, np, ric, riagg, first, ric_dopo, riagg_dopo, GHOSTS); return 0; }
    double t0 = now_ms();
    for (int b = 0; b < NB; b++) { if (!strchr(BEHS, '0' + b)) continue; for (int s = 0; s < NSEED; s++) { GHOSTS = 0; pass(b, (uint64_t)(SEED0 + s), TEST_LIVELY, NULL, NULL, NULL); } }
    printf("# ombra stimata %.2f m2, celle di A %d; lancio %.1f s\n", AREA_SH, NA, (now_ms() - t0) / 1e3);
    for (int b = 0; b < NB; b++) { if (!strchr(BEHS, '0' + b)) continue; St *s = &S_[b];
        printf("%-14s validi=%d scartati=%d | R90 grezza a 1/2/3/5 s:", BN[b], s->valid, s->invalid);
        for (int q = 0; q < NTAU; q++) printf(" %d/%d=%.3f", s->in_raw[q], s->n[q], s->n[q] ? (double)s->in_raw[q] / s->n[q] : NAN);
        printf(" | mostrata:"); for (int q = 0; q < NTAU; q++) printf(" %.3f", s->n[q] ? (double)s->in_shown[q] / s->n[q] : NAN);
        printf(" | a corpo tutto nascosto:"); for (int q = 0; q < NTAU; q++) printf(" %d/%d=%.3f", s->inT[q], s->nT[q], s->nT[q] ? (double)s->inT[q] / s->nT[q] : NAN);
        printf(" | mostrata, tutto nascosto:"); for (int q = 0; q < NTAU; q++) printf(" %.3f", s->nT[q] ? (double)s->shT[q] / s->nT[q] : NAN);
        printf(" | area/ombra:"); for (int q = 0; q < NTAU; q++) printf(" %.2f", s->n[q] ? s->ar[q] / s->n[q] : NAN);
        printf("\n    scoperti=%d (cicli %d) fuori_R100=%d centro_su_visto_libero=%d | ricomparsi=%d riagganciati=%d ambigui: solo_nucleo=%d solo_M7=%d entrambi=%d | ampio_prima_della_ricomparsa=%d/%d area_ultimo_ciclo_med=%.2f dist_porta_med=%.2f\n",
               s->scoperti, s->cyc_scop, s->fuori100, s->fuoriA, s->ricomp, s->riagg, s->amb_c1, s->amb_m7, s->amb_both, s->ampio_prima, s->n_ep, med(s->al, s->nal), med(s->gd, s->ng));
        printf("    false_entrate: passaggi=%d cicli=%d con_pavimento=%d | cambi_di_stato_med=%.0f | punto: passaggi_con_arretramento=%d su_libero_dopo5: cicli=%d passaggi=%d | cicli_previsti=%d pavimento=%d vuoti=%d corpo_tagliato_visibile_in_previsto=%d in_altri_stati=%d false_entrate_dopo_il_buio=%d\n",
               s->falsa_p, s->falsa_c, s->falsa_floor, med(s->ch, s->nch), s->back_p, s->ptfree_c, s->ptfree_p, s->hidcyc, s->floorc, s->gapc, s->cut_cyc, s->cut_altro, s->falsa_dopo);
        static float a1[CAP], a2[CAP]; memcpy(a1, s->ce, s->nce * sizeof(float)); memcpy(a2, s->fe, s->nce * sizeof(float));
        printf("    in ampio (n=%d): errore mediano croce=%.2f m, segno fisso al baricentro dell'ombra=%.2f m | nucleo fallito per distanza=%d per bordo=%d | tempo al segno ampio (o alla ricomparsa), mediana=%.2f s\n", s->nce, med(a1, s->nce), med(a2, s->nce), s->f_dist, s->f_bordo, med(s->ta, s->nta)); }
    return 0;
}
