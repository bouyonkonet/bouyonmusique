# -*- coding: utf-8 -*-
# Scene sweep wave 5 (= build wave 23, 2026-10-20): D.O.C FIX IT,
# Dernel Green, Novy, Banklaady. Empties the named sweep queue.
# FR entries assembled from parity_parts/w23_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w23_doc-fix-it.py", "w23_dernel-green.py", "w23_novy.py", "w23_banklaady.py"]

PAGES = [_part(n).FR for n in _PARTS]
