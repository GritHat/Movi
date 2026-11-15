# Previsioni del videomaker per la consegna v3 (scritte prima delle misure)

Ora: 2026-11-15T06:39:24+01:00 (`date -Is`), prima che la voce v10 finisca e prima di ogni resa.

| # | Previsione | Misura | Soglia di smentita |
|---|---|---|---|
| PV-1 | La voce EN (347 parole, bm_george, velocità 1,0) dura fra 155 e 166 s | `durata_s` di kokoro_tts.py | < 150 s o > 168 s |
| PV-2 | Il video EN finale dura fra 168 e 175 s, mai oltre 176,0 | ffprobe `format=duration` | > 176,0 s (vincolo assoluto) o < 168 s |
| PV-3 | La scena F7 dura almeno 26 s (peso di scena chiave) | tempi/scene_finale_en.json | < 22 s |
| PV-4 | Loudness integrata −14 ± 0,5 LUFS, picco vero ≤ −1,0 dBTP | ebur128 sul file finale | fuori da [−14,5; −13,5] o picco > −1,0 |
| PV-5 | Nessun fotogramma (1 al secondo) con pixel verdi saturi o con «DEV DATA» | estrazione a 1 fps e controllo dei colori; grep nel motore | ≥ 1 fotogramma |
| PV-6 | La voce IT (im_nicola) è più lunga dell'EN di 3–12 % | durata | > 15 % (servirebbero tagli) |
