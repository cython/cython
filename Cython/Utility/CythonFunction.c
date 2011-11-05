

//////////////////// CythonFunction.proto ////////////////////
#define __Pyx_CyFunction_USED 1
#include <structmember.h>

#define __Pyx_CYFUNCTION_STATICMETHOD  0x01
#define __Pyx_CYFUNCTION_CLASSMETHOD   0x02
#define __Pyx_CYFUNCTION_CCLASS        0x04

#define __Pyx_CyFunction_GetClosure(f) \
    (((__pyx_CyFunctionObject *) (f))->func_closure)
#define __Pyx_CyFunction_GetClassObj(f) \
    (((__pyx_CyFunctionObject *) (f))->func_classobj)


typedef struct {
    PyCFunctionObject func;
    int flags;
    PyObject *func_dict;
    PyObject *func_weakreflist;
    PyObject *func_name;
    PyObject *func_doc;
    PyObject *func_code;
    PyObject *func_closure;
    PyObject *func_classobj; /* No-args super() class cell */
} __pyx_CyFunctionObject;

static PyTypeObject *__pyx_CyFunctionType = 0;

#define __Pyx_CyFunction_NewEx(ml, flags, self, module, code) \
    __Pyx_CyFunction_New(__pyx_CyFunctionType, ml, flags, self, module, code)

static PyObject *__Pyx_CyFunction_New(PyTypeObject *,
                                      PyMethodDef *ml, int flags,
                                      PyObject *self, PyObject *module,
                                      PyObject* code);

static int __Pyx_CyFunction_init(void);

//////////////////// CythonFunction ////////////////////

static PyObject *
__Pyx_CyFunction_get_doc(__pyx_CyFunctionObject *op, CYTHON_UNUSED void *closure)
{
    if (op->func_doc == NULL && op->func.m_ml->ml_doc) {
#if PY_MAJOR_VERSION >= 3
        op->func_doc = PyUnicode_FromString(op->func.m_ml->ml_doc);
#else
        op->func_doc = PyString_FromString(op->func.m_ml->ml_doc);
#endif
    }
    if (op->func_doc == 0) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    Py_INCREF(op->func_doc);
    return op->func_doc;
}

static int
__Pyx_CyFunction_set_doc(__pyx_CyFunctionObject *op, PyObject *value)
{
    PyObject *tmp = op->func_doc;
    if (value == NULL)
        op->func_doc = Py_None; /* Mark as deleted */
    else
        op->func_doc = value;
    Py_INCREF(op->func_doc);
    Py_XDECREF(tmp);
    return 0;
}

static PyObject *
__Pyx_CyFunction_get_name(__pyx_CyFunctionObject *op)
{
    if (op->func_name == NULL) {
#if PY_MAJOR_VERSION >= 3
        op->func_name = PyUnicode_InternFromString(op->func.m_ml->ml_name);
#else
        op->func_name = PyString_InternFromString(op->func.m_ml->ml_name);
#endif
    }
    Py_INCREF(op->func_name);
    return op->func_name;
}

static int
__Pyx_CyFunction_set_name(__pyx_CyFunctionObject *op, PyObject *value)
{
    PyObject *tmp;

#if PY_MAJOR_VERSION >= 3
    if (value == NULL || !PyUnicode_Check(value)) {
#else
    if (value == NULL || !PyString_Check(value)) {
#endif
        PyErr_SetString(PyExc_TypeError,
                        "__name__ must be set to a string object");
        return -1;
    }
    tmp = op->func_name;
    Py_INCREF(value);
    op->func_name = value;
    Py_XDECREF(tmp);
    return 0;
}

static PyObject *
__Pyx_CyFunction_get_self(__pyx_CyFunctionObject *m, CYTHON_UNUSED void *closure)
{
    PyObject *self;

    self = m->func_closure;
    if (self == NULL)
        self = Py_None;
    Py_INCREF(self);
    return self;
}

static PyObject *
__Pyx_CyFunction_get_dict(__pyx_CyFunctionObject *op)
{
    if (op->func_dict == NULL) {
        op->func_dict = PyDict_New();
        if (op->func_dict == NULL)
            return NULL;
    }
    Py_INCREF(op->func_dict);
    return op->func_dict;
}

static int
__Pyx_CyFunction_set_dict(__pyx_CyFunctionObject *op, PyObject *value)
{
    PyObject *tmp;

    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError,
               "function's dictionary may not be deleted");
        return -1;
    }
    if (!PyDict_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
               "setting function's dictionary to a non-dict");
        return -1;
    }
    tmp = op->func_dict;
    Py_INCREF(value);
    op->func_dict = value;
    Py_XDECREF(tmp);
    return 0;
}

{{# """
/*
    TODO: we implicitly use the global module to get func_globals.  This
    will need to be passed into __Pyx_CyFunction_NewEx() if we share
    this type across modules.  We currently avoid doing this to reduce
    the overhead of creating a function object, and to avoid keeping a
    reference to the module dict as long as we don't need to.
*/
""" }}

static PyObject *
__Pyx_CyFunction_get_globals(CYTHON_UNUSED __pyx_CyFunctionObject *op)
{
    PyObject* dict = PyModule_GetDict({{module_cname}});
    Py_XINCREF(dict);
    return dict;
}

static PyObject *
__Pyx_CyFunction_get_closure(CYTHON_UNUSED __pyx_CyFunctionObject *op)
{
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *
__Pyx_CyFunction_get_code(__pyx_CyFunctionObject *op)
{
    PyObject* result = (op->func_code) ? op->func_code : Py_None;
    Py_INCREF(result);
    return result;
}

static PyGetSetDef __pyx_CyFunction_getsets[] = {
    {(char *) "func_doc", (getter)__Pyx_CyFunction_get_doc, (setter)__Pyx_CyFunction_set_doc, 0, 0},
    {(char *) "__doc__",  (getter)__Pyx_CyFunction_get_doc, (setter)__Pyx_CyFunction_set_doc, 0, 0},
    {(char *) "func_name", (getter)__Pyx_CyFunction_get_name, (setter)__Pyx_CyFunction_set_name, 0, 0},
    {(char *) "__name__", (getter)__Pyx_CyFunction_get_name, (setter)__Pyx_CyFunction_set_name, 0, 0},
    {(char *) "__self__", (getter)__Pyx_CyFunction_get_self, 0, 0, 0},
    {(char *) "func_dict", (getter)__Pyx_CyFunction_get_dict, (setter)__Pyx_CyFunction_set_dict, 0, 0},
    {(char *) "__dict__", (getter)__Pyx_CyFunction_get_dict, (setter)__Pyx_CyFunction_set_dict, 0, 0},
    {(char *) "func_globals", (getter)__Pyx_CyFunction_get_globals, 0, 0, 0},
    {(char *) "__globals__", (getter)__Pyx_CyFunction_get_globals, 0, 0, 0},
    {(char *) "func_closure", (getter)__Pyx_CyFunction_get_closure, 0, 0, 0},
    {(char *) "__closure__", (getter)__Pyx_CyFunction_get_closure, 0, 0, 0},
    {(char *) "func_code", (getter)__Pyx_CyFunction_get_code, 0, 0, 0},
    {(char *) "__code__", (getter)__Pyx_CyFunction_get_code, 0, 0, 0},
    {0, 0, 0, 0, 0}
};

#ifndef PY_WRITE_RESTRICTED /* < Py2.5 */
#define PY_WRITE_RESTRICTED WRITE_RESTRICTED
#endif

static PyMemberDef __pyx_CyFunction_members[] = {
    {(char *) "__module__", T_OBJECT, offsetof(__pyx_CyFunctionObject, func.m_module), PY_WRITE_RESTRICTED, 0},
    {0, 0, 0,  0, 0}
};

static PyObject *
__Pyx_CyFunction_reduce(__pyx_CyFunctionObject *m, CYTHON_UNUSED PyObject *args)
{
#if PY_MAJOR_VERSION >= 3
    return PyUnicode_FromString(m->func.m_ml->ml_name);
#else
    return PyString_FromString(m->func.m_ml->ml_name);
#endif
}

static PyMethodDef __pyx_CyFunction_methods[] = {
    {__Pyx_NAMESTR("__reduce__"), (PyCFunction)__Pyx_CyFunction_reduce, METH_VARARGS, 0},
    {0, 0, 0, 0}
};


static PyObject *__Pyx_CyFunction_New(PyTypeObject *type, PyMethodDef *ml, int flags,
                                      PyObject *closure, PyObject *module, PyObject* code) {
    __pyx_CyFunctionObject *op = PyObject_GC_New(__pyx_CyFunctionObject, type);
    if (op == NULL)
        return NULL;
    op->flags = flags;
    op->func_weakreflist = NULL;
    op->func.m_ml = ml;
    op->func.m_self = (PyObject *) op;
    Py_XINCREF(closure);
    op->func_closure = closure;
    Py_XINCREF(module);
    op->func.m_module = module;
    op->func_dict = NULL;
    op->func_name = NULL;
    op->func_doc = NULL;
    op->func_classobj = NULL;
    Py_XINCREF(code);
    op->func_code = code;
    PyObject_GC_Track(op);
    return (PyObject *) op;
}

static int
__Pyx_CyFunction_clear(__pyx_CyFunctionObject *m)
{
    Py_CLEAR(m->func_closure);
    Py_CLEAR(m->func.m_module);
    Py_CLEAR(m->func_dict);
    Py_CLEAR(m->func_name);
    Py_CLEAR(m->func_doc);
    Py_CLEAR(m->func_code);
    Py_CLEAR(m->func_classobj);
    return 0;
}

static void __Pyx_CyFunction_dealloc(__pyx_CyFunctionObject *m)
{
    PyObject_GC_UnTrack(m);
    if (m->func_weakreflist != NULL)
        PyObject_ClearWeakRefs((PyObject *) m);
    __Pyx_CyFunction_clear(m);
    PyObject_GC_Del(m);
}

static int __Pyx_CyFunction_traverse(__pyx_CyFunctionObject *m, visitproc visit, void *arg)
{
    Py_VISIT(m->func_closure);
    Py_VISIT(m->func.m_module);
    Py_VISIT(m->func_dict);
    Py_VISIT(m->func_name);
    Py_VISIT(m->func_doc);
    Py_VISIT(m->func_code);
    Py_VISIT(m->func_classobj);
    return 0;
}

static PyObject *__Pyx_CyFunction_descr_get(PyObject *func, PyObject *obj, PyObject *type)
{
    __pyx_CyFunctionObject *m = (__pyx_CyFunctionObject *) func;

    if (m->flags & __Pyx_CYFUNCTION_STATICMETHOD) {
        Py_INCREF(func);
        return func;
    }

    if (m->flags & __Pyx_CYFUNCTION_CLASSMETHOD) {
        if (type == NULL)
            type = (PyObject *)(Py_TYPE(obj));
        return PyMethod_New(func,
                            type, (PyObject *)(Py_TYPE(type)));
    }

    if (obj == Py_None)
        obj = NULL;
    return PyMethod_New(func, obj, type);
}

static PyObject*
__Pyx_CyFunction_repr(__pyx_CyFunctionObject *op)
{
    PyObject *func_name = __Pyx_CyFunction_get_name(op);

#if PY_MAJOR_VERSION >= 3
    return PyUnicode_FromFormat("<cyfunction %U at %p>",
                               func_name, op);
#else
    return PyString_FromFormat("<cyfunction %s at %p>",
                               PyString_AsString(func_name), op);
#endif
}

static PyTypeObject __pyx_CyFunctionType_type = {
    PyVarObject_HEAD_INIT(0, 0)
    __Pyx_NAMESTR("cython_function_or_method"), /*tp_name*/
    sizeof(__pyx_CyFunctionObject),   /*tp_basicsize*/
    0,                                  /*tp_itemsize*/
    (destructor) __Pyx_CyFunction_dealloc, /*tp_dealloc*/
    0,                                  /*tp_print*/
    0,                                  /*tp_getattr*/
    0,                                  /*tp_setattr*/
#if PY_MAJOR_VERSION < 3
    0,                                  /*tp_compare*/
#else
    0,                                  /*reserved*/
#endif
    (reprfunc) __Pyx_CyFunction_repr,   /*tp_repr*/
    0,                                  /*tp_as_number*/
    0,                                  /*tp_as_sequence*/
    0,                                  /*tp_as_mapping*/
    0,                                  /*tp_hash*/
    PyCFunction_Call,                   /*tp_call*/
    0,                                  /*tp_str*/
    0,                                  /*tp_getattro*/
    0,                                  /*tp_setattro*/
    0,                                  /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC, /* tp_flags*/
    0,                                  /*tp_doc*/
    (traverseproc) __Pyx_CyFunction_traverse,   /*tp_traverse*/
    (inquiry) __Pyx_CyFunction_clear,   /*tp_clear*/
    0,                                  /*tp_richcompare*/
    offsetof(__pyx_CyFunctionObject, func_weakreflist), /* tp_weaklistoffse */
    0,                                  /*tp_iter*/
    0,                                  /*tp_iternext*/
    __pyx_CyFunction_methods,           /*tp_methods*/
    __pyx_CyFunction_members,           /*tp_members*/
    __pyx_CyFunction_getsets,           /*tp_getset*/
    0,                                  /*tp_base*/
    0,                                  /*tp_dict*/
    __Pyx_CyFunction_descr_get,         /*tp_descr_get*/
    0,                                  /*tp_descr_set*/
    offsetof(__pyx_CyFunctionObject, func_dict),/*tp_dictoffset*/
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
    0,                                  /*tp_del*/
#if PY_VERSION_HEX >= 0x02060000
    0,                                  /*tp_version_tag*/
#endif
};


static int __Pyx_CyFunction_init(void)
{
    if (PyType_Ready(&__pyx_CyFunctionType_type) < 0)
        return -1;
    __pyx_CyFunctionType = &__pyx_CyFunctionType_type;
    return 0;
}

//////////////////// CyFunctionClassCell.proto ////////////////////
static CYTHON_INLINE void __Pyx_CyFunction_InitClassCell(PyObject *cyfunctions,
                                                         PyObject *classobj);

//////////////////// CyFunctionClassCell ////////////////////
void __Pyx_CyFunction_InitClassCell(PyObject *cyfunctions,
                                    PyObject *classobj)
{
    int i;

    for (i = 0; i < PyList_GET_SIZE(cyfunctions); i++) {
        __pyx_CyFunctionObject *m =
            (__pyx_CyFunctionObject *) PyList_GET_ITEM(cyfunctions, i);
        m->func_classobj = classobj;
        Py_INCREF(classobj);
    }
}

//////////////////// FusedFunction.proto ////////////////////
typedef struct {
    __pyx_CyFunctionObject func;
    PyObject *__signatures__;
    PyObject *type;
    PyObject *self;
} __pyx_FusedFunctionObject;

#define __pyx_FusedFunction_NewEx(ml, flags, self, module, code)         \
        __pyx_FusedFunction_New(__pyx_FusedFunctionType, ml, flags, self, module, code)
static PyObject *__pyx_FusedFunction_New(PyTypeObject *type,
                                         PyMethodDef *ml, int flags,
                                         PyObject *self, PyObject *module,
                                         PyObject *code);

static PyTypeObject *__pyx_FusedFunctionType = NULL;
static int __pyx_FusedFunction_init(void);

#define __Pyx_FusedFunction_USED

//////////////////// FusedFunction ////////////////////
static PyObject *
__pyx_FusedFunction_New(PyTypeObject *type, PyMethodDef *ml, int flags, PyObject *self,
                        PyObject *module, PyObject *code)
{
    __pyx_FusedFunctionObject *fusedfunc =
        (__pyx_FusedFunctionObject *) __Pyx_CyFunction_New(type, ml, flags,
                                                           self, module, code);
    if (!fusedfunc)
        return NULL;

    fusedfunc->__signatures__ = NULL;
    fusedfunc->type = NULL;
    fusedfunc->self = NULL;
    return (PyObject *) fusedfunc;
}

static void __pyx_FusedFunction_dealloc(__pyx_FusedFunctionObject *self) {
    Py_XDECREF(self->__signatures__);
    /* __pyx_CyFunction_dealloc((__pyx_CyFunctionObject *) m); */
    __pyx_FusedFunctionType->tp_free((PyObject *) self);
}

static int
__pyx_FusedFunction_traverse(__pyx_FusedFunctionObject *self,
                             visitproc visit,
                             void *arg)
{
    Py_VISIT(self->self);
    Py_VISIT(self->type);
    Py_VISIT(self->__signatures__);
    return __Pyx_CyFunction_traverse((__pyx_CyFunctionObject *) self, visit, arg);
}

static int
__pyx_FusedFunction_clear(__pyx_FusedFunctionObject *self)
{
    Py_CLEAR(self->self);
    Py_CLEAR(self->type);
    Py_CLEAR(self->__signatures__);
    return __Pyx_CyFunction_clear((__pyx_CyFunctionObject *) self);
}


static PyObject *
__pyx_FusedFunction_descr_get(PyObject *self, PyObject *obj, PyObject *type)
{
    __pyx_FusedFunctionObject *func, *meth;

    func = (__pyx_FusedFunctionObject *) self;

    if (func->self || func->func.flags & __Pyx_CYFUNCTION_STATICMETHOD) {
        /* Do not allow rebinding and don't do anything for static methods */
        Py_INCREF(self);
        return self;
    }

    if (obj == Py_None)
        obj = NULL;

    meth = (__pyx_FusedFunctionObject *) __pyx_FusedFunction_NewEx(
                    ((PyCFunctionObject *) func)->m_ml,
                    ((__pyx_CyFunctionObject *) func)->flags,
                    ((__pyx_CyFunctionObject *) func)->func_closure,
                    ((PyCFunctionObject *) func)->m_module,
                    ((__pyx_CyFunctionObject *) func)->func_code);
    if (!meth)
        return NULL;

    Py_XINCREF(func->func.func_classobj);
    meth->func.func_classobj = func->func.func_classobj;

    Py_XINCREF(func->__signatures__);
    meth->__signatures__ = func->__signatures__;

    Py_XINCREF(type);
    meth->type = type;

    if (func->func.flags & __Pyx_CYFUNCTION_CLASSMETHOD)
        obj = type;

    Py_XINCREF(obj);
    meth->self = obj;

    return (PyObject *) meth;
}

static PyObject *
__pyx_FusedFunction_getitem(__pyx_FusedFunctionObject *self, PyObject *idx)
{
    PyObject *signature = NULL;
    PyObject *unbound_result_func;
    PyObject *result_func = NULL;

    if (self->__signatures__ == NULL) {
        PyErr_SetString(PyExc_TypeError, "Function is not fused");
        return NULL;
    }

    if (PyTuple_Check(idx)) {
        PyObject *list = PyList_New(0);
        Py_ssize_t n = PyTuple_GET_SIZE(idx);
        PyObject *string = NULL;
        PyObject *sep = NULL;
        int i;

        if (!list)
            return NULL;

        for (i = 0; i < n; i++) {
            PyObject *item = PyTuple_GET_ITEM(idx, i);

            if (PyType_Check(item))
                string = PyObject_GetAttrString(item, "__name__");
            else
                string = PyObject_Str(item);

            if (!string || PyList_Append(list, string) < 0)
                goto __pyx_err;

            Py_DECREF(string);
        }

        sep = PyUnicode_FromString(", ");
        if (sep)
            signature = PyUnicode_Join(sep, list);
__pyx_err:
;
        Py_DECREF(list);
        Py_XDECREF(sep);
    } else {
        signature = PyObject_Str(idx);
    }

    if (!signature)
        return NULL;

    unbound_result_func = PyObject_GetItem(self->__signatures__, signature);

    if (unbound_result_func) {
        __pyx_FusedFunctionObject *unbound = (__pyx_FusedFunctionObject *) unbound_result_func;

        Py_CLEAR(unbound->func.func_classobj);
        Py_XINCREF(self->func.func_classobj);
        unbound->func.func_classobj = self->func.func_classobj;

        result_func = __pyx_FusedFunction_descr_get(unbound_result_func,
                                                    self->self, self->type);
    }

    Py_DECREF(signature);
    Py_XDECREF(unbound_result_func);

    return result_func;
}

static PyObject *
__pyx_FusedFunction_callfunction(PyObject *func, PyObject *args, PyObject *kw)
{
     __pyx_CyFunctionObject *cyfunc = (__pyx_CyFunctionObject *) func;
    PyObject *result;
    int static_specialized = (cyfunc->flags & __Pyx_CYFUNCTION_STATICMETHOD &&
                              !((__pyx_FusedFunctionObject *) func)->__signatures__);

    //PyObject_Print(args, stdout, Py_PRINT_RAW);

    if (cyfunc->flags & __Pyx_CYFUNCTION_CCLASS && !static_specialized) {
        Py_ssize_t argc;
        PyObject *new_args;
        PyObject *self;
        PyObject *m_self;

        argc = PyTuple_GET_SIZE(args);
        new_args = PyTuple_GetSlice(args, 1, argc);

        if (!new_args)
            return NULL;

        self = PyTuple_GetItem(args, 0);

        if (!self)
            return NULL;

        m_self = cyfunc->func.m_self;
        cyfunc->func.m_self = self;
        result = PyCFunction_Call(func, new_args, kw);
        cyfunc->func.m_self = m_self;

        Py_DECREF(new_args);
    } else {
        result = PyCFunction_Call(func, args, kw);
    }

    return result;
}

/* Note: the 'self' from method binding is passed in in the args tuple,
         whereas PyCFunctionObject's m_self is passed in as the first
         argument to the C function. For extension methods we need
         to pass 'self' as 'm_self' and not as the first element of the
         args tuple.
*/
static PyObject *
__pyx_FusedFunction_call(PyObject *func, PyObject *args, PyObject *kw)
{
    __pyx_FusedFunctionObject *binding_func = (__pyx_FusedFunctionObject *) func;
    Py_ssize_t argc = PyTuple_GET_SIZE(args);
    PyObject *new_args = NULL;
    __pyx_FusedFunctionObject *new_func = NULL;
    PyObject *result = NULL;
    PyObject *self = NULL;
    int is_staticmethod = binding_func->func.flags & __Pyx_CYFUNCTION_STATICMETHOD;
    int is_classmethod = binding_func->func.flags & __Pyx_CYFUNCTION_CLASSMETHOD;

    if (binding_func->self) {
        /* Bound method call, put 'self' in the args tuple */
        Py_ssize_t i;
        new_args = PyTuple_New(argc + 1);
        if (!new_args)
            return NULL;

        self = binding_func->self;
        Py_INCREF(self);
        PyTuple_SET_ITEM(new_args, 0, self);

        for (i = 0; i < argc; i++) {
            PyObject *item = PyTuple_GET_ITEM(args, i);
            Py_INCREF(item);
            PyTuple_SET_ITEM(new_args, i + 1, item);
        }

        args = new_args;
    } else if (binding_func->type) {
        /* Unbound method call */
        if (argc < 1) {
            PyErr_Format(PyExc_TypeError, "Need at least one argument, 0 given.");
            return NULL;
        }
        self = PyTuple_GET_ITEM(args, 0);
    }

    if (self && !is_classmethod && !is_staticmethod &&
            !PyObject_IsInstance(self, binding_func->type)) {
        PyErr_Format(PyExc_TypeError,
                     "First argument should be of type %s, got %s.",
                     ((PyTypeObject *) binding_func->type)->tp_name,
                     self->ob_type->tp_name);
        goto __pyx_err;
    }

    if (binding_func->__signatures__) {
        PyObject *tup = PyTuple_Pack(3, binding_func->__signatures__, args,
                                        kw == NULL ? Py_None : kw);
        if (!tup)
            goto __pyx_err;

        new_func = (__pyx_FusedFunctionObject *) __pyx_FusedFunction_callfunction(func, tup, NULL);;
        Py_DECREF(tup);

        if (!new_func)
            goto __pyx_err;

        Py_CLEAR(new_func->func.func_classobj);
        Py_XINCREF(binding_func->func.func_classobj);
        new_func->func.func_classobj = binding_func->func.func_classobj;

        func = (PyObject *) new_func;
    }

    result = __pyx_FusedFunction_callfunction(func, args, kw);
__pyx_err:
    Py_XDECREF(new_args);
    Py_XDECREF((PyObject *) new_func);
    return result;
}

static PyMemberDef __pyx_FusedFunction_members[] = {
    {(char *) "__signatures__",
     T_OBJECT,
     offsetof(__pyx_FusedFunctionObject, __signatures__),
     READONLY,
     __Pyx_DOCSTR(0)},
};

static PyMappingMethods __pyx_FusedFunction_mapping_methods = {
    0,
    (binaryfunc) __pyx_FusedFunction_getitem,
    0,
};

static PyTypeObject __pyx_FusedFunctionType_type = {
    PyVarObject_HEAD_INIT(0, 0)
    __Pyx_NAMESTR("fused_cython_function"), /*tp_name*/
    sizeof(__pyx_FusedFunctionObject), /*tp_basicsize*/
    0,                                  /*tp_itemsize*/
    (destructor) __pyx_FusedFunction_dealloc, /*tp_dealloc*/
    0,                                  /*tp_print*/
    0,                                  /*tp_getattr*/
    0,                                  /*tp_setattr*/
#if PY_MAJOR_VERSION < 3
    0,                                  /*tp_compare*/
#else
    0,                                  /*reserved*/
#endif
    0,                                  /*tp_repr*/
    0,                                  /*tp_as_number*/
    0,                                  /*tp_as_sequence*/
    &__pyx_FusedFunction_mapping_methods, /*tp_as_mapping*/
    0,                                  /*tp_hash*/
    (ternaryfunc) __pyx_FusedFunction_call, /*tp_call*/
    0,                                  /*tp_str*/
    0,                                  /*tp_getattro*/
    0,                                  /*tp_setattro*/
    0,                                  /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC | Py_TPFLAGS_BASETYPE, /* tp_flags*/
    0,                                  /*tp_doc*/
    (traverseproc) __pyx_FusedFunction_traverse,   /*tp_traverse*/
    (inquiry) __pyx_FusedFunction_clear,/*tp_clear*/
    0,                                  /*tp_richcompare*/
    0,                                  /*tp_weaklistoffset*/
    0,                                  /*tp_iter*/
    0,                                  /*tp_iternext*/
    0,                                  /*tp_methods*/
    __pyx_FusedFunction_members,        /*tp_members*/
    0,                                  /*tp_getset*/
    &__pyx_CyFunctionType_type,         /*tp_base*/
    0,                                  /*tp_dict*/
    __pyx_FusedFunction_descr_get,      /*tp_descr_get*/
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
    0,                                  /*tp_del*/
#if PY_VERSION_HEX >= 0x02060000
    0,                                  /*tp_version_tag*/
#endif
};

static int __pyx_FusedFunction_init(void) {
    if (PyType_Ready(&__pyx_FusedFunctionType_type) < 0) {
        return -1;
    }
    __pyx_FusedFunctionType = &__pyx_FusedFunctionType_type;
    return 0;
}
