#
#   Pyrex - Parse tree nodes
#

import string, sys, os, time

import Code
from Errors import error, warning, InternalError
import Naming
import PyrexTypes
import TypeSlots
from PyrexTypes import py_object_type, error_type, CTypedefType, CFuncType
from Symtab import ModuleScope, LocalScope, \
    StructOrUnionScope, PyClassScope, CClassScope
from Cython.Utils import open_new_file, replace_suffix
import Options

from DebugFlags import debug_disposal_code

absolute_path_length = len(os.path.abspath('.')) 

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
    return (pos[0][absolute_path_length+1:], pos[1])
        

class Node:
    #  pos         (string, int, int)   Source file position
    #  is_name     boolean              Is a NameNode
    #  is_literal  boolean              Is a ConstNode
    
    is_name = 0
    is_literal = 0
    
    def __init__(self, pos, **kw):
        self.pos = pos
        self.__dict__.update(kw)
    
    #
    #  There are 3 phases of parse tree processing, applied in order to
    #  all the statements in a given scope-block:
    #
    #  (1) analyse_declarations
    #        Make symbol table entries for all declarations at the current
    #        level, both explicit (def, cdef, etc.) and implicit (assignment
    #        to an otherwise undeclared name).
    #
    #		(2)	analyse_expressions
    #         Determine the result types of expressions and fill in the
    #         'type' attribute of each ExprNode. Insert coercion nodes into the
    #         tree where needed to convert to and from Python objects. 
    #         Allocate temporary locals for intermediate results. Fill
    #         in the 'result_code' attribute of each ExprNode with a C code
    #         fragment.
    #
    #   (3) generate_code
    #         Emit C code for all declarations, statements and expressions.
    #         Recursively applies the 3 processing phases to the bodies of
    #         functions.
    #
    
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


class BlockNode:
    #  Mixin class for nodes representing a declaration block.

    def generate_const_definitions(self, env, code):
        if env.const_entries:
            code.putln("")
            for entry in env.const_entries:
                if not entry.is_interned:
                    code.put_var_declaration(entry, static = 1)
    
    def generate_interned_name_decls(self, env, code):
        #  Flush accumulated interned names from the global scope
        #  and generate declarations for them.
        genv = env.global_scope()
        intern_map = genv.intern_map
        names = genv.interned_names
        if names:
            code.putln("")
            for name in names:
                code.putln(
                    "static PyObject *%s;" % intern_map[name])
            del names[:]
    
    def generate_py_string_decls(self, env, code):
        entries = env.pystring_entries
        if entries:
            code.putln("")
            for entry in entries:
                code.putln(
                    "static PyObject *%s;" % entry.pystring_cname)
    
    def generate_interned_num_decls(self, env, code):
        #  Flush accumulated interned nums from the global scope
        #  and generate declarations for them.
        genv = env.global_scope()
        entries = genv.interned_nums
        if entries:
            code.putln("")
            for entry in entries:
                code.putln(
                    "static PyObject *%s;" % entry.cname)
            del entries[:]

    def generate_cached_builtins_decls(self, env, code):
        entries = env.global_scope().undeclared_cached_builtins
        if len(entries) > 0:
            code.putln("")
        for entry in entries:
            code.putln("static PyObject *%s;" % entry.cname)
        del entries[:]
        

class StatListNode(Node):
    # stats     a list of StatNode
    
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

    calling_convention = ""

    def analyse_expressions(self, env):
        pass

    def generate_execution_code(self, env):
        pass


class CNameDeclaratorNode(CDeclaratorNode):
    #  name   string           The Pyrex name being declared
    #  cname  string or None   C name, if specified
    
    def analyse(self, base_type, env):
        self.type = base_type
        return self, base_type
        
    def analyse_expressions(self, env):
        self.entry = env.lookup(self.name)
        if self.rhs is not None:
            self.entry.used = 1
            if self.type.is_pyobject:
                self.entry.init_to_none = False
                self.entry.init = 0
            self.rhs.analyse_types(env)
            self.rhs = self.rhs.coerce_to(self.type, env)
            self.rhs.allocate_temps(env)
            self.rhs.release_temp(env)

    def generate_execution_code(self, code):
        if self.rhs is not None:
            self.rhs.generate_evaluation_code(code)
            if self.type.is_pyobject:
                self.rhs.make_owned_reference(code)
            code.putln('%s = %s;' % (self.entry.cname, self.rhs.result_as(self.entry.type)))
            self.rhs.generate_post_assignment_code(code)
            code.putln()

class CPtrDeclaratorNode(CDeclaratorNode):
    # base     CDeclaratorNode
    
    def analyse(self, base_type, env):
        if base_type.is_pyobject:
            error(self.pos,
                "Pointer base type cannot be a Python object")
        ptr_type = PyrexTypes.c_ptr_type(base_type)
        return self.base.analyse(ptr_type, env)
        
    def analyse_expressions(self, env):
        self.base.analyse_expressions(env)

    def generate_execution_code(self, env):
        self.base.generate_execution_code(env)

class CArrayDeclaratorNode(CDeclaratorNode):
    # base        CDeclaratorNode
    # dimension   ExprNode
    
    def analyse(self, base_type, env):
        if self.dimension:
            self.dimension.analyse_const_expression(env)
            if not self.dimension.type.is_int:
                error(self.dimension.pos, "Array dimension not integer")
            size = self.dimension.result_code
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
        return self.base.analyse(array_type, env)


class CFuncDeclaratorNode(CDeclaratorNode):
    # base             CDeclaratorNode
    # args             [CArgDeclNode]
    # has_varargs      boolean
    # exception_value  ConstNode
    # exception_check  boolean    True if PyErr_Occurred check needed
    # nogil            boolean    Can be called without gil
    # with_gil         boolean    Acquire gil around function body
    
    overridable = 0

    def analyse(self, return_type, env):
        func_type_args = []
        for arg_node in self.args:
            name_declarator, type = arg_node.analyse(env)
            name = name_declarator.name
            if name_declarator.cname:
                error(self.pos, 
                    "Function argument cannot have C name specification")
            # Turn *[] argument into **
            if type.is_array:
                type = PyrexTypes.c_ptr_type(type.base_type)
            # Catch attempted C-style func(void) decl
            if type.is_void:
                error(arg_node.pos, "Function argument cannot be void")
            if type.is_pyobject and self.nogil:
                error(self.pos,
                    "Function with Python argument cannot be declared nogil")
            func_type_args.append(
                PyrexTypes.CFuncTypeArg(name, type, arg_node.pos))
            if arg_node.default:
                error(arg_node.pos, "C function argument cannot have default value")
        exc_val = None
        exc_check = 0
        if return_type.is_pyobject \
            and (self.exception_value or self.exception_check):
                error(self.pos,
                    "Exception clause not allowed for function returning Python object")
        else:
            if self.exception_value:
                self.exception_value.analyse_const_expression(env)
                exc_val = self.exception_value.result_code
                if not return_type.assignable_from(self.exception_value.type):
                    error(self.exception_value.pos,
                        "Exception value incompatible with function return type")
            exc_check = self.exception_check
        if return_type.is_pyobject and self.nogil:
            error(self.pos,
                "Function with Python return type cannot be declared nogil")
        if return_type.is_array:
            error(self.pos,
                "Function cannot return an array")
        if return_type.is_cfunction:
            error(self.pos,
                "Function cannot return a function")
        func_type = PyrexTypes.CFuncType(
            return_type, func_type_args, self.has_varargs, 
            exception_value = exc_val, exception_check = exc_check,
            calling_convention = self.base.calling_convention,
            nogil = self.nogil, with_gil = self.with_gil, is_overridable = self.overridable)
        return self.base.analyse(func_type, env)


class CArgDeclNode(Node):
    # Item in a function declaration argument list.
    #
    # base_type      CBaseTypeNode
    # declarator     CDeclaratorNode
    # not_none       boolean            Tagged with 'not None'
    # default        ExprNode or None
    # default_entry  Symtab.Entry       Entry for the variable holding the default value
    # is_self_arg    boolean            Is the "self" arg of an extension type method
    # is_kw_only     boolean            Is a keyword-only argument

    is_self_arg = 0
    
    def analyse(self, env):
        #print "CArgDeclNode.analyse: is_self_arg =", self.is_self_arg ###
        base_type = self.base_type.analyse(env)
        return self.declarator.analyse(base_type, env)

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


class CSimpleBaseTypeNode(CBaseTypeNode):
    # name             string
    # module_path      [string]     Qualifying name components
    # is_basic_c_type  boolean
    # signed           boolean
    # longness         integer
    # is_self_arg      boolean      Is self argument of C method

    def analyse(self, env):
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
            scope = env
            for name in self.module_path:
                entry = scope.find(name, self.pos)
                if entry and entry.as_module:
                    scope = entry.as_module
                else:
                    if entry:
                        error(self.pos, "'%s' is not a cimported module" % name)
                    scope = None
                    break
            if scope:
                entry = scope.find(self.name, self.pos)
                if entry and entry.is_type:
                    type = entry.type
                else:
                    error(self.pos, "'%s' is not a type identifier" % self.name)
        if type:
            return type
        else:
            return PyrexTypes.error_type


class CComplexBaseTypeNode(CBaseTypeNode):
    # base_type   CBaseTypeNode
    # declarator  CDeclaratorNode
    
    def analyse(self, env):
        base = self.base_type.analyse(env)
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
    
    def analyse_declarations(self, env, dest_scope = None):
        if not dest_scope:
            dest_scope = env
        base_type = self.base_type.analyse(env)
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
                dest_scope.declare_var(name, type, declarator.pos,
                    cname = cname, visibility = self.visibility, is_cdef = 1)
    
    def analyse_expressions(self, env):
        for declarator in self.declarators:
            declarator.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        for declarator in self.declarators:
            declarator.generate_execution_code(code)


class CStructOrUnionDefNode(StatNode):
    #  name          string
    #  cname         string or None
    #  kind          "struct" or "union"
    #  typedef_flag  boolean
    #  visibility    "public" or "private"
    #  in_pxd        boolean
    #  attributes    [CVarDefNode] or None
    #  entry         Entry
    
    def analyse_declarations(self, env):
        scope = None
        if self.attributes is not None:
            scope = StructOrUnionScope()
        self.entry = env.declare_struct_or_union(
            self.name, self.kind, scope, self.typedef_flag, self.pos,
            self.cname, visibility = self.visibility)
        if self.attributes is not None:
            if self.in_pxd and not env.in_cinclude:
                self.entry.defined_in_pxd = 1
            for attr in self.attributes:
                attr.analyse_declarations(env, scope)
    
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
        pass
    
    def generate_execution_code(self, code):
        pass


class CEnumDefItemNode(StatNode):
    #  name     string
    #  cname    string or None
    #  value    ExprNode or None
    
    def analyse_declarations(self, env, enum_entry):
        if self.value:
            self.value.analyse_const_expression(env)
            value = self.value.result_code
        else:
            value = self.name
        entry = env.declare_const(self.name, enum_entry.type, 
            value, self.pos, cname = self.cname)
        enum_entry.enum_values.append(entry)


class CTypeDefNode(StatNode):
    #  base_type    CBaseTypeNode
    #  declarator   CDeclaratorNode
    #  visibility   "public" or "private"
    #  in_pxd       boolean
    
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
    
    py_func = None
    
    def analyse_expressions(self, env):
        pass

    def need_gil_acquisition(self, lenv):
        return 0
                
    def generate_function_definitions(self, env, code):
        code.mark_pos(self.pos)
        # Generate C code for header and body of function
        genv = env.global_scope()
        lenv = LocalScope(name = self.entry.name, outer_scope = genv)
        lenv.return_type = self.return_type
        code.init_labels()
        self.declare_arguments(lenv)
        self.body.analyse_declarations(lenv)
        self.body.analyse_expressions(lenv)
        # Code for nested function definitions would go here
        # if we supported them, which we probably won't.
        # ----- Top-level constants used by this function
        self.generate_interned_num_decls(lenv, code)
        self.generate_interned_name_decls(lenv, code)
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
        self.generate_argument_declarations(lenv, code)
        code.put_var_declarations(lenv.var_entries)
        init = ""
        if not self.return_type.is_void:
            code.putln(
                "%s%s;" % 
                    (self.return_type.declaration_code(
                        Naming.retval_cname),
                    init))
        code.put_var_declarations(lenv.temp_entries)
        self.generate_keyword_list(code)
        # ----- Extern library function declarations
        lenv.generate_library_function_declarations(code)
        # ----- GIL acquisition
        acquire_gil = self.need_gil_acquisition(lenv)
        if acquire_gil:
            code.putln("PyGILState_STATE _save = PyGILState_Ensure();")
        # ----- Fetch arguments
        self.generate_argument_parsing_code(code)
        self.generate_argument_increfs(lenv, code)
        # ----- Initialise local variables
        for entry in lenv.var_entries:
            if entry.type.is_pyobject and entry.init_to_none and entry.used:
                code.put_init_var_to_py_none(entry)
        # ----- Check and convert arguments
        self.generate_argument_type_tests(code)
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
        #code.putln("goto %s;" % code.return_label)
        # ----- Error cleanup
        if code.error_label in code.labels_used:
            code.put_goto(code.return_label)
            code.put_label(code.error_label)
            code.put_var_xdecrefs(lenv.temp_entries)
            err_val = self.error_value()
            exc_check = self.caller_will_check_exceptions()
            if err_val is not None or exc_check:
                code.putln(
                    '__Pyx_AddTraceback("%s");' % 
                        self.entry.qualified_name)
                if err_val is not None:
                    code.putln(
                        "%s = %s;" % (
                            Naming.retval_cname, 
                            err_val))
            else:
                code.putln(
                    '__Pyx_WriteUnraisable("%s");' % 
                        self.entry.qualified_name)
                env.use_utility_code(unraisable_exception_utility_code)
                #if not self.return_type.is_void:
                default_retval = self.return_type.default_value
                if default_retval:
                    code.putln(
                        "%s = %s;" % (
                            Naming.retval_cname,
                            default_retval))
                            #self.return_type.default_value))
        # ----- Return cleanup
        code.put_label(code.return_label)
        code.put_var_decrefs(lenv.var_entries, used_only = 1)
        code.put_var_decrefs(lenv.arg_entries)
        self.put_stararg_decrefs(code)
        if acquire_gil:
            code.putln("PyGILState_Release(_save);")
        # ----- Return
        if not self.return_type.is_void:
            code.putln("return %s;" % Naming.retval_cname)
        code.putln("}")
        # ----- Python version
        if self.py_func:
            self.py_func.generate_function_definitions(env, code)

    def put_stararg_decrefs(self, code):
        pass

    def declare_argument(self, env, arg):
        if arg.type.is_void:
            error(arg.pos, "Invalid use of 'void'")
        elif not arg.type.is_complete() and not arg.type.is_array:
            error(arg.pos,
                "Argument type '%s' is incomplete" % arg.type)
        return env.declare_arg(arg.name, arg.type, arg.pos)
    
    def generate_argument_increfs(self, env, code):
        # Turn borrowed argument refs into owned refs.
        # This is necessary, because if the argument is
        # assigned to, it will be decrefed.
        for entry in env.arg_entries:
            code.put_var_incref(entry)

    def generate_execution_code(self, code):
        pass


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
    
    def unqualified_name(self):
        return self.entry.name
        
    def analyse_declarations(self, env):
        base_type = self.base_type.analyse(env)
        name_declarator, type = self.declarator.analyse(base_type, env)
        if not type.is_cfunction:
            error(self.pos, 
                "Suite attached to non-function declaration")
        # Remember the actual type according to the function header
        # written here, because the type in the symbol table entry
        # may be different if we're overriding a C method inherited
        # from the base type of an extension type.
        self.type = type
        type.is_overridable = self.overridable
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
            arg_names = [arg.name for arg in self.type.args]
            self_arg = ExprNodes.NameNode(self.pos, name=arg_names[0])
            cfunc = ExprNodes.AttributeNode(self.pos, obj=self_arg, attribute=self.declarator.base.name)
            c_call = ExprNodes.SimpleCallNode(self.pos, function=cfunc, args=[ExprNodes.NameNode(self.pos, name=n) for n in arg_names[1:]], wrapper_call=True)
            py_func_body = ReturnStatNode(pos=self.pos, return_type=PyrexTypes.py_object_type, value=c_call)
            self.py_func = DefNode(pos = self.pos, 
                                   name = self.declarator.base.name,
                                   args = self.declarator.args,
                                   star_arg = None,
                                   starstar_arg = None,
                                   doc = self.doc,
                                   body = py_func_body)
            self.py_func.analyse_declarations(env)
            # Reset scope entry the above cfunction
            env.entries[name] = self.entry
            if Options.intern_names:
                self.py_func.interned_attr_cname = env.intern(self.py_func.entry.name)
            self.override = OverrideCheckNode(self.pos, py_func = self.py_func)
            self.body = StatListNode(self.pos, stats=[self.override, self.body])
            
                    
    def declare_arguments(self, env):
        for arg in self.type.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            self.declare_argument(env, arg)
            
    def need_gil_acquisition(self, lenv):
        with_gil = self.type.with_gil
        if self.type.nogil and not with_gil:
            for entry in lenv.var_entries + lenv.temp_entries:
                if entry.type.is_pyobject:
                    error(self.pos, "Function declared nogil has Python locals or temporaries")
        return with_gil

    def generate_function_header(self, code, with_pymethdef):
        arg_decls = []
        type = self.type
        visibility = self.entry.visibility
        for arg in type.args:
            arg_decls.append(arg.declaration_code())
        if type.has_varargs:
            arg_decls.append("...")
        if not arg_decls:
            arg_decls = ["void"]
        entity = type.function_header_code(self.entry.func_cname,
            string.join(arg_decls, ","))
        if visibility == 'public':
            dll_linkage = "DL_EXPORT"
        else:
            dll_linkage = None
        header = self.return_type.declaration_code(entity,
            dll_linkage = dll_linkage)
        if visibility <> 'private':
            storage_class = "%s " % Naming.extern_c_macro
        else:
            storage_class = "static "
        code.putln("%s%s %s {" % (
            storage_class,
            ' '.join(self.modifiers).upper(), # macro forms 
            header))

    def generate_argument_declarations(self, env, code):
        # Arguments already declared in function header
        pass
    
    def generate_keyword_list(self, code):
        pass
        
    def generate_argument_parsing_code(self, code):
        pass
    
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
                'if (unlikely(!__Pyx_ArgTypeTest(%s, %s, %d, "%s"))) %s' % (
                    arg_code, 
                    typeptr_cname,
                    not arg.not_none,
                    arg.name,
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
                    

class PyArgDeclNode(Node):
    # Argument which must be a Python object (used
    # for * and ** arguments).
    #
    # name   string
    # entry  Symtab.Entry
    
    pass
    

class DefNode(FuncDefNode):
    # A Python function definition.
    #
    # name          string                 the Python name of the function
    # args          [CArgDeclNode]         formal arguments
    # star_arg      PyArgDeclNode or None  * argument
    # starstar_arg  PyArgDeclNode or None  ** argument
    # doc           string or None
    # body          StatListNode
    #
    #  The following subnode is constructed internally
    #  when the def statement is inside a Python class definition.
    #
    #  assmt   AssignmentNode   Function construction/assignment
    
    assmt = None
    num_kwonly_args = 0
    num_required_kw_args = 0
    reqd_kw_flags_cname = "0"
    
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
    
    def analyse_declarations(self, env):
        for arg in self.args:
            base_type = arg.base_type.analyse(env)
            name_declarator, type = \
                arg.declarator.analyse(base_type, env)
            arg.name = name_declarator.name
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
        if self.star_arg:
            env.use_utility_code(get_stararg_utility_code)
        if self.starstar_arg:
            env.use_utility_code(get_splitkeywords_utility_code)
        if self.num_required_kw_args:
            env.use_utility_code(get_checkkeywords_utility_code)

    def analyse_signature(self, env):
        any_type_tests_needed = 0
        # Use the simpler calling signature for zero- and one-argument functions.
        if not self.entry.is_special and not self.star_arg and not self.starstar_arg:
            if self.entry.signature is TypeSlots.pyfunction_signature:
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
                if arg.is_generic and arg.type.is_extension_type:
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
    
    def declare_pyfunction(self, env):
        #print "DefNode.declare_pyfunction:", self.name, "in", env ###
        name = self.name
        entry = env.declare_pyfunction(self.name, self.pos)
        self.entry = entry
        prefix = env.scope_prefix
        entry.func_cname = \
            Naming.pyfunc_prefix + prefix + name
        entry.pymethdef_cname = \
            Naming.pymethdef_prefix + prefix + name
        if not Options.docstrings:
            self.entry.doc = None
        else:
            if Options.embed_pos_in_docstring:
                entry.doc = 'File: %s (starting at line %s)'%relative_position(self.pos)
                if not self.doc is None:
                    entry.doc = entry.doc + '\\n' + self.doc
            else:
                entry.doc = self.doc
            entry.doc_cname = \
                Naming.funcdoc_prefix + prefix + name

    def declare_arguments(self, env):
        for arg in self.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            if arg.needs_conversion:
                arg.entry = env.declare_var(arg.name, arg.type, arg.pos)
                if arg.type.is_pyobject:
                    arg.entry.init = "0"
                arg.entry.init_to_none = 0
            else:
                arg.entry = self.declare_argument(env, arg)
            arg.entry.used = 1
            arg.entry.is_self_arg = arg.is_self_arg
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
            
    def analyse_expressions(self, env):
        self.analyse_default_values(env)
        if env.is_py_class_scope:
            self.synthesize_assignment_node(env)
    
    def analyse_default_values(self, env):
        genv = env.global_scope()
        for arg in self.args:
            if arg.default:
                if arg.is_generic:
                    arg.default.analyse_types(genv)
                    arg.default = arg.default.coerce_to(arg.type, genv)
                    arg.default.allocate_temps(genv)
                    arg.default_entry = genv.add_default_value(arg.type)
                    arg.default_entry.used = 1
                else:
                    error(arg.pos,
                        "This argument cannot have a default value")
                    arg.default = None
    
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
            code.putln(
                'static char %s[] = "%s";' % (
                    self.entry.doc_cname,
                    self.entry.doc))
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
        if self.entry.signature.has_generic_args:
            reqd_kw_flags = []
            has_reqd_kwds = False
            code.put(
                "static char *%s[] = {" %
                    Naming.kwdlist_cname)
            for arg in self.args:
                if arg.is_generic:
                    code.put(
                        '"%s",' % 
                            arg.name)
                    if arg.kw_only and not arg.default:
                        has_reqd_kwds = 1
                        flag = "1"
                    else:
                        flag = "0"
                    reqd_kw_flags.append(flag)
            code.putln(
                "0};")
            if has_reqd_kwds:
                flags_name = Naming.reqd_kwds_cname
                self.reqd_kw_flags_cname = flags_name
                code.putln(
                    "static char %s[] = {%s};" % (
                        flags_name,
                        ",".join(reqd_kw_flags)))

    def generate_argument_parsing_code(self, code):
        # Generate PyArg_ParseTuple call for generic
        # arguments, if any.
        has_kwonly_args = self.num_kwonly_args > 0
        has_star_or_kw_args = self.star_arg is not None \
            or self.starstar_arg is not None or has_kwonly_args
        if not self.entry.signature.has_generic_args:
            if has_star_or_kw_args:
                error(self.pos, "This method cannot have * or keyword arguments")
            self.generate_argument_conversion_code(code)
        else:
            arg_addrs = []
            arg_formats = []
            positional_args = []
            default_seen = 0
            for arg in self.args:
                arg_entry = arg.entry
                if arg.is_generic:
                    if arg.default:
                        code.putln(
                            "%s = %s;" % (
                                arg_entry.cname,
                                arg.default_entry.cname))
                        if not default_seen:
                            arg_formats.append("|")
                        default_seen = 1
                        if not arg.is_self_arg and not arg.kw_only:
                            positional_args.append(arg)
                    elif arg.kw_only:
                        if not default_seen:
                            arg_formats.append("|")
                        default_seen = 1
                    elif default_seen:
                        error(arg.pos, "Non-default argument following default argument")
                    elif not arg.is_self_arg:
                        positional_args.append(arg)
                    if arg.needs_conversion:
                        arg_addrs.append("&" + arg.hdr_cname)
                        format = arg.hdr_type.parsetuple_format
                    else:
                        arg_addrs.append("&" + arg_entry.cname)
                        format = arg_entry.type.parsetuple_format
                    if format:
                        arg_formats.append(format)
                    else:
                        error(arg.pos, 
                            "Cannot convert Python object argument to type '%s' (when parsing input arguments)" 
                                % arg.type)

            if has_star_or_kw_args:
                self.generate_stararg_getting_code(code)
            old_error_label = code.new_error_label()
            our_error_label = code.error_label
            end_label = code.new_label()

            self.generate_argument_tuple_parsing_code(
                positional_args, arg_formats, arg_addrs, code)

            code.error_label = old_error_label
            code.put_goto(end_label)
            code.put_label(our_error_label)
            if has_star_or_kw_args:
                self.put_stararg_decrefs(code)
                self.generate_arg_decref(self.star_arg, code)
                if self.starstar_arg:
                    if self.starstar_arg.entry.xdecref_cleanup:
                        code.put_var_xdecref(self.starstar_arg.entry)
                    else:
                        code.put_var_decref(self.starstar_arg.entry)
            code.putln("return %s;" % self.error_value())
            code.put_label(end_label)

    def generate_argument_tuple_parsing_code(self, positional_args,
                                             arg_formats, arg_addrs, code):
        # Unpack inplace if it's simple
        if not self.num_required_kw_args:
            min_positional_args = self.num_required_args - self.num_required_kw_args
            max_positional_args = len(positional_args)
            if len(self.args) > 0 and self.args[0].is_self_arg:
                min_positional_args -= 1
            if max_positional_args == min_positional_args:
                count_cond = "likely(PyTuple_GET_SIZE(%s) == %s)" % (
                    Naming.args_cname, max_positional_args)
            else:
                count_cond = "likely(%s <= PyTuple_GET_SIZE(%s)) && likely(PyTuple_GET_SIZE(%s) <= %s)" % (
                               min_positional_args,
                               Naming.args_cname,
                               Naming.args_cname,
                               max_positional_args)
            code.putln(
                'if (likely(!%s) && %s) {' % (Naming.kwds_cname, count_cond))
            i = 0
            closing = 0
            for arg in positional_args:
                if arg.default:
                    code.putln('if (PyTuple_GET_SIZE(%s) > %s) {' % (Naming.args_cname, i))
                    closing += 1
                item = "PyTuple_GET_ITEM(%s, %s)" % (Naming.args_cname, i)
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
                i += 1
            for _ in range(closing):
                code.putln('}')
            code.putln(
                '}')
            code.putln('else {')

        argformat = '"%s"' % string.join(arg_formats, "")
        pt_arglist = [Naming.args_cname, Naming.kwds_cname, argformat,
                      Naming.kwdlist_cname] + arg_addrs
        pt_argstring = string.join(pt_arglist, ", ")
        code.putln(
            'if (unlikely(!PyArg_ParseTupleAndKeywords(%s))) %s' % (
                pt_argstring,
                code.error_goto(self.pos)))
        self.generate_argument_conversion_code(code)

        if not self.num_required_kw_args:
            code.putln('}')

    def put_stararg_decrefs(self, code):
        if self.star_arg:
            code.put_decref(Naming.args_cname, py_object_type)
        if self.starstar_arg:
            code.put_xdecref(Naming.kwds_cname, py_object_type)
    
    def generate_arg_xdecref(self, arg, code):
        if arg:
            code.put_var_xdecref(arg.entry)
    
    def generate_arg_decref(self, arg, code):
        if arg:
            code.put_var_decref(arg.entry)
    
    def arg_address(self, arg):
        if arg:
            return "&%s" % arg.entry.cname
        else:
            return 0

    def generate_stararg_getting_code(self, code):
        num_kwonly = self.num_kwonly_args
        fixed_args = self.entry.signature.num_fixed_args()
        nargs = len(self.args) - num_kwonly - fixed_args
        error_return = "return %s;" % self.error_value()

        if self.star_arg:
            star_arg_cname = self.star_arg.entry.cname
            code.putln("if (likely(PyTuple_GET_SIZE(%s) <= %d)) {" % (
                    Naming.args_cname, nargs))
            code.put_incref(Naming.args_cname, py_object_type)
            code.put("%s = %s; " % (star_arg_cname, Naming.empty_tuple))
            code.put_incref(Naming.empty_tuple, py_object_type)
            code.putln("}")
            code.putln("else {")
            code.putln(
                "if (unlikely(__Pyx_SplitStarArg(&%s, %d, &%s) < 0)) return %s;" % (
                    Naming.args_cname,
                    nargs,
                    star_arg_cname,
                    self.error_value()))
            code.putln("}")
            self.star_arg.entry.xdecref_cleanup = 0
        elif self.entry.signature.has_generic_args:
            # make sure supernumerous positional arguments do not run
            # into keyword-only arguments and provide a more helpful
            # message than PyArg_ParseTupelAndKeywords()
            code.putln("if (unlikely(PyTuple_GET_SIZE(%s) > %d)) {" % (
                    Naming.args_cname, nargs))
            error_message = "function takes at most %d positional arguments (%d given)"
            code.putln("PyErr_Format(PyExc_TypeError, \"%s\", %d, PyTuple_GET_SIZE(%s));" % (
                    error_message, nargs, Naming.args_cname))
            code.putln(error_return)
            code.putln("}")

        handle_error = 0
        if self.starstar_arg:
            handle_error = 1
            code.put(
                "if (unlikely(__Pyx_SplitKeywords(&%s, %s, &%s, %s) < 0)) " % (
                    Naming.kwds_cname,
                    Naming.kwdlist_cname,
                    self.starstar_arg.entry.cname,
                    self.reqd_kw_flags_cname))
            self.starstar_arg.entry.xdecref_cleanup = 0
        elif self.num_required_kw_args:
            handle_error = 1
            code.put("if (unlikely(__Pyx_CheckRequiredKeywords(%s, %s, %s) < 0)) " % (
                    Naming.kwds_cname,
                    Naming.kwdlist_cname,
                    self.reqd_kw_flags_cname))

        if handle_error:
            if self.star_arg:
                code.putln("{")
                code.put_decref(Naming.args_cname, py_object_type)
                code.put_decref(self.star_arg.entry.cname, py_object_type)
                code.putln(error_return)
                code.putln("}")
            else:
                code.putln(error_return)

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
                'if (unlikely(!__Pyx_ArgTypeTest(%s, %s, %d, "%s"))) %s' % (
                    arg_code, 
                    typeptr_cname,
                    not arg.not_none,
                    arg.name,
                    code.error_goto(arg.pos)))
        else:
            error(arg.pos, "Cannot test type of extern C class "
                "without type object name specification")
    
    def generate_execution_code(self, code):
        # Evaluate and store argument default values
        for arg in self.args:
            default = arg.default
            if default:
                default.generate_evaluation_code(code)
                default.make_owned_reference(code)
                code.putln(
                    "%s = %s;" % (
                        arg.default_entry.cname,
                        default.result_as(arg.default_entry.type)))
                if default.is_temp and default.type.is_pyobject:
                    code.putln(
                        "%s = 0;" %
                            default.result_code)
        # For Python class methods, create and store function object
        if self.assmt:
            self.assmt.generate_execution_code(code)
    
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
    
    def analyse_expressions(self, env):
        self.args = env.arg_entries
        import ExprNodes
        self.func_node = ExprNodes.PyTempNode(self.pos, env)
        call_tuple = ExprNodes.TupleNode(self.pos, args=[ExprNodes.NameNode(self.pos, name=arg.name) for arg in self.args[1:]])
        call_node = ExprNodes.SimpleCallNode(self.pos,
                                             function=self.func_node, 
                                             args=[ExprNodes.NameNode(self.pos, name=arg.name) for arg in self.args[1:]])
        self.body = ReturnStatNode(self.pos, value=call_node)
#        self.func_temp = env.allocate_temp_pyobject()
        self.body.analyse_expressions(env)
#        env.release_temp(self.func_temp)
        
    def generate_execution_code(self, code):
        # Check to see if we are an extension type
        self_arg = "((PyObject *)%s)" % self.args[0].cname
        code.putln("/* Check if called by wrapper */")
        code.putln("if (unlikely(%s)) %s = 0;" % (Naming.skip_dispatch_cname, Naming.skip_dispatch_cname))
        code.putln("/* Check if overriden in Python */")
        code.putln("else if (unlikely(%s->ob_type->tp_dictoffset != 0)) {" % self_arg)
        err = code.error_goto_if_null(self_arg, self.pos)
        # need to get attribute manually--scope would return cdef method
        if Options.intern_names:
            code.putln("%s = PyObject_GetAttr(%s, %s); %s" % (self.func_node.result_code, self_arg, self.py_func.interned_attr_cname, err))
        else:
            code.putln('%s = PyObject_GetAttrString(%s, "%s"); %s' % (self.func_node.result_code, self_arg, self.py_func.entry.name, err))
        # It appears that this type is not anywhere exposed in the Python/C API
        is_builtin_function_or_method = '(strcmp(%s->ob_type->tp_name, "builtin_function_or_method") == 0)' % self.func_node.result_code
        is_overridden = '(PyCFunction_GET_FUNCTION(%s) != &%s)' % (self.func_node.result_code, self.py_func.entry.func_cname)
        code.putln('if (!%s || %s) {' % (is_builtin_function_or_method, is_overridden))
        self.body.generate_execution_code(code)
        code.putln('}')
#        code.put_decref(self.func_temp, PyrexTypes.py_object_type)
        code.putln("}")



class PyClassDefNode(StatNode, BlockNode):
    #  A Python class definition.
    #
    #  name     string          Name of the class
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
    
    def __init__(self, pos, name, bases, doc, body):
        StatNode.__init__(self, pos)
        self.name = name
        self.doc = doc
        self.body = body
        import ExprNodes
        self.dict = ExprNodes.DictNode(pos, key_value_pairs = [])
        if self.doc and Options.docstrings:
            if Options.embed_pos_in_docstring:
                doc = 'File: %s (starting at line %s)'%relative_position(self.pos)
            doc = doc + '\\n' + self.doc
            doc_node = ExprNodes.StringNode(pos, value = doc)
        else:
            doc_node = None
        self.classobj = ExprNodes.ClassNode(pos,
            name = ExprNodes.StringNode(pos, value = name), 
            bases = bases, dict = self.dict, doc = doc_node)
        self.target = ExprNodes.NameNode(pos, name = name)
    
    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        self.dict.analyse_expressions(env)
        self.classobj.analyse_expressions(env)
        genv = env.global_scope()
        cenv = PyClassScope(name = self.name, outer_scope = genv)
        cenv.class_dict_cname = self.dict.result_code
        cenv.class_obj_cname = self.classobj.result_code
        self.scope = cenv
        self.body.analyse_declarations(cenv)
        self.body.analyse_expressions(cenv)
        self.target.analyse_target_expression(env, self.classobj)
        self.dict.release_temp(env)
        #self.classobj.release_temp(env)
        #self.target.release_target_temp(env)
    
    def generate_function_definitions(self, env, code):
        self.generate_py_string_decls(self.scope, code)
        self.body.generate_function_definitions(
            self.scope, code)
    
    def generate_execution_code(self, code):
        self.dict.generate_evaluation_code(code)
        self.classobj.generate_evaluation_code(code)
        self.body.generate_execution_code(code)
        self.target.generate_assignment_code(self.classobj, code)
        self.dict.generate_disposal_code(code)


class CClassDefNode(StatNode):
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
    
    def analyse_declarations(self, env):
        #print "CClassDefNode.analyse_declarations:", self.class_name
        #print "...visibility =", self.visibility
        #print "...module_name =", self.module_name
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
        self.entry = env.declare_c_class(
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
            api = self.api)
        scope = self.entry.type.scope
        
        if self.doc and Options.docstrings:
            if Options.embed_pos_in_docstring:
                scope.doc = 'File: %s (starting at line %s)'%relative_position(self.pos)
                scope.doc = scope.doc + '\\n' + self.doc
            else:
                scope.doc = self.doc

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
    #  doc    string or None    Doc string
    #  body   StatListNode
    
    def analyse_declarations(self, env):
        entry = env.declare_property(self.name, self.doc, self.pos)
        if entry:
            if self.doc and Options.docstrings:
                doc_entry = env.get_string_const(self.doc)
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
    
    def analyse_expressions(self, env):
        self.expr.analyse_expressions(env)
        self.expr.release_temp(env)
    
    def generate_execution_code(self, code):
        self.expr.generate_evaluation_code(code)
        if not self.expr.is_temp and self.expr.result_code:
            code.putln("%s;" % self.expr.result_code)
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

    def analyse_declarations(self, env):
        self.lhs.analyse_target_declaration(env)
    
    def analyse_types(self, env, use_temp = 0):
        self.rhs.analyse_types(env)
        self.lhs.analyse_target_types(env)
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
             self.result = ExprNodes.PyTempNode(self.pos, env).coerce_to(self.lhs.type, env)
             self.result.allocate_temps(env)
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
            self.result.release_temp(env)

    def generate_execution_code(self, code):
        self.rhs.generate_evaluation_code(code)
        self.dup.generate_subexpr_evaluation_code(code)
        self.dup.generate_result_code(code)
        if self.lhs.type.is_pyobject:
            code.putln(
                "%s = %s(%s, %s); %s" % (
                    self.result.result_code, 
                    self.py_operation_function(), 
                    self.dup.py_result(),
                    self.rhs.py_result(),
                    code.error_goto_if_null(self.result.py_result(), self.pos)))
            self.result.generate_evaluation_code(code) # May be a type check...
            self.rhs.generate_disposal_code(code)
            self.dup.generate_disposal_code(code)
            self.lhs.generate_assignment_code(self.result, code)
        else: 
            # have to do assignment directly to avoid side-effects
            code.putln("%s %s= %s;" % (self.lhs.result_code, self.operator, self.rhs.result_code) )
            self.rhs.generate_disposal_code(code)
        if self.dup.is_temp:
            self.dup.generate_subexpr_disposal_code(code)
            
    def create_dup_node(self, env): 
        import ExprNodes
        self.dup = self.lhs
        self.dup.analyse_types(env)
        if isinstance(self.lhs, ExprNodes.NameNode):
            target_lhs = ExprNodes.NameNode(self.dup.pos, name = self.dup.name, is_temp = self.dup.is_temp, entry = self.dup.entry)
        elif isinstance(self.lhs, ExprNodes.AttributeNode):
            target_lhs = ExprNodes.AttributeNode(self.dup.pos, obj = ExprNodes.CloneNode(self.lhs.obj), attribute = self.dup.attribute, is_temp = self.dup.is_temp)
        elif isinstance(self.lhs, ExprNodes.IndexNode):
            target_lhs = ExprNodes.IndexNode(self.dup.pos, base = ExprNodes.CloneNode(self.dup.base), index = ExprNodes.CloneNode(self.lhs.index), is_temp = self.dup.is_temp)
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
    }

    def annotate(self, code):
        self.lhs.annotate(code)
        self.rhs.annotate(code)
        self.dup.annotate(code)


class PrintStatNode(StatNode):
    #  print statement
    #
    #  args              [ExprNode]
    #  ends_with_comma   boolean
    
    def analyse_expressions(self, env):
        for i in range(len(self.args)):
            arg = self.args[i]
            arg.analyse_types(env)
            arg = arg.coerce_to_pyobject(env)
            arg.allocate_temps(env)
            arg.release_temp(env)
            self.args[i] = arg
            #env.recycle_pending_temps() # TEMPORARY
        env.use_utility_code(printing_utility_code)
    
    def generate_execution_code(self, code):
        for arg in self.args:
            arg.generate_evaluation_code(code)
            code.putln(
                "if (__Pyx_PrintItem(%s) < 0) %s" % (
                    arg.py_result(),
                    code.error_goto(self.pos)))
            arg.generate_disposal_code(code)
        if not self.ends_with_comma:
            code.putln(
                "if (__Pyx_PrintNewline() < 0) %s" %
                    code.error_goto(self.pos))
                    
    def annotate(self, code):
        for arg in self.args:
            arg.annotate(code)


class DelStatNode(StatNode):
    #  del statement
    #
    #  args     [ExprNode]
    
    def analyse_declarations(self, env):
        for arg in self.args:
            arg.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        for arg in self.args:
            arg.analyse_target_expression(env, None)
            if not arg.type.is_pyobject:
                error(arg.pos, "Deletion of non-Python object")
            #arg.release_target_temp(env)
    
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
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class BreakStatNode(StatNode):

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

    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        if code.in_try_finally:
            error(self.pos, "continue statement inside try of try...finally")
        elif not code.continue_label:
            error(self.pos, "continue statement not inside loop")
        else:
            #code.putln(
            #	"goto %s;" %
            #		code.continue_label)
            code.put_goto(code.continue_label)


class ReturnStatNode(StatNode):
    #  return statement
    #
    #  value         ExprNode or None
    #  return_type   PyrexType
    #  temps_in_use  [Entry]            Temps in use at time of return
    
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
#		if not (self.exc_type or self.exc_value or self.exc_tb):
#			env.use_utility_code(reraise_utility_code)
#		else:
        env.use_utility_code(raise_utility_code)
    
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

    def analyse_expressions(self, env):
        env.use_utility_code(raise_utility_code)

    def generate_execution_code(self, code):
        vars = code.exc_vars
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
    
    def analyse_expressions(self, env):
        self.cond = self.cond.analyse_boolean_expression(env)
        if self.value:
            self.value.analyse_types(env)
            self.value = self.value.coerce_to_pyobject(env)
            self.value.allocate_temps(env)
        self.cond.release_temp(env)
        if self.value:
            self.value.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
    
    def generate_execution_code(self, code):
        code.putln("#ifndef PYREX_WITHOUT_ASSERTIONS")
        self.cond.generate_evaluation_code(code)
        code.putln(
            "if (unlikely(!%s)) {" %
                self.cond.result_code)
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
    
    def analyse_declarations(self, env):
        self.condition.analyse_declarations(env)
        self.body.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.condition = \
            self.condition.analyse_temp_boolean_expression(env)
        self.condition.release_temp(env)
        #env.recycle_pending_temps() # TEMPORARY
        self.body.analyse_expressions(env)
    
    def generate_execution_code(self, code, end_label):
        self.condition.generate_evaluation_code(code)
        code.putln(
            "if (%s) {" %
                self.condition.result_code)
        self.body.generate_execution_code(code)
        #code.putln(
        #	"goto %s;" %
        #		end_label)
        code.put_goto(end_label)
        code.putln("}")

    def annotate(self, code):
        self.condition.annotate(code)
        self.body.annotate(code)
        
    
class WhileStatNode(StatNode):
    #  while statement
    #
    #  condition    ExprNode
    #  body         StatNode
    #  else_clause  StatNode
    
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
                self.condition.result_code)
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

class ForInStatNode(StatNode):
    #  for statement
    #
    #  target        ExprNode
    #  iterator      IteratorNode
    #  body          StatNode
    #  else_clause   StatNode
    #  item          NextNode       used internally
    
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
                step = ExprNodes.IntNode(pos = step.pos, value=-int(step.operand.value))
            if isinstance(step, ExprNodes.IntNode):
                if step.value > 0:
                    self.step = step
                    self.relation1 = '<='
                    self.relation2 = '<'
                    return True
                elif step.value < 0:
                    self.step = ExprNodes.IntNode(pos = step.pos, value=-int(step.value))
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
                  and sequence.function.name == 'range':
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


class ForFromStatNode(StatNode):
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
            self.loopvar_name = self.target.entry.cname
            self.py_loopvar_node = None
        else:
            self.is_py_target = 1
            c_loopvar_node = ExprNodes.TempNode(self.pos, 
                PyrexTypes.c_long_type, env)
            c_loopvar_node.allocate_temps(env)
            self.loopvar_name = c_loopvar_node.result_code
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
            incop = "%s=%s" % (incop[0], self.step.result_code)
        code.putln(
            "for (%s = %s%s; %s %s %s; %s%s) {" % (
                self.loopvar_name,
                self.bound1.result_code, offset,
                self.loopvar_name, self.relation2, self.bound2.result_code,
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


class TryExceptStatNode(StatNode):
    #  try .. except statement
    #
    #  body             StatNode
    #  except_clauses   [ExceptClauseNode]
    #  else_clause      StatNode or None
    #  cleanup_list     [Entry]            temps to clean up on error
    
    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        for except_clause in self.except_clauses:
            except_clause.analyse_declarations(env)
        if self.else_clause:
            self.else_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
        self.cleanup_list = env.free_temp_entries[:]
        for except_clause in self.except_clauses:
            except_clause.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)
    
    def generate_execution_code(self, code):
        old_error_label = code.new_error_label()
        our_error_label = code.error_label
        end_label = code.new_label()
        code.putln(
            "/*try:*/ {")
        self.body.generate_execution_code(code)
        code.putln(
            "}")
        code.error_label = old_error_label
        if self.else_clause:
            code.putln(
                "/*else:*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln(
                "}")
        code.put_goto(end_label)
        code.put_label(our_error_label)
        code.put_var_xdecrefs_clear(self.cleanup_list)
        default_clause_seen = 0
        for except_clause in self.except_clauses:
            if not except_clause.pattern:
                default_clause_seen = 1
            else:
                if default_clause_seen:
                    error(except_clause.pos, "Default except clause not last")
            except_clause.generate_handling_code(code, end_label)
        if not default_clause_seen:
            code.put_goto(code.error_label)
        code.put_label(end_label)

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
    #  match_flag     string             result of exception match
    #  exc_value      ExcValueNode       used internally
    #  function_name  string             qualified name of enclosing function
    #  exc_vars       (string * 3)       local exception variables
    
    def analyse_declarations(self, env):
        if self.target:
            self.target.analyse_target_declaration(env)
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
        self.body.analyse_expressions(env)
        for var in self.exc_vars:
            env.release_temp(var)
        env.use_utility_code(get_exception_utility_code)
    
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
            code.putln(
                "/*except:*/ {")
        code.putln(
            '__Pyx_AddTraceback("%s");' % (self.function_name))
        # We always have to fetch the exception value even if
        # there is no target, because this also normalises the 
        # exception and stores it in the thread state.
        exc_args = "&%s, &%s, &%s" % tuple(self.exc_vars)
        code.putln("if (__Pyx_GetException(%s) < 0) %s" % (exc_args,
            code.error_goto(self.pos)))
        if self.target:
            self.exc_value.generate_evaluation_code(code)
            self.target.generate_assignment_code(self.exc_value, code)
        old_exc_vars = code.exc_vars
        code.exc_vars = self.exc_vars
        self.body.generate_execution_code(code)
        code.exc_vars = old_exc_vars
        for var in self.exc_vars:
            code.putln("Py_DECREF(%s); %s = 0;" % (var, var))
        code.put_goto(end_label)
        code.putln(
            "}")

    def annotate(self, code):
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
    
    preserve_exception = 1
    
    disallow_continue_in_try_finally = 0
    # There doesn't seem to be any point in disallowing
    # continue in the try block, since we have no problem
    # handling it.
    
    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
        self.finally_clause.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
        self.cleanup_list = env.free_temp_entries[:]
        #self.exc_vars = (
        #	env.allocate_temp(PyrexTypes.py_object_type),
        #	env.allocate_temp(PyrexTypes.py_object_type),
        #	env.allocate_temp(PyrexTypes.py_object_type))
        #self.lineno_var = \
        #	env.allocate_temp(PyrexTypes.c_int_type)
        self.finally_clause.analyse_expressions(env)
        #for var in self.exc_vars:
        #	env.release_temp(var)
    
    def generate_execution_code(self, code):
        old_error_label = code.error_label
        old_labels = code.all_new_labels()
        new_labels = code.get_all_labels()
        new_error_label = code.error_label
        catch_label = code.new_label()
        code.putln(
            "/*try:*/ {")
        if self.disallow_continue_in_try_finally:
            was_in_try_finally = code.in_try_finally
            code.in_try_finally = 1
        self.body.generate_execution_code(code)
        if self.disallow_continue_in_try_finally:
            code.in_try_finally = was_in_try_finally
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
            code.use_label(catch_label)
            code.putln(
                    "__pyx_why = 0; goto %s;" % catch_label)
            for i in cases_used:
                new_label = new_labels[i]
                #if new_label and new_label <> "<try>":
                if new_label == new_error_label and self.preserve_exception:
                    self.put_error_catcher(code, 
                        new_error_label, i+1, catch_label)
                else:
                    code.putln(
                        "%s: __pyx_why = %s; goto %s;" % (
                            new_label,
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
        code.putln(
            "%s: {" %
                error_label)
        code.putln(
                "__pyx_why = %s;" %
                    i)
        code.put_var_xdecrefs_clear(self.cleanup_list)
        code.putln(
                "PyErr_Fetch(&%s, &%s, &%s);" %
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
        code.putln(
            "case %s: {" %
                i)
        code.putln(
                "PyErr_Restore(%s, %s, %s);" %
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
        
    preserve_exception = 0

    def __init__(self, pos, state, body):
        self.state = state
        TryFinallyStatNode.__init__(self, pos,
            body = body,
            finally_clause = GILExitNode(pos, state = state))

    def generate_execution_code(self, code):
        code.putln("/*with %s:*/ {" % self.state)
        if self.state == 'gil':
            code.putln("PyGILState_STATE _save = PyGILState_Ensure();")
        else:
            code.putln("PyThreadState *_save;")
            code.putln("Py_UNBLOCK_THREADS")
        TryFinallyStatNode.generate_execution_code(self, code)
        code.putln("}")

#class GILEntryNode(StatNode):
#	#  state   string   'gil' or 'nogil'
#
#	def analyse_expressions(self, env):
#		pass
#
#	def generate_execution_code(self, code):
#		if self.state == 'gil':
#			code.putln("PyGILState_STATE _save = PyGILState_Ensure();")
#		else:
#			code.putln("PyThreadState *_save;")
#			code.putln("Py_UNBLOCK_THREADS")


class GILExitNode(StatNode):
    #  Used as the 'finally' block in a GILStatNode
    #
    #  state   string   'gil' or 'nogil'

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
    
    def analyse_declarations(self, env):
        module_scope = env.find_module(self.module_name, self.pos)
        if "." in self.module_name:
            names = self.module_name.split(".")
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
    #  module_name     string                  Qualified name of module
    #  imported_names  [(pos, name, as_name)]  Names to be imported
    
    def analyse_declarations(self, env):
        module_scope = env.find_module(self.module_name, self.pos)
        env.add_imported_module(module_scope)
        for pos, name, as_name in self.imported_names:
            entry = module_scope.find(name, pos)
            if entry:
                local_name = as_name or name
                env.add_imported_entry(local_name, entry, pos)

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
    
    def analyse_declarations(self, env):
        for _, target in self.items:
            target.analyse_target_declaration(env)
    
    def analyse_expressions(self, env):
        import ExprNodes
        self.module.analyse_expressions(env)
        self.item = ExprNodes.PyTempNode(self.pos, env)
        self.item.allocate_temp(env)
        self.interned_items = []
        for name, target in self.items:
            if Options.intern_names:
                self.interned_items.append((env.intern(name), target))
            target.analyse_target_expression(env, None)
            #target.release_target_temp(env) # was release_temp ?!?
        self.module.release_temp(env)
        self.item.release_temp(env)
    
    def generate_execution_code(self, code):
        self.module.generate_evaluation_code(code)
        if Options.intern_names:
            for cname, target in self.interned_items:
                code.putln(
                    '%s = PyObject_GetAttr(%s, %s); %s' % (
                        self.item.result_code, 
                        self.module.py_result(),
                        cname,
                        code.error_goto_if_null(self.item.result_code, self.pos)))
                target.generate_assignment_code(self.item, code)
        else:
            for name, target in self.items:
                code.putln(
                    '%s = PyObject_GetAttrString(%s, "%s"); %s' % (
                        self.item.result_code, 
                        self.module.py_result(),
                        name,
                        code.error_goto_if_null(self.item.result_code, self.pos)))
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

typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n; int is_unicode;} __Pyx_StringTabEntry; /*proto*/

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

printing_utility_code = [
"""
static int __Pyx_PrintItem(PyObject *); /*proto*/
static int __Pyx_PrintNewline(void); /*proto*/
""",r"""
static PyObject *__Pyx_GetStdout(void) {
    PyObject *f = PySys_GetObject("stdout");
    if (!f) {
        PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
    }
    return f;
}

static int __Pyx_PrintItem(PyObject *v) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_SoftSpace(f, 1)) {
        if (PyFile_WriteString(" ", f) < 0)
            return -1;
    }
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
    return 0;
}

static int __Pyx_PrintNewline(void) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_WriteString("\n", f) < 0)
        return -1;
    PyFile_SoftSpace(f, 0);
    return 0;
}
"""]

#------------------------------------------------------------------------------------

# The following function is based on do_raise() from ceval.c.

raise_utility_code = [
"""
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
""","""
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
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception must be an old-style class or instance");
                goto raise_error;
            }
        #else
            type = (PyObject*) type->ob_type;
            Py_INCREF(type);
            if (!PyType_IsSubtype((PyTypeObject *)type, (PyTypeObject *)PyExc_BaseException)) {
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception class must be a subclass of BaseException");
                goto raise_error;
            }
        #endif
    }
    PyErr_Restore(type, value, tb);
    return;
raise_error:
    Py_XDECREF(value);
    Py_XDECREF(type);
    Py_XDECREF(tb);
    return;
}
"""]

#------------------------------------------------------------------------------------

reraise_utility_code = [
"""
static void __Pyx_ReRaise(void); /*proto*/
""","""
static void __Pyx_ReRaise(void) {
    PyThreadState *tstate = PyThreadState_Get();
    PyObject *type = tstate->exc_type;
    PyObject *value = tstate->exc_value;
    PyObject *tb = tstate->exc_traceback;
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    PyErr_Restore(type, value, tb);
}
"""]

#------------------------------------------------------------------------------------

arg_type_test_utility_code = [
"""
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name); /*proto*/
""","""
static int __Pyx_ArgTypeTest(PyObject *obj, PyTypeObject *type, int none_allowed, char *name) {
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if ((none_allowed && obj == Py_None) || PyObject_TypeCheck(obj, type))
        return 1;
    PyErr_Format(PyExc_TypeError,
        "Argument '%s' has incorrect type (expected %s, got %s)",
        name, type->tp_name, obj->ob_type->tp_name);
    return 0;
}
"""]

#------------------------------------------------------------------------------------
#
#  __Pyx_SplitStarArg splits the args tuple into two parts, one part
#  suitable for passing to PyArg_ParseTupleAndKeywords, and the other
#  containing any extra arguments. On success, replaces the borrowed
#  reference *args with references to a new tuple, and passes back a
#  new reference in *args2.  Does not touch any of its arguments on
#  failure.

get_stararg_utility_code = [
"""
static INLINE int __Pyx_SplitStarArg(PyObject **args, Py_ssize_t nargs, PyObject **args2); /*proto*/
""","""
static INLINE int __Pyx_SplitStarArg(
    PyObject **args, 
    Py_ssize_t nargs,
    PyObject **args2)
{
    PyObject *args1 = 0;
    args1 = PyTuple_GetSlice(*args, 0, nargs);
    if (!args1) {
        *args2 = 0;
        return -1;
    }
    *args2 = PyTuple_GetSlice(*args, nargs, PyTuple_GET_SIZE(*args));
    if (!*args2) {
        Py_DECREF(args1);
        return -1;
    }
    *args = args1;
    return 0;
}
"""]

#------------------------------------------------------------------------------------
#
#  __Pyx_SplitKeywords splits the kwds dict into two parts one part
#  suitable for passing to PyArg_ParseTupleAndKeywords, and the other
#  containing any extra arguments. On success, replaces the borrowed
#  reference *kwds with references to a new dict, and passes back a
#  new reference in *kwds2.  Does not touch any of its arguments on
#  failure.
#
#  Any of *kwds and kwds2 may be 0 (but not kwds). If *kwds == 0, it
#  is not changed. If kwds2 == 0 and *kwds != 0, a new reference to
#  the same dictionary is passed back in *kwds.
#
#  If rqd_kwds is not 0, it is an array of booleans corresponding to
#  the names in kwd_list, indicating required keyword arguments. If
#  any of these are not present in kwds, an exception is raised.
#

get_splitkeywords_utility_code = [
"""
static int __Pyx_SplitKeywords(PyObject **kwds, char *kwd_list[], \
    PyObject **kwds2, char rqd_kwds[]); /*proto*/
""","""
static int __Pyx_SplitKeywords(
    PyObject **kwds,
    char *kwd_list[], 
    PyObject **kwds2,
    char rqd_kwds[])
{
    PyObject *s = 0, *x = 0, *kwds1 = 0;
    int i;
    char **p;
    
    if (*kwds) {
        kwds1 = PyDict_New();
        if (!kwds1)
            goto bad;
        *kwds2 = PyDict_Copy(*kwds);
        if (!*kwds2)
            goto bad;
        for (i = 0, p = kwd_list; *p; i++, p++) {
            s = PyString_FromString(*p);
            x = PyDict_GetItem(*kwds, s);
            if (x) {
                if (PyDict_SetItem(kwds1, s, x) < 0)
                    goto bad;
                if (PyDict_DelItem(*kwds2, s) < 0)
                    goto bad;
            }
            else if (rqd_kwds && rqd_kwds[i])
                goto missing_kwarg;
            Py_DECREF(s);
        }
        s = 0;
    }
    else {
        if (rqd_kwds) {
            for (i = 0, p = kwd_list; *p; i++, p++)
                if (rqd_kwds[i])
                    goto missing_kwarg;
        }
        *kwds2 = PyDict_New();
        if (!*kwds2)
            goto bad;
    }

    *kwds = kwds1;
    return 0;
missing_kwarg:
    PyErr_Format(PyExc_TypeError,
        "required keyword argument '%s' is missing", *p);
bad:
    Py_XDECREF(s);
    Py_XDECREF(kwds1);
    Py_XDECREF(*kwds2);
    return -1;
}
"""]

get_checkkeywords_utility_code = [
"""
static INLINE int __Pyx_CheckRequiredKeywords(PyObject *kwds, char *kwd_list[],
    char rqd_kwds[]); /*proto*/
""","""
static INLINE int __Pyx_CheckRequiredKeywords(
    PyObject *kwds,
    char *kwd_list[],
    char rqd_kwds[])
{
    int i;
    char **p;

    if (kwds) {
        for (i = 0, p = kwd_list; *p; i++, p++)
            if (rqd_kwds[i] && !PyDict_GetItemString(kwds, *p))
                goto missing_kwarg;
    }
    else {
        for (i = 0, p = kwd_list; *p; i++, p++)
            if (rqd_kwds[i])
                goto missing_kwarg;
    }

    return 0;
missing_kwarg:
    PyErr_Format(PyExc_TypeError,
        "required keyword argument '%s' is missing", *p);
    return -1;
}
"""]

#------------------------------------------------------------------------------------

unraisable_exception_utility_code = [
"""
static void __Pyx_WriteUnraisable(char *name); /*proto*/
""","""
static void __Pyx_WriteUnraisable(char *name) {
    PyObject *old_exc, *old_val, *old_tb;
    PyObject *ctx;
    PyErr_Fetch(&old_exc, &old_val, &old_tb);
    ctx = PyString_FromString(name);
    PyErr_Restore(old_exc, old_val, old_tb);
    if (!ctx)
        ctx = Py_None;
    PyErr_WriteUnraisable(ctx);
}
"""]

#------------------------------------------------------------------------------------

traceback_utility_code = [
"""
static void __Pyx_AddTraceback(char *funcname); /*proto*/
""","""
#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(%(FILENAME)s);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(%(GLOBALS)s);
    if (!py_globals) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
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
        PyThreadState_Get(), /*PyThreadState *tstate,*/
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
    'GLOBALS': Naming.module_cname,
    'EMPTY_TUPLE' : Naming.empty_tuple,
}]

#------------------------------------------------------------------------------------

set_vtable_utility_code = [
"""
static int __Pyx_SetVtable(PyObject *dict, void *vtable); /*proto*/
""","""
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
"""]

#------------------------------------------------------------------------------------

get_vtable_utility_code = [
"""
static int __Pyx_GetVtable(PyObject *dict, void *vtabptr); /*proto*/
""",r"""
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
"""]

#------------------------------------------------------------------------------------

init_intern_tab_utility_code = [
"""
static int __Pyx_InternStrings(__Pyx_InternTabEntry *t); /*proto*/
""","""
static int __Pyx_InternStrings(__Pyx_InternTabEntry *t) {
    while (t->p) {
        *t->p = PyString_InternFromString(t->s);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}
"""]

#------------------------------------------------------------------------------------

init_string_tab_utility_code = [
"""
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/
""","""
static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        if (t->is_unicode) {
            *t->p = PyUnicode_DecodeUTF8(t->s, t->n - 1, NULL);
        } else {
            *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        }
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}
"""]

#------------------------------------------------------------------------------------

get_exception_utility_code = [
"""
static int __Pyx_GetException(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
""","""
static int __Pyx_GetException(PyObject **type, PyObject **value, PyObject **tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_Get();
    PyErr_Fetch(type, value, tb);
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
"""]

#------------------------------------------------------------------------------------
