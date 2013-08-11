/////////////// FetchCommonType.proto ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);

/////////////// FetchCommonType ///////////////

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    static PyObject* fake_module = NULL;
    PyTypeObject* cached_type;
    if (fake_module == NULL) {
        PyObject* sys = PyImport_ImportModule("sys");
        PyObject* sys_modules = PyObject_GetAttrString(sys, "modules");
        fake_module = PyDict_GetItemString(sys_modules, "_cython");
        if (fake_module == NULL) {
            PyObject* args = PyTuple_New(1);
            PyTuple_SET_ITEM(args, 0, __Pyx_PyStr_FromString("_cython"));
            fake_module = PyObject_Call((PyObject*) &PyModule_Type, args, NULL);
            PyDict_SetItemString(sys_modules, "_cython", fake_module);
        }
    }
    if (PyObject_HasAttrString(fake_module, type->tp_name)) {
        cached_type = (PyTypeObject*) PyObject_GetAttrString(fake_module, type->tp_name);
    } else {
        PyType_Ready(type);
        PyObject_SetAttrString(fake_module, type->tp_name, (PyObject*) type);
        cached_type = type;
    }
    return cached_type;
}
