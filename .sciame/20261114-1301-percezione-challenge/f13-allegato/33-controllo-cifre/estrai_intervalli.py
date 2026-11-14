#!/usr/bin/env python3
"""Estrae dai .tex ogni intervallo fra parentesi quadre o '(a--b %)' con il contesto. Sola lettura."""
import re,sys,glob,os
d=sys.argv[1]
pat=re.compile(r'(\$?\[[^\]\n]{1,60};[^\]\n]{1,60}\]\$?|\(\d+[,{}\d]*--\d+[,{}\d]*\\,\\%\)|\\ell\^-\s*[=>]\s*[\d{},]+(\\,\\%)?)')
for f in sorted(glob.glob(os.path.join(d,'*.tex'))):
    for i,l in enumerate(open(f,encoding='utf8'),1):
        for m in pat.finditer(l):
            s=max(0,m.start()-110); 
            print(f"{os.path.basename(f)}:{i}: …{l[s:m.end()+15].strip()}…")
