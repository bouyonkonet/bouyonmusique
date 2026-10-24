# -*- coding: utf-8 -*-
# Discovery wave 33 (2026-10-23): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w33_*.py. Sources: research/sources-w33.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w33_dj-kwab.py","w33_dj-tkrys.py","w33_keke.py","w33_lms.py","w33_lov-nee.py","w33_magistral-beats.py","w33_riko.py","w33_shashabim.py"]

PAGES = [_part(n).EN for n in _PARTS]
