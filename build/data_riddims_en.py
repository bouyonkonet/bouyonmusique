# -*- coding: utf-8 -*-
# Bouyon riddim pages (2026-10-28): one page per riddim with a sourced tracklist, plus the riddim hub.
# Entries assembled from parity_parts/r01_*.py. Sources: research/riddims/ in the notes repo.
import glob, importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = sorted(glob.glob(os.path.join(_HERE, "parity_parts", "r01_*.py")))
PAGES = [_part(p).EN for p in _PARTS]
