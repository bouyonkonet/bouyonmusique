# -*- coding: utf-8 -*-
# Parity wave 1 (2026-10-20): DJ Cut, Dada, Nursery Krew Inc, Bushtown Clan,
# ThaWizZarD, Skinny Banton. FR entries assembled from parity_parts/w1_*.py
# (each part file's header comment lists its sources).
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

PAGES = [_part(n).FR for n in _PARTS]
