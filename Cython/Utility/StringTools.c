
//////////////////// IncludeStringH.proto ////////////////////

#include <string.h>

//////////////////// IncludeCppStringH.proto ////////////////////

#include <string>

//////////////////// InitStrings.proto ////////////////////

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/

//////////////////// InitStrings ////////////////////

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        #if PY_MAJOR_VERSION < 3
        if (t->is_unicode) {
            *t->p = PyUnicode_DecodeUTF8(t->s, t->n - 1, NULL);
        } else if (t->intern) {
            *t->p = PyString_InternFromString(t->s);
        } else {
            *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        }
        #else  /* Python 3+ has unicode identifiers */
        if (t->is_unicode | t->is_str) {
            if (t->intern) {
                *t->p = PyUnicode_InternFromString(t->s);
            } else if (t->encoding) {
                *t->p = PyUnicode_Decode(t->s, t->n - 1, t->encoding, NULL);
            } else {
                *t->p = PyUnicode_FromStringAndSize(t->s, t->n - 1);
            }
        } else {
            *t->p = PyBytes_FromStringAndSize(t->s, t->n - 1);
        }
        #endif
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

//////////////////// BytesContains.proto ////////////////////

static CYTHON_INLINE int __Pyx_BytesContains(PyObject* bytes, char character); /*proto*/

//////////////////// BytesContains ////////////////////

static CYTHON_INLINE int __Pyx_BytesContains(PyObject* bytes, char character) {
    const Py_ssize_t length = PyBytes_GET_SIZE(bytes);
    char* char_start = PyBytes_AS_STRING(bytes);
    char* pos;
    for (pos=char_start; pos < char_start+length; pos++) {
        if (character == pos[0]) return 1;
    }
    return 0;
}


//////////////////// PyUCS4InUnicode.proto ////////////////////

static CYTHON_INLINE int __Pyx_UnicodeContainsUCS4(PyObject* unicode, Py_UCS4 character); /*proto*/
static CYTHON_INLINE int __Pyx_PyUnicodeBufferContainsUCS4(Py_UNICODE* buffer, Py_ssize_t length, Py_UCS4 character); /*proto*/

//////////////////// PyUCS4InUnicode ////////////////////

static CYTHON_INLINE int __Pyx_UnicodeContainsUCS4(PyObject* unicode, Py_UCS4 character) {
#if CYTHON_PEP393_ENABLED
    const int kind = PyUnicode_KIND(unicode);
    if (likely(kind != PyUnicode_WCHAR_KIND)) {
        Py_ssize_t i;
        const void* udata = PyUnicode_DATA(unicode);
        const Py_ssize_t length = PyUnicode_GET_LENGTH(unicode);
        for (i=0; i < length; i++) {
            if (unlikely(character == PyUnicode_READ(kind, udata, i))) return 1;
        }
        return 0;
    }
#endif
    return __Pyx_PyUnicodeBufferContainsUCS4(
        PyUnicode_AS_UNICODE(unicode),
        PyUnicode_GET_SIZE(unicode),
        character);
}

static CYTHON_INLINE int __Pyx_PyUnicodeBufferContainsUCS4(Py_UNICODE* buffer, Py_ssize_t length, Py_UCS4 character) {
    Py_UNICODE uchar;
    Py_UNICODE* pos;
    #if Py_UNICODE_SIZE == 2
    if (character > 65535) {
        /* handle surrogate pairs for Py_UNICODE buffers in 16bit Unicode builds */
        Py_UNICODE high_val, low_val;
        high_val = (Py_UNICODE) (0xD800 | (((character - 0x10000) >> 10) & ((1<<10)-1)));
        low_val  = (Py_UNICODE) (0xDC00 | ( (character - 0x10000)        & ((1<<10)-1)));
        for (pos=buffer; pos < buffer+length-1; pos++) {
            if (unlikely(high_val == pos[0]) & unlikely(low_val == pos[1])) return 1;
        }
        return 0;
    }
    #endif
    uchar = (Py_UNICODE) character;
    for (pos=buffer; pos < buffer+length; pos++) {
        if (unlikely(uchar == pos[0])) return 1;
    }
    return 0;
}


//////////////////// StrEquals.proto ////////////////////
//@requires: BytesEquals
//@requires: UnicodeEquals

#if PY_MAJOR_VERSION >= 3
#define __Pyx_PyString_Equals __Pyx_PyUnicode_Equals
#else
#define __Pyx_PyString_Equals __Pyx_PyBytes_Equals
#endif


//////////////////// UnicodeEquals.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals); /*proto*/

//////////////////// UnicodeEquals ////////////////////

static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals) {
#if CYTHON_COMPILING_IN_PYPY
    return PyObject_RichCompareBool(s1, s2, equals);
#else
    if (s1 == s2) {
        /* as done by PyObject_RichCompareBool(); also catches the (interned) empty string */
        return (equals == Py_EQ);
    } else if (PyUnicode_CheckExact(s1) & PyUnicode_CheckExact(s2)) {
        #if CYTHON_PEP393_ENABLED
        if ((PyUnicode_READY(s1) < 0) || (PyUnicode_READY(s2) < 0))
            return -1;
        if (PyUnicode_GET_LENGTH(s1) != PyUnicode_GET_LENGTH(s2)) {
            return (equals == Py_NE);
        } else if (PyUnicode_GET_LENGTH(s1) == 1) {
            Py_UCS4 ch1 = PyUnicode_READ_CHAR(s1, 0);
            Py_UCS4 ch2 = PyUnicode_READ_CHAR(s2, 0);
            return (equals == Py_EQ) ? (ch1 == ch2) : (ch1 != ch2);
//// currently disabled: may not be safe depending on who created the string
//        } else if (PyUnicode_MAX_CHAR_VALUE(s1) != PyUnicode_MAX_CHAR_VALUE(s2)) {
//            return (equals == Py_NE);
        #else
        if (PyUnicode_GET_SIZE(s1) != PyUnicode_GET_SIZE(s2)) {
            return (equals == Py_NE);
        } else if (PyUnicode_GET_SIZE(s1) == 1) {
            Py_UNICODE ch1 = PyUnicode_AS_UNICODE(s1)[0];
            Py_UNICODE ch2 = PyUnicode_AS_UNICODE(s2)[0];
            return (equals == Py_EQ) ? (ch1 == ch2) : (ch1 != ch2);
        #endif
        } else {
            int result = PyUnicode_Compare(s1, s2);
            if ((result == -1) && unlikely(PyErr_Occurred()))
                return -1;
            return (equals == Py_EQ) ? (result == 0) : (result != 0);
        }
    } else if ((s1 == Py_None) & PyUnicode_CheckExact(s2)) {
        return (equals == Py_NE);
    } else if ((s2 == Py_None) & PyUnicode_CheckExact(s1)) {
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


//////////////////// BytesEquals.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals); /*proto*/

//////////////////// BytesEquals ////////////////////
//@requires: IncludeStringH

static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals) {
#if CYTHON_COMPILING_IN_PYPY
    return PyObject_RichCompareBool(s1, s2, equals);
#else
    if (s1 == s2) {
        /* as done by PyObject_RichCompareBool(); also catches the (interned) empty string */
        return (equals == Py_EQ);
    } else if (PyBytes_CheckExact(s1) & PyBytes_CheckExact(s2)) {
        if (PyBytes_GET_SIZE(s1) != PyBytes_GET_SIZE(s2)) {
            return (equals == Py_NE);
        } else if (PyBytes_GET_SIZE(s1) == 1) {
            if (equals == Py_EQ)
                return (PyBytes_AS_STRING(s1)[0] == PyBytes_AS_STRING(s2)[0]);
            else
                return (PyBytes_AS_STRING(s1)[0] != PyBytes_AS_STRING(s2)[0]);
        } else {
            int result = memcmp(PyBytes_AS_STRING(s1), PyBytes_AS_STRING(s2), (size_t)PyBytes_GET_SIZE(s1));
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

//////////////////// GetItemIntUnicode.proto ////////////////////

#define __Pyx_GetItemInt_Unicode(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \
                                               __Pyx_GetItemInt_Unicode_Fast(o, i) : \
                                               __Pyx_GetItemInt_Unicode_Generic(o, to_py_func(i)))

static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Fast(PyObject* ustring, Py_ssize_t i);
static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Generic(PyObject* ustring, PyObject* j);

//////////////////// GetItemIntUnicode ////////////////////

static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Fast(PyObject* ustring, Py_ssize_t i) {
    Py_ssize_t length;
#if CYTHON_PEP393_ENABLED
    if (unlikely(__Pyx_PyUnicode_READY(ustring) < 0)) return (Py_UCS4)-1;
#endif
    length = __Pyx_PyUnicode_GET_LENGTH(ustring);
    if (likely((0 <= i) & (i < length))) {
        return __Pyx_PyUnicode_READ_CHAR(ustring, i);
    } else if ((-length <= i) & (i < 0)) {
        return __Pyx_PyUnicode_READ_CHAR(ustring, i + length);
    } else {
        PyErr_SetString(PyExc_IndexError, "string index out of range");
        return (Py_UCS4)-1;
    }
}

static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Generic(PyObject* ustring, PyObject* j) {
    Py_UCS4 uchar;
    PyObject *uchar_string;
    if (!j) return (Py_UCS4)-1;
    uchar_string = PyObject_GetItem(ustring, j);
    Py_DECREF(j);
    if (!uchar_string) return (Py_UCS4)-1;
#if CYTHON_PEP393_ENABLED
    if (unlikely(__Pyx_PyUnicode_READY(uchar_string) < 0)) {
        Py_DECREF(uchar_string);
        return (Py_UCS4)-1;
    }
#endif
    uchar = __Pyx_PyUnicode_READ_CHAR(uchar_string, 0);
    Py_DECREF(uchar_string);
    return uchar;
}

/////////////// decode_cpp_string.proto ///////////////
//@requires IncludeCppStringH

static CYTHON_INLINE PyObject* __Pyx_decode_cpp_string(
         std::string cppstring, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors));

/////////////// decode_cpp_string ///////////////

static CYTHON_INLINE PyObject* __Pyx_decode_cpp_string(
         std::string cppstring, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    const char* cstring = cppstring.data();
    Py_ssize_t length = cppstring.size();

    if (unlikely(start < 0)) {
        start += length;
        if (unlikely(start < 0))
            start = 0;
    }
    if (unlikely(stop < 0))
        stop += length;
    else if (stop >= length)
        stop = length;
    if (unlikely(start >= stop))
        return PyUnicode_FromUnicode(NULL, 0);
    cstring += start;
    length = stop - start;

    if (decode_func) {
        return decode_func(cstring, length, errors);
    } else {
        return PyUnicode_Decode(cstring, length, encoding, errors);
    }
}

/////////////// decode_c_string.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_decode_c_string(
         const char* cstring, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors));

/////////////// decode_c_string ///////////////
//@requires IncludeStringH

static CYTHON_INLINE PyObject* __Pyx_decode_c_string(
         const char* cstring, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    Py_ssize_t length;
    if (unlikely((start < 0) | (stop < 0))) {
        length = strlen(cstring);
        if (start < 0) {
            start += length;
            if (start < 0)
                start = 0;
        }
        if (stop < 0)
            stop += length;
    }
    length = stop - start;
    if (unlikely(length <= 0))
        return PyUnicode_FromUnicode(NULL, 0);
    cstring += start;
    if (decode_func) {
        return decode_func(cstring, length, errors);
    } else {
        return PyUnicode_Decode(cstring, length, encoding, errors);
    }
}

/////////////// decode_bytes.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_decode_bytes(
         PyObject* string, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors));

/////////////// decode_bytes ///////////////

static CYTHON_INLINE PyObject* __Pyx_decode_bytes(
         PyObject* string, Py_ssize_t start, Py_ssize_t stop,
         const char* encoding, const char* errors,
         PyObject* (*decode_func)(const char *s, Py_ssize_t size, const char *errors)) {
    char* cstring;
    Py_ssize_t length = PyBytes_GET_SIZE(string);
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
    length = stop - start;
    if (unlikely(length <= 0))
        return PyUnicode_FromUnicode(NULL, 0);
    cstring = PyBytes_AS_STRING(string) + start;
    if (decode_func) {
        return decode_func(cstring, length, errors);
    } else {
        return PyUnicode_Decode(cstring, length, encoding, errors);
    }
}
