/////////////// FetchCommonType.proto ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);
#if CYTHON_COMPILING_IN_LIMITED_API
static PyObject* __Pyx_FetchCommonTypeFromSpec(PyType_Spec *spec, PyObject *bases);
#endif

/////////////// FetchCommonType ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    PyObject* fake_module;
    PyTypeObject* cached_type = NULL;

    fake_module = PyImport_AddModule((char*) "_cython_" CYTHON_ABI);
    if (!fake_module) return NULL;
    Py_INCREF(fake_module);

    cached_type = (PyTypeObject*) PyObject_GetAttrString(fake_module, type->tp_name);
    if (cached_type) {
        if (!PyType_Check((PyObject*)cached_type)) {
            PyErr_Format(PyExc_TypeError,
                "Shared Cython type %.200s is not a type object",
                type->tp_name);
            goto bad;
        }
        if (cached_type->tp_basicsize != type->tp_basicsize) {
            PyErr_Format(PyExc_TypeError,
                "Shared Cython type %.200s has the wrong size, try recompiling",
                type->tp_name);
            goto bad;
        }
    } else {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
        PyErr_Clear();
        if (PyType_Ready(type) < 0) goto bad;
        if (PyObject_SetAttrString(fake_module, type->tp_name, (PyObject*) type) < 0)
            goto bad;
        Py_INCREF(type);
        cached_type = type;
    }

done:
    Py_DECREF(fake_module);
    // NOTE: always returns owned reference, or NULL on error
    return cached_type;

bad:
    Py_XDECREF(cached_type);
    cached_type = NULL;
    goto done;
}

#if CYTHON_COMPILING_IN_LIMITED_API
static PyObject *__Pyx_FetchCommonTypeFromSpec(PyType_Spec *spec, PyObject *bases) {
    PyObject *fake_module, *py_basicsize, *cached_type = NULL;
    Py_ssize_t basicsize;

    fake_module = PyImport_AddModule((char *) "_cython_" CYTHON_ABI);
    if (!fake_module) return NULL;
    Py_INCREF(fake_module);

    cached_type = PyObject_GetAttrString(fake_module, spec->name);
    if (cached_type) {
        if (!PyType_Check(cached_type)) {
            PyErr_Format(PyExc_TypeError,
                "Shared Cython type %.200s is not a type object",
                spec->name);
            goto bad;
        }
        py_basicsize = PyObject_GetAttrString(cached_type, "__basicsize__");
        if (!py_basicsize)
            goto bad;
        basicsize = PyLong_AsSsize_t(py_basicsize);
        Py_DECREF(py_basicsize);
        py_basicsize = 0;
        if (basicsize == (Py_ssize_t)-1 && PyErr_Occurred())
            goto bad;
        if (basicsize != spec->basicsize) {
            PyErr_Format(PyExc_TypeError,
                "Shared Cython type %.200s has the wrong size, try recompiling",
                spec->name);
            goto bad;
        }
    } else {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
        PyErr_Clear();
        cached_type = PyType_FromSpecWithBases(spec, bases);
        if (unlikely(!cached_type)) goto bad;
        if (PyObject_SetAttrString(fake_module, spec->name, cached_type) < 0)
            goto bad;
    }

done:
    Py_DECREF(fake_module);
    // NOTE: always returns owned reference, or NULL on error
    return cached_type;

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
    PyObject* fake_module = NULL;
    PyObject* capsule = NULL;
    void* value = NULL;

    fake_module = PyImport_AddModule((char*) "_cython_" CYTHON_ABI);
    if (!fake_module) return NULL;
    Py_INCREF(fake_module);

    capsule = PyObject_GetAttrString(fake_module, name);
    if (!capsule) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
        PyErr_Clear();
        capsule = PyCapsule_New(pointer, name, NULL);
        if (!capsule) goto bad;
        if (PyObject_SetAttrString(fake_module, name, capsule) < 0)
            goto bad;
    }
    value = PyCapsule_GetPointer(capsule, name);

bad:
    Py_XDECREF(capsule);
    Py_DECREF(fake_module);
    return value;
}
