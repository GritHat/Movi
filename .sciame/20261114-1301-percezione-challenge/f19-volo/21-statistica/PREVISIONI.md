# Previsioni del controllo statistico f19 (sciame-statistico)

Scritte il 2026-11-15T05:26:26+01:00 (da `date -Is`), prima di aprire PROVE_VOLO.md, PERDITA_DI_CONFIDENZA.md e i file grezzi.

P1. Le cifre di PROVE_VOLO.md si ricontano dai .jsonl/.json grezzi con scarto 0 su k e N.
    Smentita: almeno una cifra k/N non coincide col riconto.
P2. Le soglie delle prove di volo sono in un PREVISIONI.md con ora anteriore al primo esito (avvio_*.txt / esito_*.txt).
    Smentita: ora delle previsioni successiva all'esito, o soglia assente per una cifra riportata.
P3. Gli intervalli dichiarati sono di Wilson al 95 % e coincidono col mio calcolo entro 0,01.
    Smentita: scarto > 0,01 o intervallo non di Wilson.
P4. Le cifre sulle traiettorie reali ad alta velocità poggiano su pochi mezzi distinti (stima: meno di 30 aerei distinti, meno di 10 droni distinti); il N per passaggio è maggiore del N per mezzo.
    Smentita: N mezzi distinti >= N passaggi riportato (nessuna dipendenza).
P5. Curva di affidabilità della confidenza: in almeno una classe (fascia di confidenza prevista) lo scarto prevista-osservata supera l'intervallo di Wilson; il test d'adeguatezza (Hosmer-Lemeshow o chi-quadro per fasce) non rifiuta a 0,05 sul complesso.
    Smentita della prima parte: tutte le fasce dentro l'intervallo. Della seconda: p < 0,05.
P6. Almeno una cifra ad alta velocità (aerei o droni in collisione/detriti/impulsivi) è classificabile solo come «limite» (estremo inferiore di Wilson < 0,5).
    Smentita: tutte le cifre di alta velocità con estremo inferiore >= 0,5.
