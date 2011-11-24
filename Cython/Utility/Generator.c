//////////////////// Generator.proto ////////////////////
#define __Pyx_Generator_USED
#include <structmember.h>

typedef PyObject *(*__pyx_generator_body_t)(PyObject *, PyObject *);

typedef struct {
    PyObject_HEAD
    __pyx_generator_body_t body;
    PyObject *closure;
    int is_running;
    int resume_label;
    PyObject *exc_type;
    PyObject *exc_value;
    PyObject *exc_traceback;
    PyObject *gi_weakreflist;
    PyObject *classobj;
} __pyx_GeneratorObject;

static __pyx_GeneratorObject *__Pyx_Generator_New(__pyx_generator_body_t body,
                                                  PyObject *closure);
static int __pyx_Generator_init(void);

//////////////////// Generator ////////////////////
static PyObject *__Pyx_Generator_Next(PyObject *self);
static PyObject *__Pyx_Generator_Send(PyObject *self, PyObject *value);
static PyObject *__Pyx_Generator_Close(PyObject *self);
static PyObject *__Pyx_Generator_Throw(PyObject *gen, PyObject *args);

static CYTHON_INLINE
void __Pyx_Generator_ExceptionClear(__pyx_GeneratorObject *self)
{
    Py_XDECREF(self->exc_type);
    Py_XDECREF(self->exc_value);
    Py_XDECREF(self->exc_traceback);

    self->exc_type = NULL;
    self->exc_value = NULL;
    self->exc_traceback = NULL;
}

static CYTHON_INLINE
PyObject *__Pyx_Generator_SendEx(__pyx_GeneratorObject *self, PyObject *value)
{
    PyObject *retval;

    if (self->is_running) {
        PyErr_SetString(PyExc_ValueError,
                        "generator already executing");
        return NULL;
    }

    if (self->resume_label == 0) {
        if (value && value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
                            "can't send non-None value to a "
                            "just-started generator");
            return NULL;
        }
    }

    if (self->resume_label == -1) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }


    if (value)
        __Pyx_ExceptionSwap(&self->exc_type, &self->exc_value, &self->exc_traceback);
    else
        __Pyx_Generator_ExceptionClear(self);

    self->is_running = 1;
    retval = self->body((PyObject *) self, value);
    self->is_running = 0;

    if (retval)
        __Pyx_ExceptionSwap(&self->exc_type, &self->exc_value, &self->exc_traceback);
    else
        __Pyx_Generator_ExceptionClear(self);

    return retval;
}

static PyObject *__Pyx_Generator_Next(PyObject *self)
{
    return __Pyx_Generator_SendEx((__pyx_GeneratorObject *) self, Py_None);
}

static PyObject *__Pyx_Generator_Send(PyObject *self, PyObject *value)
{
    return __Pyx_Generator_SendEx((__pyx_GeneratorObject *) self, value);
}

static PyObject *__Pyx_Generator_Close(PyObject *self)
{
    __pyx_GeneratorObject *generator = (__pyx_GeneratorObject *) self;
    PyObject *retval;
#if PY_VERSION_HEX < 0x02050000
    PyErr_SetNone(PyExc_StopIteration);
#else
    PyErr_SetNone(PyExc_GeneratorExit);
#endif
    retval = __Pyx_Generator_SendEx(generator, NULL);
    if (retval) {
        Py_DECREF(retval);
        PyErr_SetString(PyExc_RuntimeError,
                        "generator ignored GeneratorExit");
        return NULL;
    }
#if PY_VERSION_HEX < 0x02050000
    if (PyErr_ExceptionMatches(PyExc_StopIteration))
#else
    if (PyErr_ExceptionMatches(PyExc_StopIteration)
        || PyErr_ExceptionMatches(PyExc_GeneratorExit))
#endif
    {
        PyErr_Clear();          /* ignore these errors */
        Py_INCREF(Py_None);
        return Py_None;
    }
    return NULL;
}

static PyObject *__Pyx_Generator_Throw(PyObject *self, PyObject *args)
{
    __pyx_GeneratorObject *generator = (__pyx_GeneratorObject *) self;
    PyObject *typ;
    PyObject *tb = NULL;
    PyObject *val = NULL;

    if (!PyArg_UnpackTuple(args, (char *)"throw", 1, 3, &typ, &val, &tb))
        return NULL;
    __Pyx_Raise(typ, val, tb, NULL);
    return __Pyx_Generator_SendEx(generator, NULL);
}

static int
__Pyx_Generator_traverse(PyObject *self, visitproc visit, void *arg)
{
    __pyx_GeneratorObject *gen = (__pyx_GeneratorObject *) self;

    Py_VISIT(gen->closure);
    Py_VISIT(gen->classobj);
    Py_VISIT(gen->exc_type);
    Py_VISIT(gen->exc_value);
    Py_VISIT(gen->exc_traceback);
    return 0;
}

static void
__Pyx_Generator_dealloc(PyObject *self)
{
    __pyx_GeneratorObject *gen = (__pyx_GeneratorObject *) self;

    PyObject_GC_UnTrack(gen);
    if (gen->gi_weakreflist != NULL)
        PyObject_ClearWeakRefs(self);
    PyObject_GC_Track(self);

    if (gen->resume_label > 0) {
        /* Generator is paused, so we need to close */
        Py_TYPE(gen)->tp_del(self);
        if (self->ob_refcnt > 0)
            return;                     /* resurrected.  :( */
    }

    PyObject_GC_UnTrack(self);
    Py_CLEAR(gen->closure);
    Py_CLEAR(gen->classobj);
    Py_CLEAR(gen->exc_type);
    Py_CLEAR(gen->exc_value);
    Py_CLEAR(gen->exc_traceback);
    PyObject_GC_Del(gen);
}

static void
__Pyx_Generator_del(PyObject *self)
{
    PyObject *res;
    PyObject *error_type, *error_value, *error_traceback;
    __pyx_GeneratorObject *gen = (__pyx_GeneratorObject *) self;

    if (gen->resume_label <= 0)
        return ;

    /* Temporarily resurrect the object. */
    assert(self->ob_refcnt == 0);
    self->ob_refcnt = 1;

    /* Save the current exception, if any. */
    __Pyx_ErrFetch(&error_type, &error_value, &error_traceback);

    res = __Pyx_Generator_Close(self);

    if (res == NULL)
        PyErr_WriteUnraisable(self);
    else
        Py_DECREF(res);

    /* Restore the saved exception. */
    __Pyx_ErrRestore(error_type, error_value, error_traceback);

    /* Undo the temporary resurrection; can't use DECREF here, it would
     * cause a recursive call.
     */
    assert(self->ob_refcnt > 0);
    if (--self->ob_refcnt == 0)
        return; /* this is the normal path out */

    /* close() resurrected it!  Make it look like the original Py_DECREF
     * never happened.
     */
    {
        Py_ssize_t refcnt = self->ob_refcnt;
        _Py_NewReference(self);
        self->ob_refcnt = refcnt;
    }
    assert(PyType_IS_GC(self->ob_type) &&
           _Py_AS_GC(self)->gc.gc_refs != _PyGC_REFS_UNTRACKED);

    /* If Py_REF_DEBUG, _Py_NewReference bumped _Py_RefTotal, so
     * we need to undo that. */
    _Py_DEC_REFTOTAL;
    /* If Py_TRACE_REFS, _Py_NewReference re-added self to the object
     * chain, so no more to do there.
     * If COUNT_ALLOCS, the original decref bumped tp_frees, and
     * _Py_NewReference bumped tp_allocs:  both of those need to be
     * undone.
     */
#ifdef COUNT_ALLOCS
    --self->ob_type->tp_frees;
    --self->ob_type->tp_allocs;
#endif
}

static PyMemberDef __pyx_Generator_memberlist[] = {
    {(char *) "gi_running",
     T_INT,
     offsetof(__pyx_GeneratorObject, is_running),
     READONLY,
     NULL},
    {0, 0, 0, 0, 0}
};

static PyMethodDef __pyx_Generator_methods[] = {
    {__Pyx_NAMESTR("send"), (PyCFunction) __Pyx_Generator_Send, METH_O, 0},
    {__Pyx_NAMESTR("throw"), (PyCFunction) __Pyx_Generator_Throw, METH_VARARGS, 0},
    {__Pyx_NAMESTR("close"), (PyCFunction) __Pyx_Generator_Close, METH_NOARGS, 0},
    {0, 0, 0, 0}
};

static PyTypeObject __pyx_GeneratorType = {
    PyVarObject_HEAD_INIT(0, 0)
    __Pyx_NAMESTR("generator"),         /*tp_name*/
    sizeof(__pyx_GeneratorObject),      /*tp_basicsize*/
    0,                                  /*tp_itemsize*/
    (destructor) __Pyx_Generator_dealloc,/*tp_dealloc*/
    0,                                  /*tp_print*/
    0,                                  /*tp_getattr*/
    0,                                  /*tp_setattr*/
#if PY_MAJOR_VERSION < 3
    0,                                  /*tp_compare*/
#else
    0,                                  /*reserved*/
#endif
    0,                                   /*tp_repr*/
    0,                                  /*tp_as_number*/
    0,                                  /*tp_as_sequence*/
    0,                                  /*tp_as_mapping*/
    0,                                  /*tp_hash*/
    0,                                  /*tp_call*/
    0,                                  /*tp_str*/
    PyObject_GenericGetAttr,            /*tp_getattro*/
    0,                                  /*tp_setattro*/
    0,                                  /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, /* tp_flags*/
    0,                                  /*tp_doc*/
    (traverseproc) __Pyx_Generator_traverse,   /*tp_traverse*/
    0,                                  /*tp_clear*/
    0,                                  /*tp_richcompare*/
    offsetof(__pyx_GeneratorObject, gi_weakreflist), /* tp_weaklistoffse */
    PyObject_SelfIter,                  /*tp_iter*/
    (iternextfunc) __Pyx_Generator_Next, /*tp_iternext*/
    __pyx_Generator_methods,            /*tp_methods*/
    __pyx_Generator_memberlist,         /*tp_members*/
    0,                                  /*tp_getset*/
    0,                                  /*tp_base*/
    0,                                  /*tp_dict*/
    0,                                  /*tp_descr_get*/
    0,                                  /*tp_descr_set*/
    0,                                  /*tp_dictoffset*/
    0,                                  /*tp_init*/
    0,                                  /*tp_alloc*/
    0,                                  /*tp_new*/
    0,                                  /*tp_free*/
    0,                                  /*tp_is_gc*/
    0,                                  /*tp_bases*/
    0,                                  /*tp_mro*/
    0,                                  /*tp_cache*/
    0,                                  /*tp_subclasses*/
    0,                                  /*tp_weaklist*/
    __Pyx_Generator_del,                /*tp_del*/
#if PY_VERSION_HEX >= 0x02060000
    0,                                  /*tp_version_tag*/
#endif
};

static
__pyx_GeneratorObject *__Pyx_Generator_New(__pyx_generator_body_t body,
                                           PyObject *closure)
{
    __pyx_GeneratorObject *gen =
        PyObject_GC_New(__pyx_GeneratorObject, &__pyx_GeneratorType);

    if (gen == NULL)
        return NULL;

    gen->body = body;
    gen->closure = closure;
    Py_XINCREF(closure);
    gen->is_running = 0;
    gen->resume_label = 0;
    gen->classobj = NULL;
    gen->exc_type = NULL;
    gen->exc_value = NULL;
    gen->exc_traceback = NULL;
    gen->gi_weakreflist = NULL;

    PyObject_GC_Track(gen);
    return gen;
}

static int __pyx_Generator_init(void)
{
    return PyType_Ready(&__pyx_GeneratorType);
}
