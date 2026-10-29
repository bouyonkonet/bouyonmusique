# -*- coding: utf-8 -*-
# Discovery wave 46 (2026-10-29): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w39_*.py. Sources: research/sources-w46.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w46_clint-h.py","w46_daly.py","w46_esclav.py","w46_ghetto-princess.py","w46_keith-goddard.py","w46_kross-vybez.py","w46_pahjo.py","w46_raw-redeem.py","w46_sa-sa-sammy.py","w46_soca-johnny.py","w46_tete-garcon.py"]

PAGES = [_part(n).FR for n in _PARTS]
