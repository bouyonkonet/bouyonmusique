# -*- coding: utf-8 -*-
# Discovery wave 42 (2026-10-29): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w39_*.py. Sources: research/sources-w42.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w42_frank-white.py","w42_jcro.py","w42_kaution-band.py","w42_kubu.py","w42_nattybill.py","w42_redz.py","w42_shasha.py","w42_starrin.py"]

PAGES = [_part(n).EN for n in _PARTS]
