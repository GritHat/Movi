# Previsioni dell'arbitro (f20-chiusura/20-verdetto), scritte alle 2026-11-15T06:26:20+01:00, PRIMA di ogni riconto e di ogni corsa

Riconto dai file grezzi (script miei: riconta_finale.py; attacco F7: attacco_f7.py).

- PA-1 (F3 v4c, valutazione_v4c.jsonl): entro 2 s att 34/60, sda 57/60; prima dell'urto 1/60 e 1/60. Smentita: scarto >= 1 passaggio.
- PA-2 (F6 v4c): falsi eventi 0/200 att e sda; F5 2/60 att e sda; F1 att 1/60. Smentita: scarto >= 1.
- PA-3 (F3 v3i, passaggi_volo_v3i.jsonl): entro 2 s 0/60 att e sda. Smentita: >= 1.
- PA-4 (E1 stabile): 0<=ritardo<=2 s 48/60; prima dell'urto 3/60; frammenti tutti dentro V 60/60. Smentita: scarto >= 1.
- PA-5 (F7, passaggi_valutazione.jsonl): continuita' sda 60/60 x4; att davanti 59/60; identita' vira/att 43/60; libero 0 ovunque; falsi eventi F7c 0/200 x2; evento att lato 1/60 e dietro 0/60. Smentita: scarto >= 1 in una cella.
- PA-6 (attacco F7, semi nuovi base 20261199, 20 per cella, 60 per F7c): continuita' sda >= 19/20 in ogni cella; libero 0; falsi eventi F7c 0/60. Smentita: < 19/20 in una cella sda, o libero >= 1, o un falso evento.
- PA-7 (attacco F7, geometria: collisione davanti a 10-30 m): continuita' sda >= 19/20, libero sui frammenti 0. Smentita: < 19/20 o libero >= 1. Rischio previsto: identita' piu' bassa.
- PA-8 (attacco F7, frammenti piu' veloci del volume dichiarato, dv_sim 100 m/s > dv_decl 80+10): contenimento del volume < 100 % dei campioni in almeno 1 cella (mostra che A-6 vale solo nel modello). Smentita: 100 % ovunque.
- PA-9 (attacco F7, F7c con quasi collisione a 5-20 m in quota invece di 30-60): falsi eventi >= 1/60 in almeno una configurazione. Smentita: 0/60 in tutte e due.
