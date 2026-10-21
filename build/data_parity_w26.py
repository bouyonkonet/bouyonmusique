# -*- coding: utf-8 -*-
# Scene sweep wave 8 (= build wave 26, 2026-10-20, discovery-driven):
# Xs Groove, Boston Chery, Shazdown Mmw, DJ Demafidem.
# FR entries assembled from parity_parts/w26_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w26_xs-groove.py", "w26_boston-chery.py", "w26_shazdown-mmw.py", "w26_dj-demafidem.py"]

PAGES = [_part(n).FR for n in _PARTS]
