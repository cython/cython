/////////////// FetchSharedCythonModule.proto ///////

{{py: from Cython.Compiler.Naming import shared_names_and_types}}

#if CYTHON_USE_FREELISTS && !defined(_PyAsyncGen_MAXFREELIST)
#define _PyAsyncGen_MAXFREELIST 80
#endif

typedef struct {
    // Note that we don't attempt to work out if these types are used. Because they're shared
    // no one Cython module can know.
    {{for _, type in shared_names_and_types}}
    PyTypeObject *{{type}};
    {{endfor}}

    // Cached Python types - stored here because they're used by the shared types and so they
    // need to be associated with the shared types
    #if CYTHON_COMPILING_IN_LIMITED_API
    PyObject *__Pyx_CachedCoroType;
    #endif

    
    // Freelists boost performance 6-10%; they also reduce memory
    // fragmentation, as _PyAsyncGenWrappedValue and PyAsyncGenASend
    // are short-living objects that are instantiated for every
    // __anext__ call.
    // Don't put stuff after here, because  otherwise we depend on the same definition
    // of _PyAsyncGen_MAXFREELIST being used every time it's compiled.
    #if CYTHON_USE_FREELISTS
    PyObject *__Pyx_ag_value_freelist[_PyAsyncGen_MAXFREELIST];
    int __Pyx_ag_value_freelist_free;

    PyObject *__Pyx_ag_asend_freelist[_PyAsyncGen_MAXFREELIST];
    int __Pyx_ag_asend_freelist_free;
    #endif
} __Pyx_SharedModuleStateStruct;

static PyObject *__Pyx_FetchSharedCythonABIModule(void);
static CYTHON_INLINE PyTypeObject **__Pyx_SharedCythonABIModule_FindTypePointer(PyObject *mod, const char* name);

/////////////// FetchSharedCythonModule ////////////
//@requires: ModuleSetupCode.c::CriticalSections
//@requires: StringTools.c::IncludeStringH
//@substitute: tempita

{{py: from Cython.Compiler.Naming import shared_names_and_types}}

static int __Pyx_TraverseSharedModuleState(PyObject *self, visitproc visit, void *arg) {
    __Pyx_SharedModuleStateStruct *mstate = (__Pyx_SharedModuleStateStruct*)PyModule_GetState(self);
    if (unlikely(mstate)) {
        return PyErr_Occurred() ? -1 : 0;
    }
    {{for _, type in shared_names_and_types}}
    Py_VISIT((PyObject*)mstate->{{type}});
    {{endfor}}

    #if CYTHON_COMPILING_IN_LIMITED_API
    Py_VISIT(mstate->__Pyx_CachedCoroType);
    #endif
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

    #if CYTHON_COMPILING_IN_LIMITED_API
    Py_CLEAR(mstate->__Pyx_CachedCoroType);
    #endif
    return 0;
}

static int
__Pyx_PyAsyncGen_ClearFreeLists(__Pyx_SharedModuleStateStruct *mstate)
{
    if (!mstate) return 0;

    #if CYTHON_USE_FREELISTS
    int ret = mstate->__Pyx_ag_value_freelist_free + mstate->__Pyx_ag_asend_freelist_free;

    while (mstate->__Pyx_ag_value_freelist_free) {
        PyObject *o;
        o = mstate->__Pyx_ag_value_freelist[--(mstate->__Pyx_ag_value_freelist_free)];
        __Pyx_PyHeapTypeObject_GC_Del(o);
    }

    while (mstate->__Pyx_ag_asend_freelist_free) {
        PyObject *o;
        o = mstate->__Pyx_ag_asend_freelist[--(mstate->__Pyx_ag_asend_freelist_free)];
        __Pyx_PyHeapTypeObject_GC_Del(o);
    }

    return ret;
    #else
    return 0;
    #endif
}

static void __Pyx_FreeSharedModuleState(void *self) {
    __Pyx_ClearSharedModuleState((PyObject*)self);
    // Free lists should be freed but not cleared
    __Pyx_PyAsyncGen_ClearFreeLists((__Pyx_SharedModuleStateStruct*)PyModule_GetState((PyObject*)self));
}

static PyObject *__Pyx_SharedModuleGetAttr(PyObject *self, PyObject *arg) {
    int cmp_result;
    // TODO - in principle this linear search could become a binary search, but that doesn't seem worthwhile given the short list
    {{for name, cname in shared_names_and_types}}
    cmp_result = PyUnicode_CompareWithASCIIString(arg, "{{name}}");
    if (cmp_result == 0) {
        PyObject *obj = (PyObject*)((__Pyx_SharedModuleStateStruct*)PyModule_GetState(self))->{{cname}};
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
    PyObject *dummy_spec = NULL;
    int find_module_result = __Pyx_PyDict_GetItemRef(module_dict, abi_module_name, &module);
    if (unlikely(find_module_result == -1)) goto cleanup;
    if (find_module_result == 1) goto cleanup; // Done - good

    // otherwise module doesn't yet exist.
    PyModuleDef_Init(&__Pyx_SharedModuleDef);

    
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
        return &((__Pyx_SharedModuleStateStruct*)PyModule_GetState(mod))->{{cname}};
    }
    {{endfor}}
    // Really a logic error in Cython if we get here
    PyErr_Format(PyExc_SystemError, "Failed to find '%s' in Cython shared module", name);
    return NULL;
}

/////////////// FetchCommonType.proto ///////////////

#ifndef __Pyx_SharedAbiModule_USED
#define __Pyx_SharedAbiModule_USED
#endif

static PyTypeObject* __Pyx_FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases);

/////////////// FetchCommonType ///////////////
//@requires:ExtensionTypes.c::FixUpExtensionType
//@requires: InitAndGetSharedAbiModule
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

// Called with a critical section around abi_module
static PyTypeObject *__Pyx__FetchCommonTypeFromSpec(PyObject *module, PyType_Spec *spec, PyObject *bases, PyObject* abi_module) {
    PyObject *cached_type = NULL;
    PyTypeObject **abi_module_entry;

    // get the final part of the object name (after the last dot)
    const char* object_name = strrchr(spec->name, '.');
    object_name = object_name ? object_name+1 : spec->name;

    abi_module_entry = __Pyx_SharedCythonABIModule_FindTypePointer(abi_module, object_name);
    if (unlikely(!abi_module_entry)) return NULL;

    cached_type = (PyObject*)*abi_module_entry;
    if (cached_type) {
        Py_INCREF(cached_type);
      check_type:
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
        *abi_module_entry = (PyTypeObject*)cached_type;
    } else {
        Py_DECREF(cached_type);
        Py_INCREF(*abi_module_entry);
        cached_type = (PyObject*)*abi_module_entry;
        goto check_type;
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

    abi_module = __Pyx_InitAndGetSharedAbiModule(module);
    if (!abi_module) return NULL;

    __Pyx_BEGIN_CRITICAL_SECTION(abi_module)
    result = __Pyx__FetchCommonTypeFromSpec(module, spec, bases, abi_module);
    __Pyx_END_CRITICAL_SECTION()
    return result;
}

/////////////////////// InitAndGetSharedAbiModule.proto ///////////////////////
//@requires:FetchSharedCythonModule

#ifndef __Pyx_SharedAbiModule_USED
#define __Pyx_SharedAbiModule_USED
#endif

// Generates the shared ABI module if needed, and makes sure the pointer to it in our module
// state is initialized.
// Returns a borrowed reference
static PyObject* __Pyx_InitAndGetSharedAbiModule(PyObject *this_module); /* proto */
// Must be called after the shared abi module is initialized in our module state
#define __Pyx_GetSharedModuleStateFromModule(mod) ((__Pyx_SharedModuleStateStruct*)__Pyx__GetSharedModuleStateFromModule(mod))
static CYTHON_INLINE void* __Pyx__GetSharedModuleStateFromModule(PyObject *mod); /* proto */
#define __Pyx_GetSharedModuleState() __Pyx_GetSharedModuleStateFromModule(NAMED_CGLOBAL(shared_abi_module_cname))

static CYTHON_INLINE PyObject *__Pyx_SharedAbiModuleFromSharedType(PyTypeObject *tp);

/////////////////////// InitAndGetSharedAbiModule ///////////////////////
//@substitute: naming

static CYTHON_INLINE void* __Pyx__GetSharedModuleStateFromModule(PyObject *mod) {
    if (!mod) return NULL;
    return PyModule_GetState(mod);
}

static PyObject* __Pyx_InitAndGetSharedAbiModule(PyObject *this_module) {
    $modulestatetype_cname *this_mstate = __Pyx_PyModule_GetState(this_module);
    if (!this_mstate->$shared_abi_module_cname) {
        this_mstate->$shared_abi_module_cname = __Pyx_FetchSharedCythonABIModule();
        if (!this_mstate->$shared_abi_module_cname) return NULL;
    }
    return this_mstate->$shared_abi_module_cname;
}

static CYTHON_INLINE PyObject *__Pyx_SharedAbiModuleFromSharedType(PyTypeObject *tp) {
#if (!CYTHON_COMPILING_IN_LIMITED_API || __PYX_LIMITED_VERSION_HEX >= 0x030A0000)
    PyTypeObject *base = tp;

    // All of our shared types have a shared type at the top of our inheritance heirarchy
    while ((1)) {
        PyTypeObject *new_base = __Pyx_PyType_GetSlot(base, tp_base, PyTypeObject*);
        if (likely(!new_base)) {
            break;
        }
        base = new_base;
    }
    return PyType_GetModule(base);
#else
    // We're using a Limited API version without PyType_GetModule.
    // In this case getting the shared module from an arbitrary Cython module is the best that we can do.
    // This only becomes dodgy in the unlikely event that this arbitrary module ever gets unloaded.
    CYTHON_UNUSED_VAR(tp);
    return NAMED_CGLOBAL(shared_abi_module_cname);
#endif
}
