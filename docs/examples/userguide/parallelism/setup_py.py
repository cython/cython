from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "hello",
        ["hello.py"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='hello-parallel-world',
    ext_modules=cythonize(ext_modules),
)
