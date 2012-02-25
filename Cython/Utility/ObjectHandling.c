
/////////////// RaiseNoneAttrError.proto ///////////////

static CYTHON_INLINE void __Pyx_RaiseNoneAttributeError(const char* attrname);

/////////////// RaiseNoneAttrError ///////////////

static CYTHON_INLINE void __Pyx_RaiseNoneAttributeError(const char* attrname) {
    PyErr_Format(PyExc_AttributeError, "'NoneType' object has no attribute '%s'", attrname);
}

/////////////// RaiseNoneIndexingError.proto ///////////////

static CYTHON_INLINE void __Pyx_RaiseNoneIndexingError(void);

/////////////// RaiseNoneIndexingError ///////////////

static CYTHON_INLINE void __Pyx_RaiseNoneIndexingError(void) {
    PyErr_SetString(PyExc_TypeError, "'NoneType' object is unsubscriptable");
}

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
                 "too many values to unpack (expected %"PY_FORMAT_SIZE_T"d)", expected);
}

/////////////// RaiseNeedMoreValuesToUnpack.proto ///////////////

static CYTHON_INLINE void __Pyx_RaiseNeedMoreValuesError(Py_ssize_t index);

/////////////// RaiseNeedMoreValuesToUnpack ///////////////

static CYTHON_INLINE void __Pyx_RaiseNeedMoreValuesError(Py_ssize_t index) {
    PyErr_Format(PyExc_ValueError,
                 "need more than %"PY_FORMAT_SIZE_T"d value%s to unpack",
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

/////////////// UnpackItem.proto ///////////////

static PyObject *__Pyx_UnpackItem(PyObject *, Py_ssize_t index); /*proto*/

/////////////// UnpackItem ///////////////
//@requires: RaiseNeedMoreValuesToUnpack

static PyObject *__Pyx_UnpackItem(PyObject *iter, Py_ssize_t index) {
    PyObject *item;
    if (!(item = PyIter_Next(iter))) {
        if (!PyErr_Occurred()) {
            __Pyx_RaiseNeedMoreValuesError(index);
        }
    }
    return item;
}

/////////////// UnpackItemEndCheck.proto ///////////////

static int __Pyx_IternextUnpackEndCheck(PyObject *retval, Py_ssize_t expected); /*proto*/

/////////////// UnpackItemEndCheck ///////////////
//@requires: RaiseTooManyValuesToUnpack

static int __Pyx_IternextUnpackEndCheck(PyObject *retval, Py_ssize_t expected) {
    if (unlikely(retval)) {
        Py_DECREF(retval);
        __Pyx_RaiseTooManyValuesError(expected);
        return -1;
    } else if (PyErr_Occurred()) {
        if (likely(PyErr_ExceptionMatches(PyExc_StopIteration))) {
            PyErr_Clear();
            return 0;
        } else {
            return -1;
        }
    }
    return 0;
}

/////////////// UnpackTuple2.proto ///////////////

static CYTHON_INLINE int __Pyx_unpack_tuple2(PyObject* tuple, PyObject** value1, PyObject** value2,
                                             int is_tuple, int has_known_size, int decref_tuple);

/////////////// UnpackTuple2 ///////////////
//@requires: UnpackItem
//@requires: UnpackItemEndCheck
//@requires: UnpackTupleError

static CYTHON_INLINE int __Pyx_unpack_tuple2(PyObject* tuple, PyObject** pvalue1, PyObject** pvalue2,
                                             int is_tuple, int has_known_size, int decref_tuple) {
    PyObject *value1 = NULL, *value2 = NULL, *iter = NULL;
    if (!is_tuple && unlikely(!PyTuple_Check(tuple))) {
        iter = PyObject_GetIter(tuple);
        if (unlikely(!iter)) goto bad;
        if (decref_tuple)
            Py_DECREF(tuple);
        value1 = __Pyx_UnpackItem(iter, 0);
        if (unlikely(!value1)) goto bad;
        value2 = __Pyx_UnpackItem(iter, 1);
        if (unlikely(!value2)) goto bad;
        if (!has_known_size && unlikely(__Pyx_IternextUnpackEndCheck(PyIter_Next(iter), 2))) goto bad;
        Py_DECREF(iter);
    } else {
        if (!has_known_size && unlikely(PyTuple_GET_SIZE(tuple) != 2)) {
            __Pyx_UnpackTupleError(tuple, 2);
            goto bad;
        }
        value1 = PyTuple_GET_ITEM(tuple, 0);
        value2 = PyTuple_GET_ITEM(tuple, 1);
#if CYTHON_COMPILING_IN_CPYTHON
        if (decref_tuple) {
            PyTuple_SET_ITEM(tuple, 0, NULL);
            PyTuple_SET_ITEM(tuple, 1, NULL);
        } else
#endif
        {
            Py_INCREF(value1);
            Py_INCREF(value2);
        }
        if (decref_tuple)
            Py_DECREF(tuple);
    }
    *pvalue1 = value1;
    *pvalue2 = value2;
    return 0;
bad:
    Py_XDECREF(iter);
    Py_XDECREF(value1);
    Py_XDECREF(value2);
    if (decref_tuple) Py_DECREF(tuple);
    return -1;
}
