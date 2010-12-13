#
#   Pyrex - Builtin Definitions
#

from Symtab import BuiltinScope, StructOrUnionScope
from Code import UtilityCode
from TypeSlots import Signature
import PyrexTypes
import Naming


# C-level implementations of builtin types, functions and methods

pow2_utility_code = UtilityCode(
proto = """
#define __Pyx_PyNumber_Power2(a, b) PyNumber_Power(a, b, Py_None)
""")

include_string_h_utility_code = UtilityCode(
proto = """
#include <string.h>
"""
)

iter_next_utility_code = UtilityCode(
proto = """
#define __Pyx_PyIter_Next(obj) __Pyx_PyIter_Next2(obj, NULL);
static CYTHON_INLINE PyObject *__Pyx_PyIter_Next2(PyObject *, PyObject *); /*proto*/
""",
# copied from Py3's builtin_next()
impl = '''
static CYTHON_INLINE PyObject *__Pyx_PyIter_Next2(PyObject* iterator, PyObject* defval) {
    PyObject* next;
    if (unlikely(!PyIter_Check(iterator))) {
        PyErr_Format(PyExc_TypeError,
            "%.200s object is not an iterator", iterator->ob_type->tp_name);
        return NULL;
    }
    next = (*(Py_TYPE(iterator)->tp_iternext))(iterator);
    if (likely(next)) {
        return next;
    } else if (defval) {
        if (PyErr_Occurred()) {
            if(!PyErr_ExceptionMatches(PyExc_StopIteration))
                return NULL;
            PyErr_Clear();
        }
        Py_INCREF(defval);
        return defval;
    } else if (PyErr_Occurred()) {
        return NULL;
    } else {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }
}
''')

getattr3_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE PyObject *__Pyx_GetAttr3(PyObject *, PyObject *, PyObject *); /*proto*/
""",
impl = """
static CYTHON_INLINE PyObject *__Pyx_GetAttr3(PyObject *o, PyObject *n, PyObject *d) {
    PyObject *r = PyObject_GetAttr(o, n);
    if (!r) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError))
            goto bad;
        PyErr_Clear();
        r = d;
        Py_INCREF(d);
    }
    return r;
bad:
    return NULL;
}
""")

pyexec_utility_code = UtilityCode(
proto = """
#if PY_VERSION_HEX < 0x02040000
#ifndef Py_COMPILE_H
#include "compile.h"
#endif
#ifndef Py_EVAL_H
#include "eval.h"
#endif
#endif
static PyObject* __Pyx_PyRun(PyObject*, PyObject*, PyObject*);
static CYTHON_INLINE PyObject* __Pyx_PyRun2(PyObject*, PyObject*);
""",
impl = """
static CYTHON_INLINE PyObject* __Pyx_PyRun2(PyObject* o, PyObject* globals) {
    return __Pyx_PyRun(o, globals, NULL);
}

static PyObject* __Pyx_PyRun(PyObject* o, PyObject* globals, PyObject* locals) {
    PyObject* result;
    PyObject* s = 0;
    char *code = 0;

    if (!globals || globals == Py_None) {
        globals = PyModule_GetDict(%s);""" % Naming.module_cname + """
        if (!globals)
            goto bad;
    } else if (!PyDict_Check(globals)) {
        PyErr_Format(PyExc_TypeError, "exec() arg 2 must be a dict, not %.100s",
                     globals->ob_type->tp_name);
        goto bad;
    }
    if (!locals || locals == Py_None) {
        locals = globals;
    }


    if (PyDict_GetItemString(globals, "__builtins__") == NULL) {
        PyDict_SetItemString(globals, "__builtins__", PyEval_GetBuiltins());
    }

    if (PyCode_Check(o)) {
        if (PyCode_GetNumFree((PyCodeObject *)o) > 0) {
            PyErr_SetString(PyExc_TypeError,
                "code object passed to exec() may not contain free variables");
            goto bad;
        }
        #if PY_VERSION_HEX < 0x030200B1
        result = PyEval_EvalCode((PyCodeObject *)o, globals, locals);
        #else
        result = PyEval_EvalCode(o, globals, locals);
        #endif
    } else {
        PyCompilerFlags cf;
        cf.cf_flags = 0;
        if (PyUnicode_Check(o)) {
            cf.cf_flags = PyCF_SOURCE_IS_UTF8;
            s = PyUnicode_AsUTF8String(o);
            if (!s) goto bad;
            o = s;
        #if PY_MAJOR_VERSION >= 3
        } else if (!PyBytes_Check(o)) {
        #else
        } else if (!PyString_Check(o)) {
        #endif
            PyErr_SetString(PyExc_TypeError,
                "exec: arg 1 must be string, bytes or code object");
            goto bad;
        }
        #if PY_MAJOR_VERSION >= 3
        code = PyBytes_AS_STRING(o);
        #else
        code = PyString_AS_STRING(o);
        #endif
        if (PyEval_MergeCompilerFlags(&cf)) {
            result = PyRun_StringFlags(code, Py_file_input, globals, locals, &cf);
        } else {
            result = PyRun_String(code, Py_file_input, globals, locals);
        }
        Py_XDECREF(s);
    }

    return result;
bad:
    Py_XDECREF(s);
    return 0;
}
""")

intern_utility_code = UtilityCode(
proto = """
static PyObject* __Pyx_Intern(PyObject* s); /* proto */
""",
impl = '''
static PyObject* __Pyx_Intern(PyObject* s) {
    if (!(likely(PyString_CheckExact(s)))) {
        PyErr_Format(PyExc_TypeError, "Expected str, got %s", Py_TYPE(s)->tp_name);
        return 0;
    }
    Py_INCREF(s);
    #if PY_MAJOR_VERSION >= 3
    PyUnicode_InternInPlace(&s);
    #else
    PyString_InternInPlace(&s);
    #endif
    return s;
}
''')

def put_py23_set_init_utility_code(code, pos):
    code.putln("#if PY_VERSION_HEX < 0x02040000")
    code.putln(code.error_goto_if_neg("__Pyx_Py23SetsImport()", pos))
    code.putln("#endif")

py23_set_utility_code = UtilityCode(
proto = """
#if PY_VERSION_HEX < 0x02050000
#ifndef PyAnySet_CheckExact

#define PyAnySet_CheckExact(ob) \\
    ((ob)->ob_type == &PySet_Type || \\
     (ob)->ob_type == &PyFrozenSet_Type)

#define PySet_New(iterable) \\
    PyObject_CallFunctionObjArgs((PyObject *)&PySet_Type, (iterable), NULL)

#define Pyx_PyFrozenSet_New(iterable) \\
    PyObject_CallFunctionObjArgs((PyObject *)&PyFrozenSet_Type, (iterable), NULL)

#define PySet_Size(anyset) \\
    PyObject_Size((anyset))

#define PySet_Contains(anyset, key) \\
    PySequence_Contains((anyset), (key))

#define PySet_Pop(set) \\
    PyObject_CallMethod(set, (char *)"pop", NULL)

static CYTHON_INLINE int PySet_Clear(PyObject *set) {
    PyObject *ret = PyObject_CallMethod(set, (char *)"clear", NULL);
    if (!ret) return -1;
    Py_DECREF(ret); return 0;
}

static CYTHON_INLINE int PySet_Discard(PyObject *set, PyObject *key) {
    PyObject *ret = PyObject_CallMethod(set, (char *)"discard", (char *)"O", key);
    if (!ret) return -1;
    Py_DECREF(ret); return 0;
}

static CYTHON_INLINE int PySet_Add(PyObject *set, PyObject *key) {
    PyObject *ret = PyObject_CallMethod(set, (char *)"add", (char *)"O", key);
    if (!ret) return -1;
    Py_DECREF(ret); return 0;
}

#endif /* PyAnySet_CheckExact (<= Py2.4) */

#if PY_VERSION_HEX < 0x02040000
#ifndef Py_SETOBJECT_H
#define Py_SETOBJECT_H

static PyTypeObject *__Pyx_PySet_Type = NULL;
static PyTypeObject *__Pyx_PyFrozenSet_Type = NULL;

#define PySet_Type (*__Pyx_PySet_Type)
#define PyFrozenSet_Type (*__Pyx_PyFrozenSet_Type)

#define PyAnySet_Check(ob) \\
    (PyAnySet_CheckExact(ob) || \\
     PyType_IsSubtype((ob)->ob_type, &PySet_Type) || \\
     PyType_IsSubtype((ob)->ob_type, &PyFrozenSet_Type))

#define PyFrozenSet_CheckExact(ob) ((ob)->ob_type == &PyFrozenSet_Type)

static int __Pyx_Py23SetsImport(void) {
    PyObject *sets=0, *Set=0, *ImmutableSet=0;

    sets = PyImport_ImportModule((char *)"sets");
    if (!sets) goto bad;
    Set = PyObject_GetAttrString(sets, (char *)"Set");
    if (!Set) goto bad;
    ImmutableSet = PyObject_GetAttrString(sets, (char *)"ImmutableSet");
    if (!ImmutableSet) goto bad;
    Py_DECREF(sets);

    __Pyx_PySet_Type       = (PyTypeObject*) Set;
    __Pyx_PyFrozenSet_Type = (PyTypeObject*) ImmutableSet;

    return 0;

 bad:
    Py_XDECREF(sets);
    Py_XDECREF(Set);
    Py_XDECREF(ImmutableSet);
    return -1;
}

#else
static int __Pyx_Py23SetsImport(void) { return 0; }
#endif /* !Py_SETOBJECT_H */
#endif /* < Py2.4  */
#endif /* < Py2.5  */
""",
init = put_py23_set_init_utility_code,
cleanup = """
#if PY_VERSION_HEX < 0x02040000
Py_XDECREF(__Pyx_PySet_Type); __Pyx_PySet_Type = NULL;
Py_XDECREF(__Pyx_PyFrozenSet_Type); __Pyx_PyFrozenSet_Type = NULL;
#endif /* < Py2.4  */
""")

builtin_utility_code = {
    'set'       : py23_set_utility_code,
    'frozenset' : py23_set_utility_code,
}


# mapping from builtins to their C-level equivalents

class _BuiltinOverride(object):
    def __init__(self, py_name, args, ret_type, cname, py_equiv = "*",
                 utility_code = None, sig = None, func_type = None):
        self.py_name, self.cname, self.py_equiv = py_name, cname, py_equiv
        self.args, self.ret_type = args, ret_type
        self.func_type, self.sig = func_type, sig
        self.utility_code = utility_code

class BuiltinAttribute(object):
    def __init__(self, py_name, cname=None, field_type=None, field_type_name=None):
        self.py_name = py_name
        self.cname = cname or py_name
        self.field_type_name = field_type_name # can't do the lookup before the type is declared!
        self.field_type = field_type

    def declare_in_type(self, self_type):
        if self.field_type_name is not None:
            # lazy type lookup
            field_type = builtin_scope.lookup(self.field_type_name).type
        else:
            field_type = self.field_type or PyrexTypes.py_object_type
        entry = self_type.scope.declare(self.py_name, self.cname, field_type, None, 'private')
        entry.is_variable = True

class BuiltinFunction(_BuiltinOverride):
    def declare_in_scope(self, scope):
        func_type, sig = self.func_type, self.sig
        if func_type is None:
            if sig is None:
                sig = Signature(self.args, self.ret_type)
            func_type = sig.function_type()
        scope.declare_builtin_cfunction(self.py_name, func_type, self.cname,
                                        self.py_equiv, self.utility_code)

class BuiltinMethod(_BuiltinOverride):
    def declare_in_type(self, self_type):
        method_type, sig = self.func_type, self.sig
        if method_type is None:
            if sig is None:
                sig = Signature(self.args, self.ret_type)
            # override 'self' type (first argument)
            self_arg = PyrexTypes.CFuncTypeArg("", self_type, None)
            self_arg.not_none = True
            method_type = sig.function_type(self_arg)
        self_type.scope.declare_builtin_cfunction(
            self.py_name, method_type, self.cname, utility_code = self.utility_code)


builtin_function_table = [
    # name,        args,   return,  C API func,           py equiv = "*"
    BuiltinFunction('abs',        "O",    "O",     "PyNumber_Absolute"),
    #('chr',       "",     "",      ""),
    #('cmp', "",   "",     "",      ""), # int PyObject_Cmp(PyObject *o1, PyObject *o2, int *result)
    #('compile',   "",     "",      ""), # PyObject* Py_CompileString(    char *str, char *filename, int start)
    BuiltinFunction('delattr',    "OO",   "r",     "PyObject_DelAttr"),
    BuiltinFunction('dir',        "O",    "O",     "PyObject_Dir"),
    BuiltinFunction('divmod',     "OO",   "O",     "PyNumber_Divmod"),
    BuiltinFunction('exec',       "OOO",  "O",     "__Pyx_PyRun",
                    utility_code = pyexec_utility_code),
    BuiltinFunction('exec',       "OO",   "O",     "__Pyx_PyRun2",
                    utility_code = pyexec_utility_code),
    #('eval',      "",     "",      ""),
    #('execfile',  "",     "",      ""),
    #('filter',    "",     "",      ""),
    BuiltinFunction('getattr',    "OO",   "O",     "PyObject_GetAttr"),
    BuiltinFunction('getattr',    "OOO",  "O",     "__Pyx_GetAttr3",
                    utility_code = getattr3_utility_code),
    BuiltinFunction('getattr3',   "OOO",  "O",     "__Pyx_GetAttr3",     "getattr",
                    utility_code = getattr3_utility_code), # Pyrex compatibility
    BuiltinFunction('hasattr',    "OO",   "b",     "PyObject_HasAttr"),
    BuiltinFunction('hash',       "O",    "l",     "PyObject_Hash"),
    #('hex',       "",     "",      ""),
    #('id',        "",     "",      ""),
    #('input',     "",     "",      ""),
    BuiltinFunction('intern',     "O",    "O",     "__Pyx_Intern",
                    utility_code = intern_utility_code),
    BuiltinFunction('isinstance', "OO",   "b",     "PyObject_IsInstance"),
    BuiltinFunction('issubclass', "OO",   "b",     "PyObject_IsSubclass"),
    BuiltinFunction('iter',       "OO",   "O",     "PyCallIter_New"),
    BuiltinFunction('iter',       "O",    "O",     "PyObject_GetIter"),
    BuiltinFunction('len',        "O",    "z",     "PyObject_Length"),
    BuiltinFunction('locals',     "",     "O",     "__pyx_locals"),
    #('map',       "",     "",      ""),
    #('max',       "",     "",      ""),
    #('min',       "",     "",      ""),
    BuiltinFunction('next',       "O",    "O",     "__Pyx_PyIter_Next",
                    utility_code = iter_next_utility_code),   # not available in Py2 => implemented here
    BuiltinFunction('next',      "OO",    "O",     "__Pyx_PyIter_Next2",
                    utility_code = iter_next_utility_code),  # not available in Py2 => implemented here
    #('oct',       "",     "",      ""),
    #('open',       "ss",   "O",     "PyFile_FromString"),   # not in Py3
    #('ord',       "",     "",      ""),
    BuiltinFunction('pow',        "OOO",  "O",     "PyNumber_Power"),
    BuiltinFunction('pow',        "OO",   "O",     "__Pyx_PyNumber_Power2",
                    utility_code = pow2_utility_code),
    #('range',     "",     "",      ""),
    #('raw_input', "",     "",      ""),
    #('reduce',    "",     "",      ""),
    BuiltinFunction('reload',     "O",    "O",     "PyImport_ReloadModule"),
    BuiltinFunction('repr',       "O",    "O",     "PyObject_Repr"),
    #('round',     "",     "",      ""),
    BuiltinFunction('setattr',    "OOO",  "r",     "PyObject_SetAttr"),
    #('sum',       "",     "",      ""),
    #('type',       "O",    "O",     "PyObject_Type"),
    #('unichr',    "",     "",      ""),
    #('unicode',   "",     "",      ""),
    #('vars',      "",     "",      ""),
    #('zip',       "",     "",      ""),
    #  Can't do these easily until we have builtin type entries.
    #('typecheck',  "OO",   "i",     "PyObject_TypeCheck", False),
    #('issubtype',  "OO",   "i",     "PyType_IsSubtype",   False),

    # Put in namespace append optimization.
    BuiltinFunction('__Pyx_PyObject_Append', "OO",  "O",     "__Pyx_PyObject_Append"),
]

# Builtin types
#  bool
#  buffer
#  classmethod
#  dict
#  enumerate
#  file
#  float
#  int
#  list
#  long
#  object
#  property
#  slice
#  staticmethod
#  super
#  str
#  tuple
#  type
#  xrange

builtin_types_table = [

    ("type",    "PyType_Type",     []),

# This conflicts with the C++ bool type, and unfortunately
# C++ is too liberal about PyObject* <-> bool conversions,
# resulting in unintuitive runtime behavior and segfaults.
#    ("bool",    "PyBool_Type",     []),

    ("int",     "PyInt_Type",      []),
    ("long",    "PyLong_Type",     []),
    ("float",   "PyFloat_Type",    []),

    ("complex", "PyComplex_Type",  [BuiltinAttribute('cval', field_type_name = 'Py_complex'),
                                    BuiltinAttribute('real', 'cval.real', field_type = PyrexTypes.c_double_type),
                                    BuiltinAttribute('imag', 'cval.imag', field_type = PyrexTypes.c_double_type),
                                    ]),

    ("bytes",   "PyBytes_Type",    []),
    ("str",     "PyString_Type",   []),
    ("unicode", "PyUnicode_Type",  [BuiltinMethod("join",  "TO",   "T", "PyUnicode_Join"),
                                    ]),

    ("tuple",   "PyTuple_Type",    []),

    ("list",    "PyList_Type",     [BuiltinMethod("insert",  "TzO",  "i", "PyList_Insert"),
                                    BuiltinMethod("reverse", "T",    "i", "PyList_Reverse"),
                                    BuiltinMethod("append",  "TO",   "i", "PyList_Append"),
                                    ]),

    ("dict",    "PyDict_Type",     [BuiltinMethod("items", "T",   "O", "PyDict_Items"),  # FIXME: Py3 mode?
                                    BuiltinMethod("keys",  "T",   "O", "PyDict_Keys"),   # FIXME: Py3 mode?
                                    BuiltinMethod("values","T",   "O", "PyDict_Values"), # FIXME: Py3 mode?
                                    BuiltinMethod("copy",  "T",   "T", "PyDict_Copy")]),

    ("slice",   "PySlice_Type",    [BuiltinAttribute('start'),
                                    BuiltinAttribute('stop'),
                                    BuiltinAttribute('step'),
                                    ]),
#    ("file",    "PyFile_Type",     []),  # not in Py3

    ("set",       "PySet_Type",    [BuiltinMethod("clear",   "T",  "i", "PySet_Clear"),
                                    BuiltinMethod("discard", "TO", "i", "PySet_Discard"),
                                    BuiltinMethod("add",     "TO", "i", "PySet_Add"),
                                    BuiltinMethod("pop",     "T",  "O", "PySet_Pop")]),
    ("frozenset", "PyFrozenSet_Type", []),
]

types_that_construct_their_instance = (
    # some builtin types do not always return an instance of
    # themselves - these do:
    'type', 'bool', 'long', 'float', 'bytes', 'unicode', 'tuple', 'list',
    'dict', 'set', 'frozenset'
    # 'str',             # only in Py3.x
    # 'file',            # only in Py2.x
    )


builtin_structs_table = [
    ('Py_buffer', 'Py_buffer',
     [("buf",        PyrexTypes.c_void_ptr_type),
      ("obj",        PyrexTypes.py_object_type),
      ("len",        PyrexTypes.c_py_ssize_t_type),
      ("itemsize",   PyrexTypes.c_py_ssize_t_type),
      ("readonly",   PyrexTypes.c_bint_type),
      ("ndim",       PyrexTypes.c_int_type),
      ("format",     PyrexTypes.c_char_ptr_type),
      ("shape",      PyrexTypes.c_py_ssize_t_ptr_type),
      ("strides",    PyrexTypes.c_py_ssize_t_ptr_type),
      ("suboffsets", PyrexTypes.c_py_ssize_t_ptr_type),
      ("internal",   PyrexTypes.c_void_ptr_type),
      ]),
    ('Py_complex', 'Py_complex',
     [('real', PyrexTypes.c_double_type),
      ('imag', PyrexTypes.c_double_type),
      ])
]

# set up builtin scope

builtin_scope = BuiltinScope()

def init_builtin_funcs():
    for bf in builtin_function_table:
        bf.declare_in_scope(builtin_scope)

builtin_types = {}

def init_builtin_types():
    global builtin_types
    for name, cname, methods in builtin_types_table:
        utility = builtin_utility_code.get(name)
        if name == 'frozenset':
            objstruct_cname = 'PySetObject'
        elif name == 'bool':
            objstruct_cname = None
        else:
            objstruct_cname = 'Py%sObject' % name.capitalize()
        the_type = builtin_scope.declare_builtin_type(name, cname, utility, objstruct_cname)
        builtin_types[name] = the_type
        for method in methods:
            method.declare_in_type(the_type)

def init_builtin_structs():
    for name, cname, attribute_types in builtin_structs_table:
        scope = StructOrUnionScope(name)
        for attribute_name, attribute_type in attribute_types:
            scope.declare_var(attribute_name, attribute_type, None,
                              attribute_name, allow_pyobject=True)
        builtin_scope.declare_struct_or_union(
            name, "struct", scope, 1, None, cname = cname)

def init_builtins():
    init_builtin_structs()
    init_builtin_funcs()
    init_builtin_types()
    global list_type, tuple_type, dict_type, set_type, frozenset_type
    global bytes_type, str_type, unicode_type
    global float_type, bool_type, type_type, complex_type
    type_type  = builtin_scope.lookup('type').type
    list_type  = builtin_scope.lookup('list').type
    tuple_type = builtin_scope.lookup('tuple').type
    dict_type  = builtin_scope.lookup('dict').type
    set_type   = builtin_scope.lookup('set').type
    frozenset_type = builtin_scope.lookup('frozenset').type
    bytes_type = builtin_scope.lookup('bytes').type
    str_type   = builtin_scope.lookup('str').type
    unicode_type = builtin_scope.lookup('unicode').type
    float_type = builtin_scope.lookup('float').type
    bool_type  = builtin_scope.lookup('bool').type
    complex_type  = builtin_scope.lookup('complex').type

init_builtins()
