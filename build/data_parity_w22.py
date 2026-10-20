# -*- coding: utf-8 -*-
# Scene sweep wave 4 (= build wave 22, 2026-10-20): Alkpote, Chronic Law,
# Le Daah, Gringo Jay, Foxy Jael, Le Rebelle, Kwib La Beats, Corane Vincent.
# FR entries assembled from parity_parts/w22_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w22_alkpote.py", "w22_chronic-law.py", "w22_le-daah.py", "w22_gringo-jay.py",
          "w22_foxy-jael.py", "w22_le-rebelle.py", "w22_kwib-la-beats.py", "w22_corane-vincent.py"]

PAGES = [_part(n).FR for n in _PARTS]
