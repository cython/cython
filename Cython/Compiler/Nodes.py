#
#   Pyrex - Parse tree nodes
#

import string, sys

import Code
from Errors import error, InternalError
import Naming
import PyrexTypes
from PyrexTypes import py_object_type, error_type, CTypedefType
from Symtab import ModuleScope, LocalScope, \
    StructOrUnionScope, PyClassScope, CClassScope
from Pyrex.Utils import open_new_file, replace_suffix
import Options

from DebugFlags import debug_disposal_code

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
    pass


class CNameDeclaratorNode(CDeclaratorNode):
    #  name   string           The Pyrex name being declared
    #  cname  string or None   C name, if specified
    
    def analyse(self, base_type, env):
        return self, base_type


class CPtrDeclaratorNode(CDeclaratorNode):
    # base     CDeclaratorNode
    
    def analyse(self, base_type, env):
        if base_type.is_pyobject:
            error(self.pos,
                "Pointer base type cannot be a Python object")
        ptr_type = PyrexTypes.c_ptr_type(base_type)
        return self.base.analyse(ptr_type, env)
        

class CArrayDeclaratorNode(CDeclaratorNode):
    # base        CDeclaratorNode
    # dimension   ExprNode
    
    def analyse(self, base_type, env):
        if self.dimension:
            self.dimension.analyse_const_expression(env)
            if not self.dimension.type.is_int:
                error(self.dimension.pos, "Array dimension not integer")
            #size = self.dimension.value
            size = self.dimension.result_code
        else:
            size = None
        if not base_type.is_complete():
            error(self.pos,
                "Array element type '%s' is incomplete" % base_type)
        if base_type.is_pyobject:
            error(self.pos,
                "Array element cannot be a Python object")
        array_type = PyrexTypes.c_array_type(base_type, size)
        return self.base.analyse(array_type, env)


class CFuncDeclaratorNode(CDeclaratorNode):
    # base             CDeclaratorNode
    # args             [CArgDeclNode]
    # has_varargs      boolean
    # exception_value  ConstNode
    # exception_check  boolean    True if PyErr_Occurred check needed

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
        func_type = PyrexTypes.CFuncType(
            return_type, func_type_args, self.has_varargs, 
            exception_value = exc_val, exception_check = exc_check)
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
    
    is_self_arg = 0
    
    def analyse(self, env):
        base_type = self.base_type.analyse(env)
        return self.declarator.analyse(base_type, env)


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
        type = None
        if self.is_basic_c_type:
            type = PyrexTypes.simple_c_type(self.signed, self.longness, self.name)
            if not type:
                error(self.pos, "Unrecognised type modifier combination")
        elif self.name == "object" and not self.module_path:
            type = py_object_type
        elif self.name is None:
            if self.is_self_arg and env.is_c_class_scope:
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
            if type.is_cfunction:
                dest_scope.declare_cfunction(name, type, declarator.pos,
                    cname = cname, visibility = self.visibility)
            else:
                dest_scope.declare_var(name, type, declarator.pos,
                    cname = cname, visibility = self.visibility, is_cdef = 1)
    
    def analyse_expressions(self, env):
        pass
    
    def generate_execution_code(self, code):
        pass


class CStructOrUnionDefNode(StatNode):
    #  name          string
    #  cname         string or None
    #  kind          "struct" or "union"
    #  typedef_flag  boolean
    #  attributes    [CVarDefNode] or None
    #  entry         Entry
    
    def analyse_declarations(self, env):
        scope = None
        if self.attributes is not None:
            scope = StructOrUnionScope()
        self.entry = env.declare_struct_or_union(
            self.name, self.kind, scope, self.typedef_flag, self.pos,
            self.cname)
        if self.attributes is not None:
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
    #  entry          Entry
    
    def analyse_declarations(self, env):
        self.entry = env.declare_enum(self.name, self.pos,
            cname = self.cname, typedef_flag = self.typedef_flag)
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
    #  base_type   CBaseTypeNode
    #  declarator  CDeclaratorNode
    
    def analyse_declarations(self, env):
        base = self.base_type.analyse(env)
        name_declarator, type = self.declarator.analyse(base, env)
        name = name_declarator.name
        cname = name_declarator.cname
        if env.in_cinclude:
            type = CTypedefType(cname or name, type)
        env.declare_type(name, type, self.pos, cname = cname)
    
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
    
    def analyse_expressions(self, env):
        pass
                
    def generate_function_definitions(self, env, code):
        # Generate C code for header and body of function
        genv = env.global_scope()
        lenv = LocalScope(name = self.entry.name, outer_scope = genv)
        #lenv.function_name = self.function_name()
        lenv.return_type = self.return_type
        #self.filename = lenv.get_filename_const(self.pos)
        code.init_labels()
        self.declare_arguments(lenv)
        self.body.analyse_declarations(lenv)
        self.body.analyse_expressions(lenv)
        # Code for nested function definitions would go here
        # if we supported them, which we probably won't.
        # ----- Top-level constants used by this function
        self.generate_interned_name_decls(lenv, code)
        self.generate_py_string_decls(lenv, code)
        self.generate_const_definitions(lenv, code)
        # ----- Function header
        code.putln("")
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
        # ----- Fetch arguments
        self.generate_argument_parsing_code(code)
        self.generate_argument_increfs(lenv, code)
        # ----- Initialise local variables
        for entry in lenv.var_entries:
            if entry.type.is_pyobject and entry.init_to_none and entry.used:
                code.put_init_var_to_py_none(entry)
        # ----- Check and convert arguments
        self.generate_argument_conversion_code(code)
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
        # ----- Return cleanup
        code.put_label(code.return_label)
        code.put_var_decrefs(lenv.var_entries, used_only = 1)
        code.put_var_decrefs(lenv.arg_entries)
        self.put_stararg_decrefs(code)
        if not self.return_type.is_void:
            retval_code = Naming.retval_cname
            #if self.return_type.is_extension_type:
            #	retval_code = "((%s)%s) " % (
            #		self.return_type.declaration_code(""),
            #		retval_code)
            code.putln("return %s;" % retval_code)
        code.putln("}")
    
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
    #  visibility    'private' or 'public' or 'extern'
    #  base_type     CBaseTypeNode
    #  declarator    CDeclaratorNode
    #  body          StatListNode
    #
    #  type          CFuncType
    
    def unqualified_name(self):
        return self.entry.name
        
    def analyse_declarations(self, env):
        base_type = self.base_type.analyse(env)
        name_declarator, type = self.declarator.analyse(base_type, env)
        # Remember the actual type according to the function header
        # written here, because the type in the symbol table entry
        # may be different if we're overriding a C method inherited
        # from the base type of an extension type.
        self.type = type
        if not type.is_cfunction:
            error(self.pos, 
                "Suite attached to non-function declaration")
        name = name_declarator.name
        cname = name_declarator.cname
        self.entry = env.declare_cfunction(
            name, type, self.pos, 
            cname = cname, visibility = self.visibility,
            defining = self.body is not None)
        self.return_type = type.return_type
    
    def declare_arguments(self, env):
        for arg in self.type.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            self.declare_argument(env, arg)
            
    def generate_function_header(self, code, with_pymethdef):
        arg_decls = []
        type = self.type
        for arg in type.args:
            arg_decls.append(arg.declaration_code())
        if type.has_varargs:
            arg_decls.append("...")
        if not arg_decls:
            arg_decls = ["void"]
        entity = "%s(%s)" % (self.entry.func_cname,
            string.join(arg_decls, ","))
        if self.visibility == 'public':
            dll_linkage = "DL_EXPORT"
        else:
            dll_linkage = None
        header = self.return_type.declaration_code(entity,
            dll_linkage = dll_linkage)
        if self.visibility <> 'private':
            storage_class = "%s " % Naming.extern_c_macro
        else:
            storage_class = "static "
        code.putln("%s%s {" % (
            storage_class,
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
        pass
    
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
        if self.star_arg or self.starstar_arg:
            env.use_utility_code(get_starargs_utility_code)
    
    def analyse_signature(self, env):
        any_type_tests_needed = 0
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
        self.entry = env.declare_pyfunction(self.name, self.pos)
        self.entry.doc = self.doc
        self.entry.func_cname = \
            Naming.func_prefix + env.scope_prefix + self.name
        self.entry.doc_cname = \
            Naming.funcdoc_prefix + env.scope_prefix + self.name
        self.entry.pymethdef_cname = \
            Naming.pymethdef_prefix + env.scope_prefix + self.name
        
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
        for arg in self.args:
            if arg.default:
                if arg.is_generic:
                    arg.default.analyse_types(env)
                    arg.default = arg.default.coerce_to(arg.type, env)
                    arg.default.allocate_temps(env)
                    arg.default_entry = env.add_default_value(arg.type)
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
            
    def generate_function_header(self, code, with_pymethdef):
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
        if sig.has_generic_args:
            arg_code_list.append(
                "PyObject *%s, PyObject *%s"
                    % (Naming.args_cname, Naming.kwds_cname))
        arg_code = ", ".join(arg_code_list)
        dc = self.return_type.declaration_code(self.entry.func_cname)
        header = "static %s(%s)" % (dc, arg_code)
        code.putln("%s; /*proto*/" % header)
        if self.entry.doc:
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
                code.put_var_declaration(arg.entry)
    
    def generate_keyword_list(self, code):
        if self.entry.signature.has_generic_args:
            code.put(
                "static char *%s[] = {" %
                    Naming.kwdlist_cname)
            for arg in self.args:
                if arg.is_generic:
                    code.put(
                        '"%s",' % 
                            arg.name)
            code.putln(
                "0};")
    
    def generate_argument_parsing_code(self, code):
        # Generate PyArg_ParseTuple call for generic
        # arguments, if any.
        if self.entry.signature.has_generic_args:
            arg_addrs = []
            arg_formats = []
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
                    elif default_seen:
                        error(arg.pos, "Non-default argument following default argument")
                    arg_addrs.append("&" + arg_entry.cname)
                    format = arg_entry.type.parsetuple_format
                    if format:
                        arg_formats.append(format)
                    else:
                        error(arg.pos, 
                            "Cannot convert Python object argument to type '%s'" 
                                % arg.type)
            argformat = '"%s"' % string.join(arg_formats, "")
            has_starargs = self.star_arg is not None or self.starstar_arg is not None
            if has_starargs:
                self.generate_stararg_getting_code(code)
            pt_arglist = [Naming.args_cname, Naming.kwds_cname, argformat,
                    Naming.kwdlist_cname] + arg_addrs
            pt_argstring = string.join(pt_arglist, ", ")
            code.put(
                'if (!PyArg_ParseTupleAndKeywords(%s)) ' %
                    pt_argstring)
            error_return_code = "return %s;" % self.error_value()
            if has_starargs:
                code.putln("{")
                code.put_xdecref(Naming.args_cname, py_object_type)
                code.put_xdecref(Naming.kwds_cname, py_object_type)
                self.generate_arg_xdecref(self.star_arg, code)
                self.generate_arg_xdecref(self.starstar_arg, code)
                code.putln(error_return_code)
                code.putln("}")
            else:
                code.putln(error_return_code)
            
    def put_stararg_decrefs(self, code):
        if self.star_arg or self.starstar_arg:
            code.put_xdecref(Naming.args_cname, py_object_type)
            code.put_xdecref(Naming.kwds_cname, py_object_type)
    
    def generate_arg_xdecref(self, arg, code):
        if arg:
            code.put_var_xdecref(arg.entry)
    
    def arg_address(self, arg):
        if arg:
            return "&%s" % arg.entry.cname
        else:
            return 0

    def generate_stararg_getting_code(self, code):
        if self.star_arg or self.starstar_arg:
            if not self.entry.signature.has_generic_args:
                error(self.pos, "This method cannot have * or ** arguments")
            star_arg_addr = self.arg_address(self.star_arg)
            starstar_arg_addr = self.arg_address(self.starstar_arg)
            code.putln(
                "if (__Pyx_GetStarArgs(&%s, &%s, %s, %s, %s, %s) < 0) return %s;" % (
                    Naming.args_cname,
                    Naming.kwds_cname,
                    Naming.kwdlist_cname,
                    len(self.args) - self.entry.signature.num_fixed_args(),
                    star_arg_addr,
                    starstar_arg_addr,
                    self.error_value()))
    
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
            self.generate_arg_conversion_from_pyobject(arg, code)
        elif new_type.is_pyobject:
            self.generate_arg_conversion_to_pyobject(arg, code)
        else:
            if new_type.assignable_from(old_type):
                code.putln(
                    "%s = %s;" % (arg.entry.cname, arg.hdr_cname))
            else:
                error(arg.pos,
                    "Cannot convert argument from '%s' to '%s'" %
                        (old_type, new_type))
    
    def generate_arg_conversion_from_pyobject(self, arg, code):
        new_type = arg.type
        func = new_type.from_py_function
        if func:
            code.putln("%s = %s(%s); if (PyErr_Occurred()) %s" % (
                arg.entry.cname,
                func,
                arg.hdr_cname,
                code.error_goto(arg.pos)))
        else:
            error(arg.pos, 
                "Cannot convert Python object argument to type '%s'" 
                    % new_type)
    
    def generate_arg_conversion_to_pyobject(self, arg, code):
        old_type = arg.hdr_type
        func = old_type.to_py_function
        if func:
            code.putln("%s = %s(%s); if (!%s) %s" % (
                arg.entry.cname,
                func,
                arg.hdr_cname,
                arg.entry.cname,
                code.error_goto(arg.pos)))
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
                'if (!__Pyx_ArgTypeTest(%s, %s, %d, "%s")) %s' % (
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
        if self.doc:
            doc_node = ExprNodes.StringNode(pos, value = self.doc)
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
            typedef_flag = self.typedef_flag)
        scope = self.entry.type.scope
        if self.doc:
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
            self.body.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        if self.body:
            self.body.generate_function_definitions(
                self.entry.type.scope, code)
    
    def generate_execution_code(self, code):
        # This is needed to generate evaluation code for
        # default values of method arguments.
        if self.body:
            self.body.generate_execution_code(code)


class PropertyNode(StatNode):
    #  Definition of a property in an extension type.
    #
    #  name   string
    #  doc    string or None    Doc string
    #  body   StatListNode
    
    def analyse_declarations(self, env):
        entry = env.declare_property(self.name, self.doc, self.pos)
        if entry:
            if self.doc:
                doc_entry = env.get_string_const(self.doc)
                entry.doc_cname = doc_entry.cname
            self.body.analyse_declarations(entry.scope)
        
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)

    def generate_execution_code(self, code):
        pass


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
        #env.recycle_pending_temps() # TEMPORARY
        if not (self.exc_type or self.exc_value or self.exc_tb):
            env.use_utility_code(reraise_utility_code)
        else:
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
        self.cond.generate_evaluation_code(code)
        if self.value:
            self.value.generate_evaluation_code(code)
        code.putln(
            "if (!%s) {" %
                self.cond.result_code)
        if self.value:
            code.putln(
                "PyErr_SetObject(PyExc_AssertionError, %s);" %
                    self.value.py_result())
        else:
            code.putln(
                "PyErr_SetNone(PyExc_AssertionError);")
        code.putln(
                code.error_goto(self.pos))
        code.putln(
            "}")
        self.cond.generate_disposal_code(code)
        if self.value:
            self.value.generate_disposal_code(code)


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
        end_label = code.new_label()
        for if_clause in self.if_clauses:
            if_clause.generate_execution_code(code, end_label)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(end_label)


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
    
    def analyse_expressions(self, env):
        import ExprNodes
        self.iterator.analyse_expressions(env)
        self.target.analyse_target_types(env)
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


class ForFromStatNode(StatNode):
    #  for name from expr rel name rel expr
    #
    #  target        NameNode
    #  bound1        ExprNode
    #  relation1     string
    #  relation2     string
    #  bound2        ExprNode
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
        self.bound1 = self.bound1.coerce_to_integer(env)
        self.bound2 = self.bound2.coerce_to_integer(env)
        if not (self.bound2.is_name or self.bound2.is_literal):
            self.bound2 = self.bound2.coerce_to_temp(env)
        target_type = self.target.type
        if not (target_type.is_pyobject or target_type.is_int):
            error(self.target.pos,
                "Integer for-loop variable must be of type int or Python object")
        #if not (target_type.is_pyobject
        #	or target_type.assignable_from(PyrexTypes.c_int_type)):
        #		error(self.target.pos,
        #			"Cannot assign integer to variable of type '%s'" % target_type)
        if target_type.is_int:
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
            
    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        self.bound1.generate_evaluation_code(code)
        self.bound2.generate_evaluation_code(code)
        offset, incop = self.relation_table[self.relation1]
        code.putln(
            "for (%s = %s%s; %s %s %s; %s%s) {" % (
                self.loopvar_name,
                self.bound1.result_code, offset,
                self.loopvar_name, self.relation2, self.bound2.result_code,
                incop, self.loopvar_name))
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
    
    relation_table = {
        # {relop : (initial offset, increment op)}
        '<=': ("",   "++"),
        '<' : ("+1", "++"),
        '>=': ("",   "--"),
        '>' : ("-1", "--")
    }


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
        #code.putln(
        #	"goto %s;" %
        #		end_label)
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
            #code.putln(
            #	"goto %s;" %
            #		code.error_label)
            code.put_goto(code.error_label)
        code.put_label(end_label)


class ExceptClauseNode(Node):
    #  Part of try ... except statement.
    #
    #  pattern        ExprNode
    #  target         ExprNode or None
    #  body           StatNode
    #  match_flag     string             result of exception match
    #  exc_value      ExcValueNode       used internally
    #  function_name  string             qualified name of enclosing function
    
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
        self.exc_value = ExprNodes.ExcValueNode(self.pos, env)
        self.exc_value.allocate_temps(env)
        if self.target:
            self.target.analyse_target_expression(env, self.exc_value)
        else:
            self.exc_value.release_temp(env)
        #if self.target:
        #	self.target.release_target_temp(env)
        self.body.analyse_expressions(env)
    
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
        self.exc_value.generate_evaluation_code(code)
        if self.target:
            self.target.generate_assignment_code(self.exc_value, code)
        else:
            self.exc_value.generate_disposal_code(code)
        self.body.generate_execution_code(code)
        #code.putln(
        #	"goto %s;"
        #		% end_label)
        code.put_goto(end_label)
        code.putln(
            "}")


class TryFinallyStatNode(StatNode):
    #  try ... finally statement
    #
    #  body             StatNode
    #  finally_clause   StatNode
    #  cleanup_list     [Entry]      temps to clean up on error
    #  exc_vars         3*(string,)  temps to hold saved exception
    #
    #  The plan is that we funnel all continue, break
    #  return and error gotos into the beginning of the
    #  finally block, setting a variable to remember which
    #  one we're doing. At the end of the finally block, we
    #  switch on the variable to figure out where to go.
    #  In addition, if we're doing an error, we save the
    #  exception on entry to the finally block and restore
    #  it on exit.
    
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
        self.exc_vars = (
            env.allocate_temp(PyrexTypes.py_object_type),
            env.allocate_temp(PyrexTypes.py_object_type),
            env.allocate_temp(PyrexTypes.py_object_type))
        self.lineno_var = \
            env.allocate_temp(PyrexTypes.c_int_type)
        self.finally_clause.analyse_expressions(env)
        for var in self.exc_vars:
            env.release_temp(var)
    
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
        code.putln(
                "int __pyx_why;")
        #code.putln(
        #		"PyObject *%s, *%s, *%s;" %
        #			self.exc_vars)
        #code.putln(
        #		"int %s;" %
        #			self.lineno_var)
        code.use_label(catch_label)
        code.putln(
                "__pyx_why = 0; goto %s;" %
                    catch_label)
        for i in range(len(new_labels)):
            new_label = new_labels[i]
            if new_label and new_label <> "<try>":
                if new_label in code.labels_used:
                    if new_label == new_error_label:
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
        self.finally_clause.generate_execution_code(code)
        code.putln(
                "switch (__pyx_why) {")
        for i in range(len(old_labels)):
            if old_labels[i]:
                if old_labels[i] == old_error_label:
                    self.put_error_uncatcher(code, i+1, old_error_label)
                else:
                    code.use_label(old_labels[i])
                    code.putln(
                        "case %s: goto %s;" % (
                            i+1,
                            old_labels[i]))
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
                    self.exc_vars)
        code.putln(
                "%s = %s;" % (
                    self.lineno_var, Naming.lineno_cname))
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
                    self.exc_vars)
        code.putln(
                "%s = %s;" % (
                    Naming.lineno_cname, self.lineno_var))
        for var in self.exc_vars:
            code.putln(
                "%s = 0;" %
                    var)
        #code.putln(
        #		"goto %s;" %
        #			error_label)
        code.put_goto(error_label)
        code.putln(
            "}")


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
                    '%s = PyObject_GetAttr(%s, %s); if (!%s) %s' % (
                        self.item.result_code, 
                        self.module.py_result(),
                        cname,
                        self.item.result_code,
                        code.error_goto(self.pos)))
                target.generate_assignment_code(self.item, code)
        else:
            for name, target in self.items:
                code.putln(
                    '%s = PyObject_GetAttrString(%s, "%s"); if (!%s) %s' % (
                        self.item.result_code, 
                        self.module.py_result(),
                        name,
                        self.item.result_code,
                        code.error_goto(self.pos)))
                target.generate_assignment_code(self.item, code)
        self.module.generate_disposal_code(code)

#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

utility_function_predeclarations = \
"""
typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n;} __Pyx_StringTabEntry; /*proto*/
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
        int len = PyString_Size(v);
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
    /* Next, repeatedly, replace a tuple exception with its first item */
    while (PyTuple_Check(type) && PyTuple_Size(type) > 0) {
        PyObject *tmp = type;
        type = PyTuple_GET_ITEM(type, 0);
        Py_INCREF(type);
        Py_DECREF(tmp);
    }
    if (PyString_Check(type)) {
        if (PyErr_Warn(PyExc_DeprecationWarning,
                "raising a string exception is deprecated"))
            goto raise_error;
    }
    else if (PyType_Check(type) || PyClass_Check(type))
        ; /*PyErr_NormalizeException(&type, &value, &tb);*/
    else {
        /* Raising an instance.  The value should be a dummy. */
        if (value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
                "instance exception may not have a separate value");
            goto raise_error;
        }
        /* Normalize to raise <class>, <instance> */
        Py_DECREF(value);
        value = type;
        if (PyInstance_Check(type))
            type = (PyObject*) ((PyInstanceObject*)type)->in_class;
        else
            type = (PyObject*) type->ob_type;
        Py_INCREF(type);
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
#  __Pyx_GetStarArgs splits the args tuple and kwds dict into two parts
#  each, one part suitable for passing to PyArg_ParseTupleAndKeywords,
#  and the other containing any extra arguments. On success, replaces
#  the borrowed references *args and *kwds with references to a new
#  tuple and dict, and passes back new references in *args2 and *kwds2.
#  Does not touch any of its arguments on failure.
#
#  Any of *kwds, args2 and kwds2 may be 0 (but not args or kwds). If
#  *kwds == 0, it is not changed. If kwds2 == 0 and *kwds != 0, a new
#  reference to the same dictionary is passed back in *kwds.
#

get_starargs_utility_code = [
"""
static int __Pyx_GetStarArgs(PyObject **args, PyObject **kwds,\
 char *kwd_list[], int nargs, PyObject **args2, PyObject **kwds2); /*proto*/
""","""
static int __Pyx_GetStarArgs(
    PyObject **args, 
    PyObject **kwds,
    char *kwd_list[], 
    int nargs,
    PyObject **args2, 
    PyObject **kwds2)
{
    PyObject *x = 0, *args1 = 0, *kwds1 = 0;
    
    if (args2)
        *args2 = 0;
    if (kwds2)
        *kwds2 = 0;
    
    if (args2) {
        args1 = PyTuple_GetSlice(*args, 0, nargs);
        if (!args1)
            goto bad;
        *args2 = PyTuple_GetSlice(*args, nargs, PyTuple_Size(*args));
        if (!*args2)
            goto bad;
    }
    else {
        args1 = *args;
        Py_INCREF(args1);
    }
    
    if (kwds2) {
        if (*kwds) {
            char **p;
            kwds1 = PyDict_New();
            if (!kwds)
                goto bad;
            *kwds2 = PyDict_Copy(*kwds);
            if (!*kwds2)
                goto bad;
            for (p = kwd_list; *p; p++) {
                x = PyDict_GetItemString(*kwds, *p);
                if (x) {
                    if (PyDict_SetItemString(kwds1, *p, x) < 0)
                        goto bad;
                    if (PyDict_DelItemString(*kwds2, *p) < 0)
                        goto bad;
                }
            }
        }
        else {
            *kwds2 = PyDict_New();
            if (!*kwds2)
                goto bad;
        }
    }
    else {
        kwds1 = *kwds;
        Py_XINCREF(kwds1);
    }
    
    *args = args1;
    *kwds = kwds1;
    return 0;
bad:
    Py_XDECREF(args1);
    Py_XDECREF(kwds1);
    if (*args2) {
        Py_XDECREF(*args2);
    }
    if (*kwds2) {
        Py_XDECREF(*kwds2);
    }
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
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(%(FILENAME)s);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(%(GLOBALS)s);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
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
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}
""" % {
    'FILENAME': Naming.filename_cname,
    'LINENO':  Naming.lineno_cname,
    'GLOBALS': Naming.module_cname
}]

#------------------------------------------------------------------------------------

type_import_utility_code = [
"""
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, long size);  /*proto*/
""","""
static PyTypeObject *__Pyx_ImportType(char *module_name, char *class_name, 
    long size) 
{
    PyObject *py_module_name = 0;
    PyObject *py_class_name = 0;
    PyObject *py_name_list = 0;
    PyObject *py_module = 0;
    PyObject *result = 0;
    
    py_module_name = PyString_FromString(module_name);
    if (!py_module_name)
        goto bad;
    py_class_name = PyString_FromString(class_name);
    if (!py_class_name)
        goto bad;
    py_name_list = PyList_New(1);
    if (!py_name_list)
        goto bad;
    Py_INCREF(py_class_name);
    if (PyList_SetItem(py_name_list, 0, py_class_name) < 0)
        goto bad;
    py_module = __Pyx_Import(py_module_name, py_name_list);
    if (!py_module)
        goto bad;
    result = PyObject_GetAttr(py_module, py_class_name);
    if (!result)
        goto bad;
    if (!PyType_Check(result)) {
        PyErr_Format(PyExc_TypeError, 
            "%s.%s is not a type object",
            module_name, class_name);
        goto bad;
    }
    if (((PyTypeObject *)result)->tp_basicsize != size) {
        PyErr_Format(PyExc_ValueError, 
            "%s.%s does not appear to be the correct type object",
            module_name, class_name);
        goto bad;
    }
    goto done;
bad:
    Py_XDECREF(result);
    result = 0;
done:
    Py_XDECREF(py_module_name);
    Py_XDECREF(py_class_name);
    Py_XDECREF(py_name_list);
    return (PyTypeObject *)result;
}
"""]

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
        *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}
"""]

#------------------------------------------------------------------------------------
