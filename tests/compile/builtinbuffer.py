# mode: compile
import cython

@cython.cclass
class BuiltinRef:
    cython.declare(pybuf = 'Py_buffer')

