/////////////// pop_index.proto ///////////////

static PyObject* __Pyx_PyObject_PopIndex(PyObject* L, Py_ssize_t ix);

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
