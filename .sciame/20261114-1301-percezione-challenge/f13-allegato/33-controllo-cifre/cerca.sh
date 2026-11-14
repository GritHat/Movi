#!/bin/sh
# uso: cerca.sh cartella espressione...  (sola lettura)
d="$1"; shift
for e in "$@"; do echo "--- $e"; (cd "$d" && grep -n -o -E ".{0,110}($e).{0,110}" *.tex | cut -c1-330); done
