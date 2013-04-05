/////////////// Profile.proto ///////////////
//@substitute: naming

// Note that cPython ignores PyTrace_EXCEPTION,
// but maybe some other profilers don't.

#ifndef CYTHON_PROFILE
  #define CYTHON_PROFILE 1
#endif

#ifndef CYTHON_PROFILE_REUSE_FRAME
  #define CYTHON_PROFILE_REUSE_FRAME 0
#endif

#if CYTHON_PROFILE

  #include "compile.h"
  #include "frameobject.h"
  #include "traceback.h"

  #if CYTHON_PROFILE_REUSE_FRAME
    #define CYTHON_FRAME_MODIFIER static
    #define CYTHON_FRAME_DEL
  #else
    #define CYTHON_FRAME_MODIFIER
    #define CYTHON_FRAME_DEL Py_DECREF($frame_cname)
  #endif

  #define __Pyx_TraceDeclarations                                  \
  static PyCodeObject *$frame_code_cname = NULL;                      \
  CYTHON_FRAME_MODIFIER PyFrameObject *$frame_cname = NULL;           \
  int __Pyx_use_tracing = 0;

  #define __Pyx_TraceCall(funcname, srcfile, firstlineno)                            \
  if (unlikely(PyThreadState_GET()->use_tracing && PyThreadState_GET()->c_profilefunc)) {      \
      __Pyx_use_tracing = __Pyx_TraceSetupAndCall(&$frame_code_cname, &$frame_cname, funcname, srcfile, firstlineno);  \
  }

  #define __Pyx_TraceException()                                                           \
  if (unlikely(__Pyx_use_tracing( && PyThreadState_GET()->use_tracing && PyThreadState_GET()->c_profilefunc) {  \
      PyObject *exc_info = __Pyx_GetExceptionTuple();                                      \
      if (exc_info) {                                                                      \
          PyThreadState_GET()->c_profilefunc(                                              \
              PyThreadState_GET()->c_profileobj, $frame_cname, PyTrace_EXCEPTION, exc_info);  \
          Py_DECREF(exc_info);                                                             \
      }                                                                                    \
  }

  #define __Pyx_TraceReturn(result)                                                  \
  if (unlikely(__Pyx_use_tracing) && PyThreadState_GET()->use_tracing && PyThreadState_GET()->c_profilefunc) {  \
      PyThreadState_GET()->c_profilefunc(                                            \
          PyThreadState_GET()->c_profileobj, $frame_cname, PyTrace_RETURN, (PyObject*)result);     \
      CYTHON_FRAME_DEL;                                                              \
  }

  static PyCodeObject *__Pyx_createFrameCodeObject(const char *funcname, const char *srcfile, int firstlineno); /*proto*/
  static int __Pyx_TraceSetupAndCall(PyCodeObject** code, PyFrameObject** frame, const char *funcname, const char *srcfile, int firstlineno); /*proto*/

#else

  #define __Pyx_TraceDeclarations
  #define __Pyx_TraceCall(funcname, srcfile, firstlineno)
  #define __Pyx_TraceException()
  #define __Pyx_TraceReturn(result)

#endif /* CYTHON_PROFILE */

/////////////// Profile ///////////////
//@substitute: naming

#if CYTHON_PROFILE

static int __Pyx_TraceSetupAndCall(PyCodeObject** code,
                                   PyFrameObject** frame,
                                   const char *funcname,
                                   const char *srcfile,
                                   int firstlineno) {
    if (*frame == NULL || !CYTHON_PROFILE_REUSE_FRAME) {
        if (*code == NULL) {
            *code = __Pyx_createFrameCodeObject(funcname, srcfile, firstlineno);
            if (*code == NULL) return 0;
        }
        *frame = PyFrame_New(
            PyThreadState_GET(),             /*PyThreadState *tstate*/
            *code,                           /*PyCodeObject *code*/
            $moddict_cname,                  /*PyObject *globals*/
            0                                /*PyObject *locals*/
        );
        if (*frame == NULL) return 0;
    }
    else {
        (*frame)->f_tstate = PyThreadState_GET();
    }
    return PyThreadState_GET()->c_profilefunc(PyThreadState_GET()->c_profileobj, *frame, PyTrace_CALL, NULL) == 0;
}

static PyCodeObject *__Pyx_createFrameCodeObject(const char *funcname, const char *srcfile, int firstlineno) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyCodeObject *py_code = 0;

    #if PY_MAJOR_VERSION < 3
    py_funcname = PyString_FromString(funcname);
    py_srcfile = PyString_FromString(srcfile);
    #else
    py_funcname = PyUnicode_FromString(funcname);
    py_srcfile = PyUnicode_FromString(srcfile);
    #endif
    if (!py_funcname | !py_srcfile) goto bad;

    py_code = PyCode_New(
        0,                /*int argcount,*/
        #if PY_MAJOR_VERSION >= 3
        0,                /*int kwonlyargcount,*/
        #endif
        0,                /*int nlocals,*/
        0,                /*int stacksize,*/
        0,                /*int flags,*/
        $empty_bytes,     /*PyObject *code,*/
        $empty_tuple,     /*PyObject *consts,*/
        $empty_tuple,     /*PyObject *names,*/
        $empty_tuple,     /*PyObject *varnames,*/
        $empty_tuple,     /*PyObject *freevars,*/
        $empty_tuple,     /*PyObject *cellvars,*/
        py_srcfile,       /*PyObject *filename,*/
        py_funcname,      /*PyObject *name,*/
        firstlineno,      /*int firstlineno,*/
        $empty_bytes      /*PyObject *lnotab*/
    );

bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);

    return py_code;
}

#endif /* CYTHON_PROFILE */
