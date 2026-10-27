# -*- coding: utf-8 -*-
# Discovery wave 37 (2026-10-27): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w37_*.py. Sources: research/sources-w37.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w37_claudette-peters.py","w37_hb-war.py","w37_r-b-m.py","w37_dalibido-6dl.py"]

PAGES = [_part(n).EN for n in _PARTS]
