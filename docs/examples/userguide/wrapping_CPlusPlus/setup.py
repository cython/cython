from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        name="rect",
        sources=["rect.pyx", "Rectangle.cpp"],
        language="c++",
    )
]

setup(
    ext_modules=cythonize(extensions)
)
