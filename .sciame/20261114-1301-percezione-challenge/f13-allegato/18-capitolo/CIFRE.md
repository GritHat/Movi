# CIFRE del capitolo 8 e delle appendici A e B — origine di ogni cifra

Percorsi relativi a `.sciame/20261114-1301-percezione-challenge/`. Sigle dei file:
**SOL** `f12-integrazione/20-finale/SOLUZIONE_V3.md` · **SCH** `f12-integrazione/22-schermo-finale/SCHERMO_E_DEMO.md` · **BLO** `f14-classificazione/20-inclusione/BLOCCO_CLASSIFICAZIONE.md` · **PRO** `f14-classificazione/01-profili/PROFILI.md` · **G02** `f13-allegato/02-geometria/FASCICOLO_GEOMETRIA.md` · **V04** `f13-allegato/04-statistica/FASCICOLO_VALUTAZIONE.md` · **C05** `f13-allegato/05-costo/FASCICOLO_RAPPRESENTAZIONI_E_COSTO.md` · **B06** `f13-allegato/06-bibliografia/FASCICOLO_BIBLIOGRAFIA.md` · **VD** `f10-dati/23-verdetto/VERDETTO_DATI.md` · **DISC** `f13-allegato/DISCORDANZE_DEI_FASCICOLI.md`.

Nessuna cifra è stata ricontata eseguendo un simulatore. «Rifatto a mano» = ho rifatto io il conto aritmetico dalla formula del file (controllo che condivide formula e parametri con la fonte: vale solo contro errori di aritmetica).

## 8.1 Contratto d'uscita
| Cifra | Origine |
|---|---|
| 15 Hz; 3 fotogrammi = 0,2 s | SOL §1 «Convenzioni» |
| «non confermato» per 0,2 s | SOL §1.5, tabella degli stati |
| «previsto ampio» oltre l'80 % dell'ombra | SOL §1.6, riquadro |
| 17 settori d'azimut | SCH §1 «Disposizione» |
| «suolo visto libero da 1,3 m a d m»; d ≤ portata − w = 3 − 0,40 = 2,6 m | SOL §1.10, riquadro; invariante I12 (§2) |
| 9 settori su 17 vedono il suolo da 1,3 m; 8 laterali «sconosciuto» | SOL §1.10 «Stato»; SCH §1 «Livello per settore» |
| nessun livello oltre 3 s | SOL §1.6 (orizzonte 3 s); §7 tabella «oltre 3 s» |
| segnale sonoro 0,3 s; ordine di precedenza (1)–(7) | SCH §2; SOL §1.10 |

## 8.2 Registro degli eventi
| 0 violazioni su 600 scene; eventi mancati 16–52 % delle scene; scomparse spurie 12,5 % | SOL §1.11 «Stato» (non riaperto il file d'origine di f7) |
|---|---|

## 8.3 Salute del sensore
| Cifra | Origine |
|---|---|
| pixel validi < 10 % entro 3 fotogrammi | SOL §1.1, riquadro e «Parametri» |
| scarto di posa ≥ 0,5° non parte | SOL §1.1 |
| stima del piano dai primi fotogrammi: errore di 5° su una sequenza registrata | SOL §1.1 «Stato» |
| oggetto di 10 cm a 2,5 m «occupato»; pavimento vuoto 30 s | SOL §1.1, riquadro |
| 989–995 celle «libero» per altri 3 fotogrammi coi filtri accesi | SOL §1.1 «Stato»; VD §2 «Le nove condizioni», 1 |
| 0,13 s senza fotogramma o tre identici; metà della taratura per 0,2 s; 0,5° o 5°/s; piano 0,5° | SOL §1.9, riquadro |
| 1 444 celle «note» su 1 460 col 10 % di pixel validi | SOL §1.9 «Stato» |
| dilatazione v_max·T + w | SOL §1.9, riquadro |
| segnale in 0,13 s; 0 falsi in 60 s | SOL §1.9 «Stato»; §3 riga R6 |
| 13 istanti su 13 fuori / 13 su 13 dentro | SOL §1.9 «Stato» (attacco, punto 10) |

## 8.4 Profilo di chi porta il sensore
| Cifra | Origine |
|---|---|
| t_conf = 0,267 s; τ = 0,155 s; C = 0,95 m | BLO §3 «Formule» |
| C = 0,85 m (non riscontrato sul testo della norma) + 0,10 m | G02 §7, «Confronto con la distanza di separazione» e Tabella 9 |
| formule di T_ant e d_serve | BLO §3 |
| T_r 1,0 / 0,3 / 1,5 + 0,3 / 0,3 / 1,5 s | BLO §3, tabella |
| T_ant 1,42 / 0,72 / 2,22 / 0,72 / 1,92 s | BLO §3, tabella; rifatto a mano (0,422 + T_r) |
| velocità coperta 1,44 / 2,84 / 0,92 / 2,84 / 1,07 m/s | BLO §3, tabella; rifatto a mano (2,05 / (0,422 + T_r)); G02 §7 dà 1,44 con 1,425 s |
| in moto: v_e 1,0 e a_f 1,5 → 2,01 m e 0,72 m/s; v_e 3,0 e a_f 3,0 → 4,62 m; v_e 1,0, a_f 1,0, T_r 1,5 → 3,37 m | BLO §3, tabella; rifatto a mano |
| T_r della persona con disabilità visiva: 1,0 s (PRO §2) contro 1,5 s (BLO §3; BLO §11 `sd-K12`) | **due valori, nessuno decide: riportati entrambi**; campo 0,5–1,5 s da PRO §2 e BLO §3 |
| 6 cm di margine a passo normale | BLO §6, riga «persona a piedi» (2,94 m) |
| 0,355 s nella fascia in moto | BLO §3 «Fascia in moto»; SOL §1.7 |
| aggiunta di 2σ_v nel tempo disponibile («tardivo») | BLO §4, modifica a 1.10 |

## 8.5 Bilancio di latenza
| Cifra | Origine |
|---|---|
| 16,7 / 95 / 22 / 21,3 ms; somma 155 ms | G02 §8, Tabella 10 |
| 138–172 ms; 95° percentile 170 ms; requisito 150 ms | G02 §8 |
| circa 71 ms → circa 131 ms | G02 §8; DISC geometria 8. **Contestata: riportate entrambe (155 con 95 ms, 131 con 71 ms), come dice DISC** |
| 1 024 campioni a 48 kHz | G02 §8; C05 §6 punto 3 |

## 8.6 Invarianti (tabella)
| Riga | Cifra | Origine |
|---|---|---|
| 1 | 0 su 300 condizioni, 9 000 fotogrammi; posa entro 0,5°; limite 1,3 % | SOL §1.2 «Stato»; §2 I1 |
| 3 | 8 passaggi su 90; 1 su 140 | SOL §2 I3 |
| 4 | 0,20 m; «0 casi misurati, non garantiti dalla sola regola» | SOL §2 I4; DISC dimostrazioni D9 |
| 5 | 0 su 20 000 e 0 su 20 000 | BLO §5 I15; §7 |
| 7 | 0 fotogrammi su 336, 169, 2 360; rilascio 10 su 10 | SOL §2 I7; §1.7 |
| 10 | 0 su 23 402; 6 000 camminatori; meno di 6,4 su 10 000; 24 e 928 su 23 402 | SOL §1.6 «Continuità»; §2 I10; §1.5 |
| 12 | 1,3 m; 2,6 m | SOL §2 I12 |
| 14 | 600 scene | SOL §1.11 |
| testo | 0,72 m a 2,5 m/s | G02 §7, Tabella 8; SOL §2 «Cadono» |

## 8.7 Condizioni di validità
| Cifra | Origine |
|---|---|
| 1,2 m; 15°; 0,5°; 3 m; 2,6 m; 4 fotogrammi | SOL §7 «La forma più forte che resta vera»; §1.1 |
| 0,133 + 0,155 + 0,067 = 0,355 s; 0,40/0,355 = 1,13 m/s; 0,56 m/s con 20 cm | SOL §1.7 «La fascia w». **Contestata in DISC (dimostrazioni D4: 1,85 / 1,4 / 1,13 m/s): scelto 1,13 e 0,56 perché la soluzione finale li adotta con tutti e tre i termini; 1,39 m/s (G02 §7) è a margine nullo, senza tenuta** |
| 1,61 m d'ostacolo per 1,70 m di persona | VD §2 «Le nove condizioni», 3; SOL §5 «Decise dall'adozione» |
| ostacolo largo 2 m; 3 s | SOL §1.6 |

## 8.8 Limiti
| N. | Cifra | Origine |
|---|---|---|
| 1 | 654 su 800 a 2,0 m; 600 su 800 a 1,5 m | SOL §1.2 «Controesempi e limiti» |
| 1 | 0 su 900 col corpo che non rimanda segnale; palo di 3 cm non provato | SOL §1.2 «Stato» e «Controesempi» (scritto «fotogrammi» per analogia con «900 su 900» della regola caduta: l'unità non è esplicita nel file) |
| 2 | 1,24 m; 1,71–1,73 m; 1,22 e 1,69 m con 424 px | SOL §1.1 «Vuoto vicino»; DISC geometria 2 (**due focali: riportate entrambe**) |
| 2 | 15 cm sotto 1,09 m; testa di 1,70 m sotto 2,01 m | SOL §7 «Limiti»; DISC geometria 3 (**2,01 m è per 1,70 m; 2,41 m è per 1,80 m: scelto 2,01**) |
| 2 | oggetto di 0,35 m a 0,5–0,8 m: 0 pixel | SOL §1.2; §7 |
| 3 | 374 celle; 4,7–7,3 % dei settori-fotogramma; barra di 1 cm a 0,8 m | SOL §1.2 «Controesempi e limiti» |
| 3 | circa 1,65 m; pannello di 1,6 m: 10 passaggi su 90 | SOL §7 «Limiti»; VD §2, condizione 3 |
| 4 | 9 casi su 10 e più; 12 su 12; 19 su 20 | SOL §1.8 «Stato»; §1.4 |
| 5 | 0,86/0,67/0,79 a 2 s; 0,84/0,58/0,67 a 3 s | SOL §7, tabella «Dove cede» |
| 5 | 0,82–0,83 (0,832 e 0,818) | SOL §1.6 «Chi parte da fermo»; §7 |
| 5 | «almeno 87 su 100» fino a 1 s con ostacolo da 1 m | SOL §1.6 (limite 0,87); §7 punto 2 |
| 6 | 0,30–0,46; 0,74–0,80 con 8 cicli su 10 | SOL §1.6 «Bordo stimato»; §7 |
| 6 | 2 / 15 / 1 704 / 1 979 su 2 000 con 0,10/0,20/0,45/0,60 m | SOL §1.7 «Con l'avviso davvero acceso» |
| 6 | +2…+15 cm al nominale; da −65 a +73 cm al limite | SOL §5 riga K-404; V04 §6.6 |
| 7 | 0,67° a 2,55 m; 0,57° a 3 m; soglia 7 cm | G02 §5; SOL §1.1 (0,57° a 3 m). SOL dà anche 0,69° a 2,5 m: non usato |
| 7 | 7 celle su 7 a +1°; 146–150 fotogrammi su 300 a −1° | G02 §5; SOL §1.1 «Stato» |
| 7 | identità 6 su 10 a +0,5° | SOL §1.1; §1.8 |
| 8 | 0 su 808; 140 su 140; 10 su 10 dopo 2 s | SOL §1.7 «Costo» e «Difetto aperto» |
| 9 | 0 su 90; 79 su 90 | SOL §1.8; §1.3; VD §2 |
| 9 | 176 su 180 [94–99 %]; 174 su 180 [93–98 %]; dominio 0,5–1,6 m/s, entro 2,6 m | SOL §1.8 «Stato» |
| 9 | 0–1 su 10 a 0,3 m; 2 su 10 per 1,0 m d'altezza | SOL §1.8; §7 |
| 9 | 7,8 % contro 24–34 % | SOL §7 «Limiti»; V04 §6.6; VD §2 K-407 |
| 10 | 1,44 m/s; 3 classi su 15; 0 su 15 | BLO §6 |
| 11 | 6,35 ms; 81 ms | C05 §5, Tabella 5; SOL §7 |
| 11 | 70 lavori; 51,4 %; 22,9 % | B06 §II.3, `romlay2021` |

## 8.9 Sensore in moto
| Cifra | Origine |
|---|---|
| W = 13Δ = 0,867 s; soglia 5σ√(2/3) (κ = 4,08); 3,036 σ e 2,183 σ | G02 §5, Proposizione 9. DISC geometria 9: **seguita la forma del codice (÷√3), come il fascicolo** |
| Monte Carlo N = 2·10⁶: 0,0999 e 0,0100 | G02 §5 |
| 0,88° (1,01°/s); 0,63° (0,73°/s) | G02 §5, Tabella 7. DISC geometria 5: **scelta la forma chiusa del fascicolo, non «0,7°» del file d'origine** |
| 3,5/5,3 e 5,3/11,9 cm/s; 29 e 74 ms; 1,70° e 1,03°; 1,27° e 0,79°; 9,7/16/41 cm; 2,9° e 1,9°; 95 e 64 ms | G02 §5, Tabella 7 (DISC geometria 6: **valori in forma chiusa**) |
| 0,375 m/s | G02 §5; C05 §7 |

## 8.10 Protocollo
| Riga | Cifra | Origine |
|---|---|---|
| 1 | 30 s; 0 gruppi e tracce; 10 cm a 2,5 m | SOL §1.1; §7 «Prime tre misure» |
| 2 | 150 fotogrammi; soglia 0 | SOL §7; §5 riga K-014 |
| 3 | 60 s; 80 % oltre 2 m | SOL §5 riga K-107 |
| 4 | ±20 cm | V04 §6.6 (criterio della prova simulata); SOL §5 righe K-404, K-215 (senza numerosità) |
| 5 | 100 passaggi; 87 su 100, potenza 0,88; 96 su 100 | SOL §1.12 |
| 6 | soglia 0 | SOL §2 I3, colonna del controllo |
| 7 | 0 rilasci; 5 fotogrammi | SOL §2 I7; §5 riga `sd-K8` |
| 8 | 95° percentile ≤ 150 ms | SOL §3 riga R7 |
| 9 | 1 e 2 s; 1 s; 60 s; 1° | SOL §3 riga R6; §2 I13 |
| 10 | soglia 0 nei versi detti | BLO §5 I15 |
| testo | 30 su 30: limite 0,886 | SOL §1.12 «Stato» |

## Appendice A (parametri)
Tutti i valori vengono dai paragrafi «Parametri» di SOL §1.1–§1.9 (riga per riga: 1.1 quota, inclinazione, 30 fps e 15 Hz, portata, 10 % in 3 fotogrammi, 0,5°; 1.2 cella 1° × 0,1 m, quota 0,07–2,0 m, 3 pixel, 0,03 + 3·k·z0², k = 0,004 e 0,0100, metà impronta e 8 vicine, 0 fotogrammi di memoria, 1,3 m; 1.3 0,30, 0,05 m, 0,004 m², σ(z) 1,5/3,4/6,0 cm a 2/3/4 m, 5·σ·√(2/m) con m = 3, 1 s; 1.4 q = 0,2, 0,05–0,1, porta al 99 %, 3 su 5, R + (larghezza/2)²; 1.5 4 fotogrammi con 27,1 % e 5,2 %, 2 cicli, 0,2 s, 0,75 m; 1.6 400 = 200 + 200, 0,1 a ciclo, 3 lisciature, 80 %, 3 s, 0,3 m/s e 2 s, 8 cicli e 0,167 m, almeno 200 percorsi; 1.7 w = 0,40 m, 3 fotogrammi; 1.9 soglie della salute; 1.10 0,3 s). Livello α = 0,90: SOL §1.6 («fino al 90 %»). 1,24 m: SOL §1.1. τ, t_conf, C: come 8.4 e 8.5. Soglia 0,7 e «4 su 6»: BLO §1.

## Appendice B (riproducibilità)
| Cifra | Origine |
|---|---|
| tre camere (D435i, D455, Gemini 335); due livelli di rumore | V04 §6, condizioni comuni del tipo (II) |
| gcc 16.2.1, `-O2`; AMD Ryzen AI 9 HX 370; un filo | C05 §3 «Impianto» |
| generatore, forma dei semi, 1 000 su 1 000 e 0 su 1 000; fattore 1,3–2,5 | V04 §5 |
| 23 402; 6 000; 217 861; 608–2 359 | SOL §1.6 |
| 10 scene, 300 condizioni, 9 000 fotogrammi, due lanci | SOL §1.2 |
| 90 passaggi (3 × 30); 180 per risoluzione | V04 §6.4; SOL §1.8 |
| 219 tratti, 9 persone; efficace fra 9 e 219 | V04 §6.7 |
| 20 000 sequenze, due volte | BLO §7 |
| circa 4 minuti (241 s); 2 minuti; 12–15 minuti | SOL §6, tabella del codice |
| Wilson 826/879 → [0,9220; 0,9536]; z² = 3,8415 | V04 §2, esempio svolto |
| 6,4 su 10 000 per N = 6 000 | SOL §1.6; rifatto a mano: 3,8415/6 003,84 = 6,40·10⁻⁴ |
| (0,10 − 0,07)/2,55 = 0,67°; /3 = 0,57° | G02 §5; rifatto a mano |
