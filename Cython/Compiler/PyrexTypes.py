#
#   Pyrex - Types
#

from Code import UtilityCode
import StringEncoding
import Naming
import copy
from Errors import error

class BaseType(object):
    #
    #  Base class for all Pyrex types including pseudo-types.

    def can_coerce_to_pyobject(self, env):
        return False

    def cast_code(self, expr_code):
        return "((%s)%s)" % (self.declaration_code(""), expr_code)
    
    def specialization_name(self):
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
    #  is_float              boolean     Is a C floating point type
    #  is_complex            boolean     Is a C complex type
    #  is_void               boolean     Is the C void type
    #  is_array              boolean     Is a C array type
    #  is_ptr                boolean     Is a C pointer type
    #  is_null_ptr           boolean     Is the type of NULL
    #  is_reference          boolean     Is a C reference type
    #  is_cfunction          boolean     Is a C function type
    #  is_struct_or_union    boolean     Is a C struct or union type
    #  is_struct             boolean     Is a C struct type
    #  is_enum               boolean     Is a C enum type
    #  is_typedef            boolean     Is a typedef type
    #  is_string             boolean     Is a C char * type
    #  is_unicode            boolean     Is a UTF-8 encoded C char * type
    #  is_unicode_char       boolean     Is either Py_UCS4 or Py_UNICODE
    #  is_returncode         boolean     Is used only to signal exceptions
    #  is_error              boolean     Is the dummy error type
    #  is_buffer             boolean     Is buffer access type
    #  has_attributes        boolean     Has C dot-selectable attributes
    #  default_value         string      Initial value
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
    is_unspecified = 0
    is_extension_type = 0
    is_builtin_type = 0
    is_numeric = 0
    is_int = 0
    is_float = 0
    is_complex = 0
    is_void = 0
    is_array = 0
    is_ptr = 0
    is_null_ptr = 0
    is_reference = 0
    is_cfunction = 0
    is_struct_or_union = 0
    is_cpp_class = 0
    is_struct = 0
    is_enum = 0
    is_typedef = 0
    is_string = 0
    is_unicode = 0
    is_unicode_char = 0
    is_returncode = 0
    is_error = 0
    is_buffer = 0
    has_attributes = 0
    default_value = ""
    
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


def public_decl(base_code, dll_linkage):
    if dll_linkage:
        return "%s(%s)" % (dll_linkage, base_code)
    else:
        return base_code
    
def create_typedef_type(name, base_type, cname, is_external=0):
    if base_type.is_complex:
        if is_external:
            raise ValueError("Complex external typedefs not supported")
        return base_type
    else:
        return CTypedefType(name, base_type, cname, is_external)


class CTypedefType(BaseType):
    #
    #  Pseudo-type defined with a ctypedef statement in a
    #  'cdef extern from' block. Delegates most attribute
    #  lookups to the base type. ANYTHING NOT DEFINED
    #  HERE IS DELEGATED!
    #
    #  qualified_name      string
    #  typedef_name        string
    #  typedef_cname       string
    #  typedef_base_type   PyrexType
    #  typedef_is_external bool
    
    is_typedef = 1
    typedef_is_external = 0

    to_py_utility_code = None
    from_py_utility_code = None
    
    
    def __init__(self, name, base_type, cname, is_external=0):
        assert not base_type.is_complex
        self.typedef_name = name
        self.typedef_cname = cname
        self.typedef_base_type = base_type
        self.typedef_is_external = is_external
    
    def resolve(self):
        return self.typedef_base_type.resolve()
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            base_code = self.typedef_name
        else:
            base_code = public_decl(self.typedef_cname, dll_linkage)
        return self.base_declaration_code(base_code, entity_code)
    
    def as_argument_type(self):
        return self

    def cast_code(self, expr_code):
        # If self is really an array (rather than pointer), we can't cast.
        # For example, the gmp mpz_t. 
        if self.typedef_base_type.is_array:
            base_type = self.typedef_base_type.base_type
            return CPtrType(base_type).cast_code(expr_code)
        else:
            return BaseType.cast_code(self, expr_code)

    def __repr__(self):
        return "<CTypedefType %s>" % self.typedef_cname
    
    def __str__(self):
        return self.typedef_name

    def _create_utility_code(self, template_utility_code,
                             template_function_name):
        type_name = self.typedef_cname.replace(" ","_").replace("::","__")
        utility_code = template_utility_code.specialize(
            type     = self.typedef_cname,
            TypeName = type_name)
        function_name = template_function_name % type_name
        return utility_code, function_name

    def create_to_py_utility_code(self, env):
        if self.typedef_is_external:
            if not self.to_py_utility_code:
                base_type = self.typedef_base_type
                if type(base_type) is CIntType:
                    # Various subclasses have special methods
                    # that should be inherited.
                    self.to_py_utility_code, self.to_py_function = \
                        self._create_utility_code(c_typedef_int_to_py_function,
                                                  '__Pyx_PyInt_to_py_%s')
                elif base_type.is_float:
                    pass # XXX implement!
                elif base_type.is_complex:
                    pass # XXX implement!
                    pass
            if self.to_py_utility_code:
                env.use_utility_code(self.to_py_utility_code)
                return True
        # delegation
        return self.typedef_base_type.create_to_py_utility_code(env)

    def create_from_py_utility_code(self, env):
        if self.typedef_is_external:
            if not self.from_py_utility_code:
                base_type = self.typedef_base_type
                if type(base_type) is CIntType:
                    # Various subclasses have special methods
                    # that should be inherited.
                    self.from_py_utility_code, self.from_py_function = \
                        self._create_utility_code(c_typedef_int_from_py_function,
                                                  '__Pyx_PyInt_from_py_%s')
                elif base_type.is_float:
                    pass # XXX implement!
                elif base_type.is_complex:
                    pass # XXX implement!
            if self.from_py_utility_code:
                env.use_utility_code(self.from_py_utility_code)
                return True
        # delegation
        return self.typedef_base_type.create_from_py_utility_code(env)

    def error_condition(self, result_code):
        if self.typedef_is_external:
            if self.exception_value:
                condition = "(%s == (%s)%s)" % (
                    result_code, self.typedef_cname, self.exception_value)
                if self.exception_check:
                    condition += " && PyErr_Occurred()"
                return condition
        # delegation
        return self.typedef_base_type.error_condition(result_code)

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


class PyObjectType(PyrexType):
    #
    #  Base class for all Python object types (reference-counted).
    #
    #  buffer_defaults  dict or None     Default options for bu

    name = "object"
    is_pyobject = 1
    default_value = "0"
    buffer_defaults = None
    is_extern = False
    is_subclassed = False
    
    def __str__(self):
        return "Python object"
    
    def __repr__(self):
        return "<PyObjectType>"

    def can_coerce_to_pyobject(self, env):
        return True

    def default_coerced_ctype(self):
        "The default C type that this Python type coerces to, or None."
        return None

    def assignable_from(self, src_type):
        # except for pointers, conversion will be attempted
        return not src_type.is_ptr or src_type.is_string
        
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            base_code = "object"
        else:
            base_code = public_decl("PyObject", dll_linkage)
            entity_code = "*%s" % entity_code
        return self.base_declaration_code(base_code, entity_code)

    def as_pyobject(self, cname):
        if (not self.is_complete()) or self.is_extension_type:
            return "(PyObject *)" + cname
        else:
            return cname

class BuiltinObjectType(PyObjectType):
    #  objstruct_cname  string           Name of PyObject struct

    is_builtin_type = 1
    has_attributes = 1
    base_type = None
    module_name = '__builtin__'

    # fields that let it look like an extension type
    vtabslot_cname = None
    vtabstruct_cname = None
    vtabptr_cname = None
    typedef_flag = True
    is_external = True

    def __init__(self, name, cname, objstruct_cname=None):
        self.name = name
        self.cname = cname
        self.typeptr_cname = "(&%s)" % cname
        self.objstruct_cname = objstruct_cname
                                 
    def set_scope(self, scope):
        self.scope = scope
        if scope:
            scope.parent_type = self
        
    def __str__(self):
        return "%s object" % self.name
    
    def __repr__(self):
        return "<%s>"% self.cname

    def default_coerced_ctype(self):
        if self.name == 'bytes':
            return c_char_ptr_type
        elif self.name == 'bool':
            return c_bint_type
        elif self.name == 'float':
            return c_double_type
        return None

    def assignable_from(self, src_type):
        if isinstance(src_type, BuiltinObjectType):
            return src_type.name == self.name
        elif src_type.is_extension_type:
            return (src_type.module_name == '__builtin__' and
                    src_type.name == self.name)
        else:
            return True
            
    def typeobj_is_available(self):
        return True
        
    def attributes_known(self):
        return True
        
    def subtype_of(self, type):
        return type.is_pyobject and self.assignable_from(type)

    def type_check_function(self, exact=True):
        type_name = self.name
        if type_name == 'str':
            type_check = 'PyString_Check'
        elif type_name == 'frozenset':
            type_check = 'PyFrozenSet_Check'
        else:
            type_check = 'Py%s_Check' % type_name.capitalize()
        if exact and type_name not in ('bool', 'slice'):
            type_check += 'Exact'
        return type_check

    def isinstance_code(self, arg):
        return '%s(%s)' % (self.type_check_function(exact=False), arg)

    def type_test_code(self, arg, notnone=False):
        type_check = self.type_check_function(exact=True)
        check = 'likely(%s(%s))' % (type_check, arg)
        if not notnone:
            check = check + ('||((%s) == Py_None)' % arg)
        error = '(PyErr_Format(PyExc_TypeError, "Expected %s, got %%.200s", Py_TYPE(%s)->tp_name), 0)' % (self.name, arg)
        return check + '||' + error

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            base_code = self.name
        else:
            base_code = public_decl("PyObject", dll_linkage)
            entity_code = "*%s" % entity_code
        return self.base_declaration_code(base_code, entity_code)

    def cast_code(self, expr_code, to_object_struct = False):
        return "((%s*)%s)" % (
            to_object_struct and self.objstruct_cname or "PyObject", # self.objstruct_cname may be None
            expr_code)


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
    #  objtypedef_cname string           Name of PyObject struct typedef
    #  typeobj_cname    string or None   C code fragment referring to type object
    #  typeptr_cname    string or None   Name of pointer to external type object
    #  vtabslot_cname   string           Name of C method table member
    #  vtabstruct_cname string           Name of C method table struct
    #  vtabptr_cname    string           Name of pointer to C method table
    #  vtable_cname     string           Name of C method table definition
    
    is_extension_type = 1
    has_attributes = 1
    
    objtypedef_cname = None
    
    def __init__(self, name, typedef_flag, base_type, is_external=0):
        self.name = name
        self.scope = None
        self.typedef_flag = typedef_flag
        if base_type is not None:
            base_type.is_subclassed = True
        self.base_type = base_type
        self.module_name = None
        self.objstruct_cname = None
        self.typeobj_cname = None
        self.typeptr_cname = None
        self.vtabslot_cname = None
        self.vtabstruct_cname = None
        self.vtabptr_cname = None
        self.vtable_cname = None
        self.is_external = is_external
    
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
    
    def assignable_from(self, src_type):
        if self == src_type:
            return True
        if isinstance(src_type, PyExtensionType):
            if src_type.base_type is not None:
                return self.assignable_from(src_type.base_type)
        return False

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0, deref = 0):
        if pyrex or for_display:
            base_code = self.name
        else:
            if self.typedef_flag:
                objstruct = self.objstruct_cname
            else:
                objstruct = "struct %s" % self.objstruct_cname
            base_code = public_decl(objstruct, dll_linkage)
            if deref:
                assert not entity_code
            else:
                entity_code = "*%s" % entity_code
        return self.base_declaration_code(base_code, entity_code)

    def type_test_code(self, py_arg, notnone=False):

        none_check = "((%s) == Py_None)" % py_arg
        type_check = "likely(__Pyx_TypeTest(%s, %s))" % (
            py_arg, self.typeptr_cname)
        if notnone:
            return type_check
        else:
            return "likely(%s || %s)" % (none_check, type_check)

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

    def can_coerce_to_pyobject(self, env):
        return self.create_to_py_utility_code(env)

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
    #
    #   C "void" type
    #

    is_void = 1
    
    def __repr__(self):
        return "<CVoidType>"
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            base_code = "void"
        else:
            base_code = public_decl("void", dll_linkage)
        return self.base_declaration_code(base_code, entity_code)
    
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
    has_attributes = True
    scope = None
    
    sign_words = ("unsigned ", "", "signed ")
    
    def __init__(self, rank, signed = 1):
        self.rank = rank
        self.signed = signed
    
    def sign_and_name(self):
        s = self.sign_words[self.signed]
        n = rank_to_type_name[self.rank]
        return s + n
    
    def __repr__(self):
        return "<CNumericType %s>" % self.sign_and_name()
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        type_name = self.sign_and_name()
        if pyrex or for_display:
            base_code = type_name.replace('PY_LONG_LONG', 'long long')
        else:
            base_code = public_decl(type_name, dll_linkage)
        return self.base_declaration_code(base_code, entity_code)
                    
    def attributes_known(self):
        if self.scope is None:
            import Symtab
            self.scope = scope = Symtab.CClassScope(
                    '',
                    None,
                    visibility="extern")
            scope.parent_type = self
            scope.directives = {}
            entry = scope.declare_cfunction(
                    "conjugate",
                    CFuncType(self, [CFuncTypeArg("self", self, None)], nogil=True),
                    pos=None,
                    defining=1,
                    cname=" ")
        return True


type_conversion_predeclarations = ""
type_conversion_functions = ""

c_int_from_py_function = UtilityCode(
proto="""
static CYTHON_INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject *);
""",
impl="""
static CYTHON_INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject* x) {
    const %(type)s neg_one = (%(type)s)-1, const_zero = 0;
    const int is_unsigned = neg_one > const_zero;
    if (sizeof(%(type)s) < sizeof(long)) {
        long val = __Pyx_PyInt_AsLong(x);
        if (unlikely(val != (long)(%(type)s)val)) {
            if (!unlikely(val == -1 && PyErr_Occurred())) {
                PyErr_SetString(PyExc_OverflowError,
                    (is_unsigned && unlikely(val < 0)) ?
                    "can't convert negative value to %(type)s" :
                    "value too large to convert to %(type)s");
            }
            return (%(type)s)-1;
        }
        return (%(type)s)val;
    }
    return (%(type)s)__Pyx_PyInt_As%(SignWord)sLong(x);
}
""") #fool emacs: '

c_long_from_py_function = UtilityCode(
proto="""
static CYTHON_INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject *);
""",
impl="""
static CYTHON_INLINE %(type)s __Pyx_PyInt_As%(SignWord)s%(TypeName)s(PyObject* x) {
    const %(type)s neg_one = (%(type)s)-1, const_zero = 0;
    const int is_unsigned = neg_one > const_zero;
#if PY_VERSION_HEX < 0x03000000
    if (likely(PyInt_Check(x))) {
        long val = PyInt_AS_LONG(x);
        if (is_unsigned && unlikely(val < 0)) {
            PyErr_SetString(PyExc_OverflowError,
                            "can't convert negative value to %(type)s");
            return (%(type)s)-1;
        }
        return (%(type)s)val;
    } else
#endif
    if (likely(PyLong_Check(x))) {
        if (is_unsigned) {
            if (unlikely(Py_SIZE(x) < 0)) {
                PyErr_SetString(PyExc_OverflowError,
                                "can't convert negative value to %(type)s");
                return (%(type)s)-1;
            }
            return PyLong_AsUnsigned%(TypeName)s(x);
        } else {
            return PyLong_As%(TypeName)s(x);
        }
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

c_typedef_int_from_py_function = UtilityCode(
proto="""
static CYTHON_INLINE %(type)s __Pyx_PyInt_from_py_%(TypeName)s(PyObject *);
""",
impl="""
static CYTHON_INLINE %(type)s __Pyx_PyInt_from_py_%(TypeName)s(PyObject* x) {
    const %(type)s neg_one = (%(type)s)-1, const_zero = (%(type)s)0;
    const int is_unsigned = const_zero < neg_one;
    if (sizeof(%(type)s) == sizeof(char)) {
        if (is_unsigned)
            return (%(type)s)__Pyx_PyInt_AsUnsignedChar(x);
        else
            return (%(type)s)__Pyx_PyInt_AsSignedChar(x);
    } else if (sizeof(%(type)s) == sizeof(short)) {
        if (is_unsigned)
            return (%(type)s)__Pyx_PyInt_AsUnsignedShort(x);
        else
            return (%(type)s)__Pyx_PyInt_AsSignedShort(x);
    } else if (sizeof(%(type)s) == sizeof(int)) {
        if (is_unsigned)
            return (%(type)s)__Pyx_PyInt_AsUnsignedInt(x);
        else
            return (%(type)s)__Pyx_PyInt_AsSignedInt(x);
    } else if (sizeof(%(type)s) == sizeof(long)) {
        if (is_unsigned)
            return (%(type)s)__Pyx_PyInt_AsUnsignedLong(x);
        else
            return (%(type)s)__Pyx_PyInt_AsSignedLong(x);
    } else if (sizeof(%(type)s) == sizeof(PY_LONG_LONG)) {
        if (is_unsigned)
            return (%(type)s)__Pyx_PyInt_AsUnsignedLongLong(x);
        else
            return (%(type)s)__Pyx_PyInt_AsSignedLongLong(x);
    }  else {
        %(type)s val;
        PyObject *v = __Pyx_PyNumber_Int(x);
        #if PY_VERSION_HEX < 0x03000000
        if (likely(v) && !PyLong_Check(v)) {
            PyObject *tmp = v;
            v = PyNumber_Long(tmp);
            Py_DECREF(tmp);
        }
        #endif
        if (likely(v)) {
            int one = 1; int is_little = (int)*(unsigned char *)&one;
            unsigned char *bytes = (unsigned char *)&val;
            int ret = _PyLong_AsByteArray((PyLongObject *)v,
                                          bytes, sizeof(val),
                                          is_little, !is_unsigned);
            Py_DECREF(v);
            if (likely(!ret))
                return val;
        }
        return (%(type)s)-1;
    }
}
""")

c_typedef_int_to_py_function = UtilityCode(
proto="""
static CYTHON_INLINE PyObject *__Pyx_PyInt_to_py_%(TypeName)s(%(type)s);
""",
impl="""
static CYTHON_INLINE PyObject *__Pyx_PyInt_to_py_%(TypeName)s(%(type)s val) {
    const %(type)s neg_one = (%(type)s)-1, const_zero = (%(type)s)0;
    const int is_unsigned = const_zero < neg_one;
    if ((sizeof(%(type)s) == sizeof(char))  ||
        (sizeof(%(type)s) == sizeof(short))) {
        return PyInt_FromLong((long)val);
    } else if ((sizeof(%(type)s) == sizeof(int)) ||
               (sizeof(%(type)s) == sizeof(long))) {
        if (is_unsigned)
            return PyLong_FromUnsignedLong((unsigned long)val);
        else
            return PyInt_FromLong((long)val);
    } else if (sizeof(%(type)s) == sizeof(PY_LONG_LONG)) {
        if (is_unsigned)
            return PyLong_FromUnsignedLongLong((unsigned PY_LONG_LONG)val);
        else
            return PyLong_FromLongLong((PY_LONG_LONG)val);
    } else {
        int one = 1; int little = (int)*(unsigned char *)&one;
        unsigned char *bytes = (unsigned char *)&val;
        return _PyLong_FromByteArray(bytes, sizeof(%(type)s), 
                                     little, !is_unsigned);
    }
}
""")

class CIntType(CNumericType):

    is_int = 1
    typedef_flag = 0
    to_py_function = None
    from_py_function = None
    exception_value = -1

    def __init__(self, rank, signed = 1):
        CNumericType.__init__(self, rank, signed)
        if self.to_py_function is None:
            self.to_py_function = self.get_to_py_type_conversion()
        if self.from_py_function is None:
            self.from_py_function = self.get_from_py_type_conversion()

    def get_to_py_type_conversion(self):
        if self.rank < list(rank_to_type_name).index('int'):
            # This assumes sizeof(short) < sizeof(int)
            return "PyInt_FromLong"
        else:
            # Py{Int|Long}_From[Unsigned]Long[Long]
            Prefix = "Int"
            SignWord = ""
            TypeName = "Long"
            if not self.signed:
                Prefix = "Long"
                SignWord = "Unsigned"
            if self.rank >= list(rank_to_type_name).index('PY_LONG_LONG'):
                Prefix = "Long"
                TypeName = "LongLong"
            return "Py%s_From%s%s" % (Prefix, SignWord, TypeName)

    def get_from_py_type_conversion(self):
        type_name = rank_to_type_name[self.rank]
        type_name = type_name.replace("PY_LONG_LONG", "long long")
        TypeName = type_name.title().replace(" ", "")
        SignWord = self.sign_words[self.signed].strip().title()
        if self.rank >= list(rank_to_type_name).index('long'):
            utility_code = c_long_from_py_function
        else:
            utility_code = c_int_from_py_function
        utility_code.specialize(self,
                                SignWord=SignWord,
                                TypeName=TypeName)
        func_name = "__Pyx_PyInt_As%s%s" % (SignWord, TypeName)
        return func_name

    def assignable_from_resolved_type(self, src_type):
        return src_type.is_int or src_type.is_enum or src_type is error_type


class CAnonEnumType(CIntType):

    is_enum = 1

    def sign_and_name(self):
        return 'int'


class CReturnCodeType(CIntType):

    is_returncode = 1


class CBIntType(CIntType):

    to_py_function = "__Pyx_PyBool_FromLong"
    from_py_function = "__Pyx_PyObject_IsTrue"
    exception_check = 1 # for C++ bool

    def __repr__(self):
        return "<CNumericType bint>"


class CPyUCS4IntType(CIntType):
    # Py_UCS4

    is_unicode_char = True

    # Py_UCS4 coerces from and to single character unicode strings (or
    # at most two characters on 16bit Unicode builds), but we also
    # allow Python integers as input.  The value range for Py_UCS4
    # is 0..1114111, which is checked when converting from an integer
    # value.

    to_py_function = "PyUnicode_FromOrdinal"
    from_py_function = "__Pyx_PyObject_AsPy_UCS4"

    def create_from_py_utility_code(self, env):
        env.use_utility_code(pyobject_as_py_ucs4_utility_code)
        return True

    def sign_and_name(self):
        return "Py_UCS4"


pyobject_as_py_ucs4_utility_code = UtilityCode(
proto='''
static CYTHON_INLINE Py_UCS4 __Pyx_PyObject_AsPy_UCS4(PyObject*);
''',
impl='''
static CYTHON_INLINE Py_UCS4 __Pyx_PyObject_AsPy_UCS4(PyObject* x) {
   long ival;
   if (PyUnicode_Check(x)) {
       if (likely(PyUnicode_GET_SIZE(x) == 1)) {
           return PyUnicode_AS_UNICODE(x)[0];
       }
       #if Py_UNICODE_SIZE == 2
       else if (PyUnicode_GET_SIZE(x) == 2) {
           Py_UCS4 high_val = PyUnicode_AS_UNICODE(x)[0];
           if (high_val >= 0xD800 && high_val <= 0xDBFF) {
               Py_UCS4 low_val = PyUnicode_AS_UNICODE(x)[1];
               if (low_val >= 0xDC00 && low_val <= 0xDFFF) {
                   return 0x10000 | ((high_val & ((1<<10)-1)) << 10) | (low_val & ((1<<10)-1));
               }
           }
       }
       #endif
       PyErr_Format(PyExc_ValueError,
           "only single character unicode strings can be converted to Py_UCS4, got length "
           #if PY_VERSION_HEX < 0x02050000
           "%d",
           #else
           "%zd",
           #endif
           PyUnicode_GET_SIZE(x));
       return (Py_UCS4)-1;
   }
   ival = __Pyx_PyInt_AsLong(x);
   if (unlikely(ival < 0)) {
       if (!PyErr_Occurred())
           PyErr_SetString(PyExc_OverflowError,
                           "cannot convert negative value to Py_UCS4");
       return (Py_UCS4)-1;
   } else if (unlikely(ival > 1114111)) {
       PyErr_SetString(PyExc_OverflowError,
                       "value too large to convert to Py_UCS4");
       return (Py_UCS4)-1;
   }
   return (Py_UCS4)ival;
}
''')


class CPyUnicodeIntType(CIntType):
    # Py_UNICODE

    is_unicode_char = True

    # Py_UNICODE coerces from and to single character unicode strings,
    # but we also allow Python integers as input.  The value range for
    # Py_UNICODE is 0..1114111, which is checked when converting from
    # an integer value.

    to_py_function = "PyUnicode_FromOrdinal"
    from_py_function = "__Pyx_PyObject_AsPy_UNICODE"

    def create_from_py_utility_code(self, env):
        env.use_utility_code(pyobject_as_py_unicode_utility_code)
        return True

    def sign_and_name(self):
        return "Py_UNICODE"

pyobject_as_py_unicode_utility_code = UtilityCode(
proto='''
static CYTHON_INLINE Py_UNICODE __Pyx_PyObject_AsPy_UNICODE(PyObject*);
''',
impl='''
static CYTHON_INLINE Py_UNICODE __Pyx_PyObject_AsPy_UNICODE(PyObject* x) {
   static long maxval = 0;
   long ival;
   if (PyUnicode_Check(x)) {
       if (unlikely(PyUnicode_GET_SIZE(x) != 1)) {
           PyErr_Format(PyExc_ValueError,
               "only single character unicode strings can be converted to Py_UNICODE, got length "
               #if PY_VERSION_HEX < 0x02050000
               "%d",
               #else
               "%zd",
               #endif
               PyUnicode_GET_SIZE(x));
           return (Py_UNICODE)-1;
       }
       return PyUnicode_AS_UNICODE(x)[0];
   }
   if (unlikely(!maxval))
       maxval = (long)PyUnicode_GetMax();
   ival = __Pyx_PyInt_AsLong(x);
   if (unlikely(ival < 0)) {
       if (!PyErr_Occurred())
           PyErr_SetString(PyExc_OverflowError,
                           "cannot convert negative value to Py_UNICODE");
       return (Py_UNICODE)-1;
   } else if (unlikely(ival > maxval)) {
       PyErr_SetString(PyExc_OverflowError,
                       "value too large to convert to Py_UNICODE");
       return (Py_UNICODE)-1;
   }
   return (Py_UNICODE)ival;
}
''')


class CPySSizeTType(CIntType):

    to_py_function = "PyInt_FromSsize_t"
    from_py_function = "__Pyx_PyIndex_AsSsize_t"

    def sign_and_name(self):
        return "Py_ssize_t"

class CSSizeTType(CIntType):

    to_py_function = "PyInt_FromSsize_t"
    from_py_function = "PyInt_AsSsize_t"

    def sign_and_name(self):
        return "Py_ssize_t"

class CSizeTType(CIntType):

    to_py_function = "__Pyx_PyInt_FromSize_t"
    from_py_function = "__Pyx_PyInt_AsSize_t"

    def sign_and_name(self):
        return "size_t"


class CFloatType(CNumericType):

    is_float = 1
    to_py_function = "PyFloat_FromDouble"
    from_py_function = "__pyx_PyFloat_AsDouble"

    exception_value = -1
    
    def __init__(self, rank, math_h_modifier = ''):
        CNumericType.__init__(self, rank, 1)
        self.math_h_modifier = math_h_modifier
    
    def assignable_from_resolved_type(self, src_type):
        return (src_type.is_numeric and not src_type.is_complex) or src_type is error_type


class CComplexType(CNumericType):
    
    is_complex = 1
    to_py_function = "__pyx_PyComplex_FromComplex"
    has_attributes = 1
    scope = None
    
    def __init__(self, real_type):
        while real_type.is_typedef and not real_type.typedef_is_external:
            real_type = real_type.typedef_base_type
        if real_type.is_typedef and real_type.typedef_is_external:
            # The below is not actually used: Coercions are currently disabled
            # so that complex types of external types can not be created
            self.funcsuffix = "_%s" % real_type.specialization_name()
        elif hasattr(real_type, 'math_h_modifier'):
            self.funcsuffix = real_type.math_h_modifier
        else:
            self.funcsuffix = "_%s" % real_type.specialization_name()
    
        self.real_type = real_type
        CNumericType.__init__(self, real_type.rank + 0.5, real_type.signed)
        self.binops = {}
        self.from_parts = "%s_from_parts" % self.specialization_name()
        self.default_value = "%s(0, 0)" % self.from_parts

    def __eq__(self, other):
        if isinstance(self, CComplexType) and isinstance(other, CComplexType):
            return self.real_type == other.real_type
        else:
            return False
    
    def __ne__(self, other):
        if isinstance(self, CComplexType) and isinstance(other, CComplexType):
            return self.real_type != other.real_type
        else:
            return True

    def __lt__(self, other):
        if isinstance(self, CComplexType) and isinstance(other, CComplexType):
            return self.real_type < other.real_type
        else:
            # this is arbitrary, but it makes sure we always have
            # *some* kind of order
            return False

    def __hash__(self):
        return ~hash(self.real_type)

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            real_code = self.real_type.declaration_code("", for_display, dll_linkage, pyrex)
            base_code = "%s complex" % real_code
        else:
            base_code = public_decl(self.sign_and_name(), dll_linkage)
        return self.base_declaration_code(base_code, entity_code)

    def sign_and_name(self):
        real_type_name = self.real_type.specialization_name()
        real_type_name = real_type_name.replace('long__double','long_double')
        real_type_name = real_type_name.replace('PY_LONG_LONG','long_long')
        return Naming.type_prefix + real_type_name + "_complex"
    
    def assignable_from(self, src_type):
        # Temporary hack/feature disabling, see #441
        if (not src_type.is_complex and src_type.is_numeric and src_type.is_typedef
            and src_type.typedef_is_external):
             return False
        else:
            return super(CComplexType, self).assignable_from(src_type)
        
    def assignable_from_resolved_type(self, src_type):
        return (src_type.is_complex and self.real_type.assignable_from_resolved_type(src_type.real_type)
                    or src_type.is_numeric and self.real_type.assignable_from_resolved_type(src_type) 
                    or src_type is error_type)
                    
    def attributes_known(self):
        if self.scope is None:
            import Symtab
            self.scope = scope = Symtab.CClassScope(
                    '',
                    None,
                    visibility="extern")
            scope.parent_type = self
            scope.directives = {}
            scope.declare_var("real", self.real_type, None, "real", is_cdef=True)
            scope.declare_var("imag", self.real_type, None, "imag", is_cdef=True)
            entry = scope.declare_cfunction(
                    "conjugate",
                    CFuncType(self, [CFuncTypeArg("self", self, None)], nogil=True),
                    pos=None,
                    defining=1,
                    cname="__Pyx_c_conj%s" % self.funcsuffix)

        return True

    def create_declaration_utility_code(self, env):
        # This must always be run, because a single CComplexType instance can be shared
        # across multiple compilations (the one created in the module scope)
        env.use_utility_code(complex_header_utility_code)
        env.use_utility_code(complex_real_imag_utility_code)
        for utility_code in (complex_type_utility_code,
                             complex_from_parts_utility_code,
                             complex_arithmetic_utility_code):
            env.use_utility_code(
                utility_code.specialize(
                    self, 
                    real_type = self.real_type.declaration_code(''),
                    m = self.funcsuffix,
                    is_float = self.real_type.is_float))
        return True

    def create_to_py_utility_code(self, env):
        env.use_utility_code(complex_real_imag_utility_code)
        env.use_utility_code(complex_to_py_utility_code)
        return True

    def create_from_py_utility_code(self, env):
        self.real_type.create_from_py_utility_code(env)

        for utility_code in (complex_from_parts_utility_code,
                             complex_from_py_utility_code):
            env.use_utility_code(
                utility_code.specialize(
                    self, 
                    real_type = self.real_type.declaration_code(''),
                    m = self.funcsuffix,
                    is_float = self.real_type.is_float))
        self.from_py_function = "__Pyx_PyComplex_As_" + self.specialization_name()
        return True
    
    def lookup_op(self, nargs, op):
        try:
            return self.binops[nargs, op]
        except KeyError:
            pass
        try:
            op_name = complex_ops[nargs, op]
            self.binops[nargs, op] = func_name = "__Pyx_c_%s%s" % (op_name, self.funcsuffix)
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
    (2, '+'): 'sum',
    (2, '-'): 'diff',
    (2, '*'): 'prod',
    (2, '/'): 'quot',
    (2, '=='): 'eq',
}

complex_header_utility_code = UtilityCode(
proto_block='h_code',
proto="""
#if !defined(CYTHON_CCOMPLEX)
  #if defined(__cplusplus)
    #define CYTHON_CCOMPLEX 1
  #elif defined(_Complex_I)
    #define CYTHON_CCOMPLEX 1
  #else
    #define CYTHON_CCOMPLEX 0
  #endif
#endif

#if CYTHON_CCOMPLEX
  #ifdef __cplusplus
    #include <complex>
  #else
    #include <complex.h>
  #endif
#endif

#if CYTHON_CCOMPLEX && !defined(__cplusplus) && defined(__sun__) && defined(__GNUC__)
  #undef _Complex_I
  #define _Complex_I 1.0fj
#endif
""")

complex_real_imag_utility_code = UtilityCode(
proto="""
#if CYTHON_CCOMPLEX
  #ifdef __cplusplus
    #define __Pyx_CREAL(z) ((z).real())
    #define __Pyx_CIMAG(z) ((z).imag())
  #else
    #define __Pyx_CREAL(z) (__real__(z))
    #define __Pyx_CIMAG(z) (__imag__(z))
  #endif
#else
    #define __Pyx_CREAL(z) ((z).real)
    #define __Pyx_CIMAG(z) ((z).imag)
#endif

#if defined(_WIN32) && defined(__cplusplus) && CYTHON_CCOMPLEX
    #define __Pyx_SET_CREAL(z,x) ((z).real(x))
    #define __Pyx_SET_CIMAG(z,y) ((z).imag(y))
#else
    #define __Pyx_SET_CREAL(z,x) __Pyx_CREAL(z) = (x)
    #define __Pyx_SET_CIMAG(z,y) __Pyx_CIMAG(z) = (y)
#endif
""")

complex_type_utility_code = UtilityCode(
proto_block='complex_type_declarations',
proto="""
#if CYTHON_CCOMPLEX
  #ifdef __cplusplus
    typedef ::std::complex< %(real_type)s > %(type_name)s;
  #else
    typedef %(real_type)s _Complex %(type_name)s;
  #endif
#else
    typedef struct { %(real_type)s real, imag; } %(type_name)s;
#endif
""")

complex_from_parts_utility_code = UtilityCode(
proto_block='utility_code_proto',
proto="""
static CYTHON_INLINE %(type)s %(type_name)s_from_parts(%(real_type)s, %(real_type)s);
""",
impl="""
#if CYTHON_CCOMPLEX
  #ifdef __cplusplus
    static CYTHON_INLINE %(type)s %(type_name)s_from_parts(%(real_type)s x, %(real_type)s y) {
      return ::std::complex< %(real_type)s >(x, y);
    }
  #else
    static CYTHON_INLINE %(type)s %(type_name)s_from_parts(%(real_type)s x, %(real_type)s y) {
      return x + y*(%(type)s)_Complex_I;
    }
  #endif
#else
    static CYTHON_INLINE %(type)s %(type_name)s_from_parts(%(real_type)s x, %(real_type)s y) {
      %(type)s z;
      z.real = x;
      z.imag = y;
      return z;
    }
#endif
""")

complex_to_py_utility_code = UtilityCode(
proto="""
#define __pyx_PyComplex_FromComplex(z) \\
        PyComplex_FromDoubles((double)__Pyx_CREAL(z), \\
                              (double)__Pyx_CIMAG(z))
""")

complex_from_py_utility_code = UtilityCode(
proto="""
static %(type)s __Pyx_PyComplex_As_%(type_name)s(PyObject*);
""",
impl="""
static %(type)s __Pyx_PyComplex_As_%(type_name)s(PyObject* o) {
    Py_complex cval;
    if (PyComplex_CheckExact(o))
        cval = ((PyComplexObject *)o)->cval;
    else
        cval = PyComplex_AsCComplex(o);
    return %(type_name)s_from_parts(
               (%(real_type)s)cval.real,
               (%(real_type)s)cval.imag);
}
""")

complex_arithmetic_utility_code = UtilityCode(
proto="""
#if CYTHON_CCOMPLEX
    #define __Pyx_c_eq%(m)s(a, b)   ((a)==(b))
    #define __Pyx_c_sum%(m)s(a, b)  ((a)+(b))
    #define __Pyx_c_diff%(m)s(a, b) ((a)-(b))
    #define __Pyx_c_prod%(m)s(a, b) ((a)*(b))
    #define __Pyx_c_quot%(m)s(a, b) ((a)/(b))
    #define __Pyx_c_neg%(m)s(a)     (-(a))
  #ifdef __cplusplus
    #define __Pyx_c_is_zero%(m)s(z) ((z)==(%(real_type)s)0)
    #define __Pyx_c_conj%(m)s(z)    (::std::conj(z))
    #if %(is_float)s
        #define __Pyx_c_abs%(m)s(z)     (::std::abs(z))
        #define __Pyx_c_pow%(m)s(a, b)  (::std::pow(a, b))
    #endif
  #else
    #define __Pyx_c_is_zero%(m)s(z) ((z)==0)
    #define __Pyx_c_conj%(m)s(z)    (conj%(m)s(z))
    #if %(is_float)s
        #define __Pyx_c_abs%(m)s(z)     (cabs%(m)s(z))
        #define __Pyx_c_pow%(m)s(a, b)  (cpow%(m)s(a, b))
    #endif
 #endif
#else
    static CYTHON_INLINE int __Pyx_c_eq%(m)s(%(type)s, %(type)s);
    static CYTHON_INLINE %(type)s __Pyx_c_sum%(m)s(%(type)s, %(type)s);
    static CYTHON_INLINE %(type)s __Pyx_c_diff%(m)s(%(type)s, %(type)s);
    static CYTHON_INLINE %(type)s __Pyx_c_prod%(m)s(%(type)s, %(type)s);
    static CYTHON_INLINE %(type)s __Pyx_c_quot%(m)s(%(type)s, %(type)s);
    static CYTHON_INLINE %(type)s __Pyx_c_neg%(m)s(%(type)s);
    static CYTHON_INLINE int __Pyx_c_is_zero%(m)s(%(type)s);
    static CYTHON_INLINE %(type)s __Pyx_c_conj%(m)s(%(type)s);
    #if %(is_float)s
        static CYTHON_INLINE %(real_type)s __Pyx_c_abs%(m)s(%(type)s);
        static CYTHON_INLINE %(type)s __Pyx_c_pow%(m)s(%(type)s, %(type)s);
    #endif
#endif
""",
impl="""
#if CYTHON_CCOMPLEX
#else
    static CYTHON_INLINE int __Pyx_c_eq%(m)s(%(type)s a, %(type)s b) {
       return (a.real == b.real) && (a.imag == b.imag);
    }
    static CYTHON_INLINE %(type)s __Pyx_c_sum%(m)s(%(type)s a, %(type)s b) {
        %(type)s z;
        z.real = a.real + b.real;
        z.imag = a.imag + b.imag;
        return z;
    }
    static CYTHON_INLINE %(type)s __Pyx_c_diff%(m)s(%(type)s a, %(type)s b) {
        %(type)s z;
        z.real = a.real - b.real;
        z.imag = a.imag - b.imag;
        return z;
    }
    static CYTHON_INLINE %(type)s __Pyx_c_prod%(m)s(%(type)s a, %(type)s b) {
        %(type)s z;
        z.real = a.real * b.real - a.imag * b.imag;
        z.imag = a.real * b.imag + a.imag * b.real;
        return z;
    }
    static CYTHON_INLINE %(type)s __Pyx_c_quot%(m)s(%(type)s a, %(type)s b) {
        %(type)s z;
        %(real_type)s denom = b.real * b.real + b.imag * b.imag;
        z.real = (a.real * b.real + a.imag * b.imag) / denom;
        z.imag = (a.imag * b.real - a.real * b.imag) / denom;
        return z;
    }
    static CYTHON_INLINE %(type)s __Pyx_c_neg%(m)s(%(type)s a) {
        %(type)s z;
        z.real = -a.real;
        z.imag = -a.imag;
        return z;
    }
    static CYTHON_INLINE int __Pyx_c_is_zero%(m)s(%(type)s a) {
       return (a.real == 0) && (a.imag == 0);
    }
    static CYTHON_INLINE %(type)s __Pyx_c_conj%(m)s(%(type)s a) {
        %(type)s z;
        z.real =  a.real;
        z.imag = -a.imag;
        return z;
    }
    #if %(is_float)s
        static CYTHON_INLINE %(real_type)s __Pyx_c_abs%(m)s(%(type)s z) {
          #if !defined(HAVE_HYPOT) || defined(_MSC_VER)
            return sqrt%(m)s(z.real*z.real + z.imag*z.imag);
          #else
            return hypot%(m)s(z.real, z.imag);
          #endif
        }
        static CYTHON_INLINE %(type)s __Pyx_c_pow%(m)s(%(type)s a, %(type)s b) {
            %(type)s z;
            %(real_type)s r, lnr, theta, z_r, z_theta;
            if (b.imag == 0 && b.real == (int)b.real) {
                if (b.real < 0) {
                    %(real_type)s denom = a.real * a.real + a.imag * a.imag;
                    a.real = a.real / denom;
                    a.imag = -a.imag / denom;
                    b.real = -b.real;
                }
                switch ((int)b.real) {
                    case 0:
                        z.real = 1;
                        z.imag = 0;
                        return z;
                    case 1:
                        return a;
                    case 2:
                        z = __Pyx_c_prod%(m)s(a, a);
                        return __Pyx_c_prod%(m)s(a, a);
                    case 3:
                        z = __Pyx_c_prod%(m)s(a, a);
                        return __Pyx_c_prod%(m)s(z, a);
                    case 4:
                        z = __Pyx_c_prod%(m)s(a, a);
                        return __Pyx_c_prod%(m)s(z, z);
                }
            }
            if (a.imag == 0) {
                if (a.real == 0) {
                    return a;
                }
                r = a.real;
                theta = 0;
            } else {
                r = __Pyx_c_abs%(m)s(a);
                theta = atan2%(m)s(a.imag, a.real);
            }
            lnr = log%(m)s(r);
            z_r = exp%(m)s(lnr * b.real - theta * b.imag);
            z_theta = theta * b.real + lnr * b.imag;
            z.real = z_r * cos%(m)s(z_theta);
            z.imag = z_r * sin%(m)s(z_theta);
            return z;
        }
    #endif
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
    

class CReferenceType(BaseType):

    is_reference = 1

    def __init__(self, base_type):
        self.ref_base_type = base_type

    def __repr__(self):
        return "<CReferenceType %s>" % repr(self.ref_base_type)
    
    def __str__(self):
        return "%s &" % self.ref_base_type

    def as_argument_type(self):
        return self

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        #print "CReferenceType.declaration_code: pointer to", self.base_type ###
        return self.ref_base_type.declaration_code(
            "&%s" % entity_code,
            for_display, dll_linkage, pyrex)
    
    def specialize(self, values):
        base_type = self.ref_base_type.specialize(values)
        if base_type == self.ref_base_type:
            return self
        else:
            return CReferenceType(base_type)

    def __getattr__(self, name):
        return getattr(self.ref_base_type, name)


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
        if self.exception_value:
            except_clause = " %r" % self.exception_value
        else:
            except_clause = ""
        if self.exception_check:
            except_clause += "?"
        return "<CFuncType %s %s[%s]%s>" % (
            repr(self.return_type),
            self.calling_convention_prefix(),
            ",".join(arg_reprs),
            except_clause)
    
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
    
    def specialize(self, values):
        if self.templates is None:
            new_templates = None
        else:
            new_templates = [v.specialize(values) for v in self.templates]
        return CFuncType(self.return_type.specialize(values),
                             [arg.specialize(values) for arg in self.args],
                             has_varargs = 0,
                             exception_value = self.exception_value,
                             exception_check = self.exception_check,
                             calling_convention = self.calling_convention,
                             nogil = self.nogil,
                             with_gil = self.with_gil,
                             is_overridable = self.is_overridable,
                             optional_arg_count = self.optional_arg_count,
                             templates = new_templates)
    
    def opt_arg_cname(self, arg_name):
        return self.op_arg_struct.base_type.scope.lookup(arg_name).cname


class CFuncTypeArg(object):
    #  name       string
    #  cname      string
    #  type       PyrexType
    #  pos        source file position

    # FIXME: is this the right setup? should None be allowed here?
    not_none = False
    or_none = False
    accept_none = True

    def __init__(self, name, type, pos, cname=None):
        self.name = name
        if cname is not None:
            self.cname = cname
        else:
            self.cname = Naming.var_prefix + name
        self.type = type
        self.pos = pos
        self.needs_type_test = False # TODO: should these defaults be set in analyse_types()?
    
    def __repr__(self):
        return "%s:%s" % (self.name, repr(self.type))
    
    def declaration_code(self, for_display = 0):
        return self.type.declaration_code(self.cname, for_display)
    
    def specialize(self, values):
        return CFuncTypeArg(self.name, self.type.specialize(values), self.pos, self.cname)

class StructUtilityCode(object):
    def __init__(self, type, forward_decl):
        self.type = type
        self.header = "static PyObject* %s(%s)" % (type.to_py_function, type.declaration_code('s'))
        self.forward_decl = forward_decl

    def __eq__(self, other):
        return isinstance(other, StructUtilityCode) and self.header == other.header
    def __hash__(self):
        return hash(self.header)
    
    def put_code(self, output):
        code = output['utility_code_def']
        proto = output['utility_code_proto']
        
        code.putln("%s {" % self.header)
        code.putln("PyObject* res;")
        code.putln("PyObject* member;")
        code.putln("res = PyDict_New(); if (res == NULL) return NULL;")
        for member in self.type.scope.var_entries:
            nameconst_cname = code.get_py_string_const(member.name, identifier=True)
            code.putln("member = %s(s.%s); if (member == NULL) goto bad;" % (
                member.type.to_py_function, member.cname))
            code.putln("if (PyDict_SetItem(res, %s, member) < 0) goto bad;" % nameconst_cname)
            code.putln("Py_DECREF(member);")
        code.putln("return res;")
        code.putln("bad:")
        code.putln("Py_XDECREF(member);")
        code.putln("Py_DECREF(res);")
        code.putln("return NULL;")
        code.putln("}")

        # This is a bit of a hack, we need a forward declaration
        # due to the way things are ordered in the module...
        if self.forward_decl:
            proto.putln(self.type.declaration_code('') + ';')
        proto.putln(self.header + ";")
        

class CStructOrUnionType(CType):
    #  name          string
    #  cname         string
    #  kind          string              "struct" or "union"
    #  scope         StructOrUnionScope, or None if incomplete
    #  typedef_flag  boolean
    #  packed        boolean
    
    # entry          Entry
    
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

        if self._convert_code is False: return # tri-state-ish

        if self._convert_code is None:
            for member in self.scope.var_entries:
                if not member.type.to_py_function or not member.type.create_to_py_utility_code(env):
                    self.to_py_function = None
                    self._convert_code = False
                    return False
            forward_decl = (self.entry.visibility != 'extern')
            self._convert_code = StructUtilityCode(self, forward_decl)
        
        env.use_utility_code(self._convert_code)
        return True
        
    def __repr__(self):
        return "<CStructOrUnionType %s %s%s>" % (self.name, self.cname,
            ("", " typedef")[self.typedef_flag])

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex or for_display:
            base_code = self.name
        else:
            if self.typedef_flag:
                base_code = self.cname
            else:
                base_code = "%s %s" % (self.kind, self.cname)
            base_code = public_decl(base_code, dll_linkage)
        return self.base_declaration_code(base_code, entity_code)

    def __eq__(self, other):
        try:
            return (isinstance(other, CStructOrUnionType) and
                    self.name == other.name)
        except AttributeError:
            return False

    def __lt__(self, other):
        try:
            return self.name < other.name
        except AttributeError:
            # this is arbitrary, but it makes sure we always have
            # *some* kind of order
            return False

    def __hash__(self):
        return hash(self.cname) ^ hash(self.kind)

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
    namespace = None
    
    def __init__(self, name, scope, cname, base_classes, templates = None, template_type = None):
        self.name = name
        self.cname = cname
        self.scope = scope
        self.base_classes = base_classes
        self.operators = []
        self.templates = templates
        self.template_type = template_type
        self.specializations = {}

    def specialize_here(self, pos, template_values = None):
        if self.templates is None:
            error(pos, "'%s' type is not a template" % self);
            return PyrexTypes.error_type
        if len(self.templates) != len(template_values):
            error(pos, "%s templated type receives %d arguments, got %d" % 
                  (self.name, len(self.templates), len(template_values)))
            return error_type
        return self.specialize(dict(zip(self.templates, template_values)))
    
    def specialize(self, values):
        if not self.templates and not self.namespace:
            return self
        if self.templates is None:
            self.templates = []
        key = tuple(values.items())
        if key in self.specializations:
            return self.specializations[key]
        template_values = [t.specialize(values) for t in self.templates]
        specialized = self.specializations[key] = \
            CppClassType(self.name, None, self.cname, [], template_values, template_type=self)
        # Need to do these *after* self.specializations[key] is set
        # to avoid infinite recursion on circular references.
        specialized.base_classes = [b.specialize(values) for b in self.base_classes]
        specialized.scope = self.scope.specialize(values)
        if self.namespace is not None:
            specialized.namespace = self.namespace.specialize(values)
        return specialized

    def declaration_code(self, entity_code,
            for_display = 0, dll_linkage = None, pyrex = 0):
        if self.templates:
            template_strings = [param.declaration_code('', for_display, None, pyrex)
                                for param in self.templates]
            templates = "<%s>" % ",".join(template_strings)
            if templates[-2:] == ">>":
                templates = templates[:-2] + "> >"
        else:
            templates = ""
        if pyrex or for_display:
            base_code = "%s%s" % (self.name, templates)
        else:
            base_code = "%s%s" % (self.cname, templates)
            if self.namespace is not None:
                base_code = "%s::%s" % (self.namespace.declaration_code(''), base_code)
            base_code = public_decl(base_code, dll_linkage)
        return self.base_declaration_code(base_code, entity_code)

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
            elif self.template_type and self.template_type == other_type.template_type:
                if self.templates == other_type.templates:
                    return 1
                for t1, t2 in zip(self.templates, other_type.templates):
                    if not t1.same_as_resolved_type(t2):
                        return 0
                return 1
        return 0

    def assignable_from_resolved_type(self, other_type):
        # TODO: handle operator=(...) here?
        if other_type is error_type:
            return True
        return other_type.is_cpp_class and other_type.is_subclass(self)
    
    def attributes_known(self):
        return self.scope is not None


class TemplatePlaceholderType(CType):
    
    def __init__(self, name):
        self.name = name
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if entity_code:
            return self.name + " " + entity_code
        else:
            return self.name
    
    def specialize(self, values):
        if self in values:
            return values[self]
        else:
            return self

    def same_as_resolved_type(self, other_type):
        if isinstance(other_type, TemplatePlaceholderType):
            return self.name == other_type.name
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
        if pyrex or for_display:
            base_code = self.name
        else:
            if self.typedef_flag:
                base_code = self.cname
            else:
                base_code = "enum %s" % self.cname
            base_code = public_decl(base_code, dll_linkage)
        return self.base_declaration_code(base_code, entity_code)


class CStringType(object):
    #  Mixin class for C string types.

    is_string = 1
    is_unicode = 0
    
    to_py_function = "PyBytes_FromString"
    from_py_function = "PyBytes_AsString"
    exception_value = "NULL"

    def literal_code(self, value):
        assert isinstance(value, str)
        return '"%s"' % StringEncoding.escape_byte_string(value)


class CUTF8CharArrayType(CStringType, CArrayType):
    #  C 'char []' type.
    
    is_unicode = 1
    
    to_py_function = "PyUnicode_DecodeUTF8"
    exception_value = "NULL"
    
    def __init__(self, size):
        CArrayType.__init__(self, c_char_type, size)

class CCharArrayType(CStringType, CArrayType):
    #  C 'char []' type.
    
    def __init__(self, size):
        CArrayType.__init__(self, c_char_type, size)
    

class CCharPtrType(CStringType, CPtrType):
    # C 'char *' type.
    
    def __init__(self):
        CPtrType.__init__(self, c_char_type)


class CUCharPtrType(CStringType, CPtrType):
    # C 'unsigned char *' type.
    
    to_py_function = "__Pyx_PyBytes_FromUString"
    from_py_function = "__Pyx_PyBytes_AsUString"

    def __init__(self):
        CPtrType.__init__(self, c_uchar_type)


class UnspecifiedType(PyrexType):
    # Used as a placeholder until the type can be determined.
    
    is_unspecified = 1
        
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
    "PY_LONG_LONG", # 4
    "float",        # 5
    "double",       # 6
    "long double",  # 7
)

RANK_INT  = list(rank_to_type_name).index('int')
RANK_LONG = list(rank_to_type_name).index('long')
UNSIGNED = 0
SIGNED = 2


py_object_type = PyObjectType()

c_void_type =        CVoidType()

c_uchar_type =       CIntType(0, UNSIGNED)
c_ushort_type =      CIntType(1, UNSIGNED)
c_uint_type =        CIntType(2, UNSIGNED)
c_ulong_type =       CIntType(3, UNSIGNED)
c_ulonglong_type =   CIntType(4, UNSIGNED)

c_char_type =        CIntType(0)
c_short_type =       CIntType(1)
c_int_type =         CIntType(2)
c_long_type =        CIntType(3)
c_longlong_type =    CIntType(4)

c_schar_type =       CIntType(0, SIGNED)
c_sshort_type =      CIntType(1, SIGNED)
c_sint_type =        CIntType(2, SIGNED)
c_slong_type =       CIntType(3, SIGNED)
c_slonglong_type =   CIntType(4, SIGNED)

c_float_type =       CFloatType(5, math_h_modifier='f')
c_double_type =      CFloatType(6)
c_longdouble_type =  CFloatType(7, math_h_modifier='l')

c_float_complex_type =      CComplexType(c_float_type)
c_double_complex_type =     CComplexType(c_double_type)
c_longdouble_complex_type = CComplexType(c_longdouble_type)

c_anon_enum_type =   CAnonEnumType(-1)
c_returncode_type =  CReturnCodeType(RANK_INT)
c_bint_type =        CBIntType(RANK_INT)
c_py_unicode_type =  CPyUnicodeIntType(RANK_INT-0.5, UNSIGNED)
c_py_ucs4_type =     CPyUCS4IntType(RANK_LONG-0.5, UNSIGNED)
c_py_ssize_t_type =  CPySSizeTType(RANK_LONG+0.5, SIGNED)
c_ssize_t_type =     CSSizeTType(RANK_LONG+0.5, SIGNED)
c_size_t_type =      CSizeTType(RANK_LONG+0.5, UNSIGNED)

c_null_ptr_type =     CNullPtrType(c_void_type)
c_void_ptr_type =     CPtrType(c_void_type)
c_void_ptr_ptr_type = CPtrType(c_void_ptr_type)
c_char_array_type =   CCharArrayType(None)
c_char_ptr_type =     CCharPtrType()
c_uchar_ptr_type =    CUCharPtrType()
c_utf8_char_array_type = CUTF8CharArrayType(None)
c_char_ptr_ptr_type = CPtrType(c_char_ptr_type)
c_int_ptr_type =      CPtrType(c_int_type)
c_py_unicode_ptr_type = CPtrType(c_py_unicode_type)
c_py_ssize_t_ptr_type =  CPtrType(c_py_ssize_t_type)
c_ssize_t_ptr_type =  CPtrType(c_ssize_t_type)
c_size_t_ptr_type =  CPtrType(c_size_t_type)


# the Py_buffer type is defined in Builtin.py
c_py_buffer_type = CStructOrUnionType("Py_buffer", "struct", None, 1, "Py_buffer")
c_py_buffer_ptr_type = CPtrType(c_py_buffer_type)

error_type =    ErrorType()
unspecified_type = UnspecifiedType()

modifiers_and_name_to_type = {
    #(signed, longness, name) : type
    (0,  0, "char"): c_uchar_type,
    (1,  0, "char"): c_char_type,
    (2,  0, "char"): c_schar_type,

    (0, -1, "int"): c_ushort_type,
    (0,  0, "int"): c_uint_type,
    (0,  1, "int"): c_ulong_type,
    (0,  2, "int"): c_ulonglong_type,

    (1, -1, "int"): c_short_type,
    (1,  0, "int"): c_int_type,
    (1,  1, "int"): c_long_type,
    (1,  2, "int"): c_longlong_type,

    (2, -1, "int"): c_sshort_type,
    (2,  0, "int"): c_sint_type,
    (2,  1, "int"): c_slong_type,
    (2,  2, "int"): c_slonglong_type,

    (1,  0, "float"):  c_float_type,
    (1,  0, "double"): c_double_type,
    (1,  1, "double"): c_longdouble_type,

    (1,  0, "complex"):  c_double_complex_type,  # C: float, Python: double => Python wins
    (1,  0, "floatcomplex"):  c_float_complex_type,
    (1,  0, "doublecomplex"): c_double_complex_type,
    (1,  1, "doublecomplex"): c_longdouble_complex_type,

    #
    (1,  0, "void"): c_void_type,

    (1,  0, "bint"):       c_bint_type,
    (0,  0, "Py_UNICODE"): c_py_unicode_type,
    (0,  0, "Py_UCS4"):    c_py_ucs4_type,
    (2,  0, "Py_ssize_t"): c_py_ssize_t_type,
    (2,  0, "ssize_t") :   c_ssize_t_type,
    (0,  0, "size_t") :    c_size_t_type,

    (1,  0, "object"): py_object_type,
}

def is_promotion(src_type, dst_type):
    # It's hard to find a hard definition of promotion, but empirical
    # evidence suggests that the below is all that's allowed. 
    if src_type.is_numeric:
        if dst_type.same_as(c_int_type):
            unsigned = (not src_type.signed)
            return (src_type.is_enum or
                    (src_type.is_int and
                     unsigned + src_type.rank < dst_type.rank))
        elif dst_type.same_as(c_double_type):
            return src_type.is_float and src_type.rank <= dst_type.rank
    return False

def best_match(args, functions, pos=None):
    """
    Given a list args of arguments and a list of functions, choose one
    to call which seems to be the "best" fit for this list of arguments.
    This function is used, e.g., when deciding which overloaded method
    to dispatch for C++ classes.

    We first eliminate functions based on arity, and if only one
    function has the correct arity, we return it. Otherwise, we weight
    functions based on how much work must be done to convert the
    arguments, with the following priorities:
      * identical types or pointers to identical types
      * promotions 
      * non-Python types
    That is, we prefer functions where no arguments need converted,
    and failing that, functions where only promotions are required, and
    so on.

    If no function is deemed a good fit, or if two or more functions have
    the same weight, we return None (as there is no best match). If pos
    is not None, we also generate an error.
    """
    # TODO: args should be a list of types, not a list of Nodes. 
    actual_nargs = len(args)

    candidates = []
    errors = []
    for func in functions:
        error_mesg = ""
        func_type = func.type
        if func_type.is_ptr:
            func_type = func_type.base_type
        # Check function type
        if not func_type.is_cfunction:
            if not func_type.is_error and pos is not None:
                error_mesg = "Calling non-function type '%s'" % func_type
            errors.append((func, error_mesg))
            continue
        # Check no. of args
        max_nargs = len(func_type.args)
        min_nargs = max_nargs - func_type.optional_arg_count
        if actual_nargs < min_nargs or \
            (not func_type.has_varargs and actual_nargs > max_nargs):
            if max_nargs == min_nargs and not func_type.has_varargs:
                expectation = max_nargs
            elif actual_nargs < min_nargs:
                expectation = "at least %s" % min_nargs
            else:
                expectation = "at most %s" % max_nargs
            error_mesg = "Call with wrong number of arguments (expected %s, got %s)" \
                         % (expectation, actual_nargs)
            errors.append((func, error_mesg))
            continue
        candidates.append((func, func_type))
        
    # Optimize the most common case of no overloading...
    if len(candidates) == 1:
        return candidates[0][0]
    elif len(candidates) == 0:
        if pos is not None:
            if len(errors) == 1:
                error(pos, errors[0][1])
            else:
                error(pos, "no suitable method found")
        return None
        
    possibilities = []
    bad_types = []
    for func, func_type in candidates:
        score = [0,0,0]
        for i in range(min(len(args), len(func_type.args))):
            src_type = args[i].type
            dst_type = func_type.args[i].type
            if dst_type.assignable_from(src_type):
                if src_type == dst_type or dst_type.same_as(src_type):
                    pass # score 0
                elif is_promotion(src_type, dst_type):
                    score[2] += 1
                elif not src_type.is_pyobject:
                    score[1] += 1
                else:
                    score[0] += 1
            else:
                error_mesg = "Invalid conversion from '%s' to '%s'"%(src_type,
                                                                     dst_type)
                bad_types.append((func, error_mesg))
                break
        else:
            possibilities.append((score, func)) # so we can sort it
    if possibilities:
        possibilities.sort()
        if len(possibilities) > 1 and possibilities[0][0] == possibilities[1][0]:
            if pos is not None:
                error(pos, "ambiguous overloaded method")
            return None
        return possibilities[0][1]
    if pos is not None:
        if len(bad_types) == 1:
            error(pos, bad_types[0][1])
        else:
            error(pos, "no suitable method found")
    return None

def widest_numeric_type(type1, type2):
    # Given two numeric types, return the narrowest type
    # encompassing both of them.
    if type1 == type2:
        widest_type = type1
    elif type1.is_complex or type2.is_complex:
        def real_type(ntype):
            if ntype.is_complex:
                return ntype.real_type
            return ntype
        widest_type = CComplexType(
            widest_numeric_type(
                real_type(type1), 
                real_type(type2)))
    elif type1.is_enum and type2.is_enum:
        widest_type = c_int_type
    elif type1.rank < type2.rank:
        widest_type = type2
    elif type1.rank > type2.rank:
        widest_type = type1
    elif type1.signed < type2.signed:
        widest_type = type1
    else:
        widest_type = type2
    return widest_type

def independent_spanning_type(type1, type2):
    # Return a type assignable independently from both type1 and
    # type2, but do not require any interoperability between the two.
    # For example, in "True * 2", it is safe to assume an integer
    # result type (so spanning_type() will do the right thing),
    # whereas "x = True or 2" must evaluate to a type that can hold
    # both a boolean value and an integer, so this function works
    # better.
    if type1 == type2:
        return type1
    elif (type1 is c_bint_type or type2 is c_bint_type) and (type1.is_numeric and type2.is_numeric):
        # special case: if one of the results is a bint and the other
        # is another C integer, we must prevent returning a numeric
        # type so that we do not lose the ability to coerce to a
        # Python bool if we have to.
        return py_object_type
    span_type = _spanning_type(type1, type2)
    if span_type is None:
        return error_type
    return span_type

def spanning_type(type1, type2):
    # Return a type assignable from both type1 and type2, or
    # py_object_type if no better type is found.  Assumes that the
    # code that calls this will try a coercion afterwards, which will
    # fail if the types cannot actually coerce to a py_object_type.
    if type1 == type2:
        return type1
    elif type1 is py_object_type or type2 is py_object_type:
        return py_object_type
    elif type1 is c_py_unicode_type or type2 is c_py_unicode_type:
        # Py_UNICODE behaves more like a string than an int
        return py_object_type
    span_type = _spanning_type(type1, type2)
    if span_type is None:
        return py_object_type
    return span_type

def _spanning_type(type1, type2):
    if type1.is_numeric and type2.is_numeric:
        return widest_numeric_type(type1, type2)
    elif type1.is_builtin_type and type1.name == 'float' and type2.is_numeric:
        return widest_numeric_type(c_double_type, type2)
    elif type2.is_builtin_type and type2.name == 'float' and type1.is_numeric:
        return widest_numeric_type(type1, c_double_type)
    elif type1.is_extension_type and type2.is_extension_type:
        return widest_extension_type(type1, type2)
    elif type1.is_pyobject or type2.is_pyobject:
        return py_object_type
    elif type1.assignable_from(type2):
        if type1.is_extension_type and type1.typeobj_is_imported():
            # external types are unsafe, so we use PyObject instead
            return py_object_type
        return type1
    elif type2.assignable_from(type1):
        if type2.is_extension_type and type2.typeobj_is_imported():
            # external types are unsafe, so we use PyObject instead
            return py_object_type
        return type2
    else:
        return None

def widest_extension_type(type1, type2):
    if type1.typeobj_is_imported() or type2.typeobj_is_imported():
        return py_object_type
    while True:
        if type1.subtype_of(type2):
            return type2
        elif type2.subtype_of(type1):
            return type1
        type1, type2 = type1.base_type, type2.base_type
        if type1 is None or type2 is None:
            return py_object_type

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
    #
    basic_type = simple_c_type(1, 0, name)
    if basic_type:
        return basic_type
    #
    signed = 1
    longness = 0
    if name == 'Py_UNICODE':
        signed = 0
    elif name == 'Py_UCS4':
        signed = 0
    elif name == 'Py_ssize_t':
        signed = 2
    elif name == 'ssize_t':
        signed = 2
    elif name == 'size_t':
        signed = 0
    else:
        if name.startswith('u'):
            name = name[1:]
            signed = 0
        elif (name.startswith('s') and 
              not name.startswith('short')):
            name = name[1:]
            signed = 2
        longness = 0
        while name.startswith('short'):
            name = name.replace('short', '', 1).strip()
            longness -= 1
        while name.startswith('long'):
            name = name.replace('long', '', 1).strip()
            longness += 1
        if longness != 0 and not name:
            name = 'int'
    return simple_c_type(signed, longness, name)

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
    elif base_type is c_uchar_type:
        return c_uchar_ptr_type
    elif base_type is error_type:
        return error_type
    else:
        return CPtrType(base_type)

def c_ref_type(base_type):
    # Construct a C reference type
    if base_type is error_type:
        return error_type
    else:
        return CReferenceType(base_type)

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

#define __Pyx_PyBytes_FromUString(s) PyBytes_FromString((char*)s)
#define __Pyx_PyBytes_AsUString(s)   ((unsigned char*) PyBytes_AsString(s))

#define __Pyx_PyBool_FromLong(b) ((b) ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False))
static CYTHON_INLINE int __Pyx_PyObject_IsTrue(PyObject*);
static CYTHON_INLINE PyObject* __Pyx_PyNumber_Int(PyObject* x);

static CYTHON_INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject*);
static CYTHON_INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t);
static CYTHON_INLINE size_t __Pyx_PyInt_AsSize_t(PyObject*);

#define __pyx_PyFloat_AsDouble(x) (PyFloat_CheckExact(x) ? PyFloat_AS_DOUBLE(x) : PyFloat_AsDouble(x))

""" + type_conversion_predeclarations

# Note: __Pyx_PyObject_IsTrue is written to minimize branching.
type_conversion_functions = """
/* Type Conversion Functions */

static CYTHON_INLINE int __Pyx_PyObject_IsTrue(PyObject* x) {
   int is_true = x == Py_True;
   if (is_true | (x == Py_False) | (x == Py_None)) return is_true;
   else return PyObject_IsTrue(x);
}

static CYTHON_INLINE PyObject* __Pyx_PyNumber_Int(PyObject* x) {
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

static CYTHON_INLINE Py_ssize_t __Pyx_PyIndex_AsSsize_t(PyObject* b) {
  Py_ssize_t ival;
  PyObject* x = PyNumber_Index(b);
  if (!x) return -1;
  ival = PyInt_AsSsize_t(x);
  Py_DECREF(x);
  return ival;
}

static CYTHON_INLINE PyObject * __Pyx_PyInt_FromSize_t(size_t ival) {
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

static CYTHON_INLINE size_t __Pyx_PyInt_AsSize_t(PyObject* x) {
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

