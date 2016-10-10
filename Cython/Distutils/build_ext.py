import sys

if 'setuptools' in sys.modules:
    try:
        from setuptools.command.build_ext import build_ext as _build_ext
    except ImportError:
        # We may be in the process of importing setuptools, which tries
        # to import this.
        from distutils.command.build_ext import build_ext as _build_ext
else:
    from distutils.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext, object):
    def finalize_options(self):
        if self.distribution.ext_modules:
            from Cython.Build.Dependencies import cythonize
            self.distribution.ext_modules[:] = cythonize(
                self.distribution.ext_modules)
        super(build_ext, self).finalize_options()
