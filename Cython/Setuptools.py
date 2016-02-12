from Cython.Build import cythonize
from setuptools import Command


def cython_modules(dist, attr, value):
    assert attr == 'cython_modules'

    if not dist.ext_modules:
        dist.ext_modules = []

    dist.ext_modules += cythonize(value, replace_extension=True)


def cython_manual_modules(dist, attr, value):
    pass


class BuildPyx(Command):
    description = 'Cythonize PYX sources'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            cythonize(
                self.distribution.cython_manual_modules,
                replace_extension=True
            )
        except AttributeError:
            pass
