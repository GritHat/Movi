# Previsioni dell'arbitro sul passo d'integrazione f12

Scritte alle 2026-11-14T18:56:12+01:00 (`date -Is`), dopo aver letto solo `CONTRATTO_INTEGRAZIONE.md` e il mio verdetto VD (`f10-dati/23-verdetto/VERDETTO_DATI.md`), e prima di aprire la versione 3, le prove, le critiche e i file dei risultati di f12.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| B1 | Le cifre della prova d'insieme (C-C) che adotterò tornano dai file `02-prova-insieme/ris/` con un programma mio | conteggi ricontati contro quelli scritti in `PROVA_INSIEME.md` | smentita se anche un solo conteggio adottato differisce |
| B2 | Nella prova d'insieme almeno una soglia di C-C cade (non tutte e quattro reggono in tutto il dominio) | soglie di C-C, cella per cella | smentita se tutte le soglie reggono in ogni configurazione provata |
| B3 | La prova sul «libero» (C-D) dà 0 celle libere con un ostacolo sotto, ma la mediana della distanza libera non raggiunge 2,7 m in tutte le letture col 5 % di buchi sparsi | `03-libero/riepilogo_banco*.txt` | smentita se ci sono celle libere false, oppure se la mediana è almeno 2,7 m in tutte le letture sicure |
| B4 | La «stessa identità al ritorno» corretta (F-401, F-402, F-408, F-409) NON raggiunge 28 su 30 a entrambe le risoluzioni insieme alla scatola 9 su 10, oppure la controprova trova almeno un controesempio che resta | `06-identita/risultati`, `07-controprova-identita/risultati` | smentita se il criterio di VD regge a 424 e a 848 pixel e la controprova non trova niente |
| B5 | Il controllo di completezza (C-A) trova almeno una correzione obbligata mancante o messa nel punto sbagliato nella prima versione 3 | `11-completezza/COMPLETEZZA.md` e `20-finale/TABELLA_CORREZIONI.md` | smentita se l'elenco indipendente non trova mancanze |
| B6 | Le due simulazioni del piano (autore e secondo ruolo) danno probabilità diverse di oltre 10 punti per il minimo dimostrabile in 14 ore | `21-piano-finale`, `12-piano-rifatto` | smentita se differiscono di 10 punti o meno |
| B7 | Almeno una contraddizione K# resta aperta su una conclusione adottata, e si può chiudere solo riformulando la conclusione nel suo dominio | elenco K# dopo la lettura | smentita se nessuna K# aperta tocca una conclusione adottata |
| B8 | Esito della chiusura: «chiuso» solo con H-012 provata «in simulazione, a sensore fermo» e con conclusioni riformulate nel dominio; non prevedo un «chiuso» senza riformulazioni | chiusura | smentita se chiudo senza riformulare nulla, o se non chiudo |

Esiti: in coda, dopo le prove.

## Esiti (scritti alle 2026-11-14T19:09:34+01:00, dopo i riconteggi; programmi `riconta_arbitro.py`, `riconta2…5_arbitro.py`, uscite `riconteggio*.txt`)

| # | Esito | Prova |
|---|---|---|
| B1 | **regge** | 0 vuoti su 23 402; scoperti 24 (17 + 7) e 928 (680 + 248); estraneo 3027/3041, 3493/3616, 3239/3546; riaggancio 10 711/10 757, 9 228/9 240, 6 772/6 967 (sui file `b_*_percorso`); celle peggiori 0,955, 0,921, 0,936, 0,899, 0,882: coincidono con `PROVA_INSIEME.md`. Non ricontati: 29 su 95 399 e le righe di K-215 |
| B2 | **regge** | cadono la soglia sugli scoperti, la regione col pannello da 1 m, l'ombra stretta senza c3, l'estraneo con c1 |
| B3 | **regge** | `nuvole-1` (PR4): 0 fotogrammi con violazione su 9 000, due lanci; mediana 3,0 m a errore 0 e 2,4 m a +0,5° con k = 0,010 (2,2 m con chiazze al 5 %) |
| B4 | **regge** | replica: 30, 30, 28 su 30 a 424 px e 29, 30, 27 su 30 a 848 px; fuori dominio 0, 2, 0 su 10 e 6 su 10 a +0,5° |
| B5 | **regge** | 2 voci mancanti e 15 non conformi su 149 nella prima stesura (`COMPLETEZZA.md`); nella finale restano K-017 e il decimo addendum fuori dal testo |
| B6 | **regge** | 0,428 contro 0,039: 39 punti (`21-piano-finale/risultati_variante_c2.txt`) |
| B7 | **regge** | K-505, K-219 e K-016, K-215, K-014, K-015: conclusioni riformulate nel dominio (verdetto, §4) |
| B8 | **regge** | «Esito: chiuso» con sei riformulazioni scritte (`f5/CHIUSURA.md`, §2) |

Otto su otto reggono: le previsioni non erano cieche rispetto al contratto e al mio verdetto sui dati, e vanno lette come un controllo debole. **Notato dopo, non previsto:** (1) su profondità simulata, a persona nascosta, la traccia è «perso» in 2 983 fotogrammi su 4 552 (`riconteggio4.txt`); (2) l'avviso acceso dopo la rimozione del pannello c'è anche nella catena di partenza, 10 su 10 (`riconteggio2.txt`, B); (3) pannello «in movimento» in 7 passaggi su 10 nel tipo `a12z` della replica (`riconteggio3.txt`); (4) la prova d'ingresso del rumore, com'è scritta, non può passare coi gruppi del nucleo (lettura, non eseguita).
