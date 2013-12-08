/////////////// FetchCommonType.proto ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);

/////////////// FetchCommonType ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    static PyObject* fake_module = NULL;
    PyTypeObject* cached_type = NULL;
    const char* cython_module = "_cython_" CYTHON_ABI;
    if (!fake_module) {
        fake_module = PyImport_AddModule(cython_module);
        if (!fake_module) goto bad;
    }

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
    // NOTE: always returns owned reference, or NULL on error
    return cached_type;
}
