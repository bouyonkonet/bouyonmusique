# -*- coding: utf-8 -*-
# Parity wave 2 (2026-10-20): Edday, DJ Taffy, Nice, DJ MJ, Fallon, HollyG,
# Lejuh, 1T1. FR entries assembled from parity_parts/w2_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w2_edday.py", "w2_dj-taffy.py", "w2_nice.py", "w2_dj-mj.py",
          "w2_fallon.py", "w2_holly-g.py", "w2_lejuh.py", "w2_1t1.py"]

PAGES = [_part(n).FR for n in _PARTS]
