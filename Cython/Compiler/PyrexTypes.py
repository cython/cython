#
#   Pyrex - Types
#

from Cython.Utils import UtilityCode
import StringEncoding
import Naming
import copy

class BaseType:
    #
    #  Base class for all Pyrex types including pseudo-types.

    def cast_code(self, expr_code):
        return "((%s)%s)" % (self.declaration_code(""), expr_code)
    
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
    #  parsetuple_format     string      Format char for PyArg_ParseTuple
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
    is_void = 0
    is_array = 0
    is_ptr = 0
    is_null_ptr = 0
    is_cfunction = 0
    is_struct_or_union = 0
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
    parsetuple_format = ""
    pymemberdef_typecode = None
    
    def resolve(self):
        # If a typedef, returns the base type.
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
        return (self.is_int or self.is_float or self.is_pyobject or
                self.is_extension_type or self.is_ptr)

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
    
    is_typedef = 1
    
    def __init__(self, cname, base_type):
        self.typedef_cname = cname
        self.typedef_base_type = base_type
    
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

    
class PyObjectType(PyrexType):
    #
    #  Base class for all Python object types (reference-counted).
    #
    #  buffer_defaults  dict or None     Default options for bu
    
    is_pyobject = 1
    default_value = "0"
    parsetuple_format = "O"
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


class BuiltinObjectType(PyObjectType):

    is_builtin_type = 1
    has_attributes = 1
    base_type = None
    module_name = '__builtin__'

    def __init__(self, name, cname):
        self.name = name
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
            return src_type.name == self.name
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
            type_name = 'String'
        elif type_name == 'set':
            type_name = 'AnySet'
        elif type_name == 'frozenset':
            type_name = 'FrozenSet'
        else:
            type_name = type_name.capitalize()
        return 'likely(Py%s_CheckExact(%s)) || (%s) == Py_None || (PyErr_Format(PyExc_TypeError, "Expected %s, got %%s", Py_TYPE(%s)->tp_name), 0)' % (type_name, arg, arg, self.name, arg)

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

    def create_convert_utility_code(self, env):
        return True
        
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
    
    parsetuple_formats = ( # rank -> format
        "BHIkK????", # unsigned
        "bhilL?fd?", # assumed signed
        "bhilL?fd?", # explicitly signed
    )
    
    sign_words = ("unsigned ", "", "signed ")
    
    def __init__(self, rank, signed = 1, pymemberdef_typecode = None):
        self.rank = rank
        self.signed = signed
        ptf = self.parsetuple_formats[signed][rank]
        if ptf == '?':
            ptf = None
        self.parsetuple_format = ptf
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


int_conversion_list = {}
type_conversion_functions = ""
type_conversion_predeclarations = ""

class CIntType(CNumericType):
    
    is_int = 1
    typedef_flag = 0
    to_py_function = "PyInt_FromLong"
    from_py_function = "__pyx_PyInt_AsLong"
    exception_value = -1

    def __init__(self, rank, signed, pymemberdef_typecode = None, is_returncode = 0):
        CNumericType.__init__(self, rank, signed, pymemberdef_typecode)
        self.is_returncode = is_returncode
        if self.from_py_function == '__pyx_PyInt_AsLong':
            self.from_py_function = self.get_type_conversion()

    def get_type_conversion(self):
        # error on overflow
        c_type = self.sign_and_name()
        c_name = c_type.replace(' ', '_');
        func_name = "__pyx_PyInt_%s" % c_name;
        if not int_conversion_list.has_key(func_name):
            # no env to add utility code to
            global type_conversion_predeclarations, type_conversion_functions
            if self.signed:
                neg_test = ""
            else:
                neg_test = " || (long_val < 0)"
            type_conversion_predeclarations += """
static INLINE %(c_type)s %(func_name)s(PyObject* x);""" % {'c_type': c_type, 'c_name': c_name, 'func_name': func_name }
            type_conversion_functions +=  """
static INLINE %(c_type)s %(func_name)s(PyObject* x) {
    if (sizeof(%(c_type)s) < sizeof(long)) {
        long long_val = __pyx_PyInt_AsLong(x);
        %(c_type)s val = (%(c_type)s)long_val;
        if (unlikely((val != long_val) %(neg_test)s)) {
            PyErr_SetString(PyExc_OverflowError, "value too large to convert to %(c_type)s");
            return (%(c_type)s)-1;
        }
        return val;
    }
    else {
        return __pyx_PyInt_AsLong(x);
    }
}
""" % {'c_type': c_type, 'c_name': c_name, 'func_name': func_name, 'neg_test': neg_test }
            int_conversion_list[func_name] = True
        return func_name
    
    def assignable_from_resolved_type(self, src_type):
        return src_type.is_int or src_type.is_enum or src_type is error_type


class CBIntType(CIntType):

    to_py_function = "__Pyx_PyBool_FromLong"
    from_py_function = "__Pyx_PyObject_IsTrue"
    exception_check = 0


class CAnonEnumType(CIntType):

    is_enum = 1	


class CUIntType(CIntType):

    to_py_function = "PyLong_FromUnsignedLong"
    from_py_function = "PyInt_AsUnsignedLongMask"
    exception_value = -1


class CULongType(CUIntType):

    to_py_function = "PyLong_FromUnsignedLong"
    from_py_function = "PyInt_AsUnsignedLongMask"


class CLongLongType(CIntType):

    is_longlong = 1
    to_py_function = "PyLong_FromLongLong"
    from_py_function = "__pyx_PyInt_AsLongLong"


class CULongLongType(CUIntType):

    is_longlong = 1
    to_py_function = "PyLong_FromUnsignedLongLong"
    from_py_function = "__pyx_PyInt_AsUnsignedLongLong"


class CPySSizeTType(CIntType):

    to_py_function = "PyInt_FromSsize_t"
    from_py_function = "__pyx_PyIndex_AsSsize_t"


class CFloatType(CNumericType):

    is_float = 1
    to_py_function = "PyFloat_FromDouble"
    from_py_function = "__pyx_PyFloat_AsDouble"
    
    def __init__(self, rank, pymemberdef_typecode = None):
        CNumericType.__init__(self, rank, 1, pymemberdef_typecode)
    
    def assignable_from_resolved_type(self, src_type):
        return src_type.is_numeric or src_type is error_type


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
        if other_type.is_array or other_type.is_ptr:
            return self.base_type.is_void or self.base_type.same_as(other_type.base_type)
        return 0


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
    
    is_cfunction = 1
    original_sig = None
    
    def __init__(self, return_type, args, has_varargs = 0,
            exception_value = None, exception_check = 0, calling_convention = "",
            nogil = 0, with_gil = 0, is_overridable = 0, optional_arg_count = 0):
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
        #	self, other_type, "as_cmethod =", as_cmethod ###
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
        #	self, other_type, "as_cmethod =", as_cmethod ###
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
            for_display = 0, dll_linkage = None, pyrex = 0):
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


class CFuncTypeArg:
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
    
    is_struct_or_union = 1
    has_attributes = 1
    
    def __init__(self, name, kind, scope, typedef_flag, cname):
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
        
    def create_convert_utility_code(self, env):
        if env.outer_scope is None:
            return False
        if self._convert_code is None:
            import Code
            code = Code.CCodeWriter()
            header = "static PyObject* %s(%s)" % (self.to_py_function, self.declaration_code('s'))
            code.putln("%s {" % header)
            code.putln("PyObject* res;")
            code.putln("PyObject* member;")
            code.putln("res = PyDict_New(); if (res == NULL) return NULL;")
            for member in self.scope.var_entries:
                if member.type.to_py_function and member.type.create_convert_utility_code(env):
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
        # Does the struct consist of exactly two floats?
        fields = self.scope.var_entries
        return len(fields) == 2 and fields[0].type.is_float and fields[1].type.is_float


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


class CStringType:
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
    
    parsetuple_format = "s"
    pymemberdef_typecode = "T_STRING_INPLACE"
    is_unicode = 1
    
    to_py_function = "PyUnicode_DecodeUTF8"
    exception_value = "NULL"
    
    def __init__(self, size):
        CArrayType.__init__(self, c_char_type, size)

class CCharArrayType(CStringType, CArrayType):
    #  C 'char []' type.
    
    parsetuple_format = "s"
    pymemberdef_typecode = "T_STRING_INPLACE"
    
    def __init__(self, size):
        CArrayType.__init__(self, c_char_type, size)
    

class CCharPtrType(CStringType, CPtrType):
    # C 'char *' type.
    
    parsetuple_format = "s"
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
    exception_check	= 0
    to_py_function = "dummy"
    from_py_function = "dummy"
    
    def create_convert_utility_code(self, env):
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
    "Py_ssize_t",   # 5
    "float",        # 6
    "double",       # 7
    "long double",  # 8
)

py_object_type = PyObjectType()

c_void_type =         CVoidType()
c_void_ptr_type =     CPtrType(c_void_type)
c_void_ptr_ptr_type = CPtrType(c_void_ptr_type)

c_uchar_type =       CIntType(0, 0, "T_UBYTE")
c_ushort_type =      CIntType(1, 0, "T_USHORT")
c_uint_type =        CUIntType(2, 0, "T_UINT")
c_ulong_type =       CULongType(3, 0, "T_ULONG")
c_ulonglong_type =   CULongLongType(4, 0, "T_ULONGLONG")

c_char_type =        CIntType(0, 1, "T_CHAR")
c_short_type =       CIntType(1, 1, "T_SHORT")
c_int_type =         CIntType(2, 1, "T_INT")
c_long_type =        CIntType(3, 1, "T_LONG")
c_longlong_type =    CLongLongType(4, 1, "T_LONGLONG")
c_py_ssize_t_type =  CPySSizeTType(5, 1)
c_bint_type =        CBIntType(2, 1, "T_INT")

c_schar_type =       CIntType(0, 2, "T_CHAR")
c_sshort_type =      CIntType(1, 2, "T_SHORT")
c_sint_type =        CIntType(2, 2, "T_INT")
c_slong_type =       CIntType(3, 2, "T_LONG")
c_slonglong_type =   CLongLongType(4, 2, "T_LONGLONG")

c_float_type =       CFloatType(6, "T_FLOAT")
c_double_type =      CFloatType(7, "T_DOUBLE")
c_longdouble_type =  CFloatType(8)

c_null_ptr_type =     CNullPtrType(c_void_type)
c_char_array_type =   CCharArrayType(None)
c_char_ptr_type =     CCharPtrType()
c_utf8_char_array_type = CUTF8CharArrayType(None)
c_char_ptr_ptr_type = CPtrType(c_char_ptr_type)
c_py_ssize_t_ptr_type =  CPtrType(c_py_ssize_t_type)
c_int_ptr_type =      CPtrType(c_int_type)

c_returncode_type =   CIntType(2, 1, "T_INT", is_returncode = 1)

c_anon_enum_type =    CAnonEnumType(-1, 1)

# the Py_buffer type is defined in Builtin.py
c_py_buffer_type = CStructOrUnionType("Py_buffer", "struct", None, 1, "Py_buffer")
c_py_buffer_ptr_type = CPtrType(c_py_buffer_type)

error_type =    ErrorType()
unspecified_type = UnspecifiedType()

lowest_float_rank = 6

sign_and_rank_to_type = {
    #(signed, rank)
    (0, 0, ): c_uchar_type, 
    (0, 1): c_ushort_type, 
    (0, 2): c_uint_type, 
  (0, 3): c_ulong_type,
  (0, 4): c_ulonglong_type,
    (0, 5):  c_ulonglong_type,            # I'm not sure about this.  this should be for size_t Py_ssize_t
    (1, 0): c_char_type, 
    (1, 1): c_short_type, 
    (1, 2): c_int_type, 
    (1, 3): c_long_type,
    (1, 4): c_longlong_type,
    (1, 5): c_py_ssize_t_type,
    (2, 0): c_schar_type, 
    (2, 1): c_sshort_type, 
    (2, 2): c_sint_type, 
    (2, 3): c_slong_type,
    (2, 4): c_slonglong_type,
    (2, 5): c_py_ssize_t_type,
    (1, 6): c_float_type, 
    (1, 7): c_double_type,
    (1, 8): c_longdouble_type,
# In case we're mixing unsigned ints and floats...
    (0, 6): c_float_type, 
    (0, 7): c_double_type,
    (0, 8): c_longdouble_type,
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
    (1, 0, "Py_ssize_t"): c_py_ssize_t_type,
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
    
    (1, 0, "long"): c_long_type,
    (1, 0, "short"): c_short_type,
    (1, 0, "longlong"): c_longlong_type,
    (1, 0, "bint"): c_bint_type,
}

def widest_numeric_type(type1, type2):
    # Given two numeric types, return the narrowest type
    # encompassing both of them.
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

def public_decl(base, dll_linkage):
    if dll_linkage:
        return "%s(%s)" % (dll_linkage, base)
    else:
        return base

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
#define __Pyx_PyBytes_FromString PyString_FromString
#define __Pyx_PyBytes_AsString   PyString_AsString
#else
#define __Pyx_PyBytes_FromString PyBytes_FromString
#define __Pyx_PyBytes_AsString   PyBytes_AsString
#endif

#define __Pyx_PyBool_FromLong(b) ((b) ? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False))
static INLINE int __Pyx_PyObject_IsTrue(PyObject* x);
static INLINE PY_LONG_LONG __pyx_PyInt_AsLongLong(PyObject* x);
static INLINE unsigned PY_LONG_LONG __pyx_PyInt_AsUnsignedLongLong(PyObject* x);
static INLINE Py_ssize_t __pyx_PyIndex_AsSsize_t(PyObject* b);

#define __pyx_PyInt_AsLong(x) (PyInt_CheckExact(x) ? PyInt_AS_LONG(x) : PyInt_AsLong(x))
#define __pyx_PyFloat_AsDouble(x) (PyFloat_CheckExact(x) ? PyFloat_AS_DOUBLE(x) : PyFloat_AsDouble(x))
""" + type_conversion_predeclarations

type_conversion_functions = """
/* Type Conversion Functions */

static INLINE Py_ssize_t __pyx_PyIndex_AsSsize_t(PyObject* b) {
  Py_ssize_t ival;
  PyObject* x = PyNumber_Index(b);
  if (!x) return -1;
  ival = PyInt_AsSsize_t(x);
  Py_DECREF(x);
  return ival;
}

static INLINE int __Pyx_PyObject_IsTrue(PyObject* x) {
   if (x == Py_True) return 1;
   else if (x == Py_False) return 0;
   else return PyObject_IsTrue(x);
}

static INLINE PY_LONG_LONG __pyx_PyInt_AsLongLong(PyObject* x) {
    if (PyInt_CheckExact(x)) {
        return PyInt_AS_LONG(x);
    }
    else if (PyLong_CheckExact(x)) {
        return PyLong_AsLongLong(x);
    }
    else {
        PY_LONG_LONG val;
        PyObject* tmp = PyNumber_Int(x); if (!tmp) return (PY_LONG_LONG)-1;
        val = __pyx_PyInt_AsLongLong(tmp);
        Py_DECREF(tmp);
        return val;
    }
}

static INLINE unsigned PY_LONG_LONG __pyx_PyInt_AsUnsignedLongLong(PyObject* x) {
    if (PyInt_CheckExact(x)) {
        long val = PyInt_AS_LONG(x);
        if (unlikely(val < 0)) {
            PyErr_SetString(PyExc_TypeError, "Negative assignment to unsigned type.");
            return (unsigned PY_LONG_LONG)-1;
        }
        return val;
    }
    else if (PyLong_CheckExact(x)) {
        return PyLong_AsUnsignedLongLong(x);
    }
    else {
        PY_LONG_LONG val;
        PyObject* tmp = PyNumber_Int(x); if (!tmp) return (PY_LONG_LONG)-1;
        val = __pyx_PyInt_AsUnsignedLongLong(tmp);
        Py_DECREF(tmp);
        return val;
    }
}

""" + type_conversion_functions
