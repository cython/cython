from cython.cimports.cpython.version import PY_VERSION_HEX

# Python version >= 3.2 final ?
print(PY_VERSION_HEX >= 0x030200F0)
