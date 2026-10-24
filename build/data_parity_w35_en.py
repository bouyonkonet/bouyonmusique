# -*- coding: utf-8 -*-
# Discovery wave 35 (2026-10-23): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w35_*.py. Sources: research/sources-w35.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w35_boogy-rankss.py","w35_dee-zen.py","w35_dj-ramses.py","w35_kentin-fcn.py","w35_malcolm.py","w35_oso-j.py","w35_shawn-storm.py","w35_stalk-ashley.py","w35_ti-al.py"]

PAGES = [_part(n).EN for n in _PARTS]
