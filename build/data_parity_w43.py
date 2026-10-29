# -*- coding: utf-8 -*-
# Discovery wave 43 (2026-10-29): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w39_*.py. Sources: research/sources-w43.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w43_arden-p.py","w43_deluxe-f.py","w43_fucha-kid.py","w43_jl8.py","w43_kanna.py","w43_mr-vegas.py","w43_sick-tonez.py","w43_sky-geez.py","w43_supaman-enskred.py","w43_zi.py"]

PAGES = [_part(n).FR for n in _PARTS]
