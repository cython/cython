/* ========= Asynchronous Generators ========= */


typedef struct {
    PyObject_HEAD
    PyAsyncGenObject *aw_gen;
    PyObject *aw_sendval;
    int aw_state;
} PyAsyncGenASend;


typedef struct {
    PyObject_HEAD
    PyAsyncGenObject *ac_gen;
    PyObject *ac_args;
    int ac_state;
} PyAsyncGenAThrow;


typedef struct {
    PyObject_HEAD
    PyObject *val;
} _PyAsyncGenWrappedValue;


#ifndef _PyAsyncGen_MAXFREELIST
#define _PyAsyncGen_MAXFREELIST 80
#endif

/* Freelists boost performance 6-10%; they also reduce memory
   fragmentation, as _PyAsyncGenWrappedValue and PyAsyncGenASend
   are short-living objects that are instantiated for every
   __anext__ call.
*/

static _PyAsyncGenWrappedValue *ag_value_fl[_PyAsyncGen_MAXFREELIST];
static int ag_value_fl_free = 0;

static PyAsyncGenASend *ag_asend_fl[_PyAsyncGen_MAXFREELIST];
static int ag_asend_fl_free = 0;

#define _PyAsyncGenWrappedValue_CheckExact(o) \
                    (Py_TYPE(o) == &_PyAsyncGenWrappedValue_Type)

#define PyAsyncGenASend_CheckExact(o) \
                    (Py_TYPE(o) == &_PyAsyncGenASend_Type)


static int
async_gen_traverse(PyAsyncGenObject *gen, visitproc visit, void *arg)
{
    Py_VISIT(gen->ag_finalizer);
    return gen_traverse((PyGenObject*)gen, visit, arg);
}


static PyObject *
async_gen_repr(PyAsyncGenObject *o)
{
    return PyUnicode_FromFormat("<async_generator object %S at %p>",
                                o->ag_qualname, o);
}


static int
async_gen_init_finalizer(PyAsyncGenObject *o)
{
    PyThreadState *tstate;
    PyObject *finalizer;
    PyObject *firstiter;

    if (o->ag_hooks_inited) {
        return 0;
    }

    o->ag_hooks_inited = 1;

    tstate = PyThreadState_GET();

    finalizer = tstate->async_gen_finalizer;
    if (finalizer) {
        Py_INCREF(finalizer);
        o->ag_finalizer = finalizer;
    }

    firstiter = tstate->async_gen_firstiter;
    if (firstiter) {
        PyObject *res;

        Py_INCREF(firstiter);
        res = PyObject_CallFunction(firstiter, "O", o);
        Py_DECREF(firstiter);
        if (res == NULL) {
            return 1;
        }
        Py_DECREF(res);
    }

    return 0;
}


static PyObject *
async_gen_anext(PyAsyncGenObject *o)
{
    if (async_gen_init_finalizer(o)) {
        return NULL;
    }
    return async_gen_asend_new(o, NULL);
}


static PyObject *
async_gen_asend(PyAsyncGenObject *o, PyObject *arg)
{
    if (async_gen_init_finalizer(o)) {
        return NULL;
    }
    return async_gen_asend_new(o, arg);
}


static PyObject *
async_gen_aclose(PyAsyncGenObject *o, PyObject *arg)
{
    if (async_gen_init_finalizer(o)) {
        return NULL;
    }
    return async_gen_athrow_new(o, NULL);
}

static PyObject *
async_gen_athrow(PyAsyncGenObject *o, PyObject *args)
{
    if (async_gen_init_finalizer(o)) {
        return NULL;
    }
    return async_gen_athrow_new(o, args);
}


static PyGetSetDef async_gen_getsetlist[] = {
    {"__name__", (getter)gen_get_name, (setter)gen_set_name,
     PyDoc_STR("name of the async generator")},
    {"__qualname__", (getter)gen_get_qualname, (setter)gen_set_qualname,
     PyDoc_STR("qualified name of the async generator")},
    {"ag_await", (getter)coro_get_cr_await, NULL,
     PyDoc_STR("object being awaited on, or None")},
    {NULL} /* Sentinel */
};

static PyMemberDef async_gen_memberlist[] = {
    {"ag_frame",   T_OBJECT, offsetof(PyAsyncGenObject, ag_frame),   READONLY},
    {"ag_running", T_BOOL,   offsetof(PyAsyncGenObject, ag_running), READONLY},
    {"ag_code",    T_OBJECT, offsetof(PyAsyncGenObject, ag_code),    READONLY},
    {NULL}      /* Sentinel */
};

PyDoc_STRVAR(async_aclose_doc,
"aclose() -> raise GeneratorExit inside generator.");

PyDoc_STRVAR(async_asend_doc,
"asend(v) -> send 'v' in generator.");

PyDoc_STRVAR(async_athrow_doc,
"athrow(typ[,val[,tb]]) -> raise exception in generator.");

static PyMethodDef async_gen_methods[] = {
    {"asend", (PyCFunction)async_gen_asend, METH_O, async_asend_doc},
    {"athrow",(PyCFunction)async_gen_athrow, METH_VARARGS, async_athrow_doc},
    {"aclose", (PyCFunction)async_gen_aclose, METH_NOARGS, async_aclose_doc},
    {NULL, NULL}        /* Sentinel */
};


static PyAsyncMethods async_gen_as_async = {
    0,                                          /* am_await */
    PyObject_SelfIter,                          /* am_aiter */
    (unaryfunc)async_gen_anext                  /* am_anext */
};


PyTypeObject PyAsyncGen_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator",                          /* tp_name */
    sizeof(PyAsyncGenObject),                   /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)gen_dealloc,                    /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    &async_gen_as_async,                        /* tp_as_async */
    (reprfunc)async_gen_repr,                   /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC |
        Py_TPFLAGS_HAVE_FINALIZE,               /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)async_gen_traverse,           /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    offsetof(PyAsyncGenObject, ag_weakreflist), /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    async_gen_methods,                          /* tp_methods */
    async_gen_memberlist,                       /* tp_members */
    async_gen_getsetlist,                       /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
    0,                                          /* tp_free */
    0,                                          /* tp_is_gc */
    0,                                          /* tp_bases */
    0,                                          /* tp_mro */
    0,                                          /* tp_cache */
    0,                                          /* tp_subclasses */
    0,                                          /* tp_weaklist */
    0,                                          /* tp_del */
    0,                                          /* tp_version_tag */
    _PyGen_Finalize,                            /* tp_finalize */
};


PyObject *
PyAsyncGen_New(PyFrameObject *f, PyObject *name, PyObject *qualname)
{
    PyAsyncGenObject *o;
    o = (PyAsyncGenObject *)gen_new_with_qualname(
        &PyAsyncGen_Type, f, name, qualname);
    if (o == NULL) {
        return NULL;
    }
    o->ag_finalizer = NULL;
    o->ag_closed = 0;
    o->ag_hooks_inited = 0;
    return (PyObject*)o;
}


int
PyAsyncGen_ClearFreeLists(void)
{
    int ret = ag_value_fl_free + ag_asend_fl_free;

    while (ag_value_fl_free) {
        _PyAsyncGenWrappedValue *o;
        o = ag_value_fl[--ag_value_fl_free];
        assert(_PyAsyncGenWrappedValue_CheckExact(o));
        PyObject_Del(o);
    }

    while (ag_asend_fl_free) {
        PyAsyncGenASend *o;
        o = ag_asend_fl[--ag_asend_fl_free];
        assert(Py_TYPE(o) == &_PyAsyncGenASend_Type);
        PyObject_Del(o);
    }

    return ret;
}

void
PyAsyncGen_Fini(void)
{
    PyAsyncGen_ClearFreeLists();
}


static PyObject *
async_gen_unwrap_value(PyAsyncGenObject *gen, PyObject *result)
{
    if (result == NULL) {
        if (!PyErr_Occurred()) {
            PyErr_SetNone(PyExc_StopAsyncIteration);
        }

        if (PyErr_ExceptionMatches(PyExc_StopAsyncIteration)
            || PyErr_ExceptionMatches(PyExc_GeneratorExit)
        ) {
            gen->ag_closed = 1;
        }

        return NULL;
    }

    if (_PyAsyncGenWrappedValue_CheckExact(result)) {
        /* async yield */
        PyObject *e = PyObject_CallFunctionObjArgs(
            PyExc_StopIteration,
            ((_PyAsyncGenWrappedValue*)result)->val,
            NULL);
        Py_DECREF(result);
        PyErr_SetObject(PyExc_StopIteration, e);
        Py_DECREF(e);
        return NULL;
    }

    return result;
}


/* ---------- Async Generator ASend Awaitable ------------ */


static void
async_gen_asend_dealloc(PyAsyncGenASend *o)
{
    Py_CLEAR(o->aw_gen);
    Py_CLEAR(o->aw_sendval);
    if (ag_asend_fl_free < _PyAsyncGen_MAXFREELIST) {
        assert(PyAsyncGenASend_CheckExact(o));
        ag_asend_fl[ag_asend_fl_free++] = o;
    } else {
        PyObject_Del(o);
    }
}


static PyObject *
async_gen_asend_send(PyAsyncGenASend *o, PyObject *arg)
{
    PyObject *result;

    if (o->aw_state == 2) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    if (o->aw_state == 0) {
        if (arg == NULL || arg == Py_None) {
            arg = o->aw_sendval;
        }
        o->aw_state = 1;
    }

    result = gen_send_ex((PyGenObject*)o->aw_gen, arg, 0, 0);
    result = async_gen_unwrap_value(o->aw_gen, result);

    if (result == NULL) {
        o->aw_state = 2;
    }

    return result;
}


static PyObject *
async_gen_asend_iternext(PyAsyncGenASend *o)
{
    return async_gen_asend_send(o, NULL);
}


static PyObject *
async_gen_asend_throw(PyAsyncGenASend *o, PyObject *args)
{
    PyObject *result;

    if (o->aw_state == 2) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    result = gen_throw((PyGenObject*)o->aw_gen, args);
    result = async_gen_unwrap_value(o->aw_gen, result);

    if (result == NULL) {
        o->aw_state = 2;
    }

    return result;
}


static PyObject *
async_gen_asend_close(PyAsyncGenASend *o, PyObject *args)
{
    o->aw_state = 2;
    Py_RETURN_NONE;
}


static PyMethodDef async_gen_asend_methods[] = {
    {"send", (PyCFunction)async_gen_asend_send, METH_O, send_doc},
    {"throw", (PyCFunction)async_gen_asend_throw, METH_VARARGS, throw_doc},
    {"close", (PyCFunction)async_gen_asend_close, METH_NOARGS, close_doc},
    {NULL, NULL}        /* Sentinel */
};


static PyAsyncMethods async_gen_asend_as_async = {
    PyObject_SelfIter,                          /* am_await */
    0,                                          /* am_aiter */
    0                                           /* am_anext */
};


PyTypeObject _PyAsyncGenASend_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator_asend",                    /* tp_name */
    sizeof(PyAsyncGenASend),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)async_gen_asend_dealloc,        /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    &async_gen_asend_as_async,                  /* tp_as_async */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    0,                                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)async_gen_asend_iternext,     /* tp_iternext */
    async_gen_asend_methods,                    /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


static PyObject *
async_gen_asend_new(PyAsyncGenObject *gen, PyObject *sendval)
{
    PyAsyncGenASend *o;
    if (ag_asend_fl_free) {
        ag_asend_fl_free--;
        o = ag_asend_fl[ag_asend_fl_free];
        _Py_NewReference((PyObject *)o);
    } else {
        o = PyObject_New(PyAsyncGenASend, &_PyAsyncGenASend_Type);
        if (o == NULL) {
            return NULL;
        }
    }
    o->aw_gen = gen;
    o->aw_state = 0;
    o->aw_sendval = sendval;
    Py_XINCREF(sendval);
    Py_INCREF(gen);
    return (PyObject*)o;
}


/* ---------- Async Generator Value Wrapper ------------ */


static void
async_gen_wrapped_val_dealloc(_PyAsyncGenWrappedValue *o)
{
    Py_CLEAR(o->val);
    if (ag_value_fl_free < _PyAsyncGen_MAXFREELIST) {
        assert(_PyAsyncGenWrappedValue_CheckExact(o));
        ag_value_fl[ag_value_fl_free++] = o;
    } else {
        PyObject_Del(o);
    }
}


PyTypeObject _PyAsyncGenWrappedValue_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator_wrapped_value",            /* tp_name */
    sizeof(_PyAsyncGenWrappedValue),            /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)async_gen_wrapped_val_dealloc,  /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_as_async */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    0,                                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    0,                                          /* tp_methods */
    0,                                          /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


PyObject *
_PyAsyncGenWrapValue(PyObject *val)
{
    _PyAsyncGenWrappedValue *o;
    assert(val);

    if (ag_value_fl_free) {
        ag_value_fl_free--;
        o = ag_value_fl[ag_value_fl_free];
        assert(_PyAsyncGenWrappedValue_CheckExact(o));
        _Py_NewReference((PyObject*)o);
    } else {
        o = PyObject_New(_PyAsyncGenWrappedValue, &_PyAsyncGenWrappedValue_Type);
        if (o == NULL) {
            return NULL;
        }
    }
    o->val = val;
    Py_INCREF(val);
    return (PyObject*)o;
}


/* ---------- Async Generator AThrow awaitable ------------ */


static void
async_gen_athrow_dealloc(PyAsyncGenAThrow *o)
{
    Py_CLEAR(o->ac_gen);
    Py_CLEAR(o->ac_args);
    PyObject_Del(o);
}


static PyObject *
async_gen_athrow_send(PyAsyncGenAThrow *o, PyObject *arg)
{
    PyGenObject *gen = (PyGenObject*)o->ac_gen;
    PyFrameObject *f = gen->gi_frame;
    PyObject *retval;

    if (f == NULL || f->f_stacktop == NULL || o->ac_state == 2) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    if (o->ac_state == 0) {
        if (o->ac_gen->ag_closed) {
            PyErr_SetNone(PyExc_StopIteration);
            return NULL;
        }

        if (arg != Py_None) {
            PyErr_SetString(PyExc_RuntimeError, NON_INIT_CORO_MSG);
            return NULL;
        }

        o->ac_state = 1;

        if (o->ac_args == NULL) {
            /* aclose() mode */
            o->ac_gen->ag_closed = 1;

            retval = _gen_throw((PyGenObject *)gen,
                                0,  /* Do not close generator when
                                       PyExc_GeneratorExit is passed */
                                PyExc_GeneratorExit, NULL, NULL);

            if (retval && _PyAsyncGenWrappedValue_CheckExact(retval)) {
                Py_DECREF(retval);
                goto yield_close;
            }
        } else {
            PyObject *typ;
            PyObject *tb = NULL;
            PyObject *val = NULL;

            if (!PyArg_UnpackTuple(o->ac_args, "athrow", 1, 3,
                                   &typ, &val, &tb)) {
                return NULL;
            }

            retval = _gen_throw((PyGenObject *)gen,
                                0,  /* Do not close generator when
                                       PyExc_GeneratorExit is passed */
                                typ, val, tb);
            retval = async_gen_unwrap_value(o->ac_gen, retval);
        }
        if (retval == NULL) {
            goto check_error;
        }
        return retval;
    }

    if (o->ac_state == 1) {
        PyObject *retval = gen_send_ex((PyGenObject *)gen, arg, 0, 0);
        if (o->ac_args) {
            return async_gen_unwrap_value(o->ac_gen, retval);
        } else {
            /* aclose() mode */
            if (retval && _PyAsyncGenWrappedValue_CheckExact(retval)) {
                Py_DECREF(retval);
                goto yield_close;
            }
            if (retval == NULL) {
                goto check_error;
            }
            return retval;
        }
    }

    return NULL;

yield_close:
    PyErr_SetString(
        PyExc_RuntimeError, ASYNC_GEN_IGNORED_EXIT_MSG);
    return NULL;

check_error:
    if (PyErr_ExceptionMatches(PyExc_StopAsyncIteration)
        || PyErr_ExceptionMatches(PyExc_GeneratorExit)
    ) {
        o->ac_state = 2;
        PyErr_Clear();          /* ignore these errors */
        PyErr_SetNone(PyExc_StopIteration);
    }
    return NULL;
}


static PyObject *
async_gen_athrow_throw(PyAsyncGenAThrow *o, PyObject *args)
{
    PyObject *retval;

    if (o->ac_state == 0) {
        PyErr_SetString(PyExc_RuntimeError, NON_INIT_CORO_MSG);
        return NULL;
    }

    if (o->ac_state == 2) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    retval = gen_throw((PyGenObject*)o->ac_gen, args);
    if (o->ac_args) {
        return async_gen_unwrap_value(o->ac_gen, retval);
    } else {
        /* aclose() mode */
        if (retval && _PyAsyncGenWrappedValue_CheckExact(retval)) {
            Py_DECREF(retval);
            PyErr_SetString(PyExc_RuntimeError, ASYNC_GEN_IGNORED_EXIT_MSG);
            return NULL;
        }
        return retval;
    }
}


static PyObject *
async_gen_athrow_iternext(PyAsyncGenAThrow *o)
{
    return async_gen_athrow_send(o, Py_None);
}


static PyObject *
async_gen_athrow_close(PyAsyncGenAThrow *o, PyObject *args)
{
    o->ac_state = 2;
    Py_RETURN_NONE;
}


static PyMethodDef async_gen_athrow_methods[] = {
    {"send", (PyCFunction)async_gen_athrow_send, METH_O, send_doc},
    {"throw", (PyCFunction)async_gen_athrow_throw, METH_VARARGS, throw_doc},
    {"close", (PyCFunction)async_gen_athrow_close, METH_NOARGS, close_doc},
    {NULL, NULL}        /* Sentinel */
};


static PyAsyncMethods async_gen_athrow_as_async = {
    PyObject_SelfIter,                          /* am_await */
    0,                                          /* am_aiter */
    0                                           /* am_anext */
};


PyTypeObject _PyAsyncGenAThrow_Type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator_athrow",                   /* tp_name */
    sizeof(PyAsyncGenAThrow),                   /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)async_gen_athrow_dealloc,       /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    &async_gen_athrow_as_async,                 /* tp_as_async */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    0,                                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)async_gen_athrow_iternext,    /* tp_iternext */
    async_gen_athrow_methods,                   /* tp_members */
    0,                                          /* tp_getset */
    0,                                          /* tp_base */
    0,                                          /* tp_dict */
    0,                                          /* tp_descr_get */
    0,                                          /* tp_descr_set */
    0,                                          /* tp_dictoffset */
    0,                                          /* tp_init */
    0,                                          /* tp_alloc */
    0,                                          /* tp_new */
};


static PyObject *
async_gen_athrow_new(PyAsyncGenObject *gen, PyObject *args)
{
    PyAsyncGenAThrow *o;
    o = PyObject_New(PyAsyncGenAThrow, &_PyAsyncGenAThrow_Type);
    if (o == NULL) {
        return NULL;
    }
    o->ac_gen = gen;
    o->ac_args = args;
    o->ac_state = 0;
    Py_INCREF(gen);
    Py_XINCREF(args);
    return (PyObject*)o;
}
