# -*- coding: utf-8 -*-
# Parity wave 18 (2026-10-20): Xavvoknockin, Yellow Gaza, Youry Fleming,
# YSN, Yu Mei. FINAL parity wave: closes the 142-name roster gap.
# FR entries assembled from parity_parts/w18_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w18_xavvoknockin.py", "w18_yellow-gaza.py", "w18_youry-fleming.py",
          "w18_ysn.py", "w18_yu-mei.py"]

PAGES = [_part(n).FR for n in _PARTS]
