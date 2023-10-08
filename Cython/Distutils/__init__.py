import sys
if sys.version_info > (3, 11):
    try:
        import setuptools
    except ImportError:
        raise ImportError(
            "Missing optional dependency 'setuptools'. "
            "Use pip or conda to install setuptools."
        )

del sys

from Cython.Distutils.build_ext import build_ext
from Cython.Distutils.extension import Extension
