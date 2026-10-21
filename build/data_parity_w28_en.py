# -*- coding: utf-8 -*-
# Scene sweep wave 10 EN mirrors (= build wave 28, 2026-10-20).

# Assembled from parity_parts/w28_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w28_skrazy.py", "w28_dboss.py", "w28_djmk-malachi.py", "w28_dr-eevil.py",
          "w28_sticky.py", "w28_tc.py", "w28_acce-carter.py", "w28_mystrie.py",
          "w28_marf.py", "w28_aderito-depina.py"]

PAGES = [_part(n).EN for n in _PARTS]
