# -*- coding: utf-8 -*-
# Parity wave 4 EN mirrors (2026-10-20).

# Assembled from parity_parts/w4_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w4_bilix.py", "w4_billy-bybf.py", "w4_binksdrick.py", "w4_bismok.py",
          "w4_boy-freeze.py", "w4_brg-hollywood.py", "w4_bunji-garlin.py", "w4_c4.py"]

PAGES = [_part(n).EN for n in _PARTS]
