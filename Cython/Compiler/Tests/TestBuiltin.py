import builtins
import json
import subprocess
import sys

from .. import PyrexTypes
from ..Builtin import (
    inferred_method_return_types, find_return_type_of_builtin_method,
    unsafe_compile_time_methods, is_safe_compile_time_method,
    builtin_scope, builtin_types,
)
from ..Symtab import ModuleScope
from ..PyrexTypes import (
    py_object_type,
    KNOWN_PYTHON_BUILTINS_VERSION, KNOWN_PYTHON_BUILTINS,
    uncachable_builtins,
    KNOWN_EXCEPTION_NAMES, exception_supertypes,
)

from ...TestUtils import TimedTest


class TestBuiltinReturnTypes(TimedTest):
    _min_versions = {
        'frozendict': (3, 15, 0, 'alpha', 7),
        'sentinel': (3, 15, 0, 'beta', 1),
    }
    _min_method_versions = {
        'int.is_integer': (3, 12),
    }

    def test_find_return_type_of_builtin_method(self):
        # It's enough to test the method existence in a recent Python that likely has them.
        test_module_scope = ModuleScope('test', None, None)

        for type_name in inferred_method_return_types:
            builtin_type = builtin_scope.lookup(type_name).type
            self._test_return_type_of_builtin_type(builtin_type, test_module_scope)

    def test_find_return_type_of_builtin_method_specialised(self):
        test_module_scope = ModuleScope('test', None, None)

        pos = None
        for type_name in inferred_method_return_types:
            builtin_type = builtin_scope.lookup(type_name).type
            if not builtin_type.supports_container_type:
                continue

            if type_name == 'tuple':
                generic_test_types = [
                    # Avoid C tuples by using at least one Python object type.
                    [py_object_type],
                    [PyrexTypes.c_int_type, py_object_type],
                    [py_object_type, PyrexTypes.c_float_type],
                    [builtin_type, builtin_type, builtin_type, builtin_type],
                ]
            elif type_name in ['dict', 'frozendict']:
                generic_test_types = [
                    [PyrexTypes.c_float_type, PyrexTypes.c_int_type],
                    [PyrexTypes.c_int_type, py_object_type],
                    [py_object_type, py_object_type],
                    [builtin_type, builtin_type],
                    [py_object_type, builtin_type],
                ]
            else:
                generic_test_types = [
                    [PyrexTypes.c_float_type],
                    [PyrexTypes.c_int_type],
                    [py_object_type],
                    [builtin_type],
                ]

            for subscript_types in generic_test_types:
                builtin_type = builtin_type.specialize_here(pos, test_module_scope, subscript_types)
                self._test_return_type_of_builtin_type(builtin_type, test_module_scope)

    def _test_return_type_of_builtin_type(self, builtin_type, test_module_scope):
        container_type = builtin_type.get_container_type() or builtin_type
        methods = inferred_method_return_types[container_type.name]
        type_name = container_type.name

        py_version = sys.version_info
        look_up_methods = py_version >= (3,10)
        pos = py_type = None

        try:
            py_type = getattr(builtins, type_name if type_name != 'unicode' else 'str')
        except AttributeError:
            if sys.version_info >= self._min_versions.get(type_name, ()):
                raise
            look_up_methods = False

        current_subscript_types = builtin_type.subscripted_types if builtin_type.supports_container_type else []

        def parse_subscripted_type(type_string):
            if type_string == 'T':
                return builtin_type
            if type_string == 'I':
                return current_subscript_types[-1] if current_subscript_types else py_object_type
            if type_string == 'K':
                return current_subscript_types[0] if current_subscript_types else py_object_type
            if '[' in type_string:
                origin_type_name, _, subscripted_type_names = type_string[:-1].partition('[')
                subscripted_types = [
                    parse_subscripted_type(t)
                    for t in subscripted_type_names.split(',')
                ]
                parsed_type = builtin_types[origin_type_name]
                if current_subscript_types:
                    return parsed_type.specialize_here(pos, test_module_scope, subscripted_types)
                return parsed_type

            return builtin_types.get(type_string) or PyrexTypes.parse_basic_ctype(type_string)

        for method_name, return_type_name in methods.items():
            fq_method_name = f"{type_name}.{method_name}"
            if look_up_methods and py_version >= self._min_method_versions.get(fq_method_name, py_version):
                self.assertTrue(hasattr(py_type, method_name), fq_method_name)

            actual_return_type = find_return_type_of_builtin_method(
                pos, test_module_scope, builtin_type, method_name)

            expected_return_type = parse_subscripted_type(return_type_name)
            if actual_return_type.is_builtin_type:
                self.assertEqual(actual_return_type.name, expected_return_type.name)

            self.assertEqual(actual_return_type.empty_declaration_code(pyrex=True), expected_return_type.empty_declaration_code(pyrex=True))


class TestBuiltinCompatibility(TimedTest):
    def test_python_builtin_compatibility(self):
        expected_builtins = set(KNOWN_PYTHON_BUILTINS)
        if sys.platform != 'win32':
            expected_builtins.discard("WindowsError")

        # Read builtins from fresh Python process to prevent modifications by test dependencies.
        output = subprocess.run(
            [sys.executable, '-c', 'import builtins, json, sys; sys.stdout.write(json.dumps(dir(builtins)))'],
            capture_output=True,
            encoding='utf8',
        )
        runtime_builtins = frozenset(
            name for name in json.loads(output.stdout)
            if name not in ('__doc__', '__loader__', '__name__', '__package__', '__spec__'))

        if sys.version_info < KNOWN_PYTHON_BUILTINS_VERSION:
            missing_builtins = expected_builtins - runtime_builtins
            if missing_builtins:
                missing_from_uncachable = missing_builtins - set(uncachable_builtins)
                self.assertSetEqual(missing_from_uncachable, set())
                self.skipTest(f'skipping test, older Python release found. Missing builtins: {", ".join(sorted(missing_builtins))}')
            self.skipTest('skipping test, older Python release found.')
        self.assertSetEqual(runtime_builtins, expected_builtins)

    def test_unsafe_compile_time_methods(self):
        """Validate the table of builtin methods that are not safe for compile time evaluation
        against the table of known builtin methods (and their types).
        """
        for builtin_type_name, unsafe_methods in unsafe_compile_time_methods.items():
            self.assertIsInstance(unsafe_methods, set)

            builtin_type = getattr(builtins, builtin_type_name)  # All named types must exist as builtin types.

            known_methods = sorted(
                inferred_method_return_types[builtin_type_name])  # All types are also in "inferred_method_return_types".

            self.assertFalse(unsafe_methods.difference(known_methods))  # Only known methods are listed.

            for method_name in known_methods:
                builtin_method = getattr(builtin_type, method_name, None)
                if builtin_method is None:
                    self.assertIn(method_name, unsafe_methods)  # Non-portable methods are always unsafe.
                    continue


class TestExceptions(TimedTest):
    def test_hierarchy_completeness(self):
        self.assertSetEqual(KNOWN_EXCEPTION_NAMES, set(exception_supertypes.keys()))
        self.assertFalse(KNOWN_EXCEPTION_NAMES - set(KNOWN_PYTHON_BUILTINS))

    def test_parents(self):
        for exc_name, supertype_names in exception_supertypes.items():
            exc_type = getattr(builtins, exc_name, None)
            if exc_type is None:
                # Older Python version?
                self.assertIn(exc_name, uncachable_builtins)
                continue

            for supertype_name in supertype_names:
                supertype = getattr(builtins, supertype_name, None)
                if supertype is None:
                    # Older Python version?
                    self.assertIn(supertype_name, uncachable_builtins)
                    continue

                self.assertTrue(issubclass(exc_type, supertype), (exc_type, supertype))
