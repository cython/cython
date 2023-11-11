import unittest

from Cython import Shadow
from Cython.Compiler import Options, CythonScope

class TestShadow(unittest.TestCase):
    def test_all_directives_in_shadow(self):
        missing_directives = []
        extra_directives = []
        for full_directive in Options.directive_types.keys():
            # Python 2 doesn't support "directive, *rest = full_directive.split('.')"
            split_directive = full_directive.split('.')
            directive, rest = split_directive[0], split_directive[1:]

            scope = Options.directive_scopes.get(full_directive)
            if scope and len(scope) == 1 and scope[0] == "module":
                # module-scoped things can't be used from Cython
                if hasattr(Shadow, directive):
                    extra_directives.append(full_directive)
                continue
            if full_directive == "collection_type":
                # collection_type is current restricted to utility code only
                # so doesn't need to be in Shadow
                continue
            if full_directive == "staticmethod":
                # staticmethod is a weird special-case and not really intended to be
                # used from the cython module
                continue

            if not hasattr(Shadow, directive):
                missing_directives.append(full_directive)
            elif rest:
                directive_value = getattr(Shadow, directive)
                for subdirective in rest:
                    if (hasattr(type(directive_value), '__getattr__') or
                            hasattr(type(directive_value), '__getattribute__')):
                        # skip things like "dataclasses" which override attribute lookup
                        break
        self.assertEqual(missing_directives, [])
        self.assertEqual(extra_directives, [])

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

    # TODO - there's a lot of types that are looked up by `cython_scope.lookup_type` that
    # it's unfortunately hard to get a definite list of to confirm that they're present
    # (because they're obtained by on-the-fly string parsing)
