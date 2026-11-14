# PREVISIONI — sciame-visione, f1, corsia A

Scritte alle 2026-11-14T13:05:40+01:00, PRIMA di eseguire i calcoli e i controlli che le decidono. Esiti possibili: regge, smentita, non risolta.

## P1 (visione-1) — le classi che servono non stanno in un rilevatore a classi chiuse
- Misura: quante fra 7 categorie di ostacolo tipiche dei due scenari (muro, porta, gradino o scala, palo, scatola di cartone, carrello o transpallet, cono) compaiono fra le 80 classi COCO su cui sono addestrati i rilevatori in tempo reale pronti all'uso.
- Esito atteso: 0 su 7.
- Soglia di smentita: 2 o più su 7 presenti (allora il solo rilevatore RGB coprirebbe buona parte di R2 e «la geometria prima» perderebbe il motivo principale).
- Prova: elenco delle classi nel file coco.yaml di Ultralytics (fonte indipendente da me). Classe 1.

## P2 (visione-1) — tre ToF multizona non danno 360° né una classe
- Misura: copertura orizzontale di 3 sensori ToF multizona (campo dalla scheda tecnica) e larghezza di una zona a 2 m.
- Esito atteso: copertura fra 135° e 180° (meno di 360°); zona larga fra 0,20 e 0,30 m a 2 m (una persona larga 0,5 m occupa 2-3 zone: presenza sì, classe no).
- Soglia di smentita: copertura di 300° o più, oppure zona di 0,05 m o meno a 2 m.
- Prova: calcolo a mano sui numeri della scheda tecnica ST. Classe 1.

## P3 (visione-2) — la previsione a velocità costante sotto occlusione ha una scadenza breve
- Misura: raggio d'errore al 95% della posizione prevista (modello a velocità costante, nessuna misura) per un pedone che cammina a 1,3 m/s con accelerazione casuale; simulazione Monte Carlo (10 000 corse, passo 0,05 s) con sigma_a = 0,5 e 1,0 m/s^2 per asse, tempo di correlazione 1 s (IPOTESI mia sui valori del moto umano: non verificata su dati reali).
- Esito atteso: il raggio al 95% supera 1,0 m (mezza larghezza di un corridoio) dopo un tempo compreso fra 1,5 s e 3 s di occlusione; a 0,5 s resta sotto 0,3 m.
- Soglia di smentita: (a) raggio al 95% ancora sotto 0,5 m a 3 s per entrambe le sigma (allora la scadenza non serve); oppure (b) raggio sopra 1,0 m già a 0,5 s (allora un Kalman a velocità costante non regge nemmeno le occlusioni brevi e R3 chiede altro).
- Prova: script numpy su CPU, meno di un minuto. Condivide con la proposta l'autore e il modello di moto (non è indipendente su quelli); è indipendente solo dall'algebra fatta a mente. Classe 2.

## P4 (diagnosi) — sfocatura da movimento con camera sulla testa
- Misura: sfocatura in pixel per rotazione della testa a 120 gradi/s, focale di circa 465 px (640 px su 69 gradi orizzontali), esposizione 10 ms e 33 ms.
- Esito atteso: circa 10 px a 10 ms e circa 30 px a 33 ms (oltre i 2-3 px tollerabili da rilevatore e flusso).
- Soglia di smentita: meno di 3 px a 10 ms.
- Prova: calcolo a mano (omega * t_esp * f). Classe 1.

## P5 (visione-1) — bilancio di latenza su CPU; NON eseguibile ora (serve il portatile della squadra)
- Misura: tempo per fotogramma di un rilevatore «nano» a 640 px esportato in ONNX, sul portatile della squadra, senza GPU.
- Esito atteso: fra 30 e 60 ms (da 16 a 33 Hz); con la parte geometrica (non verificata) sotto 100 ms in tutto.
- Soglia di smentita: più di 80 ms per fotogramma.
- Prova: il comando di benchmark di Ultralytics con imgsz=640 e device=cpu, cinque minuti. Stato ora: non risolta.

## P6 (visione-2) — prova di visibilità geometrica; NON eseguibile ora (serve la camera di profondità)
- Misura: su 10 passaggi di una persona dietro un pannello e 10 uscite di scena senza occlusore, quante volte la regola «profondità misurata lungo il raggio < distanza prevista - margine» dà lo stato giusto (OCCLUSO-PREVISTO contro PERSO-SCONOSCIUTO).
- Esito atteso: almeno 18 su 20.
- Soglia di smentita: 15 o meno su 20.
- Stato ora: non risolta.

---

# ESITI (scritti alle 2026-11-14T13:07:39+01:00, DOPO le prove; la parte sopra non è stata toccata)

Deviazione dal piano scritto: P3 prevedeva numpy, che sulla macchina non c'è; ho usato la libreria standard di Python (stesso modello, stesso numero di corse, seme 20261114). Script: `calcoli_p2_p3_p4.py` in questa cartella (scritto prima nello scratchpad della sessione, poi copiato qui). Comando: `python3 -I calcoli_p2_p3_p4.py`.

- **P1: regge.** 0 su 7: fra le 80 classi di coco.yaml non ci sono muro, porta, gradino o scala, palo, scatola, carrello o transpallet, cono (ci sono persona, bicicletta, auto, sedia, panca, valigia...). Fonte: https://raw.githubusercontent.com/ultralytics/ultralytics/main/ultralytics/cfg/datasets/coco.yaml (letta attraverso lo strumento di lettura delle pagine, che riassume: l'elenco delle 80 classi coincide con quello che conosco).
- **P2: regge.** VL53L8CX (45° x 45°): 3 sensori = 135°, zona 5,6°, larga 0,197 m a 2 m. VL53L7CX (60° x 60°): 3 sensori = 180°, zona 7,5°, larga 0,262 m a 2 m. I campi vengono da Pololu e ST (vedi CONSEGNA); il calcolo è mio.
- **P3: soglie di smentita non toccate; il valore atteso era sbagliato per eccesso.** Raggio al 95%: sigma_a 0,5 m/s^2: 0,14 m a 0,5 s; 0,54 m a 1 s; 1,14 m a 1,5 s; 1,93 m a 2 s; 3,97 m a 3 s. sigma_a 1,0 m/s^2: 0,28 m a 0,5 s; 1,07 m a 1 s; 2,28 m a 1,5 s; 7,89 m a 3 s. Il metro si supera a circa 1,0-1,4 s, non a 1,5-3 s come avevo scritto: la scadenza è più breve del previsto. L'enunciato «la previsione ha una scadenza breve» regge; il numero va corretto a circa 1-1,5 s. Limiti: la simulazione parte da errore di velocità nullo (ottimista) e i valori di sigma_a sono una mia ipotesi, non misurati su persone.
- **P4: regge.** f = 466 px; 9,8 px a 10 ms; 32,2 px a 33 ms; servono circa 2 ms per restare a 2 px.
- **P5: non risolta** (serve il portatile della squadra). Dato pubblicato: YOLO26n 38,9 ± 0,7 ms su CPU in ONNX a 640 px (https://docs.ultralytics.com/models/yolo26/); la CPU di quella misura non è la vostra.
- **P6: non risolta** (serve la camera di profondità).
