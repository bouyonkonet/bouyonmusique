# -*- coding: utf-8 -*-
# Parity wave 3 (2026-10-20): A-Plus Muzik, Aknose, All-Star Band,
# Anonymous Gyals, Arendi, Beevo, Benji, Bernard Gumbs (Wizito).
# FR entries assembled from parity_parts/w3_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w3_a-plus-musik.py", "w3_aknose.py", "w3_all-star-band.py",
          "w3_anonymous-gyals.py", "w3_arendi.py", "w3_beevo.py",
          "w3_benji.py", "w3_bernard-gumbs-wizito.py"]

PAGES = [_part(n).FR for n in _PARTS]
