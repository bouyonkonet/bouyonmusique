# -*- coding: utf-8 -*-
# Discovery wave 32 (2026-10-23): new artist profiles, opened-primary-source standard.
# FR entries assembled from parity_parts/w32_*.py. Sources: research/sources-w32.md
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w32_bobo-bantan.py","w32_cbgyvngsta.py","w32_devon-george.py","w32_dpeng.py","w32_eks.py","w32_ezee-wmn.py","w32_fetty-mark.py","w32_fifin.py","w32_green-apple.py","w32_heidy.py","w32_king-tipsy.py","w32_klass-money.py","w32_ktb.py","w32_madamezelle.py","w32_og-park.py","w32_redpunchdrip.py","w32_rum-lawd.py","w32_shemmy-j.py","w32_soca-inferno.py","w32_strosey.py","w32_timii-mignonne.py","w32_umpa.py","w32_wotlis.py"]

PAGES = [_part(n).FR for n in _PARTS]
