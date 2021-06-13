from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        ['primes.py',                   # Cython code file with primes() function
         'primes_python_compiled.py'],  # Python code file with primes() function
        annotate=True),                 # enables generation of the html annotation file
)
