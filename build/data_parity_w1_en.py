# -*- coding: utf-8 -*-
# Parity wave 1 EN mirrors (2026-10-20). Assembled from parity_parts/w1_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w1_dj-cut.py", "w1_dada.py", "w1_nursery-krew-inc.py",
          "w1_bushtown-clan.py", "w1_tha-wizzard.py", "w1_skinny-banton.py"]

PAGES = [_part(n).EN for n in _PARTS]
