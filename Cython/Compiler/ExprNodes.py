#
#   Pyrex - Parse tree nodes for expressions
#

import operator
from string import join

from Errors import error, warning, InternalError
from Errors import hold_errors, release_errors, held_errors, report_error
from Cython.Utils import UtilityCode
import StringEncoding
import Naming
from Nodes import Node
import PyrexTypes
from PyrexTypes import py_object_type, c_long_type, typecast, error_type
from Builtin import list_type, tuple_type, dict_type, unicode_type
import Symtab
import Options
from Annotate import AnnotationItem

from Cython.Debugging import print_call_chain
from DebugFlags import debug_disposal_code, debug_temp_alloc, \
    debug_coercion


class ExprNode(Node):
    #  subexprs     [string]     Class var holding names of subexpr node attrs
    #  type         PyrexType    Type of the result
    #  result_code  string       Code fragment
    #  result_ctype string       C type of result_code if different from type
    #  is_temp      boolean      Result is in a temporary variable
    #  is_sequence_constructor  
    #               boolean      Is a list or tuple constructor expression
    #  saved_subexpr_nodes
    #               [ExprNode or [ExprNode or None] or None]
    #                            Cached result of subexpr_nodes()
    
    result_ctype = None
    type = None

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
    #      allocate_temps
    #        - Call allocate_temps for all sub-nodes.
    #        - Call allocate_temp for this node.
    #        - If a temporary was allocated, call release_temp on 
    #          all sub-expressions.
    #
    #      allocate_target_temps
    #        - Call allocate_temps on sub-nodes and allocate any other
    #          temps used during assignment.
    #        - Fill in result_code with a C lvalue if needed.
    #        - If a rhs node is supplied, call release_temp on it.
    #        - Call release_temp on sub-nodes and release any other
    #          temps used during assignment.
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

    def get_child_attrs(self):
        return self.subexprs
    child_attrs = property(fget=get_child_attrs)
        
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
        if self.saved_subexpr_nodes is None:
            nodes = []
            for name in self.subexprs:
                item = getattr(self, name)
                if item:
                    if isinstance(item, ExprNode):
                        nodes.append(item)
                    else:
                        nodes.extend(item)
            self.saved_subexpr_nodes = nodes
        return self.saved_subexpr_nodes
        
    def result(self):
        if not self.is_temp or self.is_target:
            return self.calculate_result_code()
        else: # i.e. self.is_temp:
            return self.result_code
    
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
        self.allocate_temps(env)
        self.check_const()
    
    def analyse_expressions(self, env):
        #  Convenience routine performing both the Type
        #  Analysis and Temp Allocation phases for a whole 
        #  expression.
        self.analyse_types(env)
        self.allocate_temps(env)
    
    def analyse_target_expression(self, env, rhs):
        #  Convenience routine performing both the Type
        #  Analysis and Temp Allocation phases for the LHS of
        #  an assignment.
        self.analyse_target_types(env)
        self.allocate_target_temps(env, rhs)
    
    def analyse_boolean_expression(self, env):
        #  Analyse expression and coerce to a boolean.
        self.analyse_types(env)
        bool = self.coerce_to_boolean(env)
        bool.allocate_temps(env)
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
        temp_bool.allocate_temps(env)
        return temp_bool
    
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

    def gil_assignment_check(self, env):
        if env.nogil and self.type.is_pyobject:
            error(self.pos, "Assignment of Python object not allowed without gil")

    def check_const(self):
        self.not_const()
    
    def not_const(self):
        error(self.pos, "Not allowed in a constant expression")
    
    def check_const_addr(self):
        self.addr_not_const()
    
    def addr_not_const(self):
        error(self.pos, "Address is not constant")

    def gil_check(self, env):
        if env.nogil and self.type.is_pyobject:
            self.gil_error()

    # ----------------- Result Allocation -----------------
    
    def result_in_temp(self):
        #  Return true if result is in a temporary owned by
        #  this node or one of its subexpressions. Overridden
        #  by certain nodes which can share the result of
        #  a subnode.
        return self.is_temp
            
    def allocate_target_temps(self, env, rhs):
        #  Perform temp allocation for the LHS of an assignment.
        if debug_temp_alloc:
            print("%s Allocating target temps" % self)
        self.allocate_subexpr_temps(env)
        self.is_target = True
        if rhs:
            rhs.release_temp(env)
        self.release_subexpr_temps(env)
    
    def allocate_temps(self, env, result = None):
        #  Allocate temporary variables for this node and
        #  all its sub-expressions. If a result is specified,
        #  this must be a temp node and the specified variable
        #  is used as the result instead of allocating a new
        #  one.
        if debug_temp_alloc:
            print("%s Allocating temps" % self)
        self.allocate_subexpr_temps(env)
        self.allocate_temp(env, result)
        if self.is_temp:
            self.release_subexpr_temps(env)
    
    def allocate_subexpr_temps(self, env):
        #  Allocate temporary variables for all sub-expressions
        #  of this node.
        if debug_temp_alloc:
            print("%s Allocating temps for: %s" % (self, self.subexprs))
        for node in self.subexpr_nodes():
            if node:
                if debug_temp_alloc:
                    print("%s Allocating temps for %s" % (self, node))
                node.allocate_temps(env)
    
    def allocate_temp(self, env, result = None):
        #  If this node requires a temporary variable for its
        #  result, allocate one, otherwise set the result to
        #  a C code fragment. If a result is specified,
        #  this must be a temp node and the specified variable
        #  is used as the result instead of allocating a new
        #  one.
        if debug_temp_alloc:
            print("%s Allocating temp" % self)
        if result:
            if not self.is_temp:
                raise InternalError("Result forced on non-temp node")
            self.result_code = result
        elif self.is_temp:
            type = self.type
            if not type.is_void:
                if type.is_pyobject:
                    type = PyrexTypes.py_object_type
                self.result_code = env.allocate_temp(type)
            else:
                self.result_code = None
            if debug_temp_alloc:
                print("%s Allocated result %s" % (self, self.result_code))
                
    def target_code(self):
        #  Return code fragment for use as LHS of a C assignment.
        return self.calculate_result_code()
    
    def calculate_result_code(self):
        self.not_implemented("calculate_result_code")
    
#	def release_target_temp(self, env):
#		#  Release temporaries used by LHS of an assignment.
#		self.release_subexpr_temps(env)

    def release_temp(self, env):
        #  If this node owns a temporary result, release it,
        #  otherwise release results of its sub-expressions.
        if self.is_temp:
            if debug_temp_alloc:
                print("%s Releasing result %s" % (self, self.result_code))
            env.release_temp(self.result_code)
        else:
            self.release_subexpr_temps(env)
    
    def release_subexpr_temps(self, env):
        #  Release the results of all sub-expressions of
        #  this node.
        for node in self.subexpr_nodes():
            if node:
                node.release_temp(env)
    
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
        self.pre_generate_result_code(code)
        self.generate_result_code(code)
        if self.is_temp:
            self.generate_subexpr_disposal_code(code)

    def pre_generate_result_code(self, code):
        pass
    
    def generate_subexpr_evaluation_code(self, code):
        for node in self.subexpr_nodes():
            node.generate_evaluation_code(code)
    
    def generate_result_code(self, code):
        self.not_implemented("generate_result_code")
    
    def generate_disposal_code(self, code):
        # If necessary, generate code to dispose of 
        # temporary Python reference.
        if self.is_temp:
            if self.type.is_pyobject:
                code.put_decref_clear(self.result(), self.ctype())
        else:
            self.generate_subexpr_disposal_code(code)
    
    def generate_subexpr_disposal_code(self, code):
        #  Generate code to dispose of temporary results
        #  of all sub-expressions.
        for node in self.subexpr_nodes():
            node.generate_disposal_code(code)
    
    def generate_post_assignment_code(self, code):
        # Same as generate_disposal_code except that
        # assignment will have absorbed a reference to
        # the result if it is a Python object.
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
        src = self
        src_type = self.type
        src_is_py_type = src_type.is_pyobject
        dst_is_py_type = dst_type.is_pyobject
        
        if dst_type.is_pyobject:
            if not src.type.is_pyobject:
                src = CoerceToPyTypeNode(src, env)
            if not src.type.subtype_of(dst_type):
                if not isinstance(src, NoneNode):
                    src = PyTypeTestNode(src, dst_type, env)
        elif src.type.is_pyobject:
            src = CoerceFromPyTypeNode(dst_type, src, env)
        else: # neither src nor dst are py types
            # Added the string comparison, since for c types that
            # is enough, but Cython gets confused when the types are
            # in different files.
            if not (str(src.type) == str(dst_type) or dst_type.assignable_from(src_type)):
                error(self.pos, "Cannot assign type '%s' to '%s'" %
                    (src.type, dst_type))
        return src

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


class NewTempExprNode(ExprNode):
    backwards_compatible_result = None
    
    def result(self):
        if self.is_temp:
            return self.temp_code
        else:
            return self.calculate_result_code()

    def allocate_target_temps(self, env, rhs):
        self.allocate_subexpr_temps(env)
        rhs.release_temp(rhs)
        self.release_subexpr_temps(env)

    def allocate_temps(self, env, result = None):
        self.allocate_subexpr_temps(env)
        self.backwards_compatible_result = result
        if self.is_temp:
            self.release_subexpr_temps(env)

    def allocate_temp(self, env, result = None):
        assert result is None

    def release_temp(self, env):
        if self.is_temp:
            pass
        else:
            self.release_subexpr_temps(env)

    def pre_generate_result_code(self, code):
        if self.is_temp:
            type = self.type
            if not type.is_void:
                if type.is_pyobject:
                    type = PyrexTypes.py_object_type
                if self.backwards_compatible_result:
                    self.temp_code = self.backwards_compatible_result
                else:
                    self.temp_code = code.funcstate.allocate_temp(type)
            else:
                self.temp_code = None

    def generate_disposal_code(self, code):
        if self.is_temp:
            if self.type.is_pyobject:
                code.put_decref_clear(self.result(), self.ctype())
            if not self.backwards_compatible_result:
                code.funcstate.release_temp(self.temp_code)
        else:
            self.generate_subexpr_disposal_code(code)

    def generate_post_assignment_code(self, code):
        if self.is_temp:
            if self.type.is_pyobject:
                code.putln("%s = 0;" % self.temp_code)
            if not self.backwards_compatible_result:
                code.funcstate.release_temp(self.temp_code)
        else:
            self.generate_subexpr_disposal_code(code)

    
        

class AtomicExprNode(ExprNode):
    #  Abstract base class for expression nodes which have
    #  no sub-expressions.
    
    subexprs = []


class PyConstNode(AtomicExprNode):
    #  Abstract base class for constant Python values.
    
    is_literal = 1
    
    def is_simple(self):
        return 1
    
    def analyse_types(self, env):
        self.type = py_object_type
    
    def calculate_result_code(self):
        return self.value

    def generate_result_code(self, code):
        pass


class NoneNode(PyConstNode):
    #  The constant value None
    
    value = "Py_None"
    
    def compile_time_value(self, denv):
        return None
    
class EllipsisNode(PyConstNode):
    #  '...' in a subscript list.
    
    value = "Py_Ellipsis"

    def compile_time_value(self, denv):
        return Ellipsis


class ConstNode(AtomicExprNode):
    # Abstract base type for literal constant nodes.
    #
    # value     string      C code fragment
    
    is_literal = 1
    
    def is_simple(self):
        return 1
    
    def analyse_types(self, env):
        pass # Types are held in class variables
    
    def check_const(self):
        pass
    
    def calculate_result_code(self):
        return str(self.value)

    def generate_result_code(self, code):
        pass


class BoolNode(ConstNode):
    type = PyrexTypes.c_bint_type
    #  The constant value True or False
    
    def compile_time_value(self, denv):
        return self.value
    
    def calculate_result_code(self):
        return str(int(self.value))

class NullNode(ConstNode):
    type = PyrexTypes.c_null_ptr_type
    value = "NULL"


class CharNode(ConstNode):
    type = PyrexTypes.c_char_type
    
    def compile_time_value(self, denv):
        return ord(self.value)
    
    def calculate_result_code(self):
        return "'%s'" % StringEncoding.escape_character(self.value)


class IntNode(ConstNode):

    # unsigned     "" or "U"
    # longness     "" or "L" or "LL"

    unsigned = ""
    longness = ""
    type = PyrexTypes.c_long_type

    def coerce_to(self, dst_type, env):
        if dst_type.is_numeric:
            self.type = PyrexTypes.c_long_type
            return self
        # Arrange for a Python version of the number to be pre-allocated
        # when coercing to a Python type.
        if dst_type.is_pyobject:
            self.entry = env.get_py_num(self.value, self.longness)
            self.type = PyrexTypes.py_object_type
        # We still need to perform normal coerce_to processing on the
        # result, because we might be coercing to an extension type,
        # in which case a type test node will be needed.
        return ConstNode.coerce_to(self, dst_type, env)
        
    def coerce_to_boolean(self, env):
        self.type = PyrexTypes.c_bint_type
        return self

    def calculate_result_code(self):
        if self.type.is_pyobject:
            return self.entry.cname
        else:
            return str(self.value) + self.unsigned + self.longness

    def compile_time_value(self, denv):
        return int(self.value, 0)


class FloatNode(ConstNode):
    type = PyrexTypes.c_double_type

    def compile_time_value(self, denv):
        return float(self.value)
    
    def calculate_result_code(self):
        strval = str(self.value)
        if strval == 'nan':
            return "(Py_HUGE_VAL * 0)"
        elif strval == 'inf':
            return "Py_HUGE_VAL"
        elif strval == '-inf':
            return "(-Py_HUGE_VAL)"
        else:
            return strval


class StringNode(ConstNode):
    #  entry   Symtab.Entry
    
    type = PyrexTypes.c_char_ptr_type

    def compile_time_value(self, denv):
        return self.value
    
    def analyse_types(self, env):
        self.entry = env.add_string_const(self.value)
        
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
    
    def coerce_to(self, dst_type, env):
        if dst_type == PyrexTypes.c_char_ptr_type:
            self.type = PyrexTypes.c_char_ptr_type
            return self
            
        if dst_type.is_int:
            if not self.type.is_pyobject and len(self.entry.init) == 1:
                return CharNode(self.pos, value=self.value)
            else:
                error(self.pos, "Only coerce single-character ascii strings can be used as ints.")
                return self
        # Arrange for a Python version of the string to be pre-allocated
        # when coercing to a Python type.
        if dst_type.is_pyobject and not self.type.is_pyobject:
            node = self.as_py_string_node(env)
        else:
            node = self
        # We still need to perform normal coerce_to processing on the
        # result, because we might be coercing to an extension type,
        # in which case a type test node will be needed.
        return ConstNode.coerce_to(node, dst_type, env)

    def as_py_string_node(self, env):
        # Return a new StringNode with the same entry as this node
        # but whose type is a Python type instead of a C type.
        entry = self.entry
        env.add_py_string(entry)
        return StringNode(self.pos, value = self.value, entry = entry, type = py_object_type)
            
    def calculate_result_code(self):
        if self.type.is_pyobject:
            return self.entry.pystring_cname
        else:
            return self.entry.cname


class UnicodeNode(PyConstNode):
    #  entry   Symtab.Entry

    type = unicode_type

    def analyse_types(self, env):
        self.entry = env.add_string_const(self.value)
        env.add_py_string(self.entry)

    def calculate_result_code(self):
        return self.entry.pystring_cname
    
    def _coerce_to(self, dst_type, env):
        if not dst_type.is_pyobject:
            node = StringNode(self.pos, entry = entry, type = py_object_type)
            return ConstNode.coerce_to(node, dst_type, env)
        else:
            return self
        # We still need to perform normal coerce_to processing on the
        # result, because we might be coercing to an extension type,
        # in which case a type test node will be needed.
        
    def compile_time_value(self, env):
        return self.value


class IdentifierStringNode(ConstNode):
    # A Python string that behaves like an identifier, e.g. for
    # keyword arguments in a call, or for imported names
    type = PyrexTypes.py_object_type

    def analyse_types(self, env):
        self.cname = env.intern_identifier(self.value)

    def calculate_result_code(self):
        return self.cname


class LongNode(AtomicExprNode):
    #  Python long integer literal
    #
    #  value   string
    
    def compile_time_value(self, denv):
        return long(self.value)

    gil_message = "Constructing Python long int"
    
    def analyse_types(self, env):
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Constructing Python long int"

    def generate_evaluation_code(self, code):
        code.putln(
            '%s = PyLong_FromString("%s", 0, 0); %s' % (
                self.result(),
                self.value,
                code.error_goto_if_null(self.result(), self.pos)))


class ImagNode(AtomicExprNode):
    #  Imaginary number literal
    #
    #  value   float    imaginary part
    
    def compile_time_value(self, denv):
        return complex(0.0, self.value)
    
    def analyse_types(self, env):
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Constructing complex number"

    def generate_evaluation_code(self, code):
        code.putln(
            "%s = PyComplex_FromDoubles(0.0, %s); %s" % (
                self.result(),
                self.value,
                code.error_goto_if_null(self.result(), self.pos)))


class NameNode(AtomicExprNode):
    #  Reference to a local or global variable name.
    #
    #  name            string    Python name of the variable
    #
    #  entry           Entry     Symbol table entry
    #  interned_cname  string
    
    is_name = True
    is_cython_module = False
    cython_attribute = None
    lhs_of_first_assignment = False
    entry = None

    def create_analysed_rvalue(pos, env, entry):
        node = NameNode(pos)
        node.analyse_types(env, entry=entry)
        return node
        
    def as_cython_attribute(self):
        return self.cython_attribute
    
    create_analysed_rvalue = staticmethod(create_analysed_rvalue)
    
    def compile_time_value(self, denv):
        try:
            return denv.lookup(self.name)
        except KeyError:
            error(self.pos, "Compile-time name '%s' not defined" % self.name)
    
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
        return AtomicExprNode.coerce_to(self, dst_type, env)
    
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
            self.entry = env.declare_var(self.name, py_object_type, self.pos)
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
            env.use_utility_code(get_name_interned_utility_code)
            self.gil_check(env)

    gil_message = "Accessing Python global or builtin"

    def analyse_entry(self, env):
        #print "NameNode.analyse_entry:", self.name ###
        self.check_identifier_kind()
        entry = self.entry
        type = entry.type
        self.type = type
        if entry.is_pyglobal or entry.is_builtin:
            assert type.is_pyobject, "Python global or builtin not a Python object"
            self.interned_cname = self.entry.interned_cname = \
                env.intern_identifier(self.entry.name)

    def check_identifier_kind(self):
        #print "NameNode.check_identifier_kind:", self.entry.name ###
        #print self.entry.__dict__ ###
        entry = self.entry
        #entry.used = 1
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
    
    def check_const_addr(self):
        entry = self.entry
        if not (entry.is_cglobal or entry.is_cfunction or entry.is_builtin):
            self.addr_not_const()

    def is_lvalue(self):
        return self.entry.is_variable and \
            not self.entry.type.is_array and \
            not self.entry.is_readonly
    
    def is_ephemeral(self):
        #  Name nodes are never ephemeral, even if the
        #  result is in a temporary.
        return 0
    
    def allocate_temp(self, env, result = None):
        AtomicExprNode.allocate_temp(self, env, result)
        entry = self.entry
        if entry:
            entry.used = 1
            if entry.type.is_buffer:
                import Buffer
                Buffer.used_buffer_aux_vars(entry)
            if entry.utility_code:
                env.use_utility_code(entry.utility_code)
        
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
            if entry.is_builtin:
                namespace = Naming.builtins_cname
            else: # entry.is_pyglobal
                namespace = entry.scope.namespace_cname
            code.putln(
                '%s = __Pyx_GetName(%s, %s); %s' % (
                self.result(),
                namespace, 
                self.interned_cname,
                code.error_goto_if_null(self.result(), self.pos)))
        elif entry.is_local and False:
            # control flow not good enough yet
            assigned = entry.scope.control_flow.get_state((entry.name, 'initalized'), self.pos)
            if assigned is False:
                error(self.pos, "local variable '%s' referenced before assignment" % entry.name)
            elif not Options.init_local_none and assigned is None:
                code.putln('if (%s == 0) { PyErr_SetString(PyExc_UnboundLocalError, "%s"); %s }' % (entry.cname, entry.name, code.error_goto(self.pos)))
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
            namespace = self.entry.scope.namespace_cname
            if entry.is_member:
                # if the entry is a member we have to cheat: SetAttr does not work
                # on types, so we create a descriptor which is then added to tp_dict
                code.put_error_if_neg(self.pos,
                    'PyDict_SetItem(%s->tp_dict, %s, %s)' % (
                        namespace,
                        self.interned_cname,
                        rhs.py_result()))
                # in Py2.6+, we need to invalidate the method cache
                code.putln("PyType_Modified(%s);" %
                           entry.scope.parent_type.typeptr_cname)
            else: 
                code.put_error_if_neg(self.pos,
                    'PyObject_SetAttr(%s, %s, %s)' % (
                        namespace,
                        self.interned_cname,
                        rhs.py_result()))
                if debug_disposal_code:
                    print("NameNode.generate_assignment_code:")
                    print("...generating disposal code for %s" % rhs)
                rhs.generate_disposal_code(code)
                
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
                rhs.make_owned_reference(code)
                #print "NameNode.generate_assignment_code: to", self.name ###
                #print "...from", rhs ###
                #print "...LHS type", self.type, "ctype", self.ctype() ###
                #print "...RHS type", rhs.type, "ctype", rhs.ctype() ###
                if not self.lhs_of_first_assignment:
                    if entry.is_local and not Options.init_local_none:
                        initalized = entry.scope.control_flow.get_state((entry.name, 'initalized'), self.pos)
                        if initalized is True:
                            code.put_decref(self.result(), self.ctype())
                        elif initalized is None:
                            code.put_xdecref(self.result(), self.ctype())
                    else:
                        code.put_decref(self.result(), self.ctype())
            code.putln('%s = %s;' % (self.result(), rhs.result_as(self.ctype())))
            if debug_disposal_code:
                print("NameNode.generate_assignment_code:")
                print("...generating post-assignment code for %s" % rhs)
            rhs.generate_post_assignment_code(code)

    def generate_acquire_buffer(self, rhs, code):
        rhstmp = code.funcstate.allocate_temp(self.entry.type)
        buffer_aux = self.entry.buffer_aux
        bufstruct = buffer_aux.buffer_info_var.cname
        code.putln('%s = %s;' % (rhstmp, rhs.result_as(self.ctype())))

        import Buffer
        Buffer.put_assign_to_buffer(self.result(), rhstmp, buffer_aux, self.entry.type,
                                    is_initialized=not self.lhs_of_first_assignment,
                                    pos=self.pos, code=code)
        code.putln("%s = 0;" % rhstmp)
        code.funcstate.release_temp(rhstmp)
    
    def generate_deletion_code(self, code):
        if self.entry is None:
            return # There was an error earlier
        if not self.entry.is_pyglobal:
            error(self.pos, "Deletion of local or C global name not supported")
            return
        code.put_error_if_neg(self.pos, 
            'PyObject_DelAttrString(%s, "%s")' % (
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
    
    subexprs = ['arg']
    
    def analyse_types(self, env):
        self.arg.analyse_types(env)
        self.arg = self.arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Backquote expression"

    def generate_result_code(self, code):
        code.putln(
            "%s = PyObject_Repr(%s); %s" % (
                self.result(),
                self.arg.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))


class ImportNode(ExprNode):
    #  Used as part of import statement implementation.
    #  Implements result = 
    #    __import__(module_name, globals(), None, name_list)
    #
    #  module_name   IdentifierStringNode     dotted name of module
    #  name_list     ListNode or None         list of names to be imported
    
    subexprs = ['module_name', 'name_list']

    def analyse_types(self, env):
        self.module_name.analyse_types(env)
        self.module_name = self.module_name.coerce_to_pyobject(env)
        if self.name_list:
            self.name_list.analyse_types(env)
            self.name_list.coerce_to_pyobject(env)
        self.type = py_object_type
        self.gil_check(env)
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


class IteratorNode(ExprNode):
    #  Used as part of for statement implementation.
    #  Implements result = iter(sequence)
    #
    #  sequence   ExprNode
    
    subexprs = ['sequence']
    
    def analyse_types(self, env):
        self.sequence.analyse_types(env)
        self.sequence = self.sequence.coerce_to_pyobject(env)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1
        
        self.counter = TempNode(self.pos, PyrexTypes.c_py_ssize_t_type, env)
        self.counter.allocate_temp(env)

    gil_message = "Iterating over Python object"

    def release_temp(self, env):
        env.release_temp(self.result())
        self.counter.release_temp(env)
    
    def generate_result_code(self, code):
        code.putln(
            "if (PyList_CheckExact(%s) || PyTuple_CheckExact(%s)) {" % (
                self.sequence.py_result(),
                self.sequence.py_result()))
        code.putln(
            "%s = 0; %s = %s; Py_INCREF(%s);" % (
                self.counter.result(),
                self.result(),
                self.sequence.py_result(),
                self.result()))
        code.putln("} else {")
        code.putln("%s = -1; %s = PyObject_GetIter(%s); %s" % (
                self.counter.result(),
                self.result(),
                self.sequence.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.putln("}")


class NextNode(AtomicExprNode):
    #  Used as part of for statement implementation.
    #  Implements result = iterator.next()
    #  Created during analyse_types phase.
    #  The iterator is not owned by this node.
    #
    #  iterator   ExprNode
    
    def __init__(self, iterator, env):
        self.pos = iterator.pos
        self.iterator = iterator
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_result_code(self, code):
        for py_type in ["List", "Tuple"]:
            code.putln(
                "if (likely(Py%s_CheckExact(%s))) {" % (py_type, self.iterator.py_result()))
            code.putln(
                "if (%s >= Py%s_GET_SIZE(%s)) break;" % (
                    self.iterator.counter.result(),
                    py_type,
                    self.iterator.py_result()))
            code.putln(
                "%s = Py%s_GET_ITEM(%s, %s); Py_INCREF(%s); %s++;" % (
                    self.result(),
                    py_type,
                    self.iterator.py_result(),
                    self.iterator.counter.result(),
                    self.result(),
                    self.iterator.counter.result()))
            code.put("} else ")
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
        code.putln("}")


class ExcValueNode(AtomicExprNode):
    #  Node created during analyse_types phase
    #  of an ExceptClauseNode to fetch the current
    #  exception value.
    
    def __init__(self, pos, env, var):
        ExprNode.__init__(self, pos)
        self.type = py_object_type
        self.var = var
    
    def calculate_result_code(self):
        return self.var

    def generate_result_code(self, code):
        pass

    def analyse_types(self, env):
        pass


class TempNode(AtomicExprNode):
    #  Node created during analyse_types phase
    #  of some nodes to hold a temporary value.
    
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


class PyTempNode(TempNode):
    #  TempNode holding a Python value.
    
    def __init__(self, pos, env):
        TempNode.__init__(self, pos, PyrexTypes.py_object_type, env)


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
        # Handle the case where base is a literal char* (and we expect a string, not an int)
        if isinstance(self.base, StringNode):
            self.base = self.base.coerce_to_pyobject(env)

        skip_child_analysis = False
        buffer_access = False
        if self.base.type.is_buffer:
            assert hasattr(self.base, "entry") # Must be a NameNode-like node
            if self.indices:
                indices = self.indices
            else:
                # On cloning, indices is cloned. Otherwise, unpack index into indices
                assert not isinstance(self.index, CloneNode)
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
                if self.index.type.is_int and not self.index.type.is_longlong:
                    self.index = self.index.coerce_to(PyrexTypes.c_py_ssize_t_type, env).coerce_to_simple(env)
                else:
                    self.index = self.index.coerce_to_pyobject(env)
                self.type = py_object_type
                self.gil_check(env)
                self.is_temp = 1
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

    def check_const_addr(self):
        self.base.check_const_addr()
        self.index.check_const()
    
    def is_lvalue(self):
        return 1

    def calculate_result_code(self):
        if self.is_buffer_access:
            return "(*%s)" % self.buffer_ptr_code
        else:
            return "(%s[%s])" % (
                self.base.result(), self.index.result())
            
    def index_unsigned_parameter(self):
        if self.index.type.is_int:
            if self.original_index_type.signed:
                return ", 0"
            else:
                return ", sizeof(Py_ssize_t) <= sizeof(%s)" % self.original_index_type.declaration_code("")
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

    def generate_result_code(self, code):
        if self.is_buffer_access:
            if code.globalstate.directives['nonecheck']:
                self.put_nonecheck(code)
            self.buffer_ptr_code = self.buffer_lookup_code(code)
            if self.type.is_pyobject:
                # is_temp is True, so must pull out value and incref it.
                code.putln("%s = *%s;" % (self.result(), self.buffer_ptr_code))
                code.putln("Py_INCREF((PyObject*)%s);" % self.result())
        elif self.type.is_pyobject:
            if self.index.type.is_int:
                function = "__Pyx_GetItemInt"
                index_code = self.index.result()
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
                    self.index_unsigned_parameter(),
                    self.result(),
                    code.error_goto(self.pos)))

    def generate_setitem_code(self, value_code, code):
        if self.index.type.is_int:
            function = "__Pyx_SetItemInt"
            index_code = self.index.result()
            code.globalstate.use_utility_code(setitem_int_utility_code)
        else:
            function = "PyObject_SetItem"
            index_code = self.index.py_result()
        code.putln(
            "if (%s(%s, %s, %s%s) < 0) %s" % (
                function,
                self.base.py_result(),
                index_code,
                value_code,
                self.index_unsigned_parameter(),
                code.error_goto(self.pos)))

    def generate_buffer_setitem_code(self, rhs, code, op=""):
        # Used from generate_assignment_code and InPlaceAssignmentNode
        if code.globalstate.directives['nonecheck']:
            self.put_nonecheck(code)
        ptrexpr = self.buffer_lookup_code(code)
        if self.buffer_type.dtype.is_pyobject:
            # Must manage refcounts. Decref what is already there
            # and incref what we put in.
            ptr = code.funcstate.allocate_temp(self.buffer_type.buffer_ptr_type)
            if rhs.is_temp:
                rhs_code = code.funcstate.allocate_temp(rhs.type)
            else:
                rhs_code = rhs.result()
            code.putln("%s = %s;" % (ptr, ptrexpr))
            code.putln("Py_DECREF(*%s); Py_INCREF(%s);" % (
                ptr, rhs_code
                ))
            code.putln("*%s %s= %s;" % (ptr, op, rhs_code))
            if rhs.is_temp:
                code.funcstate.release_temp(rhs_code)
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
        rhs.generate_disposal_code(code)
    
    def generate_deletion_code(self, code):
        self.generate_subexpr_evaluation_code(code)
        #if self.type.is_pyobject:
        if self.index.type.is_int:
            function = "__Pyx_DelItemInt"
            index_code = self.index.result()
            code.globalstate.use_utility_code(delitem_int_utility_code)
        else:
            function = "PyObject_DelItem"
            index_code = self.index.py_result()
        code.putln(
            "if (%s(%s, %s%s) < 0) %s" % (
                function,
                self.base.py_result(),
                index_code,
                self.index_unsigned_parameter(),
                code.error_goto(self.pos)))
        self.generate_subexpr_disposal_code(code)

    def buffer_lookup_code(self, code):
        # Assign indices to temps
        index_temps = [code.funcstate.allocate_temp(i.type) for i in self.indices]
        for temp, index in zip(index_temps, self.indices):
            code.putln("%s = %s;" % (temp, index.result()))
        # Generate buffer access code using these temps
        import Buffer
        # The above could happen because child_attrs is wrong somewhere so that
        # options are not propagated.
        return Buffer.put_buffer_lookup_code(entry=self.base.entry,
                                             index_signeds=[i.type.signed for i in self.indices],
                                             index_cnames=index_temps,
                                             options=code.globalstate.directives,
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

    def analyse_types(self, env):
        self.base.analyse_types(env)
        if self.start:
            self.start.analyse_types(env)
        if self.stop:
            self.stop.analyse_types(env)
        self.base = self.base.coerce_to_pyobject(env)
        c_int = PyrexTypes.c_py_ssize_t_type
        if self.start:
            self.start = self.start.coerce_to(c_int, env)
        if self.stop:
            self.stop = self.stop.coerce_to(c_int, env)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Slicing Python object"

    def generate_result_code(self, code):
        code.putln(
            "%s = PySequence_GetSlice(%s, %s, %s); %s" % (
                self.result(),
                self.base.py_result(),
                self.start_code(),
                self.stop_code(),
                code.error_goto_if_null(self.result(), self.pos)))
    
    def generate_assignment_code(self, rhs, code):
        self.generate_subexpr_evaluation_code(code)
        code.put_error_if_neg(self.pos, 
            "PySequence_SetSlice(%s, %s, %s, %s)" % (
                self.base.py_result(),
                self.start_code(),
                self.stop_code(),
                rhs.result()))
        self.generate_subexpr_disposal_code(code)
        rhs.generate_disposal_code(code)

    def generate_deletion_code(self, code):
        self.generate_subexpr_evaluation_code(code)
        code.put_error_if_neg(self.pos,
            "PySequence_DelSlice(%s, %s, %s)" % (
                self.base.py_result(),
                self.start_code(),
                self.stop_code()))
        self.generate_subexpr_disposal_code(code)
    
    def start_code(self):
        if self.start:
            return self.start.result()
        else:
            return "0"
    
    def stop_code(self):
        if self.stop:
            return self.stop.result()
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
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Constructing Python slice object"

    def generate_result_code(self, code):
        code.putln(
            "%s = PySlice_New(%s, %s, %s); %s" % (
                self.result(),
                self.start.py_result(), 
                self.stop.py_result(), 
                self.step.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))


class CallNode(ExprNode):
    def gil_check(self, env):
        # Make sure we're not in a nogil environment
        if env.nogil:
            error(self.pos, "Calling gil-requiring function without gil")
    
    def analyse_as_type_constructor(self, env):
        type = self.function.analyse_as_type(env)
        if type and type.is_struct_or_union:
            args, kwds = self.explicit_args_kwds()
            items = []
            for arg, member in zip(args, type.scope.var_entries):
                items.append(DictItemNode(pos=arg.pos, key=IdentifierStringNode(pos=arg.pos, value=member.name), value=arg))
            if kwds:
                items += kwds.key_value_pairs
            self.key_value_pairs = items
            self.__class__ = DictNode
            self.analyse_types(env)
            self.coerce_to(type, env)
            return True


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
        if function.is_attribute and function.is_py_attr and \
           function.attribute == "append" and len(self.args) == 1:
            # L.append(x) is almost always applied to a list
            self.py_func = self.function
            self.function = NameNode(pos=self.function.pos, name="__Pyx_PyObject_Append")
            self.function.analyse_types(env)
            self.self = self.py_func.obj
            function.obj = CloneNode(self.self)
            env.use_utility_code(append_utility_code)
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
            self.type = py_object_type
            self.gil_check(env)
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
            self.opt_arg_struct = env.allocate_temp(func_type.op_arg_struct.base_type)
            env.release_temp(self.opt_arg_struct)
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
        if self.type.is_pyobject \
            or func_type.exception_value is not None \
            or func_type.exception_check:
                self.is_temp = 1
                if self.type.is_pyobject:
                    self.result_ctype = py_object_type
        # C++ exception handler
        if func_type.exception_check == '+':
            if func_type.exception_value is None:
                env.use_utility_code(cpp_exception_utility_code)
        # Check gil
        if not func_type.nogil:
            self.gil_check(env)

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
            join(arg_list_code, ", "))
#        if self.wrapper_call or \
#                self.function.entry.is_unbound_cmethod and self.function.entry.type.is_overridable:
#            result = "(%s = 1, %s)" % (Naming.skip_dispatch_cname, result)
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
        elif func_type.is_cfunction:
            if self.has_optional_args:
                actual_nargs = len(self.args)
                expected_nargs = len(func_type.args) - func_type.optional_arg_count
                code.putln("%s.%s = %s;" % (
                        self.opt_arg_struct,
                        Naming.pyrex_prefix + "n",
                        len(self.args) - expected_nargs))
                args = zip(func_type.args, self.args)
                for formal_arg, actual_arg in args[expected_nargs:actual_nargs]:
                    code.putln("%s.%s = %s;" % (
                            self.opt_arg_struct,
                            formal_arg.name,
                            actual_arg.result_as(formal_arg.type)))
            exc_checks = []
            if self.type.is_pyobject:
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
                        #	"from", return_type, "to pyobject" ###
                        rhs = typecast(py_object_type, self.type, rhs)
                else:
                    lhs = ""
                if func_type.exception_check == '+':
                    if func_type.exception_value is None:
                        raise_py_exception = "__Pyx_CppExn2PyErr()"
                    elif func_type.exception_value.type.is_pyobject:
                        raise_py_exception = 'PyErr_SetString(%s, "")' % func_type.exception_value.entry.cname
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

class GeneralCallNode(CallNode):
    #  General Python function call, including keyword,
    #  * and ** arguments.
    #
    #  function         ExprNode
    #  positional_args  ExprNode          Tuple of positional arguments
    #  keyword_args     ExprNode or None  Dict of keyword arguments
    #  starstar_arg     ExprNode or None  Dict of extra keyword args
    
    subexprs = ['function', 'positional_args', 'keyword_args', 'starstar_arg']

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
        self.function = self.function.coerce_to_pyobject(env)
        self.positional_args = \
            self.positional_args.coerce_to_pyobject(env)
        if self.starstar_arg:
            self.starstar_arg = \
                self.starstar_arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1
        
    def generate_result_code(self, code):
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
        else:
            keyword_code = None
        if not keyword_code:
            call_code = "PyObject_Call(%s, %s, NULL)" % (
                self.function.py_result(),
                self.positional_args.py_result())
        else:
            call_code = "PyEval_CallObjectWithKeywords(%s, %s, %s)" % (
                self.function.py_result(),
                self.positional_args.py_result(),
                keyword_code)
        code.putln(
            "%s = %s; %s" % (
                self.result(),
                call_code,
                code.error_goto_if_null(self.result(), self.pos)))


class AsTupleNode(ExprNode):
    #  Convert argument to tuple. Used for normalising
    #  the * argument of a function call.
    #
    #  arg    ExprNode
    
    subexprs = ['arg']
    
    def compile_time_value(self, denv):
        arg = self.arg.compile_time_value(denv)
        try:
            return tuple(arg)
        except Exception, e:
            self.compile_time_value_error(e)

    def analyse_types(self, env):
        self.arg.analyse_types(env)
        self.arg = self.arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Constructing Python tuple"

    def generate_result_code(self, code):
        code.putln(
            "%s = PySequence_Tuple(%s); %s" % (
                self.result(),
                self.arg.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
    

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
    #  interned_attr_cname  string    C name of interned attribute name
    
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
    
    def compile_time_value(self, denv):
        attr = self.attribute
        if attr.beginswith("__") and attr.endswith("__"):
            self.error("Invalid attribute name '%s' in compile-time expression"
                % attr)
            return None
        obj = self.arg.compile_time_value(denv)
        try:
            return getattr(obj, attr)
        except Exception, e:
            self.compile_time_value_error(e)

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
        #	self.type = self.type.element_ptr_type()
        if self.is_py_attr:
            if not target:
                self.is_temp = 1
                self.result_ctype = py_object_type
    
    def analyse_attribute(self, env):
        # Look up attribute and set self.type and self.member.
        self.is_py_attr = 0
        self.member = self.attribute
        if self.obj.type.is_string:
            self.obj = self.obj.coerce_to_pyobject(env)
        obj_type = self.obj.type
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
        self.analyse_as_python_attribute(env)
                    
    def analyse_as_python_attribute(self, env):
        obj_type = self.obj.type
        self.member = self.attribute
        if obj_type.is_pyobject:
            self.type = py_object_type
            self.is_py_attr = 1
            self.interned_attr_cname = env.intern_identifier(self.attribute)
            self.gil_check(env)
        else:
            if not obj_type.is_error:
                error(self.pos, 
                    "Object of type '%s' has no attribute '%s'" %
                    (obj_type, self.attribute))

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
        else:
            return "%s%s%s" % (obj_code, self.op, self.member)
    
    def generate_result_code(self, code):
        if self.is_py_attr:
            code.putln(
                '%s = PyObject_GetAttr(%s, %s); %s' % (
                    self.result(),
                    self.obj.py_result(),
                    self.interned_attr_cname,
                    code.error_goto_if_null(self.result(), self.pos)))
        else:
            # result_code contains what is needed, but we may need to insert
            # a check and raise an exception
            if (self.obj.type.is_extension_type
                  and self.needs_none_check
                  and code.globalstate.directives['nonecheck']):
                self.put_nonecheck(code)
    
    def generate_assignment_code(self, rhs, code):
        self.obj.generate_evaluation_code(code)
        if self.is_py_attr:
            code.put_error_if_neg(self.pos, 
                'PyObject_SetAttr(%s, %s, %s)' % (
                    self.obj.py_result(),
                    self.interned_attr_cname,
                    rhs.py_result()))
            rhs.generate_disposal_code(code)
        else:
            if (self.obj.type.is_extension_type
                  and self.needs_none_check
                  and code.globalstate.directives['nonecheck']):
                self.put_nonecheck(code)

            select_code = self.result()
            if self.type.is_pyobject:
                rhs.make_owned_reference(code)
                code.put_decref(select_code, self.ctype())
            code.putln(
                "%s = %s;" % (
                    select_code,
                    rhs.result_as(self.ctype())))
                    #rhs.result()))
            rhs.generate_post_assignment_code(code)
        self.obj.generate_disposal_code(code)
    
    def generate_deletion_code(self, code):
        self.obj.generate_evaluation_code(code)
        if self.is_py_attr:
            code.put_error_if_neg(self.pos,
                'PyObject_DelAttr(%s, %s)' % (
                    self.obj.py_result(),
                    self.interned_attr_cname))
        else:
            error(self.pos, "Cannot delete C attribute of extension type")
        self.obj.generate_disposal_code(code)
        
    def annotate(self, code):
        if self.is_py_attr:
            code.annotate(self.pos, AnnotationItem('py_attr', 'python attribute', size=len(self.attribute)))
        else:
            code.annotate(self.pos, AnnotationItem('c_attr', 'c attribute', size=len(self.attribute)))

    def put_nonecheck(self, code):
        code.globalstate.use_utility_code(raise_noneattr_error_utility_code)
        code.putln("if (%s) {" % code.unlikely("%s == Py_None") % self.obj.result_as(PyrexTypes.py_object_type))
        code.putln("__Pyx_RaiseNoneAttributeError(\"%s\");" % self.attribute.encode("UTF-8")) # todo: fix encoding
        code.putln(code.error_goto(self.pos))
        code.putln("}")


#-------------------------------------------------------------------
#
#  Constructor nodes
#
#-------------------------------------------------------------------

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

    def analyse_target_declaration(self, env):
        for arg in self.args:
            arg.analyse_target_declaration(env)

    def analyse_types(self, env, skip_children=False):
        for i in range(len(self.args)):
            arg = self.args[i]
            if not skip_children: arg.analyse_types(env)
            self.args[i] = arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    def analyse_target_types(self, env):
        self.iterator = PyTempNode(self.pos, env)
        self.unpacked_items = []
        self.coerced_unpacked_items = []
        for arg in self.args:
            arg.analyse_target_types(env)
            unpacked_item = PyTempNode(self.pos, env)
            coerced_unpacked_item = unpacked_item.coerce_to(arg.type, env)
            self.unpacked_items.append(unpacked_item)
            self.coerced_unpacked_items.append(coerced_unpacked_item)
        self.type = py_object_type
        env.use_utility_code(unpacking_utility_code)
    
    def allocate_target_temps(self, env, rhs):
        self.iterator.allocate_temps(env)
        for arg, node in zip(self.args, self.coerced_unpacked_items):
            node.allocate_temps(env)
            arg.allocate_target_temps(env, node)
            #arg.release_target_temp(env)
            #node.release_temp(env)
        if rhs:
            rhs.release_temp(env)
        self.iterator.release_temp(env)
    
#	def release_target_temp(self, env):
#		#for arg in self.args:
#		#	arg.release_target_temp(env)
#		#for node in self.coerced_unpacked_items:
#		#	node.release_temp(env)
#		self.iterator.release_temp(env)
    
    def generate_result_code(self, code):
        self.generate_operation_code(code)
    
    def generate_assignment_code(self, rhs, code):
        code.putln(
            "if (PyTuple_CheckExact(%s) && PyTuple_GET_SIZE(%s) == %s) {" % (
                rhs.py_result(), 
                rhs.py_result(), 
                len(self.args)))
        code.putln("PyObject* tuple = %s;" % rhs.py_result())
        for i in range(len(self.args)):
            item = self.unpacked_items[i]
            code.putln(
                "%s = PyTuple_GET_ITEM(tuple, %s);" % (
                    item.result(),
                    i))
            code.put_incref(item.result(), item.ctype())
            value_node = self.coerced_unpacked_items[i]
            value_node.generate_evaluation_code(code)
            self.args[i].generate_assignment_code(value_node, code)
            
        rhs.generate_disposal_code(code)
        code.putln("}")
        code.putln("else {")

        code.putln(
            "%s = PyObject_GetIter(%s); %s" % (
                self.iterator.result(),
                rhs.py_result(),
                code.error_goto_if_null(self.iterator.result(), self.pos)))
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
            value_node = self.coerced_unpacked_items[i]
            value_node.generate_evaluation_code(code)
            self.args[i].generate_assignment_code(value_node, code)
        code.put_error_if_neg(self.pos, 
            "__Pyx_EndUnpack(%s)" % (
                self.iterator.py_result()))
        if debug_disposal_code:
            print("UnpackNode.generate_assignment_code:")
            print("...generating disposal code for %s" % self.iterator)
        self.iterator.generate_disposal_code(code)

        code.putln("}")
        
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

    gil_message = "Constructing Python tuple"

    def analyse_types(self, env, skip_children=False):
        if len(self.args) == 0:
            self.is_temp = 0
            self.is_literal = 1
        else:
            SequenceNode.analyse_types(self, env, skip_children)
        self.type = tuple_type
            
    def calculate_result_code(self):
        if len(self.args) > 0:
            error(self.pos, "Positive length tuples must be constructed.")
        else:
            return Naming.empty_tuple

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
        for i in range(len(self.args)):
            arg = self.args[i]
            if not arg.result_in_temp():
                code.put_incref(arg.result(), arg.ctype())
            code.putln(
                "PyTuple_SET_ITEM(%s, %s, %s);" % (
                    self.result(),
                    i,
                    arg.py_result()))
    
    def generate_subexpr_disposal_code(self, code):
        # We call generate_post_assignment_code here instead
        # of generate_disposal_code, because values were stored
        # in the tuple using a reference-stealing operation.
        for arg in self.args:
            arg.generate_post_assignment_code(code)	


class ListNode(SequenceNode):
    #  List constructor.
    
    # obj_conversion_errors    [PyrexError]   used internally
    # orignial_args            [ExprNode]     used internally

    gil_message = "Constructing Python list"

    def analyse_expressions(self, env):
        ExprNode.analyse_expressions(self, env)
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
            for i in range(len(self.args)):
                arg = self.args[i]
                #if not arg.is_temp:
                if not arg.result_in_temp():
                    code.put_incref(arg.result(), arg.ctype())
                code.putln("PyList_SET_ITEM(%s, %s, %s);" %
                    (self.result(),
                    i,
                    arg.py_result()))
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

            
class ListComprehensionNode(SequenceNode):

    subexprs = []
    is_sequence_constructor = 0 # not unpackable

    child_attrs = ["loop", "append"]

    def analyse_types(self, env): 
        self.type = list_type
        self.is_temp = 1
        self.append.target = self # this is a CloneNode used in the PyList_Append in the inner loop
        
    def allocate_temps(self, env, result = None): 
        if debug_temp_alloc:
            print("%s Allocating temps" % self)
        self.allocate_temp(env, result)
        self.loop.analyse_declarations(env)
        self.loop.analyse_expressions(env)
        
    def generate_operation_code(self, code):
        code.putln("%s = PyList_New(%s); %s" %
            (self.result(),
            0,
            code.error_goto_if_null(self.result(), self.pos)))
        self.loop.generate_execution_code(code)
        
    def annotate(self, code):
        self.loop.annotate(code)


class ListComprehensionAppendNode(ExprNode):

    # Need to be careful to avoid infinite recursion:
    # target must not be in child_attrs/subexprs
    subexprs = ['expr']
    
    def analyse_types(self, env):
        self.expr.analyse_types(env)
        if self.expr.type != py_object_type:
            self.expr = self.expr.coerce_to_pyobject(env)
        self.type = PyrexTypes.c_int_type
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln("%s = PyList_Append(%s, (PyObject*)%s); %s" %
            (self.result(),
            self.target.result(),
            self.expr.result(),
            code.error_goto_if(self.result(), self.pos)))


class DictNode(ExprNode):
    #  Dictionary constructor.
    #
    #  key_value_pairs  [DictItemNode]
    #
    # obj_conversion_errors    [PyrexError]   used internally
    
    subexprs = ['key_value_pairs']
    
    def compile_time_value(self, denv):
        pairs = [(item.key.compile_time_value(denv), item.value.compile_time_value(denv))
            for item in self.key_value_pairs]
        try:
            return dict(pairs)
        except Exception, e:
            self.compile_time_value_error(e)
    
    def analyse_types(self, env):
        hold_errors()
        self.type = dict_type
        for item in self.key_value_pairs:
            item.analyse_types(env)
        self.gil_check(env)
        self.obj_conversion_errors = held_errors()
        release_errors(ignore=True)
        self.is_temp = 1
        
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
                if not isinstance(item.key, (StringNode, IdentifierStringNode)):
                    error(item.key.pos, "Invalid struct field identifier")
                    item.key = IdentifierStringNode(item.key.pos, value="<error>")
                else:
                    member = dst_type.scope.lookup_here(item.key.value)
                    if not member:
                        error(item.key.pos, "struct '%s' has no field '%s'" % (dst_type, item.key.value))
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

    def allocate_temps(self, env, result = None):
        #  Custom method used here because key-value
        #  pairs are evaluated and used one at a time.
        self.allocate_temp(env, result)
        for item in self.key_value_pairs:
            item.key.allocate_temps(env)
            item.value.allocate_temps(env)
            item.key.release_temp(env)
            item.value.release_temp(env)
    
    def generate_evaluation_code(self, code):
        #  Custom method used here because key-value
        #  pairs are evaluated and used one at a time.
        if self.type.is_pyobject:
            self.release_errors()
            code.putln(
                "%s = PyDict_New(); %s" % (
                    self.result(),
                    code.error_goto_if_null(self.result(), self.pos)))
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
            
    def annotate(self, code):
        for item in self.key_value_pairs:
            item.annotate(code)
            
class DictItemNode(ExprNode):
    # Represents a single item in a DictNode
    #
    # key          ExprNode
    # value        ExprNode
    subexprs = ['key', 'value']
            
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
        
    def __iter__(self):
        return iter([self.key, self.value])


class ClassNode(ExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a class object given
    #  a name, tuple of bases and class dictionary.
    #
    #  name         EncodedString      Name of the class
    #  cname        string             Class name as a Python string
    #  bases        ExprNode           Base class tuple
    #  dict         ExprNode           Class dict (not owned by this node)
    #  doc          ExprNode or None   Doc string
    #  module_name  string             Name of defining module
    
    subexprs = ['bases', 'doc']

    def analyse_types(self, env):
        self.cname = env.intern_identifier(self.name)
        self.bases.analyse_types(env)
        if self.doc:
            self.doc.analyse_types(env)
            self.doc = self.doc.coerce_to_pyobject(env)
        self.module_name = env.global_scope().qualified_name
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1
        env.use_utility_code(create_class_utility_code);

    gil_message = "Constructing Python class"

    def generate_result_code(self, code):
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
                self.cname,
                self.module_name,
                code.error_goto_if_null(self.result(), self.pos)))


class UnboundMethodNode(ExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs an unbound method
    #  object from a class and a function.
    #
    #  class_cname   string     C var holding the class object
    #  function      ExprNode   Function object
    
    subexprs = ['function']
    
    def analyse_types(self, env):
        self.function.analyse_types(env)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Constructing an unbound method"

    def generate_result_code(self, code):
        code.putln(
            "%s = PyMethod_New(%s, 0, %s); %s" % (
                self.result(),
                self.function.py_result(),
                self.class_cname,
                code.error_goto_if_null(self.result(), self.pos)))


class PyCFunctionNode(AtomicExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a PyCFunction object
    #  from a PyMethodDef struct.
    #
    #  pymethdef_cname   string   PyMethodDef structure
    
    def analyse_types(self, env):
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1

    gil_message = "Constructing Python function"

    def generate_result_code(self, code):
        code.putln(
            "%s = PyCFunction_New(&%s, 0); %s" % (
                self.result(),
                self.pymethdef_cname,
                code.error_goto_if_null(self.result(), self.pos)))

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

    def analyse_types(self, env):
        self.operand.analyse_types(env)
        if self.is_py_operation():
            self.coerce_operand_to_pyobject(env)
            self.type = py_object_type
            self.gil_check(env)
            self.is_temp = 1
        else:
            self.analyse_c_operation(env)
    
    def check_const(self):
        self.operand.check_const()
    
    def is_py_operation(self):
        return self.operand.type.is_pyobject
    
    def coerce_operand_to_pyobject(self, env):
        self.operand = self.operand.coerce_to_pyobject(env)
    
    def generate_result_code(self, code):
        if self.operand.type.is_pyobject:
            self.generate_py_operation_code(code)
        else:
            if self.is_temp:
                self.generate_c_operation_code(code)
    
    def generate_py_operation_code(self, code):
        function = self.py_operation_function()
        code.putln(
            "%s = %s(%s); %s" % (
                self.result(), 
                function, 
                self.operand.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        
    def type_error(self):
        if not self.operand.type.is_error:
            error(self.pos, "Invalid operand type for '%s' (%s)" %
                (self.operator, self.operand.type))
        self.type = PyrexTypes.error_type


class NotNode(ExprNode):
    #  'not' operator
    #
    #  operand   ExprNode
    
    def compile_time_value(self, denv):
        operand = self.operand.compile_time_value(denv)
        try:
            return not operand
        except Exception, e:
            self.compile_time_value_error(e)

    subexprs = ['operand']
    
    def analyse_types(self, env):
        self.operand.analyse_types(env)
        self.operand = self.operand.coerce_to_boolean(env)
        self.type = PyrexTypes.c_bint_type
    
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
    
    def py_operation_function(self):
        return "PyNumber_Negative"
    
    def calculate_result_code(self):
        return "(-%s)" % self.operand.result()


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
        self.operand.check_const_addr()
    
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
            if (self.operand.type.to_py_function and
                    self.operand.type.create_convert_utility_code(env)):
                self.result_ctype = py_object_type
                self.operand = self.operand.coerce_to_pyobject(env)
            else:
                warning(self.pos, "No conversion from %s to %s, python object pointer used." % (self.operand.type, self.type))
                self.operand = self.operand.coerce_to_simple(env)
        elif from_py and not to_py:
            if self.type.from_py_function:
                self.operand = self.operand.coerce_to(self.type, env)
            else:
                warning(self.pos, "No conversion from %s to %s, python object pointer used." % (self.type, self.operand.type))
        elif from_py and to_py:
            if self.typecheck and self.type.is_extension_type:
                self.operand = PyTypeTestNode(self.operand, self.type, env)
    
    def check_const(self):
        self.operand.check_const()
    
    def calculate_result_code(self):
        opnd = self.operand
        return self.type.cast_code(opnd.result())
    
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
    
    type = PyrexTypes.c_int_type

    def check_const(self):
        pass

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
    '/': operator.div,
    '//': operator.floordiv,
    '<<': operator.lshift,
    '%': operator.mod,
    '*': operator.mul,
    '|': operator.or_,
    '**': operator.pow,
    '>>': operator.rshift,
    '-': operator.sub,
    #'/': operator.truediv,
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

class BinopNode(NewTempExprNode):
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
    
    def compile_time_value(self, denv):
        func = get_compile_time_binop(self)
        operand1 = self.operand1.compile_time_value(denv)
        operand2 = self.operand2.compile_time_value(denv)
        try:
            return func(operand1, operand2)
        except Exception, e:
            self.compile_time_value_error(e)

    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        if self.is_py_operation():
            self.coerce_operands_to_pyobjects(env)
            self.type = py_object_type
            self.gil_check(env)
            self.is_temp = 1
            if Options.incref_local_binop and self.operand1.type.is_pyobject:
                self.operand1 = self.operand1.coerce_to_temp(env)
        else:
            self.analyse_c_operation(env)
    
    def is_py_operation(self):
        return (self.operand1.type.is_pyobject 
            or self.operand2.type.is_pyobject)
    
    def coerce_operands_to_pyobjects(self, env):
        self.operand1 = self.operand1.coerce_to_pyobject(env)
        self.operand2 = self.operand2.coerce_to_pyobject(env)
    
    def check_const(self):
        self.operand1.check_const()
        self.operand2.check_const()
    
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
        else:
            if self.is_temp:
                self.generate_c_operation_code(code)
    
    def type_error(self):
        if not (self.operand1.type.is_error
                or self.operand2.type.is_error):
            error(self.pos, "Invalid operand types for '%s' (%s; %s)" %
                (self.operator, self.operand1.type, 
                    self.operand2.type))
        self.type = PyrexTypes.error_type


class NumBinopNode(BinopNode):
    #  Binary operation taking numeric arguments.
    
    def analyse_c_operation(self, env):
        type1 = self.operand1.type
        type2 = self.operand2.type
        if self.operator == "**" and type1.is_int and type2.is_int:
            error(self.pos, "** with two C int types is ambiguous")
            self.type = error_type
            return
        self.type = self.compute_c_result_type(type1, type2)
        if not self.type:
            self.type_error()
    
    def compute_c_result_type(self, type1, type2):
        if self.c_types_okay(type1, type2):
            return PyrexTypes.widest_numeric_type(type1, type2)
        else:
            return None
    
    def c_types_okay(self, type1, type2):
        #print "NumBinopNode.c_types_okay:", type1, type2 ###
        return (type1.is_numeric  or type1.is_enum) \
            and (type2.is_numeric  or type2.is_enum)

    def calculate_result_code(self):
        return "(%s %s %s)" % (
            self.operand1.result(), 
            self.operator, 
            self.operand2.result())
    
    def py_operation_function(self):
        return self.py_functions[self.operator]

    py_functions = {
        "|":		"PyNumber_Or",
        "^":		"PyNumber_Xor",
        "&":		"PyNumber_And",
        "<<":		"PyNumber_Lshift",
        ">>":		"PyNumber_Rshift",
        "+":		"PyNumber_Add",
        "-":		"PyNumber_Subtract",
        "*":		"PyNumber_Multiply",
        "/":		"__Pyx_PyNumber_Divide",
        "//":		"PyNumber_FloorDivide",
        "%":		"PyNumber_Remainder",
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
    
    def is_py_operation(self):
        if self.operand1.type.is_string \
            and self.operand2.type.is_string:
                return 1
        else:
            return NumBinopNode.is_py_operation(self)

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
    
    def is_py_operation(self):
        type1 = self.operand1.type
        type2 = self.operand2.type
        if (type1.is_string and type2.is_int) \
            or (type2.is_string and type1.is_int):
                return 1
        else:
            return NumBinopNode.is_py_operation(self)


class FloorDivNode(NumBinopNode):
    #  '//' operator.
    
    def calculate_result_code(self):
        return "(%s %s %s)" % (
            self.operand1.result(), 
            "/",  # c division is by default floor-div 
            self.operand2.result())


class ModNode(NumBinopNode):
    #  '%' operator.
    
    def is_py_operation(self):
        return (self.operand1.type.is_string
            or self.operand2.type.is_string
            or NumBinopNode.is_py_operation(self))

    def calculate_result_code(self):
        if self.operand1.type.is_float or self.operand2.type.is_float:
            return "fmod(%s, %s)" % (
                self.operand1.result(), 
                self.operand2.result())
        else:
            return "(%s %% %s)" % (
                self.operand1.result(), 
                self.operand2.result())

class PowNode(NumBinopNode):
    #  '**' operator.

    def compute_c_result_type(self, type1, type2):
        if self.c_types_okay(type1, type2):
            return PyrexTypes.c_double_type
        else:
            return None

    def c_types_okay(self, type1, type2):
        return (type1.is_float or type2.is_float) and \
                NumBinopNode.c_types_okay(self, type1, type2)

    def type_error(self):
        if not (self.operand1.type.is_error or self.operand2.type.is_error):
            if self.operand1.type.is_int and self.operand2.type.is_int:
                error(self.pos, "C has no integer powering, use python ints or floats instead '%s' (%s; %s)" %
                    (self.operator, self.operand1.type, self.operand2.type))
            else:
                NumBinopNode.type_error(self)
        self.type = PyrexTypes.error_type

    def calculate_result_code(self):
        return "pow(%s, %s)" % (
            self.operand1.result(), self.operand2.result())


class BoolBinopNode(ExprNode):
    #  Short-circuiting boolean operation.
    #
    #  operator     string
    #  operand1     ExprNode
    #  operand2     ExprNode
    #  temp_bool    ExprNode     used internally
    
    temp_bool = None
    
    subexprs = ['operand1', 'operand2', 'temp_bool']
    
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
        if self.operand1.type.is_pyobject or \
                self.operand2.type.is_pyobject:
            self.operand1 = self.operand1.coerce_to_pyobject(env)
            self.operand2 = self.operand2.coerce_to_pyobject(env)
            self.temp_bool = TempNode(self.pos, PyrexTypes.c_bint_type, env)
            self.type = py_object_type
            self.gil_check(env)
        else:
            self.operand1 = self.operand1.coerce_to_boolean(env)
            self.operand2 = self.operand2.coerce_to_boolean(env)
            self.type = PyrexTypes.c_bint_type
        # For what we're about to do, it's vital that
        # both operands be temp nodes.
        self.operand1 = self.operand1.coerce_to_temp(env) #CTT
        self.operand2 = self.operand2.coerce_to_temp(env)
        self.is_temp = 1

    gil_message = "Truth-testing Python object"

    def allocate_temps(self, env, result_code = None):
        #  We don't need both operands at the same time, and
        #  one of the operands will also be our result. So we
        #  use an allocation strategy here which results in
        #  this node and both its operands sharing the same
        #  result variable. This allows us to avoid some 
        #  assignments and increfs/decrefs that would otherwise
        #  be necessary.
        self.allocate_temp(env, result_code)
        self.operand1.allocate_temps(env, self.result())
        if self.temp_bool:
            self.temp_bool.allocate_temp(env)
            self.temp_bool.release_temp(env)
        self.operand2.allocate_temps(env, self.result())
        #  We haven't called release_temp on either operand,
        #  because although they are temp nodes, they don't own 
        #  their result variable. And because they are temp
        #  nodes, any temps in their subnodes will have been
        #  released before their allocate_temps returned.
        #  Therefore, they contain no temp vars that need to
        #  be released.

    def check_const(self):
        self.operand1.check_const()
        self.operand2.check_const()
    
    def calculate_result_code(self):
        return "(%s %s %s)" % (
            self.operand1.result(),
            self.py_to_c_op[self.operator],
            self.operand2.result())
    
    py_to_c_op = {'and': "&&", 'or': "||"}

    def generate_evaluation_code(self, code):
        self.operand1.generate_evaluation_code(code)
        test_result = self.generate_operand1_test(code)
        if self.operator == 'and':
            sense = ""
        else:
            sense = "!"
        code.putln(
            "if (%s%s) {" % (
                sense,
                test_result))
        self.operand1.generate_disposal_code(code)
        self.operand2.generate_evaluation_code(code)
        code.putln(
            "}")
    
    def generate_operand1_test(self, code):
        #  Generate code to test the truth of the first operand.
        if self.type.is_pyobject:
            test_result = self.temp_bool.result()
            code.putln(
                "%s = __Pyx_PyObject_IsTrue(%s); %s" % (
                    test_result,
                    self.operand1.py_result(),
                    code.error_goto_if_neg(test_result, self.pos)))
        else:
            test_result = self.operand1.result()
        return test_result


class CondExprNode(ExprNode):
    #  Short-circuiting conditional expression.
    #
    #  test        ExprNode
    #  true_val    ExprNode
    #  false_val   ExprNode
    
    temp_bool = None
    true_val = None
    false_val = None
    
    subexprs = ['test', 'true_val', 'false_val']
    
    def analyse_types(self, env):
        self.test.analyse_types(env)
        self.test = self.test.coerce_to_boolean(env)
        self.true_val.analyse_types(env)
        self.false_val.analyse_types(env)
        self.type = self.compute_result_type(self.true_val.type, self.false_val.type)
        if self.true_val.type.is_pyobject or self.false_val.type.is_pyobject:
            self.true_val = self.true_val.coerce_to(self.type, env)
            self.false_val = self.false_val.coerce_to(self.type, env)
        # must be tmp variables so they can share a result
        self.true_val = self.true_val.coerce_to_temp(env)
        self.false_val = self.false_val.coerce_to_temp(env)
        self.is_temp = 1
        if self.type == PyrexTypes.error_type:
            self.type_error()
    
    def allocate_temps(self, env, result_code = None):
        #  We only ever evaluate one side, and this is 
        #  after evaluating the truth value, so we may
        #  use an allocation strategy here which results in
        #  this node and both its operands sharing the same
        #  result variable. This allows us to avoid some 
        #  assignments and increfs/decrefs that would otherwise
        #  be necessary.
        self.allocate_temp(env, result_code)
        self.test.allocate_temps(env, result_code)
        self.true_val.allocate_temps(env, self.result())
        self.false_val.allocate_temps(env, self.result())
        #  We haven't called release_temp on either value,
        #  because although they are temp nodes, they don't own 
        #  their result variable. And because they are temp
        #  nodes, any temps in their subnodes will have been
        #  released before their allocate_temps returned.
        #  Therefore, they contain no temp vars that need to
        #  be released.
        
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
        self.test.check_const()
        self.true_val.check_const()
        self.false_val.check_const()
    
    def generate_evaluation_code(self, code):
        self.test.generate_evaluation_code(code)
        code.putln("if (%s) {" % self.test.result() )
        self.true_val.generate_evaluation_code(code)
        code.putln("} else {")
        self.false_val.generate_evaluation_code(code)
        code.putln("}")
        self.test.generate_disposal_code(code)

richcmp_constants = {
    "<" : "Py_LT",
    "<=": "Py_LE",
    "==": "Py_EQ",
    "!=": "Py_NE",
    "<>": "Py_NE",
    ">" : "Py_GT",
    ">=": "Py_GE",
}

class CmpNode:
    #  Mixin class containing code common to PrimaryCmpNodes
    #  and CascadedCmpNodes.
    
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
                result = result and cascade.compile_time_value(operand2, denv)
        return result

    def is_python_comparison(self):
        return (self.has_python_operands()
            or (self.cascade and self.cascade.is_python_comparison())
            or self.operator in ('in', 'not_in'))

    def is_python_result(self):
        return ((self.has_python_operands() and self.operator not in ('is', 'is_not', 'in', 'not_in'))
            or (self.cascade and self.cascade.is_python_result()))

    def check_types(self, env, operand1, op, operand2):
        if not self.types_okay(operand1, op, operand2):
            error(self.pos, "Invalid types for '%s' (%s, %s)" %
                (self.operator, operand1.type, operand2.type))
    
    def types_okay(self, operand1, op, operand2):
        type1 = operand1.type
        type2 = operand2.type
        if type1.is_error or type2.is_error:
            return 1
        if type1.is_pyobject: # type2 will be, too
            return 1
        elif type1.is_ptr or type1.is_array:
            return type1.is_null_ptr or type2.is_null_ptr \
                or ((type2.is_ptr or type2.is_array)
                    and type1.base_type.same_as(type2.base_type))
        elif ((type1.is_numeric and type2.is_numeric
                    or type1.is_enum and (type1 is type2 or type2.is_int)
                    or type1.is_int and type2.is_enum)
                and op not in ('is', 'is_not')):
            return 1
        else:
            return type1.is_cfunction and type1.is_cfunction and type1 == type2

    def generate_operation_code(self, code, result_code, 
            operand1, op , operand2):
        if self.type is PyrexTypes.py_object_type:
            coerce_result = "__Pyx_PyBool_FromLong"
        else:
            coerce_result = ""
        if 'not' in op: negation = "!"
        else: negation = ""
        if op == 'in' or op == 'not_in':
            code.putln(
                "%s = %s(%sPySequence_Contains(%s, %s)); %s" % (
                    result_code, 
                    coerce_result, 
                    negation,
                    operand2.py_result(), 
                    operand1.py_result(), 
                    code.error_goto_if_neg(result_code, self.pos)))
        elif (operand1.type.is_pyobject
            and op not in ('is', 'is_not')):
                code.putln("%s = PyObject_RichCompare(%s, %s, %s); %s" % (
                        result_code, 
                        operand1.py_result(), 
                        operand2.py_result(), 
                        richcmp_constants[op],
                        code.error_goto_if_null(result_code, self.pos)))
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
    
    def compile_time_value(self, denv):
        operand1 = self.operand1.compile_time_value(denv)
        return self.cascaded_compile_time_value(operand1, denv)

    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        if self.cascade:
            self.cascade.analyse_types(env, self.operand2)
        self.is_pycmp = self.is_python_comparison()
        if self.is_pycmp:
            self.coerce_operands_to_pyobjects(env)
        if self.has_int_operands():
            self.coerce_chars_to_ints(env)
        if self.cascade:
            self.operand2 = self.operand2.coerce_to_simple(env)
            self.cascade.coerce_cascaded_operands_to_temp(env)
        self.check_operand_types(env)
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
    
    def check_operand_types(self, env):
        self.check_types(env, 
            self.operand1, self.operator, self.operand2)
        if self.cascade:
            self.cascade.check_operand_types(env, self.operand2)
    
    def has_python_operands(self):
        return (self.operand1.type.is_pyobject
            or self.operand2.type.is_pyobject)
            
    def coerce_operands_to_pyobjects(self, env):
        self.operand1 = self.operand1.coerce_to_pyobject(env)
        self.operand2 = self.operand2.coerce_to_pyobject(env)
        if self.cascade:
            self.cascade.coerce_operands_to_pyobjects(env)
        
    def has_int_operands(self):
        return (self.operand1.type.is_int or self.operand2.type.is_int) \
           or (self.cascade and self.cascade.has_int_operands())
    
    def coerce_chars_to_ints(self, env):
        # coerce literal single-char strings to c chars
        if self.operand1.type.is_string and isinstance(self.operand1, StringNode):
            self.operand1 = self.operand1.coerce_to(PyrexTypes.c_uchar_type, env)
        if self.operand2.type.is_string and isinstance(self.operand2, StringNode):
            self.operand2 = self.operand2.coerce_to(PyrexTypes.c_uchar_type, env)
        if self.cascade:
            self.cascade.coerce_chars_to_ints(env)
    
    def allocate_subexpr_temps(self, env):
        self.operand1.allocate_temps(env)
        self.operand2.allocate_temps(env)
        if self.cascade:
            self.cascade.allocate_subexpr_temps(env)
    
    def release_subexpr_temps(self, env):
        self.operand1.release_temp(env)
        self.operand2.release_temp(env)
        if self.cascade:
            self.cascade.release_subexpr_temps(env)
    
    def check_const(self):
        self.operand1.check_const()
        self.operand2.check_const()
        if self.cascade:
            self.not_const()

    def calculate_result_code(self):
        return "(%s %s %s)" % (
            self.operand1.result(),
            self.c_operator(self.operator),
            self.operand2.result())
    
    def generate_evaluation_code(self, code):
        self.operand1.generate_evaluation_code(code)
        self.operand2.generate_evaluation_code(code)
        if self.is_temp:
            self.generate_operation_code(code, self.result(), 
                self.operand1, self.operator, self.operand2)
            if self.cascade:
                self.cascade.generate_evaluation_code(code,
                    self.result(), self.operand2)
            self.operand1.generate_disposal_code(code)
            self.operand2.generate_disposal_code(code)
    
    def generate_subexpr_disposal_code(self, code):
        #  If this is called, it is a non-cascaded cmp,
        #  so only need to dispose of the two main operands.
        self.operand1.generate_disposal_code(code)
        self.operand2.generate_disposal_code(code)
        
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
    
    def analyse_types(self, env, operand1):
        self.operand2.analyse_types(env)
        if self.cascade:
            self.cascade.analyse_types(env, self.operand2)
    
    def check_operand_types(self, env, operand1):
        self.check_types(env, 
            operand1, self.operator, self.operand2)
        if self.cascade:
            self.cascade.check_operand_types(env, self.operand2)
    
    def has_python_operands(self):
        return self.operand2.type.is_pyobject
        
    def coerce_operands_to_pyobjects(self, env):
        self.operand2 = self.operand2.coerce_to_pyobject(env)
        if self.cascade:
            self.cascade.coerce_operands_to_pyobjects(env)

    def has_int_operands(self):
        return self.operand2.type.is_int
        
    def coerce_chars_to_ints(self, env):
        if self.operand2.type.is_string and isinstance(self.operand2, StringNode):
            self.operand2 = self.operand2.coerce_to(PyrexTypes.c_uchar_type, env)

    def coerce_cascaded_operands_to_temp(self, env):
        if self.cascade:
            #self.operand2 = self.operand2.coerce_to_temp(env) #CTT
            self.operand2 = self.operand2.coerce_to_simple(env)
            self.cascade.coerce_cascaded_operands_to_temp(env)
    
    def allocate_subexpr_temps(self, env):
        self.operand2.allocate_temps(env)
        if self.cascade:
            self.cascade.allocate_subexpr_temps(env)
    
    def release_subexpr_temps(self, env):
        self.operand2.release_temp(env)
        if self.cascade:
            self.cascade.release_subexpr_temps(env)
    
    def generate_evaluation_code(self, code, result, operand1):
        if self.type.is_pyobject:
            code.putln("if (__Pyx_PyObject_IsTrue(%s)) {" % result)
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
        code.putln("}")

    def annotate(self, code):
        self.operand2.annotate(code)
        if self.cascade:
            self.cascade.annotate(code)


binop_node_classes = {
    "or":		BoolBinopNode,
    "and":	BoolBinopNode,
    "|":		IntBinopNode,
    "^":		IntBinopNode,
    "&":		IntBinopNode,
    "<<":		IntBinopNode,
    ">>":		IntBinopNode,
    "+":		AddNode,
    "-":		SubNode,
    "*":		MulNode,
    "/":		NumBinopNode,
    "//":		FloorDivNode,
    "%":		ModNode,
    "**":		PowNode
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
    
    def __init__(self, arg):
        self.pos = arg.pos
        self.arg = arg
        if debug_coercion:
            print("%s Coercing %s" % (self, self.arg))
            
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

    def __init__(self, arg, dst_type, env):
        #  The arg is know to be a Python object, and
        #  the dst_type is known to be an extension type.
        assert dst_type.is_extension_type or dst_type.is_builtin_type, "PyTypeTest on non extension type"
        CoercionNode.__init__(self, arg)
        self.type = dst_type
        self.gil_check(env)
        self.result_ctype = arg.ctype()
        if not dst_type.is_builtin_type:
            env.use_utility_code(type_test_utility_code)

    gil_message = "Python type test"
    
    def analyse_types(self, env):
        pass
    
    def result_in_temp(self):
        return self.arg.result_in_temp()
    
    def is_ephemeral(self):
        return self.arg.is_ephemeral()
    
    def calculate_result_code(self):
        return self.arg.result()
    
    def generate_result_code(self, code):
        if self.type.typeobj_is_available():
            code.putln(
                "if (!(%s)) %s" % (
                    self.type.type_test_code(self.arg.py_result()),
                    code.error_goto(self.pos)))
        else:
            error(self.pos, "Cannot test type of extern C class "
                "without type object name specification")
                
    def generate_post_assignment_code(self, code):
        self.arg.generate_post_assignment_code(code)
                

class CoerceToPyTypeNode(CoercionNode):
    #  This node is used to convert a C data type
    #  to a Python object.

    def __init__(self, arg, env):
        CoercionNode.__init__(self, arg)
        self.type = py_object_type
        self.gil_check(env)
        self.is_temp = 1
        if not arg.type.to_py_function or not arg.type.create_convert_utility_code(env):
            error(arg.pos,
                "Cannot convert '%s' to Python object" % arg.type)
        
    gil_message = "Converting to Python object"
    
    def coerce_to_boolean(self, env):
        return self.arg.coerce_to_boolean(env).coerce_to_temp(env)

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


class CoerceFromPyTypeNode(CoercionNode):
    #  This node is used to convert a Python object
    #  to a C data type.

    def __init__(self, result_type, arg, env):
        CoercionNode.__init__(self, arg)
        self.type = result_type
        self.is_temp = 1
        if not result_type.from_py_function:
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


class CoerceToBooleanNode(CoercionNode):
    #  This node is used when a result needs to be used
    #  in a boolean context.
    
    def __init__(self, arg, env):
        CoercionNode.__init__(self, arg)
        self.type = PyrexTypes.c_bint_type
        if arg.type.is_pyobject:
            if env.nogil:
                self.gil_error()
            self.is_temp = 1

    gil_message = "Truth-testing Python object"
    
    def check_const(self):
        if self.is_temp:
            self.not_const()
        self.arg.check_const()
    
    def calculate_result_code(self):
        return "(%s != 0)" % self.arg.result()

    def generate_result_code(self, code):
        if self.arg.type.is_pyobject:
            code.putln(
                "%s = __Pyx_PyObject_IsTrue(%s); %s" % (
                    self.result(), 
                    self.arg.py_result(), 
                    code.error_goto_if_neg(self.result(), self.pos)))


class CoerceToTempNode(CoercionNode):
    #  This node is used to force the result of another node
    #  to be stored in a temporary. It is only used if the
    #  argument node's result is not already in a temporary.

    def __init__(self, arg, env):
        CoercionNode.__init__(self, arg)
        self.type = self.arg.type
        self.is_temp = 1
        if self.type.is_pyobject:
            self.gil_check(env)
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
        if self.type.is_pyobject:
            code.put_incref(self.result(), self.ctype())


class CloneNode(CoercionNode):
    #  This node is employed when the result of another node needs
    #  to be used multiple times. The argument node's result must
    #  be in a temporary. This node "borrows" the result from the
    #  argument node, and does not generate any evaluation or
    #  disposal code for it. The original owner of the argument 
    #  node is responsible for doing those things.
    
    subexprs = [] # Arg is not considered a subexpr
    
    def __init__(self, arg):
        CoercionNode.__init__(self, arg)
        if hasattr(arg, 'type'):
            self.type = arg.type
            self.result_ctype = arg.result_ctype
        if hasattr(arg, 'entry'):
            self.entry = arg.entry
    
    def result(self):
        return self.arg.result()
        
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
                
    def allocate_temps(self, env):
        pass
        
    def release_temp(self, env):
        pass
        
class PersistentNode(ExprNode):
    # A PersistentNode is like a CloneNode except it handles the temporary
    # allocation itself by keeping track of the number of times it has been 
    # used. 
    
    subexprs = ["arg"]
    temp_counter = 0
    generate_counter = 0
    analyse_counter = 0
    result_code = None
    
    def __init__(self, arg, uses):
        self.pos = arg.pos
        self.arg = arg
        self.uses = uses
        
    def analyse_types(self, env):
        if self.analyse_counter == 0:
            self.arg.analyse_types(env)
            self.type = self.arg.type
            self.result_ctype = self.arg.result_ctype
            self.is_temp = 1
        self.analyse_counter += 1
        
    def calculate_result_code(self):
        return self.result()

    def generate_evaluation_code(self, code):
        if self.generate_counter == 0:
            self.arg.generate_evaluation_code(code)
            code.putln("%s = %s;" % (
                self.result(), self.arg.result_as(self.ctype())))
            if self.type.is_pyobject:
                code.put_incref(self.result(), self.ctype())
            self.arg.generate_disposal_code(code)
        self.generate_counter += 1
                
    def generate_disposal_code(self, code):
        if self.generate_counter == self.uses:
            if self.type.is_pyobject:
                code.put_decref_clear(self.result(), self.ctype())

    def allocate_temps(self, env, result=None):
        if self.temp_counter == 0:
            self.arg.allocate_temps(env)
            self.allocate_temp(env, result)
            self.arg.release_temp(env)
        self.temp_counter += 1
        
    def allocate_temp(self, env, result=None):
        if result is None:
            self.result_code = env.allocate_temp(self.type)
        else:
            self.result_code = result
        
    def release_temp(self, env):
        if self.temp_counter == self.uses:
            env.release_temp(self.result())
    
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
    __import__ = PyObject_GetAttrString(%(BUILTINS)s, "__import__");
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
    module = PyObject_CallFunction(__import__, "OOOO",
        name, global_dict, empty_dict, list);
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
            PyErr_Format(PyExc_ValueError,
                #if PY_VERSION_HEX < 0x02050000
                    "need more than %d values to unpack", (int)index);
                #else
                    "need more than %zd values to unpack", index);
                #endif
        }
    }
    return item;
}

static int __Pyx_EndUnpack(PyObject *iter) {
    PyObject *item;
    if ((item = PyIter_Next(iter))) {
        Py_DECREF(item);
        PyErr_SetString(PyExc_ValueError, "too many values to unpack");
        return -1;
    }
    else if (!PyErr_Occurred())
        return 0;
    else
        return -1;
}
""")

#------------------------------------------------------------------------------------

type_test_utility_code = UtilityCode(
proto = """
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/
""",
impl = """
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type) {
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if (obj == Py_None || PyObject_TypeCheck(obj, type))
        return 1;
    PyErr_Format(PyExc_TypeError, "Cannot convert %s to %s",
        Py_TYPE(obj)->tp_name, type->tp_name);
    return 0;
}
""")

#------------------------------------------------------------------------------------

create_class_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name, char *modname); /*proto*/
""",
impl = """
static PyObject *__Pyx_CreateClass(
    PyObject *bases, PyObject *dict, PyObject *name, char *modname)
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

append_utility_code = UtilityCode(
proto = """
static INLINE PyObject* __Pyx_PyObject_Append(PyObject* L, PyObject* x) {
    if (likely(PyList_CheckExact(L))) {
        if (PyList_Append(L, x) < 0) return NULL;
        Py_INCREF(Py_None);
        return Py_None; // this is just to have an accurate signature
    }
    else {
        return PyObject_CallMethod(L, "append", "(O)", x);
    }
}
""",
impl = ""
)

#------------------------------------------------------------------------------------

# If the is_unsigned flag is set, we need to do some extra work to make 
# sure the index doesn't become negative. 

getitem_int_utility_code = UtilityCode(
proto = """
static INLINE PyObject *__Pyx_GetItemInt(PyObject *o, Py_ssize_t i, int is_unsigned) {
    PyObject *r;
    if (PyList_CheckExact(o) && 0 <= i && i < PyList_GET_SIZE(o)) {
        r = PyList_GET_ITEM(o, i);
        Py_INCREF(r);
    }
    else if (PyTuple_CheckExact(o) && 0 <= i && i < PyTuple_GET_SIZE(o)) {
        r = PyTuple_GET_ITEM(o, i);
        Py_INCREF(r);
    }
    else if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_item && (likely(i >= 0) || !is_unsigned))
        r = PySequence_GetItem(o, i);
    else {
        PyObject *j = (likely(i >= 0) || !is_unsigned) ? PyInt_FromLong(i) : PyLong_FromUnsignedLongLong((sizeof(unsigned long long) > sizeof(Py_ssize_t) ? (1ULL << (sizeof(Py_ssize_t)*8)) : 0) + i);
        if (!j)
            return 0;
        r = PyObject_GetItem(o, j);
        Py_DECREF(j);
    }
    return r;
}
""",
impl = """
""")

#------------------------------------------------------------------------------------

setitem_int_utility_code = UtilityCode(
proto = """
static INLINE int __Pyx_SetItemInt(PyObject *o, Py_ssize_t i, PyObject *v, int is_unsigned) {
    int r;
    if (PyList_CheckExact(o) && 0 <= i && i < PyList_GET_SIZE(o)) {
        Py_DECREF(PyList_GET_ITEM(o, i));
        Py_INCREF(v);
        PyList_SET_ITEM(o, i, v);
        return 1;
    }
    else if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_ass_item && (likely(i >= 0) || !is_unsigned))
        r = PySequence_SetItem(o, i, v);
    else {
        PyObject *j = (likely(i >= 0) || !is_unsigned) ? PyInt_FromLong(i) : PyLong_FromUnsignedLongLong((sizeof(unsigned long long) > sizeof(Py_ssize_t) ? (1ULL << (sizeof(Py_ssize_t)*8)) : 0) + i);
        if (!j)
            return -1;
        r = PyObject_SetItem(o, j, v);
        Py_DECREF(j);
    }
    return r;
}
""",
impl = """
""")

#------------------------------------------------------------------------------------

delitem_int_utility_code = UtilityCode(
proto = """
static INLINE int __Pyx_DelItemInt(PyObject *o, Py_ssize_t i, int is_unsigned) {
    int r;
    if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_ass_item && (likely(i >= 0) || !is_unsigned))
        r = PySequence_DelItem(o, i);
    else {
        PyObject *j = (likely(i >= 0) || !is_unsigned) ? PyInt_FromLong(i) : PyLong_FromUnsignedLongLong((sizeof(unsigned long long) > sizeof(Py_ssize_t) ? (1ULL << (sizeof(Py_ssize_t)*8)) : 0) + i);
        if (!j)
            return -1;
        r = PyObject_DelItem(o, j);
        Py_DECREF(j);
    }
    return r;
}
""",
impl = """
""")

#------------------------------------------------------------------------------------

raise_noneattr_error_utility_code = UtilityCode(
proto = """
static INLINE void __Pyx_RaiseNoneAttributeError(char* attrname);
""",
impl = """
static INLINE void __Pyx_RaiseNoneAttributeError(char* attrname) {
    PyErr_Format(PyExc_AttributeError, "'NoneType' object has no attribute '%s'", attrname);
}
""")

raise_noneindex_error_utility_code = UtilityCode(
proto = """
static INLINE void __Pyx_RaiseNoneIndexingError();
""",
impl = """
static INLINE void __Pyx_RaiseNoneIndexingError() {
    PyErr_SetString(PyExc_TypeError, "'NoneType' object is unsubscriptable");
}
""")
