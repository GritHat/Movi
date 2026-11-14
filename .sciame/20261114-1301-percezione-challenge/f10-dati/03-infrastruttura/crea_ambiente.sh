#!/usr/bin/env bash
# Crea (o ricrea uguale) l'ambiente Python di f10 in f10-dati/ambiente/venv.
# Si può rilanciare: se requisiti.txt esiste, l'ambiente viene riallineato a quello e basta.
# Non usa sudo e non scrive fuori da f10-dati/: anche la cache di uv e gli eventuali Python
# scaricati da uv stanno in f10-dati/ambiente/.
#
# Uso:   bash crea_ambiente.sh              # Python di sistema (/usr/bin/python3)
#        PYTHON_AMBIENTE=3.13 bash crea_ambiente.sh   # ripiego: Python gestito da uv, dentro la cartella
# Per tornare indietro: rm -rf f10-dati/ambiente/venv (e, se si vuole, cache-uv e python-uv).
set -euo pipefail

QUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RADICE="$(cd "$QUI/.." && pwd)"
AMB="$RADICE/ambiente"
VENV="$AMB/venv"
UV="${UV:-$HOME/.local/bin/uv}"
PY="${PYTHON_AMBIENTE:-/usr/bin/python3}"

[ "$(basename "$RADICE")" = "f10-dati" ] || { echo "ERRORE: lo script deve stare in f10-dati/03-infrastruttura" >&2; exit 2; }
[ -x "$UV" ] || { echo "ERRORE: uv non trovato in $UV" >&2; exit 2; }
mkdir -p "$AMB"

# Tutto ciò che uv scrive resta dentro f10-dati/ambiente.
export UV_CACHE_DIR="$AMB/cache-uv"
export UV_PYTHON_INSTALL_DIR="$AMB/python-uv"
export UV_PYTHON_BIN_DIR="$AMB/python-uv/bin"
export UV_NO_CONFIG=1
export UV_LINK_MODE=copy
export UV_NO_PROGRESS=1

if [ ! -x "$VENV/bin/python" ]; then
  timeout 300 "$UV" venv "$VENV" --python "$PY" --no-project
else
  echo "ambiente già presente: $("$VENV/bin/python" -I -c 'import sys; print(sys.version.split()[0])')"
fi

if [ ! -f "$QUI/requisiti.txt" ]; then
  # Prima volta: si risolvono le versioni e si congelano con le impronte. Solo ruote già compilate.
  ( cd "$QUI" && timeout 300 "$UV" pip compile requisiti.in --python "$VENV/bin/python" \
    --only-binary :all: --generate-hashes --no-header -o requisiti.txt )
fi

# Riallinea l'ambiente ai requisiti congelati, verificando le impronte di ogni ruota.
timeout 300 "$UV" pip sync "$QUI/requisiti.txt" --python "$VENV/bin/python" \
  --only-binary :all: --require-hashes

"$VENV/bin/python" -I - <<'EOF'
import importlib, sys
print("interprete:", sys.executable, sys.version.split()[0])
for nome in ("numpy", "scipy", "cv2", "PIL", "rosbags"):
    m = importlib.import_module(nome)
    print(f"  {nome:8s} {getattr(m, '__version__', '(senza __version__)')}")
EOF
echo "OK: ambiente pronto in $VENV"
