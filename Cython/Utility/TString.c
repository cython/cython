//////////////////////////// GetTemplateLib.proto ///////////////////////////

// "Public" interface is __Pyx_GetTemplateLib, defined by GetLazyCachedObjec
static PyObject* __Pyx_InitializeTemplateLib(void); /* proto */


//////////////////////////// GetTemplateLib ///////////////////////////
//@requires: Exceptions.c::IgnoreException
//@requires: Synchronization.c::GetLazyCachedObject{"guard": 1, "object_cname": "__pyx_templatelib_module", "maker_cname": "__Pyx_InitializeTemplateLib", "getter_cname": "__Pyx_GetTemplateLib"}

#if __PYX_LIMITED_VERSION_HEX < 0x030E0000
static PyObject *__Pyx_TemplateLibFallback(void) {
    if (!__Pyx_IgnoreException(PyExc_Exception)) {
        return NULL; // BaseException
    }

    // The assumption here is that Interpolation and Template are fairly simple classes
    // and the cost of compiling them with Cython (for all Python versions) is probably
    // higher than the cost of using a plain-Python fallback. 
    const char code_str[] = CSTRING("""
class Interpolation:
    __module__ = 'string.templatelib'
    __slots__ = __match_args__ = ('value', 'expression', 'conversion', 'format_spec')
    def __setattr__(self, attr, value):
        raise AttributeError('Interpolation is immutable')
    def __new__(cls, value, expression='', conversion=None, format_spec=''):
        obj = super().__new__(cls)
        super().__setattr__(obj, 'value', value)
        super().__setattr__(obj, 'expression', expression)
        super().__setattr__(obj, 'conversion', conversion)
        super().__setattr__(obj, 'format_spec', format_spec)
        return obj
    def __repr__(self):
        return f'Interpolation({self.value!r}, {self.expression!r}, {self.conversion!r}, {self.format_spec!r})'
    def __reduce__(self):
        # This probably won't work unless a t-string has already been created from Cython
        return (type(self), (self.value, self.expression, self.conversion, self.format_spec))
    def __init_subclass__(cls, **kwds):
        raise TypeError('Interpolation is not an acceptable base type')
class Template:
    __module__ = 'string.templatelib'
    __slots__ = ('strings', 'interpolations')
    def __setattr__(self, attr, value):
        raise AttributeError('Template is immutable')
    def __new__(cls, *args, strings=None, interpolations=None):
        if strings is None and interpolations is None:
            strings = []
            interpolations = []
            last_string = ''
            for arg in args:
                if isinstance(arg, str):
                    last_string += arg
                elif isinstance(arg, Interpolation):
                    strings.append(last_string)
                    last_string = ''
                    interpolations.append(arg)
                else:
                    raise TypeError('Unexpected argument to Template')
            strings.append(last_string)
        else:
            if args:
                raise ValueError("'strings' or 'interpolations' should not be passed with positional arguments")
            if strings is None: strings = ()
            if interpolations is None: interpolations = ()
        obj = super().__new__(cls)
        super().__setattr__(obj, 'strings', tuple(strings))
        super().__setattr__(obj, 'interpolations', tuple(interpolations))
        return obj
    def __repr__(self):
        return f'Template(strings={self.strings!r}, interpolations={self.interpolations!r})'
    def __reduce__(self):
        # This probably won't work unless a t-string has already been created from Cython.
        # It also doesn't quite match how CPython pickles them.
        values = tuple(iter(self))
        return (type(self), values)
    def __iter__(self):
        for n in range(len(self.interpolations)):
            if (s := self.strings[n]):
               yield s
            yield self.interpolations[n]
        if (s := self.strings[-1]):
           yield s
    def __add__(self, other):
        if not (isinstance(self, Template) and isinstance(other, Template)):
            raise TypeError('can only concatenate Template to Template')
        interpolations = self.interpolations + other.interpolations
        middle_string = self.strings[-1] + other.strings[0]
        strings = self.strings[:-1] + (middle_string,) + other.strings[1:]
        return Template(strings=strings, interpolations=interpolations)
    @property
    def values(self):
        return tuple(i.value for i in self.interpolations)
    def __init_subclass__(cls, **kwds):
        raise TypeError('Template is not an acceptable base type')
""");

    PyObject *code=NULL, *eval_result=NULL, *module=NULL, *module_dict=NULL;
    PyObject *dict = PyDict_New();
    if (unlikely(!dict)) return NULL;
#if __PYX_LIMITED_VERSION_HEX < 0x030A0000
    {
        PyObject *builtins = PyEval_GetBuiltins();
        if (unlikely(!builtins)) goto end;
        if (unlikely(PyDict_SetItemString(dict, "__builtins__", builtins) < 0)) goto end;
    }
#endif
    
    code = Py_CompileString(code_str, "<cython string.templatelib fallback>", Py_file_input);
    if (unlikely(!code)) goto end;
    eval_result = PyEval_EvalCode(code, dict, NULL);
    Py_DECREF(code);
    if (unlikely(!eval_result)) goto end;
    Py_DECREF(eval_result);

    module = __Pyx_PyImport_AddModuleRef("string.templatelib");
    if (!module) goto end;
    module_dict = PyModule_GetDict(module);
    if (!module_dict) goto bad;
    if (unlikely(PyDict_Merge(module_dict, dict, 0) < 0)) goto bad;

  end:
    Py_XDECREF(dict);
    return module;
  bad:
    Py_CLEAR(module);
    goto end;
}
#endif

static PyObject* __Pyx_InitializeTemplateLib(void) {
    // Even in earlier versions of Python, still try the import. We're happy
    // to use what's there if someone's patched it with something compatible.
    PyObject *templatelib = PyImport_ImportModule("string.templatelib");
    if (!templatelib) {
#if __PYX_LIMITED_VERSION_HEX < 0x030E0000
        templatelib = __Pyx_TemplateLibFallback();
#endif
    }
    return templatelib;
}


//////////////////////////// MakeTemplateLibInterpolation.proto //////////////////////

static PyObject* __Pyx_MakeTemplateLibInterpolation(PyObject *value, PyObject *expression, PyObject *conversion_char, PyObject *format_spec); /* proto */

static PyObject *__Pyx__GetTemplateInterpolationType(void); /* proto */


//////////////////////////// MakeTemplateLibInterpolation ////////////////////////
//@requires: GetTemplateLib
//@requires: ObjectHandling.c::PyObjectFastCall
//@requires: Synchronization.c::GetLazyCachedObject{"guard": 1, "object_cname": "__pyx_templatelib_Interpolation", "maker_cname": "__Pyx__GetTemplateInterpolationType", "getter_cname": "__Pyx_GetTemplateInterpolationType"}

static PyObject *__Pyx__GetTemplateInterpolationType(void) {
    PyObject *lib = __Pyx_GetTemplateLib();
    if (!lib) return NULL;
    return PyObject_GetAttrString(lib, "Interpolation");
}

static PyObject* __Pyx_MakeTemplateLibInterpolation(PyObject *value, PyObject *expression, PyObject *conversion_char, PyObject *format_spec) {
    PyObject *tp = __Pyx_GetTemplateInterpolationType();
    if (unlikely(!tp)) return NULL;
    PyObject *args[] = {value, expression, conversion_char, format_spec};

    PyObject *result = __Pyx_PyObject_FastCallDict(tp, args, 4, NULL);
    Py_DECREF(tp);

    return result;
}

//////////////////////////// MakeTemplateLibTemplate.proto //////////////////////

static PyObject* __Pyx_MakeTemplateLibTemplate(PyObject *strings, PyObject *interpolations); /* proto */

#if !(PY_VERSION_HEX >= 0x030E0000 && CYTHON_COMPILING_IN_CPYTHON)
static PyObject *__Pyx__GetTemplateTemplateType(void); /* proto */
#endif

//////////////////////////// MakeTemplateLibTemplate ////////////////////////
//@requires: GetTemplateLib
//@requires: ObjectHandling.c::PyObjectVectorCallKwBuilder
//@requires: Synchronization.c::GetLazyCachedObject{"guard": "!(PY_VERSION_HEX >= 0x030E0000 && CYTHON_COMPILING_IN_CPYTHON)", "object_cname": "__pyx_templatelib_Template", "maker_cname": "__Pyx__GetTemplateTemplateType", "getter_cname": "__Pyx_GetTemplateTemplateType"}


#if PY_VERSION_HEX >= 0x030E0000 && CYTHON_COMPILING_IN_CPYTHON
#ifndef Py_BUILD_CORE
#define Py_BUILD_CORE
#endif
#include "internal/pycore_template.h"

static PyObject* __Pyx_MakeTemplateLibTemplate(PyObject *strings, PyObject *interpolations) {
    return _PyTemplate_Build(strings, interpolations);
}
#else

static PyObject *__Pyx__GetTemplateTemplateType(void) {
    PyObject *lib = __Pyx_GetTemplateLib();
    if (!lib) return NULL;
    return PyObject_GetAttrString(lib, "Template");
}

static PyObject* __Pyx_MakeTemplateLibTemplate(PyObject *strings, PyObject *interpolations) {
    PyObject *tp = __Pyx_GetTemplateTemplateType();
    PyObject *result = NULL, *zipped_tuple = NULL;
    Py_ssize_t zipped_index = 0;
    if (unlikely(!tp)) return NULL;
    
#if __PYX_LIMITED_VERSION_HEX < 0x030E0000
    if (__Pyx_get_runtime_version() < 0x030E0000) {
        // There's a high chance (but not certain) that we're using our internal
        // fallback version of template. In this case we can try to use a better
        // constructor.
        PyObject *args[] = { NULL, NULL };
        PyObject *kwargs_builder = __Pyx_MakeVectorcallBuilderKwds(2);
        if (unlikely(!kwargs_builder)) goto failed_shortcut; 
        if (unlikely(__Pyx_VectorcallBuilder_AddArg(PYIDENT("strings"), strings, kwargs_builder, args, 0)<0))
            goto failed_shortcut;
        if (unlikely(__Pyx_VectorcallBuilder_AddArg(PYIDENT("interpolations"), interpolations, kwargs_builder, args, 1)<0))
            goto failed_shortcut;
        result = __Pyx_Object_Vectorcall_CallFromBuilder(tp, args, 0, kwargs_builder);
        Py_DECREF(kwargs_builder);
        if (result) {
            Py_DECREF(tp);
            return result;
        }

      failed_shortcut:
        Py_CLEAR(kwargs_builder);
        if (!__Pyx_IgnoreException(PyExc_Exception)) {
            return NULL; // BaseException
        }
    }
#endif

    // Slightly frustratingly, we have to go to the trouble of zipping together
    // the strings and the interpolations. And then internally the Template does
    // the exact opposite. 
    Py_ssize_t strings_len, interpolations_len;
    strings_len = __Pyx_PyTuple_GET_SIZE(strings);
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(strings_len < 0)) goto end;
#endif
    interpolations_len = __Pyx_PyTuple_GET_SIZE(interpolations);
#if !CYTHON_ASSUME_SAFE_SIZE
    if (unlikely(interpolations_len < 0)) goto end;
#endif
    zipped_tuple = PyTuple_New(strings_len + interpolations_len);
    if (!zipped_tuple) goto end;
    for (Py_ssize_t i=0; (i<interpolations_len || i<strings_len); ++i) {
        if (i < strings_len) {
            PyObject *s = __Pyx_PyTuple_GET_ITEM(strings, i);
#if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(!s)) goto end;
#endif
            Py_INCREF(s);
            if (unlikely(__Pyx_PyTuple_SET_ITEM(zipped_tuple, zipped_index, s) < 0)) goto end;
            ++zipped_index;
        }
        if (i < interpolations_len) {
            PyObject *interpolation = __Pyx_PyTuple_GET_ITEM(interpolations, i);
#if !CYTHON_ASSUME_SAFE_MACROS
            if (unlikely(!interpolation)) goto end;
#endif
            Py_INCREF(interpolation);
            if (unlikely(__Pyx_PyTuple_SET_ITEM(zipped_tuple, zipped_index, interpolation) < 0)) goto end;
            ++zipped_index;
        }
    }

    result = PyObject_CallObject(tp, zipped_tuple);

  end:
    Py_XDECREF(zipped_tuple);
    Py_DECREF(tp);
    return result;
}
#endif
