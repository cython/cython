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


class new_build_ext(_build_ext, object):

    user_options = _build_ext.user_options + [
        ('c-build-dir=', None, "directory for generated c files"),
    ]

    def initialize_options(self):
        _build_ext.initialize_options(self)
        self.c_build_dir = None

    def finalize_options(self):
        if self.distribution.ext_modules:
            nthreads = getattr(self, 'parallel', None)  # -j option in Py3.5+
            nthreads = int(nthreads) if nthreads else None
            from Cython.Build.Dependencies import cythonize
            self.distribution.ext_modules[:] = cythonize(
                self.distribution.ext_modules, nthreads=nthreads,
                force=self.force, quiet=self.verbose == 0, build_dir=self.c_build_dir)
        super(new_build_ext, self).finalize_options()

# This will become new_build_ext in the future.
from .old_build_ext import old_build_ext as build_ext
