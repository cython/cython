/////////////// FetchCommonType.proto ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);

/////////////// FetchCommonType ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    static PyObject* fake_module = NULL;
    PyObject* args = NULL;
    PyTypeObject* cached_type = NULL;
    const char* cython_module = "_cython_" CYTHON_ABI;
    if (fake_module == NULL) {
        PyObject* sys_modules = PyImport_GetModuleDict(); // borrowed
        fake_module = PyDict_GetItemString(sys_modules, cython_module); // borrowed
        if (fake_module != NULL) {
            Py_INCREF(fake_module);
        } else {
            PyObject* py_cython_module;
            args = PyTuple_New(1); if (args == NULL) goto bad;
#if PY_MAJOR_VERSION >= 3
            py_cython_module = PyUnicode_DecodeUTF8(cython_module, strlen(cython_module), NULL);
#else
            py_cython_module = PyBytes_FromString(cython_module);
#endif
            if (py_cython_module == NULL) goto bad;
            PyTuple_SET_ITEM(args, 0, py_cython_module);
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
    Py_XDECREF(args);
    return cached_type;

bad:
    cached_type = NULL;
    goto cleanup;
}
