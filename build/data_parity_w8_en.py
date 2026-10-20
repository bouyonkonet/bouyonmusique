# -*- coding: utf-8 -*-
# Parity wave 8 EN mirrors (2026-10-20).

# Assembled from parity_parts/w8_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w8_dova.py", "w8_ebony-empress.py", "w8_effects-band.py",
          "w8_erwinchy.py", "w8_explosive-band.py", "w8_faithii.py",
          "w8_flw.py", "w8_freddy.py"]

PAGES = [_part(n).EN for n in _PARTS]
