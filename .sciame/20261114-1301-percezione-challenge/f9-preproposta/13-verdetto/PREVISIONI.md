# Previsioni dell'arbitro (f9, verdetto sulla preproposta esterna)

## Blocco A — scritto alle 2026-11-14T16:21:09+01:00, dopo aver letto contratto, addendum e preproposta, PRIMA di aprire le dodici consegne

Indipendenza: condivido con i ruoli il contratto, l'addendum, la preproposta e il modello; non ho visto i loro file.

- A1. Leggendo la sola preproposta, mi aspetto che i ruoli trovino una lettura sbagliata del limite «sotto 1,1 m» (nel v0.5 è con ogni probabilità una distanza dal sensore o una zona non vista per geometria, non una fascia di quota). Misura: che cosa dice proposta_sciame.tex. Smentita: il tex parla di un'altezza di 1,1 m.
- A2. Mi aspetto che l'attacco 4 (tessuto nero e interferenza fra camera e sensori laterali) e l'attacco 5 nella parte «30 passaggi reali» risultino NON eseguibili oggi (niente hardware). Smentita: un ruolo porta una misura su sensore vero.
- A3. Mi aspetto che la somma delle ore del «taglio a 24 ore» della preproposta, secondo il pianificatore, superi le ore disponibili in 14 ore di orologio con 5 persone (70 ore-persona lorde). Smentita: somma dei moduli <= 70 ore-persona e catena in fila <= 14 ore.
- A4. Mi aspetto almeno una contraddizione numerica fra ruoli su S6 (probabilità d'intrusione) o su S3/S4 (pesi iniziali 0,8/0,2). Smentita: nessuna coppia di enunciati incompatibili.
- A5. Mi aspetto che i termini «ACAS», «TA/RA», «Runway Hold», «ABAR» siano giudicati prestiti impropri da almeno due ruoli. Smentita: un ruolo solo o nessuno.

## Blocco B — scritto alle 2026-11-14T16:23:20+01:00, dopo aver letto le dodici consegne (tutte presenti) e PRIMA di aprire un solo file di risultati o di lanciare uno script

Indipendenza del riconteggio: leggo i file di risultati scritti dai ruoli (stessi dati, stesso codice loro); il riconteggio trova solo errori di trascrizione fra file e consegna, non errori nei simulatori. Dove rilancio uno script di un ruolo (copiato nella mia cartella, mai eseguito nella sua), condivido il suo codice.

Cifre che riconto (soglia di smentita per ciascuna: la cifra nel file differisce da quella della consegna oltre l'arrotondamento dell'ultima cifra scritta):
- B1. architetto: 200 cambi in 10 minuti con isteresi di 2,5 s; 49,7 % dei cicli oltre 55 ms; 0,78 m² e 13,8 % (risultati_s1.txt).
- B2. tempo-reale: 17,5 cambi/min (variante B), 0,2 (variante D); picco all'arresto 0,240 m; 0,176 ms e 2,91 ms (risultati_selettore.txt, risultati_latenza.txt, risultati_banco_c.txt).
- B3. kalman: lato lontano L2-A 0,28 e 0,07 a 2 e 3 s; 760 su 1999; 65,9 % (tabelle_s3s4.txt, ris_s4_pesi.txt).
- B4. validazione: 84,4 % e 97,0 %; 234 su 291; 289 su 400; 0 su 3600 a «perso» (ris_10_*, ris_04, ris_16_falso1_W1_Nb, ris_03).
- B5. tracciamento: 381 su 392; 171 su 400; 386 su 400 (ris_pd09.txt, ris_pd09_pf002.txt).
- B6. esperto-dominio: 73,2 %; 44,8 ingressi al minuto; 0,16–0,18 (prove/risultati_*.txt).
- B7. nuvole-punti: 22 su 22, 53 su 53, 182 su 182; 28,6 / 1,11 / 23,4 ms (risultati_2.txt).
- B8. rovesciatore: 70,6 %, 99,3 %, 0,1 %; 24 cambi in 60 s (risultati_audit_imm.txt, risultati_conti.txt).
- B9. pianificatore: 96,5 ore-persona; 41,8 ore in fila; 0 su 4000 in 27 celle; tappe 9,1 / 14,0 / 17,0 / 22,7 / 27,5 / 32,0 (risultati_v2.txt).
- B10. avversario: 900 su 900; 289 su 384; 57,0 %; 60,4 %; 0,39 / 0,51 / 0,77 m (risultati_p1, p3, p6, p7 o altro).
- B11. lidar: 0,07 s; 6,5 % dei pixel (risultati_conti_s9.txt). interfacce: 39,3 %; 1,12 : 1 (risultati_interfacce.txt).
Previsione: almeno 9 blocchi su 11 tornano senza note; mi aspetto 1–3 note (denominatori, o cifre presenti solo nella consegna e non stampate nel file). Smentita: 3 o più cifre che non tornano.

Prove mie (previsioni scritte ora):
- B12. Riduzione del piano del pianificatore a 14 ore di orologio. Misura: copio piano_mc.py nella mia cartella, cambio SOLO le ore disponibili, e conto in quante estrazioni ogni tappa T1–T6 si chiude, con 3, 4 e 5 persone, a k = 1. Previsione: con 14 ore di costruzione e 5 persone, a k = 1, T1 (uscita su dati simulati) si chiude in più dell'80 % delle estrazioni; T2 in meno del 60 %; T3 (continuità sul simulatore) in meno del 20 %; T4–T6 in meno dell'1 %. Fra 3 e 5 persone T3 cambia di meno di 15 punti. Smentita: T3 oltre il 50 % a k = 1, oppure T1 sotto il 50 %. Se lo script non è parametrizzabile senza riscriverlo, lo dichiaro e uso la scala lineare k*(H) = k*(24 h)·H/13 [conto mio], marcata come estrapolazione.
- B13. Conto a mano sul corridoio di S8 (K fra «attesa a ogni cella buco» e «attesa al 2 % delle celle»): un oggetto largo 0,15 m a 2,9 m occupa circa 3 colonne da 1°; previsione: le celle che toglie in un corridoio di 454 celle sono meno di 9 (il 2 %), quindi la soglia al 2 % può non vederlo. Smentita: 9 celle o più.

### Esito di B12 (scritto alle 2026-11-14T16:26:16+01:00, dopo il lancio delle 16:25:32; file risultati_piano_14h.txt)
Regge in tutte le parti: con 5 persone, k = 1, T1 100 %; T2 35,0 % (senza sensore, su dati di ripiego) e 59,6 % (sensore dall'ora 0), 0,0–0,3 % se la mappa aspetta un sensore che arriva all'ora 5,5; T3 1,1–1,3 % entro le ore utili (7,3–7,7 % entro 14,0 h); T4–T6 0,0 %. Fra 3 e 5 persone T3 passa da 0,4–1,0 % a 1,1–1,3 %. Notato dopo (non previsto): nel grafo del pianificatore la mappa (N2) dipende dal sensore (N1), quindi nel caso «sensore dall'ora 5,5» la mappa vera si chiude a 19,3 h di mediana; è un effetto del grafo, non una misura.

## Blocco C — scritto alle 2026-11-14T16:26:16+01:00, prima del lancio di piano_14h_spezzato.py
- B14 (che cosa succede se il compito più lungo della catena della continuità, N5 «ciclo di vita + cuneo», 7 ore probabili su una persona sola, si spezza in due metà da 3,5 ore fatte da due persone: N5a il cuneo sulla mappa simulata, dopo i dati finti; N5b il ciclo di vita, dopo il Kalman; la previsione C1 dopo tutte e due). È un'ipotesi mia sulla divisibilità del compito, non verificata: il pianificatore la dichiara «non modellata». Previsione: con 5 persone e k = 1 la tappa T3 si chiude entro le ore utili fra il 20 e il 60 % delle estrazioni. Smentita: sotto il 10 % o sopra l'80 %.

### Esiti (scritti alle 2026-11-14T16:27:05+01:00)
- B14 regge: con N5 spezzato, 5 persone, k = 1, T3 entro le ore utili nel 42,7 % delle estrazioni (77,4 % entro 14,0 h); senza spezzare 1,1 % (risultati_piano_14h_spezzato.txt). Costo notato dopo: la mappa vera su dati di ripiego scende dal 35,0 al 18,2 %.
- B13 regge (conto a mano): 0,15 m a 2,9 m = 2,96° = 3 colonne da 1°; 0,15 m in distanza = 2 corone da 0,1 m; 6 celle, meno del 2 % di 454 (9,08 celle). Vale per un oggetto che non restituisce profondità (buco); un oggetto che la restituisce è «occupato» e fa scattare l'attesa per un'altra regola.
- B1–B11: nessuna cifra fuori dall'arrotondamento. Note: quattro, non «da una a tre» come previsto (la previsione sul numero delle note è smentita; quella «almeno 9 blocchi su 11 senza note» pure: sono 7). (a) pianificatore: la tabella delle tappe 9,1 / 14,0 / 17,0 / 22,7 / 27,5 / 32,0 sta in risultati_ablazione.txt (ordine «due corsie», 4 persone), non in risultati_v2.txt, che per 4 persone dà 8,0 / 12,2 / 21,2 / 22,4 / 27,4 / 31,9; (b) kalman: 65,9 % = 589 su 894 soste con ingresso a 1,0 m/s o più ancora nascoste a 3 s (ris_s4_pesi.txt), non su tutte le soste; (c) validazione: «0 su 48 279 fotogrammi» è un comportamento di una lettura (ris_04), anche gli altri blocchi stampano 0; (d) architetto: «la risalita non regge con 50 o 55 ms (11 e 100 cambi)» vale nel solo scenario B; nello scenario A è sempre 1.
- A1 regge (il sorgente scrive «fra 1,1 e 3 m» e «sotto 1,1 m gli ostacoli bassi non si vedono»: distanza; nove ruoli lo segnalano). A2 regge. A3 regge (96,5 ore-persona probabili; 41,8 ore in fila). A4 regge (orizzonte di S6: 3 s contro 1,0–1,2 s). A5 regge (esperto-dominio, interfacce, avversario; architetto per «AI» e «certified»).

### Chiusura (scritta alle 2026-11-14T16:37:07+01:00)
- Cifre ricontate in tutto: 46, negli undici blocchi B1–B11 (il 6,5 % dei pixel di lidar non è stato ricontato: è citato dalla consegna).
- Regola violata: un `git status` di sola lettura lanciato per errore nel controllo finale (uscita scartata, nessuna modifica). Dichiarato in testa al verdetto.
- File della cartella: VERDETTO_PREPROPOSTA.md (la consegna), PREVISIONI.md, piano_mc.py (copia identica di quello del pianificatore, md5 e3eca7ceb60b168a1612c1770df78abc), piano_14h.py, piano_14h_spezzato.py, risultati_piano_14h.txt, risultati_piano_14h_spezzato.txt.
