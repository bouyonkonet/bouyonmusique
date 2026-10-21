# -*- coding: utf-8 -*-
# Scene sweep wave 11 EN mirrors (= build wave 29, 2026-10-20).

# Assembled from parity_parts/w29_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w29_bad-gyal-shyanne.py", "w29_sandy-boo.py", "w29_marshee.py", "w29_chioneso.py",
          "w29_chief.py", "w29_lyrical-k.py", "w29_viv-beats.py", "w29_deejay-twix.py"]

PAGES = [_part(n).EN for n in _PARTS]
