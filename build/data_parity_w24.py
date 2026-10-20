# -*- coding: utf-8 -*-
# Scene sweep wave 6 (= build wave 24, 2026-10-20, discovery-driven):
# First Serenade Band, RSB, Ncore, Unstoppable Shax, TriSzy, Rudy Ru$h,
# Fr3EzE, Slyme Hoyss.
# FR entries assembled from parity_parts/w24_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w24_first-serenade-band.py", "w24_rsb.py", "w24_ncore.py", "w24_unstoppable-shax.py",
          "w24_triszy.py", "w24_rudy-rush.py", "w24_fr3eze.py", "w24_slyme-hoyss.py"]

PAGES = [_part(n).FR for n in _PARTS]
