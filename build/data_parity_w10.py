# -*- coding: utf-8 -*-
# Parity wave 10 (2026-10-20): Kassidje, Keks Mafia, Kenny G (Dominica),
# Kevni, KeyT Zone, Khallion, Killa Laurent, Klockerz Krew.
# FR entries assembled from parity_parts/w10_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w10_kassidje.py", "w10_keks-mafia.py", "w10_kenny-g-dominica.py",
          "w10_kevni.py", "w10_keytzone.py", "w10_khallion.py",
          "w10_killa-laurent.py", "w10_klockerz-krew.py"]

PAGES = [_part(n).FR for n in _PARTS]
