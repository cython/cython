from cpython.ref cimport PyObject, Py_INCREF, Py_DECREF, Py_XDECREF
from cpython.exc cimport PyErr_Fetch, PyErr_Restore
from cpython.pystate cimport PyThreadState_Get


loglevel = 0
reflog = []

cdef log(level, action, obj, lineno):
    if loglevel >= level:
        reflog.append((lineno, action, id(obj)))

LOG_NONE, LOG_ALL = range(2)

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
        # returns whether it is ok to do the decref operation
        log(LOG_ALL, u'delref', u"<NULL>" if is_null else obj, lineno)
        if is_null:
            self.errors.append(u"NULL argument on line %d" % lineno)
            return False
        id_ = id(obj)
        count, linenumbers = self.refs.get(id_, (0, []))
        if count == 0:
            self.errors.append(u"Too many decrefs on line %d, reference acquired on lines %r" %
                (lineno, linenumbers))
            return False
        elif count == 1:
            del self.refs[id_]
            return True
        else:
            self.refs[id_] = (count - 1, linenumbers)
            return True

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

cdef void report_unraisable(object e=None):
    try:
        if e is None:
            import sys
            e = sys.exc_info()[1]
        print u"refnanny raised an exception: %s" % e
    except:
        pass # We absolutely cannot exit with an exception

# All Python operations must happen after any existing
# exception has been fetched, in case we are called from
# exception-handling code.

cdef PyObject* SetupContext(char* funcname, int lineno, char* filename) except NULL:
    if Context is None:
        # Context may be None during finalize phase.
        # In that case, we don't want to be doing anything fancy
        # like caching and resetting exceptions.
        return NULL
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    cdef PyObject* result = NULL
    PyThreadState_Get()
    PyErr_Fetch(&type, &value, &tb)
    try:
        ctx = Context(funcname, lineno, filename)
        Py_INCREF(ctx)
        result = <PyObject*>ctx
    except Exception, e:
        report_unraisable(e)
    PyErr_Restore(type, value, tb)
    return result

cdef void GOTREF(PyObject* ctx, PyObject* p_obj, int lineno):
    if ctx == NULL: return
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    PyErr_Fetch(&type, &value, &tb)
    try:
        try:
            if p_obj is NULL:
                (<object>ctx).regref(None, lineno, True)
            else:
                (<object>ctx).regref(<object>p_obj, lineno, False)
        except:
            report_unraisable()
    except:
        # __Pyx_GetException may itself raise errors
        pass
    PyErr_Restore(type, value, tb)

cdef int GIVEREF_and_report(PyObject* ctx, PyObject* p_obj, int lineno):
    if ctx == NULL: return 1
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    cdef bint decref_ok = False
    PyErr_Fetch(&type, &value, &tb)
    try:
        try:
            if p_obj is NULL:
                decref_ok = (<object>ctx).delref(None, lineno, True)
            else:
                decref_ok = (<object>ctx).delref(<object>p_obj, lineno, False)
        except:
            report_unraisable()
    except:
        # __Pyx_GetException may itself raise errors
        pass
    PyErr_Restore(type, value, tb)
    return decref_ok

cdef void GIVEREF(PyObject* ctx, PyObject* p_obj, int lineno):
    GIVEREF_and_report(ctx, p_obj, lineno)

cdef void INCREF(PyObject* ctx, PyObject* obj, int lineno):
    if obj is not NULL: Py_INCREF(<object>obj)
    PyThreadState_Get()
    GOTREF(ctx, obj, lineno)

cdef void DECREF(PyObject* ctx, PyObject* obj, int lineno):
    if GIVEREF_and_report(ctx, obj, lineno):
        if obj is not NULL: Py_DECREF(<object>obj)
    PyThreadState_Get()

cdef void FinishContext(PyObject** ctx):
    if ctx == NULL or ctx[0] == NULL: return
    cdef PyObject* type = NULL, *value = NULL, *tb = NULL
    cdef object errors = None
    PyThreadState_Get()
    PyErr_Fetch(&type, &value, &tb)
    try:
        try:
            errors = (<object>ctx[0]).end()
            pos = (<object>ctx[0]).filename, (<object>ctx[0]).name
            if errors:
                print u"%s: %s()" % pos
                print errors
        except:
            report_unraisable()
    except:
        # __Pyx_GetException may itself raise errors
        pass
    Py_DECREF(<object>ctx[0])
    ctx[0] = NULL
    PyErr_Restore(type, value, tb)

ctypedef struct RefNannyAPIStruct:
  void (*INCREF)(PyObject*, PyObject*, int)
  void (*DECREF)(PyObject*, PyObject*, int)
  void (*GOTREF)(PyObject*, PyObject*, int)
  void (*GIVEREF)(PyObject*, PyObject*, int)
  PyObject* (*SetupContext)(char*, int, char*) except NULL
  void (*FinishContext)(PyObject**)

cdef RefNannyAPIStruct api
api.INCREF = INCREF
api.DECREF =  DECREF
api.GOTREF =  GOTREF
api.GIVEREF = GIVEREF
api.SetupContext = SetupContext
api.FinishContext = FinishContext

cdef extern from "Python.h":
    object PyLong_FromVoidPtr(void*)

RefNannyAPI = PyLong_FromVoidPtr(<void*>&api)
