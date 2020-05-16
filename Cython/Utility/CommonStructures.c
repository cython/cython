/////////////// FetchCommonType.proto ///////////////

#if !CYTHON_USE_TYPE_SPECS
static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);
#else
static PyTypeObject* __Pyx_FetchCommonTypeFromSpec(PyType_Spec *spec, PyObject *bases);
#endif

/////////////// FetchCommonType ///////////////

static PyObject *__Pyx_FetchSharedCythonABIModule(void) {
    PyObject *abi_module = PyImport_AddModule((char*) __PYX_ABI_MODULE_NAME);
    if (!abi_module) return NULL;
    Py_INCREF(abi_module);
    return abi_module;
}

static int __Pyx_VerifyCachedType(PyObject *cached_type,
                               const char *name,
                               Py_ssize_t basicsize,
                               Py_ssize_t expected_basicsize) {
    if (!PyType_Check(cached_type)) {
        PyErr_Format(PyExc_TypeError,
            "Shared Cython type %.200s is not a type object", name);
        return -1;
    }
    if (basicsize != expected_basicsize) {
        PyErr_Format(PyExc_TypeError,
            "Shared Cython type %.200s has the wrong size, try recompiling",
            name);
        return -1;
    }
    return 0;
}

#if !CYTHON_USE_TYPE_SPECS
static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    PyObject* abi_module;
    PyTypeObject *cached_type = NULL;

    abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!abi_module) return NULL;
    cached_type = (PyTypeObject*) PyObject_GetAttrString(abi_module, type->tp_name);
    if (cached_type) {
        if (__Pyx_VerifyCachedType(
              (PyObject *)cached_type,
              type->tp_name,
              cached_type->tp_basicsize,
              type->tp_basicsize) < 0) {
            goto bad;
        }
        goto done;
    }

    if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
    PyErr_Clear();
    if (PyType_Ready(type) < 0) goto bad;
    if (PyObject_SetAttrString(abi_module, type->tp_name, (PyObject *)type) < 0)
        goto bad;
    Py_INCREF(type);
    cached_type = type;

done:
    Py_DECREF(abi_module);
    // NOTE: always returns owned reference, or NULL on error
    return cached_type;

bad:
    Py_XDECREF(cached_type);
    cached_type = NULL;
    goto done;
}
#else

#if PY_VERSION_HEX < 0x030900A1
#include <string.h>
#endif

static PyTypeObject *__Pyx_FetchCommonTypeFromSpec(PyType_Spec *spec, PyObject *bases) {
    PyObject *abi_module, *cached_type = NULL;

    abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!abi_module) return NULL;

    cached_type = PyObject_GetAttrString(abi_module, spec->name);
    if (cached_type) {
        Py_ssize_t basicsize;
#if CYTHON_COMPILING_IN_LIMITED_API
        PyObject *py_basicsize;
        py_basicsize = PyObject_GetAttrString(cached_type, "__basicsize__");
        if (unlikely(!py_basicsize)) goto bad;
        basicsize = PyLong_AsSsize_t(py_basicsize);
        Py_DECREF(py_basicsize);
        py_basicsize = 0;
        if (unlikely(basicsize == (Py_ssize_t)-1) && PyErr_Occurred()) goto bad;
#else
        basicsize = likely(PyType_Check(cached_type)) ? ((PyTypeObject*) cached_type)->tp_basicsize : -1;
#endif
        if (__Pyx_VerifyCachedType(
              cached_type,
              spec->name,
              basicsize,
              spec->basicsize) < 0) {
            goto bad;
        }
        goto done;
    }

    if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
    PyErr_Clear();
    cached_type = PyType_FromSpecWithBases(spec, bases);
    if (unlikely(!cached_type)) goto bad;

    #if PY_VERSION_HEX < 0x030900A1 && !CYTHON_COMPILING_IN_LIMITED_API
    // Set tp_weakreflist, tp_dictoffset, tp_vectorcalloffset
    // Copied and adapted from https://bugs.python.org/issue38140
    {
        const PyType_Slot *slot = spec->slots;
        while (slot && slot->slot && slot->slot != Py_tp_members)
            slot++;
        if (slot && slot->slot == Py_tp_members) {
            const PyMemberDef *memb = (PyMemberDef*) slot->pfunc;
            while (memb && memb->name) {
                if (memb->name[0] == '_' && memb->name[1] == '_') {
                    if (strcmp(memb->name, "__weaklistoffset__") == 0) {
                        printf("Setting tp_weaklistoffset for %s\n", spec->name);
                        // The PyMemberDef must be a Py_ssize_t and readonly
                        assert(memb->type == T_PYSSIZET);
                        assert(memb->flags == READONLY);
                        ((PyTypeObject *)cached_type)->tp_weaklistoffset = memb->offset;
                        PyType_Modified(((PyTypeObject *)cached_type));
                    }
                    else if (strcmp(memb->name, "__dictoffset__") == 0) {
                        printf("Setting tp_dictoffset for %s\n", spec->name);
                        // The PyMemberDef must be a Py_ssize_t and readonly
                        assert(memb->type == T_PYSSIZET);
                        assert(memb->flags == READONLY);
                        ((PyTypeObject *)cached_type)->tp_dictoffset = memb->offset;
                        PyType_Modified(((PyTypeObject *)cached_type));
                    }
                    else if (strcmp(memb->name, "__vectorcalloffset__") == 0) {
                        printf("Setting tp_vectorcall_offset for %s\n", spec->name);
                        // The PyMemberDef must be a Py_ssize_t and readonly
                        assert(memb->type == T_PYSSIZET);
                        assert(memb->flags == READONLY);
#if PY_VERSION_HEX >= 0x030800b4
                        ((PyTypeObject *)cached_type)->tp_vectorcall_offset = memb->offset;
#else
                        ((PyTypeObject *)cached_type)->tp_print = (printfunc) memb->offset;
#endif
                        PyType_Modified(((PyTypeObject *)cached_type));
                    }
                }
                memb++;
            }
        }
    }
    #endif

    if (PyObject_SetAttrString(abi_module, spec->name, cached_type) < 0) goto bad;

done:
    Py_DECREF(abi_module);
    // NOTE: always returns owned reference, or NULL on error
    assert(cached_type == NULL || PyType_Check(cached_type));
    return (PyTypeObject *) cached_type;

bad:
    Py_XDECREF(cached_type);
    cached_type = NULL;
    goto done;
}
#endif


/////////////// FetchCommonPointer.proto ///////////////

static void* __Pyx_FetchCommonPointer(void* pointer, const char* name);

/////////////// FetchCommonPointer ///////////////


static void* __Pyx_FetchCommonPointer(void* pointer, const char* name) {
    PyObject* abi_module = NULL;
    PyObject* capsule = NULL;
    void* value = NULL;

    abi_module = PyImport_AddModule((char*) __PYX_ABI_MODULE_NAME);
    if (!abi_module) return NULL;
    Py_INCREF(abi_module);

    capsule = PyObject_GetAttrString(abi_module, name);
    if (!capsule) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
        PyErr_Clear();
        capsule = PyCapsule_New(pointer, name, NULL);
        if (!capsule) goto bad;
        if (PyObject_SetAttrString(abi_module, name, capsule) < 0)
            goto bad;
    }
    value = PyCapsule_GetPointer(capsule, name);

bad:
    Py_XDECREF(capsule);
    Py_DECREF(abi_module);
    return value;
}
