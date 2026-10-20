# -*- coding: utf-8 -*-
# Parity wave 5 (2026-10-20): Carlyn XP, Cocotteland, Cornell Phillip,
# Cross Vibes Band, D-Mitri, Daddy Chess, Dcamp, DeeArr.
# FR entries assembled from parity_parts/w5_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w5_carlyn-xp.py", "w5_cocotteland.py", "w5_cornell-phillip.py",
          "w5_cross-vibes-band.py", "w5_d-mitri.py", "w5_daddy-chess.py",
          "w5_dcamp.py", "w5_deearr.py"]

PAGES = [_part(n).FR for n in _PARTS]
