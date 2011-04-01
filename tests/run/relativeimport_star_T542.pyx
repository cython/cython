from distutils import core, version
__package__ = 'distutils.core' # fool Python we are in distutils
from . import *

__doc__ = """
>>> core.setup == setup
True
"""
