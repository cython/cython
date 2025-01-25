/////////////// FetchSharedCythonModule.proto ///////

static PyObject *__Pyx_FetchSharedCythonABIModule(void);
static CYTHON_INLINE PyTypeObject **__Pyx_SharedCythonABIModule_FindTypePointer(PyObject *mod, const char* name);

/////////////// FetchSharedCythonModule ////////////
//@requires: ModuleSetupCode.c::CriticalSections
//@requires: StringTools.c::IncludeStringH
//@substitute: tempita

{{py: from Cython.Compiler.Naming import shared_names_and_types}}

typedef struct {
    // Note that we don't attempt to work out if these types are used. Because they're shared
    // no one Cython module can know.
    {{for _, type in shared_names_and_types}}
    PyObject *{{type}};
    {{endfor}}
} __Pyx_SharedModuleStateStruct;

static int __Pyx_TraverseSharedModuleState(PyObject *self, visitproc visit, void *arg) {
    __Pyx_SharedModuleStateStruct *mstate = (__Pyx_SharedModuleStateStruct*)PyModule_GetState(self);
    if (unlikely(mstate)) {
        return PyErr_Occurred() ? -1 : 0;
    }
    {{for _, type in shared_names_and_types}}
    Py_VISIT(mstate->{{type}});
    {{endfor}}
    return 0;
}

static int __Pyx_ClearSharedModuleState(PyObject *self) {
    __Pyx_SharedModuleStateStruct *mstate = (__Pyx_SharedModuleStateStruct*)PyModule_GetState(self);
    if (unlikely(mstate)) {
        return PyErr_Occurred() ? -1 : 0;
    }
    {{for _, type in shared_names_and_types}}
    Py_CLEAR(mstate->{{type}});
    {{endfor}}
    return 0;
}

static void __Pyx_FreeSharedModuleState(void *self) {
    __Pyx_ClearSharedModuleState((PyObject*)self);
}

static PyObject *__Pyx_SharedModuleGetAttr(PyObject *self, PyObject *arg) {
    int cmp_result;
    // TODO - in principle this linear search could become a binary search, but that doesn't seem worthwhile given the short list
    {{for name, cname in shared_names_and_types}}
    cmp_result = PyUnicode_CompareWithASCIIString(arg, "{{name}}");
    if (cmp_result == 0) {
        PyObject *obj = ((__Pyx_SharedModuleStateStruct*)PyModule_GetState(self))->{{cname}};
        if (!obj) goto not_found;  // quite likely - we just haven't set it from a Cython module
        return obj;
    }
    {{endfor}}
    
  not_found:
    PyErr_SetObject(PyExc_AttributeError, arg);
    return NULL;
}

// Called inside a critical section
static PyObject *__Pyx__SharedModuleDir(PyObject *self) {
    __Pyx_SharedModuleStateStruct* mstate = (__Pyx_SharedModuleStateStruct*)PyModule_GetState(self);

    PyObject *module_dict = PyModule_GetDict(self);
    if (unlikely(!module_dict)) return NULL;
    PyObject *module_dict_keys = PyDict_Keys(module_dict);
    if (unlikely(!module_dict_keys)) return NULL;
    
    {{for name, cname in shared_names_and_types}}
    if (mstate->{{cname}}) {
        PyObject *unicode_name = PyUnicode_FromStringAndSize("{{name}}", {{len(name)}});
        if (unlikely(!unicode_name)) goto bad;
        int append_result = PyList_Append(module_dict_keys, unicode_name);
        Py_DECREF(unicode_name);
        if (unlikely(append_result)) goto bad;
    }
    {{endfor}}

    return module_dict_keys;

  bad:
    Py_DECREF(module_dict_keys);
    return NULL;
}

static PyObject *__Pyx_SharedModuleDir(PyObject *self, PyObject *) {
    PyObject *result;
    __Pyx_BEGIN_CRITICAL_SECTION(self);
    result = __Pyx__SharedModuleDir(self);
    __Pyx_END_CRITICAL_SECTION();
    return result;
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
    {0, 0}
};

PyMethodDef __Pyx_SharedModuleMethods[] = {
    {"__getattr__", &__Pyx_SharedModuleGetAttr, METH_O, NULL},
    {"__dir__", &__Pyx_SharedModuleDir, METH_NOARGS, NULL},
    {0, 0, 0, 0}
};

static PyModuleDef __Pyx_SharedModuleDef = {
    PyModuleDef_HEAD_INIT,
    __PYX_ABI_MODULE_NAME, /* m_doc */
    NULL,  /* m_doc */
    sizeof(__Pyx_SharedModuleStateStruct), /* m_size */
    __Pyx_SharedModuleMethods, /* m_methods */
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

static CYTHON_INLINE PyTypeObject **__Pyx_SharedCythonABIModule_FindTypePointer(PyObject *mod, const char* name) {
    {{for name, cname in shared_names_and_types}}
    if (strcmp("{{name}}", name) == 0) {
        return (PyTypeObject**)&((__Pyx_SharedModuleStateStruct*)PyModule_GetState(mod))->{{cname}};
    }
    {{endfor}}
    // Really a logic error in Cython if we get here
    PyErr_Format(PyExc_SystemError, "Failed to find '%s' in Cython shared module", name);
    return NULL;
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
//@requires: ModuleSetupCode.c::CriticalSections
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
// Called with a critical section around abi_module
static PyTypeObject* __Pyx__FetchCommonType(PyTypeObject* type, PyObject* abi_module) {
    const char* object_name;
    PyTypeObject *cached_type = NULL;
    PyTypeObject **abi_module_entry;

    // get the final part of the object name (after the last dot)
    object_name = strrchr(type->tp_name, '.');
    object_name = object_name ? object_name+1 : type->tp_name;

    abi_module_entry = __Pyx_SharedCythonABIModule_FindTypePointer(abi_module, object_name);
    if (unlikely(!abi_module_entry)) return NULL;

    cached_type = (PyTypeObject*) *abi_module_entry;
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
    
    if (PyType_Ready(type) < 0) goto bad;

    // Note potential race here to set the cached type
    if (likely(!*abi_module_entry)) {
        Py_INCREF(type);
        *abi_module_entry = type;
        Py_INCREF(type); 
        cached_type = type;
    } else {
        Py_INCREF(*abi_module_entry);
        cached_type = *abi_module_entry;
        // type is static though, so don't decref it
    }

done:
    Py_DECREF(abi_module);
    // NOTE: always returns owned reference, or NULL on error
    return cached_type;

bad:
    Py_XDECREF(cached_type);
    cached_type = NULL;
    goto done;
}

static PyTypeObject* __Pyx_FetchCommonType(PyTypeObject* type) {
    PyObject* abi_module;
    PyTypeObject* result;

    abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!abi_module) return NULL;    
    __Pyx_BEGIN_CRITICAL_SECTION(abi_module)
    result = __Pyx__FetchCommonType(type, abi_module);
    __Pyx_END_CRITICAL_SECTION()
    return result;    
}
#else

// Called with a critical section around abi_module
static PyTypeObject *__Pyx__FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases, PyObject* abi_module) {
    PyObject *cached_type = NULL;
    PyTypeObject **abi_module_entry;

    // get the final part of the object name (after the last dot)
    const char* object_name = strrchr(spec->name, '.');
    object_name = object_name ? object_name+1 : spec->name;

    abi_module_entry = __Pyx_SharedCythonABIModule_FindTypePointer(abi_module, object_name);
    if (unlikely(!abi_module_entry)) return NULL;

    cached_type = *abi_module_entry;
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

    // We pass the ABI module reference to avoid keeping the user module alive by foreign type usages.
    CYTHON_UNUSED_VAR(module);
    cached_type = __Pyx_PyType_FromModuleAndSpec(abi_module, spec, bases);
    if (unlikely(!cached_type)) goto bad;
    if (unlikely(__Pyx_fix_up_extension_type_from_spec(spec, (PyTypeObject *) cached_type) < 0)) goto bad;

    // Note potential race here to set the type on the ABI module
    if (likely(!*abi_module_entry)) {
        Py_INCREF(abi_module_entry);
        *abi_module_entry = cached_type;
    } else {
        Py_DECREF(cached_type);
        Py_INCREF(*abi_module_entry);
        cached_type = *abi_module_entry;
    }

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

static PyTypeObject *__Pyx_FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases) {
    PyObject *abi_module;
    PyTypeObject *result;

    abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!abi_module) return NULL;

    __Pyx_BEGIN_CRITICAL_SECTION(abi_module)
    result = __Pyx__FetchCommonTypeFromSpec(module, spec, bases, abi_module);
    __Pyx_END_CRITICAL_SECTION()
    return result;
}
#endif

