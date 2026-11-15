# Previsioni (sciame-comunicazione, f17-video/60-arco-volo)

Scritte alle 2026-11-15T04:37:42+01:00, prima di scrivere scaletta e voce.

- P1. Voce inglese (segnaposto esclusi, ogni cifra contata 3 parole) fra 280 e 330 parole. Smentita se > 330 (conteggio awk su voce_en_v3.txt).
- P2. Totale delle nove scene fra 168 e 175 s. Smentita se fuori.
- P3. A 125 parole al minuto (passo misurato in VOCE_GUIDA, bm_george 1.0) ogni scena ha almeno 1,5 s di margine fra voce stimata e durata. Smentita se una scena ha margine < 1,5 s.
- P4. Nessuna parola del lessico vietato nei tre file (validated, real time, real-time, threat, target, intercept, engage, neutraliz, counter-drone, detect and avoid, certif, always, guarantee, zero false). Smentita se grep ne trova una nella voce.
- P5. Almeno il 40 % delle parole della voce cade nelle scene 4–7 (collisione, fiammata, perdita di continuità, latenza), cioè il caso centrale. Smentita se < 40 %.
- P6. Il sito con rullaggio e gli altri usi stanno in 15–20 s (una scena). Smentita se fuori.
