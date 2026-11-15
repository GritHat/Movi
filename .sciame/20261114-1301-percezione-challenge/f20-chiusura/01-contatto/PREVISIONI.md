# Previsioni e protocollo (f20-chiusura/01-contatto, sciame-scene-dinamiche)

Scritte alle 2026-11-15T05:38:53+01:00 (`date -Is`), PRIMA di qualunque passaggio con la regola nuova.

## Protocollo
- Nucleo v4 = copia di `f19-volo/10-prove/prove_volo.py` in modalità v3i (inviluppo 210 m/s nel nucleo), file nuovo
  `prove_volo_v4.py` in questa cartella; `prove_volo.py` resta intatto. Regola nuova: `VOLO_REGOLA=v4c` (contatto).
- Sviluppo SOLO su idx 0–19 di F3 ed F6, att e sda (semi già usati nelle fasi precedenti).
- Valutazione UNA volta su idx MAI usati: 1000–1059 per F1, F3, F4, F5; 1000–1199 per F6; att e sda.
- Doppler simulato: v_r = v_vera·los + N(0; 0,5 m/s) sui ritorni radar (ipotesi, nessuna scheda aperta per σ_vr).
- La regola non legge mai la verità: solo tracce, covarianze, ritorni radar (posizione e v_r).

## Soglie (dal mandato, fissate qui)
- P1. F3 evento entro 2 s dall'urto: ≥ 51/60 per configurazione = INCORAGGIANTE, con F6 0/200 falsi eventi e F1, F5 0/60.
- P2. Smentita: un falso evento in F6 (att o sda) oppure F3 < 45/60 in una configurazione.
- P3. F4 non peggiora: evento entro 1 s 60/60 e «libero» sul vero 0, in att e sda.
- P4. Fra 45 e 50 su 60 senza falsi: «non risolta / limite».
- Mia previsione (prima): in sda F3 regge (≥ 51/60), in att (radar rotante 1 Hz: 3 aggiornamenti = 3 s) F3 NON regge
  entro 2 s (stima < 45/60), perché la conferma su 3 aggiornamenti Doppler costa almeno 2–3 s.
- E1 (K-709): previsione: il 51/60 cambia di al più ±3 passaggi con l'integratore stabile.
