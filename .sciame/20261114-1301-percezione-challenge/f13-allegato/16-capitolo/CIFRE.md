# CIFRE del capitolo 6 (Metodo di valutazione e risultati) — una riga per cifra, con il file e il paragrafo d'origine

Radice dei percorsi: `.sciame/20261114-1301-percezione-challenge/`. Sigle dei file d'origine:

- **FV** = `f13-allegato/04-statistica/FASCICOLO_VALUTAZIONE.md` (parte I salvo dove è scritto «II»)
- **PI** = `f12-integrazione/02-prova-insieme/PROVA_INSIEME.md`
- **CP** = `f12-integrazione/13-statistica/CONTROLLO_PROVE.md`
- **LC** = `f12-integrazione/03-libero/LIBERO_DELLA_CELLA.md`
- **ID** = `f12-integrazione/06-identita/IDENTITA_SU_PROFONDITA.md`
- **CI** = `f12-integrazione/07-controprova-identita/CONTROPROVA_IDENTITA.md`
- **SV3** = `f12-integrazione/20-finale/SOLUZIONE_V3.md`
- **BC** = `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md`
- **AC** = `f14-classificazione/10-attacco/ATTACCO_CLASSIFICAZIONE.md`
- **DISC** = `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`
- **RIC** = `f13-allegato/16-capitolo/ricalcoli.txt` (mio ricalcolo degli intervalli; non è una fonte, è un controllo)

Colonna «ricalcolo»: **sì** = l'intervallo o la probabilità è stato rifatto in `ricalcoli.py` e coincide; **letto** = copiato dal file d'origine senza rifarlo. Non ho rieseguito nessun simulatore: i conteggi sono tutti «letti».

## Scelte dichiarate (cifre contestate)

| Punto | Valore scelto | Perché |
|---|---|---|
| Denominatore della copertura | «tutti i passaggi ancora nascosti» (826/879; 461/513) | FV §1 Def. 2 e II.2 n. 1: scelta prudente, coerente con la tabella per comportamento; l'altro denominatore è nominato nel testo con l'esempio 461 su 480 |
| Intervallo per «0 su N» | Wilson a due code, z²/(N+z²) | FV §2 e II.1; DISC «D1», «D2»: i file mescolano tre convenzioni. Il limite a una coda compare solo due volte, dichiarato (99,25 % e 1,5 su 10 000) |
| «0 vuoti»: limite superiore | 0–0,064 % su 6000 soggetti distinti | CP §0 (1) e §7 n. 1; SV3 riga 162: «meno di 6,4 su 10 000», non «1,7 su 10 000» di PI |
| G₁ a 1 s | limite 0,87 (0,875 su 5 celle), non «0,88» | CP §0 (2) e §2 |
| Zero della regola del «libero» | «verificato sull'insieme dichiarato», per condizione 0–1,3 %; non «2 su 10 000» | CP §0 (3) e §3 |
| «Regione 83 su 90» e «36 su 46» | 36 su 46 = parametri di partenza; 83 su 90 = variante a soglia 40 | FV II.0 e II.2 n. 3; DISC |
| Numerosità | n stabile in grassetto, primo n accanto | FV §3 e II.0 («notato dopo») |
| «2,67» | media su 20 celle; 6,0 è la cella «prosegue a 3 s» | FV §5 e II.2 n. 4 |
| Errore del punto fermo | intervalli fra i lanci 0,97–1,00 / 1,48–1,54 / 1,59–1,66 | FV §6.3 e II.2 n. 5 |
| Aree relative | pesate sui cinque comportamenti (0,24; 0,31; 0,16; 0,27; 0,99; 1,21; 0,79; 1,12) | FV §4 e II.2 n. 6 |
| Traiettorie pubbliche, due programmi | entrambe: 0,977 / 1,000 / 1,000 e 0,982 / 0,995 / 1,000; errore 0,21 / 0,49 / 0,81 e 0,22 / 0,44 / 0,73 | FV II.2 n. 8; DISC «D6» (nessuno decide: riportate tutte e due) |
| Secondo soggetto, regola di base | entrambe: 2400 su 2400 (prova di base) e 0,481 / 0,711 / 0,676 (prove d'insieme, riaggancio a 0,40 m) | FV §6.1; PI §2 (d): prove diverse, nessun file decide |
| Scoperti con P_D = 0,7 | 17 su 5704, 1,9–4,8 per mille («fino a 5 su 1000»), non «circa 2 su 1000» | CP §2 |

## Apertura e §6.1 (misure)

| Cifra | Origine | Ricalcolo |
|---|---|---|
| almeno 4 misure per il passaggio valido | FV §1 | letto |
| ombre 1,36; 7,82; 14,70 m²; pannello 1 m (G₁) e 2 m (G₃) | FV «Simboli» | letto |
| pannello 2 m anche in G₂ | CP riga 3 («T e L: 2 m»); corrispondenza G₁=D, G₂=T, G₃=L dedotta da FV II.1 (file `prova_D`, `prova_T`, `semi_spostato_L`) | letto |
| portata 3 m | FV §1 Def. 2 | letto |
| 461 su 513 contro 461 su 480 | FV §1 Def. 2 | letto |
| livello 0,90; τ ∈ {0,5; 1; 2; 3} s; cinque comportamenti sul percorso, due fuori | FV §1 | letto |

## §6.2 (intervalli)

| Cifra | Origine | Ricalcolo |
|---|---|---|
| z = 1,960 (95 % a due code) | FV «Simboli» | — |
| esempio 826/879: 0,93970; 0,002185; 1,004370; 0,93779; 0,008106; 0,01582; [0,9220; 0,9536] | FV §2 | sì (RIC) |
| 0,05^(1/N); 2,9957/N; 3/N; 3,84/(N+3,84) | FV §2 Prop. 1 | — |
| N = 90: 3,27 % e 4,09 %; N = 131: 2,26 % e 2,85 %; N = 400: 0,746 % e 0,951 %; N = 24 835: 0,0121 % e 0,0155 % | FV §2 «Valori» | sì (RIC) |
| 400 su 400: 99,05 % (Wilson), 99,25 % (esatto a una coda) | FV §2; DISC «D1», «D2» | sì (RIC) |
| livello 1 − 0,05/m; 0,05 | FV §2 Prop. 2 | — |
| z₁₂ = 2,865; z₄₅ = 3,261; z₆₀ = 3,342 | FV §2 «Valori» | letto |
| 90 su 100: [0,826; 0,945] e [0,782; 0,958] con m = 12 | FV §2 «Valori» | sì il primo (RIC); letto il secondo |

## §6.3 (numerosità e lettura «dentro k su n»)

| Cifra | Origine | Ricalcolo |
|---|---|---|
| livello 0,05, potenza 0,80 | FV §3 tabella | — |
| 0,90 contro 0,80: 78 (k ≤ 65), stabile 89 | FV §3 | letto |
| 0,80 contro 0,90: 82 (k ≥ 72), stabile 94 | FV §3 | letto |
| 0,90 contro 0,85: 270 (k ≤ 234), stabile 299 | FV §3 | letto |
| 0,85 contro 0,90: 281 (k ≥ 249), stabile 304 | FV §3 | letto |
| 0,90 contro 0,95: 179 (k ≥ 168), stabile 203 | FV §3 | letto |
| 9 su 10: 0,596–0,982 e 0,555–0,997 | FV §3 | sì il Wilson (RIC) |
| 27 su 30: 0,744–0,965 e 0,735–0,979 | FV §3 | sì il Wilson |
| 30 su 30: 0,887–1 e 0,884–1 | FV §3 | sì il Wilson |
| 46 su 50: 0,812–0,969 e 0,808–0,978 | FV §3 | sì il Wilson |
| 90 su 100: 0,826–0,945 e 0,824–0,951 | FV §3 | sì il Wilson |
| «circa 90», «circa 300», «circa 200» passaggi | FV §3 | — |
| «fra 0,74 e 0,97» | FV §3 | sì |
| n = 30: rifiuto per k ≤ 23, potenza 0,39 | FV §3 | sì (RIC: 0,393) |
| 30 su 30: «almeno 0,89»; 4,2 % con copertura vera 0,90 | FV §3 | sì |
| 37,6 % e 73,6 % («almeno 9 su 10» con 0,80 e con 0,90) | FV §3 | sì |
| almeno 82 su 94, potenza 0,86 | CP §5 | sì (RIC: 0,856) |
| almeno 262 su 296, potenza 0,83 | CP §5 | sì |
| almeno 96 su 100; potenza 0,44 (vero 0,95) e 0,82 (vero 0,97) | CP §5 | sì |
| τ_occ = 1 s e 2 s; e_Ω = −0,2 m; 1216 su 1244 = 0,977; cella peggiore 0,68 | FV §3 regola (2) | letto (FV II.1: «non ricontato») |
| sotto n = 10 solo i conteggi | FV §3 regola (1) | — |
| m = 10, ρ = 0,2: 40 passaggi ne valgono 14 | FV §3 regola (5) | sì (14,3) |

## §6.4 (taratura per quantili)

| Cifra | Origine | Ricalcolo |
|---|---|---|
| k = ⌈(1−α)(n_c+1)⌉; limite 1−α+1/(n_c+1) | FV §4 Prop. 3 | — |
| Beta(k, n_c+1−k) | FV §4 Prop. 4 | — |
| n_c = 30 (k = 28): 5º percentile 0,805; n_c = 100 (k = 91): 0,848 | FV §4 «Valori» | letto |
| primo n_c 68, stabile 110, per superare 0,85 con probabilità 0,95; sotto n_c = 9 tutto lo spazio | FV §4 «Valori» | letto |
| 0,897–0,907 nel complesso; 0,455 a 2 s e 0,307 a 3 s per chi torna | FV §4 Oss. 2 | letto |
| miscela 90/10/0/0 provata su 50/20/20/10: 0,72 / 0,66 / 0,64 | FV §4 Oss. 2 | letto |
| variabilità 15 % anziché 6 %, rotta 8° anziché 3° | FV §4 Oss. 2 | letto |
| 323/342 = 0,944; 283/339 = 0,835 [0,792–0,871]; 226/282 = 0,801 [0,751–0,844] | FV §4 Oss. 2 | sì (RIC) |
| disco di ripiego: 0,99 e 1,21 (G₂), 0,79 e 1,12 (G₃) a 2 e 3 s | FV §4 «Costo in area» | letto |
| regione adottata: 0,24 e 0,31 (G₂), 0,16 e 0,27 (G₃) | FV §4 «Costo in area» | letto |

## §6.5 (generatore e semi)

| Cifra | Origine | Ricalcolo |
|---|---|---|
| stato in Z modulo 2^64 | FV §5 | — |
| 1000 valori uguali su 1000; 0 su 1000 con la riparazione | FV §5 | letto |
| dieci blocchi da 400 semi; 0,726–0,977; varianza 6,0 volte | FV §5 | letto |
| 20 celle; rapporto medio 2,67; 1,62 con l'altro denominatore | FV §5 | letto |
| fattore fra 1,3 e 2,5; rapporto 0,94 con i semi riparati | FV §5 | letto (√1,62 e √6,0) |
| 0 flussi spostati su 1000 coppie di semi vicini (prove d'insieme) | PI §0 «Semi» | letto |
| 71 671 dei 175 802 istanti non rifatti con semi riparati; prove fuori dal dominio con un altro programma e un altro schema di semi | FV §5 «Cifre rifatte… Non rifatte» | letto (FV II.5: l'esenzione dell'altro programma dal difetto non è stata verificata) |
| riuso degli stessi semi nelle configurazioni | CP §7 n. 1 | letto |

## §6.6, condizioni comuni

| Cifra | Origine |
|---|---|
| 0,3–1,8 m/s; ±15°; 5 cm per asse; P_D = 0,9; Δ = 1/15 s; q = 0,2 m²/s³ | FV §6, condizioni comuni |
| corpo esteso: disco di 0,45 m, misura nel baricentro della parte visibile | PI §0 («Che cosa condivido») |
| 424×240; due livelli di rumore; tre camere (D435i, D455, Gemini 335) | FV §6, condizioni comuni |

## Tavola «Sicurezza» e commento

| Cifra | Origine | Ricalcolo |
|---|---|---|
| 0 su 175 802 istanti; 24 835 passaggi a semi indipendenti; 7 comportamenti; τ = 0,5–5 s; 0–0,016 % | FV §6.1 riga 1 | sì (RIC: 0,0155 %) |
| 0 su 11 946 289 istanti, anche a −20 cm | PI §1 riga e1; CP §7 n. 2 | letto |
| 928 e 24 su 23 402; 3,97 % e 0,10 %; 0,75 m | PI §1 riga a2; SV3 righe 136–137 | letto |
| 1 su 5704 (limite 0,99 per mille); 17 su 5704 (1,9–4,8 per mille) | CP §2 | sì (RIC) |
| 0 su 14 400 (0–0,027 %); P_D = 1; e_Ω ∈ {−0,2; 0; +0,2} m; margine 0,40 m | FV §6.1 riga 2 | sì |
| 13 su 4800 (0,16–0,46 %); P_D = 0,9; e_Ω = −0,2 m | FV §6.1 riga 3 | sì |
| 0 su 2 907 032 celle·fotogramma; 131 sequenze; 0–2,9 % | FV §6.1 riga 6 | sì (RIC: 2,85 %) |
| 0 e 4 su 3 588 836 celle·fotogramma (424 e 848 px, anche limite) | ID §3 tabella, riga «Libero nell'ombra vera», colonna finale; ID §0 (4 a 848 px, limite, scatola di 15 cm a 2,0 m) | letto |
| 5 su 3 992 186 (4 al limite con buchi ×3,5; 1 al nominale, 424 px, scatola a 2,8 m) | CI §4 | letto |
| regola adottata: 0 su 9000 fotogrammi, due lanci; 10 scene; 300 condizioni; 320×240; ±0,5°; per condizione 0–1,3 % | LC §1, §2; CP §3 | sì (RIC: 1,26 %) |
| 99 su 3038 fotogrammi; 15 passaggi su 90, 10,4–25,7 % | FV §6.1 righe 7–8 | sì |
| 0 su 3921 e 0 su 3922 fotogrammi (424 e 848 px) | ID §3 tabella, riga «Nascosta fuori dall'avviso»; CI §1 | letto |
| 240 condizioni, 7200 fotogrammi; 932; 98; 6 fotogrammi con violazione | LC §2 tabella | letto (CP §1 riga 2: 0 differenze) |
| 3,0 m col 5 % sparso; 1,5 m col 30 %; 2,4 m a +0,5° con rumore al limite | LC §2; CP §3 | letto |
| a −1°: 150 fotogrammi su 300; scatola da 10 cm a 2,6–2,9 m | LC §2 «Inclinazione»; CP §3 | letto |
| regola scelta fra quattro dopo un primo lancio | CP §3; LC §0 n. 4 | letto |
| scatola di 15 cm a 2 m | ID §0 «Scoperta a margine»; CI §4 | letto |
| 140 passaggi su 140 con l'avviso acceso alla fine | ID §2 n. 6; CI §1 | letto |
| avviso acceso 2 s dopo la rimozione del pannello: 10 su 10 | CI §3 «Avviso perpetuo» | letto |

## Tavola «Continuità» e commento

| Cifra | Origine | Ricalcolo |
|---|---|---|
| 1958 / 1991 / 1999 su 1958 / 2000 / 2000; 99,8–100 / 99,1–99,8 / 99,7–100 % | FV §6.2 riga 1 | sì |
| 19,0 / 38,1 / 33,3 %; 105 301 / 118 875 / 139 132 cicli | FV §6.2 riga 2 | letto |
| 0 su 13 638 / 5600 / 5597; 0–0,028 / 0–0,069 / 0–0,069 %; insieme 0–0,016 % | FV §6.2 riga 4 | sì |
| 0 su 23 402; 12 configurazioni × 5 comportamenti; 6000 soggetti distinti; 0–0,064 % | PI §1 riga a1; CP §0 (1) e §7 n. 1; SV3 riga 162 | sì (RIC) |
| 0 su 217 861; al più 70 400 soggetti distinti | PI §1 riga a1; CP §7 n. 1; SV3 riga 162 | letto |

## «Precisione nel dominio dichiarato»

| Cifra | Origine | Ricalcolo |
|---|---|---|
| dominio: 4 fotogrammi; 0,3–1,8 m/s; 400 percorsi registrati | FV §6.3 | letto |
| semiampiezza ≤ 0,03 | FV §6.3 | letto |
| tabella per comportamento, riga «prosegue»: 1 s: 0,980 / 0,995 / 0,990; 2 s: 0,940 / 0,964 / 0,960; 3 s: 0,899 / 0,968 / 0,924 (G₁ / G₂ / G₃) | FV §6.3, prima tabella (confronto a macchina con il capitolo: uguale) | letto |
| tabella per comportamento, riga «rallenta»: 1 s: 0,988 / 0,991 / 0,996; 2 s: 0,959 / 0,959 / 0,959; 3 s: 0,935 / 0,926 / 0,919 (G₁ / G₂ / G₃) | FV §6.3, prima tabella (confronto a macchina con il capitolo: uguale) | letto |
| tabella per comportamento, riga «si ferma»: 1 s: 0,985 / 0,991 / 0,989; 2 s: 0,965 / 0,977 / 0,959; 3 s: 0,956 / 0,968 / 0,939 (G₁ / G₂ / G₃) | FV §6.3, prima tabella (confronto a macchina con il capitolo: uguale) | letto |
| tabella per comportamento, riga «torna indietro»: 1 s: 0,985 / 0,993 / 0,987; 2 s: 0,972 / 0,969 / 0,956; 3 s: 0,977 / 0,976 / 0,935 (G₁ / G₂ / G₃) | FV §6.3, prima tabella (confronto a macchina con il capitolo: uguale) | letto |
| tabella per comportamento, riga «sosta lunga»: 1 s: 0,991 / 0,991 / 0,993; 2 s: 0,970 / 0,973 / 0,971; 3 s: 0,961 / 0,966 / 0,948 (G₁ / G₂ / G₃) | FV §6.3, prima tabella (confronto a macchina con il capitolo: uguale) | letto |
| tabella per comportamento, riga «N per cella»: 1 s: 1872–1935 / 800 / 799–800; 2 s: 879–1844 / 529–783 / 774–800; 3 s: 513–1818 / 284–770 / 669–791 (G₁ / G₂ / G₃) | FV §6.3, prima tabella (confronto a macchina con il capitolo: uguale) | letto |
| tabella per comportamento, riga «area relativa»: 1 s: 0,72 / 0,12 / 0,06; 2 s: 0,95 / 0,24 / 0,16; 3 s: 1,00 / 0,31 / 0,27 (G₁ / G₂ / G₃) | FV §6.3, prima tabella (confronto a macchina con il capitolo: uguale) | letto |
| 45 celle su 45; 826/879 = 0,940 [0,922–0,954]; con z₄₅ limite 0,908 | FV §6.3 riepilogo | sì (RIC: 0,9079) |
| 60 su 60; 461/513 = 0,899 [0,869–0,922] | FV §6.3 riepilogo | sì |
| 12 su 15, 3 non decise; 437/472 [0,899–0,946]; 711/774 [0,897–0,936] | FV §6.3 riepilogo | sì |
| 2400 passaggi per comportamento in G₂ e G₃, 4000 in G₁ | PI §2 (b) | letto |
| G₂: 15 su 15; 1222/1265, 0,955 (0,946); 666/698, 0,936 (0,922) | CP §2 tabella | sì (RIC) |
| G₃: 15 su 15; 2125/2279, 0,921 (0,914); 1754/1922, 0,899 (0,890) | CP §2 tabella | sì |
| G₁: 1 su 5 a 1 s (0 su 5); 942/1045, 0,882 (0,875 su 5 celle); meno di 400 casi a 2 e 3 s | CP §2 tabella; PI §2 (b) | sì |
| G₁, tutti gli istanti: 5 su 5; 4 su 5; 4 su 5; 1257/1388, 0,889; 845/984, 0,836 | CP §2 tabella | sì |
| errore del punto: 0,18–0,19 / 0,37–0,39 / 0,54–0,60 m; punto fermo 0,97–1,00 / 1,48–1,54 / 1,59–1,66 m; N = 2400 / 2077–2115 / 1674–1734 | FV §6.3 riepilogo, ultima riga | letto (FV II.1: dalle righe riassuntive) |
| forma dichiarabile: ostacolo largo 2 m; 9 su 10 fino a 2 s; 85 su 100 fino a 3 s; 30 celle su 30; limiti 0,921 e 0,899 | CP §4 | sì i limiti |
| 400 semi per comportamento: puntiforme 0,975 / 0,967 / 0,951; esteso 0,938 / 0,924 / 0,913 | CP §2 «Confronto» | letto |
| «a 1 s circa 9 su 10 (limite 0,87)» | CP §4 | sì |
| area relativa 0,95–1,00 in G₁ da 2 s | FV §6.3 «Che cosa il risultato non dice» | letto |

## Tavola «fuori dal dominio» e commento

| Cifra | Origine | Ricalcolo |
|---|---|---|
| chi svolta: 0,864 / 0,871 / 0,941; 0,567 / 0,541 / 0,698; 0,451 / 0,383 / 0,517; N fra 538 e 1911 | FV §6.3 «Fuori dal dominio» riga 1 (N: 1911 / 800 / 798; 1578 / 667 / 792; 1504 / 538 / 735) | letto |
| chi esce lontano: 0,771 / 0,839 / 0,920; 0,320 / 0,448 / 0,665; 0,131 / 0,262 / 0,466; N fra 725 e 1933 | FV §6.3 riga 2 (N: 1933 / 800 / 800; 1791 / 761 / 800; 1762 / 725 / 788) | letto |
| corpo esteso: svolta 0,86 / 0,67 / 0,79 (2 s), 0,84 / 0,58 / 0,67 (3 s); lontano 0,82 / 0,61 / 0,79 e 0,76 / 0,57 / 0,70 | PI §2 (b) «A parte» | letto |
| τ = 5 s: 174/221 = 0,787 [0,729–0,836] | FV §6.3 riga 3 | sì |
| e_Ω = −0,2 m senza la marca: 0,459 / 0,649 / 0,765 (G₂); 0,350 / 0,375 / 0,482 (G₃) | PI §2 (c) tabella | letto |
| con la marca a ogni ciclo: 0,996 / 0,974 / 0,968; 0,986 / 0,960 / 0,928 | PI §2 (c) | letto |
| con la marca che manca 2 cicli su 10: 0,801 / 0,835 / 0,884; 0,750 / 0,708 / 0,733 | PI §2 (c) | letto |
| partenza da fermo: 15/141 = 0,11; 21/134 = 0,16; 14/54 = 0,26 | FV §6.3 riga 6 | letto (FV II.1: non ricontato) |
| 36 su 46 (su 90) = 0,78 [0,64–0,88] | FV §6.3 ultima riga; II.0 | sì |
| 83 su 90 = 0,92 [0,85–0,96]; soglia di punti da 3 a 40 | FV §6.3 ultima riga, §6.4 riga 3; II.0 | sì |
| «0,1–0,8»; «10–20 cm» | FV §6.3 «Che cosa il risultato non dice» | letto |
| fermo negli ultimi 2 s: 256/256, 342/342, 249/249 a 1 s; meno di 400 casi | PI §2 (b) | letto |
| 2 celle·fotogramma più 45 al bordo | FV §6.6 riga 4 | letto |
| nessuna cifra oltre 3 s | FV §6.3 | — |

## Tavola «Identità al ritorno» e commento

| Cifra | Origine | Ricalcolo |
|---|---|---|
| 400 su 400 in 27 configurazioni; P_D = 1; 99,05–100 % | FV §6.4 riga 1 | sì |
| 10 711/10 757; 9228/9240; 6772/6967; limiti 0,994 / 0,998 / 0,968 | PI §1 riga f; SV3 riga 210 | sì (RIC) |
| 0 su 90; 3 disposizioni × 30 semi; 0–4,1 % | FV §6.4 riga 2 | sì |
| 176 su 180 (94–99 %) a 424 px; 174 su 180 (93–98 %) a 848 px | CI §0, §5 | sì (RIC) |
| dominio: 0,5 m dietro il pannello, entro 2,6 m, nominale | CI §5 | letto |
| a 0,3 m dal pannello: 0 su 10 e 1 su 10 | ID §0 | letto |
| livello limite 0 su 10 [0–28]; oltre 2,6 m 0 su 10; bambino di 1,0 m 2 su 10 [6–51]; posa +0,5° 6 su 10 [31–83] | CI §0, §3 | sì |
| 2400 su 2400; 2 disposizioni × 3 valori di e_Ω; 99,84–100 % | FV §6.1 ultima riga, §6.4 | sì |
| 1457/3029 = 0,481; 2567/3609 = 0,711; 2393/3540 = 0,676; riaggancio a 0,40 m | PI §2 (d) | letto |
| 3027/3041; 3493/3616; 3239/3546; 0,992–0,997; 0,960–0,971; 0,904–0,922 | PI §2 (d); CP §2 | sì |
| 12 su 12 [76–100]; 19 su 20 [76–99] | ID §3 (d); CI §0 | sì |
| fusione in 90 passaggi su 90 | FV §6.4 «Che cosa il risultato non dice» | letto |
| rapporto col picco 0,30, scelto dopo i dati | ID §0, §5 | letto |
| «circa 97 %»; tre comportamenti; 27 su 30 in una serie | CI §0 | letto |
| 0 fotogrammi fuori dall'avviso su 264 (0–1,4 %) | CI §0, §4 | sì |
| le due regole mai eseguite insieme | SV3 riga 21 | letto |
| identità nuova sul bordo del campo: 10 su 10 | CI §3, §5 n. 6 | letto |

## Tavola «Elementi mobili e ostacoli» e commento

| Cifra | Origine | Ricalcolo |
|---|---|---|
| 0,5 m/s; entro 1 s; da 2 m: 100 %, N = 2000, ≥ 99,81 % | FV §6.5 riga 1; DISC «D2» | sì |
| da 3 m: 85,85 % e 26,60 %; ±1,5 e ±1,9 punti | FV §6.5 riga 2 | letto |
| parete: 0 e 400 su 400; 0–0,95 % e 99,05–100 % | FV §6.5 riga 3 | sì |
| pannello: 79 su 90, 79,4–93,0 % | FV §6.5 riga 4 | sì |
| pannello con i gruppi dalle celle forti: 0 e 0 su 140 passaggi | ID §3 tabella | letto |
| tracce sul pavimento vuoto: 137 e 206, poi 0 e 0; 9 sequenze, 270 fotogrammi | ID §3 tabella | letto |
| scatola di 15 cm a 2 m: 190 su 190 fotogrammi, 19 sequenze, 3 al limite | ID §3 tabella | letto |
| cubo di 10 cm a 2 m: gruppo 0 su 60 [0–6], «occupato» 60 su 60; scatola a 2,8 m: 45 su 60 [63–84] | CI §3 «Oggetti piccoli» | sì |
| casi limite: 0; 0; 7 su 10 fotogrammi (scatola a 0,8 m; vetro; sospeso a 2,0 m); entro 15 cm | FV §6.5 riga 7 | letto |
| taglia minima inseguibile: 15 cm entro 2 m | CI §5 correzione 1 | letto |
| 105–106 tracce confermate su 3 pavimenti vuoti al livello limite | ID §2 n. 7 | letto |

## «Profondità simulata» e «Traiettorie pubbliche»

| Cifra | Origine | Ricalcolo |
|---|---|---|
| bordo dell'ombra: +2,0…+14,6 cm, mediana +6,2 cm; 115 su 115 (96,8–100 %) entro ±20 cm | FV §6.6 righe 1–2 | sì l'intervallo |
| livello limite: 0 su 8 (0–32,4 %); errori da −65 a +73 cm | FV §6.6 riga 3 | sì |
| pixel senza dato: 7,8 % contro 24–34 % | FV §6.6 «Che cosa il risultato non dice» | letto (FV II.1: non ricontato) |
| 227 tratti (scelta di q); 219 tratti, 9 persone | FV §6.7 | letto |
| regione al 90 %; q = 0,2: 0,977 / 1,000 / 1,000 (214, 219, 219 su 219); 0,948–0,990 / 0,983–1 / 0,983–1 | FV §6.7 riga 1 | sì |
| secondo programma: 0,982 / 0,995 / 1,000 | FV II.1, II.2 n. 8; DISC «D6» | letto |
| q = 0,05: 0,795 / 0,804 / 0,831 (±0,05); q = 0,01: 0,534 / 0,521 / 0,516 (±0,07) | FV §6.7 riga 2 | letto |
| errore mediano 0,21 / 0,49 / 0,81 m; secondo programma 0,22 / 0,44 / 0,73 m | FV §6.7 riga 4; DISC «D6» | letto |
| da 7 a 42 tratti a testa; numerosità efficace fra 9 e 219 | FV §6.7 | letto |
| «non conferma il livello 0,90» | CP §6 n. 1 | — |

## «Classificazione e profili di classe»

| Cifra | Origine | Ricalcolo |
|---|---|---|
| 0 violazioni su 20 000 sequenze; limite a una coda 1,5 su 10 000; 0 su 20 000 nella seconda simulazione | BC §7 e riga 7; AC «Stati» | sì (RIC: 1,50 su 10 000, esatto a una coda) |
| regola scartata: 0,353 e 0,791 | BC §7 e riga 8 | letto |
| carrello etichettato «pedone» scoperto nel 29,1 % di 20 000 uscite | BC §7 | letto |
| coerenza cinematica: 0 scatti su 2000 da fermo; a 3,0 m/s² lo scatto precede il contatto in 2 su 2000 | AC n. 4 | letto |
| persona nella regione «carrello» 0,70–0,74, «treno» 0,11–0,24; carrello a 3 m/s nella regione «pedone» 0,02–0,10; 6000 prove | BC riga 108 | letto |
| nessuna classe diversa da «persona» nella catena; regola mai eseguita sulla catena | BC §7 «Non provato» | — |

## §6.7 (limiti comuni)

| Cifra | Origine |
|---|---|
| 10–50 passaggi per riga | FV §7 |
