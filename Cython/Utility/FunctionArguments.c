//////////////////// ArgTypeTest.proto ////////////////////


#define __Pyx_ArgTypeTest(obj, type, none_allowed, name, exact) \
    ((likely(__Pyx_IS_TYPE(obj, type) | (none_allowed && (obj == Py_None)))) ? 1 : \
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

static CYTHON_INLINE int __Pyx_ParseOptionalKeywords_Impl_Iter(PyObject* kwds, int kwds_is_tuple,
                                                          PyObject *const *kwvalues,
                                        Py_ssize_t *pos, PyObject **key, PyObject **value) {
    if (kwds_is_tuple) {
        if (*pos >= PyTuple_GET_SIZE(kwds)) return 0;
            *key = PyTuple_GET_ITEM(kwds, *pos);
            *value = kwvalues[*pos];
            (*pos)++;
    } else {
        if (!PyDict_Next(kwds, pos, key, value)) return 0;
    }
    return 1;
}

typedef int (*__Pyx_ParseOptionalKeywords_Impl_CmpFunc)(PyObject*, PyObject*);

static CYTHON_INLINE int __Pyx_ParseOptionalKeywords_Impl_BasicCheck(PyObject* rhs, PyObject* lhs) {
    return lhs != rhs;
}

static CYTHON_INLINE PyObject*** __Pyx_ParseOptionalKeywords_Impl_MatchName(PyObject* key,
                                            PyObject **name_start[], PyObject ***name_end,
                                            const char* function_name) {
    // note that an error can be set on return from this function

    PyObject ***name = name_start;
#if PY_MAJOR_VERSION < 3
    if (likely(PyString_Check(key))) {
        while ((*name) && (name != name_end)) {
            if ((CYTHON_COMPILING_IN_PYPY || PyString_GET_SIZE(**name) == PyString_GET_SIZE(key))
                        && _PyString_Eq(**name, key)) {
                return name;
            }
            ++name;
        }
    } else
#endif
    if (likely(PyUnicode_Check(key))) {
        while ((*name) && (name != name_end)) {
            int cmp = (
            #if !CYTHON_COMPILING_IN_PYPY && PY_MAJOR_VERSION >= 3
                (__Pyx_PyUnicode_GET_LENGTH(**name) != __Pyx_PyUnicode_GET_LENGTH(key)) ? 1 :
            #endif
                // In Py2, we may need to convert the argument name from str to unicode for comparison.
                PyUnicode_Compare(**name, key)
            );

            if (cmp < 0 && unlikely(PyErr_Occurred())) return NULL;
            if (cmp == 0) {
                return name;
            }
            ++name;
        }
    }
    else {
        PyErr_Format(PyExc_TypeError,
            "%.200s() keywords must be strings", function_name);
        return NULL;
    }
    return NULL;
}

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

    while (__Pyx_ParseOptionalKeywords_Impl_Iter(kwds, kwds_is_tuple, kwvalues, &pos, &key, &value)) {
        name = first_kw_arg;
        while (*name && (**name != key)) name++;
        if (*name) {
            values[name-argnames] = value;
            continue;
        }

        name = first_kw_arg;

        name = __Pyx_ParseOptionalKeywords_Impl_MatchName(key, first_kw_arg, NULL, function_name);
        if (!name && PyErr_Occurred()) goto bad;
        if (name) {
            values[name-argnames] = value;
            continue;
        } else {
            // not found after positional args, check for duplicate
            PyObject*** argname = __Pyx_ParseOptionalKeywords_Impl_MatchName(key, argnames, first_kw_arg,
                                                                                function_name);
            if (!argname && PyErr_Occurred()) goto bad;
            if (argname) {
                goto arg_passed_twice;
            }
        }

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
        if (unlikely(!PyErr_ExceptionMatches(PyExc_AttributeError))) goto bad;
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

/////////////// FastcallTuple.proto ///////////////
//@substitute: naming
// A struct which can be created cheaply without needing to construct a Python object

#if CYTHON_METH_FASTCALL
typedef struct {
    PyObject *const *args;
    Py_ssize_t nargs;
} __Pyx_FastcallTuple_obj;
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_New(PyObject *const *args, Py_ssize_t nargs);
// BorrowedEmpty useful when calling a function with only fastcall keyword arguments
#define __Pyx_FastcallTuple_BorrowedEmpty(args) __Pyx_FastcallTuple_New(args, 0)
#define __Pyx_FastcallTuple_Empty {}
// reference counting is all a no-op
#define __Pyx_FastcallTuple_GOTREF(x)
#define __Pyx_FastcallTuple_CLEAR(x, nanny)
#define __Pyx_FastcallTuple_XINCREF(x, nanny)
#define __Pyx_FastcallTuple_INCREF(x, nanny)
#define __Pyx_FastcallTuple_XDECREF(x, nanny)
#define __Pyx_FastcallTuple_DECREF_SET(lhs, rhs) do { lhs = rhs } while(0);
#define __Pyx_FastcallTuple_XDECREF_SET(lhs, rhs) do { lhs = rhs } while(0);
#define __Pyx_FastcallTuple_NULLCHECK(x) x.args
static CYTHON_INLINE Py_ssize_t __Pyx_FastcallTuple_Len(__Pyx_FastcallTuple_obj o); /* proto */
#else
typedef PyObject* __Pyx_FastcallTuple_obj;
#define __Pyx_FastcallTuple_Empty 0
#define __Pyx_FastcallTuple_New PyTuple_GetSlice
#define __Pyx_FastcallTuple_BorrowedEmpty(ignore) $empty_tuple
#define __Pyx_FastcallTuple_GOTREF(x) __Pyx_GOTREF(x)
#define __Pyx_FastcallTuple_CLEAR(x, nanny) if (nanny) { __Pyx_CLEAR(x); } else { Py_CLEAR(x); }
#define __Pyx_FastcallTuple_XINCREF(x, nanny)  if (nanny) { __Pyx_XINCREF(x); } else { Py_XINCREF(x); }
#define __Pyx_FastcallTuple_INCREF(x, nanny) if (nanny) { __Pyx_INCREF(x); } else { Py_INCREF(x); }
#define __Pyx_FastcallTuple_XDECREF(x, nanny) if (nanny) { __Pyx_XDECREF(x); } else { Py_XDECREF(x); }
#define __Pyx_FastcallTuple_DECREF_SET(lhs, rhs) __Pyx_DECREF_SET(lhs, rhs)
#define __Pyx_FastcallTuple_XDECREF_SET(lhs, rhs) __Pyx_XDECREF_SET(lhs, rhs)
#define __Pyx_FastcallTuple_NULLCHECK(x) x
#define __Pyx_FastcallTuple_Len PyTuple_GET_SIZE
#endif

static CYTHON_INLINE PyObject *__Pyx_FastcallTuple_ToTuple(__Pyx_FastcallTuple_obj o);  /* proto */

#if CYTHON_METH_FASTCALL
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_FASTCALL_struct(PyObject *const *args, Py_ssize_t start, Py_ssize_t stop);
#else
#define __Pyx_ArgsSlice_FASTCALL_struct(args, start, stop) __Pyx_ArgsSlice_VARARGS_struct(args, start, stop)
#endif
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_VARARGS_struct(PyObject *args, Py_ssize_t start, Py_ssize_t stop);

// no type-checking - used for conversion in function call
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_FromTuple(PyObject* o);

/////////////// FastcallTuple ///////////////
//@requires: ObjectHandling.c::TupleAndListFromArray

#if CYTHON_METH_FASTCALL
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_New(PyObject *const *args, Py_ssize_t nargs) {
    __Pyx_FastcallTuple_obj out = { args, nargs };
    return out;
}

static CYTHON_INLINE Py_ssize_t __Pyx_FastcallTuple_Len(__Pyx_FastcallTuple_obj o) {
    return __Pyx_PyVectorcall_NARGS(o.nargs);
}
#endif

static CYTHON_INLINE PyObject *__Pyx_FastcallTuple_ToTuple(__Pyx_FastcallTuple_obj o) {
#if CYTHON_METH_FASTCALL
    return __Pyx_PyTuple_FromArray(o.args, __Pyx_FastcallTuple_Len(o));
#else
    Py_INCREF(o);
    return o;
#endif
}

#if CYTHON_METH_FASTCALL
static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_FASTCALL_struct(PyObject *const *args, Py_ssize_t start, Py_ssize_t stop) {
    Py_ssize_t nargs = (stop - start);
    if (stop < start) nargs = 0;
#if CYTHON_VECTORCALL
    if (start > 0) {
        nargs |= PY_VECTORCALL_ARGUMENTS_OFFSET; // we know there's at least one space in front
    }
#endif
    return __Pyx_FastcallTuple_New(args+start, nargs);
}
#endif // CYTHON_METH_FASTCALL

static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_ArgsSlice_VARARGS_struct(PyObject *args, Py_ssize_t start, Py_ssize_t stop) {
#if CYTHON_METH_FASTCALL
    __Pyx_FastcallTuple_obj out = __Pyx_FastcallTuple_FromTuple(args);
    out.args += start;
    out.nargs = stop-start;
    return out;
#else
    return PyTuple_GetSlice(args, start, stop);
#endif
}

static CYTHON_INLINE __Pyx_FastcallTuple_obj __Pyx_FastcallTuple_FromTuple(PyObject* o) {
#if CYTHON_METH_FASTCALL
    return __Pyx_FastcallTuple_New(&PyTuple_GET_ITEM(o,0), PyTuple_GET_SIZE(o));
#else
    Py_INCREF(o);
    return o;
#endif
}

/////////////////// FastcallDict.proto /////////////////////////

typedef struct {
    PyObject *const *args; // start of the keyword args values
    PyObject *object;      // either a dict, a tuple or NULL
} __Pyx_FastcallDict_obj;
// exists in one of three (ish) states:
// * args is NULL, "object" is NULL, meaning no keyword arguments
// * args is NULL, in which case "object" is actually a dict, and this just defers to the dict methods
// * args is non-null, object is a tuple
// * args is non-null, object is NULL - used to signify an invalid state (but only really checked on creation)
// Defaults to "object" being a dict unless one of the quicker options can be easily created

// just a constant pointer to use for the "args is non-null object NULL" invalid state case
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_ErrorArgs[0];

static CYTHON_UNUSED Py_ssize_t __Pyx_FastcallDict_Len(__Pyx_FastcallDict_obj *o); /* proto */
static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_FastcallDict_New(void); /* proto */

// reference counting - for these always use "X" functions since object==NULL is a valid state
// It's difficult to do refnanny sensibly on these at the moment since it's valid for
// x->object to be swapped out in the middle of a function if it's coerced to Python.
// Therefore, disable it (FIXME!?)
#define __Pyx_FastcallDict_GOTREF(x)
#define __Pyx_FastcallDict_CLEAR(x, nanny) do { Py_CLEAR(x->object); x->args = NULL; } while(0)
#define __Pyx_FastcallDict_XDECREF(x, nanny) Py_XDECREF(x->object)
#define __Pyx_FastcallDict_INCREF __Pyx_FastcallDict_XINCREF
#define __Pyx_FastcallDict_XINCREF(x, nanny) Py_XINCREF(x->object)
#define __Pyx_FastcallDict_DECREF_SET __Pyx_FastcallDict_XDECREF_SET
#define __Pyx_FastcallDict_XDECREF_SET(lhs, rhs) do { \
        __PyxFastcallDict_obj *temp = lhs; \
        lhs = rhs; \
        Py_XDECREF(temp->object); \
    } while(0)
#define __Pyx_FastcallDict_NULLCHECK(x) !(x->args!=NULL && x->object==NULL)

/////////////////// FastcallDict //////////////////////

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

/////////////////// FastcallDictConvert.proto //////////////////////

static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_ToDict(__Pyx_FastcallDict_obj *o); /* proto */
static CYTHON_UNUSED PyObject* __Pyx_FastcallDict_ToDict_Explicit(__Pyx_FastcallDict_obj *o); /* proto */

/////////////////// FastcallDictConvert //////////////////////
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

/////////////// ParseKeywords_fastcallstruct.proto ///////////////
//@requires: FastcallDict

static int __Pyx_ParseOptionalKeywords_fastcallstruct(PyObject *kwds, PyObject *const *kwvalues,
    PyObject **argnames[],
    __Pyx_FastcallDict_obj *kwds2, PyObject *values[], Py_ssize_t num_pos_args,
    const char* function_name); /*proto*/

/////////////// ParseKeywords_fastcallstruct ///////////////
//@requires: ParseKeywords

static int __Pyx_ParseOptionalKeywords_fastcallstruct(PyObject *kwds, PyObject *const *kwvalues,
    PyObject **argnames[],
    __Pyx_FastcallDict_obj *kwds2, PyObject *values[], Py_ssize_t num_pos_args,
    const char* function_name) {
    PyObject*** first_kw_arg = argnames + num_pos_args;
    PyObject* key = NULL;

    int kwds_is_tuple = CYTHON_METH_FASTCALL && likely(PyTuple_Check(kwds));
    if (!kwds_is_tuple) goto make_dict_instead;

    {
        // cycle through kwds
        Py_ssize_t iter_pos=0;
        PyObject *value;
        Py_ssize_t first_unassigned_index = 0;
        Py_ssize_t last_unassigned_index = 0;
        Py_ssize_t last_assigned_index = 0;
        while (__Pyx_ParseOptionalKeywords_Impl_Iter(kwds, 1, kwvalues, &iter_pos, &key, &value)) {
            Py_ssize_t pos = iter_pos-1;  // iterator function keeps pos 1 in advance
            PyObject ***name = argnames;
            while (*name && (**name != key)) name++;
            if (!*name) {
                // try to find it with a more thorough search
                name = __Pyx_ParseOptionalKeywords_Impl_MatchName(key, argnames, NULL,
                                                                  function_name);
                if (!name && PyErr_Occurred()) goto bad;
            }
            if (name && *name) {
                if (name < first_kw_arg) {
                    // already assigned - set error
                    goto arg_passed_twice;
                } else {
                    if (first_unassigned_index == pos) {
                        first_unassigned_index = pos + 1;
                    }
                    last_assigned_index = pos;

                    values[name-argnames] = value;
                    continue; // the while loop
                }
            }

            // here we didn't find a name to match this key to
            last_unassigned_index = pos;

            if ((first_unassigned_index < last_assigned_index) &&
                (last_assigned_index < last_unassigned_index)) {
                // non-continuous block of keyword values
                goto make_dict_instead;
            }
        }

        kwds2->object = PyTuple_GetSlice(kwds, first_unassigned_index, last_unassigned_index+1);
        kwds2->args = kwvalues + first_unassigned_index;
        return 0;
    }

    make_dict_instead:
        // we don't know how to process the keywords so just do the default "dict" version
        // of the structure
        kwds2->object = PyDict_New();
        kwds2->args = NULL;
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
    bad:
        return -1;
}

//////////////////// FastcallDict_KwargsAsDict.proto ////////////////////////
//@requires: FastcallDict

static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_KwargsAsDict_FASTCALL_fastcallstruct(
    PyObject *kwds,
    PyObject *const * kwvalues); /* proto */
static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_KwargsAsDict_VARARGS_fastcallstruct(
    PyObject *kwds,
    PyObject *const * kwvalues); /* proto */

//////////////////// FastcallDict_KwargsAsDict ////////////////////////
//@requires: fastcall

static CYTHON_UNUSED __Pyx_FastcallDict_obj __Pyx_KwargsAsDict_FASTCALL_fastcallstruct(
    PyObject *kwds,
    PyObject *const * kwvalues) {
    __Pyx_FastcallDict_obj out = {};
#if CYTHON_METH_FASTCALL
    out.args = kwvalues;
    Py_INCREF(kwds);
#else
    kwds = __Pyx_KwargsAsDict_FASTCALL(kwds, kwvalues);  // default to this (dict copy)
    if (!kwds) {
        out.args = __Pyx_FastcallDict_ErrorArgs; // invalid state as error flag
    }
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
