# Previsioni dell'esperto di dominio (f14, 01-profili)

Scritte alle 2026-11-14T18:34:21+01:00, prima di aprire qualsiasi fonte in rete e prima di scrivere o eseguire il programma dei conti.
Formula: d_avv = v_rel·(τ + T_r) + s_arr(portatore) + margine, con τ = 0,155 s (stimata, non misurata), margine = w = 0,40 m,
v_rel = v_classe + v_ego (avvicinamento frontale, caso peggiore), s_arr = v_ego²/(2·a_fr). Portata dichiarata: 3 m.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| E1 | Pedone a passo normale (circa 1,4 m/s) verso stazione fissa con una persona che reagisce (T_r circa 1 s): coperto dai 3 m | d_avv | smentita se d_avv > 3,0 m |
| E2 | Auto a 8 m/s verso stazione fissa, stessa T_r: non coperta, serve una portata di circa 10 m | d_avv | smentita se d_avv <= 3,0 m, o se la portata necessaria esce da 8–12 m |
| E3 | Almeno 8 delle classi in tabella (alla velocità tipica, stazione fissa, T_r della persona) chiedono più di 3 m | conteggio | smentita se sono meno di 8 |
| E4 | Persona non vedente che cammina (circa 1 m/s) verso un ostacolo FERMO: coperta dai 3 m; verso un pedone che le viene incontro a passo normale: NON coperta | d_avv per i due casi | smentita se il primo > 3,0 m o il secondo <= 3,0 m |
| E5 | Con l'arresto automatico (T_r <= 0,3 s) di un veicolo terrestre lento (<= 1 m/s) i 3 m coprono il pedone a 1,4 m/s ma nessun veicolo a più di 5 m/s | d_avv | smentita se un veicolo a > 5 m/s rientra nei 3 m o se il pedone ne esce |
| E6 | Treno e aereo: la distanza d'avviso utile è decine di metri o più (> 20 m) anche a velocità di manovra; nessuna camera di profondità a 3 m li copre | d_avv | smentita se d_avv <= 20 m per treno in arrivo in banchina o aereo in rullaggio |
| E7 | Fonti: almeno due terzi dei valori di velocità delle classi avranno una fonte aperta oggi; accelerazioni e frenate di pedone, bicicletta e carrello resteranno in buona parte «ipotesi» | quota di valori con fonte aperta | smentita se meno di metà delle velocità ha una fonte aperta |

Esiti: in fondo a PROFILI.md (regge, smentita, non risolta), distinti da ciò che ho notato dopo.

## Esiti (scritti alle 2026-11-14T18:42:33+01:00, dopo i conti; uscita in conti_uscita.md, sezione E)

| # | misura | esito |
|---|---|---|
| E1 | d_avv = 2,02 m | regge |
| E2 | d_avv a 8 m/s = 9,64 m | regge |
| E3 | 10 classi su 15 oltre 3 m (11 al primo conto, prima di portare il mezzo di piazzale da 2,8 a 1,7 m/s dopo la lettura del PDF di Monaco) | regge |
| E4 | ostacolo fermo 2,06 m; pedone incontro 3,67 m | regge |
| E5 | pedone 1,83 m; veicolo a 5 m/s 3,46 m | regge |
| E6 | treno in banchina 13,11 m; aereo in rullaggio 10,79 m | smentita (avevo confuso lo spazio d'arresto della classe con la distanza d'avviso per chi sta fermo) |
| E7 | velocità con fonte aperta oggi: 9 su 30; solo in un risultato di ricerca: 6; ipotesi o memoria: 15 | smentita |

Notato dopo, non previsto: il multirotore a 3 m/s non copre nemmeno un ostacolo fermo (3,26 m); il passo svelto massimo (2,5 m/s) esce dai 3 m (3,29 m); la persona non vedente che cammina copre solo chi le viene incontro a meno di 0,82 m/s.
