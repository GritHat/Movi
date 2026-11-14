#!/bin/sh
# compila gli otto eseguibili del banco: sh compila.sh
cd "$(dirname "$0")" || exit 1
mkdir -p bin
for r in POLARE IMMAGINE FASCE DENSA HASH HASHOCC OCTREE OCTPOT COLBIT; do
  gcc -O2 -Wall -Wno-misleading-indentation -Wno-unused-function -Wno-unused-variable -DREP=R_$r banco.c -o bin/banco_$r -lm || exit 1
done
gcc --version | head -1
