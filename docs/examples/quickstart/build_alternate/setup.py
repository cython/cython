from setuptools import setup

setup(
    name='Hello world app',
    cython_modules="hello.pyx",
    setup_requires=['cython'],
    zip_safe=False,
)
