
//////////////////// Globals.proto ////////////////////

static PyObject* __Pyx_Globals(void); /*proto*/

//////////////////// Globals ////////////////////
//@substitute: naming

// This is a stub implementation until we have something more complete.
// Currently, we only handle the most common case of a read-only dict
// of Python names.  Supporting cdef names in the module and write
// access requires a rewrite as a dedicated class.

static PyObject* __Pyx_Globals(void) {
    Py_ssize_t i;
    //PyObject *d;
    PyObject *names = NULL;
    PyObject *globals = PyObject_GetAttr($module_cname, PYIDENT("__dict__"));
    if (!globals) {
        PyErr_SetString(PyExc_TypeError,
            "current module must have __dict__ attribute");
        goto bad;
    }
    names = PyObject_Dir($module_cname);
    if (!names)
        goto bad;
    for (i = PyList_GET_SIZE(names)-1; i >= 0; i--) {
#if CYTHON_COMPILING_IN_PYPY
        PyObject* name = PySequence_GetItem(names, i);
        if (!name)
            goto bad;
#else
        PyObject* name = PyList_GET_ITEM(names, i);
#endif
        if (!PyDict_Contains(globals, name)) {
            PyObject* value = PyObject_GetAttr($module_cname, name);
            if (!value) {
#if CYTHON_COMPILING_IN_PYPY
                Py_DECREF(name);
#endif
                goto bad;
            }
            if (PyDict_SetItem(globals, name, value) < 0) {
#if CYTHON_COMPILING_IN_PYPY
                Py_DECREF(name);
#endif
                Py_DECREF(value);
                goto bad;
            }
        }
#if CYTHON_COMPILING_IN_PYPY
        Py_DECREF(name);
#endif
    }
    Py_DECREF(names);
    return globals;
    // d = PyDictProxy_New(globals);
    // Py_DECREF(globals);
    // return d;
bad:
    Py_XDECREF(names);
    Py_XDECREF(globals);
    return NULL;
}

//////////////////// PyExecGlobals.proto ////////////////////

static PyObject* __Pyx_PyExecGlobals(PyObject*);

//////////////////// PyExecGlobals ////////////////////
//@requires: Globals
//@requires: PyExec

static PyObject* __Pyx_PyExecGlobals(PyObject* code) {
    PyObject* result;
    PyObject* globals = __Pyx_Globals();
    if (unlikely(!globals))
        return NULL;
    result = __Pyx_PyExec2(code, globals);
    Py_DECREF(globals);
    return result;
}

//////////////////// PyExec.proto ////////////////////

static PyObject* __Pyx_PyExec3(PyObject*, PyObject*, PyObject*);
static CYTHON_INLINE PyObject* __Pyx_PyExec2(PyObject*, PyObject*);

//////////////////// PyExec ////////////////////
//@substitute: naming

static CYTHON_INLINE PyObject* __Pyx_PyExec2(PyObject* o, PyObject* globals) {
    return __Pyx_PyExec3(o, globals, NULL);
}

static PyObject* __Pyx_PyExec3(PyObject* o, PyObject* globals, PyObject* locals) {
    PyObject* result;
    PyObject* s = 0;
    char *code = 0;

    if (!globals || globals == Py_None) {
        globals = PyModule_GetDict($module_cname);
        if (!globals)
            goto bad;
    } else if (!PyDict_Check(globals)) {
        PyErr_Format(PyExc_TypeError, "exec() arg 2 must be a dict, not %.200s",
                     Py_TYPE(globals)->tp_name);
        goto bad;
    }
    if (!locals || locals == Py_None) {
        locals = globals;
    }

    if (PyDict_GetItem(globals, PYIDENT("__builtins__")) == NULL) {
        if (PyDict_SetItem(globals, PYIDENT("__builtins__"), PyEval_GetBuiltins()) < 0)
            goto bad;
    }

    if (PyCode_Check(o)) {
        if (PyCode_GetNumFree((PyCodeObject *)o) > 0) {
            PyErr_SetString(PyExc_TypeError,
                "code object passed to exec() may not contain free variables");
            goto bad;
        }
        #if PY_VERSION_HEX < 0x030200B1
        result = PyEval_EvalCode((PyCodeObject *)o, globals, locals);
        #else
        result = PyEval_EvalCode(o, globals, locals);
        #endif
    } else {
        PyCompilerFlags cf;
        cf.cf_flags = 0;
        if (PyUnicode_Check(o)) {
            cf.cf_flags = PyCF_SOURCE_IS_UTF8;
            s = PyUnicode_AsUTF8String(o);
            if (!s) goto bad;
            o = s;
        #if PY_MAJOR_VERSION >= 3
        } else if (!PyBytes_Check(o)) {
        #else
        } else if (!PyString_Check(o)) {
        #endif
            PyErr_Format(PyExc_TypeError,
                "exec: arg 1 must be string, bytes or code object, got %.200s",
                Py_TYPE(o)->tp_name);
            goto bad;
        }
        #if PY_MAJOR_VERSION >= 3
        code = PyBytes_AS_STRING(o);
        #else
        code = PyString_AS_STRING(o);
        #endif
        if (PyEval_MergeCompilerFlags(&cf)) {
            result = PyRun_StringFlags(code, Py_file_input, globals, locals, &cf);
        } else {
            result = PyRun_String(code, Py_file_input, globals, locals);
        }
        Py_XDECREF(s);
    }

    return result;
bad:
    Py_XDECREF(s);
    return 0;
}

//////////////////// GetAttr.proto ////////////////////

static CYTHON_INLINE PyObject *__Pyx_GetAttr(PyObject *, PyObject *); /*proto*/

//////////////////// GetAttr ////////////////////
//@requires: ObjectHandling.c::PyObjectGetAttrStr

static CYTHON_INLINE PyObject *__Pyx_GetAttr(PyObject *o, PyObject *n) {
#if CYTHON_COMPILING_IN_CPYTHON
#if PY_MAJOR_VERSION >= 3
    if (likely(PyUnicode_Check(n)))
#else
    if (likely(PyString_Check(n)))
#endif
        return __Pyx_PyObject_GetAttrStr(o, n);
#endif
    return PyObject_GetAttr(o, n);
}

//////////////////// GetAttr3.proto ////////////////////

static CYTHON_INLINE PyObject *__Pyx_GetAttr3(PyObject *, PyObject *, PyObject *); /*proto*/

//////////////////// GetAttr3 ////////////////////
//@requires: GetAttr

static CYTHON_INLINE PyObject *__Pyx_GetAttr3(PyObject *o, PyObject *n, PyObject *d) {
    PyObject *r = __Pyx_GetAttr(o, n);
    if (!r) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError))
            goto bad;
        PyErr_Clear();
        r = d;
        Py_INCREF(d);
    }
    return r;
bad:
    return NULL;
}

//////////////////// Intern.proto ////////////////////

static PyObject* __Pyx_Intern(PyObject* s); /* proto */

//////////////////// Intern ////////////////////

static PyObject* __Pyx_Intern(PyObject* s) {
    if (!(likely(PyString_CheckExact(s)))) {
        PyErr_Format(PyExc_TypeError, "Expected str, got %s", Py_TYPE(s)->tp_name);
        return 0;
    }
    Py_INCREF(s);
    #if PY_MAJOR_VERSION >= 3
    PyUnicode_InternInPlace(&s);
    #else
    PyString_InternInPlace(&s);
    #endif
    return s;
}

//////////////////// abs_int.proto ////////////////////

static CYTHON_INLINE unsigned int __Pyx_abs_int(int x) {
    if (unlikely(x == -INT_MAX-1))
        return ((unsigned int)INT_MAX) + 1U;
    return (unsigned int) abs(x);
}

//////////////////// abs_long.proto ////////////////////

static CYTHON_INLINE unsigned long __Pyx_abs_long(long x) {
    if (unlikely(x == -LONG_MAX-1))
        return ((unsigned long)LONG_MAX) + 1U;
    return (unsigned long) labs(x);
}

//////////////////// abs_longlong.proto ////////////////////

static CYTHON_INLINE unsigned PY_LONG_LONG __Pyx_abs_longlong(PY_LONG_LONG x) {
#ifndef PY_LLONG_MAX
#ifdef LLONG_MAX
    const PY_LONG_LONG PY_LLONG_MAX = LLONG_MAX;
#else
    // copied from pyport.h in CPython 3.3, missing in 2.4
    const PY_LONG_LONG PY_LLONG_MAX = (1 + 2 * ((1LL << (CHAR_BIT * sizeof(PY_LONG_LONG) - 2)) - 1));
#endif
#endif
    if (unlikely(x == -PY_LLONG_MAX-1))
        return ((unsigned PY_LONG_LONG)PY_LLONG_MAX) + 1U;
#if defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    return (unsigned PY_LONG_LONG) llabs(x);
#else
    return (x<0) ? (unsigned PY_LONG_LONG)-x : (unsigned PY_LONG_LONG)x;
#endif
}

//////////////////// pow2.proto ////////////////////

#define __Pyx_PyNumber_Power2(a, b) PyNumber_Power(a, b, Py_None)

//////////////////// py_dict_keys.proto ////////////////////

#if PY_MAJOR_VERSION >= 3
static CYTHON_INLINE PyObject* __Pyx_PyDict_Keys(PyObject* d); /*proto*/
#else
#define __Pyx_PyDict_Keys(d) PyDict_Keys(d)
#endif

//////////////////// py_dict_keys ////////////////////

#if PY_MAJOR_VERSION >= 3
static CYTHON_INLINE PyObject* __Pyx_PyDict_Keys(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, PYIDENT("keys"), NULL);
}
#endif

//////////////////// py_dict_values.proto ////////////////////

#if PY_MAJOR_VERSION >= 3
static CYTHON_INLINE PyObject* __Pyx_PyDict_Values(PyObject* d); /*proto*/
#else
#define __Pyx_PyDict_Values(d) PyDict_Values(d)
#endif

//////////////////// py_dict_values ////////////////////

#if PY_MAJOR_VERSION >= 3
static CYTHON_INLINE PyObject* __Pyx_PyDict_Values(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, PYIDENT("values"), NULL);
}
#endif

//////////////////// py_dict_items.proto ////////////////////

#if PY_MAJOR_VERSION >= 3
static CYTHON_INLINE PyObject* __Pyx_PyDict_Items(PyObject* d); /*proto*/
#else
#define __Pyx_PyDict_Items(d) PyDict_Items(d)
#endif

//////////////////// py_dict_items ////////////////////

#if PY_MAJOR_VERSION >= 3
static CYTHON_INLINE PyObject* __Pyx_PyDict_Items(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, PYIDENT("items"), NULL);
}
#endif

//////////////////// py_dict_iterkeys.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterKeys(PyObject* d); /*proto*/

//////////////////// py_dict_iterkeys ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterKeys(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, (PY_MAJOR_VERSION >= 3) ? PYIDENT("keys") : PYIDENT("iterkeys"), NULL);
}

//////////////////// py_dict_itervalues.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterValues(PyObject* d); /*proto*/

//////////////////// py_dict_itervalues ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterValues(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, (PY_MAJOR_VERSION >= 3) ? PYIDENT("values") : PYIDENT("itervalues"), NULL);
}

//////////////////// py_dict_iteritems.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterItems(PyObject* d); /*proto*/

//////////////////// py_dict_iteritems ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterItems(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, (PY_MAJOR_VERSION >= 3) ? PYIDENT("items") : PYIDENT("iteritems"), NULL);
}

//////////////////// py_dict_viewkeys.proto ////////////////////

#if PY_VERSION_HEX < 0x02070000
#error This module uses dict views, which require Python 2.7 or later
#endif
static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewKeys(PyObject* d); /*proto*/

//////////////////// py_dict_viewkeys ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewKeys(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, (PY_MAJOR_VERSION >= 3) ? PYIDENT("keys") : PYIDENT("viewkeys"), NULL);
}

//////////////////// py_dict_viewvalues.proto ////////////////////

#if PY_VERSION_HEX < 0x02070000
#error This module uses dict views, which require Python 2.7 or later
#endif
static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewValues(PyObject* d); /*proto*/

//////////////////// py_dict_viewvalues ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewValues(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, (PY_MAJOR_VERSION >= 3) ? PYIDENT("values") : PYIDENT("viewvalues"), NULL);
}

//////////////////// py_dict_viewitems.proto ////////////////////

#if PY_VERSION_HEX < 0x02070000
#error This module uses dict views, which require Python 2.7 or later
#endif
static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewItems(PyObject* d); /*proto*/

//////////////////// py_dict_viewitems ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewItems(PyObject* d) {
    return PyObject_CallMethodObjArgs(d, (PY_MAJOR_VERSION >= 3) ? PYIDENT("items") : PYIDENT("viewitems"), NULL);
}
