# -*- coding: utf-8 -*-
# Discovery wave 44 (2026-10-29): new artist profiles, opened-primary-source standard.
# EN entries assembled from parity_parts/w39_*.py. Sources: research/sources-w44.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w44_bkz.py","w44_orgixx.py","w44_ransom-beatz.py","w44_tmx-official.py","w44_vibez-productionz.py","w44_yawiar.py"]

PAGES = [_part(n).EN for n in _PARTS]
