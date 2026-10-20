# -*- coding: utf-8 -*-
# Parity wave 13 (2026-10-20): Miky Ding La, Money Shaun, Mr Boka, Mr Delly,
# Mr Gwada, Nessa Preppy, Nils, Pinpin OSP.
# FR entries assembled from parity_parts/w13_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w13_miky-ding-la.py", "w13_money-shaun.py", "w13_mr-boka.py", "w13_mr-delly.py",
          "w13_mr-gwada.py", "w13_nessa-preppy.py", "w13_nils.py", "w13_pinpin-osp.py"]

PAGES = [_part(n).FR for n in _PARTS]
