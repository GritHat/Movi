# Previsioni del metrologo (f11, sez-c) — controllo di ripetibilità, scritte PRIMA dei rilanci

Ora di scrittura (`date -Is`): 2026-11-14T16:12:36+01:00. A quest'ora nessuno script è stato rilanciato da me.

Che cosa faccio: rilancio sette script già consegnati (uno per fase), senza modificarli, con l'uscita in questa
cartella (`riprove/`), uno alla volta, ciascuno sotto `timeout 120`, con `PYTHONDONTWRITEBYTECODE=1`.
Confronto con `diff` l'uscita nuova e il file dei risultati consegnato.

| # | Script (argomenti) | File consegnato di confronto |
|---|---|---|
| R1 | f1/21d3813ca7e1/sim_kalman.py | f1/21d3813ca7e1/risultati.txt |
| R2 | f2/04-torneo/scena_parte3.py due | f2/04-torneo/risultati_due_parte3.txt |
| R3 | f4/H-012/01-avversario/a01_riaggancio.py | f4/H-012/01-avversario/risultati_a01.txt |
| R4 | f4/H-012/03-validazione/sim_h012.py A6 400 | f4/H-012/03-validazione/out_A6.txt |
| R5 | f4/H-012/03-validazione/sim_v2.py R8 400 0.9 | f4/H-012/03-validazione/v2_R8_pd09.txt |
| R6 | f6-specializzazione/03-avversario/conti_spec.py | f6-specializzazione/03-avversario/risultati_spec.txt |
| R7 | f6-specializzazione/02-slam/bilancio_posa.py | f6-specializzazione/02-slam/risultati.txt |

**Previsione:** tutti e sette ridanno il file consegnato riga per riga, escluse le righe dei tempi (`real`, `user`,
`sys`, secondi di CPU). In particolare R5 ridà 13 passaggi falliti su 4800 a −20 cm.
**Soglia di smentita:** una sola riga numerica diversa (non di tempo) in uno dei sette. Esiti: regge, smentita,
non risolta (lo script non parte o supera i 120 s).
**Che cosa il controllo condivide con ciò che controlla:** lo stesso codice, gli stessi semi, la stessa macchina e lo
stesso interprete di sistema: prova la ripetibilità (stesso codice → stesso numero), non la correttezza del modello.

## Esito (scritto alle 2026-11-14T16:13:44+01:00, dopo i rilanci)

**Regge.** Sette script su sette ridanno il file consegnato: R2, R3, R6, R7 senza alcuna riga diversa; R1 differisce
nella sola riga «tempo di calcolo» (8,2 s contro 8,1 s); R4 e R5 differiscono nelle sole righe `real/user/sys` che il
file consegnato contiene e la mia uscita no (io non ho usato `time`). R5 ridà 13 passaggi falliti su 4800 a −20 cm.
Nessun file fuori da questa cartella è stato scritto (nessun `__pycache__` nuovo). Uscite: `R1.txt` … `R7.txt`.
Comando: `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 <script> [argomenti] > riprove/Rn.txt`, poi `diff`.
Interprete: Python 3.14.10 di sistema. Limite: è ripetibilità sulla stessa macchina, non riproducibilità altrove.
