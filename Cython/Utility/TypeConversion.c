/////////////// TypeConversions.proto ///////////////

/* Type Conversion Predeclarations */

#define __Pyx_uchar_cast(c) ((unsigned char)c)
#define __Pyx_long_cast(x) ((long)x)

#define __Pyx_fits_Py_ssize_t(v, type, is_signed)  (    \
    (sizeof(type) < sizeof(Py_ssize_t))  ||             \
    (sizeof(type) > sizeof(Py_ssize_t) &&               \
          likely(v < (type)PY_SSIZE_T_MAX ||            \
                 v == (type)PY_SSIZE_T_MAX)  &&         \
          (!is_signed || likely(v > (type)PY_SSIZE_T_MIN ||       \
                                v == (type)PY_SSIZE_T_MIN)))  ||  \
    (sizeof(type) == sizeof(Py_ssize_t) &&              \
          (is_signed || likely(v < (type)PY_SSIZE_T_MAX ||        \
                               v == (type)PY_SSIZE_T_MAX)))  )

// fast and unsafe abs(Py_ssize_t) that ignores the overflow for (-PY_SSIZE_T_MAX-1)
#if defined (__cplusplus) && __cplusplus >= 201103L
    #include <cstdlib>
    #define __Pyx_sst_abs(value) std::abs(value)
#elif SIZEOF_INT >= SIZEOF_SIZE_T
    #define __Pyx_sst_abs(value) abs(value)
#elif SIZEOF_LONG >= SIZEOF_SIZE_T
    #define __Pyx_sst_abs(value) labs(value)
#elif defined (_MSC_VER) && defined (_M_X64)
    // abs() is defined for long, but 64-bits type on MSVC is long long.
    // Use MS-specific _abs64 instead.
    #define __Pyx_sst_abs(value) _abs64(value)
#elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define __Pyx_sst_abs(value) llabs(value)
#elif defined (__GNUC__)
    // gcc or clang on 64 bit windows.
    #define __Pyx_sst_abs(value) __builtin_llabs(value)
#else
    #define __Pyx_sst_abs(value) ((value<0) ? -value : value)
#endif

static CYTHON_INLINE char* __Pyx_PyObject_AsString(PyObject*);
static CYTHON_INLINE char* __Pyx_PyObject_AsStringAndSize(PyObject*, Py_ssize_t* length);

#define __Pyx_PyByteArray_FromString(s) PyByteArray_FromStringAndSize((const char*)s, strlen((const char*)s))
#define __Pyx_PyByteArray_FromStringAndSize(s, l) PyByteArray_FromStringAndSize((const char*)s, l)
#define __Pyx_PyBytes_FromString        PyBytes_FromString
#define __Pyx_PyBytes_FromStringAndSize PyBytes_FromStringAndSize
static CYTHON_INLINE PyObject* __Pyx_PyUnicode_FromString(const char*);

#if PY_MAJOR_VERSION < 3
    #define __Pyx_PyStr_FromString        __Pyx_PyBytes_FromString
    #define __Pyx_PyStr_FromStringAndSize __Pyx_PyBytes_FromStringAndSize
#else
    #define __Pyx_PyStr_FromString        __Pyx_PyUnicode_FromString
    #define __Pyx_PyStr_FromStringAndSize __Pyx_PyUnicode_FromStringAndSize
#endif

#define __Pyx_PyObject_AsSString(s)    ((signed char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_AsUString(s)    ((unsigned char*) __Pyx_PyObject_AsString(s))
#define __Pyx_PyObject_FromCString(s)  __Pyx_PyObject_FromString((const char*)s)
#define __Pyx_PyBytes_FromCString(s)   __Pyx_PyBytes_FromString((const char*)s)
#define __Pyx_PyByteArray_FromCString(s)   __Pyx_PyByteArray_FromString((const char*)s)
#define __Pyx_PyStr_FromCString(s)     __Pyx_PyStr_FromString((const char*)s)
#define __Pyx_PyUnicode_FromCString(s) __Pyx_PyUnicode_FromString((const char*)s)

#if PY_MAJOR_VERSION < 3
static CYTHON_INLINE size_t __Pyx_Py_UNICODE_strlen(const Py_UNICODE *u)
{
    const Py_UNICODE *u_end = u;
    while (*u_end++) ;
    return (size_t)(u_end - u - 1);
}
#else
#define __Pyx_Py_UNICODE_strlen Py_UNICODE_strlen
#endif

#define __Pyx_PyUnicode_FromUnicode(u)       PyUnicode_FromUnicode(u, __Pyx_Py_UNICODE_strlen(u))
#define __Pyx_PyUnicode_FromUnicodeAndLength PyUnicode_FromUnicode
#define __Pyx_PyUnicode_AsUnicode            PyUnicode_AsUnicode

#define __Pyx_NewRef(obj) (Py_INCREF(obj), obj)
#define __Pyx_Owned_Py_None(b) __Pyx_NewRef(Py_None)
#define __Pyx_PyBool_FromLong(b) ((b) ? __Pyx_NewRef(Py_True) : __Pyx_NewRef(Py_False))
static CYTHON_INLINE int __Pyx_PyObject_IsTrue(PyObject*);
static CYTHON_INLINE PyObject* __Pyx_PyNumber_Int(PyObject* x);

static CYTHON_INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject*);
static CYTHON_INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t);

#if CYTHON_COMPILING_IN_CPYTHON
#define __pyx_PyFloat_AsDouble(x) (PyFloat_CheckExact(x) ? PyFloat_AS_DOUBLE(x) : PyFloat_AsDouble(x))
#else
#define __pyx_PyFloat_AsDouble(x) PyFloat_AsDouble(x)
#endif
#define __pyx_PyFloat_AsFloat(x) ((float) __pyx_PyFloat_AsDouble(x))

#if PY_MAJOR_VERSION < 3 && __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
static int __Pyx_sys_getdefaultencoding_not_ascii;
static int __Pyx_init_sys_getdefaultencoding_params(void) {
    PyObject* sys;
    PyObject* default_encoding = NULL;
    PyObject* ascii_chars_u = NULL;
    PyObject* ascii_chars_b = NULL;
    const char* default_encoding_c;
    sys = PyImport_ImportModule("sys");
    if (!sys) goto bad;
    default_encoding = PyObject_CallMethod(sys, (char*) "getdefaultencoding", NULL);
    Py_DECREF(sys);
    if (!default_encoding) goto bad;
    default_encoding_c = PyBytes_AsString(default_encoding);
    if (!default_encoding_c) goto bad;
    if (strcmp(default_encoding_c, "ascii") == 0) {
        __Pyx_sys_getdefaultencoding_not_ascii = 0;
    } else {
        char ascii_chars[128];
        int c;
        for (c = 0; c < 128; c++) {
            ascii_chars[c] = c;
        }
        __Pyx_sys_getdefaultencoding_not_ascii = 1;
        ascii_chars_u = PyUnicode_DecodeASCII(ascii_chars, 128, NULL);
        if (!ascii_chars_u) goto bad;
        ascii_chars_b = PyUnicode_AsEncodedString(ascii_chars_u, default_encoding_c, NULL);
        if (!ascii_chars_b || !PyBytes_Check(ascii_chars_b) || memcmp(ascii_chars, PyBytes_AS_STRING(ascii_chars_b), 128) != 0) {
            PyErr_Format(
                PyExc_ValueError,
                "This module compiled with c_string_encoding=ascii, but default encoding '%.200s' is not a superset of ascii.",
                default_encoding_c);
            goto bad;
        }
        Py_DECREF(ascii_chars_u);
        Py_DECREF(ascii_chars_b);
    }
    Py_DECREF(default_encoding);
    return 0;
bad:
    Py_XDECREF(default_encoding);
    Py_XDECREF(ascii_chars_u);
    Py_XDECREF(ascii_chars_b);
    return -1;
}
#endif

#if __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT && PY_MAJOR_VERSION >= 3
#define __Pyx_PyUnicode_FromStringAndSize(c_str, size) PyUnicode_DecodeUTF8(c_str, size, NULL)
#else
#define __Pyx_PyUnicode_FromStringAndSize(c_str, size) PyUnicode_Decode(c_str, size, __PYX_DEFAULT_STRING_ENCODING, NULL)

// __PYX_DEFAULT_STRING_ENCODING is either a user provided string constant
// or we need to look it up here
#if __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT
static char* __PYX_DEFAULT_STRING_ENCODING;

static int __Pyx_init_sys_getdefaultencoding_params(void) {
    PyObject* sys;
    PyObject* default_encoding = NULL;
    char* default_encoding_c;

    sys = PyImport_ImportModule("sys");
    if (!sys) goto bad;
    default_encoding = PyObject_CallMethod(sys, (char*) (const char*) "getdefaultencoding", NULL);
    Py_DECREF(sys);
    if (!default_encoding) goto bad;
    default_encoding_c = PyBytes_AsString(default_encoding);
    if (!default_encoding_c) goto bad;
    __PYX_DEFAULT_STRING_ENCODING = (char*) malloc(strlen(default_encoding_c));
    if (!__PYX_DEFAULT_STRING_ENCODING) goto bad;
    strcpy(__PYX_DEFAULT_STRING_ENCODING, default_encoding_c);
    Py_DECREF(default_encoding);
    return 0;
bad:
    Py_XDECREF(default_encoding);
    return -1;
}
#endif
#endif

/////////////// TypeConversions ///////////////
//@requires: PyLongInternals

/* Type Conversion Functions */

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_FromString(const char* c_str) {
    return __Pyx_PyUnicode_FromStringAndSize(c_str, (Py_ssize_t)strlen(c_str));
}

static CYTHON_INLINE char* __Pyx_PyObject_AsString(PyObject* o) {
    Py_ssize_t ignore;
    return __Pyx_PyObject_AsStringAndSize(o, &ignore);
}

static CYTHON_INLINE char* __Pyx_PyObject_AsStringAndSize(PyObject* o, Py_ssize_t *length) {
#if CYTHON_COMPILING_IN_CPYTHON && (__PYX_DEFAULT_STRING_ENCODING_IS_ASCII || __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT)
    if (
#if PY_MAJOR_VERSION < 3 && __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
            __Pyx_sys_getdefaultencoding_not_ascii &&
#endif
            PyUnicode_Check(o)) {
#if PY_VERSION_HEX < 0x03030000
        char* defenc_c;
        // borrowed reference, cached internally in 'o' by CPython
        PyObject* defenc = _PyUnicode_AsDefaultEncodedString(o, NULL);
        if (!defenc) return NULL;
        defenc_c = PyBytes_AS_STRING(defenc);
#if __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
        {
            char* end = defenc_c + PyBytes_GET_SIZE(defenc);
            char* c;
            for (c = defenc_c; c < end; c++) {
                if ((unsigned char) (*c) >= 128) {
                    // raise the error
                    PyUnicode_AsASCIIString(o);
                    return NULL;
                }
            }
        }
#endif /*__PYX_DEFAULT_STRING_ENCODING_IS_ASCII*/
        *length = PyBytes_GET_SIZE(defenc);
        return defenc_c;
#else /* PY_VERSION_HEX < 0x03030000 */
        if (__Pyx_PyUnicode_READY(o) == -1) return NULL;
#if __PYX_DEFAULT_STRING_ENCODING_IS_ASCII
        if (PyUnicode_IS_ASCII(o)) {
            // cached for the lifetime of the object
            *length = PyUnicode_GET_LENGTH(o);
            return PyUnicode_AsUTF8(o);
        } else {
            // raise the error
            PyUnicode_AsASCIIString(o);
            return NULL;
        }
#else /* __PYX_DEFAULT_STRING_ENCODING_IS_ASCII */
        return PyUnicode_AsUTF8AndSize(o, length);
#endif /* __PYX_DEFAULT_STRING_ENCODING_IS_ASCII */
#endif /* PY_VERSION_HEX < 0x03030000 */
    } else
#endif /* __PYX_DEFAULT_STRING_ENCODING_IS_ASCII  || __PYX_DEFAULT_STRING_ENCODING_IS_DEFAULT */

#if (!CYTHON_COMPILING_IN_PYPY) || (defined(PyByteArray_AS_STRING) && defined(PyByteArray_GET_SIZE))
    if (PyByteArray_Check(o)) {
        *length = PyByteArray_GET_SIZE(o);
        return PyByteArray_AS_STRING(o);
    } else
#endif
    {
        char* result;
        int r = PyBytes_AsStringAndSize(o, &result, length);
        if (unlikely(r < 0)) {
            return NULL;
        } else {
            return result;
        }
    }
}

/* Note: __Pyx_PyObject_IsTrue is written to minimize branching. */
static CYTHON_INLINE int __Pyx_PyObject_IsTrue(PyObject* x) {
   int is_true = x == Py_True;
   if (is_true | (x == Py_False) | (x == Py_None)) return is_true;
   else return PyObject_IsTrue(x);
}

static CYTHON_INLINE PyObject* __Pyx_PyNumber_Int(PyObject* x) {
  PyNumberMethods *m;
  const char *name = NULL;
  PyObject *res = NULL;
#if PY_MAJOR_VERSION < 3
  if (PyInt_Check(x) || PyLong_Check(x))
#else
  if (PyLong_Check(x))
#endif
    return __Pyx_NewRef(x);
  m = Py_TYPE(x)->tp_as_number;
#if PY_MAJOR_VERSION < 3
  if (m && m->nb_int) {
    name = "int";
    res = PyNumber_Int(x);
  }
  else if (m && m->nb_long) {
    name = "long";
    res = PyNumber_Long(x);
  }
#else
  if (m && m->nb_int) {
    name = "int";
    res = PyNumber_Long(x);
  }
#endif
  if (res) {
#if PY_MAJOR_VERSION < 3
    if (!PyInt_Check(res) && !PyLong_Check(res)) {
#else
    if (!PyLong_Check(res)) {
#endif
      PyErr_Format(PyExc_TypeError,
                   "__%.4s__ returned non-%.4s (type %.200s)",
                   name, name, Py_TYPE(res)->tp_name);
      Py_DECREF(res);
      return NULL;
    }
  }
  else if (!PyErr_Occurred()) {
    PyErr_SetString(PyExc_TypeError,
                    "an integer is required");
  }
  return res;
}

{{py: from Cython.Utility import pylong_join }}

static CYTHON_INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject* b) {
  Py_ssize_t ival;
  PyObject *x;
#if PY_MAJOR_VERSION < 3
  if (likely(PyInt_CheckExact(b))) {
    if (sizeof(Py_ssize_t) >= sizeof(long))
        return PyInt_AS_LONG(b);
    else
        return PyInt_AsSsize_t(x);
  }
#endif
  if (likely(PyLong_CheckExact(b))) {
    #if CYTHON_USE_PYLONG_INTERNALS
    const digit* digits = ((PyLongObject*)b)->ob_digit;
    const Py_ssize_t size = Py_SIZE(b);
    // handle most common case first to avoid indirect branch and optimise branch prediction
    if (likely(__Pyx_sst_abs(size) <= 1)) {
        ival = likely(size) ? digits[0] : 0;
        if (size == -1) ival = -ival;
        return ival;
    } else {
      switch (size) {
         {{for _size in (2, 3, 4)}}
         {{for _case in (_size, -_size)}}
         case {{_case}}:
           if (8 * sizeof(Py_ssize_t) > {{_size}} * PyLong_SHIFT) {
             return {{'-' if _case < 0 else ''}}(Py_ssize_t) {{pylong_join(_size, 'digits', 'size_t')}};
           }
           break;
         {{endfor}}
         {{endfor}}
      }
    }
    #endif
    return PyLong_AsSsize_t(b);
  }
  x = PyNumber_Index(b);
  if (!x) return -1;
  ival = PyInt_AsSsize_t(x);
  Py_DECREF(x);
  return ival;
}

static CYTHON_INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t ival) {
    return PyInt_FromSize_t(ival);
}


/////////////// ToPyCTupleUtility.proto ///////////////
static PyObject* {{funcname}}({{struct_type_decl}});

/////////////// ToPyCTupleUtility ///////////////
static PyObject* {{funcname}}({{struct_type_decl}} value) {
    PyObject* item = NULL;
    PyObject* result = PyTuple_New({{size}});
    if (!result) goto bad;

    {{for ix, component in enumerate(components):}}
        {{py:attr = "value.f%s" % ix}}
        item = {{component.to_py_function}}({{attr}});
        if (!item) goto bad;
        PyTuple_SET_ITEM(result, {{ix}}, item);
    {{endfor}}

    return result;
bad:
    Py_XDECREF(item);
    Py_XDECREF(result);
    return NULL;
}


/////////////// FromPyCTupleUtility.proto ///////////////
static {{struct_type_decl}} {{funcname}}(PyObject *);

/////////////// FromPyCTupleUtility ///////////////
static {{struct_type_decl}} {{funcname}}(PyObject * o) {
    {{struct_type_decl}} result;

    if (!PyTuple_Check(o) || PyTuple_GET_SIZE(o) != {{size}}) {
        PyErr_Format(PyExc_TypeError, "Expected %.16s of size %d, got %.200s", "a tuple", {{size}}, Py_TYPE(o)->tp_name);
        goto bad;
    }

#if CYTHON_COMPILING_IN_CPYTHON
    {{for ix, component in enumerate(components):}}
        {{py:attr = "result.f%s" % ix}}
        {{attr}} = {{component.from_py_function}}(PyTuple_GET_ITEM(o, {{ix}}));
        if ({{component.error_condition(attr)}}) goto bad;
    {{endfor}}
#else
    {
        PyObject *item;
    {{for ix, component in enumerate(components):}}
        {{py:attr = "result.f%s" % ix}}
        item = PySequence_ITEM(o, {{ix}});  if (unlikely(!item)) goto bad;
        {{attr}} = {{component.from_py_function}}(item);
        Py_DECREF(item);
        if ({{component.error_condition(attr)}}) goto bad;
    {{endfor}}
    }
#endif

    return result;
bad:
    return result;
}


/////////////// UnicodeAsUCS4.proto ///////////////

static CYTHON_INLINE Py_UCS4 __Pyx_PyUnicode_AsPy_UCS4(PyObject*);

/////////////// UnicodeAsUCS4 ///////////////

static CYTHON_INLINE Py_UCS4 __Pyx_PyUnicode_AsPy_UCS4(PyObject* x) {
   Py_ssize_t length;
   #if CYTHON_PEP393_ENABLED
   length = PyUnicode_GET_LENGTH(x);
   if (likely(length == 1)) {
       return PyUnicode_READ_CHAR(x, 0);
   }
   #else
   length = PyUnicode_GET_SIZE(x);
   if (likely(length == 1)) {
       return PyUnicode_AS_UNICODE(x)[0];
   }
   #if Py_UNICODE_SIZE == 2
   else if (PyUnicode_GET_SIZE(x) == 2) {
       Py_UCS4 high_val = PyUnicode_AS_UNICODE(x)[0];
       if (high_val >= 0xD800 && high_val <= 0xDBFF) {
           Py_UCS4 low_val = PyUnicode_AS_UNICODE(x)[1];
           if (low_val >= 0xDC00 && low_val <= 0xDFFF) {
               return 0x10000 + (((high_val & ((1<<10)-1)) << 10) | (low_val & ((1<<10)-1)));
           }
       }
   }
   #endif
   #endif
   PyErr_Format(PyExc_ValueError,
                "only single character unicode strings can be converted to Py_UCS4, "
                "got length %" CYTHON_FORMAT_SSIZE_T "d", length);
   return (Py_UCS4)-1;
}


/////////////// ObjectAsUCS4.proto ///////////////
//@requires: UnicodeAsUCS4

#define __Pyx_PyObject_AsPy_UCS4(x) \
    (likely(PyUnicode_Check(x)) ? __Pyx_PyUnicode_AsPy_UCS4(x) : __Pyx__PyObject_AsPy_UCS4(x))
static Py_UCS4 __Pyx__PyObject_AsPy_UCS4(PyObject*);

/////////////// ObjectAsUCS4 ///////////////

static Py_UCS4 __Pyx__PyObject_AsPy_UCS4(PyObject* x) {
   long ival;
   ival = __Pyx_PyInt_As_long(x);
   if (unlikely(ival < 0)) {
       if (!PyErr_Occurred())
           PyErr_SetString(PyExc_OverflowError,
                           "cannot convert negative value to Py_UCS4");
       return (Py_UCS4)-1;
   } else if (unlikely(ival > 1114111)) {
       PyErr_SetString(PyExc_OverflowError,
                       "value too large to convert to Py_UCS4");
       return (Py_UCS4)-1;
   }
   return (Py_UCS4)ival;
}


/////////////// ObjectAsPyUnicode.proto ///////////////

static CYTHON_INLINE Py_UNICODE __Pyx_PyObject_AsPy_UNICODE(PyObject*);

/////////////// ObjectAsPyUnicode ///////////////

static CYTHON_INLINE Py_UNICODE __Pyx_PyObject_AsPy_UNICODE(PyObject* x) {
    long ival;
    #if CYTHON_PEP393_ENABLED
    #if Py_UNICODE_SIZE > 2
    const long maxval = 1114111;
    #else
    const long maxval = 65535;
    #endif
    #else
    static long maxval = 0;
    #endif
    if (PyUnicode_Check(x)) {
        if (unlikely(__Pyx_PyUnicode_GET_LENGTH(x) != 1)) {
            PyErr_Format(PyExc_ValueError,
                         "only single character unicode strings can be converted to Py_UNICODE, "
                         "got length %" CYTHON_FORMAT_SSIZE_T "d", __Pyx_PyUnicode_GET_LENGTH(x));
            return (Py_UNICODE)-1;
        }
        #if CYTHON_PEP393_ENABLED
        ival = PyUnicode_READ_CHAR(x, 0);
        #else
        return PyUnicode_AS_UNICODE(x)[0];
        #endif
    } else {
        #if !CYTHON_PEP393_ENABLED
        if (unlikely(!maxval))
            maxval = (long)PyUnicode_GetMax();
        #endif
        ival = __Pyx_PyInt_As_long(x);
    }
    if (unlikely(ival < 0)) {
        if (!PyErr_Occurred())
            PyErr_SetString(PyExc_OverflowError,
                            "cannot convert negative value to Py_UNICODE");
        return (Py_UNICODE)-1;
    } else if (unlikely(ival > maxval)) {
        PyErr_SetString(PyExc_OverflowError,
                        "value too large to convert to Py_UNICODE");
        return (Py_UNICODE)-1;
    }
    return (Py_UNICODE)ival;
}


/////////////// CIntToPy.proto ///////////////

static CYTHON_INLINE PyObject* {{TO_PY_FUNCTION}}({{TYPE}} value);

/////////////// CIntToPy ///////////////

static CYTHON_INLINE PyObject* {{TO_PY_FUNCTION}}({{TYPE}} value) {
    const {{TYPE}} neg_one = ({{TYPE}}) -1, const_zero = ({{TYPE}}) 0;
    const int is_unsigned = neg_one > const_zero;
    if (is_unsigned) {
        if (sizeof({{TYPE}}) < sizeof(long)) {
            return PyInt_FromLong((long) value);
        } else if (sizeof({{TYPE}}) <= sizeof(unsigned long)) {
            return PyLong_FromUnsignedLong((unsigned long) value);
        } else if (sizeof({{TYPE}}) <= sizeof(unsigned PY_LONG_LONG)) {
            return PyLong_FromUnsignedLongLong((unsigned PY_LONG_LONG) value);
        }
    } else {
        if (sizeof({{TYPE}}) <= sizeof(long)) {
            return PyInt_FromLong((long) value);
        } else if (sizeof({{TYPE}}) <= sizeof(PY_LONG_LONG)) {
            return PyLong_FromLongLong((PY_LONG_LONG) value);
        }
    }
    {
        int one = 1; int little = (int)*(unsigned char *)&one;
        unsigned char *bytes = (unsigned char *)&value;
        return _PyLong_FromByteArray(bytes, sizeof({{TYPE}}),
                                     little, !is_unsigned);
    }
}


/////////////// CIntFromPyVerify ///////////////

// see CIntFromPy
#define __PYX_VERIFY_RETURN_INT(target_type, func_type, func_value)       \
    __PYX__VERIFY_RETURN_INT(target_type, func_type, func_value, 0)

#define __PYX_VERIFY_RETURN_INT_EXC(target_type, func_type, func_value)   \
    __PYX__VERIFY_RETURN_INT(target_type, func_type, func_value, 1)

#define __PYX__VERIFY_RETURN_INT(target_type, func_type, func_value, exc) \
    {                                                                     \
        func_type value = func_value;                                     \
        if (sizeof(target_type) < sizeof(func_type)) {                    \
            if (unlikely(value != (func_type) (target_type) value)) {     \
                func_type zero = 0;                                       \
                if (exc && unlikely(value == (func_type)-1 && PyErr_Occurred()))  \
                    return (target_type) -1;                              \
                if (is_unsigned && unlikely(value < zero))                \
                    goto raise_neg_overflow;                              \
                else                                                      \
                    goto raise_overflow;                                  \
            }                                                             \
        }                                                                 \
        return (target_type) value;                                       \
    }


/////////////// PyLongInternals ///////////////

#if CYTHON_USE_PYLONG_INTERNALS
  #include "longintrepr.h"
#endif


/////////////// CIntFromPy.proto ///////////////

static CYTHON_INLINE {{TYPE}} {{FROM_PY_FUNCTION}}(PyObject *);

/////////////// CIntFromPy ///////////////
//@requires: CIntFromPyVerify
//@requires: PyLongInternals

{{py: from Cython.Utility import pylong_join }}

static CYTHON_INLINE {{TYPE}} {{FROM_PY_FUNCTION}}(PyObject *x) {
    const {{TYPE}} neg_one = ({{TYPE}}) -1, const_zero = ({{TYPE}}) 0;
    const int is_unsigned = neg_one > const_zero;
#if PY_MAJOR_VERSION < 3
    if (likely(PyInt_Check(x))) {
        if (sizeof({{TYPE}}) < sizeof(long)) {
            __PYX_VERIFY_RETURN_INT({{TYPE}}, long, PyInt_AS_LONG(x))
        } else {
            long val = PyInt_AS_LONG(x);
            if (is_unsigned && unlikely(val < 0)) {
                goto raise_neg_overflow;
            }
            return ({{TYPE}}) val;
        }
    } else
#endif
    if (likely(PyLong_Check(x))) {
        if (is_unsigned) {
#if CYTHON_USE_PYLONG_INTERNALS
            const digit* digits = ((PyLongObject*)x)->ob_digit;
            switch (Py_SIZE(x)) {
                case  0: return ({{TYPE}}) 0;
                case  1: __PYX_VERIFY_RETURN_INT({{TYPE}}, digit, digits[0])
                {{for _size in (2, 3, 4)}}
                case {{_size}}:
                    if (8 * sizeof({{TYPE}}) > {{_size-1}} * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > {{_size}} * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT({{TYPE}}, unsigned long, {{pylong_join(_size, 'digits')}})
                        } else if (8 * sizeof({{TYPE}}) >= {{_size}} * PyLong_SHIFT) {
                            return ({{TYPE}}) {{pylong_join(_size, 'digits', TYPE)}};
                        }
                    }
                    break;
                {{endfor}}
            }
#endif
#if CYTHON_COMPILING_IN_CPYTHON
            if (unlikely(Py_SIZE(x) < 0)) {
                goto raise_neg_overflow;
            }
#else
            {
                // misuse Py_False as a quick way to compare to a '0' int object in PyPy
                int result = PyObject_RichCompareBool(x, Py_False, Py_LT);
                if (unlikely(result < 0))
                    return ({{TYPE}}) -1;
                if (unlikely(result == 1))
                    goto raise_neg_overflow;
            }
#endif
            if (sizeof({{TYPE}}) <= sizeof(unsigned long)) {
                __PYX_VERIFY_RETURN_INT_EXC({{TYPE}}, unsigned long, PyLong_AsUnsignedLong(x))
            } else if (sizeof({{TYPE}}) <= sizeof(unsigned PY_LONG_LONG)) {
                __PYX_VERIFY_RETURN_INT_EXC({{TYPE}}, unsigned PY_LONG_LONG, PyLong_AsUnsignedLongLong(x))
            }
        } else {
            // signed
#if CYTHON_USE_PYLONG_INTERNALS
            const digit* digits = ((PyLongObject*)x)->ob_digit;
            switch (Py_SIZE(x)) {
                case  0: return ({{TYPE}}) 0;
                case -1: __PYX_VERIFY_RETURN_INT({{TYPE}}, sdigit, -(sdigit) digits[0])
                case  1: __PYX_VERIFY_RETURN_INT({{TYPE}},  digit, +digits[0])
                {{for _size in (2, 3, 4)}}
                {{for _case in (-_size, _size)}}
                case {{_case}}:
                    if (8 * sizeof({{TYPE}}){{' - 1' if _case < 0 else ''}} > {{_size-1}} * PyLong_SHIFT) {
                        if (8 * sizeof(unsigned long) > {{_size}} * PyLong_SHIFT) {
                            __PYX_VERIFY_RETURN_INT({{TYPE}}, {{'long' if _case < 0 else 'unsigned long'}}, {{'-(long) ' if _case < 0 else ''}}{{pylong_join(_size, 'digits')}})
                        } else if (8 * sizeof({{TYPE}}) - 1 > {{_size}} * PyLong_SHIFT) {
                            return ({{TYPE}}) ({{'((%s)-1)*' % TYPE if _case < 0 else ''}}{{pylong_join(_size, 'digits', TYPE)}});
                        }
                    }
                    break;
                {{endfor}}
                {{endfor}}
            }
#endif
            if (sizeof({{TYPE}}) <= sizeof(long)) {
                __PYX_VERIFY_RETURN_INT_EXC({{TYPE}}, long, PyLong_AsLong(x))
            } else if (sizeof({{TYPE}}) <= sizeof(PY_LONG_LONG)) {
                __PYX_VERIFY_RETURN_INT_EXC({{TYPE}}, PY_LONG_LONG, PyLong_AsLongLong(x))
            }
        }
        {
#if CYTHON_COMPILING_IN_PYPY && !defined(_PyLong_AsByteArray)
            PyErr_SetString(PyExc_RuntimeError,
                            "_PyLong_AsByteArray() not available in PyPy, cannot convert large numbers");
#else
            {{TYPE}} val;
            PyObject *v = __Pyx_PyNumber_Int(x);
 #if PY_MAJOR_VERSION < 3
            if (likely(v) && !PyLong_Check(v)) {
                PyObject *tmp = v;
                v = PyNumber_Long(tmp);
                Py_DECREF(tmp);
            }
 #endif
            if (likely(v)) {
                int one = 1; int is_little = (int)*(unsigned char *)&one;
                unsigned char *bytes = (unsigned char *)&val;
                int ret = _PyLong_AsByteArray((PyLongObject *)v,
                                              bytes, sizeof(val),
                                              is_little, !is_unsigned);
                Py_DECREF(v);
                if (likely(!ret))
                    return val;
            }
#endif
            return ({{TYPE}}) -1;
        }
    } else {
        {{TYPE}} val;
        PyObject *tmp = __Pyx_PyNumber_Int(x);
        if (!tmp) return ({{TYPE}}) -1;
        val = {{FROM_PY_FUNCTION}}(tmp);
        Py_DECREF(tmp);
        return val;
    }

raise_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "value too large to convert to {{TYPE}}");
    return ({{TYPE}}) -1;

raise_neg_overflow:
    PyErr_SetString(PyExc_OverflowError,
        "can't convert negative value to {{TYPE}}");
    return ({{TYPE}}) -1;
}
