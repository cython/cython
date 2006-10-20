#
#   Pyrex - Tables describing slots in the type object
#           and associated know-how.
#

import Naming
import PyrexTypes

class Signature:
    #  Method slot signature descriptor.
    #
    #  has_dummy_arg      boolean
    #  has_generic_args   boolean
    #  fixed_arg_format   string
    #  ret_format         string
    #  error_value        string
    #
    #  The formats are strings made up of the following
    #  characters:
    #
    #    'O'  Python object
    #    'T'  Python object of the type of 'self'
    #    'v'  void
    #    'p'  void *
    #    'P'  void **
    #    'i'  int
    #    'I'  int *
    #    'l'  long
    #    's'  char *
    #    'S'  char **
    #    'r'  int used only to signal exception
    #    '-'  dummy 'self' argument (not used)
    #    '*'  rest of args passed as generic Python
    #           arg tuple and kw dict (must be last
    #           char in format string)
    
    format_map = {
        'O': PyrexTypes.py_object_type,
        'v': PyrexTypes.c_void_type,
        'p': PyrexTypes.c_void_ptr_type,
        'P': PyrexTypes.c_void_ptr_ptr_type,
        'i': PyrexTypes.c_int_type,
        'I': PyrexTypes.c_int_ptr_type,
        'l': PyrexTypes.c_long_type,
        's': PyrexTypes.c_char_ptr_type,
        'S': PyrexTypes.c_char_ptr_ptr_type,
        'r': PyrexTypes.c_returncode_type,
        # 'T', '-' and '*' are handled otherwise
        # and are not looked up in here
    }
    
    error_value_map = {
        'O': "0",
        'i': "-1",
        'l': "-1",
        'r': "-1",
    }
    
    def __init__(self, arg_format, ret_format):
        self.has_dummy_arg = 0
        self.has_generic_args = 0
        if arg_format[:1] == '-':
            self.has_dummy_arg = 1
            arg_format = arg_format[1:]
        if arg_format[-1:] == '*':
            self.has_generic_args = 1
            arg_format = arg_format[:-1]
        self.fixed_arg_format = arg_format
        self.ret_format = ret_format
        self.error_value = self.error_value_map.get(ret_format, None)
    
    def num_fixed_args(self):
        return len(self.fixed_arg_format)
    
    def is_self_arg(self, i):
        return self.fixed_arg_format[i] == 'T'
    
    def fixed_arg_type(self, i):
        return self.format_map[self.fixed_arg_format[i]]
    
    def return_type(self):
        return self.format_map[self.ret_format]


class SlotDescriptor:
    #  Abstract base class for type slot descriptors.
    #
    #  slot_name    string           Member name of the slot in the type object
    #  is_initialised_dynamically    Is initialised by code in the module init function

    def __init__(self, slot_name, dynamic = 0):
        self.slot_name = slot_name
        self.is_initialised_dynamically = dynamic
    
    def generate(self, scope, code):
        if self.is_initialised_dynamically:
            value = 0
        else:
            value = self.slot_code(scope)
        code.putln("%s, /*%s*/" % (value, self.slot_name))
    
    # Some C implementations have trouble statically 
    # initialising a global with a pointer to an extern 
    # function, so we initialise some of the type slots
    # in the module init function instead.

    def generate_dynamic_init_code(self, scope, code):
        if self.is_initialised_dynamically:
            value = self.slot_code(scope)
            if value <> "0":
                code.putln("%s.%s = %s;" % (
                    scope.parent_type.typeobj_cname, 
                    self.slot_name, 
                    value
                    )
            )


class FixedSlot(SlotDescriptor):
    #  Descriptor for a type slot with a fixed value.
    #
    #  value        string
    
    def __init__(self, slot_name, value):
        SlotDescriptor.__init__(self, slot_name)
        self.value = value
    
    def slot_code(self, scope):
        return self.value


class EmptySlot(FixedSlot):
    #  Descriptor for a type slot whose value is always 0.
    
    def __init__(self, slot_name):
        FixedSlot.__init__(self, slot_name, "0")


class GCDependentSlot(SlotDescriptor):
    #  Descriptor for a slot whose value depends on whether
    #  the type participates in GC.
    
    def __init__(self, slot_name, no_gc_value, gc_value, dynamic = 0):
        SlotDescriptor.__init__(self, slot_name, dynamic)
        self.no_gc_value = no_gc_value
        self.gc_value = gc_value
    
    def slot_code(self, scope):
        if scope.has_pyobject_attrs:
            return self.gc_value
        else:
            return self.no_gc_value


class MethodSlot(SlotDescriptor):
    #  Type slot descriptor for a user-definable method.
    #
    #  signature    Signature
    #  method_name  string           The __xxx__ name of the method
    #  default      string or None   Default value of the slot
    
    def __init__(self, signature, slot_name, method_name, default = None):
        SlotDescriptor.__init__(self, slot_name)
        self.signature = signature
        self.slot_name = slot_name
        self.method_name = method_name
        self.default = default
        method_name_to_slot[method_name] = self

    def slot_code(self, scope):
        entry = scope.lookup_here(self.method_name)
        if entry:
            return entry.func_cname
        else:
            return "0"


class InternalMethodSlot(SlotDescriptor):
    #  Type slot descriptor for a method which is always
    #  synthesized by Pyrex.
    #
    #  slot_name    string           Member name of the slot in the type object

    def __init__(self, slot_name):
        SlotDescriptor.__init__(self, slot_name)

    def slot_code(self, scope):
        return scope.mangle_internal(self.slot_name)


class SyntheticSlot(InternalMethodSlot):
    #  Type slot descriptor for a synthesized method which
    #  dispatches to one or more user-defined methods depending
    #  on its arguments. If none of the relevant methods are
    #  defined, the method will not be synthesized and an
    #  alternative default value will be placed in the type
    #  slot.
    
    def __init__(self, slot_name, user_methods, default_value):
        InternalMethodSlot.__init__(self, slot_name)
        self.user_methods = user_methods
        self.default_value = default_value
    
    def slot_code(self, scope):
        if scope.defines_any(self.user_methods):
            return InternalMethodSlot.slot_code(self, scope)
        else:
            return self.default_value


class TypeFlagsSlot(SlotDescriptor):
    #  Descriptor for the type flags slot.
    
    def slot_code(self, scope):
        # Always add Py_TPFLAGS_HAVE_GC -- PyType_Ready doesn't seem to inherit it
        value = "Py_TPFLAGS_DEFAULT|Py_TPFLAGS_CHECKTYPES|Py_TPFLAGS_BASETYPE|Py_TPFLAGS_HAVE_GC"
        #if scope.has_pyobject_attrs:
        #	value += "|Py_TPFLAGS_HAVE_GC"
        return value
        

class DocStringSlot(SlotDescriptor):
    #  Descriptor for the docstring slot.
    
    def slot_code(self, scope):
        if scope.doc is not None:
            return '"%s"' % scope.doc
        else:
            return "0"


class SuiteSlot(SlotDescriptor):
    #  Descriptor for a substructure of the type object.
    #
    #  sub_slots   [SlotDescriptor]
    
    def __init__(self, sub_slots, slot_type, slot_name):
        SlotDescriptor.__init__(self, slot_name)
        self.sub_slots = sub_slots
        self.slot_type = slot_type
        substructures.append(self)
    
    def substructure_cname(self, scope):
        return "%s%s_%s" % (Naming.pyrex_prefix, self.slot_name, scope.class_name)
    
    def slot_code(self, scope):
        return "&%s" % self.substructure_cname(scope)
        
    def generate_substructure(self, scope, code):
        code.putln("")
        code.putln(
            "static %s %s = {" % (
                self.slot_type,
                self.substructure_cname(scope)))
        for slot in self.sub_slots:
            slot.generate(scope, code)
        code.putln("};")

substructures = []   # List of all SuiteSlot instances

class MethodTableSlot(SlotDescriptor):
    #  Slot descriptor for the method table.
    
    def slot_code(self, scope):
        return scope.method_table_cname


class MemberTableSlot(SlotDescriptor):
    #  Slot descriptor for the table of Python-accessible attributes.
    
    def slot_code(self, scope):
        if scope.public_attr_entries:
            return scope.member_table_cname
        else:
            return "0"


class GetSetSlot(SlotDescriptor):
    #  Slot descriptor for the table of attribute get & set methods.
    
    def slot_code(self, scope):
        if scope.property_entries:
            return scope.getset_table_cname
        else:
            return "0"


class BaseClassSlot(SlotDescriptor):
    #  Slot descriptor for the base class slot.

    def __init__(self, name):
        SlotDescriptor.__init__(self, name, dynamic = 1)
    
    def generate_dynamic_init_code(self, scope, code):
        base_type = scope.parent_type.base_type
        if base_type:
            code.putln("%s.%s = %s;" % (
                scope.parent_type.typeobj_cname, 
                self.slot_name,
                base_type.typeptr_cname))

    
# The following dictionary maps __xxx__ method names to slot descriptors.

method_name_to_slot = {}

## The following slots are (or could be) initialised with an
## extern function pointer.
#
#slots_initialised_from_extern = (
#	"tp_free",
#)

#------------------------------------------------------------------------------------------
#
#  Utility functions for accessing slot table data structures
#
#------------------------------------------------------------------------------------------

def get_special_method_signature(name):
    #  Given a method name, if it is a special method,
    #  return its signature, else return None.
    slot = method_name_to_slot.get(name)
    if slot:
        return slot.signature
    else:
        return None

def get_property_accessor_signature(name):
    #  Return signature of accessor for an extension type
    #  property, else None.
    return property_accessor_signatures.get(name)

#------------------------------------------------------------------------------------------
#
#  Signatures for generic Python functions and methods.
#
#------------------------------------------------------------------------------------------

pyfunction_signature = Signature("-*", "O")
pymethod_signature = Signature("T*", "O")

#------------------------------------------------------------------------------------------
#
#  Signatures for the various kinds of function that
#  can appear in the type object and its substructures.
#
#------------------------------------------------------------------------------------------

unaryfunc = Signature("T", "O")            # typedef PyObject * (*unaryfunc)(PyObject *);
binaryfunc = Signature("OO", "O")          # typedef PyObject * (*binaryfunc)(PyObject *, PyObject *);
ibinaryfunc = Signature("TO", "O")         # typedef PyObject * (*binaryfunc)(PyObject *, PyObject *);
ternaryfunc = Signature("OOO", "O")        # typedef PyObject * (*ternaryfunc)(PyObject *, PyObject *, PyObject *);
iternaryfunc = Signature("TOO", "O")       # typedef PyObject * (*ternaryfunc)(PyObject *, PyObject *, PyObject *);
callfunc = Signature("T*", "O")            # typedef PyObject * (*ternaryfunc)(PyObject *, PyObject *, PyObject *);
inquiry = Signature("T", "i")              # typedef int (*inquiry)(PyObject *);
                                           # typedef int (*coercion)(PyObject **, PyObject **);
intargfunc = Signature("Ti", "O")          # typedef PyObject *(*intargfunc)(PyObject *, int);
intintargfunc = Signature("Tii", "O")      # typedef PyObject *(*intintargfunc)(PyObject *, int, int);
intobjargproc = Signature("TiO", 'r')      # typedef int(*intobjargproc)(PyObject *, int, PyObject *);
intintobjargproc = Signature("TiiO", 'r')  # typedef int(*intintobjargproc)(PyObject *, int, int, PyObject *);
intintargproc = Signature("Tii", 'r')
objargfunc = Signature("TO", "O")
objobjargproc = Signature("TOO", 'r')      # typedef int (*objobjargproc)(PyObject *, PyObject *, PyObject *);
getreadbufferproc = Signature("TiP", 'i')  # typedef int (*getreadbufferproc)(PyObject *, int, void **);
getwritebufferproc = Signature("TiP", 'i') # typedef int (*getwritebufferproc)(PyObject *, int, void **);
getsegcountproc = Signature("TI", 'i')     # typedef int (*getsegcountproc)(PyObject *, int *);
getcharbufferproc = Signature("TiS", 'i')  # typedef int (*getcharbufferproc)(PyObject *, int, const char **);
objargproc = Signature("TO", 'r')          # typedef int (*objobjproc)(PyObject *, PyObject *);
                                           # typedef int (*visitproc)(PyObject *, void *);
                                           # typedef int (*traverseproc)(PyObject *, visitproc, void *);

destructor = Signature("T", "v")           # typedef void (*destructor)(PyObject *);
# printfunc = Signature("TFi", 'r')        # typedef int (*printfunc)(PyObject *, FILE *, int);
                                           # typedef PyObject *(*getattrfunc)(PyObject *, char *);
getattrofunc = Signature("TO", "O")        # typedef PyObject *(*getattrofunc)(PyObject *, PyObject *);
                                           # typedef int (*setattrfunc)(PyObject *, char *, PyObject *);
setattrofunc = Signature("TOO", 'r')       # typedef int (*setattrofunc)(PyObject *, PyObject *, PyObject *);
delattrofunc = Signature("TO", 'r')
cmpfunc = Signature("TO", "i")             # typedef int (*cmpfunc)(PyObject *, PyObject *);
reprfunc = Signature("T", "O")             # typedef PyObject *(*reprfunc)(PyObject *);
hashfunc = Signature("T", "l")             # typedef long (*hashfunc)(PyObject *);
                                           # typedef PyObject *(*richcmpfunc) (PyObject *, PyObject *, int);
richcmpfunc = Signature("OOi", "O")        # typedef PyObject *(*richcmpfunc) (PyObject *, PyObject *, int);
getiterfunc = Signature("T", "O")          # typedef PyObject *(*getiterfunc) (PyObject *);
iternextfunc = Signature("T", "O")         # typedef PyObject *(*iternextfunc) (PyObject *);
descrgetfunc = Signature("TOO", "O")       # typedef PyObject *(*descrgetfunc) (PyObject *, PyObject *, PyObject *);
descrsetfunc = Signature("TOO", 'r')       # typedef int (*descrsetfunc) (PyObject *, PyObject *, PyObject *);
descrdelfunc = Signature("TO", 'r')
initproc = Signature("T*", 'r')            # typedef int (*initproc)(PyObject *, PyObject *, PyObject *);
                                           # typedef PyObject *(*newfunc)(struct _typeobject *, PyObject *, PyObject *);
                                           # typedef PyObject *(*allocfunc)(struct _typeobject *, int);

#------------------------------------------------------------------------------------------
#
#  Signatures for accessor methods of properties.
#
#------------------------------------------------------------------------------------------

property_accessor_signatures = {
    '__get__': Signature("T", "O"),
    '__set__': Signature("TO", 'r'),
    '__del__': Signature("T", 'r')
}

#------------------------------------------------------------------------------------------
#
#  Descriptor tables for the slots of the various type object
#  substructures, in the order they appear in the structure.
#
#------------------------------------------------------------------------------------------

PyNumberMethods = (
    MethodSlot(binaryfunc, "nb_add", "__add__"),
    MethodSlot(binaryfunc, "nb_subtract", "__sub__"),
    MethodSlot(binaryfunc, "nb_multiply", "__mul__"),
    MethodSlot(binaryfunc, "nb_divide", "__div__"),
    MethodSlot(binaryfunc, "nb_remainder", "__mod__"),
    MethodSlot(binaryfunc, "nb_divmod", "__divmod__"),
    MethodSlot(ternaryfunc, "nb_power", "__pow__"),
    MethodSlot(unaryfunc, "nb_negative", "__neg__"),
    MethodSlot(unaryfunc, "nb_positive", "__pos__"),
    MethodSlot(unaryfunc, "nb_absolute", "__abs__"),
    MethodSlot(inquiry, "nb_nonzero", "__nonzero__"),
    MethodSlot(unaryfunc, "nb_invert", "__invert__"),
    MethodSlot(binaryfunc, "nb_lshift", "__lshift__"),
    MethodSlot(binaryfunc, "nb_rshift", "__rshift__"),
    MethodSlot(binaryfunc, "nb_and", "__and__"),
    MethodSlot(binaryfunc, "nb_xor", "__xor__"),
    MethodSlot(binaryfunc, "nb_or", "__or__"),
    EmptySlot("nb_coerce"),
    MethodSlot(unaryfunc, "nb_int", "__int__"),
    MethodSlot(unaryfunc, "nb_long", "__long__"),
    MethodSlot(unaryfunc, "nb_float", "__float__"),
    MethodSlot(unaryfunc, "nb_oct", "__oct__"),
    MethodSlot(unaryfunc, "nb_hex", "__hex__"),
    
    # Added in release 2.0
    MethodSlot(ibinaryfunc, "nb_inplace_add", "__iadd__"),
    MethodSlot(ibinaryfunc, "nb_inplace_subtract", "__isub__"),
    MethodSlot(ibinaryfunc, "nb_inplace_multiply", "__imul__"),
    MethodSlot(ibinaryfunc, "nb_inplace_divide", "__idiv__"),
    MethodSlot(ibinaryfunc, "nb_inplace_remainder", "__imod__"),
    MethodSlot(ternaryfunc, "nb_inplace_power", "__ipow__"), # NOT iternaryfunc!!!
    MethodSlot(ibinaryfunc, "nb_inplace_lshift", "__ilshift__"),
    MethodSlot(ibinaryfunc, "nb_inplace_rshift", "__irshift__"),
    MethodSlot(ibinaryfunc, "nb_inplace_and", "__iand__"),
    MethodSlot(ibinaryfunc, "nb_inplace_xor", "__ixor__"),
    MethodSlot(ibinaryfunc, "nb_inplace_or", "__ior__"),
    
    # Added in release 2.2
    # The following require the Py_TPFLAGS_HAVE_CLASS flag
    MethodSlot(binaryfunc, "nb_floor_divide", "__floordiv__"),
    MethodSlot(binaryfunc, "nb_true_divide", "__truediv__"),
    MethodSlot(ibinaryfunc, "nb_inplace_floor_divide", "__ifloordiv__"),
    MethodSlot(ibinaryfunc, "nb_inplace_true_divide", "__itruediv__"),
)

PySequenceMethods = (
    MethodSlot(inquiry, "sq_length", "__len__"),    # EmptySlot("sq_length"), # mp_length used instead
    EmptySlot("sq_concat"), # nb_add used instead
    EmptySlot("sq_repeat"), # nb_multiply used instead
    SyntheticSlot("sq_item", ["__getitem__"], "0"),    #EmptySlot("sq_item"),   # mp_subscript used instead
    MethodSlot(intintargfunc, "sq_slice", "__getslice__"),
    EmptySlot("sq_ass_item"), # mp_ass_subscript used instead
    SyntheticSlot("sq_ass_slice", ["__setslice__", "__delslice__"], "0"),
    MethodSlot(cmpfunc, "sq_contains", "__contains__"),
    EmptySlot("sq_inplace_concat"), # nb_inplace_add used instead
    EmptySlot("sq_inplace_repeat"), # nb_inplace_multiply used instead
)

PyMappingMethods = (
    MethodSlot(inquiry, "mp_length", "__len__"),
    MethodSlot(objargfunc, "mp_subscript", "__getitem__"),
    SyntheticSlot("mp_ass_subscript", ["__setitem__", "__delitem__"], "0"),
)

PyBufferProcs = (
    MethodSlot(getreadbufferproc, "bf_getreadbuffer", "__getreadbuffer__"),
    MethodSlot(getwritebufferproc, "bf_getwritebuffer", "__getwritebuffer__"),
    MethodSlot(getsegcountproc, "bf_getsegcount", "__getsegcount__"),
    MethodSlot(getcharbufferproc, "bf_getcharbuffer", "__getcharbuffer__"),
)

#------------------------------------------------------------------------------------------
#
#  The main slot table. This table contains descriptors for all the
#  top-level type slots, beginning with tp_dealloc, in the order they
#  appear in the type object.
#
#------------------------------------------------------------------------------------------

slot_table = (
    InternalMethodSlot("tp_dealloc"),
    EmptySlot("tp_print"), #MethodSlot(printfunc, "tp_print", "__print__"),
    EmptySlot("tp_getattr"),
    EmptySlot("tp_setattr"),
    MethodSlot(cmpfunc, "tp_compare", "__cmp__"),
    MethodSlot(reprfunc, "tp_repr", "__repr__"),
    
    SuiteSlot(PyNumberMethods, "PyNumberMethods", "tp_as_number"),
    SuiteSlot(PySequenceMethods, "PySequenceMethods", "tp_as_sequence"),
    SuiteSlot(PyMappingMethods, "PyMappingMethods", "tp_as_mapping"),

    MethodSlot(hashfunc, "tp_hash", "__hash__"),
    MethodSlot(callfunc, "tp_call", "__call__"),
    MethodSlot(reprfunc, "tp_str", "__str__"),
    
    SyntheticSlot("tp_getattro", ["__getattr__"], "0"), #"PyObject_GenericGetAttr"),
    SyntheticSlot("tp_setattro", ["__setattr__", "__delattr__"], "0"), #"PyObject_GenericSetAttr"),

    SuiteSlot(PyBufferProcs, "PyBufferProcs", "tp_as_buffer"),
    
    TypeFlagsSlot("tp_flags"),
    DocStringSlot("tp_doc"),

    InternalMethodSlot("tp_traverse"),
    InternalMethodSlot("tp_clear"),

    # Later -- synthesize a method to split into separate ops?
    MethodSlot(richcmpfunc, "tp_richcompare", "__richcmp__"),

    EmptySlot("tp_weaklistoffset"),

    MethodSlot(getiterfunc, "tp_iter", "__iter__"),
    MethodSlot(iternextfunc, "tp_iternext", "__next__"),

    MethodTableSlot("tp_methods"),
    MemberTableSlot("tp_members"),
    GetSetSlot("tp_getset"),
    
    BaseClassSlot("tp_base"), #EmptySlot("tp_base"),
    EmptySlot("tp_dict"),
    
    SyntheticSlot("tp_descr_get", ["__get__"], "0"),
    SyntheticSlot("tp_descr_set", ["__set__", "__delete__"], "0"),
    
    EmptySlot("tp_dictoffset"),
    
    MethodSlot(initproc, "tp_init", "__init__"),
    EmptySlot("tp_alloc"), #FixedSlot("tp_alloc", "PyType_GenericAlloc"),
    InternalMethodSlot("tp_new"),
    # Some versions of Python 2.2 inherit the wrong value for tp_free when the
    # type has GC but the base type doesn't, so we explicitly set it ourselves
    # in that case.
    GCDependentSlot("tp_free", "0", "_PyObject_GC_Del", dynamic = 1),
    
    EmptySlot("tp_is_gc"),
    EmptySlot("tp_bases"),
    EmptySlot("tp_mro"),
    EmptySlot("tp_cache"),
    EmptySlot("tp_subclasses"),
    EmptySlot("tp_weaklist"),
)

#------------------------------------------------------------------------------------------
#
#  Descriptors for special methods which don't appear directly
#  in the type object or its substructures. These methods are
#  called from slot functions synthesized by Pyrex.
#
#------------------------------------------------------------------------------------------

MethodSlot(initproc, "", "__new__")
MethodSlot(destructor, "", "__dealloc__")
MethodSlot(objobjargproc, "", "__setitem__")
MethodSlot(objargproc, "", "__delitem__")
MethodSlot(intintobjargproc, "", "__setslice__")
MethodSlot(intintargproc, "", "__delslice__")
MethodSlot(getattrofunc, "", "__getattr__")
MethodSlot(setattrofunc, "", "__setattr__")
MethodSlot(delattrofunc, "", "__delattr__")
MethodSlot(descrgetfunc, "", "__get__")
MethodSlot(descrsetfunc, "", "__set__")
MethodSlot(descrdelfunc, "", "__delete__")
