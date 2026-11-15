# Previsioni dell'arbitro (fase 2), scritte prima dei riconti

Ora: 2026-11-15T01:39:08+01:00 (da `date -Is`), prima di aprire i file dei risultati di f15 e f16.

Soglie con cui leggerò le prove (decise ora, non dopo):

1. **Riconto.** Una cifra di un rapporto si adotta solo se il mio script, leggendo il file dei risultati
   (json o log), la ritrova uguale (frequenze: stesso k/n). Discordanza: la cifra non si adotta e diventa una
   contraddizione K#.
2. **Principio «mai libero il non osservato».** Regge alla nuova scala solo se il numero di casi «libero» dichiarato
   su una cella non osservata (o con oggetto presente nascosto) è 0 su tutte le prove ricontate; anche un solo caso
   lo smentisce per quella configurazione.
3. **Avviso tempestivo.** Per una classe e un sensore lo dichiaro «sostenuto in simulazione» solo se la frequenza di
   avviso entro il tempo richiesto ha limite inferiore di Wilson al 95 % >= 0,90 su n >= 30; tra 0,5 e 0,90 è «parziale»;
   sotto 0,5 «smentito» per quella configurazione.
4. **Previsione sul limite di scala.** Mi aspetto che con radar o lidar a lunga portata la velocità massima con
   avviso tempestivo salga di almeno un ordine di grandezza (>= 15 m/s) per droni e auto; per gli aerei mi aspetto che
   serva il radar o la sorveglianza cooperativa (ADS-B), e che il lidar da solo non basti. Smentita: se nessuna
   configurazione supera 15 m/s nei risultati.
5. **Prima prova da fare (regione di previsione nella catena su profondità simulata).** Se il prototipo non la
   esegue con un file di esito, resta «non risolta», senza eccezioni.
6. **Correzioni dell'attacco.** Una correzione è «applicata» solo se un file successivo all'attacco (per ora di
   modifica) mostra l'esito rifatto con la correzione.
