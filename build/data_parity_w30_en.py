# -*- coding: utf-8 -*-
# Scene sweep wave 12 EN mirrors (= build wave 30, 2026-10-20).

# Assembled from parity_parts/w30_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w30_krys.py", "w30_nfl-lil-brent.py", "w30_jasse.py", "w30_risingsun.py"]

PAGES = [_part(n).EN for n in _PARTS]
