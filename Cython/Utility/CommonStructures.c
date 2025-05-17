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
//@requires:Optimize.c::dict_setdefault

static int __Pyx_VerifyCachedType(PyObject *cached_type,
                               const char *name,
                               Py_ssize_t expected_basicsize) {
    Py_ssize_t basicsize;

    if (!PyType_Check(cached_type)) {
        PyErr_Format(PyExc_TypeError,
            "Shared Cython type %.200s is not a type object", name);
        return -1;
    }

#if CYTHON_COMPILING_IN_LIMITED_API
    PyObject *py_basicsize;
    py_basicsize = PyObject_GetAttrString(cached_type, "__basicsize__");
    if (unlikely(!py_basicsize)) return -1;
    basicsize = PyLong_AsSsize_t(py_basicsize);
    Py_DECREF(py_basicsize);
    py_basicsize = NULL;
    if (unlikely(basicsize == (Py_ssize_t)-1) && PyErr_Occurred()) return -1;
#else
    basicsize = ((PyTypeObject*) cached_type)->tp_basicsize;
#endif
    
    if (basicsize != expected_basicsize) {
        PyErr_Format(PyExc_TypeError,
            "Shared Cython type %.200s has the wrong size, try recompiling",
            name);
        return -1;
    }
    return 0;
}

static PyTypeObject *__Pyx_FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases) {
    PyObject *abi_module = NULL, *cached_type = NULL, *abi_module_dict, *new_cached_type, *py_object_name;
    int get_item_ref_result;
    // get the final part of the object name (after the last dot)
    const char* object_name = strrchr(spec->name, '.');
    object_name = object_name ? object_name+1 : spec->name;

    py_object_name = PyUnicode_FromString(object_name);
    if (!py_object_name) return NULL;

    abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!abi_module) goto done;
    abi_module_dict = PyModule_GetDict(abi_module);
    if (!abi_module_dict) goto done;


    get_item_ref_result = __Pyx_PyDict_GetItemRef(abi_module_dict, py_object_name, &cached_type);
    if (get_item_ref_result == 1) {
        if (__Pyx_VerifyCachedType(
              cached_type,
              object_name,
              spec->basicsize) < 0) {
            goto bad;
        }
        goto done;
    } else if (unlikely(get_item_ref_result == -1)) {
        goto bad;
    }

    // We pass the ABI module reference to avoid keeping the user module alive by foreign type usages.
    CYTHON_UNUSED_VAR(module);
    cached_type = __Pyx_PyType_FromModuleAndSpec(abi_module, spec, bases);
    if (unlikely(!cached_type)) goto bad;
    if (unlikely(__Pyx_fix_up_extension_type_from_spec(spec, (PyTypeObject *) cached_type) < 0)) goto bad;

    new_cached_type = __Pyx_PyDict_SetDefault(abi_module_dict, py_object_name, cached_type, 1);
    if (unlikely(new_cached_type != cached_type)) {
        if (unlikely(!new_cached_type)) goto bad;
        // race to initialize it - use the value that's already been set.
        Py_DECREF(cached_type);
        cached_type = new_cached_type;
        
        if (__Pyx_VerifyCachedType(
                cached_type,
                object_name,
                spec->basicsize) < 0) {
            goto bad;
        }
        goto done;
    } else {
        Py_DECREF(new_cached_type);
    }

done:
    Py_XDECREF(abi_module);
    Py_DECREF(py_object_name);
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

static void __Pyx_RegisterCommonTypeWithBackportsAbc(PyObject *type, PyObject *py_abc_name) {
    // This really is optional since there's no reason to assume that anyone will
    // have backports_abc installed.
    PyObject *module = PyImport_ImportModule("backports_abc");
    if (!module) goto error;

    // No need to worry about races here - collections.abc holds the master copy
    // so at worst we'll just be reinitializing the same reference.
    if (PyObject_SetAttr(module, py_abc_name, type) == -1) goto error;
    return;

  error:
    PyErr_Clear();
}

static void __Pyx_RegisterCommonTypeWithAbc(PyObject *type, const char *abc_name)
{
    int result = -1;
    int get_item_result;
    PyObject *abc_class = NULL, *collections_abc_module_dict, *py_abc_name = NULL;
    PyObject *collections_abc_module = PyImport_ImportModule("collections.abc");
    if (unlikely(!collections_abc_module)) goto done;

    collections_abc_module_dict = PyModule_GetDict(collections_abc_module);
    if (unlikely(!collections_abc_module_dict)) goto done;

    py_abc_name = PyUnicode_FromString(abc_name);
    if (unlikely(!py_abc_name))
        goto done;

    get_item_result = __Pyx_PyDict_GetItemRef(collections_abc_module_dict, py_abc_name, &abc_class);
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
            "collections.abc"
        );
        Py_DECREF(abc_type);
        if (unlikely(!new_abc_class)) goto done;

        // Retry, check that there hasn't been a race
        abc_class = __Pyx_PyDict_SetDefault(collections_abc_module_dict, py_abc_name, new_abc_class, 1);
        Py_DECREF(new_abc_class);
        if (unlikely(!abc_class)) goto done;
    }
    {
        // The class is initialized, register the type
        PyObject *register_result = PyObject_CallMethod(abc_class, "register", "O", type);

        if (likely(register_result)) {
            Py_DECREF(register_result);
            result = 0;

            if (get_item_result == 0)
                __Pyx_RegisterCommonTypeWithBackportsAbc(abc_class, py_abc_name);
        }
    }

  done:
    Py_XDECREF(collections_abc_module);
    Py_XDECREF(py_abc_name);
    Py_XDECREF(abc_class);

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