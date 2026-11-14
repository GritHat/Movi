# Trasforma la copia del banco (banco.c di 11-misure, sha256 e158c7a9...) in comp.c: aggiunge i predittori sd-1 e sd-0.
import sys
s = open('comp.c').read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:60], s.count(a))
    s = s.replace(a, b)
rep('P_C004M, NPRED };', 'P_C004M, P_SD1, P_SD0, NPRED };')
rep('"C-EST-B-senzafascia", "C-004m"};', '"C-EST-B-senzafascia", "C-004m", "sd-1", "sd-0"};')
rep('    Out out[NPRED];\n} Trk;', '    double c4tx, c4ty; int c4tok;                                   /* baricentro grezzo dei membri non visti liberi */\n    double sdx[2], sdy[2]; int sdent[2], sdsw[2], sdhold[2];        /* sd-1, sd-0: punto ibrido con attesa */\n    Out out[NPRED];\n} Trk;')
rep('    t->h9x = kx.p; t->h9y = ky.p; t->h9free = 0; t->h9sw = 0;', '    t->h9x = kx.p; t->h9y = ky.p; t->h9free = 0; t->h9sw = 0;\n    for (int v = 0; v < 2; v++) { t->sdx[v] = kx.p; t->sdy[v] = ky.p; t->sdent[v] = t->sdsw[v] = t->sdhold[v] = 0; }\n    t->c4tok = 0;')
rep('    om->px = t->c4mx; om->py = t->c4my;\n}', '''    om->px = t->c4mx; om->py = t->c4my;
    t->c4tok = S[0] + S[1] > 0; if (t->c4tok) { t->c4tx = (sx[0] + sx[1]) / (S[0] + S[1]); t->c4ty = (sy[0] + sy[1]) / (S[0] + S[1]); }
}

/*== PRED sd-1 e sd-0 (sciame-scene-dinamiche, f8 fase f3): regione con pavimento, punto ibrido con attesa ==*/
#define SD_HOLD 8
static long SD_FLOOR[2];
static void sd_point(Trk *t, int v, int i, int tok, double tx, double ty, Out *o) {
    double fx = t->kx.p, fy = t->ky.p; int c = cls(fx, fy);
    if (!t->sdsw[v]) {
        if (c != 2) { t->sdent[v] = 1; t->sdx[v] = fx; t->sdy[v] = fy; }
        else if (!t->sdent[v] && i <= 8) { t->sdx[v] = fx; t->sdy[v] = fy; }
        else { t->sdsw[v] = 1; t->sdhold[v] = 0; } }
    if (t->sdsw[v]) { t->sdhold[v]++;
        if (t->sdhold[v] > SD_HOLD && tok) { double dx = tx - t->sdx[v], dy = ty - t->sdy[v], d = hypot(dx, dy), lim = VMAX * DT;
            if (d > lim) { dx *= lim / d; dy *= lim / d; }
            if (cls(t->sdx[v] + dx, t->sdy[v] + dy) != 2) { t->sdx[v] += dx; t->sdy[v] += dy; } } }
    o->has_pt = 1; o->px = t->sdx[v]; o->py = t->sdy[v];
}
static void sd_floor(Out *o, int v) { if (!o->has_reg) { for (int a = 0; a < G.nA; a++) out_mark(o, G.A[a], 1); SD_FLOOR[v]++; } }
static void step_sd(Trk *t, int i) {
    /* sd-1: R90 di C-004 a un livello, con pavimento; punto: filtro, attesa, poi baricentro dei membri */
    Out *o = &t->out[P_SD1], *c4 = &t->out[P_C004]; out_clear(o);
    if (c4->has_reg) for (int j = c4->j0; j <= c4->j1; j++) for (int ii = c4->i0; ii <= c4->i1; ii++) { int c = j * G.nx + ii; if (c4->reg[c]) out_mark(o, c, 1); }
    sd_floor(o, 0);
    sd_point(t, 0, i, t->c4tok, t->c4tx, t->c4ty, o);
    /* sd-0: disco da tabella (C-005) a un livello, con pavimento; punto: filtro, attesa, poi baricentro della regione */
    o = &t->out[P_SD0]; out_clear(o); fill_disc(o, t->kx.p, t->ky.p, TAB90[i], -1, G.inA);
    sd_floor(o, 1);
    double sx = 0, sy = 0; int n = 0;
    for (int j = o->j0; j <= o->j1; j++) for (int ii = o->i0; ii <= o->i1; ii++) { int c = j * G.nx + ii; if (o->reg[c]) { sx += G.cx[c]; sy += G.cy[c]; n++; } }
    sd_point(t, 1, i, n > 0, n ? sx / n : 0, n ? sy / n : 0, o);
}''')
rep('static void step_all(Trk *t, int i) { step_basi(t, i); step_c004(t, i); if (ONLY_C004) return;', 'static void step_all(Trk *t, int i) { step_basi(t, i); step_c004(t, i); step_sd(t, i); if (ONLY_C004) return;')
# contatore: punto su libero dopo il quinto ciclo
rep('w50, w80, w08, nre, re40, re30, gate95, ngate, cyc0530, in0530; double stepsum; int nstep;', 'w50, w80, w08, nre, re40, re30, gate95, ngate, cyc0530, in0530, fptlate; double stepsum; int nstep;')
rep('if (cls(o->px, o->py) == 2) { pc->fptc++; anyfpt[p] = 1; }', 'if (cls(o->px, o->py) == 2) { pc->fptc++; anyfpt[p] = 1; if (i > 5) pc->fptlate++; }')
rep('\\tcicli0530=%d\\tdentro0530=%d\\n",', '\\tcicli0530=%d\\tdentro0530=%d\\tpunto_su_libero_dopo5=%d\\n",')
rep('pc->gate95, pc->ngate, pc->cyc0530, pc->in0530);', 'pc->gate95, pc->ngate, pc->cyc0530, pc->in0530, pc->fptlate);')
rep('    printf("# tempo del lancio %.1f s\\n", (now_ms() - t0) / 1e3);', '    printf("# tempo del lancio %.1f s\\n", (now_ms() - t0) / 1e3);\n    printf("# cicli con il pavimento: sd-1 %ld, sd-0 %ld\\n", SD_FLOOR[0], SD_FLOOR[1]);')
# tempi: sd dopo C-004
rep('static float tm[5][40000]; int n = 0; const char *gn[5] = {"basi(L0,L1,L2,L2r,L2q,L3,C-005)", "C-004", "C-001(2000 particelle)", "C-EST(4 varianti)", "tutti"};',
    'static float tm[6][40000]; int n = 0; const char *gn[6] = {"basi(L0,L1,L2,L2r,L2q,L3,C-005)", "C-004", "C-001(2000 particelle)", "C-EST(4 varianti)", "tutti", "sd-1+sd-0 (in piu\' di C-004)"};')
rep('e = now_ms(); tm[0][n] = (float)(b - a);', 'e = now_ms(); for (int q = 0; q < nt; q++) step_sd(&TR[q], i); double f5 = now_ms(); tm[5][n] = (float)(f5 - e); tm[0][n] = (float)(b - a);')
rep('for (int q = 0; q < 5; q++) printf("T\\t%c\\t%d\\t%s\\tmediana', 'for (int q = 0; q < 6; q++) printf("T\\t%c\\t%d\\t%s\\tmediana')
open('comp.c', 'w').write(s)
print('ok')
