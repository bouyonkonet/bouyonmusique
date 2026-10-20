# -*- coding: utf-8 -*-
# Parity wave 17 EN mirrors (2026-10-20).

# Assembled from parity_parts/w17_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w17_lewismelo.py", "w17_totally-spices.py", "w17_trev-li.py", "w17_trixx.py",
          "w17_trixzmigos.py", "w17_vador.py", "w17_vj-ben.py", "w17_weelow.py"]

PAGES = [_part(n).EN for n in _PARTS]
