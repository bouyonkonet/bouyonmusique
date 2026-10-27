# -*- coding: utf-8 -*-
# Discovery wave 38 (2026-10-27): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w38_*.py. Sources: research/sources-w38.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w38_mv-on-de-keys.py","w38_candy.py","w38_dj-kalli.py","w38_th3rd.py","w38_magikal.py","w38_big-red-hd.py","w38_ac-tafari.py","w38_daddy-keyz.py","w38_noface-beatz.py","w38_dj-sleem.py","w38_dj-snow.py"]

PAGES = [_part(n).EN for n in _PARTS]
