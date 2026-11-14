#!/usr/bin/env bash
# uso: cerca.sh FILE_DI_TESTO 'espressione' [N]  — stampa i contesti delle frasi cercate nel testo scaricato
f="$1"; e="$2"; n="${3:-4}"; echo "== $(basename "$f") :: $e"
tr '\n' ' ' < "$f" | grep -i -o -E ".{0,140}($e).{0,170}" | head -"$n"
