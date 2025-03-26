/////////////// FetchSharedCythonModule.proto ///////

static PyObject *__Pyx_FetchSharedCythonABIModule(void);

/////////////// FetchSharedCythonModule ////////////

static PyObject *__Pyx_FetchSharedCythonABIModule(void) {
    return __Pyx_PyImport_AddModuleRef(__PYX_ABI_MODULE_NAME);
}

/////////////// FetchCommonType.proto ///////////////

static PyTypeObject* __Pyx_FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases);

/////////////// FetchCommonType ///////////////
//@requires:ExtensionTypes.c::FixUpExtensionType
//@requires: FetchSharedCythonModule
//@requires:StringTools.c::IncludeStringH

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

static PyTypeObject *__Pyx_FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases) {
    PyObject *abi_module, *cached_type = NULL;
    // get the final part of the object name (after the last dot)
    const char* object_name = strrchr(spec->name, '.');
    object_name = object_name ? object_name+1 : spec->name;

    abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!abi_module) return NULL;

    cached_type = PyObject_GetAttrString(abi_module, object_name);
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
              object_name,
              basicsize,
              spec->basicsize) < 0) {
            goto bad;
        }
        goto done;
    }

    if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
    PyErr_Clear();
    // We pass the ABI module reference to avoid keeping the user module alive by foreign type usages.
    CYTHON_UNUSED_VAR(module);
    cached_type = __Pyx_PyType_FromModuleAndSpec(abi_module, spec, bases);
    if (unlikely(!cached_type)) goto bad;
    if (unlikely(__Pyx_fix_up_extension_type_from_spec(spec, (PyTypeObject *) cached_type) < 0)) goto bad;
    if (PyObject_SetAttrString(abi_module, object_name, cached_type) < 0) goto bad;

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

/////////////// RegisterABC.proto ///////////////

static void __Pyx_RegisterCommonTypeWithAbc(PyObject *type, const char *abc_name); /* proto */

/////////////// RegisterABC ///////////////
//@requires: ModuleSetupCode.c::CriticalSections
//@requires: ObjectHandling.c::PyObjectGetAttrStrNoError
//@requires: Optimize.c::dict_setdefault

static void __Pyx_RegisterCommonTypeWithAbc(PyObject *type, const char *abc_name)
{
    int result = -1;
    PyObject *runtime_dict = PyModule_GetDict(NAMED_CGLOBAL(cython_runtime_cname));
    PyObject *abc_class = NULL;
    PyObject *py_abc_name = PyUnicode_FromString(abc_name);
    int get_item_result;
    if (unlikely(!py_abc_name))
        goto done;
    get_item_result = __Pyx_PyDict_GetItemRef(runtime_dict, py_abc_name, &abc_class);
    if (unlikely(get_item_result == -1)) {
        goto done;
    } else if (get_item_result == 0) {
        PyObject *abc_module = PyImport_ImportModule("abc");
        if (unlikely(!abc_module)) goto done;

        PyObject *abc_type = PyObject_GetAttrString(abc_module, "ABC");
        Py_DECREF(abc_module);
        if (unlikely(!abc_type)) goto done;

        PyObject* new_abc_class = PyObject_CallFunction(
            (PyObject*)&PyType_Type,
            "O(O){ss}",
            py_abc_name,
            abc_type,
            "__module__",
            "cython_runtime"
        );
        Py_DECREF(abc_type);
        if (unlikely(!new_abc_class)) goto done;

        // Retry, check that there hasn't been a race
        abc_class = __Pyx_PyDict_SetDefault(runtime_dict, py_abc_name, new_abc_class, 1);
        Py_DECREF(new_abc_class);
        if (unlikely(!abc_class)) goto done;
    }
    {
        // The class is initialized, register the type
        PyObject *register_result = PyObject_CallMethod(abc_class, "register", "O", type);
        Py_DECREF(abc_class);
        if (likely(register_result)) {
            Py_DECREF(register_result);
            result = 0;
        }
    }

  done:
    Py_DECREF(py_abc_name);

    if (unlikely(result == -1)) {
        // Treat this as an allowed failure; it doesn't matter too much if we don't register the abcs.
        PyObject *type, *value, *traceback;
        PyErr_Fetch(&type, &value, &traceback);
        // and equally, formatting the message doesn't really matter.
        PyObject *msg = PyUnicode_FromFormat("Exception ignored while setting up %s abstract base class", abc_name);
        PyErr_Restore(type, value, traceback);
        PyErr_WriteUnraisable(msg);
        Py_XDECREF(msg);
    }
}