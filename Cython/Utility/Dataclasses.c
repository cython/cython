///////////////////// ModuleLoader.proto //////////////////////////

static PyObject* __Pyx_LoadInternalModule(const char* name, const char* fallback_code); /* proto */

//////////////////// ModuleLoader ///////////////////////
//@requires: CommonStructures.c::FetchCommonType

static PyObject* __Pyx_LoadInternalModule(const char* name, const char* fallback_code) {
    // In supporting dataclasses we want to be able to use directives like:
    //  cython.dataclass, cython.field, cython.InitVar (based on the Standard Library dataclasses module)
    //  cython.ClassVar (based on the standard library tying module)
    // These are processed efficiently by Cython as much as possible, but if they are treated
    // as a Python object then the objects from the standard library module should be substituted.
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
        if (PyErr_ExceptionMatches(PyExc_ImportError)) {
            PyErr_Clear();  // this is reasonably likely (especially on older versions of Python)
        } else {
            goto bad;
        }
        modulename = PyUnicode_FromFormat("_cython_" CYTHON_ABI ".%s", name);
        if (!modulename) goto bad;
        module = PyImport_AddModuleObject(modulename);
        Py_DECREF(modulename);
        if (!module) goto bad;
        if (PyObject_SetAttrString(shared_abi_module, name, module)<0) goto bad;
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

///////////////////// DataclassModuleLoader.proto //////////////////////

static PyObject* __Pyx_LoadDataclassModule(void); /* proto */


//////////////////// DataclassModuleLoader ///////////////////////
//@requires: ModuleLoader
//@substitute: naming

static PyObject* __Pyx_LoadDataclassModule(void) {
    return __Pyx_LoadInternalModule("dataclasses", $dataclass_py_code);
}

///////////////////// TypingModuleLoader.proto ////////////////////////

static PyObject* __Pyx_LoadTypingModule(void); /* proto */

///////////////////// TypingModuleLoader ///////////////////////////
//@requires: ModuleLoader
//@substitute: naming

static PyObject* __Pyx_LoadTypingModule(void) {
    return __Pyx_LoadInternalModule("typing", $typing_py_code);
}
