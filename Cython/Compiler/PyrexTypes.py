#
#   Pyrex - Types
#

from Cython.Utils import UtilityCode
import StringEncoding
import Naming
import copy

class BaseType(object):
    #
    #  Base class for all Pyrex types including pseudo-types.

    def cast_code(self, expr_code):
        return "((%s)%s)" % (self.declaration_code(""), expr_code)
    
    def specalization_name(self):
        return self.declaration_code("").replace(" ", "__")
    
    def base_declaration_code(self, base_code, entity_code):
        if entity_code:
            return "%s %s" % (base_code, entity_code)
        else:
            return base_code

class PyrexType(BaseType):
    #
    #  Base class for all Pyrex types.
    #
    #  is_pyobject           boolean     Is a Python object type
    #  is_extension_type     boolean     Is a Python extension type
    #  is_numeric            boolean     Is a C numeric type
    #  is_int                boolean     Is a C integer type
    #  is_longlong           boolean     Is a long long or unsigned long long.
    #  is_float              boolean     Is a C floating point type
    #  is_complex            boolean     Is a C complex type
    #  is_void               boolean     Is the C void type
    #  is_array              boolean     Is a C array type
    #  is_ptr                boolean     Is a C pointer type
    #  is_null_ptr           boolean     Is the type of NULL
    #  is_cfunction          boolean     Is a C function type
    #  is_struct_or_union    boolean     Is a C struct or union type
    #  is_struct             boolean     Is a C struct type
    #  is_enum               boolean     Is a C enum type
    #  is_typedef            boolean     Is a typedef type
    #  is_string             boolean     Is a C char * type
    #  is_unicode            boolean     Is a UTF-8 encoded C char * type
    #  is_returncode         boolean     Is used only to signal exceptions
    #  is_error              boolean     Is the dummy error type
    #  is_buffer             boolean     Is buffer access type
    #  has_attributes        boolean     Has C dot-selectable attributes
    #  default_value         string      Initial value
    #  pymemberdef_typecode  string      Type code for PyMemberDef struct
    #
    #  declaration_code(entity_code, 
    #      for_display = 0, dll_linkage = None, pyrex = 0)
    #    Returns a code fragment for the declaration of an entity
    #    of this type, given a code fragment for the entity.
    #    * If for_display, this is for reading by a human in an error
    #      message; otherwise it must be valid C code.
    #    * If dll_linkage is not None, it must be 'DL_EXPORT' or
    #      'DL_IMPORT', and will be added to the base type part of
    #      the declaration.
    #    * If pyrex = 1, this is for use in a 'cdef extern'
    #      statement of a Pyrex include file.
    #
    #  assignable_from(src_type)
    #    Tests whether a variable of this type can be
    #    assigned a value of type src_type.
    #
    #  same_as(other_type)
    #    Tests whether this type represents the same type
    #    as other_type.
    #
    #  as_argument_type():
    #    Coerces array type into pointer type for use as
    #    a formal argument type.
    #
        
    is_pyobject = 0
    is_extension_type = 0
    is_builtin_type = 0
    is_numeric = 0
    is_int = 0
    is_longlong = 0
    is_float = 0
    is_complex = 0
    is_void = 0
    is_array = 0
    is_ptr = 0
    is_null_ptr = 0
    is_cfunction = 0
    is_struct_or_union = 0
    is_cpp_class = 0
    is_struct = 0
    is_enum = 0
    is_typedef = 0
    is_string = 0
    is_unicode = 0
    is_returncode = 0
    is_error = 0
    is_buffer = 0
    has_attributes = 0
    default_value = ""
    pymemberdef_typecode = None
    
    def resolve(self):
        # If a typedef, returns the base type.
        return self
    
    def specialize(self, values):
        # TODO(danilo): Override wherever it makes sense.
        return self
    
    def literal_code(self, value):
        # Returns a C code fragment representing a literal
        # value of this type.
        return str(value)
    
    def __str__(self):
        return self.declaration_code("", for_display = 1).strip()
    
    def same_as(self, other_type, **kwds):
        return self.same_as_resolved_type(other_type.resolve(), **kwds)
    
    def same_as_resolved_type(self, other_type):
        return self == other_type or other_type is error_type
    
    def subtype_of(self, other_type):
        return self.subtype_of_resolved_type(other_type.resolve())
    
    def subtype_of_resolved_type(self, other_type):
        return self.same_as(other_type)
    
    def assignable_from(self, src_type):
        return self.assignable_from_resolved_type(src_type.resolve())
    
    def assignable_from_resolved_type(self, src_type):
        return self.same_as(src_type)
    
    def as_argument_type(self):
        return self
    
    def is_complete(self):
        # A type is incomplete if it is an unsized array,
        # a struct whose attributes are not defined, etc.
        return 1

    def is_simple_buffer_dtype(self):
        return (self.is_int or self.is_float or self.is_complex or self.is_pyobject or
                self.is_extension_type or self.is_ptr)

    def struct_nesting_depth(self):
        # Returns the number levels of nested structs. This is
        # used for constructing a stack for walking the run-time
        # type information of the struct.
        return 1

class CTypedefType(BaseType):
    #
    #  Pseudo-type defined with a ctypedef statement in a
    #  'cdef extern from' block. Delegates most attribute
    #  lookups to the base type. ANYTHING NOT DEFINED
    #  HERE IS DELEGATED!
    #
    #  qualified_name      string
    #  typedef_cname       string
    #  typedef_base_type   PyrexType
    #  typedef_is_external bool
    
    is_typedef = 1
    typedef_is_external = 0
    
    def __init__(self, cname, base_type, is_external=0):
        self.typedef_cname = cname
        self.typedef_base_type = base_type
        self.typedef_is_external = is_external

        # Make typecodes in external typedefs use typesize-neutral macros
        if is_external:
            typecode = None
            if base_type.is_int:
                if base_type.signed == 0:
                    typecode = "__Pyx_T_UNSIGNED_INT"
                else:
                    typecode = "__Pyx_T_SIGNED_INT"
            elif base_type.is_float and not rank_to_type_name[base_type.rank] == "long double":
                typecode = "__Pyx_T_FLOATING"
            if typecode:
                self.pymemberdef_typecode = "%s(%s)" % (typecode, cname)
    
    def resolve(self):
        return self.typedef_base_type.resolve()
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        name = self.declaration_name(for_display, pyrex)
        return self.base_declaration_code(name, entity_code)
    
    def declaration_name(self, for_display = 0, pyrex = 0):
        if pyrex or for_display:
            return self.qualified_name
        else:
            return self.typedef_cname
    
    def as_argument_type(self):
        return self

    def cast_code(self, expr_code):
        # If self is really an array (rather than pointer), we can't cast.
        # For example, the gmp mpz_t. 
        if self.typedef_base_type.is_ptr:
            return self.typedef_base_type.cast_code(expr_code)
        else:
            return BaseType.cast_code(self, expr_code)
    
    def __repr__(self):
        return "<CTypedefType %s>" % self.typedef_cname
    
    def __str__(self):
        return self.declaration_name(for_display = 1)
    
    def __getattr__(self, name):
        return getattr(self.typedef_base_type, name)

class BufferType(BaseType):
    #
    #  Delegates most attribute
    #  lookups to the base type. ANYTHING NOT DEFINED
    #  HERE IS DELEGATED!
    
    # dtype            PyrexType
    # ndim             int
    # mode             str
    # negative_indices bool
    # cast             bool
    # is_buffer        bool
    # writable         bool

    is_buffer = 1
    writable = True
    def __init__(self, base, dtype, ndim, mode, negative_indices, cast):
        self.base = base
        self.dtype = dtype
        self.ndim = ndim
        self.buffer_ptr_type = CPtrType(dtype)
        self.mode = mode
        self.negative_indices = negative_indices
        self.cast = cast
    
    def as_argument_type(self):
        return self

    def __getattr__(self, name):
        return getattr(self.base, name)

    def __repr__(self):
        return "<BufferType %r>" % self.base

def public_decl(base, dll_linkage):
    if dll_linkage:
        return "%s(%s)" % (dll_linkage, base)
    else:
        return base
    
class PyObjectType(PyrexType):
    #
    #  Base class for all Python object types (reference-counted).
    #
    #  buffer_defaults  dict or None     Default options for bu
    
    is_pyobject = 1
    default_value = "0"
    pymemberdef_typecode = "T_OBJECT"
    buffer_defaults = None
    
    def __str__(self):
        return "Python object"
    
    def __repr__(self):
        return "<PyObjectType>"
    
    def assignable_from(self, src_type):
        return 1 # Conversion will be attempted
        
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            return self.base_declaration_code("object", entity_code)
        else:
            return "%s *%s" % (public_decl("PyObject", dll_linkage), entity_code)

    def as_pyobject(self, cname):
        if (not self.is_complete()) or self.is_extension_type:
            return "(PyObject *)" + cname
        else:
            return cname

class BuiltinObjectType(PyObjectType):

    is_builtin_type = 1
    has_attributes = 1
    base_type = None
    module_name = '__builtin__'

    alternative_name = None # used for str/bytes duality

    def __init__(self, name, cname):
        self.name = name
        if name == 'str':
            self.alternative_name = 'bytes'
        elif name == 'bytes':
            self.alternative_name = 'str'
        self.cname = cname
        self.typeptr_cname = "&" + cname
                                 
    def set_scope(self, scope):
        self.scope = scope
        if scope:
            scope.parent_type = self
        
    def __str__(self):
        return "%s object" % self.name
    
    def __repr__(self):
        return "<%s>"% self.cname
        
    def assignable_from(self, src_type):
        if isinstance(src_type, BuiltinObjectType):
            return src_type.name == self.name or (
                src_type.name == self.alternative_name and
                src_type.name is not None)
        else:
            return not src_type.is_extension_type
            
    def typeobj_is_available(self):
        return True
        
    def attributes_known(self):
        return True
        
    def subtype_of(self, type):
        return type.is_pyobject and self.assignable_from(type)
        
    def type_test_code(self, arg):
        type_name = self.name
        if type_name == 'str':
            check = 'PyString_CheckExact'
        elif type_name == 'set':
            check = 'PyAnySet_CheckExact'
        elif type_name == 'frozenset':
            check = 'PyFrozenSet_CheckExact'
        elif type_name == 'bool':
            check = 'PyBool_Check'
        else:
            check = 'Py%s_CheckExact' % type_name.capitalize()
        return 'likely(%s(%s)) || (%s) == Py_None || (PyErr_Format(PyExc_TypeError, "Expected %s, got %%s", Py_TYPE(%s)->tp_name), 0)' % (check, arg, arg, self.name, arg)

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            return self.base_declaration_code(self.name, entity_code)
        else:
            return "%s *%s" % (public_decl("PyObject", dll_linkage), entity_code)


class PyExtensionType(PyObjectType):
    #
    #  A Python extension type.
    #
    #  name             string
    #  scope            CClassScope      Attribute namespace
    #  visibility       string
    #  typedef_flag     boolean
    #  base_type        PyExtensionType or None
    #  module_name      string or None   Qualified name of defining module
    #  objstruct_cname  string           Name of PyObject struct
    #  typeobj_cname    string or None   C code fragment referring to type object
    #  typeptr_cname    string or None   Name of pointer to external type object
    #  vtabslot_cname   string           Name of C method table member
    #  vtabstruct_cname string           Name of C method table struct
    #  vtabptr_cname    string           Name of pointer to C method table
    #  vtable_cname     string           Name of C method table definition
    
    is_extension_type = 1
    has_attributes = 1
    
    def __init__(self, name, typedef_flag, base_type):
        self.name = name
        self.scope = None
        self.typedef_flag = typedef_flag
        self.base_type = base_type
        self.module_name = None
        self.objstruct_cname = None
        self.typeobj_cname = None
        self.typeptr_cname = None
        self.vtabslot_cname = None
        self.vtabstruct_cname = None
        self.vtabptr_cname = None
        self.vtable_cname = None
    
    def set_scope(self, scope):
        self.scope = scope
        if scope:
            scope.parent_type = self
    
    def subtype_of_resolved_type(self, other_type):
        if other_type.is_extension_type:
            return self is other_type or (
                self.base_type and self.base_type.subtype_of(other_type))
        else:
            return other_type is py_object_type
    
    def typeobj_is_available(self):
        # Do we have a pointer to the type object?
        return self.typeptr_cname
    
    def typeobj_is_imported(self):
        # If we don't know the C name of the type object but we do
        # know which module it's defined in, it will be imported.
        return self.typeobj_cname is None and self.module_name is not None
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0, deref = 0):
        if pyrex or for_display:
            return self.base_declaration_code(self.name, entity_code)
        else:
            if self.typedef_flag:
                base_format = "%s"
            else:
                base_format = "struct %s"
            base = public_decl(base_format % self.objstruct_cname, dll_linkage)
            if deref:
                return "%s %s" % (base,  entity_code)
            else:
                return "%s *%s" % (base,  entity_code)

    def type_test_code(self, py_arg):
        return "__Pyx_TypeTest(%s, %s)" % (py_arg, self.typeptr_cname)
    
    def attributes_known(self):
        return self.scope is not None
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "<PyExtensionType %s%s>" % (self.scope.class_name,
            ("", " typedef")[self.typedef_flag])
    

class CType(PyrexType):
    #
    #  Base class for all C types (non-reference-counted).
    #
    #  to_py_function     string     C function for converting to Python object
    #  from_py_function   string     C function for constructing from Python object
    #
    
    to_py_function = None
    from_py_function = None
    exception_value = None
    exception_check = 1

    def create_to_py_utility_code(self, env):
        return self.to_py_function is not None
        
    def create_from_py_utility_code(self, env):
        return self.from_py_function is not None
        
    def error_condition(self, result_code):
        conds = []
        if self.is_string:
            conds.append("(!%s)" % result_code)
        elif self.exception_value is not None:
            conds.append("(%s == (%s)%s)" % (result_code, self.sign_and_name(), self.exception_value))
        if self.exception_check:
            conds.append("PyErr_Occurred()")
        if len(conds) > 0:
            return " && ".join(conds)
        else:
            return 0


class CVoidType(CType):
    is_void = 1
    
    def __repr__(self):
        return "<CVoidType>"
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        base = public_decl("void", dll_linkage)
        return self.base_declaration_code(base, entity_code)
    
    def is_complete(self):
        return 0


class CNumericType(CType):
    #
    #   Base class for all C numeric types.
    #
    #   rank      integer     Relative size
    #   signed    integer     0 = unsigned, 1 = unspecified, 2 = explicitly signed
    #
    
    is_numeric = 1
    default_value = "0"
    
    sign_words = ("unsigned ", "", "signed ")
    
    def __init__(self, rank, signed = 1, pymemberdef_typecode = None):
        self.rank = rank
        self.signed = signed
        self.pymemberdef_typecode = pymemberdef_typecode
    
    def sign_and_name(self):
        s = self.sign_words[self.signed]
        n = rank_to_type_name[self.rank]
        return s + n
    
    def __repr__(self):
        return "<CNumericType %s>" % self.sign_and_name()
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        base = public_decl(self.sign_and_name(), dll_linkage)
        if for_display and self.is_longlong:
            base = base.replace('PY_LONG_LONG', 'long long')
        return self.base_declaration_code(base,  entity_code)


type_conversion_predeclarations = ""
type_conversion_functions = ""

c_int_from_py_function = UtilityCode(
proto="""
static INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject *);
""",
impl="""
static INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject* x) {
    if (sizeof(%(type)s) < sizeof(long)) {
        long val = __Pyx_PyInt_AsLong(x);
        if (unlikely(val != (long)(%(type)s)val)) {
            if (unlikely(val == -1 && PyErr_Occurred()))
                return (%(type)s)-1;""" + \
           "%(IntValSignTest)s" + \
"""
            PyErr_SetString(PyExc_OverflowError,
                           "value too large to convert to %(type)s");
            return (%(type)s)-1;
        }
        return (%(type)s)val;
    }
    return (%(type)s)__Pyx_PyInt_As%(SignWord)sLong(x);
}
""")
intval_signtest = """
            if (unlikely(%(var)s < 0)) {
                PyErr_SetString(PyExc_OverflowError,
                                "can't convert negative value to %(type)s");
                return (%(type)s)-1;
            }"""

c_long_from_py_function = UtilityCode(
proto="""
static INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject *);
""",
impl="""
static INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject* x) {
#if PY_VERSION_HEX < 0x03000000
    if (likely(PyInt_CheckExact(x) || PyInt_Check(x))) {
        long val = PyInt_AS_LONG(x);""" + \
       "%(IntValSignTest)s" + \
"""
        return (%(type)s)val;
    } else
#endif
    if (likely(PyLong_CheckExact(x) || PyLong_Check(x))) {""" +\
       "%(PyLongSignTest)s" + \
"""
        return %(PyLongConvert)s(x);
    } else {
        %(type)s val;
        PyObject *tmp = __Pyx_PyNumber_Int(x);
        if (!tmp) return (%(type)s)-1;
        val = __Pyx_PyInt_As%(SignWord)s%(TypeName)s(tmp);
        Py_DECREF(tmp);
        return val;
    }
}
""")
pylong_signtest = """
        if (unlikely(Py_SIZE(%(var)s) < 0)) {
            PyErr_SetString(PyExc_OverflowError,
                            "can't convert negative value to %(type)s");
            return (%(type)s)-1;
        }"""



class CIntType(CNumericType):

    is_int = 1
    typedef_flag = 0
    to_py_function = "PyInt_FromLong"
    from_py_function = "__Pyx_PyInt_AsInt"
    exception_value = -1

    def __init__(self, rank, signed, pymemberdef_typecode = None, is_returncode = 0):
        CNumericType.__init__(self, rank, signed, pymemberdef_typecode)
        self.is_returncode = is_returncode
        if self.from_py_function == "__Pyx_PyInt_AsInt":
            self.from_py_function = self.get_type_conversion()

    def get_type_conversion(self):
        ctype = self.declaration_code('')
        bits = ctype.split(" ", 1)
        if len(bits) == 1:
            sign_word, type_name = "", bits[0]
        else:
            sign_word, type_name = bits
        type_name = type_name.replace("PY_LONG_LONG","long long")
        SignWord  = sign_word.title()
        TypeName  = type_name.title().replace(" ", "")
        data = {'IntValSignTest' : "",
                'PyLongSignTest' : "",
                'PyLongConvert'  : "",
                }
        if not self.signed:
            data['IntValSignTest'] = intval_signtest % {'var':"val", 'type':ctype}
            data['PyLongSignTest'] = pylong_signtest % {'var':"x",   'type':ctype}
        if "Long" in TypeName:
            data['PyLongConvert'] = \
                "PyLong_As" + SignWord.replace("Signed", "") + TypeName
            # the replaces below are just for generating well indented C code
            data['IntValSignTest'] = "\n".join(
                [ln.replace(" "*4, "", 1) for ln in data['IntValSignTest'].split('\n')]
                )
            utility_code = c_long_from_py_function
        else:
            utility_code = c_int_from_py_function
        utility_code.specialize(self,
                                SignWord=SignWord,
                                TypeName=TypeName,
                                **data)
        func_name = "__Pyx_PyInt_As%s%s" % (SignWord, TypeName)
        return func_name

    def assignable_from_resolved_type(self, src_type):
        return src_type.is_int or src_type.is_enum or src_type is error_type


class CBIntType(CIntType):

    to_py_function = "__Pyx_PyBool_FromLong"
    from_py_function = "__Pyx_PyObject_IsTrue"
    exception_check = 0


class CAnonEnumType(CIntType):

    is_enum = 1

    def sign_and_name(self):
        return 'int'


class CUIntType(CIntType):

    to_py_function = "PyLong_FromUnsignedLong"
    exception_value = -1


class CLongType(CIntType):

    to_py_function = "PyInt_FromLong"


class CULongType(CUIntType):

    to_py_function = "PyLong_FromUnsignedLong"


class CLongLongType(CIntType):

    is_longlong = 1
    to_py_function = "PyLong_FromLongLong"


class CULongLongType(CUIntType):

    is_longlong = 1
    to_py_function = "PyLong_FromUnsignedLongLong"


class CPySSizeTType(CIntType):

    to_py_function = "PyInt_FromSsize_t"
    from_py_function = "__Pyx_PyIndex_AsSsize_t"

    def sign_and_name(self):
        return rank_to_type_name[self.rank]


class CSizeTType(CUIntType):

    to_py_function = "__Pyx_PyInt_FromSize_t"
    from_py_function = "__Pyx_PyInt_AsSize_t"

    def sign_and_name(self):
        return rank_to_type_name[self.rank]


class CFloatType(CNumericType):

    is_float = 1
    to_py_function = "PyFloat_FromDouble"
    from_py_function = "__pyx_PyFloat_AsDouble"
    
    def __init__(self, rank, pymemberdef_typecode = None, math_h_modifier = ''):
        CNumericType.__init__(self, rank, 1, pymemberdef_typecode)
        self.math_h_modifier = math_h_modifier
    
    def assignable_from_resolved_type(self, src_type):
        return (src_type.is_numeric and not src_type.is_complex) or src_type is error_type


class CComplexType(CNumericType):
    
    is_complex = 1
    to_py_function = "__pyx_PyObject_from_complex"
    has_attributes = 1
    scope = None
    
    def __init__(self, real_type):
        self.real_type = real_type
        CNumericType.__init__(self, real_type.rank + 0.5, real_type.signed)
        self.binops = {}
        self.from_parts = "%s_from_parts" % self.specalization_name()
    
    def __cmp__(self, other):
        if isinstance(self, CComplexType) and isinstance(other, CComplexType):
            return cmp(self.real_type, other.real_type)
        else:
            return 1
    
    def __hash__(self):
        return ~hash(self.real_type)
    
    def sign_and_name(self):
        return Naming.type_prefix + self.real_type.specalization_name() + "_complex"

    def assignable_from_resolved_type(self, src_type):
        return (src_type.is_complex and self.real_type.assignable_from_resolved_type(src_type.real_type)
                    or src_type.is_numeric and self.real_type.assignable_from_resolved_type(src_type) 
                    or src_type is error_type)
                    
    def attributes_known(self):
        if self.scope is None:
            import Symtab
            self.scope = Symtab.StructOrUnionScope(self.specalization_name())
            self.scope.declare_var("real", self.real_type, None, "real")
            self.scope.declare_var("imag", self.real_type, None, "imag")
        return True

    def create_declaration_utility_code(self, env):
        # This must always be run, because a single CComplexType instance can be shared
        # across multiple compilations (the one created in the module scope)
        env.use_utility_code(complex_generic_utility_code)
        env.use_utility_code(
            complex_arithmatic_utility_code.specialize(self, 
                math_h_modifier = self.real_type.math_h_modifier,
                real_type = self.real_type.declaration_code('')))
        return True

    def create_from_py_utility_code(self, env):
        self.real_type.create_from_py_utility_code(env)
        env.use_utility_code(
            complex_conversion_utility_code.specialize(self, 
                        math_h_modifier = self.real_type.math_h_modifier,
                        real_type = self.real_type.declaration_code(''),
                        type_convert = self.real_type.from_py_function))
        self.from_py_function = "__pyx_PyObject_As_" + self.specalization_name()
        return True
    
    def lookup_op(self, nargs, op):
        try:
            return self.binops[nargs, op]
        except KeyError:
            pass
        try:
            op_name = complex_ops[nargs, op]
            self.binops[nargs, op] = func_name = "%s_%s" % (self.specalization_name(), op_name)
            return func_name
        except KeyError:
            return None

    def unary_op(self, op):
        return self.lookup_op(1, op)
        
    def binary_op(self, op):
        return self.lookup_op(2, op)
        
complex_ops = {
    (1, '-'): 'neg',
    (1, 'zero'): 'is_zero',
    (2, '+'): 'add',
    (2, '-') : 'sub',
    (2, '*'): 'mul',
    (2, '/'): 'div',
    (2, '=='): 'eq',
}

complex_generic_utility_code = UtilityCode(
proto="""
#if __PYX_USE_C99_COMPLEX
    #define __Pyx_REAL_PART(z) __real__(z)
    #define __Pyx_IMAG_PART(z) __imag__(z)
#else
    #define __Pyx_REAL_PART(z) ((z).real)
    #define __Pyx_IMAG_PART(z) ((z).imag)
#endif

#define __pyx_PyObject_from_complex(z) PyComplex_FromDoubles((double)__Pyx_REAL_PART(z), (double)__Pyx_IMAG_PART(z))
""")

complex_conversion_utility_code = UtilityCode(
proto="""
static %(type)s __pyx_PyObject_As_%(type_name)s(PyObject* o); /* proto */
""", 
impl="""
static %(type)s __pyx_PyObject_As_%(type_name)s(PyObject* o) {
    if (PyComplex_Check(o)) {
        return %(type_name)s_from_parts(
            (%(real_type)s)((PyComplexObject *)o)->cval.real,
            (%(real_type)s)((PyComplexObject *)o)->cval.imag);
    }
    else {
        return %(type_name)s_from_parts(%(type_convert)s(o), 0);
    }
}
""")

complex_arithmatic_utility_code = UtilityCode(
proto="""
#if __PYX_USE_C99_COMPLEX

    typedef %(real_type)s _Complex %(type_name)s;
    static INLINE %(type)s %(type_name)s_from_parts(%(real_type)s x, %(real_type)s y) {
      return x + y*(%(type)s)_Complex_I;
    }
    
    #define %(type_name)s_is_zero(a) ((a) == 0)
    #define %(type_name)s_eq(a, b) ((a) == (b))
    #define %(type_name)s_add(a, b) ((a)+(b))
    #define %(type_name)s_sub(a, b) ((a)-(b))
    #define %(type_name)s_mul(a, b) ((a)*(b))
    #define %(type_name)s_div(a, b) ((a)/(b))
    #define %(type_name)s_neg(a) (-(a))

#else

    typedef struct { %(real_type)s real, imag; } %(type_name)s;
    static INLINE %(type)s %(type_name)s_from_parts(%(real_type)s x, %(real_type)s y) {
      %(type)s c; c.real = x; c.imag = y; return c;
    }
    
    static INLINE int %(type_name)s_is_zero(%(type)s a) {
       return (a.real == 0) & (a.imag == 0);
    }

    static INLINE int %(type_name)s_eq(%(type)s a, %(type)s b) {
       return (a.real == b.real) & (a.imag == b.imag);
    }

    static INLINE %(type)s %(type_name)s_add(%(type)s a, %(type)s b) {
        %(type)s z;
        z.real = a.real + b.real;
        z.imag = a.imag + b.imag;
        return z;
    }

    static INLINE %(type)s %(type_name)s_sub(%(type)s a, %(type)s b) {
        %(type)s z;
        z.real = a.real - b.real;
        z.imag = a.imag - b.imag;
        return z;
    }

    static INLINE %(type)s %(type_name)s_mul(%(type)s a, %(type)s b) {
        %(type)s z;
        z.real = a.real * b.real - a.imag * b.imag;
        z.imag = a.real * b.imag + a.imag * b.real;
        return z;
    }

    static INLINE %(type)s %(type_name)s_div(%(type)s a, %(type)s b) {
        %(type)s z;
        %(real_type)s denom = b.real*b.real + b.imag*b.imag;
        z.real = (a.real * b.real + a.imag * b.imag) / denom;
        z.imag = (a.imag * b.real - a.real * b.imag) / denom;
        return z;
    }

    static INLINE %(type)s %(type_name)s_neg(%(type)s a) {
        %(type)s z;
        z.real = -a.real;
        z.imag = -a.imag;
        return z;
    }

#endif
""")


class CArrayType(CType):
    #  base_type     CType              Element type
    #  size          integer or None    Number of elements
    
    is_array = 1
    
    def __init__(self, base_type, size):
        self.base_type = base_type
        self.size = size
        if base_type is c_char_type:
            self.is_string = 1
    
    def __repr__(self):
        return "<CArrayType %s %s>" % (self.size, repr(self.base_type))
    
    def same_as_resolved_type(self, other_type):
        return ((other_type.is_array and
            self.base_type.same_as(other_type.base_type))
                or other_type is error_type)
    
    def assignable_from_resolved_type(self, src_type):
        # Can't assign to a variable of an array type
        return 0
    
    def element_ptr_type(self):
        return c_ptr_type(self.base_type)

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if self.size is not None:
            dimension_code = self.size
        else:
            dimension_code = ""
        if entity_code.startswith("*"):
            entity_code = "(%s)" % entity_code
        return self.base_type.declaration_code(
            "%s[%s]" % (entity_code, dimension_code),
            for_display, dll_linkage, pyrex)
    
    def as_argument_type(self):
        return c_ptr_type(self.base_type)
    
    def is_complete(self):
        return self.size is not None


class CPtrType(CType):
    #  base_type     CType    Referenced type
    
    is_ptr = 1
    default_value = "0"
    
    def __init__(self, base_type):
        self.base_type = base_type
    
    def __repr__(self):
        return "<CPtrType %s>" % repr(self.base_type)
    
    def same_as_resolved_type(self, other_type):
        return ((other_type.is_ptr and
            self.base_type.same_as(other_type.base_type))
                or other_type is error_type)
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        #print "CPtrType.declaration_code: pointer to", self.base_type ###
        return self.base_type.declaration_code(
            "*%s" % entity_code,
            for_display, dll_linkage, pyrex)
    
    def assignable_from_resolved_type(self, other_type):
        if other_type is error_type:
            return 1
        if other_type.is_null_ptr:
            return 1
        if self.base_type.is_cfunction:
            if other_type.is_ptr:
                other_type = other_type.base_type.resolve()
            if other_type.is_cfunction:
                return self.base_type.pointer_assignable_from_resolved_type(other_type)
            else:
                return 0
        if (self.base_type.is_cpp_class and other_type.is_ptr 
                and other_type.base_type.is_cpp_class and other_type.base_type.is_subclass(self.base_type)):
            return 1
        if other_type.is_array or other_type.is_ptr:
            return self.base_type.is_void or self.base_type.same_as(other_type.base_type)
        return 0
    
    def specialize(self, values):
        base_type = self.base_type.specialize(values)
        if base_type == self.base_type:
            return self
        else:
            return CPtrType(base_type)


class CNullPtrType(CPtrType):

    is_null_ptr = 1
    

class CFuncType(CType):
    #  return_type      CType
    #  args             [CFuncTypeArg]
    #  has_varargs      boolean
    #  exception_value  string
    #  exception_check  boolean    True if PyErr_Occurred check needed
    #  calling_convention  string  Function calling convention
    #  nogil            boolean    Can be called without gil
    #  with_gil         boolean    Acquire gil around function body
    #  templates        [string] or None
    
    is_cfunction = 1
    original_sig = None
    
    def __init__(self, return_type, args, has_varargs = 0,
            exception_value = None, exception_check = 0, calling_convention = "",
            nogil = 0, with_gil = 0, is_overridable = 0, optional_arg_count = 0,
            templates = None):
        self.return_type = return_type
        self.args = args
        self.has_varargs = has_varargs
        self.optional_arg_count = optional_arg_count
        self.exception_value = exception_value
        self.exception_check = exception_check
        self.calling_convention = calling_convention
        self.nogil = nogil
        self.with_gil = with_gil
        self.is_overridable = is_overridable
        self.templates = templates
    
    def __repr__(self):
        arg_reprs = map(repr, self.args)
        if self.has_varargs:
            arg_reprs.append("...")
        return "<CFuncType %s %s[%s]>" % (
            repr(self.return_type),
            self.calling_convention_prefix(),
            ",".join(arg_reprs))
    
    def calling_convention_prefix(self):
        cc = self.calling_convention
        if cc:
            return cc + " "
        else:
            return ""
    
    def same_c_signature_as(self, other_type, as_cmethod = 0):
        return self.same_c_signature_as_resolved_type(
            other_type.resolve(), as_cmethod)

    def same_c_signature_as_resolved_type(self, other_type, as_cmethod = 0):
        #print "CFuncType.same_c_signature_as_resolved_type:", \
        #    self, other_type, "as_cmethod =", as_cmethod ###
        if other_type is error_type:
            return 1
        if not other_type.is_cfunction:
            return 0
        if self.is_overridable != other_type.is_overridable:
            return 0
        nargs = len(self.args)
        if nargs != len(other_type.args):
            return 0
        # When comparing C method signatures, the first argument
        # is exempt from compatibility checking (the proper check
        # is performed elsewhere).
        for i in range(as_cmethod, nargs):
            if not self.args[i].type.same_as(
                other_type.args[i].type):
                    return 0
        if self.has_varargs != other_type.has_varargs:
            return 0
        if self.optional_arg_count != other_type.optional_arg_count:
            return 0
        if not self.return_type.same_as(other_type.return_type):
            return 0
        if not self.same_calling_convention_as(other_type):
            return 0
        return 1

    def compatible_signature_with(self, other_type, as_cmethod = 0):
        return self.compatible_signature_with_resolved_type(other_type.resolve(), as_cmethod)
    
    def compatible_signature_with_resolved_type(self, other_type, as_cmethod):
        #print "CFuncType.same_c_signature_as_resolved_type:", \
        #    self, other_type, "as_cmethod =", as_cmethod ###
        if other_type is error_type:
            return 1
        if not other_type.is_cfunction:
            return 0
        if not self.is_overridable and other_type.is_overridable:
            return 0
        nargs = len(self.args)
        if nargs - self.optional_arg_count != len(other_type.args) - other_type.optional_arg_count:
            return 0
        if self.optional_arg_count < other_type.optional_arg_count:
            return 0
        # When comparing C method signatures, the first argument
        # is exempt from compatibility checking (the proper check
        # is performed elsewhere).
        for i in range(as_cmethod, len(other_type.args)):
            if not self.args[i].type.same_as(
                other_type.args[i].type):
                    return 0
        if self.has_varargs != other_type.has_varargs:
            return 0
        if not self.return_type.subtype_of_resolved_type(other_type.return_type):
            return 0
        if not self.same_calling_convention_as(other_type):
            return 0
        if self.nogil != other_type.nogil:
            return 0
        self.original_sig = other_type.original_sig or other_type
        if as_cmethod:
            self.args[0] = other_type.args[0]
        return 1
        
        
    def narrower_c_signature_than(self, other_type, as_cmethod = 0):
        return self.narrower_c_signature_than_resolved_type(other_type.resolve(), as_cmethod)
        
    def narrower_c_signature_than_resolved_type(self, other_type, as_cmethod):
        if other_type is error_type:
            return 1
        if not other_type.is_cfunction:
            return 0
        nargs = len(self.args)
        if nargs != len(other_type.args):
            return 0
        for i in range(as_cmethod, nargs):
            if not self.args[i].type.subtype_of_resolved_type(other_type.args[i].type):
                return 0
            else:
                self.args[i].needs_type_test = other_type.args[i].needs_type_test \
                        or not self.args[i].type.same_as(other_type.args[i].type)
        if self.has_varargs != other_type.has_varargs:
            return 0
        if self.optional_arg_count != other_type.optional_arg_count:
            return 0
        if not self.return_type.subtype_of_resolved_type(other_type.return_type):
            return 0
        return 1

    def same_calling_convention_as(self, other):
        ## XXX Under discussion ...
        ## callspec_words = ("__stdcall", "__cdecl", "__fastcall")
        ## cs1 = self.calling_convention
        ## cs2 = other.calling_convention
        ## if (cs1 in callspec_words or
        ##     cs2 in callspec_words):
        ##     return cs1 == cs2
        ## else:
        ##     return True
        sc1 = self.calling_convention == '__stdcall'
        sc2 = other.calling_convention == '__stdcall'
        return sc1 == sc2
    
    def same_exception_signature_as(self, other_type):
        return self.same_exception_signature_as_resolved_type(
            other_type.resolve())

    def same_exception_signature_as_resolved_type(self, other_type):
        return self.exception_value == other_type.exception_value \
            and self.exception_check == other_type.exception_check
    
    def same_as_resolved_type(self, other_type, as_cmethod = 0):
        return self.same_c_signature_as_resolved_type(other_type, as_cmethod) \
            and self.same_exception_signature_as_resolved_type(other_type) \
            and self.nogil == other_type.nogil
    
    def pointer_assignable_from_resolved_type(self, other_type):
        return self.same_c_signature_as_resolved_type(other_type) \
            and self.same_exception_signature_as_resolved_type(other_type) \
            and not (self.nogil and not other_type.nogil)
    
    def declaration_code(self, entity_code, 
                         for_display = 0, dll_linkage = None, pyrex = 0,
                         with_calling_convention = 1):
        arg_decl_list = []
        for arg in self.args[:len(self.args)-self.optional_arg_count]:
            arg_decl_list.append(
                arg.type.declaration_code("", for_display, pyrex = pyrex))
        if self.is_overridable:
            arg_decl_list.append("int %s" % Naming.skip_dispatch_cname)
        if self.optional_arg_count:
            arg_decl_list.append(self.op_arg_struct.declaration_code(Naming.optional_args_cname))
        if self.has_varargs:
            arg_decl_list.append("...")
        arg_decl_code = ", ".join(arg_decl_list)
        if not arg_decl_code and not pyrex:
            arg_decl_code = "void"
        trailer = ""
        if (pyrex or for_display) and not self.return_type.is_pyobject:
            if self.exception_value and self.exception_check:
                trailer = " except? %s" % self.exception_value
            elif self.exception_value:
                trailer = " except %s" % self.exception_value
            elif self.exception_check == '+':
                trailer = " except +"
            else:
                " except *" # ignored
            if self.nogil:
                trailer += " nogil"
        if not with_calling_convention:
            cc = ''
        else:
            cc = self.calling_convention_prefix()
            if (not entity_code and cc) or entity_code.startswith("*"):
                entity_code = "(%s%s)" % (cc, entity_code)
                cc = ""
        return self.return_type.declaration_code(
            "%s%s(%s)%s" % (cc, entity_code, arg_decl_code, trailer),
            for_display, dll_linkage, pyrex)
    
    def function_header_code(self, func_name, arg_code):
        return "%s%s(%s)" % (self.calling_convention_prefix(),
            func_name, arg_code)

    def signature_string(self):
        s = self.declaration_code("")
        return s

    def signature_cast_string(self):
        s = self.declaration_code("(*)", with_calling_convention=False)
        return '(%s)' % s


class CFuncTypeArg(object):
    #  name       string
    #  cname      string
    #  type       PyrexType
    #  pos        source file position
    
    def __init__(self, name, type, pos, cname=None):
        self.name = name
        if cname is not None:
            self.cname = cname
        else:
            self.cname = Naming.var_prefix + name
        self.type = type
        self.pos = pos
        self.not_none = False
        self.needs_type_test = False # TODO: should these defaults be set in analyse_types()?
    
    def __repr__(self):
        return "%s:%s" % (self.name, repr(self.type))
    
    def declaration_code(self, for_display = 0):
        return self.type.declaration_code(self.cname, for_display)


class CStructOrUnionType(CType):
    #  name          string
    #  cname         string
    #  kind          string              "struct" or "union"
    #  scope         StructOrUnionScope, or None if incomplete
    #  typedef_flag  boolean
    #  packed        boolean
    
    is_struct_or_union = 1
    has_attributes = 1
    
    def __init__(self, name, kind, scope, typedef_flag, cname, packed=False):
        self.name = name
        self.cname = cname
        self.kind = kind
        self.scope = scope
        self.typedef_flag = typedef_flag
        self.is_struct = kind == 'struct'
        if self.is_struct:
            self.to_py_function = "%s_to_py_%s" % (Naming.convert_func_prefix, self.cname)
        self.exception_check = True
        self._convert_code = None
        self.packed = packed
        
    def create_to_py_utility_code(self, env):
        if env.outer_scope is None:
            return False
        if self._convert_code is None:
            import Code
            code = Code.CCodeWriter()
            Code.GlobalState(code)
            header = "static PyObject* %s(%s)" % (self.to_py_function, self.declaration_code('s'))
            code.putln("%s {" % header)
            code.putln("PyObject* res;")
            code.putln("PyObject* member;")
            code.putln("res = PyDict_New(); if (res == NULL) return NULL;")
            for member in self.scope.var_entries:
                if member.type.to_py_function and member.type.create_to_py_utility_code(env):
                    interned_name = env.get_string_const(member.name, identifier=True)
                    env.add_py_string(interned_name)
                    code.putln("member = %s(s.%s); if (member == NULL) goto bad;" % (
                                                member.type.to_py_function, member.cname))
                    code.putln("if (PyDict_SetItem(res, %s, member) < 0) goto bad;" % interned_name.pystring_cname)
                    code.putln("Py_DECREF(member);")
                else:
                    self.to_py_function = None
                    return False
            code.putln("return res;")
            code.putln("bad:")
            code.putln("Py_XDECREF(member);")
            code.putln("Py_DECREF(res);")
            code.putln("return NULL;")
            code.putln("}")
            proto = header + ";"
            # This is a bit of a hack, we need a forward declaration
            # due to the way things are ordered in the module...
            entry = env.lookup(self.name)
            if entry.visibility != 'extern':
                proto = self.declaration_code('') + ';\n' + proto
            self._convert_code = UtilityCode(proto=proto, impl=code.buffer.getvalue())
        
        env.use_utility_code(self._convert_code)
        return True
        
    def __repr__(self):
        return "<CStructOrUnionType %s %s%s>" % (self.name, self.cname,
            ("", " typedef")[self.typedef_flag])

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex:
            return self.base_declaration_code(self.name, entity_code)
        else:
            if for_display:
                base = self.name
            elif self.typedef_flag:
                base = self.cname
            else:
                base = "%s %s" % (self.kind, self.cname)
            return self.base_declaration_code(public_decl(base, dll_linkage), entity_code)

    def __cmp__(self, other):
        try:
            if self.name == other.name:
                return 0
            else:
                return 1
        except AttributeError:
            return 1

    def is_complete(self):
        return self.scope is not None
    
    def attributes_known(self):
        return self.is_complete()

    def can_be_complex(self):
        # Does the struct consist of exactly two identical floats?
        fields = self.scope.var_entries
        if len(fields) != 2: return False
        a, b = fields
        return (a.type.is_float and b.type.is_float and
                a.type.declaration_code("") ==
                b.type.declaration_code(""))

    def struct_nesting_depth(self):
        child_depths = [x.type.struct_nesting_depth()
                        for x in self.scope.var_entries]
        return max(child_depths) + 1

class CppClassType(CType):
    #  name          string
    #  cname         string
    #  scope         CppClassScope
    #  templates     [string] or None
    
    is_cpp_class = 1
    has_attributes = 1
    exception_check = True
    
    def __init__(self, name, scope, cname, base_classes, templates = None, template_type = None):
        self.name = name
        self.cname = cname
        self.scope = scope
        self.base_classes = base_classes
        self.operators = []
        self.templates = templates
        self.template_type = template_type

    def specialize_here(self, pos, template_values = None):
        if self.templates is None:
            error(pos, "'%s' type is not a template" % self);
            return PyrexTypes.error_type
        if len(self.templates) != len(template_values):
            error(pos, "%s templated type receives %d arguments, got %d" % 
                  (base_type, len(self.templates), len(template_values)))
            return PyrexTypes.error_type
        return self.specialize(dict(zip(self.templates, template_values)))
    
    def specialize(self, values):
        # TODO(danilo): Cache for efficiency.
        template_values = [t.specialize(values) for t in self.templates]
        return CppClassType(self.name, self.scope.specialize(values), self.cname, self.base_classes, 
                            template_values, template_type=self)

    def declaration_code(self, entity_code, for_display = 0, dll_linkage = None, pyrex = 0):
        if self.templates:
            template_strings = [param.declaration_code('', for_display, pyrex) for param in self.templates]
            templates = "<" + ",".join(template_strings) + ">"
        else:
            templates = ""
        if for_display or pyrex:
            name = self.name
        else:
            name = self.cname
        return "%s %s%s" % (name, entity_code, templates)

    def is_subclass(self, other_type):
        # TODO(danilo): Handle templates.
        if self.same_as_resolved_type(other_type):
            return 1
        for base_class in self.base_classes:
            if base_class.is_subclass(other_type):
                return 1
        return 0
    
    def same_as_resolved_type(self, other_type):
        if other_type.is_cpp_class:
            if self == other_type:
                return 1
            elif self.template_type == other.template_type:
                for t1, t2 in zip(self.templates, other.templates):
                    if not t1.same_as_resolved_type(t2):
                        return 0
                return 1
        return 0

    def attributes_known(self):
        return self.scope is not None


class TemplatePlaceholderType(CType):
    
    def __init__(self, name):
        self.name = name
    
    def declaration_code(self, entity_code, for_display = 0, dll_linkage = None, pyrex = 0):
        return self.name + " " + entity_code
    
    def specialize(self, values):
        if self in values:
            return values[self]
        else:
            return self

    def same_as_resolved_type(self, other_type):
        if isinstance(other_type, TemplatePlaceholderType):
            return self.name == other.name
        else:
            return 0
        
    def __hash__(self):
        return hash(self.name)
    
    def __cmp__(self, other):
        if isinstance(other, TemplatePlaceholderType):
            return cmp(self.name, other.name)
        else:
            return cmp(type(self), type(other))

class CEnumType(CType):
    #  name           string
    #  cname          string or None
    #  typedef_flag   boolean

    is_enum = 1
    signed = 1
    rank = -1 # Ranks below any integer type
    to_py_function = "PyInt_FromLong"
    from_py_function = "PyInt_AsLong"

    def __init__(self, name, cname, typedef_flag):
        self.name = name
        self.cname = cname
        self.values = []
        self.typedef_flag = typedef_flag
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "<CEnumType %s %s%s>" % (self.name, self.cname,
            ("", " typedef")[self.typedef_flag])
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex:
            return self.base_declaration_code(self.cname, entity_code)
        else:
            if self.typedef_flag:
                base = self.cname
            else:
                base = "enum %s" % self.cname
            return self.base_declaration_code(public_decl(base, dll_linkage), entity_code)


class CStringType(object):
    #  Mixin class for C string types.

    is_string = 1
    is_unicode = 0
    
    to_py_function = "__Pyx_PyBytes_FromString"
    from_py_function = "__Pyx_PyBytes_AsString"
    exception_value = "NULL"

    def literal_code(self, value):
        assert isinstance(value, str)
        return '"%s"' % StringEncoding.escape_byte_string(value)


class CUTF8CharArrayType(CStringType, CArrayType):
    #  C 'char []' type.
    
    pymemberdef_typecode = "T_STRING_INPLACE"
    is_unicode = 1
    
    to_py_function = "PyUnicode_DecodeUTF8"
    exception_value = "NULL"
    
    def __init__(self, size):
        CArrayType.__init__(self, c_char_type, size)

class CCharArrayType(CStringType, CArrayType):
    #  C 'char []' type.
    
    pymemberdef_typecode = "T_STRING_INPLACE"
    
    def __init__(self, size):
        CArrayType.__init__(self, c_char_type, size)
    

class CCharPtrType(CStringType, CPtrType):
    # C 'char *' type.
    
    pymemberdef_typecode = "T_STRING"
    
    def __init__(self):
        CPtrType.__init__(self, c_char_type)


class UnspecifiedType(PyrexType):
    # Used as a placeholder until the type can be determined.
        
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        return "<unspecified>"
    
    def same_as_resolved_type(self, other_type):
        return False
        

class ErrorType(PyrexType):
    # Used to prevent propagation of error messages.
    
    is_error = 1
    exception_value = "0"
    exception_check    = 0
    to_py_function = "dummy"
    from_py_function = "dummy"
    
    def create_to_py_utility_code(self, env):
        return True
    
    def create_from_py_utility_code(self, env):
        return True
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        return "<error>"
    
    def same_as_resolved_type(self, other_type):
        return 1
        
    def error_condition(self, result_code):
        return "dummy"


rank_to_type_name = (
    "char",         # 0
    "short",        # 1
    "int",          # 2
    "long",         # 3
    "Py_ssize_t",   # 4
    "size_t",       # 5
    "PY_LONG_LONG", # 6
    "float",        # 7
    "double",       # 8
    "long double",  # 9
)

py_object_type = PyObjectType()

c_void_type =         CVoidType()
c_void_ptr_type =     CPtrType(c_void_type)
c_void_ptr_ptr_type = CPtrType(c_void_ptr_type)

c_uchar_type =       CIntType(0, 0, "T_UBYTE")
c_ushort_type =      CIntType(1, 0, "T_USHORT")
c_uint_type =        CUIntType(2, 0, "T_UINT")
c_ulong_type =       CULongType(3, 0, "T_ULONG")
c_ulonglong_type =   CULongLongType(6, 0, "T_ULONGLONG")

c_char_type =        CIntType(0, 1, "T_CHAR")
c_short_type =       CIntType(1, 1, "T_SHORT")
c_int_type =         CIntType(2, 1, "T_INT")
c_long_type =        CLongType(3, 1, "T_LONG")
c_longlong_type =    CLongLongType(6, 1, "T_LONGLONG")
c_bint_type =        CBIntType(2, 1, "T_INT")

c_schar_type =       CIntType(0, 2, "T_CHAR")
c_sshort_type =      CIntType(1, 2, "T_SHORT")
c_sint_type =        CIntType(2, 2, "T_INT")
c_slong_type =       CLongType(3, 2, "T_LONG")
c_slonglong_type =   CLongLongType(6, 2, "T_LONGLONG")

c_py_ssize_t_type =  CPySSizeTType(4, 2, "T_PYSSIZET")
c_size_t_type =      CSizeTType(5, 0, "T_SIZET")

c_float_type =       CFloatType(7, "T_FLOAT", math_h_modifier='f')
c_double_type =      CFloatType(8, "T_DOUBLE")
c_longdouble_type =  CFloatType(9, math_h_modifier='l')

c_double_complex_type = CComplexType(c_double_type)

c_null_ptr_type =     CNullPtrType(c_void_type)
c_char_array_type =   CCharArrayType(None)
c_char_ptr_type =     CCharPtrType()
c_utf8_char_array_type = CUTF8CharArrayType(None)
c_char_ptr_ptr_type = CPtrType(c_char_ptr_type)
c_int_ptr_type =      CPtrType(c_int_type)
c_py_ssize_t_ptr_type =  CPtrType(c_py_ssize_t_type)
c_size_t_ptr_type =  CPtrType(c_size_t_type)

c_returncode_type =   CIntType(2, 1, "T_INT", is_returncode = 1)

c_anon_enum_type =    CAnonEnumType(-1, 1)

# the Py_buffer type is defined in Builtin.py
c_py_buffer_type = CStructOrUnionType("Py_buffer", "struct", None, 1, "Py_buffer")
c_py_buffer_ptr_type = CPtrType(c_py_buffer_type)

error_type =    ErrorType()
unspecified_type = UnspecifiedType()

sign_and_rank_to_type = {
    #(signed, rank)
    (0, 0): c_uchar_type,
    (0, 1): c_ushort_type,
    (0, 2): c_uint_type,
    (0, 3): c_ulong_type,
    (0, 6): c_ulonglong_type,

    (1, 0): c_char_type,
    (1, 1): c_short_type,
    (1, 2): c_int_type,
    (1, 3): c_long_type,
    (1, 6): c_longlong_type,

    (2, 0): c_schar_type,
    (2, 1): c_sshort_type,
    (2, 2): c_sint_type,
    (2, 3): c_slong_type,
    (2, 6): c_slonglong_type,

    (0, 4): c_py_ssize_t_type,
    (1, 4): c_py_ssize_t_type,
    (2, 4): c_py_ssize_t_type,
    (0, 5): c_size_t_type,
    (1, 5): c_size_t_type,
    (2, 5): c_size_t_type,

    (1, 7): c_float_type,
    (1, 8): c_double_type,
    (1, 9): c_longdouble_type,
# In case we're mixing unsigned ints and floats...
    (0, 7): c_float_type,
    (0, 8): c_double_type,
    (0, 9): c_longdouble_type,
}

modifiers_and_name_to_type = {
    #(signed, longness, name)
    (0, 0, "char"): c_uchar_type,
    (0, -1, "int"): c_ushort_type,
    (0, 0, "int"): c_uint_type,
    (0, 1, "int"): c_ulong_type,
    (0, 2, "int"): c_ulonglong_type,
    (1, 0, "void"): c_void_type,
    (1, 0, "char"): c_char_type,
    (1, -1, "int"): c_short_type,
    (1, 0, "int"): c_int_type,
    (1, 1, "int"): c_long_type,
    (1, 2, "int"): c_longlong_type,
    (1, 0, "float"): c_float_type,
    (1, 0, "double"): c_double_type,
    (1, 1, "double"): c_longdouble_type,
    (1, 0, "object"): py_object_type,
    (1, 0, "bint"): c_bint_type,
    (2, 0, "char"): c_schar_type,
    (2, -1, "int"): c_sshort_type,
    (2, 0, "int"): c_sint_type,
    (2, 1, "int"): c_slong_type,
    (2, 2, "int"): c_slonglong_type,

    (2, 0, "Py_ssize_t"): c_py_ssize_t_type,
    (0, 0, "size_t") : c_size_t_type,

    (1, 0, "long"): c_long_type,
    (1, 0, "short"): c_short_type,
    (1, 0, "longlong"): c_longlong_type,
    (1, 0, "bint"): c_bint_type,
}

def is_promotion(type, other_type):
    return (type.is_int and type.is_int and type.signed == other_type.signed) \
                    or (type.is_float and other_type.is_float) \
                    or (type.is_enum and other_type.is_int)

def widest_numeric_type(type1, type2):
    # Given two numeric types, return the narrowest type
    # encompassing both of them.
    if type1 == type2:
        return type1
    if type1.is_complex:
        if type2.is_complex:
            return CComplexType(widest_numeric_type(type1.real_type, type2.real_type))
        else:
            return CComplexType(widest_numeric_type(type1.real_type, type2))
    elif type2.is_complex:
        return CComplexType(widest_numeric_type(type1, type2.real_type))
    if type1.is_enum and type2.is_enum:
        return c_int_type
    elif type1 is type2:
        return type1
    elif (type1.signed and type2.signed) or (not type1.signed and not type2.signed):
        if type2.rank > type1.rank:
            return type2
        else:
            return type1
    else:
        return sign_and_rank_to_type[min(type1.signed, type2.signed), max(type1.rank, type2.rank)]
    return widest_type

def simple_c_type(signed, longness, name):
    # Find type descriptor for simple type given name and modifiers.
    # Returns None if arguments don't make sense.
    return modifiers_and_name_to_type.get((signed, longness, name))
    
def parse_basic_type(name):
    base = None
    if name.startswith('p_'):
        base = parse_basic_type(name[2:])
    elif name.startswith('p'):
        base = parse_basic_type(name[1:])
    elif name.endswith('*'):
        base = parse_basic_type(name[:-1])
    if base:
        return CPtrType(base)
    elif name.startswith('u'):
        return simple_c_type(0, 0, name[1:])
    else:
        return simple_c_type(1, 0, name)

def c_array_type(base_type, size):
    # Construct a C array type.
    if base_type is c_char_type:
        return CCharArrayType(size)
    elif base_type is error_type:
        return error_type
    else:
        return CArrayType(base_type, size)

def c_ptr_type(base_type):
    # Construct a C pointer type.
    if base_type is c_char_type:
        return c_char_ptr_type
    elif base_type is error_type:
        return error_type
    else:
        return CPtrType(base_type)
        
def Node_to_type(node, env):
    from ExprNodes import NameNode, AttributeNode, StringNode, error
    if isinstance(node, StringNode):
        node = NameNode(node.pos, name=node.value)
    if isinstance(node, NameNode) and node.name in rank_to_type_name:
        return simple_c_type(1, 0, node.name)
    elif isinstance(node, (AttributeNode, NameNode)):
        node.analyze_types(env)
        if not node.entry.is_type:
            pass
    else:
        error(node.pos, "Bad type")

def same_type(type1, type2):
    return type1.same_as(type2)
    
def assignable_from(type1, type2):
    return type1.assignable_from(type2)

def typecast(to_type, from_type, expr_code):
    #  Return expr_code cast to a C type which can be
    #  assigned to to_type, assuming its existing C type
    #  is from_type.
    if to_type is from_type or \
        (not to_type.is_pyobject and assignable_from(to_type, from_type)):
            return expr_code
    else:
        #print "typecast: to", to_type, "from", from_type ###
        return to_type.cast_code(expr_code)


type_conversion_predeclarations = """
/* Type Conversion Predeclarations */

#if PY_MAJOR_VERSION < 3
#define __Pyx_PyBytes_FromString          PyString_FromString
#define __Pyx_PyBytes_FromStringAndSize   PyString_FromStringAndSize
#define __Pyx_PyBytes_AsString            PyString_AsString
#else
#define __Pyx_PyBytes_FromString          PyBytes_FromString
#define __Pyx_PyBytes_FromStringAndSize   PyBytes_FromStringAndSize
#define __Pyx_PyBytes_AsString            PyBytes_AsString
#endif

#define __Pyx_PyBool_FromLong(b) ((b) ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False))
static INLINE int __Pyx_PyObject_IsTrue(PyObject*);
static INLINE PyObject* __Pyx_PyNumber_Int(PyObject* x);

#if !defined(T_PYSSIZET)
#if PY_VERSION_HEX < 0x02050000
#define T_PYSSIZET T_INT
#elif !defined(T_LONGLONG)
#define T_PYSSIZET \\
        ((sizeof(Py_ssize_t) == sizeof(int))  ? T_INT  : \\
        ((sizeof(Py_ssize_t) == sizeof(long)) ? T_LONG : -1))
#else
#define T_PYSSIZET \\
        ((sizeof(Py_ssize_t) == sizeof(int))          ? T_INT      : \\
        ((sizeof(Py_ssize_t) == sizeof(long))         ? T_LONG     : \\
        ((sizeof(Py_ssize_t) == sizeof(PY_LONG_LONG)) ? T_LONGLONG : -1)))
#endif
#endif


#if !defined(T_ULONGLONG)
#define __Pyx_T_UNSIGNED_INT(x) \\
        ((sizeof(x) == sizeof(unsigned char))  ? T_UBYTE : \\
        ((sizeof(x) == sizeof(unsigned short)) ? T_USHORT : \\
        ((sizeof(x) == sizeof(unsigned int))   ? T_UINT : \\
        ((sizeof(x) == sizeof(unsigned long))  ? T_ULONG : -1))))
#else
#define __Pyx_T_UNSIGNED_INT(x) \\
        ((sizeof(x) == sizeof(unsigned char))  ? T_UBYTE : \\
        ((sizeof(x) == sizeof(unsigned short)) ? T_USHORT : \\
        ((sizeof(x) == sizeof(unsigned int))   ? T_UINT : \\
        ((sizeof(x) == sizeof(unsigned long))  ? T_ULONG : \\
        ((sizeof(x) == sizeof(unsigned PY_LONG_LONG)) ? T_ULONGLONG : -1)))))
#endif
#if !defined(T_LONGLONG)
#define __Pyx_T_SIGNED_INT(x) \\
        ((sizeof(x) == sizeof(char))  ? T_BYTE : \\
        ((sizeof(x) == sizeof(short)) ? T_SHORT : \\
        ((sizeof(x) == sizeof(int))   ? T_INT : \\
        ((sizeof(x) == sizeof(long))  ? T_LONG : -1))))
#else
#define __Pyx_T_SIGNED_INT(x) \\
        ((sizeof(x) == sizeof(char))  ? T_BYTE : \\
        ((sizeof(x) == sizeof(short)) ? T_SHORT : \\
        ((sizeof(x) == sizeof(int))   ? T_INT : \\
        ((sizeof(x) == sizeof(long))  ? T_LONG : \\
        ((sizeof(x) == sizeof(PY_LONG_LONG))   ? T_LONGLONG : -1)))))
#endif

#define __Pyx_T_FLOATING(x) \\
        ((sizeof(x) == sizeof(float)) ? T_FLOAT : \\
        ((sizeof(x) == sizeof(double)) ? T_DOUBLE : -1))

#if !defined(T_SIZET)
#if !defined(T_ULONGLONG)
#define T_SIZET \\
        ((sizeof(size_t) == sizeof(unsigned int))  ? T_UINT  : \\
        ((sizeof(size_t) == sizeof(unsigned long)) ? T_ULONG : -1))
#else
#define T_SIZET \\
        ((sizeof(size_t) == sizeof(unsigned int))          ? T_UINT      : \\
        ((sizeof(size_t) == sizeof(unsigned long))         ? T_ULONG     : \\
        ((sizeof(size_t) == sizeof(unsigned PY_LONG_LONG)) ? T_ULONGLONG : -1)))
#endif
#endif

static INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject*);
static INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t);
static INLINE size_t __Pyx_PyInt_AsSize_t(PyObject*);

#define __pyx_PyFloat_AsDouble(x) (PyFloat_CheckExact(x) ? PyFloat_AS_DOUBLE(x) : PyFloat_AsDouble(x))

""" + type_conversion_predeclarations

type_conversion_functions = """
/* Type Conversion Functions */

static INLINE int __Pyx_PyObject_IsTrue(PyObject* x) {
   if (x == Py_True) return 1;
   else if ((x == Py_False) | (x == Py_None)) return 0;
   else return PyObject_IsTrue(x);
}

static INLINE PyObject* __Pyx_PyNumber_Int(PyObject* x) {
  PyNumberMethods *m;
  const char *name = NULL;
  PyObject *res = NULL;
#if PY_VERSION_HEX < 0x03000000
  if (PyInt_Check(x) || PyLong_Check(x))
#else
  if (PyLong_Check(x))
#endif
    return Py_INCREF(x), x;
  m = Py_TYPE(x)->tp_as_number;
#if PY_VERSION_HEX < 0x03000000
  if (m && m->nb_int) {
    name = "int";
    res = PyNumber_Int(x);
  }
  else if (m && m->nb_long) {
    name = "long";
    res = PyNumber_Long(x);
  }
#else
  if (m && m->nb_int) {
    name = "int";
    res = PyNumber_Long(x);
  }
#endif
  if (res) {
#if PY_VERSION_HEX < 0x03000000
    if (!PyInt_Check(res) && !PyLong_Check(res)) {
#else
    if (!PyLong_Check(res)) {
#endif
      PyErr_Format(PyExc_TypeError,
                   "__%s__ returned non-%s (type %.200s)",
                   name, name, Py_TYPE(res)->tp_name);
      Py_DECREF(res);
      return NULL;
    }
  }
  else if (!PyErr_Occurred()) {
    PyErr_SetString(PyExc_TypeError,
                    "an integer is required");
  }
  return res;
}

static INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject* b) {
  Py_ssize_t ival;
  PyObject* x = PyNumber_Index(b);
  if (!x) return -1;
  ival = PyInt_AsSsize_t(x);
  Py_DECREF(x);
  return ival;
}

static INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t ival) {
#if PY_VERSION_HEX < 0x02050000
   if (ival <= LONG_MAX)
       return PyInt_FromLong((long)ival);
   else {
       unsigned char *bytes = (unsigned char *) &ival;
       int one = 1; int little = (int)*(unsigned char*)&one;
       return _PyLong_FromByteArray(bytes, sizeof(size_t), little, 0);
   }
#else
   return PyInt_FromSize_t(ival);
#endif
}

static INLINE size_t __Pyx_PyInt_AsSize_t(PyObject* x) {
   unsigned PY_LONG_LONG val = __Pyx_PyInt_AsUnsignedLongLong(x);
   if (unlikely(val == (unsigned PY_LONG_LONG)-1 && PyErr_Occurred())) {
       return (size_t)-1;
   } else if (unlikely(val != (unsigned PY_LONG_LONG)(size_t)val)) {
       PyErr_SetString(PyExc_OverflowError,
                       "value too large to convert to size_t");
       return (size_t)-1;
   }
   return (size_t)val;
}

""" + type_conversion_functions


