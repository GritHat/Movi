# Previsioni dell'arbitro, verdetto della fase 3 (f19-volo/30-verdetto)

Scritte alle 2026-11-15T05:31:06+01:00, prima del riconto con il mio programma `riconta_verdetto.py`. Fonte dei conteggi: i record per passaggio
`10-prove/passaggi_volo_v3i.jsonl` (e v3b, v4) e `03-confidenza/casi_prova_*.json`.

- V1. Dai record v3i: F3 evento entro 2 s 0/60 in att e in sda; F4 evento entro 1 s 60/60 in entrambe; F6 falsi eventi 0/200
  in entrambe; mai «libero» sul punto vero in tutte le celle. Smentita: una qualunque di queste diversa di più di 0 passaggi.
- V2. Wilson 95 % ricalcolati da me coincidono con i rapporti entro 0,001 (51/60 -> [0,739; 0,919]; 186/200 -> [0,886; 0,958];
  56/60 -> [0,841; 0,974]; 58/60 -> [0,886; 0,991]). Smentita: scarto > 0,001.
- V3. F1/att continuità 39/60 e F6/att 186/200 nei record v3i. Smentita: scarto > 1 passaggio.
- V4. Il margine minimo dell'operatore in F4/att è sotto 0,5 s. Smentita: >= 0,5 s.
- V5. Copertura al 90 % sugli aerei reali, IMM, fascia 1-2 s, sotto 0,80 nei casi di prova. Smentita: >= 0,80.
