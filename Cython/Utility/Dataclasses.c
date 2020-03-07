///////////////////// DataclassModuleLoader.proto //////////////////////

static PyObject* __Pyx_LoadDataclassModule(void); /* proto */


//////////////////// DataclassModuleLoader ///////////////////////
//@requires: CommonStructures.c::FetchCommonType
//@substitute: naming

static PyObject* __Pyx_LoadDataclassModule(void) {
    PyObject *shared_abi_module = 0, *dataclasses_module = 0;

    shared_abi_module = __Pyx_FetchSharedCythonABIModule();
    if (!shared_abi_module) return NULL;

    if (PyObject_HasAttrString(shared_abi_module, "dataclasses")) {
        PyObject* result = PyObject_GetAttrString(shared_abi_module, "dataclasses");
        Py_DECREF(shared_abi_module);
        return result;
    }

    // the best and simplest care is simply to defer to the standard library (if available)
    dataclasses_module = PyImport_ImportModule("dataclasses");
    if (!dataclasses_module) {
        PyObject *localDict, *runValue, *builtins;
        if (PyErr_ExceptionMatches(PyExc_ImportError)) {
            PyErr_Clear();  // this is reasonably likely (especially on older versions of Python)
        } else {
            goto bad;
        }
        dataclasses_module = PyImport_AddModule((char*)"_cython_" CYTHON_ABI ".dataclasses");
        if (!dataclasses_module) goto bad;
        if (PyObject_SetAttrString(shared_abi_module, "dataclasses", dataclasses_module)<0) goto bad;
        localDict = PyModule_GetDict(dataclasses_module); // borrowed
        if (!localDict) goto bad;
        builtins = PyEval_GetBuiltins(); // borrowed
        if (!builtins) goto bad;
        if (PyDict_SetItemString(localDict, "__builtins__", builtins) <0) goto bad;


        runValue = PyRun_String($dataclass_py_code, Py_file_input, localDict, localDict);

        if (!runValue) goto bad;
        Py_DECREF(runValue);
    }
    goto shared_cleanup;

    bad:
        Py_CLEAR(dataclasses_module);
    shared_cleanup:
        Py_XDECREF(shared_abi_module);
    return dataclasses_module;
}

//////////////////////////// DataclassFuncCaller.proto //////////////////////////////

static CYTHON_INLINE PyObject* __Pyx_Dataclass_caller(const char* name, PyObject* args, PyObject* kwds); /* proto */

//////////////////////////// DataclassFuncCaller ///////////////////////////////////
//@requires: DataclassModuleLoader

static CYTHON_INLINE PyObject* __Pyx_Dataclass_caller(const char* name, PyObject* args, PyObject* kwds) {
    PyObject *dataclass = NULL, result = NULL;
    PyObject *mod = __Pyx_LoadDataclassModule();
    if (!mod) return NULL;
    dataclass = PyObject_GetAttrString(mod, name);
    Py_DECREF(mod);
    if (!dataclass) return NULL;
    // these functions are typically called infrequently on init so no need for optimization
    result = PyObject_Call(dataclass, args, kwds);
    Py_DECREF(dataclass)
    return result;
}

//////////////////////////// Dataclass_dataclass.proto ///////////////////////////////////

static CYTHON_INLINE PyObject* __Pyx_Dataclass_dataclass(PyObject *args, PyObject *kwds); /* proto */

//////////////////////////// Dataclass_dataclass.proto ///////////////////////////////////
//@requires: DataclassFuncCaller

static CYTHON_INLINE PyObject* __Pyx_Dataclass_dataclass(PyObject *args, PyObject *kwds) {
    return __Pyx_Dataclass_caller("dataclass", args, kwds);
}

//////////////////////////// Dataclass_field.proto ///////////////////////////////////

static CYTHON_INLINE PyObject* __Pyx_Dataclass_field(PyObject *args, PyObject *kwds); /* proto */

//////////////////////////// Dataclass_field.proto ///////////////////////////////////
//@requires: DataclassFuncCaller

static CYTHON_INLINE PyObject* __Pyx_Dataclass_field(PyObject *args, PyObject *kwds) {
    return __Pyx_Dataclass_caller("field", args, kwds);
}

///////////////////////////// Dataclass

#if !CYTHON_COMPILING_IN_LIMITED_API
static PyTypeObject *__Pyx_Dataclass_field = 0;
static PyTypeObject *__Pyx_Dataclass_class = 0;
#endif
