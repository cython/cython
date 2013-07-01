
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


//////////////////// PyUnicodeContains.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyUnicode_Contains(PyObject* substring, PyObject* text, int eq) {
    int result = PyUnicode_Contains(text, substring);
    return unlikely(result < 0) ? result : (result == (eq == Py_EQ));
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

#define __Pyx_GetItemInt_Unicode(o, i, size, to_py_func, is_list, wraparound, boundscheck) \
    (((size) <= sizeof(Py_ssize_t)) ? \
    __Pyx_GetItemInt_Unicode_Fast(o, i, wraparound, boundscheck) : \
    __Pyx_GetItemInt_Unicode_Generic(o, to_py_func(i)))

static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Fast(PyObject* ustring, Py_ssize_t i,
                                                           int wraparound, int boundscheck);
static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Generic(PyObject* ustring, PyObject* j);

//////////////////// GetItemIntUnicode ////////////////////

static CYTHON_INLINE Py_UCS4 __Pyx_GetItemInt_Unicode_Fast(PyObject* ustring, Py_ssize_t i,
                                                           int wraparound, int boundscheck) {
    Py_ssize_t length;
#if CYTHON_PEP393_ENABLED
    if (unlikely(__Pyx_PyUnicode_READY(ustring) < 0)) return (Py_UCS4)-1;
#endif
    if (wraparound | boundscheck) {
        length = __Pyx_PyUnicode_GET_LENGTH(ustring);
        if (wraparound & unlikely(i < 0)) i += length;
        if ((!boundscheck) || likely((0 <= i) & (i < length))) {
            return __Pyx_PyUnicode_READ_CHAR(ustring, i);
        } else {
            PyErr_SetString(PyExc_IndexError, "string index out of range");
            return (Py_UCS4)-1;
        }
    } else {
        return __Pyx_PyUnicode_READ_CHAR(ustring, i);
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

/////////////// PyUnicode_Substring.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_Substring(
            PyObject* text, Py_ssize_t start, Py_ssize_t stop);

/////////////// PyUnicode_Substring ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyUnicode_Substring(
            PyObject* text, Py_ssize_t start, Py_ssize_t stop) {
    Py_ssize_t length;
#if CYTHON_PEP393_ENABLED
    if (unlikely(PyUnicode_READY(text) == -1)) return NULL;
    length = PyUnicode_GET_LENGTH(text);
#else
    length = PyUnicode_GET_SIZE(text);
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
    length = stop - start;
    if (length <= 0)
        return PyUnicode_FromUnicode(NULL, 0);
#if CYTHON_PEP393_ENABLED
    return PyUnicode_FromKindAndData(PyUnicode_KIND(text),
        PyUnicode_1BYTE_DATA(text) + start*PyUnicode_KIND(text), stop-start);
#else
    return PyUnicode_FromUnicode(PyUnicode_AS_UNICODE(text)+start, stop-start);
#endif
}


/////////////// py_unicode_istitle.proto ///////////////

// Py_UNICODE_ISTITLE() doesn't match unicode.istitle() as the latter
// additionally allows character that comply with Py_UNICODE_ISUPPER()

#if PY_VERSION_HEX < 0x030200A2
static CYTHON_INLINE int __Pyx_Py_UNICODE_ISTITLE(Py_UNICODE uchar)
#else
static CYTHON_INLINE int __Pyx_Py_UNICODE_ISTITLE(Py_UCS4 uchar)
#endif
{
    return Py_UNICODE_ISTITLE(uchar) || Py_UNICODE_ISUPPER(uchar);
}


/////////////// unicode_tailmatch.proto ///////////////

// Python's unicode.startswith() and unicode.endswith() support a
// tuple of prefixes/suffixes, whereas it's much more common to
// test for a single unicode string.

static int __Pyx_PyUnicode_Tailmatch(PyObject* s, PyObject* substr,
                                     Py_ssize_t start, Py_ssize_t end, int direction) {
    if (unlikely(PyTuple_Check(substr))) {
        Py_ssize_t i, count = PyTuple_GET_SIZE(substr);
        for (i = 0; i < count; i++) {
            int result;
#if CYTHON_COMPILING_IN_CPYTHON
            result = PyUnicode_Tailmatch(s, PyTuple_GET_ITEM(substr, i),
                                         start, end, direction);
#else
            PyObject* sub = PySequence_GetItem(substr, i);
            if (unlikely(!sub)) return -1;
            result = PyUnicode_Tailmatch(s, sub, start, end, direction);
            Py_DECREF(sub);
#endif
            if (result) {
                return result;
            }
        }
        return 0;
    }
    return PyUnicode_Tailmatch(s, substr, start, end, direction);
}


/////////////// bytes_tailmatch.proto ///////////////

static int __Pyx_PyBytes_SingleTailmatch(PyObject* self, PyObject* arg, Py_ssize_t start,
                                         Py_ssize_t end, int direction)
{
    const char* self_ptr = PyBytes_AS_STRING(self);
    Py_ssize_t self_len = PyBytes_GET_SIZE(self);
    const char* sub_ptr;
    Py_ssize_t sub_len;
    int retval;

#if PY_VERSION_HEX >= 0x02060000
    Py_buffer view;
    view.obj = NULL;
#endif

    if ( PyBytes_Check(arg) ) {
        sub_ptr = PyBytes_AS_STRING(arg);
        sub_len = PyBytes_GET_SIZE(arg);
    }
#if PY_MAJOR_VERSION < 3
    // Python 2.x allows mixing unicode and str
    else if ( PyUnicode_Check(arg) ) {
        return PyUnicode_Tailmatch(self, arg, start, end, direction);
    }
#endif
    else {
#if PY_VERSION_HEX < 0x02060000
        if (unlikely(PyObject_AsCharBuffer(arg, &sub_ptr, &sub_len)))
            return -1;
#else
        if (unlikely(PyObject_GetBuffer(self, &view, PyBUF_SIMPLE) == -1))
            return -1;
        sub_ptr = (const char*) view.buf;
        sub_len = view.len;
#endif
    }

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
        retval = !memcmp(self_ptr+start, sub_ptr, sub_len);
    else
        retval = 0;

#if PY_VERSION_HEX >= 0x02060000
    if (view.obj)
        PyBuffer_Release(&view);
#endif

    return retval;
}

static int __Pyx_PyBytes_Tailmatch(PyObject* self, PyObject* substr, Py_ssize_t start,
                                   Py_ssize_t end, int direction)
{
    if (unlikely(PyTuple_Check(substr))) {
        Py_ssize_t i, count = PyTuple_GET_SIZE(substr);
        for (i = 0; i < count; i++) {
            int result;
#if CYTHON_COMPILING_IN_CPYTHON
            result = __Pyx_PyBytes_SingleTailmatch(self, PyTuple_GET_ITEM(substr, i),
                                                   start, end, direction);
#else
            PyObject* sub = PySequence_GetItem(substr, i);
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

    return __Pyx_PyBytes_SingleTailmatch(self, substr, start, end, direction);
}


/////////////// str_tailmatch.proto ///////////////

static CYTHON_INLINE int __Pyx_PyStr_Tailmatch(PyObject* self, PyObject* arg, Py_ssize_t start,
                                               Py_ssize_t end, int direction);

/////////////// str_tailmatch ///////////////
//@requires: bytes_tailmatch
//@requires: unicode_tailmatch

static CYTHON_INLINE int __Pyx_PyStr_Tailmatch(PyObject* self, PyObject* arg, Py_ssize_t start,
                                               Py_ssize_t end, int direction)
{
    // We do not use a C compiler macro here to avoid "unused function"
    // warnings for the *_Tailmatch() function that is not being used in
    // the specific CPython version.  The C compiler will generate the same
    // code anyway, and will usually just remove the unused function.
    if (PY_MAJOR_VERSION < 3)
        return __Pyx_PyBytes_Tailmatch(self, arg, start, end, direction);
    else
        return __Pyx_PyUnicode_Tailmatch(self, arg, start, end, direction);
}


/////////////// bytes_index.proto ///////////////

static CYTHON_INLINE char __Pyx_PyBytes_GetItemInt(PyObject* bytes, Py_ssize_t index, int check_bounds) {
    if (check_bounds) {
        Py_ssize_t size = PyBytes_GET_SIZE(bytes);
        if (unlikely(index >= size) | ((index < 0) & unlikely(index < -size))) {
            PyErr_Format(PyExc_IndexError, "string index out of range");
            return -1;
        }
    }
    if (index < 0)
        index += PyBytes_GET_SIZE(bytes);
    return PyBytes_AS_STRING(bytes)[index];
}
