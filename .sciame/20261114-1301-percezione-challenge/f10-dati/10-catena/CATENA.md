# CATENA — la catena di riferimento di f10 (`sciame-sviluppatore`, 14 novembre 2026, 16:14–16:43)

**In testa.** *Regola violata:* nel controllo finale ho lanciato un `git status` (sola lettura, nessuna modifica),
contro il «niente git». *Cambi di stato:* «nessuno script ha mai calcolato "libero" da una profondità» → ora uno c'è,
**verificato su 25 prove** (scene a mano senza rumore e l'esempio dell'infrastruttura): non dice niente del sensore
vero. Due mie previsioni sono **smentite** (P1 nel numero; P19 con la prima realizzazione) e una era **mal posta**
(P7: scena sbagliata). *Dopo un esito* ho cambiato una lettura (L3) e tre prove (P1, P7, P11): tutto in
`PREVISIONI.md`, con le ore. *Fuori consegna:* una prova di fumo con rumore (P21). Niente rete, niente GPU.

## 1. Che cosa c'è

Dieci moduli Python con solo numpy (1280 righe; più 590 di prove e scene), elenco e comandi in `LEGGIMI.md`:
sorgente (cartella nel formato comune, lista in memoria, domani un sensore) → punti sul suolo (posa di `meta.json`,
oppure piano stimato con RANSAC e dichiarato) → mappa polare 1° × 0,1 m a quattro stati con memoria ed età →
gruppi con centro, larghezza e marca «tagliato» → porta al 99 %, ungherese, Kalman a velocità quasi costante
(q = 0,2), conferma 3 su 5, «si muove» → stati dell'oggetto, strato di possibile presenza, riaggancio, **innesto del
predittore** → una riga JSON per fotogramma e un riassunto. Gli invarianti 1, 2, 3, 4, 7 sono controlli nel codice
(`InvarianteViolato`); l'1 e il 4 sono ricalcolati per un'altra via (una memoria separata dal contatore d'età; le
distanze rifatte), gli altri rileggono gli stessi dati.

```sh
ambiente/venv/bin/python -I -B 10-catena/prove.py                                  # da f10-dati/: 25 prove, 6 s
ambiente/venv/bin/python -I -B 10-catena/esegui.py <sequenza> <uscita> [--ogni 2] [-p q=0.5] [--salva-griglie]
```

## 2. Letture scelte dove il nucleo è ambiguo (tutte parametri in `parametri.py`)

- **L1** «Alla quota attesa» = entro 5 cm. Suolo «visto» e cella «occupata» con almeno 3 punti; una cella con 1–2
  punti d'ostacolo non è né libera né occupata: esce «non osservato» (contata in `celle_ambigue`).
- **L2** «In ombra» = tutto ciò che sta oltre il primo ritorno del suo azimut, anche dove il suolo si rivede dietro
  un ostacolo basso (interruttore `libero_dietro_ostacolo`; contatore `suolo_visto_in_ombra`). Un ritorno più
  lontano resta «occupato».
- **L3** La memoria di 3 fotogrammi vale solo se la cella era stata vista **libera** (non basta il suolo), e copre
  solo i buchi: ombra, ostacolo o punti d'ostacolo nel fotogramma vincono. «Occupato ricordato» non c'è.
- **L4** Gruppi a 8 vicini; centro = media dei punti; «tagliato» = accanto, nello stesso anello, c'è l'ombra di un
  altro gruppo più vicino. Un gruppo tagliato tiene viva la traccia (porta allargata di metà larghezza), non
  aggiorna il filtro, non entra in «si muove», non fa nascere tracce.
- **L5** R(z): curva nominale in radiale, 1°/√12 in tangenziale. «Si muove»: soglia 5·σ·√2 **senza** dividere
  per √3 (il testo; `sim_v2.py` divide), contro la media più vecchia entro 1 s; `null` se non valutabile.
- **L6** Ingresso in ombra (K-018): l'ultima misura è a meno di 0,40 m da un'ombra che **non** è di un gruppo che
  contiene quella misura. Il cuneo sono le celle in ombra degli azimut di quell'ostacolo.
- **L7** Strato = cuneo più fascia di 0,40 m. Una cella del cuneo si rilascia se è vista libera *nel fotogramma*
  (non per memoria) 3 volte di fila; finito il cuneo, la traccia si chiude.
- **L8** Riaggancio: rilevamento entro la fascia del cuneo, a più di 0,40 m dalla portata, senza **nessuna** cella
  non osservata o in ombra entro 0,40 m fuori dallo strato e dalla propria ombra (lettura letterale;
  `min_celle_altro_bordo`), e una sola traccia pendente in tutta la scena. Le pendenti non passano dalla porta.
- **L9** «Perso» quando le celle del cuneo dentro il cerchio al 95 % fanno metà dell'area del cuneo; «perso» non
  porta posizione. «Affidabilità persa»: la cella dell'ultima misura è «non osservato», finché lo resta.
- **L10** I «3 fotogrammi» sono fotogrammi elaborati (`--ogni`); le regole in secondi usano `tempi.csv`.

## 3. Esito delle prove (`esito_prove.txt`: 25 su 25; previsioni scritte alle 16:21:55, prima del codice)

Pavimento vuoto: 1630 celle libere su 5400, 0 occupate, 0 in ombra. Nessun dato: 0 libere; dopo il pavimento il
«libero» dura 2 fotogrammi (età 1 e 2) e al terzo è 0. Pannello a 2,05 m: 14 celle, centro (0,000; 2,050), 126 in
ombra, 0 libere dietro. Attraversamento a 1 m/s: una identità, «si muove» dopo 0,33 s, errore < 0,05 cm. Pannello
fermo tagliato dall'ombra per 15 fotogrammi su 46: mai «si muove». Demo (pannello di 1 m a 1,9 m, sagoma a 2,3 m):
13 fotogrammi nascosti, 0 «osservato», 4 «previsto» e 9 «perso», centro vero dentro lo strato 13 su 13, stessa
identità al ritorno. Sosta di 5,8 s: strato acceso 88 fotogrammi su 88, 640 celle costanti. Riaggancio rifiutato
lontano dall'ombra e al bordo della portata (0 su 2). Bracci che devono fallire: fascia a 0 (identità persa) e 2
invarianti forzati su 2 (errore sollevato). Costo: **2,5 ms** di media, 2,9 al 95° percentile, 4,7 di massimo per
ciclo a 848×480 (N = 48, un filo, invarianti accesi, lettura esclusa). *Indipendenza:* scene e catena hanno lo
stesso autore, la stessa specifica e lo stesso modello; sono di altri solo scipy (ungherese, 200 su 200),
`profondita_del_suolo` e l'esempio dell'infrastruttura (centro a 0,4 mm dalla sua verità, 0 «osservato» nei 7
fotogrammi nascosti). Zero errori su queste scene non sono una prova universale.

## 4. Critiche al nucleo emerse scrivendolo (ciascuna con la prova)

1. **«Libero» per memoria su una cella che era occupata.** Con la regola letterale (suolo visto in uno degli
   ultimi 3 fotogrammi) una cella con suolo e ostacolo, appena il dato manca, esce «libero» per 2 fotogrammi
   (prima tornata di P19; 23 celle·fotogramma sull'esempio). Corretto con L3.
2. **Dopo un riaggancio con misura tagliata il filtro non si muove** (C6): in P8 la traccia è «osservato» per 6
   fotogrammi con la posizione del filtro fino a **5,00 m** dalla verità. Tocca la continuità visiva.
3. **«Pannello alto almeno 1,5 m»** (condizione 3 del verdetto) non nasconde una persona di 1,7 m: a 1,9 e 2,3 m
   ne servono 1,61 (conto mio); con 1,6 m la sagoma è nascosta in 0 fotogrammi su 49 (prima tornata di P7).
4. **L'«anello cieco» è una striscia**: il suolo si vede da z = 1,22 m, cioè a ±44° solo da 1,69 m (P1: 54 celle
   previste libere e non viste). La zona «1,24–3 m dentro il campo» di B7 va ridisegnata.
5. **Il riaggancio letterale è fragile**: basta una cella non osservata entro 0,40 m. Sull'esempio a 160×120 con
   `--ogni 2`: 0 riagganci e 5 «identità ambigua» (3 per celle mai campionate, 2 per la portata); a passo pieno 1
   riaggancio. Sui dati veri con buchi persistenti è da attendersi lo stesso.
6. **La marca «tagliato» scatta una cella prima**: sull'esempio la sagoma a 1 m/s non è mai detta «si muove» (3
   sole misure piene di fila) e passa a «perso» senza un fotogramma di «previsto».

## 5. Stati proposti e proposte

- La catena realizza i blocchi B2–B5 del nucleo con le letture L1–L10: **verificato** sulle 25 prove dichiarate.
- Costo (ipotesi 6 del contratto): **sostenuto dai dati** solo su scene sintetiche; su immagini vere **non risolto**.
- K-014 e l'errore della maschera d'ombra: **non toccati** (nessun rumore qui); la catena dà i contatori e le griglie.
- **sviluppatore-1.** Al riaggancio far ripartire il filtro dalla misura, anche se tagliata, con R gonfiato di metà
  larghezza. *Previsione:* in P8 lo scarto massimo scende da 5,00 m a meno di 0,3 m. *La smentisce:* uno scarto
  maggiore, o un «si muove» sul pannello fermo di P6b.
- **sviluppatore-2.** Dichiarare all'avvio quante celle del campo ricevono almeno 3 pixel di suolo: sul pavimento
  vuoto, stessa posa, le libere sono 1270 a 160×120 (fx 84) contro 1630 a 848×480 (fx 424; i due campi non sono
  identici). *La smentisce:* un sensore a bassa risoluzione che riempie la griglia lo stesso.

## 6. Limiti e che cosa propongo dopo

Sensore fermo, pavimento piano, rollio nullo se la posa è nota; nessun rumore realistico provato (P21 è solo fumo:
rumore indipendente per pixel). Non ci sono B6–B8 (etichetta, decisione, voce, IMU), l'«occupato ricordato», i
filtri della camera. Soglie di punti (L1) e tolleranza del suolo sono mie: vanno rimisurate sui dati. Due oggetti
che si toccano diventano un gruppo e le identità saltano. Parametri mai provati oltre il fumo: `pendenti_ambito`,
`min_celle_altro_bordo`, `fattore_media_moto`, le curve «pessimista» e «torneo». **Dopo:** simulatore e dati veri
passano da `esegui.py --salva-griglie`; chi valida misura K-014 sulle griglie e la sensibilità a L1 e L8; lo sciame
decide su sviluppatore-1 prima di misurare la previsione (ipotesi 4).
