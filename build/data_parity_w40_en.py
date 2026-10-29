# -*- coding: utf-8 -*-
# Discovery wave 40 (2026-10-29): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w39_*.py. Sources: research/sources-w40.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w40_blaka-dan.py","w40_hxnter.py","w40_shanna-raymond.py","w40_que.py","w40_king-dice.py","w40_freezy.py","w40_shattah-ayow.py","w40_pumpa.py","w40_fadda-fox.py","w40_kisha-kay.py","w40_ian-stylez.py"]

PAGES = [_part(n).EN for n in _PARTS]
