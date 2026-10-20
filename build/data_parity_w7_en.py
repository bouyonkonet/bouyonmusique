# -*- coding: utf-8 -*-
# Parity wave 7 EN mirrors (2026-10-20).

# Assembled from parity_parts/w7_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w7_dj-leguste.py", "w7_dj-luchshiy.py", "w7_dj-skaytah.py",
          "w7_dj-skycee.py", "w7_dj-skylone.py", "w7_dj-softee.py",
          "w7_dj-weez.py", "w7_doc-j.py"]

PAGES = [_part(n).EN for n in _PARTS]
