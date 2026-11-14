# Firme di `sciame-kalman` (autore di f1 `21d3813ca7e1`)

Ho letto solo le schede `kalman-1` e `kalman-2` (righe 62–74 di `f2/01-traduzione/SCHEDE.md`).

`kalman-1`: si perde: (a) il modello è a velocità **quasi** costante, cioè con rumore di processo q > 0: a velocità costante in senso stretto (q = 0) è proprio il filtro ottimista che la consegna smentisce; (b) la prova del muro vale **da fermi e a rotazione compensata**: se il portatore cammina senza odometria il muro è «mobile» il 100 % del tempo per costruzione, e la prova scritta nella scheda smentirebbe a torto; (c) 0,20 s è una mediana, in un riferimento già compensato.
Enunciato corretto: un Kalman lineare a velocità quasi costante (q > 0, tarato come in `kalman-2`) per traccia, stato [x, y, vx, vy] sul piano del suolo, in un riferimento stabilizzato in rotazione dal giroscopio (e in traslazione, se c'è odometria), a valle di rilevamento e associazione e a monte della decisione. Niente massa né accelerazione. «Mobile» = prova sulla covarianza (v'·Pv⁻¹·v > 9,21, chi quadrato al 99 %), non soglia fissa. Gravità = classe di taglia × velocità di avvicinamento.
In simulazione (15 Hz, 5 cm, q = 0,2): velocità a 0,2 m/s; pedone a 1,2 m/s «mobile» in 0,20 s di mediana nel riferimento compensato; ostacolo fermo «mobile» nello 0,0 % del tempo con rotazione e traslazione compensate (500 prove), nel 100 % senza traslazione; sotto circa 0,62 m/s la prova non scatta.
Falsificatore sul prototipo: da fermi, muro ripreso ruotando la testa per 30 s, a rotazione compensata; smentita se «mobile» oltre il 10 % del tempo.

`kalman-2`: fedele. Una precisazione sulla riga «Vicina a», che non tocca l'enunciato: q = 0,2 m²/s³ non è un valore che propongo ma quello tarato sul pedone simulato (stato «non risolto» per pedoni e sensore reali); ciò che distingue la scheda è la regola «q tarato sul NIS e accettato con il 26/30», non il numero.
