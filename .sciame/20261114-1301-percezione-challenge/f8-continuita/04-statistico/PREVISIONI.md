# Previsioni — sciame-statistico, f8 corsia A

## Blocco 1 — scritto alle 2026-11-14T15:14:46+01:00

Che cosa avevo già letto a quest'ora: la traccia, il contratto f8, la coda di ADDENDUM_UTENTE.md, TORNEO.md per intero,
risultati_A_parte2.txt e risultati_A2_parte2.txt, SOLUZIONE_V2.md. Non ho ancora letto: VERDETTO.md, MISURE*.md, AUDIT.md,
i risultati della parte 3, gli script. Nessun calcolo mio eseguito finora. Le previsioni P1–P3 sono quindi cieche rispetto
ai miei calcoli ma NON rispetto ai numeri del torneo (0,89–0,93; torna 0,56–0,66), che conosco.

- **P1 (numerosità, binomiale esatta).** Per distinguere una copertura vera di 0,90 da 0,80 (prova a una coda, alfa 0,05,
  potenza 0,80) servono fra 80 e 130 passaggi indipendenti; per distinguere 0,90 da 0,95 fra 220 e 320. Con 30 passaggi
  la semiampiezza dell'intervallo di Wilson al 95 % attorno a 0,90 è fra 0,09 e 0,13. Smentita: un valore fuori da questi intervalli.
- **P2 (che cosa manca nei file).** In nessun file dei risultati del torneo o del nucleo compaiono, per orizzonte E per
  comportamento, tutte e quattro: copertura a due livelli (50 % e 90 %), larghezza della regione, errore mediano e al 90°
  percentile del punto previsto contro le due linee di base, una regola di punteggio propria. Mi aspetto: copertura sì (a 95 % e 99 %, non a 50/90),
  larghezza in parte (quota d'ombra), errore del punto no, punteggio proprio no. Smentita: un file che li ha tutti.
- **P3 (continuità, controllo 1).** La quota dei cicli senza osservazione in cui il nucleo emette una posizione più probabile
  con una regione a livello dichiarato è sotto il 50 % per occlusioni di 2 s o più (lo strato 2 si spegne a 0,4–0,7 s;
  dopo resta il cuneo, che non è una stima del movimento). La ricavo dai file, non da una prova nuova. Smentita: quota >= 50 % a 2 s.
- **P4 (taratura del nucleo, ricalcolo).** Ricalcolando dai conteggi con Wilson, la copertura della regione nominale 95 % con q = 0,2
  ha il limite SUPERIORE dell'intervallo al 95 % sotto 0,95 in almeno 5 celle su 7 (G1 a 1, 2, 3 s; G2 a 0,5, 1, 2, 3 s) e per «torna»
  il limite superiore sta sotto 0,70 a 1–3 s. Smentita: meno di 5 celle, o un limite superiore di «torna» >= 0,70 a 2 o 3 s.

## Blocco 2 — scritto alle 2026-11-14T15:18:35+01:00, prima di scrivere ed eseguire `misure_f8.py`

Letto in più dal blocco 1: VERDETTO.md, MISURE_V2.md, MISURE_V2_bis.md, v2_C6.txt, la testa di risultati_main1_parte3.txt
(raggio medio del cerchio 0,47 / 0,93 / 2,19 / 3,77 m a 0,5 / 1 / 2 / 3 s), f1/21d3813ca7e1/risultati.txt (Kalman), le righe 1–260
di torneo_parte2.py (generatori g1, g2 e filtro Ax, che importo senza modificarli). Nessun calcolo mio eseguito finora.

Impianto: predittore = filtro Ax con q = 0,2 (riscritto dall'avversario); generatori = g1 (avversario) e g2 (copia di tracciamento):
nessuno è mio né dell'autore del filtro. Un passaggio = una occlusione = una sola previsione all'orizzonte D (0,5, 1, 2, 3, 5 s).
Regione a livello p = cerchio d² <= quantile chi-quadro a 2 gradi (1,386 / 4,605 / 5,991 per 50 / 90 / 95 %) sulla misura alla ricomparsa.
Scelte fissate ORA e non ritoccate dopo: miscela «squadra» 90/10/0/0 e «giurato» 50/20/20/10 (prosegue/sosta/torna/svolta);
capsula: punteggio s = max(|e_par|/L, |e_perp|/W), con e misurato dall'ultima posizione filtrata lungo la direzione della velocità
stimata, L = |v|·t + 0,3 m, W = 0,15 m + 0,2·|v|·t; riferimento per il CRPS: gaussiana centrata su «fermo» con la dispersione
per asse stimata su un insieme di taratura separato.

- **P5 (diagramma di affidabilità).** A livello nominale 50 % il cerchio del filtro contiene «prosegue» in >= 0,90 dei passaggi e
  «torna» in <= 0,35 a 2 s; sulla miscela 60/15/10/15 la copertura al 50 % nominale sta fra 0,65 e 0,85: cioè la regione NON è
  tarata al 50 % benché al 95 % sembri quasi giusta. Smentita: miscela al 50 % nominale dentro [0,45; 0,55].
- **P6 (errore del punto).** Sulla miscela, mediana dell'errore del punto a velocità costante a 2 s <= 0,5 m contro >= 2,0 m di
  «fermo»; 90° percentile a 2 s fra 1,3 e 2,3 m (fermo fra 2,8 e 3,4 m). Per «torna» la mediana dell'errore del punto a velocità
  costante è >= 1,5 volte quella di «fermo» a 2 s. Smentita: uno dei tre fuori.
- **P7 (CRPS per componenti).** Sulla miscela il CRPS medio del filtro è minore di quello del riferimento «fermo con dispersione tarata»
  a tutti gli orizzonti (abilità > 0); per «torna» l'abilità è negativa da 1 s in su. Smentita: abilità <= 0 sulla miscela a un orizzonte,
  o > 0 per «torna» a 2 s.
- **P8 (fotogrammi correlati).** Correlazione intraclasse dell'indicatore «dentro la regione al 90 %» fra i fotogrammi dello stesso
  passaggio (D = 3 s, 45 fotogrammi, miscela) >= 0,5: effetto del disegno >= 20, cioè un passaggio vale al più 2,2 fotogrammi indipendenti.
  Smentita: correlazione < 0,5.
- **P9 (conforme, scambiabile).** Tarando su n = 30 passaggi della stessa miscela, la copertura realizzata ha media in [0,89; 0,92] e
  5° percentile in [0,77; 0,83]; con n = 100 il 5° percentile sta in [0,84; 0,87]. Entro 0,015 dalla teoria Beta(k, n+1-k).
  Smentita: fuori da questi intervalli.
- **P10 (conforme, spostamento).** Tarata sulla «squadra» e provata sul «giurato», copertura realizzata a 2 s <= 0,70 al nominale 0,90.
  Smentita: >= 0,80.
- **P11 (prezzo della garanzia per comportamento, disco).** La regione conforme «massimo sulle classi» centrata sul punto a velocità
  costante copre ogni classe >= 0,88 e il «giurato» >= 0,90, ma a 2 s ha raggio >= 2,3 volte il raggio al 90 % del filtro; centrata
  su «fermo» è più piccola di almeno il 15 %. Smentita: rapporto < 2, o «fermo» non più piccola.
- **P12 (capsula lungo l'asse del moto, esplorativa).** Tarata come massimo sulle tre classi sull'asse (prosegue, sosta, torna), a 2 s
  ha area fra 5 e 12 m² (cerchio al 90 % del filtro: circa 8 m²) con copertura minima sulle tre classi >= 0,85; «svolta» resta < 0,5.
  Con «svolta» nel massimo l'area supera 20 m². Smentita: area > 12 m², o copertura minima < 0,85, o svolta >= 0,5, o area con svolta <= 20 m².

## Blocco 3 — scritto alle 2026-11-14T15:22:34+01:00, DOPO aver visto le uscite di tabelle, misure, fotogrammi e conforme, PRIMA della modalità «unione»

Non è cieca rispetto a S5: conosco la copertura per classe del cerchio (svolta 0,80–0,84) e della capsula (torna 0,93–0,96).
Scelte fissate ora: regione = cerchio del filtro scalato di s UNITO alla capsula scalata di s (capsula con soglia di base 1,0);
punteggio s = min(distanza/raggio al 90 % del filtro, punteggio della capsula); soglia = massimo sulle QUATTRO classi del
quantile conforme al 90 %, 50 passaggi di taratura per classe; area vera stimata per campionamento (capsula meno la parte già nel cerchio).

- **P13 (unione, falsificatore di statistico-1).** A 1, 2 e 3 s: copertura media >= 0,88 in ognuna delle quattro classi e >= 0,93 sul
  «giurato»; soglia s fra 1,05 e 1,35; area fra 1,5 e 3,0 volte quella del cerchio al 90 % del filtro (che copre «torna» solo nel 51–60 %).
  Smentita: una classe < 0,88, oppure s > 1,35, oppure area > 3,0 volte.

## Blocco 4 — scritto alle 2026-11-14T15:25:55+01:00, dopo S6 e dopo `h9_cieco.py` (che NON aveva previsione: è un conto notato dopo), PRIMA della modalità «incrociata»

Prova incrociata fra generatori: soglia dell'unione tarata su g1 (massimo sulle 4 classi, 50 passaggi per classe, come S6) e provata
su g2 (copia di truth() di tracciamento: soste a commutazione, svolte fino a ±90°, nessuna inversione netta), 3000 passaggi per orizzonte.
Conosco già le coperture del cerchio al 90 % su g2 (0,877 / 0,885 / 0,895 a 1 / 2 / 3 s; con manovra nel buio 0,65 / 0,78 / 0,84).

- **P14.** Unione tarata su g1 e provata su g2: copertura complessiva >= 0,92 a 1, 2 e 3 s; sui passaggi con manovra nel buio >= 0,85.
  Per confronto, il disco conforme tarato sulla miscela 60/15/10/15 di g1 (n = 100) dà su g2 fra 0,85 e 0,91 (non meglio del cerchio).
  Smentita: unione < 0,90 complessiva o < 0,85 con manovra a uno dei tre orizzonti.

## Esiti — scritti alle 2026-11-14T15:27:57+01:00 (file accanto a ogni numero; per rifare: `sh rifai.sh`)

| # | Esito | Numeri (file) |
|---|---|---|
| P1 | **smentita in una clausola** | 0,90 contro 0,80: primo n 78, stabile da 89 (previsto 80–130: regge sul valore stabile). 0,90 contro 0,95: 179, stabile da 203 (previsto 220–320: **smentita**, la mia stima era alta). Semiampiezza di Wilson a n = 30: 0,111 (regge). `out_tabelle.txt` |
| P2 | **regge** | Nessun file ha le quattro misure insieme: `grep` di CRPS, energia, intervallo, conforme in f0–f6 trova solo una fonte (F24) e nessun risultato; l'errore del punto c'è solo come RMSE sul generatore dell'autore del filtro (`f1/21d3813ca7e1/risultati.txt`); le coperture sono solo a 95 e 99 % |
| P3 | **regge, per derivazione** (rapporto di mediane, non una misura diretta) | «previsto» 0,40–0,53 s su 1,07–1,13 s di buio = 35–50 % (`MISURE_V2.md`, P4); sosta: circa 0,5 s su 5,13 s = circa 10 %; torna: su 2,20 s = circa 20 % (`v2_C6.txt`) |
| P4 | **regge** | Limite superiore di Wilson sotto 0,95 in 7 celle su 7; «torna» a 2 e 3 s: limite superiore 0,610 e 0,615 (a 1 s 0,707, appena sopra 0,70). `out_tabelle.txt` |
| P5 | **regge** | Al 50 % nominale, 2 s: prosegue 0,995, torna 0,340, miscela 0,788. `out_misure.txt` |
| P6 | **smentita in una clausola su tre** | Miscela, 2 s: mediana 0,50 m (al limite) contro 2,48 m di «fermo»; 90° percentile 1,88 m (fermo 3,39 m). «Torna»: rapporto delle mediane 1,78 / 1,29 = 1,38, non >= 1,5 |
| P7 | **regge sul falsificatore scritto; un'attesa mancata** | Abilità sulla miscela +0,74 / +0,69 / +0,60 / +0,56 / +0,53; «torna» a 2 s −0,38, ma a 1 s +0,04 (avevo scritto «negativa da 1 s in su») |
| P8 | **regge** | Correlazione intraclasse 0,512 a 3 s (effetto del disegno 23,5; 1,9 fotogrammi efficaci per passaggio); a 1 s 0,205 (3,9). `out_fotogrammi.txt` |
| P9 | **regge** | n = 30: media 0,909, 5° percentile 0,803 (teoria 0,805); n = 100: 0,851 (teoria 0,848). `out_conforme.txt` |
| P10 | **regge** | Tarata sulla «squadra», sul «giurato» 0,658 a 2 s (0,720 a 1 s, 0,640 a 3 s) |
| P11 | **regge sul falsificatore scritto; due attese mancate di poco** | Raggio 4,19 m = 2,19 volte il cerchio (attese >= 2,3); su «fermo» 3,57 m: più piccola del 14,8 % nel raggio (attese >= 15 %), del 27 % nell'area. Classi >= 0,90, «giurato» 0,979 |
| P12 | **regge** | Capsula su tre classi, 2 s: 10,2 m², classi 0,92 / 0,98 / 0,95, svolta 0,47; con svolta 65,0 m² |
| P13 | **regge** (non cieca rispetto a S5) | 1 / 2 / 3 s: soglia 1,16 / 1,25 / 1,17; area 2,61 / 2,25 / 1,76 volte; classe peggiore (svolta) 0,890 / 0,904 / 0,909; «giurato» 0,988 / 0,987 / 0,982. `out_unione.txt` |
| P14 | **smentita a 1 s, di misura** | Su g2: complessiva 0,948 / 0,960 / 0,955 (regge); con manovra nel buio 0,848 / 0,922 / 0,931: a 1 s sta sotto 0,85. A 0,5 s (fuori dalla previsione) 0,738. Disco conforme sulla miscela: 0,879 / 0,888 / 0,864 (nella fascia prevista). `out_incrociata.txt` |

**Senza previsione (notato dopo):** `h9_cieco.py` (il criterio H9 passa con probabilità 1,000 con «torna» coperto al 50 % o allo 0 %); la riga (d) di S5 (una sola soglia per tutti gli orizzonti); il raggio al 90 % del cerchio (1,91 m a 2 s: nel blocco 2 avevo scritto «circa 8 m²», sono 11,4).
**Correzione di un'etichetta:** la prima uscita di `misure` diceva «1500 per la taratura del riferimento»; sono 600. Corretta la stampa, rifatto il lancio: nessun numero cambia (`diff` di una riga).

## Previsione registrata e NON eseguita (falsificatore proposto per statistico-1)

- **P15, scritta alle 2026-11-14T15:27:57+01:00.** Unione tarata su g1 e provata su g3 (`traiettoria()` del rovesciatore, con l'ombra geometrica): «torna» coperto
  >= 0,85 in ogni fascia di durata del buio da 0,75 s in su (oggi il cerchio al 95 %: 0,056 / 0,087 / 0,335 / 0,785). Smentita: una fascia < 0,80.
