# -*- coding: utf-8 -*-
# Parity wave 9 (2026-10-20): Gaza Crew, Gaza Girls Crew, Haterz BE,
# Hussey, Ignition Band, J Lion, J2MO, Jixels.
# FR entries assembled from parity_parts/w9_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w9_gaza-crew.py", "w9_gaza-girls-crew.py", "w9_haterz-be.py",
          "w9_hussey.py", "w9_ignition-band.py", "w9_j-lion.py",
          "w9_j2mo.py", "w9_jixels.py"]

PAGES = [_part(n).FR for n in _PARTS]
