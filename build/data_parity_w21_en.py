# -*- coding: utf-8 -*-
# Scene sweep wave 3 EN mirrors (= build wave 21, 2026-10-20).

# Assembled from parity_parts/w21_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w21_yuniikbeatz.py", "w21_poyzin.py", "w21_ti-locksee.py", "w21_nicolas-macbeth.py",
          "w21_magbeatz.py", "w21_yojoshii.py", "w21_brian-lomba.py", "w21_sonic-art-studios.py"]

PAGES = [_part(n).EN for n in _PARTS]
