///////////////////////////// ABCCheck //////////////////////////////

#if PY_VERSION_HEX < 0x030A0000
static int __Pyx_MatchCase_ABCCheck(PyObject *o, const char* test_for_string, const char* test_for_not_string) {
    // in Python 3.10 objects can have their sequence bit set or their mapping bit set
    // but not both. Practically this translates to "which type is registered first".
    // In Python < 3.10 we can only determine this if they're direct bases (by looking
    // at the MRO order). If they're registered manually then we can't tell


    PyObject *abc_module, *test_for_type=NULL, *test_for_not_type=NULL;
    int result, test_not_result;

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
    test_for_type = PyObject_GetAttrString(abc_module, test_for_string);
    if (!test_for_type) {
        Py_DECREF(abc_module);
        return -1;
    }
    result = PyObject_IsInstance(o, test_for_type);
    if (result <= 0) {
        Py_DECREF(test_for_type);
        Py_DECREF(abc_module);
        return result;
    }

    // from this point on return 1 on error (because we know it does match the first type)

    test_for_not_type = PyObject_GetAttrString(abc_module, test_for_not_string);
    Py_DECREF(abc_module);
    if (!test_for_not_type) {
        goto end;
    }
    test_not_result = PyObject_IsInstance(o, test_for_not_type);
    if (test_not_result == 0) {
        goto end;
    } else if (test_not_result < 0) {
        PyErr_Clear();
        goto end;
    } else {
        // It's an instance of both types. Look up the MRO order
        PyObject *idx_test_for, *idx_test_for_not;
        PyObject *mro = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__mro__");
        if (!mro) {
            PyErr_Clear();
            goto end;
        }
        idx_test_for_not = PyObject_CallMethod(mro, "index", "O", test_for_not_type);
        if (!idx_test_for_not) {
            // most likely it just isn't in the MRO
            PyErr_Clear();
            goto end;
        }
        idx_test_for = PyObject_CallMethod(mro, "index", "O", test_for_type);
        Py_DECREF(mro);
        if (!idx_test_for) {
            Py_DECREF(idx_test_for_not);
            PyErr_Clear();
            if (PyErr_ExceptionMatches(PyExc_ValueError)) {
                // We haven't found "test_for" but we have found "test_for_not" in the MRO.
                // Therefore, "test_for_not" comes first
                result = 0;
                goto end;
            } else {
                // continue the broad policy of treating failures as OK
                goto end;
            }
        }
        result = PyObject_RichCompareBool(idx_test_for, idx_test_for_not, Py_LT);
        Py_DECREF(idx_test_for);
        Py_DECREF(idx_test_for_not);
    }

    end:
    Py_XDECREF(test_for_type);
    Py_XDECREF(test_for_not_type);
    return result;
}
#endif

///////////////////////////// IsSequence.proto //////////////////////

static int __Pyx_MatchCase_IsSequence(PyObject *o); /* proto */

//////////////////////////// IsSequence /////////////////////////
//@requires: ABCCheck

static int __Pyx_MatchCase_IsSequence(PyObject *o) {
#if PY_VERSION_HEX >= 0x030A0000
    return PyType_GetFlags(Py_TYPE(o)) & Py_TPFLAGS_SEQUENCE;
#else
    PyObject *o_module_name;
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
    return __Pyx_MatchCase_ABCCheck(o, "Sequence", "Mapping");
#endif
}
