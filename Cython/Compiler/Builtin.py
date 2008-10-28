#
#   Pyrex - Builtin Definitions
#

from Symtab import BuiltinScope, StructOrUnionScope
from Cython.Utils import UtilityCode
from TypeSlots import Signature
import PyrexTypes

builtin_function_table = [
    # name,        args,   return,  C API func,           py equiv = "*"
    ('abs',        "O",    "O",     "PyNumber_Absolute"),
    #('chr',       "",     "",      ""),
    #('cmp', "",   "",     "",      ""), # int PyObject_Cmp(PyObject *o1, PyObject *o2, int *result)
    #('compile',   "",     "",      ""), # PyObject* Py_CompileString(	char *str, char *filename, int start)
    ('delattr',    "OO",   "r",     "PyObject_DelAttr"),
    ('dir',        "O",    "O",     "PyObject_Dir"),
    ('divmod',     "OO",   "O",     "PyNumber_Divmod"),
    #('eval',      "",     "",      ""),
    #('execfile',  "",     "",      ""),
    #('filter',    "",     "",      ""),
    ('getattr',    "OO",   "O",     "PyObject_GetAttr"),
    ('getattr3',   "OOO",  "O",     "__Pyx_GetAttr3",       "getattr"),
    ('hasattr',    "OO",   "b",     "PyObject_HasAttr"),
    ('hash',       "O",    "l",     "PyObject_Hash"),
    #('hex',       "",     "",      ""),
    #('id',        "",     "",      ""),
    #('input',     "",     "",      ""),
    ('intern',     "s",    "O",     "__Pyx_InternFromString"),
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
    ("complex", "PyComplex_Type",  []),

    ("bytes",   "PyBytes_Type",    []),
    ("str",     "PyString_Type",   []),
    ("unicode", "PyUnicode_Type",  []),

    ("tuple",   "PyTuple_Type",    []),

    ("list",    "PyList_Type",     [("append", "OO",   "i", "PyList_Append"),
                                    ("insert", "OiO",  "i", "PyList_Insert"),
                                    ("sort",   "O",    "i", "PyList_Sort"),
                                    ("reverse","O",    "i", "PyList_Reverse")]),

    ("dict",    "PyDict_Type",     [("items", "O",   "O", "PyDict_Items"),
                                    ("keys",  "O",   "O", "PyDict_Keys"),
                                    ("values","O",   "O", "PyDict_Values")]),

    ("slice",   "PySlice_Type",    []),
    ("file",    "PyFile_Type",     []),

    ("set",       "PySet_Type",    [("clear",   "O",  "i", "PySet_Clear"), 
                                    ("discard", "OO", "i", "PySet_Discard"),
                                    ("add",     "OO", "i", "PySet_Add"),
                                    ("pop",     "O",  "O", "PySet_Pop")]),
    ("frozenset", "PyFrozenSet_Type", []),
]


        
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

intern_utility_code = UtilityCode(
proto = """
#if PY_MAJOR_VERSION >= 3
#  define __Pyx_InternFromString(s) PyUnicode_InternFromString(s)
#else
#  define __Pyx_InternFromString(s) PyString_InternFromString(s)
#endif
""")

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
    PyObject_CallMethod(set, "pop", NULL)

static INLINE int PySet_Clear(PyObject *set) {
    PyObject *ret = PyObject_CallMethod(set, "clear", NULL);
    if (!ret) return -1;
    Py_DECREF(ret); return 0;
}

static INLINE int PySet_Discard(PyObject *set, PyObject *key) {
    PyObject *ret = PyObject_CallMethod(set, "discard", "O", key);
    if (!ret) return -1;
    Py_DECREF(ret); return 0;
}

static INLINE int PySet_Add(PyObject *set, PyObject *key) {
    PyObject *ret = PyObject_CallMethod(set, "add", "O", key);
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

    sets = PyImport_ImportModule("sets");
    if (!sets) goto bad;
    Set = PyObject_GetAttrString(sets, "Set");
    if (!Set) goto bad;
    ImmutableSet = PyObject_GetAttrString(sets, "ImmutableSet");
    if (!ImmutableSet) goto bad;
    Py_DECREF(sets);
  
    __Pyx_PySet_Type       = (PyTypeObject*) Set;
    __Pyx_PyFrozenSet_Type = (PyTypeObject*) ImmutableSet;

    /* FIXME: this should be done in dedicated module cleanup code */
    /*
    Py_DECREF(Set);
    Py_DECREF(ImmutableSet);
    */

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

def init_builtin_types():
    for name, cname, funcs in builtin_types_table:
        utility = builtin_utility_code.get(name)
        the_type = builtin_scope.declare_builtin_type(name, cname, utility)
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
    global list_type, tuple_type, dict_type, unicode_type, type_type
    type_type  = builtin_scope.lookup('type').type
    list_type  = builtin_scope.lookup('list').type
    tuple_type = builtin_scope.lookup('tuple').type
    dict_type  = builtin_scope.lookup('dict').type
    unicode_type = builtin_scope.lookup('unicode').type

init_builtins()
