# Previsioni di `sciame-kalman` — f8, corsia A

Scritte alle **2026-11-14T15:18:26+01:00** (`date -Is`), prima di scrivere e lanciare `sim_cont.py`. Nessun numero della simulazione è noto a quest'ora; conosco i numeri del torneo (`f2/04-torneo/TORNEO_parte2.md`, `TORNEO_parte3.md`) e della mia consegna di f1.

## Che cosa si misura

15 Hz, rumore isotropo di 5 cm, 2 s visibili (30 misure), poi buio. Orizzonti 0,5 / 1 / 2 / 3 / 5 s dall'ultima misura. Per ogni predittore: quota dei casi in cui la posizione VERA sta nella regione dichiarata al 50 % e al 90 %, e raggio equivalente √(area/π). Tre insiemi di semi distinti: taratura, scelta, prova.

Generatori: G0 mio (prosegue 40 %, rallenta 10 %, si ferma 15 %, sosta e riparte 5 %, torna 10 %, svolta 15 %, accelera 5 %; inizio manovra uniforme fra −0,3 e 2,5 s dall'ultima misura); G1 copia di `g1()` dell'avversario e G2 copia di `truth()` del tracciamento (da `f2/04-torneo/torneo_parte2.py`): autori diversi da me.

Predittori: A0 attuale (velocità quasi costante, q = 0,2, cerchio del chi quadrato); A0cap (A0 ∩ disco v_max·t); A1 (stesso centro, raggio = quantile empirico per orizzonte, cioè gonfiamento tarato / previsione conforme); A2 (come A1, punteggio scalato con velocità × tempo); B0 (velocità che decade, Ornstein-Uhlenbeck, τ e q scelti sulla verosimiglianza della taratura); B1 (B0 con raggio conforme); C1 (ellisse lungo la traccia: centro arretrato e semiassi ∝ velocità × tempo, tarata per orizzonte); D0 (miscela di gaussiane a regimi: prosegue, si ferma, torna, svolta; regione a densità più alta, nominale); D1 (D0 con livello conforme); E0 (la stessa miscela collassata in una gaussiana sola, come la mostrerebbe un IMM).

**Regola di scelta delle «due varianti migliori», fissata ora:** sull'insieme di scelta, fra le varianti diverse da A0 con copertura complessiva entro ± 0,03 dal nominale a tutti e cinque gli orizzonti e ai due livelli, le due con il raggio equivalente medio al 90 % (media sui cinque orizzonti) più piccolo. I numeri della consegna vengono dall'insieme di prova.

## Previsioni (esito: regge / smentita / non risolta)

- **K8-1 (A0, complesso).** Copertura al 90 % su G0: fra 0,84 e 0,93 a 1–3 s; ≥ 0,93 a 5 s (il raggio cresce come t^1,5, il pedone no). Al 50 %: ≥ 0,62 a 5 s. **Smentita se** A0 sta entro ± 0,03 dal nominale a tutti gli orizzonti e ai due livelli (allora la taratura attuale va bene e la mia critica cade).
- **K8-2 (A0, per comportamento).** A 2–3 s, al 90 %: «prosegue» ≥ 0,97 (regione più larga del necessario); «torna» fra 0,40 e 0,75. **Smentita se** «torna» ≥ 0,85 o «prosegue» ≤ 0,93.
- **K8-3 (A1, stessa popolazione).** Copertura complessiva entro ± 0,03 dal nominale a ogni orizzonte e livello; ma «torna» al 90 % resta < 0,80 a 2–3 s (la previsione conforme garantisce la media, non il comportamento). **Smentita se** scarto > 0,03 nel complesso, o «torna» ≥ 0,85.
- **K8-4 (A1, altra popolazione).** Tarata su G0 e provata su G1 e G2, la copertura al 90 % esce da ± 0,03 in almeno un orizzonte per almeno uno dei due generatori (scarto atteso fra 0,03 e 0,15). **Smentita se** resta entro ± 0,03 ovunque.
- **K8-5 (miscela, D1).** Al 90 %: raggio equivalente ≤ 0,75 volte quello di A1 a 3 s e a 5 s, con copertura complessiva entro ± 0,04; «torna» ≥ 0,80 a 2–3 s. **Smentita se** il rapporto dei raggi > 0,90 o «torna» < 0,70.
- **K8-6 (velocità che decade, B0).** τ scelto fra 1,5 e 6 s; raggio al 90 % a 5 s ≤ 0,7 volte quello di A0; errore quadratico medio del centro minore di quello di A0 a 3 e 5 s nel complesso (5–25 % in meno) e maggiore sul solo «prosegue». **Smentita se** τ scelto ≥ 10 s (cioè «nessun decadimento») o se l'errore non scende.
- **K8-7 (efficacia).** Il centro a velocità costante batte «fermo all'ultima posizione» a tutti gli orizzonti nel complesso (rapporto degli errori quadratici medi 0,3–0,8 fino a 2 s; 0,6–1,0 a 5 s). **Smentita se** «fermo» vince a un orizzonte.
- **K8-8 (limite fisico).** Intersecare A0 con il disco v_max·t + 0,1 m (v_max = 2,5 m/s) centrato sull'ultima posizione: copertura invariata (differenza ≤ 0,002), area al 90 % ridotta meno del 5 % fino a 2 s e del 10–40 % a 5 s. **Smentita se** la copertura scende di più o se l'area a 5 s scende meno del 5 %.
- **K8-9 (quanti dati).** Raggio conforme al 90 % a 2 s tarato su n passaggi estratti dalla taratura (300 estrazioni): l'intervallo 5–95 % della copertura di prova è largo ≥ 0,12 con n = 30 e ≤ 0,06 con n = 300. **Smentita se** con n = 30 è largo < 0,08.
- **K8-10 (sensore in moto).** Errore di posa non modellato sull'incremento (deriva d'imbardata 1°/s a 10 m di distanza; errore di velocità propria 0,1 m/s): la copertura di A1 al 90 % scende di ≤ 0,02 a ogni orizzonte, perché l'incertezza del moto del soggetto domina. **Smentita se** scende di più di 0,03 a un orizzonte.

## Che cosa condivide la prova con ciò che prova

G0 e i predittori hanno lo stesso autore (io) e lo stesso modello linguistico: per questo K8-4 usa G1 e G2, scritti da altri ruoli. Tutti i generatori sono pedoni puntiformi simulati, senza geometria dell'ombra, senza rilevamenti mancati, con rumore gaussiano isotropo di 5 cm ipotizzato. Nessun pedone vero, nessun sensore vero.

---

## Seconda serie, scritta alle 2026-11-14T15:24:19+01:00 (`date -Is`, riga in fondo), DOPO aver visto `risultati_main.txt` e PRIMA di scrivere i modi `extra` e `ombra`

Ciò che ho visto e che mi porta a queste prove: nessuna variante tarata «in media» copre al 90 % chi svolta (0,51–0,77 a 2–5 s) né chi torna; la regione al 90 % a 5 s ha raggio equivalente 5–7 m con ogni variante. Le due prove che seguono non erano nel piano iniziale.

- **K8-11 (taratura sul comportamento peggiore).** Scelgo la soglia in modo che, sulla taratura, OGNI comportamento con almeno 100 casi sia coperto al 90 % (il massimo dei quantili conformi per comportamento). Previsto, sulla prova G0: copertura minima per comportamento ≥ 0,86 a ogni orizzonte; copertura complessiva 0,95–0,99; raggio equivalente della miscela così tarata fra 1,3 e 2 volte quello di D1 a 2–5 s; il cerchio centrato sul punto a velocità costante così tarato ha raggio ≥ 1,3 volte quello della miscela a 3 e 5 s. **Smentita se** il minimo per comportamento scende sotto 0,84, o se il rapporto miscela/D1 supera 2,5 (regione inutile).
- **K8-12 (evidenza negativa: condizionato a «ancora nascosto»).** Ombra schematica nel riferimento della traccia: striscia lunga W = 2 m dal punto dell'ultima misura (larga 3 m: da −1 a +2 m di lato); chi ne esce è rivisto e non conta. Fra i casi di prova ancora dentro la striscia all'orizzonte h: (i) il cerchio di A0 ritagliato sulla striscia (la regola del nucleo, qui al 90 % e al 50 %) contiene il vero in ≤ 0,75 dei casi a 2 s al 90 % e in ≤ 0,35 al 50 %; a 5 s ≥ 0,95 ma copre ≥ 90 % della striscia; (ii) la stessa gaussiana troncata sulla striscia e rinormalizzata (regione a densità più alta della massa rimasta) ≥ 0,85 a 2–3 s; (iii) la miscela troncata e rinormalizzata fra 0,80 e 0,97 a 2–5 s, con area ≤ 70 % della striscia a 2–3 s. **Smentita se** il cerchio ritagliato tiene ≥ 0,85 a 2 s e a 3 s (allora il ritaglio semplice basta), o se la miscela troncata scende sotto 0,75.
2026-11-14T15:24:19+01:00

## Terza serie, scritta alle 2026-11-14T15:26:35+01:00, dopo aver visto `risultati_ombra.txt` (solo G0) e prima di rifare la prova d'ombra sui generatori degli altri autori

- **K8-13 (evidenza negativa su G1 e G2).** Stessa striscia (W = 2 m), miscela con i parametri tarati su G0. Previsto: miscela troncata e rinormalizzata al 90 % fra 0,85 e 0,99 a 2, 3 e 5 s su G1, e ≥ 0,80 su G2; cerchio di A0 ritagliato ≤ 0,88 ad almeno due dei tre orizzonti su ciascun generatore. **Smentita se** la miscela troncata scende sotto 0,80 su G1 o sotto 0,75 su G2, o se il cerchio ritagliato tiene ≥ 0,88 ovunque.

## Esiti (scritti alle 2026-11-14T15:30:16+01:00, dopo tutte le prove; i numeri sono nei file `risultati_*.txt`)

| Previsione | Esito | Numero |
|---|---|---|
| K8-1 | smentita in parte | A0 al 90 %: 0,962 / 0,939 / 0,904 / 0,890 / 0,884 (a 5 s previsto ≥ 0,93; a 1 s 0,939 sopra il tetto di 0,93); al 50 % a 5 s 0,633 (regge). Il falsificatore non scatta: al 50 % A0 copre 0,63–0,83 |
| K8-2 | regge sul falsificatore | prosegue 1,000; torna 0,765 (2 s, fuori di 0,015 dall'intervallo) e 0,647 (3 s) |
| K8-3 | regge | A1: 0,893–0,905 e 0,494–0,509; torna 0,747 / 0,664 |
| K8-4 | regge | G1: 0,953–0,983; G2: 0,859–0,950 |
| K8-5 | regge sul falsificatore | rapporto dei raggi 0,71 a 3 s e a 5 s; torna 0,829 (2 s) e 0,791 (3 s, sotto lo 0,80 previsto). Notato dopo: svolta 0,611 / 0,539 / 0,513 |
| K8-6 | smentita in parte | τ = 6 s, q = 0,2; raggio a 5 s 4,89 / 6,59 = 0,74 (previsto ≤ 0,7); errore del centro −10 / −14 / −18 % nel complesso, +20 / +35 / +54 % su «prosegue» (regge) |
| K8-7 | regge | su G0, G1, G2 a ogni orizzonte. Notato dopo: con il 40 % di ritorni a 5 s vince «fermo» (4,39 contro 5,70 m) |
| K8-8 | regge sul falsificatore | copertura identica; area −1 % a 2 s, −6 % a 5 s (previsto −10…40 %) |
| K8-9 | regge sul falsificatore | n = 30: larghezza 0,157–0,177; n = 300: 0,051–0,065 (previsto ≤ 0,06) |
| K8-10 | **smentita** | 1°/s a 10 m: 0,902 → 0,764 a 0,5 s e 0,898 → 0,820 a 1 s; con la somma in quadratura 0,889–0,905 |
| K8-11 | regge | minimo per comportamento 0,895–0,934; complesso 0,970–0,982; rapporto con D1 1,72 / 1,49 / 1,33; cerchio/miscela 1,51 e 1,65 |
| K8-12 | smentita in parte | cerchio ritagliato 0,827 (2 s; previsto ≤ 0,75), 0,562 al 50 % (previsto ≤ 0,35), 0,812 a 5 s con l'80 % della striscia (previsto ≥ 0,95 e ≥ 90 %); gaussiana troncata 0,842 / 0,828 (previsto ≥ 0,85); miscela troncata 0,940 / 0,973 / 0,951 con il 39–51 % (regge, 0,973 sopra il tetto di 0,97). Il falsificatore (cerchio ≥ 0,85 a 2 e 3 s) non scatta |
| K8-13 | smentita in parte | miscela troncata su G1: 0,953 / 0,935 / **0,785** (n = 130 a 5 s); su G2: 0,855 / 0,909 / 0,912; cerchio ritagliato G1 0,913 / 0,843 / 0,877, G2 0,817 / 0,774 / 0,855 |
