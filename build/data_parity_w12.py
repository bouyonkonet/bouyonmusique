# -*- coding: utf-8 -*-
# Parity wave 12 (2026-10-20): Leyou, LGC, Luky Lukee, Lunik, Ma6mo,
# Machel Montano, Major Lazer, Mathieu Richardson.
# FR entries assembled from parity_parts/w12_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w12_leyou.py", "w12_lgc.py", "w12_luky-lukee.py", "w12_lunik.py",
          "w12_ma6mo.py", "w12_machel-montano.py", "w12_major-lazer.py",
          "w12_mathieu-richardson.py"]

PAGES = [_part(n).FR for n in _PARTS]
