# -*- coding: utf-8 -*-
# Discovery wave 39 (2026-10-27): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w39_*.py. Sources: research/sources-w39.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w39_motto.py","w39_tallyboy.py","w39_go-fast.py","w39_general-pye.py","w39_jab-king.py","w39_wetty-beatz.py","w39_sully-jacob.py","w39_vibwoy.py","w39_punz.py","w39_quan-de-artist.py","w39_superk.py","w39_solar-million.py"]

PAGES = [_part(n).FR for n in _PARTS]
