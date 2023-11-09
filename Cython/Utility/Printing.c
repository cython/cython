////////////////////// Print.proto //////////////////////
//@substitute: naming

static int __Pyx_Print(PyObject*, PyObject *, int); /*proto*/
static PyObject* $print_function = 0;
static PyObject* $print_function_kwargs = 0;

////////////////////// Print.cleanup //////////////////////
//@substitute: naming

Py_CLEAR($print_function);
Py_CLEAR($print_function_kwargs);

////////////////////// Print //////////////////////
//@substitute: naming

static int __Pyx_Print(PyObject* stream, PyObject *arg_tuple, int newline) {
    PyObject* kwargs = 0;
    PyObject* result = 0;
    PyObject* end_string;
    if (unlikely(!$print_function)) {
        $print_function = PyObject_GetAttr(CGLOBAL($builtins_cname), PYIDENT("print"));
        if (!$print_function)
            return -1;
    }
    if (stream) {
        kwargs = PyDict_New();
        if (unlikely(!kwargs))
            return -1;
        if (unlikely(PyDict_SetItem(kwargs, PYIDENT("file"), stream) < 0))
            goto bad;
        if (!newline) {
            end_string = PyUnicode_FromStringAndSize(" ", 1);
            if (unlikely(!end_string))
                goto bad;
            if (PyDict_SetItem(kwargs, PYIDENT("end"), end_string) < 0) {
                Py_DECREF(end_string);
                goto bad;
            }
            Py_DECREF(end_string);
        }
    } else if (!newline) {
        if (unlikely(!$print_function_kwargs)) {
            $print_function_kwargs = PyDict_New();
            if (unlikely(!$print_function_kwargs))
                return -1;
            end_string = PyUnicode_FromStringAndSize(" ", 1);
            if (unlikely(!end_string))
                return -1;
            if (PyDict_SetItem($print_function_kwargs, PYIDENT("end"), end_string) < 0) {
                Py_DECREF(end_string);
                return -1;
            }
            Py_DECREF(end_string);
        }
        kwargs = $print_function_kwargs;
    }
    result = PyObject_Call($print_function, arg_tuple, kwargs);
    if (unlikely(kwargs) && (kwargs != $print_function_kwargs))
        Py_DECREF(kwargs);
    if (!result)
        return -1;
    Py_DECREF(result);
    return 0;
bad:
    if (kwargs != $print_function_kwargs)
        Py_XDECREF(kwargs);
    return -1;
}

////////////////////// PrintOne.proto //////////////////////
//@requires: Print

static int __Pyx_PrintOne(PyObject* stream, PyObject *o); /*proto*/

////////////////////// PrintOne //////////////////////

static int __Pyx_PrintOne(PyObject* stream, PyObject *o) {
    int res;
    PyObject* arg_tuple = PyTuple_Pack(1, o);
    if (unlikely(!arg_tuple))
        return -1;
    res = __Pyx_Print(stream, arg_tuple, 1);
    Py_DECREF(arg_tuple);
    return res;
}
