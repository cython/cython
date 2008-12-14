#
#   Pyrex - Parse tree nodes
#

import string, sys, os, time, copy

import Code
from Errors import error, warning, InternalError
import Naming
import PyrexTypes
import TypeSlots
from PyrexTypes import py_object_type, error_type, CTypedefType, CFuncType
from Symtab import ModuleScope, LocalScope, GeneratorLocalScope, \
    StructOrUnionScope, PyClassScope, CClassScope
from Cython.Utils import open_new_file, replace_suffix, UtilityCode
from StringEncoding import EncodedString, escape_byte_string, split_docstring
import Options
import ControlFlow

from DebugFlags import debug_disposal_code

absolute_path_length = 0

def relative_position(pos):
    """
    We embed the relative filename in the generated C file, since we
    don't want to have to regnerate and compile all the source code
    whenever the Python install directory moves (which could happen,
    e.g,. when distributing binaries.)
    
    INPUT:
        a position tuple -- (absolute filename, line number column position)

    OUTPUT:
        relative filename
        line number

    AUTHOR: William Stein
    """
    global absolute_path_length
    if absolute_path_length==0:
        absolute_path_length = len(os.path.abspath(os.getcwd())) 
    return (pos[0].get_filenametable_entry()[absolute_path_length+1:], pos[1])

def embed_position(pos, docstring):
    if not Options.embed_pos_in_docstring:
        return docstring
    pos_line = u'File: %s (starting at line %s)' % relative_position(pos)
    if docstring is None:
        # unicode string
        return EncodedString(pos_line)

    # make sure we can encode the filename in the docstring encoding
    # otherwise make the docstring a unicode string
    encoding = docstring.encoding
    if encoding is not None:
        try:
            encoded_bytes = pos_line.encode(encoding)
        except UnicodeEncodeError:
            encoding = None

    if not docstring:
        # reuse the string encoding of the original docstring
        doc = EncodedString(pos_line)
    else:
        doc = EncodedString(pos_line + u'\n' + docstring)
    doc.encoding = encoding
    return doc

class Node(object):
    #  pos         (string, int, int)   Source file position
    #  is_name     boolean              Is a NameNode
    #  is_literal  boolean              Is a ConstNode
    
    is_name = 0
    is_literal = 0
    temps = None

    # All descandants should set child_attrs to a list of the attributes
    # containing nodes considered "children" in the tree. Each such attribute
    # can either contain a single node or a list of nodes. See Visitor.py.
    child_attrs = None
    
    def __init__(self, pos, **kw):
        self.pos = pos
        self.__dict__.update(kw)
    
    gil_message = "Operation"

    def gil_check(self, env):
        if env.nogil:
            self.gil_error()

    def gil_error(self):
        error(self.pos, "%s not allowed without gil" % self.gil_message)

    def clone_node(self):
        """Clone the node. This is defined as a shallow copy, except for member lists
           amongst the child attributes (from get_child_accessors) which are also
           copied. Lists containing child nodes are thus seen as a way for the node
           to hold multiple children directly; the list is not treated as a seperate
           level in the tree."""
        result = copy.copy(self)
        for attrname in result.child_attrs:
            value = getattr(result, attrname)
            if isinstance(value, list):
                setattr(result, attrname, [x for x in value])
        return result
    
    
    #
    #  There are 4 phases of parse tree processing, applied in order to
    #  all the statements in a given scope-block:
    #
    #  (0) analyse_control_flow
    #        Create the control flow tree into which state can be asserted and
    #        queried.
    #
    #  (1) analyse_declarations
    #        Make symbol table entries for all declarations at the current
    #        level, both explicit (def, cdef, etc.) and implicit (assignment
    #        to an otherwise undeclared name).
    #
    #  (2) analyse_expressions
    #         Determine the result types of expressions and fill in the
    #         'type' attribute of each ExprNode. Insert coercion nodes into the
    #         tree where needed to convert to and from Python objects. 
    #         Allocate temporary locals for intermediate results. Fill
    #         in the 'result_code' attribute of each ExprNode with a C code
    #         fragment.
    #
    #  (3) generate_code
    #         Emit C code for all declarations, statements and expressions.
    #         Recursively applies the 3 processing phases to the bodies of
    #         functions.
    #
    
    def analyse_control_flow(self, env):
        pass
    
    def analyse_declarations(self, env):
        pass
    
    def analyse_expressions(self, env):
        raise InternalError("analyse_expressions not implemented for %s" % \
            self.__class__.__name__)
    
    def generate_code(self, code):
        raise InternalError("generate_code not implemented for %s" % \
            self.__class__.__name__)
            
    def annotate(self, code):
        # mro does the wrong thing
        if isinstance(self, BlockNode):
            self.body.annotate(code)
            
    def end_pos(self):
        if not self.child_attrs:
            return self.pos
        try:
            return self._end_pos
        except AttributeError:
            pos = self.pos
            for attr in self.child_attrs:
                child = getattr(self, attr)
                # Sometimes lists, sometimes nodes
                if child is None:
                    pass
                elif isinstance(child, list):
                    for c in child:
                        pos = max(pos, c.end_pos())
                else:
                    pos = max(pos, child.end_pos())
            self._end_pos = pos
            return pos

    def dump(self, level=0, filter_out=("pos",), cutoff=100, encountered=None):
        if cutoff == 0:
            return "<...nesting level cutoff...>"
        if encountered is None:
            encountered = set()
        if id(self) in encountered:
            return "<%s (%d) -- already output>" % (self.__class__.__name__, id(self))
        encountered.add(id(self))
        
        def dump_child(x, level):
            if isinstance(x, Node):
                return x.dump(level, filter_out, cutoff-1, encountered)
            elif isinstance(x, list):
                return "[%s]" % ", ".join([dump_child(item, level) for item in x])
            else:
                return repr(x)
            
        
        attrs = [(key, value) for key, value in self.__dict__.iteritems() if key not in filter_out]
        if len(attrs) == 0:
            return "<%s (%d)>" % (self.__class__.__name__, id(self))
        else:
            indent = "  " * level
            res = "<%s (%d)\n" % (self.__class__.__name__, id(self))
            for key, value in attrs:
                res += "%s  %s: %s\n" % (indent, key, dump_child(value, level + 1))
            res += "%s>" % indent
            return res

class CompilerDirectivesNode(Node):
    """
    Sets compiler directives for the children nodes
    """
    #  directives     {string:value}  A dictionary holding the right value for
    #                                 *all* possible directives.
    #  body           Node
    child_attrs = ["body"]

    def analyse_control_flow(self, env):
        old = env.directives
        env.directives = self.directives
        self.body.analyse_control_flow(env)
        env.directives = old

    def analyse_declarations(self, env):
        old = env.directives
        env.directives = self.directives
        self.body.analyse_declarations(env)
        env.directives = old
    
    def analyse_expressions(self, env):
        old = env.directives
        env.directives = self.directives
        self.body.analyse_expressions(env)
        env.directives = old

    def generate_function_definitions(self, env, code):
        env_old = env.directives
        code_old = code.globalstate.directives
        code.globalstate.directives = self.directives
        self.body.generate_function_definitions(env, code)
        env.directives = env_old
        code.globalstate.directives = code_old
            
    def generate_execution_code(self, code):
        old = code.globalstate.directives
        code.globalstate.directives = self.directives
        self.body.generate_execution_code(code)
        code.globalstate.directives = old
            
    def annotate(self, code):
        old = code.globalstate.directives
        code.globalstate.directives = self.directives
        self.body.annotate(code)
        code.globalstate.directives = old
        
class BlockNode:
    #  Mixin class for nodes representing a declaration block.

    def generate_const_definitions(self, env, code):
        if env.const_entries:
            for entry in env.const_entries:
                if not entry.is_interned:
                    code.globalstate.add_const_definition(entry)

    def generate_interned_string_decls(self, env, code):
        entries = env.global_scope().new_interned_string_entries
        if entries:
            for entry in entries:
                code.globalstate.add_interned_string_decl(entry)
            del entries[:]

    def generate_py_string_decls(self, env, code):
        if env is None:
            return # earlier error
        entries = env.pystring_entries
        if entries:
            for entry in entries:
                if not entry.is_interned:
                    code.globalstate.add_py_string_decl(entry)

    def generate_interned_num_decls(self, env, code):
        #  Flush accumulated interned nums from the global scope
        #  and generate declarations for them.
        genv = env.global_scope()
        entries = genv.interned_nums
        if entries:
            for entry in entries:
                code.globalstate.add_interned_num_decl(entry)
            del entries[:]

    def generate_cached_builtins_decls(self, env, code):
        entries = env.global_scope().undeclared_cached_builtins
        for entry in entries:
            code.globalstate.add_cached_builtin_decl(entry)
        del entries[:]
        

class StatListNode(Node):
    # stats     a list of StatNode
    
    child_attrs = ["stats"]

    def create_analysed(pos, env, *args, **kw):
        node = StatListNode(pos, *args, **kw)
        return node # No node-specific analysis necesarry
    create_analysed = staticmethod(create_analysed)
    
    def analyse_control_flow(self, env):
        for stat in self.stats:
            stat.analyse_control_flow(env)

    def analyse_declarations(self, env):
        #print "StatListNode.analyse_declarations" ###
        for stat in self.stats:
            stat.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        #print "StatListNode.analyse_expressions" ###
        for stat in self.stats:
            stat.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        #print "StatListNode.generate_function_definitions" ###
        for stat in self.stats:
            stat.generate_function_definitions(env, code)
            
    def generate_execution_code(self, code):
        #print "StatListNode.generate_execution_code" ###
        for stat in self.stats:
            code.mark_pos(stat.pos)
            stat.generate_execution_code(code)
            
    def annotate(self, code):
        for stat in self.stats:
            stat.annotate(code)
    

class StatNode(Node):
    #
    #  Code generation for statements is split into the following subphases:
    #
    #  (1) generate_function_definitions
    #        Emit C code for the definitions of any structs,
    #        unions, enums and functions defined in the current
    #        scope-block.
    #
    #  (2) generate_execution_code
    #        Emit C code for executable statements.
    #
    
    def generate_function_definitions(self, env, code):
        pass
    
    def generate_execution_code(self, code):
        raise InternalError("generate_execution_code not implemented for %s" % \
            self.__class__.__name__)


class CDefExternNode(StatNode):
    #  include_file   string or None
    #  body           StatNode
    
    child_attrs = ["body"]
    
    def analyse_declarations(self, env):
        if self.include_file:
            env.add_include_file(self.include_file)
        old_cinclude_flag = env.in_cinclude
        env.in_cinclude = 1
        self.body.analyse_declarations(env)
        env.in_cinclude = old_cinclude_flag
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass

    def annotate(self, code):
        self.body.annotate(code)
        

class CDeclaratorNode(Node):
    # Part of a C declaration.
    #
    # Processing during analyse_declarations phase:
    #
    #   analyse
    #      Returns (name, type) pair where name is the
    #      CNameDeclaratorNode of the name being declared 
    #      and type is the type it is being declared as.
    #
    #  calling_convention  string   Calling convention of CFuncDeclaratorNode
    #                               for which this is a base 

    child_attrs = []

    calling_convention = ""


class CNameDeclaratorNode(CDeclaratorNode):
    #  name    string             The Pyrex name being declared
    #  cname   string or None     C name, if specified
    #  default ExprNode or None   the value assigned on declaration
    
    child_attrs = ['default']
    
    default = None
    
    def analyse(self, base_type, env, nonempty = 0):
        if nonempty and self.name == '':
            # May have mistaken the name for the type. 
            if base_type.is_ptr or base_type.is_array or base_type.is_buffer:
                error(self.pos, "Missing argument name")
            elif base_type.is_void:
                error(self.pos, "Use spam() rather than spam(void) to declare a function with no arguments.")
            else:
                self.name = base_type.declaration_code("", for_display=1, pyrex=1)
                base_type = py_object_type
        self.type = base_type
        return self, base_type
        
class CPtrDeclaratorNode(CDeclaratorNode):
    # base     CDeclaratorNode
    
    child_attrs = ["base"]

    def analyse(self, base_type, env, nonempty = 0):
        if base_type.is_pyobject:
            error(self.pos,
                "Pointer base type cannot be a Python object")
        ptr_type = PyrexTypes.c_ptr_type(base_type)
        return self.base.analyse(ptr_type, env, nonempty = nonempty)
        
class CArrayDeclaratorNode(CDeclaratorNode):
    # base        CDeclaratorNode
    # dimension   ExprNode

    child_attrs = ["base", "dimension"]
    
    def analyse(self, base_type, env, nonempty = 0):
        if self.dimension:
            self.dimension.analyse_const_expression(env)
            if not self.dimension.type.is_int:
                error(self.dimension.pos, "Array dimension not integer")
            size = self.dimension.result()
        else:
            size = None
        if not base_type.is_complete():
            error(self.pos,
                "Array element type '%s' is incomplete" % base_type)
        if base_type.is_pyobject:
            error(self.pos,
                "Array element cannot be a Python object")
        if base_type.is_cfunction:
            error(self.pos,
                "Array element cannot be a function")
        array_type = PyrexTypes.c_array_type(base_type, size)
        return self.base.analyse(array_type, env, nonempty = nonempty)


class CFuncDeclaratorNode(CDeclaratorNode):
    # base             CDeclaratorNode
    # args             [CArgDeclNode]
    # has_varargs      boolean
    # exception_value  ConstNode
    # exception_check  boolean    True if PyErr_Occurred check needed
    # nogil            boolean    Can be called without gil
    # with_gil         boolean    Acquire gil around function body
    
    child_attrs = ["base", "args", "exception_value"]

    overridable = 0
    optional_arg_count = 0

    def analyse(self, return_type, env, nonempty = 0):
        if nonempty:
            nonempty -= 1
        func_type_args = []
        for arg_node in self.args:
            name_declarator, type = arg_node.analyse(env, nonempty = nonempty)
            name = name_declarator.name
            if name_declarator.cname:
                error(self.pos, 
                    "Function argument cannot have C name specification")
            # Turn *[] argument into **
            if type.is_array:
                type = PyrexTypes.c_ptr_type(type.base_type)
            # Catch attempted C-style func(void) decl
            if type.is_void:
                error(arg_node.pos, "Use spam() rather than spam(void) to declare a function with no arguments.")
#            if type.is_pyobject and self.nogil:
#                error(self.pos,
#                    "Function with Python argument cannot be declared nogil")
            func_type_args.append(
                PyrexTypes.CFuncTypeArg(name, type, arg_node.pos))
            if arg_node.default:
                self.optional_arg_count += 1
            elif self.optional_arg_count:
                error(self.pos, "Non-default argument follows default argument")
        
        if self.optional_arg_count:
            scope = StructOrUnionScope()
            scope.declare_var('%sn' % Naming.pyrex_prefix, PyrexTypes.c_int_type, self.pos)
            for arg in func_type_args[len(func_type_args)-self.optional_arg_count:]:
                scope.declare_var(arg.name, arg.type, arg.pos, allow_pyobject = 1)
            struct_cname = env.mangle(Naming.opt_arg_prefix, self.base.name)
            self.op_args_struct = env.global_scope().declare_struct_or_union(name = struct_cname,
                                        kind = 'struct',
                                        scope = scope,
                                        typedef_flag = 0,
                                        pos = self.pos,
                                        cname = struct_cname)
            self.op_args_struct.defined_in_pxd = 1
            self.op_args_struct.used = 1
        
        exc_val = None
        exc_check = 0
        if return_type.is_pyobject \
            and (self.exception_value or self.exception_check) \
            and self.exception_check != '+':
                error(self.pos,
                    "Exception clause not allowed for function returning Python object")
        else:
            if self.exception_value:
                self.exception_value.analyse_const_expression(env)
                if self.exception_check == '+':
                    exc_val_type = self.exception_value.type
                    if not exc_val_type.is_error and \
                          not exc_val_type.is_pyobject and \
                          not (exc_val_type.is_cfunction and not exc_val_type.return_type.is_pyobject and len(exc_val_type.args)==0):
                        error(self.exception_value.pos,
                            "Exception value must be a Python exception or cdef function with no arguments.")
                    exc_val = self.exception_value
                else:
                    exc_val = self.exception_value.result()
                    if not return_type.assignable_from(self.exception_value.type):
                        error(self.exception_value.pos,
                            "Exception value incompatible with function return type")
            exc_check = self.exception_check
        if return_type.is_array:
            error(self.pos,
                "Function cannot return an array")
        if return_type.is_cfunction:
            error(self.pos,
                "Function cannot return a function")
        func_type = PyrexTypes.CFuncType(
            return_type, func_type_args, self.has_varargs, 
            optional_arg_count = self.optional_arg_count,
            exception_value = exc_val, exception_check = exc_check,
            calling_convention = self.base.calling_convention,
            nogil = self.nogil, with_gil = self.with_gil, is_overridable = self.overridable)
        if self.optional_arg_count:
            func_type.op_arg_struct = PyrexTypes.c_ptr_type(self.op_args_struct.type)
        return self.base.analyse(func_type, env)


class CArgDeclNode(Node):
    # Item in a function declaration argument list.
    #
    # base_type      CBaseTypeNode
    # declarator     CDeclaratorNode
    # not_none       boolean            Tagged with 'not None'
    # default        ExprNode or None
    # default_entry  Symtab.Entry       Entry for the variable holding the default value
    # default_result_code string        cname or code fragment for default value
    # is_self_arg    boolean            Is the "self" arg of an extension type method
    # is_kw_only     boolean            Is a keyword-only argument

    child_attrs = ["base_type", "declarator", "default"]

    is_self_arg = 0
    is_generic = 1
    type = None
    name_declarator = None

    def analyse(self, env, nonempty = 0):
        #print "CArgDeclNode.analyse: is_self_arg =", self.is_self_arg ###
        if self.type is None:
            # The parser may missinterpret names as types...
            # We fix that here.
            if isinstance(self.declarator, CNameDeclaratorNode) and self.declarator.name == '':
                if nonempty:
                    self.declarator.name = self.base_type.name
                    self.base_type.name = None
                    self.base_type.is_basic_c_type = False
                could_be_name = True
            else:
                could_be_name = False
            base_type = self.base_type.analyse(env, could_be_name = could_be_name)
            if hasattr(self.base_type, 'arg_name') and self.base_type.arg_name:
                self.declarator.name = self.base_type.arg_name
            return self.declarator.analyse(base_type, env, nonempty = nonempty)
        else:
            return self.name_declarator, self.type

    def annotate(self, code):
        if self.default:
            self.default.annotate(code)


class CBaseTypeNode(Node):
    # Abstract base class for C base type nodes.
    #
    # Processing during analyse_declarations phase:
    #
    #   analyse
    #     Returns the type.
    
    pass
    
class CAnalysedBaseTypeNode(Node):
    # type            type
    
    child_attrs = []
    
    def analyse(self, env, could_be_name = False):
        return self.type

class CSimpleBaseTypeNode(CBaseTypeNode):
    # name             string
    # module_path      [string]     Qualifying name components
    # is_basic_c_type  boolean
    # signed           boolean
    # longness         integer
    # is_self_arg      boolean      Is self argument of C method

    child_attrs = []
    arg_name = None   # in case the argument name was interpreted as a type
    
    def analyse(self, env, could_be_name = False):
        # Return type descriptor.
        #print "CSimpleBaseTypeNode.analyse: is_self_arg =", self.is_self_arg ###
        type = None
        if self.is_basic_c_type:
            type = PyrexTypes.simple_c_type(self.signed, self.longness, self.name)
            if not type:
                error(self.pos, "Unrecognised type modifier combination")
        elif self.name == "object" and not self.module_path:
            type = py_object_type
        elif self.name is None:
            if self.is_self_arg and env.is_c_class_scope:
                #print "CSimpleBaseTypeNode.analyse: defaulting to parent type" ###
                type = env.parent_type
            else:
                type = py_object_type
        else:
            if self.module_path:
                scope = env.find_imported_module(self.module_path, self.pos)
            else:
                scope = env
            if scope:
                if scope.is_c_class_scope:
                    scope = scope.global_scope()
                entry = scope.lookup(self.name)
                if entry and entry.is_type:
                    type = entry.type
                elif could_be_name:
                    if self.is_self_arg and env.is_c_class_scope:
                        type = env.parent_type
                    else:
                        type = py_object_type
                    self.arg_name = self.name
                else:
                    error(self.pos, "'%s' is not a type identifier" % self.name)
        if type:
            return type
        else:
            return PyrexTypes.error_type

class CBufferAccessTypeNode(CBaseTypeNode):
    #  After parsing:
    #  positional_args  [ExprNode]        List of positional arguments
    #  keyword_args     DictNode          Keyword arguments
    #  base_type_node   CBaseTypeNode

    #  After analysis:
    #  type             PyrexType.BufferType   ...containing the right options


    child_attrs = ["base_type_node", "positional_args",
                   "keyword_args", "dtype_node"]

    dtype_node = None
    
    def analyse(self, env, could_be_name = False):
        base_type = self.base_type_node.analyse(env)
        if base_type.is_error: return base_type
        import Buffer

        options = Buffer.analyse_buffer_options(
            self.pos,
            env,
            self.positional_args,
            self.keyword_args,
            base_type.buffer_defaults)
        
        self.type = PyrexTypes.BufferType(base_type, **options)
        return self.type

class CComplexBaseTypeNode(CBaseTypeNode):
    # base_type   CBaseTypeNode
    # declarator  CDeclaratorNode
    
    child_attrs = ["base_type", "declarator"]

    def analyse(self, env, could_be_name = False):
        base = self.base_type.analyse(env, could_be_name)
        _, type = self.declarator.analyse(base, env)
        return type


class CVarDefNode(StatNode):
    #  C variable definition or forward/extern function declaration.
    #
    #  visibility    'private' or 'public' or 'extern'
    #  base_type     CBaseTypeNode
    #  declarators   [CDeclaratorNode]
    #  in_pxd        boolean
    #  api           boolean
    #  need_properties [entry]

    child_attrs = ["base_type", "declarators"]
    need_properties = ()
    
    def analyse_declarations(self, env, dest_scope = None):
        if not dest_scope:
            dest_scope = env
        self.dest_scope = dest_scope
        base_type = self.base_type.analyse(env)
        if (dest_scope.is_c_class_scope
                and self.visibility == 'public' 
                and base_type.is_pyobject 
                and (base_type.is_builtin_type or base_type.is_extension_type)):
            self.need_properties = []
            need_property = True
            visibility = 'private'
        else:
            need_property = False
            visibility = self.visibility
            
        for declarator in self.declarators:
            name_declarator, type = declarator.analyse(base_type, env)
            if not type.is_complete():
                if not (self.visibility == 'extern' and type.is_array):
                    error(declarator.pos,
                        "Variable type '%s' is incomplete" % type)
            if self.visibility == 'extern' and type.is_pyobject:
                error(declarator.pos,
                    "Python object cannot be declared extern")
            name = name_declarator.name
            cname = name_declarator.cname
            if name == '':
                error(declarator.pos, "Missing name in declaration.")
                return
            if type.is_cfunction:
                entry = dest_scope.declare_cfunction(name, type, declarator.pos,
                    cname = cname, visibility = self.visibility, in_pxd = self.in_pxd,
                    api = self.api)
            else:
                if self.in_pxd and self.visibility != 'extern':
                    error(self.pos, 
                        "Only 'extern' C variable declaration allowed in .pxd file")
                entry = dest_scope.declare_var(name, type, declarator.pos,
                            cname = cname, visibility = visibility, is_cdef = 1)
                if need_property:
                    self.need_properties.append(entry)
                    entry.needs_property = 1
    

class CStructOrUnionDefNode(StatNode):
    #  name          string
    #  cname         string or None
    #  kind          "struct" or "union"
    #  typedef_flag  boolean
    #  visibility    "public" or "private"
    #  in_pxd        boolean
    #  attributes    [CVarDefNode] or None
    #  entry         Entry
    
    child_attrs = ["attributes"]

    def analyse_declarations(self, env):
        scope = None
        if self.attributes is not None:
            scope = StructOrUnionScope(self.name)
        self.entry = env.declare_struct_or_union(
            self.name, self.kind, scope, self.typedef_flag, self.pos,
            self.cname, visibility = self.visibility)
        need_typedef_indirection = False
        if self.attributes is not None:
            if self.in_pxd and not env.in_cinclude:
                self.entry.defined_in_pxd = 1
            for attr in self.attributes:
                attr.analyse_declarations(env, scope)
            if self.visibility != 'extern':
                for attr in scope.var_entries:
                    type = attr.type
                    while type.is_array:
                        type = type.base_type
                    if type == self.entry.type:
                        error(attr.pos, "Struct cannot contain itself as a member.")
                    if self.typedef_flag:
                        while type.is_ptr:
                            type = type.base_type
                        if type == self.entry.type:
                            need_typedef_indirection = True
            if need_typedef_indirection:
                # C can't handle typedef structs that refer to themselves. 
                struct_entry = self.entry
                cname = env.new_const_cname()
                self.entry = env.declare_typedef(self.name, struct_entry.type, self.pos, cname = self.cname, visibility='ignore')
                struct_entry.type.typedef_flag = False
                struct_entry.cname = struct_entry.type.cname = env.new_const_cname()
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class CEnumDefNode(StatNode):
    #  name           string or None
    #  cname          string or None
    #  items          [CEnumDefItemNode]
    #  typedef_flag   boolean
    #  visibility     "public" or "private"
    #  in_pxd         boolean
    #  entry          Entry
    
    child_attrs = ["items"]
    
    def analyse_declarations(self, env):
        self.entry = env.declare_enum(self.name, self.pos,
            cname = self.cname, typedef_flag = self.typedef_flag,
            visibility = self.visibility)
        if self.items is not None:
            if self.in_pxd and not env.in_cinclude:
                self.entry.defined_in_pxd = 1
            for item in self.items:
                item.analyse_declarations(env, self.entry)

    def analyse_expressions(self, env):
        if self.visibility == 'public':
            self.temp = env.allocate_temp_pyobject()
            env.release_temp(self.temp)
    
    def generate_execution_code(self, code):
        if self.visibility == 'public':
            for item in self.entry.enum_values:
                code.putln("%s = PyInt_FromLong(%s); %s" % (
                        self.temp,
                        item.cname,
                        code.error_goto_if_null(self.temp, item.pos)))
                code.putln('if (PyObject_SetAttrString(%s, "%s", %s) < 0) %s' % (
                        Naming.module_cname, 
                        item.name, 
                        self.temp,
                        code.error_goto(item.pos)))
                code.putln("%s = 0;" % self.temp)


class CEnumDefItemNode(StatNode):
    #  name     string
    #  cname    string or None
    #  value    ExprNode or None
    
    child_attrs = ["value"]

    def analyse_declarations(self, env, enum_entry):
        if self.value:
            self.value.analyse_const_expression(env)
            if not self.value.type.is_int:
                self.value = self.value.coerce_to(PyrexTypes.c_int_type, env)
                self.value.analyse_const_expression(env)
            value = self.value.result()
        else:
            value = self.name
        entry = env.declare_const(self.name, enum_entry.type, 
            value, self.pos, cname = self.cname, visibility = enum_entry.visibility)
        enum_entry.enum_values.append(entry)


class CTypeDefNode(StatNode):
    #  base_type    CBaseTypeNode
    #  declarator   CDeclaratorNode
    #  visibility   "public" or "private"
    #  in_pxd       boolean

    child_attrs = ["base_type", "declarator"]
    
    def analyse_declarations(self, env):
        base = self.base_type.analyse(env)
        name_declarator, type = self.declarator.analyse(base, env)
        name = name_declarator.name
        cname = name_declarator.cname
        entry = env.declare_typedef(name, type, self.pos,
            cname = cname, visibility = self.visibility)
        if self.in_pxd and not env.in_cinclude:
            entry.defined_in_pxd = 1
    
    def analyse_expressions(self, env):
        pass
    def generate_execution_code(self, code):
        pass


class FuncDefNode(StatNode, BlockNode):
    #  Base class for function definition nodes.
    #
    #  return_type     PyrexType
    #  #filename        string        C name of filename string const
    #  entry           Symtab.Entry
    #  needs_closure   boolean        Whether or not this function has inner functions/classes/yield
    
    py_func = None
    assmt = None
    needs_closure = False
    
    def analyse_default_values(self, env):
        genv = env.global_scope()
        for arg in self.args:
            if arg.default:
                if arg.is_generic:
                    if not hasattr(arg, 'default_entry'):
                        arg.default.analyse_types(env)
                        arg.default = arg.default.coerce_to(arg.type, genv)
                        if arg.default.is_literal:
                            arg.default_entry = arg.default
                            arg.default_result_code = arg.default.calculate_result_code()
                            if arg.default.type != arg.type and not arg.type.is_int:
                                arg.default_result_code = arg.type.cast_code(arg.default_result_code)
                        else:
                            arg.default.allocate_temps(genv)
                            arg.default_entry = genv.add_default_value(arg.type)
                            arg.default_entry.used = 1
                            arg.default_result_code = arg.default_entry.cname
                else:
                    error(arg.pos,
                        "This argument cannot have a default value")
                    arg.default = None
    
    def need_gil_acquisition(self, lenv):
        return 0
        
    def create_local_scope(self, env):
        genv = env
        while env.is_py_class_scope or env.is_c_class_scope:
            env = env.outer_scope
        if self.needs_closure:
            lenv = GeneratorLocalScope(name = self.entry.name, outer_scope = genv)
        else:
            lenv = LocalScope(name = self.entry.name, outer_scope = genv)
        lenv.return_type = self.return_type
        type = self.entry.type
        if type.is_cfunction:
            lenv.nogil = type.nogil and not type.with_gil
        self.local_scope = lenv
        return lenv
                
    def generate_function_definitions(self, env, code):
        import Buffer

        lenv = self.local_scope

        is_getbuffer_slot = (self.entry.name == "__getbuffer__" and
                             self.entry.scope.is_c_class_scope)

        # Generate C code for header and body of function
        code.enter_cfunc_scope()
        code.return_from_error_cleanup_label = code.new_label()
            
        # ----- Top-level constants used by this function
        code.mark_pos(self.pos)
        self.generate_interned_num_decls(lenv, code)
        self.generate_interned_string_decls(lenv, code)
        self.generate_py_string_decls(lenv, code)
        self.generate_cached_builtins_decls(lenv, code)
        #code.putln("")
        #code.put_var_declarations(lenv.const_entries, static = 1)
        self.generate_const_definitions(lenv, code)
        # ----- Function header
        code.putln("")
        if self.py_func:
            self.py_func.generate_function_header(code, 
                with_pymethdef = env.is_py_class_scope,
                proto_only=True)
        self.generate_function_header(code,
            with_pymethdef = env.is_py_class_scope)
        # ----- Local variable declarations
        lenv.mangle_closure_cnames(Naming.cur_scope_cname)
        self.generate_argument_declarations(lenv, code)
        if self.needs_closure:
            code.putln("/* TODO: declare and create scope object */")
        code.put_var_declarations(lenv.var_entries)
        init = ""
        if not self.return_type.is_void:
            code.putln(
                "%s%s;" % 
                    (self.return_type.declaration_code(
                        Naming.retval_cname),
                    init))
        tempvardecl_code = code.insertion_point()
        self.generate_keyword_list(code)
        # ----- Extern library function declarations
        lenv.generate_library_function_declarations(code)
        # ----- GIL acquisition
        acquire_gil = self.need_gil_acquisition(lenv)
        if acquire_gil:
            code.putln("PyGILState_STATE _save = PyGILState_Ensure();")
        # ----- Automatic lead-ins for certain special functions
        if is_getbuffer_slot:
            self.getbuffer_init(code)
        # ----- Fetch arguments
        self.generate_argument_parsing_code(env, code)
        # If an argument is assigned to in the body, we must 
        # incref it to properly keep track of refcounts.
        for entry in lenv.arg_entries:
            if entry.type.is_pyobject and lenv.control_flow.get_state((entry.name, 'source')) != 'arg':
                code.put_var_incref(entry)
        # ----- Initialise local variables 
        for entry in lenv.var_entries:
            if entry.type.is_pyobject and entry.init_to_none and entry.used:
                code.put_init_var_to_py_none(entry)
        # ----- Initialise local buffer auxiliary variables
        for entry in lenv.var_entries + lenv.arg_entries:
            if entry.type.is_buffer and entry.buffer_aux.buffer_info_var.used:
                code.putln("%s.buf = NULL;" % entry.buffer_aux.buffer_info_var.cname)
        # ----- Check and convert arguments
        self.generate_argument_type_tests(code)
        # ----- Acquire buffer arguments
        for entry in lenv.arg_entries:
            if entry.type.is_buffer:
                Buffer.put_acquire_arg_buffer(entry, code, self.pos)        
        # ----- Function body
        self.body.generate_execution_code(code)
        # ----- Default return value
        code.putln("")
        if self.return_type.is_pyobject:
            #if self.return_type.is_extension_type:
            #	lhs = "(PyObject *)%s" % Naming.retval_cname
            #else:
            lhs = Naming.retval_cname
            code.put_init_to_py_none(lhs, self.return_type)
        else:
            val = self.return_type.default_value
            if val:
                code.putln("%s = %s;" % (Naming.retval_cname, val))
        # ----- Error cleanup
        if code.error_label in code.labels_used:
            code.put_goto(code.return_label)
            code.put_label(code.error_label)
            code.put_var_xdecrefs(lenv.temp_entries)

            # Clean up buffers -- this calls a Python function
            # so need to save and restore error state
            buffers_present = len(lenv.buffer_entries) > 0
            if buffers_present:
                code.globalstate.use_utility_code(restore_exception_utility_code)
                code.putln("{ PyObject *__pyx_type, *__pyx_value, *__pyx_tb;")
                code.putln("__Pyx_ErrFetch(&__pyx_type, &__pyx_value, &__pyx_tb);")
                for entry in lenv.buffer_entries:
                    code.putln("%s;" % Buffer.get_release_buffer_code(entry))
                    #code.putln("%s = 0;" % entry.cname)
                code.putln("__Pyx_ErrRestore(__pyx_type, __pyx_value, __pyx_tb);}")

            err_val = self.error_value()
            exc_check = self.caller_will_check_exceptions()
            if err_val is not None or exc_check:
                code.putln('__Pyx_AddTraceback("%s");' % self.entry.qualified_name)
            else:
                warning(self.entry.pos, "Unraisable exception in function '%s'." \
                            % self.entry.qualified_name, 0)
                code.putln(
                    '__Pyx_WriteUnraisable("%s");' % 
                        self.entry.qualified_name)
                env.use_utility_code(unraisable_exception_utility_code)
                env.use_utility_code(restore_exception_utility_code)
            default_retval = self.return_type.default_value
            if err_val is None and default_retval:
                err_val = default_retval
            if err_val is not None:
                code.putln(
                    "%s = %s;" % (
                        Naming.retval_cname, 
                        err_val))

            if is_getbuffer_slot:
                self.getbuffer_error_cleanup(code)

            # If we are using the non-error cleanup section we should
            # jump past it if we have an error. The if-test below determine
            # whether this section is used.
            if buffers_present or is_getbuffer_slot:
                code.put_goto(code.return_from_error_cleanup_label)


        # ----- Non-error return cleanup
        # If you add anything here, remember to add a condition to the
        # if-test above in the error block (so that it can jump past this
        # block).
        code.put_label(code.return_label)
        for entry in lenv.buffer_entries:
            if entry.used:
                code.putln("%s;" % Buffer.get_release_buffer_code(entry))
        if is_getbuffer_slot:
            self.getbuffer_normal_cleanup(code)
        # ----- Return cleanup for both error and no-error return
        code.put_label(code.return_from_error_cleanup_label)
        if not Options.init_local_none:
            for entry in lenv.var_entries:
                if lenv.control_flow.get_state((entry.name, 'initalized')) is not True:
                    entry.xdecref_cleanup = 1
        code.put_var_decrefs(lenv.var_entries, used_only = 1)
        # Decref any increfed args
        for entry in lenv.arg_entries:
            if entry.type.is_pyobject and lenv.control_flow.get_state((entry.name, 'source')) != 'arg':
                code.put_var_decref(entry)
        if acquire_gil:
            code.putln("PyGILState_Release(_save);")
        # code.putln("/* TODO: decref scope object */")
        # ----- Return
        if not self.return_type.is_void:
            code.putln("return %s;" % Naming.retval_cname)
        code.putln("}")
        # ----- Go back and insert temp variable declarations
        tempvardecl_code.put_var_declarations(lenv.temp_entries)
        tempvardecl_code.put_temp_declarations(code.funcstate)
        # ----- Python version
        code.exit_cfunc_scope()
        if self.py_func:
            self.py_func.generate_function_definitions(env, code)
        self.generate_wrapper_functions(code)

    def declare_argument(self, env, arg):
        if arg.type.is_void:
            error(arg.pos, "Invalid use of 'void'")
        elif not arg.type.is_complete() and not arg.type.is_array:
            error(arg.pos,
                "Argument type '%s' is incomplete" % arg.type)
        return env.declare_arg(arg.name, arg.type, arg.pos)
        
    def generate_wrapper_functions(self, code):
        pass

    def generate_execution_code(self, code):
        # Evaluate and store argument default values
        for arg in self.args:
            default = arg.default
            if default:
                if not default.is_literal:
                    default.generate_evaluation_code(code)
                    default.make_owned_reference(code)
                    code.putln(
                        "%s = %s;" % (
                            arg.default_entry.cname,
                            default.result_as(arg.default_entry.type)))
                    if default.is_temp and default.type.is_pyobject:
                        code.putln(
                            "%s = 0;" %
                                default.result())
        # For Python class methods, create and store function object
        if self.assmt:
            self.assmt.generate_execution_code(code)

    #
    # Special code for the __getbuffer__ function
    #
    def getbuffer_init(self, code):
        info = self.local_scope.arg_entries[1].cname
        # Python 3.0 betas have a bug in memoryview which makes it call
        # getbuffer with a NULL parameter. For now we work around this;
        # the following line should be removed when this bug is fixed.
        code.putln("if (%s == NULL) return 0;" % info) 
        code.putln("%s->obj = Py_None; Py_INCREF(Py_None);" % info)

    def getbuffer_error_cleanup(self, code):
        info = self.local_scope.arg_entries[1].cname
        code.putln("Py_DECREF(%s->obj); %s->obj = NULL;" %
                   (info, info))

    def getbuffer_normal_cleanup(self, code):
        info = self.local_scope.arg_entries[1].cname
        code.putln("if (%s->obj == Py_None) { Py_DECREF(Py_None); %s->obj = NULL; }" %
                   (info, info))

class CFuncDefNode(FuncDefNode):
    #  C function definition.
    #
    #  modifiers     ['inline']
    #  visibility    'private' or 'public' or 'extern'
    #  base_type     CBaseTypeNode
    #  declarator    CDeclaratorNode
    #  body          StatListNode
    #  api           boolean
    #
    #  with_gil      boolean    Acquire GIL around body
    #  type          CFuncType
    #  py_func       wrapper for calling from Python
    #  overridable   whether or not this is a cpdef function
    
    child_attrs = ["base_type", "declarator", "body", "py_func"]
    
    def unqualified_name(self):
        return self.entry.name
        
    def analyse_declarations(self, env):
        if 'locals' in env.directives:
            directive_locals = env.directives['locals']
        else:
            directive_locals = {}
        self.directive_locals = directive_locals
        base_type = self.base_type.analyse(env)
        # The 2 here is because we need both function and argument names. 
        name_declarator, type = self.declarator.analyse(base_type, env, nonempty = 2 * (self.body is not None))
        if not type.is_cfunction:
            error(self.pos, 
                "Suite attached to non-function declaration")
        # Remember the actual type according to the function header
        # written here, because the type in the symbol table entry
        # may be different if we're overriding a C method inherited
        # from the base type of an extension type.
        self.type = type
        type.is_overridable = self.overridable
        declarator = self.declarator
        while not hasattr(declarator, 'args'):
            declarator = declarator.base
        self.args = declarator.args
        for formal_arg, type_arg in zip(self.args, type.args):
            formal_arg.type = type_arg.type
            formal_arg.cname = type_arg.cname
        name = name_declarator.name
        cname = name_declarator.cname
        self.entry = env.declare_cfunction(
            name, type, self.pos, 
            cname = cname, visibility = self.visibility,
            defining = self.body is not None,
            api = self.api)
        self.return_type = type.return_type
        
        if self.overridable:
            import ExprNodes
            py_func_body = self.call_self_node(is_module_scope = env.is_module_scope)
            self.py_func = DefNode(pos = self.pos, 
                                   name = self.entry.name,
                                   args = self.args,
                                   star_arg = None,
                                   starstar_arg = None,
                                   doc = self.doc,
                                   body = py_func_body,
                                   is_wrapper = 1)
            self.py_func.is_module_scope = env.is_module_scope
            self.py_func.analyse_declarations(env)
            self.entry.as_variable = self.py_func.entry
            # Reset scope entry the above cfunction
            env.entries[name] = self.entry
            self.py_func.interned_attr_cname = env.intern_identifier(
                self.py_func.entry.name)
            if not env.is_module_scope or Options.lookup_module_cpdef:
                self.override = OverrideCheckNode(self.pos, py_func = self.py_func)
                self.body = StatListNode(self.pos, stats=[self.override, self.body])
    
    def call_self_node(self, omit_optional_args=0, is_module_scope=0):
        import ExprNodes
        args = self.type.args
        if omit_optional_args:
            args = args[:len(args) - self.type.optional_arg_count]
        arg_names = [arg.name for arg in args]
        if is_module_scope:
            cfunc = ExprNodes.NameNode(self.pos, name=self.entry.name)
        else:
            self_arg = ExprNodes.NameNode(self.pos, name=arg_names[0])
            cfunc = ExprNodes.AttributeNode(self.pos, obj=self_arg, attribute=self.entry.name)
        skip_dispatch = not is_module_scope or Options.lookup_module_cpdef
        c_call = ExprNodes.SimpleCallNode(self.pos, function=cfunc, args=[ExprNodes.NameNode(self.pos, name=n) for n in arg_names[1-is_module_scope:]], wrapper_call=skip_dispatch)
        return ReturnStatNode(pos=self.pos, return_type=PyrexTypes.py_object_type, value=c_call)
    
    def declare_arguments(self, env):
        for arg in self.type.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            self.declare_argument(env, arg)
            
    def need_gil_acquisition(self, lenv):
        type = self.type
        with_gil = self.type.with_gil
        if type.nogil and not with_gil:
            if type.return_type.is_pyobject:
                error(self.pos,
                      "Function with Python return type cannot be declared nogil")
            for entry in lenv.var_entries + lenv.temp_entries:
                if entry.type.is_pyobject:
                    error(self.pos, "Function declared nogil has Python locals or temporaries")
        return with_gil

    def analyse_expressions(self, env):
        self.analyse_default_values(env)
        if self.overridable:
            self.py_func.analyse_expressions(env)

    def generate_function_header(self, code, with_pymethdef, with_opt_args = 1, with_dispatch = 1, cname = None):
        arg_decls = []
        type = self.type
        visibility = self.entry.visibility
        for arg in type.args[:len(type.args)-type.optional_arg_count]:
            arg_decls.append(arg.declaration_code())
        if with_dispatch and self.overridable:
            arg_decls.append(PyrexTypes.c_int_type.declaration_code(Naming.skip_dispatch_cname))
        if type.optional_arg_count and with_opt_args:
            arg_decls.append(type.op_arg_struct.declaration_code(Naming.optional_args_cname))
        if type.has_varargs:
            arg_decls.append("...")
        if not arg_decls:
            arg_decls = ["void"]
        if cname is None:
            cname = self.entry.func_cname
        entity = type.function_header_code(cname, string.join(arg_decls, ", "))
        if visibility == 'public':
            dll_linkage = "DL_EXPORT"
        else:
            dll_linkage = None
        header = self.return_type.declaration_code(entity,
            dll_linkage = dll_linkage)
        if visibility == 'extern':
            storage_class = "%s " % Naming.extern_c_macro
        elif visibility == 'public':
            storage_class = ""
        else:
            storage_class = "static "
        code.putln("%s%s %s {" % (
            storage_class,
            ' '.join(self.modifiers).upper(), # macro forms 
            header))

    def generate_argument_declarations(self, env, code):
        for arg in self.args:
            if arg.default:
                    code.putln('%s = %s;' % (arg.type.declaration_code(arg.cname), arg.default_result_code))

    def generate_keyword_list(self, code):
        pass
        
    def generate_argument_parsing_code(self, env, code):
        i = 0
        if self.type.optional_arg_count:
            code.putln('if (%s) {' % Naming.optional_args_cname)
            for arg in self.args:
                if arg.default:
                    code.putln('if (%s->%sn > %s) {' % (Naming.optional_args_cname, Naming.pyrex_prefix, i))
                    declarator = arg.declarator
                    while not hasattr(declarator, 'name'):
                        declarator = declarator.base
                    code.putln('%s = %s->%s;' % (arg.cname, Naming.optional_args_cname, declarator.name))
                    i += 1
            for _ in range(self.type.optional_arg_count):
                code.putln('}')
            code.putln('}')
    
    def generate_argument_conversion_code(self, code):
        pass
    
    def generate_argument_type_tests(self, code):
        # Generate type tests for args whose type in a parent
        # class is a supertype of the declared type.
        for arg in self.type.args:
            if arg.needs_type_test:
                self.generate_arg_type_test(arg, code)
    
    def generate_arg_type_test(self, arg, code):
        # Generate type test for one argument.
        if arg.type.typeobj_is_available():
            typeptr_cname = arg.type.typeptr_cname
            arg_code = "((PyObject *)%s)" % arg.cname
            code.putln(
                'if (unlikely(!__Pyx_ArgTypeTest(%s, %s, %d, "%s", %s))) %s' % (
                    arg_code, 
                    typeptr_cname,
                    not arg.not_none,
                    arg.name,
                    type.is_builtin_type,
                    code.error_goto(arg.pos)))
        else:
            error(arg.pos, "Cannot test type of extern C class "
                "without type object name specification")

    def error_value(self):
        if self.return_type.is_pyobject:
            return "0"
        else:
            #return None
            return self.entry.type.exception_value
            
    def caller_will_check_exceptions(self):
        return self.entry.type.exception_check
        
    def generate_wrapper_functions(self, code):
        # If the C signature of a function has changed, we need to generate
        # wrappers to put in the slots here. 
        k = 0
        entry = self.entry
        func_type = entry.type
        while entry.prev_entry is not None:
            k += 1
            entry = entry.prev_entry
            entry.func_cname = "%s%swrap_%s" % (self.entry.func_cname, Naming.pyrex_prefix, k)
            code.putln()
            self.generate_function_header(code, 
                                          0,
                                          with_dispatch = entry.type.is_overridable, 
                                          with_opt_args = entry.type.optional_arg_count, 
                                          cname = entry.func_cname)
            if not self.return_type.is_void:
                code.put('return ')
            args = self.type.args
            arglist = [arg.cname for arg in args[:len(args)-self.type.optional_arg_count]]
            if entry.type.is_overridable:
                arglist.append(Naming.skip_dispatch_cname)
            elif func_type.is_overridable:
                arglist.append('0')
            if entry.type.optional_arg_count:
                arglist.append(Naming.optional_args_cname)
            elif func_type.optional_arg_count:
                arglist.append('NULL')
            code.putln('%s(%s);' % (self.entry.func_cname, ', '.join(arglist)))
            code.putln('}')
        

class PyArgDeclNode(Node):
    # Argument which must be a Python object (used
    # for * and ** arguments).
    #
    # name   string
    # entry  Symtab.Entry
    child_attrs = []
    

class DecoratorNode(Node):
    # A decorator
    #
    # decorator    NameNode or CallNode
    child_attrs = ['decorator']


class DefNode(FuncDefNode):
    # A Python function definition.
    #
    # name          string                 the Python name of the function
    # decorators    [DecoratorNode]        list of decorators
    # args          [CArgDeclNode]         formal arguments
    # star_arg      PyArgDeclNode or None  * argument
    # starstar_arg  PyArgDeclNode or None  ** argument
    # doc           EncodedString or None
    # body          StatListNode
    #
    #  The following subnode is constructed internally
    #  when the def statement is inside a Python class definition.
    #
    #  assmt   AssignmentNode   Function construction/assignment
    
    child_attrs = ["args", "star_arg", "starstar_arg", "body", "decorators"]

    assmt = None
    num_kwonly_args = 0
    num_required_kw_args = 0
    reqd_kw_flags_cname = "0"
    is_wrapper = 0
    decorators = None
    entry = None
    

    def __init__(self, pos, **kwds):
        FuncDefNode.__init__(self, pos, **kwds)
        k = rk = r = 0
        for arg in self.args:
            if arg.kw_only:
                k += 1
                if not arg.default:
                    rk += 1
            if not arg.default:
                r += 1
        self.num_kwonly_args = k
        self.num_required_kw_args = rk
        self.num_required_args = r
        
    def as_cfunction(self, cfunc):
        if self.star_arg:
            error(self.star_arg.pos, "cdef function cannot have star argument")
        if self.starstar_arg:
            error(self.starstar_arg.pos, "cdef function cannot have starstar argument")
        if len(self.args) != len(cfunc.type.args) or cfunc.type.has_varargs:
            error(self.pos, "wrong number of arguments")
            error(declarator.pos, "previous declaration here")
        for formal_arg, type_arg in zip(self.args, cfunc.type.args):
            name_declarator, type = formal_arg.analyse(cfunc.scope, nonempty=1)
            if type is PyrexTypes.py_object_type or formal_arg.is_self:
                formal_arg.type = type_arg.type
                formal_arg.name_declarator = name_declarator
        import ExprNodes
        if cfunc.type.exception_value is None:
            exception_value = None
        else:
            exception_value = ExprNodes.ConstNode(self.pos, value=cfunc.type.exception_value, type=cfunc.type.return_type)
        declarator = CFuncDeclaratorNode(self.pos, 
                                         base = CNameDeclaratorNode(self.pos, name=self.name, cname=None),
                                         args = self.args,
                                         has_varargs = False,
                                         exception_check = cfunc.type.exception_check,
                                         exception_value = exception_value,
                                         with_gil = cfunc.type.with_gil,
                                         nogil = cfunc.type.nogil)
        return CFuncDefNode(self.pos, 
                            modifiers = [],
                            base_type = CAnalysedBaseTypeNode(self.pos, type=cfunc.type.return_type),
                            declarator = declarator,
                            body = self.body,
                            doc = self.doc,
                            overridable = cfunc.type.is_overridable,
                            type = cfunc.type,
                            with_gil = cfunc.type.with_gil,
                            nogil = cfunc.type.nogil,
                            visibility = 'private',
                            api = False)
    
    def analyse_declarations(self, env):
        if 'locals' in env.directives:
            directive_locals = env.directives['locals']
        else:
            directive_locals = {}
        self.directive_locals = directive_locals
        for arg in self.args:
            base_type = arg.base_type.analyse(env)
            name_declarator, type = \
                arg.declarator.analyse(base_type, env)
            arg.name = name_declarator.name
            if arg.name in directive_locals:
                type_node = directive_locals[arg.name]
                other_type = type_node.analyse_as_type(env)
                if other_type is None:
                    error(type_node.pos, "Not a type")
                elif (type is not PyrexTypes.py_object_type 
                        and not type.same_as(other_type)):
                    error(arg.base_type.pos, "Signature does not agree with previous declaration")
                    error(type_node.pos, "Previous declaration here")
                else:
                    type = other_type
            if name_declarator.cname:
                error(self.pos,
                    "Python function argument cannot have C name specification")
            arg.type = type.as_argument_type()
            arg.hdr_type = None
            arg.needs_conversion = 0
            arg.needs_type_test = 0
            arg.is_generic = 1
            if arg.not_none and not arg.type.is_extension_type:
                error(self.pos,
                    "Only extension type arguments can have 'not None'")
        self.declare_pyfunction(env)
        self.analyse_signature(env)
        self.return_type = self.entry.signature.return_type()

    def analyse_signature(self, env):
        any_type_tests_needed = 0
        # Use the simpler calling signature for zero- and one-argument functions.
        if not self.entry.is_special and not self.star_arg and not self.starstar_arg:
            if self.entry.signature is TypeSlots.pyfunction_signature and Options.optimize_simple_methods:
                if len(self.args) == 0:
                    self.entry.signature = TypeSlots.pyfunction_noargs
                elif len(self.args) == 1:
                    if self.args[0].default is None and not self.args[0].kw_only:
                        self.entry.signature = TypeSlots.pyfunction_onearg
            elif self.entry.signature is TypeSlots.pymethod_signature:
                if len(self.args) == 1:
                    self.entry.signature = TypeSlots.unaryfunc
                elif len(self.args) == 2:
                    if self.args[1].default is None and not self.args[1].kw_only:
                        self.entry.signature = TypeSlots.ibinaryfunc
        elif self.entry.is_special:
            self.entry.trivial_signature = len(self.args) == 1 and not (self.star_arg or self.starstar_arg)
        sig = self.entry.signature
        nfixed = sig.num_fixed_args()
        for i in range(nfixed):
            if i < len(self.args):
                arg = self.args[i]
                arg.is_generic = 0
                if sig.is_self_arg(i):
                    arg.is_self_arg = 1
                    arg.hdr_type = arg.type = env.parent_type
                    arg.needs_conversion = 0
                else:
                    arg.hdr_type = sig.fixed_arg_type(i)
                    if not arg.type.same_as(arg.hdr_type):
                        if arg.hdr_type.is_pyobject and arg.type.is_pyobject:
                            arg.needs_type_test = 1
                            any_type_tests_needed = 1
                        else:
                            arg.needs_conversion = 1
                if arg.needs_conversion:
                    arg.hdr_cname = Naming.arg_prefix + arg.name
                else:
                    arg.hdr_cname = Naming.var_prefix + arg.name
            else:
                self.bad_signature()
                return
        if nfixed < len(self.args):
            if not sig.has_generic_args:
                self.bad_signature()
            for arg in self.args:
                if arg.is_generic and \
                        (arg.type.is_extension_type or arg.type.is_builtin_type):
                    arg.needs_type_test = 1
                    any_type_tests_needed = 1
                elif arg.type is PyrexTypes.c_py_ssize_t_type:
                    # Want to use __index__ rather than __int__ method
                    # that PyArg_ParseTupleAndKeywords calls
                    arg.needs_conversion = 1
                    arg.hdr_type = PyrexTypes.py_object_type
                    arg.hdr_cname = Naming.arg_prefix + arg.name
        if any_type_tests_needed:
            env.use_utility_code(arg_type_test_utility_code)
    
    def bad_signature(self):
        sig = self.entry.signature
        expected_str = "%d" % sig.num_fixed_args()
        if sig.has_generic_args:
            expected_str = expected_str + " or more"
        name = self.name
        if name.startswith("__") and name.endswith("__"):
            desc = "Special method"
        else:
            desc = "Method"
        error(self.pos,
            "%s %s has wrong number of arguments "
            "(%d declared, %s expected)" % (
                desc, self.name, len(self.args), expected_str))

    def signature_has_nongeneric_args(self):
        argcount = len(self.args)
        if argcount == 0 or (argcount == 1 and self.args[0].is_self_arg):
            return 0
        return 1

    def signature_has_generic_args(self):
        return self.entry.signature.has_generic_args
    
    def declare_pyfunction(self, env):
        #print "DefNode.declare_pyfunction:", self.name, "in", env ###
        name = self.name
        entry = env.lookup_here(self.name)
        if entry and entry.type.is_cfunction and not self.is_wrapper:
            warning(self.pos, "Overriding cdef method with def method.", 5)
        entry = env.declare_pyfunction(self.name, self.pos)
        self.entry = entry
        prefix = env.scope_prefix
        entry.func_cname = \
            Naming.pyfunc_prefix + prefix + name
        entry.pymethdef_cname = \
            Naming.pymethdef_prefix + prefix + name
        if Options.docstrings:
            entry.doc = embed_position(self.pos, self.doc)
            entry.doc_cname = \
                Naming.funcdoc_prefix + prefix + name
        else:
            entry.doc = None

    def declare_arguments(self, env):
        for arg in self.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            if arg.needs_conversion:
                arg.entry = env.declare_var(arg.name, arg.type, arg.pos)
                env.control_flow.set_state((), (arg.name, 'source'), 'arg')
                env.control_flow.set_state((), (arg.name, 'initalized'), True)
                if arg.type.is_pyobject:
                    arg.entry.init = "0"
                arg.entry.init_to_none = 0
            else:
                arg.entry = self.declare_argument(env, arg)
            arg.entry.used = 1
            arg.entry.is_self_arg = arg.is_self_arg
            if not arg.is_self_arg:
                arg.name_entry = env.get_string_const(
                    arg.name, identifier = True)
                env.add_py_string(arg.name_entry, identifier = True)
            if arg.hdr_type:
                if arg.is_self_arg or \
                    (arg.type.is_extension_type and not arg.hdr_type.is_extension_type):
                        arg.entry.is_declared_generic = 1
        self.declare_python_arg(env, self.star_arg)
        self.declare_python_arg(env, self.starstar_arg)

    def declare_python_arg(self, env, arg):
        if arg:
            entry = env.declare_var(arg.name, 
                PyrexTypes.py_object_type, arg.pos)
            entry.used = 1
            entry.init = "0"
            entry.init_to_none = 0
            entry.xdecref_cleanup = 1
            arg.entry = entry
            env.control_flow.set_state((), (arg.name, 'initalized'), True)
            
    def analyse_expressions(self, env):
        self.analyse_default_values(env)
        if env.is_py_class_scope:
            self.synthesize_assignment_node(env)
    
    def synthesize_assignment_node(self, env):
        import ExprNodes
        self.assmt = SingleAssignmentNode(self.pos,
            lhs = ExprNodes.NameNode(self.pos, name = self.name),
            rhs = ExprNodes.UnboundMethodNode(self.pos, 
                class_cname = env.class_obj_cname,
                function = ExprNodes.PyCFunctionNode(self.pos,
                    pymethdef_cname = self.entry.pymethdef_cname)))
        self.assmt.analyse_declarations(env)
        self.assmt.analyse_expressions(env)
            
    def generate_function_header(self, code, with_pymethdef, proto_only=0):
        arg_code_list = []
        sig = self.entry.signature
        if sig.has_dummy_arg:
            arg_code_list.append(
                "PyObject *%s" % Naming.self_cname)
        for arg in self.args:
            if not arg.is_generic:
                if arg.is_self_arg:
                    arg_code_list.append("PyObject *%s" % arg.hdr_cname)
                else:
                    arg_code_list.append(
                        arg.hdr_type.declaration_code(arg.hdr_cname))
        if not self.entry.is_special and sig.method_flags() == [TypeSlots.method_noargs]:
            arg_code_list.append("PyObject *unused")
        if sig.has_generic_args:
            arg_code_list.append(
                "PyObject *%s, PyObject *%s"
                    % (Naming.args_cname, Naming.kwds_cname))
        arg_code = ", ".join(arg_code_list)
        dc = self.return_type.declaration_code(self.entry.func_cname)
        header = "static %s(%s)" % (dc, arg_code)
        code.putln("%s; /*proto*/" % header)
        if proto_only:
            return
        if self.entry.doc and Options.docstrings:
            docstr = self.entry.doc
            if not isinstance(docstr, str):
                docstr = docstr.utf8encode()
            code.putln(
                'static char %s[] = "%s";' % (
                    self.entry.doc_cname,
                    split_docstring(escape_byte_string(docstr))))
        if with_pymethdef:
            code.put(
                "static PyMethodDef %s = " % 
                    self.entry.pymethdef_cname)
            code.put_pymethoddef(self.entry, ";")
        code.putln("%s {" % header)

    def generate_argument_declarations(self, env, code):
        for arg in self.args:
            if arg.is_generic: # or arg.needs_conversion:
                if arg.needs_conversion:
                    code.putln("PyObject *%s = 0;" % arg.hdr_cname)
                else:
                    code.put_var_declaration(arg.entry)
    
    def generate_keyword_list(self, code):
        if self.signature_has_generic_args() and \
                self.signature_has_nongeneric_args():
            code.put(
                "static PyObject **%s[] = {" %
                    Naming.pykwdlist_cname)
            for arg in self.args:
                if arg.is_generic:
                    code.put('&%s,' % arg.name_entry.pystring_cname)
            code.putln("0};")

    def generate_argument_parsing_code(self, env, code):
        # Generate PyArg_ParseTuple call for generic
        # arguments, if any.
        if self.entry.signature.has_dummy_arg:
            # get rid of unused argument warning
            code.putln("%s = %s;" % (Naming.self_cname, Naming.self_cname))

        old_error_label = code.new_error_label()
        our_error_label = code.error_label
        end_label = code.new_label("argument_unpacking_done")

        has_kwonly_args = self.num_kwonly_args > 0
        has_star_or_kw_args = self.star_arg is not None \
            or self.starstar_arg is not None or has_kwonly_args

        if not self.signature_has_generic_args():
            if has_star_or_kw_args:
                error(self.pos, "This method cannot have * or keyword arguments")
            self.generate_argument_conversion_code(code)

        elif not self.signature_has_nongeneric_args():
            # func(*args) or func(**kw) or func(*args, **kw)
            self.generate_stararg_copy_code(code)

        else:
            positional_args = []
            kw_only_args = []
            default_seen = 0
            for arg in self.args:
                arg_entry = arg.entry
                if arg.is_generic:
                    if arg.default:
                        code.putln(
                            "%s = %s;" % (
                                arg_entry.cname,
                                arg.default_result_code))
                        default_seen = 1
                        if not arg.is_self_arg:
                            if arg.kw_only:
                                kw_only_args.append(arg)
                            else:
                                positional_args.append(arg)
                    elif arg.kw_only:
                        kw_only_args.append(arg)
                        default_seen = 1
                    elif default_seen:
                        error(arg.pos, "Non-default argument following default argument")
                    elif not arg.is_self_arg:
                        positional_args.append(arg)
                    if arg.needs_conversion:
                        format = arg.hdr_type.parsetuple_format
                    else:
                        format = arg_entry.type.parsetuple_format
                    if not format:
                        error(arg.pos,
                              "Cannot convert Python object argument to type '%s' (when parsing input arguments)"
                              % arg.type)

            self.generate_tuple_and_keyword_parsing_code(
                positional_args, kw_only_args, end_label, code)

        code.error_label = old_error_label
        if code.label_used(our_error_label):
            if not code.label_used(end_label):
                code.put_goto(end_label)
            code.put_label(our_error_label)
            if has_star_or_kw_args:
                self.generate_arg_decref(self.star_arg, code)
                if self.starstar_arg:
                    if self.starstar_arg.entry.xdecref_cleanup:
                        code.put_var_xdecref(self.starstar_arg.entry)
                    else:
                        code.put_var_decref(self.starstar_arg.entry)
            code.putln('__Pyx_AddTraceback("%s");' % self.entry.qualified_name)
            code.putln("return %s;" % self.error_value())
        if code.label_used(end_label):
            code.put_label(end_label)

    def generate_arg_assignment(self, arg, item, code):
        if arg.type.is_pyobject:
            if arg.is_generic:
                item = PyrexTypes.typecast(arg.type, PyrexTypes.py_object_type, item)
            code.putln("%s = %s;" % (arg.entry.cname, item))
        else:
            func = arg.type.from_py_function
            if func:
                code.putln("%s = %s(%s); %s" % (
                    arg.entry.cname,
                    func,
                    item,
                    code.error_goto_if(arg.type.error_condition(arg.entry.cname), arg.pos)))
            else:
                error(arg.pos, "Cannot convert Python object argument to type '%s'" % arg.type)
    
    def generate_arg_xdecref(self, arg, code):
        if arg:
            code.put_var_xdecref(arg.entry)
    
    def generate_arg_decref(self, arg, code):
        if arg:
            code.put_var_decref(arg.entry)

    def generate_stararg_copy_code(self, code):
        if not self.star_arg:
            code.globalstate.use_utility_code(raise_argtuple_invalid_utility_code)
            code.putln("if (unlikely(PyTuple_GET_SIZE(%s) > 0)) {" %
                       Naming.args_cname)
            code.put('__Pyx_RaiseArgtupleInvalid("%s", 1, 0, 0, PyTuple_GET_SIZE(%s)); return %s;' % (
                    self.name.utf8encode(), Naming.args_cname, self.error_value()))
            code.putln("}")

        code.globalstate.use_utility_code(keyword_string_check_utility_code)

        if self.starstar_arg:
            if self.star_arg:
                kwarg_check = "unlikely(%s)" % Naming.kwds_cname
            else:
                kwarg_check = "%s" % Naming.kwds_cname
        else:
            kwarg_check = "unlikely(%s) && unlikely(PyDict_Size(%s) > 0)" % (
                Naming.kwds_cname, Naming.kwds_cname)
        code.putln(
            "if (%s && unlikely(!__Pyx_CheckKeywordStrings(%s, \"%s\", %d))) return %s;" % (
                kwarg_check, Naming.kwds_cname, self.name,
                bool(self.starstar_arg), self.error_value()))

        if self.starstar_arg:
            code.putln("%s = (%s) ? PyDict_Copy(%s) : PyDict_New();" % (
                    self.starstar_arg.entry.cname,
                    Naming.kwds_cname,
                    Naming.kwds_cname))
            code.putln("if (unlikely(!%s)) return %s;" % (
                    self.starstar_arg.entry.cname, self.error_value()))
            self.starstar_arg.entry.xdecref_cleanup = 0

        if self.star_arg:
            code.put_incref(Naming.args_cname, py_object_type)
            code.putln("%s = %s;" % (
                    self.star_arg.entry.cname,
                    Naming.args_cname))
            self.star_arg.entry.xdecref_cleanup = 0

    def generate_tuple_and_keyword_parsing_code(self, positional_args,
                                                kw_only_args, success_label, code):
        argtuple_error_label = code.new_label("argtuple_error")

        min_positional_args = self.num_required_args - self.num_required_kw_args
        if len(self.args) > 0 and self.args[0].is_self_arg:
            min_positional_args -= 1
        max_positional_args = len(positional_args)
        has_fixed_positional_count = not self.star_arg and \
            min_positional_args == max_positional_args

        code.globalstate.use_utility_code(raise_double_keywords_utility_code)
        code.globalstate.use_utility_code(raise_argtuple_invalid_utility_code)
        if self.num_required_kw_args:
            code.globalstate.use_utility_code(raise_keyword_required_utility_code)

        if self.starstar_arg or self.star_arg:
            self.generate_stararg_init_code(max_positional_args, code)

        # --- optimised code when we receive keyword arguments
        if self.num_required_kw_args:
            likely_hint = "likely"
        else:
            likely_hint = "unlikely"
        code.putln("if (%s(%s)) {" % (likely_hint, Naming.kwds_cname))
        self.generate_keyword_unpacking_code(
            min_positional_args, max_positional_args,
            has_fixed_positional_count,
            positional_args, kw_only_args, argtuple_error_label, code)

        # --- optimised code when we do not receive any keyword arguments
        if (self.num_required_kw_args and min_positional_args > 0) or min_positional_args == max_positional_args:
            # Python raises arg tuple related errors first, so we must
            # check the length here
            if min_positional_args == max_positional_args and not self.star_arg:
                compare = '!='
            else:
                compare = '<'
            code.putln('} else if (PyTuple_GET_SIZE(%s) %s %d) {' % (
                    Naming.args_cname, compare, min_positional_args))
            code.put_goto(argtuple_error_label)

        if self.num_required_kw_args:
            # pure error case: keywords required but not passed
            if max_positional_args > min_positional_args and not self.star_arg:
                code.putln('} else if (PyTuple_GET_SIZE(%s) > %d) {' % (
                        Naming.args_cname, max_positional_args))
                code.put_goto(argtuple_error_label)
            code.putln('} else {')
            for i, arg in enumerate(kw_only_args):
                if not arg.default:
                    # required keyword-only argument missing
                    code.put('__Pyx_RaiseKeywordRequired("%s", %s); ' % (
                            self.name.utf8encode(),
                            arg.name_entry.pystring_cname))
                    code.putln(code.error_goto(self.pos))
                    break

        elif min_positional_args == max_positional_args:
            # parse the exact number of positional arguments from the
            # args tuple
            code.putln('} else {')
            for i, arg in enumerate(positional_args):
                item = "PyTuple_GET_ITEM(%s, %d)" % (Naming.args_cname, i)
                self.generate_arg_assignment(arg, item, code)

        else:
            # parse the positional arguments from the variable length
            # args tuple
            code.putln('} else {')
            code.putln('switch (PyTuple_GET_SIZE(%s)) {' % Naming.args_cname)
            if self.star_arg:
                code.putln('default:')
            reversed_args = list(enumerate(positional_args))[::-1]
            for i, arg in reversed_args:
                if i >= min_positional_args-1:
                    if min_positional_args > 1:
                        code.putln('case %2d:' % (i+1)) # pure code beautification
                    else:
                        code.put('case %2d: ' % (i+1))
                item = "PyTuple_GET_ITEM(%s, %d)" % (Naming.args_cname, i)
                self.generate_arg_assignment(arg, item, code)
            if min_positional_args == 0:
                code.put('case  0: ')
            code.putln('break;')
            if self.star_arg:
                if min_positional_args:
                    for i in range(min_positional_args-1, -1, -1):
                        code.putln('case %2d:' % i)
                    code.put_goto(argtuple_error_label)
            else:
                code.put('default: ')
                code.put_goto(argtuple_error_label)
            code.putln('}')

        code.putln('}')

        if code.label_used(argtuple_error_label):
            code.put_goto(success_label)
            code.put_label(argtuple_error_label)
            code.put('__Pyx_RaiseArgtupleInvalid("%s", %d, %d, %d, PyTuple_GET_SIZE(%s)); ' % (
                    self.name.utf8encode(), has_fixed_positional_count,
                    min_positional_args, max_positional_args,
                    Naming.args_cname))
            code.putln(code.error_goto(self.pos))

    def generate_stararg_init_code(self, max_positional_args, code):
        if self.starstar_arg:
            self.starstar_arg.entry.xdecref_cleanup = 0
            code.putln('%s = PyDict_New(); if (unlikely(!%s)) return %s;' % (
                    self.starstar_arg.entry.cname,
                    self.starstar_arg.entry.cname,
                    self.error_value()))
        if self.star_arg:
            self.star_arg.entry.xdecref_cleanup = 0
            code.putln('if (PyTuple_GET_SIZE(%s) > %d) {' % (
                    Naming.args_cname,
                    max_positional_args))
            code.put('%s = PyTuple_GetSlice(%s, %d, PyTuple_GET_SIZE(%s)); ' % (
                    self.star_arg.entry.cname, Naming.args_cname,
                    max_positional_args, Naming.args_cname))
            if self.starstar_arg:
                code.putln("")
                code.putln("if (unlikely(!%s)) {" % self.star_arg.entry.cname)
                code.put_decref(self.starstar_arg.entry.cname, py_object_type)
                code.putln('return %s;' % self.error_value())
                code.putln('}')
            else:
                code.putln("if (unlikely(!%s)) return %s;" % (
                        self.star_arg.entry.cname, self.error_value()))
            code.putln('} else {')
            code.put("%s = %s; " % (self.star_arg.entry.cname, Naming.empty_tuple))
            code.put_incref(Naming.empty_tuple, py_object_type)
            code.putln('}')

    def generate_keyword_unpacking_code(self, min_positional_args, max_positional_args,
                                        has_fixed_positional_count, positional_args,
                                        kw_only_args, argtuple_error_label, code):
        all_args = tuple(positional_args) + tuple(kw_only_args)
        max_args = len(all_args)

        code.putln("PyObject* values[%d] = {%s};" % (
                max_args, ('0,'*max_args)[:-1]))
        code.putln("Py_ssize_t kw_args = PyDict_Size(%s);" %
                   Naming.kwds_cname)

        # parse the tuple and check that it's not too long
        code.putln('switch (PyTuple_GET_SIZE(%s)) {' % Naming.args_cname)
        if self.star_arg:
            code.putln('default:')
        for i in range(max_positional_args-1, -1, -1):
            code.put('case %2d: ' % (i+1))
            code.putln("values[%d] = PyTuple_GET_ITEM(%s, %d);" % (
                    i, Naming.args_cname, i))
        code.putln('case  0: break;')
        if not self.star_arg:
            code.put('default: ') # more arguments than allowed
            code.put_goto(argtuple_error_label)
        code.putln('}')

        # now fill up the required arguments with values from the kw dict
        last_required_arg = -1
        for i, arg in enumerate(all_args):
            if not arg.default:
                last_required_arg = i
        if last_required_arg >= 0:
            code.putln('switch (PyTuple_GET_SIZE(%s)) {' % Naming.args_cname)
            for i, arg in enumerate(all_args[:last_required_arg+1]):
                if i <= max_positional_args:
                    if self.star_arg and i == max_positional_args:
                        code.putln('default:')
                    else:
                        code.putln('case %2d:' % i)
                if arg.default:
                    # handled in ParseOptionalKeywords() below
                    continue
                code.putln('values[%d] = PyDict_GetItem(%s, %s);' % (
                        i, Naming.kwds_cname, arg.name_entry.pystring_cname))
                if i < min_positional_args:
                    code.putln('if (likely(values[%d])) kw_args--;' % i);
                    if i == 0:
                        # special case: we know arg 0 is missing
                        code.put('else ')
                        code.put_goto(argtuple_error_label)
                    else:
                        # print the correct number of values (args or
                        # kwargs) that were passed into positional
                        # arguments up to this point
                        code.putln('else {')
                        code.put('__Pyx_RaiseArgtupleInvalid("%s", %d, %d, %d, %d); ' % (
                                self.name.utf8encode(), has_fixed_positional_count,
                                min_positional_args, max_positional_args, i))
                        code.putln(code.error_goto(self.pos))
                        code.putln('}')
                else:
                    code.putln('if (values[%d]) kw_args--;' % i);
                    if arg.kw_only and not arg.default:
                        code.putln('else {')
                        code.put('__Pyx_RaiseKeywordRequired("%s", %s); ' %(
                                self.name.utf8encode(), arg.name_entry.pystring_cname))
                        code.putln(code.error_goto(self.pos))
                        code.putln('}')
            code.putln('}')

        code.putln('if (unlikely(kw_args > 0)) {')
        # non-positional kw args left in dict: default args, **kwargs or error
        if self.star_arg:
            code.putln("const Py_ssize_t used_pos_args = (PyTuple_GET_SIZE(%s) < %d) ? PyTuple_GET_SIZE(%s) : %d;" % (
                    Naming.args_cname, max_positional_args,
                    Naming.args_cname, max_positional_args))
            pos_arg_count = "used_pos_args"
        else:
            pos_arg_count = "PyTuple_GET_SIZE(%s)" % Naming.args_cname
        code.globalstate.use_utility_code(parse_keywords_utility_code)
        code.put(
            'if (unlikely(__Pyx_ParseOptionalKeywords(%s, %s, %s, values, %s, "%s") < 0)) ' % (
                Naming.kwds_cname,
                Naming.pykwdlist_cname,
                self.starstar_arg and self.starstar_arg.entry.cname or '0',
                pos_arg_count,
                self.name.utf8encode()))
        code.putln(code.error_goto(self.pos))
        code.putln('}')

        # convert arg values to their final type and assign them
        for i, arg in enumerate(all_args):
            if arg.default:
                code.putln("if (values[%d]) {" % i)
            self.generate_arg_assignment(arg, "values[%d]" % i, code)
            if arg.default:
                code.putln('}')

    def generate_argument_conversion_code(self, code):
        # Generate code to convert arguments from
        # signature type to declared type, if needed.
        for arg in self.args:
            if arg.needs_conversion:
                self.generate_arg_conversion(arg, code)

    def generate_arg_conversion(self, arg, code):
        # Generate conversion code for one argument.
        old_type = arg.hdr_type
        new_type = arg.type
        if old_type.is_pyobject:
            if arg.default:
                code.putln("if (%s) {" % arg.hdr_cname)
            else:
                code.putln("assert(%s); {" % arg.hdr_cname)
            self.generate_arg_conversion_from_pyobject(arg, code)
            code.putln("}")
        elif new_type.is_pyobject:
            self.generate_arg_conversion_to_pyobject(arg, code)
        else:
            if new_type.assignable_from(old_type):
                code.putln(
                    "%s = %s;" % (arg.entry.cname, arg.hdr_cname))
            else:
                error(arg.pos,
                    "Cannot convert 1 argument from '%s' to '%s'" %
                        (old_type, new_type))
    
    def generate_arg_conversion_from_pyobject(self, arg, code):
        new_type = arg.type
        func = new_type.from_py_function
        # copied from CoerceFromPyTypeNode
        if func:
            code.putln("%s = %s(%s); %s" % (
                arg.entry.cname,
                func,
                arg.hdr_cname,
                code.error_goto_if(new_type.error_condition(arg.entry.cname), arg.pos)))
        else:
            error(arg.pos, 
                "Cannot convert Python object argument to type '%s'" 
                    % new_type)
    
    def generate_arg_conversion_to_pyobject(self, arg, code):
        old_type = arg.hdr_type
        func = old_type.to_py_function
        if func:
            code.putln("%s = %s(%s); %s" % (
                arg.entry.cname,
                func,
                arg.hdr_cname,
                code.error_goto_if_null(arg.entry.cname, arg.pos)))
        else:
            error(arg.pos,
                "Cannot convert argument of type '%s' to Python object"
                    % old_type)

    def generate_argument_type_tests(self, code):
        # Generate type tests for args whose signature
        # type is PyObject * and whose declared type is
        # a subtype thereof.
        for arg in self.args:
            if arg.needs_type_test:
                self.generate_arg_type_test(arg, code)
    
    def generate_arg_type_test(self, arg, code):
        # Generate type test for one argument.
        if arg.type.typeobj_is_available():
            typeptr_cname = arg.type.typeptr_cname
            arg_code = "((PyObject *)%s)" % arg.entry.cname
            code.putln(
                'if (unlikely(!__Pyx_ArgTypeTest(%s, %s, %d, "%s", %s))) %s' % (
                    arg_code, 
                    typeptr_cname,
                    not arg.not_none,
                    arg.name,
                    arg.type.is_builtin_type,
                    code.error_goto(arg.pos)))
        else:
            error(arg.pos, "Cannot test type of extern C class "
                "without type object name specification")
    
    def error_value(self):
        return self.entry.signature.error_value
    
    def caller_will_check_exceptions(self):
        return 1
            
class OverrideCheckNode(StatNode):
    # A Node for dispatching to the def method if it
    # is overriden. 
    #
    #  py_func
    #
    #  args
    #  func_temp
    #  body
    
    child_attrs = ['body']
    
    body = None

    def analyse_expressions(self, env):
        self.args = env.arg_entries
        if self.py_func.is_module_scope:
            first_arg = 0
        else:
            first_arg = 1
        import ExprNodes
        self.func_node = ExprNodes.PyTempNode(self.pos, env)
        call_tuple = ExprNodes.TupleNode(self.pos, args=[ExprNodes.NameNode(self.pos, name=arg.name) for arg in self.args[first_arg:]])
        call_node = ExprNodes.SimpleCallNode(self.pos,
                                             function=self.func_node, 
                                             args=[ExprNodes.NameNode(self.pos, name=arg.name) for arg in self.args[first_arg:]])
        self.body = ReturnStatNode(self.pos, value=call_node)
        self.body.analyse_expressions(env)
        
    def generate_execution_code(self, code):
        # Check to see if we are an extension type
        if self.py_func.is_module_scope:
            self_arg = "((PyObject *)%s)" % Naming.module_cname
        else:
            self_arg = "((PyObject *)%s)" % self.args[0].cname
        code.putln("/* Check if called by wrapper */")
        code.putln("if (unlikely(%s)) ;" % Naming.skip_dispatch_cname)
        code.putln("/* Check if overriden in Python */")
        if self.py_func.is_module_scope:
            code.putln("else {")
        else:
            code.putln("else if (unlikely(Py_TYPE(%s)->tp_dictoffset != 0)) {" % self_arg)
        err = code.error_goto_if_null(self.func_node.result(), self.pos)
        # need to get attribute manually--scope would return cdef method
        code.putln("%s = PyObject_GetAttr(%s, %s); %s" % (self.func_node.result(), self_arg, self.py_func.interned_attr_cname, err))
        # It appears that this type is not anywhere exposed in the Python/C API
        is_builtin_function_or_method = '(strcmp(Py_TYPE(%s)->tp_name, "builtin_function_or_method") == 0)' % self.func_node.result()
        is_overridden = '(PyCFunction_GET_FUNCTION(%s) != (void *)&%s)' % (self.func_node.result(), self.py_func.entry.func_cname)
        code.putln('if (!%s || %s) {' % (is_builtin_function_or_method, is_overridden))
        self.body.generate_execution_code(code)
        code.putln('}')
        code.put_decref_clear(self.func_node.result(), PyrexTypes.py_object_type)
        code.putln("}")

class ClassDefNode(StatNode, BlockNode):
    pass

class PyClassDefNode(ClassDefNode):
    #  A Python class definition.
    #
    #  name     EncodedString   Name of the class
    #  doc      string or None
    #  body     StatNode        Attribute definition code
    #  entry    Symtab.Entry
    #  scope    PyClassScope
    #
    #  The following subnodes are constructed internally:
    #
    #  dict     DictNode   Class dictionary
    #  classobj ClassNode  Class object
    #  target   NameNode   Variable to assign class object to

    child_attrs = ["body", "dict", "classobj", "target"]
    
    def __init__(self, pos, name, bases, doc, body):
        StatNode.__init__(self, pos)
        self.name = name
        self.doc = doc
        self.body = body
        import ExprNodes
        self.dict = ExprNodes.DictNode(pos, key_value_pairs = [])
        if self.doc and Options.docstrings:
            doc = embed_position(self.pos, self.doc)
            doc_node = ExprNodes.StringNode(pos, value = doc)
        else:
            doc_node = None
        self.classobj = ExprNodes.ClassNode(pos, name = name,
            bases = bases, dict = self.dict, doc = doc_node)
        self.target = ExprNodes.NameNode(pos, name = name)
        
    def as_cclass(self):
        """
        Return this node as if it were declared as an extension class"
        """
        bases = self.classobj.bases.args
        if len(bases) == 0:
            base_class_name = None
            base_class_module = None
        elif len(bases) == 1:
            base = bases[0]
            path = []
            while isinstance(base, ExprNodes.AttributeNode):
                path.insert(0, base.attribute)
                base = base.obj
            if isinstance(base, ExprNodes.NameNode):
                path.insert(0, base.name)
                base_class_name = path[-1]
                if len(path) > 1:
                    base_class_module = u'.'.join(path[:-1])
                else:
                    base_class_module = None
            else:
                error(self.classobj.bases.args.pos, "Invalid base class")
        else:
            error(self.classobj.bases.args.pos, "C class may only have one base class")
            return None
        
        return CClassDefNode(self.pos, 
                             visibility = 'private',
                             module_name = None,
                             class_name = self.name,
                             base_class_module = base_class_module,
                             base_class_name = base_class_name,
                             body = self.body,
                             in_pxd = False,
                             doc = self.doc)
        
    def create_scope(self, env):
        genv = env
        while env.is_py_class_scope or env.is_c_class_scope:
            env = env.outer_scope
        cenv = self.scope = PyClassScope(name = self.name, outer_scope = genv)
        return cenv
    
    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
        cenv = self.create_scope(env)
        cenv.class_obj_cname = self.target.entry.cname
        self.body.analyse_declarations(cenv)
    
    def analyse_expressions(self, env):
        self.dict.analyse_expressions(env)
        self.classobj.analyse_expressions(env)
        genv = env.global_scope()
        cenv = self.scope
        cenv.class_dict_cname = self.dict.result()
        cenv.namespace_cname = cenv.class_obj_cname = self.classobj.result()
        self.body.analyse_expressions(cenv)
        self.target.analyse_target_expression(env, self.classobj)
        self.dict.release_temp(env)
        #self.classobj.release_temp(env)
        #self.target.release_target_temp(env)
    
    def generate_function_definitions(self, env, code):
        self.generate_py_string_decls(self.scope, code)
        self.body.generate_function_definitions(self.scope, code)
    
    def generate_execution_code(self, code):
        self.dict.generate_evaluation_code(code)
        self.classobj.generate_evaluation_code(code)
        self.body.generate_execution_code(code)
        self.target.generate_assignment_code(self.classobj, code)
        self.dict.generate_disposal_code(code)


class CClassDefNode(ClassDefNode):
    #  An extension type definition.
    #
    #  visibility         'private' or 'public' or 'extern'
    #  typedef_flag       boolean
    #  api                boolean
    #  module_name        string or None    For import of extern type objects
    #  class_name         string            Unqualified name of class
    #  as_name            string or None    Name to declare as in this scope
    #  base_class_module  string or None    Module containing the base class
    #  base_class_name    string or None    Name of the base class
    #  objstruct_name     string or None    Specified C name of object struct
    #  typeobj_name       string or None    Specified C name of type object
    #  in_pxd             boolean           Is in a .pxd file
    #  doc                string or None
    #  body               StatNode or None
    #  entry              Symtab.Entry
    #  base_type          PyExtensionType or None
    #  buffer_defaults_node DictNode or None Declares defaults for a buffer
    #  buffer_defaults_pos

    child_attrs = ["body"]
    buffer_defaults_node = None
    buffer_defaults_pos = None
    typedef_flag = False
    api = False
    objstruct_name = None
    typeobj_name = None

    def analyse_declarations(self, env):
        #print "CClassDefNode.analyse_declarations:", self.class_name
        #print "...visibility =", self.visibility
        #print "...module_name =", self.module_name

        import Buffer
        if self.buffer_defaults_node:
            buffer_defaults = Buffer.analyse_buffer_options(self.buffer_defaults_pos,
                                                            env, [], self.buffer_defaults_node,
                                                            need_complete=False)
        else:
            buffer_defaults = None

        if env.in_cinclude and not self.objstruct_name:
            error(self.pos, "Object struct name specification required for "
                "C class defined in 'extern from' block")
        self.base_type = None
        # Now that module imports are cached, we need to 
        # import the modules for extern classes. 
        if self.module_name:
            self.module = None
            for module in env.cimported_modules:
                if module.name == self.module_name:
                    self.module = module
            if self.module is None:
                self.module = ModuleScope(self.module_name, None, env.context)
                self.module.has_extern_class = 1
                env.cimported_modules.append(self.module)

        if self.base_class_name:
            if self.base_class_module:
                base_class_scope = env.find_module(self.base_class_module, self.pos)
            else:
                base_class_scope = env
            if base_class_scope:
                base_class_entry = base_class_scope.find(self.base_class_name, self.pos)
                if base_class_entry:
                    if not base_class_entry.is_type:
                        error(self.pos, "'%s' is not a type name" % self.base_class_name)
                    elif not base_class_entry.type.is_extension_type:
                        error(self.pos, "'%s' is not an extension type" % self.base_class_name)
                    elif not base_class_entry.type.is_complete():
                        error(self.pos, "Base class '%s' is incomplete" % self.base_class_name)
                    else:
                        self.base_type = base_class_entry.type
        has_body = self.body is not None
        if self.module_name and self.visibility != 'extern':
            module_path = self.module_name.split(".")
            home_scope = env.find_imported_module(module_path, self.pos)
            if not home_scope:
                return
        else:
            home_scope = env
        self.entry = home_scope.declare_c_class(
            name = self.class_name, 
            pos = self.pos,
            defining = has_body and self.in_pxd,
            implementing = has_body and not self.in_pxd,
            module_name = self.module_name,
            base_type = self.base_type,
            objstruct_cname = self.objstruct_name,
            typeobj_cname = self.typeobj_name,
            visibility = self.visibility,
            typedef_flag = self.typedef_flag,
            api = self.api,
            buffer_defaults = buffer_defaults)
        if home_scope is not env and self.visibility == 'extern':
            env.add_imported_entry(self.class_name, self.entry, pos)
        scope = self.entry.type.scope

        if self.doc and Options.docstrings:
            scope.doc = embed_position(self.pos, self.doc)
            
        if has_body:
            self.body.analyse_declarations(scope)
            if self.in_pxd:
                scope.defined = 1
            else:
                scope.implemented = 1
        env.allocate_vtable_names(self.entry)
        
    def analyse_expressions(self, env):
        if self.body:
            scope = self.entry.type.scope
            self.body.analyse_expressions(scope)
    
    def generate_function_definitions(self, env, code):
        self.generate_py_string_decls(self.entry.type.scope, code)
        if self.body:
            self.body.generate_function_definitions(
                self.entry.type.scope, code)
    
    def generate_execution_code(self, code):
        # This is needed to generate evaluation code for
        # default values of method arguments.
        if self.body:
            self.body.generate_execution_code(code)
            
    def annotate(self, code):
        if self.body:
            self.body.annotate(code)


class PropertyNode(StatNode):
    #  Definition of a property in an extension type.
    #
    #  name   string
    #  doc    EncodedString or None    Doc string
    #  body   StatListNode
    
    child_attrs = ["body"]

    def analyse_declarations(self, env):
        entry = env.declare_property(self.name, self.doc, self.pos)
        if entry:
            if self.doc and Options.docstrings:
                doc_entry = env.get_string_const(
                    self.doc, identifier = False)
                entry.doc_cname = doc_entry.cname
            self.body.analyse_declarations(entry.scope)

    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)

    def generate_execution_code(self, code):
        pass

    def annotate(self, code):
        self.body.annotate(code)


class GlobalNode(StatNode):
    # Global variable declaration.
    #
    # names    [string]
    
    child_attrs = []

    def analyse_declarations(self, env):
        for name in self.names:
            env.declare_global(name, self.pos)

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class ExprStatNode(StatNode):
    #  Expression used as a statement.
    #
    #  expr   ExprNode

    child_attrs = ["expr"]
    
    def analyse_declarations(self, env):
        import ExprNodes
        if isinstance(self.expr, ExprNodes.GeneralCallNode):
            func = self.expr.function.as_cython_attribute()
            if func == u'declare':
                args, kwds = self.expr.explicit_args_kwds()
                if len(args):
                    error(self.expr.pos, "Variable names must be specified.")
                for var, type_node in kwds.key_value_pairs:
                    type = type_node.analyse_as_type(env)
                    if type is None:
                        error(type_node.pos, "Unknown type")
                    else:
                        env.declare_var(var.value, type, var.pos, is_cdef = True)
                self.__class__ = PassStatNode
    
    def analyse_expressions(self, env):
        self.expr.analyse_expressions(env)
        self.expr.release_temp(env)
    
    def generate_execution_code(self, code):
        self.expr.generate_evaluation_code(code)
        if not self.expr.is_temp and self.expr.result():
            code.putln("%s;" % self.expr.result())
        self.expr.generate_disposal_code(code)

    def annotate(self, code):
        self.expr.annotate(code)


class AssignmentNode(StatNode):
    #  Abstract base class for assignment nodes.
    #
    #  The analyse_expressions and generate_execution_code
    #  phases of assignments are split into two sub-phases
    #  each, to enable all the right hand sides of a
    #  parallel assignment to be evaluated before assigning
    #  to any of the left hand sides.

    def analyse_expressions(self, env):
        self.analyse_types(env)
        self.allocate_rhs_temps(env)
        self.allocate_lhs_temps(env)

#	def analyse_expressions(self, env):
#		self.analyse_expressions_1(env)
#		self.analyse_expressions_2(env)

    def generate_execution_code(self, code):
        self.generate_rhs_evaluation_code(code)
        self.generate_assignment_code(code)
        

class SingleAssignmentNode(AssignmentNode):
    #  The simplest case:
    #
    #    a = b
    #
    #  lhs      ExprNode      Left hand side
    #  rhs      ExprNode      Right hand side
    #  first    bool          Is this guaranteed the first assignment to lhs?
    
    child_attrs = ["lhs", "rhs"]
    first = False
    declaration_only = False

    def analyse_declarations(self, env):
        import ExprNodes
        
        # handle declarations of the form x = cython.foo()
        if isinstance(self.rhs, ExprNodes.CallNode):
            func_name = self.rhs.function.as_cython_attribute()
            if func_name:
                args, kwds = self.rhs.explicit_args_kwds()
                
                if func_name in ['declare', 'typedef']:
                    if len(args) > 2 or kwds is not None:
                        error(rhs.pos, "Can only declare one type at a time.")
                        return
                    type = args[0].analyse_as_type(env)
                    if type is None:
                        error(args[0].pos, "Unknown type")
                        return
                    lhs = self.lhs
                    if func_name == 'declare':
                        if isinstance(lhs, ExprNodes.NameNode):
                            vars = [(lhs.name, lhs.pos)]
                        elif isinstance(lhs, ExprNodes.TupleNode):
                            vars = [(var.name, var.pos) for var in lhs.args]
                        else:
                            error(lhs.pos, "Invalid declaration")
                            return
                        for var, pos in vars:
                            env.declare_var(var, type, pos, is_cdef = True)
                        if len(args) == 2:
                            # we have a value
                            self.rhs = args[1]
                        else:
                            self.declaration_only = True
                    else:
                        self.declaration_only = True
                        if not isinstance(lhs, ExprNodes.NameNode):
                            error(lhs.pos, "Invalid declaration.")
                        env.declare_typedef(lhs.name, type, self.pos, visibility='private')
                    
                elif func_name in ['struct', 'union']:
                    self.declaration_only = True
                    if len(args) > 0 or kwds is None:
                        error(rhs.pos, "Struct or union members must be given by name.")
                        return
                    members = []
                    for member, type_node in kwds.key_value_pairs:
                        type = type_node.analyse_as_type(env)
                        if type is None:
                            error(type_node.pos, "Unknown type")
                        else:
                            members.append((member.value, type, member.pos))
                    if len(members) < len(kwds.key_value_pairs):
                        return
                    if not isinstance(self.lhs, ExprNodes.NameNode):
                        error(self.lhs.pos, "Invalid declaration.")
                    name = self.lhs.name
                    scope = StructOrUnionScope(name)
                    env.declare_struct_or_union(name, func_name, scope, False, self.rhs.pos)
                    for member, type, pos in members:
                        scope.declare_var(member, type, pos)
                    
        if self.declaration_only:
            return
        else:
            self.lhs.analyse_target_declaration(env)
    
    def analyse_types(self, env, use_temp = 0):
        self.rhs.analyse_types(env)
        self.lhs.analyse_target_types(env)
        self.lhs.gil_assignment_check(env)
        self.rhs = self.rhs.coerce_to(self.lhs.type, env)
        if use_temp:
            self.rhs = self.rhs.coerce_to_temp(env)
    
    def allocate_rhs_temps(self, env):
        self.rhs.allocate_temps(env)

    def allocate_lhs_temps(self, env):
        self.lhs.allocate_target_temps(env, self.rhs)
        #self.lhs.release_target_temp(env)
        #self.rhs.release_temp(env)		
    
#	def analyse_expressions_1(self, env, use_temp = 0):
#		self.rhs.analyse_types(env)
#		self.lhs.analyse_target_types(env)
#		self.rhs = self.rhs.coerce_to(self.lhs.type, env)
#		if use_temp:
#			self.rhs = self.rhs.coerce_to_temp(env)
#		self.rhs.allocate_temps(env)
#	
#	def analyse_expressions_2(self, env):
#		self.lhs.allocate_target_temps(env)
#		self.lhs.release_target_temp(env)
#		self.rhs.release_temp(env)		
        
    def generate_rhs_evaluation_code(self, code):
        self.rhs.generate_evaluation_code(code)
    
    def generate_assignment_code(self, code):
        self.lhs.generate_assignment_code(self.rhs, code)

    def annotate(self, code):
        self.lhs.annotate(code)
        self.rhs.annotate(code)


class CascadedAssignmentNode(AssignmentNode):
    #  An assignment with multiple left hand sides:
    #
    #    a = b = c
    #
    #  lhs_list   [ExprNode]   Left hand sides
    #  rhs        ExprNode     Right hand sides
    #
    #  Used internally:
    #
    #  coerced_rhs_list   [ExprNode]   RHS coerced to type of each LHS
    
    child_attrs = ["lhs_list", "rhs", "coerced_rhs_list"]
    coerced_rhs_list = None

    def analyse_declarations(self, env):
        for lhs in self.lhs_list:
            lhs.analyse_target_declaration(env)
    
    def analyse_types(self, env, use_temp = 0):
        self.rhs.analyse_types(env)
        if use_temp:
            self.rhs = self.rhs.coerce_to_temp(env)
        else:
            self.rhs = self.rhs.coerce_to_simple(env)
        from ExprNodes import CloneNode
        self.coerced_rhs_list = []
        for lhs in self.lhs_list:
            lhs.analyse_target_types(env)
            lhs.gil_assignment_check(env)
            rhs = CloneNode(self.rhs)
            rhs = rhs.coerce_to(lhs.type, env)
            self.coerced_rhs_list.append(rhs)

    def allocate_rhs_temps(self, env):
        self.rhs.allocate_temps(env)
    
    def allocate_lhs_temps(self, env):
        for lhs, rhs in zip(self.lhs_list, self.coerced_rhs_list):
            rhs.allocate_temps(env)
            lhs.allocate_target_temps(env, rhs)
            #lhs.release_target_temp(env)
            #rhs.release_temp(env)
        self.rhs.release_temp(env)
    
#	def analyse_expressions_1(self, env, use_temp = 0):
#		self.rhs.analyse_types(env)
#		if use_temp:
#			self.rhs = self.rhs.coerce_to_temp(env)
#		else:
#			self.rhs = self.rhs.coerce_to_simple(env)
#		self.rhs.allocate_temps(env)
#	
#	def analyse_expressions_2(self, env):
#		from ExprNodes import CloneNode
#		self.coerced_rhs_list = []
#		for lhs in self.lhs_list:
#			lhs.analyse_target_types(env)
#			rhs = CloneNode(self.rhs)
#			rhs = rhs.coerce_to(lhs.type, env)
#			self.coerced_rhs_list.append(rhs)
#			rhs.allocate_temps(env)
#			lhs.allocate_target_temps(env)
#			lhs.release_target_temp(env)
#			rhs.release_temp(env)
#		self.rhs.release_temp(env)
    
    def generate_rhs_evaluation_code(self, code):
        self.rhs.generate_evaluation_code(code)
    
    def generate_assignment_code(self, code):
        for i in range(len(self.lhs_list)):
            lhs = self.lhs_list[i]
            rhs = self.coerced_rhs_list[i]
            rhs.generate_evaluation_code(code)
            lhs.generate_assignment_code(rhs, code)
            # Assignment has disposed of the cloned RHS
        self.rhs.generate_disposal_code(code)

    def annotate(self, code):
        for i in range(len(self.lhs_list)):
            lhs = self.lhs_list[i].annotate(code)
            rhs = self.coerced_rhs_list[i].annotate(code)
        self.rhs.annotate(code)
        

class ParallelAssignmentNode(AssignmentNode):
    #  A combined packing/unpacking assignment:
    #
    #    a, b, c =  d, e, f
    #
    #  This has been rearranged by the parser into
    #
    #    a = d ; b = e ; c = f
    #
    #  but we must evaluate all the right hand sides
    #  before assigning to any of the left hand sides.
    #
    #  stats     [AssignmentNode]   The constituent assignments
    
    child_attrs = ["stats"]

    def analyse_declarations(self, env):
        for stat in self.stats:
            stat.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        for stat in self.stats:
            stat.analyse_types(env, use_temp = 1)
            stat.allocate_rhs_temps(env)
        for stat in self.stats:
            stat.allocate_lhs_temps(env)

#	def analyse_expressions(self, env):
#		for stat in self.stats:
#			stat.analyse_expressions_1(env, use_temp = 1)
#		for stat in self.stats:
#			stat.analyse_expressions_2(env)
    
    def generate_execution_code(self, code):
        for stat in self.stats:
            stat.generate_rhs_evaluation_code(code)
        for stat in self.stats:
            stat.generate_assignment_code(code)

    def annotate(self, code):
        for stat in self.stats:
            stat.annotate(code)


class InPlaceAssignmentNode(AssignmentNode):
    #  An in place arithmatic operand:
    #
    #    a += b
    #    a -= b
    #    ...
    #
    #  lhs      ExprNode      Left hand side
    #  rhs      ExprNode      Right hand side
    #  op       char          one of "+-*/%^&|"
    #  dup     (ExprNode)     copy of lhs used for operation (auto-generated)
    #
    #  This code is a bit tricky because in order to obey Python 
    #  semantics the sub-expressions (e.g. indices) of the lhs must 
    #  not be evaluated twice. So we must re-use the values calculated 
    #  in evaluation phase for the assignment phase as well. 
    #  Fortunately, the type of the lhs node is fairly constrained 
    #  (it must be a NameNode, AttributeNode, or IndexNode).     
    
    child_attrs = ["lhs", "rhs"]
    dup = None

    def analyse_declarations(self, env):
        self.lhs.analyse_target_declaration(env)
        
    def analyse_types(self, env):
        self.dup = self.create_dup_node(env) # re-assigns lhs to a shallow copy
        self.rhs.analyse_types(env)
        self.lhs.analyse_target_types(env)
        if Options.incref_local_binop and self.dup.type.is_pyobject:
            self.dup = self.dup.coerce_to_temp(env)
        
    def allocate_rhs_temps(self, env):
        import ExprNodes
        if self.lhs.type.is_pyobject:
            self.rhs = self.rhs.coerce_to_pyobject(env)
        elif self.rhs.type.is_pyobject:
            self.rhs = self.rhs.coerce_to(self.lhs.type, env)
        if self.lhs.type.is_pyobject:
             self.result_value = ExprNodes.PyTempNode(self.pos, env).coerce_to(self.lhs.type, env)
             self.result_value.allocate_temps(env)
#        if use_temp:
#            self.rhs = self.rhs.coerce_to_temp(env)
        self.rhs.allocate_temps(env)
        self.dup.allocate_subexpr_temps(env)
        self.dup.allocate_temp(env)
    
    def allocate_lhs_temps(self, env):
        self.lhs.allocate_target_temps(env, self.rhs)
#        self.lhs.release_target_temp(env)
        self.dup.release_temp(env)
        if self.dup.is_temp:
            self.dup.release_subexpr_temps(env)
#        self.rhs.release_temp(env)
        if self.lhs.type.is_pyobject:
            self.result_value.release_temp(env)

    def generate_execution_code(self, code):
        self.rhs.generate_evaluation_code(code)
        self.dup.generate_subexpr_evaluation_code(code)
        # self.dup.generate_result_code is run only if it is not buffer access
        if self.operator == "**":
            extra = ", Py_None"
        else:
            extra = ""
        import ExprNodes
        if self.lhs.type.is_pyobject:
            if isinstance(self.lhs, ExprNodes.IndexNode) and self.lhs.is_buffer_access:
                error(self.pos, "In-place operators not allowed on object buffers in this release.")
            self.dup.generate_result_code(code)
            code.putln(
                "%s = %s(%s, %s%s); %s" % (
                    self.result_value.result(), 
                    self.py_operation_function(), 
                    self.dup.py_result(),
                    self.rhs.py_result(),
                    extra,
                    code.error_goto_if_null(self.result_value.py_result(), self.pos)))
            self.result_value.generate_evaluation_code(code) # May be a type check...
            self.rhs.generate_disposal_code(code)
            self.dup.generate_disposal_code(code)
            self.lhs.generate_assignment_code(self.result_value, code)
        else: 
            c_op = self.operator
            if c_op == "//":
                c_op = "/"
            elif c_op == "**":
                if self.lhs.type.is_int and self.rhs.type.is_int:
                    error(self.pos, "** with two C int types is ambiguous")
                else:
                    error(self.pos, "No C inplace power operator")
            # have to do assignment directly to avoid side-effects
            if isinstance(self.lhs, ExprNodes.IndexNode) and self.lhs.is_buffer_access:
                self.lhs.generate_buffer_setitem_code(self.rhs, code, c_op)
            else:
                self.dup.generate_result_code(code)
                code.putln("%s %s= %s;" % (self.lhs.result(), c_op, self.rhs.result()) )
            self.rhs.generate_disposal_code(code)
        if self.dup.is_temp:
            self.dup.generate_subexpr_disposal_code(code)
            
    def create_dup_node(self, env): 
        import ExprNodes
        self.dup = self.lhs
        self.dup.analyse_types(env)
        if isinstance(self.lhs, ExprNodes.NameNode):
            target_lhs = ExprNodes.NameNode(self.dup.pos,
                                            name = self.dup.name,
                                            is_temp = self.dup.is_temp,
                                            entry = self.dup.entry)
        elif isinstance(self.lhs, ExprNodes.AttributeNode):
            target_lhs = ExprNodes.AttributeNode(self.dup.pos,
                                                 obj = ExprNodes.CloneNode(self.lhs.obj),
                                                 attribute = self.dup.attribute,
                                                 is_temp = self.dup.is_temp)
        elif isinstance(self.lhs, ExprNodes.IndexNode):
            if self.lhs.index:
                index = ExprNodes.CloneNode(self.lhs.index)
            else:
                index = None
            if self.lhs.indices:
                indices = [ExprNodes.CloneNode(x) for x in self.lhs.indices]
            else:
                indices = []
            target_lhs = ExprNodes.IndexNode(self.dup.pos,
                                             base = ExprNodes.CloneNode(self.dup.base),
                                             index = index,
                                             indices = indices,
                                             is_temp = self.dup.is_temp)
        self.lhs = target_lhs
        return self.dup
    
    def py_operation_function(self):
        return self.py_functions[self.operator]

    py_functions = {
        "|":		"PyNumber_InPlaceOr",
        "^":		"PyNumber_InPlaceXor",
        "&":		"PyNumber_InPlaceAnd",
        "+":		"PyNumber_InPlaceAdd",
        "-":		"PyNumber_InPlaceSubtract",
        "*":		"PyNumber_InPlaceMultiply",
        "/":		"PyNumber_InPlaceDivide",
        "%":		"PyNumber_InPlaceRemainder",
        "<<":		"PyNumber_InPlaceLshift",
        ">>":		"PyNumber_InPlaceRshift",
        "**":		"PyNumber_InPlacePower",
        "//":		"PyNumber_InPlaceFloorDivide",
    }

    def annotate(self, code):
        self.lhs.annotate(code)
        self.rhs.annotate(code)
        self.dup.annotate(code)


class PrintStatNode(StatNode):
    #  print statement
    #
    #  arg_tuple         TupleNode
    #  append_newline    boolean

    child_attrs = ["arg_tuple"]

    def analyse_expressions(self, env):
        self.arg_tuple.analyse_expressions(env)
        self.arg_tuple = self.arg_tuple.coerce_to_pyobject(env)
        self.arg_tuple.release_temp(env)
        env.use_utility_code(printing_utility_code)
        self.gil_check(env)

    gil_message = "Python print statement"

    def generate_execution_code(self, code):
        self.arg_tuple.generate_evaluation_code(code)
        code.putln(
            "if (__Pyx_Print(%s, %d) < 0) %s" % (
                self.arg_tuple.py_result(),
                self.append_newline,
                code.error_goto(self.pos)))
        self.arg_tuple.generate_disposal_code(code)

    def annotate(self, code):
        self.arg_tuple.annotate(code)


class DelStatNode(StatNode):
    #  del statement
    #
    #  args     [ExprNode]
    
    child_attrs = ["args"]

    def analyse_declarations(self, env):
        for arg in self.args:
            arg.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        for arg in self.args:
            arg.analyse_target_expression(env, None)
            if arg.type.is_pyobject:
                self.gil_check(env)
            else:
                error(arg.pos, "Deletion of non-Python object")
            #arg.release_target_temp(env)

    gil_message = "Deleting Python object"

    def generate_execution_code(self, code):
        for arg in self.args:
            if arg.type.is_pyobject:
                arg.generate_deletion_code(code)
            # else error reported earlier

    def annotate(self, code):
        for arg in self.args:
            arg.annotate(code)


class PassStatNode(StatNode):
    #  pass statement

    child_attrs = []
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class BreakStatNode(StatNode):

    child_attrs = []

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        if not code.break_label:
            error(self.pos, "break statement not inside loop")
        else:
            #code.putln(
            #	"goto %s;" %
            #		code.break_label)
            code.put_goto(code.break_label)


class ContinueStatNode(StatNode):

    child_attrs = []

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        if code.funcstate.in_try_finally:
            error(self.pos, "continue statement inside try of try...finally")
        elif not code.continue_label:
            error(self.pos, "continue statement not inside loop")
        else:
            code.put_goto(code.continue_label)


class ReturnStatNode(StatNode):
    #  return statement
    #
    #  value         ExprNode or None
    #  return_type   PyrexType
    #  temps_in_use  [Entry]            Temps in use at time of return
    
    child_attrs = ["value"]

    def analyse_expressions(self, env):
        return_type = env.return_type
        self.return_type = return_type
        self.temps_in_use = env.temps_in_use()
        if not return_type:
            error(self.pos, "Return not inside a function body")
            return
        if self.value:
            self.value.analyse_types(env)
            if return_type.is_void or return_type.is_returncode:
                error(self.value.pos, 
                    "Return with value in void function")
            else:
                self.value = self.value.coerce_to(env.return_type, env)
            self.value.allocate_temps(env)
            self.value.release_temp(env)
        else:
            if (not return_type.is_void
                and not return_type.is_pyobject
                and not return_type.is_returncode):
                    error(self.pos, "Return value required")
        if return_type.is_pyobject:
            self.gil_check(env)

    gil_message = "Returning Python object"

    def generate_execution_code(self, code):
        code.mark_pos(self.pos)
        if not self.return_type:
            # error reported earlier
            return
        if self.value:
            self.value.generate_evaluation_code(code)
            self.value.make_owned_reference(code)
            code.putln(
                "%s = %s;" % (
                    Naming.retval_cname,
                    self.value.result_as(self.return_type)))
            self.value.generate_post_assignment_code(code)
        else:
            if self.return_type.is_pyobject:
                code.put_init_to_py_none(Naming.retval_cname, self.return_type)
            elif self.return_type.is_returncode:
                code.putln(
                    "%s = %s;" % (
                        Naming.retval_cname,
                        self.return_type.default_value))
        for entry in self.temps_in_use:
            code.put_var_decref_clear(entry)
        #code.putln(
        #	"goto %s;" %
        #		code.return_label)
        code.put_goto(code.return_label)
        
    def annotate(self, code):
        if self.value:
            self.value.annotate(code)


class RaiseStatNode(StatNode):
    #  raise statement
    #
    #  exc_type    ExprNode or None
    #  exc_value   ExprNode or None
    #  exc_tb      ExprNode or None
    
    child_attrs = ["exc_type", "exc_value", "exc_tb"]

    def analyse_expressions(self, env):
        if self.exc_type:
            self.exc_type.analyse_types(env)
            self.exc_type = self.exc_type.coerce_to_pyobject(env)
            self.exc_type.allocate_temps(env)
        if self.exc_value:
            self.exc_value.analyse_types(env)
            self.exc_value = self.exc_value.coerce_to_pyobject(env)
            self.exc_value.allocate_temps(env)
        if self.exc_tb:
            self.exc_tb.analyse_types(env)
            self.exc_tb = self.exc_tb.coerce_to_pyobject(env)
            self.exc_tb.allocate_temps(env)
        if self.exc_type:
            self.exc_type.release_temp(env)
        if self.exc_value:
            self.exc_value.release_temp(env)
        if self.exc_tb:
            self.exc_tb.release_temp(env)
        env.use_utility_code(raise_utility_code)
        env.use_utility_code(restore_exception_utility_code)
        self.gil_check(env)

    gil_message = "Raising exception"

    def generate_execution_code(self, code):
        if self.exc_type:
            self.exc_type.generate_evaluation_code(code)
            type_code = self.exc_type.py_result()
        else:
            type_code = 0
        if self.exc_value:
            self.exc_value.generate_evaluation_code(code)
            value_code = self.exc_value.py_result()
        else:
            value_code = "0"
        if self.exc_tb:
            self.exc_tb.generate_evaluation_code(code)
            tb_code = self.exc_tb.py_result()
        else:
            tb_code = "0"
        if self.exc_type or self.exc_value or self.exc_tb:
            code.putln(
                "__Pyx_Raise(%s, %s, %s);" % (
                    type_code,
                    value_code,
                    tb_code))
        else:
            code.putln(
                "__Pyx_ReRaise();")
        if self.exc_type:
            self.exc_type.generate_disposal_code(code)
        if self.exc_value:
            self.exc_value.generate_disposal_code(code)
        if self.exc_tb:
            self.exc_tb.generate_disposal_code(code)
        code.putln(
            code.error_goto(self.pos))

    def annotate(self, code):
        if self.exc_type:
            self.exc_type.annotate(code)
        if self.exc_value:
            self.exc_value.annotate(code)
        if self.exc_tb:
            self.exc_tb.annotate(code)


class ReraiseStatNode(StatNode):

    child_attrs = []

    def analyse_expressions(self, env):
        self.gil_check(env)
        env.use_utility_code(raise_utility_code)
        env.use_utility_code(restore_exception_utility_code)

    gil_message = "Raising exception"

    def generate_execution_code(self, code):
        vars = code.funcstate.exc_vars
        if vars:
            code.putln("__Pyx_Raise(%s, %s, %s);" % tuple(vars))
            code.putln(code.error_goto(self.pos))
        else:
            error(self.pos, "Reraise not inside except clause")
        

class AssertStatNode(StatNode):
    #  assert statement
    #
    #  cond    ExprNode
    #  value   ExprNode or None
    
    child_attrs = ["cond", "value"]

    def analyse_expressions(self, env):
        self.cond = self.cond.analyse_boolean_expression(env)
        if self.value:
            self.value.analyse_types(env)
            self.value = self.value.coerce_to_pyobject(env)
            self.value.allocate_temps(env)
        self.cond.release_temp(env)
        if self.value:
            self.value.release_temp(env)
        self.gil_check(env)
        #env.recycle_pending_temps() # TEMPORARY

    gil_message = "Raising exception"
    
    def generate_execution_code(self, code):
        code.putln("#ifndef PYREX_WITHOUT_ASSERTIONS")
        self.cond.generate_evaluation_code(code)
        code.putln(
            "if (unlikely(!%s)) {" %
                self.cond.result())
        if self.value:
            self.value.generate_evaluation_code(code)
            code.putln(
                "PyErr_SetObject(PyExc_AssertionError, %s);" %
                    self.value.py_result())
            self.value.generate_disposal_code(code)
        else:
            code.putln(
                "PyErr_SetNone(PyExc_AssertionError);")
        code.putln(
                code.error_goto(self.pos))
        code.putln(
            "}")
        self.cond.generate_disposal_code(code)
        code.putln("#endif")

    def annotate(self, code):
        self.cond.annotate(code)
        if self.value:
            self.value.annotate(code)


class IfStatNode(StatNode):
    #  if statement
    #
    #  if_clauses   [IfClauseNode]
    #  else_clause  StatNode or None

    child_attrs = ["if_clauses", "else_clause"]
    
    def analyse_control_flow(self, env):
        env.start_branching(self.pos)
        for if_clause in self.if_clauses:
            if_clause.analyse_control_flow(env)
            env.next_branch(if_clause.end_pos())
        if self.else_clause:
            self.else_clause.analyse_control_flow(env)
        env.finish_branching(self.end_pos())

    def analyse_declarations(self, env):
        for if_clause in self.if_clauses:
            if_clause.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        for if_clause in self.if_clauses:
            if_clause.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        code.mark_pos(self.pos)
        end_label = code.new_label()
        for if_clause in self.if_clauses:
            if_clause.generate_execution_code(code, end_label)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(end_label)
        
    def annotate(self, code):
        for if_clause in self.if_clauses:
            if_clause.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)


class IfClauseNode(Node):
    #  if or elif clause in an if statement
    #
    #  condition   ExprNode
    #  body        StatNode
    
    child_attrs = ["condition", "body"]

    def analyse_control_flow(self, env):
        self.body.analyse_control_flow(env)
        
    def analyse_declarations(self, env):
        self.condition.analyse_declarations(env)
        self.body.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.condition = \
            self.condition.analyse_temp_boolean_expression(env)
        self.condition.release_temp(env)
        self.body.analyse_expressions(env)
    
    def generate_execution_code(self, code, end_label):
        self.condition.generate_evaluation_code(code)
        code.putln(
            "if (%s) {" %
                self.condition.result())
        self.body.generate_execution_code(code)
        #code.putln(
        #	"goto %s;" %
        #		end_label)
        code.put_goto(end_label)
        code.putln("}")

    def annotate(self, code):
        self.condition.annotate(code)
        self.body.annotate(code)
        

class SwitchCaseNode(StatNode):
    # Generated in the optimization of an if-elif-else node
    #
    # conditions    [ExprNode]
    # body          StatNode
    
    child_attrs = ['conditions', 'body']
    
    def generate_execution_code(self, code):
        for cond in self.conditions:
            code.putln("case %s:" % cond.calculate_result_code())
        self.body.generate_execution_code(code)
        code.putln("break;")
        
    def annotate(self, code):
        for cond in self.conditions:
            cond.annotate(code)
        self.body.annotate(code)

class SwitchStatNode(StatNode):
    # Generated in the optimization of an if-elif-else node
    #
    # test          ExprNode
    # cases         [SwitchCaseNode]
    # else_clause   StatNode or None
    
    child_attrs = ['test', 'cases', 'else_clause']
    
    def generate_execution_code(self, code):
        code.putln("switch (%s) {" % self.test.calculate_result_code())
        for case in self.cases:
            case.generate_execution_code(code)
        if self.else_clause is not None:
            code.putln("default:")
            self.else_clause.generate_execution_code(code)
            code.putln("break;")
        code.putln("}")

    def annotate(self, code):
        self.test.annotate(code)
        for case in self.cases:
            case.annotate(code)
        if self.else_clause is not None:
            self.else_clause.annotate(code)
            
class LoopNode:
    
    def analyse_control_flow(self, env):
        env.start_branching(self.pos)
        self.body.analyse_control_flow(env)
        env.next_branch(self.body.end_pos())
        if self.else_clause:
            self.else_clause.analyse_control_flow(env)
        env.finish_branching(self.end_pos())

    
class WhileStatNode(LoopNode, StatNode):
    #  while statement
    #
    #  condition    ExprNode
    #  body         StatNode
    #  else_clause  StatNode

    child_attrs = ["condition", "body", "else_clause"]

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.condition = \
            self.condition.analyse_temp_boolean_expression(env)
        self.condition.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
        self.body.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        code.putln(
            "while (1) {")
        self.condition.generate_evaluation_code(code)
        code.putln(
            "if (!%s) break;" %
                self.condition.result())
        self.body.generate_execution_code(code)
        code.put_label(code.continue_label)
        code.putln("}")
        break_label = code.break_label
        code.set_loop_labels(old_loop_labels)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(break_label)

    def annotate(self, code):
        self.condition.annotate(code)
        self.body.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)


def ForStatNode(pos, **kw):
    if kw.has_key('iterator'):
        return ForInStatNode(pos, **kw)
    else:
        return ForFromStatNode(pos, **kw)

class ForInStatNode(LoopNode, StatNode):
    #  for statement
    #
    #  target        ExprNode
    #  iterator      IteratorNode
    #  body          StatNode
    #  else_clause   StatNode
    #  item          NextNode       used internally
    
    child_attrs = ["target", "iterator", "body", "else_clause"]
    item = None
    
    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
        self.body.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
            
    def analyse_range_step(self, args):
        import ExprNodes
        # The direction must be determined at compile time to set relations. 
        # Otherwise, return False. 
        if len(args) < 3:
            self.step = ExprNodes.IntNode(pos = args[0].pos, value='1')
            self.relation1 = '<='
            self.relation2 = '<'
            return True
        else:
            step = args[2]
            if isinstance(step, ExprNodes.UnaryMinusNode) and isinstance(step.operand, ExprNodes.IntNode):
                step = ExprNodes.IntNode(pos = step.pos, value=str(-int(step.operand.value, 0)))
            if isinstance(step, ExprNodes.IntNode):
                step_value = int(step.value, 0)
                if step_value > 0:
                    self.step = step
                    self.relation1 = '<='
                    self.relation2 = '<'
                    return True
                elif step_value < 0:
                    self.step = ExprNodes.IntNode(pos = step.pos, value=str(-step_value))
                    self.relation1 = '>='
                    self.relation2 = '>'
                    return True
        return False
                
    
    def analyse_expressions(self, env):
        import ExprNodes
        self.target.analyse_target_types(env)
        if Options.convert_range and self.target.type.is_int:
            sequence = self.iterator.sequence
            if isinstance(sequence, ExprNodes.SimpleCallNode) \
                  and sequence.self is None \
                  and isinstance(sequence.function, ExprNodes.NameNode) \
                  and (sequence.function.name == 'range' or sequence.function.name == 'xrange'):
                args = sequence.args
                # Make sure we can determine direction from step
                if self.analyse_range_step(args):
                    # Mutate to ForFrom loop type
                    self.__class__ = ForFromStatNode
                    if len(args) == 1:
                        self.bound1 = ExprNodes.IntNode(pos = sequence.pos, value='0')
                        self.bound2 = args[0]
                    else:
                        self.bound1 = args[0]
                        self.bound2 = args[1]
                    ForFromStatNode.analyse_expressions(self, env)
                    return
                    
        self.iterator.analyse_expressions(env)
        self.item = ExprNodes.NextNode(self.iterator, env)
        self.item = self.item.coerce_to(self.target.type, env)
        self.item.allocate_temps(env)
        self.target.allocate_target_temps(env, self.item)
        #self.item.release_temp(env)
        #self.target.release_target_temp(env)
        self.body.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
        self.iterator.release_temp(env)

    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        self.iterator.generate_evaluation_code(code)
        code.putln(
            "for (;;) {")
        self.item.generate_evaluation_code(code)
        self.target.generate_assignment_code(self.item, code)
        self.body.generate_execution_code(code)
        code.put_label(code.continue_label)
        code.putln(
            "}")
        break_label = code.break_label
        code.set_loop_labels(old_loop_labels)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(break_label)
        self.iterator.generate_disposal_code(code)

    def annotate(self, code):
        self.target.annotate(code)
        self.iterator.annotate(code)
        self.body.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)
        self.item.annotate(code)


class ForFromStatNode(LoopNode, StatNode):
    #  for name from expr rel name rel expr
    #
    #  target        NameNode
    #  bound1        ExprNode
    #  relation1     string
    #  relation2     string
    #  bound2        ExprNode
    #  step          ExprNode or None
    #  body          StatNode
    #  else_clause   StatNode or None
    #
    #  Used internally:
    #
    #  is_py_target       bool
    #  loopvar_name       string
    #  py_loopvar_node    PyTempNode or None
    child_attrs = ["target", "bound1", "bound2", "step", "body", "else_clause"]
    
    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
        self.body.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        import ExprNodes
        self.target.analyse_target_types(env)
        self.bound1.analyse_types(env)
        self.bound2.analyse_types(env)
        if self.target.type.is_numeric:
            self.bound1 = self.bound1.coerce_to(self.target.type, env)
            self.bound2 = self.bound2.coerce_to(self.target.type, env)
        else:
            self.bound1 = self.bound1.coerce_to_integer(env)
            self.bound2 = self.bound2.coerce_to_integer(env)
        if self.step is not None:
            if isinstance(self.step, ExprNodes.UnaryMinusNode):
                warning(self.step.pos, "Probable infinite loop in for-from-by statment. Consider switching the directions of the relations.", 2)
            self.step.analyse_types(env)
            self.step = self.step.coerce_to_integer(env)
        if not (self.bound2.is_name or self.bound2.is_literal):
            self.bound2 = self.bound2.coerce_to_temp(env)
        target_type = self.target.type
        if not (target_type.is_pyobject or target_type.is_numeric):
            error(self.target.pos,
                "Integer for-loop variable must be of type int or Python object")
        #if not (target_type.is_pyobject
        #	or target_type.assignable_from(PyrexTypes.c_int_type)):
        #		error(self.target.pos,
        #			"Cannot assign integer to variable of type '%s'" % target_type)
        if target_type.is_numeric:
            self.is_py_target = 0
            if isinstance(self.target, ExprNodes.IndexNode) and self.target.is_buffer_access:
                raise error(self.pos, "Buffer indexing not allowed as for loop target.")
            self.loopvar_name = self.target.entry.cname
            self.py_loopvar_node = None
        else:
            self.is_py_target = 1
            c_loopvar_node = ExprNodes.TempNode(self.pos, 
                PyrexTypes.c_long_type, env)
            c_loopvar_node.allocate_temps(env)
            self.loopvar_name = c_loopvar_node.result()
            self.py_loopvar_node = \
                ExprNodes.CloneNode(c_loopvar_node).coerce_to_pyobject(env)
        self.bound1.allocate_temps(env)
        self.bound2.allocate_temps(env)
        if self.step is not None:
            self.step.allocate_temps(env)
        if self.is_py_target:
            self.py_loopvar_node.allocate_temps(env)
            self.target.allocate_target_temps(env, self.py_loopvar_node)
            #self.target.release_target_temp(env)
            #self.py_loopvar_node.release_temp(env)
        self.body.analyse_expressions(env)
        if self.is_py_target:
            c_loopvar_node.release_temp(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
        self.bound1.release_temp(env)
        self.bound2.release_temp(env)
        if self.step is not None:
            self.step.release_temp(env)
            
    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        self.bound1.generate_evaluation_code(code)
        self.bound2.generate_evaluation_code(code)
        offset, incop = self.relation_table[self.relation1]
        if self.step is not None:
            self.step.generate_evaluation_code(code)
            incop = "%s=%s" % (incop[0], self.step.result())
        code.putln(
            "for (%s = %s%s; %s %s %s; %s%s) {" % (
                self.loopvar_name,
                self.bound1.result(), offset,
                self.loopvar_name, self.relation2, self.bound2.result(),
                self.loopvar_name, incop))
        if self.py_loopvar_node:
            self.py_loopvar_node.generate_evaluation_code(code)
            self.target.generate_assignment_code(self.py_loopvar_node, code)
        self.body.generate_execution_code(code)
        code.put_label(code.continue_label)
        code.putln("}")
        break_label = code.break_label
        code.set_loop_labels(old_loop_labels)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(break_label)
        self.bound1.generate_disposal_code(code)
        self.bound2.generate_disposal_code(code)
        if self.step is not None:
            self.step.generate_disposal_code(code)
    
    relation_table = {
        # {relop : (initial offset, increment op)}
        '<=': ("",   "++"),
        '<' : ("+1", "++"),
        '>=': ("",   "--"),
        '>' : ("-1", "--")
    }
    
    def annotate(self, code):
        self.target.annotate(code)
        self.bound1.annotate(code)
        self.bound2.annotate(code)
        if self.step:
            self.bound2.annotate(code)
        self.body.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)


class WithStatNode(StatNode):
    """
    Represents a Python with statement.
    
    This is only used at parse tree level; and is not present in
    analysis or generation phases.
    """
    #  manager          The with statement manager object
    #  target            Node (lhs expression)
    #  body             StatNode
    child_attrs = ["manager", "target", "body"]

class TryExceptStatNode(StatNode):
    #  try .. except statement
    #
    #  body             StatNode
    #  except_clauses   [ExceptClauseNode]
    #  else_clause      StatNode or None
    #  cleanup_list     [Entry]            temps to clean up on error

    child_attrs = ["body", "except_clauses", "else_clause"]
    
    def analyse_control_flow(self, env):
        env.start_branching(self.pos)
        self.body.analyse_control_flow(env)
        successful_try = env.control_flow # grab this for later
        env.next_branch(self.body.end_pos())
        env.finish_branching(self.body.end_pos())
        
        env.start_branching(self.except_clauses[0].pos)
        for except_clause in self.except_clauses:
            except_clause.analyse_control_flow(env)
            env.next_branch(except_clause.end_pos())
            
        # the else cause it executed only when the try clause finishes
        env.control_flow.incoming = successful_try
        if self.else_clause:
            self.else_clause.analyse_control_flow(env)
        env.finish_branching(self.end_pos())

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        for except_clause in self.except_clauses:
            except_clause.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
        self.gil_check(env)
        env.use_utility_code(reset_exception_utility_code)
    
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
        self.cleanup_list = env.free_temp_entries[:]
        default_clause_seen = 0
        for except_clause in self.except_clauses:
            except_clause.analyse_expressions(env)
            if default_clause_seen:
                error(except_clause.pos, "default 'except:' must be last")
            if not except_clause.pattern:
                default_clause_seen = 1
        self.has_default_clause = default_clause_seen
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
        self.gil_check(env)

    gil_message = "Try-except statement"

    def generate_execution_code(self, code):
        old_return_label = code.return_label
        old_error_label = code.new_error_label()
        our_error_label = code.error_label
        except_end_label = code.new_label('exception_handled')
        except_error_label = code.new_label('except_error')
        except_return_label = code.new_label('except_return')
        try_return_label = code.new_label('try_return')
        try_end_label = code.new_label('try')

        code.putln("{")
        code.putln("PyObject %s;" %
                   ', '.join(['*%s' % var for var in Naming.exc_save_vars]))
        code.putln("__Pyx_ExceptionSave(%s);" %
                   ', '.join(['&%s' % var for var in Naming.exc_save_vars]))
        code.putln(
            "/*try:*/ {")
        code.return_label = try_return_label
        self.body.generate_execution_code(code)
        code.putln(
            "}")
        code.error_label = except_error_label
        code.return_label = except_return_label
        if self.else_clause:
            code.putln(
                "/*else:*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln(
                "}")
        for var in Naming.exc_save_vars:
            code.put_xdecref_clear(var, py_object_type)
        code.put_goto(try_end_label)
        if code.label_used(try_return_label):
            code.put_label(try_return_label)
            for var in Naming.exc_save_vars:
                code.put_xdecref_clear(var, py_object_type)
            code.put_goto(old_return_label)
        code.put_label(our_error_label)
        code.put_var_xdecrefs_clear(self.cleanup_list)
        for except_clause in self.except_clauses:
            except_clause.generate_handling_code(code, except_end_label)

        error_label_used = code.label_used(except_error_label)
        if error_label_used or not self.has_default_clause:
            if error_label_used:
                code.put_label(except_error_label)
            for var in Naming.exc_save_vars:
                code.put_xdecref(var, py_object_type)
            code.put_goto(old_error_label)

        if code.label_used(except_return_label):
            code.put_label(except_return_label)
            code.putln("__Pyx_ExceptionReset(%s);" %
                       ', '.join(Naming.exc_save_vars))
            code.put_goto(old_return_label)

        if code.label_used(except_end_label):
            code.put_label(except_end_label)
            code.putln("__Pyx_ExceptionReset(%s);" %
                       ', '.join(Naming.exc_save_vars))
        code.put_label(try_end_label)
        code.putln("}")

        code.return_label = old_return_label
        code.error_label = old_error_label

    def annotate(self, code):
        self.body.annotate(code)
        for except_node in self.except_clauses:
            except_node.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)


class ExceptClauseNode(Node):
    #  Part of try ... except statement.
    #
    #  pattern        ExprNode
    #  target         ExprNode or None
    #  body           StatNode
    #  excinfo_target NameNode or None   optional target for exception info
    #  match_flag     string             result of exception match
    #  exc_value      ExcValueNode       used internally
    #  function_name  string             qualified name of enclosing function
    #  exc_vars       (string * 3)       local exception variables

    # excinfo_target is never set by the parser, but can be set by a transform
    # in order to extract more extensive information about the exception as a
    # sys.exc_info()-style tuple into a target variable
    
    child_attrs = ["pattern", "target", "body", "exc_value", "excinfo_target"]

    exc_value = None
    excinfo_target = None

    def analyse_declarations(self, env):
        if self.target:
            self.target.analyse_target_declaration(env)
        if self.excinfo_target is not None:
            self.excinfo_target.analyse_target_declaration(env)
        self.body.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        import ExprNodes
        genv = env.global_scope()
        self.function_name = env.qualified_name
        if self.pattern:
            self.pattern.analyse_expressions(env)
            self.pattern = self.pattern.coerce_to_pyobject(env)
            self.match_flag = env.allocate_temp(PyrexTypes.c_int_type)
            self.pattern.release_temp(env)
            env.release_temp(self.match_flag)
        self.exc_vars = [env.allocate_temp(py_object_type) for i in xrange(3)]
        if self.target:
            self.exc_value = ExprNodes.ExcValueNode(self.pos, env, self.exc_vars[1])
            self.exc_value.allocate_temps(env)
            self.target.analyse_target_expression(env, self.exc_value)
        if self.excinfo_target is not None:
            import ExprNodes
            self.excinfo_tuple = ExprNodes.TupleNode(pos=self.pos, args=[
                ExprNodes.ExcValueNode(pos=self.pos, env=env, var=self.exc_vars[0]),
                ExprNodes.ExcValueNode(pos=self.pos, env=env, var=self.exc_vars[1]),
                ExprNodes.ExcValueNode(pos=self.pos, env=env, var=self.exc_vars[2])
            ])
            self.excinfo_tuple.analyse_expressions(env)
            self.excinfo_tuple.allocate_temps(env)
            self.excinfo_target.analyse_target_expression(env, self.excinfo_tuple)

        self.body.analyse_expressions(env)
        for var in self.exc_vars:
            env.release_temp(var)
        env.use_utility_code(get_exception_utility_code)
        env.use_utility_code(restore_exception_utility_code)
    
    def generate_handling_code(self, code, end_label):
        code.mark_pos(self.pos)
        if self.pattern:
            self.pattern.generate_evaluation_code(code)
            code.putln(
                "%s = PyErr_ExceptionMatches(%s);" % (
                    self.match_flag,
                    self.pattern.py_result()))
            self.pattern.generate_disposal_code(code)
            code.putln(
                "if (%s) {" %
                    self.match_flag)
        else:
            code.putln("/*except:*/ {")
        code.putln('__Pyx_AddTraceback("%s");' % self.function_name)
        # We always have to fetch the exception value even if
        # there is no target, because this also normalises the 
        # exception and stores it in the thread state.
        exc_args = "&%s, &%s, &%s" % tuple(self.exc_vars)
        code.putln("if (__Pyx_GetException(%s) < 0) %s" % (exc_args,
            code.error_goto(self.pos)))
        if self.target:
            self.exc_value.generate_evaluation_code(code)
            self.target.generate_assignment_code(self.exc_value, code)
        if self.excinfo_target is not None:
            self.excinfo_tuple.generate_evaluation_code(code)
            self.excinfo_target.generate_assignment_code(self.excinfo_tuple, code)

        old_exc_vars = code.funcstate.exc_vars
        code.funcstate.exc_vars = self.exc_vars
        self.body.generate_execution_code(code)
        code.funcstate.exc_vars = old_exc_vars
        for var in self.exc_vars:
            code.putln("Py_DECREF(%s); %s = 0;" % (var, var))
        code.put_goto(end_label)
        code.putln(
            "}")

    def annotate(self, code):
        if self.pattern:
            self.pattern.annotate(code)
        if self.target:
            self.target.annotate(code)
        self.body.annotate(code)


class TryFinallyStatNode(StatNode):
    #  try ... finally statement
    #
    #  body             StatNode
    #  finally_clause   StatNode
    #
    #  cleanup_list     [Entry]      temps to clean up on error
    #
    #  The plan is that we funnel all continue, break
    #  return and error gotos into the beginning of the
    #  finally block, setting a variable to remember which
    #  one we're doing. At the end of the finally block, we
    #  switch on the variable to figure out where to go.
    #  In addition, if we're doing an error, we save the
    #  exception on entry to the finally block and restore
    #  it on exit.

    child_attrs = ["body", "finally_clause"]
    
    preserve_exception = 1
    
    disallow_continue_in_try_finally = 0
    # There doesn't seem to be any point in disallowing
    # continue in the try block, since we have no problem
    # handling it.

    def create_analysed(pos, env, body, finally_clause):
        node = TryFinallyStatNode(pos, body=body, finally_clause=finally_clause)
        node.cleanup_list = []
        return node
    create_analysed = staticmethod(create_analysed)
    
    def analyse_control_flow(self, env):
        env.start_branching(self.pos)
        self.body.analyse_control_flow(env)
        env.next_branch(self.body.end_pos())
        env.finish_branching(self.body.end_pos())
        self.finally_clause.analyse_control_flow(env)

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        self.finally_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
        self.cleanup_list = env.free_temp_entries[:]
        self.finally_clause.analyse_expressions(env)
        self.gil_check(env)

    gil_message = "Try-finally statement"

    def generate_execution_code(self, code):
        old_error_label = code.error_label
        old_labels = code.all_new_labels()
        new_labels = code.get_all_labels()
        new_error_label = code.error_label
        catch_label = code.new_label()
        code.putln(
            "/*try:*/ {")
        if self.disallow_continue_in_try_finally:
            was_in_try_finally = code.funcstate.in_try_finally
            code.funcstate.in_try_finally = 1
        self.body.generate_execution_code(code)
        if self.disallow_continue_in_try_finally:
            code.funcstate.in_try_finally = was_in_try_finally
        code.putln(
            "}")
        code.putln(
            "/*finally:*/ {")
        cases_used = []
        error_label_used = 0
        for i, new_label in enumerate(new_labels):
            if new_label in code.labels_used:
                cases_used.append(i)
                if new_label == new_error_label:
                    error_label_used = 1
                    error_label_case = i
        if cases_used:
            code.putln(
                    "int __pyx_why;")
            if error_label_used and self.preserve_exception:
                code.putln(
                    "PyObject *%s, *%s, *%s;" % Naming.exc_vars)
                code.putln(
                    "int %s;" % Naming.exc_lineno_name)
                exc_var_init_zero = ''.join(["%s = 0; " % var for var in Naming.exc_vars])
                exc_var_init_zero += '%s = 0;' % Naming.exc_lineno_name
                code.putln(exc_var_init_zero)
            else:
                exc_var_init_zero = None
            code.use_label(catch_label)
            code.putln(
                    "__pyx_why = 0; goto %s;" % catch_label)
            for i in cases_used:
                new_label = new_labels[i]
                #if new_label and new_label != "<try>":
                if new_label == new_error_label and self.preserve_exception:
                    self.put_error_catcher(code, 
                        new_error_label, i+1, catch_label)
                else:
                    code.put('%s: ' % new_label)
                    if exc_var_init_zero:
                        code.putln(exc_var_init_zero)
                    code.putln("__pyx_why = %s; goto %s;" % (
                            i+1,
                            catch_label))
            code.put_label(catch_label)
        code.set_all_labels(old_labels)
        if error_label_used:
            code.new_error_label()
            finally_error_label = code.error_label
        self.finally_clause.generate_execution_code(code)
        if error_label_used:
            if finally_error_label in code.labels_used and self.preserve_exception:
                over_label = code.new_label()
                code.put_goto(over_label);
                code.put_label(finally_error_label)
                code.putln("if (__pyx_why == %d) {" % (error_label_case + 1))
                for var in Naming.exc_vars:
                    code.putln("Py_XDECREF(%s);" % var)
                code.putln("}")
                code.put_goto(old_error_label)
                code.put_label(over_label)
            code.error_label = old_error_label
        if cases_used:
            code.putln(
                "switch (__pyx_why) {")
            for i in cases_used:
                old_label = old_labels[i]
                if old_label == old_error_label and self.preserve_exception:
                    self.put_error_uncatcher(code, i+1, old_error_label)
                else:
                    code.use_label(old_label)
                    code.putln(
                        "case %s: goto %s;" % (
                            i+1,
                            old_label))
            code.putln(
                "}")		
        code.putln(
            "}")

    def put_error_catcher(self, code, error_label, i, catch_label):
        code.globalstate.use_utility_code(restore_exception_utility_code)
        code.putln(
            "%s: {" %
                error_label)
        code.putln(
                "__pyx_why = %s;" %
                    i)
        code.put_var_xdecrefs_clear(self.cleanup_list)
        code.putln(
                "__Pyx_ErrFetch(&%s, &%s, &%s);" %
                    Naming.exc_vars)
        code.putln(
                "%s = %s;" % (
                    Naming.exc_lineno_name, Naming.lineno_cname))
        #code.putln(
        #		"goto %s;" %
        #			catch_label)
        code.put_goto(catch_label)
        code.putln(
            "}")
            
    def put_error_uncatcher(self, code, i, error_label):
        code.globalstate.use_utility_code(restore_exception_utility_code)
        code.putln(
            "case %s: {" %
                i)
        code.putln(
                "__Pyx_ErrRestore(%s, %s, %s);" %
                    Naming.exc_vars)
        code.putln(
                "%s = %s;" % (
                    Naming.lineno_cname, Naming.exc_lineno_name))
        for var in Naming.exc_vars:
            code.putln(
                "%s = 0;" %
                    var)
        code.put_goto(error_label)
        code.putln(
            "}")

    def annotate(self, code):
        self.body.annotate(code)
        self.finally_clause.annotate(code)


class GILStatNode(TryFinallyStatNode):
    #  'with gil' or 'with nogil' statement
    #
    #   state   string   'gil' or 'nogil'
        
    child_attrs = []
    
    preserve_exception = 0

    def __init__(self, pos, state, body):
        self.state = state
        TryFinallyStatNode.__init__(self, pos,
            body = body,
            finally_clause = GILExitNode(pos, state = state))

    def analyse_expressions(self, env):
        was_nogil = env.nogil
        env.nogil = 1
        TryFinallyStatNode.analyse_expressions(self, env)
        env.nogil = was_nogil

    def gil_check(self, env):
        pass

    def generate_execution_code(self, code):
        code.putln("/*with %s:*/ {" % self.state)
        if self.state == 'gil':
            code.putln("PyGILState_STATE _save = PyGILState_Ensure();")
        else:
            code.putln("PyThreadState *_save;")
            code.putln("Py_UNBLOCK_THREADS")
        TryFinallyStatNode.generate_execution_code(self, code)
        code.putln("}")


class GILExitNode(StatNode):
    #  Used as the 'finally' block in a GILStatNode
    #
    #  state   string   'gil' or 'nogil'

    child_attrs = []

    def analyse_expressions(self, env):
        pass

    def generate_execution_code(self, code):
        if self.state == 'gil':
            code.putln("PyGILState_Release();")
        else:
            code.putln("Py_BLOCK_THREADS")


class CImportStatNode(StatNode):
    #  cimport statement
    #
    #  module_name   string           Qualified name of module being imported
    #  as_name       string or None   Name specified in "as" clause, if any

    child_attrs = []
    
    def analyse_declarations(self, env):
        if not env.is_module_scope:
            error(self.pos, "cimport only allowed at module level")
            return
        module_scope = env.find_module(self.module_name, self.pos)
        if "." in self.module_name:
            names = [EncodedString(name) for name in self.module_name.split(".")]
            top_name = names[0]
            top_module_scope = env.context.find_submodule(top_name)
            module_scope = top_module_scope
            for name in names[1:]:
                submodule_scope = module_scope.find_submodule(name)
                module_scope.declare_module(name, submodule_scope, self.pos)
                module_scope = submodule_scope
            if self.as_name:
                env.declare_module(self.as_name, module_scope, self.pos)
            else:
                env.declare_module(top_name, top_module_scope, self.pos)
        else:
            name = self.as_name or self.module_name
            env.declare_module(name, module_scope, self.pos)

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass
    

class FromCImportStatNode(StatNode):
    #  from ... cimport statement
    #
    #  module_name     string                        Qualified name of module
    #  imported_names  [(pos, name, as_name, kind)]  Names to be imported
    
    child_attrs = []

    def analyse_declarations(self, env):
        if not env.is_module_scope:
            error(self.pos, "cimport only allowed at module level")
            return
        module_scope = env.find_module(self.module_name, self.pos)
        env.add_imported_module(module_scope)
        for pos, name, as_name, kind in self.imported_names:
            if name == "*":
                for local_name, entry in module_scope.entries.items():
                    env.add_imported_entry(local_name, entry, pos)
            else:
                entry = module_scope.lookup(name)
                if entry:
                    if kind and not self.declaration_matches(entry, kind):
                        entry.redeclared(pos)
                else:
                    if kind == 'struct' or kind == 'union':
                        entry = module_scope.declare_struct_or_union(name,
                            kind = kind, scope = None, typedef_flag = 0, pos = pos)
                    elif kind == 'class':
                        entry = module_scope.declare_c_class(name, pos = pos,
                            module_name = self.module_name)
                    else:
                        error(pos, "Name '%s' not declared in module '%s'"
                            % (name, self.module_name))
                        
                if entry:
                    local_name = as_name or name
                    env.add_imported_entry(local_name, entry, pos)
    
    def declaration_matches(self, entry, kind):
		if not entry.is_type:
			return 0
		type = entry.type
		if kind == 'class':
			if not type.is_extension_type:
				return 0
		else:
			if not type.is_struct_or_union:
				return 0
			if kind <> type.kind:
				return 0
		return 1

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class FromImportStatNode(StatNode):
    #  from ... import statement
    #
    #  module           ImportNode
    #  items            [(string, NameNode)]
    #  interned_items   [(string, NameNode)]
    #  item             PyTempNode            used internally
    #  import_star      boolean               used internally

    child_attrs = ["module"]
    import_star = 0
    
    def analyse_declarations(self, env):
        for name, target in self.items:
            if name == "*":
                if not env.is_module_scope:
                    error(self.pos, "import * only allowed at module level")
                    return
                env.has_import_star = 1
                self.import_star = 1
            else:
                target.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        import ExprNodes
        self.module.analyse_expressions(env)
        self.item = ExprNodes.PyTempNode(self.pos, env)
        self.item.allocate_temp(env)
        self.interned_items = []
        for name, target in self.items:
            if name == '*':
                for _, entry in env.entries.items():
                    if not entry.is_type and entry.type.is_extension_type:
                        env.use_utility_code(ExprNodes.type_test_utility_code)
                        break
            else:
                self.interned_items.append(
                    (env.intern_identifier(name), target))
                target.analyse_target_expression(env, None)
                #target.release_target_temp(env) # was release_temp ?!?
        self.module.release_temp(env)
        self.item.release_temp(env)
    
    def generate_execution_code(self, code):
        self.module.generate_evaluation_code(code)
        if self.import_star:
            code.putln(
                'if (%s(%s) < 0) %s;' % (
                    Naming.import_star,
                    self.module.py_result(),
                    code.error_goto(self.pos)))
        for cname, target in self.interned_items:
            code.putln(
                '%s = PyObject_GetAttr(%s, %s); %s' % (
                    self.item.result(), 
                    self.module.py_result(),
                    cname,
                    code.error_goto_if_null(self.item.result(), self.pos)))
            target.generate_assignment_code(self.item, code)
        self.module.generate_disposal_code(code)



#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

utility_function_predeclarations = \
"""
#ifdef __GNUC__
#define INLINE __inline__
#elif _WIN32
#define INLINE __inline
#else
#define INLINE 
#endif

typedef struct {PyObject **p; char *s; long n; char is_unicode; char intern; char is_identifier;} __Pyx_StringTabEntry; /*proto*/

""" + """

static int %(skip_dispatch_cname)s = 0;

""" % { 'skip_dispatch_cname': Naming.skip_dispatch_cname }

if Options.gcc_branch_hints:
    branch_prediction_macros = \
    """
#ifdef __GNUC__
/* Test for GCC > 2.95 */
#if __GNUC__ > 2 || \
              (__GNUC__ == 2 && (__GNUC_MINOR__ > 95)) 
#define likely(x)   __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)
#else /* __GNUC__ > 2 ... */
#define likely(x)   (x)
#define unlikely(x) (x)
#endif /* __GNUC__ > 2 ... */
#else /* __GNUC__ */
#define likely(x)   (x)
#define unlikely(x) (x)
#endif /* __GNUC__ */
    """
else:
    branch_prediction_macros = \
    """
#define likely(x)   (x)
#define unlikely(x) (x)
    """

#get_name_predeclaration = \
#"static PyObject *__Pyx_GetName(PyObject *dict, char *name); /*proto*/"

#get_name_interned_predeclaration = \
#"static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/"

#------------------------------------------------------------------------------------

printing_utility_code = UtilityCode(
proto = """
static int __Pyx_Print(PyObject *, int); /*proto*/
#if PY_MAJOR_VERSION >= 3
static PyObject* %s = 0;
static PyObject* %s = 0;
#endif
""" % (Naming.print_function, Naming.print_function_kwargs),
impl = r"""
#if PY_MAJOR_VERSION < 3
static PyObject *__Pyx_GetStdout(void) {
    PyObject *f = PySys_GetObject("stdout");
    if (!f) {
        PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
    }
    return f;
}

static int __Pyx_Print(PyObject *arg_tuple, int newline) {
    PyObject *f;
    PyObject* v;
    int i;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    for (i=0; i < PyTuple_GET_SIZE(arg_tuple); i++) {
        if (PyFile_SoftSpace(f, 1)) {
            if (PyFile_WriteString(" ", f) < 0)
                return -1;
        }
        v = PyTuple_GET_ITEM(arg_tuple, i);
        if (PyFile_WriteObject(v, f, Py_PRINT_RAW) < 0)
            return -1;
        if (PyString_Check(v)) {
            char *s = PyString_AsString(v);
            Py_ssize_t len = PyString_Size(v);
            if (len > 0 &&
                isspace(Py_CHARMASK(s[len-1])) &&
                s[len-1] != ' ')
                    PyFile_SoftSpace(f, 0);
        }
    }
    if (newline) {
        if (PyFile_WriteString("\n", f) < 0)
            return -1;
        PyFile_SoftSpace(f, 0);
    }
    return 0;
}

#else /* Python 3 has a print function */
static int __Pyx_Print(PyObject *arg_tuple, int newline) {
    PyObject* kwargs = 0;
    PyObject* result = 0;
    PyObject* end_string;
    if (!%(PRINT_FUNCTION)s) {
        %(PRINT_FUNCTION)s = PyObject_GetAttrString(%(BUILTINS)s, "print");
        if (!%(PRINT_FUNCTION)s)
            return -1;
    }
    if (!newline) {
        if (!%(PRINT_KWARGS)s) {
            %(PRINT_KWARGS)s = PyDict_New();
            if (!%(PRINT_KWARGS)s)
                return -1;
            end_string = PyUnicode_FromStringAndSize(" ", 1);
            if (!end_string)
                return -1;
            if (PyDict_SetItemString(%(PRINT_KWARGS)s, "end", end_string) < 0) {
                Py_DECREF(end_string);
                return -1;
            }
            Py_DECREF(end_string);
        }
        kwargs = %(PRINT_KWARGS)s;
    }
    result = PyObject_Call(%(PRINT_FUNCTION)s, arg_tuple, kwargs);
    if (!result)
        return -1;
    Py_DECREF(result);
    return 0;
}
#endif
""" % {'BUILTINS'       : Naming.builtins_cname,
       'PRINT_FUNCTION' : Naming.print_function,
       'PRINT_KWARGS'   : Naming.print_function_kwargs}
)

#------------------------------------------------------------------------------------

# The following function is based on do_raise() from ceval.c.

raise_utility_code = UtilityCode(
proto = """
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
""",
impl = """
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb) {
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    /* First, check the traceback argument, replacing None with NULL. */
    if (tb == Py_None) {
        Py_DECREF(tb);
        tb = 0;
    }
    else if (tb != NULL && !PyTraceBack_Check(tb)) {
        PyErr_SetString(PyExc_TypeError,
            "raise: arg 3 must be a traceback or None");
        goto raise_error;
    }
    /* Next, replace a missing value with None */
    if (value == NULL) {
        value = Py_None;
        Py_INCREF(value);
    }
    #if PY_VERSION_HEX < 0x02050000
    if (!PyClass_Check(type))
    #else
    if (!PyType_Check(type))
    #endif
    {
        /* Raising an instance.  The value should be a dummy. */
        if (value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
                "instance exception may not have a separate value");
            goto raise_error;
        }
        /* Normalize to raise <class>, <instance> */
        Py_DECREF(value);
        value = type;
        #if PY_VERSION_HEX < 0x02050000
            if (PyInstance_Check(type)) {
                type = (PyObject*) ((PyInstanceObject*)type)->in_class;
                Py_INCREF(type);
            }
            else {
                type = 0;
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception must be an old-style class or instance");
                goto raise_error;
            }
        #else
            type = (PyObject*) Py_TYPE(type);
            Py_INCREF(type);
            if (!PyType_IsSubtype((PyTypeObject *)type, (PyTypeObject *)PyExc_BaseException)) {
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception class must be a subclass of BaseException");
                goto raise_error;
            }
        #endif
    }
    __Pyx_ErrRestore(type, value, tb);
    return;
raise_error:
    Py_XDECREF(value);
    Py_XDECREF(type);
    Py_XDECREF(tb);
    return;
}
""")

#------------------------------------------------------------------------------------

reraise_utility_code = UtilityCode(
proto = """
static void __Pyx_ReRaise(void); /*proto*/
""",
impl = """
static void __Pyx_ReRaise(void) {
    PyThreadState *tstate = PyThreadState_Get();
    PyObject *type = tstate->exc_type;
    PyObject *value = tstate->exc_value;
    PyObject *tb = tstate->exc_traceback;
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    __Pyx_ErrRestore(type, value, tb);
}
""")

#------------------------------------------------------------------------------------

arg_type_test_utility_code = UtilityCode(
proto = """
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed,
    const char *name, int exact); /*proto*/
""",
impl = """
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed,
    const char *name, int exact)
{
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if (none_allowed && obj == Py_None) return 1;
    else if (exact) {
        if (Py_TYPE(obj) == type) return 1;
    }
    else {
        if (PyObject_TypeCheck(obj, type)) return 1;
    }
    PyErr_Format(PyExc_TypeError,
        "Argument '%s' has incorrect type (expected %s, got %s)",
        name, type->tp_name, Py_TYPE(obj)->tp_name);
    return 0;
}
""")

#------------------------------------------------------------------------------------
#
#  __Pyx_RaiseArgtupleInvalid raises the correct exception when too
#  many or too few positional arguments were found.  This handles
#  Py_ssize_t formatting correctly.

raise_argtuple_invalid_utility_code = UtilityCode(
proto = """
static void __Pyx_RaiseArgtupleInvalid(const char* func_name, int exact,
    Py_ssize_t num_min, Py_ssize_t num_max, Py_ssize_t num_found); /*proto*/
""",
impl = """
static void __Pyx_RaiseArgtupleInvalid(
    const char* func_name,
    int exact,
    Py_ssize_t num_min,
    Py_ssize_t num_max,
    Py_ssize_t num_found)
{
    Py_ssize_t num_expected;
    const char *number, *more_or_less;

    if (num_found < num_min) {
        num_expected = num_min;
        more_or_less = "at least";
    } else {
        num_expected = num_max;
        more_or_less = "at most";
    }
    if (exact) {
        more_or_less = "exactly";
    }
    number = (num_expected == 1) ? "" : "s";
    PyErr_Format(PyExc_TypeError,
        #if PY_VERSION_HEX < 0x02050000
            "%s() takes %s %d positional argument%s (%d given)",
        #else
            "%s() takes %s %zd positional argument%s (%zd given)",
        #endif
        func_name, more_or_less, num_expected, number, num_found);
}
""")

raise_keyword_required_utility_code = UtilityCode(
proto = """
static INLINE void __Pyx_RaiseKeywordRequired(const char* func_name, PyObject* kw_name); /*proto*/
""",
impl = """
static INLINE void __Pyx_RaiseKeywordRequired(
    const char* func_name,
    PyObject* kw_name)
{
    PyErr_Format(PyExc_TypeError,
        #if PY_MAJOR_VERSION >= 3
        "%s() needs keyword-only argument %U", func_name, kw_name);
        #else
        "%s() needs keyword-only argument %s", func_name,
        PyString_AS_STRING(kw_name));
        #endif
}
""")

raise_double_keywords_utility_code = UtilityCode(
proto = """
static void __Pyx_RaiseDoubleKeywordsError(
    const char* func_name, PyObject* kw_name); /*proto*/
""",
impl = """
static void __Pyx_RaiseDoubleKeywordsError(
    const char* func_name,
    PyObject* kw_name)
{
    PyErr_Format(PyExc_TypeError,
        #if PY_MAJOR_VERSION >= 3
        "%s() got multiple values for keyword argument '%U'", func_name, kw_name);
        #else
        "%s() got multiple values for keyword argument '%s'", func_name,
        PyString_AS_STRING(kw_name));
        #endif
}
""")

#------------------------------------------------------------------------------------
#
#  __Pyx_CheckKeywordStrings raises an error if non-string keywords
#  were passed to a function, or if any keywords were passed to a
#  function that does not accept them.

keyword_string_check_utility_code = UtilityCode(
proto = """
static INLINE int __Pyx_CheckKeywordStrings(PyObject *kwdict,
    const char* function_name, int kw_allowed); /*proto*/
""",
impl = """
static INLINE int __Pyx_CheckKeywordStrings(
    PyObject *kwdict,
    const char* function_name,
    int kw_allowed)
{
    PyObject* key = 0;
    Py_ssize_t pos = 0;
    while (PyDict_Next(kwdict, &pos, &key, 0)) {
        #if PY_MAJOR_VERSION < 3
        if (unlikely(!PyString_CheckExact(key)) && unlikely(!PyString_Check(key)))
        #else
        if (unlikely(!PyUnicode_CheckExact(key)) && unlikely(!PyUnicode_Check(key)))
        #endif
            goto invalid_keyword_type;
    }
    if ((!kw_allowed) && unlikely(key))
        goto invalid_keyword;
    return 1;
invalid_keyword_type:
    PyErr_Format(PyExc_TypeError,
        "%s() keywords must be strings", function_name);
    return 0;
invalid_keyword:
    PyErr_Format(PyExc_TypeError,
    #if PY_MAJOR_VERSION < 3
        "%s() got an unexpected keyword argument '%s'",
        function_name, PyString_AsString(key));
    #else
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
    #endif
    return 0;
}
""")

#------------------------------------------------------------------------------------
#
#  __Pyx_ParseOptionalKeywords copies the optional/unknown keyword
#  arguments from the kwds dict into kwds2.  If kwds2 is NULL, unknown
#  keywords will raise an invalid keyword error.
#
#  Three kinds of errors are checked: 1) non-string keywords, 2)
#  unexpected keywords and 3) overlap with positional arguments.
#
#  If num_posargs is greater 0, it denotes the number of positional
#  arguments that were passed and that must therefore not appear
#  amongst the keywords as well.
#
#  This method does not check for required keyword arguments.
#

parse_keywords_utility_code = UtilityCode(
proto = """
static int __Pyx_ParseOptionalKeywords(PyObject *kwds, PyObject **argnames[], \
    PyObject *kwds2, PyObject *values[], Py_ssize_t num_pos_args, \
    const char* function_name); /*proto*/
""",
impl = """
static int __Pyx_ParseOptionalKeywords(
    PyObject *kwds,
    PyObject **argnames[],
    PyObject *kwds2,
    PyObject *values[],
    Py_ssize_t num_pos_args,
    const char* function_name)
{
    PyObject *key = 0, *value = 0;
    Py_ssize_t pos = 0;
    PyObject*** name;
    PyObject*** first_kw_arg = argnames + num_pos_args;

    while (PyDict_Next(kwds, &pos, &key, &value)) {
        #if PY_MAJOR_VERSION < 3
        if (unlikely(!PyString_CheckExact(key)) && unlikely(!PyString_Check(key))) {
        #else
        if (unlikely(!PyUnicode_CheckExact(key)) && unlikely(!PyUnicode_Check(key))) {
        #endif
            goto invalid_keyword_type;
        } else {
            name = argnames;
            while (*name && (**name != key)) name++;
            if (*name) {
                if (name < first_kw_arg) goto arg_passed_twice;
                values[name-argnames] = value;
            } else {
                for (name = first_kw_arg; *name; name++) {
                    #if PY_MAJOR_VERSION >= 3
                    if (PyUnicode_GET_SIZE(**name) == PyUnicode_GET_SIZE(key) &&
                        PyUnicode_Compare(**name, key) == 0) break;
                    #else
                    if (PyString_GET_SIZE(**name) == PyString_GET_SIZE(key) &&
                        strcmp(PyString_AS_STRING(**name),
                               PyString_AS_STRING(key)) == 0) break;
                    #endif
                }
                if (*name) {
                    values[name-argnames] = value;
                } else {
                    /* unexpected keyword found */
                    for (name=argnames; name != first_kw_arg; name++) {
                        if (**name == key) goto arg_passed_twice;
                        #if PY_MAJOR_VERSION >= 3
                        if (PyUnicode_GET_SIZE(**name) == PyUnicode_GET_SIZE(key) &&
                            PyUnicode_Compare(**name, key) == 0) goto arg_passed_twice;
                        #else
                        if (PyString_GET_SIZE(**name) == PyString_GET_SIZE(key) &&
                            strcmp(PyString_AS_STRING(**name),
                                   PyString_AS_STRING(key)) == 0) goto arg_passed_twice;
                        #endif
                    }
                    if (kwds2) {
                        if (unlikely(PyDict_SetItem(kwds2, key, value))) goto bad;
                    } else {
                        goto invalid_keyword;
                    }
                }
            }
        }
    }
    return 0;
arg_passed_twice:
    __Pyx_RaiseDoubleKeywordsError(function_name, **name);
    goto bad;
invalid_keyword_type:
    PyErr_Format(PyExc_TypeError,
        "%s() keywords must be strings", function_name);
    goto bad;
invalid_keyword:
    PyErr_Format(PyExc_TypeError,
    #if PY_MAJOR_VERSION < 3
        "%s() got an unexpected keyword argument '%s'",
        function_name, PyString_AsString(key));
    #else
        "%s() got an unexpected keyword argument '%U'",
        function_name, key);
    #endif
bad:
    return -1;
}
""")

#------------------------------------------------------------------------------------

unraisable_exception_utility_code = UtilityCode(
proto = """
static void __Pyx_WriteUnraisable(const char *name); /*proto*/
""",
impl = """
static void __Pyx_WriteUnraisable(const char *name) {
    PyObject *old_exc, *old_val, *old_tb;
    PyObject *ctx;
    __Pyx_ErrFetch(&old_exc, &old_val, &old_tb);
    #if PY_MAJOR_VERSION < 3
    ctx = PyString_FromString(name);
    #else
    ctx = PyUnicode_FromString(name);
    #endif
    __Pyx_ErrRestore(old_exc, old_val, old_tb);
    if (!ctx) {
        PyErr_WriteUnraisable(Py_None);
    } else {
        PyErr_WriteUnraisable(ctx);
        Py_DECREF(ctx);
    }
}
""")

#------------------------------------------------------------------------------------

traceback_utility_code = UtilityCode(
proto = """
static void __Pyx_AddTraceback(const char *funcname); /*proto*/
""",
impl = """
#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(const char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;

    #if PY_MAJOR_VERSION < 3
    py_srcfile = PyString_FromString(%(FILENAME)s);
    #else
    py_srcfile = PyUnicode_FromString(%(FILENAME)s);
    #endif
    if (!py_srcfile) goto bad;
    if (%(CLINENO)s) {
        #if PY_MAJOR_VERSION < 3
        py_funcname = PyString_FromFormat( "%%s (%%s:%%d)", funcname, %(CFILENAME)s, %(CLINENO)s);
        #else
        py_funcname = PyUnicode_FromFormat( "%%s (%%s:%%d)", funcname, %(CFILENAME)s, %(CLINENO)s);
        #endif
    }
    else {
        #if PY_MAJOR_VERSION < 3
        py_funcname = PyString_FromString(funcname);
        #else
        py_funcname = PyUnicode_FromString(funcname);
        #endif
    }
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(%(GLOBALS)s);
    if (!py_globals) goto bad;
    #if PY_MAJOR_VERSION < 3
    empty_string = PyString_FromStringAndSize("", 0);
    #else
    empty_string = PyBytes_FromStringAndSize("", 0);
    #endif
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        #if PY_MAJOR_VERSION >= 3
        0,            /*int kwonlyargcount,*/
        #endif
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        %(EMPTY_TUPLE)s,  /*PyObject *consts,*/
        %(EMPTY_TUPLE)s,  /*PyObject *names,*/
        %(EMPTY_TUPLE)s,  /*PyObject *varnames,*/
        %(EMPTY_TUPLE)s,  /*PyObject *freevars,*/
        %(EMPTY_TUPLE)s,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        %(LINENO)s,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_GET(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = %(LINENO)s;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}
""" % {
    'FILENAME': Naming.filename_cname,
    'LINENO':  Naming.lineno_cname,
    'CFILENAME': Naming.cfilenm_cname,
    'CLINENO':  Naming.clineno_cname,
    'GLOBALS': Naming.module_cname,
    'EMPTY_TUPLE' : Naming.empty_tuple,
})

restore_exception_utility_code = UtilityCode(
proto = """
static INLINE void __Pyx_ErrRestore(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
static INLINE void __Pyx_ErrFetch(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
""",
impl = """
static INLINE void __Pyx_ErrRestore(PyObject *type, PyObject *value, PyObject *tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_GET();

    tmp_type = tstate->curexc_type;
    tmp_value = tstate->curexc_value;
    tmp_tb = tstate->curexc_traceback;
    tstate->curexc_type = type;
    tstate->curexc_value = value;
    tstate->curexc_traceback = tb;
    Py_XDECREF(tmp_type);
    Py_XDECREF(tmp_value);
    Py_XDECREF(tmp_tb);
}

static INLINE void __Pyx_ErrFetch(PyObject **type, PyObject **value, PyObject **tb) {
    PyThreadState *tstate = PyThreadState_GET();
    *type = tstate->curexc_type;
    *value = tstate->curexc_value;
    *tb = tstate->curexc_traceback;

    tstate->curexc_type = 0;
    tstate->curexc_value = 0;
    tstate->curexc_traceback = 0;
}

""")

#------------------------------------------------------------------------------------

set_vtable_utility_code = UtilityCode(
proto = """
static int __Pyx_SetVtable(PyObject *dict, void *vtable); /*proto*/
""",
impl = """
static int __Pyx_SetVtable(PyObject *dict, void *vtable) {
    PyObject *pycobj = 0;
    int result;
    
    pycobj = PyCObject_FromVoidPtr(vtable, 0);
    if (!pycobj)
        goto bad;
    if (PyDict_SetItemString(dict, "__pyx_vtable__", pycobj) < 0)
        goto bad;
    result = 0;
    goto done;

bad:
    result = -1;
done:
    Py_XDECREF(pycobj);
    return result;
}
""")

#------------------------------------------------------------------------------------

get_vtable_utility_code = UtilityCode(
proto = """
static int __Pyx_GetVtable(PyObject *dict, void *vtabptr); /*proto*/
""",
impl = r"""
static int __Pyx_GetVtable(PyObject *dict, void *vtabptr) {
    int result;
    PyObject *pycobj;
    
    pycobj = PyMapping_GetItemString(dict, "__pyx_vtable__");
    if (!pycobj)
        goto bad;
    *(void **)vtabptr = PyCObject_AsVoidPtr(pycobj);
    if (!*(void **)vtabptr)
        goto bad;
    result = 0;
    goto done;

bad:
    result = -1;
done:
    Py_XDECREF(pycobj);
    return result;
}
""")

#------------------------------------------------------------------------------------

init_string_tab_utility_code = UtilityCode(
proto = """
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/
""",
impl = """
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        #if PY_MAJOR_VERSION < 3
        if (t->is_unicode && (!t->is_identifier)) {
            *t->p = PyUnicode_DecodeUTF8(t->s, t->n - 1, NULL);
        } else if (t->intern) {
            *t->p = PyString_InternFromString(t->s);
        } else {
            *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        }
        #else  /* Python 3+ has unicode identifiers */
        if (t->is_identifier || (t->is_unicode && t->intern)) {
            *t->p = PyUnicode_InternFromString(t->s);
        } else if (t->is_unicode) {
            *t->p = PyUnicode_FromStringAndSize(t->s, t->n - 1);
        } else {
            *t->p = PyBytes_FromStringAndSize(t->s, t->n - 1);
        }
        #endif
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}
""")

#------------------------------------------------------------------------------------

get_exception_utility_code = UtilityCode(
proto = """
static int __Pyx_GetException(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
""",
impl = """
static int __Pyx_GetException(PyObject **type, PyObject **value, PyObject **tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_GET();
    __Pyx_ErrFetch(type, value, tb);
    PyErr_NormalizeException(type, value, tb);
    if (PyErr_Occurred())
        goto bad;
    Py_INCREF(*type);
    Py_INCREF(*value);
    Py_INCREF(*tb);
    tmp_type = tstate->exc_type;
    tmp_value = tstate->exc_value;
    tmp_tb = tstate->exc_traceback;
    tstate->exc_type = *type;
    tstate->exc_value = *value;
    tstate->exc_traceback = *tb;
    /* Make sure tstate is in a consistent state when we XDECREF
    these objects (XDECREF may run arbitrary code). */
    Py_XDECREF(tmp_type);
    Py_XDECREF(tmp_value);
    Py_XDECREF(tmp_tb);
    return 0;
bad:
    Py_XDECREF(*type);
    Py_XDECREF(*value);
    Py_XDECREF(*tb);
    return -1;
}

""")

#------------------------------------------------------------------------------------

reset_exception_utility_code = UtilityCode(
proto = """
static INLINE void __Pyx_ExceptionSave(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
static void __Pyx_ExceptionReset(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
""",
impl = """
static INLINE void __Pyx_ExceptionSave(PyObject **type, PyObject **value, PyObject **tb) {
    PyThreadState *tstate = PyThreadState_GET();
    *type = tstate->exc_type;
    *value = tstate->exc_value;
    *tb = tstate->exc_traceback;
    Py_XINCREF(*type);
    Py_XINCREF(*value);
    Py_XINCREF(*tb);
}

static void __Pyx_ExceptionReset(PyObject *type, PyObject *value, PyObject *tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_GET();
    tmp_type = tstate->exc_type;
    tmp_value = tstate->exc_value;
    tmp_tb = tstate->exc_traceback;
    tstate->exc_type = type;
    tstate->exc_value = value;
    tstate->exc_traceback = tb;
    Py_XDECREF(tmp_type);
    Py_XDECREF(tmp_value);
    Py_XDECREF(tmp_tb);
}
""")

#------------------------------------------------------------------------------------
