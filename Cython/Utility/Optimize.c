/////////////// append.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyObject_Append(PyObject* L, PyObject* x) {
    if (likely(PyList_CheckExact(L))) {
        if (PyList_Append(L, x) < 0) return NULL;
        Py_INCREF(Py_None);
        return Py_None; /* this is just to have an accurate signature */
    }
    else {
        PyObject *r, *m;
        m = __Pyx_GetAttrString(L, "append");
        if (!m) return NULL;
        r = PyObject_CallFunctionObjArgs(m, x, NULL);
        Py_DECREF(m);
        return r;
    }
}


/////////////// pop.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyObject_Pop(PyObject* L) {
#if PY_VERSION_HEX >= 0x02040000
    if (likely(PyList_CheckExact(L))
        /* Check that both the size is positive and no reallocation shrinking needs to be done. */
        && likely(PyList_GET_SIZE(L) > (((PyListObject*)L)->allocated >> 1))) {
        Py_SIZE(L) -= 1;
        return PyList_GET_ITEM(L, PyList_GET_SIZE(L));
    }
#if PY_VERSION_HEX >= 0x02050000
    else if (Py_TYPE(L) == (&PySet_Type)) {
        return PySet_Pop(L);
    }
#endif
#endif
    return PyObject_CallMethod(L, (char*)"pop", NULL);
}


/////////////// pop_index.proto ///////////////

static PyObject* __Pyx_PyObject_PopIndex(PyObject* L, Py_ssize_t ix) {
    PyObject *r, *m, *t, *py_ix;
#if PY_VERSION_HEX >= 0x02040000
    if (likely(PyList_CheckExact(L))) {
        Py_ssize_t size = PyList_GET_SIZE(L);
        if (likely(size > (((PyListObject*)L)->allocated >> 1))) {
            if (ix < 0) {
                ix += size;
            }
            if (likely(0 <= ix && ix < size)) {
                PyObject* v = PyList_GET_ITEM(L, ix);
                Py_SIZE(L) -= 1;
                size -= 1;
                memmove(&PyList_GET_ITEM(L, ix), &PyList_GET_ITEM(L, ix+1), (size-ix)*sizeof(PyObject*));
                return v;
            }
        }
    }
#endif
    py_ix = t = NULL;
    m = __Pyx_GetAttrString(L, "pop");
    if (!m) goto bad;
    py_ix = PyInt_FromSsize_t(ix);
    if (!py_ix) goto bad;
    t = PyTuple_New(1);
    if (!t) goto bad;
    PyTuple_SET_ITEM(t, 0, py_ix);
    py_ix = NULL;
    r = PyObject_CallObject(m, t);
    Py_DECREF(m);
    Py_DECREF(t);
    return r;
bad:
    Py_XDECREF(m);
    Py_XDECREF(t);
    Py_XDECREF(py_ix);
    return NULL;
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
        int result;
        Py_ssize_t i;
        for (i = 0; i < PyTuple_GET_SIZE(substr); i++) {
            result = PyUnicode_Tailmatch(s, PyTuple_GET_ITEM(substr, i),
                                         start, end, direction);
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
        int result;
        Py_ssize_t i;
        for (i = 0; i < PyTuple_GET_SIZE(substr); i++) {
            result = __Pyx_PyBytes_SingleTailmatch(self, PyTuple_GET_ITEM(substr, i),
                                                   start, end, direction);
            if (result) {
                return result;
            }
        }
        return 0;
    }
    
    return __Pyx_PyBytes_SingleTailmatch(self, substr, start, end, direction);
}


/////////////// bytes_index.proto ///////////////

static CYTHON_INLINE char __Pyx_PyBytes_GetItemInt(PyObject* bytes, Py_ssize_t index, int check_bounds) {
    if (check_bounds) {
        if (unlikely(index >= PyBytes_GET_SIZE(bytes)) |
            ((index < 0) & unlikely(index < -PyBytes_GET_SIZE(bytes)))) {
            PyErr_Format(PyExc_IndexError, "string index out of range");
            return -1;
        }
    }
    if (index < 0)
        index += PyBytes_GET_SIZE(bytes);
    return PyBytes_AS_STRING(bytes)[index];
}


/////////////// dict_getitem_default.proto ///////////////

static PyObject* __Pyx_PyDict_GetItemDefault(PyObject* d, PyObject* key, PyObject* default_value) {
    PyObject* value;
#if PY_MAJOR_VERSION >= 3
    value = PyDict_GetItemWithError(d, key);
    if (unlikely(!value)) {
        if (unlikely(PyErr_Occurred()))
            return NULL;
        value = default_value;
    }
    Py_INCREF(value);
#else
    if (PyString_CheckExact(key) || PyUnicode_CheckExact(key) || PyInt_CheckExact(key)) {
        /* these presumably have safe hash functions */
        value = PyDict_GetItem(d, key);
        if (unlikely(!value)) {
            value = default_value;
        }
        Py_INCREF(value);
    } else {
        PyObject *m;
        m = __Pyx_GetAttrString(d, "get");
        if (!m) return NULL;
        value = PyObject_CallFunctionObjArgs(m, key,
                                             (default_value == Py_None) ? NULL : default_value, NULL);
        Py_DECREF(m);
    }
#endif
    return value;
}


/////////////// dict_setdefault.proto ///////////////

static PyObject *__Pyx_PyDict_SetDefault(PyObject *d, PyObject *key, PyObject *default_value) {
    PyObject* value;
#if PY_MAJOR_VERSION >= 3
    value = PyDict_GetItemWithError(d, key);
    if (unlikely(!value)) {
        if (unlikely(PyErr_Occurred()))
            return NULL;
        if (unlikely(PyDict_SetItem(d, key, default_value) == -1))
            return NULL;
        value = default_value;
    }
    Py_INCREF(value);
#else
    if (PyString_CheckExact(key) || PyUnicode_CheckExact(key) || PyInt_CheckExact(key)) {
        /* these presumably have safe hash functions */
        value = PyDict_GetItem(d, key);
        if (unlikely(!value)) {
            if (unlikely(PyDict_SetItem(d, key, default_value) == -1))
                return NULL;
            value = default_value;
        }
        Py_INCREF(value);
    } else {
        PyObject *m;
        m = __Pyx_GetAttrString(d, "setdefault");
        if (!m) return NULL;
        value = PyObject_CallFunctionObjArgs(m, key, default_value, NULL);
        Py_DECREF(m);
    }
#endif
    return value;
}


/////////////// py_dict_clear.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyDict_Clear(PyObject* d) {
    PyDict_Clear(d);
    Py_INCREF(Py_None);
    return Py_None;
}


/////////////// pyobject_as_double.proto ///////////////

static double __Pyx__PyObject_AsDouble(PyObject* obj); /* proto */

#define __Pyx_PyObject_AsDouble(obj) \
((likely(PyFloat_CheckExact(obj))) ? \
 PyFloat_AS_DOUBLE(obj) : __Pyx__PyObject_AsDouble(obj))

/////////////// pyobject_as_double ///////////////

static double __Pyx__PyObject_AsDouble(PyObject* obj) {
    PyObject* float_value;
    if (Py_TYPE(obj)->tp_as_number && Py_TYPE(obj)->tp_as_number->nb_float) {
        return PyFloat_AsDouble(obj);
    } else if (PyUnicode_CheckExact(obj) || PyBytes_CheckExact(obj)) {
#if PY_MAJOR_VERSION >= 3
        float_value = PyFloat_FromString(obj);
#else
        float_value = PyFloat_FromString(obj, 0);
#endif
    } else {
        PyObject* args = PyTuple_New(1);
        if (unlikely(!args)) goto bad;
        PyTuple_SET_ITEM(args, 0, obj);
        float_value = PyObject_Call((PyObject*)&PyFloat_Type, args, 0);
        PyTuple_SET_ITEM(args, 0, 0);
        Py_DECREF(args);
    }
    if (likely(float_value)) {
        double value = PyFloat_AS_DOUBLE(float_value);
        Py_DECREF(float_value);
        return value;
    }
bad:
    return (double)-1;
}
