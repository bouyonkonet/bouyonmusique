# -*- coding: utf-8 -*-
# Parity wave 14 (2026-10-20): Problem Child, Quan, Qwann, Real Reel,
# Riddim Knockaz, Riddla, Rohie, Shanika.
# FR entries assembled from parity_parts/w14_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w14_problem-child.py", "w14_quan.py", "w14_qwann.py", "w14_real-reel.py",
          "w14_riddim-knockaz.py", "w14_riddla.py", "w14_rohie.py", "w14_shanika.py"]

PAGES = [_part(n).FR for n in _PARTS]
