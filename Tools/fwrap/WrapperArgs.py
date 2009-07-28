from fparser.block_statements import Function, SubProgramStatement, \
        Module, Program, Subroutine, \
        EndFunction, EndSubroutine, Interface
from utils import warning, mangle_prefix, valid_name

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
        self.type_name = self.var.typedecl.name.lower().replace(' ', '')
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

class FortranWrapperVar(object):

    def __init__(self, var):
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

        if var.is_intent_in(): self.intent = 'IN'
        elif var.is_intent_inout(): self.intent = 'INOUT'
        elif var.is_intent_out(): self.intent = 'OUT'
        # else:
            # node = self.defining_scope
            # if isinstance(node, Function) and \
                    # self.var is node.a.variables[node.result]:
                        # self.intent = None

    def need_conversion(self):
        return False

    
    def get_declaration(self):
        var = self.var
        attributes = []
        if self.intent is not None:
            attributes.append('intent(%s)' % self.intent)
            if self.intent == 'IN':
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
        return decl

    def convert_temp_declaration(self):
        raise NotImplementedError()
        # return "%s(kind=%s) :: %s" % (self.orig_type, 

    def gen_temp(self):
        self.temp_name = mangle_prefix+'_tmp_'+self.var.name
        return self.temp_name

    def pre_call_conversion(self):
        if not self.need_conversion():
            return None

    def post_call_conversion(self):
        if not self.need_conversion():
            return None

class LogicalWrapperVar(FortranWrapperVar):

    def need_conversion(self):
        return True

    def get_temp_declaration(self, temp_name):
        return "%s(kind=%s) :: %s" % (self.type_name, self.resolved_name, temp_name)

    def pre_call_conversion(self, temp_name):
        if self.intent == 'OUT':
            return ''
        return "%s = logical(%s .ne. 0, kind=%s)" % (temp_name, self.var.name, self.resolved_name)

    def post_call_conversion(self, temp_name):
        if self.intent == 'IN':
            return ''
        return """if (%s) then\n%s = 1\nelse\n%s = 0\nendif""" % (temp_name, self.var.name, self.var.name)
