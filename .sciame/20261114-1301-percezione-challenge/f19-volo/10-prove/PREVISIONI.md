# Previsioni e soglie scritte PRIMA delle prove F1–F6 (sciame-validazione, f19-volo/10-prove)

Scritte alle 2026-11-15T04:49:34+01:00 (date -Is), prima di scrivere il codice delle prove e prima di qualunque passaggio.
Configurazioni: «att» = sensori di f15 (radar_sorveglianza_droni 1 Hz rotante, camere EO/IR del catalogo) con latenza
CPU (scheda + 80 ms di elaborazione, da latenza.json: stadi CPU superiori); «sda» = radar AESA a 10 Hz non rotante
(parametri_volo.json: radar_aesa_traccia_droni, sigma 0,5 gradi), camere a 10 Hz, latenza dedicata (scheda + 1,2 ms
di elaborazione: STIMA per analogia, latenza.json). ADS-B spento in entrambe (ipotesi prudente: nessun mezzo coopera).
Wilson 95 % PER PASSAGGIO. N = 60 per scenario e configurazione, 200 per F6. Semi: SeedSequence(20261119, …), nuovi.

| id | misura | soglia | smentita se |
|---|---|---|---|
| P1 | F3, evento dichiarato entro 2 s | att >= 0,75; sda >= 0,90 | att: Wilson sup < 0,75; sda: stima < 0,85 |
| P2 | F4, camere con affidabilità persa entro 3 cicli; evento entro 2 s | 100 %; >= 0,80 | un passaggio > 3 cicli; Wilson sup < 0,80 |
| P3 | calibrazione: vero dentro la zona al 99 % (r99 dalla P del nucleo) nei cicli «non vista» | 0,99 | Wilson sup (per passaggio, un campione per fascia) < 0,97 |
| P3b | per fasce di C prevista (porta di raggio g: 50 m aerei, 30 m droni) | frequenza osservata entro ±0,10 da C media | una fascia con n >= 30 con Wilson che esclude C media ± 0,10 |
| P4 | continuità: cicli in cui un oggetto vero non ha nessuna regione dichiarata che lo contenga (traccia aperta con r99, o insieme di presenza) | 0 cicli nel >= 95 % dei passaggi | stima < 0,95 |
| P5 | F5 (solo radar per 2–4 s): nessun falso evento; entrambe le tracce con regione per tutta la cecità | >= 0,95 dei passaggi | Wilson sup < 0,95 |
| P6 | F6: falsi eventi | 0/200 per configurazione (Wilson sup 1,9 %) | >= 1 |
| P7 | «libero» su un frammento vero dentro l'impronta | 0 passaggi | >= 1 |
| P8 | frammenti conformi dentro V(tau) | >= 0,99 dei campioni | < 0,99 |
| P9 | F1: avviso di prossimità (CPA previsto < 150 m) con anticipo >= 20 s sul CPA vero; F1/F6 nessun evento | >= 0,90 | Wilson sup < 0,90 |
| P10 | sda riduce il ritardo mediano dell'evento F3 di >= 0,5 s rispetto ad att | >= 0,5 s | < 0,5 s |
| P11 | F3 tempestività: primo frammento vero a terra dopo (dichiarazione + uscita + risposta + ritardo mezzo). Bordo (0,001 + 0 + 0,5 s) | sda >= 0,80 | Wilson sup < 0,80 |
| P11b | stesso per l'operatore (0,05 + 5,4 + 0,5 s) | previsto < 0,20 (cioè NON tempestivo) | stima >= 0,50 |

Video: per ogni scenario si rigenera il registro per fotogramma del passaggio idx = 0 in configurazione «sda» (seme
dichiarato qui, prima). Stato di tutto: simulato; nessuna prova su hardware.

## Aggiunta alle 2026-11-15T04:53:25+01:00 (A POSTERIORI rispetto a due passaggi di prova: F3 idx 0, att e sda, senza evento)

Regola v4 «contatto con impulso cinematico» (in prove_volo.py, regola_v4): evento se due tracce confermate sono state in
contatto negli ultimi 4 s e una delle due cambia velocità di almeno max(10 m/s, 4 sigma_v). Previsioni scritte prima di
eseguirla su N passaggi:

| id | misura | soglia | smentita se |
|---|---|---|---|
| P12 | F3 v4: evento entro 2 s | att >= 0,75; sda >= 0,85 | Wilson sup sotto la soglia |
| P13 | v4: falsi eventi in F1, F5, F6 (quasi collisioni a 40 m e incroci) | 0 in F6; <= 5 % in F1 e F5 | F6 >= 1 su 200; F1 o F5 Wilson inf > 0,05 |

## Aggiunta alle 2026-11-15T05:04:42+01:00 (A POSTERIORI rispetto ai risultati v3b)

v4 porta anche l'inviluppo di 210 m/s nell'insieme di presenza del nucleo. Previsione: P14, in F6/att e F4 il vero
dentro r99 o insieme di presenza nei cicli di perdita sale a >= 0,99 (campioni); smentita se < 0,97. P15: la
continuità (passaggi senza cicli senza regione) in F1/att, F4/att, F6/att sale a >= 0,95; smentita se Wilson sup < 0,95.

## Aggiunta alle 2026-11-15T05:15:46+01:00 (A POSTERIORI)

v4 smentita su P13 (falsi eventi F6 198/200 att). Configurazione v3i = regole eventi v3 + inviluppo 210 m/s nel nucleo. Previsioni: P14 e P15 come sopra; F3 resta 0/60 entro 2 s (l'impulso non c'è in v3i); F4 entro 2 s 60/60 come v3b; F6 0/200 falsi eventi.
