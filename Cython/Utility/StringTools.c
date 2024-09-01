
//////////////////// IncludeStringH.proto ////////////////////

#include <string.h>

//////////////////// IncludeCppStringH.proto ////////////////////

#include <string>


//////////////////// ssize_pyunicode_strlen.proto ////////////////////

static CYTHON_INLINE Py_ssize_t __Pyx_Py_UNICODE_ssize_strlen(const Py_UNICODE *u);/*proto*/

//////////////////// ssize_pyunicode_strlen ////////////////////
//@requires: pyunicode_strlen

static CYTHON_INLINE Py_ssize_t __Pyx_Py_UNICODE_ssize_strlen(const Py_UNICODE *u) {
    size_t len = __Pyx_Py_UNICODE_strlen(u);
    if (unlikely(len > PY_SSIZE_T_MAX)) {
        PyErr_SetString(PyExc_OverflowError, "Py_UNICODE string is too long");
        return -1;
    }
    return (Py_ssize_t) len;
}

//////////////////// pyunicode_strlen.proto ///////////////

// There used to be a Py_UNICODE_strlen() in CPython 3.x, but it is deprecated since Py3.3.
static CYTHON_INLINE size_t __Pyx_Py_UNICODE_strlen(const Py_UNICODE *u); /* proto */

//////////////////// pyunicode_strlen /////////////////////

// Note: will not work in the limited API since Py_UNICODE is not available there.
// May stop working at some point after Python 3.13 (deprecated)
static CYTHON_INLINE size_t __Pyx_Py_UNICODE_strlen(const Py_UNICODE *u)
{
    const Py_UNICODE *u_end = u;
    while (*u_end++) ;
    return (size_t)(u_end - u - 1);
}

//////////////////// pyunicode_from_unicode.proto //////////////////////
//@requires: pyunicode_strlen

#define __Pyx_PyUnicode_FromUnicode(u)       PyUnicode_FromUnicode(u, __Pyx_Py_UNICODE_strlen(u))
#define __Pyx_PyUnicode_FromUnicodeAndLength PyUnicode_FromUnicode


//////////////////// InitStrings.proto ////////////////////
//@proto_block: pystring_table

static int __Pyx_InitStrings(__Pyx_StringTabEntry const *t, PyObject **target, const char* const* encoding_names); /*proto*/

//////////////////// InitStrings ////////////////////

static int __Pyx_InitStrings(__Pyx_StringTabEntry const *t, PyObject **target, const char* const* encoding_names) {
    while (t->s) {
        PyObject *str;
        if (t->is_unicode) {
            if (t->intern) {
                str = PyUnicode_InternFromString(t->s);
            } else if (t->encoding) {
                str = PyUnicode_Decode(t->s, t->n - 1, encoding_names[t->encoding], NULL);
            } else {
                str = PyUnicode_FromStringAndSize(t->s, t->n - 1);
            }
        } else {
            str = PyBytes_FromStringAndSize(t->s, t->n - 1);
        }
        if (!str)
            return -1;
        *target = str;
        // initialise cached hash value
        if (PyObject_Hash(str) == -1)
            return -1;
        ++t;
        ++target;
    }
    return 0;
}

//////////////////// BytesContains.proto ////////////////////

static CYTHON_INLINE int __Pyx_BytesContains(PyObject* bytes, char character); /*proto*/

//////////////////// BytesContains ////////////////////
//@requires: IncludeStringH

static CYTHON_INLINE int __Pyx_BytesContains(PyObject* bytes, char character) {
    const Py_ssize_t length = __Pyx_PyBytes_GET_SIZE(bytes);
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(length == -1)) return -1;
#endif
    const char* char_start = __Pyx_PyBytes_AsString(bytes);
#if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(!char_start)) return -1;
#endif
    return memchr(char_start, (unsigned char)character, (size_t)length) != NULL;
}


//////////////////// PyUCS4InUnicode.proto ////////////////////

static CYTHON_INLINE int __Pyx_UnicodeContainsUCS4(PyObject* unicode, Py_UCS4 character); /*proto*/

//////////////////// PyUCS4InUnicode ////////////////////

static CYTHON_INLINE int __Pyx_UnicodeContainsUCS4(PyObject* unicode, Py_UCS4 character) {
    // Note that from Python 3.7, the indices of FindChar are adjusted to match the bounds
    // so need to check the length
    Py_ssize_t idx = PyUnicode_FindChar(unicode, character, 0, PY_SSIZE_T_MAX, 1);
    if (unlikely(idx == -2)) return -1;
    // >= 0: found the index, == -1: not found
    return idx >= 0;
}


//////////////////// PyUnicodeContains.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyUnicode_ContainsTF(PyObject* substring, PyObject* text, int eq) {
    int result = PyUnicode_Contains(text, substring);
    return unlikely(result < 0) ? result : (result == (eq == Py_EQ));
}


//////////////////// CStringEquals.proto ////////////////////

static CYTHON_INLINE int __Pyx_StrEq(const char *, const char *); /*proto*/

//////////////////// CStringEquals ////////////////////

static CYTHON_INLINE int __Pyx_StrEq(const char *s1, const char *s2) {
    while (*s1 != '\0' && *s1 == *s2) { s1++; s2++; }
    return *s1 == *s2;
}


//////////////////// UnicodeEquals.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals); /*proto*/

//////////////////// UnicodeEquals ////////////////////
//@requires: BytesEquals

static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals) {
#if CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_GRAAL
    return PyObject_RichCompareBool(s1, s2, equals);
#else
    int s1_is_unicode, s2_is_unicode;
    if (s1 == s2) {
        /* as done by PyObject_RichCompareBool(); also catches the (interned) empty string */
        goto return_eq;
    }
    s1_is_unicode = PyUnicode_CheckExact(s1);
    s2_is_unicode = PyUnicode_CheckExact(s2);
    if (s1_is_unicode & s2_is_unicode) {
        Py_ssize_t length, length2;
        int kind;
        void *data1, *data2;
        #if !CYTHON_COMPILING_IN_LIMITED_API
        if (unlikely(__Pyx_PyUnicode_READY(s1) < 0) || unlikely(__Pyx_PyUnicode_READY(s2) < 0))
            return -1;
        #endif
        length = __Pyx_PyUnicode_GET_LENGTH(s1);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(length < 0)) return -1;
        #endif
        length2 = __Pyx_PyUnicode_GET_LENGTH(s2);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(length2 < 0)) return -1;
        #endif
        if (length != length2) {
            goto return_ne;
        }
#if CYTHON_USE_UNICODE_INTERNALS
        {
            Py_hash_t hash1, hash2;
            hash1 = ((PyASCIIObject*)s1)->hash;
            hash2 = ((PyASCIIObject*)s2)->hash;
            if (hash1 != hash2 && hash1 != -1 && hash2 != -1) {
                goto return_ne;
            }
        }
#endif
        // len(s1) == len(s2) >= 1  (empty string is interned, and "s1 is not s2")
        kind = __Pyx_PyUnicode_KIND(s1);
        if (kind != __Pyx_PyUnicode_KIND(s2)) {
            goto return_ne;
        }
        data1 = __Pyx_PyUnicode_DATA(s1);
        data2 = __Pyx_PyUnicode_DATA(s2);
        if (__Pyx_PyUnicode_READ(kind, data1, 0) != __Pyx_PyUnicode_READ(kind, data2, 0)) {
            goto return_ne;
        } else if (length == 1) {
            goto return_eq;
        } else {
            int result = memcmp(data1, data2, (size_t)(length * kind));
            return (equals == Py_EQ) ? (result == 0) : (result != 0);
        }
    } else if ((s1 == Py_None) & s2_is_unicode) {
        goto return_ne;
    } else if ((s2 == Py_None) & s1_is_unicode) {
        goto return_ne;
    } else {
        int result;
        PyObject* py_result = PyObject_RichCompare(s1, s2, equals);
        if (!py_result)
            return -1;
        result = __Pyx_PyObject_IsTrue(py_result);
        Py_DECREF(py_result);
        return result;
    }
return_eq:
    return (equals == Py_EQ);
return_ne:
    return (equals == Py_NE);
#endif
}


//////////////////// BytesEquals.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals); /*proto*/

//////////////////// BytesEquals ////////////////////
//@requires: IncludeStringH

static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals) {
#if CYTHON_COMPILING_IN_PYPY || CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_GRAAL || \
        !(CYTHON_ASSUME_SAFE_SIZE && CYTHON_ASSUME_SAFE_MACROS)
    return PyObject_RichCompareBool(s1, s2, equals);
#else
    if (s1 == s2) {
        /* as done by PyObject_RichCompareBool(); also catches the (interned) empty string */
        return (equals == Py_EQ);
    } else if (PyBytes_CheckExact(s1) & PyBytes_CheckExact(s2)) {
        const char *ps1, *ps2;
        Py_ssize_t length = PyBytes_GET_SIZE(s1);
        if (length != PyBytes_GET_SIZE(s2))
            return (equals == Py_NE);
        // len(s1) == len(s2) >= 1  (empty string is interned, and "s1 is not s2")
        ps1 = PyBytes_AS_STRING(s1);
        ps2 = PyBytes_AS_STRING(s2);
        if (ps1[0] != ps2[0]) {
            return (equals == Py_NE);
        } else if (length == 1) {
            return (equals == Py_EQ);
        } else {
            int result;
#if CYTHON_USE_UNICODE_INTERNALS && (PY_VERSION_HEX < 0x030B0000)
            Py_hash_t hash1, hash2;
            hash1 = ((PyBytesObject*)s1)->ob_shash;
            hash2 = ((PyBytesObject*)s2)->ob_shash;
            if (hash1 != hash2 && hash1 != -1 && hash2 != -1) {
                return (equals == Py_NE);
            }
#endif
            result = memcmp(ps1, ps2, (size_t)length);
            return (equals == Py_EQ) ? (result == 0) : (result != 0);
        }
    } else if ((s1 == Py_None) & PyBytes_CheckExact(s2)) {
        return (equals == Py_NE);
    } else if ((s2 == Py_None) & PyBytes_CheckExact(s1)) {
        return (equals == Py_NE);
    } else {
        int result;
        PyObject* py_result = PyObject_RichCompare(s1, s2, equals);
        if (!py_result)
            return -1;
        result = __Pyx_PyObject_IsTrue(py_result);
        Py_DECREF(py_result);
        return result;
    }
#endif
}

//////////////////// GetItemIntByteArray.proto ////////////////////

#define __Pyx_GetItemInt_ByteArray(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck) \
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ? \
    __Pyx_GetItemInt_ByteArray_Fast(o, (Py_ssize_t)i, wraparound, boundscheck) : \
    (PyErr_SetString(PyExc_IndexError, "bytearray index out of range"), -1))

static CYTHON_INLINE int __Pyx_GetItemInt_ByteArray_Fast(PyObject* string, Py_ssize_t i,
                                                         int wraparound, int boundscheck);

//////////////////// GetItemIntByteArray ////////////////////

static CYTHON_INLINE int __Pyx_GetItemInt_ByteArray_Fast(PyObject* string, Py_ssize_t i,
                                                         int wraparound, int boundscheck) {
    Py_ssize_t length;
    if (wraparound | boundscheck) {
        length = __Pyx_PyByteArray_GET_SIZE(string);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(length < 0)) return -1;
        #endif
        if (wraparound & unlikely(i < 0)) i += length;
        if ((!boundscheck) || likely(__Pyx_is_valid_index(i, length))) {
            #if !CYTHON_ASSUME_SAFE_MACROS
            char *asString = PyByteArray_AsString(string);
            return likely(asString) ? (unsigned char) asString[i] : -1;
            #else
            return (unsigned char) (PyByteArray_AS_STRING(string)[i]);
            #endif
        } else {
            PyErr_SetString(PyExc_IndexError, "bytearray index out of range");
            return -1;
        }
    } else {
        #if !CYTHON_ASSUME_SAFE_MACROS
        char *asString = PyByteArray_AsString(string);
        return likely(asString) ? (unsigned char) asString[i] : -1;
        #else
        return (unsigned char) (PyByteArray_AS_STRING(string)[i]);
        #endif
    }
}


//////////////////// SetItemIntByteArray.proto ////////////////////

#define __Pyx_SetItemInt_ByteArray(o, i, v, type, is_signed, to_py_func, is_list, wraparound, boundscheck) \
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ? \
    __Pyx_SetItemInt_ByteArray_Fast(o, (Py_ssize_t)i, v, wraparound, boundscheck) : \
    (PyErr_SetString(PyExc_IndexError, "bytearray index out of range"), -1))

static CYTHON_INLINE int __Pyx_SetItemInt_ByteArray_Fast(PyObject* string, Py_ssize_t i, unsigned char v,
                                                         int wraparound, int boundscheck);

//////////////////// SetItemIntByteArray ////////////////////

static CYTHON_INLINE int __Pyx_SetItemInt_ByteArray_Fast(PyObject* string, Py_ssize_t i, unsigned char v,
                                                         int wraparound, int boundscheck) {
    Py_ssize_t length;
    if (wraparound | boundscheck) {
        length = __Pyx_PyByteArray_GET_SIZE(string);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(length < 0)) return -1;
        #endif
        if (wraparound & unlikely(i < 0)) i += length;
        if ((!boundscheck) || likely(__Pyx_is_valid_index(i, length))) {
            #if !CYTHON_ASSUME_SAFE_MACROS
            char *asString = PyByteArray_AsString(string);
            if (unlikely(!asString)) return -1;
            asString[i] = (char)v;
            #else
            PyByteArray_AS_STRING(string)[i] = (char) v;
            #endif
            return 0;
        } else {
            PyErr_SetString(PyExc_IndexError, "bytearray index out of range");
            return -1;
        }
    } else {
        #if !CYTHON_ASSUME_SAFE_MACROS
        char *asString = PyByteArray_AsString(string);
        if (unlikely(!asString)) return -1;
        asString[i] = (char)v;
        #else
        PyByteArray_AS_STRING(string)[i] = (char) v;
        #endif
        return 0;
    }
}


//////////////////// GetItemIntUnicode.proto ////////////////////

#define __Pyx_GetItemInt_Unicode(o, i, type, is_signed, to_py_func, is_list, wraparound, boundscheck) \
    (__Pyx_fits_Py_ssize_t(i, type, is_signed) ? \
    __Pyx_GetItemInt_Unicode_Fast(o, (Py_ssize_t)i, wraparound, boundscheck) : \
    (PyErr_SetString(PyExc_IndexError, "string index out of range"), (Py_UCS4)-1))

static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Fast(PyObject* ustring, Py_ssize_t i,
                                                           int wraparound, int boundscheck);

//////////////////// GetItemIntUnicode ////////////////////

static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Fast(PyObject* ustring, Py_ssize_t i,
                                                           int wraparound, int boundscheck) {
    Py_ssize_t length;
    if (unlikely(__Pyx_PyUnicode_READY(ustring) < 0)) return (Py_UCS4)-1;
    if (wraparound | boundscheck) {
        length = __Pyx_PyUnicode_GET_LENGTH(ustring);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(length < 0)) return (Py_UCS4)-1;
        #endif
        if (wraparound & unlikely(i < 0)) i += length;
        if ((!boundscheck) || likely(__Pyx_is_valid_index(i, length))) {
            return __Pyx_PyUnicode_READ_CHAR(ustring, i);
        } else {
            PyErr_SetString(PyExc_IndexError, "string index out of range");
            return (Py_UCS4)-1;
        }
    } else {
        return __Pyx_PyUnicode_READ_CHAR(ustring, i);
    }
}


/////////////// decode_c_string_utf16.proto ///////////////

static CYTHON_INLINE PyObject *__Pyx_PyUnicode_DecodeUTF16(const char *s, Py_ssize_t size, const char *errors) {
    int byteorder = 0;
    return PyUnicode_DecodeUTF16(s, size, errors, &byteorder);
}
static CYTHON_INLINE PyObject *__Pyx_PyUnicode_DecodeUTF16LE(const char *s, Py_ssize_t size, const char *errors) {
    int byteorder = -1;
    return PyUnicode_DecodeUTF16(s, size, errors, &byteorder);
}
static CYTHON_INLINE PyObject *__Pyx_PyUnicode_DecodeUTF16BE(const char *s, Py_ssize_t size, const char *errors) {
    int byteorder = 1;
    return PyUnicode_DecodeUTF16(s, size, errors, &byteorder);
}

/////////////// decode_cpp_string.proto ///////////////
//@requires: IncludeCppStringH
//@requires: decode_c_bytes

static CYTHON_INLINE PyObject* __Pyx_decode_cpp_string(
         std::string cppstring, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    return __Pyx_decode_c_bytes(
        cppstring.data(), cppstring.size(), start, stop, encoding, errors, decode_func);
}

/////////////// decode_c_string.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_decode_c_string(
         const char* cstring, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors));

/////////////// decode_c_string ///////////////
//@requires: IncludeStringH
//@requires: decode_c_string_utf16

/* duplicate code to avoid calling strlen() if start >= 0 and stop >= 0 */
static CYTHON_INLINE PyObject* __Pyx_decode_c_string(
         const char* cstring, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    Py_ssize_t length;
    if (unlikely((start < 0) | (stop < 0))) {
        size_t slen = strlen(cstring);
        if (unlikely(slen > (size_t) PY_SSIZE_T_MAX)) {
            PyErr_SetString(PyExc_OverflowError,
                            "c-string too long to convert to Python");
            return NULL;
        }
        length = (Py_ssize_t) slen;
        if (start < 0) {
            start += length;
            if (start < 0)
                start = 0;
        }
        if (stop < 0)
            stop += length;
    }
    if (unlikely(stop <= start))
        return __Pyx_NewRef(EMPTY(unicode));
    length = stop - start;
    cstring += start;
    if (decode_func) {
        return decode_func(cstring, length, errors);
    } else {
        return PyUnicode_Decode(cstring, length, encoding, errors);
    }
}

/////////////// decode_c_bytes.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_decode_c_bytes(
         const char* cstring, Py_ssize_t length, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors));

/////////////// decode_c_bytes ///////////////
//@requires: decode_c_string_utf16

static CYTHON_INLINE PyObject* __Pyx_decode_c_bytes(
         const char* cstring, Py_ssize_t length, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    if (unlikely((start < 0) | (stop < 0))) {
        if (start < 0) {
            start += length;
            if (start < 0)
                start = 0;
        }
        if (stop < 0)
            stop += length;
    }
    if (stop > length)
        stop = length;
    if (unlikely(stop <= start))
        return __Pyx_NewRef(EMPTY(unicode));
    length = stop - start;
    cstring += start;
    if (decode_func) {
        return decode_func(cstring, length, errors);
    } else {
        return PyUnicode_Decode(cstring, length, encoding, errors);
    }
}

/////////////// decode_bytes.proto ///////////////
//@requires: decode_c_bytes

static CYTHON_INLINE PyObject* __Pyx_decode_bytes(
         PyObject* string, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS && CYTHON_ASSUME_SAFE_SIZE
    as_c_string = PyBytes_AS_STRING(string);
    size = PyBytes_GET_SIZE(string);
#else
    if (PyBytes_AsStringAndSize(string, &as_c_string, &size) < 0) {
        return NULL;
    }
#endif
    return __Pyx_decode_c_bytes(
        as_c_string, size,
        start, stop, encoding, errors, decode_func);
}

/////////////// decode_bytearray.proto ///////////////
//@requires: decode_c_bytes

static CYTHON_INLINE PyObject* __Pyx_decode_bytearray(
         PyObject* string, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS && CYTHON_ASSUME_SAFE_SIZE
    as_c_string = PyByteArray_AS_STRING(string);
    size = PyByteArray_GET_SIZE(string);
#else
    if (!(as_c_string = PyByteArray_AsString(string))) return NULL;
    if ((size = PyByteArray_Size(string)) < 0) return NULL;
#endif
    return __Pyx_decode_c_bytes(
        as_c_string, size,
        start, stop, encoding, errors, decode_func);
}

/////////////// PyUnicode_Substring.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_Substring(
            PyObject* text, Py_ssize_t start, Py_ssize_t stop);

/////////////// PyUnicode_Substring ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_Substring(
            PyObject* text, Py_ssize_t start, Py_ssize_t stop) {
    Py_ssize_t length;
    #if !CYTHON_COMPILING_IN_LIMITED_API
    if (unlikely(__Pyx_PyUnicode_READY(text) == -1)) return NULL;
    #endif
    length = __Pyx_PyUnicode_GET_LENGTH(text);
    #if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(length < 0)) return NULL;
    #endif
    if (start < 0) {
        start += length;
        if (start < 0)
            start = 0;
    }
    if (stop < 0)
        stop += length;
    else if (stop > length)
        stop = length;
    if (stop <= start)
        return __Pyx_NewRef(EMPTY(unicode));
    if (start == 0 && stop == length)
        return __Pyx_NewRef(text);
#if CYTHON_COMPILING_IN_LIMITED_API
    // PyUnicode_Substring() does not support negative indexing but is otherwise fine to use.
    return PyUnicode_Substring(text, start, stop);
#else
    return PyUnicode_FromKindAndData(PyUnicode_KIND(text),
        PyUnicode_1BYTE_DATA(text) + start*PyUnicode_KIND(text), stop-start);
#endif
}


/////////////// py_unicode_istitle.proto ///////////////

// Py_UNICODE_ISTITLE() doesn't match unicode.istitle() as the latter
// additionally allows character that comply with Py_UNICODE_ISUPPER()

static CYTHON_INLINE int __Pyx_Py_UNICODE_ISTITLE(Py_UCS4 uchar) {
    return Py_UNICODE_ISTITLE(uchar) || Py_UNICODE_ISUPPER(uchar);
}


/////////////// py_unicode_isprintable.proto ///////////////

#if CYTHON_COMPILING_IN_PYPY && !defined(Py_UNICODE_ISPRINTABLE)
static int __Pyx_Py_UNICODE_ISPRINTABLE(Py_UCS4 uchar);/*proto*/
#else
#define __Pyx_Py_UNICODE_ISPRINTABLE(u)  Py_UNICODE_ISPRINTABLE(u)
#endif

/////////////// py_unicode_isprintable ///////////////

#if CYTHON_COMPILING_IN_PYPY && !defined(Py_UNICODE_ISPRINTABLE)
static int __Pyx_Py_UNICODE_ISPRINTABLE(Py_UCS4 uchar) {
    int result;
    PyObject* py_result;
    PyObject* ustring = PyUnicode_FromOrdinal(uchar);
    if (!ustring) goto bad;
    py_result = PyObject_CallMethod(ustring, "isprintable", NULL);
    Py_DECREF(ustring);
    if (!py_result) goto bad;
    result = PyObject_IsTrue(py_result);
    Py_DECREF(py_result);
    if (result == -1) goto bad;
    return result != 0;

bad:
    PyErr_Clear();
    return 0; /* cannot fail */
}
#endif


/////////////// unicode_tailmatch.proto ///////////////

static int __Pyx_PyUnicode_Tailmatch(
    PyObject* s, PyObject* substr, Py_ssize_t start, Py_ssize_t end, int direction); /*proto*/

/////////////// unicode_tailmatch ///////////////

// Python's unicode.startswith() and unicode.endswith() support a
// tuple of prefixes/suffixes, whereas it's much more common to
// test for a single unicode string.

static int __Pyx_PyUnicode_TailmatchTuple(PyObject* s, PyObject* substrings,
                                          Py_ssize_t start, Py_ssize_t end, int direction) {
    Py_ssize_t i, count = __Pyx_PyTuple_GET_SIZE(substrings);
    #if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(count < 0)) return -1;
    #endif
    for (i = 0; i < count; i++) {
        Py_ssize_t result;
#if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
        result = PyUnicode_Tailmatch(s, PyTuple_GET_ITEM(substrings, i),
                                     start, end, direction);
#else
        PyObject* sub = __Pyx_PySequence_ITEM(substrings, i);
        if (unlikely(!sub)) return -1;
        result = PyUnicode_Tailmatch(s, sub, start, end, direction);
        Py_DECREF(sub);
#endif
        if (result) {
            return (int) result;
        }
    }
    return 0;
}

static int __Pyx_PyUnicode_Tailmatch(PyObject* s, PyObject* substr,
                                     Py_ssize_t start, Py_ssize_t end, int direction) {
    if (unlikely(PyTuple_Check(substr))) {
        return __Pyx_PyUnicode_TailmatchTuple(s, substr, start, end, direction);
    }
    return (int) PyUnicode_Tailmatch(s, substr, start, end, direction);
}


/////////////// bytes_tailmatch.proto ///////////////

static int __Pyx_PyBytes_SingleTailmatch(PyObject* self, PyObject* arg,
                                         Py_ssize_t start, Py_ssize_t end, int direction); /*proto*/
static int __Pyx_PyBytes_Tailmatch(PyObject* self, PyObject* substr,
                                   Py_ssize_t start, Py_ssize_t end, int direction); /*proto*/

/////////////// bytes_tailmatch ///////////////

static int __Pyx_PyBytes_SingleTailmatch(PyObject* self, PyObject* arg,
                                         Py_ssize_t start, Py_ssize_t end, int direction) {
    char* self_ptr;
    Py_ssize_t self_len;
    char* sub_ptr;
    Py_ssize_t sub_len;
    int retval;

    #if CYTHON_COMPILING_IN_LIMITED_API && __PYX_LIMITED_VERSION_HEX < 0x030B0000
    PyObject *converted_arg = NULL;
    #else
    Py_buffer view;
    view.obj = NULL;
    #endif

    #if !(CYTHON_ASSUME_SAFE_MACROS && CYTHON_ASSUME_SAFE_SIZE)
    if (PyBytes_AsStringAndSize(self, &self_ptr, &self_len) == -1) return -1;
    #else
    self_ptr = PyBytes_AS_STRING(self);
    self_len = PyBytes_GET_SIZE(self);
    #endif

    if (PyBytes_Check(arg)) {
        #if !(CYTHON_ASSUME_SAFE_MACROS && CYTHON_ASSUME_SAFE_SIZE)
        if (PyBytes_AsStringAndSize(arg, &sub_ptr, &sub_len) == -1) return -1;
        #else
        sub_ptr = PyBytes_AS_STRING(arg);
        sub_len = PyBytes_GET_SIZE(arg);
        #endif
    }
    #if CYTHON_COMPILING_IN_LIMITED_API && __PYX_LIMITED_VERSION_HEX < 0x030B0000
    else if (PyByteArray_Check(arg)) {
        // The Limited API fallback is inefficient,
        // so special-case bytearray to be a bit faster. Keep this to the Limited
        // API only since the buffer protocol code is good enough otherwise.
        sub_ptr = PyByteArray_AsString(arg);
        if (unlikely(!sub_ptr)) return -1;
        sub_len = PyByteArray_Size(arg);
        if (unlikely(sub_len < 0)) return -1;
    } else {
        // Where buffer protocol is unavailable, just convert to bytes
        // (which is probably inefficient, but does work)
        // First check that the object is a buffer (since PyBytes_FromObject)
        // is more flexible than what endswith accepts.
        PyObject *as_memoryview = PyMemoryView_FromObject(arg);
        if (!as_memoryview) return -1;
        Py_DECREF(as_memoryview);
        converted_arg = PyBytes_FromObject(arg);
        if (!converted_arg) return -1;
        if (PyBytes_AsStringAndSize(converted_arg, &sub_ptr, &sub_len) == -1) {
            Py_DECREF(converted_arg);
            return -1;
        }

    }
    #else // LIMITED_API >= 030B0000 or !LIMITED_API
    else {
        if (unlikely(PyObject_GetBuffer(arg, &view, PyBUF_SIMPLE) == -1))
            return -1;
        sub_ptr = (char*) view.buf;
        sub_len = view.len;
    }
    #endif

    if (end > self_len)
        end = self_len;
    else if (end < 0)
        end += self_len;
    if (end < 0)
        end = 0;
    if (start < 0)
        start += self_len;
    if (start < 0)
        start = 0;

    if (direction > 0) {
        /* endswith */
        if (end-sub_len > start)
            start = end - sub_len;
    }

    if (start + sub_len <= end)
        retval = !memcmp(self_ptr+start, sub_ptr, (size_t)sub_len);
    else
        retval = 0;

    #if CYTHON_COMPILING_IN_LIMITED_API && __PYX_LIMITED_VERSION_HEX < 0x030B0000
    Py_XDECREF(converted_arg);
    #else
    if (view.obj)
        PyBuffer_Release(&view);
    #endif

    return retval;
}

static int __Pyx_PyBytes_TailmatchTuple(PyObject* self, PyObject* substrings,
                                        Py_ssize_t start, Py_ssize_t end, int direction) {
    Py_ssize_t i, count = __Pyx_PyTuple_GET_SIZE(substrings);
    #if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(count < 0)) return -1;
    #endif
    for (i = 0; i < count; i++) {
        int result;
#if CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
        result = __Pyx_PyBytes_SingleTailmatch(self, PyTuple_GET_ITEM(substrings, i),
                                               start, end, direction);
#else
        PyObject* sub = __Pyx_PySequence_ITEM(substrings, i);
        if (unlikely(!sub)) return -1;
        result = __Pyx_PyBytes_SingleTailmatch(self, sub, start, end, direction);
        Py_DECREF(sub);
#endif
        if (result) {
            return result;
        }
    }
    return 0;
}

static int __Pyx_PyBytes_Tailmatch(PyObject* self, PyObject* substr,
                                   Py_ssize_t start, Py_ssize_t end, int direction) {
    if (unlikely(PyTuple_Check(substr))) {
        return __Pyx_PyBytes_TailmatchTuple(self, substr, start, end, direction);
    }

    return __Pyx_PyBytes_SingleTailmatch(self, substr, start, end, direction);
}


/////////////// bytes_index.proto ///////////////

static CYTHON_INLINE char __Pyx_PyBytes_GetItemInt(PyObject* bytes, Py_ssize_t index, int check_bounds); /*proto*/

/////////////// bytes_index ///////////////

static CYTHON_INLINE char __Pyx_PyBytes_GetItemInt(PyObject* bytes, Py_ssize_t index, int check_bounds) {
    const char *asString;
    if (index < 0) {
        Py_ssize_t size = __Pyx_PyBytes_GET_SIZE(bytes);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(size < 0)) return (char) -1;
        #endif
        index += size;
    }
    if (check_bounds) {
        Py_ssize_t size = __Pyx_PyBytes_GET_SIZE(bytes);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(size < 0)) return (char) -1;
        #endif
        if (unlikely(!__Pyx_is_valid_index(index, size))) {
            PyErr_SetString(PyExc_IndexError, "string index out of range");
            return (char) -1;
        }
    }
    asString = __Pyx_PyBytes_AsString(bytes);
    #if !CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(!asString)) return (char)-1;
    #endif
    return asString[index];
}


//////////////////// StringJoin.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyBytes_Join(PyObject* sep, PyObject* values); /*proto*/

//////////////////// StringJoin ////////////////////
//@requires: ObjectHandling.c::PyObjectCallMethod1

static CYTHON_INLINE PyObject* __Pyx_PyBytes_Join(PyObject* sep, PyObject* values) {
    // avoid unused function
    (void) __Pyx_PyObject_CallMethod1;
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030d0000
    return _PyBytes_Join(sep, values);
#else
    return __Pyx_PyObject_CallMethod1(sep, PYIDENT("join"), values);
#endif
}


/////////////// JoinPyUnicode.proto ///////////////

static PyObject* __Pyx_PyUnicode_Join(PyObject** values, Py_ssize_t value_count, Py_ssize_t result_ulength,
                                      Py_UCS4 max_char);

/////////////// JoinPyUnicode ///////////////
//@requires: IncludeStringH

static PyObject* __Pyx_PyUnicode_Join(PyObject** values, Py_ssize_t value_count, Py_ssize_t result_ulength,
                                      Py_UCS4 max_char) {
#if CYTHON_USE_UNICODE_INTERNALS && CYTHON_ASSUME_SAFE_MACROS && !CYTHON_AVOID_BORROWED_REFS
    PyObject *result_uval;
    int result_ukind, kind_shift;
    Py_ssize_t i, char_pos;
    void *result_udata;

    if (max_char > 1114111) max_char = 1114111;
    result_uval = PyUnicode_New(result_ulength, max_char);
    if (unlikely(!result_uval)) return NULL;
    result_ukind = (max_char <= 255) ? PyUnicode_1BYTE_KIND : (max_char <= 65535) ? PyUnicode_2BYTE_KIND : PyUnicode_4BYTE_KIND;
    kind_shift = (result_ukind == PyUnicode_4BYTE_KIND) ? 2 : result_ukind - 1;
    result_udata = PyUnicode_DATA(result_uval);
    assert(kind_shift == 2 || kind_shift == 1 || kind_shift == 0);

    if (unlikely((PY_SSIZE_T_MAX >> kind_shift) - result_ulength < 0))
        goto overflow;

    char_pos = 0;
    for (i=0; i < value_count; i++) {
        int ukind;
        Py_ssize_t ulength;
        void *udata;
        PyObject *uval = values[i];
        #if !CYTHON_COMPILING_IN_LIMITED_API
        if (__Pyx_PyUnicode_READY(uval) == (-1))
            goto bad;
        #endif
        ulength = __Pyx_PyUnicode_GET_LENGTH(uval);
        #if !CYTHON_ASSUME_SAFE_SIZE
        if (unlikely(ulength < 0)) goto bad;
        #endif
        if (unlikely(!ulength))
            continue;
        if (unlikely((PY_SSIZE_T_MAX >> kind_shift) - ulength < char_pos))
            goto overflow;
        ukind = __Pyx_PyUnicode_KIND(uval);
        udata = __Pyx_PyUnicode_DATA(uval);
        if (ukind == result_ukind) {
            memcpy((char *)result_udata + (char_pos << kind_shift), udata, (size_t) (ulength << kind_shift));
        } else {
            #if PY_VERSION_HEX >= 0x030d0000
            if (unlikely(PyUnicode_CopyCharacters(result_uval, char_pos, uval, 0, ulength) < 0)) goto bad;
            #elif CYTHON_COMPILING_IN_CPYTHON || defined(_PyUnicode_FastCopyCharacters)
            _PyUnicode_FastCopyCharacters(result_uval, char_pos, uval, 0, ulength);
            #else
            Py_ssize_t j;
            for (j=0; j < ulength; j++) {
                Py_UCS4 uchar = __Pyx_PyUnicode_READ(ukind, udata, j);
                __Pyx_PyUnicode_WRITE(result_ukind, result_udata, char_pos+j, uchar);
            }
            #endif
        }
        char_pos += ulength;
    }
    return result_uval;
overflow:
    PyErr_SetString(PyExc_OverflowError, "join() result is too long for a Python string");
bad:
    Py_DECREF(result_uval);
    return NULL;
#else
    // non-CPython fallback
    Py_ssize_t i;
    PyObject *result = NULL;
    PyObject *value_tuple = PyTuple_New(value_count);
    if (unlikely(!value_tuple)) return NULL;
    CYTHON_UNUSED_VAR(max_char);
    CYTHON_UNUSED_VAR(result_ulength);

    for (i=0; i<value_count; i++) {
        if (__Pyx_PyTuple_SET_ITEM(value_tuple, i, values[i]) != (0)) goto bad;
        Py_INCREF(values[i]);
    }

    result = PyUnicode_Join(EMPTY(unicode), value_tuple);

bad:
    Py_DECREF(value_tuple);
    return result;
#endif
}


/////////////// BuildPyUnicode.proto ///////////////

static PyObject* __Pyx_PyUnicode_BuildFromAscii(Py_ssize_t ulength, const char* chars, int clength,
                                                int prepend_sign, char padding_char);

/////////////// BuildPyUnicode ///////////////

// Create a PyUnicode object from an ASCII char*, e.g. a formatted number.

static PyObject* __Pyx_PyUnicode_BuildFromAscii(Py_ssize_t ulength, const char* chars, int clength,
                                                int prepend_sign, char padding_char) {
    PyObject *uval;
    Py_ssize_t uoffset = ulength - clength;
#if CYTHON_USE_UNICODE_INTERNALS
    Py_ssize_t i;
    void *udata;
    uval = PyUnicode_New(ulength, 127);
    if (unlikely(!uval)) return NULL;
    udata = PyUnicode_DATA(uval);
    if (uoffset > 0) {
        i = 0;
        if (prepend_sign) {
            __Pyx_PyUnicode_WRITE(PyUnicode_1BYTE_KIND, udata, 0, '-');
            i++;
        }
        for (; i < uoffset; i++) {
            __Pyx_PyUnicode_WRITE(PyUnicode_1BYTE_KIND, udata, i, padding_char);
        }
    }
    for (i=0; i < clength; i++) {
        __Pyx_PyUnicode_WRITE(PyUnicode_1BYTE_KIND, udata, uoffset+i, chars[i]);
    }

#else
    // non-CPython
    {
        PyObject *sign = NULL, *padding = NULL;
        uval = NULL;
        if (uoffset > 0) {
            prepend_sign = !!prepend_sign;
            if (uoffset > prepend_sign) {
                padding = PyUnicode_FromOrdinal(padding_char);
                if (likely(padding) && uoffset > prepend_sign + 1) {
                    PyObject *tmp = PySequence_Repeat(padding, uoffset - prepend_sign);
                    Py_DECREF(padding);
                    padding = tmp;
                }
                if (unlikely(!padding)) goto done_or_error;
            }
            if (prepend_sign) {
                sign = PyUnicode_FromOrdinal('-');
                if (unlikely(!sign)) goto done_or_error;
            }
        }

        uval = PyUnicode_DecodeASCII(chars, clength, NULL);
        if (likely(uval) && padding) {
            PyObject *tmp = PyUnicode_Concat(padding, uval);
            Py_DECREF(uval);
            uval = tmp;
        }
        if (likely(uval) && sign) {
            PyObject *tmp = PyUnicode_Concat(sign, uval);
            Py_DECREF(uval);
            uval = tmp;
        }
done_or_error:
        Py_XDECREF(padding);
        Py_XDECREF(sign);
    }
#endif

    return uval;
}


//////////////////// ByteArrayAppendObject.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyByteArray_AppendObject(PyObject* bytearray, PyObject* value);

//////////////////// ByteArrayAppendObject ////////////////////
//@requires: ByteArrayAppend

static CYTHON_INLINE int __Pyx_PyByteArray_AppendObject(PyObject* bytearray, PyObject* value) {
    Py_ssize_t ival;
#if CYTHON_USE_PYLONG_INTERNALS
    if (likely(PyLong_CheckExact(value)) && likely(__Pyx_PyLong_IsCompact(value))) {
        if (__Pyx_PyLong_IsZero(value)) {
            ival = 0;
        } else {
            ival = __Pyx_PyLong_CompactValue(value);
            if (unlikely(ival > 255)) goto bad_range;
        }
    } else
#endif
    {
        // CPython calls PyNumber_Index() internally
        ival = __Pyx_PyIndex_AsSsize_t(value);
        if (unlikely(!__Pyx_is_valid_index(ival, 256))) {
            if (ival == -1 && PyErr_Occurred())
                return -1;
            goto bad_range;
        }
    }
    return __Pyx_PyByteArray_Append(bytearray, ival);
bad_range:
    PyErr_SetString(PyExc_ValueError, "byte must be in range(0, 256)");
    return -1;
}

//////////////////// ByteArrayAppend.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyByteArray_Append(PyObject* bytearray, int value);

//////////////////// ByteArrayAppend ////////////////////
//@requires: ObjectHandling.c::PyObjectCallMethod1

static CYTHON_INLINE int __Pyx_PyByteArray_Append(PyObject* bytearray, int value) {
    PyObject *pyval, *retval;
#if CYTHON_COMPILING_IN_CPYTHON
    if (likely(__Pyx_is_valid_index(value, 256))) {
        Py_ssize_t n = Py_SIZE(bytearray);
        if (likely(n != PY_SSIZE_T_MAX)) {
            if (unlikely(PyByteArray_Resize(bytearray, n + 1) < 0))
                return -1;
            PyByteArray_AS_STRING(bytearray)[n] = value;
            return 0;
        }
    } else {
        PyErr_SetString(PyExc_ValueError, "byte must be in range(0, 256)");
        return -1;
    }
#endif
    pyval = PyLong_FromLong(value);
    if (unlikely(!pyval))
        return -1;
    retval = __Pyx_PyObject_CallMethod1(bytearray, PYIDENT("append"), pyval);
    Py_DECREF(pyval);
    if (unlikely(!retval))
        return -1;
    Py_DECREF(retval);
    return 0;
}


//////////////////// PyObjectFormat.proto ////////////////////

#if CYTHON_USE_UNICODE_WRITER
static PyObject* __Pyx_PyObject_Format(PyObject* s, PyObject* f);
#else
#define __Pyx_PyObject_Format(s, f) PyObject_Format(s, f)
#endif

//////////////////// PyObjectFormat ////////////////////

#if CYTHON_USE_UNICODE_WRITER
static PyObject* __Pyx_PyObject_Format(PyObject* obj, PyObject* format_spec) {
    int ret;
    _PyUnicodeWriter writer;

    if (likely(PyFloat_CheckExact(obj))) {
        // copied from CPython 3.5 "float__format__()" in floatobject.c
        _PyUnicodeWriter_Init(&writer);
        ret = _PyFloat_FormatAdvancedWriter(
            &writer,
            obj,
            format_spec, 0, PyUnicode_GET_LENGTH(format_spec));
    } else if (likely(PyLong_CheckExact(obj))) {
        // copied from CPython 3.5 "long__format__()" in longobject.c
        _PyUnicodeWriter_Init(&writer);
        ret = _PyLong_FormatAdvancedWriter(
            &writer,
            obj,
            format_spec, 0, PyUnicode_GET_LENGTH(format_spec));
    } else {
        return PyObject_Format(obj, format_spec);
    }

    if (unlikely(ret == -1)) {
        _PyUnicodeWriter_Dealloc(&writer);
        return NULL;
    }
    return _PyUnicodeWriter_Finish(&writer);
}
#endif


//////////////////// PyObjectFormatSimple.proto ////////////////////

#if CYTHON_COMPILING_IN_PYPY
    #define __Pyx_PyObject_FormatSimple(s, f) ( \
        likely(PyUnicode_CheckExact(s)) ? (Py_INCREF(s), s) : \
        PyObject_Format(s, f))
#elif CYTHON_USE_TYPE_SLOTS
    // Py3 nicely returns unicode strings from str() and repr(), which makes this quite efficient for builtin types.
    // In Py3.8+, tp_str() delegates to tp_repr(), so we call tp_repr() directly here.
    #define __Pyx_PyObject_FormatSimple(s, f) ( \
        likely(PyUnicode_CheckExact(s)) ? (Py_INCREF(s), s) : \
        likely(PyLong_CheckExact(s)) ? PyLong_Type.tp_repr(s) : \
        likely(PyFloat_CheckExact(s)) ? PyFloat_Type.tp_repr(s) : \
        PyObject_Format(s, f))
#else
    #define __Pyx_PyObject_FormatSimple(s, f) ( \
        likely(PyUnicode_CheckExact(s)) ? (Py_INCREF(s), s) : \
        PyObject_Format(s, f))
#endif


//////////////////// PyObjectFormatAndDecref.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyObject_FormatSimpleAndDecref(PyObject* s, PyObject* f);
static CYTHON_INLINE PyObject* __Pyx_PyObject_FormatAndDecref(PyObject* s, PyObject* f);

//////////////////// PyObjectFormatAndDecref ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyObject_FormatSimpleAndDecref(PyObject* s, PyObject* f) {
    if (unlikely(!s)) return NULL;
    if (likely(PyUnicode_CheckExact(s))) return s;
    return __Pyx_PyObject_FormatAndDecref(s, f);
}

static CYTHON_INLINE PyObject* __Pyx_PyObject_FormatAndDecref(PyObject* s, PyObject* f) {
    PyObject *result;
    if (unlikely(!s)) return NULL;
    result = PyObject_Format(s, f);
    Py_DECREF(s);
    return result;
}


//////////////////// PyUnicode_Unicode.proto ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_Unicode(PyObject *obj);/*proto*/

//////////////////// PyUnicode_Unicode ////////////////////

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_Unicode(PyObject *obj) {
    if (unlikely(obj == Py_None))
        obj = PYUNICODE("None");
    return __Pyx_NewRef(obj);
}


//////////////////// PyObject_Unicode.proto ////////////////////

#define __Pyx_PyObject_Unicode(obj) \
    (likely(PyUnicode_CheckExact(obj)) ? __Pyx_NewRef(obj) : PyObject_Str(obj))
