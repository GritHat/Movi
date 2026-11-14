"""Prova di apri_archivio.py su archivi ostili e buoni costruiti qui (solo libreria standard).

    python3 -I prova_archivi.py

Lavora in 03-infrastruttura/prove-tmp/ (creata e cancellata dalla prova). Esce con 0 se ogni archivio ostile
è rifiutato senza che nasca niente fuori dalla destinazione e ogni archivio buono è aperto fedelmente.
Limite dichiarato: gli archivi ostili li ha scritti lo stesso autore dell'apritore."""
import io
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
APRITORE = os.path.join(QUI, "apri_archivio.py")
BANCO = os.path.join(QUI, "prove-tmp")
shutil.rmtree(BANCO, ignore_errors=True)
os.makedirs(os.path.join(BANCO, "archivi"))
os.makedirs(os.path.join(BANCO, "aperti"))
ARCH = os.path.join(BANCO, "archivi")
SENTINELLE = [os.path.join(BANCO, "aperti", "sentinella_fuori.txt"),
              os.path.join(BANCO, "sentinella_assoluta.txt"),
              os.path.join(BANCO, "sentinella_via_collegamento.txt")]


def tar_con(nome, membri, modo="w"):
    p = os.path.join(ARCH, nome)
    with tarfile.open(p, modo) as t:
        for info, dati in membri:
            t.addfile(info, io.BytesIO(dati) if dati is not None else None)
    return p


def info_tar(nome, dati=b"", tipo=tarfile.REGTYPE, bersaglio="", modo=0o644):
    i = tarfile.TarInfo(nome)
    i.type, i.linkname, i.mode = tipo, bersaglio, modo
    i.size = len(dati) if tipo == tarfile.REGTYPE else 0
    return i, (dati if tipo == tarfile.REGTYPE else None)


ostili = {}
ostili["1 tar, percorso con «..»"] = (tar_con("o1.tar", [info_tar("dati/ok.txt", b"ok"),
                                                         info_tar("../sentinella_fuori.txt", b"fuori")]), [], 3)
ostili["2 tar, percorso assoluto"] = (tar_con("o2.tar", [info_tar(SENTINELLE[1], b"assoluto")]), [], 3)
ostili["3 tar, collegamento simbolico e file che lo attraversa"] = (tar_con("o3.tar", [
    info_tar("uscita", tipo=tarfile.SYMTYPE, bersaglio="../.."),
    info_tar("uscita/sentinella_via_collegamento.txt", b"via collegamento")]), [], 3)
ostili["4 tar, collegamento fisico"] = (tar_con("o4.tar", [
    info_tar("a.txt", b"a"), info_tar("b.txt", tipo=tarfile.LNKTYPE, bersaglio="/etc/hostname")]), [], 3)
ostili["5 tar, file speciale (coda)"] = (tar_con("o5.tar", [info_tar("coda", tipo=tarfile.FIFOTYPE)]), [], 3)
p6 = os.path.join(ARCH, "o6.zip")
with zipfile.ZipFile(p6, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("zeri.bin", b"\0" * (20 << 20))  # 20 MiB che compressi occupano pochi kB
ostili["6 zip, contenuto oltre il tetto (20 MiB contro 1M)"] = (p6, ["--tetto", "1M"], 4)

# In più rispetto alla previsione infra-P7:
p7 = os.path.join(ARCH, "o7.zip")
with zipfile.ZipFile(p7, "w") as z:
    z.writestr(zipfile.ZipInfo("../sentinella_fuori.txt"), b"fuori da zip")
ostili["7 zip, percorso con «..»"] = (p7, [], 3)
p8 = os.path.join(ARCH, "o8.zip")
with zipfile.ZipFile(p8, "w") as z:
    i = zipfile.ZipInfo("uscita")
    i.external_attr = (stat.S_IFLNK | 0o777) << 16
    z.writestr(i, "../..")
ostili["8 zip, collegamento simbolico"] = (p8, [], 3)
ostili["9 tar.gz, 20 MiB oltre il tetto di 1M"] = (tar_con("o9.tar.gz", [info_tar("zeri.bin", b"\0" * (20 << 20))],
                                                           "w:gz"), ["--tetto", "1M"], 4)
ostili["10 tar, nome ripetuto (sovrascrittura)"] = (tar_con("o10.tar", [info_tar("a.txt", b"1"),
                                                                        info_tar("a.txt", b"2")]), [], 3)
ostili["11 tar, barra rovesciata e «..»"] = (tar_con("o11.tar", [info_tar("..\\..\\x.txt", b"x")]), [], 3)
ostili["12 tar, troppi elementi (tetto 3)"] = (tar_con("o12.tar", [info_tar(f"f{k}.txt", b"x") for k in range(5)]),
                                               ["--tetto-file", "3"], 4)
p13 = os.path.join(ARCH, "o13.bin")
with open(p13, "wb") as f:
    f.write(os.urandom(4096))
ostili["13 file che non è un archivio"] = (p13, [], 5)

# 14: zip che mente sulla dimensione: dichiara 100 byte, ne contiene 20 MiB (intestazioni ritoccate a mano).
p14 = os.path.join(ARCH, "o14.zip")
with zipfile.ZipFile(p14, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("zeri.bin", b"\0" * (20 << 20))
grezzo = bytearray(open(p14, "rb").read())
for firma, scarto in ((b"PK\x03\x04", 22), (b"PK\x01\x02", 24)):
    pos = grezzo.find(firma)
    grezzo[pos + scarto:pos + scarto + 4] = (100).to_bytes(4, "little")
open(p14, "wb").write(grezzo)
ostili["14 zip che dichiara 100 byte e ne contiene 20 MiB (tetto 1M)"] = (p14, ["--tetto", "1M"], 5)

# Controllo negativo: un estrattore ingenuo, sullo stesso archivio ostile 1, la sentinella la crea davvero
# (resta dentro prove-tmp/). Serve a mostrare che la prova può fallire.
os.makedirs(os.path.join(BANCO, "aperti", "ingenuo"))
with tarfile.open(ostili["1 tar, percorso con «..»"][0]) as t:
    t.extractall(os.path.join(BANCO, "aperti", "ingenuo"), filter="fully_trusted")
print(f"[controllo negativo] estrattore ingenuo sull'ostile 1: sentinella fuori dalla destinazione creata = "
      f"{os.path.exists(SENTINELLE[0])}")
CONTROLLO_NEGATIVO = os.path.exists(SENTINELLE[0])
os.remove(SENTINELLE[0]) if CONTROLLO_NEGATIVO else None

contenuto = {"dati/a.txt": b"alfa\n", "dati/sotto/b.bin": bytes(range(256)) * 40, "LEGGIMI": b"prova\n"}
buoni = {}
buoni["B1 tar.gz buono (con un file dichiarato 04755)"] = tar_con(
    "b1.tar.gz", [info_tar("dati", tipo=tarfile.DIRTYPE, modo=0o755)]
    + [info_tar(n, d, modo=0o4755) for n, d in contenuto.items()], "w:gz")
pb2 = os.path.join(ARCH, "b2.zip")
with zipfile.ZipFile(pb2, "w", zipfile.ZIP_DEFLATED) as z:
    for n, d in contenuto.items():
        z.writestr(n, d)
buoni["B2 zip buono"] = pb2


def lancia(archivio, dest, extra):
    r = subprocess.run([sys.executable, "-I", APRITORE, archivio, dest, *extra],
                       capture_output=True, text=True, timeout=120)
    return r.returncode, (r.stderr.strip() or r.stdout.strip()).splitlines()[0][:110]


falliti = 0
for k, (nome, (archivio, extra, atteso)) in enumerate(ostili.items()):
    dest = os.path.join(BANCO, "aperti", f"ostile{k + 1}")
    codice, riga = lancia(archivio, dest, extra)
    resti = [p for p in (dest, dest + ".in-corso") if os.path.lexists(p)]
    fuori = [s for s in SENTINELLE if os.path.lexists(s)]
    ok = codice == atteso and not resti and not fuori
    falliti += not ok
    print(f"[{'OK' if ok else 'FALLITA'}] ostile {nome}: uscita {codice} (attesa {atteso}); resti {len(resti)}; "
          f"sentinelle fuori {len(fuori)}\n        {riga}")

for k, (nome, archivio) in enumerate(buoni.items()):
    dest = os.path.join(BANCO, "aperti", f"buono{k + 1}")
    codice, riga = lancia(archivio, dest, [])
    uguali = codice == 0 and all(
        os.path.isfile(os.path.join(dest, n)) and open(os.path.join(dest, n), "rb").read() == d
        for n, d in contenuto.items())
    permessi = codice == 0 and all(
        stat.S_IMODE(os.lstat(os.path.join(dest, n)).st_mode) & 0o7133 == 0 for n in contenuto)
    ok = uguali and permessi
    falliti += not ok
    print(f"[{'OK' if ok else 'FALLITA'}] {nome}: uscita {codice}; contenuto uguale: {uguali}; "
          f"nessun bit d'esecuzione o setuid: {permessi}")

# Destinazione già esistente, e destinazione fuori da f10-dati: rifiuto con codice 2.
codice, riga = lancia(pb2, os.path.join(BANCO, "aperti", "buono1"), [])
ok = codice == 2
falliti += not ok
print(f"[{'OK' if ok else 'FALLITA'}] destinazione già esistente: uscita {codice} (attesa 2)")
fuori_radice = os.path.join(os.environ.get("TMPDIR", "/tmp"), "apri_archivio_prova_fuori")
codice, riga = lancia(pb2, fuori_radice, [])
ok = codice == 2 and not os.path.lexists(fuori_radice)
falliti += not ok
print(f"[{'OK' if ok else 'FALLITA'}] destinazione fuori da f10-dati: uscita {codice} (attesa 2); creata: "
      f"{os.path.lexists(fuori_radice)}")

shutil.rmtree(BANCO, ignore_errors=True)
totale = len(ostili) + len(buoni) + 2
print(f"ESITO: {totale - falliti}/{totale} prove passate ({len(ostili)} archivi ostili, {len(buoni)} buoni, "
      f"2 destinazioni non ammesse)")
sys.exit(1 if falliti or not CONTROLLO_NEGATIVO else 0)
