from distutils.core import setup
from Cython.Build import cythonize

directives = {
    'optimize.inline_defnode_calls': True
}

setup(
  name = 'benchmarks',
  ext_modules = cythonize("*.py", language_level=3, annotate=True,
                          compiler_directives=directives,
                          exclude=["setup.py"]),
)
