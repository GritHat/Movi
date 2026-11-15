"""Importa il nucleo movi_lp.py di f15/04-moto SENZA scrivere nulla nella sua cartella (niente __pycache__)."""
import os
import sys

sys.dont_write_bytecode = True
_M = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "04-moto")
if _M not in sys.path:
    sys.path.insert(0, _M)
from movi_lp import *  # noqa: F401,F403,E402
import movi_lp as nucleo  # noqa: E402,F401
