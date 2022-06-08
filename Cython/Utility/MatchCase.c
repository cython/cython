///////////////////////////// IsSequence.proto //////////////////////

static int __Pyx_MatchCase_IsSequence(PyObject *o); /* proto */

//////////////////////////// IsSequence /////////////////////////

static int __Pyx_MatchCase_IsSequence(PyObject *o) {
#if PY_VERSION_HEX >= 0x030A0000
    return PyType_GetFlags(Py_TYPE(o)) & Py_TPFLAGS_SEQUENCE;
#else
    PyObject *o_module_name, *abc_module, *Sequence;
    int result;
    // Py_TPFLAGS_SEQUENCE doesn't exit. Check a known list of types
    if (PyUnicode_Check(o) || PyBytes_Check(o) || PyByteArray_Check(o) || o == Py_None) {
        return 0;  // these types are deliberately excluded and treated not as a sequence
    }
    if (PyList_Check(o) || PyTuple_Check(o) || PyRange_Check(o) || PyMemoryView_Check(o)) {
        return 1;
    }
    // array.array is a more complicated check (and unfortunately isn't covered by
    // collections.abc.Sequence on Python <3.10).
    // Do the test by checking the module name, and then importing/testing the class
    o_module_name = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__module__");
    if (!o_module_name) {
        // This test seems pretty non-essentially - just jump to the abc test
        PyErr_Clear();
        goto abc_test;
    }
#if PY_MAJOR_VERSION >= 3
    if (PyUnicode_Check(o_module_name) && PyUnicode_CompareWithASCIIString(o_module_name, "array") == 0)
#else
    if (PyBytes_Check(o_module_name) && PyBytes_AS_STRING(o_module_name)[0] == 'a' &&
        PyBytes_AS_STRING(o_module_name)[1] == 'r' && PyBytes_AS_STRING(o_module_name)[2] == 'r' &&
        PyBytes_AS_STRING(o_module_name)[3] == 'a' && PyBytes_AS_STRING(o_module_name)[4] == 'y' &&
        PyBytes_AS_STRING(o_module_name)[5] == '\0')
#endif
    {
        int is_array;
        PyObject *array_module, *array_object;
        Py_DECREF(o_module_name);
        array_module = PyImport_ImportModule("array");
        if (!array_module) {
            PyErr_Clear();
            goto abc_test;
        }
        array_object = PyObject_GetAttrString(array_module, "array");
        Py_DECREF(array_module);
        if (!array_object) {
            PyErr_Clear();
            goto abc_test;
        }
        is_array = PyObject_IsInstance(o, array_object);
        Py_DECREF(array_object);
        if (is_array) {
            return 1;
        }
        PyErr_Clear();
    } else {
        Py_DECREF(o_module_name);
    }

    abc_test:
    // otherwise check against collections.abc.Sequence
    abc_module = PyImport_ImportModule(
#if PY_VERSION_HEX > 0x03030000
        "collections.abc"
#else
        "collections"
#endif
                 );
    if (!abc_module) {
        return -1;
    }
    Sequence = PyObject_GetAttrString(abc_module, "Sequence");
    Py_DECREF(abc_module);
    if (!Sequence) {
        return -1;
    }
    result = PyObject_IsInstance(o, Sequence);
    Py_DECREF(Sequence);
    return result;
#endif
}
