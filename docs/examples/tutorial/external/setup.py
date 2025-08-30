from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension("demo",
              sources=["demo.pyx"],
              libraries=["m"]  # Unix-like specific
              )
]

setup(name="Demos",
      ext_modules=cythonize(ext_modules))
