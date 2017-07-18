
/////////////// CallNextTpDealloc.proto ///////////////

static void __Pyx_call_next_tp_dealloc(PyObject* obj, destructor current_tp_dealloc);

/////////////// CallNextTpDealloc ///////////////

static void __Pyx_call_next_tp_dealloc(PyObject* obj, destructor current_tp_dealloc) {
    PyTypeObject* type = Py_TYPE(obj);
    /* try to find the first parent type that has a different tp_dealloc() function */
    while (type && type->tp_dealloc != current_tp_dealloc)
        type = type->tp_base;
    while (type && type->tp_dealloc == current_tp_dealloc)
        type = type->tp_base;
    if (type)
        type->tp_dealloc(obj);
}

/////////////// CallNextTpTraverse.proto ///////////////

static int __Pyx_call_next_tp_traverse(PyObject* obj, visitproc v, void *a, traverseproc current_tp_traverse);

/////////////// CallNextTpTraverse ///////////////

static int __Pyx_call_next_tp_traverse(PyObject* obj, visitproc v, void *a, traverseproc current_tp_traverse) {
    PyTypeObject* type = Py_TYPE(obj);
    /* try to find the first parent type that has a different tp_traverse() function */
    while (type && type->tp_traverse != current_tp_traverse)
        type = type->tp_base;
    while (type && type->tp_traverse == current_tp_traverse)
        type = type->tp_base;
    if (type && type->tp_traverse)
        return type->tp_traverse(obj, v, a);
    // FIXME: really ignore?
    return 0;
}

/////////////// CallNextTpClear.proto ///////////////

static void __Pyx_call_next_tp_clear(PyObject* obj, inquiry current_tp_dealloc);

/////////////// CallNextTpClear ///////////////

static void __Pyx_call_next_tp_clear(PyObject* obj, inquiry current_tp_clear) {
    PyTypeObject* type = Py_TYPE(obj);
    /* try to find the first parent type that has a different tp_clear() function */
    while (type && type->tp_clear != current_tp_clear)
        type = type->tp_base;
    while (type && type->tp_clear == current_tp_clear)
        type = type->tp_base;
    if (type && type->tp_clear)
        type->tp_clear(obj);
}

/////////////// SetupReduce.proto ///////////////

static int __Pyx_setup_reduce(PyObject* type_obj);

/////////////// SetupReduce ///////////////

#define __Pyx_setup_reduce_GET_ATTR_OR_BAD(res, obj, name) res = PyObject_GetAttrString(obj, name); if (res == NULL) goto BAD;

static int __Pyx_setup_reduce_is_named(PyObject* meth, PyObject* name) {
  int ret;
  PyObject *name_attr;

  name_attr = PyObject_GetAttrString(meth, "__name__");
  if (name_attr) {
      ret = PyObject_RichCompareBool(name_attr, name, Py_EQ);
  } else {
      ret = -1;
  }

  if (ret < 0) {
      PyErr_Clear();
      ret = 0;
  }

  Py_XDECREF(name_attr);
  return ret;
}

static int __Pyx_setup_reduce(PyObject* type_obj) {
    int ret = 0;
    PyObject* builtin_object = NULL;
    static PyObject *object_reduce = NULL;
    static PyObject *object_reduce_ex = NULL;
    PyObject *reduce = NULL;
    PyObject *reduce_ex = NULL;
    PyObject *reduce_cython = NULL;
    PyObject *setstate = NULL;
    PyObject *setstate_cython = NULL;

    if (PyObject_HasAttrString(type_obj, "__getstate__")) goto GOOD;

    if (object_reduce_ex == NULL) {
        __Pyx_setup_reduce_GET_ATTR_OR_BAD(builtin_object, __pyx_b, "object");
        __Pyx_setup_reduce_GET_ATTR_OR_BAD(object_reduce, builtin_object, "__reduce__");
        __Pyx_setup_reduce_GET_ATTR_OR_BAD(object_reduce_ex, builtin_object, "__reduce_ex__");
    }

    __Pyx_setup_reduce_GET_ATTR_OR_BAD(reduce_ex, type_obj, "__reduce_ex__");
    if (reduce_ex == object_reduce_ex) {
        __Pyx_setup_reduce_GET_ATTR_OR_BAD(reduce, type_obj, "__reduce__");
        if (object_reduce == reduce || __Pyx_setup_reduce_is_named(reduce, PYIDENT("__reduce_cython__"))) {
            __Pyx_setup_reduce_GET_ATTR_OR_BAD(reduce_cython, type_obj, "__reduce_cython__");
            ret = PyDict_SetItemString(((PyTypeObject*)type_obj)->tp_dict, "__reduce__", reduce_cython); if (ret < 0) goto BAD;
            ret = PyDict_DelItemString(((PyTypeObject*)type_obj)->tp_dict, "__reduce_cython__"); if (ret < 0) goto BAD;

            setstate = PyObject_GetAttrString(type_obj, "__setstate__");
            if (!setstate) PyErr_Clear();
            if (!setstate || __Pyx_setup_reduce_is_named(setstate, PYIDENT("__setstate_cython__"))) {
            __Pyx_setup_reduce_GET_ATTR_OR_BAD(setstate_cython, type_obj, "__setstate_cython__");
                ret = PyDict_SetItemString(((PyTypeObject*)type_obj)->tp_dict, "__setstate__", setstate_cython); if (ret < 0) goto BAD;
                ret = PyDict_DelItemString(((PyTypeObject*)type_obj)->tp_dict, "__setstate_cython__"); if (ret < 0) goto BAD;
            }
            PyType_Modified((PyTypeObject*)type_obj);
        }
    }
    goto GOOD;

BAD:
    if (!PyErr_Occurred()) PyErr_Format(PyExc_RuntimeError, "Unable to initialize pickling for %s", ((PyTypeObject*)type_obj)->tp_name);
    ret = -1;
GOOD:
    Py_XDECREF(builtin_object);
    Py_XDECREF(reduce);
    Py_XDECREF(reduce_ex);
    Py_XDECREF(reduce_cython);
    Py_XDECREF(setstate);
    Py_XDECREF(setstate_cython);
    return ret;
}
