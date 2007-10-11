#
#   Pyrex - Builtin Definitions
#

from Symtab import BuiltinScope
from TypeSlots import Signature

builtin_function_table = [
    # name,        args,   return,  C API func,           has py equiv = True
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
    ('hasattr',    "OO",   "i",     "PyObject_HasAttr"),
    ('hash',       "O",    "i",     "PyObject_Hash"),
    #('hex',       "",     "",      ""),
    #('id',        "",     "",      ""),
    #('input',     "",     "",      ""),
    ('intern',     "s",    "O",     "PyString_InternFromString"),
    ('isinstance', "OO",   "i",     "PyObject_IsInstance"),
    ('issubclass', "OO",   "i",     "PyObject_IsSubclass"),
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

builtin_scope = BuiltinScope()

def declare_builtin_func(name, args, ret, cname, py_equiv = 1):
    sig = Signature(args, ret)
    type = sig.function_type()
    builtin_scope.declare_builtin_cfunction(name, type, cname, py_equiv)

def init_builtin_funcs():
    for desc in builtin_function_table:
        declare_builtin_func(*desc)

def init_builtins():
    init_builtin_funcs()

init_builtins()
