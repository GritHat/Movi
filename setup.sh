#!/usr/bin/env bash
# setup.sh — prepara l'ambiente del prototipo MoVi in un solo comando.
#   bash setup.sh            crea .venv, installa le dipendenze, fa una prova rapida
#   bash setup.sh --prove    in più esegue tutte le prove e le scene (alcuni minuti)
#   bash setup.sh --sciame   in più installa lo sciame di agenti per Claude Code (serve il comando `claude`)
set -euo pipefail
QUI=$(cd "$(dirname "$0")" && pwd)
cd "$QUI"
PYTHON=${PYTHON:-python3}
command -v "$PYTHON" >/dev/null || { echo "Serve python3 (3.10 o più recente)."; exit 1; }
"$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
  || { echo "Serve Python 3.10 o più recente: trovato $("$PYTHON" --version)."; exit 1; }

if [ ! -x .venv/bin/python ]; then
  echo "== Creo l'ambiente virtuale .venv"
  "$PYTHON" -m venv .venv
fi
echo "== Installo le dipendenze (requirements.txt)"
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements.txt

echo "== Prova rapida: elenco delle scene del prototipo"
PY="$QUI/.venv/bin/python" sh prototipo/movi.sh scene | head -n 12

for arg in "$@"; do
  case "$arg" in
    --prove)  echo "== Prove e scene complete"; (cd prototipo && PY="$QUI/.venv/bin/python" sh prova_tutto.sh) ;;
    --sciame) echo "== Installo lo sciame di agenti"; bash sciame.sh installa ;;
    *) echo "Opzione sconosciuta: $arg"; exit 2 ;;
  esac
done
echo "== Fatto. Esempio:  PY=$QUI/.venv/bin/python sh prototipo/movi.sh esegui lp_A1 --config prototipo/scene/lp_A1.json --uscita prototipo/uscite/lp_A1"
