# Previsioni dell'attacco (sciame-avversario, f19-volo/20-attacco)

Scritte alle 2026-11-15T05:28:03+01:00, dopo aver letto i cinque documenti e la struttura dei dati, PRIMA di ogni conto o simulazione mia.

- **PA1 (ADS-B, manovre).** Sui casi di prova degli aerei veloci (03-confidenza/casi_prova_aerei_veloci.json), nei tratti
  di tipo «virata» o «accelerazione», la copertura al 90 % dell'IMM in almeno una fascia di tau ha il limite SUPERIORE di
  Wilson < 0,90 (la curva promette più di quanto si osserva). Smentita se in tutte le fasce il superiore è >= 0,90.
- **PA2 (ADS-B, CV in manovra).** La copertura al 90 % del CV nei tratti «virata» a tau >= 6 s è < 0,50. Smentita se >= 0,50.
- **PA3 (prima fascia).** Alla fascia 1–2 s degli aerei la copertura al 50 % (non solo al 90 %) è anch'essa sotto il
  livello: Wilson superiore < 0,50 per IMM. Smentita se >= 0,50.
- **PA4 (tempestività).** La colonna «umano senza ausilio» di SENSORI_E_HARDWARE conta due volte i 2,0 s del ritardo del
  mezzo: d_tabella − v·(L + 12,5) = v·2,0 entro 1 m in tutte le righe. Smentita se lo scarto non è v·2,0.
- **PA5 (hardware).** La somma dei soli stadi di calcolo dedicato di latenza.json nel caso peggiore supera 1 ms, quindi la
  frase «caso peggiore sotto il millisecondo» non regge sui propri numeri. Smentita se <= 1 ms.
- **PA6 (F3 al limite, conforme).** Frammenti F3 con |u| = dv = 120 m/s sul bordo e vento al limite W = 15 m/s: quota dei
  campioni dentro V(tau) >= 0,99 (il volume regge dentro le sue ipotesi). Smentita se < 0,99.
- **PA7 (F4 avaria NON contenuta realistica).** Con il 5 % dei frammenti come pezzi di disco a 250 m/s (ipotesi: «centinaia
  di m/s», già dichiarati fuori inviluppo) e v_t 80 m/s, la quota di frammenti SEMPRE dentro V(tau) è < 0,97. Smentita se >= 0,97.
- **PA8 (F3, velocità delle tracce sbagliata).** Con |u| sul bordo e la vc dichiarata di ciascuna traccia sbagliata di 8 m/s
  (errore di traccia a 1 Hz dopo manovra, ipotesi), la quota dei campioni dentro V < 0,999. Smentita se >= 0,999.
