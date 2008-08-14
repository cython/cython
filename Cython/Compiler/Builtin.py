#
#   Pyrex - Builtin Definitions
#

from Symtab import BuiltinScope, StructOrUnionScope
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
#    ("str",     "PyBytes_Type",   []),
    ("unicode", "PyUnicode_Type",  []),
    ("file",    "PyFile_Type",     []),
#    ("slice",   "PySlice_Type",    []),
#    ("set",     "PySet_Type",      []),
    ("frozenset", "PyFrozenSet_Type",   []),

    ("tuple",   "PyTuple_Type",    []),
    
    ("list",    "PyList_Type",     [("append", "OO",   "i", "PyList_Append"),
                                    ("insert", "OiO",  "i", "PyList_Insert"),
                                    ("sort",   "O",    "i", "PyList_Sort"),
                                    ("reverse","O",    "i", "PyList_Reverse")]),
                                    
    ("dict",    "PyDict_Type",     [("items", "O",   "O", "PyDict_Items"),
                                    ("keys",  "O",   "O", "PyDict_Keys"),
                                    ("values","O",   "O", "PyDict_Values")]),
]

builtin_structs_table = [
    ('Py_buffer', 'Py_buffer',
     [("buf",        PyrexTypes.c_void_ptr_type),
      ("len",        PyrexTypes.c_py_ssize_t_type),
      ("readonly",   PyrexTypes.c_bint_type),
      ("format",     PyrexTypes.c_char_ptr_type),
      ("ndim",       PyrexTypes.c_int_type),
      ("shape",      PyrexTypes.c_py_ssize_t_ptr_type),
      ("strides",    PyrexTypes.c_py_ssize_t_ptr_type),
      ("suboffsets", PyrexTypes.c_py_ssize_t_ptr_type),
      ("itemsize",   PyrexTypes.c_py_ssize_t_type),
      ("internal",   PyrexTypes.c_void_ptr_type),
      ])
]

getattr3_utility_code = ["""
static PyObject *__Pyx_GetAttr3(PyObject *, PyObject *, PyObject *); /*proto*/
""","""
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
"""]

intern_utility_code = ["""
#if PY_MAJOR_VERSION >= 3
#  define __Pyx_InternFromString(s) PyUnicode_InternFromString(s)
#else
#  define __Pyx_InternFromString(s) PyString_InternFromString(s)
#endif
""","""
"""]

builtin_utility_code = {
    'getattr3': getattr3_utility_code,
    'intern'  : intern_utility_code,
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
        the_type = builtin_scope.declare_builtin_type(name, cname)
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
    global list_type, tuple_type, dict_type, unicode_type
    list_type  = builtin_scope.lookup('list').type
    tuple_type = builtin_scope.lookup('tuple').type
    dict_type  = builtin_scope.lookup('dict').type
    unicode_type = builtin_scope.lookup('unicode').type

init_builtins()
