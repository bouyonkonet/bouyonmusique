# -*- coding: utf-8 -*-
# Scene sweep wave 1 (= build wave 19, 2026-10-20): Earlson Matthew,
# D0 Production, Le Det, Laka, Dezod, Judi Silva, Zwady, Fireman Lee.
# FR entries assembled from parity_parts/w19_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w19_earlson-matthew.py", "w19_d0-production.py", "w19_le-det.py", "w19_laka.py",
          "w19_dezod.py", "w19_judi-silva.py", "w19_zwady.py", "w19_fireman-lee.py"]

PAGES = [_part(n).FR for n in _PARTS]
