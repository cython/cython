# mode: compile
# tag: test_in_limited_api
import cython

@cython.cclass
class BuiltinRef:
    cython.declare(pybuf = 'Py_buffer')
