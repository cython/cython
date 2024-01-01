import unittest

from Cython import Shadow
from Cython.Compiler import Options, CythonScope

class TestShadow(unittest.TestCase):
    def test_all_types_in_shadow(self):
        cython_scope = CythonScope.create_cython_scope(None)
        # Not doing load_cythonscope at this stage because it requires a proper context and
        # Errors.py to be set up

        missing_types = []
        for key in cython_scope.entries.keys():
            if key.startswith('__') and key.endswith('__'):
                continue
            if key in ('PyTypeObject', 'PyObject_TypeCheck'):
                # These are declared in Shadow.py for reasons that look to
                # be an implementation detail, but it isn't our intention for
                # users to access them from Pure Python mode.
                continue
            if not hasattr(Shadow, key):
                missing_types.append(key)
        self.assertEqual(missing_types, [])

    def test_int_types_in_shadow(self):
        missing_types = []
        for int_name in Shadow.int_types:
            for sign in ['', 'u', 's']:
                name = sign + int_name

                if sign and int_name in ['Py_UNICODE', 'Py_UCS4', 'Py_ssize_t', 'size_t']:
                    self.assertNotIn(name, dir(Shadow))
                    self.assertNotIn('p_' + name, dir(Shadow))
                    continue

                if not hasattr(Shadow, name):
                    missing_types.append(name)

                for ptr in range(1, 4):
                    ptr_name = 'p' * ptr + '_' + name
                    if not hasattr(Shadow, ptr_name):
                        missing_types.append(ptr_name)
        self.assertEqual(missing_types, [])

    # TODO - there's a lot of types that are looked up by `cython_scope.lookup_type` that
    # it's unfortunately hard to get a definite list of to confirm that they're present
    # (because they're obtained by on-the-fly string parsing)
