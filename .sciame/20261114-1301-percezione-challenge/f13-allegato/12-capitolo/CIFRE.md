# CIFRE del capitolo 2 (Sensore e geometria d'osservazione)

Origini, abbreviate:
- **G** = `f13-allegato/02-geometria/FASCICOLO_GEOMETRIA.md`, parte I (il paragrafo è indicato; i ricalcoli sono in `02-geometria/ricalcoli.txt`).
- **B** = `f13-allegato/06-bibliografia/FASCICOLO_BIBLIOGRAFIA.md` (parte II, §II.3, mappa «affermazione → chiave»).
- **D** = `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`, sezione «Da 02-geometria», II.2 (numero del punto).
- **SOL** = `f12-integrazione/20-finale/SOLUZIONE_V3.md`.

Colonna «rifatta»: «sì» se ho rifatto il conto in forma chiusa durante la stesura (stesse formule del fascicolo: vale contro errori di trascrizione, non contro un errore di formula o di lettura delle schede); «no» se è solo trascritta.

## Modello della camera (§2.1)

| Cifra | Origine | Rifatta | Nota |
|---|---|---|---|
| h = 1,2 m; θ = 15° | G §1, Def. 1; SOL §1.1 | no | posa di riferimento |
| 848 × 480; 30 fotogrammi al secondo | G §1, Tab. 1 | no | |
| D455: 87° × 58°; 95 mm; 0,6–6 m | G §1, Tab. 1; B II.3 (`realsense-d455`) | no | |
| D455: distanza minima 0,35 m | G §1, Tab. 1 | no | senza citazione (nessuna chiave la sostiene) |
| D435i: 87° × 58°; 0,3–3 m | G §1, Tab. 1; B II.3 (`realsense-confronto-camere`) | no | |
| D435i: base 50 mm; f = 424 px | G §1, Tab. 1; B II.3 (`realsense-taratura-profondita`: 90°, 848 px, 50 mm) | sì (424) | |
| D435i: distanza minima 0,195 m | G §1, Tab. 1 | no | senza citazione |
| Gemini 335: 90° × 60° a 848 × 480; 90° × 65° a 1280 × 800 | G §1, Tab. 1; D 10; B II.3 (`orbbec-gemini-335` per 90° × 65°) | no | **contestata** (D 10): riportate entrambe con la risoluzione di ciascuna |
| Gemini 335: base 50 mm | G §1, Tab. 1; B II.3 | no | |
| Gemini 335: f = 410,7 px; distanza minima 0,18 m | G §1, Tab. 1 | no | senza citazione |
| Gemini 335: intervallo ideale 0,3–3 m (scheda) e 0,26–3 m (pagina del prodotto) | G §1, Tab. 1 (0,3–3); B II.3, riga `orbbec-gemini-335` (0,26–3) | no | **due file non concordano e nessuno decide**: riportate entrambe con la fonte di ciascuna |
| σ_d nominale / limite: 0,08 / 0,20; 0,08 / 0,21; 0,082 / 0,154 px | G §1, Tab. 1 | no | |
| tolleranza sul campo ±3° | G §1, Tab. 1 | no | |
| 446,8 px (87° su 848 px); 433,0 px (58° su 480 px); 90° × 59,0° per f = 424 | G §1, Oss. 1 | sì | |
| scarto 5 % sulle grandezze laterali; 2 cm su z_min (1,22 contro 1,24 m) | G §1, Oss. 1; D 1–2 | sì | **contestata** (D 1–2): scelta del fascicolo dichiarata una volta (geometria con 87° × 58°, rumore con f = 424) |

## Visibilità del suolo (§2.2)

| Cifra | Origine | Rifatta | Nota |
|---|---|---|---|
| β₋ = 44°; β₊ = 14° | G §2 | sì | |
| z_min = 1,243 m; 0,917 z + 0,295 m | G §2, Cor. 1 | sì | |
| 1,24 m sull'asse; 1,43 m a 30°; 1,71 m a 43,5° | G §2, Cor. 1; D 2 | sì | **contestata** (D 2): «1,69 m a ±44°» veniva da 1,22/cos 44° troncato; vale 1,71 m a 43,5° con 58° |
| x = ±1,43 m; φ = ±49,1°; ρ = 1,90 m | G §2, Cor. 1 | sì | |
| z_min = 1,221 m e 1,70 m a 44° con f = 424 px (59,0°) | G §2, Cor. 1; D 2; SOL §1.1 («1,22 m»; «1,69 m», troncato) | no (1,697 in `ricalcoli.txt` r. 18) | scritto 1,70 (arrotondato), come nel fascicolo |
| ostacolo di 0,15 m: 1,087 m; di 0,10 m: 1,139 m | G §2, Cor. 2 | sì | |
| y_max = 1,2 + 0,249 z | G §2, Cor. 3 | sì | |
| y_max: 1,51 / 1,62 / 1,67 / 1,70 / 1,77 / 1,95 m a z = 1,24 / 1,7 / 1,9 / 2,0 / 2,3 / 3,0 m | G §2, Tab. 2 | sì | |
| quota 1,60 / 1,70 / 1,80 / 1,90 / 2,00 m vista da 1,60 / 2,01 / 2,41 / 2,81 / 3,21 m | G §2, Tab. 2 | sì | |
| testa a 1,70 m non vista sotto 2,01 m; ostacolo sospeso a 1,80 m sotto 2,41 m | G §2; D 3; SOL «Limiti» | sì | **contestata** (D 3): 2,41 m è la distanza per 1,80 m; per 1,70 m vale 2,01 m |
| per profilo, 58°: 1,243 m; 1,087 m; 0,249; 2,41 m | G §2, seconda tabella | sì | |
| per profilo, 60°: 1,200 m; 1,050 m; 0,268; 2,24 m | G §2, seconda tabella | sì | |
| per profilo, 65°: 1,100 m; 0,962 m; 0,315; 1,90 m | G §2, seconda tabella | sì | |
| z_min da 1,18 a 1,31 m (58° ± 3°); da 1,20 a 1,29 m (15° ± 1°) | G §2, «Sensibilità» | sì | |
| lancio di raggi: 1,245 m ai centri dei pixel | G §2, «Livello» | no | |
| disco di 3 m: 28,27 m² | G §2, Prop. 2 | sì | |
| settore d'anello: 5,66 m², 20,0 % | G §2, Prop. 2 (i); D 4 | sì | **contestata** (D 4): riportate entrambe, ciascuna con la sua regione |
| regione esatta: 5,79 m², 20,5 %; griglia di 2 mm | G §2, Prop. 2 (ii); D 4 | no (integrazione numerica) | il fascicolo la segnala come riderivazione propria (parte II, II.0) |

## Ombra (§2.3)

| Cifra | Origine | Rifatta | Nota |
|---|---|---|---|
| a = 0,3 m a 1,7 m → 2,27 m; 0,5 m a 1,5 m → 2,57 m; 1,0 m a 1,5 m → 9,0 m | G §3, dopo Prop. 3 | sì | |
| Tab. a_min, s = 1,60 m: 1,40 / 1,46 / 1,50 / 1,51 / 1,53 / 1,55 | G §3, Tab. 3 | sì | |
| Tab. a_min, s = 1,70 m: 1,45 / 1,53 / 1,57 / 1,59 / 1,61 / 1,63 | G §3, Tab. 3 | sì | |
| Tab. a_min, s = 1,75 m: 1,48 / 1,56 / 1,61 / 1,63 / 1,65 / 1,68 | G §3, Tab. 3 | sì | |
| Tab. a_min, s ≥ 1,77 m: 1,49 / 1,57 / 1,62 / 1,65 / 1,67 / 1,70 | G §3, Tab. 3 | sì | |
| z_p = 2,3 m; z_o = 1,15 … 2,0 m | G §3, Tab. 3 | — | |
| pannello di 1,5 m a 1,7–1,9 m: in vista sopra 1,61 m (a 1,7 m) o 1,56 m (a 1,9 m), fino a 1,77 m | G §3, dopo Tab. 3; `ricalcoli.txt` r. 66 | no | |
| servono fra 1,61 m (statura 1,75 m) e 1,67 m (ogni statura) | G §3, dopo Tab. 3 | sì (dalla tabella) | |
| pannello di 1,7 m: margine nullo a 2,0 m; 3–8 cm a 1,9–1,7 m | G §3, dopo Tab. 3 | sì (dalla tabella) | |
| pannello di 1,8 m: 10–18 cm di margine | G §3, dopo Tab. 3 | sì (dalla tabella) | |
| tolleranza del campo: tetto ±5 cm a 1,9 m | G §3, «Limite» | no | |
| Tab. T_tot, 1 m; 1,7 m: 1,35; 0,90; 0,64 / 0,90 / 1,81 | G §3, Tab. 4 | sì | |
| Tab. T_tot, 1 m; 1,9 m: 1,21; 0,76; 0,54 / 0,76 / 1,52 | G §3, Tab. 4 | sì | |
| Tab. T_tot, 2 m; 1,7 m: 2,71; 2,26; 1,61 / 2,26 / 4,51 | G §3, Tab. 4 | sì | |
| Tab. T_tot, 2 m; 1,9 m: 2,42; 1,97; 1,41 / 1,97 / 3,94 | G §3, Tab. 4 | sì | |
| w = 0,45 m; velocità 1,4 / 1,0 / 0,5 m/s | G §3, Tab. 4 | — | |
| passo normale 1,0–1,4 m/s: 0,54–0,90 s (1 m); 1,4–2,3 s (2 m) | G §3, dopo Tab. 4 | sì | |
| Tab. banda, 1 m; 3 m: 19,0 cm = 27 px; 10,0 = 14; 10,0 = 14 | G §3, Tab. 5 | sì | |
| Tab. banda, 1,5 m; 3 m: 9,5 = 13; 5,0 = 7; 5,0 = 7 | G §3, Tab. 5 | sì | |
| Tab. banda, 2 m; 3 m: 4,8 = 7; 2,5 = 4; 2,5 = 3 | G §3, Tab. 5 | sì | |
| striscia al bordo sinistro: 20 px a 2 m (95 mm); 11 px (50 mm) | G §3, dopo Tab. 5 | sì | |
| 0,16 s a 1,2 m/s con 19 cm | G §3, dopo Tab. 5 | sì | |
| verifica numerica 0,1900 m | G §3, «Livello» | no | |
| rumore laterale 4,3 cm al 90° percentile, bordo sinistro | G §4 «Risoluzione e rumore laterali»; B II.3 (`ahn2019`) | no | il valore del bordo destro (4,1 cm) è lasciato fuori: non è nella mappa |

## Rumore di profondità (§2.4)

| Cifra | Origine | Rifatta | Nota |
|---|---|---|---|
| σ_d = 0,08 px (curva teorica); < 0,1 px (camera ben tarata) | G §4; B II.3 (`realsense-taratura-profondita`, `realsense-bkm-taratura`) | no | il fascicolo 02 attribuisce entrambe a `realsense-bkm-taratura`; la mappa del fascicolo 06 assegna 0,08 a `realsense-taratura-profondita`: seguita la mappa |
| D455: ≤ 2 % a 4 m; k = 0,005 m⁻¹ | G §4; B II.3 (`realsense-d455`) | sì | |
| D435i: ≤ 2 % a 2 m; k = 0,010 m⁻¹ | G §4; B II.3 (`realsense-d400-accuratezza`) | sì | |
| Gemini 335: ≤ 1,5 % a 2 m; k = 0,0075 m⁻¹; nominale k = 0,004 m⁻¹ | G §4; B II.3 (`orbbec-gemini-335`) | sì (0,0075) | il nominale è letto da un grafico di scheda (non citato) |
| f·b: 40,28; 21,20; 20,54 px·m | G §4, Tab. 6 | sì | |
| D455 nominale: 0,20 / 0,79 / 1,79 / 3,18 cm; 5 cm a 5,0 m | G §4, Tab. 6 | sì | |
| D455 limite: 0,50 / 2,00 / 4,50 / 8,00 cm; 3,2 m | G §4, Tab. 6 | sì | |
| D435i nominale: 0,38 / 1,51 / 3,40 / 6,04 cm; 3,6 m | G §4, Tab. 6 | sì | |
| D435i limite: 1,00 / 4,00 / 9,00 / 16,0 cm; 2,2 m | G §4, Tab. 6 | sì | |
| Gemini 335 nominale: 0,40 / 1,60 / 3,60 / 6,40 cm; 3,5 m | G §4, Tab. 6 | sì (con k = 0,004) | |
| Gemini 335 limite: 0,75 / 3,00 / 6,75 / 12,0 cm; 2,6 m | G §4, Tab. 6 | sì | |
| quantizzazione a 1/32 px, D455: 0,8 / 3,1 / 7,0 / 12,4 mm | G §4, Tab. 6 | sì | 1/32 px è un'ipotesi (detto nel testo) |
| quantizzazione, D435i: 1,5 / 5,9 / 13,3 / 23,6 mm | G §4, Tab. 6 | sì | |
| scarto tipo di quantizzazione: 2,0 mm (D455) e 3,8 mm (D435i) a 3 m | G §4, «Quantizzazione» | sì | |
| σ_z = 0,00106 + 0,00073 d + 0,00395 d²; 0,4–2,1 m | G §4, «Confronto»; B II.3 (`ahn2019`) | — | coefficienti arrotondati come nel fascicolo 02 |
| 1,83 cm a 2 m; 1,21 volte il nominale; 0,097 px; 3,9 cm a 3 m | G §4, «Confronto» | sì | |
| incidenza: 46° a 1,24 m; 60° a 2,08 m; 68° a 3 m | G §4, «Limiti di validità» | sì | |
| pixel: 4,5 mm a 2 m; 6,7 mm a 3 m (f = 446,8) | G §4, «Risoluzione» | sì | |
| 5 pixel: 3,4 cm a 3 m; 6,7 cm a 6 m; 1 cm entro 0,89 m; 3,5 cm con f = 424 (+5 %) | G §4, «Risoluzione» | sì | |
| sfocatura: 12 mm (1,5 m/s, 8 ms); 45 mm (30 ms) | G §4, «Risoluzione» | sì | |

## Errore di posa (§2.5)

| Cifra | Origine | Rifatta | Nota |
|---|---|---|---|
| 1°: 3,5 cm a 2 m; 4,9 cm a 2,8 m; 5,2 cm a 3 m | G §5, dopo Prop. 8 | sì | |
| y_s = 0,07 m | G §5; SOL §1.1 («sopra 0,07 m») | — | parametro (appendice A) |
| 2°: suolo «occupato» da 1,99 m | G §5 | sì (1,985 con la formula esatta) | |
| a = 0,10 m: 0,86° a 2 m; 0,67° a 2,55 m; 0,57° a 3 m | G §5; SOL §1.1 (0,69° a 2,5 m, 0,57° a 3 m: coerente) | sì | |
| a = 0,15 m: 2,3° a 2 m | G §5 | sì | |
| 10 cm a 2,55 m: 7 celle su 7 «occupato» a 0°, 7 su 7 «libero» a +1° | G §5, «Riscontro in simulazione»; SOL §1.1 | no | |
| 12 cm: fra 1,0° e 1,5° (previsione 1,12°); 15 cm: fra 1,5° e 2,0° (previsione 1,78°) | G §5, «Riscontro» | no | |
| scatola di 15 cm a 2,0–2,15 m: 0, 1, 2, 9, 10 su 10 a 0°, 1°, 2°, 2,5°, 3° | G §5, «Riscontro» | no | |
| Wilson 95 %: 0,60–0,98 (9 su 10); 0,72–1 (10 su 10) | G §5, «Riscontro» | sì | |
| soglia prevista 2,1–2,3° | G §5, «Riscontro» | no | |

## Sensori a tempo di volo e LiDAR (§2.6)

| Cifra | Origine | Rifatta | Nota |
|---|---|---|---|
| VL53L7CX: 60° × 60°; 8 × 8; 2,0 m al buio e 0,5 m a 5 klx a 15 Hz | G §6; B II.3 (`st-vl53l7cx`) | no | |
| VL53L8CX: 45° × 45°; 1,55 m a 5 klx; 4,0 m al buio | G §6, tabella; B II.3 (`st-vl53l8cx`: «400 cm», 1,55 m) | no | |
| zona: 7,5° e 5,625° | G §6 | sì | |
| lato a 2 m: 26 cm e 20 cm; diagonale 37 e 28 cm | G §6, tabella; D 7 | sì | **contestata** (D 7): 13 e 10 cm erano mezza zona; vale 26 e 20 cm |
| campo a 2 m: 2,31 m e 1,66 m | G §6, tabella | sì | |
| tre sensori: 180° × 60° e 135° × 45°; per 360°: 6 e 8 | G §6, tabella | sì | scritto come conto, non come dichiarazione del costruttore |
| persona di 0,5 m a 4 m: 0,95 e 1,27 zone | G §6, tabella | sì | |
| celle 1° × 0,1 m = 3,5 cm × 10 cm a 2 m | G §6 (a) | sì | |
| distanza obliqua: almeno 1,20 m; 2,33 m a ρ = 2 m | G §6 (b) | sì | |
| primo campione dopo «nessun bersaglio»: fiducia sotto il 50 % | B II.3, riga `st-um3038` | no | il fascicolo 02 scrive «solo lo stato 5 è valido al 100 %»: la mappa non lo riporta, usata la frase della mappa |
| 6,28 m²; 22,2 % del disco; 1,4 % con 0,5 m | G §6 | sì | |
| LiDAR: 0,72°; 0,8° (da 4500 misure al secondo a 10 giri) ; 10 giri al secondo | G §6; B II.3 (`slamtec-rplidar-c1`, `ldrobot-ld19`) | sì (360°/450 = 0,8°) | |
| passo a 3 m: 3,8–4,2 cm; 12–13 punti su 0,5 m; meno di 2 su 12 cm a 5 m | G §6 | sì | |
| 30°/s: 3° dentro un giro | G §6 | sì | |

## Figure

Le figure riportano solo cifre già elencate sopra (1,09; 1,24; 2,01; 2,57; 3 m; 1,62; 1,70; 1,77; 1,95 m; 44°; 14°; z_o = 1,8 m, z_p = 2,3 m, a = 1,7 m e pannello di 1,5 m: G §9, figura A, e SOL «Geometria della demo» per 1,8 m e 2,3 m; 2 m, 0,5 m, 2,31 m, 26 cm: G §9, figura C). Le coordinate di disegno che non compaiono come testo (per esempio l'intersezione dei bordi laterali con il cerchio di 3 m) sono calcolate dalle formule del Corollario sul suolo e non sono cifre del documento.
