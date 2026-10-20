# -*- coding: utf-8 -*-
# Parity wave 11 EN mirrors (2026-10-20).

# Assembled from parity_parts/w11_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w11_larose.py", "w11_le-bluff.py", "w11_le-dext.py", "w11_legacy-band.py",
          "w11_les-ptits-du-rzt.py", "w11_lestef-kjf-boyz.py",
          "w11_letin-severine.py", "w11_letin-sylia.py"]

PAGES = [_part(n).EN for n in _PARTS]
