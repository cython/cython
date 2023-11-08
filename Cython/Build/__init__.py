from .Dependencies import cythonize

import sys
del sys


def __getattr__(name):
    if name == 'build_ext':
        # Lazy import, fails if distutils is not available (in Python 3.12+).
        from .Distutils import build_ext
        return build_ext
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
