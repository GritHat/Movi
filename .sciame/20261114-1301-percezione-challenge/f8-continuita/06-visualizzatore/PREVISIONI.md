# Previsioni — sciame-visualizzatore, f8, corsia A

Scritte alle 2026-11-14T15:16:11+01:00 (`date -Is`), PRIMA di scrivere e lanciare ogni script. A quest'ora ho letto: la traccia, il contratto f8, gli addendum, `SOLUZIONE_V2.md`, `VERDETTO.md`, `TORNEO_parte3.md`, e righe scelte (con grep) di `MISURE_V2.md`, `SPECIALIZZAZIONE.md`, `MOTO_PROPRIO.md`, `proposta_sciame.tex`. Non ho ancora cercato fonti in rete.

Non è una previsione (i numeri li ho già letti): la quota dei cicli senza osservazione in cui il nucleo mostra una regione si ricava a mano da `MISURE_V2.md`, P4 (buio 1,07 s, «previsto» 0,47 s; in sosta «perso» 4,6–4,8 s). La riporto come conto, non come prova.

## PV-1 — il punto mostrato, scena «si ferma dietro» (`punto_mostrato.py`, modello mio, senza rumore)
Modello: sensore in (0,0); pannello largo 1 m; filtro a velocità costante con q = 0,2 m²/s³ lasciato in sola previsione dall'ingresso in ombra; 15 cicli al secondo. Geometria T (torneo: pannello a 2 m, persona a 4 m, portata 6 m, campo ±43,5°) e geometria D (demo: pannello a 1,9 m, persona a 2,3 m, griglia fino a 3 m). Persona a 1,0 / 1,25 / 1,5 m/s che si ferma a 1/4, 1/2, 3/4 dell'ombra per 3 s e poi prosegue (9 casi per geometria). Tre candidati per «la posizione più probabile» da disegnare: (a) la media del filtro; (b) la media proiettata sul punto più vicino del cuneo d'ombra; (c) il baricentro della gaussiana troncata al cuneo (celle di 5 cm).
- **PV-1a.** Con (a), nella geometria T, il punto sta su suolo visto libero in almeno il 40 % dei cicli senza osservazione (media dei 9 casi). **Smentita:** meno del 20 %. (Atteso circa 45–65 %.)
- **PV-1b.** Con (b), il punto resta parcheggiato a meno di 10 cm dal bordo visibile del cuneo (il posto dove la persona si vedrebbe) in almeno il 40 % dei cicli. **Smentita:** meno del 20 %.
- **PV-1c.** Con (c): 0 cicli su suolo visto libero (controllo per costruzione, non dato); nessun passo fra due cicli oltre 2·v·dt (13–20 cm) e nessun passo all'indietro, lungo il verso del moto, oltre 5 cm. **Smentita:** un solo ciclo che viola una delle tre. Non sono sicuro del passo all'indietro: quando la media esce dal cuneo, il baricentro potrebbe arretrare.
- **PV-1d.** Errore del punto rispetto alla persona vera a 3 s dall'ingresso (media dei 9 casi, geometria T): (c) minore di (a). **Smentita:** (c) ≥ (a).
- **PV-1e.** Scena «prosegue» (senza sosta, stesse velocità): salto a schermo alla ricomparsa. Con la regola del nucleo (dopo «perso» non c'è alcun punto) l'ultimo punto mostrato dista dalla ricomparsa più di 0,5 m in tutte e due le geometrie; con (c) meno di 0,3 m. **Smentita:** una delle due non vale in un caso. La durata del «previsto» del nucleo la calcolo con la sua regola (cerchio al 95 % ritagliato < metà dell'area del cuneo in griglia): NON la prendo dai file.

## PV-2 — il tabellone dal vivo (`tabellone.py`, conto binomiale esatto)
- **PV-2a.** Con 9 ricomparse su 10 dentro la regione dichiarata, l'intervallo esatto al 95 % (Clopper-Pearson) è largo più di 40 punti. **Smentita:** ≤ 40.
- **PV-2b.** Una regione «al 90 %» che in realtà copre l'80 % mostra almeno 9 su 10 in più del 30 % delle demo; una che copre il 70 %, in più del 10 %. **Smentita:** una delle due sotto soglia.
- **PV-2c.** Per distinguere 90 % da 80 % con errore di prima e seconda specie ≤ 10 % servono più di 60 transiti (conto esatto, non ancora fatto: atteso 80–140). **Smentita:** ≤ 60.
Conseguenza di progetto se reggono: il tabellone non può dire «tarato» con i soli transiti dal vivo; mostra il conto dal vivo con l'intervallo, accanto al conto sulle registrazioni.

## PV-3 — lettura in bianco e nero (`fotogrammi.svg` → PNG a 1 bit)
- **PV-3a.** Reso con `rsvg-convert` e portato a 1 bit (soglia al 50 %), i quattro segni della legenda (osservato, previsto entro soglia, previsto oltre soglia, possibile presenza) restano diversi fra loro per forma o tratto. **Smentita:** due segni indistinguibili nell'immagine a 1 bit. Limite: il giudice sono io, autore del disegno (stesso autore, stesso modello): vale solo come controllo che il file si rende e che nessuna distinzione dipende dal colore; la leggibilità per un daltonico o un giurato vero resta «non verificata».

---

# Esiti (scritti alle 2026-11-14T15:22:48+01:00, dopo le prove)

Lanci: `punto_mostrato.py` alle 15:17:11 (0,70 s), `tabellone.py` alle 15:17:42, `fotogrammi.py` alle 15:20:40 e, dopo la correzione del disegno, alle 15:21:18.

| Previsione | Esito | Numeri (file) |
|---|---|---|
| PV-1a | **regge** | geometria T: 48,0 % dei cicli su suolo visto libero (41,5–54,7 %); geometria D: 26,5 % (`risultati_punto_mostrato.txt`) |
| PV-1b | **regge** | 68,6 % (T) e 79,5 % (D) dei cicli sul bordo visibile |
| PV-1c | **regge** | 0 casi su 18 violano; passo massimo = v·dt (6,7–10,0 cm); passo all'indietro massimo 1,1 cm; 0 cicli su libero (per costruzione) |
| PV-1d | **regge** in media | T: 0,62 m contro 2,75 m; D: 0,33 m contro 3,14 m. **[dopo]** chi si ferma a 1/4 dell'ombra è previsto meglio da «fermo all'ultima posizione» (T: 0,50 m contro 0,87–1,10; D: 0,30 contro 0,49–0,57) |
| PV-1e, prima metà | **smentita nel mio modello** | salto del nucleo > 0,5 m solo a 1,0 m/s (0,53 e 0,54 m); 0,00–0,13 m negli altri 4 casi. Causa: la mia emulazione della regola «metà del cuneo» dà un «previsto» di 0,67–0,87 s (D), più lungo dei 0,40–0,53 s misurati dalla validazione; a 1,5 m/s nel mio modello la soglia non scatta mai (il cerchio esce dal cuneo prima di coprirne metà). L'emulazione non è fedele: non la uso per giudicare il nucleo |
| PV-1e, seconda metà | **smentita** | salto con (c): 0,61 / 0,46 / 0,36 m (T) e 0,32 / 0,23 / 0,18 m (D): sopra 0,3 m in 4 casi su 6. È 0,31–0,34 volte il raggio al 95 % in tutti e sei |
| PV-2a | **regge** | 9 su 10: 55,5–99,7 %, largo 44,2 punti (`risultati_tabellone.txt`) |
| PV-2b | **regge** | 37,6 % (copertura vera 0,80) e 14,9 % (0,70) |
| PV-2c | **regge** | 86 transiti, soglia 74 (contro 0,80); 25 transiti, soglia 21 (contro 0,70) |
| PV-3a | **regge alla lettera, con un difetto trovato** | nella prima resa (`fotogrammi_v1_1bit.png`) i quattro segni restano diversi, ma le righe rade da 0,7 px spariscono e «possibile presenza» diventa uguale all'ombra senza traccia (un quinto segno che non avevo messo nella previsione). Corretto a 1,5 px (`fotogrammi_1bit.png`). Giudice: io |

**Notato dopo, non previsto [dopo]:** (1) la regione al 90 % della previsione troncata al cuneo è limitata e cresce in modo monotono: 4 % del cuneo a 0,2 s, 39 % a 0,8 s, 52 % a 1,53 s, 84 % a 4 s; larghezza equivalente da 0,24 a 1,07 m (`risultati_fotogrammi.txt`); (2) il cerchio nominale al 95 % ritagliato sul cuneo contiene il 94,3–100 % della massa troncata: nel mio modello il livello dichiarato dal nucleo non è tradito dal ritaglio; (3) costo indicativo del baricentro e della regione in Python puro: l'intero `punto_mostrato.py` (circa 1300 cicli su 548–3132 celle) gira in 0,70 s.
