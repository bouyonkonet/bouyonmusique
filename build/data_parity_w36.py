# -*- coding: utf-8 -*-
# Discovery wave 36 (2026-10-23): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w36_*.py. Sources: research/sources-w36.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w36_bajan-balotelli.py","w36_bermixx.py","w36_daddy2sec.py","w36_detal.py","w36_django-de-cayenne.py","w36_dyonte.py","w36_fiddy-ii.py","w36_imran-nerdy.py","w36_jauwan-hadaway.py","w36_jayanti.py","w36_jordan-english.py","w36_kas-matik.py","w36_kenzii-bwa.py","w36_king-low-rider.py","w36_louse-king.py","w36_lyrikal.py","w36_messemupbeats.py","w36_msina.py","w36_queen-paranoya.py","w36_ricardo-drue.py","w36_sharkie.py","w36_spyout.py","w36_stella-billy.py","w36_vghn.py"]

PAGES = [_part(n).FR for n in _PARTS]
