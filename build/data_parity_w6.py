# -*- coding: utf-8 -*-
# Parity wave 6 (2026-10-20): Deejay Guyguy, Denden, Derek Rah Peters,
# Diixly, Dinho, DJ Boko, Dj Dirtee, DJ Joe.
# FR entries assembled from parity_parts/w6_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w6_deejay-guyguy.py", "w6_denden.py", "w6_derek-rah-peters.py",
          "w6_diixly.py", "w6_dinho.py", "w6_dj-boko.py",
          "w6_dj-dirtee.py", "w6_dj-joe.py"]

PAGES = [_part(n).FR for n in _PARTS]
