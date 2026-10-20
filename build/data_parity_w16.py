# -*- coding: utf-8 -*-
# Parity wave 16 (2026-10-20): Ted La, Tehilah, Tenslay, Teyma, Theodora,
# Theomaa, The SMS Girls, Tolly Boys.
# FR entries assembled from parity_parts/w16_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w16_ted-la.py", "w16_tehilah.py", "w16_tenslay.py", "w16_teyma.py",
          "w16_theodora.py", "w16_theomaa.py", "w16_thesmsgirls.py", "w16_tolly-boys.py"]

PAGES = [_part(n).FR for n in _PARTS]
