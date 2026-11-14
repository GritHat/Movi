# CIFRE del capitolo 4 (sti) — origine di ogni cifra

Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Sigle dei file:
**FS** = `f13-allegato/03-stima/FASCICOLO_STIMA.md` (parte I, salvo «II»); **FD** = `f13-allegato/01-dimostrazioni/FASCICOLO_DIMOSTRAZIONI.md`;
**FB** = `f13-allegato/06-bibliografia/FASCICOLO_BIBLIOGRAFIA.md`; **ID** = `f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md`;
**CI** = `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md`; **SV3** = `f12-integrazione/20-finale/SOLUZIONE_V3.md`;
**PI** = `f12-integrazione/02-prova-insieme/PROVA_INSIEME.md`; **VD** = `f10-dati/23-verdetto/VERDETTO_DATI.md`;
**BC** = `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`; **UC** = `f14-classificazione/02-uso/USO_DELLA_CLASSE.md`;
**CL** = `f14-classificazione/03-classificatore/CLASSIFICATORE.md`; **PR** = `f14-classificazione/01-profili/PROFILI.md`.

Nessuna cifra è stata ricalcolata da me: sono trascritte. Ho controllato la trascrizione rileggendo il PDF (`pdftotext`) contro i file.

## Cifre contestate: valore scelto e perché

| Cifra | Scelta | Perché |
|---|---|---|
| Soglia della regola «mobile» | $k_s\,\sigma\,\sqrt{2/m}$, $m=3$, $k_s=5$ | FS II.2 D1 e SV3 1.3: è la soglia del codice che ha dato 100 / 85,9 / 26,6 %; la forma «5·σ·√2» sul singolo fotogramma darebbe 0 % da 3 m |
| Limiti inferiori «99,85 %» e «99,25 %» | 99,81 % (2000 su 2000) e 99,05 % (400 su 400) | FS II.2 D2: i file davano limiti unilaterali esatti; l'allegato usa Wilson al 95 % |
| Etichette false con rumore creduto la metà | 10,9 % delle tracce nel primo secondo | FS II.1: il «31 %» dei file è della regola precedente, non confrontabile |
| $\sigma_p$ = 3 cm nel conto dell'accelerazione | 3 cm, dichiarato «valore assunto» | FS II.2 D4 |
| «0,00–0,06 a 2 s» | copertura della regione *emessa* su chi *prosegue* | FS II.2 D5: è il senso dei file; la consegna diceva «chi si ferma» |
| Copertura su traiettorie pubbliche, due elaborazioni | riportate entrambe (0,977/1,000/1,000 e 0,982/0,995/1,000, ecc.) | FS II.2 D6: nessun file decide |
| Chiave per 0,08 px e crescita quadratica | `realsense-taratura-profondita` | FS cita `realsense-bkm-taratura`; la mappa FB II.3 attribuisce 0,08 px e «scales as the square» a `realsense-taratura-profondita`: vale la mappa |
| Fascia del riaggancio | 0,40 m e 0,75 m, entrambe con la condizione | FS §8 e ID §5 dicono 0,40 m; SV3 1.8 dice 0,75 m dall'ombra d'ingresso (prove d'insieme): nessun file decide |
| Identità al ritorno su profondità simulata | tasso 176/180 e 174/180 | CI §0 e SV3 1.8: il criterio «≥ 28 su 30 per caso» non regge alla replica; resta il tasso |
| Pannello «mobile» con i gruppi di base | 79 su 90 (semi d'origine) e 130·94 su 140 (semi nuovi) | due prove diverse, entrambe riportate con la loro condizione |
| Ritardo di conferma $t$ = 0,27 s | 0,27 s (4 fotogrammi a 15 Hz) | FS §5, CL §5 RC-3, BC §3 (0,267) concordi |

## Introduzione e ordine della catena
- Proposizione dell'ordine, porta: FD §6.

## Dai punti ai gruppi
- 1° × 0,1 m; ρ ≤ 3 m; n_min = 3; quota 0,07–2 m; 8 vicini: FS §1 Def. 1–2.
- σ_d = 0,08 px; f = 424 px; b = 0,05 m (assunti); σ_z 1,51 / 3,40 / 6,04 cm a 2 / 3 / 4 m: FS §1.
- σ_t = d(π/180)/√12 = 1,01 / 1,51 / 2,02 cm: FS §1.
- Curva pessimista 4(d/2)² (4 / 9 / 16 cm); severa 5(d/2)² (5 / 11,25 / 20 cm): FS §1.
- σ/√n ≤ σ_c ≤ σ: FS §1 Lemma 1.
- Rumore radiale mediano simulato 0,36 / 0,99 / 1,25 cm (20 semi); sequenza pubblica reale 5,8–6,8 cm sotto 3 m, 288 fotogrammi: FS §1.

## Regola «mobile»
- m = 3; finestra ≤ 1 s; k_s = 5: FS §2 Def. 3.
- σ_δ = 0,8165 σ; soglia 4,08 σ; P_fa = 5,7·10⁻⁷; 13 prove per asse; ≤ 1,5·10⁻⁵; 6,2 e 4,1 cm a 2 m: FS §2 dopo Prop. 1.
- 1,2816; finestra 13Δ = 0,867 s; v_0,5 / v_0,9: 0,071 / 0,089 (2 m) e 0,160 / 0,201 (3 m) nominale; 0,424 / 0,533 pessimista a 3 m; 0,530 / 0,666 severa a 3 m: FS §2 dopo Prop. 2.
- Tabella: 100 % (≥ 99,81 %; ≥ 99,98 %); 85,9 % (84,3–87,3) e 86,2 % (85,7–86,7), 0,853; 26,6 % (24,7–28,6) e 26,9 % (26,3–27,5), 0,371; 0 su 4000 (≤ 0,10 %); 1 su 120 000; N = 2000 e 20 000: FS §2 Tabella 1.
- Soglia 2,5 σ_δ; 10,9 %; N = 20 000, curva pessimista, 2 m: FS §2 «Condizioni di validità».
- 79 su 90 (79,4–93,0 %); 90 su 90; 10 su 10 → 1 su 10; soglia 4–6 cm: FS §2 controesempio; VD riga H-405 e F-401.
- n_min = 40: 5 su 90 (2,4–12,4 %); scatola 3 su 10 contro 10 su 10: FS §2; VD riga H-405.
- 848×480 con soglia 40: 0 su 10; con 160: 10 su 10: VD F-412.
- Celle ponte 33–125 punti; scatola 13–43: ID §2 critica 1.
- 98 e 91 celle·fotogramma «libero» in ombra; 0 e 4 con mappa invariata: ID §2 critica 2 e §3 tabella.
- Celle forti: h_rif = 0,05 m; η = 0,30; A_rif = 0,004 m²; 20 punti a 2 m a 424 px, 79 a 848: ID §5 «Soglie»; SV3 1.3.
- Pannello «mobile» 0 su 140 (prima 130 e 94); tracce sul pavimento vuoto 0 (9 sequenze; prima 137 e 206); scatola 190 su 190: ID §3 tabella.
- Cubo di 10 cm: 0 su 60 (occupato 60 su 60); scatola a 2,8 m: 45 su 60 (63–84 %); taglia minima 15 cm entro 2 m: CI §3 e §5 correzione 1; SV3 1.3.
- 105–106 tracce confermate su 3 pavimenti vuoti (rumore degradato): ID §2 critica 7.

## Classificazione
- Interfaccia (campi, 1–2 Hz, 15 Hz): BC §1; CL §2.
- Sei categorie; soglia 0,7: BC §1; CL §1.
- Tabella dei profili (tutte le righe e le marche d'origine: F→a; R, M→b; I→senza marca): BC §2. «9 velocità su 30»: BC §2, PR §0.
- 200 m e 37,6 m contro 3 m: BC §1 «Stato dichiarato».
- Coerenza: dal 4° ciclo; 4 su 6; 2σ; 0,30 m; 1,5; 1 s: BC §1, UC §3.
- 4000 tracce per caso; 0 / 1 / 0 su 4000; 6 m/s e 3,5 m/s: 1,000 dopo 0,47 s; 2,8 m; 2,8 m/s: 0,106; carrello lento 0,041; pedone «carrello» 0,052: UC §3 tabella. Veicolo fermo «persona» 0 su 2000: BC §1.
- Requisiti: 0,05; 0,5 s; 0,75 s a 4 m/s; 0,21 s a 14 m/s; 0,27 s; 10 %; 1 %; 5 %; 2 s: CL §5.
- Massa con fonte per tre classi: BC §8; PR §4.

## Filtro
- F, Q, H, forma di Joseph, Prop. su Q e crescita: FS §3.
- r_0,50 = 1,177 σ_p; r_0,90 = 2,146 σ_p; r_0,95 = 2,448 σ_p: FS §3.
- Tabella σ_p: 0,156 / 0,344 / 0,848 / 1,485; r_0,95 0,38 / 0,84 / 2,08 / 3,64; 0,121 / 0,257 / 0,618 / 1,072; 0,096 / 0,194 / 0,453 / 0,777; 15 Hz, 5 cm; 3,3 cm e 0,205 m/s: FS §3 Tabella 2.
- 1 m dopo 1,15 s; 2 m dopo 1,95 s: FS §3.

## Massa e accelerazione
- Proposizione, Fisher di rango 1; u = 120 N, M = 75 kg, 30 misure a 15 Hz, determinante 0: FD §5.
- σ_a = √6 σ_p/Δ²; 66,1 / 16,5 / 7,3 m/s² a 30 / 15 / 10 Hz; 0,67 m/s²; 2,8 m: FS §4 Lemma 2.
- Rango 3; σ_a = 0,71 m/s² su 0,5 s a 30 Hz: FS §4 Oss. 1.
- 1500 prove; 0,82 contro 0,67 m/s²; 2,29 contro 1,18 m a 2 s: FS §4.

## Associazione e conferma
- γ = 9,210 al 99 %: FS §5; FD §6.
- 3 su 5; formule; 27,1 / 5,2 / 0,9 %; 0,27 s; +2 cicli 0,133 s con 0,81; media 0,147 s: FS §5 Prop. 6.
- 7–66 tracce false per passaggio: FS §5; VD «nove condizioni», punto 6.

## Valore di q
- q = 0,2; NIS 1,95; 0,936 / 0,917 / 0,903 / 0,920 a 0,5 / 1 / 2 / 3 s; 1500 prove; q = 0,01 → 0,42: FS §6.
- 15 Hz; 2 cm; 1 s + 3 s; 227 e 219 tratti, 9 persone: FS §6.
- Tabella: tutta da FS §6 Tabella 3.
- Seconda elaborazione 0,982 / 0,995 / 1,000; 0,922 / 0,950 / 0,941; 0,836 / 0,822 / 0,840: FS §6. Errore mediano 0,22 / 0,44 / 0,73 m: FS II.2 D6.
- 0,43–1,00 per persona; 1,27: FS §6.
- 197,1 ± 4,4; 188–205; 214 (8·10⁻⁶); 174 (2,5·10⁻⁶); 207 (0,012); fra 0,05 e 0,1; q_eff 0,058 / 0,050 / 0,044; raggio 3,5 m a 3 s: FS §6 Prop. 8 e «Lettura».

## Cerchio di covarianza e consistenza
- 0,88–0,96 fino a 5 s (N = 6000); 0,63–0,85; per comportamento 1,00; 0,86–1,00; 0,72–0,90; 0,29–0,77 a 2 s; rapporto 1,8–4,5; 1,82; 0,00–0,06 (tre disposizioni, 400 passaggi): FS §7.
- NIS 1,93–1,97; NEES 3,29–3,41; autocorrelazione −0,02; 5 cm, q = 0,2, 10–30 Hz: FS §9 tabella.

## Riaggancio
- Regola (a)–(f): FS §8 (a, b, f); ID §5 «Riaggancio» righe 3–7 e SV3 1.8 (c, d, e).
- Fascia 0,40 m: FS §8, ID §5; 0,75 m: SV3 1.8.
- Ripartenza: R + (larghezza/2)²; σ_v = 2,5 m/s: ID §5 riga 8. Scarto 5,00 → 0,17 m, N = 1, sosta di 5 s: ID §3 «F-408»; SV3 1.4.
- ±20 cm; 400 su 400 in 27 configurazioni (99,05 %); 0 su 2400 (≤ 0,16 %): FS §8.
- 10 711/10 757; 9228/9240; 6772/6967; 0,994 / 0,998 / 0,968; 0,72–0,80: PI riga «f» della tabella; SV3 1.8.
- 0 su 90 (4,1 %): FS §8 limite 2; VD. 41 su 45 (79,3–96,5 %); 0 su 6: FS §8 limite 3; VD riga H-404.
- 176 su 180 (94–99 %) a 424 px; 174 su 180 (93–98 %) a 848 px: CI §0 e §5; SV3 1.8. Comportamenti (1,2 m/s; 0,5 m/s; sosta di 3 s): ID §3 tabella per caso.
- Riagganci a persona nascosta 11 e 6 → 1 e 1 su 140: ID §3 tabella.
- Dominio (≥ 1,2 m; 0,5–1,6 m/s; 1,5–1,8 m; 0,5 m; 2,6 m; tre profili; 424–848 px; < 0,5°): CI §5.
- Fuori dal dominio: 2,8 m 0 su 10; bambino 2 su 10 (6–51 %); +0,5° 6 su 10 (31–83 %); rumore degradato 0 su 10; bordo del campo 10 su 10 identità nuova: CI §3. Persona a 0,3 m dal pannello 0 e 1 su 10: ID §0 e §3 (riga «linea a 2,1 m»).
- Secondo soggetto: 2400 su 2400 (99,84 %); 193 su 193: FS §8 limite 1. 19 su 20 (76–99 %): CI §0 e §4.
- −20 cm: FS §8 limite 4.
