import sys
from .Dependencies import cythonize

if 'setuptools' in sys.modules:
    from setuptools.command import build_ext as _build_ext
else:
    from distutils.command import build_ext as _build_ext

class build_ext(_build_ext.build_ext, object):
    def finalize_options(self):
        self.distribution.ext_modules[:] = cythonize(
            self.distribution.ext_modules)
        super(build_ext, self).finalize_options()
