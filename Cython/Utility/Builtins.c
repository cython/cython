/*
 * Special implementations of built-in functions and methods.
 *
 * Optional optimisations for builtins are in Optimize.c.
 *
 * General object operations and protocols are in ObjectHandling.c.
 */

//////////////////// Globals.proto ////////////////////

static PyObject* __Pyx_Globals(void); /*proto*/

//////////////////// Globals ////////////////////
//@requires: ObjectHandling.c::GetAttr

// This is a stub implementation until we have something more complete.
// Currently, we only handle the most common case of a read-only dict
// of Python names.  Supporting cdef names in the module and write
// access requires a rewrite as a dedicated class.

static PyObject* __Pyx_Globals(void) {
    return __Pyx_NewRef(NAMED_CGLOBAL(moddict_cname));
}

//////////////////// PyExecGlobals.proto ////////////////////

static PyObject* __Pyx_PyExecGlobals(PyObject*);

//////////////////// PyExecGlobals ////////////////////
//@requires: PyExec

static PyObject* __Pyx_PyExecGlobals(PyObject* code) {
    return __Pyx_PyExec2(code, NAMED_CGLOBAL(moddict_cname));
}

//////////////////// PyExec.proto ////////////////////

static PyObject* __Pyx_PyExec3(PyObject*, PyObject*, PyObject*);
static CYTHON_INLINE PyObject* __Pyx_PyExec2(PyObject*, PyObject*);

//////////////////// PyExec ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyExec2(PyObject* o, PyObject* globals) {
    return __Pyx_PyExec3(o, globals, NULL);
}

static PyObject* __Pyx_PyExec3(PyObject* o, PyObject* globals, PyObject* locals) {
    PyObject* result;
#if !CYTHON_COMPILING_IN_LIMITED_API
    PyObject* s = 0;
    char *code = 0;
#endif

    if (!globals || globals == Py_None) {
        globals = NAMED_CGLOBAL(moddict_cname);
    }
#if !CYTHON_COMPILING_IN_LIMITED_API
    // In Limited API we just use exec builtin which already has this
    else if (unlikely(!PyDict_Check(globals))) {
        __Pyx_TypeName globals_type_name =
            __Pyx_PyType_GetName(Py_TYPE(globals));
        PyErr_Format(PyExc_TypeError,
                     "exec() arg 2 must be a dict, not " __Pyx_FMT_TYPENAME,
                     globals_type_name);
        __Pyx_DECREF_TypeName(globals_type_name);
        goto bad;
    }
#endif
    if (!locals || locals == Py_None) {
        locals = globals;
    }

#if !CYTHON_COMPILING_IN_LIMITED_API
    if (__Pyx_PyDict_GetItemStr(globals, PYIDENT("__builtins__")) == NULL) {
        if (unlikely(PyDict_SetItem(globals, PYIDENT("__builtins__"), PyEval_GetBuiltins()) < 0))
            goto bad;
    }

    if (PyCode_Check(o)) {
        if (unlikely(__Pyx_PyCode_HasFreeVars((PyCodeObject *)o))) {
            PyErr_SetString(PyExc_TypeError,
                "code object passed to exec() may not contain free variables");
            goto bad;
        }
        #if CYTHON_COMPILING_IN_PYPY && PYPY_VERSION_NUM < 0x07030400
        result = PyEval_EvalCode((PyCodeObject *)o, globals, locals);
        #else
        result = PyEval_EvalCode(o, globals, locals);
        #endif
    } else {
        PyCompilerFlags cf;
        cf.cf_flags = 0;
#if PY_VERSION_HEX >= 0x030800A3
        cf.cf_feature_version = PY_MINOR_VERSION;
#endif
        if (PyUnicode_Check(o)) {
            cf.cf_flags = PyCF_SOURCE_IS_UTF8;
            s = PyUnicode_AsUTF8String(o);
            if (unlikely(!s)) goto bad;
            o = s;
        } else if (unlikely(!PyBytes_Check(o))) {
            __Pyx_TypeName o_type_name = __Pyx_PyType_GetName(Py_TYPE(o));
            PyErr_Format(PyExc_TypeError,
                "exec: arg 1 must be string, bytes or code object, got " __Pyx_FMT_TYPENAME,
                o_type_name);
            __Pyx_DECREF_TypeName(o_type_name);
            goto bad;
        }
        code = PyBytes_AS_STRING(o);
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
#else // CYTHON_COMPILING_IN_LIMITED_API
    {
        // For the limited API we just defer to the actual builtin
        // (after setting up globals and locals) - there's too much we can't do otherwise
        PyObject *builtins, *exec;
        builtins = PyEval_GetBuiltins();
        if (!builtins) return NULL;
        exec = PyDict_GetItemString(builtins, "exec");
        if (!exec) return NULL;
        result = PyObject_CallFunctionObjArgs(exec, o, globals, locals, NULL);
        return result;
    }
#endif
}

//////////////////// GetAttr3.proto ////////////////////

static CYTHON_INLINE PyObject *__Pyx_GetAttr3(PyObject *, PyObject *, PyObject *); /*proto*/

//////////////////// GetAttr3 ////////////////////
//@requires: ObjectHandling.c::PyObjectGetAttrStr
//@requires: Exceptions.c::PyThreadStateGet
//@requires: Exceptions.c::PyErrFetchRestore
//@requires: Exceptions.c::PyErrExceptionMatches

#if __PYX_LIMITED_VERSION_HEX < 0x030d00A1
static PyObject *__Pyx_GetAttr3Default(PyObject *d) {
    __Pyx_PyThreadState_declare
    __Pyx_PyThreadState_assign
    if (unlikely(!__Pyx_PyErr_ExceptionMatches(PyExc_AttributeError)))
        return NULL;
    __Pyx_PyErr_Clear();
    Py_INCREF(d);
    return d;
}
#endif

static CYTHON_INLINE PyObject *__Pyx_GetAttr3(PyObject *o, PyObject *n, PyObject *d) {
    PyObject *r;
#if __PYX_LIMITED_VERSION_HEX >= 0x030d00A1
    int res = PyObject_GetOptionalAttr(o, n, &r);
    // On failure (res == -1), r is set to NULL.
    return (res != 0) ? r : __Pyx_NewRef(d);
#else
  #if CYTHON_USE_TYPE_SLOTS
    if (likely(PyUnicode_Check(n))) {
        r = __Pyx_PyObject_GetAttrStrNoError(o, n);
        if (unlikely(!r) && likely(!PyErr_Occurred())) {
            r = __Pyx_NewRef(d);
        }
        return r;
    }
  #endif
    r = PyObject_GetAttr(o, n);
    return (likely(r)) ? r : __Pyx_GetAttr3Default(d);
#endif
}

//////////////////// HasAttr.proto ////////////////////

#if __PYX_LIMITED_VERSION_HEX >= 0x030d00A1
#define __Pyx_HasAttr(o, n)  PyObject_HasAttrWithError(o, n)
#else
static CYTHON_INLINE int __Pyx_HasAttr(PyObject *, PyObject *); /*proto*/
#endif

//////////////////// HasAttr ////////////////////
//@requires: ObjectHandling.c::PyObjectGetAttrStrNoError

#if __PYX_LIMITED_VERSION_HEX < 0x030d00A1
static CYTHON_INLINE int __Pyx_HasAttr(PyObject *o, PyObject *n) {
    PyObject *r;
    if (unlikely(!PyUnicode_Check(n))) {
        PyErr_SetString(PyExc_TypeError,
                        "hasattr(): attribute name must be string");
        return -1;
    }
    r = __Pyx_PyObject_GetAttrStrNoError(o, n);
    if (!r) {
        return (unlikely(PyErr_Occurred())) ? -1 : 0;
    } else {
        Py_DECREF(r);
        return 1;
    }
}
#endif

//////////////////// Intern.proto ////////////////////

static PyObject* __Pyx_Intern(PyObject* s); /* proto */

//////////////////// Intern ////////////////////
//@requires: ObjectHandling.c::RaiseUnexpectedTypeError

static PyObject* __Pyx_Intern(PyObject* s) {
    if (unlikely(!PyUnicode_CheckExact(s))) {
        __Pyx_RaiseUnexpectedTypeError("str", s);
        return NULL;
    }
    Py_INCREF(s);
    PyUnicode_InternInPlace(&s);
    return s;
}

//////////////////// abs_longlong.proto ////////////////////

static CYTHON_INLINE PY_LONG_LONG __Pyx_abs_longlong(PY_LONG_LONG x) {
#if defined (__cplusplus) && __cplusplus >= 201103L
    return std::abs(x);
#elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    return llabs(x);
#elif defined (_MSC_VER)
    // abs() is defined for long, but 64-bits type on MSVC is long long.
    // Use MS-specific _abs64() instead, which returns the original (negative) value for abs(-MAX-1)
    return _abs64(x);
#elif defined (__GNUC__)
    // gcc or clang on 64 bit windows.
    return __builtin_llabs(x);
#else
    if (sizeof(PY_LONG_LONG) <= sizeof(Py_ssize_t))
        return __Pyx_sst_abs(x);
    return (x<0) ? -x : x;
#endif
}


//////////////////// py_abs.proto ////////////////////

#if CYTHON_USE_PYLONG_INTERNALS
static PyObject *__Pyx_PyLong_AbsNeg(PyObject *num);/*proto*/

#define __Pyx_PyNumber_Absolute(x) \
    ((likely(PyLong_CheckExact(x))) ? \
         (likely(__Pyx_PyLong_IsNonNeg(x)) ? (Py_INCREF(x), (x)) : __Pyx_PyLong_AbsNeg(x)) : \
         PyNumber_Absolute(x))

#else
#define __Pyx_PyNumber_Absolute(x)  PyNumber_Absolute(x)
#endif

//////////////////// py_abs ////////////////////

#if CYTHON_USE_PYLONG_INTERNALS
static PyObject *__Pyx_PyLong_AbsNeg(PyObject *n) {
#if PY_VERSION_HEX >= 0x030C00A7
    if (likely(__Pyx_PyLong_IsCompact(n))) {
        return PyLong_FromSize_t(__Pyx_PyLong_CompactValueUnsigned(n));
    }
#else
    if (likely(Py_SIZE(n) == -1)) {
        // digits are unsigned
        return PyLong_FromUnsignedLong(__Pyx_PyLong_Digits(n)[0]);
    }
#endif
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030d0000
    {
        PyObject *copy = _PyLong_Copy((PyLongObject*)n);
        if (likely(copy)) {
            #if PY_VERSION_HEX >= 0x030C00A7
            // clear the sign bits to set the sign from SIGN_NEGATIVE (2) to positive (0)
            ((PyLongObject*)copy)->long_value.lv_tag = ((PyLongObject*)copy)->long_value.lv_tag & ~_PyLong_SIGN_MASK;
            #else
            // negate the size to swap the sign
            __Pyx_SET_SIZE(copy, -Py_SIZE(copy));
            #endif
        }
        return copy;
    }
#else
    return PyNumber_Negative(n);
#endif
}
#endif


//////////////////// pow2.proto ////////////////////

#define __Pyx_PyNumber_Power2(a, b) PyNumber_Power(a, b, Py_None)


//////////////////// divmod_int.proto //////////////////

static CYTHON_INLINE PyObject* __Pyx_divmod_int(int a, int b); /*proto*/


//////////////////// divmod_int //////////////////

static CYTHON_INLINE PyObject* __Pyx_divmod_int(int a, int b) {
    PyObject *result_tuple = NULL, *pyvalue = NULL;
    // Python and C/C++ use different algorithms in calculating quotients and remainders.
    // This results in different answers between Python and C/C++
    // when the dividend is negative and the divisor is positive and vice versa.
    int q, r;
    if ((a < 0 && b > 0) || (a > 0 && b < 0)) {
        // see CMath.c :: DivInt and ModInt utility code
        q = a / b;
        r = a - q * b;
        q -= ((r != 0) & ((r ^ b) < 0));
        r += ((r != 0) & ((r ^ b) < 0)) * b;
    }
    else if (b == 0) {
        PyErr_SetString(PyExc_ZeroDivisionError, "integer division or modulo by zero");
        return NULL;
    }
    else {
        div_t res = div(a, b);
        q = res.quot;
        r = res.rem;
    }
    result_tuple = PyTuple_New(2);
    if (unlikely(!result_tuple)) return NULL;
    pyvalue = PyLong_FromLong(q);
    if (unlikely(!pyvalue)) goto bad;
    if (__Pyx_PyTuple_SET_ITEM(result_tuple, 0, pyvalue) != (0)) goto bad;
    pyvalue = PyLong_FromLong(r);
    if (unlikely(!pyvalue)) goto bad;
    if (__Pyx_PyTuple_SET_ITEM(result_tuple, 1, pyvalue) != (0)) goto bad;
    return result_tuple;

bad:
    Py_DECREF(result_tuple);
    return NULL;
}


//////////////////// int_pyucs4.proto ////////////////////

static CYTHON_INLINE int __Pyx_int_from_UCS4(Py_UCS4 uchar);

//////////////////// int_pyucs4 ////////////////////

static int __Pyx_int_from_UCS4(Py_UCS4 uchar) {
    int digit = Py_UNICODE_TODIGIT(uchar);
    if (unlikely(digit < 0)) {
        PyErr_Format(PyExc_ValueError,
            "invalid literal for int() with base 10: '%c'",
            (int) uchar);
        return -1;
    }
    return digit;
}


//////////////////// float_pyucs4.proto ////////////////////

static CYTHON_INLINE double __Pyx_double_from_UCS4(Py_UCS4 uchar);

//////////////////// float_pyucs4 ////////////////////

static double __Pyx_double_from_UCS4(Py_UCS4 uchar) {
    double digit = Py_UNICODE_TONUMERIC(uchar);
    if (unlikely(digit < 0.0)) {
        PyErr_Format(PyExc_ValueError,
            "could not convert string to float: '%c'",
            (int) uchar);
        return -1.0;
    }
    return digit;
}


//////////////////// object_ord.proto ////////////////////
//@requires: TypeConversion.c::UnicodeAsUCS4

#define __Pyx_PyObject_Ord(c) \
    (likely(PyUnicode_Check(c)) ? (long)__Pyx_PyUnicode_AsPy_UCS4(c) : __Pyx__PyObject_Ord(c))
static long __Pyx__PyObject_Ord(PyObject* c); /*proto*/

//////////////////// object_ord ////////////////////

static long __Pyx__PyObject_Ord(PyObject* c) {
    Py_ssize_t size;
    if (PyBytes_Check(c)) {
        size = __Pyx_PyBytes_GET_SIZE(c);
        if (likely(size == 1)) {
#if CYTHON_ASSUME_SAFE_MACROS
            return (unsigned char) PyBytes_AS_STRING(c)[0];
#else
            char *data = PyBytes_AsString(c);
            if (unlikely(!data)) return -1;
            return (unsigned char) data[0];
#endif
        }
#if !CYTHON_ASSUME_SAFE_SIZE
        else if (unlikely(size < 0)) return -1;
#endif
    } else if (PyByteArray_Check(c)) {
        size = __Pyx_PyByteArray_GET_SIZE(c);
        if (likely(size == 1)) {
#if CYTHON_ASSUME_SAFE_MACROS
            return (unsigned char) PyByteArray_AS_STRING(c)[0];
#else
            char *data = PyByteArray_AsString(c);
            if (unlikely(!data)) return -1;
            return (unsigned char) data[0];
#endif
        }
#if !CYTHON_ASSUME_SAFE_SIZE
        else if (unlikely(size < 0)) return -1;
#endif
    } else {
        // FIXME: support character buffers - but CPython doesn't support them either
        __Pyx_TypeName c_type_name = __Pyx_PyType_GetName(Py_TYPE(c));
        PyErr_Format(PyExc_TypeError,
            "ord() expected string of length 1, but " __Pyx_FMT_TYPENAME " found",
            c_type_name);
        __Pyx_DECREF_TypeName(c_type_name);
        return (long)(Py_UCS4)-1;
    }
    PyErr_Format(PyExc_TypeError,
        "ord() expected a character, but string of length %zd found", size);
    return (long)(Py_UCS4)-1;
}


//////////////////// py_dict_keys.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_Keys(PyObject* d); /*proto*/

//////////////////// py_dict_keys ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_Keys(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "keys", d);
}

//////////////////// py_dict_values.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_Values(PyObject* d); /*proto*/

//////////////////// py_dict_values ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_Values(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "values", d);
}

//////////////////// py_dict_items.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_Items(PyObject* d); /*proto*/

//////////////////// py_dict_items ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_Items(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "items", d);
}

//////////////////// py_dict_iterkeys.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterKeys(PyObject* d); /*proto*/

//////////////////// py_dict_iterkeys ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterKeys(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "keys", d);
}

//////////////////// py_dict_itervalues.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterValues(PyObject* d); /*proto*/

//////////////////// py_dict_itervalues ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterValues(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "values", d);
}

//////////////////// py_dict_iteritems.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterItems(PyObject* d); /*proto*/

//////////////////// py_dict_iteritems ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_IterItems(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "items", d);
}

//////////////////// py_dict_viewkeys.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewKeys(PyObject* d); /*proto*/

//////////////////// py_dict_viewkeys ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewKeys(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "keys", d);
}

//////////////////// py_dict_viewvalues.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewValues(PyObject* d); /*proto*/

//////////////////// py_dict_viewvalues ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewValues(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "values", d);
}

//////////////////// py_dict_viewitems.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewItems(PyObject* d); /*proto*/

//////////////////// py_dict_viewitems ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_ViewItems(PyObject* d) {
    return CALL_UNBOUND_METHOD(PyDict_Type, "items", d);
}


//////////////////// pyfrozenset_new.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyFrozenSet_New(PyObject* it);

//////////////////// pyfrozenset_new ////////////////////
//@requires: ObjectHandling.c::PyObjectCallNoArg

static CYTHON_INLINE PyObject* __Pyx_PyFrozenSet_New(PyObject* it) {
    if (it) {
        PyObject* result;
#if CYTHON_COMPILING_IN_PYPY
        // PyPy currently lacks PyFrozenSet_CheckExact() and PyFrozenSet_New()
        PyObject* args;
        args = PyTuple_Pack(1, it);
        if (unlikely(!args))
            return NULL;
        result = PyObject_Call((PyObject*)&PyFrozenSet_Type, args, NULL);
        Py_DECREF(args);
        return result;
#else
        if (PyFrozenSet_CheckExact(it)) {
            Py_INCREF(it);
            return it;
        }
        result = PyFrozenSet_New(it);
        if (unlikely(!result))
            return NULL;
        if ((__PYX_LIMITED_VERSION_HEX >= 0x030A00A1)
#if CYTHON_COMPILING_IN_LIMITED_API
            || __Pyx_get_runtime_version() >= 0x030A00A1
#endif
            )
            return result;
        {
            Py_ssize_t size = __Pyx_PySet_GET_SIZE(result);
            if (likely(size > 0))
                return result;
#if !CYTHON_ASSUME_SAFE_SIZE
            if (unlikely(size < 0)) {
                Py_DECREF(result);
                return NULL;
            }
#endif
        }
        // empty frozenset is a singleton (on Python <3.10)
        // seems wasteful, but CPython does the same
        Py_DECREF(result);
#endif
    }
    return __Pyx_PyObject_CallNoArg((PyObject*) &PyFrozenSet_Type);
}


//////////////////// PySet_Update.proto ////////////////////

static CYTHON_INLINE int __Pyx_PySet_Update(PyObject* set, PyObject* it); /*proto*/

//////////////////// PySet_Update ////////////////////

static CYTHON_INLINE int __Pyx_PySet_Update(PyObject* set, PyObject* it) {
    PyObject *retval;
    #if CYTHON_USE_TYPE_SLOTS && !CYTHON_COMPILING_IN_PYPY
    if (PyAnySet_Check(it)) {
        Py_ssize_t size = __Pyx_PySet_GET_SIZE(it);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(size < 0)) return -1;
        #endif
        if (size == 0)
            return 0;
        // fast and safe case: CPython will update our result set and return it
        retval = PySet_Type.tp_as_number->nb_inplace_or(set, it);
        if (likely(retval == set)) {
            Py_DECREF(retval);
            return 0;
        }
        if (unlikely(!retval))
            return -1;
        // unusual result, fall through to set.update() call below
        Py_DECREF(retval);
    }
    #endif
    retval = CALL_UNBOUND_METHOD(PySet_Type, "update", set, it);
    if (unlikely(!retval)) return -1;
    Py_DECREF(retval);
    return 0;
}

///////////////// memoryview_get_from_buffer.proto ////////////////////

// buffer is in limited api from Py3.11
#if !CYTHON_COMPILING_IN_LIMITED_API || __PYX_LIMITED_VERSION_HEX >= 0x030b0000
#define __Pyx_PyMemoryView_Get_{{name}}(o) PyMemoryView_GET_BUFFER(o)->{{name}}
#else
{{py:
out_types = dict(
    ndim='int', readonly='int',
    len='Py_ssize_t', itemsize='Py_ssize_t')
}} // can't get format like this unfortunately. It's unicode via getattr
{{py: out_type = out_types[name]}}
static {{out_type}} __Pyx_PyMemoryView_Get_{{name}}(PyObject *obj); /* proto */
#endif

////////////// memoryview_get_from_buffer /////////////////////////

#if !CYTHON_COMPILING_IN_LIMITED_API || __PYX_LIMITED_VERSION_HEX >= 0x030b0000
#else
{{py:
out_types = dict(
    ndim='int', readonly='int',
    len='Py_ssize_t', itemsize='Py_ssize_t')
}}
{{py: out_type = out_types[name]}}
static {{out_type}} __Pyx_PyMemoryView_Get_{{name}}(PyObject *obj) {
    {{out_type}} result;
    PyObject *attr = PyObject_GetAttr(obj, PYIDENT("{{name}}"));
    if (!attr) {
        goto bad;
    }
{{if out_type == 'int'}}
    // I'm not worrying about overflow here because
    // ultimately it comes from a C struct that's an int
    result = PyLong_AsLong(attr);
{{elif out_type == 'Py_ssize_t'}}
    result = PyLong_AsSsize_t(attr);
{{endif}}
    Py_DECREF(attr);
    return result;

    bad:
    Py_XDECREF(attr);
    return -1;
}
#endif

//////////////////// PyInt_bit_count.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyInt_bit_count(PyObject *x); /*proto*/

//////////////////// PyInt_bit_count ////////////////////

static CYTHON_INLINE int __Pyx_PyInt_bit_count(PyObject *x) {
#ifdef __has_builtin
#if __has_builtin(__builtin_popcountll)
    long long result;
    int overflow;

    result = PyLong_AsLongLongAndOverflow(x, &overflow);
    if (overflow) {
        return (int)PyLong_AsLong(CALL_UNBOUND_METHOD(PyLong_Type, "bit_count", x));
    } else {
        unsigned long long value;

        if (result < 0) {
            value = -result;
        } else {
            value = result;
        }

        return __builtin_popcountll(value);
    };
#else
#define _FALLBACK
#endif
#else
#define _FALLBACK
#endif
#ifdef _FALLBACK
#undef _FALLBACK
    return (int)PyLong_AsLong(CALL_UNBOUND_METHOD(PyLong_Type, "bit_count", x));
#endif
}

//////////////////// bit_count_base ////////////////////


static inline int bit_count_base (unsigned long long x, int size) {
    if (size == 8) {
        uint8_t tmp = (uint8_t)x;
        tmp -= (tmp >> 1) & 0x55;
        tmp = (tmp & 0x33) + ((tmp >> 2) & 0x33);
        tmp = ((tmp + (tmp >> 4)) & 0x0F) * 0x01;

        return (unsigned long long)tmp;
    } else if (size == 16) {
        uint16_t tmp = (uint16_t)x;
        tmp -= (tmp >> 1) & 0x5555U;
        tmp = (tmp & 0x3333U) + ((tmp >> 2) & 0x3333U);
        tmp = (((tmp + (tmp >> 4)) & 0x0F0FU) * 0x0101U) >> 8;

        return (unsigned long long)tmp;
    } else if (size == 32) {
        uint32_t tmp = (uint32_t)x;
        tmp -= (tmp >> 1) & 0x55555555UL;
        tmp = (tmp & 0x33333333UL) + ((tmp >> 2) & 0x33333333UL);
        tmp = (((tmp + (tmp >> 4)) & 0x0F0F0F0FUL) * 0x01010101UL) >> 24;

        return (unsigned long long)tmp;
    } else if (size == 64) {
        uint64_t tmp = (uint64_t)x;
        tmp -= (tmp >> 1) & 0x55555555ULL;
        tmp = (tmp & 0x33333333ULL) + ((tmp >> 2) & 0x33333333ULL);
        tmp = (((tmp + (tmp >> 4)) & 0x0F0F0F0FULL) * 0x01010101ULL) >> 56;

        return (unsigned long long)tmp;
    } else if (size == 128) {
        uint128_t tmp = (uint128_t)x;
        tmp -= (tmp >> 1) & 0x55555555ULL;
        tmp = (tmp & 0x33333333ULL) + ((tmp >> 2) & 0x33333333ULL);
        tmp = (((tmp + (tmp >> 4)) & 0x0F0F0F0FULL) * 0x01010101ULL) >> 120;

        return (unsigned long long)tmp;
    }
}

//////////////////// unsigned_char_bit_count.proto ////////////////////

static CYTHON_INLINE unsigned char __Pyx_unsigned_char_bit_count(unsigned char x);

//////////////////// unsigned_char_bit_count ////////////////////
//@requires: bit_count_base

static CYTHON_INLINE unsigned char __Pyx_unsigned_char_bit_count(unsigned char x) {
#if defined(__has_builtin) && __has_builtin(__builtin_popcount)
    return (unsigned char)__builtin_popcount((unsigned int)x);
#else
    return (unsigned char)bit_count_base((unsigned long long)x, sizeof(unsigned char));
#endif
}

//////////////////// unsigned_short_bit_count.proto ////////////////////

static CYTHON_INLINE short __Pyx_unsigned_short_bit_count(unsigned short x);

//////////////////// unsigned_short_bit_count ////////////////////
//@requires: bit_count_base

static CYTHON_INLINE short __Pyx_unsigned_short_bit_count(unsigned short x) {
#if defined(__has_builtin) && __has_builtin(__builtin_popcount)
    return (short)__builtin_popcount((unsigned int)x);
#else
    return (short)bit_count_base((unsigned long long)x, sizeof(unsigned short));
#endif
}

//////////////////// unsigned_int_bit_count.proto ////////////////////

static CYTHON_INLINE int __Pyx_unsigned_int_bit_count(unsigned int x);

//////////////////// unsigned_int_bit_count ////////////////////
//@requires: bit_count_base

static CYTHON_INLINE int __Pyx_unsigned_int_bit_count(unsigned int x) {
#if defined(__has_builtin) && __has_builtin(__builtin_popcount)
    return __builtin_popcount(x);
#else
    return bit_count_base((unsigned long long)x, sizeof(unsigned int));
#endif
}

//////////////////// unsigned_long_bit_count.proto ////////////////////

static CYTHON_INLINE int __Pyx_unsigned_long_bit_count(unsigned long x);

//////////////////// unsigned_long_bit_count ////////////////////
//@requires: bit_count_base

static CYTHON_INLINE int __Pyx_unsigned_long_bit_count(unsigned long x) {
#if defined(__has_builtin) && __has_builtin(__builtin_popcountl)
    return __builtin_popcountl(x);
#else
    return bit_count_base((unsigned long long)x, sizeof(unsigned long));
#endif
}

/////////////////// unsigned_longlong_bit_count.proto ////////////////////

static CYTHON_INLINE int __Pyx_unsigned_longlong_bit_count(unsigned long long x);

//////////////////// unsigned_longlong_bit_count ////////////////////
//@requires: bit_count_base

static CYTHON_INLINE int __Pyx_unsigned_longlong_bit_count(unsigned long long x) {
#if defined(__has_builtin) && __has_builtin(__builtin_popcountll)
    return __builtin_popcountll(x);
#else
    return bit_count_base(x, sizeof(unsigned long long));
#endif
}

//////////////////// char_bit_count.proto ////////////////////

static CYTHON_INLINE unsigned char __Pyx_char_bit_count(char x);

//////////////////// char_bit_count ////////////////////
//@requires: unsigned_char_bit_count

static CYTHON_INLINE unsigned char __Pyx_char_bit_count(char x) {
    unsigned char value = (x < 0) ? -x : x;
    return __Pyx_unsigned_char_bit_count(value);
}

//////////////////// signed_char_bit_count.proto ////////////////////

static CYTHON_INLINE unsigned char __Pyx_signed_char_bit_count(signed char x);

//////////////////// signed_char_bit_count ////////////////////
//@requires: unsigned_char_bit_count

static CYTHON_INLINE unsigned char __Pyx_signed_char_bit_count(signed char x) {
    unsigned char value = (x < 0) ? -x : x;
    return __Pyx_unsigned_char_bit_count(value);
}

//////////////////// signed_short_bit_count.proto ////////////////////

static CYTHON_INLINE short __Pyx_signed_short_bit_count(signed short x);

//////////////////// signed_short_bit_count ////////////////////
//@requires: unsigned_short_bit_count

static CYTHON_INLINE short __Pyx_signed_short_bit_count(signed short x) {
    unsigned short value = (x < 0) ? -x : x;
    return __Pyx_unsigned_short_bit_count(value);
}

//////////////////// signed_int_bit_count.proto ////////////////////

static int __Pyx_signed_int_bit_count(signed int x);

//////////////////// signed_int_bit_count ////////////////////
//@requires: unsigned_int_bit_count

static int __Pyx_signed_int_bit_count(signed int x) {
    unsigned int value = (x < 0) ? -x : x;
    return __Pyx_unsigned_int_bit_count(value);
}

//////////////////// signed_long_bit_count.proto ////////////////////

static CYTHON_INLINE int __Pyx_signed_long_bit_count(signed long x);

//////////////////// signed_long_bit_count ////////////////////
//@requires: unsigned_long_bit_count

static CYTHON_INLINE int __Pyx_signed_long_bit_count(signed long x) {
    unsigned long value = (x < 0) ? -x : x;
    return __Pyx_unsigned_long_bit_count(value);
}

//////////////////// signed_longlong_bit_count.proto ////////////////////

static CYTHON_INLINE int __Pyx_signed_longlong_bit_count(signed long long x);

//////////////////// signed_longlong_bit_count ////////////////////
//@requires: unsigned_longlong_bit_count

static CYTHON_INLINE int __Pyx_signed_longlong_bit_count(signed long long x) {
    unsigned long long value = (x < 0) ? -x : x;
    return __Pyx_unsigned_longlong_bit_count(value);
}
