/////////////// PyType_Ready.proto ///////////////

// FIXME: is this really suitable for CYTHON_COMPILING_IN_LIMITED_API?
#if CYTHON_COMPILING_IN_CPYTHON || CYTHON_COMPILING_IN_LIMITED_API
static int __Pyx_PyType_Ready(PyTypeObject *t);/*proto*/
#else
#define __Pyx_PyType_Ready(t) PyType_Ready(t)
#endif

/////////////// PyType_Ready ///////////////
//@requires: ObjectHandling.c::PyObjectCallMethod0

#if CYTHON_COMPILING_IN_CPYTHON || CYTHON_COMPILING_IN_LIMITED_API
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
            if (!__Pyx_PyType_HasFeature(b, Py_TPFLAGS_HEAPTYPE))
            {
                __Pyx_TypeName b_name = __Pyx_PyType_GetName(b);
                PyErr_Format(PyExc_TypeError,
                    "base class '" __Pyx_FMT_TYPENAME "' is not a heap type", b_name);
                __Pyx_DECREF_TypeName(b_name);
                return -1;
            }
            if (t->tp_dictoffset == 0 && b->tp_dictoffset)
            {
                __Pyx_TypeName t_name = __Pyx_PyType_GetName(t);
                __Pyx_TypeName b_name = __Pyx_PyType_GetName(b);
                PyErr_Format(PyExc_TypeError,
                    "extension type '" __Pyx_FMT_TYPENAME "' has no __dict__ slot, "
                    "but base type '" __Pyx_FMT_TYPENAME "' has: "
                    "either add 'cdef dict __dict__' to the extension type "
                    "or add '__slots__ = [...]' to the base type",
                    t_name, b_name);
                __Pyx_DECREF_TypeName(t_name);
                __Pyx_DECREF_TypeName(b_name);
                return -1;
            }
        }
    }

#if PY_VERSION_HEX >= 0x03050000
    {
        // Make sure GC does not pick up our non-heap type as heap type with this hack!
        // For details, see https://github.com/cython/cython/issues/3603
        int gc_was_enabled;
    #if PY_VERSION_HEX >= 0x030A00b1
        // finally added in Py3.10 :)
        gc_was_enabled = PyGC_Disable();
        (void)__Pyx_PyObject_CallMethod0;

    #else
        // Call gc.disable() as a backwards compatible fallback, but only if needed.
        PyObject *ret, *py_status;
        PyObject *gc = NULL;
        #if PY_VERSION_HEX >= 0x030700a1 && (!CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM+0 >= 0x07030400)
        // https://foss.heptapod.net/pypy/pypy/-/issues/3385
        gc = PyImport_GetModule(PYUNICODE("gc"));
        #endif
        if (unlikely(!gc)) gc = PyImport_Import(PYUNICODE("gc"));
        if (unlikely(!gc)) return -1;
        py_status = __Pyx_PyObject_CallMethod0(gc, PYUNICODE("isenabled"));
        if (unlikely(!py_status)) {
            Py_DECREF(gc);
            return -1;
        }
        gc_was_enabled = __Pyx_PyObject_IsTrue(py_status);
        Py_DECREF(py_status);
        if (gc_was_enabled > 0) {
            ret = __Pyx_PyObject_CallMethod0(gc, PYUNICODE("disable"));
            if (unlikely(!ret)) {
                Py_DECREF(gc);
                return -1;
            }
            Py_DECREF(ret);
        } else if (unlikely(gc_was_enabled == -1)) {
            Py_DECREF(gc);
            return -1;
        }
    #endif

        // As of https://bugs.python.org/issue22079
        // PyType_Ready enforces that all bases of a non-heap type are
        // non-heap. We know that this is the case for the solid base but
        // other bases are heap allocated and are kept alive through the
        // tp_bases reference.
        // Other than this check, the Py_TPFLAGS_HEAPTYPE flag is unused
        // in PyType_Ready().
        t->tp_flags |= Py_TPFLAGS_HEAPTYPE;
#else
        // avoid C warning about unused helper function
        (void)__Pyx_PyObject_CallMethod0;
#endif

    r = PyType_Ready(t);

#if PY_VERSION_HEX >= 0x03050000
        t->tp_flags &= ~Py_TPFLAGS_HEAPTYPE;

    #if PY_VERSION_HEX >= 0x030A00b1
        if (gc_was_enabled)
            PyGC_Enable();
    #else
        if (gc_was_enabled) {
            PyObject *tp, *v, *tb;
            PyErr_Fetch(&tp, &v, &tb);
            ret = __Pyx_PyObject_CallMethod0(gc, PYUNICODE("enable"));
            if (likely(ret || r == -1)) {
                Py_XDECREF(ret);
                // do not overwrite exceptions raised by PyType_Ready() above
                PyErr_Restore(tp, v, tb);
            } else {
                // PyType_Ready() succeeded, but gc.enable() failed.
                Py_XDECREF(tp);
                Py_XDECREF(v);
                Py_XDECREF(tb);
                r = -1;
            }
        }
        Py_DECREF(gc);
    #endif
    }
#endif

    return r;
}
#endif

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
            reduce_cython = __Pyx_PyObject_GetAttrStrNoError(type_obj, PYIDENT("__reduce_cython__"));
            if (likely(reduce_cython)) {
                ret = PyDict_SetItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__reduce__"), reduce_cython); if (unlikely(ret < 0)) goto __PYX_BAD;
                ret = PyDict_DelItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__reduce_cython__")); if (unlikely(ret < 0)) goto __PYX_BAD;
            } else if (reduce == object_reduce || PyErr_Occurred()) {
                // Ignore if we're done, i.e. if 'reduce' already has the right name and the original is gone.
                // Otherwise: error.
                goto __PYX_BAD;
            }

            setstate = __Pyx_PyObject_GetAttrStrNoError(type_obj, PYIDENT("__setstate__"));
            if (!setstate) PyErr_Clear();
            if (!setstate || __Pyx_setup_reduce_is_named(setstate, PYIDENT("__setstate_cython__"))) {
                setstate_cython = __Pyx_PyObject_GetAttrStrNoError(type_obj, PYIDENT("__setstate_cython__"));
                if (likely(setstate_cython)) {
                    ret = PyDict_SetItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__setstate__"), setstate_cython); if (unlikely(ret < 0)) goto __PYX_BAD;
                    ret = PyDict_DelItem(((PyTypeObject*)type_obj)->tp_dict, PYIDENT("__setstate_cython__")); if (unlikely(ret < 0)) goto __PYX_BAD;
                } else if (!setstate || PyErr_Occurred()) {
                    // Ignore if we're done, i.e. if 'setstate' already has the right name and the original is gone.
                    // Otherwise: error.
                    goto __PYX_BAD;
                }
            }
            PyType_Modified((PyTypeObject*)type_obj);
        }
    }
    goto __PYX_GOOD;

__PYX_BAD:
    if (!PyErr_Occurred()) {
        __Pyx_TypeName type_obj_name =
            __Pyx_PyType_GetName((PyTypeObject*)type_obj);
        PyErr_Format(PyExc_RuntimeError,
            "Unable to initialize pickling for " __Pyx_FMT_TYPENAME, type_obj_name);
        __Pyx_DECREF_TypeName(type_obj_name);
    }
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


/////////////// BinopSlot ///////////////

static CYTHON_INLINE PyObject *{{func_name}}_maybe_call_slot(PyTypeObject* type, PyObject *left, PyObject *right {{extra_arg_decl}}) {
    {{slot_type}} slot;
#if CYTHON_USE_TYPE_SLOTS || PY_MAJOR_VERSION < 3 || CYTHON_COMPILING_IN_PYPY
    slot = type->tp_as_number ? type->tp_as_number->{{slot_name}} : NULL;
#else
    slot = ({{slot_type}}) PyType_GetSlot(type, Py_{{slot_name}});
#endif
    return slot ? slot(left, right {{extra_arg}}) : __Pyx_NewRef(Py_NotImplemented);
}

static PyObject *{{func_name}}(PyObject *left, PyObject *right {{extra_arg_decl}}) {
    int maybe_self_is_left, maybe_self_is_right = 0;
    maybe_self_is_left = Py_TYPE(left) == Py_TYPE(right)
#if CYTHON_USE_TYPE_SLOTS
            || (Py_TYPE(left)->tp_as_number && Py_TYPE(left)->tp_as_number->{{slot_name}} == &{{func_name}})
#endif
            || __Pyx_TypeCheck(left, {{type_cname}});
    // Optimize for the common case where the left operation is defined (and successful).
    if (!({{overloads_left}})) {
        maybe_self_is_right = Py_TYPE(left) == Py_TYPE(right)
#if CYTHON_USE_TYPE_SLOTS
                || (Py_TYPE(right)->tp_as_number && Py_TYPE(right)->tp_as_number->{{slot_name}} == &{{func_name}})
#endif
                || __Pyx_TypeCheck(right, {{type_cname}});
    }
    if (maybe_self_is_left) {
        PyObject *res;
        if (maybe_self_is_right && !({{overloads_left}})) {
            res = {{call_right}};
            if (res != Py_NotImplemented) return res;
            Py_DECREF(res);
            // Don't bother calling it again.
            maybe_self_is_right = 0;
        }
        res = {{call_left}};
        if (res != Py_NotImplemented) return res;
        Py_DECREF(res);
    }
    if (({{overloads_left}})) {
        maybe_self_is_right = Py_TYPE(left) == Py_TYPE(right)
#if CYTHON_USE_TYPE_SLOTS
                || (Py_TYPE(right)->tp_as_number && Py_TYPE(right)->tp_as_number->{{slot_name}} == &{{func_name}})
#endif
                || PyType_IsSubtype(Py_TYPE(right), {{type_cname}});
    }
    if (maybe_self_is_right) {
        return {{call_right}};
    }
    return __Pyx_NewRef(Py_NotImplemented);
}
