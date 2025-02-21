//////////////////// ArgTypeTest.proto ////////////////////


// Exact is 0 (False), 1 (True) or 2 (True and from annotation)
// The latter gives a small amount of extra error diagnostics
#define __Pyx_ArgTypeTest(obj, type, none_allowed, name, exact) \
    ((likely(__Pyx_IS_TYPE(obj, type) | (none_allowed && (obj == Py_None)))) ? 1 : \
        __Pyx__ArgTypeTest(obj, type, name, exact))

static int __Pyx__ArgTypeTest(PyObject *obj, PyTypeObject *type, const char *name, int exact); /*proto*/

//////////////////// ArgTypeTest ////////////////////

static int __Pyx__ArgTypeTest(PyObject *obj, PyTypeObject *type, const char *name, int exact)
{
    __Pyx_TypeName type_name;
    __Pyx_TypeName obj_type_name;
    PyObject *extra_info = EMPTY(unicode);
    int from_annotation_subclass = 0;
    if (unlikely(!type)) {
        PyErr_SetString(PyExc_SystemError, "Missing type object");
        return 0;
    }
    else if (!exact) {
        if (likely(__Pyx_TypeCheck(obj, type))) return 1;
    } else if (exact == 2) {
        // type from annotation
        if (__Pyx_TypeCheck(obj, type)) {
            from_annotation_subclass = 1;
            extra_info = PYUNICODE("Note that Cython is deliberately stricter than PEP-484 and rejects subclasses of builtin types. If you need to pass subclasses then set the 'annotation_typing' directive to False.");
        }
    }
    type_name = __Pyx_PyType_GetFullyQualifiedName(type);
    obj_type_name = __Pyx_PyType_GetFullyQualifiedName(Py_TYPE(obj));
    PyErr_Format(PyExc_TypeError,
        "Argument '%.200s' has incorrect type (expected " __Pyx_FMT_TYPENAME
        ", got " __Pyx_FMT_TYPENAME ")"
#if __PYX_LIMITED_VERSION_HEX < 0x030C0000
        "%s%U"
#endif
        , name, type_name, obj_type_name
#if __PYX_LIMITED_VERSION_HEX < 0x030C0000
        , (from_annotation_subclass ? ". " : ""), extra_info
#endif
        );
#if __PYX_LIMITED_VERSION_HEX >= 0x030C0000
    // Set the extra_info as a note instead. In principle it'd be possible to do this
    // from Python 3.11 up, but PyErr_GetRaisedException makes it much easier so do it
    // from Python 3.12 instead.
    if (exact == 2 && from_annotation_subclass) {
        PyObject *res;
        PyObject *vargs[2];
        vargs[0] = PyErr_GetRaisedException();
        vargs[1] = extra_info;
        res = PyObject_VectorcallMethod(PYUNICODE("add_note"), vargs, 2, NULL);
        Py_XDECREF(res);
        PyErr_SetRaisedException(vargs[0]);
    }
#endif
    __Pyx_DECREF_TypeName(type_name);
    __Pyx_DECREF_TypeName(obj_type_name);
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
        "%s() needs keyword-only argument %U", func_name, kw_name);
}


//////////////////// RaiseDoubleKeywords.proto ////////////////////

static void __Pyx_RaiseDoubleKeywordsError(const char* func_name, PyObject* kw_name); /*proto*/

//////////////////// RaiseDoubleKeywords ////////////////////

static void __Pyx_RaiseDoubleKeywordsError(
    const char* func_name,
    PyObject* kw_name)
{
    PyErr_Format(PyExc_TypeError,
        "%s() got multiple values for keyword argument '%U'", func_name, kw_name);
}


//////////////////// RaiseMappingExpected.proto ////////////////////

static void __Pyx_RaiseMappingExpectedError(PyObject* arg); /*proto*/

//////////////////// RaiseMappingExpected ////////////////////

static void __Pyx_RaiseMappingExpectedError(PyObject* arg) {
    __Pyx_TypeName arg_type_name = __Pyx_PyType_GetFullyQualifiedName(Py_TYPE(arg));
    PyErr_Format(PyExc_TypeError,
        "'" __Pyx_FMT_TYPENAME "' object is not a mapping", arg_type_name);
    __Pyx_DECREF_TypeName(arg_type_name);
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
        Py_ssize_t kwsize;
#if CYTHON_ASSUME_SAFE_SIZE
        kwsize = PyTuple_GET_SIZE(kw);
#else
        kwsize = PyTuple_Size(kw);
        if (kwsize < 0) return 0;
#endif
        if (unlikely(kwsize == 0))
            return 1;
        if (!kw_allowed) {
#if CYTHON_ASSUME_SAFE_MACROS
            key = PyTuple_GET_ITEM(kw, 0);
#else
            key = PyTuple_GetItem(kw, pos);
            if (!key) return 0;
#endif
            goto invalid_keyword;
        }
#if PY_VERSION_HEX < 0x03090000
        // On CPython >= 3.9, the FASTCALL protocol guarantees that keyword
        // names are strings (see https://bugs.python.org/issue37540)
        for (pos = 0; pos < kwsize; pos++) {
#if CYTHON_ASSUME_SAFE_MACROS
            key = PyTuple_GET_ITEM(kw, pos);
#else
            key = PyTuple_GetItem(kw, pos);
            if (!key) return 0;
#endif
            if (unlikely(!PyUnicode_Check(key)))
                goto invalid_keyword_type;
        }
#endif
        return 1;
    }

    while (PyDict_Next(kw, &pos, &key, 0)) {
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
    PyErr_Format(PyExc_TypeError,
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
    return 0;
}


//////////////////// ParseKeywords.proto ////////////////////

static int __Pyx_ParseOptionalKeywords(PyObject *kwds, PyObject *const *kwvalues,
    PyObject **argnames[],
    PyObject *kwds2, PyObject *values[], Py_ssize_t num_pos_args,
    const char* function_name,
    int ignore_unknown_kwargs
); /*proto*/

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

static int __Pyx_ParseOptionalKeywordDict(
    PyObject *kwds,
    PyObject **argnames[],
    PyObject *kwds2,
    PyObject *values[],
    Py_ssize_t num_pos_args,
    const char* function_name)
{
    // Validate and parse keyword arguments from kwds dict.
    PyObject *key;
    PyObject*** name;
    PyObject*** first_kw_arg = argnames + num_pos_args;

    // Check if dict is unicode-keys-only and let Python set the error otherwise.
    if (unlikely(!PyArg_ValidateKeywordArguments(kwds))) goto bad;

    // Fast copy of all kwargs.
    if (PyDict_Update(kwds2, kwds) < 0) goto bad;

    // Extract declared keyword arguments (if any).
    name = first_kw_arg;
    while (*name) {
        key = **name;
        PyObject *value;

#if !CYTHON_COMPILING_IN_LIMITED_API && (PY_VERSION_HEX >= 0x030d00A2 || defined(PyDict_Pop))
        int found = PyDict_Pop(kwds2, key, &value);
        if (unlikely(found < 0)) goto bad;
        if (found) {
            values[name-argnames] = value;
        }
#elif __PYX_LIMITED_VERSION_HEX >= 0x030d0000
        int found = PyDict_GetItemRef(kwds2, key, &value);
        if (unlikely(found < 0)) goto bad;
        if (found) {
            values[name-argnames] = value;
            if (unlikely(PyDict_DelItem(kwds2, key) < 0)) goto bad;
        }
#else
    // We use 'kdws2' as sentinel value to dict.pop() to avoid an exception on missing key.
    #if CYTHON_COMPILING_IN_CPYTHON
        value = _PyDict_Pop(kwds2, key, kwds2);
    #else
        value = CALL_UNBOUND_METHOD(PyDict_Type, "pop", kwds2, key, kwds2);
    #endif
        if (unlikely(!value)) goto bad;
        if (value == kwds2) {
            // Not found.
            Py_DECREF(value);
        } else {
            values[name-argnames] = value;
        }
#endif
        name++;
    }

    // If unmatched keywords remain, check for duplicates of positional arguments.
    if (PyDict_Size(kwds2) > 0) {
        name = argnames;
        while (*name && name != first_kw_arg) {
            int check;
            key = **name;
            check = PyDict_Contains(kwds, key);
            if (unlikely(check == -1)) goto bad;
            if (unlikely(check == 1)) goto arg_passed_twice;
            name++;
        }
    }

    return 0;

arg_passed_twice:
    __Pyx_RaiseDoubleKeywordsError(function_name, key);
    goto bad;
bad:
    return -1;
}

#if CYTHON_USE_UNICODE_INTERNALS
static CYTHON_INLINE int __Pyx_UnicodeKeywordsEqual(PyObject *s1, PyObject *s2) {
    int kind;
    Py_ssize_t len = PyUnicode_GET_LENGTH(s1);
    if (len != PyUnicode_GET_LENGTH(s2)) return 0;

    kind = PyUnicode_KIND(s1);
    if (kind != PyUnicode_KIND(s2)) return 0;

    const void *data1 = PyUnicode_DATA(s1);
    const void *data2 = PyUnicode_DATA(s2);
    return (memcmp(data1, data2, (size_t) len * kind) == 0);
}
#endif

static int __Pyx__ParseOptionalKeywords(
    PyObject *kwds,
    PyObject *const *kwvalues,
    PyObject **argnames[],
    PyObject *kwds2,
    PyObject *values[],
    Py_ssize_t num_pos_args,
    const char* function_name,
    int ignore_unknown_kwargs)
{
    PyObject *key = 0, *value = 0;
    Py_ssize_t pos = 0;
    PyObject*** name;
    PyObject*** first_kw_arg = argnames + num_pos_args;
    int kwds_is_tuple = CYTHON_METH_FASTCALL && likely(PyTuple_Check(kwds));

    while (1) {
        #if CYTHON_USE_UNICODE_INTERNALS
        Py_hash_t key_hash;
        #endif

        // clean up key and value when the loop is "continued"
        Py_XDECREF(key); key = NULL;
        Py_XDECREF(value); value = NULL;

        if (kwds_is_tuple) {
            Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_SIZE
            size = PyTuple_GET_SIZE(kwds);
#else
            size = PyTuple_Size(kwds);
            if (size < 0) goto bad;
#endif
            if (pos >= size) break;

#if CYTHON_AVOID_BORROWED_REFS
            // Get an owned reference to key.
            key = __Pyx_PySequence_ITEM(kwds, pos);
            if (!key) goto bad;
#elif CYTHON_ASSUME_SAFE_MACROS
            key = PyTuple_GET_ITEM(kwds, pos);
#else
            key = PyTuple_GetItem(kwds, pos);
            if (!key) goto bad;
#endif

            value = kwvalues[pos];
            pos++;
        }
        else
        {
            if (!PyDict_Next(kwds, &pos, &key, &value)) break;
            // It's unfortunately hard to avoid borrowed references (briefly) with PyDict_Next
#if CYTHON_AVOID_BORROWED_REFS
            // Own the reference to match the behaviour above.
            Py_INCREF(key);
#endif
        }

        // Quick pointer search for interned parameter matches.
        name = first_kw_arg;
        while (*name && (**name != key)) name++;
        if (*name) {
            values[name-argnames] = value;
#if CYTHON_AVOID_BORROWED_REFS
            Py_INCREF(value);  /* transfer ownership of value to values */
            Py_DECREF(key);
#endif
            key = NULL;
            value = NULL;
            continue;
        }

        // Now make sure we own both references since we're doing non-trivial Python operations.
#if !CYTHON_AVOID_BORROWED_REFS
        Py_INCREF(key);
#endif
        Py_INCREF(value);

        if (unlikely(!PyUnicode_Check(key))) goto invalid_keyword_type;

        #if CYTHON_USE_UNICODE_INTERNALS
        // The key hash is probably pre-calculated.
        key_hash = ((PyASCIIObject*)key)->hash;
        if (unlikely(key_hash == -1)) {
            key_hash = PyObject_Hash(key);
            if (unlikely(key_hash == -1))
                goto bad;
        }
        #endif

        // Compare strings for non-interned matches.
        name = first_kw_arg;
        while (*name) {
            PyObject *name_str = **name;
            #if CYTHON_USE_UNICODE_INTERNALS
            // Our argument hash is definitely pre-calculated.
            if (key_hash == ((PyASCIIObject*)name_str)->hash)
            #elif CYTHON_ASSUME_SAFE_SIZE
            if (PyUnicode_GET_LENGTH(name_str) == PyUnicode_GET_LENGTH(key))
            #endif
            {
                #if CYTHON_USE_UNICODE_INTERNALS
                if (__Pyx_UnicodeKeywordsEqual(name_str, key))
                #else
                int cmp = PyUnicode_Compare(name_str, key);
                if (cmp < 0 && unlikely(PyErr_Occurred())) goto bad;
                if (cmp == 0)
                #endif
                {
                    values[name-argnames] = value;
#if CYTHON_AVOID_BORROWED_REFS
                    value = NULL;  /* ownership transferred to values */
#endif
                    break;
                }
            }
            name++;
        }
        if (*name) continue;

        // Not found after positional args, check for (unlikely) duplicate positional argument.
        {
        #if CYTHON_USE_UNICODE_INTERNALS
            PyObject*** argname = argnames;
            int hash_matches_any = 0;
            while (argname != first_kw_arg) {
                hash_matches_any |= (key_hash == ((PyASCIIObject*)**argname)->hash);
                argname++;
            }
            if (hash_matches_any) {
                argname = argnames;
                while (argname != first_kw_arg) {
                    PyObject *name_str = **argname;
                    if (unlikely(key_hash == ((PyASCIIObject*)name_str)->hash) && unlikely(__Pyx_UnicodeKeywordsEqual(name_str, key))) goto arg_passed_twice;
                    argname++;
                }
            }
        #else
            PyObject*** argname = argnames;
            while (argname != first_kw_arg) {
                PyObject *name_str = **argname;
                if (unlikely(name_str == key)) goto arg_passed_twice;
                #if CYTHON_ASSUME_SAFE_SIZE
                if (PyUnicode_GET_LENGTH(name_str) == PyUnicode_GET_LENGTH(key))
                #endif
                {
                    int cmp = PyUnicode_Compare(name_str, key);
                    if (cmp < 0 && unlikely(PyErr_Occurred())) goto bad;
                    if (cmp == 0) goto arg_passed_twice;
                }
                argname++;
            }
        #endif
        }

        if (kwds2) {
            if (unlikely(PyDict_SetItem(kwds2, key, value))) goto bad;
        } else if (!ignore_unknown_kwargs) {
            goto invalid_keyword;
        }
    }
    Py_XDECREF(key);
    Py_XDECREF(value);
    return 0;

arg_passed_twice:
    __Pyx_RaiseDoubleKeywordsError(function_name, key);
    goto bad;
invalid_keyword_type:
    PyErr_Format(PyExc_TypeError,
        "%.200s() keywords must be strings", function_name);
    goto bad;
invalid_keyword:
    PyErr_Format(PyExc_TypeError,
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
bad:
    Py_XDECREF(key);
    Py_XDECREF(value);
    return -1;
}

static CYTHON_INLINE int __Pyx_ParseOptionalKeywords(
    PyObject *kwds,
    PyObject *const *kwvalues,
    PyObject **argnames[],
    PyObject *kwds2,
    PyObject *values[],
    Py_ssize_t num_pos_args,
    const char* function_name,
    int ignore_unknown_kwargs)
{
    int kwds_is_tuple = CYTHON_METH_FASTCALL && likely(PyTuple_Check(kwds));
    if (!kwds_is_tuple && kwds && kwds2) {
        // Special case: copy dict to dict.
        return __Pyx_ParseOptionalKeywordDict(kwds, argnames, kwds2, values, num_pos_args, function_name);
    } else {
        return __Pyx__ParseOptionalKeywords(kwds, kwvalues, argnames, kwds2, values, num_pos_args, function_name, ignore_unknown_kwargs);
    }
}


//////////////////// MergeKeywords.proto ////////////////////

static int __Pyx_MergeKeywords(PyObject *kwdict, PyObject *source_mapping); /*proto*/

//////////////////// MergeKeywords ////////////////////
//@requires: RaiseDoubleKeywords
//@requires: Optimize.c::dict_iter

static int __Pyx_MergeKeywords_dict(PyObject *kwdict, PyObject *source_dict) {
    int duplicates_found = 0;
    Py_ssize_t ppos = 0;
    PyObject *key, *smaller_dict, *larger_dict;

    if (PyDict_Size(kwdict) <= PyDict_Size(source_dict)) {
        smaller_dict = kwdict;
        larger_dict = source_dict;
    } else {
        smaller_dict = source_dict;
        larger_dict = kwdict;
    }

    __Pyx_BEGIN_CRITICAL_SECTION(smaller_dict);
    while (PyDict_Next(smaller_dict, &ppos, &key, NULL)) {
        #if CYTHON_AVOID_BORROWED_REFS || CYTHON_AVOID_THREAD_UNSAFE_BORROWED_REFS
        Py_INCREF(key);
        #endif
        if (unlikely(PyDict_Contains(larger_dict, key))) {
            __Pyx_RaiseDoubleKeywordsError("function", key);
            #if CYTHON_AVOID_BORROWED_REFS || CYTHON_AVOID_THREAD_UNSAFE_BORROWED_REFS
            Py_DECREF(key);
            #endif
            duplicates_found = 1;
            break;
        };
        #if CYTHON_AVOID_BORROWED_REFS || CYTHON_AVOID_THREAD_UNSAFE_BORROWED_REFS
        Py_DECREF(key);
        #endif
    }
    __Pyx_END_CRITICAL_SECTION();

    if (unlikely(duplicates_found))
        return -1;

    return PyDict_Update(kwdict, source_dict);
}

static int __Pyx_MergeKeywords_any(PyObject *kwdict, PyObject *source_mapping) {
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
                result = __Pyx_MergeKeywords_dict(kwdict, fallback);
                Py_DECREF(fallback);
                return result;
            }
        }
        if (unlikely(!iter)) goto bad;
    }

    while (1) {
        result = __Pyx_dict_iter_next(iter, orig_length, &ppos, &key, &value, NULL, source_is_dict);
        if (unlikely(result < 0)) goto bad;
        if (!result) break;

    #if PY_VERSION_HEX >= 0x030d0000 && !CYTHON_COMPILING_IN_LIMITED_API
        {
            int inserted = PyDict_SetDefaultRef(kwdict, key, value, NULL);
            if (unlikely(inserted != 0)) {
                if (inserted == 1) __Pyx_RaiseDoubleKeywordsError("function", key);
                result = -1;
            }
        }
    #else
        if (unlikely(PyDict_Contains(kwdict, key))) {
            __Pyx_RaiseDoubleKeywordsError("function", key);
            result = -1;
        } else {
            result = PyDict_SetItem(kwdict, key, value);
        }
    #endif

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

static CYTHON_INLINE int __Pyx_MergeKeywords(PyObject *kwdict, PyObject *source_mapping) {
    assert(PyDict_Check(kwdict));
    if (likely(PyDict_Check(source_mapping))) {
        return __Pyx_MergeKeywords_dict(kwdict, source_mapping);
    } else {
        return __Pyx_MergeKeywords_any(kwdict, source_mapping);
    }
}


/////////////// fastcall.proto ///////////////

// We define various functions and macros with two variants:
//..._FASTCALL and ..._VARARGS

// The first is used when METH_FASTCALL is enabled and the second is used
// otherwise. If the Python implementation does not support METH_FASTCALL
// (because it's an old version of CPython or it's not CPython at all),
// then the ..._FASTCALL macros simply alias ..._VARARGS

#if CYTHON_AVOID_BORROWED_REFS
    // This is the only case where we request an owned reference.
    #define __Pyx_Arg_VARARGS(args, i) PySequence_GetItem(args, i)
#elif CYTHON_ASSUME_SAFE_MACROS
    #define __Pyx_Arg_VARARGS(args, i) PyTuple_GET_ITEM(args, i)
#else
    #define __Pyx_Arg_VARARGS(args, i) PyTuple_GetItem(args, i)
#endif
#if CYTHON_AVOID_BORROWED_REFS
    #define __Pyx_Arg_NewRef_VARARGS(arg) __Pyx_NewRef(arg)
    #define __Pyx_Arg_XDECREF_VARARGS(arg) Py_XDECREF(arg)
#else
    #define __Pyx_Arg_NewRef_VARARGS(arg) arg  /* no-op */
    #define __Pyx_Arg_XDECREF_VARARGS(arg)     /* no-op - arg is borrowed */
#endif
#define __Pyx_NumKwargs_VARARGS(kwds) PyDict_Size(kwds)
#define __Pyx_KwValues_VARARGS(args, nargs) NULL
#define __Pyx_GetKwValue_VARARGS(kw, kwvalues, s) __Pyx_PyDict_GetItemStrWithError(kw, s)
#define __Pyx_KwargsAsDict_VARARGS(kw, kwvalues) PyDict_Copy(kw)
#if CYTHON_METH_FASTCALL
    #define __Pyx_Arg_FASTCALL(args, i) args[i]
    #define __Pyx_NumKwargs_FASTCALL(kwds) __Pyx_PyTuple_GET_SIZE(kwds)
    #define __Pyx_KwValues_FASTCALL(args, nargs) ((args) + (nargs))
    static CYTHON_INLINE PyObject * __Pyx_GetKwValue_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues, PyObject *s);
  #if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000 || CYTHON_COMPILING_IN_LIMITED_API
    CYTHON_UNUSED static PyObject *__Pyx_KwargsAsDict_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues);/*proto*/
  #else
    #define __Pyx_KwargsAsDict_FASTCALL(kw, kwvalues) _PyStack_AsDict(kwvalues, kw)
  #endif
    #define __Pyx_Arg_NewRef_FASTCALL(arg) arg  /* no-op, __Pyx_Arg_FASTCALL is direct and this needs
                                                   to have the same reference counting */
    #define __Pyx_Arg_XDECREF_FASTCALL(arg)     /* no-op - arg was returned from array */
#else
    #define __Pyx_Arg_FASTCALL __Pyx_Arg_VARARGS
    #define __Pyx_NumKwargs_FASTCALL __Pyx_NumKwargs_VARARGS
    #define __Pyx_KwValues_FASTCALL __Pyx_KwValues_VARARGS
    #define __Pyx_GetKwValue_FASTCALL __Pyx_GetKwValue_VARARGS
    #define __Pyx_KwargsAsDict_FASTCALL __Pyx_KwargsAsDict_VARARGS
    #define __Pyx_Arg_NewRef_FASTCALL(arg) __Pyx_Arg_NewRef_VARARGS(arg)
    #define __Pyx_Arg_XDECREF_FASTCALL(arg) __Pyx_Arg_XDECREF_VARARGS(arg)
#endif

#if CYTHON_COMPILING_IN_CPYTHON && CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
#define __Pyx_ArgsSlice_VARARGS(args, start, stop) __Pyx_PyTuple_FromArray(&__Pyx_Arg_VARARGS(args, start), stop - start)
#else
#define __Pyx_ArgsSlice_VARARGS(args, start, stop) PyTuple_GetSlice(args, start, stop)
#endif
#if CYTHON_METH_FASTCALL || (CYTHON_COMPILING_IN_CPYTHON && CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS)
#define __Pyx_ArgsSlice_FASTCALL(args, start, stop) __Pyx_PyTuple_FromArray(&__Pyx_Arg_FASTCALL(args, start), stop - start)
#else
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
    Py_ssize_t i, n = __Pyx_PyTuple_GET_SIZE(kwnames);
    #if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(n == -1)) return NULL;
    #endif
    for (i = 0; i < n; i++)
    {
        PyObject *namei = __Pyx_PyTuple_GET_ITEM(kwnames, i);
        #if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely(!namei)) return NULL;
        #endif
        if (s == namei) return kwvalues[i];
    }
    for (i = 0; i < n; i++)
    {
        PyObject *namei = __Pyx_PyTuple_GET_ITEM(kwnames, i);
        #if !CYTHON_ASSUME_SAFE_MACROS
        if (unlikely(!namei)) return NULL;
        #endif
        int eq = __Pyx_PyUnicode_Equals(s, namei, Py_EQ);
        if (unlikely(eq != 0)) {
            if (unlikely(eq < 0)) return NULL;  /* error */
            return kwvalues[i];
        }
    }
    return NULL;  /* not found (no exception set) */
}

#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000 || CYTHON_COMPILING_IN_LIMITED_API
CYTHON_UNUSED static PyObject *__Pyx_KwargsAsDict_FASTCALL(PyObject *kwnames, PyObject *const *kwvalues) {
    Py_ssize_t i, nkwargs;
    PyObject *dict;
#if !CYTHON_ASSUME_SAFE_SIZE
    nkwargs = PyTuple_Size(kwnames);
    if (unlikely(nkwargs < 0)) return NULL;
#else
    nkwargs = PyTuple_GET_SIZE(kwnames);
#endif

    dict = PyDict_New();
    if (unlikely(!dict))
        return NULL;

    for (i=0; i<nkwargs; i++) {
#if !CYTHON_ASSUME_SAFE_MACROS
        PyObject *key = PyTuple_GetItem(kwnames, i);
        if (!key) goto bad;
#else
        PyObject *key = PyTuple_GET_ITEM(kwnames, i);
#endif
        if (unlikely(PyDict_SetItem(dict, key, kwvalues[i]) < 0))
            goto bad;
    }
    return dict;

bad:
    Py_DECREF(dict);
    return NULL;
}
#endif

#endif
