from Cython.Build import cythonize

def cython_modules(dist, attr, value):
    assert attr == 'cython_modules'

    if not dist.ext_modules:
        dist.ext_modules = []

    dist.ext_modules += cythonize(value)
