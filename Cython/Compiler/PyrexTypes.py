#
#   Pyrex - Types
#

import string
import Naming

class PyrexType:
    #
    #  Base class for all Pyrex types.
    #
    #  is_pyobject           boolean     Is a Python object type
    #  is_extension_type     boolean     Is a Python extension type
    #  is_numeric            boolean     Is a C numeric type
    #  is_int                boolean     Is a C integer type
    #  is_float              boolean     Is a C floating point type
    #  is_void               boolean     Is the C void type
    #  is_array              boolean     Is a C array type
    #  is_ptr                boolean     Is a C pointer type
    #  is_null_ptr           boolean     Is the type of NULL
    #  is_cfunction          boolean     Is a C function type
    #  is_struct_or_union    boolean     Is a C struct or union type
    #  is_enum               boolean     Is a C enum type
    #  is_string             boolean     Is a C char * type
    #  is_returncode         boolean     Is used only to signal exceptions
    #  is_error              boolean     Is the dummy error type
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
    is_numeric = 0
    is_int = 0
    is_float = 0
    is_void = 0
    is_array = 0
    is_ptr = 0
    is_null_ptr = 0
    is_cfunction = 0
    is_struct_or_union = 0
    is_enum = 0
    is_string = 0
    is_returncode = 0
    is_error = 0
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
        return string.strip(self.declaration_code("", for_display = 1))
    
    def same_as(self, other_type, **kwds):
        return self.same_as_resolved_type(other_type.resolve(), **kwds)
    
    def same_as_resolved_type(self, other_type):
        return self is other_type or other_type is error_type
    
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
    
    def cast_code(self, expr_code):
        return "((%s)%s)" % (self.declaration_code(""), expr_code)


class CTypedefType:
    #
    #  Type defined with a ctypedef statement in a
    #  'cdef extern from' block. Delegates most attribute
    #  lookups to the base type.
    #
    
    def __init__(self, cname, base_type):
        self.typedef_cname = cname
        self.typedef_base_type = base_type
    
    def resolve(self):
        return self.typedef_base_type.resolve()
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        return "%s %s" % (self.typedef_cname, entity_code)
    
    def __str__(self):
        return self.typedef_cname
    
    def __getattr__(self, name):
        return getattr(self.typedef_base_type, name)


class PyObjectType(PyrexType):
    #
    #  Base class for all Python object types (reference-counted).
    #
    
    is_pyobject = 1
    default_value = "0"
    parsetuple_format = "O"
    pymemberdef_typecode = "T_OBJECT"
    
    def __str__(self):
        return "Python object"
    
    def __repr__(self):
        return "PyObjectType"
    
    def assignable_from(self, src_type):
        return 1 # Conversion will be attempted
        
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex:
            return "object %s" % entity_code
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
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex:
            return "%s %s" % (self.name, entity_code)
        else:
            if self.typedef_flag:
                base_format = "%s"
            else:
                base_format = "struct %s"
            base = public_decl(base_format % self.objstruct_cname, dll_linkage)
            return "%s *%s" % (base,  entity_code)

    def attributes_known(self):
        return self.scope is not None
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "PyExtensionType(%s%s)" % (self.scope.class_name,
            ("", ".typedef_flag=1")[self.typedef_flag])
    

class CType(PyrexType):
    #
    #  Base class for all C types (non-reference-counted).
    #
    #  to_py_function     string     C function for converting to Python object
    #  from_py_function   string     C function for constructing from Python object
    #
    
    to_py_function = None
    from_py_function = None


#class CSimpleType(CType):
#	#
#	#  Base class for all unstructured C types.
#	#
#	pass


class CVoidType(CType):
    is_void = 1
    
    def __repr__(self):
        return "<CVoidType>"
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        base = public_decl("void", dll_linkage)
        return "%s %s" % (base, entity_code)
    
    def is_complete(self):
        return 0


class CNumericType(CType):
    #
    #   Base class for all C numeric types.
    #
    #   rank      integer     Relative size
    #   signed    boolean
    #
    
    is_numeric = 1
    default_value = "0"
    
    parsetuple_formats = ( # rank -> format
        "?HIkK???", # unsigned
        "chilLfd?", # signed
    )
    
    def __init__(self, rank, signed = 1, pymemberdef_typecode = None):
        self.rank = rank
        self.signed = signed
        ptf = self.parsetuple_formats[signed][rank]
        if ptf == '?':
            ptf = None
        self.parsetuple_format = ptf
        self.pymemberdef_typecode = pymemberdef_typecode
    
    def __repr__(self):
        if self.signed:
            u = ""
        else:
            u = "unsigned "
        return "<CNumericType %s%s>" % (u, rank_to_type_name[self.rank])
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if self.signed:
            u = ""
        else:
            u = "unsigned "
        base = public_decl(u + rank_to_type_name[self.rank], dll_linkage)
        return "%s %s" % (base,  entity_code)
    

class CIntType(CNumericType):
    
    is_int = 1
    typedef_flag = 0
    to_py_function = "PyInt_FromLong"
    from_py_function = "PyInt_AsLong"

    def __init__(self, rank, signed, pymemberdef_typecode = None, is_returncode = 0):
        CNumericType.__init__(self, rank, signed, pymemberdef_typecode)
        self.is_returncode = is_returncode
    
    def assignable_from_resolved_type(self, src_type):
        return src_type.is_int or src_type.is_enum or src_type is error_type


class CUIntType(CIntType):

    to_py_function = "PyLong_FromUnsignedLong"
    from_py_function = "PyInt_AsUnsignedLongMask"


class CULongType(CIntType):

    to_py_function = "PyLong_FromUnsignedLong"
    from_py_function = "PyInt_AsUnsignedLongMask"


class CLongLongType(CIntType):

    to_py_function = "PyLong_FromLongLong"
    from_py_function = "PyInt_AsUnsignedLongLongMask"


class CULongLongType(CIntType):

    to_py_function = "PyLong_FromUnsignedLongLong"
    from_py_function = "PyInt_AsUnsignedLongLongMask"


class CFloatType(CNumericType):

    is_float = 1
    to_py_function = "PyFloat_FromDouble"
    from_py_function = "PyFloat_AsDouble"
    
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
        return "CArrayType(%s,%s)" % (self.size, repr(self.base_type))
    
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
        return self.base_type.declaration_code(
            "(%s[%s])" % (entity_code, dimension_code),
            for_display, dll_linkage, pyrex)
    
    def as_argument_type(self):
        return c_ptr_type(self.base_type)
    
    def is_complete(self):
        return self.size is not None


class CPtrType(CType):
    #  base_type     CType    Referenced type
    
    is_ptr = 1
    default_value = 0
    
    def __init__(self, base_type):
        self.base_type = base_type
    
    def __repr__(self):
        return "CPtrType(%s)" % repr(self.base_type)
    
    def same_as_resolved_type(self, other_type):
        return ((other_type.is_ptr and
            self.base_type.same_as(other_type.base_type))
                or other_type is error_type)
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        #print "CPtrType.declaration_code: pointer to", self.base_type ###
        return self.base_type.declaration_code(
            "(*%s)" % entity_code,
            for_display, dll_linkage, pyrex)
    
    def assignable_from_resolved_type(self, other_type):
        if other_type is error_type:
            return 1
        elif self.base_type.is_cfunction and other_type.is_cfunction:
            return self.base_type.same_as(other_type)
        elif other_type.is_array:
            return self.base_type.same_as(other_type.base_type)
        elif not other_type.is_ptr:
            return 0
        elif self.base_type.is_void:
            return 1
        elif other_type.is_null_ptr:
            return 1
        else:
            return self.base_type.same_as(other_type.base_type)


class CNullPtrType(CPtrType):

    is_null_ptr = 1
    

class CFuncType(CType):
    #  return_type      CType
    #  args             [CFuncTypeArg]
    #  has_varargs      boolean
    #  exception_value  string
    #  exception_check  boolean  True if PyErr_Occurred check needed
    
    is_cfunction = 1
    
    def __init__(self, return_type, args, has_varargs,
            exception_value = None, exception_check = 0):
        self.return_type = return_type
        self.args = args
        self.has_varargs = has_varargs
        self.exception_value = exception_value
        self.exception_check = exception_check
    
    def __repr__(self):
        arg_reprs = map(repr, self.args)
        if self.has_varargs:
            arg_reprs.append("...")
        return "CFuncType(%s,[%s])" % (
            repr(self.return_type),
            string.join(arg_reprs, ","))
    
    def same_c_signature_as(self, other_type, as_cmethod = 0):
        return self.same_c_signature_as_resolved_type(
            other_type.resolve(), as_cmethod)

    def same_c_signature_as_resolved_type(self, other_type, as_cmethod):
        if other_type is error_type:
            return 1
        if not other_type.is_cfunction:
            return 0
        nargs = len(self.args)
        if nargs <> len(other_type.args):
            return 0
        # When comparing C method signatures, the first argument
        # is exempt from compatibility checking (the proper check
        # is performed elsewhere).
        for i in range(as_cmethod, nargs):
            if not self.args[i].type.same_as(
                other_type.args[i].type):
                    return 0
        if self.has_varargs <> other_type.has_varargs:
            return 0
        if not self.return_type.same_as(other_type.return_type):
            return 0
        return 1
    
    def same_exception_signature_as(self, other_type):
        return self.same_exception_signature_as_resolved_type(
            other_type.resolve())

    def same_exception_signature_as_resolved_type(self, other_type):
        return self.exception_value == other_type.exception_value \
            and self.exception_check == other_type.exception_check
    
    def same_as_resolved_type(self, other_type, as_cmethod = 0):
        return self.same_c_signature_as_resolved_type(other_type, as_cmethod) \
            and self.same_exception_signature_as_resolved_type(other_type)
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        arg_decl_list = []
        for arg in self.args:
            arg_decl_list.append(
                arg.type.declaration_code("", for_display, pyrex = pyrex))
        if self.has_varargs:
            arg_decl_list.append("...")
        arg_decl_code = string.join(arg_decl_list, ",")
        if not arg_decl_code and not pyrex:
            arg_decl_code = "void"
        exc_clause = ""
        if pyrex or for_display:
            if self.exception_value and self.exception_check:
                exc_clause = " except? %s" % self.exception_value
            elif self.exception_value:
                exc_clause = " except %s" % self.exception_value
            elif self.exception_check:
                exc_clause = " except *"
        return self.return_type.declaration_code(
            "(%s(%s)%s)" % (entity_code, arg_decl_code, exc_clause),
            for_display, dll_linkage, pyrex)


class CFuncTypeArg:
    #  name       string
    #  cname      string
    #  type       PyrexType
    #  pos        source file position
    
    def __init__(self, name, type, pos):
        self.name = name
        self.cname = Naming.var_prefix + name
        self.type = type
        self.pos = pos
    
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
        
    def __repr__(self):
        return "CStructOrUnionType(%s,%s%s)" % (self.name, self.cname,
            ("", ",typedef_flag=1")[self.typedef_flag])

    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex:
            return "%s %s" % (self.name, entity_code)
        else:
            if for_display:
                base = self.name
            elif self.typedef_flag:
                base = self.cname
            else:
                base = "%s %s" % (self.kind, self.cname)
            return "%s %s" % (public_decl(base, dll_linkage), entity_code)

    def is_complete(self):
        return self.scope is not None
    
    def attributes_known(self):
        return self.is_complete()


class CEnumType(CType):
    #  name           string
    #  cname          string or None
    #  typedef_flag   boolean
    
    is_enum = 1
    #signed = 1
    #rank = 2
    to_py_function = "PyInt_FromLong"
    from_py_function = "PyInt_AsLong"

    def __init__(self, name, cname, typedef_flag):
        self.name = name
        self.cname = cname
        self.values = []
        self.typedef_flag = typedef_flag
    
    def __repr__(self):
        return "CEnumType(%s,%s%s)" % (self.name, self.cname,
            ("", ",typedef_flag=1")[self.typedef_flag])
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        if pyrex:
            return "%s %s" % (self.cname, entity_code)
        else:
            if self.typedef_flag:
                base = self.cname
            else:
                base = "enum %s" % self.cname
            return "%s %s" % (public_decl(base, dll_linkage), entity_code)


class CStringType:
    #  Mixin class for C string types.

    is_string = 1
    
    to_py_function = "PyString_FromString"
    from_py_function = "PyString_AsString"

    def literal_code(self, value):
        return '"%s"' % value


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


class ErrorType(PyrexType):
    # Used to prevent propagation of error messages.
    
    is_error = 1
    exception_value = "0"
    exception_check	= 0
    to_py_function = "dummy"
    from_py_function = "dummy"
    
    def declaration_code(self, entity_code, 
            for_display = 0, dll_linkage = None, pyrex = 0):
        return "<error>"
    
    def same_as_resolved_type(self, other_type):
        return 1


py_object_type = PyObjectType()

c_void_type =         CVoidType()
c_void_ptr_type =     CPtrType(c_void_type)
c_void_ptr_ptr_type = CPtrType(c_void_ptr_type)

c_char_type =     CIntType(0, 1, "T_CHAR")
c_short_type =    CIntType(1, 1, "T_SHORT")
c_int_type =      CIntType(2, 1, "T_INT")
c_long_type =     CIntType(3, 1, "T_LONG")
c_longlong_type = CLongLongType(4, 1, "T_LONGLONG")

c_uchar_type =     CIntType(0, 0, "T_UBYTE")
c_ushort_type =    CIntType(1, 0, "T_USHORT")
c_uint_type =      CUIntType(2, 0, "T_UINT")
c_ulong_type =     CULongType(3, 0, "T_ULONG")
c_ulonglong_type = CULongLongType(4, 0, "T_ULONGLONG")

c_float_type =      CFloatType(5, "T_FLOAT")
c_double_type =     CFloatType(6, "T_DOUBLE")
c_longdouble_type = CFloatType(7)

c_null_ptr_type =     CNullPtrType(c_void_type)
c_char_array_type =   CCharArrayType(None)
c_char_ptr_type =     CCharPtrType()
c_char_ptr_ptr_type = CPtrType(c_char_ptr_type)
c_int_ptr_type =      CPtrType(c_int_type)

c_returncode_type =   CIntType(2, 1, "T_INT", is_returncode = 1)

error_type =    ErrorType()

lowest_float_rank = 5

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

sign_and_rank_to_type = {
    #(signed, rank)
    (0, 0, ): c_uchar_type, 
    (0, 1): c_ushort_type, 
    (0, 2): c_uint_type, 
  (0, 3): c_ulong_type,
  (0, 4): c_ulonglong_type,
    (1, 0): c_char_type, 
    (1, 1): c_short_type, 
    (1, 2): c_int_type, 
    (1, 3): c_long_type,
    (1, 4): c_longlong_type,
    (1, 5): c_float_type, 
    (1, 6): c_double_type,
    (1, 7): c_longdouble_type,
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
}

def widest_numeric_type(type1, type2):
    # Given two numeric types, return the narrowest type
    # encompassing both of them.
    signed = type1.signed
    rank = max(type1.rank, type2.rank)
    if rank >= lowest_float_rank:
        signed = 1
    return sign_and_rank_to_type[signed, rank]

def simple_c_type(signed, longness, name):
    # Find type descriptor for simple type given name and modifiers.
    # Returns None if arguments don't make sense.
    return modifiers_and_name_to_type.get((signed, longness, name))

def c_array_type(base_type, size):
    # Construct a C array type.
    if base_type is c_char_type:
        return CCharArrayType(size)
    else:
        return CArrayType(base_type, size)

def c_ptr_type(base_type):
    # Construct a C pointer type.
    if base_type is c_char_type:
        return c_char_ptr_type
    else:
        return CPtrType(base_type)

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
