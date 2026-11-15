"""Compone i fotogrammi 3D di Unreal con i testi nello stile del video 2D (carattere Inter, pillole, schede).
Uso: python componi.py <cartella dei fotogrammi con stato.jsonl> <cartella d'uscita>"""
import json, os, sys
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageEnhance, ImageFont

QUI = os.path.dirname(os.path.abspath(__file__))
INK, BLU, GRIGIO, VERDE, ROSSO, ARANCIO = (11, 27, 51), (29, 111, 232), (92, 104, 122), (14, 159, 110), (224, 60, 49), (245, 130, 32)
B = lambda s: ImageFont.truetype(QUI + "/font/Inter-Bold.ttf", s)
M = lambda s: ImageFont.truetype(QUI + "/font/Inter-Medium.ttf", s)


def pillola(d, x, y, testo, f, sfondo, colore, punto=None, pad=22):
    w = d.textlength(testo, font=f) + 2 * pad + (30 if punto else 0)
    h = f.size + 26
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=sfondo)
    if punto:
        d.ellipse((x + pad, y + h / 2 - 8, x + pad + 16, y + h / 2 + 8), fill=punto)
    d.text((x + pad + (30 if punto else 0), y + 12), testo, font=f, fill=colore)
    return x + w + 14


def uno(arg):
    src, dst, r = arg
    im = Image.open(src).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(1.38)
    im = ImageEnhance.Color(im).enhance(1.12).convert("RGBA")
    o = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(o)
    tau, pov, visto = r["tau"], r["pov"], r["stato"] == "visto"
    conf = round(100 * r["conf"])
    # titolo
    if pov:
        d.text((110, 78), "VISTA DAL DRONE CHE PORTA MOVI", font=B(26), fill=GRIGIO)
        t1, t2 = ("Sensori accecati.", "MoVi sa dove può essere.") if not visto else ("I sensori tornano.", "MoVi lo riprende.")
    elif tau < 0:
        t1, t2 = "Un drone segue un oggetto veloce.", "MoVi lo vede."
    elif tau < 0.75:
        t1, t2 = "Una collisione vicina.", "Il tempo rallenta."
    elif not visto:
        t1, t2 = "Sensori accecati.", "MoVi sa dove può essere."
    else:
        t1, t2 = "I sensori tornano.", "MoVi lo riprende."
    y0 = 118 if pov else 84
    d.text((108, y0), t1, font=B(64), fill=INK)
    d.text((108, y0 + 76), t2, font=B(64), fill=BLU)
    # sensori
    x = 1920 - 110 - 520
    x = pillola(d, x, 84, "RADAR", B(26), (255, 255, 255, 235), INK, VERDE if r["radar"] == "ok" else ROSSO)
    x = pillola(d, x, 84, "CAMERA", B(26), (255, 255, 255, 235), INK, VERDE if r["camera"] == "ok" else ROSSO)
    if r["radar"] != "ok" and r["camera"] != "ok":
        pillola(d, x, 84, "ACCECATI", B(26), ROSSO + (255,), (255, 255, 255))
    # tempo rallentato
    if r["k"] < 1:
        pillola(d, 110, 822, ("tempo ×%.2f" % r["k"]).replace(".", ","), B(40), INK + (255,), (255, 255, 255), pad=34)
    # didascalia
    if tau < 0:
        cap = "Lo vedo."
    elif not visto:
        cap = ("Avviso inviato subito. " if r["avviso"] else "") + "Non lo vedo, ma è qui dentro: confidenza %d %%." % conf
    elif r["avviso"]:
        cap = "Avviso inviato: evento vicino. Il bersaglio è di nuovo visto."
    else:
        cap = "Bersaglio ripreso."
    f = M(38)
    w = d.textlength(cap, font=f) + 80
    d.rounded_rectangle((960 - w / 2, 918, 960 + w / 2, 990), 20, fill=(255, 255, 255, 240))
    d.text((960 - w / 2 + 40, 931), cap, font=f, fill=INK)
    d.text((110, 1030), "PROTOTIPO SIMULATO · SIMULAZIONE 3D CON MOTORE FISICO", font=B(20), fill=GRIGIO)
    # scheda del filtro, in soggettiva
    if pov:
        X, Y, W, H = 110, 330, 480, 560
        d.rounded_rectangle((X, Y, X + W, Y + H), 36, fill=(255, 255, 255, 245))
        d.rounded_rectangle((X, Y, X + W, Y + 14), 7, fill=BLU)
        d.text((X + 40, Y + 44), "Stima", font=B(46), fill=INK)
        d.text((X + 40, Y + 102), "filtro di Kalman", font=M(26), fill=GRIGIO)
        d.text((X + 40, Y + 142), "prevede dove può essere", font=B(28), fill=BLU)
        (ax, bx, cx), (ay, by, cy) = r["P"]
        P = [[ax, 0, bx, 0], [0, ay, 0, by], [bx, 0, cx, 0], [0, by, 0, cy]]
        rif = [9.0e4, 9.0e4, 6.0e4, 6.0e4]            # scala fissa: le caselle si scuriscono mentre l'incertezza cresce
        for i in range(4):
            for j in range(4):
                v = min(1.0, abs(P[i][j]) / ((rif[i] * rif[j]) ** 0.5))
                col = tuple(int(232 + (BLU[n] - 232) * (0.10 + 0.90 * v)) for n in range(3))
                d.rounded_rectangle((X + 112 + j * 66, Y + 196 + i * 66, X + 168 + j * 66, Y + 252 + i * 66), 11, fill=col)
        d.text((X + 40, Y + 468), "matrice d'incertezza del filtro", font=M(22), fill=GRIGIO)
        d.text((X + 40, Y + 502), "CONFIDENZA", font=B(20), fill=GRIGIO)
        d.rounded_rectangle((X + 190, Y + 504, X + W - 40, Y + 524), 10, fill=(225, 231, 240))
        d.rounded_rectangle((X + 190, Y + 504, X + 190 + (W - 230) * max(0.04, r["conf"]), Y + 524), 10, fill=BLU)
    Image.alpha_composite(im, o).convert("RGB").save(dst, quality=93)


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    os.makedirs(dst, exist_ok=True)
    righe = [json.loads(l) for l in open(src + "/stato.jsonl")]
    lav = [("%s/f_%05d.png" % (src, r["f"]), "%s/c_%05d.jpg" % (dst, n), r) for n, r in enumerate(righe)
           if os.path.exists("%s/f_%05d.png" % (src, r["f"]))]
    with Pool(12) as p:
        p.map(uno, lav)
    print(len(lav), "fotogrammi composti")
