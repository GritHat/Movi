# PREVISIONI (sciame-dati, f15/01-dati)

Scritte alle 2026-11-15T00:01:41+01:00, PRIMA di scaricare o misurare alcunché. Nessun dato aperto finora.

| id | previsione | misura | soglia di smentita |
|---|---|---|---|
| dati-P1 | Per tutte e quattro le classi (aerei, droni, auto, treni) si trovano dati reali scaricabili per https senza credenziali, entro 15 min e 6 GB | numero di tratti convertiti per classe | smentita per la classe se < 30 tratti |
| dati-P2 | Aerei (ADS-B, avvicinamento/decollo sotto 3000 m): mediana della velocità al suolo fra 60 e 120 m/s; 95° percentile dell'accelerazione longitudinale < 2 m/s^2; 95° percentile della velocità di virata < 3 gradi/s (virata standard) | statistiche.json | smentita se un valore esce dall'intervallo |
| dati-P3 | Multirotori (registri di volo reali): mediana della velocità < 15 m/s, 95° percentile < 25 m/s; 95° percentile dell'accelerazione < 5 m/s^2 | statistiche.json | smentita se un valore esce |
| dati-P4 | Auto (traiettorie dall'alto, autostrada/arteria urbana): mediana fra 5 e 35 m/s; 95° percentile di |a| < 3,4 m/s^2 (decelerazione di progetto in classi.json, fonte F4) | statistiche.json | smentita se esce |
| dati-P5 | Treni (posizioni GPS pubbliche): 95° percentile della velocità < 61 m/s (220 km/h); 95° percentile di |a| < 1,5 m/s^2 (frenata d'emergenza, fonte F7 di classi.json) | statistiche.json | smentita se esce |
| dati-P6 | La frequenza di campionamento dei dati pubblici di aerei e treni è >= 1 Hz | passo mediano in s | smentita se il passo mediano > 1 s (me l'aspetto smentita per i treni: ipotesi 15 s) |

Esiti possibili: regge, smentita, non risolta. Gli esiti si scrivono in fondo, dopo le misure, senza toccare la tabella.

## Esiti (scritti alle 2026-11-15T00:15:57+01:00, DOPO le misure; prova: `statistiche.json`, uscita di `converti.py statistiche`)

| id | esito | numeri |
|---|---|---|
| dati-P1 | **regge** per le quattro classi | aerei 193 tratti, droni 243, auto 157, treni 111 (704 scene, 0 errori di formato). Notato dopo: per sottotipo la soglia di 30 NON è raggiunta da rullaggio (19), avvicinamento non elaborato (9), elicottero (4) |
| dati-P2 | **smentita in parte** | mediana: cattura dal vivo avvicinamento 88,8 e decollo 83,0 m/s (dentro); Zenodo decollo 133,7 m/s (fuori). \|a\| p95: dal vivo 1,27 e 1,97 (dentro), Zenodo 2,69 e 3,27 (fuori). Virata p95: dal vivo 3,21 e 3,16 gradi/s (fuori di poco), Zenodo 1,86 e 2,21 (dentro) |
| dati-P3 | **regge** | multirotore: mediana 2,71, p95 9,74 m/s; \|a\| p95 2,13 m/s^2 (196 voli) |
| dati-P4 | **regge** | auto: mediana 10,61 m/s; \|a\| p95 1,44 m/s^2 (154 tratti) |
| dati-P5 | **regge** | treni: v p95 43,5 m/s; \|a\| p95 0,59 m/s^2 (111 tratti) |
| dati-P6 | **smentita** | passo mediano: aerei dal vivo 3,1-5,1 s; treni 3,0 s (meglio dei 15 s che ipotizzavo). Solo gli insiemi già interpolati dalla fonte (Zenodo, TrajAir) sono a 1 Hz |
