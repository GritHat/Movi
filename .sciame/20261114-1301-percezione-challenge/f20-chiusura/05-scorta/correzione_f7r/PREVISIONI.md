# Previsioni della correzione F7r-c1 (sciame-tracciamento)

Scritte il 2026-11-15T06:33:25+01:00 (`date -Is`), PRIMA della valutazione. Tutto simulato.

Codice: `scorta_f7r_c1.py` (copia di `scorta_f7r.py` con le correzioni a, b, c). Sviluppo: seme 20261123 (gia' seme di
sviluppo di F7r). Valutazione: UNA sola, seme NUOVO 20261124, 60 passaggi per cella, 200 per F7c, configurazioni att e sda.
Il «prima» per confronto e' la valutazione F7r esistente (seme 20261122, stessa distribuzione, semi diversi: dichiarato).

| # | misura | soglia (regge se) | smentita se |
|---|---|---|---|
| P1 | avviso prima del frammento entro 10 m, cella totale (att e sda), sui passaggi che intersecano | >= 0,9 | < 0,9 |
| P2 | riacquisizione radar <= 2 s, davanti/att e vira/att | >= 51/60 ciascuna | < 51/60 in una |
| P3 | identita' spurie non dichiarate (riacquisizione da traccia non del bersaglio con identita' «presunta» senza «dubbia», piu' associazioni a detriti non dichiarate), tutte le celle | 0 | >= 1 |
| P4 | F7c falsi avvisi (evento o avviso) per passaggio, att e sda (200) | <= 0,05 | > 0,05 |
| P5 | continuita' 60/60 (200/200 in F7c) e «libero» 0 in tutte le celle | invariati | un solo passaggio fuori |

Esiti possibili: regge, smentita, non risolta. Nessuna soglia si cambia dopo.
