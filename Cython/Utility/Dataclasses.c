///////////////////// ModuleLoader.proto //////////////////////////

static PyObject* __Pyx_LoadInternalModule(const char* name, const char* fallback_code); /* proto */

//////////////////// ModuleLoader ///////////////////////
//@requires: CommonStructures.c::FetchSharedCythonModule

static PyObject* __Pyx_LoadInternalModule(const char* name, const char* fallback_code) {
    // We want to be able to use the contents of the standard library dataclasses module where available.
    // If those objects aren't available (due to Python version) then a simple fallback is substituted
    // instead, which largely just fails with a not-implemented error.
    //
    // The fallbacks are placed in the "shared abi module" as a convenient internal place to
    // store them

    PyObject *shared_abi_module = 0, *module = 0;

    shared_abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!shared_abi_module) return NULL;

    if (PyObject_HasAttrString(shared_abi_module, name)) {
        PyObject* result = PyObject_GetAttrString(shared_abi_module, name);
        Py_DECREF(shared_abi_module);
        return result;
    }

    // the best and simplest case is simply to defer to the standard library (if available)
    module = PyImport_ImportModule(name);
    if (!module) {
        PyObject *localDict, *runValue, *builtins, *modulename;
        if (!PyErr_ExceptionMatches(PyExc_ImportError)) goto bad;
        PyErr_Clear();  // this is reasonably likely (especially on older versions of Python)
#if PY_MAJOR_VERSION < 3
        modulename = PyBytes_FromFormat("_cython_" CYTHON_ABI ".%s", name);
#else
        modulename = PyUnicode_FromFormat("_cython_" CYTHON_ABI ".%s", name);
#endif
        if (!modulename) goto bad;
#if PY_MAJOR_VERSION >= 3 && CYTHON_COMPILING_IN_CPYTHON
        module = PyImport_AddModuleObject(modulename); // borrowed
#else
        module = PyImport_AddModule(PyBytes_AsString(modulename)); // borrowed
#endif
        Py_DECREF(modulename);
        if (!module) goto bad;
        Py_INCREF(module);
        if (PyObject_SetAttrString(shared_abi_module, name, module) < 0) goto bad;
        localDict = PyModule_GetDict(module); // borrowed
        if (!localDict) goto bad;
        builtins = PyEval_GetBuiltins(); // borrowed
        if (!builtins) goto bad;
        if (PyDict_SetItemString(localDict, "__builtins__", builtins) <0) goto bad;

        runValue = PyRun_String(fallback_code, Py_file_input, localDict, localDict);
        if (!runValue) goto bad;
        Py_DECREF(runValue);
    }
    goto shared_cleanup;

    bad:
        Py_CLEAR(module);
    shared_cleanup:
        Py_XDECREF(shared_abi_module);
    return module;
}

///////////////////// SpecificModuleLoader.proto //////////////////////
//@substitute: tempita

static PyObject* __Pyx_Load_{{cname}}_Module(void); /* proto */


//////////////////// SpecificModuleLoader ///////////////////////
//@requires: ModuleLoader

static PyObject* __Pyx_Load_{{cname}}_Module(void) {
    return __Pyx_LoadInternalModule("{{cname}}", {{py_code}});
}
