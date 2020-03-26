from distutils import core, version

__name__='distutils.core.cytest_relativeimport_T542' # fool Python we are in distutils
__package__='distutils.core' # fool Python we are in distutils

from . import *

__doc__ = """
>>> core.setup == setup
True
"""
