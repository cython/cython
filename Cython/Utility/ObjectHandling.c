/////////////// RaiseNoneIterError.proto ///////////////

static CYTHON_INLINE void __Pyx_RaiseNoneNotIterableError(void);

/////////////// RaiseNoneIterError ///////////////

static CYTHON_INLINE void __Pyx_RaiseNoneNotIterableError(void) {
    PyErr_SetString(PyExc_TypeError, "'NoneType' object is not iterable");
}

/////////////// RaiseTooManyValuesToUnpack.proto ///////////////

static CYTHON_INLINE void __Pyx_RaiseTooManyValuesError(Py_ssize_t expected);

/////////////// RaiseTooManyValuesToUnpack ///////////////

static CYTHON_INLINE void __Pyx_RaiseTooManyValuesError(Py_ssize_t expected) {
    PyErr_Format(PyExc_ValueError,
                 "too many values to unpack (expected %" CYTHON_FORMAT_SSIZE_T "d)", expected);
}

/////////////// RaiseNeedMoreValuesToUnpack.proto ///////////////

static CYTHON_INLINE void __Pyx_RaiseNeedMoreValuesError(Py_ssize_t index);

/////////////// RaiseNeedMoreValuesToUnpack ///////////////

static CYTHON_INLINE void __Pyx_RaiseNeedMoreValuesError(Py_ssize_t index) {
    PyErr_Format(PyExc_ValueError,
                 "need more than %" CYTHON_FORMAT_SSIZE_T "d value%s to unpack",
                 index, (index == 1) ? "" : "s");
}

/////////////// UnpackTupleError.proto ///////////////

static void __Pyx_UnpackTupleError(PyObject *, Py_ssize_t index); /*proto*/

/////////////// UnpackTupleError ///////////////
//@requires: RaiseNoneIterError
//@requires: RaiseNeedMoreValuesToUnpack
//@requires: RaiseTooManyValuesToUnpack

static void __Pyx_UnpackTupleError(PyObject *t, Py_ssize_t index) {
    if (t == Py_None) {
      __Pyx_RaiseNoneNotIterableError();
    } else if (PyTuple_GET_SIZE(t) < index) {
      __Pyx_RaiseNeedMoreValuesError(PyTuple_GET_SIZE(t));
    } else {
      __Pyx_RaiseTooManyValuesError(index);
    }
}

/////////////// UnpackItemEndCheck.proto ///////////////

static int __Pyx_IternextUnpackEndCheck(PyObject *retval, Py_ssize_t expected); /*proto*/

/////////////// UnpackItemEndCheck ///////////////
//@requires: RaiseTooManyValuesToUnpack
//@requires: IterFinish

static int __Pyx_IternextUnpackEndCheck(PyObject *retval, Py_ssize_t expected) {
    if (unlikely(retval)) {
        Py_DECREF(retval);
        __Pyx_RaiseTooManyValuesError(expected);
        return -1;
    } else {
        return __Pyx_IterFinish();
    }
    return 0;
}

/////////////// UnpackTuple2.proto ///////////////

static CYTHON_INLINE int __Pyx_unpack_tuple2(PyObject* tuple, PyObject** value1, PyObject** value2,
                                             int is_tuple, int has_known_size, int decref_tuple);

/////////////// UnpackTuple2 ///////////////
//@requires: UnpackItemEndCheck
//@requires: UnpackTupleError
//@requires: RaiseNeedMoreValuesToUnpack

static CYTHON_INLINE int __Pyx_unpack_tuple2(PyObject* tuple, PyObject** pvalue1, PyObject** pvalue2,
                                             int is_tuple, int has_known_size, int decref_tuple) {
    Py_ssize_t index;
    PyObject *value1 = NULL, *value2 = NULL, *iter = NULL;
    if (!is_tuple && unlikely(!PyTuple_Check(tuple))) {
        iternextfunc iternext;
        iter = PyObject_GetIter(tuple);
        if (unlikely(!iter)) goto bad;
        if (decref_tuple) { Py_DECREF(tuple); tuple = NULL; }
        iternext = Py_TYPE(iter)->tp_iternext;
        value1 = iternext(iter); if (unlikely(!value1)) { index = 0; goto unpacking_failed; }
        value2 = iternext(iter); if (unlikely(!value2)) { index = 1; goto unpacking_failed; }
        if (!has_known_size && unlikely(__Pyx_IternextUnpackEndCheck(iternext(iter), 2))) goto bad;
        Py_DECREF(iter);
    } else {
        if (!has_known_size && unlikely(PyTuple_GET_SIZE(tuple) != 2)) {
            __Pyx_UnpackTupleError(tuple, 2);
            goto bad;
        }
#if CYTHON_COMPILING_IN_PYPY
        value1 = PySequence_ITEM(tuple, 0);
        if (unlikely(!value1)) goto bad;
        value2 = PySequence_ITEM(tuple, 1);
        if (unlikely(!value2)) goto bad;
#else
        value1 = PyTuple_GET_ITEM(tuple, 0);
        value2 = PyTuple_GET_ITEM(tuple, 1);
        Py_INCREF(value1);
        Py_INCREF(value2);
#endif
        if (decref_tuple) { Py_DECREF(tuple); }
    }
    *pvalue1 = value1;
    *pvalue2 = value2;
    return 0;
unpacking_failed:
    if (!has_known_size && __Pyx_IterFinish() == 0)
        __Pyx_RaiseNeedMoreValuesError(index);
bad:
    Py_XDECREF(iter);
    Py_XDECREF(value1);
    Py_XDECREF(value2);
    if (decref_tuple) { Py_XDECREF(tuple); }
    return -1;
}

/////////////// IterNext.proto ///////////////

#define __Pyx_PyIter_Next(obj) __Pyx_PyIter_Next2(obj, NULL)
static CYTHON_INLINE PyObject *__Pyx_PyIter_Next2(PyObject *, PyObject *); /*proto*/

/////////////// IterNext ///////////////

// originally copied from Py3's builtin_next()
static CYTHON_INLINE PyObject *__Pyx_PyIter_Next2(PyObject* iterator, PyObject* defval) {
    PyObject* next;
    iternextfunc iternext = Py_TYPE(iterator)->tp_iternext;
#if CYTHON_COMPILING_IN_CPYTHON
    if (unlikely(!iternext)) {
#else
    if (unlikely(!iternext) || unlikely(!PyIter_Check(iterator))) {
#endif
        PyErr_Format(PyExc_TypeError,
            "%.200s object is not an iterator", Py_TYPE(iterator)->tp_name);
        return NULL;
    }
    next = iternext(iterator);
    if (likely(next))
        return next;
#if CYTHON_COMPILING_IN_CPYTHON
#if PY_VERSION_HEX >= 0x03010000 || (PY_MAJOR_VERSION < 3 && PY_VERSION_HEX >= 0x02070000)
    if (unlikely(iternext == &_PyObject_NextNotImplemented))
        return NULL;
#endif
#endif
    if (defval) {
        PyObject* exc_type = PyErr_Occurred();
        if (exc_type) {
            if (unlikely(exc_type != PyExc_StopIteration) &&
                    !PyErr_GivenExceptionMatches(exc_type, PyExc_StopIteration))
                return NULL;
            PyErr_Clear();
        }
        Py_INCREF(defval);
        return defval;
    }
    if (!PyErr_Occurred())
        PyErr_SetNone(PyExc_StopIteration);
    return NULL;
}

/////////////// IterFinish.proto ///////////////

static CYTHON_INLINE int __Pyx_IterFinish(void); /*proto*/

/////////////// IterFinish ///////////////

// When PyIter_Next(iter) has returned NULL in order to signal termination,
// this function does the right cleanup and returns 0 on success.  If it
// detects an error that occurred in the iterator, it returns -1.

static CYTHON_INLINE int __Pyx_IterFinish(void) {
#if CYTHON_COMPILING_IN_CPYTHON
    PyThreadState *tstate = PyThreadState_GET();
    PyObject* exc_type = tstate->curexc_type;
    if (unlikely(exc_type)) {
        if (likely(exc_type == PyExc_StopIteration) || PyErr_GivenExceptionMatches(exc_type, PyExc_StopIteration)) {
            PyObject *exc_value, *exc_tb;
            exc_value = tstate->curexc_value;
            exc_tb = tstate->curexc_traceback;
            tstate->curexc_type = 0;
            tstate->curexc_value = 0;
            tstate->curexc_traceback = 0;
            Py_DECREF(exc_type);
            Py_XDECREF(exc_value);
            Py_XDECREF(exc_tb);
            return 0;
        } else {
            return -1;
        }
    }
    return 0;
#else
    if (unlikely(PyErr_Occurred())) {
        if (likely(PyErr_ExceptionMatches(PyExc_StopIteration))) {
            PyErr_Clear();
            return 0;
        } else {
            return -1;
        }
    }
    return 0;
#endif
}

/////////////// DictGetItem.proto ///////////////

#if PY_MAJOR_VERSION >= 3
static PyObject *__Pyx_PyDict_GetItem(PyObject *d, PyObject* key) {
    PyObject *value;
    value = PyDict_GetItemWithError(d, key);
    if (unlikely(!value)) {
        if (!PyErr_Occurred())
            PyErr_SetObject(PyExc_KeyError, key);
        return NULL;
    }
    Py_INCREF(value);
    return value;
}
#else
    #define __Pyx_PyDict_GetItem(d, key) PyObject_GetItem(d, key)
#endif

/////////////// GetItemInt.proto ///////////////

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Generic(PyObject *o, PyObject* j) {
    PyObject *r;
    if (!j) return NULL;
    r = PyObject_GetItem(o, j);
    Py_DECREF(j);
    return r;
}

{{for type in ['List', 'Tuple']}}
#define __Pyx_GetItemInt_{{type}}(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \
                                                    __Pyx_GetItemInt_{{type}}_Fast(o, i) : \
                                                    __Pyx_GetItemInt_Generic(o, to_py_func(i)))

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_{{type}}_Fast(PyObject *o, Py_ssize_t i) {
#if CYTHON_COMPILING_IN_CPYTHON
    if (likely((0 <= i) & (i < Py{{type}}_GET_SIZE(o)))) {
        PyObject *r = Py{{type}}_GET_ITEM(o, i);
        Py_INCREF(r);
        return r;
    }
    else if ((-Py{{type}}_GET_SIZE(o) <= i) & (i < 0)) {
        PyObject *r = Py{{type}}_GET_ITEM(o, Py{{type}}_GET_SIZE(o) + i);
        Py_INCREF(r);
        return r;
    }
    return __Pyx_GetItemInt_Generic(o, PyInt_FromSsize_t(i));
#else
    return PySequence_GetItem(o, i);
#endif
}
{{endfor}}

#define __Pyx_GetItemInt(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \
                                                    __Pyx_GetItemInt_Fast(o, i) : \
                                                    __Pyx_GetItemInt_Generic(o, to_py_func(i)))

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i) {
#if CYTHON_COMPILING_IN_CPYTHON
    if (PyList_CheckExact(o)) {
        Py_ssize_t n = (likely(i >= 0)) ? i : i + PyList_GET_SIZE(o);
        if (likely((n >= 0) & (n < PyList_GET_SIZE(o)))) {
            PyObject *r = PyList_GET_ITEM(o, n);
            Py_INCREF(r);
            return r;
        }
    }
    else if (PyTuple_CheckExact(o)) {
        Py_ssize_t n = (likely(i >= 0)) ? i : i + PyTuple_GET_SIZE(o);
        if (likely((n >= 0) & (n < PyTuple_GET_SIZE(o)))) {
            PyObject *r = PyTuple_GET_ITEM(o, n);
            Py_INCREF(r);
            return r;
        }
    } else {  /* inlined PySequence_GetItem() */
        PySequenceMethods *m = Py_TYPE(o)->tp_as_sequence;
        if (likely(m && m->sq_item)) {
            if (unlikely(i < 0) && likely(m->sq_length)) {
                Py_ssize_t l = m->sq_length(o);
                if (unlikely(l < 0)) return NULL;
                i += l;
            }
            return m->sq_item(o, i);
        }
    }
#else
    if (PySequence_Check(o)) {
        return PySequence_GetItem(o, i);
    }
#endif
    return __Pyx_GetItemInt_Generic(o, PyInt_FromSsize_t(i));
}

/////////////// SetItemInt.proto ///////////////

#define __Pyx_SetItemInt(o, i, v, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \
                                                    __Pyx_SetItemInt_Fast(o, i, v) : \
                                                    __Pyx_SetItemInt_Generic(o, to_py_func(i), v))

static CYTHON_INLINE int __Pyx_SetItemInt_Generic(PyObject *o, PyObject *j, PyObject *v) {
    int r;
    if (!j) return -1;
    r = PyObject_SetItem(o, j, v);
    Py_DECREF(j);
    return r;
}

static CYTHON_INLINE int __Pyx_SetItemInt_Fast(PyObject *o, Py_ssize_t i, PyObject *v) {
#if CYTHON_COMPILING_IN_CPYTHON
    if (PyList_CheckExact(o)) {
        Py_ssize_t n = (likely(i >= 0)) ? i : i + PyList_GET_SIZE(o);
        if (likely((n >= 0) & (n < PyList_GET_SIZE(o)))) {
            PyObject* old = PyList_GET_ITEM(o, n);
            Py_INCREF(v);
            PyList_SET_ITEM(o, n, v);
            Py_DECREF(old);
            return 1;
        }
    } else {  /* inlined PySequence_SetItem() */
        PySequenceMethods *m = Py_TYPE(o)->tp_as_sequence;
        if (likely(m && m->sq_ass_item)) {
            if (unlikely(i < 0) && likely(m->sq_length)) {
                Py_ssize_t l = m->sq_length(o);
                if (unlikely(l < 0)) return -1;
                i += l;
            }
            return m->sq_ass_item(o, i, v);
        }
    }
#else
#if CYTHON_COMPILING_IN_PYPY
    if (PySequence_Check(o) && !PyDict_Check(o)) {
#else
    if (PySequence_Check(o)) {
#endif
        return PySequence_SetItem(o, i, v);
    }
#endif
    return __Pyx_SetItemInt_Generic(o, PyInt_FromSsize_t(i), v);
}

/////////////// DelItemInt.proto ///////////////

#define __Pyx_DelItemInt(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \
                                                    __Pyx_DelItemInt_Fast(o, i) : \
                                                    __Pyx_DelItem_Generic(o, to_py_func(i)))

static CYTHON_INLINE int __Pyx_DelItem_Generic(PyObject *o, PyObject *j) {
    int r;
    if (!j) return -1;
    r = PyObject_DelItem(o, j);
    Py_DECREF(j);
    return r;
}

static CYTHON_INLINE int __Pyx_DelItemInt_Fast(PyObject *o, Py_ssize_t i) {
#if CYTHON_COMPILING_IN_PYPY
    if (PySequence_Check(o)) {
        return PySequence_DelItem(o, i);
    }
#else
    /* inlined PySequence_DelItem() */
    PySequenceMethods *m = Py_TYPE(o)->tp_as_sequence;
    if (likely(m && m->sq_ass_item)) {
        if (unlikely(i < 0) && likely(m->sq_length)) {
            Py_ssize_t l = m->sq_length(o);
            if (unlikely(l < 0)) return -1;
            i += l;
        }
        return m->sq_ass_item(o, i, (PyObject *)NULL);
    }
#endif
    return __Pyx_DelItem_Generic(o, PyInt_FromSsize_t(i));
}

/////////////// FindPy2Metaclass.proto ///////////////

static PyObject *__Pyx_FindPy2Metaclass(PyObject *bases); /*proto*/

/////////////// FindPy2Metaclass ///////////////

static PyObject *__Pyx_FindPy2Metaclass(PyObject *bases) {
    PyObject *metaclass;
    /* Default metaclass */
#if PY_MAJOR_VERSION < 3
    if (PyTuple_Check(bases) && PyTuple_GET_SIZE(bases) > 0) {
        PyObject *base = PyTuple_GET_ITEM(bases, 0);
        metaclass = PyObject_GetAttrString(base, (char *)"__class__");
        if (!metaclass) {
            PyErr_Clear();
            metaclass = (PyObject*) Py_TYPE(base);
        }
    } else {
        metaclass = (PyObject *) &PyClass_Type;
    }
#else
    if (PyTuple_Check(bases) && PyTuple_GET_SIZE(bases) > 0) {
        PyObject *base = PyTuple_GET_ITEM(bases, 0);
        metaclass = (PyObject*) Py_TYPE(base);
    } else {
        metaclass = (PyObject *) &PyType_Type;
    }
#endif
    Py_INCREF(metaclass);
    return metaclass;
}

/////////////// Py3MetaclassGet.proto ///////////////

static PyObject *__Pyx_Py3MetaclassGet(PyObject *bases, PyObject *mkw); /*proto*/

/////////////// Py3MetaclassGet ///////////////
//@requires: FindPy2Metaclass

static PyObject *__Pyx_Py3MetaclassGet(PyObject *bases, PyObject *mkw) {
    PyObject *metaclass = PyDict_GetItemString(mkw, "metaclass");
    if (metaclass) {
        Py_INCREF(metaclass);
        if (PyDict_DelItemString(mkw, "metaclass") < 0) {
            Py_DECREF(metaclass);
            return NULL;
        }
        return metaclass;
    }
    return __Pyx_FindPy2Metaclass(bases);
}

/////////////// CreateClass.proto ///////////////

static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name,
                                   PyObject *modname); /*proto*/

/////////////// CreateClass ///////////////
//@requires: FindPy2Metaclass

static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name,
                                   PyObject *modname) {
    PyObject *result;
    PyObject *metaclass;

    if (PyDict_SetItemString(dict, "__module__", modname) < 0)
        return NULL;

    /* Python2 __metaclass__ */
    metaclass = PyDict_GetItemString(dict, "__metaclass__");
    if (metaclass) {
        Py_INCREF(metaclass);
    } else {
        metaclass = __Pyx_FindPy2Metaclass(bases);
    }
    result = PyObject_CallFunctionObjArgs(metaclass, name, bases, dict, NULL);
    Py_DECREF(metaclass);
    return result;
}

/////////////// Py3ClassCreate.proto ///////////////

static PyObject *__Pyx_Py3MetaclassPrepare(PyObject *metaclass, PyObject *bases, PyObject *name, PyObject *mkw, PyObject *modname, PyObject *doc); /*proto*/
static PyObject *__Pyx_Py3ClassCreate(PyObject *metaclass, PyObject *name, PyObject *bases, PyObject *dict, PyObject *mkw); /*proto*/

/////////////// Py3ClassCreate ///////////////

static PyObject *__Pyx_Py3MetaclassPrepare(PyObject *metaclass, PyObject *bases, PyObject *name,
                                           PyObject *mkw, PyObject *modname, PyObject *doc) {
    PyObject *prep;
    PyObject *pargs;
    PyObject *ns;
    PyObject *str;

    prep = PyObject_GetAttrString(metaclass, (char *)"__prepare__");
    if (!prep) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError))
            return NULL;
        PyErr_Clear();
        return PyDict_New();
    }
    pargs = PyTuple_Pack(2, name, bases);
    if (!pargs) {
        Py_DECREF(prep);
        return NULL;
    }
    ns = PyObject_Call(prep, pargs, mkw);
    Py_DECREF(prep);
    Py_DECREF(pargs);

    if (ns == NULL)
        return NULL;

    /* Required here to emulate assignment order */
    /* XXX: use consts here */
    #if PY_MAJOR_VERSION >= 3
    str = PyUnicode_FromString("__module__");
    #else
    str = PyString_FromString("__module__");
    #endif
    if (!str) {
        Py_DECREF(ns);
        return NULL;
    }

    if (PyObject_SetItem(ns, str, modname) < 0) {
        Py_DECREF(ns);
        Py_DECREF(str);
        return NULL;
    }
    Py_DECREF(str);
    if (doc) {
        #if PY_MAJOR_VERSION >= 3
        str = PyUnicode_FromString("__doc__");
        #else
        str = PyString_FromString("__doc__");
        #endif
        if (!str) {
            Py_DECREF(ns);
            return NULL;
        }
        if (PyObject_SetItem(ns, str, doc) < 0) {
            Py_DECREF(ns);
            Py_DECREF(str);
            return NULL;
        }
        Py_DECREF(str);
    }
    return ns;
}

static PyObject *__Pyx_Py3ClassCreate(PyObject *metaclass, PyObject *name, PyObject *bases,
                                      PyObject *dict, PyObject *mkw) {
    PyObject *result;
    PyObject *margs = PyTuple_Pack(3, name, bases, dict);
    if (!margs)
        return NULL;
    result = PyObject_Call(metaclass, margs, mkw);
    Py_DECREF(margs);
    return result;
}

/////////////// ExtTypeTest.proto ///////////////

static CYTHON_INLINE int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/

/////////////// ExtTypeTest ///////////////

static CYTHON_INLINE int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type) {
    if (unlikely(!type)) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if (likely(PyObject_TypeCheck(obj, type)))
        return 1;
    PyErr_Format(PyExc_TypeError, "Cannot convert %.200s to %.200s",
                 Py_TYPE(obj)->tp_name, type->tp_name);
    return 0;
}

/////////////// CallableCheck.proto ///////////////

#if CYTHON_COMPILING_IN_CPYTHON && PY_MAJOR_VERSION >= 3
#define __Pyx_PyCallable_Check(obj)   ((obj)->ob_type->tp_call != NULL)
#else
#define __Pyx_PyCallable_Check(obj)   PyCallable_Check(obj)
#endif

/////////////// PyDictContains.proto ///////////////

static CYTHON_INLINE int __Pyx_PyDict_Contains(PyObject* item, PyObject* dict, int eq) {
    int result = PyDict_Contains(dict, item);
    return unlikely(result < 0) ? result : (result == (eq == Py_EQ));
}

/////////////// PySequenceContains.proto ///////////////

static CYTHON_INLINE int __Pyx_PySequence_Contains(PyObject* item, PyObject* seq, int eq) {
    int result = PySequence_Contains(seq, item);
    return unlikely(result < 0) ? result : (result == (eq == Py_EQ));
}

/////////////// PyBoolOrNullFromLong.proto ///////////////

static CYTHON_INLINE PyObject* __Pyx_PyBoolOrNull_FromLong(long b) {
    return unlikely(b < 0) ? NULL : __Pyx_PyBool_FromLong(b);
}
