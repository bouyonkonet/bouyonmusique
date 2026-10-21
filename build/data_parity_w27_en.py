# -*- coding: utf-8 -*-
# Scene sweep wave 9 EN mirrors (= build wave 27, 2026-10-20).

# Assembled from parity_parts/w27_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w27_tazzo-thaboss.py", "w27_baps.py", "w27_d4a-nillio.py", "w27_young-ob.py",
          "w27_lu-city.py", "w27_dj-killerz.py", "w27_pslbeat.py", "w27_alpha.py", "w27_blicassty.py"]

PAGES = [_part(n).EN for n in _PARTS]
