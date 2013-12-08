/////////////// FetchCommonType.proto ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);

/////////////// FetchCommonType ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    PyObject* fake_module;
    PyTypeObject* cached_type = NULL;
    const char* cython_module = "_cython_" CYTHON_ABI;

    fake_module = PyImport_AddModule(cython_module);
    if (!fake_module) return NULL;
    Py_INCREF(fake_module);

    cached_type = (PyTypeObject*) PyObject_GetAttrString(fake_module, type->tp_name);
    if (!cached_type) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
        PyErr_Clear();
        if (PyType_Ready(type) < 0) goto bad;
        if (PyObject_SetAttrString(fake_module, type->tp_name, (PyObject*) type) < 0)
            goto bad;
        Py_INCREF(type);
        cached_type = type;
    }

bad:
    Py_DECREF(fake_module);
    // NOTE: always returns owned reference, or NULL on error
    return cached_type;
}
