#
#   Pyrex - Builtin Definitions
#

from Symtab import BuiltinScope, StructOrUnionScope
from Code import UtilityCode
from TypeSlots import Signature
import PyrexTypes
import Naming

builtin_function_table = [
    # name,        args,   return,  C API func,           py equiv = "*"
    ('abs',        "O",    "O",     "PyNumber_Absolute"),
    #('chr',       "",     "",      ""),
    #('cmp', "",   "",     "",      ""), # int PyObject_Cmp(PyObject *o1, PyObject *o2, int *result)
    #('compile',   "",     "",      ""), # PyObject* Py_CompileString(    char *str, char *filename, int start)
    ('delattr',    "OO",   "r",     "PyObject_DelAttr"),
    ('dir',        "O",    "O",     "PyObject_Dir"),
    ('divmod',     "OO",   "O",     "PyNumber_Divmod"),
    ('exec',       "OOO",  "O",     "__Pyx_PyRun"),
    #('eval',      "",     "",      ""),
    #('execfile',  "",     "",      ""),
    #('filter',    "",     "",      ""),
    #('getattr',    "OO",   "O",     "PyObject_GetAttr"),   # optimised later on
    ('getattr3',   "OOO",  "O",     "__Pyx_GetAttr3",       "getattr"),
    ('hasattr',    "OO",   "b",     "PyObject_HasAttr"),
    ('hash',       "O",    "l",     "PyObject_Hash"),
    #('hex',       "",     "",      ""),
    #('id',        "",     "",      ""),
    #('input',     "",     "",      ""),
    ('intern',     "O",    "O",     "__Pyx_Intern"),
    ('isinstance', "OO",   "b",     "PyObject_IsInstance"),
    ('issubclass', "OO",   "b",     "PyObject_IsSubclass"),
    ('iter',       "O",    "O",     "PyObject_GetIter"),
    ('len',        "O",    "Z",     "PyObject_Length"),
    ('locals',     "",     "O",     "__pyx_locals"),
    #('map',       "",     "",      ""),
    #('max',       "",     "",      ""),
    #('min',       "",     "",      ""),
    #('oct',       "",     "",      ""),
    # Not worth doing open, when second argument would become mandatory
    #('open',       "ss",   "O",     "PyFile_FromString"),
    #('ord',       "",     "",      ""),
    ('pow',        "OOO",  "O",     "PyNumber_Power"),
    #('range',     "",     "",      ""),
    #('raw_input', "",     "",      ""),
    #('reduce',    "",     "",      ""),
    ('reload',     "O",    "O",     "PyImport_ReloadModule"),
    ('repr',       "O",    "O",     "PyObject_Repr"),
    #('round',     "",     "",      ""),
    ('setattr',    "OOO",  "r",     "PyObject_SetAttr"),
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
    ('__Pyx_PyObject_Append', "OO",  "O",     "__Pyx_PyObject_Append"),
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

    ("bool",    "PyBool_Type",     []),
    ("int",     "PyInt_Type",      []),
    ("long",    "PyLong_Type",     []),
    ("float",   "PyFloat_Type",    []),
    
# Until we have a way to access attributes of a type, 
# we don't want to make this one builtin.    
#    ("complex", "PyComplex_Type",  []),

    ("bytes",   "PyBytes_Type",    []),
    ("str",     "PyString_Type",   []),
    ("unicode", "PyUnicode_Type",  []),

    ("tuple",   "PyTuple_Type",    []),

    ("list",    "PyList_Type",     [("insert", "OZO",  "i", "PyList_Insert")]),

    ("dict",    "PyDict_Type",     [("items", "O",   "O", "PyDict_Items"),
                                    ("keys",  "O",   "O", "PyDict_Keys"),
                                    ("values","O",   "O", "PyDict_Values"),
                                    ("copy",  "O",   "O", "PyDict_Copy")]),

    ("slice",   "PySlice_Type",    []),
    ("file",    "PyFile_Type",     []),

    ("set",       "PySet_Type",    [("clear",   "O",  "i", "PySet_Clear"), 
                                    ("discard", "OO", "i", "PySet_Discard"),
                                    ("add",     "OO", "i", "PySet_Add"),
                                    ("pop",     "O",  "O", "PySet_Pop")]),
    ("frozenset", "PyFrozenSet_Type", []),
]

types_that_construct_their_instance = (
    # some builtin types do not always return an instance of
    # themselves - these do:
    'type', 'bool', 'long', 'float', 'bytes', 'unicode', 'tuple', 'list',
    'dict', 'file', 'set', 'frozenset'
    # 'str',             # only in Py3.x
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
      ])
]

getattr3_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_GetAttr3(PyObject *, PyObject *, PyObject *); /*proto*/
""",
impl = """
static PyObject *__Pyx_GetAttr3(PyObject *o, PyObject *n, PyObject *d) {
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
    return 0;
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
""",
impl = """
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
	result = PyEval_EvalCode((PyCodeObject *)o, globals, locals);
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
    'exec'      : pyexec_utility_code,
    'getattr3'  : getattr3_utility_code,
    'intern'    : intern_utility_code,
    'set'       : py23_set_utility_code,
    'frozenset' : py23_set_utility_code,
}

builtin_scope = BuiltinScope()

def declare_builtin_func(name, args, ret, cname, py_equiv = "*"):
    sig = Signature(args, ret)
    type = sig.function_type()
    utility = builtin_utility_code.get(name)
    builtin_scope.declare_builtin_cfunction(name, type, cname, py_equiv, utility)

def init_builtin_funcs():
    for desc in builtin_function_table:
        declare_builtin_func(*desc)

builtin_types = {}

def init_builtin_types():
    global builtin_types
    for name, cname, funcs in builtin_types_table:
        utility = builtin_utility_code.get(name)
        the_type = builtin_scope.declare_builtin_type(name, cname, utility)
        builtin_types[name] = the_type
        for name, args, ret, cname in funcs:
            sig = Signature(args, ret)
            the_type.scope.declare_cfunction(name, sig.function_type(), None, cname)

def init_builtin_structs():
    for name, cname, attribute_types in builtin_structs_table:
        scope = StructOrUnionScope(name)
        for attribute_name, attribute_type in attribute_types:
            scope.declare_var(
                attribute_name, attribute_type, None, attribute_name)
        builtin_scope.declare_struct_or_union(
            name, "struct", scope, 1, None, cname = cname)

def init_builtins():
    init_builtin_funcs()
    init_builtin_types()
    init_builtin_structs()
    global list_type, tuple_type, dict_type, set_type, type_type
    global bytes_type, str_type, unicode_type, float_type
    type_type  = builtin_scope.lookup('type').type
    list_type  = builtin_scope.lookup('list').type
    tuple_type = builtin_scope.lookup('tuple').type
    dict_type  = builtin_scope.lookup('dict').type
    set_type   = builtin_scope.lookup('set').type
    bytes_type = builtin_scope.lookup('bytes').type
    str_type   = builtin_scope.lookup('str').type
    unicode_type = builtin_scope.lookup('unicode').type
    float_type = builtin_scope.lookup('float').type

init_builtins()
