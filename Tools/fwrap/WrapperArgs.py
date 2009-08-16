from fparser.block_statements import Function, SubProgramStatement, \
        Module, Program, Subroutine, \
        EndFunction, EndSubroutine, Interface
from utils import warning, mangle_prefix, valid_name, CY_IMPORT_ALIAS

class WrapperError(Exception):
    pass

def _get_type_name(var):
    return var.typedecl.name.lower().replace(' ', '')

def type_from_vkr(vkr):
    typename_to_class = {
            'integer' : FortranIntegerType,
            'real'    : FortranRealType,
            'doubleprecision' : FortranRealType,
            'character': FortranCharacterType,
            'logical' : FortranLogicalType,
            'complex' : FortranComplexType,
            'doublecomplex' : FortranComplexType
        }
    return typename_to_class[vkr.type_name](ktp=vkr.resolved_name)

class VarKindResolution(object):

    short_type_name = {
            "integer" : "int",
            "real"    : "real",
            "character" : "char",
            "logical" : "lgcl",
            "doubleprecision" : "dprc",
            "complex" : "cpx",
            "doublecomplex" : "dcpx"
            }

    def __init__(self, variable):
        self.var = variable # the variable that will have the ktp resolved.
        self.type_name = None # type of the variable ('integer', 'real', 'complex', 'logical', 'character')
        self.resolved_name = None # name that will be used for the ktp in the wrapper.
        self.ktp_str = None # string-form of the ktp.
        self.defining_param = None # 'variable' (parameter) that defines the ktp.
        self.defining_scope = None # scope in which the defining_param is defined.
        self.length = None

        self.init_from_var()

        if self.type_name not in ('integer', 'real', 'character', 'logical', 'complex'):
            raise WrapperError("unknown type name '%s'." % self.type_name)

        if not self.resolved_name:
            raise WrapperError("unable to resolve the kind type parameter for variable %s" % self.var.name)


    def init_from_var(self):
        self.type_name = _get_type_name(self.var)
        var_scope = self.var.typedecl.parent
        assert isinstance(var_scope, (SubProgramStatement, Module, Program))
        length, ktp = self.var.typedecl.selector
        ktp_str = str(ktp).lower().strip()

        self.resolved_name = ''

        if not ktp:
            self.handle_default_ktp()
            return

        ktp_parse = VarKindResolution.parse_ktp(ktp)

        stn = self.short_type_name

        if isinstance(ktp_parse[0], int):
            self.ktp_str = str(ktp_parse[0])
            self.resolved_name = mangle_prefix+stn[self.type_name]+ktp_str
            self.defining_scope = var_scope
            self.defining_param = None

        elif ktp_parse[0] == 'kind':
            self.ktp_str = ktp
            num_str = ktp_parse[1].replace('.','')
            num_str = num_str.replace('(','')
            num_str = num_str.replace(')','')
            num_str = num_str.replace(',','')
            self.resolved_name = mangle_prefix+stn[self.type_name]+'_kind'+num_str
            self.defining_scope = var_scope
            self.defining_param = None

        elif ktp_parse[0] == 'selected_int_kind':
            self.ktp_str = ktp
            self.resolved_name = mangle_prefix+stn[self.type_name]+'_slctd_int'+ktp_parse[1]
            self.defining_scope = var_scope
            self.defining_param = None

        elif ktp_parse[0] == 'selected_real_kind':
            self.resolved_name = mangle_prefix+stn[self.type_name]+'slctd_real'+ktp_parse[1]
            if len(ktp_parse) == 3:
                self.resolved_name += ktp_parse[2]
            self.ktp_str = ktp
            self.defining_scope = var_scope
            self.defining_param = None

        elif valid_name(ktp_parse[0]):
            # XXX TODO: still have to fill this in...
            raise NotImplementedError("kind-type-parameter '%s' is not resolvable yet" % ktp)
            # lookup_name = ktp_parse[0]
            # def_scope, var = find_defining_scope(var_scope, lookup_name)
            # assert var.is_parameter()
            # assert type(var.typedecl).name.lower() == 'integer'
            # if def_scope is var_scope:
                # # it's defined locally.
                # # TODO: check this over...
                # resolve_name = "%s_%s_%s" % (mangle_prefix, var_scope.name, var.name)
                # # self.local_param_ktp.append((resolve_name, var.init))
            # else:
                # # it's defined in a module, possibly with a use-rename.
                # resolve_name = "%s_%s_%s" % (mangle_prefix, var_scope.name, var.name)
                # raise RuntimeError("finish here!!!")

        else:
            raise KindResolutionError("unable to resolve kind-type-parameter '%s'" % ktp)

    @staticmethod
    def find_defining_scope(node, param_name):
        '''
        finds where param_name is defined in the local & enclosing scopes of node.

        returns (<defining-scope-block>, <variable-defined>)

        NOTE: the variable returned may not have the same name as param_name, due
        to a renaming in a use statement.
        '''
        raise NotImplementedError("finish me!!!")

    @staticmethod
    def parse_ktp(ktp):
        # this should ideally all be in the parser
        ktp = ktp.lower().strip()
        try:
            ktp_int = int(ktp)
        except ValueError:
            pass
        else:
            return (ktp_int,)

        if valid_name(ktp):
            return (ktp,)

        for sw in ('kind', 'selected_int_kind'):
            if ktp.startswith(sw):
                retval = [sw]
                ktp = ktp[len(sw):].strip()
                assert ktp[0] + ktp[-1] == '()'
                # handle the middle...
                arg = ktp[1:-1].strip()
                retval.append(arg.replace(' ',''))
                return tuple(retval)

        srk = 'selected_real_kind'
        if ktp.startswith(srk):
            retval = [srk]
            ktp = ktp[len(srk):].strip()
            assert ktp[0] + ktp[-1] == '()'
            arg = ktp[1:-1].split(',')
            retval.append(arg[0].replace(' ',''))
            if len(arg) == 2:
                retval.append(arg[1].replace(' ', ''))
            return tuple(retval)

        # nothing matches, raise error for now...
        raise KindResolutionError("unable to resolve kind-type-parameter '%s'" % ktp)

    def handle_default_ktp(self):
        length, ktp = self.var.typedecl.selector
        assert not ktp
        length = str(length).strip()
        type_name = self.type_name
        scope = self.var.typedecl.parent

        stn = self.short_type_name
        if length:
            warning("variable '%s' in '%s' declared with old syntax." % (self.var.name, scope.name))
            #XXX TODO ktp_str here is incorrect -- assumes the length is the same as a ktp, which ain't always so!!!
            # in autoconfig, for an integer*N variable:
            # declare local variable integer*N
            self.length = length
            self.ktp_str = None
            self.resolved_name = mangle_prefix+stn[type_name]+'_x_'+length

        # the default types follow.
        elif type_name == 'doubleprecision':
            self.ktp_str = 'kind(1.0D0)'
            self.resolved_name = mangle_prefix+'default_'+stn[type_name]
            self.type_name = 'real'

        elif type_name == 'logical':
            self.ktp_str = 'kind(.true.)'
            self.resolved_name = mangle_prefix+'default_'+stn[type_name]

        elif type_name == 'integer':
            self.ktp_str = 'kind(0)'
            self.resolved_name = mangle_prefix+'default_'+stn[type_name]

        elif type_name == 'real':
            self.ktp_str = 'kind(0.0)'
            self.resolved_name = mangle_prefix+'default_'+stn[type_name]

        elif type_name == 'character':
            self.ktp_str = "kind('a')"
            self.resolved_name = mangle_prefix+'default_'+stn[type_name]

        elif type_name == 'complex':
            self.ktp_str = 'kind((0.0,0.0))'
            self.resolved_name = mangle_prefix+'default_'+stn[type_name]

        elif type_name == 'doublecomplex':
            self.ktp_str = 'kind((0.0D0,0.0D0))'
            self.resolved_name = mangle_prefix+'default_'+stn[type_name]
            self.type_name = 'complex'

        else:
            raise KindResolutionError()

        # self.type_name, self.ktp_str, self.resolved_name are all set at this point.

        self.defining_scope = scope
        self.defining_param = None

class Disambiguator(object):

    def __init__(self):
        self.counter = 0

    def __call__(self):
        ret = 'fw%d' % self.counter
        self.counter += 1
        return ret

def wrapper_var_factory(node, var, _cache={}):
    _type_name_to_class = {
            'integer' : IntegerWrapperVar,
            'real'    : RealWrapperVar,
            'doubleprecision' : RealWrapperVar,
            'character': CharacterWrapperVar,
            'logical' : LogicalWrapperVar,
            'complex' : ComplexWrapperVar,
            'doublecomplex' : ComplexWrapperVar
            }

    _array_to_class = {
            'integer' : IntegerArrayWrapperVar,
            'real'    : RealArrayWrapperVar,
            'doubleprecision' : RealArrayWrapperVar,
            'character': CharacterWrapperVar,
            'logical' : LogicalArrayWrapperVar,
            'complex' : ComplexArrayWrapperVar,
            'doublecomplex' : ComplexArrayWrapperVar
            }

    d = _cache.get(node)
    if d is None:
        d = Disambiguator()
        _cache[node] = d

    type_name = _get_type_name(var)

    if var.is_array():
        return _array_to_class[type_name](var, d)
    else:
        return _type_name_to_class[type_name](var, d)

INTENT_IN = 'IN'
INTENT_OUT = 'OUT'
INTENT_INOUT = 'INOUT'

class FortranWrapperVar(object):
    #
    # A FortranWrapperVar is responsible for setting-up an appropriate
    # conversion between the fortran-wrapper procedure input arguments and the
    # argument of the wrapped procedure.  Some argument types (real, integer,
    # complex if C99 _Complex is supported, etc.) have a 1-to-1 correspondence
    # with a C type.  Others (logical) must be passed to the fortran wrapper
    # procedure as a different type (a C-int) and converted before or after the
    # wrapped procedure call, as appropriate.

    # Arrays are different.  Each array argument of the wrapped procedure
    # requires multiple wrapper arguments (at least a data pointer and the
    # extent in each dimension).  A c_f_pointer() call is required before the
    # wrapped procedure call, and possibly a copy is required for, e.g., a
    # C-int -> logical -> C-int type. Each array requires a temporary array
    # pointer that is the second argument to the c_f_pointer() call, and is the
    # array passed to the wrapped procedure.
     
    # XXX: user-defined type description here.

    is_array = False

    def __init__(self, var, disambig):
        self.disambig = disambig
        vkr = VarKindResolution(var)
        self.var = var
        self.type_name = vkr.type_name
        self.resolved_name = vkr.resolved_name
        self.ktp_str = vkr.ktp_str
        self.defining_param = vkr.defining_param
        self.defining_scope = vkr.defining_scope
        self.length = vkr.length
        self.vkr = vkr
        self.intent = None

        if var.is_intent_in(): self.intent = INTENT_IN
        elif var.is_intent_inout(): self.intent = INTENT_INOUT
        elif var.is_intent_out(): self.intent = INTENT_OUT
        # else:
            # node = self.defining_scope
            # if isinstance(node, Function) and \
                    # self.var is node.a.variables[node.result]:
                        # self.intent = None

    def get_py_arg_declarations(self):
        return ((self.resolved_name, self.var.name),)

    def get_py_pass_argnames(self):
        return (self.var.name,)

    def get_cy_arg_declarations(self):
        return ((self.get_c_proto_types()[0], self.var.name),)

    def pre_call_cy_code(self, code):
        pass

    def post_call_cy_code(self, code):
        pass


    def get_cy_pass_argnames(self):
        return (self.var.name,)

    def generate_cy_declarations(self, code):
        pass

    def get_c_proto_types(self):
        if self.intent == INTENT_IN:
            ret = self.resolved_name
        else:
            ret = self.resolved_name+'*'
        return [ret]

    def get_fort_argnames(self):
        return [self.var.name]

    def get_fort_pass_argnames_map(self):
        return (self.var.name, self.var.name)

    def generate_fort_declarations(self, code):
        var = self.var
        attributes = []
        if self.intent is not None:
            attributes.append('intent(%s)' % self.intent)
            if self.intent == INTENT_IN:
                attributes.append('value')
            # collect other attributes here...
        attr_str = ''
        if attributes:
            attr_str += ", " + (", ".join(attributes))
        decl = "%(type_name)s(kind=%(ktp)s) %(attrs)s :: %(var_name)s" % \
                { 'type_name' : self.type_name,
                  'attrs'     : attr_str,
                  'ktp'       : self.resolved_name,
                  'var_name'  : self.var.name
                  }
        code.putln(decl)

    def pre_call_fortran_code(self, code):
        pass

    def post_call_fortran_code(self, code):
        pass

class LogicalWrapperVar(FortranWrapperVar):

    def __init__(self, *args, **kwargs):
        FortranWrapperVar.__init__(self, *args, **kwargs)

        self.int_proxy = Entry(self.disambig()+self.var.name, FortranIntegerType(self.resolved_name))
        self.int_proxy.is_arg = True
        self.int_proxy.intent = self.intent
        # self.int_proxy.attributes.append("intent(%s)" % self.intent)
        if self.intent == INTENT_IN:
            self.int_proxy.is_value = True

        self.log_var = Entry(self.disambig()+self.var.name, FortranLogicalType(self.resolved_name))
        self.log_var.is_arg = False

    def get_c_proto_types(self):
        if not self.int_proxy.is_value:
            return [self.int_proxy.get_base_type_name() + '*']
        else:
            return [self.int_proxy.get_base_type_name()]

    def get_fort_argnames(self):
        return [self.int_proxy.name]

    def get_fort_pass_argnames_map(self):
        return (self.var.name, self.log_var.name)

    def generate_fort_declarations(self, code):
        for entry in (self.int_proxy, self.log_var):
            entry.generate_fort_declaration(code)

    def pre_call_fortran_code(self, code):
        if self.intent in (INTENT_IN, INTENT_INOUT):
            code.putln("%s = logical(%s .ne. 0, kind=%s)" % (self.log_var.name, self.int_proxy.name, self.int_proxy.type.ktp))

    def post_call_fortran_code(self, code):
        if self.intent in (INTENT_INOUT, INTENT_OUT):
            code.putln("if (%s) then" % self.log_var.name  )
            code.putln("  %s = 1    " % self.int_proxy.name)
            code.putln("else        "                      )
            code.putln("  %s = 0    " % self.int_proxy.name)
            code.putln("endif       "                      )

class IntegerWrapperVar(FortranWrapperVar):
    pass

class RealWrapperVar(FortranWrapperVar):
    pass

class ComplexWrapperVar(FortranWrapperVar):
    pass

class CharacterWrapperVar(FortranWrapperVar):
    pass

# class CyArrayWrapperVar(object):

    # def __init__(self, fort_wrapper_var, disambig):
        # self.disambig = disambig
        # self.fort_wrapper_var = fort_wrapper_var
        # self.memview_in = Entry(self.disambig()+'mvs', fort_wrapper_var.var_entry.type)
        # self.ndim = fort_wrapper_var.ndim

    # def get_signature_types(self):
        # slice_decl = [":"]*self.ndim
        # slice_decl[0] = "::1"
        # return ["%s[%s]" % (self.memview_in.get_base_type_name(),','.join(slice_decl))]

ARRAY_SHAPE_TYPE = "fwrap_ardim_long"
class ArrayWrapperVar(FortranWrapperVar):

    def __init__(self, var, disambig):
        assert var.is_array()
        FortranWrapperVar.__init__(self, var, disambig)
        # array-specific initializations
        self.is_array = True
        self.is_explicit_shape = var.is_explicit_shape_array()
        self.is_assumed_shape  = var.is_assumed_shape_array()
        self.is_assumed_size   = var.is_assumed_size_array()
        self.array_spec = var.get_array_spec()
        self.ndim = len(self.array_spec)

        if not self.is_assumed_shape:
            raise NotImplementedError("only assumed shape arrays for now...")

        self.shape_array = Entry(self.disambig()+self.var.name,
                                 FortranArrayType(FortranIntegerType(ktp=ARRAY_SHAPE_TYPE),
                                                  (str(self.ndim),)
                                                  )
                                 )

        self.shape_array.is_arg = True
        self.shape_array.intent = INTENT_IN

        self.data_ptr = Entry(self.disambig()+self.var.name, FortranCPtrType())
        self.data_ptr.is_arg = True
        self.data_ptr.is_value = True

        self.arr_proxy = Entry(self.disambig()+self.var.name,
                               FortranArrayType(type_from_vkr(self.vkr),
                                                (('',''),)*self.ndim))
        self.arr_proxy.is_pointer = True

        self.var_entry = Entry(self.var.name, type_from_vkr(self.vkr))

    def get_py_arg_declarations(self):
        return (('', self.var_entry.name),)

    def get_py_pass_argnames(self):
        return (self.var_entry.name,)

    def get_cy_arg_declarations(self):
        slice_decl = [":"]*self.ndim
        slice_decl[0] = "::1"
        return (("%s[%s]" % (self.var_entry.get_base_type_name(),','.join(slice_decl)),
                    self.var_entry.name),)

    def get_cy_pass_argnames(self):
        return (self.data_ptr.name, self.shape_array.name)

    def generate_cy_declarations(self, code):
        if not self.is_assumed_shape:
            raise NotImplementedError("only assumed shape arrays for now...")
        code.putln("cdef %s.%s *%s" % (CY_IMPORT_ALIAS,
                                      self.var_entry.get_base_type_name(),
                                      self.data_ptr.name))
        code.putln("cdef %s.%s *%s" % (CY_IMPORT_ALIAS,
                                      self.shape_array.get_base_type_name(),
                                      self.shape_array.name))

    def pre_call_cy_code(self, code):
        code.putln("%s = <%s.%s*>%s._data" % (
                                    self.data_ptr.name,
                                    CY_IMPORT_ALIAS,
                                    self.var_entry.get_base_type_name(),
                                    self.var_entry.name))
        code.putln("%s = <%s.%s*>%s.shape" % (
                                    self.shape_array.name,
                                    CY_IMPORT_ALIAS,
                                    self.shape_array.get_base_type_name(),
                                    self.var_entry.name))

    def post_call_cy_code(self, code):
        pass

    def get_c_proto_types(self):
        return [self.var_entry.get_base_type_name()+'*', self.shape_array.get_base_type_name()+'*']

    def get_fort_argnames(self):
        return [self.data_ptr.name, self.shape_array.name]

    def get_fort_pass_argnames_map(self):
        return [self.var.name, self.arr_proxy.name]

    def generate_fort_declarations(self, code):
        if self.is_assumed_shape:
            for entry in (self.shape_array, self.data_ptr, self.arr_proxy):
                entry.generate_fort_declaration(code)
        else:
            raise NotImplementedError("only assumed shape arrays for now...")

    def pre_call_fortran_code(self, code):
        code.putln("call c_f_pointer(%s, %s, %s)" % (self.data_ptr.name, self.arr_proxy.name, self.shape_array.name))

    def post_call_fortran_code(self, code):
        pass

class IntegerArrayWrapperVar(ArrayWrapperVar):
    pass

class RealArrayWrapperVar(ArrayWrapperVar):
    pass

class ComplexArrayWrapperVar(ArrayWrapperVar):
    pass

class LogicalArrayWrapperVar(ArrayWrapperVar):
    pass

_c_binding_to_c_type = {
        # 'c_int' : 'int',
        }

class Entry(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.is_arg = False
        self.is_value = False
        self.is_pointer = False
        self.intent = None

    def generate_fort_declaration(self, code):
        attributes = []
        if self.is_pointer:
            attributes.append('pointer')
        if self.is_value:
            # assert self.intent == INTENT_IN
            attributes.append('value')
        if self.intent:
            attributes.append('intent(%s)' % self.intent)
        before_colons = [self.type.get_type_code()] + self.type.attributes + attributes
        code.putln("%s :: %s" % (",".join(before_colons), self.name))

    def get_base_type_name(self):
        # ret = _c_binding_to_c_type.get(self.type.ktp, self.type.ktp)
        return self.type.ktp
        # if self.is_value:
            # return ret
        # else:
            # return ret+"*"

class FortranType(object):

    def __init__(self, ktp=None):
        self.ktp = ktp
        self.attributes = []

    def get_type_code(self):
        if self.ktp:
            return "%s(kind=%s)" % (self.type_name, self.ktp)
        else:
            return self.type_name

class FortranIntegerType(FortranType):

    type_name = "integer"

class FortranRealType(FortranType):
    
    type_name = "real"

class FortranCharacterType(FortranType):
    
    type_name = "character"

class FortranLogicalType(FortranType):
    
    type_name = "logical"

class FortranComplexType(FortranType):
    
    type_name = "complex"

class FortranCPtrType(FortranType):

    def get_type_code(self):
        return "type(c_ptr)"

class FortranArrayType(FortranType):

    def __init__(self, base_type, shape):
        self.base_type = base_type
        self.ktp = self.base_type.ktp
        self.shape = shape
        self.attributes = []

        dims = []
        for sh in shape:
            if len(sh) == 1:
                dims.append(sh[0])
            else:
                dims.append("%s:%s" % (sh[0], sh[1]))

        self.attributes.append("dimension(%s)" % (",".join(dims)))

    def get_type_code(self):
        return self.base_type.get_type_code()
