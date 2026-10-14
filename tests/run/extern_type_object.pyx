# mode: run
# cython: freethreading_compatible=True

import subprocess
import sys
import textwrap

cdef extern from "Python.h":
    """
    typedef PyObject __Pyx_ExternalListObject;
    typedef PyObject __Pyx_ExternalIntObject;

    static PyTypeObject *__Pyx_ExternTupleType(void) {
        PyObject *type = PySys_GetObject("_cython_extern_type");
        if (type == Py_None) {
            PyErr_SetString(PyExc_RuntimeError, "Cannot load external type");
            return NULL;
        }
        return type ? (PyTypeObject *)type : &PyTuple_Type;
    }
    #define __Pyx_ExternTuple_Type (*__Pyx_ExternTupleType())
    """
    ctypedef extern class unavailable_module.NativeList[object __Pyx_ExternalListObject, type PyList_Type, check_size ignore]:
        pass

    ctypedef extern class unavailable_module.NativeTuple[object PyVarObject, type __Pyx_ExternTuple_Type]:
        pass

    ctypedef extern class __builtin__.py_int[object __Pyx_ExternalIntObject, type PyLong_Type, check_size ignore]:
        pass


def test_static_type():
    """
    A C type object can be used without a corresponding Python module.

    >>> test_static_type()
    """
    assert NativeList is list
    assert NativeTuple is tuple
    assert py_int is int
    assert NativeList((1, 2)) == [1, 2]
    assert NativeTuple([1, 2]) == (1, 2)


def get_types():
    return NativeList, NativeTuple


def test_type_import(mode):
    """
    Borrowed types stay alive; failed imports propagate errors and release refs.

    >>> test_type_import('owned')
    >>> test_type_import('null')
    >>> test_type_import('not_type')
    >>> test_type_import('size')
    """
    code = textwrap.dedent("""
        import gc
        import importlib.util
        import sys
        import weakref

        mode = sys.argv[3]
        reference = None
        if mode == 'owned':
            sys._cython_extern_type = type('BorrowedTuple', (tuple,), {'__slots__': ()})
            reference = weakref.ref(sys._cython_extern_type)
        elif mode == 'null':
            sys._cython_extern_type = None
            error_type = RuntimeError
            error_text = 'Cannot load external type'
        elif mode == 'not_type':
            sys._cython_extern_type = 42
            error_type = TypeError
            error_text = 'is not a type object'
        else:
            sys._cython_extern_type = type('Small', (), {'__slots__': ()})
            reference = weakref.ref(sys._cython_extern_type)
            error_type = ValueError
            error_text = 'size changed'

        spec = importlib.util.spec_from_file_location(sys.argv[1], sys.argv[2])
        module = importlib.util.module_from_spec(spec)
        if mode == 'owned':
            spec.loader.exec_module(module)
            del sys._cython_extern_type
            gc.collect()
            assert reference() is not None, 'Imported type was not kept alive'
            assert module.get_types()[1] is reference()
        else:
            try:
                spec.loader.exec_module(module)
            except error_type as exc:
                assert error_text in str(exc), str(exc)
            else:
                raise AssertionError('Invalid external type was accepted')

            del sys._cython_extern_type
            gc.collect()
            # PyPy's cpyext retains borrowed PySys_GetObject type references.
            if reference is not None and sys.implementation.name == 'cpython':
                assert reference() is None, 'Failed import retained the type'
    """)
    result = subprocess.run(
        [sys.executable, '-c', code, __name__, __file__, mode],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode('utf8', 'replace')
