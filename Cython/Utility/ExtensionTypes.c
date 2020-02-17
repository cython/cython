/////////////// PyType_Ready.proto ///////////////

static int __Pyx_PyType_Ready(PyTypeObject *t);

/////////////// PyType_Ready ///////////////

// Wrapper around PyType_Ready() with some runtime checks and fixes
// to deal with multiple inheritance.
static int __Pyx_PyType_Ready(PyTypeObject *t) {
    // Loop over all bases (except the first) and check that those
    // really are heap types. Otherwise, it would not be safe to
    // subclass them.
    //
    // We also check tp_dictoffset: it is unsafe to inherit
    // tp_dictoffset from a base class because the object structures
    // would not be compatible. So, if our extension type doesn't set
    // tp_dictoffset (i.e. there is no __dict__ attribute in the object
    // structure), we need to check that none of the base classes sets
    // it either.
    int r;
    PyObject *bases = t->tp_bases;
    if (bases)
    {
        Py_ssize_t i, n = PyTuple_GET_SIZE(bases);
        for (i = 1; i < n; i++)  /* Skip first base */
        {
            PyObject *b0 = PyTuple_GET_ITEM(bases, i);
            PyTypeObject *b;
#if PY_MAJOR_VERSION < 3
            /* Disallow old-style classes */
            if (PyClass_Check(b0))
            {
                PyErr_Format(PyExc_TypeError, "base class '%.200s' is an old-style class",
                             PyString_AS_STRING(((PyClassObject*)b0)->cl_name));
                return -1;
            }
#endif
            b = (PyTypeObject*)b0;
            if (!PyType_HasFeature(b, Py_TPFLAGS_HEAPTYPE))
            {
                PyErr_Format(PyExc_TypeError, "base class '%.200s' is not a heap type",
                             b->tp_name);
                return -1;
            }
            if (t->tp_dictoffset == 0 && b->tp_dictoffset)
            {
                PyErr_Format(PyExc_TypeError,
                    "extension type '%.200s' has no __dict__ slot, but base type '%.200s' has: "
                    "either add 'cdef dict __dict__' to the extension type "
                    "or add '__slots__ = [...]' to the base type",
                    t->tp_name, b->tp_name);
                return -1;
            }
        }
    }

#if PY_VERSION_HEX >= 0x03050000
    // As of https://bugs.python.org/issue22079
    // PyType_Ready enforces that all bases of a non-heap type are
    // non-heap. We know that this is the case for the solid base but
    // other bases are heap allocated and are kept alive through the
    // tp_bases reference.
    // Other than this check, the Py_TPFLAGS_HEAPTYPE flag is unused
    // in PyType_Ready().
    t->tp_flags |= Py_TPFLAGS_HEAPTYPE;
#endif

    r = PyType_Ready(t);

#if PY_VERSION_HEX >= 0x03050000
    t->tp_flags &= ~Py_TPFLAGS_HEAPTYPE;
#endif

    return r;
}

/////////////// PyTrashcan.proto ///////////////

// These macros are taken from https://github.com/python/cpython/pull/11841
// Unlike the Py_TRASHCAN_SAFE_BEGIN/Py_TRASHCAN_SAFE_END macros, they
// allow dealing correctly with subclasses.

// This requires CPython version >= 2.7.4
// (or >= 3.2.4 but we don't support such old Python 3 versions anyway)
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x02070400
#define __Pyx_TRASHCAN_BEGIN_CONDITION(op, cond) \
    do { \
        PyThreadState *_tstate = NULL; \
        // If "cond" is false, then _tstate remains NULL and the deallocator
        // is run normally without involving the trashcan
        if (cond) { \
            _tstate = PyThreadState_GET(); \
            if (_tstate->trash_delete_nesting >= PyTrash_UNWIND_LEVEL) { \
                // Store the object (to be deallocated later) and jump past
                // Py_TRASHCAN_END, skipping the body of the deallocator
                _PyTrash_thread_deposit_object((PyObject*)(op)); \
                break; \
            } \
            ++_tstate->trash_delete_nesting; \
        }
        // The body of the deallocator is here.
#define __Pyx_TRASHCAN_END \
        if (_tstate) { \
            --_tstate->trash_delete_nesting; \
            if (_tstate->trash_delete_later && _tstate->trash_delete_nesting <= 0) \
                _PyTrash_thread_destroy_chain(); \
        } \
    } while (0);

#define __Pyx_TRASHCAN_BEGIN(op, dealloc) __Pyx_TRASHCAN_BEGIN_CONDITION(op, \
        Py_TYPE(op)->tp_dealloc == (destructor)(dealloc))

#else
// The trashcan is a no-op on other Python implementations
// or old CPython versions
#define __Pyx_TRASHCAN_BEGIN(op, dealloc)
#define __Pyx_TRASHCAN_END
#endif

/////////////// CallNextTpDealloc.proto ///////////////

static void __Pyx_call_next_tp_dealloc(PyObject* obj, destructor current_tp_dealloc);

/////////////// CallNextTpDealloc ///////////////

static void __Pyx_call_next_tp_dealloc(PyObject* obj, destructor current_tp_dealloc) {
    PyTypeObject* type = Py_TYPE(obj);
    /* try to find the first parent type that has a different tp_dealloc() function */
    while (type && type->tp_dealloc != current_tp_dealloc)
        type = type->tp_base;
    while (type && type->tp_dealloc == current_tp_dealloc)
        type = type->tp_base;
    if (type)
        type->tp_dealloc(obj);
}

/////////////// CallNextTpTraverse.proto ///////////////

static int __Pyx_call_next_tp_traverse(PyObject* obj, visitproc v, void *a, traverseproc current_tp_traverse);

/////////////// CallNextTpTraverse ///////////////

static int __Pyx_call_next_tp_traverse(PyObject* obj, visitproc v, void *a, traverseproc current_tp_traverse) {
    PyTypeObject* type = Py_TYPE(obj);
    /* try to find the first parent type that has a different tp_traverse() function */
    while (type && type->tp_traverse != current_tp_traverse)
        type = type->tp_base;
    while (type && type->tp_traverse == current_tp_traverse)
        type = type->tp_base;
    if (type && type->tp_traverse)
        return type->tp_traverse(obj, v, a);
    // FIXME: really ignore?
    return 0;
}

/////////////// CallNextTpClear.proto ///////////////

static void __Pyx_call_next_tp_clear(PyObject* obj, inquiry current_tp_dealloc);

/////////////// CallNextTpClear ///////////////

static void __Pyx_call_next_tp_clear(PyObject* obj, inquiry current_tp_clear) {
    PyTypeObject* type = Py_TYPE(obj);
    /* try to find the first parent type that has a different tp_clear() function */
    while (type && type->tp_clear != current_tp_clear)
        type = type->tp_base;
    while (type && type->tp_clear == current_tp_clear)
        type = type->tp_base;
    if (type && type->tp_clear)
        type->tp_clear(obj);
}

/////////////// SetupReduce.proto ///////////////

#if !CYTHON_COMPILING_IN_LIMITED_API
static int __Pyx_setup_reduce(PyObject* type_obj);
#endif

/////////////// SetupReduce ///////////////
//@requires: ObjectHandling.c::PyObjectGetAttrStrNoError
//@requires: ObjectHandling.c::PyObjectGetAttrStr
//@substitute: naming

#if !CYTHON_COMPILING_IN_LIMITED_API
static int __Pyx_setup_reduce_is_named(PyObject* meth, PyObject* name) {
  int ret;
  PyObject *name_attr;

  name_attr = __Pyx_PyObject_GetAttrStrNoError(meth, PYIDENT("__name__"));
  if (likely(name_attr)) {
      ret = PyObject_RichCompareBool(name_attr, name, Py_EQ);
  } else {
      ret = -1;
  }

  if (unlikely(ret < 0)) {
      PyErr_Clear();
      ret = 0;
  }

  Py_XDECREF(name_attr);
  return ret;
}

static int __Pyx_setup_reduce(PyObject* type_obj) {
    int ret = 0;
    PyObject *object_reduce = NULL;
    PyObject *object_reduce_ex = NULL;
    PyObject *reduce = NULL;
    PyObject *reduce_ex = NULL;
    PyObject *reduce_cython = NULL;
    PyObject *setstate = NULL;
    PyObject *setstate_cython = NULL;

#if CYTHON_USE_PYTYPE_LOOKUP
    if (_PyType_Lookup((PyTypeObject*)type_obj, PYIDENT("__getstate__"))) goto __PYX_GOOD;
#else
    if (PyObject_HasAttr(type_obj, PYIDENT("__getstate__"))) goto __PYX_GOOD;
#endif

#if CYTHON_USE_PYTYPE_LOOKUP
    object_reduce_ex = _PyType_Lookup(&PyBaseObject_Type, PYIDENT("__reduce_ex__")); if (!object_reduce_ex) goto __PYX_BAD;
#else
    object_reduce_ex = __Pyx_PyObject_GetAttrStr((PyObject*)&PyBaseObject_Type, PYIDENT("__reduce_ex__")); if (!object_reduce_ex) goto __PYX_BAD;
#endif

    reduce_ex = __Pyx_PyObject_GetAttrStr(type_obj, PYIDENT("__reduce_ex__")); if (unlikely(!reduce_ex)) goto __PYX_BAD;
    if (reduce_ex == object_reduce_ex) {

#if CYTHON_USE_PYTYPE_LOOKUP
        object_reduce = _PyType_Lookup(&PyBaseObject_Type, PYIDENT("__reduce__")); if (!object_reduce) goto __PYX_BAD;
#else
        object_reduce = __Pyx_PyObject_GetAttrStr((PyObject*)&PyBaseObject_Type, PYIDENT("__reduce__")); if (!object_reduce) goto __PYX_BAD;
#endif
        reduce = __Pyx_PyObject_GetAttrStr(type_obj, PYIDENT("__reduce__")); if (unlikely(!reduce)) goto __PYX_BAD;

        if (reduce == object_reduce || __Pyx_setup_reduce_is_named(reduce, PYIDENT("__reduce_cython__"))) {
            reduce_cython = __Pyx_PyObject_GetAttrStr(type_obj, PYIDENT("__reduce_cython__")); if (unlikely(!reduce_cython)) goto __PYX_BAD;
            ret = PyDict_SetItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__reduce__"), reduce_cython); if (unlikely(ret < 0)) goto __PYX_BAD;
            ret = PyDict_DelItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__reduce_cython__")); if (unlikely(ret < 0)) goto __PYX_BAD;

            setstate = __Pyx_PyObject_GetAttrStrNoError(type_obj, PYIDENT("__setstate__"));
            if (!setstate) PyErr_Clear();
            if (!setstate || __Pyx_setup_reduce_is_named(setstate, PYIDENT("__setstate_cython__"))) {
                setstate_cython = __Pyx_PyObject_GetAttrStr(type_obj, PYIDENT("__setstate_cython__")); if (unlikely(!setstate_cython)) goto __PYX_BAD;
                ret = PyDict_SetItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__setstate__"), setstate_cython); if (unlikely(ret < 0)) goto __PYX_BAD;
                ret = PyDict_DelItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__setstate_cython__")); if (unlikely(ret < 0)) goto __PYX_BAD;
            }
            PyType_Modified((PyTypeObject*)type_obj);
        }
    }
    goto __PYX_GOOD;

__PYX_BAD:
    if (!PyErr_Occurred())
        PyErr_Format(PyExc_RuntimeError, "Unable to initialize pickling for %s", __Pyx_PyType_Name(type_obj));
    ret = -1;
__PYX_GOOD:
#if !CYTHON_USE_PYTYPE_LOOKUP
    Py_XDECREF(object_reduce);
    Py_XDECREF(object_reduce_ex);
#endif
    Py_XDECREF(reduce);
    Py_XDECREF(reduce_ex);
    Py_XDECREF(reduce_cython);
    Py_XDECREF(setstate);
    Py_XDECREF(setstate_cython);
    return ret;
}
#endif
