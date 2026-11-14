# PREVISIONI (esperto di dominio, f15/03-scenari)

Scritte alle 2026-11-15T00:01:24+01:00, PRIMA di aprire le fonti in rete e PRIMA di fare i conti delle distanze d'avviso
(conti in `conti.py`, esito in `conti_esito.txt`). Campo: sorveglianza aeroportuale e dello spazio aereo a bassa quota,
sistemi senza equipaggio, sicurezza dei trasporti. Tutto e' conto su valori di fonte o ipotesi: niente sensore fisico.

Formula: d = v_rel*(latenza + reazione) + spazio di manovra + margine.

| id | previsione | misura | soglia di smentita |
|---|---|---|---|
| esperto-dominio-P1 | In nessuno dei sei scenari bastano i 3 m della camera di profondita' della prima fase | d richiesta per scenario | smentita se un solo scenario ha d <= 3 m |
| esperto-dominio-P2 | A1 (multirotore piccolo verso un sito, avviso a un operatore di sito) chiede d fra 300 m e 1500 m | d di A1 con v di classe da fonte | smentita se d < 300 m o > 1500 m |
| esperto-dominio-P3 | A3 (aereo in finale + drone) chiede d > 3 km: fuori dalla portata di camere e lidar, solo radar o sorveglianza cooperativa | d di A3 | smentita se d <= 3 km |
| esperto-dominio-P4 | A2 (rullaggio) e S1 (incrocio) chiedono d fra 30 m e 300 m: alla portata di lidar e radar a onde millimetriche da scheda | d di A2 e S1 | smentita se una delle due e' fuori da [30, 300] m |
| esperto-dominio-P5 | S2 (treno): d > 500 m per via dello spazio di frenata; un avviso a bordo non serve a fermarsi a vista | d di S2 con frenata di servizio | smentita se d <= 500 m |
| esperto-dominio-P6 | L'insieme raggiungibile di un multirotore dopo 30 s ha raggio > 500 m (zona prevista poco informativa: resta la «possibile presenza»); quello di un treno resta un segmento 1D | raggio = v_max*t (inviluppo) per classe | smentita se raggio a 30 s < 500 m |
| esperto-dominio-P7 | Almeno 8 fonti su 12 fra quelle che cerchero' si aprono oggi con il dato leggibile | conteggio aperte/cercate, con intervallo di Wilson | smentita se < 8 su 12 |

Esiti possibili: regge, smentita, non risolta. Gli esiti si scrivono in fondo dopo i conti.

## Esiti (scritti alle 2026-11-15T00:06:03+01:00, dopo `conti.py`; prova: `conti_esito.txt`)

| id | esito | numero |
|---|---|---|
| P1 | regge | d minima fra tutti gli scenari e le varianti: 24 m (S1, sistema di bordo); 3 m non bastano in nessuno |
| P2 | regge | A1: 806 m |
| P3 | regge | A3: 3932 m |
| P4 | regge sul nominale | A2: 147 m (277 m via torre); S1: 67 m. La variante «sistema di bordo» di S1 (24 m) esce dall'intervallo: notato dopo |
| P5 | **smentita** | S2a (stazione, 60 km/h): 261 m, sotto i 500 m previsti; solo S2b (linea, 160 km/h) da' 798 m. La previsione non distingueva le varianti: errore mio |
| P6 | regge | multirotore a 30 s: 630 m di raggio; treno: segmento di 1332 m |
| P7 | regge, con uno scarto dal piano | aperte con il dato 13 pagine su 16 cercate (non 12 come scritto): 81 %, Wilson 95 %: 57-93 % |

Notato DOPO (non previsto): in A1, A2, A3 e S1 l'oggetto entra in occlusione, o ne esce, quando e' gia' PIU' VICINO della distanza
d'avviso richiesta. L'avviso va quindi dato prima dell'occlusione e tenuto acceso durante: e' il caso della «possibile presenza».
