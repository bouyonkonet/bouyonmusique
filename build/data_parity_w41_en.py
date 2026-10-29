# -*- coding: utf-8 -*-
# Discovery wave 41 (2026-10-29): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w39_*.py. Sources: research/sources-w41.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w41_caspa-g.py","w41_college-boy-jesse.py","w41_fowko.py","w41_kilogram.py","w41_mad-general.py","w41_major-mystic.py","w41_mikty.py","w41_supalyne.py","w41_zone-rouge.py"]

PAGES = [_part(n).EN for n in _PARTS]
