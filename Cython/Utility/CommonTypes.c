/////////////// FetchCommonType.proto ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);

/////////////// FetchCommonType ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    static PyObject* fake_module = NULL;
    PyObject* sys = NULL;
    PyObject* sys_modules = NULL;
    PyObject* args = NULL;
    PyTypeObject* cached_type = NULL;
    char* cython_module = "_cython_" CYTHON_ABI;
    if (fake_module == NULL) {
        sys = PyImport_ImportModule("sys"); if (sys == NULL) goto bad;
        sys_modules = PyObject_GetAttrString(sys, "modules"); if (sys_modules == NULL) goto bad;
        fake_module = PyDict_GetItemString(sys_modules, cython_module);
        if (fake_module != NULL) {
            // borrowed
            Py_INCREF(fake_module);
        } else {
            args = PyTuple_New(1); if (args == NULL) goto bad;
            PyTuple_SET_ITEM(args, 0, __Pyx_PyStr_FromString(cython_module));
            if (PyTuple_GET_ITEM(args, 0) == NULL) goto bad;
            fake_module = PyObject_Call((PyObject*) &PyModule_Type, args, NULL);
            if (PyDict_SetItemString(sys_modules, cython_module, fake_module) < 0)
                goto bad;
        }
    }
    if (PyObject_HasAttrString(fake_module, type->tp_name)) {
        cached_type = (PyTypeObject*) PyObject_GetAttrString(fake_module, type->tp_name);
    } else {
        if (PyType_Ready(type) < 0) goto bad;
        if (PyObject_SetAttrString(fake_module, type->tp_name, (PyObject*) type) < 0)
            goto bad;
        cached_type = type;
    }

cleanup:
    Py_XDECREF(sys);
    Py_XDECREF(sys_modules);
    Py_XDECREF(args);
    return cached_type;

bad:
    cached_type = NULL;
    goto cleanup;
}
