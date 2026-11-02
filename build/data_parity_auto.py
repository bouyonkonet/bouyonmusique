# -*- coding: utf-8 -*-
# Artist profiles added by the Airtable artist-updates pipeline (new artists found by the daily discovery run,
# drafted by Claude, approved by the owner). One file per artist: parity_parts/auto_<slug>.py with FR and EN dicts,
# same shape as the wave parts. Loaded automatically; no generator edit is needed for a new profile.
import glob, importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))


def _load(lang):
    pages = []
    for path in sorted(glob.glob(os.path.join(_HERE, "parity_parts", "auto_*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        pages.append(getattr(m, lang))
    return pages


PAGES = _load("FR")
