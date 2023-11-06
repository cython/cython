/*
 * Optional optimisations of built-in functions and methods.
 *
 * Required replacements of builtins are in Builtins.c.
 *
 * General object operations and protocols are in ObjectHandling.c.
 */

/////////////// append.proto ///////////////

static CYTHON_INLINE int __Pyx_PyObject_Append(PyObject* L, PyObject* x); /*proto*/

/////////////// append ///////////////
//@requires: ListAppend
//@requires: ObjectHandling.c::PyObjectCallMethod1

static CYTHON_INLINE int __Pyx_PyObject_Append(PyObject* L, PyObject* x) {
    if (likely(PyList_CheckExact(L))) {
        if (unlikely(__Pyx_PyList_Append(L, x) < 0)) return -1;
    } else {
        PyObject* retval = __Pyx_PyObject_CallMethod1(L, PYIDENT("append"), x);
        if (unlikely(!retval))
            return -1;
        Py_DECREF(retval);
    }
    return 0;
}

/////////////// ListAppend.proto ///////////////

#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static CYTHON_INLINE int __Pyx_PyList_Append(PyObject* list, PyObject* x) {
    PyListObject* L = (PyListObject*) list;
    Py_ssize_t len = Py_SIZE(list);
    if (likely(L->allocated > len) & likely(len > (L->allocated >> 1))) {
        Py_INCREF(x);
        #if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000
        // In Py3.13a1, PyList_SET_ITEM() checks that the end index is lower than the current size.
        // However, extending the size *before* setting the value would not be correct,
        // so we cannot call PyList_SET_ITEM().
        L->ob_item[len] = x;
        #else
        PyList_SET_ITEM(list, len, x);
        #endif
        __Pyx_SET_SIZE(list, len + 1);
        return 0;
    }
    return PyList_Append(list, x);
}
#else
#define __Pyx_PyList_Append(L,x) PyList_Append(L,x)
#endif

/////////////// ListCompAppend.proto ///////////////

#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static CYTHON_INLINE int __Pyx_ListComp_Append(PyObject* list, PyObject* x) {
    PyListObject* L = (PyListObject*) list;
    Py_ssize_t len = Py_SIZE(list);
    if (likely(L->allocated > len)) {
        Py_INCREF(x);
        #if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX >= 0x030d0000
        // In Py3.13a1, PyList_SET_ITEM() checks that the end index is lower than the current size.
        // However, extending the size *before* setting the value would not be correct,
        // so we cannot call PyList_SET_ITEM().
        L->ob_item[len] = x;
        #else
        PyList_SET_ITEM(list, len, x);
        #endif
        __Pyx_SET_SIZE(list, len + 1);
        return 0;
    }
    return PyList_Append(list, x);
}
#else
#define __Pyx_ListComp_Append(L,x) PyList_Append(L,x)
#endif

//////////////////// ListExtend.proto ////////////////////

static CYTHON_INLINE int __Pyx_PyList_Extend(PyObject* L, PyObject* v) {
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030d0000
    PyObject* none = _PyList_Extend((PyListObject*)L, v);
    if (unlikely(!none))
        return -1;
    Py_DECREF(none);
    return 0;
#else
    return PyList_SetSlice(L, PY_SSIZE_T_MAX, PY_SSIZE_T_MAX, v);
#endif
}

/////////////// pop.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx__PyObject_Pop(PyObject* L); /*proto*/

#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static CYTHON_INLINE PyObject* __Pyx_PyList_Pop(PyObject* L); /*proto*/
#define __Pyx_PyObject_Pop(L) (likely(PyList_CheckExact(L)) ? \
    __Pyx_PyList_Pop(L) : __Pyx__PyObject_Pop(L))

#else
#define __Pyx_PyList_Pop(L)  __Pyx__PyObject_Pop(L)
#define __Pyx_PyObject_Pop(L)  __Pyx__PyObject_Pop(L)
#endif

/////////////// pop ///////////////
//@requires: ObjectHandling.c::PyObjectCallMethod0

static CYTHON_INLINE PyObject* __Pyx__PyObject_Pop(PyObject* L) {
    if (__Pyx_IS_TYPE(L, &PySet_Type)) {
        return PySet_Pop(L);
    }
    return __Pyx_PyObject_CallMethod0(L, PYIDENT("pop"));
}

#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static CYTHON_INLINE PyObject* __Pyx_PyList_Pop(PyObject* L) {
    /* Check that both the size is positive and no reallocation shrinking needs to be done. */
    if (likely(PyList_GET_SIZE(L) > (((PyListObject*)L)->allocated >> 1))) {
        __Pyx_SET_SIZE(L, Py_SIZE(L) - 1);
        return PyList_GET_ITEM(L, PyList_GET_SIZE(L));
    }
    return CALL_UNBOUND_METHOD(PyList_Type, "pop", L);
}
#endif


/////////////// pop_index.proto ///////////////

static PyObject* __Pyx__PyObject_PopNewIndex(PyObject* L, PyObject* py_ix); /*proto*/
static PyObject* __Pyx__PyObject_PopIndex(PyObject* L, PyObject* py_ix); /*proto*/

#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static PyObject* __Pyx__PyList_PopIndex(PyObject* L, PyObject* py_ix, Py_ssize_t ix); /*proto*/

#define __Pyx_PyObject_PopIndex(L, py_ix, ix, is_signed, type, to_py_func) ( \
    (likely(PyList_CheckExact(L) && __Pyx_fits_Py_ssize_t(ix, type, is_signed))) ? \
        __Pyx__PyList_PopIndex(L, py_ix, ix) : ( \
        (unlikely((py_ix) == Py_None)) ? __Pyx__PyObject_PopNewIndex(L, to_py_func(ix)) : \
            __Pyx__PyObject_PopIndex(L, py_ix)))

#define __Pyx_PyList_PopIndex(L, py_ix, ix, is_signed, type, to_py_func) ( \
    __Pyx_fits_Py_ssize_t(ix, type, is_signed) ? \
        __Pyx__PyList_PopIndex(L, py_ix, ix) : ( \
        (unlikely((py_ix) == Py_None)) ? __Pyx__PyObject_PopNewIndex(L, to_py_func(ix)) : \
            __Pyx__PyObject_PopIndex(L, py_ix)))

#else

#define __Pyx_PyList_PopIndex(L, py_ix, ix, is_signed, type, to_py_func) \
    __Pyx_PyObject_PopIndex(L, py_ix, ix, is_signed, type, to_py_func)

#define __Pyx_PyObject_PopIndex(L, py_ix, ix, is_signed, type, to_py_func) ( \
    (unlikely((py_ix) == Py_None)) ? __Pyx__PyObject_PopNewIndex(L, to_py_func(ix)) : \
        __Pyx__PyObject_PopIndex(L, py_ix))
#endif

/////////////// pop_index ///////////////
//@requires: ObjectHandling.c::PyObjectCallMethod1

static PyObject* __Pyx__PyObject_PopNewIndex(PyObject* L, PyObject* py_ix) {
    PyObject *r;
    if (unlikely(!py_ix)) return NULL;
    r = __Pyx__PyObject_PopIndex(L, py_ix);
    Py_DECREF(py_ix);
    return r;
}

static PyObject* __Pyx__PyObject_PopIndex(PyObject* L, PyObject* py_ix) {
    return __Pyx_PyObject_CallMethod1(L, PYIDENT("pop"), py_ix);
}

#if CYTHON_USE_PYLIST_INTERNALS && CYTHON_ASSUME_SAFE_MACROS
static PyObject* __Pyx__PyList_PopIndex(PyObject* L, PyObject* py_ix, Py_ssize_t ix) {
    Py_ssize_t size = PyList_GET_SIZE(L);
    if (likely(size > (((PyListObject*)L)->allocated >> 1))) {
        Py_ssize_t cix = ix;
        if (cix < 0) {
            cix += size;
        }
        if (likely(__Pyx_is_valid_index(cix, size))) {
            PyObject* v = PyList_GET_ITEM(L, cix);
            __Pyx_SET_SIZE(L, Py_SIZE(L) - 1);
            size -= 1;
            memmove(&PyList_GET_ITEM(L, cix), &PyList_GET_ITEM(L, cix+1), (size_t)(size-cix)*sizeof(PyObject*));
            return v;
        }
    }
    if (py_ix == Py_None) {
        return __Pyx__PyObject_PopNewIndex(L, PyInt_FromSsize_t(ix));
    } else {
        return __Pyx__PyObject_PopIndex(L, py_ix);
    }
}
#endif


/////////////// dict_getitem_default.proto ///////////////

static PyObject* __Pyx_PyDict_GetItemDefault(PyObject* d, PyObject* key, PyObject* default_value); /*proto*/

/////////////// dict_getitem_default ///////////////

static PyObject* __Pyx_PyDict_GetItemDefault(PyObject* d, PyObject* key, PyObject* default_value) {
    PyObject* value;
#if PY_MAJOR_VERSION >= 3 && (!CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM >= 0x07020000)
    value = PyDict_GetItemWithError(d, key);
    if (unlikely(!value)) {
        if (unlikely(PyErr_Occurred()))
            return NULL;
        value = default_value;
    }
    Py_INCREF(value);
    // avoid C compiler warning about unused utility functions
    if ((1));
#else
    if (PyString_CheckExact(key) || PyUnicode_CheckExact(key) || PyInt_CheckExact(key)) {
        /* these presumably have safe hash functions */
        value = PyDict_GetItem(d, key);
        if (unlikely(!value)) {
            value = default_value;
        }
        Py_INCREF(value);
    }
#endif
    else {
        if (default_value == Py_None)
            value = CALL_UNBOUND_METHOD(PyDict_Type, "get", d, key);
        else
            value = CALL_UNBOUND_METHOD(PyDict_Type, "get", d, key, default_value);
    }
    return value;
}


/////////////// dict_setdefault.proto ///////////////

static CYTHON_INLINE PyObject *__Pyx_PyDict_SetDefault(PyObject *d, PyObject *key, PyObject *default_value, int is_safe_type); /*proto*/

/////////////// dict_setdefault ///////////////

static CYTHON_INLINE PyObject *__Pyx_PyDict_SetDefault(PyObject *d, PyObject *key, PyObject *default_value,
                                                       int is_safe_type) {
    PyObject* value;
    CYTHON_MAYBE_UNUSED_VAR(is_safe_type);
#if PY_VERSION_HEX >= 0x030400A0
    // we keep the method call at the end to avoid "unused" C compiler warnings
    if ((1)) {
        value = PyDict_SetDefault(d, key, default_value);
        if (unlikely(!value)) return NULL;
        Py_INCREF(value);
#else
    if (is_safe_type == 1 || (is_safe_type == -1 &&
        /* the following builtins presumably have repeatably safe and fast hash functions */
#if PY_MAJOR_VERSION >= 3 && (!CYTHON_COMPILING_IN_PYPY || PYPY_VERSION_NUM >= 0x07020000)
            (PyUnicode_CheckExact(key) || PyString_CheckExact(key) || PyLong_CheckExact(key)))) {
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
            (PyString_CheckExact(key) || PyUnicode_CheckExact(key) || PyInt_CheckExact(key) || PyLong_CheckExact(key)))) {
        value = PyDict_GetItem(d, key);
        if (unlikely(!value)) {
            if (unlikely(PyDict_SetItem(d, key, default_value) == -1))
                return NULL;
            value = default_value;
        }
        Py_INCREF(value);
#endif
#endif
    } else {
        value = CALL_UNBOUND_METHOD(PyDict_Type, "setdefault", d, key, default_value);
    }
    return value;
}


/////////////// py_dict_clear.proto ///////////////

#define __Pyx_PyDict_Clear(d) (PyDict_Clear(d), 0)


/////////////// py_dict_pop.proto ///////////////

static CYTHON_INLINE PyObject *__Pyx_PyDict_Pop(PyObject *d, PyObject *key, PyObject *default_value); /*proto*/

/////////////// py_dict_pop ///////////////

static CYTHON_INLINE PyObject *__Pyx_PyDict_Pop(PyObject *d, PyObject *key, PyObject *default_value) {
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX > 0x030600B3 & PY_VERSION_HEX < 0x030d0000
    if ((1)) {
        return _PyDict_Pop(d, key, default_value);
    } else
    // avoid "function unused" warnings
#endif
    if (default_value) {
        return CALL_UNBOUND_METHOD(PyDict_Type, "pop", d, key, default_value);
    } else {
        return CALL_UNBOUND_METHOD(PyDict_Type, "pop", d, key);
    }
}


/////////////// dict_iter.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_dict_iterator(PyObject* dict, int is_dict, PyObject* method_name,
                                                   Py_ssize_t* p_orig_length, int* p_is_dict);
static CYTHON_INLINE int __Pyx_dict_iter_next(PyObject* dict_or_iter, Py_ssize_t orig_length, Py_ssize_t* ppos,
                                              PyObject** pkey, PyObject** pvalue, PyObject** pitem, int is_dict);

/////////////// dict_iter ///////////////
//@requires: ObjectHandling.c::UnpackTuple2
//@requires: ObjectHandling.c::IterFinish
//@requires: ObjectHandling.c::PyObjectCallMethod0

#if CYTHON_COMPILING_IN_PYPY && PY_MAJOR_VERSION >= 3
#include <string.h>
#endif

static CYTHON_INLINE PyObject* __Pyx_dict_iterator(PyObject* iterable, int is_dict, PyObject* method_name,
                                                   Py_ssize_t* p_orig_length, int* p_source_is_dict) {
    is_dict = is_dict || likely(PyDict_CheckExact(iterable));
    *p_source_is_dict = is_dict;
    if (is_dict) {
#if !CYTHON_COMPILING_IN_PYPY
        *p_orig_length = PyDict_Size(iterable);
        Py_INCREF(iterable);
        return iterable;
#elif PY_MAJOR_VERSION >= 3
        // On PyPy3, we need to translate manually a few method names.
        // This logic is not needed on CPython thanks to the fast case above.
        static PyObject *py_items = NULL, *py_keys = NULL, *py_values = NULL;
        PyObject **pp = NULL;
        if (method_name) {
            const char *name = PyUnicode_AsUTF8(method_name);
            if (strcmp(name, "iteritems") == 0) pp = &py_items;
            else if (strcmp(name, "iterkeys") == 0) pp = &py_keys;
            else if (strcmp(name, "itervalues") == 0) pp = &py_values;
            if (pp) {
                if (!*pp) {
                    *pp = PyUnicode_FromString(name + 4);
                    if (!*pp)
                        return NULL;
                }
                method_name = *pp;
            }
        }
#endif
    }
    *p_orig_length = 0;
    if (method_name) {
        PyObject* iter;
        iterable = __Pyx_PyObject_CallMethod0(iterable, method_name);
        if (!iterable)
            return NULL;
#if !CYTHON_COMPILING_IN_PYPY
        if (PyTuple_CheckExact(iterable) || PyList_CheckExact(iterable))
            return iterable;
#endif
        iter = PyObject_GetIter(iterable);
        Py_DECREF(iterable);
        return iter;
    }
    return PyObject_GetIter(iterable);
}

static CYTHON_INLINE int __Pyx_dict_iter_next(
        PyObject* iter_obj, CYTHON_NCP_UNUSED Py_ssize_t orig_length, CYTHON_NCP_UNUSED Py_ssize_t* ppos,
        PyObject** pkey, PyObject** pvalue, PyObject** pitem, int source_is_dict) {
    PyObject* next_item;
#if !CYTHON_COMPILING_IN_PYPY
    if (source_is_dict) {
        PyObject *key, *value;
        if (unlikely(orig_length != PyDict_Size(iter_obj))) {
            PyErr_SetString(PyExc_RuntimeError, "dictionary changed size during iteration");
            return -1;
        }
        if (unlikely(!PyDict_Next(iter_obj, ppos, &key, &value))) {
            return 0;
        }
        if (pitem) {
            PyObject* tuple = PyTuple_New(2);
            if (unlikely(!tuple)) {
                return -1;
            }
            Py_INCREF(key);
            Py_INCREF(value);
            PyTuple_SET_ITEM(tuple, 0, key);
            PyTuple_SET_ITEM(tuple, 1, value);
            *pitem = tuple;
        } else {
            if (pkey) {
                Py_INCREF(key);
                *pkey = key;
            }
            if (pvalue) {
                Py_INCREF(value);
                *pvalue = value;
            }
        }
        return 1;
    } else if (PyTuple_CheckExact(iter_obj)) {
        Py_ssize_t pos = *ppos;
        if (unlikely(pos >= PyTuple_GET_SIZE(iter_obj))) return 0;
        *ppos = pos + 1;
        next_item = PyTuple_GET_ITEM(iter_obj, pos);
        Py_INCREF(next_item);
    } else if (PyList_CheckExact(iter_obj)) {
        Py_ssize_t pos = *ppos;
        if (unlikely(pos >= PyList_GET_SIZE(iter_obj))) return 0;
        *ppos = pos + 1;
        next_item = PyList_GET_ITEM(iter_obj, pos);
        Py_INCREF(next_item);
    } else
#endif
    {
        next_item = PyIter_Next(iter_obj);
        if (unlikely(!next_item)) {
            return __Pyx_IterFinish();
        }
    }
    if (pitem) {
        *pitem = next_item;
    } else if (pkey && pvalue) {
        if (__Pyx_unpack_tuple2(next_item, pkey, pvalue, source_is_dict, source_is_dict, 1))
            return -1;
    } else if (pkey) {
        *pkey = next_item;
    } else {
        *pvalue = next_item;
    }
    return 1;
}


/////////////// set_iter.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_set_iterator(PyObject* iterable, int is_set,
                                                  Py_ssize_t* p_orig_length, int* p_source_is_set); /*proto*/
static CYTHON_INLINE int __Pyx_set_iter_next(
        PyObject* iter_obj, Py_ssize_t orig_length,
        Py_ssize_t* ppos, PyObject **value,
        int source_is_set); /*proto*/

/////////////// set_iter ///////////////
//@requires: ObjectHandling.c::IterFinish

static CYTHON_INLINE PyObject* __Pyx_set_iterator(PyObject* iterable, int is_set,
                                                  Py_ssize_t* p_orig_length, int* p_source_is_set) {
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030d0000
    is_set = is_set || likely(PySet_CheckExact(iterable) || PyFrozenSet_CheckExact(iterable));
    *p_source_is_set = is_set;
    if (likely(is_set)) {
        *p_orig_length = PySet_Size(iterable);
        Py_INCREF(iterable);
        return iterable;
    }
#else
    CYTHON_UNUSED_VAR(is_set);
    *p_source_is_set = 0;
#endif
    *p_orig_length = 0;
    return PyObject_GetIter(iterable);
}

static CYTHON_INLINE int __Pyx_set_iter_next(
        PyObject* iter_obj, Py_ssize_t orig_length,
        Py_ssize_t* ppos, PyObject **value,
        int source_is_set) {
    if (!CYTHON_COMPILING_IN_CPYTHON || PY_VERSION_HEX >= 0x030d0000 || unlikely(!source_is_set)) {
        *value = PyIter_Next(iter_obj);
        if (unlikely(!*value)) {
            return __Pyx_IterFinish();
        }
        CYTHON_UNUSED_VAR(orig_length);
        CYTHON_UNUSED_VAR(ppos);
        return 1;
    }
#if CYTHON_COMPILING_IN_CPYTHON && PY_VERSION_HEX < 0x030d0000
    if (unlikely(PySet_GET_SIZE(iter_obj) != orig_length)) {
        PyErr_SetString(
            PyExc_RuntimeError,
            "set changed size during iteration");
        return -1;
    }
    {
        Py_hash_t hash;
        int ret = _PySet_NextEntry(iter_obj, ppos, value, &hash);
        // CPython does not raise errors here, only if !isinstance(iter_obj, set/frozenset)
        assert (ret != -1);
        if (likely(ret)) {
            Py_INCREF(*value);
            return 1;
        }
    }
#endif
    return 0;
}

/////////////// py_set_discard_unhashable ///////////////
//@requires: Builtins.c::pyfrozenset_new

static int __Pyx_PySet_DiscardUnhashable(PyObject *set, PyObject *key) {
    PyObject *tmpkey;
    int rv;

    if (likely(!PySet_Check(key) || !PyErr_ExceptionMatches(PyExc_TypeError)))
        return -1;
    PyErr_Clear();
    tmpkey = __Pyx_PyFrozenSet_New(key);
    if (tmpkey == NULL)
        return -1;
    rv = PySet_Discard(set, tmpkey);
    Py_DECREF(tmpkey);
    return rv;
}


/////////////// py_set_discard.proto ///////////////

static CYTHON_INLINE int __Pyx_PySet_Discard(PyObject *set, PyObject *key); /*proto*/

/////////////// py_set_discard ///////////////
//@requires: py_set_discard_unhashable

static CYTHON_INLINE int __Pyx_PySet_Discard(PyObject *set, PyObject *key) {
    int found = PySet_Discard(set, key);
    // Convert *key* to frozenset if necessary
    if (unlikely(found < 0)) {
        found = __Pyx_PySet_DiscardUnhashable(set, key);
    }
    // note: returns -1 on error, 0 (not found) or 1 (found) otherwise => error check for -1 or < 0 works
    return found;
}


/////////////// py_set_remove.proto ///////////////

static CYTHON_INLINE int __Pyx_PySet_Remove(PyObject *set, PyObject *key); /*proto*/

/////////////// py_set_remove ///////////////
//@requires: py_set_discard_unhashable

static int __Pyx_PySet_RemoveNotFound(PyObject *set, PyObject *key, int found) {
    // Convert *key* to frozenset if necessary
    if (unlikely(found < 0)) {
        found = __Pyx_PySet_DiscardUnhashable(set, key);
    }
    if (likely(found == 0)) {
        // Not found
        PyObject *tup;
        tup = PyTuple_Pack(1, key);
        if (!tup)
            return -1;
        PyErr_SetObject(PyExc_KeyError, tup);
        Py_DECREF(tup);
        return -1;
    }
    // note: returns -1 on error, 0 (not found) or 1 (found) otherwise => error check for -1 or < 0 works
    return found;
}

static CYTHON_INLINE int __Pyx_PySet_Remove(PyObject *set, PyObject *key) {
    int found = PySet_Discard(set, key);
    if (unlikely(found != 1)) {
        // note: returns -1 on error, 0 (not found) or 1 (found) otherwise => error check for -1 or < 0 works
        return __Pyx_PySet_RemoveNotFound(set, key, found);
    }
    return 0;
}


/////////////// unicode_iter.proto ///////////////

static CYTHON_INLINE int __Pyx_init_unicode_iteration(
    PyObject* ustring, Py_ssize_t *length, void** data, int *kind); /* proto */

/////////////// unicode_iter ///////////////

static CYTHON_INLINE int __Pyx_init_unicode_iteration(
    PyObject* ustring, Py_ssize_t *length, void** data, int *kind) {
#if CYTHON_COMPILING_IN_LIMITED_API
    // In the limited API we just point data to the unicode object
    *kind   = 0;
    *length = PyUnicode_GetLength(ustring);
    *data   = (void*)ustring;
#elif CYTHON_PEP393_ENABLED
    if (unlikely(__Pyx_PyUnicode_READY(ustring) < 0)) return -1;
    *kind   = PyUnicode_KIND(ustring);
    *length = PyUnicode_GET_LENGTH(ustring);
    *data   = PyUnicode_DATA(ustring);
#else
    *kind   = 0;
    *length = PyUnicode_GET_SIZE(ustring);
    *data   = (void*)PyUnicode_AS_UNICODE(ustring);
#endif
    return 0;
}

/////////////// pyobject_as_double.proto ///////////////

static double __Pyx__PyObject_AsDouble(PyObject* obj); /* proto */

#if CYTHON_COMPILING_IN_PYPY
#define __Pyx_PyObject_AsDouble(obj) \
(likely(PyFloat_CheckExact(obj)) ? PyFloat_AS_DOUBLE(obj) : \
 likely(PyInt_CheckExact(obj)) ? \
 PyFloat_AsDouble(obj) : __Pyx__PyObject_AsDouble(obj))
#else
#define __Pyx_PyObject_AsDouble(obj) \
((likely(PyFloat_CheckExact(obj))) ?  PyFloat_AS_DOUBLE(obj) : \
 likely(PyLong_CheckExact(obj)) ? \
 PyLong_AsDouble(obj) : __Pyx__PyObject_AsDouble(obj))
#endif

/////////////// pyobject_as_double ///////////////
//@requires: pybytes_as_double
//@requires: pyunicode_as_double
//@requires: ObjectHandling.c::PyObjectCallOneArg

static double __Pyx__PyObject_AsDouble(PyObject* obj) {
    if (PyUnicode_CheckExact(obj)) {
        return __Pyx_PyUnicode_AsDouble(obj);
    } else if (PyBytes_CheckExact(obj)) {
        return __Pyx_PyBytes_AsDouble(obj);
    } else if (PyByteArray_CheckExact(obj)) {
        return __Pyx_PyByteArray_AsDouble(obj);
    } else {
        PyObject* float_value;
#if !CYTHON_USE_TYPE_SLOTS
        float_value = PyNumber_Float(obj);  if ((0)) goto bad;
        // avoid "unused" warnings
        (void)__Pyx_PyObject_CallOneArg;
#else
        PyNumberMethods *nb = Py_TYPE(obj)->tp_as_number;
        if (likely(nb) && likely(nb->nb_float)) {
            float_value = nb->nb_float(obj);
            if (likely(float_value) && unlikely(!PyFloat_Check(float_value))) {
                __Pyx_TypeName float_value_type_name = __Pyx_PyType_GetName(Py_TYPE(float_value));
                PyErr_Format(PyExc_TypeError,
                    "__float__ returned non-float (type " __Pyx_FMT_TYPENAME ")",
                    float_value_type_name);
                __Pyx_DECREF_TypeName(float_value_type_name);
                Py_DECREF(float_value);
                goto bad;
            }
        } else {
            float_value = __Pyx_PyObject_CallOneArg((PyObject*)&PyFloat_Type, obj);
        }
#endif
        if (likely(float_value)) {
            double value = PyFloat_AS_DOUBLE(float_value);
            Py_DECREF(float_value);
            return value;
        }
    }
bad:
    return (double)-1;
}


/////////////// pystring_as_double.proto ///////////////
//@requires: pyunicode_as_double
//@requires: pybytes_as_double

static CYTHON_INLINE double __Pyx_PyString_AsDouble(PyObject *obj) {
    #if PY_MAJOR_VERSION >= 3
    (void)__Pyx_PyBytes_AsDouble;
    return __Pyx_PyUnicode_AsDouble(obj);
    #else
    (void)__Pyx_PyUnicode_AsDouble;
    return __Pyx_PyBytes_AsDouble(obj);
    #endif
}


/////////////// pyunicode_as_double.proto ///////////////

static CYTHON_INLINE double __Pyx_PyUnicode_AsDouble(PyObject *obj);/*proto*/

/////////////// pyunicode_as_double.proto ///////////////
//@requires: pybytes_as_double

#if PY_MAJOR_VERSION >= 3 && !CYTHON_COMPILING_IN_PYPY && CYTHON_ASSUME_SAFE_MACROS
static const char* __Pyx__PyUnicode_AsDouble_Copy(const void* data, const int kind, char* buffer, Py_ssize_t start, Py_ssize_t end) {
    int last_was_punctuation;
    Py_ssize_t i;
    // number must not start with punctuation
    last_was_punctuation = 1;
    for (i=start; i <= end; i++) {
        Py_UCS4 chr = PyUnicode_READ(kind, data, i);
        int is_punctuation = (chr == '_') | (chr == '.');
        *buffer = (char)chr;
        // reject sequences of '_' and '.'
        buffer += (chr != '_');
        if (unlikely(chr > 127)) goto parse_failure;
        if (unlikely(last_was_punctuation & is_punctuation)) goto parse_failure;
        last_was_punctuation = is_punctuation;
    }
    if (unlikely(last_was_punctuation)) goto parse_failure;
    *buffer = '\0';
    return buffer;

parse_failure:
    return NULL;
}

static double __Pyx__PyUnicode_AsDouble_inf_nan(const void* data, int kind, Py_ssize_t start, Py_ssize_t length) {
    int matches = 1;
    Py_UCS4 chr;
    Py_UCS4 sign = PyUnicode_READ(kind, data, start);
    int is_signed = (sign == '-') | (sign == '+');
    start += is_signed;
    length -= is_signed;

    switch (PyUnicode_READ(kind, data, start)) {
        #ifdef Py_NAN
        case 'n':
        case 'N':
            if (unlikely(length != 3)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+1);
            matches &= (chr == 'a') | (chr == 'A');
            chr = PyUnicode_READ(kind, data, start+2);
            matches &= (chr == 'n') | (chr == 'N');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_NAN : Py_NAN;
        #endif
        case 'i':
        case 'I':
            if (unlikely(length < 3)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+1);
            matches &= (chr == 'n') | (chr == 'N');
            chr = PyUnicode_READ(kind, data, start+2);
            matches &= (chr == 'f') | (chr == 'F');
            if (likely(length == 3 && matches))
                return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
            if (unlikely(length != 8)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+3);
            matches &= (chr == 'i') | (chr == 'I');
            chr = PyUnicode_READ(kind, data, start+4);
            matches &= (chr == 'n') | (chr == 'N');
            chr = PyUnicode_READ(kind, data, start+5);
            matches &= (chr == 'i') | (chr == 'I');
            chr = PyUnicode_READ(kind, data, start+6);
            matches &= (chr == 't') | (chr == 'T');
            chr = PyUnicode_READ(kind, data, start+7);
            matches &= (chr == 'y') | (chr == 'Y');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
        case '.': case '0': case '1': case '2': case '3': case '4': case '5': case '6': case '7': case '8': case '9':
            break;
        default:
            goto parse_failure;
    }
    return 0.0;
parse_failure:
    return -1.0;
}

static double __Pyx_PyUnicode_AsDouble_WithSpaces(PyObject *obj) {
    double value;
    const char *last;
    char *end;
    Py_ssize_t start, length = PyUnicode_GET_LENGTH(obj);
    const int kind = PyUnicode_KIND(obj);
    const void* data = PyUnicode_DATA(obj);

    // strip spaces at start and end
    start = 0;
    while (Py_UNICODE_ISSPACE(PyUnicode_READ(kind, data, start)))
        start++;
    while (start < length - 1 && Py_UNICODE_ISSPACE(PyUnicode_READ(kind, data, length - 1)))
        length--;
    length -= start;
    if (unlikely(length <= 0)) goto fallback;

    // parse NaN / inf
    value = __Pyx__PyUnicode_AsDouble_inf_nan(data, kind, start, length);
    if (unlikely(value == -1.0)) goto fallback;
    if (value != 0.0) return value;

    if (length < 40) {
        char number[40];
        last = __Pyx__PyUnicode_AsDouble_Copy(data, kind, number, start, start + length);
        if (unlikely(!last)) goto fallback;
        value = PyOS_string_to_double(number, &end, NULL);
    } else {
        char *number = (char*) PyMem_Malloc((length + 1) * sizeof(char));
        if (unlikely(!number)) goto fallback;
        last = __Pyx__PyUnicode_AsDouble_Copy(data, kind, number, start, start + length);
        if (unlikely(!last)) {
            PyMem_Free(number);
            goto fallback;
        }
        value = PyOS_string_to_double(number, &end, NULL);
        PyMem_Free(number);
    }
    if (likely(end == last) || (value == (double)-1 && PyErr_Occurred())) {
        return value;
    }
fallback:
    return __Pyx_SlowPyString_AsDouble(obj);
}
#endif

static CYTHON_INLINE double __Pyx_PyUnicode_AsDouble(PyObject *obj) {
    // Currently not optimised for Py2.7.
#if PY_MAJOR_VERSION >= 3 && !CYTHON_COMPILING_IN_PYPY && CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(__Pyx_PyUnicode_READY(obj) == -1))
        return (double)-1;
    if (likely(PyUnicode_IS_ASCII(obj))) {
        const char *s;
        Py_ssize_t length;
        s = PyUnicode_AsUTF8AndSize(obj, &length);
        return __Pyx__PyBytes_AsDouble(obj, s, length);
    }
    return __Pyx_PyUnicode_AsDouble_WithSpaces(obj);
#else
    return __Pyx_SlowPyString_AsDouble(obj);
#endif
}


/////////////// pybytes_as_double.proto ///////////////

static double __Pyx_SlowPyString_AsDouble(PyObject *obj);/*proto*/
static double __Pyx__PyBytes_AsDouble(PyObject *obj, const char* start, Py_ssize_t length);/*proto*/

static CYTHON_INLINE double __Pyx_PyBytes_AsDouble(PyObject *obj) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS
    as_c_string = PyBytes_AS_STRING(obj);
    size = PyBytes_GET_SIZE(obj);
#else
    if (PyBytes_AsStringAndSize(obj, &as_c_string, &size) < 0) {
        return (double)-1;
    }
#endif
    return __Pyx__PyBytes_AsDouble(obj, as_c_string, size);
}
static CYTHON_INLINE double __Pyx_PyByteArray_AsDouble(PyObject *obj) {
    char* as_c_string;
    Py_ssize_t size;
#if CYTHON_ASSUME_SAFE_MACROS
    as_c_string = PyByteArray_AS_STRING(obj);
    size = PyByteArray_GET_SIZE(obj);
#else
    as_c_string = PyByteArray_AsString(obj);
    if (as_c_string == NULL) {
        return (double)-1;
    }
    size = PyByteArray_Size(obj);
#endif
    return __Pyx__PyBytes_AsDouble(obj, as_c_string, size);
}


/////////////// pybytes_as_double ///////////////

static double __Pyx_SlowPyString_AsDouble(PyObject *obj) {
    PyObject *float_value;
#if PY_MAJOR_VERSION >= 3
    float_value = PyFloat_FromString(obj);
#else
    float_value = PyFloat_FromString(obj, 0);
#endif
    if (likely(float_value)) {
#if CYTHON_ASSUME_SAFE_MACROS
        double value = PyFloat_AS_DOUBLE(float_value);
#else
        double value = PyFloat_AsDouble(float_value);
#endif
        Py_DECREF(float_value);
        return value;
    }
    return (double)-1;
}

static const char* __Pyx__PyBytes_AsDouble_Copy(const char* start, char* buffer, Py_ssize_t length) {
    // number must not start with punctuation
    int last_was_punctuation = 1;
    Py_ssize_t i;
    for (i=0; i < length; i++) {
        char chr = start[i];
        int is_punctuation = (chr == '_') | (chr == '.') | (chr == 'e') | (chr == 'E');
        *buffer = chr;
        buffer += (chr != '_');
        // reject sequences of '_' and '.'
        if (unlikely(last_was_punctuation & is_punctuation)) goto parse_failure;
        last_was_punctuation = is_punctuation;
    }
    if (unlikely(last_was_punctuation)) goto parse_failure;
    *buffer = '\0';
    return buffer;

parse_failure:
    return NULL;
}

static double __Pyx__PyBytes_AsDouble_inf_nan(const char* start, Py_ssize_t length) {
    int matches = 1;
    char sign = start[0];
    int is_signed = (sign == '+') | (sign == '-');
    start += is_signed;
    length -= is_signed;

    switch (start[0]) {
        #ifdef Py_NAN
        case 'n':
        case 'N':
            if (unlikely(length != 3)) goto parse_failure;
            matches &= (start[1] == 'a' || start[1] == 'A');
            matches &= (start[2] == 'n' || start[2] == 'N');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_NAN : Py_NAN;
        #endif
        case 'i':
        case 'I':
            if (unlikely(length < 3)) goto parse_failure;
            matches &= (start[1] == 'n' || start[1] == 'N');
            matches &= (start[2] == 'f' || start[2] == 'F');
            if (likely(length == 3 && matches))
                return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
            if (unlikely(length != 8)) goto parse_failure;
            matches &= (start[3] == 'i' || start[3] == 'I');
            matches &= (start[4] == 'n' || start[4] == 'N');
            matches &= (start[5] == 'i' || start[5] == 'I');
            matches &= (start[6] == 't' || start[6] == 'T');
            matches &= (start[7] == 'y' || start[7] == 'Y');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
        case '.': case '0': case '1': case '2': case '3': case '4': case '5': case '6': case '7': case '8': case '9':
            break;
        default:
            goto parse_failure;
    }
    return 0.0;
parse_failure:
    return -1.0;
}

static CYTHON_INLINE int __Pyx__PyBytes_AsDouble_IsSpace(char ch) {
    // see Py_ISSPACE() in CPython
    // https://github.com/python/cpython/blob/master/Python/pyctype.c
    return (ch == 0x20) | !((ch < 0x9) | (ch > 0xd));
}

CYTHON_UNUSED static double __Pyx__PyBytes_AsDouble(PyObject *obj, const char* start, Py_ssize_t length) {
    double value;
    Py_ssize_t i, digits;
    const char *last = start + length;
    char *end;

    // strip spaces at start and end
    while (__Pyx__PyBytes_AsDouble_IsSpace(*start))
        start++;
    while (start < last - 1 && __Pyx__PyBytes_AsDouble_IsSpace(last[-1]))
        last--;
    length = last - start;
    if (unlikely(length <= 0)) goto fallback;

    // parse NaN / inf
    value = __Pyx__PyBytes_AsDouble_inf_nan(start, length);
    if (unlikely(value == -1.0)) goto fallback;
    if (value != 0.0) return value;

    // look for underscores
    digits = 0;
    for (i=0; i < length; digits += start[i++] != '_');

    if (likely(digits == length)) {
        value = PyOS_string_to_double(start, &end, NULL);
    } else if (digits < 40) {
        char number[40];
        last = __Pyx__PyBytes_AsDouble_Copy(start, number, length);
        if (unlikely(!last)) goto fallback;
        value = PyOS_string_to_double(number, &end, NULL);
    } else {
        char *number = (char*) PyMem_Malloc((digits + 1) * sizeof(char));
        if (unlikely(!number)) goto fallback;
        last = __Pyx__PyBytes_AsDouble_Copy(start, number, length);
        if (unlikely(!last)) {
            PyMem_Free(number);
            goto fallback;
        }
        value = PyOS_string_to_double(number, &end, NULL);
        PyMem_Free(number);
    }
    if (likely(end == last) || (value == (double)-1 && PyErr_Occurred())) {
        return value;
    }
fallback:
    return __Pyx_SlowPyString_AsDouble(obj);
}


/////////////// PyNumberPow2.proto ///////////////

#define __Pyx_PyNumber_InPlacePowerOf2(a, b, c) __Pyx__PyNumber_PowerOf2(a, b, c, 1)
#define __Pyx_PyNumber_PowerOf2(a, b, c) __Pyx__PyNumber_PowerOf2(a, b, c, 0)

static PyObject* __Pyx__PyNumber_PowerOf2(PyObject *two, PyObject *exp, PyObject *none, int inplace); /*proto*/

/////////////// PyNumberPow2 ///////////////

static PyObject* __Pyx__PyNumber_PowerOf2(PyObject *two, PyObject *exp, PyObject *none, int inplace) {
// in CPython, 1<<N is substantially faster than 2**N
// see https://bugs.python.org/issue21420
#if !CYTHON_COMPILING_IN_PYPY
    Py_ssize_t shiftby;
#if PY_MAJOR_VERSION < 3
    if (likely(PyInt_CheckExact(exp))) {
        shiftby = PyInt_AS_LONG(exp);
    } else
#endif
    if (likely(PyLong_CheckExact(exp))) {
        #if CYTHON_USE_PYLONG_INTERNALS
        if (__Pyx_PyLong_IsZero(exp)) {
            return PyInt_FromLong(1L);
        } else if (__Pyx_PyLong_IsNeg(exp)) {
            goto fallback;
        } else if (__Pyx_PyLong_IsCompact(exp)) {
            shiftby = __Pyx_PyLong_CompactValueUnsigned(exp);
        } else {
            shiftby = PyLong_AsSsize_t(exp);
        }
        #else
        shiftby = PyLong_AsSsize_t(exp);
        #endif
    } else {
        goto fallback;
    }
    if (likely(shiftby >= 0)) {
        if ((size_t)shiftby <= sizeof(long) * 8 - 2) {
            long value = 1L << shiftby;
            return PyInt_FromLong(value);
#ifdef HAVE_LONG_LONG
        } else if ((size_t)shiftby <= sizeof(unsigned PY_LONG_LONG) * 8 - 1) {
            unsigned PY_LONG_LONG value = ((unsigned PY_LONG_LONG)1) << shiftby;
            return PyLong_FromUnsignedLongLong(value);
#endif
        } else {
            PyObject *result, *one = PyInt_FromLong(1L);
            if (unlikely(!one)) return NULL;
            result = PyNumber_Lshift(one, exp);
            Py_DECREF(one);
            return result;
        }
    } else if (shiftby == -1 && PyErr_Occurred()) {
        PyErr_Clear();
    }
fallback:
#endif
    return (inplace ? PyNumber_InPlacePower : PyNumber_Power)(two, exp, none);
}


/////////////// PyIntCompare.proto ///////////////

{{py: c_ret_type = 'PyObject*' if ret_type.is_pyobject else 'int'}}
static CYTHON_INLINE {{c_ret_type}} __Pyx_PyInt_{{'' if ret_type.is_pyobject else 'Bool'}}{{op}}{{order}}(PyObject *op1, PyObject *op2, long intval, long inplace); /*proto*/

/////////////// PyIntCompare ///////////////

{{py: pyval, ival = ('op2', 'b') if order == 'CObj' else ('op1', 'a') }}
{{py: c_ret_type = 'PyObject*' if ret_type.is_pyobject else 'int'}}
{{py: return_true = 'Py_RETURN_TRUE' if ret_type.is_pyobject else 'return 1'}}
{{py: return_false = 'Py_RETURN_FALSE' if ret_type.is_pyobject else 'return 0'}}
{{py: slot_name = op.lower() }}
{{py: c_op = {'Eq': '==', 'Ne': '!='}[op] }}
{{py:
return_compare = (
    (lambda a,b,c_op, return_true=return_true, return_false=return_false: "if ({a} {c_op} {b}) {return_true}; else {return_false};".format(
        a=a, b=b, c_op=c_op, return_true=return_true, return_false=return_false))
    if ret_type.is_pyobject else
    (lambda a,b,c_op: "return ({a} {c_op} {b});".format(a=a, b=b, c_op=c_op))
    )
}}

static CYTHON_INLINE {{c_ret_type}} __Pyx_PyInt_{{'' if ret_type.is_pyobject else 'Bool'}}{{op}}{{order}}(PyObject *op1, PyObject *op2, long intval, long inplace) {
    CYTHON_MAYBE_UNUSED_VAR(intval);
    CYTHON_UNUSED_VAR(inplace);
    if (op1 == op2) {
        {{return_true if op == 'Eq' else return_false}};
    }

    #if PY_MAJOR_VERSION < 3
    if (likely(PyInt_CheckExact({{pyval}}))) {
        const long {{'a' if order == 'CObj' else 'b'}} = intval;
        long {{ival}} = PyInt_AS_LONG({{pyval}});
        {{return_compare('a', 'b', c_op)}}
    }
    #endif

    #if CYTHON_USE_PYLONG_INTERNALS
    if (likely(PyLong_CheckExact({{pyval}}))) {
        int unequal;
        unsigned long uintval;
        Py_ssize_t size = __Pyx_PyLong_DigitCount({{pyval}});
        const digit* digits = __Pyx_PyLong_Digits({{pyval}});
        if (intval == 0) {
            {{return_compare('__Pyx_PyLong_IsZero(%s)' % pyval, '1', c_op)}}
        } else if (intval < 0) {
            if (__Pyx_PyLong_IsNonNeg({{pyval}}))
                {{return_false if op == 'Eq' else return_true}};
            // both are negative => can use absolute values now.
            intval = -intval;
        } else {
            // > 0  =>  Py_SIZE(pyval) > 0
            if (__Pyx_PyLong_IsNeg({{pyval}}))
                {{return_false if op == 'Eq' else return_true}};
        }
        // After checking that the sign is the same (and excluding 0), now compare the absolute values.
        // When inlining, the C compiler should select exactly one line from this unrolled loop.
        uintval = (unsigned long) intval;
        {{for _size in range(4, 0, -1)}}
#if PyLong_SHIFT * {{_size}} < SIZEOF_LONG*8
        if (uintval >> (PyLong_SHIFT * {{_size}})) {
            // The C integer value is between (PyLong_BASE ** _size) and MIN(PyLong_BASE ** _size, LONG_MAX).
            unequal = (size != {{_size+1}}) || (digits[0] != (uintval & (unsigned long) PyLong_MASK))
                {{for _i in range(1, _size+1)}} | (digits[{{_i}}] != ((uintval >> ({{_i}} * PyLong_SHIFT)) & (unsigned long) PyLong_MASK)){{endfor}};
        } else
#endif
        {{endfor}}
            unequal = (size != 1) || (((unsigned long) digits[0]) != (uintval & (unsigned long) PyLong_MASK));

        {{return_compare('unequal', '0', c_op)}}
    }
    #endif

    if (PyFloat_CheckExact({{pyval}})) {
        const long {{'a' if order == 'CObj' else 'b'}} = intval;
#if CYTHON_COMPILING_IN_LIMITED_API
        double {{ival}} = __pyx_PyFloat_AsDouble({{pyval}});
#else
        double {{ival}} = PyFloat_AS_DOUBLE({{pyval}});
#endif
        {{return_compare('(double)a', '(double)b', c_op)}}
    }

    return {{'' if ret_type.is_pyobject else '__Pyx_PyObject_IsTrueAndDecref'}}(
        PyObject_RichCompare(op1, op2, Py_{{op.upper()}}));
}


/////////////// PyIntBinop.proto ///////////////

{{py: c_ret_type = 'PyObject*' if ret_type.is_pyobject else 'int'}}
#if !CYTHON_COMPILING_IN_PYPY
static {{c_ret_type}} __Pyx_PyInt_{{'' if ret_type.is_pyobject else 'Bool'}}{{op}}{{order}}(PyObject *op1, PyObject *op2, long intval, int inplace, int zerodivision_check); /*proto*/
#else
#define __Pyx_PyInt_{{'' if ret_type.is_pyobject else 'Bool'}}{{op}}{{order}}(op1, op2, intval, inplace, zerodivision_check) \
    {{if op in ('Eq', 'Ne')}}{{'' if ret_type.is_pyobject else '__Pyx_PyObject_IsTrueAndDecref'}}(PyObject_RichCompare(op1, op2, Py_{{op.upper()}}))
    {{else}}(inplace ? PyNumber_InPlace{{op}}(op1, op2) : PyNumber_{{op}}(op1, op2))
    {{endif}}
#endif

/////////////// PyIntBinop ///////////////

#if !CYTHON_COMPILING_IN_PYPY
{{py: from Cython.Utility import pylong_join }}
{{py: pyval, ival = ('op2', 'b') if order == 'CObj' else ('op1', 'a') }}
{{py: c_ret_type = 'PyObject*' if ret_type.is_pyobject else 'int'}}
{{py: return_true = 'Py_RETURN_TRUE' if ret_type.is_pyobject else 'return 1'}}
{{py: return_false = 'Py_RETURN_FALSE' if ret_type.is_pyobject else 'return 0'}}
{{py: slot_name = {'TrueDivide': 'true_divide', 'FloorDivide': 'floor_divide'}.get(op, op.lower()) }}
{{py: cfunc_name = '__Pyx_PyInt_%s%s%s' % ('' if ret_type.is_pyobject else 'Bool', op, order)}}
{{py:
c_op = {
    'Add': '+', 'Subtract': '-', 'Multiply': '*', 'Remainder': '%', 'TrueDivide': '/', 'FloorDivide': '/',
    'Or': '|', 'Xor': '^', 'And': '&', 'Rshift': '>>', 'Lshift': '<<',
    'Eq': '==', 'Ne': '!=',
    }[op]
}}
{{py:
def zerodiv_check(operand, optype='integer', _is_mod=op == 'Remainder', _needs_check=(order == 'CObj' and c_op in '%/')):
    return (((
    'if (unlikely(zerodivision_check && ((%s) == 0))) {'
    ' PyErr_SetString(PyExc_ZeroDivisionError, "%s division%s by zero");'
    ' return NULL;'
    '}') % (operand, optype, ' or modulo' if _is_mod else '')
    ) if _needs_check else '')
}}

static {{c_ret_type}} {{cfunc_name}}(PyObject *op1, PyObject *op2, long intval, int inplace, int zerodivision_check) {
    CYTHON_MAYBE_UNUSED_VAR(intval);
    CYTHON_MAYBE_UNUSED_VAR(inplace);
    CYTHON_UNUSED_VAR(zerodivision_check);

    {{if op in ('Eq', 'Ne')}}
    if (op1 == op2) {
        {{return_true if op == 'Eq' else return_false}};
    }
    {{endif}}

    #if PY_MAJOR_VERSION < 3
    if (likely(PyInt_CheckExact({{pyval}}))) {
        const long {{'a' if order == 'CObj' else 'b'}} = intval;
        {{if c_op in '+-%' or op == 'FloorDivide'}}
        long x;
        {{endif}}
        long {{ival}} = PyInt_AS_LONG({{pyval}});
        {{zerodiv_check('b')}}

        {{if op in ('Eq', 'Ne')}}
        if (a {{c_op}} b) {
            {{return_true}};
        } else {
            {{return_false}};
        }
        {{elif c_op in '+-'}}
            // adapted from intobject.c in Py2.7:
            // casts in the line below avoid undefined behaviour on overflow
            x = (long)((unsigned long)a {{c_op}} (unsigned long)b);
            if (likely((x^a) >= 0 || (x^{{ '~' if op == 'Subtract' else '' }}b) >= 0))
                return PyInt_FromLong(x);
            return PyLong_Type.tp_as_number->nb_{{slot_name}}(op1, op2);
        {{elif c_op == '%'}}
            // see CMath.c :: ModInt utility code
            x = a % b;
            x += ((x != 0) & ((x ^ b) < 0)) * b;
            return PyInt_FromLong(x);
        {{elif op == 'TrueDivide'}}
            if (8 * sizeof(long) <= 53 || likely(labs({{ival}}) <= ((PY_LONG_LONG)1 << 53))) {
                return PyFloat_FromDouble((double)a / (double)b);
            }
            // let Python do the rounding
            return PyInt_Type.tp_as_number->nb_{{slot_name}}(op1, op2);
        {{elif op == 'FloorDivide'}}
            // INT_MIN / -1  is the only case that overflows
            if (unlikely(b == -1 && ((unsigned long)a) == 0-(unsigned long)a))
                return PyInt_Type.tp_as_number->nb_{{slot_name}}(op1, op2);
            else {
                long q, r;
                // see CMath.c :: DivInt utility code
                q = a / b;
                r = a - q*b;
                q -= ((r != 0) & ((r ^ b) < 0));
                x = q;
            }
            return PyInt_FromLong(x);
        {{elif op == 'Lshift'}}
            if (likely(b < (long) (sizeof(long)*8) && a == (a << b) >> b) || !a) {
                return PyInt_FromLong(a {{c_op}} b);
            }
        {{elif c_op == '*'}}
#ifdef HAVE_LONG_LONG
            if (sizeof(PY_LONG_LONG) > sizeof(long)) {
                PY_LONG_LONG result = (PY_LONG_LONG)a {{c_op}} (PY_LONG_LONG)b;
                return (result >= LONG_MIN && result <= LONG_MAX) ?
                    PyInt_FromLong((long)result) : PyLong_FromLongLong(result);
            }
#endif
#if CYTHON_USE_TYPE_SLOTS
            return PyInt_Type.tp_as_number->nb_{{slot_name}}(op1, op2);
#else
            return PyNumber_{{op}}(op1, op2);
#endif
        {{else}}
            // other operations are safe, no overflow
            return PyInt_FromLong(a {{c_op}} b);
        {{endif}}
    }
    #endif

    #if CYTHON_USE_PYLONG_INTERNALS
    if (likely(PyLong_CheckExact({{pyval}}))) {
        const long {{'a' if order == 'CObj' else 'b'}} = intval;
        long {{ival}}{{if op not in ('Eq', 'Ne')}}, x{{endif}};
        {{if op not in ('Eq', 'Ne', 'TrueDivide')}}
#ifdef HAVE_LONG_LONG
        const PY_LONG_LONG ll{{'a' if order == 'CObj' else 'b'}} = intval;
        PY_LONG_LONG ll{{ival}}, llx;
#endif
        {{endif}}
        {{if c_op == '&'}}
        // special case for &-ing arbitrarily large numbers with known single digit operands
        if ((intval & PyLong_MASK) == intval) {
            // Calling PyLong_CompactValue() requires the PyLong value to be compact, we only need the last digit.
            long last_digit = (long) __Pyx_PyLong_Digits({{pyval}})[0];
            long result = intval & (likely(__Pyx_PyLong_IsPos({{pyval}})) ? last_digit : (PyLong_MASK - last_digit + 1));
            return PyLong_FromLong(result);
        }
        {{endif}}
        // special cases for 0: + - * % / // | ^ & >> <<
        if (unlikely(__Pyx_PyLong_IsZero({{pyval}}))) {
            {{if order == 'CObj' and c_op in '%/'}}
            // division by zero!
            {{zerodiv_check('0')}}
            {{elif order == 'CObj' and c_op in '+-|^>><<'}}
            // x == x+0 == x-0 == x|0 == x^0 == x>>0 == x<<0
            return __Pyx_NewRef(op1);
            {{elif order == 'CObj' and c_op in '*&'}}
            // 0 == x*0 == x&0
            return __Pyx_NewRef(op2);
            {{elif order == 'ObjC' and c_op in '+|^'}}
            // x == 0+x == 0|x == 0^x
            return __Pyx_NewRef(op2);
            {{elif order == 'ObjC' and c_op == '-'}}
            // -x == 0-x
            return PyLong_FromLong(-intval);
            {{elif order == 'ObjC' and (c_op in '*%&>><<' or op == 'FloorDivide')}}
            // 0 == 0*x == 0%x == 0&x == 0>>x == 0<<x == 0//x
            return __Pyx_NewRef(op1);
            {{endif}}
        }
        // handle most common case first to avoid indirect branch and optimise branch prediction
        if (likely(__Pyx_PyLong_IsCompact({{pyval}}))) {
            {{ival}} = __Pyx_PyLong_CompactValue({{pyval}});
        } else {
            const digit* digits = __Pyx_PyLong_Digits({{pyval}});
            const Py_ssize_t size = __Pyx_PyLong_SignedDigitCount({{pyval}});
            switch (size) {
                {{for _size in range(2, 5)}}
                {{for _case in (-_size, _size)}}
                case {{_case}}:
                    if (8 * sizeof(long) - 1 > {{_size}} * PyLong_SHIFT{{if c_op == '*'}}+30{{endif}}{{if op == 'TrueDivide'}} && {{_size-1}} * PyLong_SHIFT < 53{{endif}}) {
                        {{ival}} = {{'-' if _case < 0 else ''}}(long) {{pylong_join(_size, 'digits')}};
                        break;
                    {{if op not in ('Eq', 'Ne', 'TrueDivide')}}
                    #ifdef HAVE_LONG_LONG
                    } else if (8 * sizeof(PY_LONG_LONG) - 1 > {{_size}} * PyLong_SHIFT{{if c_op == '*'}}+30{{endif}}) {
                        ll{{ival}} = {{'-' if _case < 0 else ''}}(PY_LONG_LONG) {{pylong_join(_size, 'digits', 'unsigned PY_LONG_LONG')}};
                        goto long_long;
                    #endif
                    {{endif}}
                    }
                    // if size doesn't fit into a long or PY_LONG_LONG anymore, fall through to default
                    CYTHON_FALLTHROUGH;
                {{endfor}}
                {{endfor}}

                {{if op in ('Eq', 'Ne')}}
                #if PyLong_SHIFT < 30 && PyLong_SHIFT != 15
                // unusual setup - your fault
                default: return {{'' if ret_type.is_pyobject else '__Pyx_PyObject_IsTrueAndDecref'}}(
                    PyLong_Type.tp_richcompare({{'op1, op2' if order == 'ObjC' else 'op2, op1'}}, Py_{{op.upper()}}));
                #else
                // too large for the long values we allow => definitely not equal
                default: {{return_false if op == 'Eq' else return_true}};
                #endif
                {{else}}
                default: return PyLong_Type.tp_as_number->nb_{{slot_name}}(op1, op2);
                {{endif}}
            }
        }
        {{if op in ('Eq', 'Ne')}}
            if (a {{c_op}} b) {
                {{return_true}};
            } else {
                {{return_false}};
            }
        {{else}}
            {{if c_op == '*'}}
                CYTHON_UNUSED_VAR(a);
                CYTHON_UNUSED_VAR(b);
                #ifdef HAVE_LONG_LONG
                ll{{ival}} = {{ival}};
                goto long_long;
                #else
                return PyLong_Type.tp_as_number->nb_{{slot_name}}(op1, op2);
                #endif
            {{elif c_op == '%'}}
                // see CMath.c :: ModInt utility code
                x = a % b;
                x += ((x != 0) & ((x ^ b) < 0)) * b;
            {{elif op == 'TrueDivide'}}
                if ((8 * sizeof(long) <= 53 || likely(labs({{ival}}) <= ((PY_LONG_LONG)1 << 53)))
                        || __Pyx_PyLong_DigitCount({{pyval}}) <= 52 / PyLong_SHIFT) {
                    return PyFloat_FromDouble((double)a / (double)b);
                }
                return PyLong_Type.tp_as_number->nb_{{slot_name}}(op1, op2);
            {{elif op == 'FloorDivide'}}
                {
                    long q, r;
                    // see CMath.c :: DivInt utility code
                    q = a / b;
                    r = a - q*b;
                    q -= ((r != 0) & ((r ^ b) < 0));
                    x = q;
                }
            {{else}}
                x = a {{c_op}} b;
                {{if op == 'Lshift'}}
#ifdef HAVE_LONG_LONG
                if (unlikely(!(b < (long) (sizeof(long)*8) && a == x >> b)) && a) {
                    ll{{ival}} = {{ival}};
                    goto long_long;
                }
#else
                if (likely(b < (long) (sizeof(long)*8) && a == x >> b) || !a) /* execute return statement below */
#endif
                {{endif}}
            {{endif}}
            return PyLong_FromLong(x);

        {{if op != 'TrueDivide'}}
#ifdef HAVE_LONG_LONG
        long_long:
            {{if c_op == '%'}}
                // see CMath.c :: ModInt utility code
                llx = lla % llb;
                llx += ((llx != 0) & ((llx ^ llb) < 0)) * llb;
            {{elif op == 'FloorDivide'}}
                {
                    PY_LONG_LONG q, r;
                    // see CMath.c :: DivInt utility code
                    q = lla / llb;
                    r = lla - q*llb;
                    q -= ((r != 0) & ((r ^ llb) < 0));
                    llx = q;
                }
            {{else}}
                llx = lla {{c_op}} llb;
                {{if op == 'Lshift'}}
                if (likely(lla == llx >> llb)) /* then execute 'return' below */
                {{endif}}
            {{endif}}
            return PyLong_FromLongLong(llx);
#endif
        {{endif}}{{# if op != 'TrueDivide' #}}
        {{endif}}{{# if op in ('Eq', 'Ne') #}}
    }
    #endif

    {{if c_op in '+-*' or op in ('TrueDivide', 'Eq', 'Ne')}}
    if (PyFloat_CheckExact({{pyval}})) {
        const long {{'a' if order == 'CObj' else 'b'}} = intval;
#if CYTHON_COMPILING_IN_LIMITED_API
        double {{ival}} = __pyx_PyFloat_AsDouble({{pyval}});
#else
        double {{ival}} = PyFloat_AS_DOUBLE({{pyval}});
#endif
        {{if op in ('Eq', 'Ne')}}
            if ((double)a {{c_op}} (double)b) {
                {{return_true}};
            } else {
                {{return_false}};
            }
        {{else}}
            double result;
            {{zerodiv_check('b', 'float')}}
            // copied from floatobject.c in Py3.5:
            PyFPE_START_PROTECT("{{op.lower() if not op.endswith('Divide') else 'divide'}}", return NULL)
            result = ((double)a) {{c_op}} (double)b;
            PyFPE_END_PROTECT(result)
            return PyFloat_FromDouble(result);
        {{endif}}
    }
    {{endif}}

    {{if op in ('Eq', 'Ne')}}
    return {{'' if ret_type.is_pyobject else '__Pyx_PyObject_IsTrueAndDecref'}}(
        PyObject_RichCompare(op1, op2, Py_{{op.upper()}}));
    {{else}}
    return (inplace ? PyNumber_InPlace{{op}} : PyNumber_{{op}})(op1, op2);
    {{endif}}
}
#endif

/////////////// PyFloatBinop.proto ///////////////

{{py: c_ret_type = 'PyObject*' if ret_type.is_pyobject else 'int'}}
#if !CYTHON_COMPILING_IN_PYPY
static {{c_ret_type}} __Pyx_PyFloat_{{'' if ret_type.is_pyobject else 'Bool'}}{{op}}{{order}}(PyObject *op1, PyObject *op2, double floatval, int inplace, int zerodivision_check); /*proto*/
#else
#define __Pyx_PyFloat_{{'' if ret_type.is_pyobject else 'Bool'}}{{op}}{{order}}(op1, op2, floatval, inplace, zerodivision_check) \
    {{if op in ('Eq', 'Ne')}}{{'' if ret_type.is_pyobject else '__Pyx_PyObject_IsTrueAndDecref'}}(PyObject_RichCompare(op1, op2, Py_{{op.upper()}}))
    {{elif op == 'Divide'}}((inplace ? __Pyx_PyNumber_InPlaceDivide(op1, op2) : __Pyx_PyNumber_Divide(op1, op2)))
    {{else}}(inplace ? PyNumber_InPlace{{op}}(op1, op2) : PyNumber_{{op}}(op1, op2))
    {{endif}}
#endif

/////////////// PyFloatBinop ///////////////

#if !CYTHON_COMPILING_IN_PYPY
{{py: from Cython.Utility import pylong_join }}
{{py: c_ret_type = 'PyObject*' if ret_type.is_pyobject else 'int'}}
{{py: return_true = 'Py_RETURN_TRUE' if ret_type.is_pyobject else 'return 1'}}
{{py: return_false = 'Py_RETURN_FALSE' if ret_type.is_pyobject else 'return 0'}}
{{py: pyval, fval = ('op2', 'b') if order == 'CObj' else ('op1', 'a') }}
{{py: cfunc_name = '__Pyx_PyFloat_%s%s%s' % ('' if ret_type.is_pyobject else 'Bool', op, order) }}
{{py:
c_op = {
    'Add': '+', 'Subtract': '-', 'TrueDivide': '/', 'Divide': '/', 'Remainder': '%',
    'Eq': '==', 'Ne': '!=',
    }[op]
}}
{{py:
def zerodiv_check(operand, _is_mod=op == 'Remainder', _needs_check=(order == 'CObj' and c_op in '%/')):
    return (((
        'if (unlikely(zerodivision_check && ((%s) == 0.0))) {'
        ' PyErr_SetString(PyExc_ZeroDivisionError, "float division%s by zero");'
        ' return NULL;'
        '}') % (operand, ' or modulo' if _is_mod else '')
    ) if _needs_check else '')
}}

static {{c_ret_type}} {{cfunc_name}}(PyObject *op1, PyObject *op2, double floatval, int inplace, int zerodivision_check) {
    const double {{'a' if order == 'CObj' else 'b'}} = floatval;
    double {{fval}}{{if op not in ('Eq', 'Ne')}}, result{{endif}};
    CYTHON_UNUSED_VAR(inplace);
    CYTHON_UNUSED_VAR(zerodivision_check);

    {{if op in ('Eq', 'Ne')}}
    if (op1 == op2) {
        {{return_true if op == 'Eq' else return_false}};
    }
    {{endif}}

    if (likely(PyFloat_CheckExact({{pyval}}))) {
#if CYTHON_COMPILING_IN_LIMITED_API
        {{fval}} = __pyx_PyFloat_AsDouble({{pyval}});
#else
        {{fval}} = PyFloat_AS_DOUBLE({{pyval}});
#endif
        {{zerodiv_check(fval)}}
    } else

    #if PY_MAJOR_VERSION < 3
    if (likely(PyInt_CheckExact({{pyval}}))) {
        {{fval}} = (double) PyInt_AS_LONG({{pyval}});
        {{zerodiv_check(fval)}}
    } else
    #endif

    if (likely(PyLong_CheckExact({{pyval}}))) {
        #if CYTHON_USE_PYLONG_INTERNALS
        if (__Pyx_PyLong_IsZero({{pyval}})) {
            {{fval}} = 0.0;
            {{zerodiv_check(fval)}}
        } else if (__Pyx_PyLong_IsCompact({{pyval}})) {
            {{fval}} = (double) __Pyx_PyLong_CompactValue({{pyval}});
        } else {
            const digit* digits = __Pyx_PyLong_Digits({{pyval}});
            const Py_ssize_t size = __Pyx_PyLong_SignedDigitCount({{pyval}});
            switch (size) {
                {{for _size in (2, 3, 4)}}
                case -{{_size}}:
                case {{_size}}:
                    if (8 * sizeof(unsigned long) > {{_size}} * PyLong_SHIFT && ((8 * sizeof(unsigned long) < 53) || ({{_size-1}} * PyLong_SHIFT < 53))) {
                        {{fval}} = (double) {{pylong_join(_size, 'digits')}};
                        // let CPython do its own float rounding from 2**53 on (max. consecutive integer in double float)
                        if ((8 * sizeof(unsigned long) < 53) || ({{_size}} * PyLong_SHIFT < 53) || ({{fval}} < (double) ((PY_LONG_LONG)1 << 53))) {
                            if (size == {{-_size}})
                                {{fval}} = -{{fval}};
                            break;
                        }
                    }
                    // Fall through if size doesn't fit safely into a double anymore.
                    // It may not be obvious that this is a safe fall-through given the "fval < 2**53"
                    // check above.  However, the number of digits that CPython uses for a given PyLong
                    // value is minimal, and together with the "(size-1) * SHIFT < 53" check above,
                    // this should make it safe.
                    CYTHON_FALLTHROUGH;
                {{endfor}}
                default:
        #endif
        {{if op in ('Eq', 'Ne')}}
                    return {{'' if ret_type.is_pyobject else '__Pyx_PyObject_IsTrueAndDecref'}}(
                        PyFloat_Type.tp_richcompare({{'op1, op2' if order == 'CObj' else 'op2, op1'}}, Py_{{op.upper()}}));
        {{else}}
                    {{fval}} = PyLong_AsDouble({{pyval}});
                    if (unlikely({{fval}} == -1.0 && PyErr_Occurred())) return NULL;
                    {{if zerodiv_check(fval)}}
                    #if !CYTHON_USE_PYLONG_INTERNALS
                    {{zerodiv_check(fval)}}
                    #endif
                    {{endif}}
        {{endif}}
        #if CYTHON_USE_PYLONG_INTERNALS
            }
        }
        #endif
    } else {
        {{if op in ('Eq', 'Ne')}}
        return {{'' if ret_type.is_pyobject else '__Pyx_PyObject_IsTrueAndDecref'}}(
            PyObject_RichCompare(op1, op2, Py_{{op.upper()}}));
        {{elif op == 'Divide'}}
        return (inplace ? __Pyx_PyNumber_InPlaceDivide(op1, op2) : __Pyx_PyNumber_Divide(op1, op2));
        {{else}}
        return (inplace ? PyNumber_InPlace{{op}} : PyNumber_{{op}})(op1, op2);
        {{endif}}
    }

    {{if op in ('Eq', 'Ne')}}
        if (a {{c_op}} b) {
            {{return_true}};
        } else {
            {{return_false}};
        }
    {{else}}
        // copied from floatobject.c in Py3.5:
        PyFPE_START_PROTECT("{{op.lower() if not op.endswith('Divide') else 'divide'}}", return NULL)
        {{if c_op == '%'}}
        result = fmod(a, b);
        if (result)
            result += ((result < 0) ^ (b < 0)) * b;
        else
            result = copysign(0.0, b);
        {{else}}
        result = a {{c_op}} b;
        {{endif}}
        PyFPE_END_PROTECT(result)
        return PyFloat_FromDouble(result);
    {{endif}}
}
#endif
