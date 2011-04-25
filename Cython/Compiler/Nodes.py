
#
#   Pyrex - Parse tree nodes
#

import cython
from cython import set
cython.declare(sys=object, os=object, time=object, copy=object,
               Builtin=object, error=object, warning=object, Naming=object, PyrexTypes=object,
               py_object_type=object, ModuleScope=object, LocalScope=object, ClosureScope=object, \
               StructOrUnionScope=object, PyClassScope=object, CClassScope=object,
               CppClassScope=object, UtilityCode=object, EncodedString=object,
               absolute_path_length=cython.Py_ssize_t)

import sys, os, time, copy

import Builtin
from Errors import error, warning, InternalError
import Naming
import PyrexTypes
import TypeSlots
from PyrexTypes import py_object_type, error_type, CFuncType
from Symtab import ModuleScope, LocalScope, ClosureScope, \
    StructOrUnionScope, PyClassScope, CClassScope, CppClassScope
from Cython.Utils import open_new_file, replace_suffix
from Code import UtilityCode, ClosureTempAllocator
from StringEncoding import EncodedString, escape_byte_string, split_string_literal
import Options
import ControlFlow
import DebugFlags

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


from Code import CCodeWriter
from types import FunctionType

def write_func_call(func):
    def f(*args, **kwds):
        if len(args) > 1 and isinstance(args[1], CCodeWriter):
            # here we annotate the code with this function call
            # but only if new code is generated
            node, code = args[:2]
            marker = '                    /* %s -> %s.%s %s */' % (
                    ' ' * code.call_level,
                    node.__class__.__name__,
                    func.__name__,
                    node.pos[1:])
            pristine = code.buffer.stream.tell()
            code.putln(marker)
            start = code.buffer.stream.tell()
            code.call_level += 4
            res = func(*args, **kwds)
            code.call_level -= 4
            if start == code.buffer.stream.tell():
                code.buffer.stream.seek(pristine)
            else:
                marker = marker.replace('->', '<-')
                code.putln(marker)
            return res
        else:
            return func(*args, **kwds)
    return f

class VerboseCodeWriter(type):
    # Set this as a metaclass to trace function calls in code.
    # This slows down code generation and makes much larger files.
    def __new__(cls, name, bases, attrs):
        attrs = dict(attrs)
        for mname, m in attrs.items():
            if isinstance(m, FunctionType):
                attrs[mname] = write_func_call(m)
        return super(VerboseCodeWriter, cls).__new__(cls, name, bases, attrs)


class Node(object):
    #  pos         (string, int, int)   Source file position
    #  is_name     boolean              Is a NameNode
    #  is_literal  boolean              Is a ConstNode

    if DebugFlags.debug_trace_code_generation:
        __metaclass__ = VerboseCodeWriter

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

    nogil_check = None

    def gil_error(self, env=None):
        error(self.pos, "%s not allowed without gil" % self.gil_message)

    cpp_message = "Operation"

    def cpp_check(self, env):
        if not env.is_cpp():
            self.cpp_error()

    def cpp_error(self):
        error(self.pos, "%s only allowed in c++" % self.cpp_message)

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
        try:
            return self._end_pos
        except AttributeError:
            pos = self.pos
            if not self.child_attrs:
                self._end_pos = pos
                return pos
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
            return "<%s (0x%x) -- already output>" % (self.__class__.__name__, id(self))
        encountered.add(id(self))

        def dump_child(x, level):
            if isinstance(x, Node):
                return x.dump(level, filter_out, cutoff-1, encountered)
            elif isinstance(x, list):
                return "[%s]" % ", ".join([dump_child(item, level) for item in x])
            else:
                return repr(x)


        attrs = [(key, value) for key, value in self.__dict__.items() if key not in filter_out]
        if len(attrs) == 0:
            return "<%s (0x%x)>" % (self.__class__.__name__, id(self))
        else:
            indent = "  " * level
            res = "<%s (0x%x)\n" % (self.__class__.__name__, id(self))
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

class BlockNode(object):
    #  Mixin class for nodes representing a declaration block.

    def generate_cached_builtins_decls(self, env, code):
        entries = env.global_scope().undeclared_cached_builtins
        for entry in entries:
            code.globalstate.add_cached_builtin_decl(entry)
        del entries[:]

    def generate_lambda_definitions(self, env, code):
        for node in env.lambda_defs:
            node.generate_function_definitions(env, code)

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

class CReferenceDeclaratorNode(CDeclaratorNode):
    # base     CDeclaratorNode

    child_attrs = ["base"]

    def analyse(self, base_type, env, nonempty = 0):
        if base_type.is_pyobject:
            error(self.pos,
                  "Reference base type cannot be a Python object")
        ref_type = PyrexTypes.c_ref_type(base_type)
        return self.base.analyse(ref_type, env, nonempty = nonempty)

class CArrayDeclaratorNode(CDeclaratorNode):
    # base        CDeclaratorNode
    # dimension   ExprNode

    child_attrs = ["base", "dimension"]

    def analyse(self, base_type, env, nonempty = 0):
        if base_type.is_cpp_class:
            from ExprNodes import TupleNode
            if isinstance(self.dimension, TupleNode):
                args = self.dimension.args
            else:
                args = self.dimension,
            values = [v.analyse_as_type(env) for v in args]
            if None in values:
                ix = values.index(None)
                error(args[ix].pos, "Template parameter not a type.")
                return error_type
            base_type = base_type.specialize_here(self.pos, values)
            return self.base.analyse(base_type, env, nonempty = nonempty)
        if self.dimension:
            self.dimension.analyse_const_expression(env)
            if not self.dimension.type.is_int:
                error(self.dimension.pos, "Array dimension not integer")
            size = self.dimension.get_constant_c_result_code()
            if size is not None:
                try:
                    size = int(size)
                except ValueError:
                    # runtime constant?
                    pass
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

    def analyse(self, return_type, env, nonempty = 0, directive_locals = {}):
        if nonempty:
            nonempty -= 1
        func_type_args = []
        for i, arg_node in enumerate(self.args):
            name_declarator, type = arg_node.analyse(env, nonempty = nonempty,
                                                     is_self_arg = (i == 0 and env.is_c_class_scope))
            name = name_declarator.name
            if name in directive_locals:
                type_node = directive_locals[name]
                other_type = type_node.analyse_as_type(env)
                if other_type is None:
                    error(type_node.pos, "Not a type")
                elif (type is not PyrexTypes.py_object_type
                      and not type.same_as(other_type)):
                    error(self.base.pos, "Signature does not agree with previous declaration")
                    error(type_node.pos, "Previous declaration here")
                else:
                    type = other_type
            if name_declarator.cname:
                error(self.pos,
                    "Function argument cannot have C name specification")
            # Turn *[] argument into **
            if type.is_array:
                type = PyrexTypes.c_ptr_type(type.base_type)
            # Catch attempted C-style func(void) decl
            if type.is_void:
                error(arg_node.pos, "Use spam() rather than spam(void) to declare a function with no arguments.")
            func_type_args.append(
                PyrexTypes.CFuncTypeArg(name, type, arg_node.pos))
            if arg_node.default:
                self.optional_arg_count += 1
            elif self.optional_arg_count:
                error(self.pos, "Non-default argument follows default argument")

        if self.optional_arg_count:
            scope = StructOrUnionScope()
            arg_count_member = '%sn' % Naming.pyrex_prefix
            scope.declare_var(arg_count_member, PyrexTypes.c_int_type, self.pos)
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
        if self.exception_check == '+':
            env.add_include_file('stdexcept')
        if return_type.is_pyobject \
            and (self.exception_value or self.exception_check) \
            and self.exception_check != '+':
                error(self.pos,
                    "Exception clause not allowed for function returning Python object")
        else:
            if self.exception_value:
                self.exception_value.analyse_const_expression(env)
                if self.exception_check == '+':
                    self.exception_value.analyse_types(env)
                    exc_val_type = self.exception_value.type
                    if not exc_val_type.is_error and \
                          not exc_val_type.is_pyobject and \
                          not (exc_val_type.is_cfunction and not exc_val_type.return_type.is_pyobject and len(exc_val_type.args)==0):
                        error(self.exception_value.pos,
                            "Exception value must be a Python exception or cdef function with no arguments.")
                    exc_val = self.exception_value
                else:
                    self.exception_value = self.exception_value.coerce_to(return_type, env)
                    if self.exception_value.analyse_const_expression(env):
                        exc_val = self.exception_value.get_constant_c_result_code()
                        if exc_val is None:
                            raise InternalError("get_constant_c_result_code not implemented for %s" %
                                self.exception_value.__class__.__name__)
                        if not return_type.assignable_from(self.exception_value.type):
                            error(self.exception_value.pos,
                                  "Exception value incompatible with function return type")
            exc_check = self.exception_check
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
        callspec = env.directives['callspec']
        if callspec:
            current = func_type.calling_convention
            if current and current != callspec:
                error(self.pos, "cannot have both '%s' and '%s' "
                      "calling conventions" % (current, callspec))
            func_type.calling_convention = callspec
        return self.base.analyse(func_type, env)


class CArgDeclNode(Node):
    # Item in a function declaration argument list.
    #
    # base_type      CBaseTypeNode
    # declarator     CDeclaratorNode
    # not_none       boolean            Tagged with 'not None'
    # or_none        boolean            Tagged with 'or None'
    # accept_none    boolean            Resolved boolean for not_none/or_none
    # default        ExprNode or None
    # default_value  PyObjectConst      constant for default value
    # annotation     ExprNode or None   Py3 function arg annotation
    # is_self_arg    boolean            Is the "self" arg of an extension type method
    # is_type_arg    boolean            Is the "class" arg of an extension type classmethod
    # is_kw_only     boolean            Is a keyword-only argument

    child_attrs = ["base_type", "declarator", "default"]

    is_self_arg = 0
    is_type_arg = 0
    is_generic = 1
    kw_only = 0
    not_none = 0
    or_none = 0
    type = None
    name_declarator = None
    default_value = None
    annotation = None

    def analyse(self, env, nonempty = 0, is_self_arg = False):
        if is_self_arg:
            self.base_type.is_self_arg = self.is_self_arg = True
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
            # The parser is unable to resolve the ambiguity of [] as part of the
            # type (e.g. in buffers) or empty declarator (as with arrays).
            # This is only arises for empty multi-dimensional arrays.
            if (base_type.is_array
                    and isinstance(self.base_type, TemplatedTypeNode)
                    and isinstance(self.declarator, CArrayDeclaratorNode)):
                declarator = self.declarator
                while isinstance(declarator.base, CArrayDeclaratorNode):
                    declarator = declarator.base
                declarator.base = self.base_type.array_declarator
                base_type = base_type.base_type
            return self.declarator.analyse(base_type, env, nonempty = nonempty)
        else:
            return self.name_declarator, self.type

    def calculate_default_value_code(self, code):
        if self.default_value is None:
            if self.default:
                if self.default.is_literal:
                    # will not output any code, just assign the result_code
                    self.default.generate_evaluation_code(code)
                    return self.type.cast_code(self.default.result())
                self.default_value = code.get_argument_default_const(self.type)
        return self.default_value

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

    def analyse_as_type(self, env):
        return self.analyse(env)

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
    # complex          boolean
    # is_self_arg      boolean      Is self argument of C method
    # ##is_type_arg      boolean      Is type argument of class method

    child_attrs = []
    arg_name = None   # in case the argument name was interpreted as a type
    module_path = []
    is_basic_c_type = False
    complex = False

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
            ## elif self.is_type_arg and env.is_c_class_scope:
            ##     type = Builtin.type_type
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
                    ## elif self.is_type_arg and env.is_c_class_scope:
                    ##     type = Builtin.type_type
                    else:
                        type = py_object_type
                    self.arg_name = self.name
                else:
                    if self.templates:
                        if not self.name in self.templates:
                            error(self.pos, "'%s' is not a type identifier" % self.name)
                        type = PyrexTypes.TemplatePlaceholderType(self.name)
                    else:
                        error(self.pos, "'%s' is not a type identifier" % self.name)
        if self.complex:
            if not type.is_numeric or type.is_complex:
                error(self.pos, "can only complexify c numeric types")
            type = PyrexTypes.CComplexType(type)
            type.create_declaration_utility_code(env)
        elif type is Builtin.complex_type:
            # Special case: optimise builtin complex type into C's
            # double complex.  The parser cannot do this (as for the
            # normal scalar types) as the user may have redeclared the
            # 'complex' type.  Testing for the exact type here works.
            type = PyrexTypes.c_double_complex_type
            type.create_declaration_utility_code(env)
            self.complex = True
        if type:
            return type
        else:
            return PyrexTypes.error_type

class CNestedBaseTypeNode(CBaseTypeNode):
    # For C++ classes that live inside other C++ classes.

    # name             string
    # base_type        CBaseTypeNode

    child_attrs = ['base_type']

    def analyse(self, env, could_be_name = None):
        base_type = self.base_type.analyse(env)
        if base_type is PyrexTypes.error_type:
            return PyrexTypes.error_type
        if not base_type.is_cpp_class:
            error(self.pos, "'%s' is not a valid type scope" % base_type)
            return PyrexTypes.error_type
        type_entry = base_type.scope.lookup_here(self.name)
        if not type_entry or not type_entry.is_type:
            error(self.pos, "'%s.%s' is not a type identifier" % (base_type, self.name))
            return PyrexTypes.error_type
        return type_entry.type

class TemplatedTypeNode(CBaseTypeNode):
    #  After parsing:
    #  positional_args  [ExprNode]        List of positional arguments
    #  keyword_args     DictNode          Keyword arguments
    #  base_type_node   CBaseTypeNode

    #  After analysis:
    #  type             PyrexTypes.BufferType or PyrexTypes.CppClassType  ...containing the right options


    child_attrs = ["base_type_node", "positional_args",
                   "keyword_args", "dtype_node"]

    dtype_node = None

    name = None

    def analyse(self, env, could_be_name = False, base_type = None):
        if base_type is None:
            base_type = self.base_type_node.analyse(env)
        if base_type.is_error: return base_type

        if base_type.is_cpp_class:
            # Templated class
            if self.keyword_args and self.keyword_args.key_value_pairs:
                error(self.pos, "c++ templates cannot take keyword arguments");
                self.type = PyrexTypes.error_type
            else:
                template_types = []
                for template_node in self.positional_args:
                    type = template_node.analyse_as_type(env)
                    if type is None:
                        error(template_node.pos, "unknown type in template argument")
                        return error_type
                    template_types.append(type)
                self.type = base_type.specialize_here(self.pos, template_types)

        elif base_type.is_pyobject:
            # Buffer
            import Buffer

            options = Buffer.analyse_buffer_options(
                self.pos,
                env,
                self.positional_args,
                self.keyword_args,
                base_type.buffer_defaults)

            if sys.version_info[0] < 3:
                # Py 2.x enforces byte strings as keyword arguments ...
                options = dict([ (name.encode('ASCII'), value)
                                 for name, value in options.items() ])

            self.type = PyrexTypes.BufferType(base_type, **options)

        else:
            # Array
            empty_declarator = CNameDeclaratorNode(self.pos, name="", cname=None)
            if len(self.positional_args) > 1 or self.keyword_args.key_value_pairs:
                error(self.pos, "invalid array declaration")
                self.type = PyrexTypes.error_type
            else:
                # It would be nice to merge this class with CArrayDeclaratorNode,
                # but arrays are part of the declaration, not the type...
                if not self.positional_args:
                    dimension = None
                else:
                    dimension = self.positional_args[0]
                self.array_declarator = CArrayDeclaratorNode(self.pos,
                    base = empty_declarator,
                    dimension = dimension)
                self.type = self.array_declarator.analyse(base_type, env)[1]

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

    #  decorators    [cython.locals(...)] or None
    #  directive_locals { string : NameNode } locals defined by cython.locals(...)

    child_attrs = ["base_type", "declarators"]

    decorators = None
    directive_locals = None

    def analyse_declarations(self, env, dest_scope = None):
        if self.directive_locals is None:
            self.directive_locals = {}
        if not dest_scope:
            dest_scope = env
        self.dest_scope = dest_scope
        base_type = self.base_type.analyse(env)

        # If the field is an external typedef, we cannot be sure about the type,
        # so do conversion ourself rather than rely on the CPython mechanism (through
        # a property; made in AnalyseDeclarationsTransform).
        if (dest_scope.is_c_class_scope
            and self.visibility in ('public', 'readonly')):
            need_property = True
        else:
            need_property = False
        visibility = self.visibility

        for declarator in self.declarators:
            if isinstance(declarator, CFuncDeclaratorNode):
                name_declarator, type = declarator.analyse(base_type, env, directive_locals=self.directive_locals)
            else:
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
                if entry is not None:
                    entry.directive_locals = copy.copy(self.directive_locals)
            else:
                if self.directive_locals:
                    error(self.pos, "Decorators can only be followed by functions")
                if self.in_pxd and self.visibility != 'extern':
                    error(self.pos,
                        "Only 'extern' C variable declaration allowed in .pxd file")
                entry = dest_scope.declare_var(name, type, declarator.pos,
                            cname=cname, visibility=visibility, api=self.api, is_cdef=1)
                entry.needs_property = need_property


class CStructOrUnionDefNode(StatNode):
    #  name          string
    #  cname         string or None
    #  kind          "struct" or "union"
    #  typedef_flag  boolean
    #  visibility    "public" or "private"
    #  api           boolean
    #  in_pxd        boolean
    #  attributes    [CVarDefNode] or None
    #  entry         Entry
    #  packed        boolean

    child_attrs = ["attributes"]

    def analyse_declarations(self, env):
        scope = None
        if self.visibility == 'extern' and self.packed:
            error(self.pos, "Cannot declare extern struct as 'packed'")
        if self.attributes is not None:
            scope = StructOrUnionScope(self.name)
        self.entry = env.declare_struct_or_union(
            self.name, self.kind, scope, self.typedef_flag, self.pos,
            self.cname, visibility = self.visibility, api = self.api,
            packed = self.packed)
        if self.attributes is not None:
            if self.in_pxd and not env.in_cinclude:
                self.entry.defined_in_pxd = 1
            for attr in self.attributes:
                attr.analyse_declarations(env, scope)
            if self.visibility != 'extern':
                need_typedef_indirection = False
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
                    self.entry = env.declare_typedef(
                        self.name, struct_entry.type, self.pos,
                        cname = self.cname, visibility='ignore')
                    struct_entry.type.typedef_flag = False
                    # FIXME: this might be considered a hack ;-)
                    struct_entry.cname = struct_entry.type.cname = \
                                         '_' + self.entry.type.typedef_cname

    def analyse_expressions(self, env):
        pass

    def generate_execution_code(self, code):
        pass


class CppClassNode(CStructOrUnionDefNode):

    #  name          string
    #  cname         string or None
    #  visibility    "extern"
    #  in_pxd        boolean
    #  attributes    [CVarDefNode] or None
    #  entry         Entry
    #  base_classes  [string]
    #  templates     [string] or None

    def analyse_declarations(self, env):
        scope = None
        if self.attributes is not None:
            scope = CppClassScope(self.name, env)
        base_class_types = []
        for base_class_name in self.base_classes:
            base_class_entry = env.lookup(base_class_name)
            if base_class_entry is None:
                error(self.pos, "'%s' not found" % base_class_name)
            elif not base_class_entry.is_type or not base_class_entry.type.is_cpp_class:
                error(self.pos, "'%s' is not a cpp class type" % base_class_name)
            else:
                base_class_types.append(base_class_entry.type)
        if self.templates is None:
            template_types = None
        else:
            template_types = [PyrexTypes.TemplatePlaceholderType(template_name) for template_name in self.templates]
        self.entry = env.declare_cpp_class(
            self.name, scope, self.pos,
            self.cname, base_class_types, visibility = self.visibility, templates = template_types)
        if self.entry is None:
            return
        self.entry.is_cpp_class = 1
        if self.attributes is not None:
            if self.in_pxd and not env.in_cinclude:
                self.entry.defined_in_pxd = 1
            for attr in self.attributes:
                attr.analyse_declarations(scope)

class CEnumDefNode(StatNode):
    #  name           string or None
    #  cname          string or None
    #  items          [CEnumDefItemNode]
    #  typedef_flag   boolean
    #  visibility     "public" or "private"
    #  api            boolean
    #  in_pxd         boolean
    #  entry          Entry

    child_attrs = ["items"]

    def analyse_declarations(self, env):
        self.entry = env.declare_enum(self.name, self.pos,
            cname = self.cname, typedef_flag = self.typedef_flag,
            visibility = self.visibility, api = self.api)
        if self.items is not None:
            if self.in_pxd and not env.in_cinclude:
                self.entry.defined_in_pxd = 1
            for item in self.items:
                item.analyse_declarations(env, self.entry)

    def analyse_expressions(self, env):
        pass

    def generate_execution_code(self, code):
        if self.visibility == 'public' or self.api:
            temp = code.funcstate.allocate_temp(PyrexTypes.py_object_type, manage_ref=True)
            for item in self.entry.enum_values:
                code.putln("%s = PyInt_FromLong(%s); %s" % (
                        temp,
                        item.cname,
                        code.error_goto_if_null(temp, item.pos)))
                code.put_gotref(temp)
                code.putln('if (__Pyx_SetAttrString(%s, "%s", %s) < 0) %s' % (
                        Naming.module_cname,
                        item.name,
                        temp,
                        code.error_goto(item.pos)))
                code.put_decref_clear(temp, PyrexTypes.py_object_type)
            code.funcstate.release_temp(temp)


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
        entry = env.declare_const(self.name, enum_entry.type,
            self.value, self.pos, cname = self.cname,
            visibility = enum_entry.visibility, api = enum_entry.api)
        enum_entry.enum_values.append(entry)


class CTypeDefNode(StatNode):
    #  base_type    CBaseTypeNode
    #  declarator   CDeclaratorNode
    #  visibility   "public" or "private"
    #  api          boolean
    #  in_pxd       boolean

    child_attrs = ["base_type", "declarator"]

    def analyse_declarations(self, env):
        base = self.base_type.analyse(env)
        name_declarator, type = self.declarator.analyse(base, env)
        name = name_declarator.name
        cname = name_declarator.cname
        entry = env.declare_typedef(name, type, self.pos,
            cname = cname, visibility = self.visibility, api = self.api)
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
    #  needs_outer_scope boolean      Whether or not this function requires outer scope
    #  directive_locals { string : NameNode } locals defined by cython.locals(...)

    py_func = None
    assmt = None
    needs_closure = False
    needs_outer_scope = False
    is_generator = False
    is_generator_body = False
    modifiers = []

    def analyse_default_values(self, env):
        genv = env.global_scope()
        default_seen = 0
        for arg in self.args:
            if arg.default:
                default_seen = 1
                if arg.is_generic:
                    arg.default.analyse_types(env)
                    arg.default = arg.default.coerce_to(arg.type, genv)
                else:
                    error(arg.pos,
                        "This argument cannot have a default value")
                    arg.default = None
            elif arg.kw_only:
                default_seen = 1
            elif default_seen:
                error(arg.pos, "Non-default argument following default argument")

    def align_argument_type(self, env, arg):
        directive_locals = self.directive_locals
        type = arg.type
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
                arg.type = other_type
        return arg

    def need_gil_acquisition(self, lenv):
        return 0

    def create_local_scope(self, env):
        genv = env
        while genv.is_py_class_scope or genv.is_c_class_scope:
            genv = genv.outer_scope
        if self.needs_closure:
            lenv = ClosureScope(name=self.entry.name,
                                outer_scope = genv,
                                scope_name=self.entry.cname)
        else:
            lenv = LocalScope(name=self.entry.name,
                              outer_scope=genv,
                              parent_scope=env)
        lenv.return_type = self.return_type
        type = self.entry.type
        if type.is_cfunction:
            lenv.nogil = type.nogil and not type.with_gil
        self.local_scope = lenv
        lenv.directives = env.directives
        return lenv

    def generate_function_body(self, env, code):
        self.body.generate_execution_code(code)

    def generate_function_definitions(self, env, code):
        import Buffer

        lenv = self.local_scope
        if lenv.is_closure_scope and not lenv.is_passthrough:
            outer_scope_cname = "%s->%s" % (Naming.cur_scope_cname,
                                            Naming.outer_scope_cname)
        else:
            outer_scope_cname = Naming.outer_scope_cname
        lenv.mangle_closure_cnames(outer_scope_cname)
        # Generate closure function definitions
        self.body.generate_function_definitions(lenv, code)
        # generate lambda function definitions
        self.generate_lambda_definitions(lenv, code)

        is_getbuffer_slot = (self.entry.name == "__getbuffer__" and
                             self.entry.scope.is_c_class_scope)
        is_releasebuffer_slot = (self.entry.name == "__releasebuffer__" and
                                 self.entry.scope.is_c_class_scope)
        is_buffer_slot = is_getbuffer_slot or is_releasebuffer_slot
        if is_buffer_slot:
            if 'cython_unused' not in self.modifiers:
                self.modifiers = self.modifiers + ['cython_unused']

        preprocessor_guard = None
        if self.entry.is_special and not is_buffer_slot:
            slot = TypeSlots.method_name_to_slot.get(self.entry.name)
            if slot:
                preprocessor_guard = slot.preprocessor_guard_code()
                if (self.entry.name == '__long__' and
                    not self.entry.scope.lookup_here('__int__')):
                    preprocessor_guard = None

        profile = code.globalstate.directives['profile']
        if profile and lenv.nogil:
            warning(self.pos, "Cannot profile nogil function.", 1)
            profile = False
        if profile:
            code.globalstate.use_utility_code(profile_utility_code)

        # Generate C code for header and body of function
        code.enter_cfunc_scope()
        code.return_from_error_cleanup_label = code.new_label()

        # ----- Top-level constants used by this function
        code.mark_pos(self.pos)
        self.generate_cached_builtins_decls(lenv, code)
        # ----- Function header
        code.putln("")

        if preprocessor_guard:
            code.putln(preprocessor_guard)

        with_pymethdef = self.needs_assignment_synthesis(env, code)
        if self.py_func:
            self.py_func.generate_function_header(code,
                with_pymethdef = with_pymethdef,
                proto_only=True)
        self.generate_function_header(code,
            with_pymethdef = with_pymethdef)
        # ----- Local variable declarations
        # Find function scope
        cenv = env
        while cenv.is_py_class_scope or cenv.is_c_class_scope:
            cenv = cenv.outer_scope
        if self.needs_closure:
            code.put(lenv.scope_class.type.declaration_code(Naming.cur_scope_cname))
            code.putln(";")
        elif self.needs_outer_scope:
            if lenv.is_passthrough:
                code.put(lenv.scope_class.type.declaration_code(Naming.cur_scope_cname))
                code.putln(";")
            code.put(cenv.scope_class.type.declaration_code(Naming.outer_scope_cname))
            code.putln(";")
        self.generate_argument_declarations(lenv, code)
        for entry in lenv.var_entries:
            if not entry.in_closure:
                code.put_var_declaration(entry)
        init = ""
        if not self.return_type.is_void:
            if self.return_type.is_pyobject:
                init = " = NULL"
            code.putln(
                "%s%s;" %
                    (self.return_type.declaration_code(Naming.retval_cname),
                     init))
        tempvardecl_code = code.insertion_point()
        if not lenv.nogil:
            code.put_declare_refcount_context()
        self.generate_keyword_list(code)
        if profile:
            code.put_trace_declarations()
        # ----- Extern library function declarations
        lenv.generate_library_function_declarations(code)
        # ----- GIL acquisition
        acquire_gil = self.acquire_gil
        if acquire_gil:
            env.use_utility_code(force_init_threads_utility_code)
            code.putln("#ifdef WITH_THREAD")
            code.putln("PyGILState_STATE _save = PyGILState_Ensure();")
            code.putln("#endif")
        # ----- set up refnanny
        if not lenv.nogil:
            code.put_setup_refcount_context(self.entry.name)
        # ----- Automatic lead-ins for certain special functions
        if is_getbuffer_slot:
            self.getbuffer_init(code)
        # ----- Create closure scope object
        if self.needs_closure:
            code.putln("%s = (%s)%s->tp_new(%s, %s, NULL);" % (
                Naming.cur_scope_cname,
                lenv.scope_class.type.declaration_code(''),
                lenv.scope_class.type.typeptr_cname,
                lenv.scope_class.type.typeptr_cname,
                Naming.empty_tuple))
            code.putln("if (unlikely(!%s)) {" % Naming.cur_scope_cname)
            if is_getbuffer_slot:
                self.getbuffer_error_cleanup(code)
            if not lenv.nogil:
                code.put_finish_refcount_context()
            # FIXME: what if the error return value is a Python value?
            code.putln("return %s;" % self.error_value())
            code.putln("}")
            code.put_gotref(Naming.cur_scope_cname)
            # Note that it is unsafe to decref the scope at this point.
        if self.needs_outer_scope:
            code.putln("%s = (%s)%s;" % (
                            outer_scope_cname,
                            cenv.scope_class.type.declaration_code(''),
                            Naming.self_cname))
            if lenv.is_passthrough:
                code.putln("%s = %s;" % (Naming.cur_scope_cname, outer_scope_cname));
            elif self.needs_closure:
                # inner closures own a reference to their outer parent
                code.put_incref(outer_scope_cname, cenv.scope_class.type)
                code.put_giveref(outer_scope_cname)
        # ----- Trace function call
        if profile:
            # this looks a bit late, but if we don't get here due to a
            # fatal error before hand, it's not really worth tracing
            code.put_trace_call(self.entry.name, self.pos)
        # ----- Fetch arguments
        self.generate_argument_parsing_code(env, code)
        # If an argument is assigned to in the body, we must
        # incref it to properly keep track of refcounts.
        for entry in lenv.arg_entries:
            if entry.type.is_pyobject:
                if (acquire_gil or entry.assignments) and not entry.in_closure:
                    code.put_var_incref(entry)
        # ----- Initialise local variables
        for entry in lenv.var_entries:
            if entry.type.is_pyobject and entry.init_to_none and entry.used:
                code.put_init_var_to_py_none(entry)
        # ----- Initialise local buffer auxiliary variables
        for entry in lenv.var_entries + lenv.arg_entries:
            if entry.type.is_buffer and entry.buffer_aux.buffer_info_var.used:
                code.putln("%s.buf = NULL;" %
                           entry.buffer_aux.buffer_info_var.cname)
        # ----- Check and convert arguments
        self.generate_argument_type_tests(code)
        # ----- Acquire buffer arguments
        for entry in lenv.arg_entries:
            if entry.type.is_buffer:
                Buffer.put_acquire_arg_buffer(entry, code, self.pos)

        # -------------------------
        # ----- Function body -----
        # -------------------------
        self.generate_function_body(env, code)

        # ----- Default return value
        code.putln("")
        if self.return_type.is_pyobject:
            #if self.return_type.is_extension_type:
            #    lhs = "(PyObject *)%s" % Naming.retval_cname
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
            for cname, type in code.funcstate.all_managed_temps():
                code.put_xdecref(cname, type)

            # Clean up buffers -- this calls a Python function
            # so need to save and restore error state
            buffers_present = len(lenv.buffer_entries) > 0
            if buffers_present:
                code.globalstate.use_utility_code(restore_exception_utility_code)
                code.putln("{ PyObject *__pyx_type, *__pyx_value, *__pyx_tb;")
                code.putln("__Pyx_ErrFetch(&__pyx_type, &__pyx_value, &__pyx_tb);")
                for entry in lenv.buffer_entries:
                    Buffer.put_release_buffer_code(code, entry)
                    #code.putln("%s = 0;" % entry.cname)
                code.putln("__Pyx_ErrRestore(__pyx_type, __pyx_value, __pyx_tb);}")

            err_val = self.error_value()
            exc_check = self.caller_will_check_exceptions()
            if err_val is not None or exc_check:
                # TODO: Fix exception tracing (though currently unused by cProfile).
                # code.globalstate.use_utility_code(get_exception_tuple_utility_code)
                # code.put_trace_exception()
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
                code.putln("%s = %s;" % (Naming.retval_cname, err_val))

            if is_getbuffer_slot:
                self.getbuffer_error_cleanup(code)

            # If we are using the non-error cleanup section we should
            # jump past it if we have an error. The if-test below determine
            # whether this section is used.
            if buffers_present or is_getbuffer_slot:
                code.put_goto(code.return_from_error_cleanup_label)


        # ----- Non-error return cleanup
        code.put_label(code.return_label)
        for entry in lenv.buffer_entries:
            if entry.used:
                Buffer.put_release_buffer_code(code, entry)
        if is_getbuffer_slot:
            self.getbuffer_normal_cleanup(code)
        # ----- Return cleanup for both error and no-error return
        code.put_label(code.return_from_error_cleanup_label)
        if not Options.init_local_none:
            for entry in lenv.var_entries:
                if lenv.control_flow.get_state((entry.name, 'initialized')) is not True:
                    entry.xdecref_cleanup = 1

        for entry in lenv.var_entries:
            if entry.type.is_pyobject:
                if entry.used and not entry.in_closure:
                    code.put_var_decref(entry)
        # Decref any increfed args
        for entry in lenv.arg_entries:
            if entry.type.is_pyobject:
                if (acquire_gil or entry.assignments) and not entry.in_closure:
                    code.put_var_decref(entry)
        if self.needs_closure:
            code.put_decref(Naming.cur_scope_cname, lenv.scope_class.type)

        # ----- Return
        # This code is duplicated in ModuleNode.generate_module_init_func
        if not lenv.nogil:
            default_retval = self.return_type.default_value
            err_val = self.error_value()
            if err_val is None and default_retval:
                err_val = default_retval
            if self.return_type.is_pyobject:
                code.put_xgiveref(self.return_type.as_pyobject(Naming.retval_cname))

        if self.entry.is_special and self.entry.name == "__hash__":
            # Returning -1 for __hash__ is supposed to signal an error
            # We do as Python instances and coerce -1 into -2.
            code.putln("if (unlikely(%s == -1) && !PyErr_Occurred()) %s = -2;" % (
                    Naming.retval_cname, Naming.retval_cname))

        if profile:
            if self.return_type.is_pyobject:
                code.put_trace_return(Naming.retval_cname)
            else:
                code.put_trace_return("Py_None")
        if not lenv.nogil:
            code.put_finish_refcount_context()

        if acquire_gil:
            code.putln("#ifdef WITH_THREAD")
            code.putln("PyGILState_Release(_save);")
            code.putln("#endif")

        if not self.return_type.is_void:
            code.putln("return %s;" % Naming.retval_cname)

        code.putln("}")

        if preprocessor_guard:
            code.putln("#endif /*!(%s)*/" % preprocessor_guard)

        # ----- Go back and insert temp variable declarations
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

    def generate_arg_type_test(self, arg, code):
        # Generate type test for one argument.
        if arg.type.typeobj_is_available():
            code.globalstate.use_utility_code(arg_type_test_utility_code)
            typeptr_cname = arg.type.typeptr_cname
            arg_code = "((PyObject *)%s)" % arg.entry.cname
            code.putln(
                'if (unlikely(!__Pyx_ArgTypeTest(%s, %s, %d, "%s", %s))) %s' % (
                    arg_code,
                    typeptr_cname,
                    arg.accept_none,
                    arg.name,
                    arg.type.is_builtin_type,
                    code.error_goto(arg.pos)))
        else:
            error(arg.pos, "Cannot test type of extern C class "
                "without type object name specification")

    def generate_arg_none_check(self, arg, code):
        # Generate None check for one argument.
        code.putln('if (unlikely(((PyObject *)%s) == Py_None)) {' % arg.entry.cname)
        code.putln('''PyErr_Format(PyExc_TypeError, "Argument '%s' must not be None"); %s''' % (
            arg.name,
            code.error_goto(arg.pos)))
        code.putln('}')

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
                    result = default.result_as(arg.type)
                    code.putln(
                        "%s = %s;" % (
                            arg.calculate_default_value_code(code),
                            result))
                    if arg.type.is_pyobject:
                        code.put_giveref(default.result())
                    default.generate_post_assignment_code(code)
                    default.free_temps(code)
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
        # the following block should be removed when this bug is fixed.
        code.putln("if (%s != NULL) {" % info)
        code.putln("%s->obj = Py_None; __Pyx_INCREF(Py_None);" % info)
        code.put_giveref("%s->obj" % info) # Do not refnanny object within structs
        code.putln("}")

    def getbuffer_error_cleanup(self, code):
        info = self.local_scope.arg_entries[1].cname
        code.putln("if (%s != NULL && %s->obj != NULL) {"
                   % (info, info))
        code.put_gotref("%s->obj" % info)
        code.putln("__Pyx_DECREF(%s->obj); %s->obj = NULL;"
                   % (info, info))
        code.putln("}")

    def getbuffer_normal_cleanup(self, code):
        info = self.local_scope.arg_entries[1].cname
        code.putln("if (%s != NULL && %s->obj == Py_None) {" % (info, info))
        code.put_gotref("Py_None")
        code.putln("__Pyx_DECREF(Py_None); %s->obj = NULL;" % info)
        code.putln("}")

class CFuncDefNode(FuncDefNode):
    #  C function definition.
    #
    #  modifiers     ['inline']
    #  visibility    'private' or 'public' or 'extern'
    #  base_type     CBaseTypeNode
    #  declarator    CDeclaratorNode
    #  body          StatListNode
    #  api           boolean
    #  decorators    [DecoratorNode]        list of decorators
    #
    #  with_gil      boolean    Acquire GIL around body
    #  type          CFuncType
    #  py_func       wrapper for calling from Python
    #  overridable   whether or not this is a cpdef function
    #  inline_in_pxd whether this is an inline function in a pxd file

    child_attrs = ["base_type", "declarator", "body", "py_func"]

    inline_in_pxd = False
    decorators = None
    directive_locals = None

    def unqualified_name(self):
        return self.entry.name

    def analyse_declarations(self, env):
        if self.directive_locals is None:
            self.directive_locals = {}
        self.directive_locals.update(env.directives['locals'])
        base_type = self.base_type.analyse(env)
        # The 2 here is because we need both function and argument names.
        if isinstance(self.declarator, CFuncDeclaratorNode):
            name_declarator, type = self.declarator.analyse(base_type, env,
                                                            nonempty = 2 * (self.body is not None),
                                                            directive_locals = self.directive_locals)
        else:
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
            self.align_argument_type(env, type_arg)
            formal_arg.type = type_arg.type
            formal_arg.name = type_arg.name
            formal_arg.cname = type_arg.cname
            if type_arg.type.is_buffer and 'inline' in self.modifiers:
                warning(formal_arg.pos, "Buffer unpacking not optimized away.", 1)
        name = name_declarator.name
        cname = name_declarator.cname
        self.entry = env.declare_cfunction(
            name, type, self.pos,
            cname = cname, visibility = self.visibility,
            defining = self.body is not None,
            api = self.api, modifiers = self.modifiers)
        self.entry.inline_func_in_pxd = self.inline_in_pxd
        self.return_type = type.return_type
        if self.return_type.is_array and visibility != 'extern':
            error(self.pos,
                "Function cannot return an array")

        if self.overridable and not env.is_module_scope:
            if len(self.args) < 1 or not self.args[0].type.is_pyobject:
                # An error will be produced in the cdef function
                self.overridable = False

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
            if not env.is_module_scope or Options.lookup_module_cpdef:
                self.override = OverrideCheckNode(self.pos, py_func = self.py_func)
                self.body = StatListNode(self.pos, stats=[self.override, self.body])
        self.create_local_scope(env)

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
        return self.type.with_gil

    def nogil_check(self, env):
        type = self.type
        with_gil = type.with_gil
        if type.nogil and not with_gil:
            if type.return_type.is_pyobject:
                error(self.pos,
                      "Function with Python return type cannot be declared nogil")
            for entry in self.local_scope.var_entries:
                if entry.type.is_pyobject:
                    error(self.pos, "Function declared nogil has Python locals or temporaries")

    def analyse_expressions(self, env):
        self.local_scope.directives = env.directives
        if self.py_func is not None:
            # this will also analyse the default values
            self.py_func.analyse_expressions(env)
        else:
            self.analyse_default_values(env)
        self.acquire_gil = self.need_gil_acquisition(self.local_scope)

    def needs_assignment_synthesis(self, env, code=None):
        return False

    def generate_function_header(self, code, with_pymethdef, with_opt_args = 1, with_dispatch = 1, cname = None):
        arg_decls = []
        type = self.type
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
        entity = type.function_header_code(cname, ', '.join(arg_decls))
        if self.entry.visibility == 'private':
            storage_class = "static "
        else:
            storage_class = ""
        dll_linkage = None
        modifiers = ""
        if 'inline' in self.modifiers:
            self.modifiers[self.modifiers.index('inline')] = 'cython_inline'
        if self.modifiers:
            modifiers = "%s " % ' '.join(self.modifiers).upper()

        header = self.return_type.declaration_code(entity, dll_linkage=dll_linkage)
        #print (storage_class, modifiers, header)
        code.putln("%s%s%s {" % (storage_class, modifiers, header))

    def generate_argument_declarations(self, env, code):
        for arg in self.args:
            if arg.default:
                result = arg.calculate_default_value_code(code)
                code.putln('%s = %s;' % (
                    arg.type.declaration_code(arg.cname), result))

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
                    code.putln('%s = %s->%s;' % (arg.cname, Naming.optional_args_cname, self.type.opt_arg_cname(declarator.name)))
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
            elif arg.type.is_pyobject and not arg.accept_none:
                self.generate_arg_none_check(arg, code)

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
    # name        string
    # entry       Symtab.Entry
    # annotation  ExprNode or None   Py3 argument annotation
    child_attrs = []

    def generate_function_definitions(self, env, code):
        self.entry.generate_function_definitions(env, code)

class DecoratorNode(Node):
    # A decorator
    #
    # decorator    NameNode or CallNode or AttributeNode
    child_attrs = ['decorator']


class DefNode(FuncDefNode):
    # A Python function definition.
    #
    # name          string                 the Python name of the function
    # lambda_name   string                 the internal name of a lambda 'function'
    # decorators    [DecoratorNode]        list of decorators
    # args          [CArgDeclNode]         formal arguments
    # star_arg      PyArgDeclNode or None  * argument
    # starstar_arg  PyArgDeclNode or None  ** argument
    # doc           EncodedString or None
    # body          StatListNode
    # return_type_annotation
    #               ExprNode or None       the Py3 return type annotation
    #
    #  The following subnode is constructed internally
    #  when the def statement is inside a Python class definition.
    #
    #  assmt   AssignmentNode   Function construction/assignment

    child_attrs = ["args", "star_arg", "starstar_arg", "body", "decorators"]

    lambda_name = None
    assmt = None
    num_kwonly_args = 0
    num_required_kw_args = 0
    reqd_kw_flags_cname = "0"
    is_wrapper = 0
    no_assignment_synthesis = 0
    decorators = None
    return_type_annotation = None
    entry = None
    acquire_gil = 0
    self_in_stararg = 0
    star_arg = None
    starstar_arg = None
    doc = None

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

    def as_cfunction(self, cfunc=None, scope=None):
        if self.star_arg:
            error(self.star_arg.pos, "cdef function cannot have star argument")
        if self.starstar_arg:
            error(self.starstar_arg.pos, "cdef function cannot have starstar argument")
        if cfunc is None:
            cfunc_args = []
            for formal_arg in self.args:
                name_declarator, type = formal_arg.analyse(scope, nonempty=1)
                cfunc_args.append(PyrexTypes.CFuncTypeArg(name = name_declarator.name,
                                                          cname = None,
                                                          type = py_object_type,
                                                          pos = formal_arg.pos))
            cfunc_type = PyrexTypes.CFuncType(return_type = py_object_type,
                                              args = cfunc_args,
                                              has_varargs = False,
                                              exception_value = None,
                                              exception_check = False,
                                              nogil = False,
                                              with_gil = False,
                                              is_overridable = True)
            cfunc = CVarDefNode(self.pos, type=cfunc_type)
        else:
            if scope is None:
                scope = cfunc.scope
            cfunc_type = cfunc.type
            if len(self.args) != len(cfunc_type.args) or cfunc_type.has_varargs:
                error(self.pos, "wrong number of arguments")
                error(cfunc.pos, "previous declaration here")
            for i, (formal_arg, type_arg) in enumerate(zip(self.args, cfunc_type.args)):
                name_declarator, type = formal_arg.analyse(scope, nonempty=1,
                                                           is_self_arg = (i == 0 and scope.is_c_class_scope))
                if type is None or type is PyrexTypes.py_object_type:
                    formal_arg.type = type_arg.type
                    formal_arg.name_declarator = name_declarator
        import ExprNodes
        if cfunc_type.exception_value is None:
            exception_value = None
        else:
            exception_value = ExprNodes.ConstNode(self.pos, value=cfunc_type.exception_value, type=cfunc_type.return_type)
        declarator = CFuncDeclaratorNode(self.pos,
                                         base = CNameDeclaratorNode(self.pos, name=self.name, cname=None),
                                         args = self.args,
                                         has_varargs = False,
                                         exception_check = cfunc_type.exception_check,
                                         exception_value = exception_value,
                                         with_gil = cfunc_type.with_gil,
                                         nogil = cfunc_type.nogil)
        return CFuncDefNode(self.pos,
                            modifiers = [],
                            base_type = CAnalysedBaseTypeNode(self.pos, type=cfunc_type.return_type),
                            declarator = declarator,
                            body = self.body,
                            doc = self.doc,
                            overridable = cfunc_type.is_overridable,
                            type = cfunc_type,
                            with_gil = cfunc_type.with_gil,
                            nogil = cfunc_type.nogil,
                            visibility = 'private',
                            api = False,
                            directive_locals = getattr(cfunc, 'directive_locals', {}))

    def is_cdef_func_compatible(self):
        """Determines if the function's signature is compatible with a
        cdef function.  This can be used before calling
        .as_cfunction() to see if that will be successful.
        """
        if self.needs_closure:
            return False
        if self.star_arg or self.starstar_arg:
            return False
        return True

    def analyse_declarations(self, env):
        self.is_classmethod = self.is_staticmethod = False
        if self.decorators:
            for decorator in self.decorators:
                func = decorator.decorator
                if func.is_name:
                    self.is_classmethod |= func.name == 'classmethod'
                    self.is_staticmethod |= func.name == 'staticmethod'

        if self.is_classmethod and env.lookup_here('classmethod'):
            # classmethod() was overridden - not much we can do here ...
            self.is_classmethod = False
        if self.is_staticmethod and env.lookup_here('staticmethod'):
            # staticmethod() was overridden - not much we can do here ...
            self.is_staticmethod = False

        if self.name == '__new__' and env.is_py_class_scope:
            self.is_staticmethod = 1

        self.analyse_argument_types(env)
        if self.name == '<lambda>':
            self.declare_lambda_function(env)
        else:
            self.declare_pyfunction(env)
        self.analyse_signature(env)
        self.return_type = self.entry.signature.return_type()
        self.create_local_scope(env)

    def analyse_argument_types(self, env):
        directive_locals = self.directive_locals = env.directives['locals']
        allow_none_for_extension_args = env.directives['allow_none_for_extension_args']
        for arg in self.args:
            if hasattr(arg, 'name'):
                name_declarator = None
            else:
                base_type = arg.base_type.analyse(env)
                name_declarator, type = \
                    arg.declarator.analyse(base_type, env)
                arg.name = name_declarator.name
                arg.type = type
            self.align_argument_type(env, arg)
            if name_declarator and name_declarator.cname:
                error(self.pos,
                    "Python function argument cannot have C name specification")
            arg.type = arg.type.as_argument_type()
            arg.hdr_type = None
            arg.needs_conversion = 0
            arg.needs_type_test = 0
            arg.is_generic = 1
            if arg.type.is_pyobject:
                if arg.or_none:
                    arg.accept_none = True
                elif arg.not_none:
                    arg.accept_none = False
                elif arg.type.is_extension_type or arg.type.is_builtin_type:
                    if arg.default and arg.default.constant_result is None:
                        # special case: def func(MyType obj = None)
                        arg.accept_none = True
                    else:
                        # default depends on compiler directive
                        arg.accept_none = allow_none_for_extension_args
                else:
                    # probably just a plain 'object'
                    arg.accept_none = True
            else:
                arg.accept_none = True # won't be used, but must be there
                if arg.not_none:
                    error(arg.pos, "Only Python type arguments can have 'not None'")
                if arg.or_none:
                    error(arg.pos, "Only Python type arguments can have 'or None'")

    def analyse_signature(self, env):
        if self.entry.is_special:
            if self.decorators:
                error(self.pos, "special functions of cdef classes cannot have decorators")
            self.entry.trivial_signature = len(self.args) == 1 and not (self.star_arg or self.starstar_arg)
        elif not env.directives['always_allow_keywords'] and not (self.star_arg or self.starstar_arg):
            # Use the simpler calling signature for zero- and one-argument functions.
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

        sig = self.entry.signature
        nfixed = sig.num_fixed_args()
        if sig is TypeSlots.pymethod_signature and nfixed == 1 \
               and len(self.args) == 0 and self.star_arg:
            # this is the only case where a diverging number of
            # arguments is not an error - when we have no explicit
            # 'self' parameter as in method(*args)
            sig = self.entry.signature = TypeSlots.pyfunction_signature # self is not 'really' used
            self.self_in_stararg = 1
            nfixed = 0

        for i in range(min(nfixed, len(self.args))):
            arg = self.args[i]
            arg.is_generic = 0
            if sig.is_self_arg(i) and not self.is_staticmethod:
                if self.is_classmethod:
                    arg.is_type_arg = 1
                    arg.hdr_type = arg.type = Builtin.type_type
                else:
                    arg.is_self_arg = 1
                    arg.hdr_type = arg.type = env.parent_type
                arg.needs_conversion = 0
            else:
                arg.hdr_type = sig.fixed_arg_type(i)
                if not arg.type.same_as(arg.hdr_type):
                    if arg.hdr_type.is_pyobject and arg.type.is_pyobject:
                        arg.needs_type_test = 1
                    else:
                        arg.needs_conversion = 1
            if arg.needs_conversion:
                arg.hdr_cname = Naming.arg_prefix + arg.name
            else:
                arg.hdr_cname = Naming.var_prefix + arg.name

        if nfixed > len(self.args):
            self.bad_signature()
            return
        elif nfixed < len(self.args):
            if not sig.has_generic_args:
                self.bad_signature()
            for arg in self.args:
                if arg.is_generic and \
                        (arg.type.is_extension_type or arg.type.is_builtin_type):
                    arg.needs_type_test = 1

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
        if argcount == 0 or (
                argcount == 1 and (self.args[0].is_self_arg or
                                   self.args[0].is_type_arg)):
            return 0
        return 1

    def signature_has_generic_args(self):
        return self.entry.signature.has_generic_args

    def declare_pyfunction(self, env):
        #print "DefNode.declare_pyfunction:", self.name, "in", env ###
        name = self.name
        entry = env.lookup_here(name)
        if entry and entry.type.is_cfunction and not self.is_wrapper:
            warning(self.pos, "Overriding cdef method with def method.", 5)
        entry = env.declare_pyfunction(name, self.pos, allow_redefine=not self.is_wrapper)
        self.entry = entry
        prefix = env.next_id(env.scope_prefix)

        entry.func_cname = \
            Naming.pyfunc_prefix + prefix + name
        entry.pymethdef_cname = \
            Naming.pymethdef_prefix + prefix + name
        if Options.docstrings:
            entry.doc = embed_position(self.pos, self.doc)
            entry.doc_cname = \
                Naming.funcdoc_prefix + prefix + name
            if entry.is_special:
                if entry.name in TypeSlots.invisible or not entry.doc or (entry.name in '__getattr__' and env.directives['fast_getattr']):
                    entry.wrapperbase_cname = None
                else:
                    entry.wrapperbase_cname = Naming.wrapperbase_prefix + prefix + name
        else:
            entry.doc = None

    def declare_lambda_function(self, env):
        entry = env.declare_lambda_function(self.lambda_name, self.pos)
        entry.doc = None
        self.entry = entry

    def declare_arguments(self, env):
        for arg in self.args:
            if not arg.name:
                error(arg.pos, "Missing argument name")
            else:
                env.control_flow.set_state((), (arg.name, 'source'), 'arg')
                env.control_flow.set_state((), (arg.name, 'initialized'), True)
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
                if arg.is_self_arg or arg.is_type_arg or \
                    (arg.type.is_extension_type and not arg.hdr_type.is_extension_type):
                        arg.entry.is_declared_generic = 1
        self.declare_python_arg(env, self.star_arg)
        self.declare_python_arg(env, self.starstar_arg)

    def declare_python_arg(self, env, arg):
        if arg:
            if env.directives['infer_types'] != False:
                type = PyrexTypes.unspecified_type
            else:
                type = py_object_type
            entry = env.declare_var(arg.name, type, arg.pos)
            entry.used = 1
            entry.init = "0"
            entry.init_to_none = 0
            entry.xdecref_cleanup = 1
            arg.entry = entry
            env.control_flow.set_state((), (arg.name, 'initialized'), True)

    def analyse_expressions(self, env):
        self.local_scope.directives = env.directives
        self.analyse_default_values(env)
        if self.needs_assignment_synthesis(env):
            # Shouldn't we be doing this at the module level too?
            self.synthesize_assignment_node(env)

    def needs_assignment_synthesis(self, env, code=None):
        if self.no_assignment_synthesis:
            return False
        # Should enable for module level as well, that will require more testing...
        if self.entry.is_anonymous:
            return True
        if env.is_module_scope:
            if code is None:
                return env.directives['binding']
            else:
                return code.globalstate.directives['binding']
        return env.is_py_class_scope or env.is_closure_scope

    def synthesize_assignment_node(self, env):
        import ExprNodes
        genv = env
        while genv.is_py_class_scope or genv.is_c_class_scope:
            genv = genv.outer_scope

        if genv.is_closure_scope:
            rhs = ExprNodes.InnerFunctionNode(
                self.pos, pymethdef_cname = self.entry.pymethdef_cname)
        else:
            rhs = ExprNodes.PyCFunctionNode(
                self.pos, pymethdef_cname = self.entry.pymethdef_cname, binding = env.directives['binding'])

        if env.is_py_class_scope:
            if not self.is_staticmethod and not self.is_classmethod:
                rhs.binding = True

        self.assmt = SingleAssignmentNode(self.pos,
            lhs = ExprNodes.NameNode(self.pos, name = self.name),
            rhs = rhs)
        self.assmt.analyse_declarations(env)
        self.assmt.analyse_expressions(env)

    def generate_function_header(self, code, with_pymethdef, proto_only=0):
        arg_code_list = []
        sig = self.entry.signature
        if sig.has_dummy_arg or self.self_in_stararg:
            arg_code_list.append(
                "PyObject *%s" % Naming.self_cname)
        for arg in self.args:
            if not arg.is_generic:
                if arg.is_self_arg or arg.is_type_arg:
                    arg_code_list.append("PyObject *%s" % arg.hdr_cname)
                else:
                    arg_code_list.append(
                        arg.hdr_type.declaration_code(arg.hdr_cname))
        if not self.entry.is_special and sig.method_flags() == [TypeSlots.method_noargs]:
            arg_code_list.append("CYTHON_UNUSED PyObject *unused")
        if (self.entry.scope.is_c_class_scope and self.entry.name == "__ipow__"):
            arg_code_list.append("CYTHON_UNUSED PyObject *unused")
        if sig.has_generic_args:
            arg_code_list.append(
                "PyObject *%s, PyObject *%s"
                    % (Naming.args_cname, Naming.kwds_cname))
        arg_code = ", ".join(arg_code_list)
        dc = self.return_type.declaration_code(self.entry.func_cname)
        mf = " ".join(self.modifiers).upper()
        if mf: mf += " "
        header = "static %s%s(%s)" % (mf, dc, arg_code)
        code.putln("%s; /*proto*/" % header)
        if proto_only:
            return
        if (Options.docstrings and self.entry.doc and
                not self.entry.scope.is_property_scope and
                (not self.entry.is_special or self.entry.wrapperbase_cname)):
            docstr = self.entry.doc
            if docstr.is_unicode:
                docstr = docstr.utf8encode()
            code.putln(
                'static char %s[] = "%s";' % (
                    self.entry.doc_cname,
                    split_string_literal(escape_byte_string(docstr))))
            if self.entry.is_special:
                code.putln(
                    "struct wrapperbase %s;" % self.entry.wrapperbase_cname)
        if with_pymethdef:
            code.put(
                "static PyMethodDef %s = " %
                    self.entry.pymethdef_cname)
            code.put_pymethoddef(self.entry, ";", allow_skip=False)
        code.putln("%s {" % header)

    def generate_argument_declarations(self, env, code):
        for arg in self.args:
            if arg.is_generic: # or arg.needs_conversion:
                if arg.needs_conversion:
                    code.putln("PyObject *%s = 0;" % arg.hdr_cname)
                elif not arg.entry.in_closure:
                    code.put_var_declaration(arg.entry)

    def generate_keyword_list(self, code):
        if self.signature_has_generic_args() and \
                self.signature_has_nongeneric_args():
            code.put(
                "static PyObject **%s[] = {" %
                    Naming.pykwdlist_cname)
            for arg in self.args:
                if arg.is_generic:
                    pystring_cname = code.intern_identifier(arg.name)
                    code.put('&%s,' % pystring_cname)
            code.putln("0};")

    def generate_argument_parsing_code(self, env, code):
        # Generate fast equivalent of PyArg_ParseTuple call for
        # generic arguments, if any, including args/kwargs
        if self.entry.signature.has_dummy_arg and not self.self_in_stararg:
            # get rid of unused argument warning
            code.putln("%s = %s;" % (Naming.self_cname, Naming.self_cname))

        old_error_label = code.new_error_label()
        our_error_label = code.error_label
        end_label = code.new_label("argument_unpacking_done")

        has_kwonly_args = self.num_kwonly_args > 0
        has_star_or_kw_args = self.star_arg is not None \
            or self.starstar_arg is not None or has_kwonly_args

        for arg in self.args:
            if not arg.type.is_pyobject:
                done = arg.type.create_from_py_utility_code(env)
                if not done: pass # will fail later

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
            for arg in self.args:
                arg_entry = arg.entry
                if arg.is_generic:
                    if arg.default:
                        if not arg.is_self_arg and not arg.is_type_arg:
                            if arg.kw_only:
                                kw_only_args.append(arg)
                            else:
                                positional_args.append(arg)
                    elif arg.kw_only:
                        kw_only_args.append(arg)
                    elif not arg.is_self_arg and not arg.is_type_arg:
                        positional_args.append(arg)

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
                        code.put_var_xdecref_clear(self.starstar_arg.entry)
                    else:
                        code.put_var_decref_clear(self.starstar_arg.entry)
            code.putln('__Pyx_AddTraceback("%s");' % self.entry.qualified_name)
            # The arguments are put into the closure one after the
            # other, so when type errors are found, all references in
            # the closure instance must be properly ref-counted to
            # facilitate generic closure instance deallocation.  In
            # the case of an argument type error, it's best to just
            # DECREF+clear the already handled references, as this
            # frees their references as early as possible.
            for arg in self.args:
                if arg.type.is_pyobject and arg.entry.in_closure:
                    code.put_var_xdecref_clear(arg.entry)
            if self.needs_closure:
                code.put_decref(Naming.cur_scope_cname, self.local_scope.scope_class.type)
            code.put_finish_refcount_context()
            code.putln("return %s;" % self.error_value())
        if code.label_used(end_label):
            code.put_label(end_label)

        # fix refnanny view on closure variables here, instead of
        # doing it separately for each arg parsing special case
        if self.star_arg and self.star_arg.entry.in_closure:
            code.put_var_giveref(self.star_arg.entry)
        if self.starstar_arg and self.starstar_arg.entry.in_closure:
            code.put_var_giveref(self.starstar_arg.entry)
        for arg in self.args:
            if arg.type.is_pyobject and arg.entry.in_closure:
                code.put_var_giveref(arg.entry)

    def generate_arg_assignment(self, arg, item, code):
        if arg.type.is_pyobject:
            if arg.is_generic:
                item = PyrexTypes.typecast(arg.type, PyrexTypes.py_object_type, item)
            entry = arg.entry
            if entry.in_closure:
                code.put_incref(item, PyrexTypes.py_object_type)
            code.putln("%s = %s;" % (entry.cname, item))
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
            code.put_var_xdecref_clear(arg.entry)

    def generate_arg_decref(self, arg, code):
        if arg:
            code.put_var_decref_clear(arg.entry)

    def generate_stararg_copy_code(self, code):
        if not self.star_arg:
            code.globalstate.use_utility_code(raise_argtuple_invalid_utility_code)
            code.putln("if (unlikely(PyTuple_GET_SIZE(%s) > 0)) {" %
                       Naming.args_cname)
            code.put('__Pyx_RaiseArgtupleInvalid("%s", 1, 0, 0, PyTuple_GET_SIZE(%s)); return %s;' % (
                    self.name, Naming.args_cname, self.error_value()))
            code.putln("}")

        if self.starstar_arg:
            if self.star_arg:
                kwarg_check = "unlikely(%s)" % Naming.kwds_cname
            else:
                kwarg_check = "%s" % Naming.kwds_cname
        else:
            kwarg_check = "unlikely(%s) && unlikely(PyDict_Size(%s) > 0)" % (
                Naming.kwds_cname, Naming.kwds_cname)
        code.globalstate.use_utility_code(keyword_string_check_utility_code)
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
            code.put_gotref(self.starstar_arg.entry.cname)

        if self.self_in_stararg:
            # need to create a new tuple with 'self' inserted as first item
            code.put("%s = PyTuple_New(PyTuple_GET_SIZE(%s)+1); if (unlikely(!%s)) " % (
                    self.star_arg.entry.cname,
                    Naming.args_cname,
                    self.star_arg.entry.cname))
            if self.starstar_arg:
                code.putln("{")
                code.put_decref_clear(self.starstar_arg.entry.cname, py_object_type)
                code.putln("return %s;" % self.error_value())
                code.putln("}")
            else:
                code.putln("return %s;" % self.error_value())
            code.put_gotref(self.star_arg.entry.cname)
            code.put_incref(Naming.self_cname, py_object_type)
            code.put_giveref(Naming.self_cname)
            code.putln("PyTuple_SET_ITEM(%s, 0, %s);" % (
                self.star_arg.entry.cname, Naming.self_cname))
            temp = code.funcstate.allocate_temp(PyrexTypes.c_py_ssize_t_type, manage_ref=False)
            code.putln("for (%s=0; %s < PyTuple_GET_SIZE(%s); %s++) {" % (
                temp, temp, Naming.args_cname, temp))
            code.putln("PyObject* item = PyTuple_GET_ITEM(%s, %s);" % (
                Naming.args_cname, temp))
            code.put_incref("item", py_object_type)
            code.put_giveref("item")
            code.putln("PyTuple_SET_ITEM(%s, %s+1, item);" % (
                self.star_arg.entry.cname, temp))
            code.putln("}")
            code.funcstate.release_temp(temp)
            self.star_arg.entry.xdecref_cleanup = 0
        elif self.star_arg:
            code.put_incref(Naming.args_cname, py_object_type)
            code.putln("%s = %s;" % (
                    self.star_arg.entry.cname,
                    Naming.args_cname))
            self.star_arg.entry.xdecref_cleanup = 0

    def generate_tuple_and_keyword_parsing_code(self, positional_args,
                                                kw_only_args, success_label, code):
        argtuple_error_label = code.new_label("argtuple_error")

        min_positional_args = self.num_required_args - self.num_required_kw_args
        if len(self.args) > 0 and (self.args[0].is_self_arg or self.args[0].is_type_arg):
            min_positional_args -= 1
        max_positional_args = len(positional_args)
        has_fixed_positional_count = not self.star_arg and \
            min_positional_args == max_positional_args

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
                    pystring_cname = code.intern_identifier(arg.name)
                    # required keyword-only argument missing
                    code.put('__Pyx_RaiseKeywordRequired("%s", %s); ' % (
                            self.name,
                            pystring_cname))
                    code.putln(code.error_goto(self.pos))
                    break

        elif min_positional_args == max_positional_args:
            # parse the exact number of positional arguments from the
            # args tuple
            code.putln('} else {')
            for i, arg in enumerate(positional_args):
                item = "PyTuple_GET_ITEM(%s, %d)" % (Naming.args_cname, i)
                self.generate_arg_assignment(arg, item, code)
            self.generate_arg_default_assignments(code)

        else:
            # parse the positional arguments from the variable length
            # args tuple
            code.putln('} else {')
            self.generate_arg_default_assignments(code)
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
            code.globalstate.use_utility_code(raise_argtuple_invalid_utility_code)
            code.put('__Pyx_RaiseArgtupleInvalid("%s", %d, %d, %d, PyTuple_GET_SIZE(%s)); ' % (
                    self.name, has_fixed_positional_count,
                    min_positional_args, max_positional_args,
                    Naming.args_cname))
            code.putln(code.error_goto(self.pos))

    def generate_arg_default_assignments(self, code):
        for arg in self.args:
            if arg.is_generic and arg.default:
                code.putln(
                    "%s = %s;" % (
                        arg.entry.cname,
                        arg.calculate_default_value_code(code)))

    def generate_stararg_init_code(self, max_positional_args, code):
        if self.starstar_arg:
            self.starstar_arg.entry.xdecref_cleanup = 0
            code.putln('%s = PyDict_New(); if (unlikely(!%s)) return %s;' % (
                    self.starstar_arg.entry.cname,
                    self.starstar_arg.entry.cname,
                    self.error_value()))
            code.put_gotref(self.starstar_arg.entry.cname)
        if self.star_arg:
            self.star_arg.entry.xdecref_cleanup = 0
            code.putln('if (PyTuple_GET_SIZE(%s) > %d) {' % (
                    Naming.args_cname,
                    max_positional_args))
            code.putln('%s = PyTuple_GetSlice(%s, %d, PyTuple_GET_SIZE(%s));' % (
                    self.star_arg.entry.cname, Naming.args_cname,
                    max_positional_args, Naming.args_cname))
            code.putln("if (unlikely(!%s)) {" % self.star_arg.entry.cname)
            if self.starstar_arg:
                code.put_decref_clear(self.starstar_arg.entry.cname, py_object_type)
            if self.needs_closure:
                code.put_decref(Naming.cur_scope_cname, self.local_scope.scope_class.type)
            code.put_finish_refcount_context()
            code.putln('return %s;' % self.error_value())
            code.putln('}')
            code.put_gotref(self.star_arg.entry.cname)
            code.putln('} else {')
            code.put("%s = %s; " % (self.star_arg.entry.cname, Naming.empty_tuple))
            code.put_incref(Naming.empty_tuple, py_object_type)
            code.putln('}')

    def generate_keyword_unpacking_code(self, min_positional_args, max_positional_args,
                                        has_fixed_positional_count, positional_args,
                                        kw_only_args, argtuple_error_label, code):
        all_args = tuple(positional_args) + tuple(kw_only_args)
        max_args = len(all_args)

        code.putln("Py_ssize_t kw_args = PyDict_Size(%s);" %
                   Naming.kwds_cname)
        # the 'values' array collects borrowed references to arguments
        # before doing any type coercion etc.
        code.putln("PyObject* values[%d] = {%s};" % (
            max_args, ','.join('0'*max_args)))

        # assign borrowed Python default values to the values array,
        # so that they can be overwritten by received arguments below
        for i, arg in enumerate(all_args):
            if arg.default and arg.type.is_pyobject:
                default_value = arg.calculate_default_value_code(code)
                code.putln('values[%d] = %s;' % (i, arg.type.as_pyobject(default_value)))

        # parse the args tuple and check that it's not too long
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

        # now fill up the positional/required arguments with values
        # from the kw dict
        if self.num_required_args or max_positional_args > 0:
            last_required_arg = -1
            for i, arg in enumerate(all_args):
                if not arg.default:
                    last_required_arg = i
            if last_required_arg < max_positional_args:
                last_required_arg = max_positional_args-1
            num_required_args = self.num_required_args
            if max_positional_args > 0:
                code.putln('switch (PyTuple_GET_SIZE(%s)) {' % Naming.args_cname)
            for i, arg in enumerate(all_args[:last_required_arg+1]):
                if max_positional_args > 0 and i <= max_positional_args:
                    if self.star_arg and i == max_positional_args:
                        code.putln('default:')
                    else:
                        code.putln('case %2d:' % i)
                pystring_cname = code.intern_identifier(arg.name)
                if arg.default:
                    if arg.kw_only:
                        # handled separately below
                        continue
                    code.putln('if (kw_args > 0) {')
                    code.putln('PyObject* value = PyDict_GetItem(%s, %s);' % (
                        Naming.kwds_cname, pystring_cname))
                    code.putln('if (value) { values[%d] = value; kw_args--; }' % i)
                    code.putln('}')
                else:
                    num_required_args -= 1
                    code.putln('values[%d] = PyDict_GetItem(%s, %s);' % (
                        i, Naming.kwds_cname, pystring_cname))
                    code.putln('if (likely(values[%d])) kw_args--;' % i);
                    if i < min_positional_args:
                        if i == 0:
                            # special case: we know arg 0 is missing
                            code.put('else ')
                            code.put_goto(argtuple_error_label)
                        else:
                            # print the correct number of values (args or
                            # kwargs) that were passed into positional
                            # arguments up to this point
                            code.putln('else {')
                            code.globalstate.use_utility_code(raise_argtuple_invalid_utility_code)
                            code.put('__Pyx_RaiseArgtupleInvalid("%s", %d, %d, %d, %d); ' % (
                                    self.name, has_fixed_positional_count,
                                    min_positional_args, max_positional_args, i))
                            code.putln(code.error_goto(self.pos))
                            code.putln('}')
                    elif arg.kw_only:
                        code.putln('else {')
                        code.put('__Pyx_RaiseKeywordRequired("%s", %s); ' %(
                                self.name, pystring_cname))
                        code.putln(code.error_goto(self.pos))
                        code.putln('}')
            if max_positional_args > 0:
                code.putln('}')

        if kw_only_args and not self.starstar_arg:
            # unpack optional keyword-only arguments
            # checking for interned strings in a dict is faster than iterating
            # but it's too likely that we must iterate if we expect **kwargs
            optional_args = []
            for i, arg in enumerate(all_args[max_positional_args:]):
                if not arg.kw_only or not arg.default:
                    continue
                optional_args.append((i+max_positional_args, arg))
            if optional_args:
                # this mimics an unrolled loop so that we can "break" out of it
                code.putln('while (kw_args > 0) {')
                code.putln('PyObject* value;')
                for i, arg in optional_args:
                    pystring_cname = code.intern_identifier(arg.name)
                    code.putln(
                        'value = PyDict_GetItem(%s, %s);' % (
                        Naming.kwds_cname, pystring_cname))
                    code.putln(
                        'if (value) { values[%d] = value; if (!(--kw_args)) break; }' % i)
                code.putln('break;')
                code.putln('}')

        code.putln('if (unlikely(kw_args > 0)) {')
        # non-positional/-required kw args left in dict: default args,
        # kw-only args, **kwargs or error
        #
        # This is sort of a catch-all: except for checking required
        # arguments, this will always do the right thing for unpacking
        # keyword arguments, so that we can concentrate on optimising
        # common cases above.
        if max_positional_args == 0:
            pos_arg_count = "0"
        elif self.star_arg:
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
                self.name))
        code.putln(code.error_goto(self.pos))
        code.putln('}')

        # convert arg values to their final type and assign them
        for i, arg in enumerate(all_args):
            if arg.default and not arg.type.is_pyobject:
                code.putln("if (values[%d]) {" % i)
            self.generate_arg_assignment(arg, "values[%d]" % i, code)
            if arg.default and not arg.type.is_pyobject:
                code.putln('} else {')
                code.putln(
                    "%s = %s;" % (
                        arg.entry.cname,
                        arg.calculate_default_value_code(code)))
                code.putln('}')

    def generate_argument_conversion_code(self, code):
        # Generate code to convert arguments from signature type to
        # declared type, if needed.  Also copies signature arguments
        # into closure fields.
        for arg in self.args:
            if arg.needs_conversion:
                self.generate_arg_conversion(arg, code)
            elif arg.entry.in_closure:
                if arg.type.is_pyobject:
                    code.put_incref(arg.hdr_cname, py_object_type)
                code.putln('%s = %s;' % (arg.entry.cname, arg.hdr_cname))

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
            lhs = arg.entry.cname
            rhs = "%s(%s)" % (func, arg.hdr_cname)
            if new_type.is_enum:
                rhs = PyrexTypes.typecast(new_type, PyrexTypes.c_long_type, rhs)
            code.putln("%s = %s; %s" % (
                lhs,
                rhs,
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
            code.put_var_gotref(arg.entry)
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
            elif not arg.accept_none and arg.type.is_pyobject:
                self.generate_arg_none_check(arg, code)

    def error_value(self):
        return self.entry.signature.error_value

    def caller_will_check_exceptions(self):
        return 1


class GeneratorDefNode(DefNode):
    # Generator DefNode.
    #
    # gbody          GeneratorBodyDefNode
    #

    is_generator = True
    needs_closure = True

    child_attrs = DefNode.child_attrs + ["gbody"]

    def __init__(self, **kwargs):
        # XXX: don't actually needs a body
        kwargs['body'] = StatListNode(kwargs['pos'], stats=[])
        super(GeneratorDefNode, self).__init__(**kwargs)

    def analyse_declarations(self, env):
        super(GeneratorDefNode, self).analyse_declarations(env)
        self.gbody.local_scope = self.local_scope
        self.gbody.analyse_declarations(env)

    def generate_function_body(self, env, code):
        body_cname = self.gbody.entry.func_cname
        generator_cname = '%s->%s' % (Naming.cur_scope_cname, Naming.obj_base_cname)

        code.putln('%s.resume_label = 0;' % generator_cname)
        code.putln('%s.body = (__pyx_generator_body_t) %s;' % (generator_cname, body_cname))
        code.put_giveref(Naming.cur_scope_cname)
        code.put_finish_refcount_context()
        code.putln("return (PyObject *) %s;" % Naming.cur_scope_cname);

    def generate_function_definitions(self, env, code):
        self.gbody.generate_function_header(code, proto=True)
        super(GeneratorDefNode, self).generate_function_definitions(env, code)
        self.gbody.generate_function_definitions(env, code)


class GeneratorBodyDefNode(DefNode):
    # Generator body DefNode.
    #

    is_generator_body = True

    def __init__(self, pos=None, name=None, body=None):
        super(GeneratorBodyDefNode, self).__init__(pos=pos, body=body, name=name, doc=None,
                                                   args=[],
                                                   star_arg=None, starstar_arg=None)

    def declare_generator_body(self, env):
        prefix = env.next_id(env.scope_prefix)
        name = env.next_id('generator')
        entry = env.declare_var(prefix + name, py_object_type, self.pos, visibility='private')
        entry.func_cname = Naming.genbody_prefix + prefix + name
        entry.qualified_name = EncodedString(self.name)
        self.entry = entry

    def analyse_declarations(self, env):
        self.analyse_argument_types(env)
        self.declare_generator_body(env)

    def generate_function_header(self, code, proto=False):
        header = "static PyObject *%s(%s, PyObject *%s)" % (
            self.entry.func_cname,
            self.local_scope.scope_class.type.declaration_code(Naming.cur_scope_cname),
            Naming.sent_value_cname)
        if proto:
            code.putln('%s; /* proto */' % header)
        else:
            code.putln('%s /* generator body */\n{' % header);

    def generate_function_definitions(self, env, code):
        lenv = self.local_scope

        # Generate closure function definitions
        self.body.generate_function_definitions(lenv, code)

        # Generate C code for header and body of function
        code.enter_cfunc_scope()
        code.return_from_error_cleanup_label = code.new_label()

        # ----- Top-level constants used by this function
        code.mark_pos(self.pos)
        self.generate_cached_builtins_decls(lenv, code)
        # ----- Function header
        code.putln("")
        self.generate_function_header(code)
        # ----- Local variables
        code.putln("PyObject *%s = NULL;" % Naming.retval_cname)
        tempvardecl_code = code.insertion_point()
        code.put_declare_refcount_context()
        code.put_setup_refcount_context(self.entry.name)

        # ----- Resume switch point.
        code.funcstate.init_closure_temps(lenv.scope_class.type.scope)
        resume_code = code.insertion_point()
        first_run_label = code.new_label('first_run')
        code.use_label(first_run_label)
        code.put_label(first_run_label)
        code.putln('%s' %
                   (code.error_goto_if_null(Naming.sent_value_cname, self.pos)))

        # ----- Function body
        self.generate_function_body(env, code)
        code.putln('PyErr_SetNone(PyExc_StopIteration); %s' % code.error_goto(self.pos))
        # ----- Error cleanup
        if code.error_label in code.labels_used:
            code.put_goto(code.return_label)
            code.put_label(code.error_label)
            for cname, type in code.funcstate.all_managed_temps():
                code.put_xdecref(cname, type)
            code.putln('__Pyx_AddTraceback("%s");' % self.entry.qualified_name)

        # ----- Non-error return cleanup
        code.put_label(code.return_label)
        code.put_xdecref(Naming.retval_cname, py_object_type)
        code.putln('%s->%s.resume_label = -1;' % (Naming.cur_scope_cname, Naming.obj_base_cname))
        code.put_finish_refcount_context()
        code.putln('return NULL;');
        code.putln("}")

        # ----- Go back and insert temp variable declarations
        tempvardecl_code.put_temp_declarations(code.funcstate)
        # ----- Generator resume code
        resume_code.putln("switch (%s->%s.resume_label) {" % (Naming.cur_scope_cname, Naming.obj_base_cname));
        resume_code.putln("case 0: goto %s;" % first_run_label)

        from ParseTreeTransforms import YieldNodeCollector
        collector = YieldNodeCollector()
        collector.visitchildren(self)
        for yield_expr in collector.yields:
            resume_code.putln("case %d: goto %s;" % (yield_expr.label_num, yield_expr.label_name));
        resume_code.putln("default: /* CPython raises the right error here */");
        resume_code.put_finish_refcount_context()
        resume_code.putln("return NULL;");
        resume_code.putln("}");

        code.exit_cfunc_scope()


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
        self.func_node = ExprNodes.RawCNameExprNode(self.pos, py_object_type)
        call_tuple = ExprNodes.TupleNode(self.pos, args=[ExprNodes.NameNode(self.pos, name=arg.name) for arg in self.args[first_arg:]])
        call_node = ExprNodes.SimpleCallNode(self.pos,
                                             function=self.func_node,
                                             args=[ExprNodes.NameNode(self.pos, name=arg.name) for arg in self.args[first_arg:]])
        self.body = ReturnStatNode(self.pos, value=call_node)
        self.body.analyse_expressions(env)

    def generate_execution_code(self, code):
        interned_attr_cname = code.intern_identifier(self.py_func.entry.name)
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
        func_node_temp = code.funcstate.allocate_temp(py_object_type, manage_ref=True)
        self.func_node.set_cname(func_node_temp)
        # need to get attribute manually--scope would return cdef method
        err = code.error_goto_if_null(func_node_temp, self.pos)
        code.putln("%s = PyObject_GetAttr(%s, %s); %s" % (
            func_node_temp, self_arg, interned_attr_cname, err))
        code.put_gotref(func_node_temp)
        is_builtin_function_or_method = "PyCFunction_Check(%s)" % func_node_temp
        is_overridden = "(PyCFunction_GET_FUNCTION(%s) != (void *)&%s)" % (
            func_node_temp, self.py_func.entry.func_cname)
        code.putln("if (!%s || %s) {" % (is_builtin_function_or_method, is_overridden))
        self.body.generate_execution_code(code)
        code.putln("}")
        code.put_decref_clear(func_node_temp, PyrexTypes.py_object_type)
        code.funcstate.release_temp(func_node_temp)
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
    #  decorators    [DecoratorNode]        list of decorators or None
    #
    #  The following subnodes are constructed internally:
    #
    #  dict     DictNode   Class dictionary or Py3 namespace
    #  classobj ClassNode  Class object
    #  target   NameNode   Variable to assign class object to

    child_attrs = ["body", "dict", "metaclass", "mkw", "bases", "classobj", "target"]
    decorators = None
    py3_style_class = False # Python3 style class (bases+kwargs)

    def __init__(self, pos, name, bases, doc, body, decorators = None,
                 keyword_args = None, starstar_arg = None):
        StatNode.__init__(self, pos)
        self.name = name
        self.doc = doc
        self.body = body
        self.decorators = decorators
        import ExprNodes
        if self.doc and Options.docstrings:
            doc = embed_position(self.pos, self.doc)
            doc_node = ExprNodes.StringNode(pos, value = doc)
        else:
            doc_node = None
        if keyword_args or starstar_arg:
            self.py3_style_class = True
            self.bases = bases
            self.metaclass = None
            if keyword_args and not starstar_arg:
                for i, item in list(enumerate(keyword_args.key_value_pairs))[::-1]:
                    if item.key.value == 'metaclass':
                        if self.metaclass is not None:
                            error(item.pos, "keyword argument 'metaclass' passed multiple times")
                        # special case: we already know the metaclass,
                        # so we don't need to do the "build kwargs,
                        # find metaclass" dance at runtime
                        self.metaclass = item.value
                        del keyword_args.key_value_pairs[i]
            if starstar_arg or (keyword_args and keyword_args.key_value_pairs):
                self.mkw = ExprNodes.KeywordArgsNode(
                    pos, keyword_args = keyword_args, starstar_arg = starstar_arg)
            else:
                self.mkw = ExprNodes.NullNode(pos)
            if self.metaclass is None:
                self.metaclass = ExprNodes.PyClassMetaclassNode(
                    pos, mkw = self.mkw, bases = self.bases)
            self.dict = ExprNodes.PyClassNamespaceNode(pos, name = name,
                        doc = doc_node, metaclass = self.metaclass, bases = self.bases,
                        mkw = self.mkw)
            self.classobj = ExprNodes.Py3ClassNode(pos, name = name,
                    bases = self.bases, dict = self.dict, doc = doc_node,
                    metaclass = self.metaclass, mkw = self.mkw)
        else:
            self.dict = ExprNodes.DictNode(pos, key_value_pairs = [])
            self.metaclass = None
            self.mkw = None
            self.bases = None
            self.classobj = ExprNodes.ClassNode(pos, name = name,
                    bases = bases, dict = self.dict, doc = doc_node)
        self.target = ExprNodes.NameNode(pos, name = name)

    def as_cclass(self):
        """
        Return this node as if it were declared as an extension class
        """
        if self.py3_style_class:
            error(self.classobj.pos, "Python3 style class could not be represented as C class")
            return
        bases = self.classobj.bases.args
        if len(bases) == 0:
            base_class_name = None
            base_class_module = None
        elif len(bases) == 1:
            base = bases[0]
            path = []
            from ExprNodes import AttributeNode, NameNode
            while isinstance(base, AttributeNode):
                path.insert(0, base.attribute)
                base = base.obj
            if isinstance(base, NameNode):
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
                             decorators = self.decorators,
                             body = self.body,
                             in_pxd = False,
                             doc = self.doc)

    def create_scope(self, env):
        genv = env
        while genv.is_py_class_scope or genv.is_c_class_scope:
            genv = genv.outer_scope
        cenv = self.scope = PyClassScope(name = self.name, outer_scope = genv)
        return cenv

    def analyse_declarations(self, env):
        self.target.analyse_target_declaration(env)
        cenv = self.create_scope(env)
        cenv.directives = env.directives
        cenv.class_obj_cname = self.target.entry.cname
        self.body.analyse_declarations(cenv)

    def analyse_expressions(self, env):
        if self.py3_style_class:
            self.bases.analyse_expressions(env)
            self.metaclass.analyse_expressions(env)
            self.mkw.analyse_expressions(env)
        self.dict.analyse_expressions(env)
        self.classobj.analyse_expressions(env)
        genv = env.global_scope()
        cenv = self.scope
        self.body.analyse_expressions(cenv)
        self.target.analyse_target_expression(env, self.classobj)

    def generate_function_definitions(self, env, code):
        self.generate_lambda_definitions(self.scope, code)
        self.body.generate_function_definitions(self.scope, code)

    def generate_execution_code(self, code):
        code.pyclass_stack.append(self)
        cenv = self.scope
        if self.py3_style_class:
            self.bases.generate_evaluation_code(code)
            self.mkw.generate_evaluation_code(code)
            self.metaclass.generate_evaluation_code(code)
        self.dict.generate_evaluation_code(code)
        cenv.namespace_cname = cenv.class_obj_cname = self.dict.result()
        self.body.generate_execution_code(code)
        self.classobj.generate_evaluation_code(code)
        cenv.namespace_cname = cenv.class_obj_cname = self.classobj.result()
        self.target.generate_assignment_code(self.classobj, code)
        self.dict.generate_disposal_code(code)
        self.dict.free_temps(code)
        if self.py3_style_class:
            self.mkw.generate_disposal_code(code)
            self.mkw.free_temps(code)
            self.metaclass.generate_disposal_code(code)
            self.metaclass.free_temps(code)
            self.bases.generate_disposal_code(code)
            self.bases.free_temps(code)
        code.pyclass_stack.pop()

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
    #  decorators         [DecoratorNode]   list of decorators or None
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
    decorators = None
    shadow = False

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
                env.add_imported_module(self.module)

        if self.base_class_name:
            if self.base_class_module:
                base_class_scope = env.find_module(self.base_class_module, self.pos)
            else:
                base_class_scope = env
            if self.base_class_name == 'object':
                # extension classes are special and don't need to inherit from object
                if base_class_scope is None or base_class_scope.lookup('object') is None:
                    self.base_class_name = None
                    self.base_class_module = None
                    base_class_scope = None
            if base_class_scope:
                base_class_entry = base_class_scope.find(self.base_class_name, self.pos)
                if base_class_entry:
                    if not base_class_entry.is_type:
                        error(self.pos, "'%s' is not a type name" % self.base_class_name)
                    elif not base_class_entry.type.is_extension_type and \
                             not (base_class_entry.type.is_builtin_type and \
                                  base_class_entry.type.objstruct_cname):
                        error(self.pos, "'%s' is not an extension type" % self.base_class_name)
                    elif not base_class_entry.type.is_complete():
                        error(self.pos, "Base class '%s' of type '%s' is incomplete" % (
                            self.base_class_name, self.class_name))
                    elif base_class_entry.type.scope and base_class_entry.type.scope.directives and \
                             base_class_entry.type.scope.directives['final']:
                        error(self.pos, "Base class '%s' of type '%s' is final" % (
                            self.base_class_name, self.class_name))
                    elif base_class_entry.type.is_builtin_type and \
                             base_class_entry.type.name in ('tuple', 'str', 'bytes'):
                        error(self.pos, "inheritance from PyVarObject types like '%s' is not currently supported"
                              % base_class_entry.type.name)
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

        if self.visibility == 'extern':
            if (self.module_name == '__builtin__' and
                self.class_name in Builtin.builtin_types and
                env.qualified_name[:8] != 'cpython.'): # allow overloaded names for cimporting from cpython
                warning(self.pos, "%s already a builtin Cython type" % self.class_name, 1)

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
            buffer_defaults = buffer_defaults,
            shadow = self.shadow)
        if self.shadow:
            home_scope.lookup(self.class_name).as_variable = self.entry
        if home_scope is not env and self.visibility == 'extern':
            env.add_imported_entry(self.class_name, self.entry, self.pos)
        self.scope = scope = self.entry.type.scope
        if scope is not None:
            scope.directives = env.directives

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
        if self.body:
            self.generate_lambda_definitions(self.scope, code)
            self.body.generate_function_definitions(self.scope, code)

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
            entry.scope.directives = env.directives
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


class NonlocalNode(StatNode):
    # Nonlocal variable declaration via the 'nonlocal' keyword.
    #
    # names    [string]

    child_attrs = []

    def analyse_declarations(self, env):
        for name in self.names:
            env.declare_nonlocal(name, self.pos)

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
        self.expr.result_is_used = False # hint that .result() may safely be left empty
        self.expr.analyse_expressions(env)

    def nogil_check(self, env):
        if self.expr.type.is_pyobject and self.expr.is_temp:
            self.gil_error()

    gil_message = "Discarding owned Python object"

    def generate_execution_code(self, code):
        self.expr.generate_evaluation_code(code)
        if not self.expr.is_temp and self.expr.result():
            code.putln("%s;" % self.expr.result())
        self.expr.generate_disposal_code(code)
        self.expr.free_temps(code)

    def generate_function_definitions(self, env, code):
        self.expr.generate_function_definitions(env, code)

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

#       def analyse_expressions(self, env):
#           self.analyse_expressions_1(env)
#           self.analyse_expressions_2(env)

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
                        error(self.rhs.pos, "Can only declare one type at a time.")
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
                        error(self.rhs.pos, "Struct or union members must be given by name.")
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

    def generate_rhs_evaluation_code(self, code):
        self.rhs.generate_evaluation_code(code)

    def generate_assignment_code(self, code):
        self.lhs.generate_assignment_code(self.rhs, code)

    def generate_function_definitions(self, env, code):
        self.rhs.generate_function_definitions(env, code)

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
        if not self.rhs.is_simple():
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
        self.rhs.free_temps(code)

    def generate_function_definitions(self, env, code):
        self.rhs.generate_function_definitions(env, code)

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

#    def analyse_expressions(self, env):
#        for stat in self.stats:
#            stat.analyse_expressions_1(env, use_temp = 1)
#        for stat in self.stats:
#            stat.analyse_expressions_2(env)

    def generate_execution_code(self, code):
        for stat in self.stats:
            stat.generate_rhs_evaluation_code(code)
        for stat in self.stats:
            stat.generate_assignment_code(code)

    def generate_function_definitions(self, env, code):
        for stat in self.stats:
            stat.generate_function_definitions(env, code)

    def annotate(self, code):
        for stat in self.stats:
            stat.annotate(code)


class InPlaceAssignmentNode(AssignmentNode):
    #  An in place arithmetic operand:
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

    def analyse_declarations(self, env):
        self.lhs.analyse_target_declaration(env)

    def analyse_types(self, env):
        self.rhs.analyse_types(env)
        self.lhs.analyse_target_types(env)

    def generate_execution_code(self, code):
        import ExprNodes
        self.rhs.generate_evaluation_code(code)
        self.lhs.generate_subexpr_evaluation_code(code)
        c_op = self.operator
        if c_op == "//":
            c_op = "/"
        elif c_op == "**":
            error(self.pos, "No C inplace power operator")
        if isinstance(self.lhs, ExprNodes.IndexNode) and self.lhs.is_buffer_access:
            if self.lhs.type.is_pyobject:
                error(self.pos, "In-place operators not allowed on object buffers in this release.")
            if c_op in ('/', '%') and self.lhs.type.is_int and not code.directives['cdivision']:
                error(self.pos, "In-place non-c divide operators not allowed on int buffers.")
            self.lhs.generate_buffer_setitem_code(self.rhs, code, c_op)
        else:
            # C++
            # TODO: make sure overload is declared
            code.putln("%s %s= %s;" % (self.lhs.result(), c_op, self.rhs.result()))
        self.lhs.generate_subexpr_disposal_code(code)
        self.lhs.free_subexpr_temps(code)
        self.rhs.generate_disposal_code(code)
        self.rhs.free_temps(code)

    def annotate(self, code):
        self.lhs.annotate(code)
        self.rhs.annotate(code)

    def create_binop_node(self):
        import ExprNodes
        return ExprNodes.binop_node(self.pos, self.operator, self.lhs, self.rhs)


class PrintStatNode(StatNode):
    #  print statement
    #
    #  arg_tuple         TupleNode
    #  stream            ExprNode or None (stdout)
    #  append_newline    boolean

    child_attrs = ["arg_tuple", "stream"]

    def analyse_expressions(self, env):
        if self.stream:
            self.stream.analyse_expressions(env)
            self.stream = self.stream.coerce_to_pyobject(env)
        self.arg_tuple.analyse_expressions(env)
        self.arg_tuple = self.arg_tuple.coerce_to_pyobject(env)
        env.use_utility_code(printing_utility_code)
        if len(self.arg_tuple.args) == 1 and self.append_newline:
            env.use_utility_code(printing_one_utility_code)

    nogil_check = Node.gil_error
    gil_message = "Python print statement"

    def generate_execution_code(self, code):
        if self.stream:
            self.stream.generate_evaluation_code(code)
            stream_result = self.stream.py_result()
        else:
            stream_result = '0'
        if len(self.arg_tuple.args) == 1 and self.append_newline:
            arg = self.arg_tuple.args[0]
            arg.generate_evaluation_code(code)

            code.putln(
                "if (__Pyx_PrintOne(%s, %s) < 0) %s" % (
                    stream_result,
                    arg.py_result(),
                    code.error_goto(self.pos)))
            arg.generate_disposal_code(code)
            arg.free_temps(code)
        else:
            self.arg_tuple.generate_evaluation_code(code)
            code.putln(
                "if (__Pyx_Print(%s, %s, %d) < 0) %s" % (
                    stream_result,
                    self.arg_tuple.py_result(),
                    self.append_newline,
                    code.error_goto(self.pos)))
            self.arg_tuple.generate_disposal_code(code)
            self.arg_tuple.free_temps(code)

        if self.stream:
            self.stream.generate_disposal_code(code)
            self.stream.free_temps(code)

    def generate_function_definitions(self, env, code):
        if self.stream:
            self.stream.generate_function_definitions(env, code)
        self.arg_tuple.generate_function_definitions(env, code)

    def annotate(self, code):
        if self.stream:
            self.stream.annotate(code)
        self.arg_tuple.annotate(code)


class ExecStatNode(StatNode):
    #  exec statement
    #
    #  args     [ExprNode]

    child_attrs = ["args"]

    def analyse_expressions(self, env):
        for i, arg in enumerate(self.args):
            arg.analyse_expressions(env)
            arg = arg.coerce_to_pyobject(env)
            self.args[i] = arg
        env.use_utility_code(Builtin.pyexec_utility_code)

    nogil_check = Node.gil_error
    gil_message = "Python exec statement"

    def generate_execution_code(self, code):
        args = []
        for arg in self.args:
            arg.generate_evaluation_code(code)
            args.append( arg.py_result() )
        args = tuple(args + ['0', '0'][:3-len(args)])
        temp_result = code.funcstate.allocate_temp(PyrexTypes.py_object_type, manage_ref=True)
        code.putln("%s = __Pyx_PyRun(%s, %s, %s);" % (
                (temp_result,) + args))
        for arg in self.args:
            arg.generate_disposal_code(code)
            arg.free_temps(code)
        code.putln(
            code.error_goto_if_null(temp_result, self.pos))
        code.put_gotref(temp_result)
        code.put_decref_clear(temp_result, py_object_type)
        code.funcstate.release_temp(temp_result)

    def annotate(self, code):
        for arg in self.args:
            arg.annotate(code)


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
                pass
            elif arg.type.is_ptr and arg.type.base_type.is_cpp_class:
                self.cpp_check(env)
            elif arg.type.is_cpp_class:
                error(arg.pos, "Deletion of non-heap C++ object")
            else:
                error(arg.pos, "Deletion of non-Python, non-C++ object")
            #arg.release_target_temp(env)

    def nogil_check(self, env):
        for arg in self.args:
            if arg.type.is_pyobject:
                self.gil_error()

    gil_message = "Deleting Python object"

    def generate_execution_code(self, code):
        for arg in self.args:
            if arg.type.is_pyobject:
                arg.generate_deletion_code(code)
            elif arg.type.is_ptr and arg.type.base_type.is_cpp_class:
                arg.generate_result_code(code)
                code.putln("delete %s;" % arg.result())
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

    child_attrs = ["value"]

    def analyse_expressions(self, env):
        return_type = env.return_type
        self.return_type = return_type
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
        else:
            if (not return_type.is_void
                and not return_type.is_pyobject
                and not return_type.is_returncode):
                    error(self.pos, "Return value required")

    def nogil_check(self, env):
        if self.return_type.is_pyobject:
            self.gil_error()

    gil_message = "Returning Python object"

    def generate_execution_code(self, code):
        code.mark_pos(self.pos)
        if not self.return_type:
            # error reported earlier
            return
        if self.return_type.is_pyobject:
            code.put_xdecref(Naming.retval_cname,
                             self.return_type)
        if self.value:
            self.value.generate_evaluation_code(code)
            self.value.make_owned_reference(code)
            code.putln(
                "%s = %s;" % (
                    Naming.retval_cname,
                    self.value.result_as(self.return_type)))
            self.value.generate_post_assignment_code(code)
            self.value.free_temps(code)
        else:
            if self.return_type.is_pyobject:
                code.put_init_to_py_none(Naming.retval_cname, self.return_type)
            elif self.return_type.is_returncode:
                code.putln(
                    "%s = %s;" % (
                        Naming.retval_cname,
                        self.return_type.default_value))
        for cname, type in code.funcstate.temps_holding_reference():
            code.put_decref_clear(cname, type)
        code.put_goto(code.return_label)

    def generate_function_definitions(self, env, code):
        if self.value is not None:
            self.value.generate_function_definitions(env, code)

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
        if self.exc_value:
            self.exc_value.analyse_types(env)
            self.exc_value = self.exc_value.coerce_to_pyobject(env)
        if self.exc_tb:
            self.exc_tb.analyse_types(env)
            self.exc_tb = self.exc_tb.coerce_to_pyobject(env)
        # special cases for builtin exceptions
        self.builtin_exc_name = None
        if self.exc_type and not self.exc_value and not self.exc_tb:
            exc = self.exc_type
            import ExprNodes
            if (isinstance(exc, ExprNodes.SimpleCallNode) and
                not (exc.args or (exc.arg_tuple is not None and
                                  exc.arg_tuple.args))):
                exc = exc.function # extract the exception type
            if exc.is_name and exc.entry.is_builtin:
                self.builtin_exc_name = exc.name
                if self.builtin_exc_name == 'MemoryError':
                    self.exc_type = None # has a separate implementation

    nogil_check = Node.gil_error
    gil_message = "Raising exception"

    def generate_execution_code(self, code):
        if self.builtin_exc_name == 'MemoryError':
            code.putln('PyErr_NoMemory(); %s' % code.error_goto(self.pos))
            return

        if self.exc_type:
            self.exc_type.generate_evaluation_code(code)
            type_code = self.exc_type.py_result()
        else:
            type_code = "0"
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
        code.globalstate.use_utility_code(raise_utility_code)
        code.putln(
            "__Pyx_Raise(%s, %s, %s);" % (
                type_code,
                value_code,
                tb_code))
        for obj in (self.exc_type, self.exc_value, self.exc_tb):
            if obj:
                obj.generate_disposal_code(code)
                obj.free_temps(code)
        code.putln(
            code.error_goto(self.pos))

    def generate_function_definitions(self, env, code):
        if self.exc_type is not None:
            self.exc_type.generate_function_definitions(env, code)
        if self.exc_value is not None:
            self.exc_value.generate_function_definitions(env, code)
        if self.exc_tb is not None:
            self.exc_tb.generate_function_definitions(env, code)

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
        env.use_utility_code(restore_exception_utility_code)

    nogil_check = Node.gil_error
    gil_message = "Raising exception"

    def generate_execution_code(self, code):
        vars = code.funcstate.exc_vars
        if vars:
            for varname in vars:
                code.put_giveref(varname)
            code.putln("__Pyx_ErrRestore(%s, %s, %s);" % tuple(vars))
            for varname in vars:
                code.put("%s = 0; " % varname)
            code.putln()
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

    nogil_check = Node.gil_error
    gil_message = "Raising exception"

    def generate_execution_code(self, code):
        code.putln("#ifndef CYTHON_WITHOUT_ASSERTIONS")
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
            self.value.free_temps(code)
        else:
            code.putln(
                "PyErr_SetNone(PyExc_AssertionError);")
        code.putln(
                code.error_goto(self.pos))
        code.putln(
            "}")
        self.cond.generate_disposal_code(code)
        self.cond.free_temps(code)
        code.putln("#endif")

    def generate_function_definitions(self, env, code):
        self.cond.generate_function_definitions(env, code)
        if self.value is not None:
            self.value.generate_function_definitions(env, code)

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

    def generate_function_definitions(self, env, code):
        for clause in self.if_clauses:
            clause.generate_function_definitions(env, code)
        if self.else_clause is not None:
            self.else_clause.generate_function_definitions(env, code)

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
        self.body.analyse_declarations(env)

    def analyse_expressions(self, env):
        self.condition = \
            self.condition.analyse_temp_boolean_expression(env)
        self.body.analyse_expressions(env)

    def get_constant_condition_result(self):
        if self.condition.has_constant_result():
            return bool(self.condition.constant_result)
        else:
            return None

    def generate_execution_code(self, code, end_label):
        self.condition.generate_evaluation_code(code)
        code.putln(
            "if (%s) {" %
                self.condition.result())
        self.condition.generate_disposal_code(code)
        self.condition.free_temps(code)
        self.body.generate_execution_code(code)
        code.put_goto(end_label)
        code.putln("}")

    def generate_function_definitions(self, env, code):
        self.condition.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)

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
            code.mark_pos(cond.pos)
            cond.generate_evaluation_code(code)
            code.putln("case %s:" % cond.result())
        self.body.generate_execution_code(code)
        code.putln("break;")

    def generate_function_definitions(self, env, code):
        for cond in self.conditions:
            cond.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)

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
        self.test.generate_evaluation_code(code)
        code.putln("switch (%s) {" % self.test.result())
        for case in self.cases:
            case.generate_execution_code(code)
        if self.else_clause is not None:
            code.putln("default:")
            self.else_clause.generate_execution_code(code)
            code.putln("break;")
        code.putln("}")

    def generate_function_definitions(self, env, code):
        self.test.generate_function_definitions(env, code)
        for case in self.cases:
            case.generate_function_definitions(env, code)
        if self.else_clause is not None:
            self.else_clause.generate_function_definitions(env, code)

    def annotate(self, code):
        self.test.annotate(code)
        for case in self.cases:
            case.annotate(code)
        if self.else_clause is not None:
            self.else_clause.annotate(code)

class LoopNode(object):

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
        self.body.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)

    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        code.putln(
            "while (1) {")
        self.condition.generate_evaluation_code(code)
        self.condition.generate_disposal_code(code)
        code.putln(
            "if (!%s) break;" %
                self.condition.result())
        self.condition.free_temps(code)
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

    def generate_function_definitions(self, env, code):
        self.condition.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)
        if self.else_clause is not None:
            self.else_clause.generate_function_definitions(env, code)

    def annotate(self, code):
        self.condition.annotate(code)
        self.body.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)


def ForStatNode(pos, **kw):
    if 'iterator' in kw:
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

    def analyse_expressions(self, env):
        import ExprNodes
        self.target.analyse_target_types(env)
        self.iterator.analyse_expressions(env)
        self.item = ExprNodes.NextNode(self.iterator, env)
        if (self.iterator.type.is_ptr or self.iterator.type.is_array) and \
            self.target.type.assignable_from(self.iterator.type):
            # C array slice optimization.
            pass
        else:
            self.item = self.item.coerce_to(self.target.type, env)
        self.body.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)

    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        self.iterator.allocate_counter_temp(code)
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
            # in nested loops, the 'else' block can contain a
            # 'continue' statement for the outer loop, but we may need
            # to generate cleanup code before taking that path, so we
            # intercept it here
            orig_continue_label = code.continue_label
            code.continue_label = code.new_label('outer_continue')

            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")

            if code.label_used(code.continue_label):
                code.put_goto(break_label)
                code.put_label(code.continue_label)
                self.iterator.generate_disposal_code(code)
                code.put_goto(orig_continue_label)
            code.set_loop_labels(old_loop_labels)

        if code.label_used(break_label):
            code.put_label(break_label)
        self.iterator.release_counter_temp(code)
        self.iterator.generate_disposal_code(code)
        self.iterator.free_temps(code)

    def generate_function_definitions(self, env, code):
        self.target.generate_function_definitions(env, code)
        self.iterator.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)
        if self.else_clause is not None:
            self.else_clause.generate_function_definitions(env, code)

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
    #  from_range         bool
    #  is_py_target       bool
    #  loopvar_node       ExprNode (usually a NameNode or temp node)
    #  py_loopvar_node    PyTempNode or None
    child_attrs = ["target", "bound1", "bound2", "step", "body", "else_clause"]

    is_py_target = False
    loopvar_node = None
    py_loopvar_node = None
    from_range = False

    gil_message = "For-loop using object bounds or target"

    def nogil_check(self, env):
        for x in (self.target, self.bound1, self.bound2):
            if x.type.is_pyobject:
                self.gil_error()

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
        if self.step is not None:
            if isinstance(self.step, ExprNodes.UnaryMinusNode):
                warning(self.step.pos, "Probable infinite loop in for-from-by statment. Consider switching the directions of the relations.", 2)
            self.step.analyse_types(env)

        target_type = self.target.type
        if self.target.type.is_numeric:
            loop_type = self.target.type
        else:
            loop_type = PyrexTypes.c_int_type
            if not self.bound1.type.is_pyobject:
                loop_type = PyrexTypes.widest_numeric_type(loop_type, self.bound1.type)
            if not self.bound2.type.is_pyobject:
                loop_type = PyrexTypes.widest_numeric_type(loop_type, self.bound2.type)
            if self.step is not None and not self.step.type.is_pyobject:
                loop_type = PyrexTypes.widest_numeric_type(loop_type, self.step.type)
        self.bound1 = self.bound1.coerce_to(loop_type, env)
        self.bound2 = self.bound2.coerce_to(loop_type, env)
        if not self.bound2.is_literal:
            self.bound2 = self.bound2.coerce_to_temp(env)
        if self.step is not None:
            self.step = self.step.coerce_to(loop_type, env)
            if not self.step.is_literal:
                self.step = self.step.coerce_to_temp(env)

        target_type = self.target.type
        if not (target_type.is_pyobject or target_type.is_numeric):
            error(self.target.pos,
                "for-from loop variable must be c numeric type or Python object")
        if target_type.is_numeric:
            self.is_py_target = False
            if isinstance(self.target, ExprNodes.IndexNode) and self.target.is_buffer_access:
                raise error(self.pos, "Buffer indexing not allowed as for loop target.")
            self.loopvar_node = self.target
            self.py_loopvar_node = None
        else:
            self.is_py_target = True
            c_loopvar_node = ExprNodes.TempNode(self.pos, loop_type, env)
            self.loopvar_node = c_loopvar_node
            self.py_loopvar_node = \
                ExprNodes.CloneNode(c_loopvar_node).coerce_to_pyobject(env)
        self.body.analyse_expressions(env)
        if self.else_clause:
            self.else_clause.analyse_expressions(env)

    def generate_execution_code(self, code):
        old_loop_labels = code.new_loop_labels()
        from_range = self.from_range
        self.bound1.generate_evaluation_code(code)
        self.bound2.generate_evaluation_code(code)
        offset, incop = self.relation_table[self.relation1]
        if self.step is not None:
            self.step.generate_evaluation_code(code)
            step = self.step.result()
            incop = "%s=%s" % (incop[0], step)
        import ExprNodes
        if isinstance(self.loopvar_node, ExprNodes.TempNode):
            self.loopvar_node.allocate(code)
        if isinstance(self.py_loopvar_node, ExprNodes.TempNode):
            self.py_loopvar_node.allocate(code)
        if from_range:
            loopvar_name = code.funcstate.allocate_temp(self.target.type, False)
        else:
            loopvar_name = self.loopvar_node.result()
        code.putln(
            "for (%s = %s%s; %s %s %s; %s%s) {" % (
                loopvar_name,
                self.bound1.result(), offset,
                loopvar_name, self.relation2, self.bound2.result(),
                loopvar_name, incop))
        if self.py_loopvar_node:
            self.py_loopvar_node.generate_evaluation_code(code)
            self.target.generate_assignment_code(self.py_loopvar_node, code)
        elif from_range:
            code.putln("%s = %s;" % (
                            self.target.result(), loopvar_name))
        self.body.generate_execution_code(code)
        code.put_label(code.continue_label)
        if self.py_loopvar_node:
            # This mess is to make for..from loops with python targets behave
            # exactly like those with C targets with regards to re-assignment
            # of the loop variable.
            import ExprNodes
            if self.target.entry.is_pyglobal:
                # We know target is a NameNode, this is the only ugly case.
                target_node = ExprNodes.PyTempNode(self.target.pos, None)
                target_node.allocate(code)
                interned_cname = code.intern_identifier(self.target.entry.name)
                code.globalstate.use_utility_code(ExprNodes.get_name_interned_utility_code)
                code.putln("%s = __Pyx_GetName(%s, %s); %s" % (
                                target_node.result(),
                                Naming.module_cname,
                                interned_cname,
                                code.error_goto_if_null(target_node.result(), self.target.pos)))
                code.put_gotref(target_node.result())
            else:
                target_node = self.target
            from_py_node = ExprNodes.CoerceFromPyTypeNode(self.loopvar_node.type, target_node, None)
            from_py_node.temp_code = loopvar_name
            from_py_node.generate_result_code(code)
            if self.target.entry.is_pyglobal:
                code.put_decref(target_node.result(), target_node.type)
                target_node.release(code)
        code.putln("}")
        if self.py_loopvar_node:
            # This is potentially wasteful, but we don't want the semantics to
            # depend on whether or not the loop is a python type.
            self.py_loopvar_node.generate_evaluation_code(code)
            self.target.generate_assignment_code(self.py_loopvar_node, code)
        if from_range:
            code.funcstate.release_temp(loopvar_name)
        break_label = code.break_label
        code.set_loop_labels(old_loop_labels)
        if self.else_clause:
            code.putln("/*else*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln("}")
        code.put_label(break_label)
        self.bound1.generate_disposal_code(code)
        self.bound1.free_temps(code)
        self.bound2.generate_disposal_code(code)
        self.bound2.free_temps(code)
        if isinstance(self.loopvar_node, ExprNodes.TempNode):
            self.loopvar_node.release(code)
        if isinstance(self.py_loopvar_node, ExprNodes.TempNode):
            self.py_loopvar_node.release(code)
        if self.step is not None:
            self.step.generate_disposal_code(code)
            self.step.free_temps(code)

    relation_table = {
        # {relop : (initial offset, increment op)}
        '<=': ("",   "++"),
        '<' : ("+1", "++"),
        '>=': ("",   "--"),
        '>' : ("-1", "--")
    }

    def generate_function_definitions(self, env, code):
        self.target.generate_function_definitions(env, code)
        self.bound1.generate_function_definitions(env, code)
        self.bound2.generate_function_definitions(env, code)
        if self.step is not None:
            self.step.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)
        if self.else_clause is not None:
            self.else_clause.generate_function_definitions(env, code)

    def annotate(self, code):
        self.target.annotate(code)
        self.bound1.annotate(code)
        self.bound2.annotate(code)
        if self.step:
            self.step.annotate(code)
        self.body.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)


class WithStatNode(StatNode):
    """
    Represents a Python with statement.

    Implemented by the WithTransform as follows:

        MGR = EXPR
        EXIT = MGR.__exit__
        VALUE = MGR.__enter__()
        EXC = True
        try:
            try:
                TARGET = VALUE  # optional
                BODY
            except:
                EXC = False
                if not EXIT(*EXCINFO):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
            MGR = EXIT = VALUE = None
    """
    #  manager          The with statement manager object
    #  target           ExprNode  the target lhs of the __enter__() call
    #  body             StatNode

    child_attrs = ["manager", "target", "body"]

    has_target = False

    def analyse_declarations(self, env):
        self.manager.analyse_declarations(env)
        self.body.analyse_declarations(env)

    def analyse_expressions(self, env):
        self.manager.analyse_types(env)
        self.body.analyse_expressions(env)

    def generate_function_definitions(self, env, code):
        self.manager.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)

    def generate_execution_code(self, code):
        code.putln("/*with:*/ {")
        self.manager.generate_evaluation_code(code)
        self.exit_var = code.funcstate.allocate_temp(py_object_type, manage_ref=False)
        code.putln("%s = PyObject_GetAttr(%s, %s); %s" % (
            self.exit_var,
            self.manager.py_result(),
            code.get_py_string_const(EncodedString('__exit__'), identifier=True),
            code.error_goto_if_null(self.exit_var, self.pos),
            ))
        code.put_gotref(self.exit_var)

        # need to free exit_var in the face of exceptions during setup
        old_error_label = code.new_error_label()
        intermediate_error_label = code.error_label

        enter_func = code.funcstate.allocate_temp(py_object_type, manage_ref=True)
        code.putln("%s = PyObject_GetAttr(%s, %s); %s" % (
            enter_func,
            self.manager.py_result(),
            code.get_py_string_const(EncodedString('__enter__'), identifier=True),
            code.error_goto_if_null(enter_func, self.pos),
            ))
        code.put_gotref(enter_func)
        self.manager.generate_disposal_code(code)
        self.manager.free_temps(code)
        self.target_temp.allocate(code)
        code.putln('%s = PyObject_Call(%s, ((PyObject *)%s), NULL); %s' % (
            self.target_temp.result(),
            enter_func,
            Naming.empty_tuple,
            code.error_goto_if_null(self.target_temp.result(), self.pos),
            ))
        code.put_gotref(self.target_temp.result())
        code.put_decref_clear(enter_func, py_object_type)
        code.funcstate.release_temp(enter_func)
        if not self.has_target:
            code.put_decref_clear(self.target_temp.result(), type=py_object_type)
            self.target_temp.release(code)
            # otherwise, WithTargetAssignmentStatNode will do it for us

        code.error_label = old_error_label
        self.body.generate_execution_code(code)

        step_over_label = code.new_label()
        code.put_goto(step_over_label)
        code.put_label(intermediate_error_label)
        code.put_decref_clear(self.exit_var, py_object_type)
        code.put_goto(old_error_label)
        code.put_label(step_over_label)

        code.funcstate.release_temp(self.exit_var)
        code.putln('}')

class WithTargetAssignmentStatNode(AssignmentNode):
    # The target assignment of the 'with' statement value (return
    # value of the __enter__() call).
    #
    # This is a special cased assignment that steals the RHS reference
    # and frees its temp.
    #
    # lhs  ExprNode  the assignment target
    # rhs  TempNode  the return value of the __enter__() call

    child_attrs = ["lhs", "rhs"]

    def analyse_declarations(self, env):
        self.lhs.analyse_target_declaration(env)

    def analyse_types(self, env):
        self.rhs.analyse_types(env)
        self.lhs.analyse_target_types(env)
        self.lhs.gil_assignment_check(env)
        self.orig_rhs = self.rhs
        self.rhs = self.rhs.coerce_to(self.lhs.type, env)

    def generate_execution_code(self, code):
        self.rhs.generate_evaluation_code(code)
        self.lhs.generate_assignment_code(self.rhs, code)
        self.orig_rhs.release(code)

    def generate_function_definitions(self, env, code):
        self.rhs.generate_function_definitions(env, code)

    def annotate(self, code):
        self.lhs.annotate(code)
        self.rhs.annotate(code)


class TryExceptStatNode(StatNode):
    #  try .. except statement
    #
    #  body             StatNode
    #  except_clauses   [ExceptClauseNode]
    #  else_clause      StatNode or None

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
        env.use_utility_code(reset_exception_utility_code)

    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
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

    nogil_check = Node.gil_error
    gil_message = "Try-except statement"

    def generate_execution_code(self, code):
        old_return_label = code.return_label
        old_break_label = code.break_label
        old_continue_label = code.continue_label
        old_error_label = code.new_error_label()
        our_error_label = code.error_label
        except_end_label = code.new_label('exception_handled')
        except_error_label = code.new_label('except_error')
        except_return_label = code.new_label('except_return')
        try_return_label = code.new_label('try_return')
        try_break_label = code.new_label('try_break')
        try_continue_label = code.new_label('try_continue')
        try_end_label = code.new_label('try_end')

        exc_save_vars = [code.funcstate.allocate_temp(py_object_type, False)
                         for i in xrange(3)]
        code.putln("{")
        code.putln("__Pyx_ExceptionSave(%s);" %
                   ', '.join(['&%s' % var for var in exc_save_vars]))
        for var in exc_save_vars:
            code.put_xgotref(var)
        code.putln(
            "/*try:*/ {")
        code.return_label = try_return_label
        code.break_label = try_break_label
        code.continue_label = try_continue_label
        self.body.generate_execution_code(code)
        code.putln(
            "}")
        temps_to_clean_up = code.funcstate.all_free_managed_temps()
        code.error_label = except_error_label
        code.return_label = except_return_label
        if self.else_clause:
            code.putln(
                "/*else:*/ {")
            self.else_clause.generate_execution_code(code)
            code.putln(
                "}")
        for var in exc_save_vars:
            code.put_xdecref_clear(var, py_object_type)
        code.put_goto(try_end_label)
        if code.label_used(try_return_label):
            code.put_label(try_return_label)
            for var in exc_save_vars:
                code.put_xgiveref(var)
            code.putln("__Pyx_ExceptionReset(%s);" %
                       ', '.join(exc_save_vars))
            code.put_goto(old_return_label)
        code.put_label(our_error_label)
        for temp_name, type in temps_to_clean_up:
            code.put_xdecref_clear(temp_name, type)
        for except_clause in self.except_clauses:
            except_clause.generate_handling_code(code, except_end_label)

        error_label_used = code.label_used(except_error_label)
        if error_label_used or not self.has_default_clause:
            if error_label_used:
                code.put_label(except_error_label)
            for var in exc_save_vars:
                code.put_xgiveref(var)
            code.putln("__Pyx_ExceptionReset(%s);" %
                       ', '.join(exc_save_vars))
            code.put_goto(old_error_label)

        for exit_label, old_label in zip(
            [try_break_label, try_continue_label, except_return_label],
            [old_break_label, old_continue_label, old_return_label]):

            if code.label_used(exit_label):
                code.put_label(exit_label)
                for var in exc_save_vars:
                    code.put_xgiveref(var)
                code.putln("__Pyx_ExceptionReset(%s);" %
                           ', '.join(exc_save_vars))
                code.put_goto(old_label)

        if code.label_used(except_end_label):
            code.put_label(except_end_label)
            for var in exc_save_vars:
                code.put_xgiveref(var)
            code.putln("__Pyx_ExceptionReset(%s);" %
                       ', '.join(exc_save_vars))
        code.put_label(try_end_label)
        code.putln("}")

        for cname in exc_save_vars:
            code.funcstate.release_temp(cname)

        code.return_label = old_return_label
        code.break_label = old_break_label
        code.continue_label = old_continue_label
        code.error_label = old_error_label

    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)
        for except_clause in self.except_clauses:
            except_clause.generate_function_definitions(env, code)
        if self.else_clause is not None:
            self.else_clause.generate_function_definitions(env, code)

    def annotate(self, code):
        self.body.annotate(code)
        for except_node in self.except_clauses:
            except_node.annotate(code)
        if self.else_clause:
            self.else_clause.annotate(code)


class ExceptClauseNode(Node):
    #  Part of try ... except statement.
    #
    #  pattern        [ExprNode]
    #  target         ExprNode or None
    #  body           StatNode
    #  excinfo_target ResultRefNode or None   optional target for exception info
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
        self.body.analyse_declarations(env)

    def analyse_expressions(self, env):
        import ExprNodes
        genv = env.global_scope()
        self.function_name = env.qualified_name
        if self.pattern:
            # normalise/unpack self.pattern into a list
            for i, pattern in enumerate(self.pattern):
                pattern.analyse_expressions(env)
                self.pattern[i] = pattern.coerce_to_pyobject(env)

        if self.target:
            self.exc_value = ExprNodes.ExcValueNode(self.pos, env)
            self.target.analyse_target_expression(env, self.exc_value)
        if self.excinfo_target is not None:
            import ExprNodes
            self.excinfo_tuple = ExprNodes.TupleNode(pos=self.pos, args=[
                ExprNodes.ExcValueNode(pos=self.pos, env=env) for x in range(3)])
            self.excinfo_tuple.analyse_expressions(env)

        self.body.analyse_expressions(env)

    def generate_handling_code(self, code, end_label):
        code.mark_pos(self.pos)
        if self.pattern:
            exc_tests = []
            for pattern in self.pattern:
                pattern.generate_evaluation_code(code)
                exc_tests.append("PyErr_ExceptionMatches(%s)" % pattern.py_result())

            match_flag = code.funcstate.allocate_temp(PyrexTypes.c_int_type, False)
            code.putln(
                "%s = %s;" % (match_flag, ' || '.join(exc_tests)))
            for pattern in self.pattern:
                pattern.generate_disposal_code(code)
                pattern.free_temps(code)
            code.putln(
                "if (%s) {" %
                    match_flag)
            code.funcstate.release_temp(match_flag)
        else:
            code.putln("/*except:*/ {")

        if not getattr(self.body, 'stats', True) and \
                self.excinfo_target is None and self.target is None:
            # most simple case: no exception variable, empty body (pass)
            # => reset the exception state, done
            code.putln("PyErr_Restore(0,0,0);")
            code.put_goto(end_label)
            code.putln("}")
            return

        exc_vars = [code.funcstate.allocate_temp(py_object_type,
                                                 manage_ref=True)
                    for i in xrange(3)]
        code.putln('__Pyx_AddTraceback("%s");' % self.function_name)
        # We always have to fetch the exception value even if
        # there is no target, because this also normalises the
        # exception and stores it in the thread state.
        code.globalstate.use_utility_code(get_exception_utility_code)
        exc_args = "&%s, &%s, &%s" % tuple(exc_vars)
        code.putln("if (__Pyx_GetException(%s) < 0) %s" % (exc_args,
            code.error_goto(self.pos)))
        for x in exc_vars:
            code.put_gotref(x)
        if self.target:
            self.exc_value.set_var(exc_vars[1])
            self.exc_value.generate_evaluation_code(code)
            self.target.generate_assignment_code(self.exc_value, code)
        if self.excinfo_target is not None:
            for tempvar, node in zip(exc_vars, self.excinfo_tuple.args):
                node.set_var(tempvar)
            self.excinfo_tuple.generate_evaluation_code(code)
            self.excinfo_target.result_code = self.excinfo_tuple.result()

        old_break_label, old_continue_label = code.break_label, code.continue_label
        code.break_label = code.new_label('except_break')
        code.continue_label = code.new_label('except_continue')

        old_exc_vars = code.funcstate.exc_vars
        code.funcstate.exc_vars = exc_vars
        self.body.generate_execution_code(code)
        code.funcstate.exc_vars = old_exc_vars
        if self.excinfo_target is not None:
            self.excinfo_tuple.generate_disposal_code(code)
        for var in exc_vars:
            code.put_decref_clear(var, py_object_type)
        code.put_goto(end_label)

        if code.label_used(code.break_label):
            code.put_label(code.break_label)
            if self.excinfo_target is not None:
                self.excinfo_tuple.generate_disposal_code(code)
            for var in exc_vars:
                code.put_decref_clear(var, py_object_type)
            code.put_goto(old_break_label)
        code.break_label = old_break_label

        if code.label_used(code.continue_label):
            code.put_label(code.continue_label)
            if self.excinfo_target is not None:
                self.excinfo_tuple.generate_disposal_code(code)
            for var in exc_vars:
                code.put_decref_clear(var, py_object_type)
            code.put_goto(old_continue_label)
        code.continue_label = old_continue_label

        if self.excinfo_target is not None:
            self.excinfo_tuple.free_temps(code)
        for temp in exc_vars:
            code.funcstate.release_temp(temp)

        code.putln(
            "}")

    def generate_function_definitions(self, env, code):
        if self.target is not None:
            self.target.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)

    def annotate(self, code):
        if self.pattern:
            for pattern in self.pattern:
                pattern.annotate(code)
        if self.target:
            self.target.annotate(code)
        self.body.annotate(code)


class TryFinallyStatNode(StatNode):
    #  try ... finally statement
    #
    #  body             StatNode
    #  finally_clause   StatNode
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

    # handle exception case, in addition to return/break/continue
    handle_error_case = True

    disallow_continue_in_try_finally = 0
    # There doesn't seem to be any point in disallowing
    # continue in the try block, since we have no problem
    # handling it.

    def create_analysed(pos, env, body, finally_clause):
        node = TryFinallyStatNode(pos, body=body, finally_clause=finally_clause)
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
        self.finally_clause.analyse_expressions(env)

    nogil_check = Node.gil_error
    gil_message = "Try-finally statement"

    def generate_execution_code(self, code):
        old_error_label = code.error_label
        old_labels = code.all_new_labels()
        new_labels = code.get_all_labels()
        new_error_label = code.error_label
        if not self.handle_error_case:
            code.error_label = old_error_label
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
        temps_to_clean_up = code.funcstate.all_free_managed_temps()
        code.mark_pos(self.finally_clause.pos)
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
                        new_error_label, i+1, catch_label, temps_to_clean_up)
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

    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)
        self.finally_clause.generate_function_definitions(env, code)

    def put_error_catcher(self, code, error_label, i, catch_label, temps_to_clean_up):
        code.globalstate.use_utility_code(restore_exception_utility_code)
        code.putln(
            "%s: {" %
                error_label)
        code.putln(
                "__pyx_why = %s;" %
                    i)
        for temp_name, type in temps_to_clean_up:
            code.put_xdecref_clear(temp_name, type)
        code.putln(
                "__Pyx_ErrFetch(&%s, &%s, &%s);" %
                    Naming.exc_vars)
        code.putln(
                "%s = %s;" % (
                    Naming.exc_lineno_name, Naming.lineno_cname))
        code.put_goto(catch_label)
        code.putln("}")

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

#    child_attrs = []

    preserve_exception = 0

    def __init__(self, pos, state, body):
        self.state = state
        TryFinallyStatNode.__init__(self, pos,
            body = body,
            finally_clause = GILExitNode(pos, state = state))

    def analyse_expressions(self, env):
        env.use_utility_code(force_init_threads_utility_code)
        was_nogil = env.nogil
        env.nogil = 1
        TryFinallyStatNode.analyse_expressions(self, env)
        env.nogil = was_nogil

    nogil_check = None

    def generate_execution_code(self, code):
        code.mark_pos(self.pos)
        code.putln("{")
        if self.state == 'gil':
            code.putln("#ifdef WITH_THREAD")
            code.putln("PyGILState_STATE _save = PyGILState_Ensure();")
            code.putln("#endif")
        else:
            code.putln("#ifdef WITH_THREAD")
            code.putln("PyThreadState *_save = NULL;")
            code.putln("#endif")
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
            code.putln("#ifdef WITH_THREAD")
            code.putln("PyGILState_Release(_save);")
            code.putln("#endif")
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
                        submodule_scope = env.context.find_module(name, relative_to = module_scope, pos = self.pos)
                        if submodule_scope.parent_module is module_scope:
                            env.declare_module(as_name or name, submodule_scope, self.pos)
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
            if kind != type.kind:
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
    #  interned_items   [(string, NameNode, ExprNode)]
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
        self.item = ExprNodes.RawCNameExprNode(self.pos, py_object_type)
        self.interned_items = []
        for name, target in self.items:
            if name == '*':
                for _, entry in env.entries.items():
                    if not entry.is_type and entry.type.is_extension_type:
                        env.use_utility_code(ExprNodes.type_test_utility_code)
                        break
            else:
                entry =  env.lookup(target.name)
                # check whether or not entry is already cimported
                if (entry.is_type and entry.type.name == name
                    and hasattr(entry.type, 'module_name')):
                    if entry.type.module_name == self.module.module_name.value:
                        # cimported with absolute name
                        continue
                    try:
                        # cimported with relative name
                        module = env.find_module(self.module.module_name.value,
                                                 pos=None)
                        if entry.type.module_name == module.qualified_name:
                            continue
                    except AttributeError:
                        pass
                target.analyse_target_expression(env, None)
                if target.type is py_object_type:
                    coerced_item = None
                else:
                    coerced_item = self.item.coerce_to(target.type, env)
                self.interned_items.append((name, target, coerced_item))

    def generate_execution_code(self, code):
        self.module.generate_evaluation_code(code)
        if self.import_star:
            code.putln(
                'if (%s(%s) < 0) %s;' % (
                    Naming.import_star,
                    self.module.py_result(),
                    code.error_goto(self.pos)))
        item_temp = code.funcstate.allocate_temp(py_object_type, manage_ref=True)
        self.item.set_cname(item_temp)
        for name, target, coerced_item in self.interned_items:
            cname = code.intern_identifier(name)
            code.putln(
                '%s = PyObject_GetAttr(%s, %s); %s' % (
                    item_temp,
                    self.module.py_result(),
                    cname,
                    code.error_goto_if_null(item_temp, self.pos)))
            code.put_gotref(item_temp)
            if coerced_item is None:
                target.generate_assignment_code(self.item, code)
            else:
                coerced_item.allocate_temp_result(code)
                coerced_item.generate_result_code(code)
                target.generate_assignment_code(coerced_item, code)
            code.put_decref_clear(item_temp, py_object_type)
        code.funcstate.release_temp(item_temp)
        self.module.generate_disposal_code(code)
        self.module.free_temps(code)



#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

utility_function_predeclarations = \
"""
/* inline attribute */
#ifndef CYTHON_INLINE
  #if defined(__GNUC__)
    #define CYTHON_INLINE __inline__
  #elif defined(_MSC_VER)
    #define CYTHON_INLINE __inline
  #elif defined (__STDC_VERSION__) && __STDC_VERSION__ >= 199901L
    #define CYTHON_INLINE inline
  #else
    #define CYTHON_INLINE
  #endif
#endif

/* unused attribute */
#ifndef CYTHON_UNUSED
# if defined(__GNUC__)
#   if !(defined(__cplusplus)) || (__GNUC__ > 3 || (__GNUC__ == 3 && __GNUC_MINOR__ >= 4))
#     define CYTHON_UNUSED __attribute__ ((__unused__))
#   else
#     define CYTHON_UNUSED
#   endif
# elif defined(__ICC) || defined(__INTEL_COMPILER)
#   define CYTHON_UNUSED __attribute__ ((__unused__))
# else
#   define CYTHON_UNUSED
# endif
#endif

typedef struct {PyObject **p; char *s; const long n; const char* encoding; const char is_unicode; const char is_str; const char intern; } __Pyx_StringTabEntry; /*proto*/

"""

if Options.gcc_branch_hints:
    branch_prediction_macros = \
    """
#ifdef __GNUC__
/* Test for GCC > 2.95 */
#if __GNUC__ > 2 || (__GNUC__ == 2 && (__GNUC_MINOR__ > 95))
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
static int __Pyx_Print(PyObject*, PyObject *, int); /*proto*/
#if PY_MAJOR_VERSION >= 3
static PyObject* %s = 0;
static PyObject* %s = 0;
#endif
""" % (Naming.print_function, Naming.print_function_kwargs),
cleanup = """
#if PY_MAJOR_VERSION >= 3
Py_CLEAR(%s);
Py_CLEAR(%s);
#endif
""" % (Naming.print_function, Naming.print_function_kwargs),
impl = r"""
#if PY_MAJOR_VERSION < 3
static PyObject *__Pyx_GetStdout(void) {
    PyObject *f = PySys_GetObject((char *)"stdout");
    if (!f) {
        PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
    }
    return f;
}

static int __Pyx_Print(PyObject* f, PyObject *arg_tuple, int newline) {
    PyObject* v;
    int i;

    if (!f) {
        if (!(f = __Pyx_GetStdout()))
            return -1;
    }
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

static int __Pyx_Print(PyObject* stream, PyObject *arg_tuple, int newline) {
    PyObject* kwargs = 0;
    PyObject* result = 0;
    PyObject* end_string;
    if (unlikely(!%(PRINT_FUNCTION)s)) {
        %(PRINT_FUNCTION)s = __Pyx_GetAttrString(%(BUILTINS)s, "print");
        if (!%(PRINT_FUNCTION)s)
            return -1;
    }
    if (stream) {
        kwargs = PyDict_New();
        if (unlikely(!kwargs))
            return -1;
        if (unlikely(PyDict_SetItemString(kwargs, "file", stream) < 0))
            goto bad;
        if (!newline) {
            end_string = PyUnicode_FromStringAndSize(" ", 1);
            if (unlikely(!end_string))
                goto bad;
            if (PyDict_SetItemString(kwargs, "end", end_string) < 0) {
                Py_DECREF(end_string);
                goto bad;
            }
            Py_DECREF(end_string);
        }
    } else if (!newline) {
        if (unlikely(!%(PRINT_KWARGS)s)) {
            %(PRINT_KWARGS)s = PyDict_New();
            if (unlikely(!%(PRINT_KWARGS)s))
                return -1;
            end_string = PyUnicode_FromStringAndSize(" ", 1);
            if (unlikely(!end_string))
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
    if (unlikely(kwargs) && (kwargs != %(PRINT_KWARGS)s))
        Py_DECREF(kwargs);
    if (!result)
        return -1;
    Py_DECREF(result);
    return 0;
bad:
    if (kwargs != %(PRINT_KWARGS)s)
        Py_XDECREF(kwargs);
    return -1;
}

#endif
""" % {'BUILTINS'       : Naming.builtins_cname,
       'PRINT_FUNCTION' : Naming.print_function,
       'PRINT_KWARGS'   : Naming.print_function_kwargs}
)


printing_one_utility_code = UtilityCode(
proto = """
static int __Pyx_PrintOne(PyObject* stream, PyObject *o); /*proto*/
""",
impl = r"""
#if PY_MAJOR_VERSION < 3

static int __Pyx_PrintOne(PyObject* f, PyObject *o) {
    if (!f) {
        if (!(f = __Pyx_GetStdout()))
            return -1;
    }
    if (PyFile_SoftSpace(f, 0)) {
        if (PyFile_WriteString(" ", f) < 0)
            return -1;
    }
    if (PyFile_WriteObject(o, f, Py_PRINT_RAW) < 0)
        return -1;
    if (PyFile_WriteString("\n", f) < 0)
        return -1;
    return 0;
    /* the line below is just to avoid compiler
     * compiler warnings about unused functions */
    return __Pyx_Print(f, NULL, 0);
}

#else /* Python 3 has a print function */

static int __Pyx_PrintOne(PyObject* stream, PyObject *o) {
    int res;
    PyObject* arg_tuple = PyTuple_New(1);
    if (unlikely(!arg_tuple))
        return -1;
    Py_INCREF(o);
    PyTuple_SET_ITEM(arg_tuple, 0, o);
    res = __Pyx_Print(stream, arg_tuple, 1);
    Py_DECREF(arg_tuple);
    return res;
}

#endif
""",
requires=[printing_utility_code])



#------------------------------------------------------------------------------------

# Exception raising code
#
# Exceptions are raised by __Pyx_Raise() and stored as plain
# type/value/tb in PyThreadState->curexc_*.  When being caught by an
# 'except' statement, curexc_* is moved over to exc_* by
# __Pyx_GetException()

restore_exception_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_ErrRestore(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
static CYTHON_INLINE void __Pyx_ErrFetch(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
""",
impl = """
static CYTHON_INLINE void __Pyx_ErrRestore(PyObject *type, PyObject *value, PyObject *tb) {
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

static CYTHON_INLINE void __Pyx_ErrFetch(PyObject **type, PyObject **value, PyObject **tb) {
    PyThreadState *tstate = PyThreadState_GET();
    *type = tstate->curexc_type;
    *value = tstate->curexc_value;
    *tb = tstate->curexc_traceback;

    tstate->curexc_type = 0;
    tstate->curexc_value = 0;
    tstate->curexc_traceback = 0;
}

""")

# The following function is based on do_raise() from ceval.c. There
# are separate versions for Python2 and Python3 as exception handling
# has changed quite a lot between the two versions.

raise_utility_code = UtilityCode(
proto = """
static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
""",
impl = """
#if PY_MAJOR_VERSION < 3
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

#else /* Python 3+ */

static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb) {
    if (tb == Py_None) {
        tb = 0;
    } else if (tb && !PyTraceBack_Check(tb)) {
        PyErr_SetString(PyExc_TypeError,
            "raise: arg 3 must be a traceback or None");
        goto bad;
    }
    if (value == Py_None)
        value = 0;

    if (PyExceptionInstance_Check(type)) {
        if (value) {
            PyErr_SetString(PyExc_TypeError,
                "instance exception may not have a separate value");
            goto bad;
        }
        value = type;
        type = (PyObject*) Py_TYPE(value);
    } else if (!PyExceptionClass_Check(type)) {
        PyErr_SetString(PyExc_TypeError,
            "raise: exception class must be a subclass of BaseException");
        goto bad;
    }

    PyErr_SetObject(type, value);

    if (tb) {
        PyThreadState *tstate = PyThreadState_GET();
        PyObject* tmp_tb = tstate->curexc_traceback;
        if (tb != tmp_tb) {
            Py_INCREF(tb);
            tstate->curexc_traceback = tb;
            Py_XDECREF(tmp_tb);
        }
    }

bad:
    return;
}
#endif
""",
requires=[restore_exception_utility_code])

#------------------------------------------------------------------------------------

get_exception_utility_code = UtilityCode(
proto = """
static int __Pyx_GetException(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
""",
impl = """
static int __Pyx_GetException(PyObject **type, PyObject **value, PyObject **tb) {
    PyObject *local_type, *local_value, *local_tb;
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_GET();
    local_type = tstate->curexc_type;
    local_value = tstate->curexc_value;
    local_tb = tstate->curexc_traceback;
    tstate->curexc_type = 0;
    tstate->curexc_value = 0;
    tstate->curexc_traceback = 0;
    PyErr_NormalizeException(&local_type, &local_value, &local_tb);
    if (unlikely(tstate->curexc_type))
        goto bad;
    #if PY_MAJOR_VERSION >= 3
    if (unlikely(PyException_SetTraceback(local_value, local_tb) < 0))
        goto bad;
    #endif
    *type = local_type;
    *value = local_value;
    *tb = local_tb;
    Py_INCREF(local_type);
    Py_INCREF(local_value);
    Py_INCREF(local_tb);
    tmp_type = tstate->exc_type;
    tmp_value = tstate->exc_value;
    tmp_tb = tstate->exc_traceback;
    tstate->exc_type = local_type;
    tstate->exc_value = local_value;
    tstate->exc_traceback = local_tb;
    /* Make sure tstate is in a consistent state when we XDECREF
       these objects (XDECREF may run arbitrary code). */
    Py_XDECREF(tmp_type);
    Py_XDECREF(tmp_value);
    Py_XDECREF(tmp_tb);
    return 0;
bad:
    *type = 0;
    *value = 0;
    *tb = 0;
    Py_XDECREF(local_type);
    Py_XDECREF(local_value);
    Py_XDECREF(local_tb);
    return -1;
}

""")

#------------------------------------------------------------------------------------

get_exception_tuple_utility_code = UtilityCode(proto="""
static PyObject *__Pyx_GetExceptionTuple(void); /*proto*/
""",
# I doubt that calling __Pyx_GetException() here is correct as it moves
# the exception from tstate->curexc_* to tstate->exc_*, which prevents
# exception handlers later on from receiving it.
impl = """
static PyObject *__Pyx_GetExceptionTuple(void) {
    PyObject *type = NULL, *value = NULL, *tb = NULL;
    if (__Pyx_GetException(&type, &value, &tb) == 0) {
        PyObject* exc_info = PyTuple_New(3);
        if (exc_info) {
            Py_INCREF(type);
            Py_INCREF(value);
            Py_INCREF(tb);
            PyTuple_SET_ITEM(exc_info, 0, type);
            PyTuple_SET_ITEM(exc_info, 1, value);
            PyTuple_SET_ITEM(exc_info, 2, tb);
            return exc_info;
        }
    }
    return NULL;
}
""",
requires=[get_exception_utility_code])

#------------------------------------------------------------------------------------

reset_exception_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_ExceptionSave(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
static void __Pyx_ExceptionReset(PyObject *type, PyObject *value, PyObject *tb); /*proto*/
""",
impl = """
static CYTHON_INLINE void __Pyx_ExceptionSave(PyObject **type, PyObject **value, PyObject **tb) {
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

swap_exception_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_ExceptionSwap(PyObject **type, PyObject **value, PyObject **tb); /*proto*/
""",
impl = """
static CYTHON_INLINE void __Pyx_ExceptionSwap(PyObject **type, PyObject **value, PyObject **tb) {
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyThreadState *tstate = PyThreadState_GET();

    tmp_type = tstate->exc_type;
    tmp_value = tstate->exc_value;
    tmp_tb = tstate->exc_traceback;

    tstate->exc_type = *type;
    tstate->exc_value = *value;
    tstate->exc_traceback = *tb;

    *type = tmp_type;
    *value = tmp_value;
    *tb = tmp_tb;
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
static CYTHON_INLINE void __Pyx_RaiseKeywordRequired(const char* func_name, PyObject* kw_name); /*proto*/
""",
impl = """
static CYTHON_INLINE void __Pyx_RaiseKeywordRequired(
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
static CYTHON_INLINE int __Pyx_CheckKeywordStrings(PyObject *kwdict,
    const char* function_name, int kw_allowed); /*proto*/
""",
impl = """
static CYTHON_INLINE int __Pyx_CheckKeywordStrings(
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
        name = first_kw_arg;
        while (*name && (**name != key)) name++;
        if (*name) {
            values[name-argnames] = value;
        } else {
            #if PY_MAJOR_VERSION < 3
            if (unlikely(!PyString_CheckExact(key)) && unlikely(!PyString_Check(key))) {
            #else
            if (unlikely(!PyUnicode_CheckExact(key)) && unlikely(!PyUnicode_Check(key))) {
            #endif
                goto invalid_keyword_type;
            } else {
                for (name = first_kw_arg; *name; name++) {
                    #if PY_MAJOR_VERSION >= 3
                    if (PyUnicode_GET_SIZE(**name) == PyUnicode_GET_SIZE(key) &&
                        PyUnicode_Compare(**name, key) == 0) break;
                    #else
                    if (PyString_GET_SIZE(**name) == PyString_GET_SIZE(key) &&
                        _PyString_Eq(**name, key)) break;
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
                            _PyString_Eq(**name, key)) goto arg_passed_twice;
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
""",
requires=[raise_double_keywords_utility_code])

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
    py_code = PyCode_New(
        0,            /*int argcount,*/
        #if PY_MAJOR_VERSION >= 3
        0,            /*int kwonlyargcount,*/
        #endif
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        %(EMPTY_BYTES)s, /*PyObject *code,*/
        %(EMPTY_TUPLE)s,  /*PyObject *consts,*/
        %(EMPTY_TUPLE)s,  /*PyObject *names,*/
        %(EMPTY_TUPLE)s,  /*PyObject *varnames,*/
        %(EMPTY_TUPLE)s,  /*PyObject *freevars,*/
        %(EMPTY_TUPLE)s,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        %(LINENO)s,   /*int firstlineno,*/
        %(EMPTY_BYTES)s  /*PyObject *lnotab*/
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
    'EMPTY_BYTES' : Naming.empty_bytes,
})

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
""",
requires=[restore_exception_utility_code])

#------------------------------------------------------------------------------------

set_vtable_utility_code = UtilityCode(
proto = """
static int __Pyx_SetVtable(PyObject *dict, void *vtable); /*proto*/
""",
impl = """
static int __Pyx_SetVtable(PyObject *dict, void *vtable) {
#if PY_VERSION_HEX >= 0x02070000 && !(PY_MAJOR_VERSION==3&&PY_MINOR_VERSION==0)
    PyObject *ob = PyCapsule_New(vtable, 0, 0);
#else
    PyObject *ob = PyCObject_FromVoidPtr(vtable, 0);
#endif
    if (!ob)
        goto bad;
    if (PyDict_SetItemString(dict, "__pyx_vtable__", ob) < 0)
        goto bad;
    Py_DECREF(ob);
    return 0;
bad:
    Py_XDECREF(ob);
    return -1;
}
""")

#------------------------------------------------------------------------------------

get_vtable_utility_code = UtilityCode(
proto = """
static void* __Pyx_GetVtable(PyObject *dict); /*proto*/
""",
impl = r"""
static void* __Pyx_GetVtable(PyObject *dict) {
    void* ptr;
    PyObject *ob = PyMapping_GetItemString(dict, (char *)"__pyx_vtable__");
    if (!ob)
        goto bad;
#if PY_VERSION_HEX >= 0x02070000 && !(PY_MAJOR_VERSION==3&&PY_MINOR_VERSION==0)
    ptr = PyCapsule_GetPointer(ob, 0);
#else
    ptr = PyCObject_AsVoidPtr(ob);
#endif
    if (!ptr && !PyErr_Occurred())
        PyErr_SetString(PyExc_RuntimeError, "invalid vtable found for imported type");
    Py_DECREF(ob);
    return ptr;
bad:
    Py_XDECREF(ob);
    return NULL;
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
        if (t->is_unicode) {
            *t->p = PyUnicode_DecodeUTF8(t->s, t->n - 1, NULL);
        } else if (t->intern) {
            *t->p = PyString_InternFromString(t->s);
        } else {
            *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        }
        #else  /* Python 3+ has unicode identifiers */
        if (t->is_unicode | t->is_str) {
            if (t->intern) {
                *t->p = PyUnicode_InternFromString(t->s);
            } else if (t->encoding) {
                *t->p = PyUnicode_Decode(t->s, t->n - 1, t->encoding, NULL);
            } else {
                *t->p = PyUnicode_FromStringAndSize(t->s, t->n - 1);
            }
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

force_init_threads_utility_code = UtilityCode(
proto="""
#ifndef __PYX_FORCE_INIT_THREADS
  #if PY_VERSION_HEX < 0x02040200
    #define __PYX_FORCE_INIT_THREADS 1
  #else
    #define __PYX_FORCE_INIT_THREADS 0
  #endif
#endif
""")

#------------------------------------------------------------------------------------

# Note that cPython ignores PyTrace_EXCEPTION,
# but maybe some other profilers don't.

profile_utility_code = UtilityCode(proto="""
#ifndef CYTHON_PROFILE
  #define CYTHON_PROFILE 1
#endif

#ifndef CYTHON_PROFILE_REUSE_FRAME
  #define CYTHON_PROFILE_REUSE_FRAME 0
#endif

#if CYTHON_PROFILE

  #include "compile.h"
  #include "frameobject.h"
  #include "traceback.h"

  #if CYTHON_PROFILE_REUSE_FRAME
    #define CYTHON_FRAME_MODIFIER static
    #define CYTHON_FRAME_DEL
  #else
    #define CYTHON_FRAME_MODIFIER
    #define CYTHON_FRAME_DEL Py_DECREF(%(FRAME)s)
  #endif

  #define __Pyx_TraceDeclarations                                  \\
  static PyCodeObject *%(FRAME_CODE)s = NULL;                      \\
  CYTHON_FRAME_MODIFIER PyFrameObject *%(FRAME)s = NULL;           \\
  int __Pyx_use_tracing = 0;

  #define __Pyx_TraceCall(funcname, srcfile, firstlineno)                            \\
  if (unlikely(PyThreadState_GET()->use_tracing && PyThreadState_GET()->c_profilefunc)) {      \\
      __Pyx_use_tracing = __Pyx_TraceSetupAndCall(&%(FRAME_CODE)s, &%(FRAME)s, funcname, srcfile, firstlineno);  \\
  }

  #define __Pyx_TraceException()                                                           \\
  if (unlikely(__Pyx_use_tracing( && PyThreadState_GET()->use_tracing && PyThreadState_GET()->c_profilefunc) {  \\
      PyObject *exc_info = __Pyx_GetExceptionTuple();                                      \\
      if (exc_info) {                                                                      \\
          PyThreadState_GET()->c_profilefunc(                                              \\
              PyThreadState_GET()->c_profileobj, %(FRAME)s, PyTrace_EXCEPTION, exc_info);  \\
          Py_DECREF(exc_info);                                                             \\
      }                                                                                    \\
  }

  #define __Pyx_TraceReturn(result)                                                  \\
  if (unlikely(__Pyx_use_tracing) && PyThreadState_GET()->use_tracing && PyThreadState_GET()->c_profilefunc) {  \\
      PyThreadState_GET()->c_profilefunc(                                            \\
          PyThreadState_GET()->c_profileobj, %(FRAME)s, PyTrace_RETURN, (PyObject*)result);     \\
      CYTHON_FRAME_DEL;                                                               \\
  }

  static PyCodeObject *__Pyx_createFrameCodeObject(const char *funcname, const char *srcfile, int firstlineno); /*proto*/
  static int __Pyx_TraceSetupAndCall(PyCodeObject** code, PyFrameObject** frame, const char *funcname, const char *srcfile, int firstlineno); /*proto*/

#else

  #define __Pyx_TraceDeclarations
  #define __Pyx_TraceCall(funcname, srcfile, firstlineno)
  #define __Pyx_TraceException()
  #define __Pyx_TraceReturn(result)

#endif /* CYTHON_PROFILE */
"""
% {
    "FRAME": Naming.frame_cname,
    "FRAME_CODE": Naming.frame_code_cname,
},
impl = """

#if CYTHON_PROFILE

static int __Pyx_TraceSetupAndCall(PyCodeObject** code,
                                   PyFrameObject** frame,
                                   const char *funcname,
                                   const char *srcfile,
                                   int firstlineno) {
    if (*frame == NULL || !CYTHON_PROFILE_REUSE_FRAME) {
        if (*code == NULL) {
            *code = __Pyx_createFrameCodeObject(funcname, srcfile, firstlineno);
            if (*code == NULL) return 0;
        }
        *frame = PyFrame_New(
            PyThreadState_GET(),            /*PyThreadState *tstate*/
            *code,                          /*PyCodeObject *code*/
            PyModule_GetDict(%(MODULE)s),      /*PyObject *globals*/
            0                               /*PyObject *locals*/
        );
        if (*frame == NULL) return 0;
    }
    else {
        (*frame)->f_tstate = PyThreadState_GET();
    }
    return PyThreadState_GET()->c_profilefunc(PyThreadState_GET()->c_profileobj, *frame, PyTrace_CALL, NULL) == 0;
}

static PyCodeObject *__Pyx_createFrameCodeObject(const char *funcname, const char *srcfile, int firstlineno) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyCodeObject *py_code = 0;

    #if PY_MAJOR_VERSION < 3
    py_funcname = PyString_FromString(funcname);
    py_srcfile = PyString_FromString(srcfile);
    #else
    py_funcname = PyUnicode_FromString(funcname);
    py_srcfile = PyUnicode_FromString(srcfile);
    #endif
    if (!py_funcname | !py_srcfile) goto bad;

    py_code = PyCode_New(
        0,                /*int argcount,*/
        #if PY_MAJOR_VERSION >= 3
        0,                /*int kwonlyargcount,*/
        #endif
        0,                /*int nlocals,*/
        0,                /*int stacksize,*/
        0,                /*int flags,*/
        %(EMPTY_BYTES)s,  /*PyObject *code,*/
        %(EMPTY_TUPLE)s,  /*PyObject *consts,*/
        %(EMPTY_TUPLE)s,  /*PyObject *names,*/
        %(EMPTY_TUPLE)s,  /*PyObject *varnames,*/
        %(EMPTY_TUPLE)s,  /*PyObject *freevars,*/
        %(EMPTY_TUPLE)s,  /*PyObject *cellvars,*/
        py_srcfile,       /*PyObject *filename,*/
        py_funcname,      /*PyObject *name,*/
        firstlineno,      /*int firstlineno,*/
        %(EMPTY_BYTES)s   /*PyObject *lnotab*/
    );

bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);

    return py_code;
}

#endif /* CYTHON_PROFILE */
""" % {
    'EMPTY_TUPLE' : Naming.empty_tuple,
    'EMPTY_BYTES' : Naming.empty_bytes,
    "MODULE": Naming.module_cname,
})
