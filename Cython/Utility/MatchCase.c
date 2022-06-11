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
        PyObject *mro = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__mro__");
        Py_ssize_t i;
        if (!mro) {
            PyErr_Clear();
            goto end;
        }
        //PyObject_Print(mro, stdout, 0);
        //printf("\n");
        if (!PyTuple_Check(mro)) {
            Py_DECREF(mro);
            goto end;
        }
        for (i=1; i < PyTuple_GET_SIZE(mro); ++i) {
            int is_subclass_test_for, is_subclass_test_not_for;
            PyObject *mro_item = PyTuple_GET_ITEM(mro, i);
            is_subclass_test_for = PyObject_IsSubclass(mro_item, test_for_type);
            if (is_subclass_test_for < 0) goto loop_error;
            is_subclass_test_not_for = PyObject_IsSubclass(mro_item, test_for_not_type);
            if (is_subclass_test_not_for < 0) goto loop_error;
            //printf("%d %d\n", is_subclass_test_for, is_subclass_test_not_for);
            if (is_subclass_test_for && !is_subclass_test_not_for) {
                // The "good" type is earlier in the MRO. Success
                break;
            } else if (is_subclass_test_not_for && !is_subclass_test_for) {
                // The "bad" type is earlier in the MRO
                result = 0;
                break;
            }
        }
        // If we get to the end of the loop without breaking then neither type is in
        // the MRO, so they've both been registered manually. We don't know which was
        // registered first, but returning "1" is an OK answer
        if (0) {
            loop_error:
            PyErr_Clear();
        }
        Py_DECREF(mro);
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
    int abc_result;
    // Py_TPFLAGS_SEQUENCE doesn't exit. Check a known list of types
    if (PyUnicode_Check(o) || PyBytes_Check(o) || PyByteArray_Check(o) || o == Py_None) {
        return 0;  // these types are deliberately excluded and treated not as a sequence
    }
    if (PyList_CheckExact(o) || PyTuple_CheckExact(o)) {
        // Use exact type match for these checks. I in the event of inheritence we need to make sure
        // that it isn't a mapping too
        return 1;
    }
    if (PyRange_Check(o) || PyMemoryView_Check(o)) {
        // Exact check isn't possible so do exact check in another way
        PyObject *mro = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__mro__");
        if (mro) {
            Py_ssize_t len = PyObject_Length(mro);
            Py_DECREF(mro);
            if (len < 0) {
                PyErr_Clear(); // doesn't really matter, just proceed with other checks
            } else if (len == 2) {
                return 1; // the type and "object" and no other bases
            }
        } else {
            PyErr_Clear(); // doesn't really matter, just proceed with other checks
        }
    }

    abc_result = __Pyx_MatchCase_ABCCheck(o, "Sequence", "Mapping");
    if (abc_result) {  // either success or error
        return abc_result;
    }

    // array.array is a more complicated check (and unfortunately isn't covered by
    // collections.abc.Sequence on Python <3.10).
    // Do the test by checking the module name, and then importing/testing the class
    // It also doesn't give perfect results for classes that inherit from both array.array
    // and a mapping
    o_module_name = PyObject_GetAttrString((PyObject*)Py_TYPE(o), "__module__");
    if (!o_module_name) {
        return -1;
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
            return 0;  // treat these tests as "soft" and don't cause an exception
        }
        array_object = PyObject_GetAttrString(array_module, "array");
        Py_DECREF(array_module);
        if (!array_object) {
            PyErr_Clear();
            return 0;
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
    return 0;
#endif
}
