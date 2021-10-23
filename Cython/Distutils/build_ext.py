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

    user_options = _build_ext.user_options[:]
    boolean_options = _build_ext.boolean_options[:]

    user_options.extend([
        ('cython-c-in-temp', None,
             "put generated C files in temp directory"),
        ])

    boolean_options.extend([
        'cython-c-in-temp'
    ])

    def initialize_options(self):
        _build_ext.initialize_options(self)
        self.cython_c_in_temp = 0

    def build_extension(self, ext):
        from Cython.Build.Dependencies import cythonize
        if self.cython_c_in_temp:
            build_dir = self.build_temp
        else:
            build_dir = None
        ext = cythonize(ext,force=self.force, quiet=self.verbose == 0, build_dir=build_dir)[0]
        super(new_build_ext, self).build_extension(ext)

# This will become new_build_ext in the future.
from .old_build_ext import old_build_ext as build_ext
