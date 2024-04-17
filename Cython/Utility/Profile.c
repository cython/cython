/////////////// Profile.proto ///////////////
//@requires: Exceptions.c::PyErrFetchRestore
//@substitute: naming

// Note that cPython ignores PyTrace_EXCEPTION,
// but maybe some other profilers don't.

#ifndef CYTHON_PROFILE
#if CYTHON_COMPILING_IN_LIMITED_API || CYTHON_COMPILING_IN_PYPY
  #define CYTHON_PROFILE 0
#else
  #define CYTHON_PROFILE 1
#endif
#endif

#ifndef CYTHON_TRACE_NOGIL
  #define CYTHON_TRACE_NOGIL 0
#else
  #if CYTHON_TRACE_NOGIL && !defined(CYTHON_TRACE)
    #define CYTHON_TRACE 1
  #endif
#endif

#ifndef CYTHON_TRACE
  #define CYTHON_TRACE 0
#endif

#if CYTHON_TRACE
  #undef CYTHON_PROFILE_REUSE_FRAME
#endif

#ifndef CYTHON_PROFILE_REUSE_FRAME
  #define CYTHON_PROFILE_REUSE_FRAME 0
#endif

#if CYTHON_PROFILE || CYTHON_TRACE

#if PY_VERSION_HEX >= 0x030d00B1
// Use the Py3.13 monitoring C-API: https://github.com/python/cpython/issues/111997

  // TODO: separate offset and lineno, calculate lineno and column
  // TODO: make list of event types specific to functions

  typedef enum {
      __Pyx_Monitoring_PY_START = 0,
      __Pyx_Monitoring_PY_RETURN,
      #if CYTHON_TRACE
      __Pyx_Monitoring_LINE,
      #endif
      __Pyx_Monitoring_RAISE,
      __Pyx_Monitoring_PY_RESUME,
      __Pyx_Monitoring_PY_YIELD,
      __Pyx_Monitoring_STOP_ITERATION,
  } __Pyx_Monitoring_Event_Index;

  static const unsigned char __Pyx_MonitoringEventTypes_CyFunc[] = {
      PY_MONITORING_EVENT_PY_START,
      PY_MONITORING_EVENT_PY_RETURN,
      //PY_MONITORING_EVENT_CALL,
      #if CYTHON_TRACE
      PY_MONITORING_EVENT_LINE,
      #endif
      PY_MONITORING_EVENT_RAISE,
  };

  #define __Pyx_MonitoringEventTypes_CyFunc_count (sizeof(__Pyx_MonitoringEventTypes_CyFunc) - 1)

  static const unsigned char __Pyx_MonitoringEventTypes_CyGen[] = {
      PY_MONITORING_EVENT_PY_START,
      PY_MONITORING_EVENT_PY_RETURN,
      //PY_MONITORING_EVENT_CALL,
      #if CYTHON_TRACE
      PY_MONITORING_EVENT_LINE,
      #endif
      PY_MONITORING_EVENT_RAISE,
      // generator specific:
      PY_MONITORING_EVENT_PY_RESUME,
      PY_MONITORING_EVENT_PY_YIELD,
      PY_MONITORING_EVENT_STOP_ITERATION,
  };

  #define __Pyx_MonitoringEventTypes_CyGen_count (sizeof(__Pyx_MonitoringEventTypes_CyGen) - 1)

  #define __Pyx_TraceDeclarations(is_gen)                                 \
      static PyCodeObject *$frame_code_cname = NULL;                      \
      PyMonitoringState $monitoring_states_cname[is_gen ? __Pyx_MonitoringEventTypes_CyGen_count : __Pyx_MonitoringEventTypes_CyFunc_count];

  #define __Pyx_IsTracing(event_id)  (($monitoring_states_cname[event_id]).active)
  #define __Pyx_TraceFrameInit(codeobj)

  static PyCodeObject *__Pyx_createFrameCodeObject(const char *funcname, const char *srcfile, int firstlineno); /*proto*/

  CYTHON_UNUSED static int __Pyx__TraceStart(PyMonitoringState *state_array, PyObject *code_obj, long firstlineno, int is_generator) {
      int ret;
      #if SIZEOF_LONG == 8
      unsigned long version = 0;
      #else
      unsigned long long version = 0;
      #endif
      ret = PyMonitoring_EnterScope(state_array, &version,
          is_generator ? __Pyx_MonitoringEventTypes_CyGen : __Pyx_MonitoringEventTypes_CyFunc,
          is_generator ? __Pyx_MonitoringEventTypes_CyGen_count : __Pyx_MonitoringEventTypes_CyFunc_count);
      if (unlikely(ret == -1)) return -1;
      return PyMonitoring_FirePyStartEvent(&state_array[__Pyx_Monitoring_PY_START], code_obj, firstlineno);
  }

  #define __Pyx_TraceStart(funcname, srcfile, firstlineno, nogil, goto_error) \
  if (1 /* __Pyx_IsTracing(__Pyx_Monitoring_PY_START) */) {                                          \
      int ret = 0;                                                                           \
      memset($monitoring_states_cname, 0, sizeof($monitoring_states_cname));                 \
      if (nogil) {                                                                           \
          if (CYTHON_TRACE_NOGIL) {                                                          \
              PyGILState_STATE state = PyGILState_Ensure();                                  \
              if (unlikely(!$frame_code_cname)) $frame_code_cname = __Pyx_createFrameCodeObject(funcname, srcfile, firstlineno); \
              if (unlikely(!$frame_code_cname)) goto_error;                                  \
              ret = __Pyx__TraceStart($monitoring_states_cname, (PyObject*) $frame_code_cname, firstlineno, 0); \
              PyGILState_Release(state);                                                     \
          }                                                                                  \
      } else {                                                                               \
          if (unlikely(!$frame_code_cname)) $frame_code_cname = __Pyx_createFrameCodeObject(funcname, srcfile, firstlineno); \
          if (unlikely(!$frame_code_cname)) goto_error;                                      \
          ret = __Pyx__TraceStart($monitoring_states_cname, (PyObject*) $frame_code_cname, firstlineno, 0); \
      }                                                                                      \
      if (unlikely(ret == -1)) goto_error;                                                   \
  }

  CYTHON_UNUSED static int __Pyx__TraceException(PyMonitoringState *monitoring_state, PyObject *code_obj, long offset) {
      int ret;
      PyObject *exc_value = PyErr_GetRaisedException();
      if (unlikely(!exc_value)) return 0;

      ret = PyMonitoring_FireRaiseEvent(monitoring_state, code_obj, offset, exc_value);
      if (unlikely(ret == -1)) {
          Py_DECREF(exc_value);
      } else {
          PyErr_SetRaisedException(exc_value);
      }
      return ret;
  }

  #define __Pyx_TraceException(lineno, goto_error) \
  if (__Pyx_IsTracing(__Pyx_Monitoring_RAISE)) {                                             \
      if (unlikely(__Pyx__TraceException(&$monitoring_states_cname[__Pyx_Monitoring_RAISE], (PyObject*) $frame_code_cname, lineno) == -1)) goto_error; \
  }

  // We do not trace function ends, just 'return' statements
  #define __Pyx_TraceReturn(result, lineno, nogil)

  // We assume that we own a safe reference to the returned value, usually in `__pyx_r`.
  #define __Pyx_TraceReturnValue(result, lineno, nogil, goto_error) \
  if (__Pyx_IsTracing(__Pyx_Monitoring_PY_RETURN)) {                                         \
      int ret = 0;                                                                           \
      if (nogil) {                                                                           \
          if (CYTHON_TRACE_NOGIL) {                                                          \
              PyGILState_STATE state = PyGILState_Ensure();                                  \
              ret = PyMonitoring_FirePyReturnEvent(&$monitoring_states_cname[__Pyx_Monitoring_PY_RETURN], (PyObject*) $frame_code_cname, lineno, result); \
              PyGILState_Release(state);                                                     \
          }                                                                                  \
      } else {                                                                               \
          ret = PyMonitoring_FirePyReturnEvent(&$monitoring_states_cname[__Pyx_Monitoring_PY_RETURN], (PyObject*) $frame_code_cname, lineno, result); \
      }                                                                                      \
      if (unlikely(ret == -1)) goto_error;                                                   \
  }

  #define __Pyx_TraceReturnCValue(cresult, convert_function, lineno, nogil, goto_error) \
  if (__Pyx_IsTracing(__Pyx_Monitoring_PY_RETURN)) {                                         \
      int ret = 0;                                                                           \
      if (nogil) {                                                                           \
          if (CYTHON_TRACE_NOGIL) {                                                          \
              PyGILState_STATE state = PyGILState_Ensure();                                  \
              PyObject *pyvalue = convert_function(cresult);                                 \
              if (unlikely(!pyvalue)) goto_error;                                            \
              ret = PyMonitoring_FirePyReturnEvent(&$monitoring_states_cname[__Pyx_Monitoring_PY_RETURN], (PyObject*) $frame_code_cname, lineno, pyvalue); \
              Py_DECREF(pyvalue);                                                            \
              PyGILState_Release(state);                                                     \
          }                                                                                  \
      } else {                                                                               \
          PyObject *pyvalue = convert_function(cresult);                                     \
          if (unlikely(!pyvalue)) goto_error;                                                \
          ret = PyMonitoring_FirePyReturnEvent(&$monitoring_states_cname[__Pyx_Monitoring_PY_RETURN], (PyObject*) $frame_code_cname, lineno, pyvalue); \
          Py_DECREF(pyvalue);                                                                \
      }                                                                                      \
      if (unlikely(ret == -1)) goto_error;                                                   \
  }

  #if CYTHON_TRACE
  #define __Pyx_TraceLine(lineno, nogil, goto_error) \
  if (__Pyx_IsTracing(__Pyx_Monitoring_LINE)) {                                              \
      int ret = 0;                                                                           \
      if (nogil) {                                                                           \
          if (CYTHON_TRACE_NOGIL) {                                                          \
              PyGILState_STATE state = PyGILState_Ensure();                                  \
              ret = PyMonitoring_FireLineEvent(&$monitoring_states_cname[__Pyx_Monitoring_LINE], (PyObject*) $frame_code_cname, lineno, lineno); \
              PyGILState_Release(state);                                                     \
          }                                                                                  \
      } else {                                                                               \
          ret = PyMonitoring_FireLineEvent(&$monitoring_states_cname[__Pyx_Monitoring_LINE], (PyObject*) $frame_code_cname, lineno, lineno); \
      }                                                                                      \
      if (unlikely(ret == -1)) goto_error;                                                   \
  }
  #endif

#else
// Use pre-Py3.12 profiling/tracing "C-API".

  #include "compile.h"
  #include "frameobject.h"
  #include "traceback.h"
#if PY_VERSION_HEX >= 0x030b00a6
  #ifndef Py_BUILD_CORE
    #define Py_BUILD_CORE 1
  #endif
  #include "internal/pycore_frame.h"
#endif

  #if CYTHON_PROFILE_REUSE_FRAME
    #define CYTHON_FRAME_MODIFIER static
    #define CYTHON_FRAME_DEL(frame)
  #else
    #define CYTHON_FRAME_MODIFIER
    #define CYTHON_FRAME_DEL(frame) Py_CLEAR(frame)
  #endif

  #define __Pyx_TraceDeclarations(is_gen)                                 \
      static PyCodeObject *$frame_code_cname = NULL;                      \
      CYTHON_FRAME_MODIFIER PyFrameObject *$frame_cname = NULL;           \
      int __Pyx_use_tracing = 0;

  #define __Pyx_TraceFrameInit(codeobj)                                   \
      if (codeobj) $frame_code_cname = (PyCodeObject*) codeobj;


#if PY_VERSION_HEX >= 0x030b00a2
  #if PY_VERSION_HEX >= 0x030C00b1
  #define __Pyx_IsTracing(tstate, check_tracing, check_funcs) \
     ((!(check_tracing) || !(tstate)->tracing) && \
         (!(check_funcs) || (tstate)->c_profilefunc || (CYTHON_TRACE && (tstate)->c_tracefunc)))
  #else
  #define __Pyx_IsTracing(tstate, check_tracing, check_funcs) \
     (unlikely((tstate)->cframe->use_tracing) && \
         (!(check_tracing) || !(tstate)->tracing) && \
         (!(check_funcs) || (tstate)->c_profilefunc || (CYTHON_TRACE && (tstate)->c_tracefunc)))
  #endif

  #define __Pyx_EnterTracing(tstate)  PyThreadState_EnterTracing(tstate)
  #define __Pyx_LeaveTracing(tstate)  PyThreadState_LeaveTracing(tstate)

#elif PY_VERSION_HEX >= 0x030a00b1
  #define __Pyx_IsTracing(tstate, check_tracing, check_funcs) \
     (unlikely((tstate)->cframe->use_tracing) && \
         (!(check_tracing) || !(tstate)->tracing) && \
         (!(check_funcs) || (tstate)->c_profilefunc || (CYTHON_TRACE && (tstate)->c_tracefunc)))

  #define __Pyx_EnterTracing(tstate) \
      do { tstate->tracing++; tstate->cframe->use_tracing = 0; } while (0)

  #define __Pyx_LeaveTracing(tstate) \
      do { \
          tstate->tracing--; \
          tstate->cframe->use_tracing = ((CYTHON_TRACE && tstate->c_tracefunc != NULL) \
                                 || tstate->c_profilefunc != NULL); \
      } while (0)

#else
  #define __Pyx_IsTracing(tstate, check_tracing, check_funcs) \
     (unlikely((tstate)->use_tracing) && \
         (!(check_tracing) || !(tstate)->tracing) && \
         (!(check_funcs) || (tstate)->c_profilefunc || (CYTHON_TRACE && (tstate)->c_tracefunc)))

  #define __Pyx_EnterTracing(tstate) \
      do { tstate->tracing++; tstate->use_tracing = 0; } while (0)

  #define __Pyx_LeaveTracing(tstate) \
      do { \
          tstate->tracing--; \
          tstate->use_tracing = ((CYTHON_TRACE && tstate->c_tracefunc != NULL) \
                                         || tstate->c_profilefunc != NULL); \
      } while (0)

#endif

  #define __Pyx_TraceStart(funcname, srcfile, firstlineno, nogil, goto_error)             \
  if (nogil) {                                                                           \
      if (CYTHON_TRACE_NOGIL) {                                                          \
          PyThreadState *tstate;                                                         \
          PyGILState_STATE state = PyGILState_Ensure();                                  \
          tstate = __Pyx_PyThreadState_Current;                                          \
          if (__Pyx_IsTracing(tstate, 1, 1)) {                                           \
              __Pyx_use_tracing = __Pyx_TraceSetupAndCall(&$frame_code_cname, &$frame_cname, tstate, funcname, srcfile, firstlineno);  \
          }                                                                              \
          PyGILState_Release(state);                                                     \
          if (unlikely(__Pyx_use_tracing < 0)) goto_error;                               \
      }                                                                                  \
  } else {                                                                               \
      PyThreadState* tstate = PyThreadState_GET();                                       \
      if (__Pyx_IsTracing(tstate, 1, 1)) {                                               \
          __Pyx_use_tracing = __Pyx_TraceSetupAndCall(&$frame_code_cname, &$frame_cname, tstate, funcname, srcfile, firstlineno);  \
          if (unlikely(__Pyx_use_tracing < 0)) goto_error;                               \
      }                                                                                  \
  }

  #define __Pyx_TraceException(lineno, goto_error)                                         \
  if (likely(!__Pyx_use_tracing)); else {                                                  \
      PyThreadState* tstate = __Pyx_PyThreadState_Current;                                 \
      if (__Pyx_IsTracing(tstate, 0, 1)) {                                                 \
          __Pyx_EnterTracing(tstate);                                                      \
          PyObject *exc_info = __Pyx_GetExceptionTuple(tstate);                            \
          if (exc_info) {                                                                  \
              if (CYTHON_TRACE && tstate->c_tracefunc)                                     \
                  tstate->c_tracefunc(                                                     \
                      tstate->c_traceobj, $frame_cname, PyTrace_EXCEPTION, exc_info);      \
              tstate->c_profilefunc(                                                       \
                  tstate->c_profileobj, $frame_cname, PyTrace_EXCEPTION, exc_info);        \
              Py_DECREF(exc_info);                                                         \
          }                                                                                \
          __Pyx_LeaveTracing(tstate);                                                      \
      }                                                                                    \
      if ((1)); else goto_error;                                                           \
  }

  static void __Pyx_call_return_trace_func(PyThreadState *tstate, PyFrameObject *frame, PyObject *result) {
      PyObject *type, *value, *traceback;
      __Pyx_ErrFetchInState(tstate, &type, &value, &traceback);
      __Pyx_EnterTracing(tstate);
      if (CYTHON_TRACE && tstate->c_tracefunc)
          tstate->c_tracefunc(tstate->c_traceobj, frame, PyTrace_RETURN, result);
      if (tstate->c_profilefunc)
          tstate->c_profilefunc(tstate->c_profileobj, frame, PyTrace_RETURN, result);
      CYTHON_FRAME_DEL(frame);
      __Pyx_LeaveTracing(tstate);
      __Pyx_ErrRestoreInState(tstate, type, value, traceback);
  }

  // We do not trace "return value", just function exits
  #define __Pyx_TraceReturnValue(result, lineno, nogil, goto_error) \
      if ((1)); else goto_error;

  #define __Pyx_TraceReturnCValue(cresult, convert_function, lineno, nogil, goto_error) \
      if ((1)); else { (void) convert_function; goto_error }

  #define __Pyx_TraceReturn(result, nogil)                                                \
  if (likely(!__Pyx_use_tracing)); else {                                                 \
      if (nogil) {                                                                        \
          if (CYTHON_TRACE_NOGIL) {                                                       \
              PyThreadState *tstate;                                                      \
              PyGILState_STATE state = PyGILState_Ensure();                               \
              tstate = __Pyx_PyThreadState_Current;                                       \
              if (__Pyx_IsTracing(tstate, 0, 0)) {                                        \
                  __Pyx_call_return_trace_func(tstate, $frame_cname, (PyObject*)result);  \
              }                                                                           \
              PyGILState_Release(state);                                                  \
          }                                                                               \
      } else {                                                                            \
          PyThreadState* tstate = __Pyx_PyThreadState_Current;                            \
          if (__Pyx_IsTracing(tstate, 0, 0)) {                                            \
              __Pyx_call_return_trace_func(tstate, $frame_cname, (PyObject*)result);      \
          }                                                                               \
      }                                                                                   \
  }

  static int __Pyx_TraceSetupAndCall(PyCodeObject** code, PyFrameObject** frame, PyThreadState* tstate, const char *funcname, const char *srcfile, int firstlineno); /*proto*/

// End of pre-monitoring implementation (Py<3.12)
#endif

#else

  #define __Pyx_TraceDeclarations(is_gen)
  #define __Pyx_TraceFrameInit(codeobj)
  // mark error label as used to avoid compiler warnings
  #define __Pyx_TraceStart(funcname, srcfile, firstlineno, nogil, goto_error)   if ((1)); else goto_error;
  #define __Pyx_TraceException(lineno, goto_error)   if ((1)); else goto_error;
  #define __Pyx_TraceReturn(result, nogil)

#endif /* CYTHON_PROFILE || CYTHON_TRACE */


#if CYTHON_TRACE && PY_VERSION_HEX < 0x030C0000
  // see call_trace_protected() in CPython's ceval.c
  static int __Pyx_call_line_trace_func(PyThreadState *tstate, PyFrameObject *frame, int lineno) {
      // see call_trace_protected() in CPython's ceval.c
      int ret;
      PyObject *type, *value, *traceback;
      __Pyx_ErrFetchInState(tstate, &type, &value, &traceback);
      __Pyx_PyFrame_SetLineNumber(frame, lineno);
      __Pyx_EnterTracing(tstate);

      ret = tstate->c_tracefunc(tstate->c_traceobj, frame, PyTrace_LINE, NULL);

      __Pyx_LeaveTracing(tstate);
      if (likely(!ret)) {
          __Pyx_ErrRestoreInState(tstate, type, value, traceback);
      } else {
          Py_XDECREF(type);
          Py_XDECREF(value);
          Py_XDECREF(traceback);
      }
      return ret;
  }

  #define __Pyx_TraceLine(lineno, nogil, goto_error)                                       \
  if (likely(!__Pyx_use_tracing)); else {                                                  \
      int ret = 0;                                                                         \
      if (nogil) {                                                                         \
          if (CYTHON_TRACE_NOGIL) {                                                        \
              PyThreadState *tstate;                                                       \
              PyGILState_STATE state = __Pyx_PyGILState_Ensure();                          \
              tstate = __Pyx_PyThreadState_Current;                                        \
              if (__Pyx_IsTracing(tstate, 0, 0) && tstate->c_tracefunc && $frame_cname->f_trace) { \
                  ret = __Pyx_call_line_trace_func(tstate, $frame_cname, lineno);          \
              }                                                                            \
              __Pyx_PyGILState_Release(state);                                             \
          }                                                                                \
      } else {                                                                             \
          PyThreadState* tstate = __Pyx_PyThreadState_Current;                             \
          if (__Pyx_IsTracing(tstate, 0, 0) && tstate->c_tracefunc && $frame_cname->f_trace) { \
              ret = __Pyx_call_line_trace_func(tstate, $frame_cname, lineno);              \
          }                                                                                \
      }                                                                                    \
      if (unlikely(ret)) goto_error;                                                       \
  }

#elif !CYTHON_TRACE
  // mark error label as used to avoid compiler warnings
  #define __Pyx_TraceLine(lineno, nogil, goto_error)   if ((1)); else goto_error;
#endif

/////////////// Profile ///////////////
//@substitute: naming

#if CYTHON_PROFILE

static PyCodeObject *__Pyx_createFrameCodeObject(const char *funcname, const char *srcfile, int firstlineno) {
    PyCodeObject *py_code = PyCode_NewEmpty(srcfile, funcname, firstlineno);
    // make CPython use a fresh dict for "f_locals" at need (see GH #1836)
    if (likely(py_code)) {
        py_code->co_flags |= CO_OPTIMIZED | CO_NEWLOCALS;
    }
    return py_code;
}

#if PY_VERSION_HEX < 0x030d00B1

static int __Pyx_TraceSetupAndCall(PyCodeObject** code,
                                   PyFrameObject** frame,
                                   PyThreadState* tstate,
                                   const char *funcname,
                                   const char *srcfile,
                                   int firstlineno) {
    PyObject *type, *value, *traceback;
    int retval;
    if (*frame == NULL || !CYTHON_PROFILE_REUSE_FRAME) {
        if (*code == NULL) {
            *code = __Pyx_createFrameCodeObject(funcname, srcfile, firstlineno);
            if (*code == NULL) return 0;
        }
        *frame = PyFrame_New(
            tstate,                          /*PyThreadState *tstate*/
            *code,                           /*PyCodeObject *code*/
            $moddict_cname,                  /*PyObject *globals*/
            0                                /*PyObject *locals*/
        );
        if (*frame == NULL) return 0;
        if (CYTHON_TRACE && (*frame)->f_trace == NULL) {
            // this enables "f_lineno" lookup, at least in CPython ...
            Py_INCREF(Py_None);
            (*frame)->f_trace = Py_None;
        }
    }
    __Pyx_PyFrame_SetLineNumber(*frame, firstlineno);

    retval = 1;
    __Pyx_EnterTracing(tstate);
    __Pyx_ErrFetchInState(tstate, &type, &value, &traceback);

    #if CYTHON_TRACE
    if (tstate->c_tracefunc)
        retval = tstate->c_tracefunc(tstate->c_traceobj, *frame, PyTrace_CALL, NULL) == 0;
    if (retval && tstate->c_profilefunc)
    #endif
        retval = tstate->c_profilefunc(tstate->c_profileobj, *frame, PyTrace_CALL, NULL) == 0;

    __Pyx_LeaveTracing(tstate);
    if (retval) {
        __Pyx_ErrRestoreInState(tstate, type, value, traceback);
        return __Pyx_IsTracing(tstate, 0, 0) && retval;
    } else {
        Py_XDECREF(type);
        Py_XDECREF(value);
        Py_XDECREF(traceback);
        return -1;
    }
}

#endif
#endif /* CYTHON_PROFILE */
