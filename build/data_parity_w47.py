# -*- coding: utf-8 -*-
# Discovery wave 47 (2026-10-29): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w39_*.py. Sources: research/sources-w47.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w47_admiral-t.py","w47_burn-brain-jolly.py","w47_dexterman.py","w47_diyoute.py","w47_keros-n.py","w47_konshens.py","w47_nailah-blackman.py","w47_natoxie.py","w47_nicy.py","w47_patrice-roberts.py","w47_wawa.py"]

PAGES = [_part(n).FR for n in _PARTS]
