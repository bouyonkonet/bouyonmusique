# -*- coding: utf-8 -*-
# Scene sweep wave 7 (= build wave 25, 2026-10-20, discovery-driven):
# DJ Wizz767, DJ Flip Tha Boss, ScarnX, Avatar Omish, Don Lash, Pa Pel,
# Pryhmex, Klassik Frescobar.
# FR entries assembled from parity_parts/w25_*.py.
import importlib.util, os

_HERE = os.path.dirname(os.path.abspath(__file__))

def _part(name):
    path = os.path.join(_HERE, "parity_parts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

_PARTS = ["w25_dj-wizz767.py", "w25_dj-flip-tha-boss.py", "w25_scarnx.py", "w25_avatar-omish.py",
          "w25_don-lash.py", "w25_pa-pel.py", "w25_pryhmex.py", "w25_klassik-frescobar.py"]

PAGES = [_part(n).FR for n in _PARTS]
