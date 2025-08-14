# mode: run
# tag: module_state_utility_code

# cython: language_level=3

# Currently this test only checks the adding/removal of modules
# and not the thread safety.

from cpython.ref cimport PyObject
from libc.stdint cimport int64_t

cdef extern from *:
    ctypedef struct __Pyx_ModuleStateLookupData:
        pass

    __Pyx_ModuleStateLookupData* __Pyx_ModuleStateLookup_allocate_for_tests() except NULL
    void __Pyx_ModuleStateLookup_free_for_tests(__Pyx_ModuleStateLookupData*)
    PyObject *__Pyx_ModuleStateLookup_FindModule(__Pyx_ModuleStateLookupData*, int64_t)
    int __Pyx_ModuleStateLookup_AddModule(__Pyx_ModuleStateLookupData*, int64_t, PyObject*) except -1
    int __Pyx_ModuleStateLookup_RemoveModule(__Pyx_ModuleStateLookupData*, int64_t) except -1


def test_module0():
    """
    >>> test_module0()
    """
    data = __Pyx_ModuleStateLookup_allocate_for_tests();
    try:
        assert __Pyx_ModuleStateLookup_FindModule(data, 0) == NULL

        example_mod = object()
        __Pyx_ModuleStateLookup_AddModule(data, 0, <PyObject*>example_mod)
        assert __Pyx_ModuleStateLookup_FindModule(data, 0) == <PyObject*>example_mod

        __Pyx_ModuleStateLookup_RemoveModule(data, 0)
        assert __Pyx_ModuleStateLookup_FindModule(data, 0) == NULL
    finally:
        __Pyx_ModuleStateLookup_free_for_tests(data)


def test_add_modules():
    """
    >>> test_add_modules()
    """
    data = __Pyx_ModuleStateLookup_allocate_for_tests();
    try:
        modules = [object() for _ in range(500)]
        for n, module in enumerate(modules):
            assert __Pyx_ModuleStateLookup_FindModule(data, n) == NULL
            __Pyx_ModuleStateLookup_AddModule(data, n, <PyObject*>module)

        for n, module in enumerate(modules):
            assert __Pyx_ModuleStateLookup_FindModule(data, n) == <PyObject*>module
    finally:
        __Pyx_ModuleStateLookup_free_for_tests(data)


def test_remove_modules():
    """
    test_remove_modules()
    """
    data = __Pyx_ModuleStateLookup_allocate_for_tests();
    try:
        modules = [object() for _ in range(500)]
        for n, module in enumerate(modules):
            try:
                __Pyx_ModuleStateLookup_RemoveModule(data, n)
            except SystemError:
                pass  # expected
            else:
                assert False, "Didn't raise SystemError"
            __Pyx_ModuleStateLookup_AddModule(data, n, <PyObject*>module)

        for n, module in range(len(modules)):
            __Pyx_ModuleStateLookup_RemoveModule(data, n)
        for n, module in range(len(modules)):
            assert __Pyx_ModuleStateLookup_FindModule(data, n) == NULL
    finally:
        __Pyx_ModuleStateLookup_free_for_tests(data)


def test_random_add_removal(state=None):
    """
    The state argument is to help debugging test failures.
    On failure this function will print the initial state.
    To debug it, modify the call to pass that state in.

    >>> test_random_add_removal()
    """
    import random

    generator = random.Random()
    if state is not None:
        generator.setstate(state)
    initial_state = generator.getstate()

    data = __Pyx_ModuleStateLookup_allocate_for_tests();
    try:
        removed_modules = {n: object() for n in range(50)}
        added_modules = {}

        def do(mode):
            if mode == "add":
                count_to_add = generator.randint(0, len(removed_modules))
                ids_to_add = generator.sample(list(removed_modules.keys()), count_to_add)
                for id in ids_to_add:
                    m = removed_modules.pop(id)
                    __Pyx_ModuleStateLookup_AddModule(data, id, <PyObject*>m)
                    added_modules[id] = m
            elif mode == "remove":
                count_to_remove = generator.randint(0, len(added_modules))
                ids_to_remove = generator.sample(list(added_modules.keys()), count_to_remove)
                for id in ids_to_remove:
                    m = added_modules.pop(id)
                    __Pyx_ModuleStateLookup_RemoveModule(data, id)
                    removed_modules[id] = m
            elif mode == "check":
                for id, m in added_modules.items():
                    assert __Pyx_ModuleStateLookup_FindModule(data, id) == <PyObject*>m
                for id, m in removed_modules.items():
                    assert __Pyx_ModuleStateLookup_FindModule(data, id) == NULL
            else:
                assert False, mode

        mode = "add"

        for count in range(100):
            do(mode)

            mode = generator.choices(
                ("add", "remove", "check"),
                (0.45, 0.45, 0.1),
            )[0]

        do("check")

    except:
        # Make debugging a little easier
        raise RuntimeError(f"Failed: state {initial_state}")
    finally:
        __Pyx_ModuleStateLookup_free_for_tests(data)
