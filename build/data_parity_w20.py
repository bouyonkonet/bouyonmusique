# -*- coding: utf-8 -*-
# Scene sweep wave 2 (= build wave 20, 2026-10-20): Tedla, D.O.C FIX DEM,
# Young Dinero, Starsha, Kai Du M, Nensha, Malko, Mopao Mumu.
# FR entries assembled from parity_parts/w20_*.py.
# Coordinator QC at assembly: Nensha schema trimmed to the 1 Shazam-verified
# track (aggregator-only titles stay as attributed text mentions); Starsha
# rendered text holds Dada's full published name pending confirmation
# (the Dada production credit stands; name kept in the part's research header).
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w20_tedla.py", "w20_doc-fix-dem.py", "w20_young-dinero.py", "w20_starsha.py",
          "w20_kai-du-m.py", "w20_nensha.py", "w20_malko.py", "w20_mopao-mumu.py"]

PAGES = [_part(n).FR for n in _PARTS]
