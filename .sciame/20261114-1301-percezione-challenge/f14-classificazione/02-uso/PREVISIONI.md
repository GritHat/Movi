# Previsioni di `sciame-tracciamento` (f14, 02-uso) — scritte PRIMA di eseguire `sim_classe.py`

Ora di scrittura: 2026-11-14T18:35:59+01:00 (`date -Is`). Il simulatore a quest'ora non esiste ancora. Letti prima: contratto f14, addendum 10,
soluzione v3 finale (§0, §1.4–1.7, §2), fascicolo dimostrazioni §3 e §8, fascicolo geometria §7. Non cieche rispetto a quei testi.
Valori delle classi: «valori di lavoro», ipotesi senza fonte (la tabella con le fonti è di un altro ruolo).

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| tr-P1 | A pari stato d'ingresso (1,5 m/s) la regione al 90 % del carrello (non olonomo) è più piccola di quella del pedone | rapporto delle aree a 2 s | smentita se rapporto ≥ 0,8 |
| tr-P2a | Pedone vero con etichetta «carrello»: la regione al 90 % della classe sbagliata lo perde | copertura a 2 s | smentita se ≥ 0,85 |
| tr-P2b | Carrello vero (ingresso a 1,5 m/s) con etichetta «pedone»: copertura bassa a 3 s (accelera, non si ferma) | copertura a 3 s | smentita se ≥ 0,90 |
| tr-P3 | L'inviluppo cinematico della classe GIUSTA copre sempre; quello della classe sbagliata no (pedone dentro l'inviluppo «carrello») | copertura a 2 s | smentita se giusta < 0,999 o sbagliata ≥ 0,90 |
| tr-P4a | «Persona» a 6 m/s in linea retta: il controllo di coerenza la smentisce presto | quota smentita e ritardo mediano dalla prima misura | smentita se quota < 0,95 o mediana > 0,5 s |
| tr-P4b | Il controllo non scatta sul pedone vero etichettato «pedone» | tracce di 3 s con almeno uno scatto | smentita se > 1 % |
| tr-P4c | Un carrello LENTO (1–2,2 m/s, quasi rettilineo) etichettato «pedone» NON è smentibile dalla cinematica | quota smentita in 3 s | smentita se > 5 % |
| tr-P5 | Se l'etichetta potesse restringere la fascia (w dalla v_max dell'etichetta), un carrello etichettato «pedone» esce scoperto in più di metà delle uscite dall'ombra; con la fascia dello scenario mai | quota di uscite con un istante fuori dall'avviso | smentita se ≤ 0,5 (regola che restringe) o > 0 (regola dello scenario) |
| tr-P6 | Con portata 3 m e reazione di 1 s nessuna classe di veicolo alla sua v_max riceve un avviso tempestivo; il limite è sotto 2,2 m/s | conto | smentita se una classe di veicolo alla v_max rientra |

Esiti: regge, smentita, non risolta. Ciò che noto dopo l'esecuzione va in USO_DELLA_CLASSE.md marcato «notato dopo».

## Esiti (scritti DOPO l'esecuzione, 2026-11-14T18:40:32+01:00; numeri in `risultati.txt`)

| # | Esito | Numero |
|---|---|---|
| tr-P1 | regge | 1,47 / 2,76 = 0,53 a 2 s (ingresso 1,5 m/s). Notato dopo: a 3 m/s d'ingresso il rapporto si rovescia (5,53 contro 2,74) |
| tr-P2a | regge | 0,719 a 2 s |
| tr-P2b | regge alla lettera, meccanismo smentito | 0,876 a 3 s, ma l'etichetta giusta dà 0,879: nessuna differenza |
| tr-P3 | smentita | pedone dentro l'inviluppo «carrello» 0,989 a 2 s (soglia 0,90); inviluppo giusto del carrello 0,995 a 3 s con ingresso a 3 m/s (soglia 0,999) |
| tr-P4a | regge | 1,000; mediana 0,47 s (è il minimo strutturale della regola: 2,8 m a 6 m/s) |
| tr-P4b | regge | 0 su 4 000 |
| tr-P4c | regge | 0,041 |
| tr-P5 | smentita per metà | regola che restringe: 0,291 (non > 0,5); regola dello scenario: 0 dentro lo scenario. Notato dopo: 0,048 per una classe fuori dallo scenario dichiarato |
| tr-P6 | regge | 2,11 m/s (C = 0); 1,76 (C = 0,5 m) |

Notato dopo, non previsto: l'estensione di R90 (tabella aggiunta al programma dopo la prima esecuzione, in coda: i numeri precedenti non cambiano, seme fisso); la regione del treno non contiene il treno fermo; il controllo di coerenza vede il pedone etichettato «carrello» solo nel 5,2 % dei casi.
