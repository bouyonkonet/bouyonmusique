# -*- coding: utf-8 -*-
# Discovery wave 34 (2026-10-23): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w34_*.py. Sources: research/sources-w34.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w34_ck-gee.py","w34_djadja.py","w34_le-cus.py","w34_leken-sm.py","w34_le-matt.py","w34_les-curvyzz.py","w34_leseb.py","w34_managyalis.py","w34_see-v.py","w34_sheyta.py","w34_toupit.py","w34_uglyboy.py","w34_yoshy-et-lejo.py","w34_zepek.py"]

PAGES = [_part(n).FR for n in _PARTS]
