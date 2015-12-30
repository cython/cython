from Cython.Build import cythonize

def cython_modules(dist, attr, value):
    assert attr == 'cython_modules'

    if dist.ext_modules:
        raise ValueError(
            "You may not set both ext_modules and cython_modules keyword "
            "arguments. Aborting."
        )

    dist.ext_modules = cythonize(value)
