# -*- coding: utf-8 -*-
# Discovery wave 45 (2026-10-29): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w39_*.py. Sources: research/sources-w45.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w45_dj-eyedol.py","w45_gg3.py","w45_halibut.py","w45_king-kembe.py","w45_soca-ras.py","w45_subance.py","w45_zamoni.py"]

PAGES = [_part(n).FR for n in _PARTS]
