import json,glob,sys
for f in sorted(glob.glob(sys.argv[1]+"/limite_*.json")):
    d=json.load(open(f))
    for k,a in d["agg"].items():
        print(d["variante"],k,"err",a["errori"],"tempest",a["tempestivo"][:2],"fuori",a["cicli_nascosti_fuori_avviso"],"senza_reg",a["cicli_nascosti_senza_regione"][:2],"libero",{x:y[:3] for x,y in a["libero_su_oggetto"].items()},"falsi/h",a["falsi_avvisi"]["per_ora"],a["falsi_avvisi"]["sup95_per_ora"])
