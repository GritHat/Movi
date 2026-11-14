# Previsioni di `sciame-nuvole-punti` (f7, corsia A) — scritte PRIMA di ogni prova

Ora di scrittura: **2026-11-14T15:09:32+01:00** (`date -Is`). A quest'ora non esiste nessun codice mio e nessun lancio: esistono solo le letture di `CONTRATTO_ESTENSIONE.md`, `promptMare.txt`, `SOLUZIONE_V2.md`, `comune_f4.py` (righe 1–75) e i conti a mano qui sotto.

## Il modello della prova (dichiarato prima)

- Sensore del nucleo: a 1,2 m, inclinato di 15° in basso, 87° × 58°, immagine 848 × 480 a foro stenopeico, profondità senza rumore (più un lancio con rumore nominale σ = 0,00375·z² m, seme fisso).
- Stanza: pavimento piano, parete di fondo a 4,5 m (ogni raggio ha un ritorno valido).
- Volume giudicato: settore di 87° fino a 3 m in pianta, quote 0–2 m (13,7 m³), campionato a 2,5 cm.
- Verità: visibilità analitica punto per punto (segmento sensore–punto contro i solidi; campo visivo). Quattro classi vere: visto libero, nascosto, fuori campo, dentro un solido.
- Scene: **S1** cassa 0,8 × 0,4 × 1,0 m a 1,5–1,9 m, con dietro un adulto in piedi (cilindro alto 1,7 m) oppure un soggetto accovacciato (0,8 m); **S2a** trave sospesa 1,7–1,9 m di quota a 1,5–1,7 m di distanza (sopra il campo visivo); **S2b** la stessa trave a 2,2–2,4 m (visibile) con un adulto a 2,7 m; **S3** (aggiunta mia) pedana alta 0,4 m a 1,3–1,7 m con un oggetto basso dietro: conto a mano, l'ombra al suolo finisce a 1,7·1,2/0,8 = 2,55 m. Conto a mano per S1: l'ombra al suolo della cassa arriva a 6 × 1,9 = 11,4 m, cioè OLTRE la portata: in S1 il difetto del cuneo non è al suolo ma in quota (sopra la linea di vista).
- Rappresentazioni: **N-L** nucleo alla lettera (griglia polare 1° × 0,1 m; oltre il primo ritorno tutto «in ombra» fino a 3 m; lo stato vale per la colonna 0–2 m); **N-G** nucleo con «suolo visto vince» cella per cella; **B4, B8** fasce di quota (4 da 0,5 m, 8 da 0,25 m) per cella polare, regola prudente (ombra batte libero; libero solo se la cella è tutta nel campo); **V5, V10** voxel cartesiani da 5 e 10 cm con DDA, regola «alla OctoMap» (**-O**: attraversato = libero) e regola prudente (**-C**: ombra batte libero, cella tutta nel campo); **Q** interrogazione nello spazio dell'immagine senza memoria (minimo e massimo 3 × 3, margine 2 cm); **P** «profilo» (per cella polare due numeri: quota sotto cui non si vede, quota fino a cui si vede), ricavato da Q.
- Misure: «falso libero» = volume dichiarato libero che non è visto (in litri e in % del non visto); «falso nascosto» = volume dichiarato in ombra che è visto (in % del dichiarato in ombra e del visto); «resa» = quota del visto dichiarata libera; quota del corpo del soggetto (o della trave) dentro una regione dichiarata libera.

## Previsioni, con la soglia che le smentisce

| # | Previsione | Smentita se |
|---|---|---|
| np-P1 | S1, N-L: almeno il 30 % del volume che il nucleo dichiara «in ombra» è in realtà visto (atteso 35–60 %). | < 30 % |
| np-P2 | S1, soggetto accovacciato del tutto nascosto (0 pixel): in N-L, N-G, B4, B8, V5-C, V10-C, Q, P la quota del suo corpo in regione «libera» è ≤ 1 % in ogni posizione. Per V10-O mi aspetto invece > 0 in almeno una posizione (bordo dell'ombra), sotto il 15 %. | una rappresentazione prudente > 1 %; oppure V10-O sempre 0 (allora la regola -C non serve) |
| np-P3 | S3, N-L: almeno l'80 % del volume dichiarato «in ombra» è visto (cuneo fino al bordo contro ombra che finisce a 2,55 m). | < 60 % |
| np-P4 | S2a (trave non vista): N-L e N-G mettono ≥ 90 % del volume della trave in colonne «libero»; B4, B8, V-C, V-O, Q, P ≤ 1 %. Inoltre ≥ 8 % del volume che il nucleo dichiara libero (colonna 0–2 m) non è visto (sta sopra il campo). | trave < 90 % per il nucleo; una 3D > 1 %; quota < 5 % |
| np-P5 | S2b (trave vista, adulto dietro in pianta): N-L dichiara «in ombra» la cella del centro dell'adulto, che ha invece > 1000 pixel di ritorno; ≥ 80 % dell'ombra dichiarata da N-L è vista. | cella «occupato» in N-L; < 60 % |
| np-P6 | Costo su un filo: DDA a piena risoluzione (407 040 raggi) su V5 fa > 20 milioni di passi e sta fra 50 e 500 ms per fotogramma (cioè oltre i 66 ms dei 15 Hz); l'aggiornamento proiettivo dei 576 000 centri di V5 e il profilo P stanno sotto 10 ms. | DDA < 66 ms; proiettivo o P > 66 ms |
| np-P7 | Q, senza rumore: falso libero ≤ 0,1 % del non visto, falso nascosto ≤ 0,1 % del visto, resa ≥ 90 %, in tutte le scene. | falso libero > 0,5 % |
| np-P8 | LA PREVISIONE CHE DECIDE: sulle misure di sicurezza (soggetto nascosto in «libero», trave in «libero») B8, P e Q danno lo stesso esito di V5-C (tutti ≤ 1 %); la resa di P è ≥ 0,8 volte quella di V5-C in S1 e S3. Cioè: il voxel 3D non chiude nessun buco che l'alternativa economica lasci aperto. | V5-C ≤ 1 % e P o B8 > 1 % in una scena; resa di P < 0,6 × V5-C |
| np-P9 | Con rumore nominale e scavo fino al punto misurato (senza troncamento), V5-O e V5-C in un fotogramma mettono «libero» dentro un solido (> 0 punti del corpo); con troncamento a 3σ, ≤ 0,1 %. | 0 punti senza troncamento (il troncamento non serve) |

## Che cosa queste prove NON decidono (scritto prima)

Un fotogramma solo: niente memoria nel tempo, niente log-odds, niente decadimento. Niente piattaforma in moto, niente errore di posa. Niente vetro (per costruzione: la lastra dà profondità sbagliata a ogni rappresentazione). Niente sparsità (la classificazione non ne dipende: un voxel non toccato è «sconosciuto»). Il costo è misurato su questa macchina, un filo, C con `-O2`: è un ordine di grandezza, non il prototipo. La verità e le rappresentazioni condividono l'autore, il modello geometrico della camera e i solidi; non condividono il codice di visibilità (analitico per la verità, immagine di profondità per le rappresentazioni).
