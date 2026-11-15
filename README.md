# MoVi — gruppo SDMs

Progetto per The Big Hack 2026 («Ritorno al Futuro Remoto», Città della Scienza), challenge di computer vision.

**Autori:** Ignazio Crocchiolo, Federico Dellini, Danilo Amalfitano, Emanuele Ciotola, Pierfrancesco Amendola.

MoVi è un sistema di percezione che **dichiara ciò che non ha osservato**. Di ogni oggetto seguito dice se lo vede,
se non lo vede ma sa in quale regione può essere, o se non lo sa. Ciò che non è stato osservato non è mai «libero».
Il caso centrale è il volo ad alta velocità di aerei e droni con eventi improvvisi: collisioni, detriti, fiammate,
sensori accecati.

**Stato:** è un prototipo **simulato**. I sensori sono modellati dalle schede tecniche e le traiettorie reali vengono
da archivi pubblici. Non c'è nessuna prova su hardware. Limiti e risultati sono nel documento tecnico.

## Che cosa c'è

| Cartella o file | Contenuto |
|---|---|
| `proposta/proposta_sciame.pdf` | proposta di due pagine (storia delle versioni in `VERSIONI.md`) |
| `allegato_tecnico/allegato_tecnico.pdf` | documento tecnico: dimostrazioni, prove, limiti, bibliografia |
| `documentazione/` | stato del progetto, riferimenti (`RIFERIMENTI.md`, `riferimenti.bib`) |
| `prototipo/` | prototipo simulato in Python (`README.md` proprio, con tutti i comandi) |
| `video/` | marchio, script della voce, progetto del video pitch |
| `sciame.sh`, `sciame/`, `.claude/` | lo sciame di agenti per Claude Code usato per analisi e verifiche |
| `.sciame/` | registro di lavoro dello sciame: prove, codice delle simulazioni, verdetti |
| `setup.sh`, `requirements.txt` | setup automatico dell'ambiente |

## Setup automatico

Servono `bash` e Python 3.10 o più recente.

    git clone https://github.com/GritHat/Movi.git
    cd Movi
    bash setup.sh

`setup.sh` crea l'ambiente virtuale `.venv`, installa le dipendenze di `requirements.txt` e fa una prova rapida:
stampa l'elenco delle scene del prototipo. Opzioni:

| Comando | Che cosa fa in più |
|---|---|
| `bash setup.sh --prove` | esegue tutte le prove e tutte le scene (alcuni minuti) |
| `bash setup.sh --sciame` | installa lo sciame di agenti (serve il comando `claude` di Claude Code) |
| `PYTHON=python3.12 bash setup.sh` | usa un interprete specifico |

Gli script del prototipo trovano da soli l'interprete di `.venv`. Per forzarne un altro: `PY=/percorso/python`.

## Setup manuale

    python3 -m venv .venv
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install -r requirements.txt

Poi, per controllare che funzioni:

    sh prototipo/movi.sh scene

Senza ambiente virtuale bastano `numpy`, `scipy`, `pillow` e `opencv-python-headless` nel Python di sistema: gli
script usano `python3` se non trovano `.venv`.

## Uso del prototipo

Da `prototipo/` (dettagli in `prototipo/README.md`):

    sh movi.sh scene                                                   # elenco delle scene
    sh movi.sh esegui lp_A1 --config scene/lp_A1.json --uscita uscite/lp_A1
    sh movi.sh tabellone uscite/lp_A1/registro.jsonl                   # conteggi con intervallo di Wilson al 95 %
    sh movi.sh convalida uscite/lp_A1/registro.jsonl                   # controlla i principi sul registro
    sh movi.sh mostra uscite/lp_A1/registro.jsonl --filmato            # viste e filmato
    sh prova_tutto.sh                                                  # tutte le prove e le scene

Le uscite vanno in `prototipo/uscite/`, che non è nel repository: si rigenera.

## Sciame di agenti (facoltativo)

`sciame.sh` è un solo file che installa e avvia lo sciame in un progetto con Claude Code:

    bash sciame.sh installa                       # una volta: scrive sciame/ e .claude/
    bash sciame/sciame.sh classica "richiesta"    # convoca lo sciame; anche: singolo, completa, auto
    bash sciame/sciame.sh ruoli                   # elenco dei ruoli e dei profili

La guida completa è nell'intestazione di `sciame.sh` e in `sciame/README.md`.

## Documenti: come ricompilarli

Serve una distribuzione LaTeX con `xelatex` e `bibtex`.

    cd allegato_tecnico && xelatex allegato_tecnico && bibtex allegato_tecnico && xelatex allegato_tecnico && xelatex allegato_tecnico
    cd proposta && xelatex proposta_sciame

## Che cosa non è nel repository

Il `.gitignore` lascia fuori il materiale temporaneo (ambienti, file ausiliari di LaTeX, uscite delle simulazioni,
dati scaricati, audio e video) e le versioni superate dei documenti. Resta solo la versione corrente di proposta,
documento tecnico, stato e riferimenti.
