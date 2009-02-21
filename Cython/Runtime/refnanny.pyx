from python_ref cimport Py_INCREF, Py_DECREF, Py_XDECREF
from python_exc cimport PyObject, PyErr_Fetch, PyErr_Restore


loglevel = 0
reflog = []

cdef log(level, action, obj, lineno):
    if loglevel >= level:
        reflog.append((lineno, action, id(obj)))

LOG_NONE, LOG_ALL = range(2)

class Error(Exception):
    pass

class Context(object):
    def __init__(self, name, line=0, filename=None):
        self.name = name
        self.start = line
        self.filename = filename
        self.refs = {} # id -> (count, [lineno])
        self.errors = []

    def regref(self, obj, lineno, is_null):
        log(LOG_ALL, u'regref', u"<NULL>" if is_null else obj, lineno)
        if is_null:
            self.errors.append(u"NULL argument on line %d" % lineno)
            return
        id_ = id(obj)
        count, linenumbers = self.refs.get(id_, (0, []))
        self.refs[id_] = (count + 1, linenumbers)
        linenumbers.append(lineno)

    def delref(self, obj, lineno, is_null):
        log(LOG_ALL, u'delref', u"<NULL>" if is_null else obj, lineno)
        if is_null:
            self.errors.append(u"NULL argument on line %d" % lineno)
            return
        id_ = id(obj)
        count, linenumbers = self.refs.get(id_, (0, []))
        if count == 0:
            self.errors.append(u"Too many decrefs on line %d, reference acquired on lines %r" %
                (lineno, linenumbers))
        elif count == 1:
            del self.refs[id_]
        else:
            self.refs[id_] = (count - 1, linenumbers)

    def end(self):
        if len(self.refs) > 0:
            msg = u""
            for count, linenos in self.refs.itervalues():
                msg += u"\n  Acquired on lines: " + u", ".join([u"%d" % x for x in linenos])
            self.errors.append(u"References leaked: %s" % msg)
        if self.errors:
            return u"\n".join(self.errors)
        else:
            return None



cdef PyObject* NewContext(char* funcname, int lineno, char* filename) except NULL:
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    PyErr_Fetch(&type, &value, &tb)
    try:
        ctx = Context(funcname, lineno, filename)
        PyErr_Restore(<object>type, <object>value, <object>tb)
        Py_INCREF(ctx)
        return <PyObject*>ctx
    except:
        Py_XDECREF(<object>type)
        Py_XDECREF(<object>value)
        Py_XDECREF(<object>tb)
        raise

cdef void GOTREF(PyObject* ctx, PyObject* p_obj, int lineno):
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    if ctx == NULL: return
    PyErr_Fetch(&type, &value, &tb)
    try:
        if p_obj is NULL:
            (<object>ctx).regref(None, lineno, True)
        else:
            (<object>ctx).regref(<object>p_obj, lineno, False)
        PyErr_Restore(<object>type, <object>value, <object>tb)
    except:
        Py_XDECREF(<object>type)
        Py_XDECREF(<object>value)
        Py_XDECREF(<object>tb)
        raise

cdef void GIVEREF(PyObject* ctx, PyObject* p_obj, int lineno):
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    if ctx == NULL: return
    PyErr_Fetch(&type, &value, &tb)
    try:
        if p_obj is NULL:
            (<object>ctx).delref(None, lineno, True)
        else:
            (<object>ctx).delref(<object>p_obj, lineno, False)
        PyErr_Restore(<object>type, <object>value, <object>tb)
    except:
        Py_XDECREF(<object>type)
        Py_XDECREF(<object>value)
        Py_XDECREF(<object>tb)
        raise

cdef void INCREF(PyObject* ctx, PyObject* obj, int lineno):
    if obj is not NULL: Py_INCREF(<object>obj)
    GOTREF(ctx, obj, lineno)

cdef void DECREF(PyObject* ctx, PyObject* obj, int lineno):
    # GIVEREF raises exception if we hit 0
    GIVEREF(ctx, obj, lineno)
    if obj is not NULL: Py_DECREF(<object>obj)

cdef void FinishContext(PyObject** ctx):
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    if ctx == NULL: assert False
    if ctx[0] == NULL: assert False # XXX What to do here?
    cdef object errors = None
    PyErr_Fetch(&type, &value, &tb)
    try:
        errors = (<object>ctx[0]).end()
        pos = (<object>ctx[0]).filename, (<object>ctx[0]).name
        if errors:
            print u"%s: %s()" % pos
            print errors # raise Error(errors)
        PyErr_Restore(<object>type, <object>value, <object>tb)
    except:
        Py_XDECREF(<object>type)
        Py_XDECREF(<object>value)
        Py_XDECREF(<object>tb)
    finally:
        Py_XDECREF(<object>ctx[0])
        ctx[0] = NULL

cdef extern from "Python.h":
    object PyCObject_FromVoidPtr(void*, void (*)(void*))

ctypedef struct RefnannyAPIStruct:
  void (*INCREF)(PyObject*, PyObject*, int)
  void (*DECREF)(PyObject*, PyObject*, int)
  void (*GOTREF)(PyObject*, PyObject*, int)
  void (*GIVEREF)(PyObject*, PyObject*, int)
  PyObject* (*NewContext)(char*, int, char*) except NULL
  void (*FinishContext)(PyObject**)

cdef RefnannyAPIStruct api
api.INCREF = INCREF
api.DECREF =  DECREF
api.GOTREF =  GOTREF
api.GIVEREF = GIVEREF
api.NewContext = NewContext
api.FinishContext = FinishContext

RefnannyAPI = PyCObject_FromVoidPtr(<void*>&api, NULL)
