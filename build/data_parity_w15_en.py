# -*- coding: utf-8 -*-
# Parity wave 15 EN mirrors (2026-10-20).

# Assembled from parity_parts/w15_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w15_skinny-fabulous.py", "w15_stratvincybwoy.py", "w15_sukie.py", "w15_suppa.py",
          "w15_sweet-ticky.py", "w15_tasmo.py", "w15_tazzy.py", "w15_team-bwe-tou-sa.py"]

PAGES = [_part(n).EN for n in _PARTS]
