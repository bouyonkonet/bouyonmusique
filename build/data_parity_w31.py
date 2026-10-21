# -*- coding: utf-8 -*-
# Scene sweep wave 13 (= build wave 31, 2026-10-20, discovery-driven):
# Supatronic (final sweep profile at the opened-source standard).
# FR entries assembled from parity_parts/w31_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w31_supatronic.py"]

PAGES = [_part(n).FR for n in _PARTS]
