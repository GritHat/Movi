# Previsioni scritte prima di far girare frammenti.py

Ora: 2026-11-15T00:11:58+01:00. Autore: sciame-scene-dinamiche (scheda 49). Nessun risultato visto prima di questa scrittura.

Modello del frammento: punto materiale, gravita', resistenza quadratica isotropa con coefficiente costante
(velocita' limite v_t), vento orizzontale e verticale. Volume dichiarato V(tau) e impronta come in regole_eventi.json.

- P1 (conforme al modello: |u| <= dv_max, vento costante entro i limiti). Misura: quota dei campioni
  (frammento, istante ogni 0,5 s) dentro V(tau), tolleranza numerica 0,05 m. Attesa: 100 % (c'e' una prova scritta).
  Smentita: anche un solo campione fuori oltre la tolleranza, sia con i valori nominali sia con i prudenti.
- P2 (gittata: la resistenza non allunga la gittata nel riferimento dell'aria). Misura: quota dei punti di caduta
  dentro l'impronta finale, frammenti con v_t >= v_t_min. Attesa >= 99,9 %. Smentita: < 99,9 %. NON c'e' una prova.
- P3 (tempo di chiusura T_c). Misura: quota dei frammenti con v_t >= v_t_min a terra entro T_c. Attesa >= 99,9 %.
  Smentita: < 99,9 %. NON c'e' una prova.
- P4 (controllo negativo: velocita' vera dei frammenti 1,5 volte quella ipotizzata). Attesa: la quota dentro V
  scende sotto il 100 % (fra 80 e 99,9 %). Se resta 100 %: l'inviluppo e' piu' largo di quanto credo (da annotare).
- P5 (raffiche: vento variabile nel tempo ma entro i limiti). Attesa >= 99,9 % dentro V. NON c'e' una prova.
- P6 (frammenti piu' leggeri di v_t_min, controllo negativo). Attesa: una parte e' ancora in volo a T_c (> 1 %).

## Aggiunta delle 2026-11-15T00:16:50+01:00: scritta DOPO aver visto i primi 4 casi del primo giro (interrotto)

Il primo giro (frammenti_esito_primo_giro_interrotto.txt, 4 casi di E1 nominale, passo 0,02 s, 12 000 frammenti)
dava 0 campioni fuori dal volume, ma T_c = 131 s e impronta di 1832 m contro un volo massimo simulato di 41 s e una
gittata massima di 406 m: formula inutilmente larga (sommava il frammento piu' leggero con la salita senza
resistenza). Ho cambiato T_c e l'impronta (T_volo per velocita' limite, R_imp come massimo su v_t); passo a 0,04 s
e 10 000 frammenti per stare nel tempo. P1, P4, P5, P6 restano come scritte sopra.
P2 e P3 valgono ora per la NUOVA formula: sono previsioni scritte dopo aver visto dati della vecchia. Soglie
invariate (>= 99,9 %).
Gia' visto su P4: con dv vera 1,5 volte, dentro il volume il 99,96 % (attesa 80-99,9 %): l'inviluppo e' piu' largo
di quanto credevo (la resistenza frena subito i frammenti leggeri). Previsione sbagliata di poco, annotata.

## Nota delle 2026-11-15T00:17:24+01:00: secondo giro buttato (errore mio nel programma)

Il secondo giro (frammenti_esito_secondo_giro_instabile.txt, un caso) dava 4 campioni fuori con eccedenza 1e207 m:
non e' una smentita di P1, e' l'integratore esplicito che diverge a passo 0,04 s per i frammenti leggeri e veloci
(k |v| dt > 1). Corretto con sottopassi h <= 0,2/(k |v_rel|). Previsioni e soglie invariate.

## Esiti (2026-11-15T00:20:40+01:00; terzo giro, risultati_frammenti.json, 88 s di calcolo)

- P1: REGGE. 0 campioni fuori su 8 casi conformi (uniforme e bordo, E1 ed E2, nominale e prudente), 10 000 frammenti l'uno.
- P2: REGGE (100 % delle cadute dentro l'impronta, larga e stretta), ma la formula e' stata cambiata dopo il primo giro.
- P3: REGGE (100 % a terra entro T_c), stessa riserva.
- P4: SMENTITA IN PARTE. La quota scende sotto il 100 % (99,83-99,997 %) ma in 3 casi su 4 resta sopra il 99,9 %
  che avevo dato come tetto: l'inviluppo ha piu' margine di quanto credevo.
- P5: REGGE (0 fuori su 4 casi con raffiche). Non e' una prova.
- P6: REGGE. Ancora in volo a T_c: 36 % e 26 % (E1), 3 % e 6 % (E2); cadute fuori dall'impronta fino al 19 %.
