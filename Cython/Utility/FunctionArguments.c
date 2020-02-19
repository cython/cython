//////////////////// ArgTypeTest.proto ////////////////////


#define __Pyx_ArgTypeTest(obj, type, none_allowed, name, exact) \
    ((likely((Py_TYPE(obj) == type) | (none_allowed && (obj == Py_None)))) ? 1 : \
        __Pyx__ArgTypeTest(obj, type, name, exact))

static int __Pyx__ArgTypeTest(PyObject *obj, PyTypeObject *type, const char *name, int exact); /*proto*/

//////////////////// ArgTypeTest ////////////////////

static int __Pyx__ArgTypeTest(PyObject *obj, PyTypeObject *type, const char *name, int exact)
{
    if (unlikely(!type)) {
        PyErr_SetString(PyExc_SystemError, "Missing type object");
        return 0;
    }
    else if (exact) {
        #if PY_MAJOR_VERSION == 2
        if ((type == &PyBaseString_Type) && likely(__Pyx_PyBaseString_CheckExact(obj))) return 1;
        #endif
    }
    else {
        if (likely(__Pyx_TypeCheck(obj, type))) return 1;
    }
    PyErr_Format(PyExc_TypeError,
        "Argument '%.200s' has incorrect type (expected %.200s, got %.200s)",
        name, type->tp_name, Py_TYPE(obj)->tp_name);
    return 0;
}

//////////////////// RaiseArgTupleInvalid.proto ////////////////////

static void __Pyx_RaiseArgtupleInvalid(const char* func_name, int exact,
    Py_ssize_t num_min, Py_ssize_t num_max, Py_ssize_t num_found); /*proto*/

//////////////////// RaiseArgTupleInvalid ////////////////////

//  __Pyx_RaiseArgtupleInvalid raises the correct exception when too
//  many or too few positional arguments were found.  This handles
//  Py_ssize_t formatting correctly.

static void __Pyx_RaiseArgtupleInvalid(
    const char* func_name,
    int exact,
    Py_ssize_t num_min,
    Py_ssize_t num_max,
    Py_ssize_t num_found)
{
    Py_ssize_t num_expected;
    const char *more_or_less;

    if (num_found < num_min) {
        num_expected = num_min;
        more_or_less = "at least";
    } else {
        num_expected = num_max;
        more_or_less = "at most";
    }
    if (exact) {
        more_or_less = "exactly";
    }
    PyErr_Format(PyExc_TypeError,
                 "%.200s() takes %.8s %" CYTHON_FORMAT_SSIZE_T "d positional argument%.1s (%" CYTHON_FORMAT_SSIZE_T "d given)",
                 func_name, more_or_less, num_expected,
                 (num_expected == 1) ? "" : "s", num_found);
}


//////////////////// RaiseKeywordRequired.proto ////////////////////

static void __Pyx_RaiseKeywordRequired(const char* func_name, PyObject* kw_name); /*proto*/

//////////////////// RaiseKeywordRequired ////////////////////

static void __Pyx_RaiseKeywordRequired(const char* func_name, PyObject* kw_name) {
    PyErr_Format(PyExc_TypeError,
        #if PY_MAJOR_VERSION >= 3
        "%s() needs keyword-only argument %U", func_name, kw_name);
        #else
        "%s() needs keyword-only argument %s", func_name,
        PyString_AS_STRING(kw_name));
        #endif
}


//////////////////// RaiseDoubleKeywords.proto ////////////////////

static void __Pyx_RaiseDoubleKeywordsError(const char* func_name, PyObject* kw_name); /*proto*/

//////////////////// RaiseDoubleKeywords ////////////////////

static void __Pyx_RaiseDoubleKeywordsError(
    const char* func_name,
    PyObject* kw_name)
{
    PyErr_Format(PyExc_TypeError,
        #if PY_MAJOR_VERSION >= 3
        "%s() got multiple values for keyword argument '%U'", func_name, kw_name);
        #else
        "%s() got multiple values for keyword argument '%s'", func_name,
        PyString_AsString(kw_name));
        #endif
}


//////////////////// RaiseMappingExpected.proto ////////////////////

static void __Pyx_RaiseMappingExpectedError(PyObject* arg); /*proto*/

//////////////////// RaiseMappingExpected ////////////////////

static void __Pyx_RaiseMappingExpectedError(PyObject* arg) {
    PyErr_Format(PyExc_TypeError, "'%.200s' object is not a mapping", Py_TYPE(arg)->tp_name);
}


//////////////////// KeywordStringCheck.proto ////////////////////

static int __Pyx_CheckKeywordStrings(PyObject *kw, const char* function_name, int kw_allowed); /*proto*/

//////////////////// KeywordStringCheck ////////////////////

// __Pyx_CheckKeywordStrings raises an error if non-string keywords
// were passed to a function, or if any keywords were passed to a
// function that does not accept them.
//
// The "kw" argument is either a dict (for METH_VARARGS) or a tuple
// (for METH_FASTCALL).

static int __Pyx_CheckKeywordStrings(
    PyObject *kw,
    const char* function_name,
    int kw_allowed)
{
    PyObject* key = 0;
    Py_ssize_t pos = 0;
#if CYTHON_COMPILING_IN_PYPY
    /* PyPy appears to check keywords at call time, not at unpacking time => not much to do here */
    if (!kw_allowed && PyDict_Next(kw, &pos, &key, 0))
        goto invalid_keyword;
    return 1;
#else
    if (CYTHON_METH_FASTCALL && likely(PyTuple_Check(kw))) {
        if (unlikely(PyTuple_GET_SIZE(kw) == 0))
            return 1;
        if (!kw_allowed)
            goto invalid_keyword;
#if PY_VERSION_HEX < 0x03090000
        // On CPython >= 3.9, the FASTCALL protocol guarantees that keyword
        // names are strings (see https://bugs.python.org/issue37540)
        for (pos = 0; pos < PyTuple_GET_SIZE(kw); pos++) {
            key = PyTuple_GET_ITEM(kw, pos);
            if (unlikely(!PyUnicode_Check(key)))
                goto invalid_keyword_type;
        }
#endif
        return 1;
    }

    while (PyDict_Next(kw, &pos, &key, 0)) {
        #if PY_MAJOR_VERSION < 3
        if (unlikely(!PyString_Check(key)))
        #endif
            if (unlikely(!PyUnicode_Check(key)))
                goto invalid_keyword_type;
    }
    if (!kw_allowed && unlikely(key))
        goto invalid_keyword;
    return 1;
invalid_keyword_type:
    PyErr_Format(PyExc_TypeError,
        "%.200s() keywords must be strings", function_name);
    return 0;
#endif
invalid_keyword:
    #if PY_MAJOR_VERSION < 3
    PyErr_Format(PyExc_TypeError,
        "%.200s() got an unexpected keyword argument '%.200s'",
        function_name, PyString_AsString(key));
    #else
    PyErr_Format(PyExc_TypeError,
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
    #endif
    return 0;
}


//////////////////// ParseKeywords.proto ////////////////////

static int __Pyx_ParseOptionalKeywords(PyObject *kwds, PyObject *const *kwvalues,
    PyObject **argnames[],
    PyObject *kwds2, PyObject *values[], Py_ssize_t num_pos_args,
    const char* function_name); /*proto*/

//////////////////// ParseKeywords ////////////////////
//@requires: RaiseDoubleKeywords

//  __Pyx_ParseOptionalKeywords copies the optional/unknown keyword
//  arguments from kwds into the dict kwds2.  If kwds2 is NULL, unknown
//  keywords will raise an invalid keyword error.
//
//  When not using METH_FASTCALL, kwds is a dict and kwvalues is NULL.
//  Otherwise, kwds is a tuple with keyword names and kwvalues is a C
//  array with the corresponding values.
//
//  Three kinds of errors are checked: 1) non-string keywords, 2)
//  unexpected keywords and 3) overlap with positional arguments.
//
//  If num_posargs is greater 0, it denotes the number of positional
//  arguments that were passed and that must therefore not appear
//  amongst the keywords as well.
//
//  This method does not check for required keyword arguments.

static int __Pyx_ParseOptionalKeywords(
    PyObject *kwds,
    PyObject *const *kwvalues,
    PyObject **argnames[],
    PyObject *kwds2,
    PyObject *values[],
    Py_ssize_t num_pos_args,
    const char* function_name)
{
    PyObject *key = 0, *value = 0;
    Py_ssize_t pos = 0;
    PyObject*** name;
    PyObject*** first_kw_arg = argnames + num_pos_args;
    int kwds_is_tuple = CYTHON_METH_FASTCALL && likely(PyTuple_Check(kwds));

    while (1) {
        if (kwds_is_tuple) {
            if (pos >= PyTuple_GET_SIZE(kwds)) break;
            key = PyTuple_GET_ITEM(kwds, pos);
            value = kwvalues[pos];
            pos++;
        }
        else
        {
            if (!PyDict_Next(kwds, &pos, &key, &value)) break;
        }

        name = first_kw_arg;
        while (*name && (**name != key)) name++;
        if (*name) {
            values[name-argnames] = value;
            continue;
        }

        name = first_kw_arg;
        #if PY_MAJOR_VERSION < 3
        if (likely(PyString_CheckExact(key)) || likely(PyString_Check(key))) {
            while (*name) {
                if ((CYTHON_COMPILING_IN_PYPY || PyString_GET_SIZE(**name) == PyString_GET_SIZE(key))
                        && _PyString_Eq(**name, key)) {
                    values[name-argnames] = value;
                    break;
                }
                name++;
            }
            if (*name) continue;
            else {
                // not found after positional args, check for duplicate
                PyObject*** argname = argnames;
                while (argname != first_kw_arg) {
                    if ((**argname == key) || (
                            (CYTHON_COMPILING_IN_PYPY || PyString_GET_SIZE(**argname) == PyString_GET_SIZE(key))
                             && _PyString_Eq(**argname, key))) {
                        goto arg_passed_twice;
                    }
                    argname++;
                }
            }
        } else
        #endif
        if (likely(PyUnicode_Check(key))) {
            while (*name) {
                int cmp = (**name == key) ? 0 :
                #if !CYTHON_COMPILING_IN_PYPY && PY_MAJOR_VERSION >= 3
                    (PyUnicode_GET_SIZE(**name) != PyUnicode_GET_SIZE(key)) ? 1 :
                #endif
                    // need to convert argument name from bytes to unicode for comparison
                    PyUnicode_Compare(**name, key);
                if (cmp < 0 && unlikely(PyErr_Occurred())) goto bad;
                if (cmp == 0) {
                    values[name-argnames] = value;
                    break;
                }
                name++;
            }
            if (*name) continue;
            else {
                // not found after positional args, check for duplicate
                PyObject*** argname = argnames;
                while (argname != first_kw_arg) {
                    int cmp = (**argname == key) ? 0 :
                    #if !CYTHON_COMPILING_IN_PYPY && PY_MAJOR_VERSION >= 3
                        (PyUnicode_GET_SIZE(**argname) != PyUnicode_GET_SIZE(key)) ? 1 :
                    #endif
                        // need to convert argument name from bytes to unicode for comparison
                        PyUnicode_Compare(**argname, key);
                    if (cmp < 0 && unlikely(PyErr_Occurred())) goto bad;
                    if (cmp == 0) goto arg_passed_twice;
                    argname++;
                }
            }
        } else
            goto invalid_keyword_type;

        if (kwds2) {
            if (unlikely(PyDict_SetItem(kwds2, key, value))) goto bad;
        } else {
            goto invalid_keyword;
        }
    }
    return 0;
arg_passed_twice:
    __Pyx_RaiseDoubleKeywordsError(function_name, key);
    goto bad;
invalid_keyword_type:
    PyErr_Format(PyExc_TypeError,
        "%.200s() keywords must be strings", function_name);
    goto bad;
invalid_keyword:
    #if PY_MAJOR_VERSION < 3
    PyErr_Format(PyExc_TypeError,
        "%.200s() got an unexpected keyword argument '%.200s'",
        function_name, PyString_AsString(key));
    #else
    PyErr_Format(PyExc_TypeError,
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
    #endif
bad:
    return -1;
}


//////////////////// MergeKeywords.proto ////////////////////

static int __Pyx_MergeKeywords(PyObject *kwdict, PyObject *source_mapping); /*proto*/

//////////////////// MergeKeywords ////////////////////
//@requires: RaiseDoubleKeywords
//@requires: Optimize.c::dict_iter

static int __Pyx_MergeKeywords(PyObject *kwdict, PyObject *source_mapping) {
    PyObject *iter, *key = NULL, *value = NULL;
    int source_is_dict, result;
    Py_ssize_t orig_length, ppos = 0;

    iter = __Pyx_dict_iterator(source_mapping, 0, PYIDENT("items"), &orig_length, &source_is_dict);
    if (unlikely(!iter)) {
        // slow fallback: try converting to dict, then iterate
        PyObject *args;
        if (!PyErr_ExceptionMatches(PyExc_AttributeError)) goto bad;
        PyErr_Clear();
        args = PyTuple_Pack(1, source_mapping);
        if (likely(args)) {
            PyObject *fallback = PyObject_Call((PyObject*)&PyDict_Type, args, NULL);
            Py_DECREF(args);
            if (likely(fallback)) {
                iter = __Pyx_dict_iterator(fallback, 1, PYIDENT("items"), &orig_length, &source_is_dict);
                Py_DECREF(fallback);
            }
        }
        if (unlikely(!iter)) goto bad;
    }

    while (1) {
        result = __Pyx_dict_iter_next(iter, orig_length, &ppos, &key, &value, NULL, source_is_dict);
        if (unlikely(result < 0)) goto bad;
        if (!result) break;

        if (unlikely(PyDict_Contains(kwdict, key))) {
            __Pyx_RaiseDoubleKeywordsError("function", key);
            result = -1;
        } else {
            result = PyDict_SetItem(kwdict, key, value);
        }
        Py_DECREF(key);
        Py_DECREF(value);
        if (unlikely(result < 0)) goto bad;
    }
    Py_XDECREF(iter);
    return 0;

bad:
    Py_XDECREF(iter);
    return -1;
}


/////////////// fastcall.proto ///////////////

// We define various functions and macros with two variants:
//..._FASTCALL and ..._VARARGS

// The first is used when METH_FASTCALL is enabled and the second is used
// otherwise. If the Python implementation does not support METH_FASTCALL
// (because it's an old version of CPython or it's not CPython at all),
// then the ..._FASTCALL macros simply alias ..._VARARGS

#define __Pyx_Arg_VARARGS(args, i) PyTuple_GET_ITEM(args, i)
#define __Pyx_NumKwargs_VARARGS(kwds) PyDict_Size(kwds)
#define __Pyx_KwValues_VARARGS(args, nargs) NULL
#define __Pyx_GetKwValue_VARARGS(kw, kwvalues, s) __Pyx_PyDict_GetItemStrWithError(kw, s)
#define __Pyx_KwargsAsDict_VARARGS(kw, kwvalues) PyDict_Copy(kw)
#if CYTHON_METH_FASTCALL
    #define __Pyx_Arg_FASTCALL(args, i) args[i]
    #define __Pyx_NumKwargs_FASTCALL(kwds) PyTuple_GET_SIZE(kwds)
    #define __Pyx_KwValues_FASTCALL(args, nargs) (&args[nargs])
    static CYTHON_INLINE PyObject * __Pyx_GetKwValue_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues, PyObject *s);
    #define __Pyx_KwargsAsDict_FASTCALL(kw, kwvalues) _PyStack_AsDict(kwvalues, kw)
#else
    #define __Pyx_Arg_FASTCALL __Pyx_Arg_VARARGS
    #define __Pyx_NumKwargs_FASTCALL __Pyx_NumKwargs_VARARGS
    #define __Pyx_KwValues_FASTCALL __Pyx_KwValues_VARARGS
    #define __Pyx_GetKwValue_FASTCALL __Pyx_GetKwValue_VARARGS
    #define __Pyx_KwargsAsDict_FASTCALL __Pyx_KwargsAsDict_VARARGS
#endif

#if CYTHON_COMPILING_IN_CPYTHON
#define __Pyx_ArgsSlice_VARARGS(args, start, stop) __Pyx_PyTuple_FromArray(&__Pyx_Arg_VARARGS(args, start), stop - start)
#define __Pyx_ArgsSlice_FASTCALL(args, start, stop) __Pyx_PyTuple_FromArray(&__Pyx_Arg_FASTCALL(args, start), stop - start)
#else
/* Not CPython, so certainly no METH_FASTCALL support */
#define __Pyx_ArgsSlice_VARARGS(args, start, stop) PyTuple_GetSlice(args, start, stop)
#define __Pyx_ArgsSlice_FASTCALL(args, start, stop) PyTuple_GetSlice(args, start, stop)
#endif


/////////////// fastcall ///////////////
//@requires: ObjectHandling.c::TupleAndListFromArray
//@requires: StringTools.c::UnicodeEquals

#if CYTHON_METH_FASTCALL
// kwnames: tuple with names of keyword arguments
// kwvalues: C array with values of keyword arguments
// s: str with the keyword name to look for
static CYTHON_INLINE PyObject * __Pyx_GetKwValue_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues, PyObject *s)
{
    // Search the kwnames array for s and return the corresponding value.
    // We do two loops: a first one to compare pointers (which will find a
    // match if the name in kwnames is interned, given that s is interned
    // by Cython). A second loop compares the actual strings.
    Py_ssize_t i, n = PyTuple_GET_SIZE(kwnames);
    for (i = 0; i < n; i++)
    {
        if (s == PyTuple_GET_ITEM(kwnames, i)) return kwvalues[i];
    }
    for (i = 0; i < n; i++)
    {
        int eq = __Pyx_PyUnicode_Equals(s, PyTuple_GET_ITEM(kwnames, i), Py_EQ);
        if (unlikely(eq != 0)) {
            if (unlikely(eq < 0)) return NULL;  // error
            return kwvalues[i];
        }
    }
    return NULL;  // not found (no exception set)
}
#endif

/////////////// fastcall_tuple.proto ///////////////
// A struct which can be created cheaply without needing to construct a Python object

#if CYTHON_COMPILING_IN_CPYTHON
typedef struct {
    PyObject *const *args;
    Py_ssize_t nargs;
} __Pyx_FastcallTuple_obj;
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_New(PyObject *const *args, Py_ssize_t nargs);
#else
typedef struct {
    PyObject* referenced_tuple;  // not owned by this struct
    // The two indices are relative to "referenced_tuple"
    Py_ssize_t start_idx;
    Py_ssize_t end_idx;
} __Pyx_FastcallTuple_obj;
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_New(PyObject *rt, Py_ssize_t start_idx, Py_ssize_t end_idx);
#endif

static CYTHON_INLINE Py_ssize_t __Pyx_FastcallTuple_Len(__Pyx_FastcallTuple_obj o);
static CYTHON_INLINE PyObject *__Pyx_FastcallTuple_ToTuple(__Pyx_FastcallTuple_obj o);

#if CYTHON_METH_FASTCALL
    static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_FASTCALL_struct(PyObject *const *args, Py_ssize_t start, Py_ssize_t stop);
#else
#define __Pyx_ArgsSlice_FASTCALL_struct(PyObject *args, Py_ssize_t start, Py_ssize_t stop) __Pyx_ArgsSlice_VARARGS_struct(args, start, stop)
#endif
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_VARARGS_struct(PyObject *args, Py_ssize_t start, Py_ssize_t stop);

// no type-checking - used for conversion in function call
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_FromTuple(PyObject* o);

/////////////// fastcall_tuple ///////////////
//@requires: ObjectHandling.c::PyVectorcallNargs

#if CYTHON_COMPILING_IN_CPYTHON
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_New(PyObject *const *args, Py_ssize_t nargs) {
    __Pyx_FastcallTuple_obj out = { args, nargs };
    return out;
}
#else
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_New(PyObject *rt, Py_ssize_t start_idx, Py_ssize_t end_idx) {
    __Pyx_FastcallTuple_obj out = { rt, start_idx, end_idx };
    return out;
}
#endif

static CYTHON_INLINE Py_ssize_t __Pyx_FastcallTuple_Len(__Pyx_FastcallTuple_obj o) {
#if CYTHON_COMPILING_IN_CPYTHON
    return __Pyx_PyVectorcall_NARGS(o.nargs);
#else
    return o.end_idx - o.start_idx;
#endif
}

static CYTHON_INLINE PyObject *__Pyx_FastcallTuple_ToTuple(__Pyx_FastcallTuple_obj o) {
#if CYTHON_COMPILING_IN_CPYTHON
    return __Pyx_PyTuple_FromArray(o.args, __Pyx_FastcallTuple_Len(o));
#else
    return PySequence_GetSlice(o.referenced_tuple, o.start_idx, os.stop_idx);
#endif
}

#if CYTHON_METH_FASTCALL
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_FASTCALL_struct(PyObject *const *args, Py_ssize_t start, Py_ssize_t stop) {
    Py_ssize_t nargs = (stop - start);
#if CYTHON_VECTORCALL
    if (start > 0) {
        nargs |= PY_VECTORCALL_ARGUMENTS_OFFSET; // we know there's at least one space in front
    }
#endif
    return __Pyx_FastcallTuple_New(args+start, nargs);
}
#endif // CYTHON_METH_FASTCALL

static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_VARARGS_struct(PyObject *args, Py_ssize_t start, Py_ssize_t stop) {
    __Pyx_FastcallTuple_obj out = __Pyx_FastcallTuple_FromTuple(args);
#if CYTHON_COMPILING_IN_CPYTHON
    out.args += start;
    out.nargs = stop-start;
#else
    out.start_idx = start;
    out.end_idx = stop;
#endif
    return out;
}

static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_FromTuple(PyObject* o) {
#if !CYTHON_COMPILING_IN_CPYTHON
    return __Pyx_FastcallTuple_New(o, 0, PyTuple_Size(0));
#else
    return __Pyx_FastcallTuple_New(&PyTuple_GET_ITEM(o,0), PyTuple_GET_SIZE(o));
#endif
}

/////////////// fastcall_tuple_indexing.proto ///////////////
//@requires: fastcall_tuple

// based on ObjectHandling.c
#define __Pyx_GetItemInt_FastcallTuple(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck) \
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ? \
    __Pyx_GetItemInt_FastcallTuple_Fast(o, (Py_ssize_t)i, wraparound, boundscheck) : \
    (PyErr_SetString(PyExc_IndexError, "tuple index out of range"), (PyObject*)NULL))
static CYTHON_INLINE PyObject *__Pyx_GetItemInt_FastcallTuple_Fast(__Pyx_FastcallTuple_obj o, Py_ssize_t i,
                                                              int wraparound, int boundscheck);
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_SliceIndex(__Pyx_FastcallTuple_obj in,
                                                            Py_ssize_t start, Py_ssize_t stop, int wraparound);

/////////////// fastcall_tuple_indexing ///////////////

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_FastcallTuple_Fast(__Pyx_FastcallTuple_obj o, Py_ssize_t i,
                                                              int wraparound, int boundscheck) {
    Py_ssize_t len = __Pyx_FastcallTuple_Len(o);
    if (wraparound) {
        if (i < 0) {
            i = len + i;
        }
    }
    if (boundscheck) {
        if ((i < 0) || (i >= len)) {
            PyErr_SetString(PyExc_IndexError, "tuple index out of range");
            return NULL;
        }
    }

#if CYTHON_COMPILING_IN_CPYTHON
    PyObject* result = o.args[i];
    Py_INCREF(result);
    return result;
#else
    Py_ssize_t i_actual = i+o.start_idx;
    return PyTuple_GetItem(o.referenced_tuple, i_actual); // TODO ideally use __Pyx_GetItemInt_Tuple_Fast
                                                   // but need to work out how to include it reliably
#endif
}

static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_SliceIndex(__Pyx_FastcallTuple_obj in, Py_ssize_t start, Py_ssize_t stop, int wraparound) {
    if (stop < start) {
        return in;
    }
    Py_ssize_t len_in = __Pyx_FastcallTuple_Len(in);
    if (wraparound) {
        if (start < 0) start = len_in + start;
        if (stop < 0) stop = len_in + stop;
    }
    if (start < 0) start = 0;
    if (stop < 0) stop = 0;
    Py_ssize_t out_len = stop - start;
    if (out_len < 0) out_len = 0;

#if CYTHON_COMPILING_IN_CPYTHON
#if CYTHON_VECTORCALL
    if ((start > 0) || (in.nargs & PY_VECTORCALL_ARGUMENTS_OFFSET)) {
        out_len |= PY_VECTORCALL_ARGUMENTS_OFFSET;
    }
#endif // CYTHON_VECTORCALL
    return __Pyx_FastcallTuple_New(in.args + start, out_len);
#else // CYTHON_COMPILING_IN_CPYTHON
    return __Pyx_FastcallTuple_New(in.referenced_tuple, start+in.start_idx, stop+in.start_idx);
#endif
}


/////////////////// fastcall_dict.proto /////////////////////////

typedef struct {
    PyObject *const *args; // start of the keyword args values
    PyObject *object;      // either a dict, a tuple or NULL
} __Pyx_FastcallDict_obj;
// exists in one of three states:
// * args is NULL, "object" is NULL, meaning no keyword arguments
// * args is NULL, in which case "object" is actually a dict, and this just defers to the dict methods
// * args is non-null, kwnames is a tuple
// Defaults to "object" being a dict unless one of the quicker options can be easily created

static CYTHON_UNUSED Py_ssize_t __Pyx_FastcallDict_Len(__Pyx_FastcallDict_obj *o); /* proto */
static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_FastcallDict_New(void); /* proto */

/////////////////// fastcall_dict //////////////////////

static CYTHON_UNUSED Py_ssize_t __Pyx_FastcallDict_Len(__Pyx_FastcallDict_obj *o) {
    if (o->object == NULL) {
        return 0;
    } else if (o->args) {
        return PyTuple_GET_SIZE(o->object);
    } else {
        return PyDict_Size(o->object);
    }
}

static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_FastcallDict_New(void) {
    __Pyx_FastcallDict_obj out = {};
    return out;
}

/////////////////// fastcall_dict_convert.proto //////////////////////

static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_ToDict(__Pyx_FastcallDict_obj *o); /* proto */
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_ToDict_Explicit(__Pyx_FastcallDict_obj *o); /* proto */

/////////////////// fastcall_dict_convert //////////////////////
//@requires: fastcall

static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_ToDict(__Pyx_FastcallDict_obj *o){
    // when implicitly converted to dict change o.object so that modifications
    // to the dict propagate
    PyObject* dict = __Pyx_FastcallDict_ToDict_Explicit(o);
    if (!dict) return NULL;
    o->args = NULL;
    Py_CLEAR(o->object);
    o->object = dict;
    Py_INCREF(dict);
    return dict;
}
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_ToDict_Explicit(__Pyx_FastcallDict_obj* o) {
    if (o->object == NULL) {
        return PyDict_New();
    } else if (o->args) {
        return __Pyx_KwargsAsDict_FASTCALL(o->object, o->args);
    } else { // already a dict
        Py_INCREF(o->object);
        return o->object;
    }
}

/////////////////// fastcall_dict_iter.proto //////////////////////

// These methods behaves slightly differently from the regular dict methods
// in that they just return a list rather than an iterator. For most of them
// an iterator would be dangerous since it might outlive the __Pyx_FastcallDict_obj
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_Keys(__Pyx_FastcallDict_obj* o);
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_Values(__Pyx_FastcallDict_obj* o);
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_Items(__Pyx_FastcallDict_obj* o);

/////////////////// fastcall_dict_iter //////////////////////
//@requires:ObjectHandling.c::TupleAndListFromArray

static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_Keys(__Pyx_FastcallDict_obj *o) {
    if (o->object == NULL) {
        return PyList_New(0);
    } else if (o->args) {
        Py_INCREF(o->object);
        return o->object;  // a tuple
    } else {
        return PyDict_Keys(o->object);
    }
}
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_Values(__Pyx_FastcallDict_obj *o) {
    if (o->object == NULL) {
        return PyList_New(0);
    } else if (o->args) {
        return __Pyx_PyList_FromArray(o->args, __Pyx_FastcallDict_Len(o));  // a tuple
    } else {
        return PyDict_Values(o->object);
    }
}
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_Items(__Pyx_FastcallDict_obj* o) {
    if (o->object == NULL) {
        return PyList_New(0);
    } else if (o->args) {
        PyObject* output = NULL;
        Py_ssize_t len = PyTuple_GET_SIZE(o->object);
        Py_ssize_t i;
        output = PyTuple_New(len);
        if (!output) return NULL;
        for (i=0; i<len; ++i) {
            PyObject* this_item = PyTuple_Pack(2, PyTuple_GET_ITEM(o->object, i), o->args[i]);
            if (!this_item) {
                Py_CLEAR(output);
                break;
            }
            PyTuple_SET_ITEM(output, i, this_item);
        }
        return output;
    } else {
        return PyDict_Items(o->object);
    }
}

/////////////////// fastcall_dict_loopiter.proto //////////////////////

static CYTHON_INLINE PyObject* __Pyx_dict_iterator_fastcalldict(__Pyx_FastcallDict_obj* iterable,
                                                                int is_dict, PyObject* method_name,
                                                   Py_ssize_t* p_orig_length, int* p_source_is_dict);

/////////////////// fastcall_dict_loopiter //////////////////////
// fastcall_dict_iter
//@requires:Optimize.c::dict_iter // partly to get __Pyx_dict_iter_next (which we don't need to redefine)
//@requires:fastcall_dict_iter

static CYTHON_INLINE PyObject* __Pyx_dict_iterator_fastcalldict(__Pyx_FastcallDict_obj* iterable,
                                                                int is_dict, PyObject* method_name,
                                                   Py_ssize_t* p_orig_length, int* p_source_is_dict) {
    PyObject* obj = NULL;
    if (iterable->object == NULL) {
        obj = PyDict_New(); // empty tuple is likely to be a cheap iterator
        if (!obj) return NULL;
    } else if (iterable->args == NULL) {
        obj = iterable->object; // is a dict
        Py_INCREF(obj);
    } else {
        const char *name;
        if (!method_name) name = "keys";
#if PY_MAJOR_VERSION >= 3
        else name = PyUnicode_AsUTF8(method_name);
#else
        else name = PyString_AsString(method_name);
#endif

        if (strncmp(name, "iter", 4)==0) name = name + 4;

        if (strcmp(name, "items") == 0) {
            obj = __Pyx_FastcallDict_Items(iterable);
        } else if (strcmp(name, "keys") == 0) {
            obj = __Pyx_FastcallDict_Keys(iterable);
        } else if (strcmp(name, "values") == 0) {
            obj = __Pyx_FastcallDict_Values(iterable);
        } else {
            obj = NULL; // should never happen
        }
        method_name = NULL; // so __Pyx_dict_iterator doesn't try to use it on these objects
    }
    PyObject* result = __Pyx_dict_iterator(obj, is_dict, method_name, p_orig_length, p_source_is_dict);
    Py_DECREF(obj);
    return result;
}

/////////////////// fastcall_dict_getitem.proto ///////////////////////

static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_GetItem(__Pyx_FastcallDict_obj* o, PyObject* key);

/////////////////// fastcall_dict_getitem //////////////////////////////
//@requires:ObjectHandling.c::DictGetItem
//@requires:fastcall_dict_contains

static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_GetItem(__Pyx_FastcallDict_obj* o, PyObject* key) {
    if (o->object == NULL) {
        // not found
    } else if (o->args) {
        Py_ssize_t idx = __Pyx_FastcallDict_Index_impl(o, key);
        if (idx>=0) {
            Py_INCREF(o->args[idx]);
            return o->args[idx];
        }
    } else {
        return __Pyx_PyDict_GetItem(o->object, key);
    }
    if (unlikely(PyErr_Occurred())) PyErr_Clear(); // set our own exception
    PyErr_SetObject(PyExc_KeyError, key);
    return NULL;
}

/////////////////// fastcall_dict_contains.proto //////////////////////

static CYTHON_UNUSED int __Pyx_FastcallDict_Index_impl(__Pyx_FastcallDict_obj* o, PyObject* key);
static CYTHON_UNUSED int __Pyx_FastcallDict_Contains(__Pyx_FastcallDict_obj* o, PyObject* key);
static CYTHON_INLINE int __Pyx_FastcallDict_ContainsTF(PyObject* item, __Pyx_FastcallDict_obj* dict, int eq);

/////////////////// fastcall_dict_contains //////////////////////

static CYTHON_UNUSED int __Pyx_FastcallDict_Index_impl(__Pyx_FastcallDict_obj* o, PyObject* key) {
// returns -1 if not found otherwise the index
// only to be used when we know o->object is a tuple
#if (PY_MAJOR_VERSION >= 3)
    const int is_unicode = PyUnicode_Check(key);
#endif
    Py_ssize_t idx;
    const Py_ssize_t len =  PyTuple_GET_SIZE(o->object);
    for (idx = 0; idx < len; ++idx) {
        PyObject* lhs = PyTuple_GET_ITEM(o->object, idx);
#if (PY_MAJOR_VERSION >= 3)
        if (lhs == key) return idx;
        if (likely((is_unicode) && PyUnicode_Check(lhs))) {
            int cmp = PyUnicode_Compare(lhs, key);
            if (cmp == 0) {
                return idx;
            } else if ((cmp < 0) && unlikely(PyErr_Occurred())) {
                return -1;
            } else {
                continue; // FIXME? may fail with odd types that define an __eq__ function
                    // but these should be in function arguments anyway...
            }
        }
#endif
        if (PyObject_RichCompareBool(lhs, key, Py_EQ)) return idx;
    }
    return -1;
}

static CYTHON_UNUSED int __Pyx_FastcallDict_Contains(__Pyx_FastcallDict_obj* o, PyObject* key) {
    if (o->object == NULL) {
        return 0;
    } else if (o->args) {
        //return PySequence_Contains(o->object, key);
        int res = __Pyx_FastcallDict_Index_impl(o, key);
        if (res == -1) {
            return (unlikely(PyErr_Occurred())) ? -1 : 0;
        } else {
            return 1;
        }
    } else {
        return PyDict_Contains(o->object, key);
    }
}

static CYTHON_INLINE int __Pyx_FastcallDict_ContainsTF(PyObject* item, __Pyx_FastcallDict_obj* dict, int eq) {
    int result = __Pyx_FastcallDict_Contains(dict, item);
    return unlikely(result < 0) ? result : (result == (eq == Py_EQ));
}

/////////////////// fastcall_tuple_contains.proto //////////////////////

static CYTHON_UNUSED int __Pyx_FastcallTuple_Contains(__Pyx_FastcallTuple_obj o, PyObject* key);
static CYTHON_INLINE int __Pyx_FastcallTuple_ContainsTF(PyObject* item, __Pyx_FastcallTuple_obj t, int eq);

/////////////////// fastcall_tuple_contains //////////////////////

static CYTHON_UNUSED int __Pyx_FastcallTuple_Contains(__Pyx_FastcallTuple_obj o, PyObject* key) {
    Py_ssize_t idx;
    for (idx = 0; idx < o.nargs; ++idx) {
        PyObject* val = o.args[idx];
        return PyObject_RichCompareBool(val, key, Py_EQ);
    }
    return 0;
}

static CYTHON_INLINE int __Pyx_FastcallTuple_ContainsTF(PyObject* item, __Pyx_FastcallTuple_obj t, int eq) {
    int result = __Pyx_FastcallTuple_Contains(t, item);
    return unlikely(result < 0) ? result : (result == (eq == Py_EQ));
}

/////////////// ParseKeywords_fastcallstruct.proto ///////////////
//@requires: fastcall_dict

static CYTHON_UNUSED int __Pyx_ParseOptionalKeywords_fastcallstruct(PyObject *kwds, PyObject *const *kwvalues,
    PyObject **argnames[],
    __Pyx_FastcallDict_obj *kwds2, PyObject *values[], Py_ssize_t num_pos_args,
    const char* function_name); /*proto*/
static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_KwargsAsDict_FASTCALL_fastcallstruct(
    PyObject *kwds,
    PyObject *const * kwvalues);
static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_KwargsAsDict_VARARGS_fastcallstruct(
    PyObject *kwds,
    PyObject *const * kwvalues);

/////////////// ParseKeywords_fastcallstruct ///////////////
//@requires: ParseKeywords

static CYTHON_UNUSED int __Pyx_ParseOptionalKeywords_fastcallstruct(PyObject *kwds, PyObject *const *kwvalues,
    PyObject **argnames[],
    __Pyx_FastcallDict_obj *kwds2, PyObject *values[], Py_ssize_t num_pos_args,
    const char* function_name) {
    PyObject*** first_kw_arg = argnames + num_pos_args;
    PyObject* key = NULL;

    int kwds_is_tuple = CYTHON_METH_FASTCALL && likely(PyTuple_Check(kwds));
    if (!kwds_is_tuple) goto make_dict_instead;

    {
        // cycle through kwds
        Py_ssize_t pos;
        const Py_ssize_t len_kwds = PyTuple_GET_SIZE(kwds);
        PyObject *value, ***name;
        Py_ssize_t first_unassigned_index = 0;
        Py_ssize_t last_unassigned_index = 0;
        Py_ssize_t last_assigned_index = 0;
        for (pos = 0; pos < len_kwds; ++pos) {
            key = PyTuple_GET_ITEM(kwds, pos);
            value = kwvalues[pos];

            name = argnames;
            while (*name && (**name != key)) name++;
            if (*name) {
                if (name < first_kw_arg) {
                    // already assigned - set error
                    goto arg_passed_twice;
                } else {
                    if (first_unassigned_index == pos) {
                        first_unassigned_index = pos + 1;
                    } //else if (last_assigned_index < (pos-1)) {
                        // non-contiguous array
                    //  goto make_dict_instead;
                    //}
                    last_assigned_index = pos;

                    values[name-argnames] = value;
                    continue; // the for loop
                }
            }
            if (unlikely(!PyUnicode_Check(key))) {
                goto invalid_keyword_type;
            }

            name = argnames;
            while (*name) {
                // don't both with string comparison from the other function - this one only happens in Py3
                int cmp = (PyUnicode_GET_SIZE(**name) != PyUnicode_GET_SIZE(key)) ? 1 :
                        PyUnicode_Compare(**name, key);
                if (cmp < 0 && unlikely(PyErr_Occurred())) goto bad;
                if (cmp == 0) {
                    if (name < first_kw_arg) {
                        goto arg_passed_twice;
                    } else {
                        if (first_unassigned_index == pos) {
                            first_unassigned_index = pos + 1;
                        } else if (last_assigned_index < (pos-1)) {
                            // non-contiguous array
                            goto make_dict_instead;
                        }
                        last_assigned_index = pos;
                        values[name-argnames] = value;
                        goto continue_for_loop;
                    }
                }
                ++name;
            }
            // here we didn't find a name to match this key to
            last_unassigned_index = pos;

            if ((first_unassigned_index < last_assigned_index) &&
                (last_assigned_index < last_unassigned_index)) {
                // non continuous block of keyword values
                goto make_dict_instead;
            }

            continue_for_loop:
            ;
        }

        kwds2->object = PyTuple_GetSlice(kwds, first_unassigned_index, last_unassigned_index+1);
        kwds2->args = kwvalues + first_unassigned_index;
        return 0;
    }

    make_dict_instead:
        // we don't know how to process the keywords so just do the default "dict" version
        // of the structure
        kwds2->object = PyDict_New();
        if (!kwds2->object) return -1;
        {
            int result = __Pyx_ParseOptionalKeywords(kwds, kwvalues, argnames,
                                           kwds2->object, values, num_pos_args, function_name);
            if (result) {
                Py_CLEAR(kwds2->object);
            }
            return result;
        }
    arg_passed_twice:
        __Pyx_RaiseDoubleKeywordsError(function_name, key);
        goto bad;
    invalid_keyword_type:
        PyErr_Format(PyExc_TypeError,
            "%.200s() keywords must be strings", function_name);
        goto bad;
    bad:
        return -1;
}

static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_KwargsAsDict_FASTCALL_fastcallstruct(
    PyObject *kwds,
    PyObject *const * kwvalues) {
    __Pyx_FastcallDict_obj out = {};
#if CYTHON_METH_FASTCALL
    out.args = kwvalues;
    Py_INCREF(kwds);
#else
    kwds = __Pyx_KwargsAsDict_FASTCALL(kwds, kwvalues);  // default to this (dict copy)
#endif
    out.object = kwds;
    return out;
}

static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_KwargsAsDict_VARARGS_fastcallstruct(
    PyObject *kwds,
    PyObject *const * kwvalues) {
    __Pyx_FastcallDict_obj out = {};
    kwds = __Pyx_KwargsAsDict_VARARGS(kwds, kwvalues);
    out.object = kwds;
    return out;
}
