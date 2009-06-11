#
# classes BasicVisitor & TreeVisitor were lifted from Cython.Compiler.Visitor
# and adapted for f2cy.
# 

import inspect
from pprint import pprint
import re
import sys
from fparser.block_statements import Function, SubProgramStatement, Module, Program
from Cython.StringIOTree import StringIOTree

LEVEL = 0

def warning(message, position=None, level=0, stream=sys.stderr):
    if level < LEVEL:
        return
    # for now, echo on stream
    stream.write("warning: %s\n" % message)
    stream.flush()

class BasicVisitor(object):
    """A generic visitor base class which can be used for visiting any kind of object."""
    def __init__(self):
        self.dispatch_table = {}

    def visit(self, obj):
        cls = type(obj)
        try:
            handler_method = self.dispatch_table[cls]
        except KeyError:
            #print "Cache miss for class %s in visitor %s" % (
            #    cls.__name__, type(self).__name__)
            # Must resolve, try entire hierarchy
            pattern = "visit_%s"
            mro = inspect.getmro(cls)
            handler_method = None
            for mro_cls in mro:
                if hasattr(self, pattern % mro_cls.__name__):
                    handler_method = getattr(self, pattern % mro_cls.__name__)
                    break
            if handler_method is None:
                print type(self), type(obj)
                if hasattr(self, 'access_path') and self.access_path:
                    print self.access_path
                    if self.access_path:
                        print self.access_path[-1][0].pos
                        print self.access_path[-1][0].__dict__
                raise RuntimeError("Visitor does not accept object: %s" % obj)
            #print "Caching " + cls.__name__
            self.dispatch_table[cls] = handler_method
        return handler_method(obj)

class TreeVisitor(BasicVisitor):
    """
    Base class for writing visitors for a Cython tree, contains utilities for
    recursing such trees using visitors. Each node is
    expected to have a content iterable containing the names of attributes
    containing child nodes or lists of child nodes. Lists are not considered
    part of the tree structure (i.e. contained nodes are considered direct
    children of the parent node).
    
    visit_children visits each of the children of a given node (see the visit_children
    documentation). When recursing the tree using visit_children, an attribute
    access_path is maintained which gives information about the current location
    in the tree as a stack of tuples: (parent_node, attrname, index), representing
    the node, attribute and optional list index that was taken in each step in the path to
    the current node.
    
    Example:
    
    >>> class SampleNode(object):
    ...     child_attrs = ["head", "body"]
    ...     def __init__(self, value, head=None, body=None):
    ...         self.value = value
    ...         self.head = head
    ...         self.body = body
    ...     def __repr__(self): return "SampleNode(%s)" % self.value
    ...
    >>> tree = SampleNode(0, SampleNode(1), [SampleNode(2), SampleNode(3)])
    >>> class MyVisitor(TreeVisitor):
    ...     def visit_SampleNode(self, node):
    ...         print "in", node.value, self.access_path
    ...         self.visitchildren(node)
    ...         print "out", node.value
    ...
    >>> MyVisitor().visit(tree)
    in 0 []
    in 1 [(SampleNode(0), 'head', None)]
    out 1
    in 2 [(SampleNode(0), 'body', 0)]
    out 2
    in 3 [(SampleNode(0), 'body', 1)]
    out 3
    out 0
    """
    
    def __init__(self):
        super(TreeVisitor, self).__init__()
        self.access_path = []

    def __call__(self, tree):
        self.visit(tree)
        return tree

    def visit_Statement(self, node):
        self.visitchildren(node)
        return node

    def visitchild(self, child, parent, idx):
        self.access_path.append((parent, idx))
        result = self.visit(child)
        self.access_path.pop()
        return result

    def visitchildren(self, parent, attrs=None):
        """
        Visits the children of the given parent. If parent is None, returns
        immediately (returning None).
        
        The return value is a dictionary giving the results for each
        child (mapping the attribute name to either the return value
        or a list of return values (in the case of multiple children
        in an attribute)).
        """

        if parent is None: return None
        content = getattr(parent, 'content', None)
        if content is None or not isinstance(content, list):
            return None
        result = [self.visitchild(child, parent, idx) for (idx, child) in \
                enumerate(content)]
        return result

class PrintTree(TreeVisitor):

    def __init__(self):
        TreeVisitor.__init__(self)
        self._indent = ""

    def indent(self):
        self._indent += "  "

    def unindent(self):
        self._indent = self._indent[:-2]

    def visit_Statement(self, node):
        print("%s|%s" % (self._indent, type(node)))
        self.indent()
        self.visitchildren(node)
        self.unindent()
        return node

    def visit_TypeDeclarationStatement(self, node):
        print("%s %s" % (self._indent, node.name))
        return node

mangle_prefix = 'f2cy_'
valid_name = re.compile(r'[a-z]\w+$',re.I).match

class KindResolutionError(Exception):
    pass

class KindResolutionVisitor(TreeVisitor):

    def visit_SubProgramStatement(self, node):
        #FIXME: when a variable's type is
        # integer*8 :: a
        # the get_kind() is the default integer kind (i.e., '4')
        # while the selector is ('8', '').
        interface_var_names = node.args
        if isinstance(node, Function):
            interface_var_names += [node.result]
        for argname in interface_var_names:
            var = node.a.variables[argname]
            # print "%s: " % argname
            vkr = VarKindResolution(var)
            # print "    type_name   : %s" % vkr.type_name
            # print "    resolve_name: %s" % vkr.resolved_name
            # print "    scope_name  : %s" % vkr.defining_scope.name
            # print "    defining_var: %s" % vkr.defining_var
            # add vkr to the variable instance
            # XXX: a better way to do the below?
            var.f2cy_var_kind_res = vkr
        return node


class VarKindResolution(object):

    def __init__(self, variable):
        self.var = variable # the variable that will have the ktp resolved.
        self.type_name = None # type of the variable ('integer', 'real', 'complex', 'logical', 'character')
        self.resolved_name = None # name that will be used for the ktp in the wrapper.
        self.ktp_str = None # string-form of the ktp.
        self.defining_var = None # 'variable' (parameter) that defines the ktp.
        self.defining_scope = None # scope in which the defining_var is defined.

        self.type_name, self.resolved_name, self.ktp_str, self.defining_scope, self.defining_var =\
                self.init_from_var(self.var)


    def init_from_var(self, var):
        var_scope = var.typedecl.parent
        assert isinstance(var_scope, (SubProgramStatement, Module, Program))
        length, ktp = var.typedecl.selector
        type_name = var.typedecl.name.lower()

        resolve_name = ''

        if not ktp:
            return VarKindResolution.handle_default_ktp(length, type_name, var_scope, var)

        ktp_parse = VarKindResolution.parse_ktp(ktp)

        if isinstance(ktp_parse[0], int):
            ktp_str = str(ktp_parse[0])
            resolve_name = mangle_prefix+'const_'+ktp_str
            scope = var_scope
            var = None

        elif ktp_parse[0] == 'kind':
            ktp_str = ktp
            resolve_name = mangle_prefix+'kind_'+ktp_parse[1]
            scope = var_scope
            var = None

        elif ktp_parse[0] == 'selected_int_kind':
            resolve_name = mangle_prefix+'selected_int_kind_'+ktp_parse[1]
            ktp_str = ktp
            scope = var_scope
            var = None

        elif ktp_parse[0] == 'selected_real_kind':
            resolve_name = mangle_prefix+'selected_real_kind_'+ktp_parse[1]
            if len(ktp_parse) == 3:
                resolve_name += '_'+ktp_parse[2]
            ktp_str = ktp
            scope = var_scope
            var = None

        elif valid_name(ktp_parse[0]):
            # XXX TODO: still have to fill this in...
            raise NotImplementedError("kind-type-parameter '%s' is not resolvable yet" % ktp)
            lookup_name = ktp_parse[0]
            def_scope, var = find_defining_scope(var_scope, lookup_name)
            assert var.is_parameter()
            assert type(var.typedecl).name.lower() == 'integer'
            if def_scope is var_scope:
                # it's defined locally.
                # TODO: check this over...
                resolve_name = "%s_%s_%s" % (mangle_prefix, var_scope.name, var.name)
                # self.local_param_ktp.append((resolve_name, var.init))
            else:
                # it's defined in a module, possibly with a use-rename.
                resolve_name = "%s_%s_%s" % (mangle_prefix, var_scope.name, var.name)
                raise RuntimeError("finish here!!!")

        else:
            raise KindResolutionError("unable to resolve kind-type-parameter '%s'" % ktp)

        return (type_name, resolve_name, ktp_str, scope, var)

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
        if isinstance(ktp, int):
            import pdb; pdb.set_trace()
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
        import pdb; pdb.set_trace()
        raise KindResolutionError("unable to resolve kind-type-parameter '%s'" % ktp)

    @staticmethod
    def handle_default_ktp(length, type_name, node, var):
        length = str(length).strip()
        type_name = type_name.replace(' ','').lower()

        if length:
            warning("variable '%s' in '%s' declared with deprecated syntax, may not resolve kind-type-parameter." % (var.name, node.name))
            ktp_str = length
            resolve_name = mangle_prefix+ktp_str+type_name.replace(' ','_')+'_bytes'

        # the default types follow.
        elif type_name == 'doubleprecision':
            ktp_str = 'kind(1.0D0)'
            resolve_name = mangle_prefix+'default_'+type_name
            type_name = 'real'

        elif type_name == 'logical':
            ktp_str = 'kind(.true.)'
            resolve_name = mangle_prefix+'default_'+type_name
            type_name = 'integer'

        elif type_name == 'integer':
            ktp_str = 'kind(0)'
            resolve_name = mangle_prefix+'default_'+type_name

        elif type_name == 'real':
            ktp_str = 'kind(0.0)'
            resolve_name = mangle_prefix+'default_'+type_name

        elif type_name == 'character':
            ktp_str = "kind('a')"
            resolve_name = mangle_prefix+'default_'+type_name

        elif type_name == 'complex':
            ktp_str = 'kind((0.0,0.0))'
            resolve_name = mangle_prefix+'default_'+type_name

        else:
            raise KindResolutionError()

        scope = node
        var = None

        return (type_name, resolve_name, ktp_str, scope, var)

from Code import CompositeBlock, ModuleCode, SubProgramCode, SubroutineCode, ProgramCode, UtilityCode

class AutoConfigGenerator(TreeVisitor):

    def __init__(self, *args, **kwargs):
        TreeVisitor.__init__(self, *args, **kwargs)

        self.utility = UtilityCode()
        self.resolve_mod = ModuleCode()
        self.driver_prog = ProgramCode()

        self._init_toplevel()

        self.seen_mods = set()
        self.seen_subprograms = set()
        self.seen_resolved_names = set()
        self.resolve_subrs = {}
        local_ktp_subr = SubroutineCode(level=1)
        self.resolve_mod.add_subprogram_block(local_ktp_subr)
        self.resolve_subrs['local_ktp'] = local_ktp_subr

    def _init_toplevel(self):
        self.utility.root.put(lookup_mod_code,indent=True)
        self.resolve_mod.block_start.putln("module resolve_mod")
        self.resolve_mod.block_end.putln("end module resolve_mod")

        self.driver_prog.block_start.putln("program autoconfig")
        self.driver_prog.block_end.putln("end program autoconfig")

        self.resolve_mod.use_stmts.putln("use iso_c_binding")
        self.resolve_mod.use_stmts.putln("use lookup_types")

        self.driver_prog.use_stmts.putln("use resolve_mod")
        self.driver_prog.declarations.putln("integer :: fh_num, ch_num, iserr")

    def visit_SubProgramStatement(self, node):
        interface_var_names = node.args
        if isinstance(node, Function):
            interface_var_names += [node.result]
        for argname in interface_var_names:
            var = node.a.variables[argname]
            vkr = var.f2cy_var_kind_res
            if vkr.resolved_name in self.seen_resolved_names:
                continue
            self.seen_resolved_names.add(vkr.resolved_name)
            if vkr.defining_var is None:
                # it's a literal integer, or selected_*_kind() or kind() call...
                assert vkr.defining_scope is vkr.var.parent.parent, `vkr.defining_scope,vkr.var.parent`
                subr_code = self.resolve_subrs['local_ktp']
                self.put_scalar_int_code(subr_code, vkr)
        return node

    def put_scalar_int_code(self, subr_code, vkr):
        subr_code.executable_stmts.put(ktp_scalar_int_code % {
            'scalar_int_expr' : vkr.ktp_str,
            'type_name': vkr.type_name,
            'mapped_name' : vkr.resolved_name
            }, indent=True)



    def __call__(self, tree, fh):
        self.visit(tree)
        # write the utility code.
        self.utility.copyto(fh)
        # write the resove_mod code.
        self.driver_prog.executable_stmts.put(open_files_code,indent=True)
        for subr_code_name, subr_code in self.resolve_subrs.items():
            subr_code.block_start.putln("subroutine %s(fh_num, ch_num, iserr)" % subr_code_name)
            subr_code.block_end.putln("end subroutine %s" % subr_code_name)
            subr_code.declarations.putln("integer, intent(in) :: fh_num, ch_num")
            subr_code.declarations.putln("integer, intent(out) :: iserr")
            subr_code.declarations.putln("integer :: ktp")
            subr_code.declarations.putln("character(len=ktp_str_len) :: fort_ktp_str, c_type_str")
            # write the subroutine wrapper call inside the driver_prog
            self.driver_prog.executable_stmts.putln("call %s(fh_num, ch_num, iserr)" % subr_code_name)
            self.driver_prog.executable_stmts.putln("if (iserr .gt. 0) then")
            self.driver_prog.executable_stmts.putln("print *, \"an error occurred in the kind resolution\"")
            self.driver_prog.executable_stmts.putln("stop")
            self.driver_prog.executable_stmts.putln("end if")
        self.resolve_mod.copyto(fh)
        # write the driver_prog
        self.driver_prog.executable_stmts.put(close_files_code,indent=True)
        self.driver_prog.copyto(fh)

class FortranWrapperVisitor(TreeVisitor):

    def visit_SubProgramStatement(self, node):
        pass

class CHeaderVisitor(TreeVisitor):
    pass

class PxdVisitor(TreeVisitor):
    pass

autoconfig_header = """
module autoconfig_mod
  use iso_c_binding
  implicit none
"""

autoconfig_footer = """end module autoconfig_mod"""

open_files_code = """
fh_num = 17
ch_num = 18
open(unit=fh_num, file='autoconfig_mod.f95', status='REPLACE', form='FORMATTED', action='WRITE', iostat=iserr)
if (iserr .gt. 0) then
  print *, \"an error occured opening the file 'autoconfig_mod.f95', unable to continue\"
  stop
end if
open(unit=ch_num, file='autoconfig_header.h', status='REPLACE', form='FORMATTED', action='WRITE', iostat=iserr)
if (iserr .gt. 0) then
  print *, \"an error occured opening the file 'autoconfig_header.h', unable to continue\"
  stop
end if

write(unit=fh_num, fmt="(' ',A)") "module autoconfig_mod"
write(unit=fh_num, fmt="(' ',A)") "  use iso_c_binding"
write(unit=fh_num, fmt="(' ',A)") "  implicit none"

"""

close_files_code = """

write(unit=fh_num, fmt="(' ',A)") "end module autoconfig_mod"

close(unit=fh_num)
close(unit=ch_num)
"""


ktp_scalar_int_code = '''

ktp = %(scalar_int_expr)s
call lookup_%(type_name)s (ktp, fort_ktp_str, c_type_str, iserr)
if (iserr .gt. 0) return
write(unit=fh_num, fmt="(' ',2A)") "integer, parameter :: %(mapped_name)s = ", trim(adjustl(fort_ktp_str))
write(unit=ch_num, fmt="(' ',3A)") "typedef ", trim(adjustl(c_type_str)), " %(mapped_name)s;"
'''

lookup_mod_code = '''
module lookup_types
  use iso_c_binding
  implicit none

  integer, parameter :: ktp_str_len = 25
  
  contains


  subroutine lookup_real(real_kind, fort_ktp_str, c_type_str, iserr)
    use iso_c_binding
    implicit none
    integer, intent(in) :: real_kind 
    character(len=ktp_str_len), intent(out) :: fort_ktp_str, c_type_str
    integer, intent(out) :: iserr
    
    iserr = 0
    ! make sure kind .gt. 0
    if (real_kind .lt. 0) then
        ! set error condition
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    endif
    
    if (real_kind .eq. c_float) then
        fort_ktp_str = "c_float"
        c_type_str = "float"
        return
    else if (real_kind .eq. c_double) then
        fort_ktp_str = "c_double"
        c_type_str = "double"
        return
    else if (real_kind .eq. c_long_double) then
        fort_ktp_str = "c_long_double"
        c_type_str = "long double"
        return
    else
        ! No corresponding interoperable type, set error.
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    end if
    
  end subroutine lookup_real
  
  subroutine lookup_integer(int_kind, fort_ktp_str, c_type_str, iserr)
    use iso_c_binding
    implicit none
    integer, intent(in) :: int_kind 
    character(len=ktp_str_len), intent(out) :: fort_ktp_str, c_type_str
    integer, intent(out) :: iserr
    
    iserr = 0
    ! make sure kind .gt. 0
    if (int_kind .lt. 0) then
        ! set error condition
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    endif
    
    if (int_kind .eq. c_signed_char) then
        fort_ktp_str = "c_signed_char"
        c_type_str = "signed char"
        return
    else if (int_kind .eq. c_short) then
        fort_ktp_str = "c_short"
        c_type_str = "short int"
        return
    else if (int_kind .eq. c_int) then
        fort_ktp_str = "c_int"
        c_type_str = "int"
        return
    else if (int_kind .eq. c_long) then
        fort_ktp_str = "c_long"
        c_type_str = "long int"
        return
    else if (int_kind .eq. c_long_long) then
        ! XXX assumes C99 long long type exists
        fort_ktp_str = "c_long_long"
        c_type_str = "long long int"
        return
    else
        ! No corresponding interoperable type, set error.
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    end if
    
  end subroutine lookup_integer

  subroutine lookup_character(char_kind, fort_ktp_str, c_type_str, iserr)
    use iso_c_binding
    implicit none
    integer, intent(in) :: char_kind 
    character(len=ktp_str_len), intent(out) :: fort_ktp_str, c_type_str
    integer, intent(out) :: iserr
    
    iserr = 0
    ! make sure kind .gt. 0
    if (char_kind .lt. 0) then
        ! set error condition
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    endif
    
    if (char_kind .eq. c_char) then
        fort_ktp_str = "c_char"
        c_type_str = "char"
        return
    else
        ! No corresponding interoperable type, set error.
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    end if
    
  end subroutine lookup_character

  subroutine lookup_logical(log_kind, fort_ktp_str, c_type_str, iserr) 
    ! XXX assumes C99 _Bool.
    use iso_c_binding
    implicit none
    integer, intent(in) :: log_kind 
    character(len=ktp_str_len), intent(out) :: fort_ktp_str, c_type_str
    integer, intent(out) :: iserr
    
    iserr = 0
    ! make sure kind .gt. 0
    if (log_kind .lt. 0) then
        ! set error condition
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    endif
    
    if (log_kind .eq. c_bool) then
        fort_ktp_str = "c_bool"
        c_type_str = "_Bool"
        return
    else if (log_kind .eq. c_signed_char) then
        fort_ktp_str = "c_signed_char"
        c_type_str = "signed char"
        return
    else if (log_kind .eq. c_short) then
        fort_ktp_str = "c_short"
        c_type_str = "short int"
        return
    else if (log_kind .eq. c_int) then
        fort_ktp_str = "c_int"
        c_type_str = "int"
        return
    else if (log_kind .eq. c_long) then
        fort_ktp_str = "c_long"
        c_type_str = "long int"
        return
    else if (log_kind .eq. c_long_long) then
        ! XXX assumes C99 long long type exists
        fort_ktp_str = "c_long_long"
        c_type_str = "long long int"
        return
    else
        ! No corresponding interoperable type, set error.
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    end if
    
  end subroutine lookup_logical

  subroutine lookup_complex(complex_kind, fort_ktp_str, c_type_str, iserr)
    ! XXX assumes C99 _Complex.
    use iso_c_binding
    implicit none
    integer, intent(in) :: complex_kind 
    character(len=ktp_str_len), intent(out) :: fort_ktp_str, c_type_str
    integer, intent(out) :: iserr
    
    iserr = 0
    ! make sure kind .gt. 0
    if (complex_kind .lt. 0) then
        ! set error condition
        iserr = 1 
        fort_ktp_str = ""
        c_type_str = ""
        return
    endif
    
    if (complex_kind .eq. c_float_complex) then
        fort_ktp_str = "c_float_complex"
        c_type_str = "float _Complex"
        return
    else if (complex_kind .eq. c_double_complex) then
        fort_ktp_str = "c_double_complex"
        c_type_str = "double _Complex"
        return
    else if (complex_kind .eq. c_long_double_complex) then
        fort_ktp_str = "c_long_double_complex"
        c_type_str = "long double _Complex"
        return
    else
        ! No corresponding interoperable type, set error.
        iserr = 1
        fort_ktp_str = ""
        c_type_str = ""
        return
    end if
    
  end subroutine lookup_complex

end module lookup_types
'''

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # 'lookup_mod' : lookup_mod,
    # 'resolve_mod' : resolve_mod
    # 'proc_local_resolve' : proc_local_resolve
    # 'driver_program' : driver_program

    # lookup_mod is a single, unchanged block.

    # resolve mod is:
        # header
        # [module_resolve_subr]
        # proc_local_resolve
        # footer

    # each module_resolve_subr is:
        # header
        # body -> where the entries are written from above.
        # footer

    # the proc_local_resolve is:
        # header
        # body -> ditto.
        # footer

    # the driver program is:
        # header -> 'use' the resolve mod to pull in all module_resolve_subrs and proc_local_resolve
        # body -> call all the module_resolve_subrs, with error-handling.
        # footer


