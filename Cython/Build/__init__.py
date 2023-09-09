from .Dependencies import cythonize
try:
    from .Distutils import build_ext
except ModuleNotFoundError:
    pass
