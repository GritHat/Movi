import json, sys
for l in open(sys.argv[1]):
    try: r=json.loads(l)
    except Exception: print('??',l[:300]); continue
    k={x:r.get(x) for x in ('sequenza','variante','pixel','min_punti_ostacolo','portata_m','errore','posa_stimata','posa_usata','posa_vera_primo_fotogramma','fotogrammi','celle_per_fotogramma','libero_min_mediana_max','pixel_validi_frazione','tracce_confermate','tracce_si_muove','durata_s','tempo_ciclo_ms','bersaglio') if r.get(x) is not None}
    print(json.dumps(k,ensure_ascii=False)[:1400])
