
/////////////// CallNextTpDealloc.proto ///////////////

static void __Pyx_call_next_tp_dealloc(PyObject* obj, destructor current_tp_dealloc);

/////////////// CallNextTpDealloc ///////////////

static void __Pyx_call_next_tp_dealloc(PyObject* obj, destructor current_tp_dealloc) {
    PyTypeObject* type = Py_TYPE(obj);
    while (type && type->tp_dealloc != current_tp_dealloc)
        type = type->tp_base;
    if (type && type->tp_base)
        type->tp_base->tp_dealloc(obj);
}

/////////////// CallNextTpTraverse.proto ///////////////

static int __Pyx_call_next_tp_traverse(PyObject* obj, visitproc v, void *a, traverseproc current_tp_traverse);

/////////////// CallNextTpTraverse ///////////////

static int __Pyx_call_next_tp_traverse(PyObject* obj, visitproc v, void *a, traverseproc current_tp_traverse) {
    PyTypeObject* type = Py_TYPE(obj);
    while (type && type->tp_traverse != current_tp_traverse)
        type = type->tp_base;
    if (type && type->tp_base && type->tp_base->tp_traverse)
        return type->tp_base->tp_traverse(obj, v, a);
    // FIXME: really ignore?
    return 0;
}

/////////////// CallNextTpClear.proto ///////////////

static void __Pyx_call_next_tp_clear(PyObject* obj, inquiry current_tp_dealloc);

/////////////// CallNextTpClear ///////////////

static void __Pyx_call_next_tp_clear(PyObject* obj, inquiry current_tp_clear) {
    PyTypeObject* type = Py_TYPE(obj);
    while (type && type->tp_clear != current_tp_clear)
        type = type->tp_base;
    if (type && type->tp_base && type->tp_base->tp_clear)
        type->tp_base->tp_clear(obj);
}
