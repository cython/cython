/////////////// FetchSharedCythonModule.proto ///////

static PyObject *__Pyx_FetchSharedCythonABIModule(void);

/////////////// FetchSharedCythonModule ////////////
// @requires::ModuleSetupCode.c:CriticalSections

typedef struct {

} __Pyx_SharedModuleStateStruct;

static int __Pyx_TraverseSharedModuleState(PyObject *self, visitproc visit, void *arg) {
    return 0;
}

static int __Pyx_ClearSharedModuleState(PyObject *self) {
    return 0;
}

static void __Pyx_FreeSharedModuleState(void *self) {
}

static PyModuleDef_Slot __Pyx_SharedModuleSlots[] = {
    // The shared module shouldn't block either multiple interpreters or
    // freethreaded Python.  Unfortunately multiple interpreters is difficult
    // to backdate in the Limited API.
#if __PYX_LIMITED_VERSION_HEX >= 0x030C0000
    {Py_mod_multiple_interpreters, Py_MOD_PER_INTERPRETER_GIL_SUPPORTED},
#endif
#if __PYX_LIMITED_VERSION_HEX >= 0x030d0000
    {Py_mod_gil, Py_MOD_GIL_NOT_USED},
#endif
};

static PyModuleDef __Pyx_SharedModuleDef = {
    PyModuleDef_HEAD_INIT,
    __PYX_ABI_MODULE_NAME, /* m_doc */
    NULL,  /* m_doc */
    sizeof(__Pyx_SharedModuleStateStruct), /* m_size */
    NULL, /* m_methods */
    __Pyx_SharedModuleSlots, /* m_slots */
    __Pyx_TraverseSharedModuleState, /* m_traverse */
    __Pyx_ClearSharedModuleState, /* m_clear */
    __Pyx_FreeSharedModuleState, /* m_free */
};

static PyObject *__Pyx_FetchSharedCythonABIModule(void) {
    PyObject *module_dict = PyImport_GetModuleDict(); // borrowed
    if (unlikely(!module_dict)) return NULL;
    PyObject *abi_module_name = PyUnicode_FromString(__PYX_ABI_MODULE_NAME);
    if (unlikely(!abi_module_name)) return NULL;
    PyObject *module = NULL;
    int find_module_result = __Pyx_PyDict_GetItemRef(module_dict, abi_module_name, &module);
    if (unlikely(find_module_result == -1)) goto cleanup;
    if (find_module_result == 1) goto cleanup; // Done - good

    // otherwise module doesn't yet exist.
    PyModuleDef_Init(&__Pyx_SharedModuleDef);

    PyObject *dummy_spec = NULL;
    {
        // Create a dummy spec object (Python does this internally so it's OK)
        PyObject *namespace_dict = PyDict_New();
        PyObject *empty_tuple = NULL, *dummy_spec_name = NULL;
        
        if (unlikely(!namespace_dict)) goto cleanup;
        if (unlikely(PyDict_SetItemString(namespace_dict, "name", abi_module_name) == -1)) goto cleanup_dummy_spec_creation;
        empty_tuple = PyTuple_New(0); // This is called quite early so don't use the constant
        if (unlikely(!empty_tuple)) goto cleanup_dummy_spec_creation;
        dummy_spec_name = PyUnicode_FromString("DummySpec");
        if (unlikely(!dummy_spec_name)) goto cleanup_dummy_spec_creation;
        dummy_spec = PyObject_CallFunctionObjArgs((PyObject*)&PyType_Type, dummy_spec_name, empty_tuple, namespace_dict, NULL);

      cleanup_dummy_spec_creation:
        Py_XDECREF(namespace_dict);
        Py_XDECREF(empty_tuple);
        Py_XDECREF(dummy_spec_name);
        
    }
    if (unlikely(!dummy_spec)) goto cleanup;

    module = PyModule_FromDefAndSpec2(&__Pyx_SharedModuleDef, dummy_spec, PYTHON_API_VERSION);
    Py_DECREF(dummy_spec);
    if (unlikely(!module)) goto cleanup;
    if (unlikely(PyModule_ExecDef(module, &__Pyx_SharedModuleDef) == -1)) {
        Py_CLEAR(module);
        goto cleanup;
    }

    // At this point we have a potential race, that another module might have managed to create the shared module
    // before us.
    __Pyx_BEGIN_CRITICAL_SECTION(module_dict)
    PyObject *module_again;
    find_module_result = __Pyx_PyDict_GetItemRef(module_dict, abi_module_name, &module_again);
    if (likely(find_module_result == 0)) {
        // Nothing got there first.
        if (unlikely(PyDict_SetItem(module_dict, abi_module_name, module) == -1)) {
            Py_CLEAR(module);
        }
    } else if (find_module_result == 1) {
        // Someone else got there first.
        Py_DECREF(module);
        module = module_again;
    } else {
        // error
        Py_CLEAR(module);
    }
    __Pyx_END_CRITICAL_SECTION()

  cleanup:
    Py_DECREF(abi_module_name);
    return module;
}

/////////////// FetchCommonType.proto ///////////////

#if !CYTHON_USE_TYPE_SPECS
static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type);
#else
static PyTypeObject* __Pyx_FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases);
#endif

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

#if !CYTHON_USE_TYPE_SPECS
static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    PyObject* abi_module;
    const char* object_name;
    PyTypeObject *cached_type = NULL;

    abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!abi_module) return NULL;
    // get the final part of the object name (after the last dot)
    object_name = strrchr(type->tp_name, '.');
    object_name = object_name ? object_name+1 : type->tp_name;
    cached_type = (PyTypeObject*) PyObject_GetAttrString(abi_module, object_name);
    if (cached_type) {
        if (__Pyx_VerifyCachedType(
              (PyObject *)cached_type,
              object_name,
              cached_type->tp_basicsize,
              type->tp_basicsize) < 0) {
            goto bad;
        }
        goto done;
    }

    if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
    PyErr_Clear();
    if (PyType_Ready(type) < 0) goto bad;
    if (PyObject_SetAttrString(abi_module, object_name, (PyObject *)type) < 0)
        goto bad;
    Py_INCREF(type);
    cached_type = type;

done:
    Py_DECREF(abi_module);
    // NOTE: always returns owned reference, or NULL on error
    return cached_type;

bad:
    Py_XDECREF(cached_type);
    cached_type = NULL;
    goto done;
}
#else

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
#endif

