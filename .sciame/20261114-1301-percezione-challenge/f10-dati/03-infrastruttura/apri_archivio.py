#!/usr/bin/env python3
"""Apre un archivio NON fidato in una cartella NUOVA, senza lasciar uscire niente da quella cartella.

Uso (solo libreria standard; va bene anche il python3 di sistema):
    python3 -I apri_archivio.py <archivio> <cartella_nuova> [--tetto 2G] [--tetto-file 100000]
                                                             [--salta-collegamenti]

Formati: zip; tar semplice o compresso (gz, bz2, xz, zst). Non apre file compressi singoli (.gz di un solo
file) né archivi cifrati.

Regole (un solo elemento che le viola fa rifiutare TUTTO l'archivio, e non resta niente su disco):
  - la cartella di destinazione non deve esistere e deve stare dentro f10-dati/;
  - ogni percorso deve essere relativo, senza «..», senza barre rovesciate, senza caratteri di controllo;
  - si accettano solo file normali e cartelle: niente collegamenti simbolici o fisici, niente file speciali
    (con --salta-collegamenti i collegamenti vengono saltati ed elencati invece di far rifiutare l'archivio);
  - tetto ai byte estratti (contati mentre si scrive, non creduti all'intestazione) e al numero di elementi;
  - i file sono creati nuovi (mai sovrascritti), con permessi 0644, senza proprietario, date né bit
    d'esecuzione presi dall'archivio; le cartelle con 0755;
  - niente del contenuto viene eseguito o importato.
Si estrae in «<cartella>.in-corso» e si rinomina alla fine: la cartella finale esiste solo se è completa.

Codici d'uscita: 0 aperto; 2 uso sbagliato; 3 archivio rifiutato (percorso o tipo pericoloso);
4 tetto superato; 5 archivio illeggibile o formato non riconosciuto.
"""
import argparse
import datetime
import hashlib
import os
import re
import shutil
import stat
import sys
import tarfile
import zipfile

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.realpath(os.path.join(QUI, ".."))  # f10-dati
BLOCCO = 1 << 20


class Rifiuto(Exception):
    """Elemento pericoloso: l'archivio non si apre."""


class Tetto(Exception):
    """Tetto ai byte o al numero di elementi superato."""


def byte_da_testo(testo):
    m = re.fullmatch(r"(\d+)([KMG]?)", testo)
    if not m:
        raise argparse.ArgumentTypeError(f"tetto non valido: {testo!r} (esempi: 500000, 200M, 2G)")
    return int(m.group(1)) * {"": 1, "K": 1 << 10, "M": 1 << 20, "G": 1 << 30}[m.group(2)]


def parti_sicure(nome):
    """Restituisce le componenti del percorso, oppure solleva Rifiuto."""
    if not isinstance(nome, str) or nome == "":
        raise Rifiuto("nome vuoto")
    if any(ord(c) < 32 or ord(c) == 127 for c in nome):
        raise Rifiuto(f"caratteri di controllo nel nome: {nome!r}")
    if "\\" in nome:
        raise Rifiuto(f"barra rovesciata nel nome: {nome!r}")
    if nome.startswith("/") or re.match(r"^[A-Za-z]:", nome):
        raise Rifiuto(f"percorso assoluto: {nome!r}")
    parti = [p for p in nome.split("/") if p not in ("", ".")]
    if not parti:
        return []  # «./»: la radice dell'archivio
    for p in parti:
        if p == "..":
            raise Rifiuto(f"percorso che risale con «..»: {nome!r}")
        if len(p.encode("utf-8", "surrogateescape")) > 255:
            raise Rifiuto(f"componente del nome troppo lunga: {nome[:60]!r}…")
    return parti


def elementi_zip(percorso):
    """Genera (nome, tipo, dimensione dichiarata, apri) per ogni elemento di uno zip."""
    with zipfile.ZipFile(percorso) as z:
        for info in z.infolist():
            modo = info.external_attr >> 16
            if info.flag_bits & 0x1:
                raise Rifiuto(f"elemento cifrato: {info.filename!r}")
            if modo and stat.S_ISLNK(modo):
                tipo = "collegamento"
            elif info.is_dir():
                tipo = "cartella"
            elif modo and not (stat.S_ISREG(modo) or stat.S_IFMT(modo) == 0):
                tipo = "speciale"
            else:
                tipo = "file"
            yield info.filename, tipo, info.file_size, (lambda i=info: z.open(i))


def elementi_tar(percorso):
    """Genera (nome, tipo, dimensione dichiarata, apri) per ogni elemento di un tar."""
    with tarfile.open(percorso, mode="r:*") as t:
        for m in t:
            if m.issym() or m.islnk():
                tipo = "collegamento"
            elif m.isdir():
                tipo = "cartella"
            elif m.isreg():
                tipo = "file"
            else:
                tipo = "speciale"
            yield m.name, tipo, m.size, (lambda mm=m: t.extractfile(mm))


def apri(archivio, dest, tetto_byte, tetto_file, salta_collegamenti):
    if zipfile.is_zipfile(archivio):
        formato, elementi = "zip", elementi_zip
    elif tarfile.is_tarfile(archivio):
        formato, elementi = "tar", elementi_tar
    else:
        raise OSError("formato non riconosciuto (né zip né tar)")

    # Primo passaggio: si controlla TUTTO senza scrivere niente.
    n, dichiarati, saltati, visti = 0, 0, [], set()
    for nome, tipo, dim, _ in elementi(archivio):
        n += 1
        if n > tetto_file:
            raise Tetto(f"più di {tetto_file} elementi")
        parti = parti_sicure(nome)
        if tipo == "collegamento":
            if not salta_collegamenti:
                raise Rifiuto(f"collegamento (simbolico o fisico): {nome!r}")
            saltati.append(nome)
            continue
        if tipo == "speciale":
            raise Rifiuto(f"file speciale (dispositivo, coda o altro): {nome!r}")
        chiave = "/".join(parti)
        if tipo == "file":
            if chiave in visti:
                raise Rifiuto(f"nome ripetuto: {nome!r}")
            visti.add(chiave)
            dichiarati += max(0, dim)
            if dichiarati > tetto_byte:
                raise Tetto(f"dimensione dichiarata oltre il tetto di {tetto_byte} byte")

    # Secondo passaggio: si estrae in una cartella provvisoria, rifacendo gli stessi controlli.
    provvisoria = dest + ".in-corso"
    os.mkdir(provvisoria, 0o755)
    radice_vera = os.path.realpath(provvisoria)
    scritti, n_file, n_cartelle = 0, 0, 0
    try:
        for nome, tipo, dim, apri_elemento in elementi(archivio):
            parti = parti_sicure(nome)
            if tipo == "collegamento":
                if not salta_collegamenti:
                    raise Rifiuto(f"collegamento: {nome!r}")
                continue
            if tipo == "speciale":
                raise Rifiuto(f"file speciale: {nome!r}")
            if not parti:
                continue
            bersaglio = os.path.join(radice_vera, *parti)
            genitore = bersaglio if tipo == "cartella" else os.path.dirname(bersaglio)
            os.makedirs(genitore, mode=0o755, exist_ok=True)
            vero = os.path.realpath(genitore)
            if vero != radice_vera and not vero.startswith(radice_vera + os.sep):
                raise Rifiuto(f"il percorso esce dalla cartella: {nome!r}")
            if tipo == "cartella":
                n_cartelle += 1
                continue
            fd = os.open(bersaglio, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
            with os.fdopen(fd, "wb") as uscita, apri_elemento() as ingresso:
                while True:
                    pezzo = ingresso.read(BLOCCO)
                    if not pezzo:
                        break
                    scritti += len(pezzo)
                    if scritti > tetto_byte:
                        raise Tetto(f"byte estratti oltre il tetto di {tetto_byte}")
                    uscita.write(pezzo)
            n_file += 1
        os.rename(provvisoria, dest)
    except BaseException:
        shutil.rmtree(provvisoria, ignore_errors=True)
        raise
    return formato, n_file, n_cartelle, scritti, saltati


def impronta(percorso):
    h = hashlib.sha256()
    with open(percorso, "rb") as f:
        for pezzo in iter(lambda: f.read(BLOCCO), b""):
            h.update(pezzo)
    return h.hexdigest()


def main():
    p = argparse.ArgumentParser(description="Apre un archivio non fidato in una cartella nuova.")
    p.add_argument("archivio")
    p.add_argument("cartella_nuova")
    p.add_argument("--tetto", type=byte_da_testo, default=2 << 30, help="byte estratti al massimo (default 2G)")
    p.add_argument("--tetto-file", type=int, default=100000, help="numero massimo di elementi (default 100000)")
    p.add_argument("--salta-collegamenti", action="store_true",
                   help="salta i collegamenti simbolici e fisici invece di rifiutare l'archivio")
    a = p.parse_args()

    archivio = os.path.abspath(a.archivio)
    dest = os.path.abspath(a.cartella_nuova)
    if not os.path.isfile(archivio):
        print(f"ERRORE: archivio non trovato: {archivio}", file=sys.stderr)
        return 2
    if os.path.lexists(dest) or os.path.lexists(dest + ".in-corso"):
        print(f"ERRORE: la destinazione esiste già (deve essere nuova): {dest}", file=sys.stderr)
        return 2
    genitore = os.path.realpath(os.path.dirname(dest))
    if not os.path.isdir(genitore):
        print(f"ERRORE: la cartella che deve contenere la destinazione non esiste: {genitore}", file=sys.stderr)
        return 2
    if genitore != RADICE and not genitore.startswith(RADICE + os.sep):
        print(f"ERRORE: la destinazione deve stare dentro {RADICE}", file=sys.stderr)
        return 2

    try:
        formato, n_file, n_cartelle, scritti, saltati = apri(archivio, dest, a.tetto, a.tetto_file,
                                                             a.salta_collegamenti)
    except Rifiuto as e:
        print(f"RIFIUTATO: {e}. Niente è stato estratto.", file=sys.stderr)
        return 3
    except Tetto as e:
        print(f"TETTO SUPERATO: {e}. Niente è stato tenuto.", file=sys.stderr)
        return 4
    except (OSError, EOFError, zipfile.BadZipFile, tarfile.TarError, RuntimeError, NotImplementedError) as e:
        print(f"ILLEGGIBILE: {type(e).__name__}: {e}. Niente è stato tenuto.", file=sys.stderr)
        return 5

    h = impronta(archivio)
    print(f"APERTO: {dest}")
    print(f"  formato {formato}; {n_file} file, {n_cartelle} cartelle, {scritti} byte; sha256 dell'archivio {h}")
    if saltati:
        print(f"  collegamenti saltati: {len(saltati)} (primi: {saltati[:5]})")
    prov = os.path.join(os.path.dirname(archivio), "PROVENIENZA.md")
    if os.path.isfile(prov):
        ora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        with open(prov, "a", encoding="utf-8") as f:
            f.write(f"- `{os.path.basename(archivio)}` (sha256 `{h}`) aperto il {ora} con `apri_archivio.py` in "
                    f"`{os.path.relpath(dest, os.path.dirname(archivio))}/`: {n_file} file, {scritti} byte"
                    f"{', ' + str(len(saltati)) + ' collegamenti saltati' if saltati else ''}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
