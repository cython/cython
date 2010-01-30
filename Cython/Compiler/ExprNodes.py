#
#   Pyrex - Parse tree nodes for expressions
#

import operator

from Errors import error, warning, warn_once, InternalError
from Errors import hold_errors, release_errors, held_errors, report_error
from Code import UtilityCode
import StringEncoding
import Naming
import Nodes
from Nodes import Node
import PyrexTypes
from PyrexTypes import py_object_type, c_long_type, typecast, error_type, unspecified_type
from Builtin import list_type, tuple_type, set_type, dict_type, \
     unicode_type, str_type, bytes_type, type_type
import Builtin
import Symtab
import Options
from Annotate import AnnotationItem

from Cython.Debugging import print_call_chain
from DebugFlags import debug_disposal_code, debug_temp_alloc, \
    debug_coercion

try:
    set
except NameError:
    from sets import Set as set

class NotConstant(object): pass # just for the name
not_a_constant = NotConstant()
constant_value_not_set = object()

# error messages when coercing from key[0] to key[1]
find_coercion_error = {
    # string related errors
    (Builtin.unicode_type, Builtin.bytes_type) : "Cannot convert Unicode string to 'bytes' implicitly, encoding required.",
    (Builtin.unicode_type, Builtin.str_type)   : "Cannot convert Unicode string to 'str' implicitly. This is not portable and requires explicit encoding.",
    (Builtin.unicode_type, PyrexTypes.c_char_ptr_type) : "Unicode objects do not support coercion to C types.",
    (Builtin.bytes_type, Builtin.unicode_type) : "Cannot convert 'bytes' object to unicode implicitly, decoding required",
    (Builtin.bytes_type, Builtin.str_type) : "Cannot convert 'bytes' object to str implicitly. This is not portable to Py3.",
    (Builtin.str_type, Builtin.unicode_type) : "str objects do not support coercion to unicode, use a unicode string literal instead (u'')",
    (Builtin.str_type, Builtin.bytes_type) : "Cannot convert 'str' to 'bytes' implicitly. This is not portable.",
    (Builtin.str_type, PyrexTypes.c_char_ptr_type) : "'str' objects do not support coercion to C types (use 'bytes'?).",
    (PyrexTypes.c_char_ptr_type, Builtin.unicode_type) : "Cannot convert 'char*' to unicode implicitly, decoding required",
    (PyrexTypes.c_uchar_ptr_type, Builtin.unicode_type) : "Cannot convert 'char*' to unicode implicitly, decoding required",
    }.get


class ExprNode(Node):
    #  subexprs     [string]     Class var holding names of subexpr node attrs
    #  type         PyrexType    Type of the result
    #  result_code  string       Code fragment
    #  result_ctype string       C type of result_code if different from type
    #  is_temp      boolean      Result is in a temporary variable
    #  is_sequence_constructor  
    #               boolean      Is a list or tuple constructor expression
    #  is_starred   boolean      Is a starred expression (e.g. '*a')
    #  saved_subexpr_nodes
    #               [ExprNode or [ExprNode or None] or None]
    #                            Cached result of subexpr_nodes()
    #  use_managed_ref boolean   use ref-counted temps/assignments/etc.
    
    result_ctype = None
    type = None
    temp_code = None
    old_temp = None # error checker for multiple frees etc.
    use_managed_ref = True # can be set by optimisation transforms

    #  The Analyse Expressions phase for expressions is split
    #  into two sub-phases:
    #
    #    Analyse Types
    #      Determines the result type of the expression based
    #      on the types of its sub-expressions, and inserts
    #      coercion nodes into the expression tree where needed.
    #      Marks nodes which will need to have temporary variables
    #      allocated.
    #
    #    Allocate Temps
    #      Allocates temporary variables where needed, and fills
    #      in the result_code field of each node.
    #
    #  ExprNode provides some convenience routines which
    #  perform both of the above phases. These should only
    #  be called from statement nodes, and only when no
    #  coercion nodes need to be added around the expression
    #  being analysed. In that case, the above two phases
    #  should be invoked separately.
    #
    #  Framework code in ExprNode provides much of the common
    #  processing for the various phases. It makes use of the
    #  'subexprs' class attribute of ExprNodes, which should
    #  contain a list of the names of attributes which can
    #  hold sub-nodes or sequences of sub-nodes.
    #  
    #  The framework makes use of a number of abstract methods. 
    #  Their responsibilities are as follows.
    #
    #    Declaration Analysis phase
    #
    #      analyse_target_declaration
    #        Called during the Analyse Declarations phase to analyse
    #        the LHS of an assignment or argument of a del statement.
    #        Nodes which cannot be the LHS of an assignment need not
    #        implement it.
    #
    #    Expression Analysis phase
    #
    #      analyse_types
    #        - Call analyse_types on all sub-expressions.
    #        - Check operand types, and wrap coercion nodes around
    #          sub-expressions where needed.
    #        - Set the type of this node.
    #        - If a temporary variable will be required for the
    #          result, set the is_temp flag of this node.
    #
    #      analyse_target_types
    #        Called during the Analyse Types phase to analyse
    #        the LHS of an assignment or argument of a del 
    #        statement. Similar responsibilities to analyse_types.
    #
    #      target_code
    #        Called by the default implementation of allocate_target_temps.
    #        Should return a C lvalue for assigning to the node. The default
    #        implementation calls calculate_result_code.
    #
    #      check_const
    #        - Check that this node and its subnodes form a
    #          legal constant expression. If so, do nothing,
    #          otherwise call not_const. 
    #
    #        The default implementation of check_const 
    #        assumes that the expression is not constant.
    #
    #      check_const_addr
    #        - Same as check_const, except check that the
    #          expression is a C lvalue whose address is
    #          constant. Otherwise, call addr_not_const.
    #
    #        The default implementation of calc_const_addr
    #        assumes that the expression is not a constant 
    #        lvalue.
    #
    #   Code Generation phase
    #
    #      generate_evaluation_code
    #        - Call generate_evaluation_code for sub-expressions.
    #        - Perform the functions of generate_result_code
    #          (see below).
    #        - If result is temporary, call generate_disposal_code
    #          on all sub-expressions.
    #
    #        A default implementation of generate_evaluation_code
    #        is provided which uses the following abstract methods:
    #
    #          generate_result_code
    #            - Generate any C statements necessary to calculate
    #              the result of this node from the results of its
    #              sub-expressions.
    #
    #          calculate_result_code
    #            - Should return a C code fragment evaluating to the 
    #              result. This is only called when the result is not 
    #              a temporary.
    #
    #      generate_assignment_code
    #        Called on the LHS of an assignment.
    #        - Call generate_evaluation_code for sub-expressions.
    #        - Generate code to perform the assignment.
    #        - If the assignment absorbed a reference, call
    #          generate_post_assignment_code on the RHS,
    #          otherwise call generate_disposal_code on it.
    #
    #      generate_deletion_code
    #        Called on an argument of a del statement.
    #        - Call generate_evaluation_code for sub-expressions.
    #        - Generate code to perform the deletion.
    #        - Call generate_disposal_code on all sub-expressions.
    #
    #
    
    is_sequence_constructor = 0
    is_attribute = 0
    
    saved_subexpr_nodes = None
    is_temp = 0
    is_target = 0
    is_starred = 0

    constant_result = constant_value_not_set

    try:
        _get_child_attrs = operator.attrgetter('subexprs')
    except AttributeError:
        # Python 2.3
        def _get_child_attrs(self):
            return self.subexprs
    child_attrs = property(fget=_get_child_attrs)
        
    def not_implemented(self, method_name):
        print_call_chain(method_name, "not implemented") ###
        raise InternalError(
            "%s.%s not implemented" %
                (self.__class__.__name__, method_name))
                
    def is_lvalue(self):
        return 0
    
    def is_ephemeral(self):
        #  An ephemeral node is one whose result is in
        #  a Python temporary and we suspect there are no
        #  other references to it. Certain operations are
        #  disallowed on such values, since they are
        #  likely to result in a dangling pointer.
        return self.type.is_pyobject and self.is_temp

    def subexpr_nodes(self):
        #  Extract a list of subexpression nodes based
        #  on the contents of the subexprs class attribute.
        nodes = []
        for name in self.subexprs:
            item = getattr(self, name)
            if item is not None:
                if type(item) is list:
                    nodes.extend(item)
                else:
                    nodes.append(item)
        return nodes
        
    def result(self):
        if self.is_temp:
            return self.temp_code
        else:
            return self.calculate_result_code()
    
    def result_as(self, type = None):
        #  Return the result code cast to the specified C type.
        return typecast(type, self.ctype(), self.result())
    
    def py_result(self):
        #  Return the result code cast to PyObject *.
        return self.result_as(py_object_type)
    
    def ctype(self):
        #  Return the native C type of the result (i.e. the
        #  C type of the result_code expression).
        return self.result_ctype or self.type

    def get_constant_c_result_code(self):
        # Return the constant value of this node as a result code
        # string, or None if the node is not constant.  This method
        # can be called when the constant result code is required
        # before the code generation phase.
        #
        # The return value is a string that can represent a simple C
        # value, a constant C name or a constant C expression.  If the
        # node type depends on Python code, this must return None.
        return None

    def calculate_constant_result(self):
        # Calculate the constant compile time result value of this
        # expression and store it in ``self.constant_result``.  Does
        # nothing by default, thus leaving ``self.constant_result``
        # unknown.  If valid, the result can be an arbitrary Python
        # value.
        #
        # This must only be called when it is assured that all
        # sub-expressions have a valid constant_result value.  The
        # ConstantFolding transform will do this.
        pass

    def compile_time_value(self, denv):
        #  Return value of compile-time expression, or report error.
        error(self.pos, "Invalid compile-time expression")
    
    def compile_time_value_error(self, e):
        error(self.pos, "Error in compile-time expression: %s: %s" % (
            e.__class__.__name__, e))
    
    # ------------- Declaration Analysis ----------------
    
    def analyse_target_declaration(self, env):
        error(self.pos, "Cannot assign to or delete this")
    
    # ------------- Expression Analysis ----------------
    
    def analyse_const_expression(self, env):
        #  Called during the analyse_declarations phase of a
        #  constant expression. Analyses the expression's type,
        #  checks whether it is a legal const expression,
        #  and determines its value.
        self.analyse_types(env)
        return self.check_const()
    
    def analyse_expressions(self, env):
        #  Convenience routine performing both the Type
        #  Analysis and Temp Allocation phases for a whole 
        #  expression.
        self.analyse_types(env)
    
    def analyse_target_expression(self, env, rhs):
        #  Convenience routine performing both the Type
        #  Analysis and Temp Allocation phases for the LHS of
        #  an assignment.
        self.analyse_target_types(env)
    
    def analyse_boolean_expression(self, env):
        #  Analyse expression and coerce to a boolean.
        self.analyse_types(env)
        bool = self.coerce_to_boolean(env)
        return bool
    
    def analyse_temp_boolean_expression(self, env):
        #  Analyse boolean expression and coerce result into
        #  a temporary. This is used when a branch is to be
        #  performed on the result and we won't have an
        #  opportunity to ensure disposal code is executed
        #  afterwards. By forcing the result into a temporary,
        #  we ensure that all disposal has been done by the
        #  time we get the result.
        self.analyse_types(env)
        bool = self.coerce_to_boolean(env)
        temp_bool = bool.coerce_to_temp(env)
        return temp_bool
    
    # --------------- Type Inference -----------------
    
    def type_dependencies(self, env):
        # Returns the list of entries whose types must be determined
        # before the type of self can be infered.
        if hasattr(self, 'type') and self.type is not None:
            return ()
        return sum([node.type_dependencies(env) for node in self.subexpr_nodes()], ())
    
    def infer_type(self, env):
        # Attempt to deduce the type of self. 
        # Differs from analyse_types as it avoids unnecessary 
        # analysis of subexpressions, but can assume everything
        # in self.type_dependencies() has been resolved.
        if hasattr(self, 'type') and self.type is not None:
            return self.type
        elif hasattr(self, 'entry') and self.entry is not None:
            return self.entry.type
        else:
            self.not_implemented("infer_type")
    
    # --------------- Type Analysis ------------------
    
    def analyse_as_module(self, env):
        # If this node can be interpreted as a reference to a
        # cimported module, return its scope, else None.
        return None
        
    def analyse_as_type(self, env):
        # If this node can be interpreted as a reference to a
        # type, return that type, else None.
        return None
    
    def analyse_as_extension_type(self, env):
        # If this node can be interpreted as a reference to an
        # extension type, return its type, else None.
        return None
    
    def analyse_types(self, env):
        self.not_implemented("analyse_types")
    
    def analyse_target_types(self, env):
        self.analyse_types(env)

    def nogil_check(self, env):
        # By default, any expression based on Python objects is
        # prevented in nogil environments.  Subtypes must override
        # this if they can work without the GIL.
        if self.type.is_pyobject:
            self.gil_error()

    def gil_assignment_check(self, env):
        if env.nogil and self.type.is_pyobject:
            error(self.pos, "Assignment of Python object not allowed without gil")

    def check_const(self):
        self.not_const()
        return False
    
    def not_const(self):
        error(self.pos, "Not allowed in a constant expression")
    
    def check_const_addr(self):
        self.addr_not_const()
        return False
    
    def addr_not_const(self):
        error(self.pos, "Address is not constant")

    # ----------------- Result Allocation -----------------
    
    def result_in_temp(self):
        #  Return true if result is in a temporary owned by
        #  this node or one of its subexpressions. Overridden
        #  by certain nodes which can share the result of
        #  a subnode.
        return self.is_temp
            
    def target_code(self):
        #  Return code fragment for use as LHS of a C assignment.
        return self.calculate_result_code()
    
    def calculate_result_code(self):
        self.not_implemented("calculate_result_code")
    
#    def release_target_temp(self, env):
#        #  Release temporaries used by LHS of an assignment.
#        self.release_subexpr_temps(env)

    def allocate_temp_result(self, code):
        if self.temp_code:
            raise RuntimeError("Temp allocated multiple times in %r: %r" % (self.__class__.__name__, self.pos))
        type = self.type
        if not type.is_void:
            if type.is_pyobject:
                type = PyrexTypes.py_object_type
            self.temp_code = code.funcstate.allocate_temp(
                type, manage_ref=self.use_managed_ref)
        else:
            self.temp_code = None

    def release_temp_result(self, code):
        if not self.temp_code:
            if self.old_temp:
                raise RuntimeError("temp %s released multiple times in %s" % (
                        self.old_temp, self.__class__.__name__))
            else:
                raise RuntimeError("no temp, but release requested in %s" % (
                        self.__class__.__name__))
        code.funcstate.release_temp(self.temp_code)
        self.old_temp = self.temp_code
        self.temp_code = None

    # ---------------- Code Generation -----------------
    
    def make_owned_reference(self, code):
        #  If result is a pyobject, make sure we own
        #  a reference to it.
        if self.type.is_pyobject and not self.result_in_temp():
            code.put_incref(self.result(), self.ctype())
    
    def generate_evaluation_code(self, code):
        code.mark_pos(self.pos)
        
        #  Generate code to evaluate this node and
        #  its sub-expressions, and dispose of any
        #  temporary results of its sub-expressions.
        self.generate_subexpr_evaluation_code(code)

        if self.is_temp:
            self.allocate_temp_result(code)

        self.generate_result_code(code)
        if self.is_temp:
            # If we are temp we do not need to wait until this node is disposed
            # before disposing children.
            self.generate_subexpr_disposal_code(code)
            self.free_subexpr_temps(code)

    def generate_subexpr_evaluation_code(self, code):
        for node in self.subexpr_nodes():
            node.generate_evaluation_code(code)
    
    def generate_result_code(self, code):
        self.not_implemented("generate_result_code")
    
    def generate_disposal_code(self, code):
        if self.is_temp:
            if self.type.is_pyobject:
                code.put_decref_clear(self.result(), self.ctype())
        else:
            # Already done if self.is_temp
            self.generate_subexpr_disposal_code(code)

    def generate_subexpr_disposal_code(self, code):
        #  Generate code to dispose of temporary results
        #  of all sub-expressions.
        for node in self.subexpr_nodes():
            node.generate_disposal_code(code)
    
    def generate_post_assignment_code(self, code):
        if self.is_temp:
            if self.type.is_pyobject:
                code.putln("%s = 0;" % self.result())
        else:
            self.generate_subexpr_disposal_code(code)

    def generate_assignment_code(self, rhs, code):
        #  Stub method for nodes which are not legal as
        #  the LHS of an assignment. An error will have 
        #  been reported earlier.
        pass
    
    def generate_deletion_code(self, code):
        #  Stub method for nodes that are not legal as
        #  the argument of a del statement. An error
        #  will have been reported earlier.
        pass

    def free_temps(self, code):
        if self.is_temp:
            if not self.type.is_void:
                self.release_temp_result(code)
        else:
            self.free_subexpr_temps(code)
    
    def free_subexpr_temps(self, code):
        for sub in self.subexpr_nodes():
            sub.free_temps(code)

    # ---------------- Annotation ---------------------
    
    def annotate(self, code):
        for node in self.subexpr_nodes():
            node.annotate(code)
    
    # ----------------- Coercion ----------------------
    
    def coerce_to(self, dst_type, env):
        #   Coerce the result so that it can be assigned to
        #   something of type dst_type. If processing is necessary,
        #   wraps this node in a coercion node and returns that.
        #   Otherwise, returns this node unchanged.
        #
        #   This method is called during the analyse_expressions
        #   phase of the src_node's processing.
        #
        #   Note that subclasses that override this (especially
        #   ConstNodes) must not (re-)set their own .type attribute
        #   here.  Since expression nodes may turn up in different
        #   places in the tree (e.g. inside of CloneNodes in cascaded
        #   assignments), this method must return a new node instance
        #   if it changes the type.
        #
        src = self
        src_type = self.type
        src_is_py_type = src_type.is_pyobject
        dst_is_py_type = dst_type.is_pyobject

        if self.check_for_coercion_error(dst_type):
            return self

        if dst_type.is_pyobject:
            if not src.type.is_pyobject:
                src = CoerceToPyTypeNode(src, env)
            if not src.type.subtype_of(dst_type):
                if not isinstance(src, NoneNode):
                    src = PyTypeTestNode(src, dst_type, env)
        elif src.type.is_pyobject:
            src = CoerceFromPyTypeNode(dst_type, src, env)
        elif (dst_type.is_complex 
              and src_type != dst_type
              and dst_type.assignable_from(src_type)):
            src = CoerceToComplexNode(src, dst_type, env)
        else: # neither src nor dst are py types
            # Added the string comparison, since for c types that
            # is enough, but Cython gets confused when the types are
            # in different pxi files.
            if not (str(src.type) == str(dst_type) or dst_type.assignable_from(src_type)):
                self.fail_assignment(dst_type)
        return src

    def fail_assignment(self, dst_type):
        error(self.pos, "Cannot assign type '%s' to '%s'" % (self.type, dst_type))

    def check_for_coercion_error(self, dst_type, fail=False, default=None):
        if fail and not default:
            default = "Cannot assign type '%(FROM)s' to '%(TO)s'"
        message = find_coercion_error((self.type, dst_type), default)
        if message is not None:
            error(self.pos, message % {'FROM': self.type, 'TO': dst_type})
            return True
        if fail:
            self.fail_assignment(dst_type)
            return True
        return False

    def coerce_to_pyobject(self, env):
        return self.coerce_to(PyrexTypes.py_object_type, env)

    def coerce_to_boolean(self, env):
        #  Coerce result to something acceptable as
        #  a boolean value.
        type = self.type
        if type.is_pyobject or type.is_ptr or type.is_float:
            return CoerceToBooleanNode(self, env)
        else:
            if not type.is_int and not type.is_error:
                error(self.pos, 
                    "Type '%s' not acceptable as a boolean" % type)
            return self
    
    def coerce_to_integer(self, env):
        # If not already some C integer type, coerce to longint.
        if self.type.is_int:
            return self
        else:
            return self.coerce_to(PyrexTypes.c_long_type, env)
    
    def coerce_to_temp(self, env):
        #  Ensure that the result is in a temporary.
        if self.result_in_temp():
            return self
        else:
            return CoerceToTempNode(self, env)
    
    def coerce_to_simple(self, env):
        #  Ensure that the result is simple (see is_simple).
        if self.is_simple():
            return self
        else:
            return self.coerce_to_temp(env)
    
    def is_simple(self):
        #  A node is simple if its result is something that can
        #  be referred to without performing any operations, e.g.
        #  a constant, local var, C global var, struct member
        #  reference, or temporary.
        return self.result_in_temp()
        
    def as_cython_attribute(self):
        return None

class AtomicExprNode(ExprNode):
    #  Abstract base class for expression nodes which have
    #  no sub-expressions.
    
    subexprs = []

    # Override to optimize -- we know we have no children
    def generate_subexpr_evaluation_code(self, code):
        pass
    def generate_subexpr_disposal_code(self, code):
        pass

class PyConstNode(AtomicExprNode):
    #  Abstract base class for constant Python values.
    
    is_literal = 1
    type = py_object_type
    
    def is_simple(self):
        return 1
    
    def analyse_types(self, env):
        pass
    
    def calculate_result_code(self):
        return self.value

    def generate_result_code(self, code):
        pass


class NoneNode(PyConstNode):
    #  The constant value None
    
    value = "Py_None"

    constant_result = None
    
    nogil_check = None

    def compile_time_value(self, denv):
        return None
    
class EllipsisNode(PyConstNode):
    #  '...' in a subscript list.
    
    value = "Py_Ellipsis"

    constant_result = Ellipsis

    def compile_time_value(self, denv):
        return Ellipsis


class ConstNode(AtomicExprNode):
    # Abstract base type for literal constant nodes.
    #
    # value     string      C code fragment
    
    is_literal = 1
    nogil_check = None

    def is_simple(self):
        return 1
    
    def analyse_types(self, env):
        pass # Types are held in class variables
    
    def check_const(self):
        return True
    
    def get_constant_c_result_code(self):
        return self.calculate_result_code()

    def calculate_result_code(self):
        return str(self.value)

    def generate_result_code(self, code):
        pass


class BoolNode(ConstNode):
    type = PyrexTypes.c_bint_type
    #  The constant value True or False

    def calculate_constant_result(self):
        self.constant_result = self.value

    def compile_time_value(self, denv):
        return self.value
    
    def calculate_result_code(self):
        return str(int(self.value))


class NullNode(ConstNode):
    type = PyrexTypes.c_null_ptr_type
    value = "NULL"
    constant_result = 0

    def get_constant_c_result_code(self):
        return self.value


class CharNode(ConstNode):
    type = PyrexTypes.c_char_type

    def calculate_constant_result(self):
        self.constant_result = ord(self.value)
    
    def compile_time_value(self, denv):
        return ord(self.value)
    
    def calculate_result_code(self):
        return "'%s'" % StringEncoding.escape_char(self.value)


class IntNode(ConstNode):

    # unsigned     "" or "U"
    # longness     "" or "L" or "LL"

    unsigned = ""
    longness = ""
    type = PyrexTypes.c_long_type

    def coerce_to(self, dst_type, env):
        if self.type is dst_type:
            return self
        node = IntNode(self.pos, value=self.value,
                       unsigned=self.unsigned, longness=self.longness)
        if dst_type.is_numeric and not dst_type.is_complex:
            return node
        if dst_type.is_pyobject:
            node.type = PyrexTypes.py_object_type
        # We still need to perform normal coerce_to processing on the
        # result, because we might be coercing to an extension type,
        # in which case a type test node will be needed.
        return ConstNode.coerce_to(node, dst_type, env)

    def coerce_to_boolean(self, env):
        return IntNode(
            self.pos, value=self.value,
            type = PyrexTypes.c_bint_type,
            unsigned=self.unsigned, longness=self.longness)

    def generate_evaluation_code(self, code):
        if self.type.is_pyobject:
            # pre-allocate a Python version of the number
            self.result_code = code.get_py_num(self.value, self.longness)
        else:
            self.result_code = self.get_constant_c_result_code()
    
    def get_constant_c_result_code(self):
        return str(self.value) + self.unsigned + self.longness

    def calculate_result_code(self):
        return self.result_code

    def calculate_constant_result(self):
        self.constant_result = int(self.value, 0)

    def compile_time_value(self, denv):
        return int(self.value, 0)


class FloatNode(ConstNode):
    type = PyrexTypes.c_double_type

    def calculate_constant_result(self):
        self.constant_result = float(self.value)

    def compile_time_value(self, denv):
        return float(self.value)
    
    def calculate_result_code(self):
        strval = repr(float(self.value))
        if strval == 'nan':
            return "(Py_HUGE_VAL * 0)"
        elif strval == 'inf':
            return "Py_HUGE_VAL"
        elif strval == '-inf':
            return "(-Py_HUGE_VAL)"
        else:
            return strval


class BytesNode(ConstNode):
    # A char* or bytes literal
    #
    # value      BytesLiteral

    type = PyrexTypes.c_char_ptr_type

    def compile_time_value(self, denv):
        return self.value

    def analyse_as_type(self, env):
        type = PyrexTypes.parse_basic_type(self.value)
        if type is not None:    
            return type
        from TreeFragment import TreeFragment
        pos = (self.pos[0], self.pos[1], self.pos[2]-7)
        declaration = TreeFragment(u"sizeof(%s)" % self.value, name=pos[0].filename, initial_pos=pos)
        sizeof_node = declaration.root.stats[0].expr
        sizeof_node.analyse_types(env)
        if isinstance(sizeof_node, SizeofTypeNode):
            return sizeof_node.arg_type

    def can_coerce_to_char_literal(self):
        return len(self.value) == 1

    def coerce_to(self, dst_type, env):
        if dst_type.is_int:
            if not self.can_coerce_to_char_literal():
                error(self.pos, "Only single-character strings can be coerced into ints.")
                return self
            return CharNode(self.pos, value=self.value)

        node = BytesNode(self.pos, value=self.value)
        if dst_type == PyrexTypes.c_char_ptr_type:
            node.type = PyrexTypes.c_char_ptr_type
            return node
        elif dst_type == PyrexTypes.c_uchar_ptr_type:
            node.type = PyrexTypes.c_char_ptr_type
            return CastNode(node, PyrexTypes.c_uchar_ptr_type)

        if not self.type.is_pyobject:
            if dst_type in (py_object_type, Builtin.bytes_type):
                node.type = Builtin.bytes_type
            elif dst_type.is_pyobject:
                self.fail_assignment(dst_type)
                return self
        elif dst_type.is_pyobject and dst_type is not py_object_type:
            self.check_for_coercion_error(dst_type, fail=True)
            return node

        # We still need to perform normal coerce_to processing on the
        # result, because we might be coercing to an extension type,
        # in which case a type test node will be needed.
        return ConstNode.coerce_to(node, dst_type, env)

    def as_py_string_node(self, env):
        # Return a new BytesNode with the same value as this node
        # but whose type is a Python type instead of a C type.
        return BytesNode(self.pos, value = self.value, type = Builtin.bytes_type)

    def generate_evaluation_code(self, code):
        if self.type.is_pyobject:
            self.result_code = code.get_py_string_const(self.value)
        else:
            self.result_code = code.get_string_const(self.value)

    def get_constant_c_result_code(self):
        return None # FIXME
    
    def calculate_result_code(self):
        return self.result_code


class UnicodeNode(PyConstNode):
    # A Python unicode object
    #
    # value    EncodedString

    type = unicode_type

    def coerce_to(self, dst_type, env):
        if dst_type is self.type:
            pass
        elif not dst_type.is_pyobject:
            error(self.pos, "Unicode objects do not support coercion to C types.")
        elif dst_type is not py_object_type:
            if not self.check_for_coercion_error(dst_type):
                self.fail_assignment(dst_type)
        return self

    def generate_evaluation_code(self, code):
        self.result_code = code.get_py_string_const(self.value)

    def calculate_result_code(self):
        return self.result_code
        
    def compile_time_value(self, env):
        return self.value


class StringNode(PyConstNode):
    # A Python str object, i.e. a byte string in Python 2.x and a
    # unicode string in Python 3.x
    #
    # value          BytesLiteral or EncodedString
    # is_identifier  boolean

    type = str_type
    is_identifier = None

    def coerce_to(self, dst_type, env):
        if dst_type is not py_object_type and not str_type.subtype_of(dst_type):
#            if dst_type is Builtin.bytes_type:
#                # special case: bytes = 'str literal'
#                return BytesNode(self.pos, value=self.value)
            if not dst_type.is_pyobject:
                return BytesNode(self.pos, value=self.value).coerce_to(dst_type, env)
            self.check_for_coercion_error(dst_type, fail=True)

        # this will be a unicode string in Py3, so make sure we can decode it
        if self.value.encoding:
            encoding = self.value.encoding
            try:
                self.value.decode(encoding)
            except UnicodeDecodeError:
                error(self.pos, "String decoding as '%s' failed. Consider using a byte string or unicode string explicitly, or adjust the source code encoding." % encoding)

        return self

    def can_coerce_to_char_literal(self):
        return not self.is_identifier and len(self.value) == 1

    def generate_evaluation_code(self, code):
        self.result_code = code.get_py_string_const(
            self.value, identifier=self.is_identifier, is_str=True)

    def get_constant_c_result_code(self):
        return None

    def calculate_result_code(self):
        return self.result_code
        
    def compile_time_value(self, env):
        return self.value


class IdentifierStringNode(StringNode):
    # A special str value that represents an identifier (bytes in Py2,
    # unicode in Py3).
    is_identifier = True


class LongNode(AtomicExprNode):
    #  Python long integer literal
    #
    #  value   string

    type = py_object_type

    def calculate_constant_result(self):
        self.constant_result = long(self.value)
    
    def compile_time_value(self, denv):
        return long(self.value)
    
    def analyse_types(self, env):
        self.is_temp = 1

    gil_message = "Constructing Python long int"

    def generate_result_code(self, code):
        code.putln(
            '%s = PyLong_FromString((char *)"%s", 0, 0); %s' % (
                self.result(),
                self.value,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class ImagNode(AtomicExprNode):
    #  Imaginary number literal
    #
    #  value   float    imaginary part
    
    type = PyrexTypes.c_double_complex_type

    def calculate_constant_result(self):
        self.constant_result = complex(0.0, self.value)
    
    def compile_time_value(self, denv):
        return complex(0.0, self.value)
    
    def analyse_types(self, env):
        self.type.create_declaration_utility_code(env)

    def coerce_to(self, dst_type, env):
        if self.type is dst_type:
            return self
        node = ImagNode(self.pos, value=self.value)
        if dst_type.is_pyobject:
            node.is_temp = 1
            node.type = PyrexTypes.py_object_type
        # We still need to perform normal coerce_to processing on the
        # result, because we might be coercing to an extension type,
        # in which case a type test node will be needed.
        return AtomicExprNode.coerce_to(node, dst_type, env)

    gil_message = "Constructing complex number"

    def calculate_result_code(self):
        if self.type.is_pyobject:
            return self.result()
        else:
            return "%s(0, %r)" % (self.type.from_parts, float(self.value))

    def generate_result_code(self, code):
        if self.type.is_pyobject:
            code.putln(
                "%s = PyComplex_FromDoubles(0.0, %r); %s" % (
                    self.result(),
                    float(self.value),
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
        


class NameNode(AtomicExprNode):
    #  Reference to a local or global variable name.
    #
    #  name            string    Python name of the variable
    #  entry           Entry     Symbol table entry
    #  type_entry      Entry     For extension type names, the original type entry
    
    is_name = True
    is_cython_module = False
    cython_attribute = None
    lhs_of_first_assignment = False
    is_used_as_rvalue = 0
    entry = None
    type_entry = None

    def create_analysed_rvalue(pos, env, entry):
        node = NameNode(pos)
        node.analyse_types(env, entry=entry)
        return node
        
    def as_cython_attribute(self):
        return self.cython_attribute
    
    create_analysed_rvalue = staticmethod(create_analysed_rvalue)
    
    def type_dependencies(self, env):
        if self.entry is None:
            self.entry = env.lookup(self.name)
        if self.entry is not None and self.entry.type.is_unspecified:
            return (self.entry,)
        else:
            return ()
    
    def infer_type(self, env):
        if self.entry is None:
            self.entry = env.lookup(self.name)
        if self.entry is None:
            return py_object_type
        elif (self.entry.type.is_extension_type or self.entry.type.is_builtin_type) and \
                self.name == self.entry.type.name:
            # Unfortunately the type attribute of type objects
            # is used for the pointer to the type they represent.
            return type_type
        else:
            return self.entry.type
    
    def compile_time_value(self, denv):
        try:
            return denv.lookup(self.name)
        except KeyError:
            error(self.pos, "Compile-time name '%s' not defined" % self.name)

    def get_constant_c_result_code(self):
        if not self.entry or self.entry.type.is_pyobject:
            return None
        return self.entry.cname
    
    def coerce_to(self, dst_type, env):
        #  If coercing to a generic pyobject and this is a builtin
        #  C function with a Python equivalent, manufacture a NameNode
        #  referring to the Python builtin.
        #print "NameNode.coerce_to:", self.name, dst_type ###
        if dst_type is py_object_type:
            entry = self.entry
            if entry and entry.is_cfunction:
                var_entry = entry.as_variable
                if var_entry:
                    if var_entry.is_builtin and Options.cache_builtins:
                        var_entry = env.declare_builtin(var_entry.name, self.pos)
                    node = NameNode(self.pos, name = self.name)
                    node.entry = var_entry
                    node.analyse_rvalue_entry(env)
                    return node
        return super(NameNode, self).coerce_to(dst_type, env)
    
    def analyse_as_module(self, env):
        # Try to interpret this as a reference to a cimported module.
        # Returns the module scope, or None.
        entry = self.entry
        if not entry:
            entry = env.lookup(self.name)
        if entry and entry.as_module:
            return entry.as_module
        return None
        
    def analyse_as_type(self, env):
        if self.cython_attribute:
            type = PyrexTypes.parse_basic_type(self.cython_attribute)
        else:
            type = PyrexTypes.parse_basic_type(self.name)
        if type:
            return type
        entry = self.entry
        if not entry:
            entry = env.lookup(self.name)
        if entry and entry.is_type:
            return entry.type
        else:
            return None
    
    def analyse_as_extension_type(self, env):
        # Try to interpret this as a reference to an extension type.
        # Returns the extension type, or None.
        entry = self.entry
        if not entry:
            entry = env.lookup(self.name)
        if entry and entry.is_type and entry.type.is_extension_type:
            return entry.type
        else:
            return None
    
    def analyse_target_declaration(self, env):
        if not self.entry:
            self.entry = env.lookup_here(self.name)
        if not self.entry:
            if env.directives['warn.undeclared']:
                warning(self.pos, "implicit declaration of '%s'" % self.name, 1)
            if env.directives['infer_types'] != False:
                type = unspecified_type
            else:
                type = py_object_type
            self.entry = env.declare_var(self.name, type, self.pos)
        env.control_flow.set_state(self.pos, (self.name, 'initalized'), True)
        env.control_flow.set_state(self.pos, (self.name, 'source'), 'assignment')
        if self.entry.is_declared_generic:
            self.result_ctype = py_object_type
    
    def analyse_types(self, env):
        if self.entry is None:
            self.entry = env.lookup(self.name)
        if not self.entry:
            self.entry = env.declare_builtin(self.name, self.pos)
        if not self.entry:
            self.type = PyrexTypes.error_type
            return
        entry = self.entry
        if entry:
            entry.used = 1
            if entry.type.is_buffer:
                import Buffer
                Buffer.used_buffer_aux_vars(entry)
            if entry.utility_code:
                env.use_utility_code(entry.utility_code)
        self.analyse_rvalue_entry(env)
        
    def analyse_target_types(self, env):
        self.analyse_entry(env)
        if not self.is_lvalue():
            error(self.pos, "Assignment to non-lvalue '%s'"
                % self.name)
            self.type = PyrexTypes.error_type
        self.entry.used = 1
        if self.entry.type.is_buffer:
            import Buffer
            Buffer.used_buffer_aux_vars(self.entry)
                
    def analyse_rvalue_entry(self, env):
        #print "NameNode.analyse_rvalue_entry:", self.name ###
        #print "Entry:", self.entry.__dict__ ###
        self.analyse_entry(env)
        entry = self.entry
        if entry.is_declared_generic:
            self.result_ctype = py_object_type
        if entry.is_pyglobal or entry.is_builtin:
            if Options.cache_builtins and entry.is_builtin:
                self.is_temp = 0
            else:
                self.is_temp = 1
            self.is_used_as_rvalue = 1
            env.use_utility_code(get_name_interned_utility_code)

    def nogil_check(self, env):
        if self.is_used_as_rvalue:
            entry = self.entry
            if entry.is_builtin:
                # if not Options.cache_builtins: # cached builtins are ok
                self.gil_error()
            elif entry.is_pyglobal:
                self.gil_error()

    gil_message = "Accessing Python global or builtin"

    def analyse_entry(self, env):
        #print "NameNode.analyse_entry:", self.name ###
        self.check_identifier_kind()
        entry = self.entry
        type = entry.type
        self.type = type

    def check_identifier_kind(self):
        # Check that this is an appropriate kind of name for use in an
        # expression.  Also finds the variable entry associated with
        # an extension type.
        entry = self.entry
        if entry.is_type and entry.type.is_extension_type:
            self.type_entry = entry
        if not (entry.is_const or entry.is_variable 
            or entry.is_builtin or entry.is_cfunction):
                if self.entry.as_variable:
                    self.entry = self.entry.as_variable
                else:
                    error(self.pos, 
                          "'%s' is not a constant, variable or function identifier" % self.name)

    def is_simple(self):
        #  If it's not a C variable, it'll be in a temp.
        return 1
    
    def calculate_target_results(self, env):
        pass
    
    def check_const(self):
        entry = self.entry
        if entry is not None and not (entry.is_const or entry.is_cfunction or entry.is_builtin):
            self.not_const()
            return False
        return True
    
    def check_const_addr(self):
        entry = self.entry
        if not (entry.is_cglobal or entry.is_cfunction or entry.is_builtin):
            self.addr_not_const()
            return False
        return True

    def is_lvalue(self):
        return self.entry.is_variable and \
            not self.entry.type.is_array and \
            not self.entry.is_readonly
    
    def is_ephemeral(self):
        #  Name nodes are never ephemeral, even if the
        #  result is in a temporary.
        return 0
    
    def calculate_result_code(self):
        entry = self.entry
        if not entry:
            return "<error>" # There was an error earlier
        return entry.cname
    
    def generate_result_code(self, code):
        assert hasattr(self, 'entry')
        entry = self.entry
        if entry is None:
            return # There was an error earlier
        if entry.is_builtin and Options.cache_builtins:
            return # Lookup already cached
        elif entry.is_pyglobal or entry.is_builtin:
            assert entry.type.is_pyobject, "Python global or builtin not a Python object"
            interned_cname = code.intern_identifier(self.entry.name)
            if entry.is_builtin:
                namespace = Naming.builtins_cname
            else: # entry.is_pyglobal
                namespace = entry.scope.namespace_cname
            code.putln(
                '%s = __Pyx_GetName(%s, %s); %s' % (
                self.result(),
                namespace, 
                interned_cname,
                code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
            
        elif entry.is_local and False:
            # control flow not good enough yet
            assigned = entry.scope.control_flow.get_state((entry.name, 'initalized'), self.pos)
            if assigned is False:
                error(self.pos, "local variable '%s' referenced before assignment" % entry.name)
            elif not Options.init_local_none and assigned is None:
                code.putln('if (%s == 0) { PyErr_SetString(PyExc_UnboundLocalError, "%s"); %s }' %
                           (entry.cname, entry.name, code.error_goto(self.pos)))
                entry.scope.control_flow.set_state(self.pos, (entry.name, 'initalized'), True)

    def generate_assignment_code(self, rhs, code):
        #print "NameNode.generate_assignment_code:", self.name ###
        entry = self.entry
        if entry is None:
            return # There was an error earlier

        if (self.entry.type.is_ptr and isinstance(rhs, ListNode)
            and not self.lhs_of_first_assignment):
            error(self.pos, "Literal list must be assigned to pointer at time of declaration")
        
        # is_pyglobal seems to be True for module level-globals only.
        # We use this to access class->tp_dict if necessary.
        if entry.is_pyglobal:
            assert entry.type.is_pyobject, "Python global or builtin not a Python object"
            interned_cname = code.intern_identifier(self.entry.name)
            namespace = self.entry.scope.namespace_cname
            if entry.is_member:
                # if the entry is a member we have to cheat: SetAttr does not work
                # on types, so we create a descriptor which is then added to tp_dict
                code.put_error_if_neg(self.pos,
                    'PyDict_SetItem(%s->tp_dict, %s, %s)' % (
                        namespace,
                        interned_cname,
                        rhs.py_result()))
                rhs.generate_disposal_code(code)
                rhs.free_temps(code)
                # in Py2.6+, we need to invalidate the method cache
                code.putln("PyType_Modified(%s);" %
                           entry.scope.parent_type.typeptr_cname)
            else: 
                code.put_error_if_neg(self.pos,
                    'PyObject_SetAttr(%s, %s, %s)' % (
                        namespace,
                        interned_cname,
                        rhs.py_result()))
                if debug_disposal_code:
                    print("NameNode.generate_assignment_code:")
                    print("...generating disposal code for %s" % rhs)
                rhs.generate_disposal_code(code)
                rhs.free_temps(code)
        else:
            if self.type.is_buffer:
                # Generate code for doing the buffer release/acquisition.
                # This might raise an exception in which case the assignment (done
                # below) will not happen.
                #
                # The reason this is not in a typetest-like node is because the
                # variables that the acquired buffer info is stored to is allocated
                # per entry and coupled with it.
                self.generate_acquire_buffer(rhs, code)

            if self.type.is_pyobject:
                #print "NameNode.generate_assignment_code: to", self.name ###
                #print "...from", rhs ###
                #print "...LHS type", self.type, "ctype", self.ctype() ###
                #print "...RHS type", rhs.type, "ctype", rhs.ctype() ###
                if self.use_managed_ref:
                    rhs.make_owned_reference(code)
                    if entry.is_cglobal:
                        code.put_gotref(self.py_result())
                if self.use_managed_ref and not self.lhs_of_first_assignment:
                    if entry.is_local and not Options.init_local_none:
                        initalized = entry.scope.control_flow.get_state((entry.name, 'initalized'), self.pos)
                        if initalized is True:
                            code.put_decref(self.result(), self.ctype())
                        elif initalized is None:
                            code.put_xdecref(self.result(), self.ctype())
                    else:
                        code.put_decref(self.result(), self.ctype())
                if self.use_managed_ref:
                    if entry.is_cglobal:
                        code.put_giveref(rhs.py_result())
            code.putln('%s = %s;' % (self.result(), rhs.result_as(self.ctype())))
            if debug_disposal_code:
                print("NameNode.generate_assignment_code:")
                print("...generating post-assignment code for %s" % rhs)
            rhs.generate_post_assignment_code(code)
            rhs.free_temps(code)

    def generate_acquire_buffer(self, rhs, code):
        # rhstmp is only used in case the rhs is a complicated expression leading to
        # the object, to avoid repeating the same C expression for every reference
        # to the rhs. It does NOT hold a reference.
        pretty_rhs = isinstance(rhs, NameNode) or rhs.is_temp
        if pretty_rhs:
            rhstmp = rhs.result_as(self.ctype())
        else:
            rhstmp = code.funcstate.allocate_temp(self.entry.type, manage_ref=False)
            code.putln('%s = %s;' % (rhstmp, rhs.result_as(self.ctype())))

        buffer_aux = self.entry.buffer_aux
        bufstruct = buffer_aux.buffer_info_var.cname
        import Buffer
        Buffer.put_assign_to_buffer(self.result(), rhstmp, buffer_aux, self.entry.type,
                                    is_initialized=not self.lhs_of_first_assignment,
                                    pos=self.pos, code=code)
        
        if not pretty_rhs:
            code.putln("%s = 0;" % rhstmp)
            code.funcstate.release_temp(rhstmp)
    
    def generate_deletion_code(self, code):
        if self.entry is None:
            return # There was an error earlier
        if not self.entry.is_pyglobal:
            error(self.pos, "Deletion of local or C global name not supported")
            return
        code.put_error_if_neg(self.pos, 
            '__Pyx_DelAttrString(%s, "%s")' % (
                Naming.module_cname,
                self.entry.name))
                
    def annotate(self, code):
        if hasattr(self, 'is_called') and self.is_called:
            pos = (self.pos[0], self.pos[1], self.pos[2] - len(self.name) - 1)
            if self.type.is_pyobject:
                code.annotate(pos, AnnotationItem('py_call', 'python function', size=len(self.name)))
            else:
                code.annotate(pos, AnnotationItem('c_call', 'c function', size=len(self.name)))
            
class BackquoteNode(ExprNode):
    #  `expr`
    #
    #  arg    ExprNode
    
    type = py_object_type
    
    subexprs = ['arg']
    
    def analyse_types(self, env):
        self.arg.analyse_types(env)
        self.arg = self.arg.coerce_to_pyobject(env)
        self.is_temp = 1

    gil_message = "Backquote expression"

    def calculate_constant_result(self):
        self.constant_result = repr(self.arg.constant_result)

    def generate_result_code(self, code):
        code.putln(
            "%s = PyObject_Repr(%s); %s" % (
                self.result(),
                self.arg.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())
        


class ImportNode(ExprNode):
    #  Used as part of import statement implementation.
    #  Implements result = 
    #    __import__(module_name, globals(), None, name_list)
    #
    #  module_name   StringNode            dotted name of module
    #  name_list     ListNode or None      list of names to be imported
    
    type = py_object_type
    
    subexprs = ['module_name', 'name_list']
    
    def analyse_types(self, env):
        self.module_name.analyse_types(env)
        self.module_name = self.module_name.coerce_to_pyobject(env)
        if self.name_list:
            self.name_list.analyse_types(env)
            self.name_list.coerce_to_pyobject(env)
        self.is_temp = 1
        env.use_utility_code(import_utility_code)

    gil_message = "Python import"

    def generate_result_code(self, code):
        if self.name_list:
            name_list_code = self.name_list.py_result()
        else:
            name_list_code = "0"
        code.putln(
            "%s = __Pyx_Import(%s, %s); %s" % (
                self.result(),
                self.module_name.py_result(),
                name_list_code,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class IteratorNode(ExprNode):
    #  Used as part of for statement implementation.
    #
    #  allocate_counter_temp/release_counter_temp needs to be called
    #  by parent (ForInStatNode)
    #
    #  Implements result = iter(sequence)
    #
    #  sequence   ExprNode
    
    type = py_object_type
    
    subexprs = ['sequence']
    
    def analyse_types(self, env):
        self.sequence.analyse_types(env)
        self.sequence = self.sequence.coerce_to_pyobject(env)
        self.is_temp = 1

    gil_message = "Iterating over Python object"

    def allocate_counter_temp(self, code):
        self.counter_cname = code.funcstate.allocate_temp(
            PyrexTypes.c_py_ssize_t_type, manage_ref=False)

    def release_counter_temp(self, code):
        code.funcstate.release_temp(self.counter_cname)

    def generate_result_code(self, code):
        is_builtin_sequence = self.sequence.type is list_type or \
                              self.sequence.type is tuple_type
        may_be_a_sequence = is_builtin_sequence or not self.sequence.type.is_builtin_type
        if is_builtin_sequence:
            code.putln(
                "if (likely(%s != Py_None)) {" % self.sequence.py_result())
        elif may_be_a_sequence:
            code.putln(
                "if (PyList_CheckExact(%s) || PyTuple_CheckExact(%s)) {" % (
                    self.sequence.py_result(),
                    self.sequence.py_result()))
        if may_be_a_sequence:
            code.putln(
                "%s = 0; %s = %s; __Pyx_INCREF(%s);" % (
                    self.counter_cname,
                    self.result(),
                    self.sequence.py_result(),
                    self.result()))
            code.putln("} else {")
        if is_builtin_sequence:
            code.putln(
                'PyErr_SetString(PyExc_TypeError, "\'NoneType\' object is not iterable"); %s' %
                code.error_goto(self.pos))
        else:
            code.putln("%s = -1; %s = PyObject_GetIter(%s); %s" % (
                    self.counter_cname,
                    self.result(),
                    self.sequence.py_result(),
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
        if may_be_a_sequence:
            code.putln("}")


class NextNode(AtomicExprNode):
    #  Used as part of for statement implementation.
    #  Implements result = iterator.next()
    #  Created during analyse_types phase.
    #  The iterator is not owned by this node.
    #
    #  iterator   ExprNode
    
    type = py_object_type
    
    def __init__(self, iterator, env):
        self.pos = iterator.pos
        self.iterator = iterator
        self.is_temp = 1
    
    def generate_result_code(self, code):
        sequence_type = self.iterator.sequence.type
        if sequence_type is list_type:
            type_checks = [(list_type, "List")]
        elif sequence_type is tuple_type:
            type_checks = [(tuple_type, "Tuple")]
        elif not sequence_type.is_builtin_type:
            type_checks = [(list_type, "List"), (tuple_type, "Tuple")]
        else:
            type_checks = []

        for py_type, prefix in type_checks:
            if len(type_checks) > 1:
                code.putln(
                    "if (likely(Py%s_CheckExact(%s))) {" % (
                        prefix, self.iterator.py_result()))
            code.putln(
                "if (%s >= Py%s_GET_SIZE(%s)) break;" % (
                    self.iterator.counter_cname,
                    prefix,
                    self.iterator.py_result()))
            code.putln(
                "%s = Py%s_GET_ITEM(%s, %s); __Pyx_INCREF(%s); %s++;" % (
                    self.result(),
                    prefix,
                    self.iterator.py_result(),
                    self.iterator.counter_cname,
                    self.result(),
                    self.iterator.counter_cname))
            if len(type_checks) > 1:
                code.put("} else ")
        if len(type_checks) == 1:
            return
        code.putln("{")
        code.putln(
            "%s = PyIter_Next(%s);" % (
                self.result(),
                self.iterator.py_result()))
        code.putln(
            "if (!%s) {" %
                self.result())
        code.putln(code.error_goto_if_PyErr(self.pos))
        code.putln("break;")
        code.putln("}")
        code.put_gotref(self.py_result())
        code.putln("}")


class ExcValueNode(AtomicExprNode):
    #  Node created during analyse_types phase
    #  of an ExceptClauseNode to fetch the current
    #  exception value.
    
    type = py_object_type
    
    def __init__(self, pos, env):
        ExprNode.__init__(self, pos)

    def set_var(self, var):
        self.var = var
    
    def calculate_result_code(self):
        return self.var

    def generate_result_code(self, code):
        pass

    def analyse_types(self, env):
        pass


class TempNode(ExprNode):
    # Node created during analyse_types phase
    # of some nodes to hold a temporary value.
    #
    # Note: One must call "allocate" and "release" on
    # the node during code generation to get/release the temp.
    # This is because the temp result is often used outside of
    # the regular cycle.

    subexprs = []
    
    def __init__(self, pos, type, env):
        ExprNode.__init__(self, pos)
        self.type = type
        if type.is_pyobject:
            self.result_ctype = py_object_type
        self.is_temp = 1
        
    def analyse_types(self, env):
        return self.type
    
    def generate_result_code(self, code):
        pass

    def allocate(self, code):
        self.temp_cname = code.funcstate.allocate_temp(self.type, manage_ref=True)

    def release(self, code):
        code.funcstate.release_temp(self.temp_cname)
        self.temp_cname = None

    def result(self):
        try:
            return self.temp_cname
        except:
            assert False, "Remember to call allocate/release on TempNode"
            raise

    # Do not participate in normal temp alloc/dealloc:
    def allocate_temp_result(self, code):
        pass
    
    def release_temp_result(self, code):
        pass

class PyTempNode(TempNode):
    #  TempNode holding a Python value.
    
    def __init__(self, pos, env):
        TempNode.__init__(self, pos, PyrexTypes.py_object_type, env)

class RawCNameExprNode(ExprNode):
    subexprs = []
    
    def __init__(self, pos, type=None):
        self.pos = pos
        self.type = type

    def analyse_types(self, env):
        return self.type

    def set_cname(self, cname):
        self.cname = cname

    def result(self):
        return self.cname

    def generate_result_code(self, code):
        pass


#-------------------------------------------------------------------
#
#  Trailer nodes
#
#-------------------------------------------------------------------

class IndexNode(ExprNode):
    #  Sequence indexing.
    #
    #  base     ExprNode
    #  index    ExprNode
    #  indices  [ExprNode]
    #  is_buffer_access boolean Whether this is a buffer access.
    #
    #  indices is used on buffer access, index on non-buffer access.
    #  The former contains a clean list of index parameters, the
    #  latter whatever Python object is needed for index access.
    
    subexprs = ['base', 'index', 'indices']
    indices = None

    def __init__(self, pos, index, *args, **kw):
        ExprNode.__init__(self, pos, index=index, *args, **kw)
        self._index = index

    def calculate_constant_result(self):
        self.constant_result = \
            self.base.constant_result[self.index.constant_result]

    def compile_time_value(self, denv):
        base = self.base.compile_time_value(denv)
        index = self.index.compile_time_value(denv)
        try:
            return base[index]
        except Exception, e:
            self.compile_time_value_error(e)
    
    def is_ephemeral(self):
        return self.base.is_ephemeral()
    
    def analyse_target_declaration(self, env):
        pass
        
    def analyse_as_type(self, env):
        base_type = self.base.analyse_as_type(env)
        if base_type and not base_type.is_pyobject:
            return PyrexTypes.CArrayType(base_type, int(self.index.compile_time_value(env)))
        return None
    
    def type_dependencies(self, env):
        return self.base.type_dependencies(env)
    
    def infer_type(self, env):
        if isinstance(self.base, (StringNode, UnicodeNode)): # FIXME: BytesNode?
            return py_object_type
        base_type = self.base.infer_type(env)
        if base_type.is_ptr or base_type.is_array:
            return base_type.base_type
        else:
            # TODO: Handle buffers (hopefully without too much redundancy).
            return py_object_type
    
    def analyse_types(self, env):
        self.analyse_base_and_index_types(env, getting = 1)
    
    def analyse_target_types(self, env):
        self.analyse_base_and_index_types(env, setting = 1)

    def analyse_base_and_index_types(self, env, getting = 0, setting = 0):
        # Note: This might be cleaned up by having IndexNode
        # parsed in a saner way and only construct the tuple if
        # needed.

        # Note that this function must leave IndexNode in a cloneable state.
        # For buffers, self.index is packed out on the initial analysis, and
        # when cloning self.indices is copied.
        self.is_buffer_access = False

        self.base.analyse_types(env)
        if self.base.type.is_error:
            # Do not visit child tree if base is undeclared to avoid confusing
            # error messages
            self.type = PyrexTypes.error_type
            return
        
        # Handle the case where base is a literal char* (and we expect a string, not an int)
        if isinstance(self.base, BytesNode):
            self.base = self.base.coerce_to_pyobject(env)

        skip_child_analysis = False
        buffer_access = False
        if self.base.type.is_buffer:
            assert hasattr(self.base, "entry") # Must be a NameNode-like node
            if self.indices:
                indices = self.indices
            else:
                if isinstance(self.index, TupleNode):
                    indices = self.index.args
                else:
                    indices = [self.index]
            if len(indices) == self.base.type.ndim:
                buffer_access = True
                skip_child_analysis = True
                for x in indices:
                    x.analyse_types(env)
                    if not x.type.is_int:
                        buffer_access = False

        # On cloning, indices is cloned. Otherwise, unpack index into indices
        assert not (buffer_access and isinstance(self.index, CloneNode))

        if buffer_access:
            self.indices = indices
            self.index = None
            self.type = self.base.type.dtype
            self.is_buffer_access = True
            self.buffer_type = self.base.entry.type

            if getting and self.type.is_pyobject:
                self.is_temp = True
            if setting:
                if not self.base.entry.type.writable:
                    error(self.pos, "Writing to readonly buffer")
                else:
                    self.base.entry.buffer_aux.writable_needed = True
        else:
            if isinstance(self.index, TupleNode):
                self.index.analyse_types(env, skip_children=skip_child_analysis)
            elif not skip_child_analysis:
                self.index.analyse_types(env)
            self.original_index_type = self.index.type
            if self.base.type.is_pyobject:
                if self.index.type.is_int:
                    if (not setting
                        and (self.base.type is list_type or self.base.type is tuple_type)
                        and (not self.index.type.signed or isinstance(self.index, IntNode) and int(self.index.value) >= 0)
                        and not env.directives['boundscheck']):
                        self.is_temp = 0
                    else:
                        self.is_temp = 1
                    self.index = self.index.coerce_to(PyrexTypes.c_py_ssize_t_type, env).coerce_to_simple(env)
                else:
                    self.index = self.index.coerce_to_pyobject(env)
                    self.is_temp = 1
                self.type = py_object_type
            else:
                if self.base.type.is_ptr or self.base.type.is_array:
                    self.type = self.base.type.base_type
                else:
                    error(self.pos,
                        "Attempting to index non-array type '%s'" %
                            self.base.type)
                    self.type = PyrexTypes.error_type
                if self.index.type.is_pyobject:
                    self.index = self.index.coerce_to(
                        PyrexTypes.c_py_ssize_t_type, env)
                if not self.index.type.is_int:
                    error(self.pos,
                        "Invalid index type '%s'" %
                            self.index.type)
    gil_message = "Indexing Python object"

    def nogil_check(self, env):
        if self.is_buffer_access:
            if env.directives['boundscheck']:
                error(self.pos, "Cannot check buffer index bounds without gil; use boundscheck(False) directive")
                return
            elif self.type.is_pyobject:
                error(self.pos, "Cannot access buffer with object dtype without gil")
                return
        super(IndexNode, self).nogil_check(env)


    def check_const_addr(self):
        return self.base.check_const_addr() and self.index.check_const()
    
    def is_lvalue(self):
        return 1

    def calculate_result_code(self):
        if self.is_buffer_access:
            return "(*%s)" % self.buffer_ptr_code
        elif self.base.type is list_type:
            return "PyList_GET_ITEM(%s, %s)" % (self.base.result(), self.index.result())
        elif self.base.type is tuple_type:
            return "PyTuple_GET_ITEM(%s, %s)" % (self.base.result(), self.index.result())
        else:
            return "(%s[%s])" % (
                self.base.result(), self.index.result())
            
    def extra_index_params(self):
        if self.index.type.is_int:
            if self.original_index_type.signed:
                size_adjustment = ""
            else:
                size_adjustment = "+1"
            return ", sizeof(%s)%s, %s" % (self.original_index_type.declaration_code(""), size_adjustment, self.original_index_type.to_py_function)
        else:
            return ""

    def generate_subexpr_evaluation_code(self, code):
        self.base.generate_evaluation_code(code)
        if not self.indices:
            self.index.generate_evaluation_code(code)
        else:
            for i in self.indices:
                i.generate_evaluation_code(code)
        
    def generate_subexpr_disposal_code(self, code):
        self.base.generate_disposal_code(code)
        if not self.indices:
            self.index.generate_disposal_code(code)
        else:
            for i in self.indices:
                i.generate_disposal_code(code)

    def free_subexpr_temps(self, code):
        self.base.free_temps(code)
        if not self.indices:
            self.index.free_temps(code)
        else:
            for i in self.indices:
                i.free_temps(code)

    def generate_result_code(self, code):
        if self.is_buffer_access:
            if code.globalstate.directives['nonecheck']:
                self.put_nonecheck(code)
            self.buffer_ptr_code = self.buffer_lookup_code(code)
            if self.type.is_pyobject:
                # is_temp is True, so must pull out value and incref it.
                code.putln("%s = *%s;" % (self.result(), self.buffer_ptr_code))
                code.putln("__Pyx_INCREF((PyObject*)%s);" % self.result())
        elif self.type.is_pyobject and self.is_temp:
            if self.index.type.is_int:
                index_code = self.index.result()
                if self.base.type is list_type:
                    function = "__Pyx_GetItemInt_List"
                elif self.base.type is tuple_type:
                    function = "__Pyx_GetItemInt_Tuple"
                else:
                    function = "__Pyx_GetItemInt"
                code.globalstate.use_utility_code(getitem_int_utility_code)
            else:
                function = "PyObject_GetItem"
                index_code = self.index.py_result()
                sign_code = ""
            code.putln(
                "%s = %s(%s, %s%s); if (!%s) %s" % (
                    self.result(),
                    function,
                    self.base.py_result(),
                    index_code,
                    self.extra_index_params(),
                    self.result(),
                    code.error_goto(self.pos)))
            code.put_gotref(self.py_result())
            
    def generate_setitem_code(self, value_code, code):
        if self.index.type.is_int:
            function = "__Pyx_SetItemInt"
            index_code = self.index.result()
            code.globalstate.use_utility_code(setitem_int_utility_code)
        else:
            index_code = self.index.py_result()
            if self.base.type is dict_type:
                function = "PyDict_SetItem"
            # It would seem that we could specalized lists/tuples, but that
            # shouldn't happen here. 
            # Both PyList_SetItem PyTuple_SetItem and a Py_ssize_t as input, 
            # not a PyObject*, and bad conversion here would give the wrong 
            # exception. Also, tuples are supposed to be immutable, and raise 
            # TypeErrors when trying to set their entries (PyTuple_SetItem 
            # is for creating new tuples from). 
            else:
                function = "PyObject_SetItem"
        code.putln(
            "if (%s(%s, %s, %s%s) < 0) %s" % (
                function,
                self.base.py_result(),
                index_code,
                value_code,
                self.extra_index_params(),
                code.error_goto(self.pos)))

    def generate_buffer_setitem_code(self, rhs, code, op=""):
        # Used from generate_assignment_code and InPlaceAssignmentNode
        if code.globalstate.directives['nonecheck']:
            self.put_nonecheck(code)
        ptrexpr = self.buffer_lookup_code(code)
        if self.buffer_type.dtype.is_pyobject:
            # Must manage refcounts. Decref what is already there
            # and incref what we put in.
            ptr = code.funcstate.allocate_temp(self.buffer_type.buffer_ptr_type, manage_ref=False)
            rhs_code = rhs.result()
            code.putln("%s = %s;" % (ptr, ptrexpr))
            code.put_gotref("*%s" % ptr)
            code.putln("__Pyx_DECREF(*%s); __Pyx_INCREF(%s);" % (
                ptr, rhs_code
                ))
            code.putln("*%s %s= %s;" % (ptr, op, rhs_code))
            code.put_giveref("*%s" % ptr)
            code.funcstate.release_temp(ptr)
        else: 
            # Simple case
            code.putln("*%s %s= %s;" % (ptrexpr, op, rhs.result()))

    def generate_assignment_code(self, rhs, code):
        self.generate_subexpr_evaluation_code(code)
        if self.is_buffer_access:
            self.generate_buffer_setitem_code(rhs, code)
        elif self.type.is_pyobject:
            self.generate_setitem_code(rhs.py_result(), code)
        else:
            code.putln(
                "%s = %s;" % (
                    self.result(), rhs.result()))
        self.generate_subexpr_disposal_code(code)
        self.free_subexpr_temps(code)
        rhs.generate_disposal_code(code)
        rhs.free_temps(code)
    
    def generate_deletion_code(self, code):
        self.generate_subexpr_evaluation_code(code)
        #if self.type.is_pyobject:
        if self.index.type.is_int:
            function = "__Pyx_DelItemInt"
            index_code = self.index.result()
            code.globalstate.use_utility_code(delitem_int_utility_code)
        else:
            index_code = self.index.py_result()
            if self.base.type is dict_type:
                function = "PyDict_DelItem"
            else:
                function = "PyObject_DelItem"
        code.putln(
            "if (%s(%s, %s%s) < 0) %s" % (
                function,
                self.base.py_result(),
                index_code,
                self.extra_index_params(),
                code.error_goto(self.pos)))
        self.generate_subexpr_disposal_code(code)
        self.free_subexpr_temps(code)

    def buffer_lookup_code(self, code):
        # Assign indices to temps
        index_temps = [code.funcstate.allocate_temp(i.type, manage_ref=False) for i in self.indices]
        for temp, index in zip(index_temps, self.indices):
            code.putln("%s = %s;" % (temp, index.result()))
        # Generate buffer access code using these temps
        import Buffer
        # The above could happen because child_attrs is wrong somewhere so that
        # options are not propagated.
        return Buffer.put_buffer_lookup_code(entry=self.base.entry,
                                             index_signeds=[i.type.signed for i in self.indices],
                                             index_cnames=index_temps,
                                             directives=code.globalstate.directives,
                                             pos=self.pos, code=code)

    def put_nonecheck(self, code):
        code.globalstate.use_utility_code(raise_noneindex_error_utility_code)
        code.putln("if (%s) {" % code.unlikely("%s == Py_None") % self.base.result_as(PyrexTypes.py_object_type))
        code.putln("__Pyx_RaiseNoneIndexingError();")
        code.putln(code.error_goto(self.pos))
        code.putln("}")

class SliceIndexNode(ExprNode):
    #  2-element slice indexing
    #
    #  base      ExprNode
    #  start     ExprNode or None
    #  stop      ExprNode or None
    
    subexprs = ['base', 'start', 'stop']

    def infer_type(self, env):
        base_type = self.base.infer_type(env)
        if base_type.is_string:
            return bytes_type
        elif base_type in (bytes_type, str_type, unicode_type,
                           list_type, tuple_type):
            return base_type
        return py_object_type

    def calculate_constant_result(self):
        self.constant_result = self.base.constant_result[
            self.start.constant_result : self.stop.constant_result]

    def compile_time_value(self, denv):
        base = self.base.compile_time_value(denv)
        if self.start is None:
            start = 0
        else:
            start = self.start.compile_time_value(denv)
        if self.stop is None:
            stop = None
        else:
            stop = self.stop.compile_time_value(denv)
        try:
            return base[start:stop]
        except Exception, e:
            self.compile_time_value_error(e)
    
    def analyse_target_declaration(self, env):
        pass
    
    def analyse_target_types(self, env):
        self.analyse_types(env)
        # when assigning, we must accept any Python type
        if self.type.is_pyobject:
            self.type = py_object_type

    def analyse_types(self, env):
        self.base.analyse_types(env)
        if self.start:
            self.start.analyse_types(env)
        if self.stop:
            self.stop.analyse_types(env)
        base_type = self.base.type
        if base_type.is_string:
            self.type = bytes_type
        elif base_type.is_array or base_type.is_ptr:
            # we need a ptr type here instead of an array type, as
            # array types can result in invalid type casts in the C
            # code
            self.type = PyrexTypes.CPtrType(base_type.base_type)
        else:
            self.base = self.base.coerce_to_pyobject(env)
            self.type = py_object_type
        if base_type.is_builtin_type:
            # slicing builtin types returns something of the same type
            self.type = base_type
        c_int = PyrexTypes.c_py_ssize_t_type
        if self.start:
            self.start = self.start.coerce_to(c_int, env)
        if self.stop:
            self.stop = self.stop.coerce_to(c_int, env)
        self.is_temp = 1

    nogil_check = Node.gil_error
    gil_message = "Slicing Python object"

    def generate_result_code(self, code):
        if not self.type.is_pyobject:
            error(self.pos,
                  "Slicing is not currently supported for '%s'." % self.type)
            return
        if self.base.type.is_string:
            if self.stop is None:
                code.putln(
                    "%s = __Pyx_PyBytes_FromString(%s + %s); %s" % (
                        self.result(),
                        self.base.result(),
                        self.start_code(),
                        code.error_goto_if_null(self.result(), self.pos)))
            else:
                code.putln(
                    "%s = __Pyx_PyBytes_FromStringAndSize(%s + %s, %s - %s); %s" % (
                        self.result(),
                        self.base.result(),
                        self.start_code(),
                        self.stop_code(),
                        self.start_code(),
                        code.error_goto_if_null(self.result(), self.pos)))
        else:
            code.putln(
                "%s = PySequence_GetSlice(%s, %s, %s); %s" % (
                    self.result(),
                    self.base.py_result(),
                    self.start_code(),
                    self.stop_code(),
                    code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())
    
    def generate_assignment_code(self, rhs, code):
        self.generate_subexpr_evaluation_code(code)
        if self.type.is_pyobject:
            code.put_error_if_neg(self.pos, 
                "PySequence_SetSlice(%s, %s, %s, %s)" % (
                    self.base.py_result(),
                    self.start_code(),
                    self.stop_code(),
                    rhs.result()))
        else:
            start_offset = ''
            if self.start:
                start_offset = self.start_code()
                if start_offset == '0':
                    start_offset = ''
                else:
                    start_offset += '+'
            if rhs.type.is_array:
                array_length = rhs.type.size
                self.generate_slice_guard_code(code, array_length)
            else:
                error(self.pos,
                      "Slice assignments from pointers are not yet supported.")
                # FIXME: fix the array size according to start/stop
                array_length = self.base.type.size
            for i in range(array_length):
                code.putln("%s[%s%s] = %s[%d];" % (
                        self.base.result(), start_offset, i,
                        rhs.result(), i))
        self.generate_subexpr_disposal_code(code)
        self.free_subexpr_temps(code)
        rhs.generate_disposal_code(code)
        rhs.free_temps(code)

    def generate_deletion_code(self, code):
        if not self.base.type.is_pyobject:
            error(self.pos,
                  "Deleting slices is only supported for Python types, not '%s'." % self.type)
            return
        self.generate_subexpr_evaluation_code(code)
        code.put_error_if_neg(self.pos,
            "PySequence_DelSlice(%s, %s, %s)" % (
                self.base.py_result(),
                self.start_code(),
                self.stop_code()))
        self.generate_subexpr_disposal_code(code)

    def generate_slice_guard_code(self, code, target_size):
        if not self.base.type.is_array:
            return
        slice_size = self.base.type.size
        start = stop = None
        if self.stop:
            stop = self.stop.result()
            try:
                stop = int(stop)
                if stop < 0:
                    slice_size = self.base.type.size + stop
                else:
                    slice_size = stop
                stop = None
            except ValueError:
                pass
        if self.start:
            start = self.start.result()
            try:
                start = int(start)
                if start < 0:
                    start = self.base.type.size + start
                slice_size -= start
                start = None
            except ValueError:
                pass
        check = None
        if slice_size < 0:
            if target_size > 0:
                error(self.pos, "Assignment to empty slice.")
        elif start is None and stop is None:
            # we know the exact slice length
            if target_size != slice_size:
                error(self.pos, "Assignment to slice of wrong length, expected %d, got %d" % (
                        slice_size, target_size))
        elif start is not None:
            if stop is None:
                stop = slice_size
            check = "(%s)-(%s)" % (stop, start)
        else: # stop is not None:
            check = stop
        if check:
            code.putln("if (unlikely((%s) != %d)) {" % (check, target_size))
            code.putln('PyErr_Format(PyExc_ValueError, "Assignment to slice of wrong length, expected %%"PY_FORMAT_SIZE_T"d, got %%"PY_FORMAT_SIZE_T"d", (Py_ssize_t)%d, (Py_ssize_t)(%s));' % (
                        target_size, check))
            code.putln(code.error_goto(self.pos))
            code.putln("}")
    
    def start_code(self):
        if self.start:
            return self.start.result()
        else:
            return "0"
    
    def stop_code(self):
        if self.stop:
            return self.stop.result()
        elif self.base.type.is_array:
            return self.base.type.size
        else:
            return "PY_SSIZE_T_MAX"
    
    def calculate_result_code(self):
        # self.result() is not used, but this method must exist
        return "<unused>"
    

class SliceNode(ExprNode):
    #  start:stop:step in subscript list
    #
    #  start     ExprNode
    #  stop      ExprNode
    #  step      ExprNode
    
    type = py_object_type
    is_temp = 1

    def calculate_constant_result(self):
        self.constant_result = self.base.constant_result[
            self.start.constant_result : \
                self.stop.constant_result : \
                self.step.constant_result]

    def compile_time_value(self, denv):
        start = self.start.compile_time_value(denv)
        if self.stop is None:
            stop = None
        else:
            stop = self.stop.compile_time_value(denv)
        if self.step is None:
            step = None
        else:
            step = self.step.compile_time_value(denv)
        try:
            return slice(start, stop, step)
        except Exception, e:
            self.compile_time_value_error(e)

    subexprs = ['start', 'stop', 'step']
    
    def analyse_types(self, env):
        self.start.analyse_types(env)
        self.stop.analyse_types(env)
        self.step.analyse_types(env)
        self.start = self.start.coerce_to_pyobject(env)
        self.stop = self.stop.coerce_to_pyobject(env)
        self.step = self.step.coerce_to_pyobject(env)

    gil_message = "Constructing Python slice object"

    def generate_result_code(self, code):
        code.putln(
            "%s = PySlice_New(%s, %s, %s); %s" % (
                self.result(),
                self.start.py_result(), 
                self.stop.py_result(), 
                self.step.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class CallNode(ExprNode):

    def analyse_as_type_constructor(self, env):
        type = self.function.analyse_as_type(env)
        if type and type.is_struct_or_union:
            args, kwds = self.explicit_args_kwds()
            items = []
            for arg, member in zip(args, type.scope.var_entries):
                items.append(DictItemNode(pos=arg.pos, key=StringNode(pos=arg.pos, value=member.name), value=arg))
            if kwds:
                items += kwds.key_value_pairs
            self.key_value_pairs = items
            self.__class__ = DictNode
            self.analyse_types(env)
            self.coerce_to(type, env)
            return True

    def nogil_check(self, env):
        func_type = self.function_type()
        if func_type.is_pyobject:
            self.gil_error()
        elif not getattr(func_type, 'nogil', False):
            self.gil_error()

    gil_message = "Calling gil-requiring function"


class SimpleCallNode(CallNode):
    #  Function call without keyword, * or ** args.
    #
    #  function       ExprNode
    #  args           [ExprNode]
    #  arg_tuple      ExprNode or None     used internally
    #  self           ExprNode or None     used internally
    #  coerced_self   ExprNode or None     used internally
    #  wrapper_call   bool                 used internally
    #  has_optional_args   bool            used internally
    
    subexprs = ['self', 'coerced_self', 'function', 'args', 'arg_tuple']
    
    self = None
    coerced_self = None
    arg_tuple = None
    wrapper_call = False
    has_optional_args = False
    
    def compile_time_value(self, denv):
        function = self.function.compile_time_value(denv)
        args = [arg.compile_time_value(denv) for arg in self.args]
        try:
            return function(*args)
        except Exception, e:
            self.compile_time_value_error(e)
            
    def type_dependencies(self, env):
        # TODO: Update when Danilo's C++ code merged in to handle the
        # the case of function overloading.
        return self.function.type_dependencies(env)
    
    def infer_type(self, env):
        function = self.function
        func_type = function.infer_type(env)
        if func_type.is_ptr:
            func_type = func_type.base_type
        if func_type.is_cfunction:
            return func_type.return_type
        elif func_type is type_type:
            if function.is_name and function.entry and function.entry.type:
                result_type = function.entry.type
                if result_type.is_extension_type:
                    return result_type
                elif result_type.is_builtin_type:
                    if function.entry.name == 'float':
                        return PyrexTypes.c_double_type
                    elif function.entry.name in Builtin.types_that_construct_their_instance:
                        return result_type
        return py_object_type

    def analyse_as_type(self, env):
        attr = self.function.as_cython_attribute()
        if attr == 'pointer':
            if len(self.args) != 1:
                error(self.args.pos, "only one type allowed.")
            else:
                type = self.args[0].analyse_as_type(env)
                if not type:
                    error(self.args[0].pos, "Unknown type")
                else:
                    return PyrexTypes.CPtrType(type)

    def explicit_args_kwds(self):
        return self.args, None

    def analyse_types(self, env):
        if self.analyse_as_type_constructor(env):
            return
        function = self.function
        function.is_called = 1
        self.function.analyse_types(env)
        if function.is_attribute and function.entry and function.entry.is_cmethod:
            # Take ownership of the object from which the attribute
            # was obtained, because we need to pass it as 'self'.
            self.self = function.obj
            function.obj = CloneNode(self.self)
        func_type = self.function_type()
        if func_type.is_pyobject:
            self.arg_tuple = TupleNode(self.pos, args = self.args)
            self.arg_tuple.analyse_types(env)
            self.args = None
            if func_type is Builtin.type_type and function.is_name and \
                   function.entry and \
                   function.entry.is_builtin and \
                   function.entry.name in Builtin.types_that_construct_their_instance:
                # calling a builtin type that returns a specific object type
                if function.entry.name == 'float':
                    # the following will come true later on in a transform
                    self.type = PyrexTypes.c_double_type
                    self.result_ctype = PyrexTypes.c_double_type
                else:
                    self.type = Builtin.builtin_types[function.entry.name]
                    self.result_ctype = py_object_type
            elif function.is_name and function.type_entry:
                # We are calling an extension type constructor.  As
                # long as we do not support __new__(), the result type
                # is clear
                self.type = function.type_entry.type
                self.result_ctype = py_object_type
            else:
                self.type = py_object_type
            self.is_temp = 1
        else:
            for arg in self.args:
                arg.analyse_types(env)
            if self.self and func_type.args:
                # Coerce 'self' to the type expected by the method.
                expected_type = func_type.args[0].type
                self.coerced_self = CloneNode(self.self).coerce_to(
                    expected_type, env)
                # Insert coerced 'self' argument into argument list.
                self.args.insert(0, self.coerced_self)
            self.analyse_c_function_call(env)
    
    def function_type(self):
        # Return the type of the function being called, coercing a function
        # pointer to a function if necessary.
        func_type = self.function.type
        if func_type.is_ptr:
            func_type = func_type.base_type
        return func_type
    
    def analyse_c_function_call(self, env):
        func_type = self.function_type()
        # Check function type
        if not func_type.is_cfunction:
            if not func_type.is_error:
                error(self.pos, "Calling non-function type '%s'" %
                    func_type)
            self.type = PyrexTypes.error_type
            self.result_code = "<error>"
            return
        # Check no. of args
        max_nargs = len(func_type.args)
        expected_nargs = max_nargs - func_type.optional_arg_count
        actual_nargs = len(self.args)
        if actual_nargs < expected_nargs \
            or (not func_type.has_varargs and actual_nargs > max_nargs):
                expected_str = str(expected_nargs)
                if func_type.has_varargs:
                    expected_str = "at least " + expected_str
                elif func_type.optional_arg_count:
                    if actual_nargs < max_nargs:
                        expected_str = "at least " + expected_str
                    else:
                        expected_str = "at most " + str(max_nargs)
                error(self.pos, 
                    "Call with wrong number of arguments (expected %s, got %s)"
                        % (expected_str, actual_nargs))
                self.args = None
                self.type = PyrexTypes.error_type
                self.result_code = "<error>"
                return
        if func_type.optional_arg_count and expected_nargs != actual_nargs:
            self.has_optional_args = 1
            self.is_temp = 1
        # Coerce arguments
        for i in range(min(max_nargs, actual_nargs)):
            formal_type = func_type.args[i].type
            self.args[i] = self.args[i].coerce_to(formal_type, env)
        for i in range(max_nargs, actual_nargs):
            if self.args[i].type.is_pyobject:
                error(self.args[i].pos, 
                    "Python object cannot be passed as a varargs parameter")
        # Calc result type and code fragment
        self.type = func_type.return_type
        if self.type.is_pyobject:
            self.result_ctype = py_object_type
            self.is_temp = 1
        elif func_type.exception_value is not None \
                 or func_type.exception_check:
            self.is_temp = 1
        # C++ exception handler
        if func_type.exception_check == '+':
            if func_type.exception_value is None:
                env.use_utility_code(cpp_exception_utility_code)

    def calculate_result_code(self):
        return self.c_call_code()
    
    def c_call_code(self):
        func_type = self.function_type()
        if self.args is None or not func_type.is_cfunction:
            return "<error>"
        formal_args = func_type.args
        arg_list_code = []
        args = zip(formal_args, self.args)
        max_nargs = len(func_type.args)
        expected_nargs = max_nargs - func_type.optional_arg_count
        actual_nargs = len(self.args)
        for formal_arg, actual_arg in args[:expected_nargs]:
                arg_code = actual_arg.result_as(formal_arg.type)
                arg_list_code.append(arg_code)
                
        if func_type.is_overridable:
            arg_list_code.append(str(int(self.wrapper_call or self.function.entry.is_unbound_cmethod)))
                
        if func_type.optional_arg_count:
            if expected_nargs == actual_nargs:
                optional_args = 'NULL'
            else:
                optional_args = "&%s" % self.opt_arg_struct
            arg_list_code.append(optional_args)
            
        for actual_arg in self.args[len(formal_args):]:
            arg_list_code.append(actual_arg.result())
        result = "%s(%s)" % (self.function.result(),
            ', '.join(arg_list_code))
        return result
    
    def generate_result_code(self, code):
        func_type = self.function_type()
        if func_type.is_pyobject:
            arg_code = self.arg_tuple.py_result()
            code.putln(
                "%s = PyObject_Call(%s, %s, NULL); %s" % (
                    self.result(),
                    self.function.py_result(),
                    arg_code,
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
        elif func_type.is_cfunction:
            if self.has_optional_args:
                actual_nargs = len(self.args)
                expected_nargs = len(func_type.args) - func_type.optional_arg_count
                self.opt_arg_struct = code.funcstate.allocate_temp(
                    func_type.op_arg_struct.base_type, manage_ref=True)
                code.putln("%s.%s = %s;" % (
                        self.opt_arg_struct,
                        Naming.pyrex_prefix + "n",
                        len(self.args) - expected_nargs))
                args = zip(func_type.args, self.args)
                for formal_arg, actual_arg in args[expected_nargs:actual_nargs]:
                    code.putln("%s.%s = %s;" % (
                            self.opt_arg_struct,
                            func_type.opt_arg_cname(formal_arg.name),
                            actual_arg.result_as(formal_arg.type)))
            exc_checks = []
            if self.type.is_pyobject and self.is_temp:
                exc_checks.append("!%s" % self.result())
            else:
                exc_val = func_type.exception_value
                exc_check = func_type.exception_check
                if exc_val is not None:
                    exc_checks.append("%s == %s" % (self.result(), exc_val))
                if exc_check:
                    exc_checks.append("PyErr_Occurred()")
            if self.is_temp or exc_checks:
                rhs = self.c_call_code()
                if self.result():
                    lhs = "%s = " % self.result()
                    if self.is_temp and self.type.is_pyobject:
                        #return_type = self.type # func_type.return_type
                        #print "SimpleCallNode.generate_result_code: casting", rhs, \
                        #    "from", return_type, "to pyobject" ###
                        rhs = typecast(py_object_type, self.type, rhs)
                else:
                    lhs = ""
                if func_type.exception_check == '+':
                    if func_type.exception_value is None:
                        raise_py_exception = "__Pyx_CppExn2PyErr()"
                    elif func_type.exception_value.type.is_pyobject:
                        raise_py_exception = ' try { throw; } catch(const std::exception& exn) { PyErr_SetString(%s, exn.what()); } catch(...) { PyErr_SetNone(%s); }' % (
                            func_type.exception_value.entry.cname,
                            func_type.exception_value.entry.cname)
                    else:
                        raise_py_exception = '%s(); if (!PyErr_Occurred()) PyErr_SetString(PyExc_RuntimeError , "Error converting c++ exception.")' % func_type.exception_value.entry.cname
                    code.putln(
                    "try {%s%s;} catch(...) {%s; %s}" % (
                        lhs,
                        rhs,
                        raise_py_exception,
                        code.error_goto(self.pos)))
                else:
                    if exc_checks:
                        goto_error = code.error_goto_if(" && ".join(exc_checks), self.pos)
                    else:
                        goto_error = ""
                    code.putln("%s%s; %s" % (lhs, rhs, goto_error))
                if self.type.is_pyobject and self.result():
                    code.put_gotref(self.py_result())
            if self.has_optional_args:
                code.funcstate.release_temp(self.opt_arg_struct)


class PythonCapiFunctionNode(ExprNode):
    subexprs = []
    def __init__(self, pos, py_name, cname, func_type, utility_code = None):
        self.pos = pos
        self.name = py_name
        self.cname = cname
        self.type = func_type
        self.utility_code = utility_code

    def analyse_types(self, env):
        pass

    def generate_result_code(self, code):
        if self.utility_code:
            code.globalstate.use_utility_code(self.utility_code)

    def calculate_result_code(self):
        return self.cname

class PythonCapiCallNode(SimpleCallNode):
    # Python C-API Function call (only created in transforms)

    def __init__(self, pos, function_name, func_type,
                 utility_code = None, py_name=None, **kwargs):
        self.type = func_type.return_type
        self.result_ctype = self.type
        self.function = PythonCapiFunctionNode(
            pos, py_name, function_name, func_type,
            utility_code = utility_code)
        # call this last so that we can override the constructed
        # attributes above with explicit keyword arguments if required
        SimpleCallNode.__init__(self, pos, **kwargs)


class GeneralCallNode(CallNode):
    #  General Python function call, including keyword,
    #  * and ** arguments.
    #
    #  function         ExprNode
    #  positional_args  ExprNode          Tuple of positional arguments
    #  keyword_args     ExprNode or None  Dict of keyword arguments
    #  starstar_arg     ExprNode or None  Dict of extra keyword args
    
    type = py_object_type
    
    subexprs = ['function', 'positional_args', 'keyword_args', 'starstar_arg']

    nogil_check = Node.gil_error

    def compile_time_value(self, denv):
        function = self.function.compile_time_value(denv)
        positional_args = self.positional_args.compile_time_value(denv)
        keyword_args = self.keyword_args.compile_time_value(denv)
        starstar_arg = self.starstar_arg.compile_time_value(denv)
        try:
            keyword_args.update(starstar_arg)
            return function(*positional_args, **keyword_args)
        except Exception, e:
            self.compile_time_value_error(e)
            
    def explicit_args_kwds(self):
        if self.starstar_arg or not isinstance(self.positional_args, TupleNode):
            raise PostParseError(self.pos,
                'Compile-time keyword arguments must be explicit.')
        return self.positional_args.args, self.keyword_args

    def analyse_types(self, env):
        if self.analyse_as_type_constructor(env):
            return
        self.function.analyse_types(env)
        self.positional_args.analyse_types(env)
        if self.keyword_args:
            self.keyword_args.analyse_types(env)
        if self.starstar_arg:
            self.starstar_arg.analyse_types(env)
        if not self.function.type.is_pyobject:
            if self.function.type.is_error:
                self.type = error_type
                return
            if hasattr(self.function, 'entry') and not self.function.entry.as_variable:
                error(self.pos, "Keyword and starred arguments not allowed in cdef functions.")
            else:
                self.function = self.function.coerce_to_pyobject(env)
        self.positional_args = \
            self.positional_args.coerce_to_pyobject(env)
        if self.starstar_arg:
            self.starstar_arg = \
                self.starstar_arg.coerce_to_pyobject(env)
        function = self.function
        if function.is_name and function.type_entry:
            # We are calling an extension type constructor.  As long
            # as we do not support __new__(), the result type is clear
            self.type = function.type_entry.type
            self.result_ctype = py_object_type
        else:
            self.type = py_object_type
        self.is_temp = 1
        
    def generate_result_code(self, code):
        if self.type.is_error: return
        kwargs_call_function = "PyEval_CallObjectWithKeywords"
        if self.keyword_args and self.starstar_arg:
            code.put_error_if_neg(self.pos, 
                "PyDict_Update(%s, %s)" % (
                    self.keyword_args.py_result(), 
                    self.starstar_arg.py_result()))
            keyword_code = self.keyword_args.py_result()
        elif self.keyword_args:
            keyword_code = self.keyword_args.py_result()
        elif self.starstar_arg:
            keyword_code = self.starstar_arg.py_result()
            if self.starstar_arg.type is not Builtin.dict_type:
                # CPython supports calling functions with non-dicts, so do we
                code.globalstate.use_utility_code(kwargs_call_utility_code)
                kwargs_call_function = "__Pyx_PyEval_CallObjectWithKeywords"
        else:
            keyword_code = None
        if not keyword_code:
            call_code = "PyObject_Call(%s, %s, NULL)" % (
                self.function.py_result(),
                self.positional_args.py_result())
        else:
            call_code = "%s(%s, %s, %s)" % (
                kwargs_call_function,
                self.function.py_result(),
                self.positional_args.py_result(),
                keyword_code)
        code.putln(
            "%s = %s; %s" % (
                self.result(),
                call_code,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class AsTupleNode(ExprNode):
    #  Convert argument to tuple. Used for normalising
    #  the * argument of a function call.
    #
    #  arg    ExprNode
    
    subexprs = ['arg']

    def calculate_constant_result(self):
        self.constant_result = tuple(self.base.constant_result)
    
    def compile_time_value(self, denv):
        arg = self.arg.compile_time_value(denv)
        try:
            return tuple(arg)
        except Exception, e:
            self.compile_time_value_error(e)

    def analyse_types(self, env):
        self.arg.analyse_types(env)
        self.arg = self.arg.coerce_to_pyobject(env)
        self.type = tuple_type
        self.is_temp = 1

    nogil_check = Node.gil_error
    gil_message = "Constructing Python tuple"

    def generate_result_code(self, code):
        code.putln(
            "%s = PySequence_Tuple(%s); %s" % (
                self.result(),
                self.arg.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())
    

class AttributeNode(ExprNode):
    #  obj.attribute
    #
    #  obj          ExprNode
    #  attribute    string
    #  needs_none_check boolean        Used if obj is an extension type.
    #                                  If set to True, it is known that the type is not None.
    #
    #  Used internally:
    #
    #  is_py_attr           boolean   Is a Python getattr operation
    #  member               string    C name of struct member
    #  is_called            boolean   Function call is being done on result
    #  entry                Entry     Symbol table entry of attribute
    
    is_attribute = 1
    subexprs = ['obj']
    
    type = PyrexTypes.error_type
    entry = None
    is_called = 0
    needs_none_check = True

    def as_cython_attribute(self):
        if isinstance(self.obj, NameNode) and self.obj.is_cython_module:
            return self.attribute

    def coerce_to(self, dst_type, env):
        #  If coercing to a generic pyobject and this is a cpdef function
        #  we can create the corresponding attribute
        if dst_type is py_object_type:
            entry = self.entry
            if entry and entry.is_cfunction and entry.as_variable:
                # must be a cpdef function
                self.is_temp = 1
                self.entry = entry.as_variable
                self.analyse_as_python_attribute(env) 
                return self
        return ExprNode.coerce_to(self, dst_type, env)

    def calculate_constant_result(self):
        attr = self.attribute
        if attr.startswith("__") and attr.endswith("__"):
            return
        self.constant_result = getattr(self.obj.constant_result, attr)

    def compile_time_value(self, denv):
        attr = self.attribute
        if attr.startswith("__") and attr.endswith("__"):
            error(self.pos,
                  "Invalid attribute name '%s' in compile-time expression" % attr)
            return None
        obj = self.obj.compile_time_value(denv)
        try:
            return getattr(obj, attr)
        except Exception, e:
            self.compile_time_value_error(e)
    
    def type_dependencies(self, env):
        return self.obj.type_dependencies(env)
    
    def infer_type(self, env):
        if self.analyse_as_cimported_attribute(env, 0):
            return self.entry.type
        elif self.analyse_as_unbound_cmethod(env):
            return self.entry.type
        else:
            self.analyse_attribute(env, obj_type = self.obj.infer_type(env))
            return self.type

    def analyse_target_declaration(self, env):
        pass
    
    def analyse_target_types(self, env):
        self.analyse_types(env, target = 1)
    
    def analyse_types(self, env, target = 0):
        if self.analyse_as_cimported_attribute(env, target):
            return
        if not target and self.analyse_as_unbound_cmethod(env):
            return
        self.analyse_as_ordinary_attribute(env, target)
    
    def analyse_as_cimported_attribute(self, env, target):
        # Try to interpret this as a reference to an imported
        # C const, type, var or function. If successful, mutates
        # this node into a NameNode and returns 1, otherwise
        # returns 0.
        module_scope = self.obj.analyse_as_module(env)
        if module_scope:
            entry = module_scope.lookup_here(self.attribute)
            if entry and (
                entry.is_cglobal or entry.is_cfunction
                or entry.is_type or entry.is_const):
                    self.mutate_into_name_node(env, entry, target)
                    return 1
        return 0
    
    def analyse_as_unbound_cmethod(self, env):
        # Try to interpret this as a reference to an unbound
        # C method of an extension type. If successful, mutates
        # this node into a NameNode and returns 1, otherwise
        # returns 0.
        type = self.obj.analyse_as_extension_type(env)
        if type:
            entry = type.scope.lookup_here(self.attribute)
            if entry and entry.is_cmethod:
                # Create a temporary entry describing the C method
                # as an ordinary function.
                ubcm_entry = Symtab.Entry(entry.name,
                    "%s->%s" % (type.vtabptr_cname, entry.cname),
                    entry.type)
                ubcm_entry.is_cfunction = 1
                ubcm_entry.func_cname = entry.func_cname
                ubcm_entry.is_unbound_cmethod = 1
                self.mutate_into_name_node(env, ubcm_entry, None)
                return 1
        return 0
        
    def analyse_as_type(self, env):
        module_scope = self.obj.analyse_as_module(env)
        if module_scope:
            return module_scope.lookup_type(self.attribute)
        return None
    
    def analyse_as_extension_type(self, env):
        # Try to interpret this as a reference to an extension type
        # in a cimported module. Returns the extension type, or None.
        module_scope = self.obj.analyse_as_module(env)
        if module_scope:
            entry = module_scope.lookup_here(self.attribute)
            if entry and entry.is_type and entry.type.is_extension_type:
                return entry.type
        return None
    
    def analyse_as_module(self, env):
        # Try to interpret this as a reference to a cimported module
        # in another cimported module. Returns the module scope, or None.
        module_scope = self.obj.analyse_as_module(env)
        if module_scope:
            entry = module_scope.lookup_here(self.attribute)
            if entry and entry.as_module:
                return entry.as_module
        return None
                
    def mutate_into_name_node(self, env, entry, target):
        # Mutate this node into a NameNode and complete the
        # analyse_types phase.
        self.__class__ = NameNode
        self.name = self.attribute
        self.entry = entry
        del self.obj
        del self.attribute
        if target:
            NameNode.analyse_target_types(self, env)
        else:
            NameNode.analyse_rvalue_entry(self, env)
    
    def analyse_as_ordinary_attribute(self, env, target):
        self.obj.analyse_types(env)
        self.analyse_attribute(env)
        if self.entry and self.entry.is_cmethod and not self.is_called:
#            error(self.pos, "C method can only be called")
            pass
        ## Reference to C array turns into pointer to first element.
        #while self.type.is_array:
        #    self.type = self.type.element_ptr_type()
        if self.is_py_attr:
            if not target:
                self.is_temp = 1
                self.result_ctype = py_object_type
    
    def analyse_attribute(self, env, obj_type = None):
        # Look up attribute and set self.type and self.member.
        self.is_py_attr = 0
        self.member = self.attribute
        if obj_type is None:
            if self.obj.type.is_string:
                self.obj = self.obj.coerce_to_pyobject(env)
            obj_type = self.obj.type
        else:
            if obj_type.is_string:
                obj_type = py_object_type
        if obj_type.is_ptr or obj_type.is_array:
            obj_type = obj_type.base_type
            self.op = "->"
        elif obj_type.is_extension_type:
            self.op = "->"
        else:
            self.op = "."
        if obj_type.has_attributes:
            entry = None
            if obj_type.attributes_known():
                entry = obj_type.scope.lookup_here(self.attribute)
                if entry and entry.is_member:
                    entry = None
            else:
                error(self.pos, 
                    "Cannot select attribute of incomplete type '%s'" 
                    % obj_type)
                self.type = PyrexTypes.error_type
                return
            self.entry = entry
            if entry:
                if obj_type.is_extension_type and entry.name == "__weakref__":
                    error(self.pos, "Illegal use of special attribute __weakref__")
                # methods need the normal attribute lookup
                # because they do not have struct entries
                if entry.is_variable or entry.is_cmethod:
                    self.type = entry.type
                    self.member = entry.cname
                    return
                else:
                    # If it's not a variable or C method, it must be a Python
                    # method of an extension type, so we treat it like a Python
                    # attribute.
                    pass
        # If we get here, the base object is not a struct/union/extension 
        # type, or it is an extension type and the attribute is either not
        # declared or is declared as a Python method. Treat it as a Python
        # attribute reference.
        self.analyse_as_python_attribute(env, obj_type)

    def analyse_as_python_attribute(self, env, obj_type = None):
        if obj_type is None:
            obj_type = self.obj.type
        self.member = self.attribute
        self.type = py_object_type
        self.is_py_attr = 1
        if not obj_type.is_pyobject and not obj_type.is_error:
            if obj_type.can_coerce_to_pyobject(env):
                self.obj = self.obj.coerce_to_pyobject(env)
            else:
                error(self.pos,
                      "Object of type '%s' has no attribute '%s'" %
                      (obj_type, self.attribute))

    def nogil_check(self, env):
        if self.is_py_attr:
            self.gil_error()

    gil_message = "Accessing Python attribute"

    def is_simple(self):
        if self.obj:
            return self.result_in_temp() or self.obj.is_simple()
        else:
            return NameNode.is_simple(self)

    def is_lvalue(self):
        if self.obj:
            return 1
        else:
            return NameNode.is_lvalue(self)
    
    def is_ephemeral(self):
        if self.obj:
            return self.obj.is_ephemeral()
        else:
            return NameNode.is_ephemeral(self)
    
    def calculate_result_code(self):
        #print "AttributeNode.calculate_result_code:", self.member ###
        #print "...obj node =", self.obj, "code", self.obj.result() ###
        #print "...obj type", self.obj.type, "ctype", self.obj.ctype() ###
        obj = self.obj
        obj_code = obj.result_as(obj.type)
        #print "...obj_code =", obj_code ###
        if self.entry and self.entry.is_cmethod:
            if obj.type.is_extension_type:
                return "((struct %s *)%s%s%s)->%s" % (
                    obj.type.vtabstruct_cname, obj_code, self.op, 
                    obj.type.vtabslot_cname, self.member)
            else:
                return self.member
        elif obj.type.is_complex:
            return "__Pyx_C%s(%s)" % (self.member.upper(), obj_code)
        else:
            return "%s%s%s" % (obj_code, self.op, self.member)
    
    def generate_result_code(self, code):
        interned_attr_cname = code.intern_identifier(self.attribute)
        if self.is_py_attr:
            code.putln(
                '%s = PyObject_GetAttr(%s, %s); %s' % (
                    self.result(),
                    self.obj.py_result(),
                    interned_attr_cname,
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
        else:
            # result_code contains what is needed, but we may need to insert
            # a check and raise an exception
            if (self.obj.type.is_extension_type
                  and self.needs_none_check
                  and code.globalstate.directives['nonecheck']):
                self.put_nonecheck(code)
    
    def generate_assignment_code(self, rhs, code):
        interned_attr_cname = code.intern_identifier(self.attribute)
        self.obj.generate_evaluation_code(code)
        if self.is_py_attr:
            code.put_error_if_neg(self.pos, 
                'PyObject_SetAttr(%s, %s, %s)' % (
                    self.obj.py_result(),
                    interned_attr_cname,
                    rhs.py_result()))
            rhs.generate_disposal_code(code)
            rhs.free_temps(code)
        elif self.obj.type.is_complex:
            code.putln("__Pyx_SET_C%s(%s, %s);" % (
                self.member.upper(),
                self.obj.result_as(self.obj.type),
                rhs.result_as(self.ctype())))
        else:
            if (self.obj.type.is_extension_type
                  and self.needs_none_check
                  and code.globalstate.directives['nonecheck']):
                self.put_nonecheck(code)

            select_code = self.result()
            if self.type.is_pyobject and self.use_managed_ref:
                rhs.make_owned_reference(code)
                code.put_giveref(rhs.py_result())
                code.put_gotref(select_code)
                code.put_decref(select_code, self.ctype())
            code.putln(
                "%s = %s;" % (
                    select_code,
                    rhs.result_as(self.ctype())))
                    #rhs.result()))
            rhs.generate_post_assignment_code(code)
            rhs.free_temps(code)
        self.obj.generate_disposal_code(code)
        self.obj.free_temps(code)
    
    def generate_deletion_code(self, code):
        interned_attr_cname = code.intern_identifier(self.attribute)
        self.obj.generate_evaluation_code(code)
        if self.is_py_attr:
            code.put_error_if_neg(self.pos,
                'PyObject_DelAttr(%s, %s)' % (
                    self.obj.py_result(),
                    interned_attr_cname))
        else:
            error(self.pos, "Cannot delete C attribute of extension type")
        self.obj.generate_disposal_code(code)
        self.obj.free_temps(code)
        
    def annotate(self, code):
        if self.is_py_attr:
            code.annotate(self.pos, AnnotationItem('py_attr', 'python attribute', size=len(self.attribute)))
        else:
            code.annotate(self.pos, AnnotationItem('c_attr', 'c attribute', size=len(self.attribute)))

    def put_nonecheck(self, code):
        code.globalstate.use_utility_code(raise_noneattr_error_utility_code)
        code.putln("if (%s) {" % code.unlikely("%s == Py_None") % self.obj.result_as(PyrexTypes.py_object_type))
        code.putln("__Pyx_RaiseNoneAttributeError(\"%s\");" % self.attribute)
        code.putln(code.error_goto(self.pos))
        code.putln("}")


#-------------------------------------------------------------------
#
#  Constructor nodes
#
#-------------------------------------------------------------------

class StarredTargetNode(ExprNode):
    #  A starred expression like "*a"
    #
    #  This is only allowed in sequence assignment targets such as
    #
    #      a, *b = (1,2,3,4)    =>     a = 1 ; b = [2,3,4]
    #
    #  and will be removed during type analysis (or generate an error
    #  if it's found at unexpected places).
    #
    #  target          ExprNode

    subexprs = ['target']
    is_starred = 1
    type = py_object_type
    is_temp = 1

    def __init__(self, pos, target):
        self.pos = pos
        self.target = target

    def analyse_declarations(self, env):
        error(self.pos, "can use starred expression only as assignment target")
        self.target.analyse_declarations(env)

    def analyse_types(self, env):
        error(self.pos, "can use starred expression only as assignment target")
        self.target.analyse_types(env)
        self.type = self.target.type

    def analyse_target_declaration(self, env):
        self.target.analyse_target_declaration(env)

    def analyse_target_types(self, env):
        self.target.analyse_target_types(env)
        self.type = self.target.type

    def calculate_result_code(self):
        return ""

    def generate_result_code(self, code):
        pass


class SequenceNode(ExprNode):
    #  Base class for list and tuple constructor nodes.
    #  Contains common code for performing sequence unpacking.
    #
    #  args                    [ExprNode]
    #  iterator                ExprNode
    #  unpacked_items          [ExprNode] or None
    #  coerced_unpacked_items  [ExprNode] or None
    
    subexprs = ['args']
    
    is_sequence_constructor = 1
    unpacked_items = None

    def compile_time_value_list(self, denv):
        return [arg.compile_time_value(denv) for arg in self.args]

    def replace_starred_target_node(self):
        # replace a starred node in the targets by the contained expression
        self.starred_assignment = False
        args = []
        for arg in self.args:
            if arg.is_starred:
                if self.starred_assignment:
                    error(arg.pos, "more than 1 starred expression in assignment")
                self.starred_assignment = True
                arg = arg.target
                arg.is_starred = True
            args.append(arg)
        self.args = args

    def analyse_target_declaration(self, env):
        self.replace_starred_target_node()
        for arg in self.args:
            arg.analyse_target_declaration(env)

    def analyse_types(self, env, skip_children=False):
        for i in range(len(self.args)):
            arg = self.args[i]
            if not skip_children: arg.analyse_types(env)
            self.args[i] = arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.is_temp = 1

    def analyse_target_types(self, env):
        self.iterator = PyTempNode(self.pos, env)
        self.unpacked_items = []
        self.coerced_unpacked_items = []
        for arg in self.args:
            arg.analyse_target_types(env)
            if arg.is_starred:
                if not arg.type.assignable_from(Builtin.list_type):
                    error(arg.pos,
                          "starred target must have Python object (list) type")
                if arg.type is py_object_type:
                    arg.type = Builtin.list_type
            unpacked_item = PyTempNode(self.pos, env)
            coerced_unpacked_item = unpacked_item.coerce_to(arg.type, env)
            self.unpacked_items.append(unpacked_item)
            self.coerced_unpacked_items.append(coerced_unpacked_item)
        self.type = py_object_type

    def generate_result_code(self, code):
        self.generate_operation_code(code)
    
    def generate_assignment_code(self, rhs, code):
        if self.starred_assignment:
            self.generate_starred_assignment_code(rhs, code)
        else:
            self.generate_parallel_assignment_code(rhs, code)

        for item in self.unpacked_items:
            item.release(code)
        rhs.free_temps(code)

    def generate_parallel_assignment_code(self, rhs, code):
        # Need to work around the fact that generate_evaluation_code
        # allocates the temps in a rather hacky way -- the assignment
        # is evaluated twice, within each if-block.

        code.globalstate.use_utility_code(unpacking_utility_code)

        if rhs.type is tuple_type:
            tuple_check = "likely(%s != Py_None)"
        else:
            tuple_check = "PyTuple_CheckExact(%s)"
        code.putln(
            "if (%s && likely(PyTuple_GET_SIZE(%s) == %s)) {" % (
                tuple_check % rhs.py_result(), 
                rhs.py_result(), 
                len(self.args)))
        code.putln("PyObject* tuple = %s;" % rhs.py_result())
        for item in self.unpacked_items:
            item.allocate(code)
        for i in range(len(self.args)):
            item = self.unpacked_items[i]
            code.put(
                "%s = PyTuple_GET_ITEM(tuple, %s); " % (
                    item.result(),
                    i))
            code.put_incref(item.result(), item.ctype())
            value_node = self.coerced_unpacked_items[i]
            value_node.generate_evaluation_code(code)
        rhs.generate_disposal_code(code)

        for i in range(len(self.args)):
            self.args[i].generate_assignment_code(
                self.coerced_unpacked_items[i], code)
                 
        code.putln("} else {")

        if rhs.type is tuple_type:
            code.globalstate.use_utility_code(tuple_unpacking_error_code)
            code.putln("__Pyx_UnpackTupleError(%s, %s);" % (
                        rhs.py_result(), len(self.args)))
            code.putln(code.error_goto(self.pos))
        else:
            self.iterator.allocate(code)
            code.putln(
                "%s = PyObject_GetIter(%s); %s" % (
                    self.iterator.result(),
                    rhs.py_result(),
                    code.error_goto_if_null(self.iterator.result(), self.pos)))
            code.put_gotref(self.iterator.py_result())
            rhs.generate_disposal_code(code)
            for i in range(len(self.args)):
                item = self.unpacked_items[i]
                unpack_code = "__Pyx_UnpackItem(%s, %d)" % (
                    self.iterator.py_result(), i)
                code.putln(
                    "%s = %s; %s" % (
                        item.result(),
                        typecast(item.ctype(), py_object_type, unpack_code),
                        code.error_goto_if_null(item.result(), self.pos)))
                code.put_gotref(item.py_result())
                value_node = self.coerced_unpacked_items[i]
                value_node.generate_evaluation_code(code)
            code.put_error_if_neg(self.pos, 
                "__Pyx_EndUnpack(%s)" % (
                    self.iterator.py_result()))
            if debug_disposal_code:
                print("UnpackNode.generate_assignment_code:")
                print("...generating disposal code for %s" % self.iterator)
            self.iterator.generate_disposal_code(code)
            self.iterator.free_temps(code)
            self.iterator.release(code)

            for i in range(len(self.args)):
                self.args[i].generate_assignment_code(
                    self.coerced_unpacked_items[i], code)

        code.putln("}")

    def generate_starred_assignment_code(self, rhs, code):
        code.globalstate.use_utility_code(unpacking_utility_code)

        for i, arg in enumerate(self.args):
            if arg.is_starred:
                starred_target = self.unpacked_items[i]
                fixed_args_left  = self.args[:i]
                fixed_args_right = self.args[i+1:]
                break

        self.iterator.allocate(code)
        code.putln(
            "%s = PyObject_GetIter(%s); %s" % (
                self.iterator.result(),
                rhs.py_result(),
                code.error_goto_if_null(self.iterator.result(), self.pos)))
        code.put_gotref(self.iterator.py_result())
        rhs.generate_disposal_code(code)

        for item in self.unpacked_items:
            item.allocate(code)
        for i in range(len(fixed_args_left)):
            item = self.unpacked_items[i]
            unpack_code = "__Pyx_UnpackItem(%s, %d)" % (
                self.iterator.py_result(), i)
            code.putln(
                "%s = %s; %s" % (
                    item.result(),
                    typecast(item.ctype(), py_object_type, unpack_code),
                    code.error_goto_if_null(item.result(), self.pos)))
            code.put_gotref(item.py_result())
            value_node = self.coerced_unpacked_items[i]
            value_node.generate_evaluation_code(code)

        target_list = starred_target.result()
        code.putln("%s = PySequence_List(%s); %s" % (
            target_list, self.iterator.py_result(),
            code.error_goto_if_null(target_list, self.pos)))
        code.put_gotref(target_list)
        if fixed_args_right:
            code.globalstate.use_utility_code(raise_need_more_values_to_unpack)
            unpacked_right_args = self.unpacked_items[-len(fixed_args_right):]
            code.putln("if (unlikely(PyList_GET_SIZE(%s) < %d)) {" % (
                (target_list, len(unpacked_right_args))))
            code.put("__Pyx_RaiseNeedMoreValuesError(%d+PyList_GET_SIZE(%s)); %s" % (
                     len(fixed_args_left), target_list,
                     code.error_goto(self.pos)))
            code.putln('}')
            for i, (arg, coerced_arg) in enumerate(zip(unpacked_right_args[::-1],
                                                       self.coerced_unpacked_items[::-1])):
                code.putln(
                    "%s = PyList_GET_ITEM(%s, PyList_GET_SIZE(%s)-1); " % (
                        arg.py_result(),
                        target_list, target_list))
                # resize the list the hard way
                code.putln("((PyVarObject*)%s)->ob_size--;" % target_list)
                code.put_gotref(arg.py_result())
                coerced_arg.generate_evaluation_code(code)

        self.iterator.generate_disposal_code(code)
        self.iterator.free_temps(code)
        self.iterator.release(code)

        for i in range(len(self.args)):
            self.args[i].generate_assignment_code(
                self.coerced_unpacked_items[i], code)

    def annotate(self, code):
        for arg in self.args:
            arg.annotate(code)
        if self.unpacked_items:
            for arg in self.unpacked_items:
                arg.annotate(code)
            for arg in self.coerced_unpacked_items:
                arg.annotate(code)


class TupleNode(SequenceNode):
    #  Tuple constructor.
    
    type = tuple_type

    gil_message = "Constructing Python tuple"

    def analyse_types(self, env, skip_children=False):
        if len(self.args) == 0:
            self.is_temp = 0
            self.is_literal = 1
        else:
            SequenceNode.analyse_types(self, env, skip_children)
            
    def calculate_result_code(self):
        if len(self.args) > 0:
            error(self.pos, "Positive length tuples must be constructed.")
        else:
            return Naming.empty_tuple

    def calculate_constant_result(self):
        self.constant_result = tuple([
                arg.constant_result for arg in self.args])

    def compile_time_value(self, denv):
        values = self.compile_time_value_list(denv)
        try:
            return tuple(values)
        except Exception, e:
            self.compile_time_value_error(e)
    
    def generate_operation_code(self, code):
        if len(self.args) == 0:
            # result_code is Naming.empty_tuple
            return
        code.putln(
            "%s = PyTuple_New(%s); %s" % (
                self.result(),
                len(self.args),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())
        for i in range(len(self.args)):
            arg = self.args[i]
            if not arg.result_in_temp():
                code.put_incref(arg.result(), arg.ctype())
            code.putln(
                "PyTuple_SET_ITEM(%s, %s, %s);" % (
                    self.result(),
                    i,
                    arg.py_result()))
            code.put_giveref(arg.py_result())
    
    def generate_subexpr_disposal_code(self, code):
        # We call generate_post_assignment_code here instead
        # of generate_disposal_code, because values were stored
        # in the tuple using a reference-stealing operation.
        for arg in self.args:
            arg.generate_post_assignment_code(code)
            # Should NOT call free_temps -- this is invoked by the default
            # generate_evaluation_code which will do that.


class ListNode(SequenceNode):
    #  List constructor.
    
    # obj_conversion_errors    [PyrexError]   used internally
    # orignial_args            [ExprNode]     used internally

    obj_conversion_errors = []

    gil_message = "Constructing Python list"
    
    def type_dependencies(self, env):
        return ()
    
    def infer_type(self, env):
        # TOOD: Infer non-object list arrays.
        return list_type

    def analyse_expressions(self, env):
        SequenceNode.analyse_expressions(self, env)
        self.coerce_to_pyobject(env)

    def analyse_types(self, env):
        hold_errors()
        self.original_args = list(self.args)
        SequenceNode.analyse_types(self, env)
        self.type = list_type
        self.obj_conversion_errors = held_errors()
        release_errors(ignore=True)
        
    def coerce_to(self, dst_type, env):
        if dst_type.is_pyobject:
            for err in self.obj_conversion_errors:
                report_error(err)
            self.obj_conversion_errors = []
            if not self.type.subtype_of(dst_type):
                error(self.pos, "Cannot coerce list to type '%s'" % dst_type)
        elif dst_type.is_ptr:
            base_type = dst_type.base_type
            self.type = PyrexTypes.CArrayType(base_type, len(self.args))
            for i in range(len(self.original_args)):
                arg = self.args[i]
                if isinstance(arg, CoerceToPyTypeNode):
                    arg = arg.arg
                self.args[i] = arg.coerce_to(base_type, env)
        elif dst_type.is_struct:
            if len(self.args) > len(dst_type.scope.var_entries):
                error(self.pos, "Too may members for '%s'" % dst_type)
            else:
                if len(self.args) < len(dst_type.scope.var_entries):
                    warning(self.pos, "Too few members for '%s'" % dst_type, 1)
                for i, (arg, member) in enumerate(zip(self.original_args, dst_type.scope.var_entries)):
                    if isinstance(arg, CoerceToPyTypeNode):
                        arg = arg.arg
                    self.args[i] = arg.coerce_to(member.type, env)
            self.type = dst_type
        else:
            self.type = error_type
            error(self.pos, "Cannot coerce list to type '%s'" % dst_type)
        return self
        
    def release_temp(self, env):
        if self.type.is_array:
            # To be valid C++, we must allocate the memory on the stack 
            # manually and be sure not to reuse it for something else. 
            pass
        else:
            SequenceNode.release_temp(self, env)

    def calculate_constant_result(self):
        self.constant_result = [
            arg.constant_result for arg in self.args]

    def compile_time_value(self, denv):
        return self.compile_time_value_list(denv)

    def generate_operation_code(self, code):
        if self.type.is_pyobject:
            for err in self.obj_conversion_errors:
                report_error(err)
            code.putln("%s = PyList_New(%s); %s" %
                (self.result(),
                len(self.args),
                code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
            for i in range(len(self.args)):
                arg = self.args[i]
                #if not arg.is_temp:
                if not arg.result_in_temp():
                    code.put_incref(arg.result(), arg.ctype())
                code.putln("PyList_SET_ITEM(%s, %s, %s);" %
                    (self.result(),
                    i,
                    arg.py_result()))
                code.put_giveref(arg.py_result())
        elif self.type.is_array:
            for i, arg in enumerate(self.args):
                code.putln("%s[%s] = %s;" % (
                                self.result(),
                                i,
                                arg.result()))
        elif self.type.is_struct:
            for arg, member in zip(self.args, self.type.scope.var_entries):
                code.putln("%s.%s = %s;" % (
                        self.result(),
                        member.cname,
                        arg.result()))
        else:
            raise InternalError("List type never specified")

    def generate_subexpr_disposal_code(self, code):
        # We call generate_post_assignment_code here instead
        # of generate_disposal_code, because values were stored
        # in the list using a reference-stealing operation.
        for arg in self.args:
            arg.generate_post_assignment_code(code)
            # Should NOT call free_temps -- this is invoked by the default
            # generate_evaluation_code which will do that.


class ComprehensionNode(ExprNode):
    subexprs = ["target"]
    child_attrs = ["loop", "append"]

    def infer_type(self, env):
        return self.target.infer_type(env)

    def analyse_declarations(self, env):
        self.append.target = self # this is used in the PyList_Append of the inner loop
        self.loop.analyse_declarations(env)

    def analyse_types(self, env):
        self.target.analyse_expressions(env)
        self.type = self.target.type
        self.loop.analyse_expressions(env)

    def calculate_result_code(self):
        return self.target.result()
    
    def generate_result_code(self, code):
        self.generate_operation_code(code)

    def generate_operation_code(self, code):
        self.loop.generate_execution_code(code)

    def annotate(self, code):
        self.loop.annotate(code)


class ComprehensionAppendNode(ExprNode):
    # Need to be careful to avoid infinite recursion:
    # target must not be in child_attrs/subexprs
    subexprs = ['expr']

    type = PyrexTypes.c_int_type
    
    def analyse_types(self, env):
        self.expr.analyse_types(env)
        if not self.expr.type.is_pyobject:
            self.expr = self.expr.coerce_to_pyobject(env)
        self.is_temp = 1

    def generate_result_code(self, code):
        if self.target.type is list_type:
            function = "PyList_Append"
        elif self.target.type is set_type:
            function = "PySet_Add"
        else:
            raise InternalError(
                "Invalid type for comprehension node: %s" % self.target.type)
            
        code.putln("%s = %s(%s, (PyObject*)%s); %s" %
            (self.result(),
             function,
             self.target.result(),
             self.expr.result(),
             code.error_goto_if(self.result(), self.pos)))

class DictComprehensionAppendNode(ComprehensionAppendNode):
    subexprs = ['key_expr', 'value_expr']

    def analyse_types(self, env):
        self.key_expr.analyse_types(env)
        if not self.key_expr.type.is_pyobject:
            self.key_expr = self.key_expr.coerce_to_pyobject(env)
        self.value_expr.analyse_types(env)
        if not self.value_expr.type.is_pyobject:
            self.value_expr = self.value_expr.coerce_to_pyobject(env)
        self.is_temp = 1

    def generate_result_code(self, code):
        code.putln("%s = PyDict_SetItem(%s, (PyObject*)%s, (PyObject*)%s); %s" %
            (self.result(),
             self.target.result(),
             self.key_expr.result(),
             self.value_expr.result(),
             code.error_goto_if(self.result(), self.pos)))


class SetNode(ExprNode):
    #  Set constructor.

    type = set_type

    subexprs = ['args']

    gil_message = "Constructing Python set"
    
    def analyse_types(self, env):
        for i in range(len(self.args)):
            arg = self.args[i]
            arg.analyse_types(env)
            self.args[i] = arg.coerce_to_pyobject(env)
        self.type = set_type
        self.is_temp = 1

    def calculate_constant_result(self):
        self.constant_result = set([
                arg.constant_result for arg in self.args])

    def compile_time_value(self, denv):
        values = [arg.compile_time_value(denv) for arg in self.args]
        try:
            return set(values)
        except Exception, e:
            self.compile_time_value_error(e)

    def generate_evaluation_code(self, code):
        code.globalstate.use_utility_code(Builtin.py23_set_utility_code)
        self.allocate_temp_result(code)
        code.putln(
            "%s = PySet_New(0); %s" % (
                self.result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())
        for arg in self.args:
            arg.generate_evaluation_code(code)
            code.putln(
                code.error_goto_if_neg(
                    "PySet_Add(%s, %s)" % (self.result(), arg.py_result()),
                    self.pos))
            arg.generate_disposal_code(code)
            arg.free_temps(code)


class DictNode(ExprNode):
    #  Dictionary constructor.
    #
    #  key_value_pairs  [DictItemNode]
    #
    # obj_conversion_errors    [PyrexError]   used internally
    
    subexprs = ['key_value_pairs']
    is_temp = 1
    type = dict_type

    obj_conversion_errors = []

    def calculate_constant_result(self):
        self.constant_result = dict([
                item.constant_result for item in self.key_value_pairs])
    
    def compile_time_value(self, denv):
        pairs = [(item.key.compile_time_value(denv), item.value.compile_time_value(denv))
            for item in self.key_value_pairs]
        try:
            return dict(pairs)
        except Exception, e:
            self.compile_time_value_error(e)
    
    def type_dependencies(self, env):
        return ()
    
    def infer_type(self, env):
        # TOOD: Infer struct constructors.
        return dict_type

    def analyse_types(self, env):
        hold_errors()
        for item in self.key_value_pairs:
            item.analyse_types(env)
        self.obj_conversion_errors = held_errors()
        release_errors(ignore=True)
        
    def coerce_to(self, dst_type, env):
        if dst_type.is_pyobject:
            self.release_errors()
            if not self.type.subtype_of(dst_type):
                error(self.pos, "Cannot interpret dict as type '%s'" % dst_type)
        elif dst_type.is_struct_or_union:
            self.type = dst_type
            if not dst_type.is_struct and len(self.key_value_pairs) != 1:
                error(self.pos, "Exactly one field must be specified to convert to union '%s'" % dst_type)
            elif dst_type.is_struct and len(self.key_value_pairs) < len(dst_type.scope.var_entries):
                warning(self.pos, "Not all members given for struct '%s'" % dst_type, 1)
            for item in self.key_value_pairs:
                if isinstance(item.key, CoerceToPyTypeNode):
                    item.key = item.key.arg
                if not isinstance(item.key, (UnicodeNode, StringNode, BytesNode)):
                    error(item.key.pos, "Invalid struct field identifier")
                    item.key = StringNode(item.key.pos, value="<error>")
                else:
                    key = str(item.key.value) # converts string literals to unicode in Py3
                    member = dst_type.scope.lookup_here(key)
                    if not member:
                        error(item.key.pos, "struct '%s' has no field '%s'" % (dst_type, key))
                    else:
                        value = item.value
                        if isinstance(value, CoerceToPyTypeNode):
                            value = value.arg
                        item.value = value.coerce_to(member.type, env)
        else:
            self.type = error_type
            error(self.pos, "Cannot interpret dict as type '%s'" % dst_type)
        return self
    
    def release_errors(self):
        for err in self.obj_conversion_errors:
            report_error(err)
        self.obj_conversion_errors = []

    gil_message = "Constructing Python dict"

    def generate_evaluation_code(self, code):
        #  Custom method used here because key-value
        #  pairs are evaluated and used one at a time.
        code.mark_pos(self.pos)
        self.allocate_temp_result(code)
        if self.type.is_pyobject:
            self.release_errors()
            code.putln(
                "%s = PyDict_New(); %s" % (
                    self.result(),
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
        for item in self.key_value_pairs:
            item.generate_evaluation_code(code)
            if self.type.is_pyobject:
                code.put_error_if_neg(self.pos, 
                    "PyDict_SetItem(%s, %s, %s)" % (
                        self.result(),
                        item.key.py_result(),
                        item.value.py_result()))
            else:
                code.putln("%s.%s = %s;" % (
                        self.result(),
                        item.key.value,
                        item.value.result()))
            item.generate_disposal_code(code)
            item.free_temps(code)
            
    def annotate(self, code):
        for item in self.key_value_pairs:
            item.annotate(code)
            
class DictItemNode(ExprNode):
    # Represents a single item in a DictNode
    #
    # key          ExprNode
    # value        ExprNode
    subexprs = ['key', 'value']

    nogil_check = None # Parent DictNode takes care of it

    def calculate_constant_result(self):
        self.constant_result = (
            self.key.constant_result, self.value.constant_result)
            
    def analyse_types(self, env):
        self.key.analyse_types(env)
        self.value.analyse_types(env)
        self.key = self.key.coerce_to_pyobject(env)
        self.value = self.value.coerce_to_pyobject(env)
        
    def generate_evaluation_code(self, code):
        self.key.generate_evaluation_code(code)
        self.value.generate_evaluation_code(code)

    def generate_disposal_code(self, code):
        self.key.generate_disposal_code(code)
        self.value.generate_disposal_code(code)

    def free_temps(self, code):
        self.key.free_temps(code)
        self.value.free_temps(code)
        
    def __iter__(self):
        return iter([self.key, self.value])


class ClassNode(ExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a class object given
    #  a name, tuple of bases and class dictionary.
    #
    #  name         EncodedString      Name of the class
    #  bases        ExprNode           Base class tuple
    #  dict         ExprNode           Class dict (not owned by this node)
    #  doc          ExprNode or None   Doc string
    #  module_name  string             Name of defining module
    
    subexprs = ['bases', 'doc']

    def analyse_types(self, env):
        self.bases.analyse_types(env)
        if self.doc:
            self.doc.analyse_types(env)
            self.doc = self.doc.coerce_to_pyobject(env)
        self.module_name = env.global_scope().qualified_name
        self.type = py_object_type
        self.is_temp = 1
        env.use_utility_code(create_class_utility_code);

    gil_message = "Constructing Python class"

    def generate_result_code(self, code):
        cname = code.intern_identifier(self.name)
        if self.doc:
            code.put_error_if_neg(self.pos, 
                'PyDict_SetItemString(%s, "__doc__", %s)' % (
                    self.dict.py_result(),
                    self.doc.py_result()))
        code.putln(
            '%s = __Pyx_CreateClass(%s, %s, %s, "%s"); %s' % (
                self.result(),
                self.bases.py_result(),
                self.dict.py_result(),
                cname,
                self.module_name,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class UnboundMethodNode(ExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs an unbound method
    #  object from a class and a function.
    #
    #  function      ExprNode   Function object
    
    type = py_object_type
    is_temp = 1
    
    subexprs = ['function']
    
    def analyse_types(self, env):
        self.function.analyse_types(env)

    gil_message = "Constructing an unbound method"

    def generate_result_code(self, code):
        class_cname = code.pyclass_stack[-1].classobj.result()
        code.putln(
            "%s = PyMethod_New(%s, 0, %s); %s" % (
                self.result(),
                self.function.py_result(),
                class_cname,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())

class PyCFunctionNode(AtomicExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a PyCFunction object
    #  from a PyMethodDef struct.
    #
    #  pymethdef_cname   string   PyMethodDef structure
    
    type = py_object_type
    is_temp = 1
    
    def analyse_types(self, env):
        pass
    
    gil_message = "Constructing Python function"

    def generate_result_code(self, code):
        code.putln(
            "%s = PyCFunction_New(&%s, 0); %s" % (
                self.result(),
                self.pymethdef_cname,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())

#-------------------------------------------------------------------
#
#  Unary operator nodes
#
#-------------------------------------------------------------------

compile_time_unary_operators = {
    'not': operator.not_,
    '~': operator.inv,
    '-': operator.neg,
    '+': operator.pos,
}

class UnopNode(ExprNode):
    #  operator     string
    #  operand      ExprNode
    #
    #  Processing during analyse_expressions phase:
    #
    #    analyse_c_operation
    #      Called when the operand is not a pyobject.
    #      - Check operand type and coerce if needed.
    #      - Determine result type and result code fragment.
    #      - Allocate temporary for result if needed.
    
    subexprs = ['operand']
    infix = True

    def calculate_constant_result(self):
        func = compile_time_unary_operators[self.operator]
        self.constant_result = func(self.operand.constant_result)
    
    def compile_time_value(self, denv):
        func = compile_time_unary_operators.get(self.operator)
        if not func:
            error(self.pos,
                "Unary '%s' not supported in compile-time expression"
                    % self.operator)
        operand = self.operand.compile_time_value(denv)
        try:
            return func(operand)
        except Exception, e:
            self.compile_time_value_error(e)
    
    def infer_type(self, env):
        return self.operand.infer_type(env)

    def analyse_types(self, env):
        self.operand.analyse_types(env)
        if self.is_py_operation():
            self.coerce_operand_to_pyobject(env)
            self.type = py_object_type
            self.is_temp = 1
        else:
            self.analyse_c_operation(env)
    
    def check_const(self):
        return self.operand.check_const()
    
    def is_py_operation(self):
        return self.operand.type.is_pyobject

    def nogil_check(self, env):
        if self.is_py_operation():
            self.gil_error()

    def coerce_operand_to_pyobject(self, env):
        self.operand = self.operand.coerce_to_pyobject(env)
    
    def generate_result_code(self, code):
        if self.operand.type.is_pyobject:
            self.generate_py_operation_code(code)
    
    def generate_py_operation_code(self, code):
        function = self.py_operation_function()
        code.putln(
            "%s = %s(%s); %s" % (
                self.result(), 
                function, 
                self.operand.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())
        
    def type_error(self):
        if not self.operand.type.is_error:
            error(self.pos, "Invalid operand type for '%s' (%s)" %
                (self.operator, self.operand.type))
        self.type = PyrexTypes.error_type


class NotNode(ExprNode):
    #  'not' operator
    #
    #  operand   ExprNode
    
    type = PyrexTypes.c_bint_type

    subexprs = ['operand']
    
    def calculate_constant_result(self):
        self.constant_result = not self.operand.constant_result

    def compile_time_value(self, denv):
        operand = self.operand.compile_time_value(denv)
        try:
            return not operand
        except Exception, e:
            self.compile_time_value_error(e)

    def infer_type(self, env):
        return PyrexTypes.c_bint_type
    
    def analyse_types(self, env):
        self.operand.analyse_types(env)
        self.operand = self.operand.coerce_to_boolean(env)
    
    def calculate_result_code(self):
        return "(!%s)" % self.operand.result()
    
    def generate_result_code(self, code):
        pass


class UnaryPlusNode(UnopNode):
    #  unary '+' operator
    
    operator = '+'
    
    def analyse_c_operation(self, env):
        self.type = self.operand.type
    
    def py_operation_function(self):
        return "PyNumber_Positive"
    
    def calculate_result_code(self):
        return self.operand.result()


class UnaryMinusNode(UnopNode):
    #  unary '-' operator
    
    operator = '-'
    
    def analyse_c_operation(self, env):
        if self.operand.type.is_numeric:
            self.type = self.operand.type
        else:
            self.type_error()
        if self.type.is_complex:
            self.infix = False
    
    def py_operation_function(self):
        return "PyNumber_Negative"
    
    def calculate_result_code(self):
        if self.infix:
            return "(-%s)" % self.operand.result()
        else:
            return "%s(%s)" % (self.operand.type.unary_op('-'), self.operand.result())

    def get_constant_c_result_code(self):
        value = self.operand.get_constant_c_result_code()
        if value:
            return "(-%s)" % (value)

class TildeNode(UnopNode):
    #  unary '~' operator

    def analyse_c_operation(self, env):
        if self.operand.type.is_int:
            self.type = self.operand.type
        else:
            self.type_error()

    def py_operation_function(self):
        return "PyNumber_Invert"
    
    def calculate_result_code(self):
        return "(~%s)" % self.operand.result()


class AmpersandNode(ExprNode):
    #  The C address-of operator.
    #
    #  operand  ExprNode
    
    subexprs = ['operand']
    
    def infer_type(self, env):
        return PyrexTypes.c_ptr_type(self.operand.infer_type(env))

    def analyse_types(self, env):
        self.operand.analyse_types(env)
        argtype = self.operand.type
        if not (argtype.is_cfunction or self.operand.is_lvalue()):
            self.error("Taking address of non-lvalue")
            return
        if argtype.is_pyobject:
            self.error("Cannot take address of Python variable")
            return
        self.type = PyrexTypes.c_ptr_type(argtype)
    
    def check_const(self):
        return self.operand.check_const_addr()
    
    def error(self, mess):
        error(self.pos, mess)
        self.type = PyrexTypes.error_type
        self.result_code = "<error>"
    
    def calculate_result_code(self):
        return "(&%s)" % self.operand.result()

    def generate_result_code(self, code):
        pass
    

unop_node_classes = {
    "+":  UnaryPlusNode,
    "-":  UnaryMinusNode,
    "~":  TildeNode,
}

def unop_node(pos, operator, operand):
    # Construct unnop node of appropriate class for 
    # given operator.
    if isinstance(operand, IntNode) and operator == '-':
        return IntNode(pos = operand.pos, value = str(-int(operand.value, 0)))
    elif isinstance(operand, UnopNode) and operand.operator == operator:
        warning(pos, "Python has no increment/decrement operator: %s%sx = %s(%sx) = x" % ((operator,)*4), 5)
    return unop_node_classes[operator](pos, 
        operator = operator, 
        operand = operand)


class TypecastNode(ExprNode):
    #  C type cast
    #
    #  operand      ExprNode
    #  base_type    CBaseTypeNode
    #  declarator   CDeclaratorNode
    #
    #  If used from a transform, one can if wanted specify the attribute
    #  "type" directly and leave base_type and declarator to None
    
    subexprs = ['operand']
    base_type = declarator = type = None
    
    def type_dependencies(self, env):
        return ()
    
    def infer_type(self, env):
        if self.type is None:
            base_type = self.base_type.analyse(env)
            _, self.type = self.declarator.analyse(base_type, env)
        return self.type
    
    def analyse_types(self, env):
        if self.type is None:
            base_type = self.base_type.analyse(env)
            _, self.type = self.declarator.analyse(base_type, env)
        if self.type.is_cfunction:
            error(self.pos,
                "Cannot cast to a function type")
            self.type = PyrexTypes.error_type
        self.operand.analyse_types(env)
        to_py = self.type.is_pyobject
        from_py = self.operand.type.is_pyobject
        if from_py and not to_py and self.operand.is_ephemeral() and not self.type.is_numeric:
            error(self.pos, "Casting temporary Python object to non-numeric non-Python type")
        if to_py and not from_py:
            if self.operand.type.can_coerce_to_pyobject(env):
                self.result_ctype = py_object_type
                self.operand = self.operand.coerce_to_pyobject(env)
            else:
                if self.operand.type.is_ptr:
                    if not (self.operand.type.base_type.is_void or self.operand.type.base_type.is_struct):
                        error(self.pos, "Python objects cannot be cast from pointers of primitive types")
                else:
                    # Should this be an error? 
                    warning(self.pos, "No conversion from %s to %s, python object pointer used." % (self.operand.type, self.type))
                self.operand = self.operand.coerce_to_simple(env)
        elif from_py and not to_py:
            if self.type.create_from_py_utility_code(env):
                self.operand = self.operand.coerce_to(self.type, env)
            elif self.type.is_ptr:
                if not (self.type.base_type.is_void or self.type.base_type.is_struct):
                    error(self.pos, "Python objects cannot be cast to pointers of primitive types")
            else:
                warning(self.pos, "No conversion from %s to %s, python object pointer used." % (self.type, self.operand.type))
        elif from_py and to_py:
            if self.typecheck and self.type.is_extension_type:
                self.operand = PyTypeTestNode(self.operand, self.type, env, notnone=True)
        elif self.type.is_complex and self.operand.type.is_complex:
            self.operand = self.operand.coerce_to_simple(env)

    def nogil_check(self, env):
        if self.type and self.type.is_pyobject and self.is_temp:
            self.gil_error()

    def check_const(self):
        return self.operand.check_const()

    def calculate_constant_result(self):
        # we usually do not know the result of a type cast at code
        # generation time
        pass
    
    def calculate_result_code(self):
        if self.type.is_complex:
            operand_result = self.operand.result()
            if self.operand.type.is_complex:
                real_part = self.type.real_type.cast_code("__Pyx_CREAL(%s)" % operand_result)
                imag_part = self.type.real_type.cast_code("__Pyx_CIMAG(%s)" % operand_result)
            else:
                real_part = self.type.real_type.cast_code(operand_result)
                imag_part = "0"
            return "%s(%s, %s)" % (
                    self.type.from_parts,
                    real_part,
                    imag_part)    
        else:
            return self.type.cast_code(self.operand.result())
    
    def get_constant_c_result_code(self):
        operand_result = self.operand.get_constant_c_result_code()
        if operand_result:
            return self.type.cast_code(operand_result)
    
    def result_as(self, type):
        if self.type.is_pyobject and not self.is_temp:
            #  Optimise away some unnecessary casting
            return self.operand.result_as(type)
        else:
            return ExprNode.result_as(self, type)

    def generate_result_code(self, code):
        if self.is_temp:
            code.putln(
                "%s = (PyObject *)%s;" % (
                    self.result(),
                    self.operand.result()))
            code.put_incref(self.result(), self.ctype())


class SizeofNode(ExprNode):
    #  Abstract base class for sizeof(x) expression nodes.
    
    type = PyrexTypes.c_size_t_type

    def check_const(self):
        return True

    def generate_result_code(self, code):
        pass


class SizeofTypeNode(SizeofNode):
    #  C sizeof function applied to a type
    #
    #  base_type   CBaseTypeNode
    #  declarator  CDeclaratorNode
    
    subexprs = []
    arg_type = None
    
    def analyse_types(self, env):
        # we may have incorrectly interpreted a dotted name as a type rather than an attribute
        # this could be better handled by more uniformly treating types as runtime-available objects
        if 0 and self.base_type.module_path:
            path = self.base_type.module_path
            obj = env.lookup(path[0])
            if obj.as_module is None:
                operand = NameNode(pos=self.pos, name=path[0])
                for attr in path[1:]:
                    operand = AttributeNode(pos=self.pos, obj=operand, attribute=attr)
                operand = AttributeNode(pos=self.pos, obj=operand, attribute=self.base_type.name)
                self.operand = operand
                self.__class__ = SizeofVarNode
                self.analyse_types(env)
                return
        if self.arg_type is None:
            base_type = self.base_type.analyse(env)
            _, arg_type = self.declarator.analyse(base_type, env)
            self.arg_type = arg_type
        self.check_type()
        
    def check_type(self):
        arg_type = self.arg_type
        if arg_type.is_pyobject and not arg_type.is_extension_type:
            error(self.pos, "Cannot take sizeof Python object")
        elif arg_type.is_void:
            error(self.pos, "Cannot take sizeof void")
        elif not arg_type.is_complete():
            error(self.pos, "Cannot take sizeof incomplete type '%s'" % arg_type)
        
    def calculate_result_code(self):
        if self.arg_type.is_extension_type:
            # the size of the pointer is boring
            # we want the size of the actual struct
            arg_code = self.arg_type.declaration_code("", deref=1)
        else:
            arg_code = self.arg_type.declaration_code("")
        return "(sizeof(%s))" % arg_code
    

class SizeofVarNode(SizeofNode):
    #  C sizeof function applied to a variable
    #
    #  operand   ExprNode
    
    subexprs = ['operand']
    
    def analyse_types(self, env):
        # We may actually be looking at a type rather than a variable...
        # If we are, traditional analysis would fail...
        operand_as_type = self.operand.analyse_as_type(env)
        if operand_as_type:
            self.arg_type = operand_as_type
            self.__class__ = SizeofTypeNode
            self.check_type()
        else:
            self.operand.analyse_types(env)
    
    def calculate_result_code(self):
        return "(sizeof(%s))" % self.operand.result()
    
    def generate_result_code(self, code):
        pass

class TypeofNode(ExprNode):
    #  Compile-time type of an expression, as a string.
    #
    #  operand   ExprNode
    #  literal   StringNode # internal
    
    literal = None
    type = py_object_type
    
    subexprs = ['literal'] # 'operand' will be ignored after type analysis!
    
    def analyse_types(self, env):
        self.operand.analyse_types(env)
        self.literal = StringNode(
            self.pos, value=StringEncoding.EncodedString(str(self.operand.type)))
        self.literal.analyse_types(env)
        self.literal = self.literal.coerce_to_pyobject(env)
    
    def generate_evaluation_code(self, code):
        self.literal.generate_evaluation_code(code)
    
    def calculate_result_code(self):
        return self.literal.calculate_result_code()

#-------------------------------------------------------------------
#
#  Binary operator nodes
#
#-------------------------------------------------------------------

def _not_in(x, seq):
    return x not in seq

compile_time_binary_operators = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt,
    'is': operator.is_,
    'is_not': operator.is_not,
    '+': operator.add,
    '&': operator.and_,
    '/': operator.truediv,
    '//': operator.floordiv,
    '<<': operator.lshift,
    '%': operator.mod,
    '*': operator.mul,
    '|': operator.or_,
    '**': operator.pow,
    '>>': operator.rshift,
    '-': operator.sub,
    '^': operator.xor,
    'in': operator.contains,
    'not_in': _not_in,
}

def get_compile_time_binop(node):
    func = compile_time_binary_operators.get(node.operator)
    if not func:
        error(node.pos,
            "Binary '%s' not supported in compile-time expression"
                % node.operator)
    return func

class BinopNode(ExprNode):
    #  operator     string
    #  operand1     ExprNode
    #  operand2     ExprNode
    #
    #  Processing during analyse_expressions phase:
    #
    #    analyse_c_operation
    #      Called when neither operand is a pyobject.
    #      - Check operand types and coerce if needed.
    #      - Determine result type and result code fragment.
    #      - Allocate temporary for result if needed.
    
    subexprs = ['operand1', 'operand2']

    def calculate_constant_result(self):
        func = compile_time_binary_operators[self.operator]
        self.constant_result = func(
            self.operand1.constant_result,
            self.operand2.constant_result)

    def compile_time_value(self, denv):
        func = get_compile_time_binop(self)
        operand1 = self.operand1.compile_time_value(denv)
        operand2 = self.operand2.compile_time_value(denv)
        try:
            return func(operand1, operand2)
        except Exception, e:
            self.compile_time_value_error(e)
    
    def infer_type(self, env):
        return self.result_type(self.operand1.infer_type(env),
                                self.operand2.infer_type(env))
    
    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        if self.is_py_operation():
            self.coerce_operands_to_pyobjects(env)
            self.type = py_object_type
            self.is_temp = 1
        else:
            self.analyse_c_operation(env)
    
    def is_py_operation(self):
        return self.is_py_operation_types(self.operand1.type, self.operand2.type)
    
    def is_py_operation_types(self, type1, type2):
        return type1.is_pyobject or type2.is_pyobject

    def result_type(self, type1, type2):
        if self.is_py_operation_types(type1, type2):
            return py_object_type
        else:
            return self.compute_c_result_type(type1, type2)

    def nogil_check(self, env):
        if self.is_py_operation():
            self.gil_error()
        
    def coerce_operands_to_pyobjects(self, env):
        self.operand1 = self.operand1.coerce_to_pyobject(env)
        self.operand2 = self.operand2.coerce_to_pyobject(env)
    
    def check_const(self):
        return self.operand1.check_const() and self.operand2.check_const()
    
    def generate_result_code(self, code):
        #print "BinopNode.generate_result_code:", self.operand1, self.operand2 ###
        if self.operand1.type.is_pyobject:
            function = self.py_operation_function()
            if function == "PyNumber_Power":
                extra_args = ", Py_None"
            else:
                extra_args = ""
            code.putln(
                "%s = %s(%s, %s%s); %s" % (
                    self.result(), 
                    function, 
                    self.operand1.py_result(),
                    self.operand2.py_result(),
                    extra_args,
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
    
    def type_error(self):
        if not (self.operand1.type.is_error
                or self.operand2.type.is_error):
            error(self.pos, "Invalid operand types for '%s' (%s; %s)" %
                (self.operator, self.operand1.type, 
                    self.operand2.type))
        self.type = PyrexTypes.error_type


class NumBinopNode(BinopNode):
    #  Binary operation taking numeric arguments.
    
    infix = True
    
    def analyse_c_operation(self, env):
        type1 = self.operand1.type
        type2 = self.operand2.type
        self.type = self.compute_c_result_type(type1, type2)
        if not self.type:
            self.type_error()
            return
        if self.type.is_complex:
            self.infix = False
        if not self.infix:
            self.operand1 = self.operand1.coerce_to(self.type, env)
            self.operand2 = self.operand2.coerce_to(self.type, env)
    
    def compute_c_result_type(self, type1, type2):
        if self.c_types_okay(type1, type2):
            return PyrexTypes.widest_numeric_type(type1, type2)
        else:
            return None

    def get_constant_c_result_code(self):
        value1 = self.operand1.get_constant_c_result_code()
        value2 = self.operand2.get_constant_c_result_code()
        if value1 and value2:
            return "(%s %s %s)" % (value1, self.operator, value2)
        else:
            return None
    
    def c_types_okay(self, type1, type2):
        #print "NumBinopNode.c_types_okay:", type1, type2 ###
        return (type1.is_numeric  or type1.is_enum) \
            and (type2.is_numeric  or type2.is_enum)

    def calculate_result_code(self):
        if self.infix:
            return "(%s %s %s)" % (
                self.operand1.result(), 
                self.operator, 
                self.operand2.result())
        else:
            func = self.type.binary_op(self.operator)
            if func is None:
                error(self.pos, "binary operator %s not supported for %s" % (self.operator, self.type))
            return "%s(%s, %s)" % (
                func,
                self.operand1.result(),
                self.operand2.result())
    
    def py_operation_function(self):
        return self.py_functions[self.operator]

    py_functions = {
        "|":        "PyNumber_Or",
        "^":        "PyNumber_Xor",
        "&":        "PyNumber_And",
        "<<":       "PyNumber_Lshift",
        ">>":       "PyNumber_Rshift",
        "+":        "PyNumber_Add",
        "-":        "PyNumber_Subtract",
        "*":        "PyNumber_Multiply",
        "/":        "__Pyx_PyNumber_Divide",
        "//":       "PyNumber_FloorDivide",
        "%":        "PyNumber_Remainder",
        "**":       "PyNumber_Power"
    }


class IntBinopNode(NumBinopNode):
    #  Binary operation taking integer arguments.
    
    def c_types_okay(self, type1, type2):
        #print "IntBinopNode.c_types_okay:", type1, type2 ###
        return (type1.is_int or type1.is_enum) \
            and (type2.is_int or type2.is_enum)

    
class AddNode(NumBinopNode):
    #  '+' operator.
    
    def is_py_operation_types(self, type1, type2):
        if type1.is_string and type2.is_string:
            return 1
        else:
            return NumBinopNode.is_py_operation_types(self, type1, type2)

    def compute_c_result_type(self, type1, type2):
        #print "AddNode.compute_c_result_type:", type1, self.operator, type2 ###
        if (type1.is_ptr or type1.is_array) and (type2.is_int or type2.is_enum):
            return type1
        elif (type2.is_ptr or type2.is_array) and (type1.is_int or type1.is_enum):
            return type2
        else:
            return NumBinopNode.compute_c_result_type(
                self, type1, type2)


class SubNode(NumBinopNode):
    #  '-' operator.
    
    def compute_c_result_type(self, type1, type2):
        if (type1.is_ptr or type1.is_array) and (type2.is_int or type2.is_enum):
            return type1
        elif (type1.is_ptr or type1.is_array) and (type2.is_ptr or type2.is_array):
            return PyrexTypes.c_int_type
        else:
            return NumBinopNode.compute_c_result_type(
                self, type1, type2)


class MulNode(NumBinopNode):
    #  '*' operator.
    
    def is_py_operation_types(self, type1, type2):
        if (type1.is_string and type2.is_int) \
            or (type2.is_string and type1.is_int):
                return 1
        else:
            return NumBinopNode.is_py_operation_types(self, type1, type2)


class DivNode(NumBinopNode):
    #  '/' or '//' operator.
    
    cdivision = None
    truedivision = None   # == "unknown" if operator == '/'
    ctruedivision = False
    cdivision_warnings = False
    zerodivision_check = None

    def find_compile_time_binary_operator(self, op1, op2):
        func = compile_time_binary_operators[self.operator]
        if self.operator == '/' and self.truedivision is None:
            # => true div for floats, floor div for integers
            if isinstance(op1, (int,long)) and isinstance(op2, (int,long)):
                func = compile_time_binary_operators['//']
        return func

    def calculate_constant_result(self):
        op1 = self.operand1.constant_result
        op2 = self.operand2.constant_result
        func = self.find_compile_time_binary_operator(op1, op2)
        self.constant_result = func(
            self.operand1.constant_result,
            self.operand2.constant_result)

    def compile_time_value(self, denv):
        operand1 = self.operand1.compile_time_value(denv)
        operand2 = self.operand2.compile_time_value(denv)
        try:
            func = self.find_compile_time_binary_operator(
                self, operand1, operand2)
            return func(operand1, operand2)
        except Exception, e:
            self.compile_time_value_error(e)

    def analyse_types(self, env):
        if self.cdivision or env.directives['cdivision']:
            self.ctruedivision = False
        else:
            self.ctruedivision = self.truedivision
        NumBinopNode.analyse_types(self, env)
        if not self.type.is_pyobject:
            self.zerodivision_check = (
                self.cdivision is None and not env.directives['cdivision']
                and (self.operand2.constant_result is not_a_constant or
                     self.operand2.constant_result == 0))
            if self.zerodivision_check or env.directives['cdivision_warnings']:
                # Need to check ahead of time to warn or raise zero division error
                self.operand1 = self.operand1.coerce_to_simple(env)
                self.operand2 = self.operand2.coerce_to_simple(env)
                if env.nogil:
                    error(self.pos, "Pythonic division not allowed without gil, consider using cython.cdivision(True)")

    def compute_c_result_type(self, type1, type2):
        if self.operator == '/' and self.ctruedivision:
            if not type1.is_float and not type2.is_float:
                widest_type = PyrexTypes.widest_numeric_type(type1, PyrexTypes.c_double_type)
                widest_type = PyrexTypes.widest_numeric_type(type2, widest_type)
                return widest_type
        return NumBinopNode.compute_c_result_type(self, type1, type2)

    def zero_division_message(self):
        if self.type.is_int:
            return "integer division or modulo by zero"
        else:
            return "float division"

    def generate_evaluation_code(self, code):
        if not self.type.is_pyobject and not self.type.is_complex:
            if self.cdivision is None:
                self.cdivision = (code.globalstate.directives['cdivision'] 
                                    or not self.type.signed
                                    or self.type.is_float)
            if not self.cdivision:
                code.globalstate.use_utility_code(div_int_utility_code.specialize(self.type))
        NumBinopNode.generate_evaluation_code(self, code)
        self.generate_div_warning_code(code)
    
    def generate_div_warning_code(self, code):
        if not self.type.is_pyobject:
            if self.zerodivision_check:
                if not self.infix:
                    zero_test = "%s(%s)" % (self.type.unary_op('zero'), self.operand2.result())
                else:
                    zero_test = "%s == 0" % self.operand2.result()
                code.putln("if (unlikely(%s)) {" % zero_test)
                code.putln('PyErr_Format(PyExc_ZeroDivisionError, "%s");' % self.zero_division_message())
                code.putln(code.error_goto(self.pos))
                code.putln("}")
                if self.type.is_int and self.type.signed and self.operator != '%':
                    code.globalstate.use_utility_code(division_overflow_test_code)
                    code.putln("else if (sizeof(%s) == sizeof(long) && unlikely(%s == -1) && unlikely(UNARY_NEG_WOULD_OVERFLOW(%s))) {" % (
                                    self.type.declaration_code(''), 
                                    self.operand2.result(),
                                    self.operand1.result()))
                    code.putln('PyErr_Format(PyExc_OverflowError, "value too large to perform division");')
                    code.putln(code.error_goto(self.pos))
                    code.putln("}")
            if code.globalstate.directives['cdivision_warnings'] and self.operator != '/':
                code.globalstate.use_utility_code(cdivision_warning_utility_code)
                code.putln("if ((%s < 0) ^ (%s < 0)) {" % (
                                self.operand1.result(),
                                self.operand2.result()))
                code.putln(code.set_error_info(self.pos));
                code.put("if (__Pyx_cdivision_warning()) ")
                code.put_goto(code.error_label)
                code.putln("}")
    
    def calculate_result_code(self):
        if self.type.is_complex:
            return NumBinopNode.calculate_result_code(self)
        elif self.type.is_float and self.operator == '//':
            return "floor(%s / %s)" % (
                self.operand1.result(),
                self.operand2.result())
        elif self.truedivision or self.cdivision:
            op1 = self.operand1.result()
            op2 = self.operand2.result()
            if self.truedivision:
                if self.type != self.operand1.type:
                    op1 = self.type.cast_code(op1)
                if self.type != self.operand2.type:
                    op2 = self.type.cast_code(op2)
            return "(%s / %s)" % (op1, op2)
        else:
            return "__Pyx_div_%s(%s, %s)" % (
                    self.type.specalization_name(),
                    self.operand1.result(), 
                    self.operand2.result())


class ModNode(DivNode):
    #  '%' operator.

    def is_py_operation_types(self, type1, type2):
        return (type1.is_string
            or type2.is_string
            or NumBinopNode.is_py_operation_types(self, type1, type2))

    def zero_division_message(self):
        if self.type.is_int:
            return "integer division or modulo by zero"
        else:
            return "float divmod()"
    
    def generate_evaluation_code(self, code):
        if not self.type.is_pyobject:
            if self.cdivision is None:
                self.cdivision = code.globalstate.directives['cdivision'] or not self.type.signed
            if not self.cdivision:
                if self.type.is_int:
                    code.globalstate.use_utility_code(mod_int_utility_code.specialize(self.type))
                else:
                    code.globalstate.use_utility_code(
                        mod_float_utility_code.specialize(self.type, math_h_modifier=self.type.math_h_modifier))
        NumBinopNode.generate_evaluation_code(self, code)
        self.generate_div_warning_code(code)
    
    def calculate_result_code(self):
        if self.cdivision:
            if self.type.is_float:
                return "fmod%s(%s, %s)" % (
                    self.type.math_h_modifier,
                    self.operand1.result(), 
                    self.operand2.result())
            else:
                return "(%s %% %s)" % (
                    self.operand1.result(), 
                    self.operand2.result())
        else:
            return "__Pyx_mod_%s(%s, %s)" % (
                    self.type.specalization_name(),
                    self.operand1.result(), 
                    self.operand2.result())

class PowNode(NumBinopNode):
    #  '**' operator.
    
    def analyse_c_operation(self, env):
        NumBinopNode.analyse_c_operation(self, env)
        if self.type.is_complex:
            error(self.pos, "complex powers not yet supported")
            self.pow_func = "<error>"
        elif self.type.is_float:
            self.pow_func = "pow"
        else:
            self.pow_func = "__Pyx_pow_%s" % self.type.declaration_code('').replace(' ', '_')
            env.use_utility_code(
                    int_pow_utility_code.specialize(func_name=self.pow_func, 
                                                type=self.type.declaration_code('')))

    def calculate_result_code(self):
        return "%s(%s, %s)" % (
            self.pow_func, 
            self.operand1.result(), 
            self.operand2.result())


# Note: This class is temporary "shut down" into an ineffective mode temp
# allocation mode.
#
# More sophisticated temp reuse was going on before,
# one could have a look at adding this again after /all/ classes
# are converted to the new temp scheme. (The temp juggling cannot work
# otherwise).
class BoolBinopNode(ExprNode):
    #  Short-circuiting boolean operation.
    #
    #  operator     string
    #  operand1     ExprNode
    #  operand2     ExprNode
    
    subexprs = ['operand1', 'operand2']
    
    def infer_type(self, env):
        type1 = self.operand1.infer_type(env)
        type2 = self.operand2.infer_type(env)
        return PyrexTypes.spanning_type(type1, type2)

    def calculate_constant_result(self):
        if self.operator == 'and':
            self.constant_result = \
                self.operand1.constant_result and \
                self.operand2.constant_result
        else:
            self.constant_result = \
                self.operand1.constant_result or \
                self.operand2.constant_result
    
    def compile_time_value(self, denv):
        if self.operator == 'and':
            return self.operand1.compile_time_value(denv) \
                and self.operand2.compile_time_value(denv)
        else:
            return self.operand1.compile_time_value(denv) \
                or self.operand2.compile_time_value(denv)
    
    def coerce_to_boolean(self, env):
        self.operand1 = self.operand1.coerce_to_boolean(env)
        self.operand2 = self.operand2.coerce_to_boolean(env)
        self.type = PyrexTypes.c_bint_type
        return self

    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        self.type = PyrexTypes.spanning_type(self.operand1.type, self.operand2.type)
        self.operand1 = self.operand1.coerce_to(self.type, env)
        self.operand2 = self.operand2.coerce_to(self.type, env)
        
        # For what we're about to do, it's vital that
        # both operands be temp nodes.
        self.operand1 = self.operand1.coerce_to_simple(env)
        self.operand2 = self.operand2.coerce_to_simple(env)
        self.is_temp = 1

    gil_message = "Truth-testing Python object"

    def check_const(self):
        return self.operand1.check_const() and self.operand2.check_const()
    
    def generate_evaluation_code(self, code):
        code.mark_pos(self.pos)
        self.operand1.generate_evaluation_code(code)
        test_result, uses_temp = self.generate_operand1_test(code)
        if self.operator == 'and':
            sense = ""
        else:
            sense = "!"
        code.putln(
            "if (%s%s) {" % (
                sense,
                test_result))
        if uses_temp:
            code.funcstate.release_temp(test_result)
        self.operand1.generate_disposal_code(code)
        self.operand2.generate_evaluation_code(code)
        self.allocate_temp_result(code)
        self.operand2.make_owned_reference(code)
        code.putln("%s = %s;" % (self.result(), self.operand2.result()))
        self.operand2.generate_post_assignment_code(code)
        self.operand2.free_temps(code)
        code.putln("} else {")
        self.operand1.make_owned_reference(code)
        code.putln("%s = %s;" % (self.result(), self.operand1.result()))
        self.operand1.generate_post_assignment_code(code)
        self.operand1.free_temps(code)
        code.putln("}")
    
    def generate_operand1_test(self, code):
        #  Generate code to test the truth of the first operand.
        if self.type.is_pyobject:
            test_result = code.funcstate.allocate_temp(PyrexTypes.c_bint_type,
                                                       manage_ref=False)
            code.putln(
                "%s = __Pyx_PyObject_IsTrue(%s); %s" % (
                    test_result,
                    self.operand1.py_result(),
                    code.error_goto_if_neg(test_result, self.pos)))
        else:
            test_result = self.operand1.result()
        return (test_result, self.type.is_pyobject)


class CondExprNode(ExprNode):
    #  Short-circuiting conditional expression.
    #
    #  test        ExprNode
    #  true_val    ExprNode
    #  false_val   ExprNode
    
    true_val = None
    false_val = None
    
    subexprs = ['test', 'true_val', 'false_val']
    
    def type_dependencies(self, env):
        return self.true_val.type_dependencies(env) + self.false_val.type_dependencies(env)
    
    def infer_type(self, env):
        return self.compute_result_type(self.true_val.infer_type(env),
                                        self.false_val.infer_type(env))

    def calculate_constant_result(self):
        if self.test.constant_result:
            self.constant_result = self.true_val.constant_result
        else:
            self.constant_result = self.false_val.constant_result

    def analyse_types(self, env):
        self.test.analyse_types(env)
        self.test = self.test.coerce_to_boolean(env)
        self.true_val.analyse_types(env)
        self.false_val.analyse_types(env)
        self.type = self.compute_result_type(self.true_val.type, self.false_val.type)
        if self.true_val.type.is_pyobject or self.false_val.type.is_pyobject:
            self.true_val = self.true_val.coerce_to(self.type, env)
            self.false_val = self.false_val.coerce_to(self.type, env)
        self.is_temp = 1
        if self.type == PyrexTypes.error_type:
            self.type_error()
        
    def compute_result_type(self, type1, type2):
        if type1 == type2:
            return type1
        elif type1.is_numeric and type2.is_numeric:
            return PyrexTypes.widest_numeric_type(type1, type2)
        elif type1.is_extension_type and type1.subtype_of_resolved_type(type2):
            return type2
        elif type2.is_extension_type and type2.subtype_of_resolved_type(type1):
            return type1
        elif type1.is_pyobject or type2.is_pyobject:
            return py_object_type
        elif type1.assignable_from(type2):
            return type1
        elif type2.assignable_from(type1):
            return type2
        else:
            return PyrexTypes.error_type
        
    def type_error(self):
        if not (self.true_val.type.is_error or self.false_val.type.is_error):
            error(self.pos, "Incompatable types in conditional expression (%s; %s)" %
                (self.true_val.type, self.false_val.type))
        self.type = PyrexTypes.error_type
    
    def check_const(self):
        return (self.test.check_const() 
            and self.true_val.check_const()
            and self.false_val.check_const())
    
    def generate_evaluation_code(self, code):
        # Because subexprs may not be evaluated we can use a more optimal
        # subexpr allocation strategy than the default, so override evaluation_code.
        
        code.mark_pos(self.pos)
        self.allocate_temp_result(code)
        self.test.generate_evaluation_code(code)
        code.putln("if (%s) {" % self.test.result() )
        self.eval_and_get(code, self.true_val)
        code.putln("} else {")
        self.eval_and_get(code, self.false_val)
        code.putln("}")
        self.test.generate_disposal_code(code)
        self.test.free_temps(code)

    def eval_and_get(self, code, expr):
        expr.generate_evaluation_code(code)
        expr.make_owned_reference(code)
        code.putln("%s = %s;" % (self.result(), expr.result()))
        expr.generate_post_assignment_code(code)
        expr.free_temps(code)

richcmp_constants = {
    "<" : "Py_LT",
    "<=": "Py_LE",
    "==": "Py_EQ",
    "!=": "Py_NE",
    "<>": "Py_NE",
    ">" : "Py_GT",
    ">=": "Py_GE",
}

class CmpNode(object):
    #  Mixin class containing code common to PrimaryCmpNodes
    #  and CascadedCmpNodes.
    
    def infer_types(self, env):
        # TODO: Actually implement this (after merging with -unstable).
        return py_object_type

    def calculate_cascaded_constant_result(self, operand1_result):
        func = compile_time_binary_operators[self.operator]
        operand2_result = self.operand2.constant_result
        result = func(operand1_result, operand2_result)
        if result and self.cascade:
            result = result and \
                self.cascade.cascaded_compile_time_value(operand2_result)
        self.constant_result = result
    
    def cascaded_compile_time_value(self, operand1, denv):
        func = get_compile_time_binop(self)
        operand2 = self.operand2.compile_time_value(denv)
        try:
            result = func(operand1, operand2)
        except Exception, e:
            self.compile_time_value_error(e)
            result = None
        if result:
            cascade = self.cascade
            if cascade:
                # FIXME: I bet this must call cascaded_compile_time_value()
                result = result and cascade.compile_time_value(operand2, denv)
        return result

    def find_common_int_type(self, env, op, operand1, operand2):
        # type1 != type2 and at least one of the types is not a C int
        type1 = operand1.type
        type2 = operand2.type
        type1_can_be_int = False
        type2_can_be_int = False

        if isinstance(operand1, (StringNode, BytesNode)) \
               and operand1.can_coerce_to_char_literal():
            type1_can_be_int = True
        if isinstance(operand2, (StringNode, BytesNode)) \
                 and operand2.can_coerce_to_char_literal():
            type2_can_be_int = True

        if type1.is_int:
            if type2_can_be_int:
                return type1
        elif type2.is_int:
            if type1_can_be_int:
                return type2
        elif type1_can_be_int:
            if type2_can_be_int:
                return PyrexTypes.c_uchar_type

        return None

    def find_common_type(self, env, op, operand1, common_type=None):
        operand2 = self.operand2
        type1 = operand1.type
        type2 = operand2.type

        new_common_type = None

        # catch general errors
        if type1 == str_type and (type2.is_string or type2 in (bytes_type, unicode_type)) or \
               type2 == str_type and (type1.is_string or type1 in (bytes_type, unicode_type)):
            error(self.pos, "Comparisons between bytes/unicode and str are not portable to Python 3")
            new_common_type = error_type

        # try to use numeric comparisons where possible
        elif type1.is_complex or type2.is_complex:
            if op not in ('==', '!='):
                error(self.pos, "complex types are unordered")
                new_common_type = error_type
            if type1.is_pyobject:
                new_common_type = type1
            elif type2.is_pyobject:
                new_common_type = type2
            else:
                new_common_type = PyrexTypes.widest_numeric_type(type1, type2)
        elif type1.is_numeric and type2.is_numeric:
            new_common_type = PyrexTypes.widest_numeric_type(type1, type2)
        elif common_type is None or not common_type.is_pyobject:
            new_common_type = self.find_common_int_type(env, op, operand1, operand2)

        if new_common_type is None:
            # fall back to generic type compatibility tests
            if type1 == type2:
                new_common_type = type1
            elif type1.is_pyobject or type2.is_pyobject:
                if type2.is_numeric or type2.is_string:
                    if operand2.check_for_coercion_error(type1):
                        new_common_type = error_type
                    else:
                        new_common_type = py_object_type
                elif type1.is_numeric or type1.is_string:
                    if operand1.check_for_coercion_error(type2):
                        new_common_type = error_type
                    else:
                        new_common_type = py_object_type
                elif py_object_type.assignable_from(type1) and py_object_type.assignable_from(type2):
                    new_common_type = py_object_type
                else:
                    # one Python type and one non-Python type, not assignable
                    self.invalid_types_error(operand1, op, operand2)
                    new_common_type = error_type
            elif type1.assignable_from(type2):
                new_common_type = type1
            elif type2.assignable_from(type1):
                new_common_type = type2
            else:
                # C types that we couldn't handle up to here are an error
                self.invalid_types_error(operand1, op, operand2)
                new_common_type = error_type

        # recursively merge types
        if common_type is None or new_common_type.is_error:
            common_type = new_common_type
        else:
            # we could do a lot better by splitting the comparison
            # into a non-Python part and a Python part, but this is
            # safer for now
            common_type = PyrexTypes.spanning_type(common_type, new_common_type)

        if self.cascade:
            common_type = self.cascade.find_common_type(env, self.operator, operand2, common_type)

        return common_type

    def invalid_types_error(self, operand1, op, operand2):
        error(self.pos, "Invalid types for '%s' (%s, %s)" %
              (op, operand1.type, operand2.type))

    def is_python_comparison(self):
        return (self.has_python_operands()
                or (self.cascade and self.cascade.is_python_comparison())
                or self.operator in ('in', 'not_in'))

    def coerce_operands_to(self, dst_type, env):
        operand2 = self.operand2
        if operand2.type != dst_type:
            self.operand2 = operand2.coerce_to(dst_type, env)
        if self.cascade:
            self.cascade.coerce_operands_to(dst_type, env)

    def is_python_result(self):
        return ((self.has_python_operands() and
                 self.operator not in ('is', 'is_not', 'in', 'not_in'))
            or (self.cascade and self.cascade.is_python_result()))

    def generate_operation_code(self, code, result_code, 
            operand1, op , operand2):
        if self.type is PyrexTypes.py_object_type:
            coerce_result = "__Pyx_PyBool_FromLong"
        else:
            coerce_result = ""
        if 'not' in op: 
            negation = "!"
        else: 
            negation = ""
        if op == 'in' or op == 'not_in':
            code.globalstate.use_utility_code(contians_utility_code)
            if self.type is PyrexTypes.py_object_type:
                coerce_result = "__Pyx_PyBoolOrNull_FromLong"
            if op == 'not_in':
                negation = "__Pyx_NegateNonNeg"
            if operand2.type is dict_type:
                code.globalstate.use_utility_code(
                    raise_none_iter_error_utility_code)
                code.putln("if (unlikely(%s == Py_None)) {" % operand2.py_result())
                code.putln("__Pyx_RaiseNoneNotIterableError(); %s" %
                           code.error_goto(self.pos))
                code.putln("} else {")
                method = "PyDict_Contains"
            else:
                method = "PySequence_Contains"
            if self.type is PyrexTypes.py_object_type:
                error_clause = code.error_goto_if_null
                got_ref = "__Pyx_XGOTREF(%s); " % result_code
            else:
                error_clause = code.error_goto_if_neg
                got_ref = ""
            code.putln(
                "%s = %s(%s(%s(%s, %s))); %s%s" % (
                    result_code,
                    coerce_result,
                    negation,
                    method,
                    operand2.py_result(), 
                    operand1.py_result(), 
                    got_ref,
                    error_clause(result_code, self.pos)))
            if operand2.type is dict_type:
                code.putln("}")
                    
        elif (operand1.type.is_pyobject
            and op not in ('is', 'is_not')):
                code.putln("%s = PyObject_RichCompare(%s, %s, %s); %s" % (
                        result_code, 
                        operand1.py_result(), 
                        operand2.py_result(), 
                        richcmp_constants[op],
                        code.error_goto_if_null(result_code, self.pos)))
                code.put_gotref(result_code)
        elif operand1.type.is_complex:
            if op == "!=": 
                negation = "!"
            else: 
                negation = ""
            code.putln("%s = %s(%s%s(%s, %s));" % (
                result_code, 
                coerce_result,
                negation,
                operand1.type.unary_op('eq'), 
                operand1.result(), 
                operand2.result()))
        else:
            type1 = operand1.type
            type2 = operand2.type
            if (type1.is_extension_type or type2.is_extension_type) \
                    and not type1.same_as(type2):
                common_type = py_object_type
            elif type1.is_numeric:
                common_type = PyrexTypes.widest_numeric_type(type1, type2)
            else:
                common_type = type1
            code1 = operand1.result_as(common_type)
            code2 = operand2.result_as(common_type)
            code.putln("%s = %s(%s %s %s);" % (
                result_code, 
                coerce_result, 
                code1, 
                self.c_operator(op), 
                code2))

    def c_operator(self, op):
        if op == 'is':
            return "=="
        elif op == 'is_not':
            return "!="
        else:
            return op
    
contians_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE long __Pyx_NegateNonNeg(long b) { return unlikely(b < 0) ? b : !b; }
static CYTHON_INLINE PyObject* __Pyx_PyBoolOrNull_FromLong(long b) {
    return unlikely(b < 0) ? NULL : __Pyx_PyBool_FromLong(b);
}
""")


class PrimaryCmpNode(ExprNode, CmpNode):
    #  Non-cascaded comparison or first comparison of
    #  a cascaded sequence.
    #
    #  operator      string
    #  operand1      ExprNode
    #  operand2      ExprNode
    #  cascade       CascadedCmpNode
    
    #  We don't use the subexprs mechanism, because
    #  things here are too complicated for it to handle.
    #  Instead, we override all the framework methods
    #  which use it.
    
    child_attrs = ['operand1', 'operand2', 'cascade']
    
    cascade = None

    def infer_type(self, env):
        # TODO: Actually implement this (after merging with -unstable).
        return py_object_type

    def type_dependencies(self, env):
        return ()

    def calculate_constant_result(self):
        self.constant_result = self.calculate_cascaded_constant_result(
            self.operand1.constant_result)
    
    def compile_time_value(self, denv):
        operand1 = self.operand1.compile_time_value(denv)
        return self.cascaded_compile_time_value(operand1, denv)

    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        if self.cascade:
            self.cascade.analyse_types(env)

        if self.operator in ('in', 'not_in'):
            common_type = py_object_type
            self.is_pycmp = True
        else:
            common_type = self.find_common_type(env, self.operator, self.operand1)
            self.is_pycmp = common_type.is_pyobject

        if not common_type.is_error:
            if self.operand1.type != common_type:
                self.operand1 = self.operand1.coerce_to(common_type, env)
            self.coerce_operands_to(common_type, env)

        if self.cascade:
            self.operand2 = self.operand2.coerce_to_simple(env)
            self.cascade.coerce_cascaded_operands_to_temp(env)
        if self.is_python_result():
            self.type = PyrexTypes.py_object_type
        else:
            self.type = PyrexTypes.c_bint_type
        cdr = self.cascade
        while cdr:
            cdr.type = self.type
            cdr = cdr.cascade
        if self.is_pycmp or self.cascade:
            self.is_temp = 1

    def has_python_operands(self):
        return (self.operand1.type.is_pyobject
            or self.operand2.type.is_pyobject)
    
    def check_const(self):
        if self.cascade:
            self.not_const()
            return False
        else:
            return self.operand1.check_const() and self.operand2.check_const()

    def calculate_result_code(self):
        if self.operand1.type.is_complex:
            if self.operator == "!=":
                negation = "!"
            else:
                negation = ""
            return "(%s%s(%s, %s))" % (
                negation,
                self.operand1.type.binary_op('=='), 
                self.operand1.result(), 
                self.operand2.result())
        else:
            return "(%s %s %s)" % (
                self.operand1.result(),
                self.c_operator(self.operator),
                self.operand2.result())

    def generate_evaluation_code(self, code):
        self.operand1.generate_evaluation_code(code)
        self.operand2.generate_evaluation_code(code)
        if self.is_temp:
            self.allocate_temp_result(code)
            self.generate_operation_code(code, self.result(), 
                self.operand1, self.operator, self.operand2)
            if self.cascade:
                self.cascade.generate_evaluation_code(code,
                    self.result(), self.operand2)
            self.operand1.generate_disposal_code(code)
            self.operand1.free_temps(code)
            self.operand2.generate_disposal_code(code)
            self.operand2.free_temps(code)

    def generate_subexpr_disposal_code(self, code):
        #  If this is called, it is a non-cascaded cmp,
        #  so only need to dispose of the two main operands.
        self.operand1.generate_disposal_code(code)
        self.operand2.generate_disposal_code(code)
        
    def free_subexpr_temps(self, code):
        #  If this is called, it is a non-cascaded cmp,
        #  so only need to dispose of the two main operands.
        self.operand1.free_temps(code)
        self.operand2.free_temps(code)
        
    def annotate(self, code):
        self.operand1.annotate(code)
        self.operand2.annotate(code)
        if self.cascade:
            self.cascade.annotate(code)


class CascadedCmpNode(Node, CmpNode):
    #  A CascadedCmpNode is not a complete expression node. It 
    #  hangs off the side of another comparison node, shares 
    #  its left operand with that node, and shares its result 
    #  with the PrimaryCmpNode at the head of the chain.
    #
    #  operator      string
    #  operand2      ExprNode
    #  cascade       CascadedCmpNode

    child_attrs = ['operand2', 'cascade']

    cascade = None
    constant_result = constant_value_not_set # FIXME: where to calculate this?

    def infer_type(self, env):
        # TODO: Actually implement this (after merging with -unstable).
        return py_object_type

    def type_dependencies(self, env):
        return ()

    def analyse_types(self, env):
        self.operand2.analyse_types(env)
        if self.cascade:
            self.cascade.analyse_types(env)

    def has_python_operands(self):
        return self.operand2.type.is_pyobject
        
    def coerce_operands_to_pyobjects(self, env):
        self.operand2 = self.operand2.coerce_to_pyobject(env)
        if self.cascade:
            self.cascade.coerce_operands_to_pyobjects(env)

    def coerce_cascaded_operands_to_temp(self, env):
        if self.cascade:
            #self.operand2 = self.operand2.coerce_to_temp(env) #CTT
            self.operand2 = self.operand2.coerce_to_simple(env)
            self.cascade.coerce_cascaded_operands_to_temp(env)
    
    def generate_evaluation_code(self, code, result, operand1):
        if self.type.is_pyobject:
            code.putln("if (__Pyx_PyObject_IsTrue(%s)) {" % result)
            code.put_decref(result, self.type)
        else:
            code.putln("if (%s) {" % result)
        self.operand2.generate_evaluation_code(code)
        self.generate_operation_code(code, result, 
            operand1, self.operator, self.operand2)
        if self.cascade:
            self.cascade.generate_evaluation_code(
                code, result, self.operand2)
        # Cascaded cmp result is always temp
        self.operand2.generate_disposal_code(code)
        self.operand2.free_temps(code)
        code.putln("}")

    def annotate(self, code):
        self.operand2.annotate(code)
        if self.cascade:
            self.cascade.annotate(code)


binop_node_classes = {
    "or":       BoolBinopNode,
    "and":      BoolBinopNode,
    "|":        IntBinopNode,
    "^":        IntBinopNode,
    "&":        IntBinopNode,
    "<<":       IntBinopNode,
    ">>":       IntBinopNode,
    "+":        AddNode,
    "-":        SubNode,
    "*":        MulNode,
    "/":        DivNode,
    "//":       DivNode,
    "%":        ModNode,
    "**":       PowNode
}

def binop_node(pos, operator, operand1, operand2):
    # Construct binop node of appropriate class for 
    # given operator.
    return binop_node_classes[operator](pos, 
        operator = operator, 
        operand1 = operand1, 
        operand2 = operand2)

#-------------------------------------------------------------------
#
#  Coercion nodes
#
#  Coercion nodes are special in that they are created during
#  the analyse_types phase of parse tree processing.
#  Their __init__ methods consequently incorporate some aspects
#  of that phase.
#
#-------------------------------------------------------------------

class CoercionNode(ExprNode):
    #  Abstract base class for coercion nodes.
    #
    #  arg       ExprNode       node being coerced
    
    subexprs = ['arg']
    constant_result = not_a_constant
    
    def __init__(self, arg):
        self.pos = arg.pos
        self.arg = arg
        if debug_coercion:
            print("%s Coercing %s" % (self, self.arg))

    def calculate_constant_result(self):
        # constant folding can break type coercion, so this is disabled
        pass
            
    def annotate(self, code):
        self.arg.annotate(code)
        if self.arg.type != self.type:
            file, line, col = self.pos
            code.annotate((file, line, col-1), AnnotationItem(style='coerce', tag='coerce', text='[%s] to [%s]' % (self.arg.type, self.type)))


class CastNode(CoercionNode):
    #  Wrap a node in a C type cast.
    
    def __init__(self, arg, new_type):
        CoercionNode.__init__(self, arg)
        self.type = new_type
    
    def calculate_result_code(self):
        return self.arg.result_as(self.type)

    def generate_result_code(self, code):
        self.arg.generate_result_code(code)


class PyTypeTestNode(CoercionNode):
    #  This node is used to check that a generic Python
    #  object is an instance of a particular extension type.
    #  This node borrows the result of its argument node.

    def __init__(self, arg, dst_type, env, notnone=False):
        #  The arg is know to be a Python object, and
        #  the dst_type is known to be an extension type.
        assert dst_type.is_extension_type or dst_type.is_builtin_type, "PyTypeTest on non extension type"
        CoercionNode.__init__(self, arg)
        self.type = dst_type
        self.result_ctype = arg.ctype()
        self.notnone = notnone

    nogil_check = Node.gil_error
    gil_message = "Python type test"
    
    def analyse_types(self, env):
        pass
    
    def result_in_temp(self):
        return self.arg.result_in_temp()
    
    def is_ephemeral(self):
        return self.arg.is_ephemeral()

    def calculate_constant_result(self):
        # FIXME
        pass

    def calculate_result_code(self):
        return self.arg.result()
    
    def generate_result_code(self, code):
        if self.type.typeobj_is_available():
            if not self.type.is_builtin_type:
                code.globalstate.use_utility_code(type_test_utility_code)
            code.putln(
                "if (!(%s)) %s" % (
                    self.type.type_test_code(self.arg.py_result(), self.notnone),
                    code.error_goto(self.pos)))
        else:
            error(self.pos, "Cannot test type of extern C class "
                "without type object name specification")
                
    def generate_post_assignment_code(self, code):
        self.arg.generate_post_assignment_code(code)

    def free_temps(self, code):
        self.arg.free_temps(code)


class NoneCheckNode(CoercionNode):
    # This node is used to check that a Python object is not None and
    # raises an appropriate exception (as specified by the creating
    # transform).

    def __init__(self, arg, exception_type_cname, exception_message):
        CoercionNode.__init__(self, arg)
        self.type = arg.type
        self.result_ctype = arg.ctype()
        self.exception_type_cname = exception_type_cname
        self.exception_message = exception_message

    def analyse_types(self, env):
        pass

    def result_in_temp(self):
        return self.arg.result_in_temp()

    def calculate_result_code(self):
        return self.arg.result()
    
    def generate_result_code(self, code):
        code.putln(
            "if (unlikely(%s == Py_None)) {" % self.arg.result())
        code.putln('PyErr_SetString(%s, "%s"); %s ' % (
            self.exception_type_cname,
            StringEncoding.escape_byte_string(
                self.exception_message.encode('UTF-8')),
            code.error_goto(self.pos)))
        code.putln("}")

    def generate_post_assignment_code(self, code):
        self.arg.generate_post_assignment_code(code)

    def free_temps(self, code):
        self.arg.free_temps(code)


class CoerceToPyTypeNode(CoercionNode):
    #  This node is used to convert a C data type
    #  to a Python object.
    
    type = py_object_type
    is_temp = 1

    def __init__(self, arg, env, type=py_object_type):
        CoercionNode.__init__(self, arg)
        if not arg.type.create_to_py_utility_code(env):
            error(arg.pos,
                "Cannot convert '%s' to Python object" % arg.type)
        if type is not py_object_type:
            self.type = py_object_type
        elif arg.type.is_string:
            self.type = Builtin.bytes_type

    gil_message = "Converting to Python object"

    def coerce_to_boolean(self, env):
        return self.arg.coerce_to_boolean(env).coerce_to_temp(env)
    
    def coerce_to_integer(self, env):
        # If not already some C integer type, coerce to longint.
        if self.arg.type.is_int:
            return self.arg
        else:
            return self.arg.coerce_to(PyrexTypes.c_long_type, env)

    def analyse_types(self, env):
        # The arg is always already analysed
        pass

    def generate_result_code(self, code):
        function = self.arg.type.to_py_function
        code.putln('%s = %s(%s); %s' % (
            self.result(), 
            function, 
            self.arg.result(), 
            code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class CoerceFromPyTypeNode(CoercionNode):
    #  This node is used to convert a Python object
    #  to a C data type.

    def __init__(self, result_type, arg, env):
        CoercionNode.__init__(self, arg)
        self.type = result_type
        self.is_temp = 1
        if not result_type.create_from_py_utility_code(env):
            error(arg.pos,
                "Cannot convert Python object to '%s'" % result_type)
        if self.type.is_string and self.arg.is_ephemeral():
            error(arg.pos,
                "Obtaining char * from temporary Python value")
    
    def analyse_types(self, env):
        # The arg is always already analysed
        pass

    def generate_result_code(self, code):
        function = self.type.from_py_function
        operand = self.arg.py_result()
        rhs = "%s(%s)" % (function, operand)
        if self.type.is_enum:
            rhs = typecast(self.type, c_long_type, rhs)
        code.putln('%s = %s; %s' % (
            self.result(), 
            rhs,
            code.error_goto_if(self.type.error_condition(self.result()), self.pos)))
        if self.type.is_pyobject:
            code.put_gotref(self.py_result())


class CoerceToBooleanNode(CoercionNode):
    #  This node is used when a result needs to be used
    #  in a boolean context.
    
    type = PyrexTypes.c_bint_type
    
    def __init__(self, arg, env):
        CoercionNode.__init__(self, arg)
        if arg.type.is_pyobject:
            self.is_temp = 1

    def nogil_check(self, env):
        if self.arg.type.is_pyobject:
            self.gil_error()

    gil_message = "Truth-testing Python object"
    
    def check_const(self):
        if self.is_temp:
            self.not_const()
            return False
        return self.arg.check_const()
    
    def calculate_result_code(self):
        return "(%s != 0)" % self.arg.result()

    def generate_result_code(self, code):
        if self.arg.type.is_pyobject:
            code.putln(
                "%s = __Pyx_PyObject_IsTrue(%s); %s" % (
                    self.result(), 
                    self.arg.py_result(), 
                    code.error_goto_if_neg(self.result(), self.pos)))

class CoerceToComplexNode(CoercionNode):

    def __init__(self, arg, dst_type, env):
        if arg.type.is_complex:
            arg = arg.coerce_to_simple(env)
        self.type = dst_type
        CoercionNode.__init__(self, arg)
        dst_type.create_declaration_utility_code(env)

    def calculate_result_code(self):
        if self.arg.type.is_complex:
            real_part = "__Pyx_CREAL(%s)" % self.arg.result()
            imag_part = "__Pyx_CIMAG(%s)" % self.arg.result()
        else:
            real_part = self.arg.result()
            imag_part = "0"
        return "%s(%s, %s)" % (
                self.type.from_parts,
                real_part,
                imag_part)
    
    def generate_result_code(self, code):
        pass

class CoerceToTempNode(CoercionNode):
    #  This node is used to force the result of another node
    #  to be stored in a temporary. It is only used if the
    #  argument node's result is not already in a temporary.

    def __init__(self, arg, env):
        CoercionNode.__init__(self, arg)
        self.type = self.arg.type
        self.is_temp = 1
        if self.type.is_pyobject:
            self.result_ctype = py_object_type

    gil_message = "Creating temporary Python reference"

    def analyse_types(self, env):
        # The arg is always already analysed
        pass
        
    def coerce_to_boolean(self, env):
        self.arg = self.arg.coerce_to_boolean(env)
        self.type = self.arg.type
        self.result_ctype = self.type
        return self

    def generate_result_code(self, code):
        #self.arg.generate_evaluation_code(code) # Already done
        # by generic generate_subexpr_evaluation_code!
        code.putln("%s = %s;" % (
            self.result(), self.arg.result_as(self.ctype())))
        if self.type.is_pyobject and self.use_managed_ref:
            code.put_incref(self.result(), self.ctype())


class CloneNode(CoercionNode):
    #  This node is employed when the result of another node needs
    #  to be used multiple times. The argument node's result must
    #  be in a temporary. This node "borrows" the result from the
    #  argument node, and does not generate any evaluation or
    #  disposal code for it. The original owner of the argument 
    #  node is responsible for doing those things.
    
    subexprs = [] # Arg is not considered a subexpr
    nogil_check = None
    
    def __init__(self, arg):
        CoercionNode.__init__(self, arg)
        if hasattr(arg, 'type'):
            self.type = arg.type
            self.result_ctype = arg.result_ctype
        if hasattr(arg, 'entry'):
            self.entry = arg.entry
            
    def result(self):
        return self.arg.result()
    
    def type_dependencies(self, env):
        return self.arg.type_dependencies(env)
    
    def infer_type(self, env):
        return self.arg.infer_type(env)

    def analyse_types(self, env):
        self.type = self.arg.type
        self.result_ctype = self.arg.result_ctype
        self.is_temp = 1
        if hasattr(self.arg, 'entry'):
            self.entry = self.arg.entry
    
    def generate_evaluation_code(self, code):
        pass

    def generate_result_code(self, code):
        pass
        
    def generate_disposal_code(self, code):
        pass
                
    def free_temps(self, code):
        pass


class ModuleRefNode(ExprNode):
    # Simple returns the module object
    
    type = py_object_type
    is_temp = False
    subexprs = []
    
    def analyse_types(self, env):
        pass

    def calculate_result_code(self):
        return Naming.module_cname

    def generate_result_code(self, code):
        pass

class DocstringRefNode(ExprNode):
    # Extracts the docstring of the body element
    
    subexprs = ['body']
    type = py_object_type
    is_temp = True
    
    def __init__(self, pos, body):
        ExprNode.__init__(self, pos)
        assert body.type.is_pyobject
        self.body = body

    def analyse_types(self, env):
        pass

    def generate_result_code(self, code):
        code.putln('%s = __Pyx_GetAttrString(%s, "__doc__");' %
                   (self.result(), self.body.result()))
        code.put_gotref(self.result())



#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

get_name_interned_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/
""",
impl = """
static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name) {
    PyObject *result;
    result = PyObject_GetAttr(dict, name);
    if (!result)
        PyErr_SetObject(PyExc_NameError, name);
    return result;
}
""")

#------------------------------------------------------------------------------------

import_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/
""",
impl = """
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list) {
    PyObject *__import__ = 0;
    PyObject *empty_list = 0;
    PyObject *module = 0;
    PyObject *global_dict = 0;
    PyObject *empty_dict = 0;
    PyObject *list;
    __import__ = __Pyx_GetAttrString(%(BUILTINS)s, "__import__");
    if (!__import__)
        goto bad;
    if (from_list)
        list = from_list;
    else {
        empty_list = PyList_New(0);
        if (!empty_list)
            goto bad;
        list = empty_list;
    }
    global_dict = PyModule_GetDict(%(GLOBALS)s);
    if (!global_dict)
        goto bad;
    empty_dict = PyDict_New();
    if (!empty_dict)
        goto bad;
    module = PyObject_CallFunctionObjArgs(__import__,
        name, global_dict, empty_dict, list, NULL);
bad:
    Py_XDECREF(empty_list);
    Py_XDECREF(__import__);
    Py_XDECREF(empty_dict);
    return module;
}
""" % {
    "BUILTINS": Naming.builtins_cname,
    "GLOBALS":  Naming.module_cname,
})

#------------------------------------------------------------------------------------

get_exception_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_GetExcValue(void); /*proto*/
""",
impl = """
static PyObject *__Pyx_GetExcValue(void) {
    PyObject *type = 0, *value = 0, *tb = 0;
    PyObject *tmp_type, *tmp_value, *tmp_tb;
    PyObject *result = 0;
    PyThreadState *tstate = PyThreadState_Get();
    PyErr_Fetch(&type, &value, &tb);
    PyErr_NormalizeException(&type, &value, &tb);
    if (PyErr_Occurred())
        goto bad;
    if (!value) {
        value = Py_None;
        Py_INCREF(value);
    }
    tmp_type = tstate->exc_type;
    tmp_value = tstate->exc_value;
    tmp_tb = tstate->exc_traceback;
    tstate->exc_type = type;
    tstate->exc_value = value;
    tstate->exc_traceback = tb;
    /* Make sure tstate is in a consistent state when we XDECREF
    these objects (XDECREF may run arbitrary code). */
    Py_XDECREF(tmp_type);
    Py_XDECREF(tmp_value);
    Py_XDECREF(tmp_tb);
    result = value;
    Py_XINCREF(result);
    type = 0;
    value = 0;
    tb = 0;
bad:
    Py_XDECREF(type);
    Py_XDECREF(value);
    Py_XDECREF(tb);
    return result;
}
""")

#------------------------------------------------------------------------------------

type_test_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/
""",
impl = """
static CYTHON_INLINE int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type) {
    if (unlikely(!type)) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if (likely(PyObject_TypeCheck(obj, type)))
        return 1;
    PyErr_Format(PyExc_TypeError, "Cannot convert %.200s to %.200s",
                 Py_TYPE(obj)->tp_name, type->tp_name);
    return 0;
}
""")

#------------------------------------------------------------------------------------

create_class_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name, const char *modname); /*proto*/
""",
impl = """
static PyObject *__Pyx_CreateClass(
    PyObject *bases, PyObject *dict, PyObject *name, const char *modname)
{
    PyObject *py_modname;
    PyObject *result = 0;

    #if PY_MAJOR_VERSION < 3
    py_modname = PyString_FromString(modname);
    #else
    py_modname = PyUnicode_FromString(modname);
    #endif
    if (!py_modname)
        goto bad;
    if (PyDict_SetItemString(dict, "__module__", py_modname) < 0)
        goto bad;
    #if PY_MAJOR_VERSION < 3
    result = PyClass_New(bases, dict, name);
    #else
    result = PyObject_CallFunctionObjArgs((PyObject *)&PyType_Type, name, bases, dict, NULL);
    #endif
bad:
    Py_XDECREF(py_modname);
    return result;
}
""")

#------------------------------------------------------------------------------------

cpp_exception_utility_code = UtilityCode(
proto = """
#ifndef __Pyx_CppExn2PyErr
static void __Pyx_CppExn2PyErr() {
  try {
    if (PyErr_Occurred())
      ; // let the latest Python exn pass through and ignore the current one
    else
      throw;
  } catch (const std::out_of_range& exn) {
    // catch out_of_range explicitly so the proper Python exn may be raised
    PyErr_SetString(PyExc_IndexError, exn.what());
  } catch (const std::exception& exn) {
    PyErr_SetString(PyExc_RuntimeError, exn.what());
  }
  catch (...)
  {
    PyErr_SetString(PyExc_RuntimeError, "Unknown exception");
  }
}
#endif
""",
impl = ""
)

#------------------------------------------------------------------------------------

# If the is_unsigned flag is set, we need to do some extra work to make 
# sure the index doesn't become negative. 

getitem_int_utility_code = UtilityCode(
proto = """

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Generic(PyObject *o, PyObject* j) {
    PyObject *r;
    if (!j) return NULL;
    r = PyObject_GetItem(o, j);
    Py_DECREF(j);
    return r;
}

""" + ''.join([
"""
#define __Pyx_GetItemInt_%(type)s(o, i, size, to_py_func) ((size <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_GetItemInt_%(type)s_Fast(o, i, size <= sizeof(long)) : \\
                                                    __Pyx_GetItemInt_Generic(o, to_py_func(i)))

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_%(type)s_Fast(PyObject *o, Py_ssize_t i, int fits_long) {
    if (likely(o != Py_None)) {
        if (likely((0 <= i) & (i < Py%(type)s_GET_SIZE(o)))) {
            PyObject *r = Py%(type)s_GET_ITEM(o, i);
            Py_INCREF(r);
            return r;
        }
        else if ((-Py%(type)s_GET_SIZE(o) <= i) & (i < 0)) {
            PyObject *r = Py%(type)s_GET_ITEM(o, Py%(type)s_GET_SIZE(o) + i);
            Py_INCREF(r);
            return r;
        }
    }
    return __Pyx_GetItemInt_Generic(o, fits_long ? PyInt_FromLong(i) : PyLong_FromLongLong(i));
}
""" % {'type' : type_name} for type_name in ('List', 'Tuple')
]) + """

#define __Pyx_GetItemInt(o, i, size, to_py_func) ((size <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_GetItemInt_Fast(o, i, size <= sizeof(long)) : \\
                                                    __Pyx_GetItemInt_Generic(o, to_py_func(i)))

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i, int fits_long) {
    PyObject *r;
    if (PyList_CheckExact(o) && ((0 <= i) & (i < PyList_GET_SIZE(o)))) {
        r = PyList_GET_ITEM(o, i);
        Py_INCREF(r);
    }
    else if (PyTuple_CheckExact(o) && ((0 <= i) & (i < PyTuple_GET_SIZE(o)))) {
        r = PyTuple_GET_ITEM(o, i);
        Py_INCREF(r);
    }
    else if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_item && (likely(i >= 0))) {
        r = PySequence_GetItem(o, i);
    }
    else {
        r = __Pyx_GetItemInt_Generic(o, fits_long ? PyInt_FromLong(i) : PyLong_FromLongLong(i));
    }
    return r;
}
""",
impl = """
""")



#------------------------------------------------------------------------------------

setitem_int_utility_code = UtilityCode(
proto = """
#define __Pyx_SetItemInt(o, i, v, size, to_py_func) ((size <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_SetItemInt_Fast(o, i, v, size <= sizeof(long)) : \\
                                                    __Pyx_SetItemInt_Generic(o, to_py_func(i), v))

static CYTHON_INLINE int __Pyx_SetItemInt_Generic(PyObject *o, PyObject *j, PyObject *v) {
    int r;
    if (!j) return -1;
    r = PyObject_SetItem(o, j, v);
    Py_DECREF(j);
    return r;
}

static CYTHON_INLINE int __Pyx_SetItemInt_Fast(PyObject *o, Py_ssize_t i, PyObject *v, int fits_long) {
    if (PyList_CheckExact(o) && ((0 <= i) & (i < PyList_GET_SIZE(o)))) {
        Py_INCREF(v);
        Py_DECREF(PyList_GET_ITEM(o, i));
        PyList_SET_ITEM(o, i, v);
        return 1;
    }
    else if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_ass_item && (likely(i >= 0)))
        return PySequence_SetItem(o, i, v);
    else {
        PyObject *j = fits_long ? PyInt_FromLong(i) : PyLong_FromLongLong(i);
        return __Pyx_SetItemInt_Generic(o, j, v);
    }
}
""",
impl = """
""")

#------------------------------------------------------------------------------------

delitem_int_utility_code = UtilityCode(
proto = """
#define __Pyx_DelItemInt(o, i, size, to_py_func) ((size <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_DelItemInt_Fast(o, i, size <= sizeof(long)) : \\
                                                    __Pyx_DelItem_Generic(o, to_py_func(i)))

static CYTHON_INLINE int __Pyx_DelItem_Generic(PyObject *o, PyObject *j) {
    int r;
    if (!j) return -1;
    r = PyObject_DelItem(o, j);
    Py_DECREF(j);
    return r;
}

static CYTHON_INLINE int __Pyx_DelItemInt_Fast(PyObject *o, Py_ssize_t i, int fits_long) {
    if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_ass_item && likely(i >= 0))
        return PySequence_DelItem(o, i);
    else {
        PyObject *j = fits_long ? PyInt_FromLong(i) : PyLong_FromLongLong(i);
        return __Pyx_DelItem_Generic(o, j);
    }
}
""",
impl = """
""")

#------------------------------------------------------------------------------------

raise_noneattr_error_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_RaiseNoneAttributeError(const char* attrname);
""",
impl = '''
static CYTHON_INLINE void __Pyx_RaiseNoneAttributeError(const char* attrname) {
    PyErr_Format(PyExc_AttributeError, "'NoneType' object has no attribute '%s'", attrname);
}
''')

raise_noneindex_error_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_RaiseNoneIndexingError(void);
""",
impl = '''
static CYTHON_INLINE void __Pyx_RaiseNoneIndexingError(void) {
    PyErr_SetString(PyExc_TypeError, "'NoneType' object is unsubscriptable");
}
''')

raise_none_iter_error_utility_code = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_RaiseNoneNotIterableError(void);
""",
impl = '''
static CYTHON_INLINE void __Pyx_RaiseNoneNotIterableError(void) {
    PyErr_SetString(PyExc_TypeError, "'NoneType' object is not iterable");
}
''')

raise_too_many_values_to_unpack = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_RaiseTooManyValuesError(void);
""",
impl = '''
static CYTHON_INLINE void __Pyx_RaiseTooManyValuesError(void) {
    PyErr_SetString(PyExc_ValueError, "too many values to unpack");
}
''')

raise_need_more_values_to_unpack = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_RaiseNeedMoreValuesError(Py_ssize_t index);
""",
impl = '''
static CYTHON_INLINE void __Pyx_RaiseNeedMoreValuesError(Py_ssize_t index) {
    PyErr_Format(PyExc_ValueError,
        #if PY_VERSION_HEX < 0x02050000
                 "need more than %d value%s to unpack", (int)index,
        #else
                 "need more than %zd value%s to unpack", index,
        #endif
                 (index == 1) ? "" : "s");
}
''')

#------------------------------------------------------------------------------------

tuple_unpacking_error_code = UtilityCode(
proto = """
static void __Pyx_UnpackTupleError(PyObject *, Py_ssize_t index); /*proto*/
""", 
impl = """
static void __Pyx_UnpackTupleError(PyObject *t, Py_ssize_t index) {
    if (t == Py_None) {
      __Pyx_RaiseNoneNotIterableError();
    } else if (PyTuple_GET_SIZE(t) < index) {
      __Pyx_RaiseNeedMoreValuesError(PyTuple_GET_SIZE(t));
    } else {
      __Pyx_RaiseTooManyValuesError();
    }
}
""", 
requires = [raise_none_iter_error_utility_code,
            raise_need_more_values_to_unpack,
            raise_too_many_values_to_unpack]
)

unpacking_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_UnpackItem(PyObject *, Py_ssize_t index); /*proto*/
static int __Pyx_EndUnpack(PyObject *); /*proto*/
""",
impl = """
static PyObject *__Pyx_UnpackItem(PyObject *iter, Py_ssize_t index) {
    PyObject *item;
    if (!(item = PyIter_Next(iter))) {
        if (!PyErr_Occurred()) {
            __Pyx_RaiseNeedMoreValuesError(index);
        }
    }
    return item;
}

static int __Pyx_EndUnpack(PyObject *iter) {
    PyObject *item;
    if ((item = PyIter_Next(iter))) {
        Py_DECREF(item);
        __Pyx_RaiseTooManyValuesError();
        return -1;
    }
    else if (!PyErr_Occurred())
        return 0;
    else
        return -1;
}
""",
requires = [raise_need_more_values_to_unpack,
            raise_too_many_values_to_unpack]
)

#------------------------------------------------------------------------------------

# CPython supports calling functions with non-dict kwargs by
# converting them to a dict first

kwargs_call_utility_code = UtilityCode(
proto = """
static PyObject* __Pyx_PyEval_CallObjectWithKeywords(PyObject*, PyObject*, PyObject*); /*proto*/
""",
impl = """
static PyObject* __Pyx_PyEval_CallObjectWithKeywords(PyObject *callable, PyObject *args, PyObject *kwargs) {
    PyObject* result;
    if (likely(PyDict_Check(kwargs))) {
        return PyEval_CallObjectWithKeywords(callable, args, kwargs);
    } else {
        PyObject* real_dict;
        real_dict = PyObject_CallFunctionObjArgs((PyObject*)&PyDict_Type, kwargs, NULL);
        if (unlikely(!real_dict))
            return NULL;
        result = PyEval_CallObjectWithKeywords(callable, args, real_dict);
        Py_DECREF(real_dict);
        return result; /* may be NULL */
    }
}
""", 
)


#------------------------------------------------------------------------------------

int_pow_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE %(type)s %(func_name)s(%(type)s, %(type)s); /* proto */
""",
impl="""
static CYTHON_INLINE %(type)s %(func_name)s(%(type)s b, %(type)s e) {
    %(type)s t = b;
    switch (e) {
        case 3:
            t *= b;
        case 2:
            t *= b;
        case 1:
            return t;
        case 0:
            return 1;
    }
    if (unlikely(e<0)) return 0;
    t = 1;
    while (likely(e)) {
        t *= (b * (e&1)) | ((~e)&1);    /* 1 or b */
        b *= b;
        e >>= 1;
    }
    return t;
}
""")

# ------------------------------ Division ------------------------------------

div_int_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE %(type)s __Pyx_div_%(type_name)s(%(type)s, %(type)s); /* proto */
""",
impl="""
static CYTHON_INLINE %(type)s __Pyx_div_%(type_name)s(%(type)s a, %(type)s b) {
    %(type)s q = a / b;
    %(type)s r = a - q*b;
    q -= ((r != 0) & ((r ^ b) < 0));
    return q;
}
""")

mod_int_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE %(type)s __Pyx_mod_%(type_name)s(%(type)s, %(type)s); /* proto */
""",
impl="""
static CYTHON_INLINE %(type)s __Pyx_mod_%(type_name)s(%(type)s a, %(type)s b) {
    %(type)s r = a %% b;
    r += ((r != 0) & ((r ^ b) < 0)) * b;
    return r;
}
""")

mod_float_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE %(type)s __Pyx_mod_%(type_name)s(%(type)s, %(type)s); /* proto */
""",
impl="""
static CYTHON_INLINE %(type)s __Pyx_mod_%(type_name)s(%(type)s a, %(type)s b) {
    %(type)s r = fmod%(math_h_modifier)s(a, b);
    r += ((r != 0) & ((r < 0) ^ (b < 0))) * b;
    return r;
}
""")

cdivision_warning_utility_code = UtilityCode(
proto="""
static int __Pyx_cdivision_warning(void); /* proto */
""",
impl="""
static int __Pyx_cdivision_warning(void) {
    return PyErr_WarnExplicit(PyExc_RuntimeWarning, 
                              "division with oppositely signed operands, C and Python semantics differ",
                              %(FILENAME)s, 
                              %(LINENO)s,
                              __Pyx_MODULE_NAME,
                              NULL);
}
""" % {
    'FILENAME': Naming.filename_cname,
    'LINENO':  Naming.lineno_cname,
})

# from intobject.c
division_overflow_test_code = UtilityCode(
proto="""
#define UNARY_NEG_WOULD_OVERFLOW(x)	\
	(((x) < 0) & ((unsigned long)(x) == 0-(unsigned long)(x)))
""")
