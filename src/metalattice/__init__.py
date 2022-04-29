"""
MetaLattice
===========
MetaLattice is a python FEM package to model lattice metamaterials.
"""

import os
from . import _version

__version__ = _version.get_versions()['version']

_abaqus_exist: bool = (os.system("abaqus information=versions") == 0)
