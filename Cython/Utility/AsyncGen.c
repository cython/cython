// This is copied from genobject.c in CPython 3.6.
// Try to keep it in sync.

//////////////////// AsyncGenerator.proto ////////////////////
//@requires: Coroutine.c::Coroutine

#define __Pyx_AsyncGen_USED
typedef struct {
    __pyx_CoroutineObject coro;
    PyObject *ag_finalizer;
    int ag_hooks_inited;
    int ag_closed;
} __pyx_AsyncGenObject;


static PyTypeObject *__pyx__PyAsyncGenWrappedValueType = 0;
static PyTypeObject *__pyx__PyAsyncGenASendType = 0;
static PyTypeObject *__pyx__PyAsyncGenAThrowType = 0;
static PyTypeObject *__pyx_AsyncGenType = 0;
#define __Pyx_AsyncGen_CheckExact(obj) (Py_TYPE(obj) == __pyx_AsyncGenType)


static __pyx_CoroutineObject *__Pyx_AsyncGen_New(
            __pyx_coroutine_body_t body, PyObject *closure,
            PyObject *name, PyObject *qualname, PyObject *module_name) {
    __pyx_AsyncGenObject *gen = PyObject_GC_New(__pyx_AsyncGenObject, __pyx_AsyncGenType);
    if (unlikely(!gen))
        return NULL;
    gen->ag_finalizer = NULL;
    gen->ag_hooks_inited = 0;
    gen->ag_closed = 0;
    return __Pyx__Coroutine_NewInit((__pyx_CoroutineObject*)gen, body, closure, name, qualname, module_name);
}

static int __pyx_AsyncGen_init(void);


//////////////////// AsyncGeneratorInitFinalizer ////////////////////

// this is separated out because it needs more adaptation

#if PY_VERSION_HEX < 0x030600B0
static int __Pyx_async_gen_init_finalizer(__pyx_AsyncGenObject *o) {
#if 0
    // TODO: implement finalizer support in older Python versions
    PyThreadState *tstate;
    PyObject *finalizer;
    PyObject *firstiter;
#endif

    if (likely(o->ag_hooks_inited)) {
        return 0;
    }

    o->ag_hooks_inited = 1;

#if 0
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
        res = __Pyx_PyObject_CallOneArg(firstiter, (PyObject*)o);
        Py_DECREF(firstiter);
        if (res == NULL) {
            return 1;
        }
        Py_DECREF(res);
    }
#endif

    return 0;
}
#endif


//////////////////// AsyncGenerator ////////////////////
//@requires: AsyncGeneratorInitFinalizer
//@requires: Coroutine.c::Coroutine


PyDoc_STRVAR(__Pyx_async_gen_send_doc,
"send(arg) -> send 'arg' into generator,\n\
return next yielded value or raise StopIteration.");

PyDoc_STRVAR(__Pyx_async_gen_close_doc,
"close() -> raise GeneratorExit inside generator.");

PyDoc_STRVAR(__Pyx_async_gen_throw_doc,
"throw(typ[,val[,tb]]) -> raise exception in generator,\n\
return next yielded value or raise StopIteration.");

// COPY STARTS HERE:

static PyObject *__Pyx_async_gen_asend_new(__pyx_AsyncGenObject *, PyObject *);
static PyObject *__Pyx_async_gen_athrow_new(__pyx_AsyncGenObject *, PyObject *);

static const char *__Pyx_NON_INIT_CORO_MSG = "can't send non-None value to a just-started coroutine";
static const char *__Pyx_ASYNC_GEN_IGNORED_EXIT_MSG = "async generator ignored GeneratorExit";

typedef struct {
    PyObject_HEAD
    __pyx_AsyncGenObject *aw_gen;
    PyObject *aw_sendval;
    int aw_state;
} __pyx_PyAsyncGenASend;


typedef struct {
    PyObject_HEAD
    __pyx_AsyncGenObject *ac_gen;
    PyObject *ac_args;
    int ac_state;
} __pyx_PyAsyncGenAThrow;


typedef struct {
    PyObject_HEAD
    PyObject *val;
} __pyx__PyAsyncGenWrappedValue;


#ifndef _PyAsyncGen_MAXFREELIST
#define _PyAsyncGen_MAXFREELIST 80
#endif

/* Freelists boost performance 6-10%; they also reduce memory
   fragmentation, as _PyAsyncGenWrappedValue and PyAsyncGenASend
   are short-living objects that are instantiated for every
   __anext__ call.
*/

static __pyx__PyAsyncGenWrappedValue *__Pyx_ag_value_fl[_PyAsyncGen_MAXFREELIST];
static int __Pyx_ag_value_fl_free = 0;

static __pyx_PyAsyncGenASend *__Pyx_ag_asend_fl[_PyAsyncGen_MAXFREELIST];
static int __Pyx_ag_asend_fl_free = 0;

#define __pyx__PyAsyncGenWrappedValue_CheckExact(o) \
                    (Py_TYPE(o) == __pyx__PyAsyncGenWrappedValueType)

#define __pyx_PyAsyncGenASend_CheckExact(o) \
                    (Py_TYPE(o) == __pyx__PyAsyncGenASendType)


static int
__Pyx_async_gen_traverse(__pyx_AsyncGenObject *gen, visitproc visit, void *arg)
{
    Py_VISIT(gen->ag_finalizer);
    return __Pyx_Coroutine_traverse((__pyx_CoroutineObject*)gen, visit, arg);
}


static PyObject *
__Pyx_async_gen_repr(__pyx_CoroutineObject *o)
{
    return PyUnicode_FromFormat("<async_generator object %S at %p>",
                                o->gi_qualname, o);
}


#if PY_VERSION_HEX >= 0x030600B0
static int
__Pyx_async_gen_init_finalizer(__pyx_AsyncGenObject *o)
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
        res = __Pyx_PyObject_CallOneArg(firstiter, (PyObject*)o);
        Py_DECREF(firstiter);
        if (res == NULL) {
            return 1;
        }
        Py_DECREF(res);
    }

    return 0;
}
#endif


static PyObject *
__Pyx_async_gen_anext(__pyx_AsyncGenObject *o)
{
    if (__Pyx_async_gen_init_finalizer(o)) {
        return NULL;
    }
    return __Pyx_async_gen_asend_new(o, NULL);
}


static PyObject *
__Pyx_async_gen_asend(__pyx_AsyncGenObject *o, PyObject *arg)
{
    if (__Pyx_async_gen_init_finalizer(o)) {
        return NULL;
    }
    return __Pyx_async_gen_asend_new(o, arg);
}


static PyObject *
__Pyx_async_gen_aclose(__pyx_AsyncGenObject *o, CYTHON_UNUSED PyObject *arg)
{
    if (__Pyx_async_gen_init_finalizer(o)) {
        return NULL;
    }
    return __Pyx_async_gen_athrow_new(o, NULL);
}

static PyObject *
__Pyx_async_gen_athrow(__pyx_AsyncGenObject *o, PyObject *args)
{
    if (__Pyx_async_gen_init_finalizer(o)) {
        return NULL;
    }
    return __Pyx_async_gen_athrow_new(o, args);
}


static PyGetSetDef __Pyx_async_gen_getsetlist[] = {
    {"__name__", (getter)__Pyx_Coroutine_get_name, (setter)__Pyx_Coroutine_set_name,
     PyDoc_STR("name of the async generator"), 0},
    {"__qualname__", (getter)__Pyx_Coroutine_get_qualname, (setter)__Pyx_Coroutine_set_qualname,
     PyDoc_STR("qualified name of the async generator"), 0},
    //REMOVED: {"ag_await", (getter)coro_get_cr_await, NULL,
    //REMOVED:  PyDoc_STR("object being awaited on, or None")},
    {0, 0, 0, 0, 0} /* Sentinel */
};

static PyMemberDef __Pyx_async_gen_memberlist[] = {
    //REMOVED: {"ag_frame",   T_OBJECT, offsetof(__pyx_AsyncGenObject, ag_frame),   READONLY},
    {"ag_running", T_BOOL,   offsetof(__pyx_CoroutineObject, is_running), READONLY, NULL},
    //REMOVED: {"ag_code",    T_OBJECT, offsetof(__pyx_AsyncGenObject, ag_code),    READONLY},
    //ADDED: "ag_await"
    {(char*) "ag_await", T_OBJECT, offsetof(__pyx_CoroutineObject, yieldfrom), READONLY,
     (char*) PyDoc_STR("object being awaited on, or None")},
    {0, 0, 0, 0, 0}      /* Sentinel */
};

PyDoc_STRVAR(__Pyx_async_aclose_doc,
"aclose() -> raise GeneratorExit inside generator.");

PyDoc_STRVAR(__Pyx_async_asend_doc,
"asend(v) -> send 'v' in generator.");

PyDoc_STRVAR(__Pyx_async_athrow_doc,
"athrow(typ[,val[,tb]]) -> raise exception in generator.");

static PyMethodDef __Pyx_async_gen_methods[] = {
    {"asend", (PyCFunction)__Pyx_async_gen_asend, METH_O, __Pyx_async_asend_doc},
    {"athrow",(PyCFunction)__Pyx_async_gen_athrow, METH_VARARGS, __Pyx_async_athrow_doc},
    {"aclose", (PyCFunction)__Pyx_async_gen_aclose, METH_NOARGS, __Pyx_async_aclose_doc},
    {0, 0, 0, 0}        /* Sentinel */
};


static PyAsyncMethods __Pyx_async_gen_as_async = {
    0,                                          /* am_await */
    PyObject_SelfIter,                          /* am_aiter */
    (unaryfunc)__Pyx_async_gen_anext            /* am_anext */
};


PyTypeObject __pyx_AsyncGenType_type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator",                          /* tp_name */
    sizeof(__pyx_AsyncGenObject),                   /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)__Pyx_Coroutine_check_and_dealloc,                    /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
#if CYTHON_USE_ASYNC_SLOTS
    &__Pyx_async_gen_as_async,                        /* tp_as_async */
#else
    0,                                          /*tp_reserved*/
#endif
    (reprfunc)__Pyx_async_gen_repr,                   /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_HAVE_FINALIZE,               /* tp_flags */
    0,                                          /* tp_doc */
    (traverseproc)__Pyx_async_gen_traverse,           /* tp_traverse */
    0,                                          /* tp_clear */
#if CYTHON_USE_ASYNC_SLOTS && CYTHON_COMPILING_IN_CPYTHON && PY_MAJOR_VERSION >= 3 && PY_VERSION_HEX < 0x030500B1
    // in order to (mis-)use tp_reserved above, we must also implement tp_richcompare
    __Pyx_Coroutine_compare,            /*tp_richcompare*/
#else
    0,                                  /*tp_richcompare*/
#endif
    offsetof(__pyx_CoroutineObject, gi_weakreflist), /* tp_weaklistoffset */
    0,                                          /* tp_iter */
    0,                                          /* tp_iternext */
    __Pyx_async_gen_methods,                          /* tp_methods */
    __Pyx_async_gen_memberlist,                       /* tp_members */
    __Pyx_async_gen_getsetlist,                       /* tp_getset */
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
#if PY_VERSION_HEX >= 0x030400a1
    0,                                  /*tp_del*/
#else
    __Pyx_Coroutine_del,                /*tp_del*/
#endif
    0,                                          /* tp_version_tag */
#if PY_VERSION_HEX >= 0x030400a1
    __Pyx_Coroutine_del,                        /* tp_finalize */
#endif
};


static int
__Pyx_PyAsyncGen_ClearFreeLists(void)
{
    int ret = __Pyx_ag_value_fl_free + __Pyx_ag_asend_fl_free;

    while (__Pyx_ag_value_fl_free) {
        __pyx__PyAsyncGenWrappedValue *o;
        o = __Pyx_ag_value_fl[--__Pyx_ag_value_fl_free];
        assert(__pyx__PyAsyncGenWrappedValue_CheckExact(o));
        PyObject_Del(o);
    }

    while (__Pyx_ag_asend_fl_free) {
        __pyx_PyAsyncGenASend *o;
        o = __Pyx_ag_asend_fl[--__Pyx_ag_asend_fl_free];
        assert(Py_TYPE(o) == __pyx__PyAsyncGenASendType);
        PyObject_Del(o);
    }

    return ret;
}

static void
__Pyx_PyAsyncGen_Fini(void)
{
    __Pyx_PyAsyncGen_ClearFreeLists();
}


static PyObject *
__Pyx_async_gen_unwrap_value(__pyx_AsyncGenObject *gen, PyObject *result)
{
    if (result == NULL) {
        if (!PyErr_Occurred()) {
            PyErr_SetNone(__Pyx_PyExc_StopAsyncIteration);
        }

        if (PyErr_ExceptionMatches(__Pyx_PyExc_StopAsyncIteration)
            || PyErr_ExceptionMatches(PyExc_GeneratorExit)
        ) {
            gen->ag_closed = 1;
        }

        return NULL;
    }

    if (__pyx__PyAsyncGenWrappedValue_CheckExact(result)) {
        /* async yield */
        PyObject *e = __Pyx_PyObject_CallOneArg(
            PyExc_StopIteration,
            ((__pyx__PyAsyncGenWrappedValue*)result)->val);
        Py_DECREF(result);
        PyErr_SetObject(PyExc_StopIteration, e);
        Py_DECREF(e);
        return NULL;
    }

    return result;
}


/* ---------- Async Generator ASend Awaitable ------------ */


static void
__Pyx_async_gen_asend_dealloc(__pyx_PyAsyncGenASend *o)
{
    Py_CLEAR(o->aw_gen);
    Py_CLEAR(o->aw_sendval);
    if (__Pyx_ag_asend_fl_free < _PyAsyncGen_MAXFREELIST) {
        assert(__pyx_PyAsyncGenASend_CheckExact(o));
        __Pyx_ag_asend_fl[__Pyx_ag_asend_fl_free++] = o;
    } else {
        PyObject_Del(o);
    }
}


static PyObject *
__Pyx_async_gen_asend_send(__pyx_PyAsyncGenASend *o, PyObject *arg)
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

    result = __Pyx_Coroutine_SendEx((__pyx_CoroutineObject*)o->aw_gen, arg);
    result = __Pyx_async_gen_unwrap_value(o->aw_gen, result);

    if (result == NULL) {
        o->aw_state = 2;
    }

    return result;
}


static PyObject *
__Pyx_async_gen_asend_iternext(__pyx_PyAsyncGenASend *o)
{
    return __Pyx_async_gen_asend_send(o, NULL);
}


static PyObject *
__Pyx_async_gen_asend_throw(__pyx_PyAsyncGenASend *o, PyObject *args)
{
    PyObject *result;

    if (o->aw_state == 2) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    result = __Pyx_Coroutine_Throw((PyObject*)o->aw_gen, args);
    result = __Pyx_async_gen_unwrap_value(o->aw_gen, result);

    if (result == NULL) {
        o->aw_state = 2;
    }

    return result;
}


static PyObject *
__Pyx_async_gen_asend_close(__pyx_PyAsyncGenASend *o, CYTHON_UNUSED PyObject *args)
{
    o->aw_state = 2;
    Py_RETURN_NONE;
}


static PyMethodDef __Pyx_async_gen_asend_methods[] = {
    {"send", (PyCFunction)__Pyx_async_gen_asend_send, METH_O, __Pyx_async_gen_send_doc},
    {"throw", (PyCFunction)__Pyx_async_gen_asend_throw, METH_VARARGS, __Pyx_async_gen_throw_doc},
    {"close", (PyCFunction)__Pyx_async_gen_asend_close, METH_NOARGS, __Pyx_async_gen_close_doc},
    {0, 0, 0, 0}        /* Sentinel */
};


static PyAsyncMethods __Pyx_async_gen_asend_as_async = {
    PyObject_SelfIter,                          /* am_await */
    0,                                          /* am_aiter */
    0                                           /* am_anext */
};


PyTypeObject __pyx__PyAsyncGenASendType_type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator_asend",                    /* tp_name */
    sizeof(__pyx_PyAsyncGenASend),                    /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)__Pyx_async_gen_asend_dealloc,        /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
#if CYTHON_USE_ASYNC_SLOTS
    &__Pyx_async_gen_asend_as_async,                  /* tp_as_async */
#else
    0,                                          /*tp_reserved*/
#endif
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    0,                                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
#if CYTHON_USE_ASYNC_SLOTS && CYTHON_COMPILING_IN_CPYTHON && PY_MAJOR_VERSION >= 3 && PY_VERSION_HEX < 0x030500B1
    // in order to (mis-)use tp_reserved above, we must also implement tp_richcompare
    __Pyx_Coroutine_compare,            /*tp_richcompare*/
#else
    0,                                  /*tp_richcompare*/
#endif
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)__Pyx_async_gen_asend_iternext,     /* tp_iternext */
    __Pyx_async_gen_asend_methods,                    /* tp_methods */
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
    0,                                          /* tp_free */
    0,                                          /* tp_is_gc */
    0,                                          /* tp_bases */
    0,                                          /* tp_mro */
    0,                                          /* tp_cache */
    0,                                          /* tp_subclasses */
    0,                                          /* tp_weaklist */
    0,                                          /* tp_del */
    0,                                          /* tp_version_tag */
#if PY_VERSION_HEX >= 0x030400a1
    0,                                          /* tp_finalize */
#endif
};


static PyObject *
__Pyx_async_gen_asend_new(__pyx_AsyncGenObject *gen, PyObject *sendval)
{
    __pyx_PyAsyncGenASend *o;
    if (__Pyx_ag_asend_fl_free) {
        __Pyx_ag_asend_fl_free--;
        o = __Pyx_ag_asend_fl[__Pyx_ag_asend_fl_free];
        _Py_NewReference((PyObject *)o);
    } else {
        o = PyObject_New(__pyx_PyAsyncGenASend, __pyx__PyAsyncGenASendType);
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
__Pyx_async_gen_wrapped_val_dealloc(__pyx__PyAsyncGenWrappedValue *o)
{
    Py_CLEAR(o->val);
    if (__Pyx_ag_value_fl_free < _PyAsyncGen_MAXFREELIST) {
        assert(__pyx__PyAsyncGenWrappedValue_CheckExact(o));
        __Pyx_ag_value_fl[__Pyx_ag_value_fl_free++] = o;
    } else {
        PyObject_Del(o);
    }
}


PyTypeObject __pyx__PyAsyncGenWrappedValueType_type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator_wrapped_value",            /* tp_name */
    sizeof(__pyx__PyAsyncGenWrappedValue),            /* tp_basicsize */
    0,                                          /* tp_itemsize */
    /* methods */
    (destructor)__Pyx_async_gen_wrapped_val_dealloc,  /* tp_dealloc */
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
    0,                                          /* tp_getattro */
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
    0,                                          /* tp_free */
    0,                                          /* tp_is_gc */
    0,                                          /* tp_bases */
    0,                                          /* tp_mro */
    0,                                          /* tp_cache */
    0,                                          /* tp_subclasses */
    0,                                          /* tp_weaklist */
    0,                                          /* tp_del */
    0,                                          /* tp_version_tag */
#if PY_VERSION_HEX >= 0x030400a1
    0,                                          /* tp_finalize */
#endif
};


static PyObject *
__pyx__PyAsyncGenWrapValue(PyObject *val)
{
    __pyx__PyAsyncGenWrappedValue *o;
    assert(val);

    if (__Pyx_ag_value_fl_free) {
        __Pyx_ag_value_fl_free--;
        o = __Pyx_ag_value_fl[__Pyx_ag_value_fl_free];
        assert(__pyx__PyAsyncGenWrappedValue_CheckExact(o));
        _Py_NewReference((PyObject*)o);
    } else {
        o = PyObject_New(__pyx__PyAsyncGenWrappedValue, __pyx__PyAsyncGenWrappedValueType);
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
__Pyx_async_gen_athrow_dealloc(__pyx_PyAsyncGenAThrow *o)
{
    Py_CLEAR(o->ac_gen);
    Py_CLEAR(o->ac_args);
    PyObject_Del(o);
}


static PyObject *
__Pyx_async_gen_athrow_send(__pyx_PyAsyncGenAThrow *o, PyObject *arg)
{
    __pyx_CoroutineObject *gen = (__pyx_CoroutineObject*)o->ac_gen;
    PyObject *retval;

    if (o->ac_state == 2) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    if (o->ac_state == 0) {
        if (o->ac_gen->ag_closed) {
            PyErr_SetNone(PyExc_StopIteration);
            return NULL;
        }

        if (arg != Py_None) {
            PyErr_SetString(PyExc_RuntimeError, __Pyx_NON_INIT_CORO_MSG);
            return NULL;
        }

        o->ac_state = 1;

        if (o->ac_args == NULL) {
            /* aclose() mode */
            o->ac_gen->ag_closed = 1;

            retval = __Pyx__Coroutine_Throw((PyObject*)gen,
                                /* Do not close generator when
                                   PyExc_GeneratorExit is passed */
                                PyExc_GeneratorExit, NULL, NULL, NULL, 0);

            if (retval && __pyx__PyAsyncGenWrappedValue_CheckExact(retval)) {
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

            retval = __Pyx__Coroutine_Throw((PyObject*)gen,
                                /* Do not close generator when
                                   PyExc_GeneratorExit is passed */
                                typ, val, tb, o->ac_args, 0);
            retval = __Pyx_async_gen_unwrap_value(o->ac_gen, retval);
        }
        if (retval == NULL) {
            goto check_error;
        }
        return retval;
    }

    if (o->ac_state == 1) {
        PyObject *retval = __Pyx_Coroutine_SendEx((__pyx_CoroutineObject *)gen, arg);
        if (o->ac_args) {
            return __Pyx_async_gen_unwrap_value(o->ac_gen, retval);
        } else {
            /* aclose() mode */
            if (retval && __pyx__PyAsyncGenWrappedValue_CheckExact(retval)) {
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
        PyExc_RuntimeError, __Pyx_ASYNC_GEN_IGNORED_EXIT_MSG);
    return NULL;

check_error:
    if (PyErr_ExceptionMatches(__Pyx_PyExc_StopAsyncIteration)
        || PyErr_ExceptionMatches(PyExc_GeneratorExit)
    ) {
        o->ac_state = 2;
        PyErr_Clear();          /* ignore these errors */
        PyErr_SetNone(PyExc_StopIteration);
    }
    return NULL;
}


static PyObject *
__Pyx_async_gen_athrow_throw(__pyx_PyAsyncGenAThrow *o, PyObject *args)
{
    PyObject *retval;

    if (o->ac_state == 0) {
        PyErr_SetString(PyExc_RuntimeError, __Pyx_NON_INIT_CORO_MSG);
        return NULL;
    }

    if (o->ac_state == 2) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }

    retval = __Pyx_Coroutine_Throw((PyObject*)o->ac_gen, args);
    if (o->ac_args) {
        return __Pyx_async_gen_unwrap_value(o->ac_gen, retval);
    } else {
        /* aclose() mode */
        if (retval && __pyx__PyAsyncGenWrappedValue_CheckExact(retval)) {
            Py_DECREF(retval);
            PyErr_SetString(PyExc_RuntimeError, __Pyx_ASYNC_GEN_IGNORED_EXIT_MSG);
            return NULL;
        }
        return retval;
    }
}


static PyObject *
__Pyx_async_gen_athrow_iternext(__pyx_PyAsyncGenAThrow *o)
{
    return __Pyx_async_gen_athrow_send(o, Py_None);
}


static PyObject *
__Pyx_async_gen_athrow_close(__pyx_PyAsyncGenAThrow *o, CYTHON_UNUSED PyObject *args)
{
    o->ac_state = 2;
    Py_RETURN_NONE;
}


static PyMethodDef __Pyx_async_gen_athrow_methods[] = {
    {"send", (PyCFunction)__Pyx_async_gen_athrow_send, METH_O, __Pyx_async_gen_send_doc},
    {"throw", (PyCFunction)__Pyx_async_gen_athrow_throw, METH_VARARGS, __Pyx_async_gen_throw_doc},
    {"close", (PyCFunction)__Pyx_async_gen_athrow_close, METH_NOARGS, __Pyx_async_gen_close_doc},
    {0, 0, 0, 0}        /* Sentinel */
};


static PyAsyncMethods __Pyx_async_gen_athrow_as_async = {
    PyObject_SelfIter,                          /* am_await */
    0,                                          /* am_aiter */
    0                                           /* am_anext */
};


PyTypeObject __pyx__PyAsyncGenAThrowType_type = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    "async_generator_athrow",                   /* tp_name */
    sizeof(__pyx_PyAsyncGenAThrow),                   /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)__Pyx_async_gen_athrow_dealloc,       /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
#if CYTHON_USE_ASYNC_SLOTS
    &__Pyx_async_gen_athrow_as_async,                 /* tp_as_async */
#else
    0,                                          /*tp_reserved*/
#endif
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    0,                                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
#if CYTHON_USE_ASYNC_SLOTS && CYTHON_COMPILING_IN_CPYTHON && PY_MAJOR_VERSION >= 3 && PY_VERSION_HEX < 0x030500B1
    // in order to (mis-)use tp_reserved above, we must also implement tp_richcompare
    __Pyx_Coroutine_compare,            /*tp_richcompare*/
#else
    0,                                  /*tp_richcompare*/
#endif
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)__Pyx_async_gen_athrow_iternext,    /* tp_iternext */
    __Pyx_async_gen_athrow_methods,                   /* tp_methods */
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
    0,                                          /* tp_free */
    0,                                          /* tp_is_gc */
    0,                                          /* tp_bases */
    0,                                          /* tp_mro */
    0,                                          /* tp_cache */
    0,                                          /* tp_subclasses */
    0,                                          /* tp_weaklist */
    0,                                          /* tp_del */
    0,                                          /* tp_version_tag */
#if PY_VERSION_HEX >= 0x030400a1
    0,                                          /* tp_finalize */
#endif
};


static PyObject *
__Pyx_async_gen_athrow_new(__pyx_AsyncGenObject *gen, PyObject *args)
{
    __pyx_PyAsyncGenAThrow *o;
    o = PyObject_New(__pyx_PyAsyncGenAThrow, __pyx__PyAsyncGenAThrowType);
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


/* ---------- global type sharing ------------ */

static int __pyx_AsyncGen_init(void) {
    // on Windows, C-API functions can't be used in slots statically
    __pyx_AsyncGenType_type.tp_getattro = PyObject_GenericGetAttr;
    __pyx__PyAsyncGenWrappedValueType_type.tp_getattro = PyObject_GenericGetAttr;
    __pyx__PyAsyncGenAThrowType_type.tp_getattro = PyObject_GenericGetAttr;
    __pyx__PyAsyncGenASendType_type.tp_getattro = PyObject_GenericGetAttr;

    __pyx_AsyncGenType = __Pyx_FetchCommonType(&__pyx_AsyncGenType_type);
    if (unlikely(!__pyx_AsyncGenType))
        return -1;

    __pyx__PyAsyncGenAThrowType = __Pyx_FetchCommonType(&__pyx__PyAsyncGenAThrowType_type);
    if (unlikely(!__pyx__PyAsyncGenAThrowType))
        return -1;

    __pyx__PyAsyncGenWrappedValueType = __Pyx_FetchCommonType(&__pyx__PyAsyncGenWrappedValueType_type);
    if (unlikely(!__pyx__PyAsyncGenWrappedValueType))
        return -1;

    __pyx__PyAsyncGenASendType = __Pyx_FetchCommonType(&__pyx__PyAsyncGenASendType_type);
    if (unlikely(!__pyx__PyAsyncGenASendType))
        return -1;

    return 0;
}
