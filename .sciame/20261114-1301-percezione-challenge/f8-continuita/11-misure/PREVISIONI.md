# Previsioni del banco di prova indipendente — `sciame-validazione`, f8, fase f4

Scritte alle **2026-11-14T16:06:00+01:00** (`date -Is`), **prima** di scrivere una riga del banco e prima di ogni
lancio. Ho letto: contratto, triage, preproposta (§2 e §5), `SOLUZIONE_V2.md` (B4, B5), le sezioni «proposte» di
creativo, ricercatore, tracciamento, inferenza, kalman, rovesciatore, e di `sim_v2.py` solo le classi `KF1`, `Geo` e
la funzione `pass_v2` (la regola del nucleo). Non ho aperto il codice di nessuna candidata né i generatori altrui.
Conosco quindi i numeri che gli autori dichiarano: le previsioni sono cieche rispetto al mio banco, non rispetto a quei
numeri.

Soglie: quelle del triage (§6, «Soglie, fissate ora»). Qui scrivo che cosa mi aspetto e che cosa mi smentisce.

| # | Previsione | Misura | Mi smentisce |
|---|---|---|---|
| P-val-1 | La regola del nucleo (L0) **non** rispetta C1a: in ogni cella sul percorso di T e L più del 50 % dei passaggi ha almeno un ciclo nascosto senza regione; su «sosta lunga» la regione c'è in meno del 20 % dei cicli nascosti | passaggi con vuoto / 400; quota dei cicli con regione | una cella sul percorso di T con vuoti in meno del 10 % dei passaggi |
| P-val-2 | K-211: in D, su «prosegue», con C6, la durata mediana del «previsto» di L0 è 0,6–1,0 s (non 0,40–0,53) | mediana della durata | mediana fuori da 0,6–1,0 s |
| P-val-3 | K-202: in D su «prosegue» la soglia «metà» scatta prima della ricomparsa nel 55–85 % dei passaggi | quota dei passaggi | quota fuori da 55–85 % |
| P-val-4 | Il filtro lasciato correre (L2, q = 0,2), regione al 90 %: «prosegue» ≥ 0,85 fino a 3 s; «torna» e «sosta» a 2 s sotto 0,60 | copertura per cella | «torna» o «sosta» ≥ 0,80 a 2 s in T |
| P-val-5 | Braccio che deve fallire: q = 0,01 copre «prosegue» a 2 s sotto 0,85 e la «squadra» sotto 0,75 | copertura | «prosegue» ≥ 0,85: il banco è cieco alla troppa sicurezza |
| P-val-6 | C-005 (tabella sul peggiore, tarata in D e T): in D e T ogni cella sul percorso ≥ 0,85 fino a 3 s; in L (mai tarata) il minimo sul percorso sta fra 0,75 e 0,92; l'area di R90 in T supera 0,60 dell'ombra già a 2 s (soglia d'area smentita) | copertura, area / ombra | in D o T una cella < 0,85; in T area ≤ 0,60 a 2 e 3 s |
| P-val-7 | C-004 (fronte + scia): ≥ 0,85 in almeno il 90 % delle celle sul percorso (n ≥ 30) di D, T, L fino a 5 s; area in T ≤ 0,50 dell'ombra a 2–3 s; «svolta» e «lato lontano» sotto 0,50 a 2 s; R50 sulla «squadra» fuori da 0,40–0,60 ad almeno un τ | copertura, area | meno dell'80 % delle celle ≥ 0,85; oppure area > 0,60 |
| P-val-8 | C-001 (particelle con sosta): cade sotto 0,85 su «torna» a 2–3 s o su «sosta lunga» a 5 s (non ha un modo «torna»; le particelle ferme ripartono) | copertura | tutte le celle sul percorso ≥ 0,85 |
| P-val-9 | C-EST, K-201: in almeno una lettura, su «sosta lunga» in T o L ci sono cicli senza regione (σ_eff > 0,8 m → «perso»): C1a smentita. In D mai «perso» (l'ombra è piccola) | passaggi con cicli senza regione | 0 passaggi nelle due letture in T e L |
| P-val-10 | C-EST, K-206: la regione dichiarata (ellisse al 95 %) contiene chi sosta a 3 s in meno dello 0,85 dei passaggi in T (lettura A) e in L (tutte e due) | copertura «sosta» a 3 s | ≥ 0,85 in T-A e in L |
| P-val-11 | C-EST, attacco 1: 0 cicli di «previsto» su celle libere oltre la fascia (per costruzione); il peso del transito oltre 0,5 s dopo l'uscita attesa resta dominante in ≤ 5 % dei passaggi (lettura A: 0); a sosta improvvisa in D la regione contiene il vero in ≥ 0,85 dei cicli (lettura A) | cicli; passaggi; quota | un ciclo su libero oltre la fascia; peso dominante in > 5 % |
| P-val-12 | C-EST, attacco 5: l'errore alla ricomparsa sta nell'ellisse al 95 % in meno del 90 % dei passaggi, già su «prosegue» (la regione ritagliata non può contenere una misura che cade su spazio visto) | quota | ≥ 0,90 su «prosegue» |
| P-val-13 | L3 (raggiungibile ∩ non visto libero) contiene il vero nascosto nel 100 % dei cicli; da 2 s copre oltre 0,60 dell'ombra | copertura, area | un ciclo fuori |
| P-val-14 | K-203: nessun punto è «non peggiore di fermo» a ogni τ ≤ 5 s sulla «squadra» in tutte e tre le geometrie | errore mediano | un punto che non perde mai con L1 |
| P-val-15 | K-204: il punto ibrido (C-009) tocca celle libere oltre la fascia in 1–20 % dei passaggi; la media condizionata (C-008) mai | passaggi | C-009: 0 passaggi |
| P-val-16 | K-205 e regola della scadenza: in T, a 2 e 3 s, C-004 ha un'area di R90 ≤ 1,2 volte C-001 e almeno un terzo più stretta di C-005 | rapporti d'area | uno dei due rapporti violato |
| P-val-17 | C6: in C, ogni predittore sta sotto 6,7 ms per ciclo al 95º percentile, anche con dieci tracce | tempo | un predittore oltre 6,7 ms con dieci tracce |
| P-val-18 | C4: con la fascia 0,20 m e C6 a 0,22 m il ritaglio toglie il vero in pochi passaggi (> 0 ma < 2 %) per l'incoerenza 0,20 / 0,22 del protocollo; con l'ombra a −20 cm e fascia 0 in oltre il 50 % dei passaggi | passaggi | 0 nel braccio a −20 cm senza fascia: il banco è cieco |

**Esito atteso d'insieme, scritto ora:** la regola attuale del nucleo non rispetta l'imperativo (P-val-1); C-EST com'è
scritta non lo rispetta (P-val-9, 10, 12); C-005 lo rispetta sulla copertura ma con una regione larga quanto l'ombra;
C-004 è la candidata che regge con la regione più stretta, e cede su chi lascia il percorso.

Le scelte del banco che non stanno nel protocollo (letture mie) sono elencate in `BANCO_DI_PROVA.md`, §«Letture».

---

# Esiti (scritti DOPO le prove, alle 2026-11-14T16:35+01:00; numeri da `risultati/TABELLE.txt`)

| # | Esito | Numeri (rilevamento 0,9; D / T / L) |
|---|---|---|
| P-val-1 | **regge** la prima metà; la seconda **smentita** in T e L | passaggi con un vuoto 1958/1958, 1991/2000, 1999/2000; su «sosta lunga» la regione c'è nel 13,4 / 36,7 / 30,9 % dei cicli (avevo detto < 20 %) |
| P-val-2 | **regge** | mediana 0,667 s (quartili 0,60–0,73) |
| P-val-3 | **smentita** (più del previsto) | 332 su 355 = 93,5 % |
| P-val-4 | **smentita** | «torna» e «sosta» a 2 s: 0,855 e 0,858 in T (0,744 e 0,796 in D); «prosegue» a 3 s 0,815 in D |
| P-val-5 | **smentita su «prosegue»**, regge sulle manovre | q = 0,01: «prosegue» a 2 s 0,989 (T), 0,990 (L), 0,841 (D); «squadra» 0,76; 14 celle su 20 sotto soglia in T. Il banco **non vede** la troppa sicurezza su «prosegue» in T e L |
| P-val-6 | **regge** in D e T e per l'area; l'intervallo per L **smentito** (meglio) | minimo 0,891 / 0,902 / 0,958; area in T a 2 s: 1,07 dell'ombra |
| P-val-7 | **regge** (copertura, area, R50); «fuori percorso sotto 0,50» **smentita** | 25 celle su 25 ≥ 0,85 in D, T, L; area T 0,27 e 0,36; svolta 0,58, lontano 0,54 a 2 s (T); R50 0,94 → 0,46 |
| P-val-8 | **smentita** | C-001: minimo sul percorso 0,946 / 0,993 / 0,998 |
| P-val-9 | **regge** | passaggi con cicli senza regione: A 2 / 374 / 1976, B 2 / 1312 / 1987 su circa 2000 |
| P-val-10 | **regge** | «sosta» a 3 s: T 0,718 (A) e 0,532 (B); L 0,135 e 0,000 |
| P-val-11 | **regge** per A; per B **smentita** in T | 0 cicli su libero; transito dominante tardi: A 1/200 (D), 0/200 (T); B 1/200 (D), 89/200 (T); copertura a sosta improvvisa in D, A: 1,000 |
| P-val-12 | **regge** per A e per B in T e L; **smentita** per B in D | «prosegue»: A 0,282 / 0,303 / 0,000; B 0,997 / 0,714 / 0,000 |
| P-val-13 | **regge** | 1,000 sui nascosti dentro la griglia; area 1,32 dell'ombra da 2 s (T) |
| P-val-14 | **smentita** | C-005b e C-009 non superano mai 1,07 volte la migliore base, in nessuna cella |
| P-val-15 | **smentita** sui numeri (direzione giusta) | C-009: 77 % dei passaggi (4,3 % dei cicli); C-008: 18 cicli su 172 497 |
| P-val-16 | **regge** | area C-004 / C-001 = 0,44 e 0,48; C-004 / C-005 = 0,25 e 0,29 (T, 2 e 3 s) |
| P-val-17 | **regge** (in C) | tutti i predittori insieme, dieci tracce: 95º percentile 3,98 ms |
| P-val-18 | **regge** | 22/2737, 1/2800, 0/2800; a −20 cm senza fascia 2799/2800 |

Notato dopo, non previsto: (a) con il rumore 4/9/16 cm e il filtro fermo a 5 cm tutte le regioni tarate cadono (C-004 0,436,
C-005 0,295); con R dalla curva e la taratura rifatta tornano su (0,873, 0,920); (b) C-005 lascia vuoti nel 0,5–3,5 % dei
passaggi (il disco non tocca più l'ombra); (c) la regola di riaggancio del nucleo dà allo sconosciuto l'identità del primo
in 193 casi su 193 (T); (d) la lisciatura di C-004 è un parametro che decide (una passata: minimo 0,78–0,83).
