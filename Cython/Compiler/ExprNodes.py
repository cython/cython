#
#   Pyrex - Parse tree nodes for expressions
#

import cython
from cython import set
cython.declare(error=object, warning=object, warn_once=object, InternalError=object,
               CompileError=object, UtilityCode=object, StringEncoding=object, operator=object,
               Naming=object, Nodes=object, PyrexTypes=object, py_object_type=object,
               list_type=object, tuple_type=object, set_type=object, dict_type=object, \
               unicode_type=object, str_type=object, bytes_type=object, type_type=object,
               Builtin=object, Symtab=object, Utils=object, find_coercion_error=object,
               debug_disposal_code=object, debug_temp_alloc=object, debug_coercion=object)

import operator

from Errors import error, warning, warn_once, InternalError, CompileError
from Errors import hold_errors, release_errors, held_errors, report_error
from Code import UtilityCode
import StringEncoding
import Naming
import Nodes
from Nodes import Node
import PyrexTypes
from PyrexTypes import py_object_type, c_long_type, typecast, error_type, \
     unspecified_type
from Builtin import list_type, tuple_type, set_type, dict_type, \
     unicode_type, str_type, bytes_type, type_type
import Builtin
import Symtab
import Options
from Cython import Utils
from Annotate import AnnotationItem

from Cython.Debugging import print_call_chain
from DebugFlags import debug_disposal_code, debug_temp_alloc, \
    debug_coercion

try:
    from __builtin__ import basestring
except ImportError:
    basestring = str # Python 3

class NotConstant(object):
    def __repr__(self):
        return "<NOT CONSTANT>"

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
    #  result_is_used  boolean   indicates that the result will be dropped and the
    #                            result_code/temp_result can safely be set to None

    result_ctype = None
    type = None
    temp_code = None
    old_temp = None # error checker for multiple frees etc.
    use_managed_ref = True # can be set by optimisation transforms
    result_is_used = True

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
        def __get_child_attrs(self):
            return self.subexprs
        _get_child_attrs = __get_child_attrs
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

    def has_constant_result(self):
        return self.constant_result is not constant_value_not_set and \
               self.constant_result is not not_a_constant

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
        return self.coerce_to_boolean(env).coerce_to_simple(env)

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

    def nonlocally_immutable(self):
        # Returns whether this variable is a safe reference, i.e.
        # can't be modified as part of globals or closures.
        return self.is_temp or self.type.is_array or self.type.is_cfunction

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
            if not self.result_is_used:
                # not used anyway, so ignore if not set up
                return
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
            if self.type.is_pyobject and self.result():
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

    def generate_function_definitions(self, env, code):
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

        if dst_type.is_reference:
            dst_type = dst_type.ref_base_type

        if dst_type.is_pyobject:
            if not src.type.is_pyobject:
                if dst_type is bytes_type and src.type.is_int:
                    src = CoerceIntToBytesNode(src, env)
                else:
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

        # if it's constant, calculate the result now
        if self.has_constant_result():
            bool_value = bool(self.constant_result)
            return BoolNode(self.pos, value=bool_value,
                            constant_result=bool_value)

        type = self.type
        if type.is_pyobject or type.is_ptr or type.is_float:
            return CoerceToBooleanNode(self, env)
        else:
            if not (type.is_int or type.is_enum or type.is_error):
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

    def may_be_none(self):
        if not self.type.is_pyobject:
            return False
        if self.constant_result not in (not_a_constant, constant_value_not_set):
            return self.constant_result is not None
        return True

    def as_cython_attribute(self):
        return None

    def as_none_safe_node(self, message, error="PyExc_TypeError"):
        # Wraps the node in a NoneCheckNode if it is not known to be
        # not-None (e.g. because it is a Python literal).
        if self.may_be_none():
            return NoneCheckNode(self, error, message)
        else:
            return self


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

    def may_be_none(self):
        return False

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

    def may_be_none(self):
        return True


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

    def nonlocally_immutable(self):
        return 1

    def may_be_none(self):
        return False

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
    # is_c_literal   True/False/None   creator considers this a C integer literal

    unsigned = ""
    longness = ""
    is_c_literal = None # unknown

    def __init__(self, pos, **kwds):
        ExprNode.__init__(self, pos, **kwds)
        if 'type' not in kwds:
            self.type = self.find_suitable_type_for_value()

    def find_suitable_type_for_value(self):
        if self.constant_result is constant_value_not_set:
            try:
                self.calculate_constant_result()
            except ValueError:
                pass
        # we ignore 'is_c_literal = True' and instead map signed 32bit
        # integers as C long values
        if self.is_c_literal or \
               self.constant_result in (constant_value_not_set, not_a_constant) or \
               self.unsigned or self.longness == 'LL':
            # clearly a C literal
            rank = (self.longness == 'LL') and 2 or 1
            suitable_type = PyrexTypes.modifiers_and_name_to_type[not self.unsigned, rank, "int"]
            if self.type:
                suitable_type = PyrexTypes.widest_numeric_type(suitable_type, self.type)
        else:
            # C literal or Python literal - split at 32bit boundary
            if self.constant_result >= -2**31 and self.constant_result < 2**31:
                if self.type and self.type.is_int:
                    suitable_type = self.type
                else:
                    suitable_type = PyrexTypes.c_long_type
            else:
                suitable_type = PyrexTypes.py_object_type
        return suitable_type

    def coerce_to(self, dst_type, env):
        if self.type is dst_type:
            return self
        elif dst_type.is_float:
            if self.constant_result is not not_a_constant:
                return FloatNode(self.pos, value='%d.0' % int(self.constant_result), type=dst_type,
                                 constant_result=float(self.constant_result))
            else:
                return FloatNode(self.pos, value=self.value, type=dst_type,
                                 constant_result=not_a_constant)
        if dst_type.is_numeric and not dst_type.is_complex:
            node = IntNode(self.pos, value=self.value, constant_result=self.constant_result,
                           type = dst_type, is_c_literal = True,
                           unsigned=self.unsigned, longness=self.longness)
            return node
        elif dst_type.is_pyobject:
            node = IntNode(self.pos, value=self.value, constant_result=self.constant_result,
                           type = PyrexTypes.py_object_type, is_c_literal = False,
                           unsigned=self.unsigned, longness=self.longness)
        else:
            # FIXME: not setting the type here to keep it working with
            # complex numbers. Should they be special cased?
            node = IntNode(self.pos, value=self.value, constant_result=self.constant_result,
                           unsigned=self.unsigned, longness=self.longness)
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
            plain_integer_string = self.value_as_c_integer_string(plain_digits=True)
            self.result_code = code.get_py_num(plain_integer_string, self.longness)
        else:
            self.result_code = self.get_constant_c_result_code()

    def get_constant_c_result_code(self):
        return self.value_as_c_integer_string() + self.unsigned + self.longness

    def value_as_c_integer_string(self, plain_digits=False):
        value = self.value
        if isinstance(value, basestring) and len(value) > 2:
            # must convert C-incompatible Py3 oct/bin notations
            if value[1] in 'oO':
                if plain_digits:
                    value = int(value[2:], 8)
                else:
                    value = value[0] + value[2:] # '0o123' => '0123'
            elif value[1] in 'bB':
                value = int(value[2:], 2)
            elif plain_digits and value[1] in 'xX':
                value = int(value[2:], 16)
        return str(value)

    def calculate_result_code(self):
        return self.result_code

    def calculate_constant_result(self):
        self.constant_result = Utils.str_to_number(self.value)

    def compile_time_value(self, denv):
        return Utils.str_to_number(self.value)


class FloatNode(ConstNode):
    type = PyrexTypes.c_double_type

    def calculate_constant_result(self):
        self.constant_result = float(self.value)

    def compile_time_value(self, denv):
        return float(self.value)

    def calculate_result_code(self):
        strval = self.value
        assert isinstance(strval, (str, unicode))
        cmpval = repr(float(strval))
        if cmpval == 'nan':
            return "(Py_HUGE_VAL * 0)"
        elif cmpval == 'inf':
            return "Py_HUGE_VAL"
        elif cmpval == '-inf':
            return "(-Py_HUGE_VAL)"
        else:
            return strval


class BytesNode(ConstNode):
    # A char* or bytes literal
    #
    # value      BytesLiteral

    # start off as Python 'bytes' to support len() in O(1)
    type = bytes_type

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

    def coerce_to_boolean(self, env):
        # This is special because testing a C char* for truth directly
        # would yield the wrong result.
        return BoolNode(self.pos, value=bool(self.value))

    def coerce_to(self, dst_type, env):
        if self.type == dst_type:
            return self
        if dst_type.is_int:
            if not self.can_coerce_to_char_literal():
                error(self.pos, "Only single-character string literals can be coerced into ints.")
                return self
            if dst_type.is_unicode_char:
                error(self.pos, "Bytes literals cannot coerce to Py_UNICODE/Py_UCS4, use a unicode literal instead.")
                return self
            return CharNode(self.pos, value=self.value)

        node = BytesNode(self.pos, value=self.value)
        if dst_type.is_pyobject:
            if dst_type in (py_object_type, Builtin.bytes_type):
                node.type = Builtin.bytes_type
            else:
                self.check_for_coercion_error(dst_type, fail=True)
                return node
        elif dst_type == PyrexTypes.c_char_ptr_type:
            node.type = dst_type
            return node
        elif dst_type == PyrexTypes.c_uchar_ptr_type:
            node.type = PyrexTypes.c_char_ptr_type
            return CastNode(node, PyrexTypes.c_uchar_ptr_type)
        elif dst_type.assignable_from(PyrexTypes.c_char_ptr_type):
            node.type = dst_type
            return node

        # We still need to perform normal coerce_to processing on the
        # result, because we might be coercing to an extension type,
        # in which case a type test node will be needed.
        return ConstNode.coerce_to(node, dst_type, env)

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
    # value        EncodedString
    # bytes_value  BytesLiteral    the literal parsed as bytes string ('-3' unicode literals only)

    bytes_value = None
    type = unicode_type

    def coerce_to(self, dst_type, env):
        if dst_type is self.type:
            pass
        elif dst_type.is_unicode_char:
            if not self.can_coerce_to_char_literal():
                error(self.pos, "Only single-character Unicode string literals or surrogate pairs can be coerced into Py_UCS4/Py_UNICODE.")
                return self
            int_value = ord(self.value)
            return IntNode(self.pos, type=dst_type, value=str(int_value), constant_result=int_value)
        elif not dst_type.is_pyobject:
            if dst_type.is_string and self.bytes_value is not None:
                # special case: '-3' enforced unicode literal used in a C char* context
                return BytesNode(self.pos, value=self.bytes_value).coerce_to(dst_type, env)
            error(self.pos, "Unicode literals do not support coercion to C types other than Py_UNICODE or Py_UCS4.")
        elif dst_type is not py_object_type:
            if not self.check_for_coercion_error(dst_type):
                self.fail_assignment(dst_type)
        return self

    def can_coerce_to_char_literal(self):
        return len(self.value) == 1
            ## or (len(self.value) == 2
            ##     and (0xD800 <= self.value[0] <= 0xDBFF)
            ##     and (0xDC00 <= self.value[1] <= 0xDFFF))

    def contains_surrogates(self):
        # Check if the unicode string contains surrogate code points
        # on a CPython platform with wide (UCS-4) or narrow (UTF-16)
        # Unicode, i.e. characters that would be spelled as two
        # separate code units on a narrow platform.
        for c in map(ord, self.value):
            if c > 65535: # can only happen on wide platforms
                return True
            # We only look for the first code unit (D800-DBFF) of a
            # surrogate pair - if we find one, the other one
            # (DC00-DFFF) is likely there, too.  If we don't find it,
            # any second code unit cannot make for a surrogate pair by
            # itself.
            if c >= 0xD800 and c <= 0xDBFF:
                return True
        return False

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
    # value          BytesLiteral (or EncodedString with ASCII content)
    # unicode_value  EncodedString or None
    # is_identifier  boolean

    type = str_type
    is_identifier = None
    unicode_value = None

    def coerce_to(self, dst_type, env):
        if dst_type is not py_object_type and not str_type.subtype_of(dst_type):
#            if dst_type is Builtin.bytes_type:
#                # special case: bytes = 'str literal'
#                return BytesNode(self.pos, value=self.value)
            if not dst_type.is_pyobject:
                return BytesNode(self.pos, value=self.value).coerce_to(dst_type, env)
            self.check_for_coercion_error(dst_type, fail=True)
        return self

    def can_coerce_to_char_literal(self):
        return not self.is_identifier and len(self.value) == 1

    def generate_evaluation_code(self, code):
        self.result_code = code.get_py_string_const(
            self.value, identifier=self.is_identifier, is_str=True,
            unicode_value=self.unicode_value)

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
        self.constant_result = Utils.str_to_number(self.value)

    def compile_time_value(self, denv):
        return Utils.str_to_number(self.value)

    def analyse_types(self, env):
        self.is_temp = 1

    def may_be_none(self):
        return False

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

    def may_be_none(self):
        return False

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


class NewExprNode(AtomicExprNode):

    # C++ new statement
    #
    # cppclass              node                 c++ class to create

    type = None

    def infer_type(self, env):
        type = self.cppclass.analyse_as_type(env)
        if type is None or not type.is_cpp_class:
            error(self.pos, "new operator can only be applied to a C++ class")
            self.type = error_type
            return
        self.cpp_check(env)
        constructor = type.scope.lookup(u'<init>')
        if constructor is None:
            return_type = PyrexTypes.CFuncType(type, [])
            return_type = PyrexTypes.CPtrType(return_type)
            type.scope.declare_cfunction(u'<init>', return_type, self.pos)
            constructor = type.scope.lookup(u'<init>')
        self.class_type = type
        self.entry = constructor
        self.type = constructor.type
        return self.type

    def analyse_types(self, env):
        if self.type is None:
            self.infer_type(env)

    def may_be_none(self):
        return False

    def generate_result_code(self, code):
        pass

    def calculate_result_code(self):
        return "new " + self.class_type.declaration_code("")


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
        elif self.entry.type.is_cfunction:
            # special case: referring to a C function must return its pointer
            return PyrexTypes.CPtrType(self.entry.type)
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
                    if var_entry.is_builtin and var_entry.is_const:
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
        env.control_flow.set_state(self.pos, (self.name, 'initialized'), True)
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
            if entry.is_builtin and entry.is_const:
                self.is_temp = 0
            else:
                self.is_temp = 1
                env.use_utility_code(get_name_interned_utility_code)
            self.is_used_as_rvalue = 1

    def nogil_check(self, env):
        if self.is_used_as_rvalue:
            entry = self.entry
            if entry.is_builtin:
                if not entry.is_const: # cached builtins are ok
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
            or entry.is_builtin or entry.is_cfunction
            or entry.is_cpp_class):
                if self.entry.as_variable:
                    self.entry = self.entry.as_variable
                else:
                    error(self.pos,
                          "'%s' is not a constant, variable or function identifier" % self.name)

    def is_simple(self):
        #  If it's not a C variable, it'll be in a temp.
        return 1

    def nonlocally_immutable(self):
        if ExprNode.nonlocally_immutable(self):
            return True
        entry = self.entry
        return entry and (entry.is_local or entry.is_arg) and not entry.in_closure

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
        if entry.is_builtin and entry.is_const:
            return # Lookup already cached
        elif entry.is_pyclass_attr:
            assert entry.type.is_pyobject, "Python global or builtin not a Python object"
            interned_cname = code.intern_identifier(self.entry.name)
            if entry.is_builtin:
                namespace = Naming.builtins_cname
            else: # entry.is_pyglobal
                namespace = entry.scope.namespace_cname
            code.putln(
                '%s = PyObject_GetItem(%s, %s); %s' % (
                self.result(),
                namespace,
                interned_cname,
                code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())

        elif entry.is_pyglobal or entry.is_builtin:
            assert entry.type.is_pyobject, "Python global or builtin not a Python object"
            interned_cname = code.intern_identifier(self.entry.name)
            if entry.is_builtin:
                namespace = Naming.builtins_cname
            else: # entry.is_pyglobal
                namespace = entry.scope.namespace_cname
            code.globalstate.use_utility_code(get_name_interned_utility_code)
            code.putln(
                '%s = __Pyx_GetName(%s, %s); %s' % (
                self.result(),
                namespace,
                interned_cname,
                code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())

        elif entry.is_local and False:
            # control flow not good enough yet
            assigned = entry.scope.control_flow.get_state((entry.name, 'initialized'), self.pos)
            if assigned is False:
                error(self.pos, "local variable '%s' referenced before assignment" % entry.name)
            elif not Options.init_local_none and assigned is None:
                code.putln('if (%s == 0) { PyErr_SetString(PyExc_UnboundLocalError, "%s"); %s }' %
                           (entry.cname, entry.name, code.error_goto(self.pos)))
                entry.scope.control_flow.set_state(self.pos, (entry.name, 'initialized'), True)

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
            elif entry.is_pyclass_attr:
                code.put_error_if_neg(self.pos,
                    'PyObject_SetItem(%s, %s, %s)' % (
                        namespace,
                        interned_cname,
                        rhs.py_result()))
                rhs.generate_disposal_code(code)
                rhs.free_temps(code)
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
                    is_external_ref = entry.is_cglobal or self.entry.in_closure or self.entry.from_closure
                    if not self.lhs_of_first_assignment:
                        if is_external_ref:
                            code.put_gotref(self.py_result())
                        if entry.is_local and not Options.init_local_none:
                            initialized = entry.scope.control_flow.get_state((entry.name, 'initialized'), self.pos)
                            if initialized is True:
                                code.put_decref(self.result(), self.ctype())
                            elif initialized is None:
                                code.put_xdecref(self.result(), self.ctype())
                        else:
                            code.put_decref(self.result(), self.ctype())
                    if is_external_ref:
                        code.put_giveref(rhs.py_result())

            code.putln('%s = %s;' % (self.result(),
                                     rhs.result_as(self.ctype())))
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
        elif self.entry.is_pyclass_attr:
            namespace = self.entry.scope.namespace_cname
            code.put_error_if_neg(self.pos,
                'PyMapping_DelItemString(%s, "%s")' % (
                    namespace,
                    self.entry.name))
        elif self.entry.is_pyglobal:
            code.put_error_if_neg(self.pos,
                '__Pyx_DelAttrString(%s, "%s")' % (
                    Naming.module_cname,
                    self.entry.name))
        elif self.entry.type.is_pyobject:
            # Fake it until we can do it for real...
            self.generate_assignment_code(NoneNode(self.pos), code)
        else:
            error(self.pos, "Deletion of C names not supported")

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
    #    __import__(module_name, globals(), None, name_list, level)
    #
    #  module_name   StringNode            dotted name of module. Empty module
    #                       name means importing the parent package accourding
    #                       to level
    #  name_list     ListNode or None      list of names to be imported
    #  level         int                   relative import level:
    #                       -1: attempt both relative import and absolute import;
    #                        0: absolute import;
    #                       >0: the number of parent directories to search
    #                           relative to the current module.
    #                     None: decide the level according to language level and
    #                           directives

    type = py_object_type

    subexprs = ['module_name', 'name_list']

    def analyse_types(self, env):
        if self.level is None:
            if env.directives['language_level'] < 3 or env.directives['py2_import']:
                self.level = -1
            else:
                self.level = 0
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
            "%s = __Pyx_Import(%s, %s, %d); %s" % (
                self.result(),
                self.module_name.py_result(),
                name_list_code,
                self.level,
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
    iter_func_ptr = None

    subexprs = ['sequence']

    def analyse_types(self, env):
        self.sequence.analyse_types(env)
        if (self.sequence.type.is_array or self.sequence.type.is_ptr) and \
                not self.sequence.type.is_string:
            # C array iteration will be transformed later on
            self.type = self.sequence.type
        else:
            self.sequence = self.sequence.coerce_to_pyobject(env)
            if self.sequence.type is list_type or \
                   self.sequence.type is tuple_type:
                self.sequence = self.sequence.as_none_safe_node("'NoneType' object is not iterable")
        self.is_temp = 1

    gil_message = "Iterating over Python object"

    def allocate_counter_temp(self, code):
        self.counter_cname = code.funcstate.allocate_temp(
            PyrexTypes.c_py_ssize_t_type, manage_ref=False)

    def release_counter_temp(self, code):
        code.funcstate.release_temp(self.counter_cname)

    _func_iternext_type = PyrexTypes.CPtrType(PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("it", PyrexTypes.py_object_type, None),
            ]))

    def generate_result_code(self, code):
        sequence_type = self.sequence.type
        if sequence_type.is_array or sequence_type.is_ptr:
            raise InternalError("for in carray slice not transformed")
        is_builtin_sequence = sequence_type is list_type or \
                              sequence_type is tuple_type
        self.may_be_a_sequence = not sequence_type.is_builtin_type
        if self.may_be_a_sequence:
            code.putln(
                "if (PyList_CheckExact(%s) || PyTuple_CheckExact(%s)) {" % (
                    self.sequence.py_result(),
                    self.sequence.py_result()))
        if is_builtin_sequence or self.may_be_a_sequence:
            code.putln(
                "%s = 0; %s = %s; __Pyx_INCREF(%s);" % (
                    self.counter_cname,
                    self.result(),
                    self.sequence.py_result(),
                    self.result()))
        if not is_builtin_sequence:
            self.iter_func_ptr = code.funcstate.allocate_temp(self._func_iternext_type, manage_ref=False)
            if self.may_be_a_sequence:
                code.putln("%s = NULL;" % self.iter_func_ptr)
                code.putln("} else {")
            code.putln("%s = -1; %s = PyObject_GetIter(%s); %s" % (
                    self.counter_cname,
                    self.result(),
                    self.sequence.py_result(),
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
            code.putln("%s = Py_TYPE(%s)->tp_iternext;" % (self.iter_func_ptr, self.py_result()))
        if self.may_be_a_sequence:
            code.putln("}")

    def generate_next_sequence_item(self, test_name, result_name, code):
        code.putln(
            "if (%s >= Py%s_GET_SIZE(%s)) break;" % (
                self.counter_cname,
                test_name,
                self.py_result()))
        code.putln(
            "%s = Py%s_GET_ITEM(%s, %s); __Pyx_INCREF(%s); %s++;" % (
                result_name,
                test_name,
                self.py_result(),
                self.counter_cname,
                result_name,
                self.counter_cname))

    def generate_iter_next_result_code(self, result_name, code):
        sequence_type = self.sequence.type
        if sequence_type is list_type:
            self.generate_next_sequence_item('List', result_name, code)
            return
        elif sequence_type is tuple_type:
            self.generate_next_sequence_item('Tuple', result_name, code)
            return

        if self.may_be_a_sequence:
            for test_name in ('List', 'Tuple'):
                code.putln("if (Py%s_CheckExact(%s)) {" % (test_name, self.py_result()))
                self.generate_next_sequence_item(test_name, result_name, code)
                code.put("} else ")

        code.putln("{")
        code.putln(
            "%s = %s(%s);" % (
                result_name,
                self.iter_func_ptr,
                self.py_result()))
        code.putln("if (unlikely(!%s)) {" % result_name)
        code.putln("if (PyErr_Occurred()) {")
        code.putln("if (likely(PyErr_ExceptionMatches(PyExc_StopIteration))) PyErr_Clear();")
        code.putln("else %s" % code.error_goto(self.pos))
        code.putln("}")
        code.putln("break;")
        code.putln("}")
        code.put_gotref(result_name)
        code.putln("}")

    def free_temps(self, code):
        if self.iter_func_ptr:
            code.funcstate.release_temp(self.iter_func_ptr)
            self.iter_func_ptr = None
        ExprNode.free_temps(self, code)


class NextNode(AtomicExprNode):
    #  Used as part of for statement implementation.
    #  Implements result = iterator.next()
    #  Created during analyse_types phase.
    #  The iterator is not owned by this node.
    #
    #  iterator   IteratorNode

    type = py_object_type

    def __init__(self, iterator, env):
        self.pos = iterator.pos
        self.iterator = iterator
        if iterator.type.is_ptr or iterator.type.is_array:
            self.type = iterator.type.base_type
        self.is_temp = 1

    def generate_result_code(self, code):
        self.iterator.generate_iter_next_result_code(self.result(), code)


class WithExitCallNode(ExprNode):
    # The __exit__() call of a 'with' statement.  Used in both the
    # except and finally clauses.

    # with_stat  WithStatNode                the surrounding 'with' statement
    # args       TupleNode or ResultStatNode the exception info tuple

    subexprs = ['args']

    def analyse_types(self, env):
        self.args.analyse_types(env)
        self.type = PyrexTypes.c_bint_type
        self.is_temp = True

    def generate_result_code(self, code):
        if isinstance(self.args, TupleNode):
            # call only if it was not already called (and decref-cleared)
            code.putln("if (%s) {" % self.with_stat.exit_var)
        result_var = code.funcstate.allocate_temp(py_object_type, manage_ref=False)
        code.putln("%s = PyObject_Call(%s, %s, NULL);" % (
            result_var,
            self.with_stat.exit_var,
            self.args.result()))
        code.put_decref_clear(self.with_stat.exit_var, type=py_object_type)
        code.putln(code.error_goto_if_null(result_var, self.pos))
        code.put_gotref(result_var)
        code.putln("%s = __Pyx_PyObject_IsTrue(%s);" % (self.result(), result_var))
        code.put_decref_clear(result_var, type=py_object_type)
        code.putln(code.error_goto_if_neg(self.result(), self.pos))
        code.funcstate.release_temp(result_var)
        if isinstance(self.args, TupleNode):
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

    def __init__(self, pos, type, env=None):
        ExprNode.__init__(self, pos)
        self.type = type
        if type.is_pyobject:
            self.result_ctype = py_object_type
        self.is_temp = 1

    def analyse_types(self, env):
        return self.type

    def analyse_target_declaration(self, env):
        pass

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
#  Parallel nodes (cython.parallel.thread(savailable|id))
#
#-------------------------------------------------------------------

class ParallelThreadsAvailableNode(AtomicExprNode):
    """
    Note: this is disabled and not a valid directive at this moment

    Implements cython.parallel.threadsavailable(). If we are called from the
    sequential part of the application, we need to call omp_get_max_threads(),
    and in the parallel part we can just call omp_get_num_threads()
    """

    type = PyrexTypes.c_int_type

    def analyse_types(self, env):
        self.is_temp = True
        # env.add_include_file("omp.h")
        return self.type

    def generate_result_code(self, code):
        code.putln("#ifdef _OPENMP")
        code.putln("if (omp_in_parallel()) %s = omp_get_max_threads();" %
                                                            self.temp_code)
        code.putln("else %s = omp_get_num_threads();" % self.temp_code)
        code.putln("#else")
        code.putln("%s = 1;" % self.temp_code)
        code.putln("#endif")

    def result(self):
        return self.temp_code


class ParallelThreadIdNode(AtomicExprNode): #, Nodes.ParallelNode):
    """
    Implements cython.parallel.threadid()
    """

    type = PyrexTypes.c_int_type

    def analyse_types(self, env):
        self.is_temp = True
        # env.add_include_file("omp.h")
        return self.type

    def generate_result_code(self, code):
        code.putln("#ifdef _OPENMP")
        code.putln("%s = omp_get_thread_num();" % self.temp_code)
        code.putln("#else")
        code.putln("%s = 0;" % self.temp_code)
        code.putln("#endif")

    def result(self):
        return self.temp_code


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

    def is_simple(self):
        if self.is_buffer_access:
            return False
        base = self.base
        return (base.is_simple() and self.index.is_simple()
                and base.type and (base.type.is_ptr or base.type.is_array))

    def analyse_target_declaration(self, env):
        pass

    def analyse_as_type(self, env):
        base_type = self.base.analyse_as_type(env)
        if base_type and not base_type.is_pyobject:
            if base_type.is_cpp_class:
                if isinstance(self.index, TupleNode):
                    template_values = self.index.args
                else:
                    template_values = [self.index]
                import Nodes
                type_node = Nodes.TemplatedTypeNode(
                    pos = self.pos,
                    positional_args = template_values,
                    keyword_args = None)
                return type_node.analyse(env, base_type = base_type)
            else:
                return PyrexTypes.CArrayType(base_type, int(self.index.compile_time_value(env)))
        return None

    def type_dependencies(self, env):
        return self.base.type_dependencies(env) + self.index.type_dependencies(env)

    def infer_type(self, env):
        base_type = self.base.infer_type(env)
        if isinstance(self.index, SliceNode):
            # slicing!
            if base_type.is_string:
                # sliced C strings must coerce to Python
                return bytes_type
            elif base_type in (unicode_type, bytes_type, str_type, list_type, tuple_type):
                # slicing these returns the same type
                return base_type
            else:
                # TODO: Handle buffers (hopefully without too much redundancy).
                return py_object_type

        index_type = self.index.infer_type(env)
        if index_type and index_type.is_int or isinstance(self.index, (IntNode, LongNode)):
            # indexing!
            if base_type is unicode_type:
                # Py_UCS4 will automatically coerce to a unicode string
                # if required, so this is safe.  We only infer Py_UCS4
                # when the index is a C integer type.  Otherwise, we may
                # need to use normal Python item access, in which case
                # it's faster to return the one-char unicode string than
                # to receive it, throw it away, and potentially rebuild it
                # on a subsequent PyObject coercion.
                return PyrexTypes.c_py_ucs4_type
            elif base_type is str_type:
                # always returns str - Py2: bytes, Py3: unicode
                return base_type
            elif isinstance(self.base, BytesNode):
                #if env.global_scope().context.language_level >= 3:
                #    # infering 'char' can be made to work in Python 3 mode
                #    return PyrexTypes.c_char_type
                # Py2/3 return different types on indexing bytes objects
                return py_object_type
            elif base_type.is_ptr or base_type.is_array:
                return base_type.base_type

        # may be slicing or indexing, we don't know
        if base_type in (unicode_type, str_type):
            # these types always returns their own type on Python indexing/slicing
            return base_type
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

        is_slice = isinstance(self.index, SliceNode)
        # Potentially overflowing index value.
        if not is_slice and isinstance(self.index, IntNode) and Utils.long_literal(self.index.value):
            self.index = self.index.coerce_to_pyobject(env)

        # Handle the case where base is a literal char* (and we expect a string, not an int)
        if isinstance(self.base, BytesNode) or is_slice:
            if self.base.type.is_string or not (self.base.type.is_ptr or self.base.type.is_array):
                self.base = self.base.coerce_to_pyobject(env)

        skip_child_analysis = False
        buffer_access = False
        if self.base.type.is_buffer:
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
            if buffer_access:
                assert hasattr(self.base, "entry") # Must be a NameNode-like node

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
            base_type = self.base.type
            if isinstance(self.index, TupleNode):
                self.index.analyse_types(env, skip_children=skip_child_analysis)
            elif not skip_child_analysis:
                self.index.analyse_types(env)
            self.original_index_type = self.index.type
            if base_type.is_unicode_char:
                # we infer Py_UNICODE/Py_UCS4 for unicode strings in some
                # cases, but indexing must still work for them
                if self.index.constant_result in (0, -1):
                    # FIXME: we know that this node is redundant -
                    # currently, this needs to get handled in Optimize.py
                    pass
                self.base = self.base.coerce_to_pyobject(env)
                base_type = self.base.type
            if base_type.is_pyobject:
                if self.index.type.is_int:
                    if (not setting
                        and (base_type in (list_type, tuple_type, unicode_type))
                        and (not self.index.type.signed or isinstance(self.index, IntNode) and int(self.index.value) >= 0)
                        and not env.directives['boundscheck']):
                        self.is_temp = 0
                    else:
                        self.is_temp = 1
                    self.index = self.index.coerce_to(PyrexTypes.c_py_ssize_t_type, env).coerce_to_simple(env)
                else:
                    self.index = self.index.coerce_to_pyobject(env)
                    self.is_temp = 1
                if self.index.type.is_int and base_type is unicode_type:
                    # Py_UNICODE/Py_UCS4 will automatically coerce to a unicode string
                    # if required, so this is fast and safe
                    self.type = PyrexTypes.c_py_ucs4_type
                elif is_slice and base_type in (bytes_type, str_type, unicode_type, list_type, tuple_type):
                    self.type = base_type
                else:
                    self.type = py_object_type
            else:
                if base_type.is_ptr or base_type.is_array:
                    self.type = base_type.base_type
                    if is_slice:
                        self.type = base_type
                    elif self.index.type.is_pyobject:
                        self.index = self.index.coerce_to(
                            PyrexTypes.c_py_ssize_t_type, env)
                    elif not self.index.type.is_int:
                        error(self.pos,
                            "Invalid index type '%s'" %
                                self.index.type)
                elif base_type.is_cpp_class:
                    function = env.lookup_operator("[]", [self.base, self.index])
                    if function is None:
                        error(self.pos, "Indexing '%s' not supported for index type '%s'" % (base_type, self.index.type))
                        self.type = PyrexTypes.error_type
                        self.result_code = "<error>"
                        return
                    func_type = function.type
                    if func_type.is_ptr:
                        func_type = func_type.base_type
                    self.index = self.index.coerce_to(func_type.args[0].type, env)
                    self.type = func_type.return_type
                    if setting and not func_type.return_type.is_reference:
                        error(self.pos, "Can't set non-reference result '%s'" % self.type)
                else:
                    error(self.pos,
                        "Attempting to index non-array type '%s'" %
                            base_type)
                    self.type = PyrexTypes.error_type

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
        elif self.base.type is unicode_type and self.type.is_unicode_char:
            return "PyUnicode_AS_UNICODE(%s)[%s]" % (self.base.result(), self.index.result())
        elif (self.type.is_ptr or self.type.is_array) and self.type == self.base.type:
            error(self.pos, "Invalid use of pointer slice")
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
        elif self.is_temp:
            if self.type.is_pyobject:
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
                    index_code = self.index.py_result()
                    if self.base.type is dict_type:
                        function = "__Pyx_PyDict_GetItem"
                        code.globalstate.use_utility_code(getitem_dict_utility_code)
                    else:
                        function = "PyObject_GetItem"
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
            elif self.type.is_unicode_char and self.base.type is unicode_type:
                assert self.index.type.is_int
                index_code = self.index.result()
                function = "__Pyx_GetItemInt_Unicode"
                code.globalstate.use_utility_code(getitem_int_pyunicode_utility_code)
                code.putln(
                    "%s = %s(%s, %s%s); if (unlikely(%s == (Py_UNICODE)-1)) %s;" % (
                        self.result(),
                        function,
                        self.base.py_result(),
                        index_code,
                        self.extra_index_params(),
                        self.result(),
                        code.error_goto(self.pos)))

    def generate_setitem_code(self, value_code, code):
        if self.index.type.is_int:
            function = "__Pyx_SetItemInt"
            index_code = self.index.result()
            code.globalstate.use_utility_code(setitem_int_utility_code)
        else:
            index_code = self.index.py_result()
            if self.base.type is dict_type:
                function = "PyDict_SetItem"
            # It would seem that we could specialized lists/tuples, but that
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
        elif base_type.is_ptr or base_type.is_array:
            return PyrexTypes.c_array_type(base_type.base_type, None)
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
        elif base_type.is_ptr:
            self.type = base_type
        elif base_type.is_array:
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
                    "%s = PyBytes_FromString(%s + %s); %s" % (
                        self.result(),
                        self.base.result(),
                        self.start_code(),
                        code.error_goto_if_null(self.result(), self.pos)))
            else:
                code.putln(
                    "%s = PyBytes_FromStringAndSize(%s + %s, %s - %s); %s" % (
                        self.result(),
                        self.base.result(),
                        self.start_code(),
                        self.stop_code(),
                        self.start_code(),
                        code.error_goto_if_null(self.result(), self.pos)))
        else:
            code.putln(
                "%s = __Pyx_PySequence_GetSlice(%s, %s, %s); %s" % (
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
                "__Pyx_PySequence_SetSlice(%s, %s, %s, %s)" % (
                    self.base.py_result(),
                    self.start_code(),
                    self.stop_code(),
                    rhs.py_result()))
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
            "__Pyx_PySequence_DelSlice(%s, %s, %s)" % (
                self.base.py_result(),
                self.start_code(),
                self.stop_code()))
        self.generate_subexpr_disposal_code(code)
        self.free_subexpr_temps(code)

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

    subexprs = ['start', 'stop', 'step']

    type = py_object_type
    is_temp = 1

    def calculate_constant_result(self):
        self.constant_result = slice(
            self.start.constant_result,
            self.stop.constant_result,
            self.step.constant_result)

    def compile_time_value(self, denv):
        start = self.start.compile_time_value(denv)
        stop = self.stop.compile_time_value(denv)
        step = self.step.compile_time_value(denv)
        try:
            return slice(start, stop, step)
        except Exception, e:
            self.compile_time_value_error(e)

    def analyse_types(self, env):
        self.start.analyse_types(env)
        self.stop.analyse_types(env)
        self.step.analyse_types(env)
        self.start = self.start.coerce_to_pyobject(env)
        self.stop = self.stop.coerce_to_pyobject(env)
        self.step = self.step.coerce_to_pyobject(env)
        if self.start.is_literal and self.stop.is_literal and self.step.is_literal:
            self.is_literal = True
            self.is_temp = False

    gil_message = "Constructing Python slice object"

    def calculate_result_code(self):
        return self.result_code

    def generate_result_code(self, code):
        if self.is_literal:
            self.result_code = code.get_py_const(py_object_type, 'slice_', cleanup_level=2)
            code = code.get_cached_constants_writer()
            code.mark_pos(self.pos)

        code.putln(
            "%s = PySlice_New(%s, %s, %s); %s" % (
                self.result(),
                self.start.py_result(),
                self.stop.py_result(),
                self.step.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())
        if self.is_literal:
            code.put_giveref(self.py_result())


class CallNode(ExprNode):

    # allow overriding the default 'may_be_none' behaviour
    may_return_none = None

    def may_be_none(self):
        if self.may_return_none is not None:
            return self.may_return_none
        return ExprNode.may_be_none(self)

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
        elif type and type.is_cpp_class:
            for arg in self.args:
                arg.analyse_types(env)
            constructor = type.scope.lookup("<init>")
            self.function = RawCNameExprNode(self.function.pos, constructor.type)
            self.function.entry = constructor
            self.function.set_cname(type.declaration_code(""))
            self.analyse_c_function_call(env)
            return True

    def is_lvalue(self):
        return self.type.is_reference

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
    #  nogil          bool                 used internally

    subexprs = ['self', 'coerced_self', 'function', 'args', 'arg_tuple']

    self = None
    coerced_self = None
    arg_tuple = None
    wrapper_call = False
    has_optional_args = False
    nogil = False
    analysed = False

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
        if isinstance(self.function, NewExprNode):
            return PyrexTypes.CPtrType(self.function.class_type)
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
        if self.analysed:
            return
        self.analysed = True
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
                self.may_return_none = False
            elif function.is_name and function.type_entry:
                # We are calling an extension type constructor.  As
                # long as we do not support __new__(), the result type
                # is clear
                self.type = function.type_entry.type
                self.result_ctype = py_object_type
                self.may_return_none = False
            else:
                self.type = py_object_type
            self.is_temp = 1
        else:
            for arg in self.args:
                arg.analyse_types(env)
            if self.self and func_type.args:
                # Coerce 'self' to the type expected by the method.
                self_arg = func_type.args[0]
                if self_arg.not_none: # C methods must do the None test for self at *call* time
                    self.self = self.self.as_none_safe_node(
                        "'NoneType' object has no attribute '%s'" % self.function.entry.name,
                        'PyExc_AttributeError')
                expected_type = self_arg.type
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

    def is_simple(self):
        # C function calls could be considered simple, but they may
        # have side-effects that may hit when multiple operations must
        # be effected in order, e.g. when constructing the argument
        # sequence for a function call or comparing values.
        return False

    def analyse_c_function_call(self, env):
        if self.function.type is error_type:
            self.type = error_type
            return
        if self.function.type.is_cpp_class:
            overloaded_entry = self.function.type.scope.lookup("operator()")
            if overloaded_entry is None:
                self.type = PyrexTypes.error_type
                self.result_code = "<error>"
                return
        elif hasattr(self.function, 'entry'):
            overloaded_entry = self.function.entry
        else:
            overloaded_entry = None
        if overloaded_entry:
            entry = PyrexTypes.best_match(self.args, overloaded_entry.all_alternatives(), self.pos)
            if not entry:
                self.type = PyrexTypes.error_type
                self.result_code = "<error>"
                return
            self.function.entry = entry
            self.function.type = entry.type
            func_type = self.function_type()
        else:
            func_type = self.function_type()
            if not func_type.is_cfunction:
                error(self.pos, "Calling non-function type '%s'" % func_type)
                self.type = PyrexTypes.error_type
                self.result_code = "<error>"
                return
        # Check no. of args
        max_nargs = len(func_type.args)
        expected_nargs = max_nargs - func_type.optional_arg_count
        actual_nargs = len(self.args)
        if func_type.optional_arg_count and expected_nargs != actual_nargs:
            self.has_optional_args = 1
            self.is_temp = 1
        # Coerce arguments
        some_args_in_temps = False
        for i in xrange(min(max_nargs, actual_nargs)):
            formal_type = func_type.args[i].type
            arg = self.args[i].coerce_to(formal_type, env)
            if arg.is_temp:
                if i > 0:
                    # first argument in temp doesn't impact subsequent arguments
                    some_args_in_temps = True
            elif arg.type.is_pyobject and not env.nogil:
                if i == 0 and self.self is not None:
                    # a method's cloned "self" argument is ok
                    pass
                elif arg.nonlocally_immutable():
                    # plain local variables are ok
                    pass
                else:
                    # we do not safely own the argument's reference,
                    # but we must make sure it cannot be collected
                    # before we return from the function, so we create
                    # an owned temp reference to it
                    if i > 0: # first argument doesn't matter
                        some_args_in_temps = True
                    arg = arg.coerce_to_temp(env)
            self.args[i] = arg
        # handle additional varargs parameters
        for i in xrange(max_nargs, actual_nargs):
            arg = self.args[i]
            if arg.type.is_pyobject:
                arg_ctype = arg.type.default_coerced_ctype()
                if arg_ctype is None:
                    error(self.args[i].pos,
                          "Python object cannot be passed as a varargs parameter")
                else:
                    self.args[i] = arg = arg.coerce_to(arg_ctype, env)
            if arg.is_temp and i > 0:
                some_args_in_temps = True
        if some_args_in_temps:
            # if some args are temps and others are not, they may get
            # constructed in the wrong order (temps first) => make
            # sure they are either all temps or all not temps (except
            # for the last argument, which is evaluated last in any
            # case)
            for i in xrange(actual_nargs-1):
                if i == 0 and self.self is not None:
                    continue # self is ok
                arg = self.args[i]
                if arg.nonlocally_immutable():
                    # locals, C functions, unassignable types are safe.
                    pass
                elif arg.type.is_cpp_class:
                    # Assignment has side effects, avoid.
                    pass
                elif env.nogil and arg.type.is_pyobject:
                    # can't copy a Python reference into a temp in nogil
                    # env (this is safe: a construction would fail in
                    # nogil anyway)
                    pass
                else:
                    #self.args[i] = arg.coerce_to_temp(env)
                    # instead: issue a warning
                    if i > 0 or i == 1 and self.self is not None: # skip first arg
                        warning(arg.pos, "Argument evaluation order in C function call is undefined and may not be as expected", 0)
                        break
        # Calc result type and code fragment
        if isinstance(self.function, NewExprNode):
            self.type = PyrexTypes.CPtrType(self.function.class_type)
        else:
            self.type = func_type.return_type
        if self.type.is_pyobject:
            self.result_ctype = py_object_type
            self.is_temp = 1
        elif func_type.exception_value is not None \
                 or func_type.exception_check:
            self.is_temp = 1
        # Called in 'nogil' context?
        self.nogil = env.nogil
        if (self.nogil and
            func_type.exception_check and
            func_type.exception_check != '+'):
            env.use_utility_code(pyerr_occurred_withgil_utility_code)
        # C++ exception handler
        if func_type.exception_check == '+':
            if func_type.exception_value is None:
                env.use_utility_code(cpp_exception_utility_code)

    def calculate_result_code(self):
        return self.c_call_code()

    def c_call_code(self):
        func_type = self.function_type()
        if self.type is PyrexTypes.error_type or not func_type.is_cfunction:
            return "<error>"
        formal_args = func_type.args
        arg_list_code = []
        args = list(zip(formal_args, self.args))
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
                args = list(zip(func_type.args, self.args))
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
                    if self.nogil:
                        exc_checks.append("__Pyx_ErrOccurredWithGIL()")
                    else:
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
                    if self.nogil:
                        raise_py_exception = 'Py_BLOCK_THREADS; %s; Py_UNBLOCK_THREADS' % raise_py_exception
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

    # By default, we assume that the call never returns None, as this
    # is true for most C-API functions in CPython.  If this does not
    # apply to a call, set the following to True (or None to inherit
    # the default behaviour).
    may_return_none = False

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
            raise CompileError(self.pos,
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
            self.may_return_none = False
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

    def may_be_none(self):
        return False

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
        if (isinstance(self.obj, NameNode) and
                self.obj.is_cython_module and not
                self.attribute == u"parallel"):
            return self.attribute

        cy = self.obj.as_cython_attribute()
        if cy:
            return "%s.%s" % (cy, self.attribute)

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
            obj_type = self.obj.infer_type(env)
            self.analyse_attribute(env, obj_type = obj_type)
            if obj_type.is_builtin_type and self.type.is_cfunction:
                # special case: C-API replacements for C methods of
                # builtin types cannot be inferred as C functions as
                # that would prevent their use as bound methods
                self.type = py_object_type
                return py_object_type
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
        if not isinstance(self.obj, (UnicodeNode, StringNode, BytesNode)):
            base_type = self.obj.analyse_as_type(env)
            if base_type and hasattr(base_type, 'scope') and base_type.scope is not None:
                return base_type.scope.lookup_type(self.attribute)
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
        elif target and self.obj.type.is_builtin_type:
            error(self.pos, "Assignment to an immutable object field")

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
        elif obj_type.is_extension_type or obj_type.is_builtin_type:
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
            if obj.type.is_builtin_type and self.entry and self.entry.is_variable:
                # accessing a field of a builtin type, need to cast better than result_as() does
                obj_code = obj.type.cast_code(obj.result(), to_object_struct = True)
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
        if self.is_py_attr or (isinstance(self.entry.scope, Symtab.PropertyScope)
                               and u'__del__' in self.entry.scope.entries):
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
        self.is_temp = 1
        # not setting self.type here, subtypes do this

    def may_be_none(self):
        return False

    def analyse_target_types(self, env):
        self.unpacked_items = []
        self.coerced_unpacked_items = []
        self.any_coerced_items = False
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
            if unpacked_item is not coerced_unpacked_item:
                self.any_coerced_items = True
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

    _func_iternext_type = PyrexTypes.CPtrType(PyrexTypes.CFuncType(
        PyrexTypes.py_object_type, [
            PyrexTypes.CFuncTypeArg("it", PyrexTypes.py_object_type, None),
            ]))

    def generate_parallel_assignment_code(self, rhs, code):
        # Need to work around the fact that generate_evaluation_code
        # allocates the temps in a rather hacky way -- the assignment
        # is evaluated twice, within each if-block.
        special_unpack = (rhs.type is py_object_type
                          or rhs.type in (tuple_type, list_type)
                          or not rhs.type.is_builtin_type)
        if special_unpack:
            tuple_check = 'likely(PyTuple_CheckExact(%s))' % rhs.py_result()
            list_check  = 'PyList_CheckExact(%s)' % rhs.py_result()
            if rhs.type is list_type:
                sequence_types = ['List']
                sequence_type_test = list_check
            elif rhs.type is tuple_type:
                sequence_types = ['Tuple']
                sequence_type_test = tuple_check
            else:
                sequence_types = ['Tuple', 'List']
                sequence_type_test = "(%s) || (%s)" % (tuple_check, list_check)
            code.putln("if (%s) {" % sequence_type_test)
            code.putln("PyObject* sequence = %s;" % rhs.py_result())
            for item in self.unpacked_items:
                item.allocate(code)
            if len(sequence_types) == 2:
                code.putln("if (likely(Py%s_CheckExact(sequence))) {" % sequence_types[0])
            self.generate_special_parallel_unpacking_code(code, sequence_types[0])
            if len(sequence_types) == 2:
                code.putln("} else {")
                self.generate_special_parallel_unpacking_code(code, sequence_types[1])
                code.putln("}")
            for item in self.unpacked_items:
                code.put_incref(item.result(), item.ctype())
            rhs.generate_disposal_code(code)
            code.putln("} else {")

        if special_unpack and rhs.type is tuple_type:
            code.globalstate.use_utility_code(tuple_unpacking_error_code)
            code.putln("__Pyx_UnpackTupleError(%s, %s);" % (
                        rhs.py_result(), len(self.args)))
            code.putln(code.error_goto(self.pos))
        else:
            self.generate_generic_parallel_unpacking_code(code, rhs)
        if special_unpack:
            code.putln("}")

        for value_node in self.coerced_unpacked_items:
            value_node.generate_evaluation_code(code)
        for i in range(len(self.args)):
            self.args[i].generate_assignment_code(
                self.coerced_unpacked_items[i], code)

    def generate_special_parallel_unpacking_code(self, code, sequence_type):
        code.globalstate.use_utility_code(raise_need_more_values_to_unpack)
        code.globalstate.use_utility_code(raise_too_many_values_to_unpack)
        code.putln("if (unlikely(Py%s_GET_SIZE(sequence) != %d)) {" % (
            sequence_type, len(self.args)))
        code.putln("if (Py%s_GET_SIZE(sequence) > %d) __Pyx_RaiseTooManyValuesError(%d);" % (
            sequence_type, len(self.args), len(self.args)))
        code.putln("else __Pyx_RaiseNeedMoreValuesError(Py%s_GET_SIZE(sequence));" % sequence_type)
        code.putln(code.error_goto(self.pos))
        code.putln("}")
        for i, item in enumerate(self.unpacked_items):
            code.putln("%s = Py%s_GET_ITEM(sequence, %d); " % (item.result(), sequence_type, i))

    def generate_generic_parallel_unpacking_code(self, code, rhs):
        code.globalstate.use_utility_code(iternext_unpacking_end_utility_code)
        code.globalstate.use_utility_code(raise_need_more_values_to_unpack)
        code.putln("Py_ssize_t index = -1;")

        iterator_temp = code.funcstate.allocate_temp(py_object_type, manage_ref=True)
        code.putln(
            "%s = PyObject_GetIter(%s); %s" % (
                iterator_temp,
                rhs.py_result(),
                code.error_goto_if_null(iterator_temp, self.pos)))
        code.put_gotref(iterator_temp)
        rhs.generate_disposal_code(code)

        iternext_func = code.funcstate.allocate_temp(self._func_iternext_type, manage_ref=False)
        code.putln("%s = Py_TYPE(%s)->tp_iternext;" % (
            iternext_func, iterator_temp))

        unpacking_error_label = code.new_label('unpacking_failed')
        code.use_label(unpacking_error_label)
        unpack_code = "%s(%s)" % (iternext_func, iterator_temp)
        for i in range(len(self.args)):
            item = self.unpacked_items[i]
            code.putln(
                "index = %d; %s = %s; if (unlikely(!%s)) goto %s;" % (
                    i,
                    item.result(),
                    typecast(item.ctype(), py_object_type, unpack_code),
                    item.result(),
                    unpacking_error_label))
            code.put_gotref(item.py_result())
        code.put_error_if_neg(self.pos, "__Pyx_IternextUnpackEndCheck(%s(%s), %d)" % (
            iternext_func,
            iterator_temp,
            len(self.args)))
        code.put_decref_clear(iterator_temp, py_object_type)
        code.funcstate.release_temp(iterator_temp)
        code.funcstate.release_temp(iternext_func)
        unpacking_done_label = code.new_label('unpacking_done')
        code.put_goto(unpacking_done_label)

        code.put_label(unpacking_error_label)
        code.put_decref_clear(iterator_temp, py_object_type)
        code.putln("if (PyErr_Occurred() && PyErr_ExceptionMatches(PyExc_StopIteration)) PyErr_Clear();")
        code.putln("if (!PyErr_Occurred()) __Pyx_RaiseNeedMoreValuesError(index);")
        code.putln(code.error_goto(self.pos))
        code.put_label(unpacking_done_label)

    def generate_starred_assignment_code(self, rhs, code):
        for i, arg in enumerate(self.args):
            if arg.is_starred:
                starred_target = self.unpacked_items[i]
                fixed_args_left  = self.args[:i]
                fixed_args_right = self.args[i+1:]
                break

        iterator_temp = code.funcstate.allocate_temp(py_object_type, manage_ref=True)
        code.putln(
            "%s = PyObject_GetIter(%s); %s" % (
                iterator_temp,
                rhs.py_result(),
                code.error_goto_if_null(iterator_temp, self.pos)))
        code.put_gotref(iterator_temp)
        rhs.generate_disposal_code(code)

        for item in self.unpacked_items:
            item.allocate(code)
        code.globalstate.use_utility_code(unpacking_utility_code)
        for i in range(len(fixed_args_left)):
            item = self.unpacked_items[i]
            unpack_code = "__Pyx_UnpackItem(%s, %d)" % (
                iterator_temp, i)
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
            target_list, iterator_temp,
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

        code.put_decref_clear(iterator_temp, py_object_type)
        code.funcstate.release_temp(iterator_temp)

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
            for child in self.args:
                if not child.is_literal:
                    break
            else:
                self.is_temp = 0
                self.is_literal = 1

    def is_simple(self):
        # either temp or constant => always simple
        return True

    def nonlocally_immutable(self):
        # either temp or constant => always safe
        return True

    def calculate_result_code(self):
        if len(self.args) > 0:
            return self.result_code
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
        if self.is_literal:
            # non-empty cached tuple => result is global constant,
            # creation code goes into separate code writer
            self.result_code = code.get_py_const(py_object_type, 'tuple_', cleanup_level=2)
            code = code.get_cached_constants_writer()
            code.mark_pos(self.pos)

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
        if self.is_literal:
            code.put_giveref(self.py_result())

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
    type = list_type

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
        self.obj_conversion_errors = held_errors()
        release_errors(ignore=True)

    def coerce_to(self, dst_type, env):
        if dst_type.is_pyobject:
            for err in self.obj_conversion_errors:
                report_error(err)
            self.obj_conversion_errors = []
            if not self.type.subtype_of(dst_type):
                error(self.pos, "Cannot coerce list to type '%s'" % dst_type)
        elif dst_type.is_ptr and dst_type.base_type is not PyrexTypes.c_void_type:
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


class ScopedExprNode(ExprNode):
    # Abstract base class for ExprNodes that have their own local
    # scope, such as generator expressions.
    #
    # expr_scope    Scope  the inner scope of the expression

    subexprs = []
    expr_scope = None

    # does this node really have a local scope, e.g. does it leak loop
    # variables or not?  non-leaking Py3 behaviour is default, except
    # for list comprehensions where the behaviour differs in Py2 and
    # Py3 (set in Parsing.py based on parser context)
    has_local_scope = True

    def init_scope(self, outer_scope, expr_scope=None):
        if expr_scope is not None:
            self.expr_scope = expr_scope
        elif self.has_local_scope:
            self.expr_scope = Symtab.GeneratorExpressionScope(outer_scope)
        else:
            self.expr_scope = None

    def analyse_declarations(self, env):
        self.init_scope(env)

    def analyse_scoped_declarations(self, env):
        # this is called with the expr_scope as env
        pass

    def analyse_types(self, env):
        # no recursion here, the children will be analysed separately below
        pass

    def analyse_scoped_expressions(self, env):
        # this is called with the expr_scope as env
        pass

    def generate_evaluation_code(self, code):
        # set up local variables and free their references on exit
        generate_inner_evaluation_code = super(ScopedExprNode, self).generate_evaluation_code
        if not self.has_local_scope or not self.expr_scope.var_entries:
            # no local variables => delegate, done
            generate_inner_evaluation_code(code)
            return

        code.putln('{ /* enter inner scope */')
        py_entries = []
        for entry in self.expr_scope.var_entries:
            if not entry.in_closure:
                code.put_var_declaration(entry)
                if entry.type.is_pyobject and entry.used:
                    py_entries.append(entry)
        if not py_entries:
            # no local Python references => no cleanup required
            generate_inner_evaluation_code(code)
            code.putln('} /* exit inner scope */')
            return
        for entry in py_entries:
            code.put_init_var_to_py_none(entry)

        # must free all local Python references at each exit point
        old_loop_labels = tuple(code.new_loop_labels())
        old_error_label = code.new_error_label()

        generate_inner_evaluation_code(code)

        # normal (non-error) exit
        for entry in py_entries:
            code.put_var_decref(entry)

        # error/loop body exit points
        exit_scope = code.new_label('exit_scope')
        code.put_goto(exit_scope)
        for label, old_label in ([(code.error_label, old_error_label)] +
                                 list(zip(code.get_loop_labels(), old_loop_labels))):
            if code.label_used(label):
                code.put_label(label)
                for entry in py_entries:
                    code.put_var_decref(entry)
                code.put_goto(old_label)
        code.put_label(exit_scope)
        code.putln('} /* exit inner scope */')

        code.set_loop_labels(old_loop_labels)
        code.error_label = old_error_label


class ComprehensionNode(ScopedExprNode):
    subexprs = ["target"]
    child_attrs = ["loop", "append"]

    def infer_type(self, env):
        return self.target.infer_type(env)

    def analyse_declarations(self, env):
        self.append.target = self # this is used in the PyList_Append of the inner loop
        self.init_scope(env)

    def analyse_scoped_declarations(self, env):
        self.loop.analyse_declarations(env)

    def analyse_types(self, env):
        self.target.analyse_expressions(env)
        self.type = self.target.type
        if not self.has_local_scope:
            self.loop.analyse_expressions(env)

    def analyse_scoped_expressions(self, env):
        if self.has_local_scope:
            self.loop.analyse_expressions(env)

    def may_be_none(self):
        return False

    def calculate_result_code(self):
        return self.target.result()

    def generate_result_code(self, code):
        self.generate_operation_code(code)

    def generate_operation_code(self, code):
        self.loop.generate_execution_code(code)

    def annotate(self, code):
        self.loop.annotate(code)


class ComprehensionAppendNode(Node):
    # Need to be careful to avoid infinite recursion:
    # target must not be in child_attrs/subexprs

    child_attrs = ['expr']

    type = PyrexTypes.c_int_type

    def analyse_expressions(self, env):
        self.expr.analyse_expressions(env)
        if not self.expr.type.is_pyobject:
            self.expr = self.expr.coerce_to_pyobject(env)

    def generate_execution_code(self, code):
        if self.target.type is list_type:
            function = "PyList_Append"
        elif self.target.type is set_type:
            function = "PySet_Add"
        else:
            raise InternalError(
                "Invalid type for comprehension node: %s" % self.target.type)

        self.expr.generate_evaluation_code(code)
        code.putln(code.error_goto_if("%s(%s, (PyObject*)%s)" % (
            function,
            self.target.result(),
            self.expr.result()
            ), self.pos))
        self.expr.generate_disposal_code(code)
        self.expr.free_temps(code)

    def generate_function_definitions(self, env, code):
        self.expr.generate_function_definitions(env, code)

    def annotate(self, code):
        self.expr.annotate(code)

class DictComprehensionAppendNode(ComprehensionAppendNode):
    child_attrs = ['key_expr', 'value_expr']

    def analyse_expressions(self, env):
        self.key_expr.analyse_expressions(env)
        if not self.key_expr.type.is_pyobject:
            self.key_expr = self.key_expr.coerce_to_pyobject(env)
        self.value_expr.analyse_expressions(env)
        if not self.value_expr.type.is_pyobject:
            self.value_expr = self.value_expr.coerce_to_pyobject(env)

    def generate_execution_code(self, code):
        self.key_expr.generate_evaluation_code(code)
        self.value_expr.generate_evaluation_code(code)
        code.putln(code.error_goto_if("PyDict_SetItem(%s, (PyObject*)%s, (PyObject*)%s)" % (
            self.target.result(),
            self.key_expr.result(),
            self.value_expr.result()
            ), self.pos))
        self.key_expr.generate_disposal_code(code)
        self.key_expr.free_temps(code)
        self.value_expr.generate_disposal_code(code)
        self.value_expr.free_temps(code)

    def generate_function_definitions(self, env, code):
        self.key_expr.generate_function_definitions(env, code)
        self.value_expr.generate_function_definitions(env, code)

    def annotate(self, code):
        self.key_expr.annotate(code)
        self.value_expr.annotate(code)


class InlinedGeneratorExpressionNode(ScopedExprNode):
    # An inlined generator expression for which the result is
    # calculated inside of the loop.  This will only be created by
    # transforms when replacing builtin calls on generator
    # expressions.
    #
    # loop           ForStatNode      the for-loop, not containing any YieldExprNodes
    # result_node    ResultRefNode    the reference to the result value temp
    # orig_func      String           the name of the builtin function this node replaces

    child_attrs = ["loop"]
    loop_analysed = False
    type = py_object_type

    def analyse_scoped_declarations(self, env):
        self.loop.analyse_declarations(env)

    def analyse_types(self, env):
        if not self.has_local_scope:
            self.loop.analyse_expressions(env)
        self.is_temp = True

    def may_be_none(self):
        return False

    def annotate(self, code):
        self.loop.annotate(code)

    def infer_type(self, env):
        return self.result_node.infer_type(env)

    def analyse_types(self, env):
        if not self.has_local_scope:
            self.loop_analysed = True
            self.loop.analyse_expressions(env)
        self.type = self.result_node.type
        self.is_temp = True

    def analyse_scoped_expressions(self, env):
        self.loop_analysed = True
        if self.has_local_scope:
            self.loop.analyse_expressions(env)

    def coerce_to(self, dst_type, env):
        if self.orig_func == 'sum' and dst_type.is_numeric and not self.loop_analysed:
            # We can optimise by dropping the aggregation variable and
            # the add operations into C.  This can only be done safely
            # before analysing the loop body, after that, the result
            # reference type will have infected expressions and
            # assignments.
            self.result_node.type = self.type = dst_type
            return self
        return super(InlinedGeneratorExpressionNode, self).coerce_to(dst_type, env)

    def generate_result_code(self, code):
        self.result_node.result_code = self.result()
        self.loop.generate_execution_code(code)


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

    def may_be_none(self):
        return False

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

    def may_be_none(self):
        return False

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

class ModuleNameMixin(object):
    def set_mod_name(self, env):
        self.module_name = env.global_scope().qualified_name

    def get_py_mod_name(self, code):
        return code.get_py_string_const(
                 self.module_name, identifier=True)

class ClassNode(ExprNode, ModuleNameMixin):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a class object given
    #  a name, tuple of bases and class dictionary.
    #
    #  name         EncodedString      Name of the class
    #  bases        ExprNode           Base class tuple
    #  dict         ExprNode           Class dict (not owned by this node)
    #  doc          ExprNode or None   Doc string
    #  module_name  EncodedString      Name of defining module

    subexprs = ['bases', 'doc']

    def analyse_types(self, env):
        self.bases.analyse_types(env)
        if self.doc:
            self.doc.analyse_types(env)
            self.doc = self.doc.coerce_to_pyobject(env)
        self.type = py_object_type
        self.is_temp = 1
        env.use_utility_code(create_class_utility_code);
        #TODO(craig,haoyu) This should be moved to a better place
        self.set_mod_name(env)

    def may_be_none(self):
        return True

    gil_message = "Constructing Python class"

    def generate_result_code(self, code):
        cname = code.intern_identifier(self.name)

        if self.doc:
            code.put_error_if_neg(self.pos,
                'PyDict_SetItemString(%s, "__doc__", %s)' % (
                    self.dict.py_result(),
                    self.doc.py_result()))
        py_mod_name = self.get_py_mod_name(code)
        code.putln(
            '%s = __Pyx_CreateClass(%s, %s, %s, %s); %s' % (
                self.result(),
                self.bases.py_result(),
                self.dict.py_result(),
                cname,
                py_mod_name,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class Py3ClassNode(ExprNode):
    #  Helper class used in the implementation of Python3+
    #  class definitions. Constructs a class object given
    #  a name, tuple of bases and class dictionary.
    #
    #  name         EncodedString      Name of the class
    #  dict         ExprNode           Class dict (not owned by this node)
    #  module_name  EncodedString      Name of defining module

    subexprs = []

    def analyse_types(self, env):
        self.type = py_object_type
        self.is_temp = 1

    def may_be_none(self):
        return True

    gil_message = "Constructing Python class"

    def generate_result_code(self, code):
        code.globalstate.use_utility_code(create_py3class_utility_code)
        cname = code.intern_identifier(self.name)
        code.putln(
            '%s = __Pyx_Py3ClassCreate(%s, %s, %s, %s, %s); %s' % (
                self.result(),
                self.metaclass.result(),
                cname,
                self.bases.py_result(),
                self.dict.py_result(),
                self.mkw.py_result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())

class KeywordArgsNode(ExprNode):
    # Helper class for keyword arguments
    #
    # keyword_args ExprNode or None     Keyword arguments
    # starstar_arg ExprNode or None     Extra arguments

    subexprs = ['keyword_args', 'starstar_arg']

    def analyse_types(self, env):
        if self.keyword_args:
            self.keyword_args.analyse_types(env)
        if self.starstar_arg:
            self.starstar_arg.analyse_types(env)
            # make sure we have a Python object as **kwargs mapping
            self.starstar_arg = \
                self.starstar_arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.is_temp = 1

    gil_message = "Constructing Keyword Args"

    def generate_result_code(self, code):
        if self.keyword_args and self.starstar_arg:
            code.put_error_if_neg(self.pos,
                "PyDict_Update(%s, %s)" % (
                    self.keyword_args.py_result(),
                    self.starstar_arg.py_result()))
        if self.keyword_args:
            code.putln("%s = %s;" % (self.result(), self.keyword_args.result()))
            code.put_incref(self.keyword_args.result(), self.keyword_args.ctype())
        elif self.starstar_arg:
            code.putln(
                "%s = PyDict_Copy(%s); %s" % (
                    self.result(),
                    self.starstar_arg.py_result(),
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())
        else:
            code.putln(
                "%s = PyDict_New(); %s" % (
                    self.result(),
                    code.error_goto_if_null(self.result(), self.pos)))
            code.put_gotref(self.py_result())

class PyClassMetaclassNode(ExprNode):
    # Helper class holds Python3 metaclass object
    #
    #  bases        ExprNode           Base class tuple (not owned by this node)
    #  mkw          ExprNode           Class keyword arguments (not owned by this node)

    subexprs = []

    def analyse_types(self, env):
        self.type = py_object_type
        self.is_temp = True

    def may_be_none(self):
        return True

    def generate_result_code(self, code):
        code.putln(
            "%s = __Pyx_Py3MetaclassGet(%s, %s); %s" % (
                self.result(),
                self.bases.result(),
                self.mkw.result(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())

class PyClassNamespaceNode(ExprNode, ModuleNameMixin):
    # Helper class holds Python3 namespace object
    #
    # All this are not owned by this node
    #  metaclass    ExprNode           Metaclass object
    #  bases        ExprNode           Base class tuple
    #  mkw          ExprNode           Class keyword arguments
    #  doc          ExprNode or None   Doc string (owned)

    subexprs = ['doc']

    def analyse_types(self, env):
        self.bases.analyse_types(env)
        if self.doc:
            self.doc.analyse_types(env)
            self.doc = self.doc.coerce_to_pyobject(env)
        self.type = py_object_type
        self.is_temp = 1
        #TODO(craig,haoyu) This should be moved to a better place
        self.set_mod_name(env)

    def may_be_none(self):
        return True

    def generate_result_code(self, code):
        cname = code.intern_identifier(self.name)
        py_mod_name = self.get_py_mod_name(code)
        if self.doc:
            doc_code = self.doc.result()
        else:
            doc_code = '(PyObject *) NULL'
        code.putln(
            "%s = __Pyx_Py3MetaclassPrepare(%s, %s, %s, %s, %s, %s); %s" % (
                self.result(),
                self.metaclass.result(),
                self.bases.result(),
                cname,
                self.mkw.result(),
                py_mod_name,
                doc_code,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())

class BoundMethodNode(ExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs an bound method
    #  object from a class and a function.
    #
    #  function      ExprNode   Function object
    #  self_object   ExprNode   self object

    subexprs = ['function']

    def analyse_types(self, env):
        self.function.analyse_types(env)
        self.type = py_object_type
        self.is_temp = 1

    gil_message = "Constructing an bound method"

    def generate_result_code(self, code):
        code.putln(
            "%s = PyMethod_New(%s, %s, (PyObject*)%s->ob_type); %s" % (
                self.result(),
                self.function.py_result(),
                self.self_object.py_result(),
                self.self_object.py_result(),
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

    def may_be_none(self):
        return False

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


class PyCFunctionNode(ExprNode, ModuleNameMixin):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a PyCFunction object
    #  from a PyMethodDef struct.
    #
    #  pymethdef_cname   string             PyMethodDef structure
    #  self_object       ExprNode or None
    #  binding           bool
    #  module_name       EncodedString      Name of defining module

    subexprs = []
    self_object = None
    binding = False

    type = py_object_type
    is_temp = 1

    def analyse_types(self, env):
        if self.binding:
            env.use_utility_code(binding_cfunc_utility_code)

        #TODO(craig,haoyu) This should be moved to a better place
        self.set_mod_name(env)

    def may_be_none(self):
        return False

    gil_message = "Constructing Python function"

    def self_result_code(self):
        if self.self_object is None:
            self_result = "NULL"
        else:
            self_result = self.self_object.py_result()
        return self_result

    def generate_result_code(self, code):
        if self.binding:
            constructor = "%s_NewEx" % Naming.binding_cfunc
        else:
            constructor = "PyCFunction_NewEx"
        py_mod_name = self.get_py_mod_name(code)
        code.putln(
            '%s = %s(&%s, %s, %s); %s' % (
                self.result(),
                constructor,
                self.pymethdef_cname,
                self.self_result_code(),
                py_mod_name,
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())

class InnerFunctionNode(PyCFunctionNode):
    # Special PyCFunctionNode that depends on a closure class
    #

    binding = True
    needs_self_code = True

    def self_result_code(self):
        if self.needs_self_code:
            return "((PyObject*)%s)" % (Naming.cur_scope_cname)
        return "NULL"

class LambdaNode(InnerFunctionNode):
    # Lambda expression node (only used as a function reference)
    #
    # args          [CArgDeclNode]         formal arguments
    # star_arg      PyArgDeclNode or None  * argument
    # starstar_arg  PyArgDeclNode or None  ** argument
    # lambda_name   string                 a module-globally unique lambda name
    # result_expr   ExprNode
    # def_node      DefNode                the underlying function 'def' node

    child_attrs = ['def_node']

    def_node = None
    name = StringEncoding.EncodedString('<lambda>')

    def analyse_declarations(self, env):
        self.def_node.analyse_declarations(env)
        self.pymethdef_cname = self.def_node.entry.pymethdef_cname
        env.add_lambda_def(self.def_node)


class GeneratorExpressionNode(LambdaNode):
    # A generator expression, e.g.  (i for i in range(10))
    #
    # Result is a generator.
    #
    # loop      ForStatNode   the for-loop, containing a YieldExprNode
    # def_node  DefNode       the underlying generator 'def' node

    name = StringEncoding.EncodedString('genexpr')
    binding = False

    def analyse_declarations(self, env):
        self.def_node.no_assignment_synthesis = True
        self.def_node.analyse_declarations(env)
        env.add_lambda_def(self.def_node)

    def generate_result_code(self, code):
        code.putln(
            '%s = %s(%s, NULL); %s' % (
                self.result(),
                self.def_node.entry.func_cname,
                self.self_result_code(),
                code.error_goto_if_null(self.result(), self.pos)))
        code.put_gotref(self.py_result())


class YieldExprNode(ExprNode):
    # Yield expression node
    #
    # arg         ExprNode   the value to return from the generator
    # label_name  string     name of the C label used for this yield
    # label_num   integer    yield label number

    subexprs = ['arg']
    type = py_object_type
    label_num = 0

    def analyse_types(self, env):
        if not self.label_num:
            error(self.pos, "'yield' not supported here")
        self.is_temp = 1
        if self.arg is not None:
            self.arg.analyse_types(env)
            if not self.arg.type.is_pyobject:
                self.arg = self.arg.coerce_to_pyobject(env)
        env.use_utility_code(generator_utility_code)

    def generate_evaluation_code(self, code):
        self.label_name = code.new_label('resume_from_yield')
        code.use_label(self.label_name)
        if self.arg:
            self.arg.generate_evaluation_code(code)
            self.arg.make_owned_reference(code)
            code.putln(
                "%s = %s;" % (
                    Naming.retval_cname,
                    self.arg.result_as(py_object_type)))
            self.arg.generate_post_assignment_code(code)
            #self.arg.generate_disposal_code(code)
            self.arg.free_temps(code)
        else:
            code.put_init_to_py_none(Naming.retval_cname, py_object_type)
        saved = []
        code.funcstate.closure_temps.reset()
        for cname, type, manage_ref in code.funcstate.temps_in_use():
            save_cname = code.funcstate.closure_temps.allocate_temp(type)
            saved.append((cname, save_cname, type))
            if type.is_pyobject:
                code.put_xgiveref(cname)
            code.putln('%s->%s = %s;' % (Naming.cur_scope_cname, save_cname, cname))

        code.put_xgiveref(Naming.retval_cname)
        code.put_finish_refcount_context()
        code.putln("/* return from generator, yielding value */")
        code.putln("%s->%s.resume_label = %d;" % (Naming.cur_scope_cname, Naming.obj_base_cname, self.label_num))
        code.putln("return %s;" % Naming.retval_cname);
        code.put_label(self.label_name)
        for cname, save_cname, type in saved:
            code.putln('%s = %s->%s;' % (cname, Naming.cur_scope_cname, save_cname))
            if type.is_pyobject:
                code.putln('%s->%s = 0;' % (Naming.cur_scope_cname, save_cname))
            if type.is_pyobject:
                code.put_xgotref(cname)
        if self.result_is_used:
            self.allocate_temp_result(code)
            code.putln('%s = %s; %s' %
                       (self.result(), Naming.sent_value_cname,
                        code.error_goto_if_null(self.result(), self.pos)))
            code.put_incref(self.result(), py_object_type)
        else:
            code.putln(code.error_goto_if_null(Naming.sent_value_cname, self.pos))

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
        operand_type = self.operand.infer_type(env)
        if operand_type.is_pyobject:
            return py_object_type
        else:
            return operand_type

    def analyse_types(self, env):
        self.operand.analyse_types(env)
        if self.is_py_operation():
            self.coerce_operand_to_pyobject(env)
            self.type = py_object_type
            self.is_temp = 1
        elif self.is_cpp_operation():
            self.analyse_cpp_operation(env)
        else:
            self.analyse_c_operation(env)

    def check_const(self):
        return self.operand.check_const()

    def is_py_operation(self):
        return self.operand.type.is_pyobject

    def nogil_check(self, env):
        if self.is_py_operation():
            self.gil_error()

    def is_cpp_operation(self):
        type = self.operand.type
        return type.is_cpp_class

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

    def analyse_cpp_operation(self, env):
        type = self.operand.type
        if type.is_ptr:
            type = type.base_type
        function = type.scope.lookup("operator%s" % self.operator)
        if not function:
            error(self.pos, "'%s' operator not defined for %s"
                % (self.operator, type))
            self.type_error()
            return
        func_type = function.type
        if func_type.is_ptr:
            func_type = func_type.base_type
        self.type = func_type.return_type


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
        self.type = PyrexTypes.widest_numeric_type(
            self.operand.type, PyrexTypes.c_int_type)

    def py_operation_function(self):
        return "PyNumber_Positive"

    def calculate_result_code(self):
        if self.is_cpp_operation():
            return "(+%s)" % self.operand.result()
        else:
            return self.operand.result()


class UnaryMinusNode(UnopNode):
    #  unary '-' operator

    operator = '-'

    def analyse_c_operation(self, env):
        if self.operand.type.is_numeric:
            self.type = PyrexTypes.widest_numeric_type(
                self.operand.type, PyrexTypes.c_int_type)
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
            self.type = PyrexTypes.widest_numeric_type(
                self.operand.type, PyrexTypes.c_int_type)
        else:
            self.type_error()

    def py_operation_function(self):
        return "PyNumber_Invert"

    def calculate_result_code(self):
        return "(~%s)" % self.operand.result()


class CUnopNode(UnopNode):

    def is_py_operation(self):
        return False

class DereferenceNode(CUnopNode):
    #  unary * operator

    operator = '*'

    def analyse_c_operation(self, env):
        if self.operand.type.is_ptr:
            self.type = self.operand.type.base_type
        else:
            self.type_error()

    def calculate_result_code(self):
        return "(*%s)" % self.operand.result()


class DecrementIncrementNode(CUnopNode):
    #  unary ++/-- operator

    def analyse_c_operation(self, env):
        if self.operand.type.is_numeric:
            self.type = PyrexTypes.widest_numeric_type(
                self.operand.type, PyrexTypes.c_int_type)
        elif self.operand.type.is_ptr:
            self.type = self.operand.type
        else:
            self.type_error()

    def calculate_result_code(self):
        if self.is_prefix:
            return "(%s%s)" % (self.operator, self.operand.result())
        else:
            return "(%s%s)" % (self.operand.result(), self.operator)

def inc_dec_constructor(is_prefix, operator):
    return lambda pos, **kwds: DecrementIncrementNode(pos, is_prefix=is_prefix, operator=operator, **kwds)


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
        return IntNode(pos = operand.pos, value = str(-Utils.str_to_number(operand.value)))
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
            if self.type is bytes_type and self.operand.type.is_int:
                # FIXME: the type cast node isn't needed in this case
                # and can be dropped once analyse_types() can return a
                # different node
                self.operand = CoerceIntToBytesNode(self.operand, env)
            elif self.operand.type.can_coerce_to_pyobject(env):
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

    def is_simple(self):
        # either temp or a C cast => no side effects
        return True

    def nonlocally_immutable(self):
        return self.operand.nonlocally_immutable()

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

    def may_be_none(self):
        return False

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
    inplace = False

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
        self.analyse_operation(env)

    def analyse_operation(self, env):
        if self.is_py_operation():
            self.coerce_operands_to_pyobjects(env)
            self.type = self.result_type(self.operand1.type,
                                         self.operand2.type)
            assert self.type.is_pyobject
            self.is_temp = 1
        elif self.is_cpp_operation():
            self.analyse_cpp_operation(env)
        else:
            self.analyse_c_operation(env)

    def is_py_operation(self):
        return self.is_py_operation_types(self.operand1.type, self.operand2.type)

    def is_py_operation_types(self, type1, type2):
        return type1.is_pyobject or type2.is_pyobject

    def is_cpp_operation(self):
        return (self.operand1.type.is_cpp_class
            or self.operand2.type.is_cpp_class)

    def analyse_cpp_operation(self, env):
        type1 = self.operand1.type
        type2 = self.operand2.type
        entry = env.lookup_operator(self.operator, [self.operand1, self.operand2])
        if not entry:
            self.type_error()
            return
        func_type = entry.type
        if func_type.is_ptr:
            func_type = func_type.base_type
        if len(func_type.args) == 1:
            self.operand2 = self.operand2.coerce_to(func_type.args[0].type, env)
        else:
            self.operand1 = self.operand1.coerce_to(func_type.args[0].type, env)
            self.operand2 = self.operand2.coerce_to(func_type.args[1].type, env)
        self.type = func_type.return_type

    def result_type(self, type1, type2):
        if self.is_py_operation_types(type1, type2):
            if type2.is_string:
                type2 = Builtin.bytes_type
            if type1.is_string:
                type1 = Builtin.bytes_type
            elif self.operator == '%' \
                     and type1 in (Builtin.str_type, Builtin.unicode_type):
                # note that  b'%s' % b'abc'  doesn't work in Py3
                return type1
            if type1.is_builtin_type:
                if type1 is type2:
                    if self.operator in '**%+|&^':
                        # FIXME: at least these operators should be safe - others?
                        return type1
                elif self.operator == '*':
                    if type1 in (Builtin.bytes_type, Builtin.str_type, Builtin.unicode_type):
                        return type1
                    # multiplication of containers/numbers with an
                    # integer value always (?) returns the same type
                    if type2.is_int:
                        return type1
            elif type2.is_builtin_type and type1.is_int and self.operator == '*':
                # multiplication of containers/numbers with an
                # integer value always (?) returns the same type
                return type2
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
            if self.operator == '**':
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


class CBinopNode(BinopNode):

    def analyse_types(self, env):
        BinopNode.analyse_types(self, env)
        if self.is_py_operation():
            self.type = PyrexTypes.error_type

    def py_operation_function():
        return ""

    def calculate_result_code(self):
        return "(%s %s %s)" % (
            self.operand1.result(),
            self.operator,
            self.operand2.result())


def c_binop_constructor(operator):
    def make_binop_node(pos, **operands):
        return CBinopNode(pos, operator=operator, **operands)
    return make_binop_node

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
        if not self.infix or (type1.is_numeric and type2.is_numeric):
            self.operand1 = self.operand1.coerce_to(self.type, env)
            self.operand2 = self.operand2.coerce_to(self.type, env)

    def compute_c_result_type(self, type1, type2):
        if self.c_types_okay(type1, type2):
            widest_type = PyrexTypes.widest_numeric_type(type1, type2)
            if widest_type is PyrexTypes.c_bint_type:
                if self.operator not in '|^&':
                    # False + False == 0 # not False!
                    widest_type = PyrexTypes.c_int_type
            else:
                widest_type = PyrexTypes.widest_numeric_type(
                    widest_type, PyrexTypes.c_int_type)
            return widest_type
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

    def is_py_operation_types(self, type1, type2):
        return (type1.is_unicode_char or
                type2.is_unicode_char or
                BinopNode.is_py_operation_types(self, type1, type2))

    def py_operation_function(self):
        fuction = self.py_functions[self.operator]
        if self.inplace:
            fuction = fuction.replace('PyNumber_', 'PyNumber_InPlace')
        return fuction

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
                operand1, operand2)
            return func(operand1, operand2)
        except Exception, e:
            self.compile_time_value_error(e)

    def analyse_operation(self, env):
        if self.cdivision or env.directives['cdivision']:
            self.ctruedivision = False
        else:
            self.ctruedivision = self.truedivision
        NumBinopNode.analyse_operation(self, env)
        if self.is_cpp_operation():
            self.cdivision = True
        if not self.type.is_pyobject:
            self.zerodivision_check = (
                self.cdivision is None and not env.directives['cdivision']
                and (not self.operand2.has_constant_result() or
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
                code.put("if (__Pyx_cdivision_warning(%(FILENAME)s, "
                                                     "%(LINENO)s)) " % {
                    'FILENAME': Naming.filename_cname,
                    'LINENO':  Naming.lineno_cname,
                    })

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
                    self.type.specialization_name(),
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
                    self.type.specialization_name(),
                    self.operand1.result(),
                    self.operand2.result())

class PowNode(NumBinopNode):
    #  '**' operator.

    def analyse_c_operation(self, env):
        NumBinopNode.analyse_c_operation(self, env)
        if self.type.is_complex:
            if self.type.real_type.is_float:
                self.operand1 = self.operand1.coerce_to(self.type, env)
                self.operand2 = self.operand2.coerce_to(self.type, env)
                self.pow_func = "__Pyx_c_pow" + self.type.real_type.math_h_modifier
            else:
                error(self.pos, "complex int powers not supported")
                self.pow_func = "<error>"
        elif self.type.is_float:
            self.pow_func = "pow" + self.type.math_h_modifier
        else:
            self.pow_func = "__Pyx_pow_%s" % self.type.declaration_code('').replace(' ', '_')
            env.use_utility_code(
                    int_pow_utility_code.specialize(func_name=self.pow_func,
                                                type=self.type.declaration_code('')))

    def calculate_result_code(self):
        # Work around MSVC overloading ambiguity.
        def typecast(operand):
            if self.type == operand.type:
                return operand.result()
            else:
                return self.type.cast_code(operand.result())
        return "%s(%s, %s)" % (
            self.pow_func,
            typecast(self.operand1),
            typecast(self.operand2))


# Note: This class is temporarily "shut down" into an ineffective temp
# allocation mode.
#
# More sophisticated temp reuse was going on before, one could have a
# look at adding this again after /all/ classes are converted to the
# new temp scheme. (The temp juggling cannot work otherwise).
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
        return PyrexTypes.independent_spanning_type(type1, type2)

    def may_be_none(self):
        if self.operator == 'or':
            return self.operand2.may_be_none()
        else:
            return self.operand1.may_be_none() or self.operand2.may_be_none()

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
        return BoolBinopNode(
            self.pos,
            operator = self.operator,
            operand1 = self.operand1.coerce_to_boolean(env),
            operand2 = self.operand2.coerce_to_boolean(env),
            type = PyrexTypes.c_bint_type,
            is_temp = self.is_temp)

    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        self.type = PyrexTypes.independent_spanning_type(self.operand1.type, self.operand2.type)
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
        return PyrexTypes.independent_spanning_type(self.true_val.infer_type(env),
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
        self.type = PyrexTypes.independent_spanning_type(self.true_val.type, self.false_val.type)
        if self.true_val.type.is_pyobject or self.false_val.type.is_pyobject:
            self.true_val = self.true_val.coerce_to(self.type, env)
            self.false_val = self.false_val.coerce_to(self.type, env)
        self.is_temp = 1
        if self.type == PyrexTypes.error_type:
            self.type_error()

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

    special_bool_cmp_function = None

    def infer_type(self, env):
        # TODO: Actually implement this (after merging with -unstable).
        return py_object_type

    def calculate_cascaded_constant_result(self, operand1_result):
        func = compile_time_binary_operators[self.operator]
        operand2_result = self.operand2.constant_result
        result = func(operand1_result, operand2_result)
        if self.cascade:
            self.cascade.calculate_cascaded_constant_result(operand2_result)
            if self.cascade.constant_result:
                self.constant_result = result and self.cascade.constant_result
        else:
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
                result = result and cascade.cascaded_compile_time_value(operand2, denv)
        return result

    def is_cpp_comparison(self):
        return self.operand1.type.is_cpp_class or self.operand2.type.is_cpp_class

    def find_common_int_type(self, env, op, operand1, operand2):
        # type1 != type2 and at least one of the types is not a C int
        type1 = operand1.type
        type2 = operand2.type
        type1_can_be_int = False
        type2_can_be_int = False

        if isinstance(operand1, (StringNode, BytesNode, UnicodeNode)) \
               and operand1.can_coerce_to_char_literal():
            type1_can_be_int = True
        if isinstance(operand2, (StringNode, BytesNode, UnicodeNode)) \
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

        if new_common_type.is_string and (isinstance(operand1, BytesNode) or
                                          isinstance(operand2, BytesNode)):
            # special case when comparing char* to bytes literal: must
            # compare string values!
            new_common_type = bytes_type

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
        return (not self.is_ptr_contains()
            and not self.is_c_string_contains()
            and (self.has_python_operands()
                 or (self.cascade and self.cascade.is_python_comparison())
                 or self.operator in ('in', 'not_in')))

    def coerce_operands_to(self, dst_type, env):
        operand2 = self.operand2
        if operand2.type != dst_type:
            self.operand2 = operand2.coerce_to(dst_type, env)
        if self.cascade:
            self.cascade.coerce_operands_to(dst_type, env)

    def is_python_result(self):
        return ((self.has_python_operands() and
                 self.special_bool_cmp_function is None and
                 self.operator not in ('is', 'is_not', 'in', 'not_in') and
                 not self.is_c_string_contains() and
                 not self.is_ptr_contains())
            or (self.cascade and self.cascade.is_python_result()))

    def is_c_string_contains(self):
        return self.operator in ('in', 'not_in') and \
               ((self.operand1.type.is_int
                 and (self.operand2.type.is_string or self.operand2.type is bytes_type)) or
                (self.operand1.type.is_unicode_char
                 and self.operand2.type is unicode_type))

    def is_ptr_contains(self):
        if self.operator in ('in', 'not_in'):
            container_type = self.operand2.type
            return (container_type.is_ptr or container_type.is_array) \
                and not container_type.is_string

    def find_special_bool_compare_function(self, env):
        if self.operator in ('==', '!='):
            type1, type2 = self.operand1.type, self.operand2.type
            if type1.is_pyobject and type2.is_pyobject:
                if type1 is Builtin.unicode_type or type2 is Builtin.unicode_type:
                    env.use_utility_code(pyunicode_equals_utility_code)
                    self.special_bool_cmp_function = "__Pyx_PyUnicode_Equals"
                    return True
                elif type1 is Builtin.bytes_type or type2 is Builtin.bytes_type:
                    env.use_utility_code(pybytes_equals_utility_code)
                    self.special_bool_cmp_function = "__Pyx_PyBytes_Equals"
                    return True
                elif type1 is Builtin.str_type or type2 is Builtin.str_type:
                    env.use_utility_code(pystr_equals_utility_code)
                    self.special_bool_cmp_function = "__Pyx_PyString_Equals"
                    return True
        return False

    def generate_operation_code(self, code, result_code,
            operand1, op , operand2):
        if self.type.is_pyobject:
            coerce_result = "__Pyx_PyBool_FromLong"
        else:
            coerce_result = ""
        if 'not' in op:
            negation = "!"
        else:
            negation = ""
        if self.special_bool_cmp_function:
            if operand1.type.is_pyobject:
                result1 = operand1.py_result()
            else:
                result1 = operand1.result()
            if operand2.type.is_pyobject:
                result2 = operand2.py_result()
            else:
                result2 = operand2.result()
            code.putln("%s = %s(%s, %s, %s); %s" % (
                result_code,
                self.special_bool_cmp_function,
                result1,
                result2,
                richcmp_constants[op],
                code.error_goto_if_neg(result_code, self.pos)))
        elif op == 'in' or op == 'not_in':
            code.globalstate.use_utility_code(contains_utility_code)
            if self.type.is_pyobject:
                coerce_result = "__Pyx_PyBoolOrNull_FromLong"
            if op == 'not_in':
                negation = "__Pyx_NegateNonNeg"
            if operand2.type is dict_type:
                method = "PyDict_Contains"
            else:
                method = "PySequence_Contains"
            if self.type.is_pyobject:
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

contains_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE long __Pyx_NegateNonNeg(long b) { return unlikely(b < 0) ? b : !b; }
static CYTHON_INLINE PyObject* __Pyx_PyBoolOrNull_FromLong(long b) {
    return unlikely(b < 0) ? NULL : __Pyx_PyBool_FromLong(b);
}
""")

char_in_bytes_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE int __Pyx_BytesContains(PyObject* bytes, char character); /*proto*/
""",
impl="""
static CYTHON_INLINE int __Pyx_BytesContains(PyObject* bytes, char character) {
    const Py_ssize_t length = PyBytes_GET_SIZE(bytes);
    char* char_start = PyBytes_AS_STRING(bytes);
    char* pos;
    for (pos=char_start; pos < char_start+length; pos++) {
        if (character == pos[0]) return 1;
    }
    return 0;
}
""")

pyunicode_in_unicode_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE int __Pyx_UnicodeContains(PyObject* unicode, Py_UNICODE character); /*proto*/
""",
impl="""
static CYTHON_INLINE int __Pyx_UnicodeContains(PyObject* unicode, Py_UNICODE character) {
    Py_UNICODE* pos;
    const Py_ssize_t length = PyUnicode_GET_SIZE(unicode);
    Py_UNICODE* char_start = PyUnicode_AS_UNICODE(unicode);

    for (pos=char_start; pos < char_start+length; pos++) {
        if (unlikely(character == pos[0])) return 1;
    }
    return 0;
}
""")

py_ucs4_in_unicode_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE int __Pyx_UnicodeContainsUCS4(PyObject* unicode, Py_UCS4 character); /*proto*/
""",
# additionally handles surrogate pairs in 16bit Unicode builds
impl="""
static CYTHON_INLINE int __Pyx_UnicodeContainsUCS4(PyObject* unicode, Py_UCS4 character) {
    Py_UNICODE* pos;
    Py_UNICODE uchar;
    const Py_ssize_t length = PyUnicode_GET_SIZE(unicode);
    Py_UNICODE* char_start = PyUnicode_AS_UNICODE(unicode);

    #if Py_UNICODE_SIZE == 2
    if (unlikely(character > 65535)) {
        Py_UNICODE high_val, low_val;
        high_val = (Py_UNICODE) (0xD800 | (((character - 0x10000) >> 10) & ((1<<10)-1)));
        low_val  = (Py_UNICODE) (0xDC00 | ( (character - 0x10000)        & ((1<<10)-1)));
        for (pos=char_start; pos < char_start+length-1; pos++) {
            if (unlikely(high_val == pos[0]) & unlikely(low_val == pos[1])) return 1;
        }
        return 0;
    }
    #endif
    uchar = (Py_UNICODE) character;
    for (pos=char_start; pos < char_start+length; pos++) {
        if (unlikely(uchar == pos[0])) return 1;
    }
    return 0;
}
""")

pyunicode_equals_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals); /*proto*/
""",
impl="""
static CYTHON_INLINE int __Pyx_PyUnicode_Equals(PyObject* s1, PyObject* s2, int equals) {
    if (s1 == s2) {   /* as done by PyObject_RichCompareBool(); also catches the (interned) empty string */
        return (equals == Py_EQ);
    } else if (PyUnicode_CheckExact(s1) & PyUnicode_CheckExact(s2)) {
        if (PyUnicode_GET_SIZE(s1) != PyUnicode_GET_SIZE(s2)) {
            return (equals == Py_NE);
        } else if (PyUnicode_GET_SIZE(s1) == 1) {
            if (equals == Py_EQ)
                return (PyUnicode_AS_UNICODE(s1)[0] == PyUnicode_AS_UNICODE(s2)[0]);
            else
                return (PyUnicode_AS_UNICODE(s1)[0] != PyUnicode_AS_UNICODE(s2)[0]);
        } else {
            int result = PyUnicode_Compare(s1, s2);
            if ((result == -1) && unlikely(PyErr_Occurred()))
                return -1;
            return (equals == Py_EQ) ? (result == 0) : (result != 0);
        }
    } else if ((s1 == Py_None) & PyUnicode_CheckExact(s2)) {
        return (equals == Py_NE);
    } else if ((s2 == Py_None) & PyUnicode_CheckExact(s1)) {
        return (equals == Py_NE);
    } else {
        int result;
        PyObject* py_result = PyObject_RichCompare(s1, s2, equals);
        if (!py_result)
            return -1;
        result = __Pyx_PyObject_IsTrue(py_result);
        Py_DECREF(py_result);
        return result;
    }
}
""")

pybytes_equals_utility_code = UtilityCode(
proto="""
static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals); /*proto*/
""",
impl="""
static CYTHON_INLINE int __Pyx_PyBytes_Equals(PyObject* s1, PyObject* s2, int equals) {
    if (s1 == s2) {   /* as done by PyObject_RichCompareBool(); also catches the (interned) empty string */
        return (equals == Py_EQ);
    } else if (PyBytes_CheckExact(s1) & PyBytes_CheckExact(s2)) {
        if (PyBytes_GET_SIZE(s1) != PyBytes_GET_SIZE(s2)) {
            return (equals == Py_NE);
        } else if (PyBytes_GET_SIZE(s1) == 1) {
            if (equals == Py_EQ)
                return (PyBytes_AS_STRING(s1)[0] == PyBytes_AS_STRING(s2)[0]);
            else
                return (PyBytes_AS_STRING(s1)[0] != PyBytes_AS_STRING(s2)[0]);
        } else {
            int result = memcmp(PyBytes_AS_STRING(s1), PyBytes_AS_STRING(s2), PyBytes_GET_SIZE(s1));
            return (equals == Py_EQ) ? (result == 0) : (result != 0);
        }
    } else if ((s1 == Py_None) & PyBytes_CheckExact(s2)) {
        return (equals == Py_NE);
    } else if ((s2 == Py_None) & PyBytes_CheckExact(s1)) {
        return (equals == Py_NE);
    } else {
        int result;
        PyObject* py_result = PyObject_RichCompare(s1, s2, equals);
        if (!py_result)
            return -1;
        result = __Pyx_PyObject_IsTrue(py_result);
        Py_DECREF(py_result);
        return result;
    }
}
""",
requires=[Builtin.include_string_h_utility_code])

pystr_equals_utility_code = UtilityCode(
proto="""
#if PY_MAJOR_VERSION >= 3
#define __Pyx_PyString_Equals __Pyx_PyUnicode_Equals
#else
#define __Pyx_PyString_Equals __Pyx_PyBytes_Equals
#endif
""",
requires=[pybytes_equals_utility_code, pyunicode_equals_utility_code])


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
        self.calculate_cascaded_constant_result(self.operand1.constant_result)

    def compile_time_value(self, denv):
        operand1 = self.operand1.compile_time_value(denv)
        return self.cascaded_compile_time_value(operand1, denv)

    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        if self.is_cpp_comparison():
            self.analyse_cpp_comparison(env)
            if self.cascade:
                error(self.pos, "Cascading comparison not yet supported for cpp types.")
            return
        if self.cascade:
            self.cascade.analyse_types(env)

        if self.operator in ('in', 'not_in'):
            if self.is_c_string_contains():
                self.is_pycmp = False
                common_type = None
                if self.cascade:
                    error(self.pos, "Cascading comparison not yet supported for 'int_val in string'.")
                    return
                if self.operand2.type is unicode_type:
                    self.uchar_test_type = PyrexTypes.widest_numeric_type(
                        self.operand1.type, PyrexTypes.c_py_unicode_type)
                    if self.uchar_test_type is PyrexTypes.c_py_unicode_type:
                        env.use_utility_code(pyunicode_in_unicode_utility_code)
                    else:
                        env.use_utility_code(py_ucs4_in_unicode_utility_code)
                else:
                    if self.operand1.type is PyrexTypes.c_uchar_type:
                        self.operand1 = self.operand1.coerce_to(PyrexTypes.c_char_type, env)
                    if self.operand2.type is not bytes_type:
                        self.operand2 = self.operand2.coerce_to(bytes_type, env)
                    env.use_utility_code(char_in_bytes_utility_code)
                self.operand2 = self.operand2.as_none_safe_node(
                    "argument of type 'NoneType' is not iterable")
            elif self.is_ptr_contains():
                if self.cascade:
                    error(self.pos, "Cascading comparison not yet supported for 'val in sliced pointer'.")
                self.type = PyrexTypes.c_bint_type
                # Will be transformed by IterationTransform
                return
            else:
                if self.operand2.type is dict_type:
                    self.operand2 = self.operand2.as_none_safe_node("'NoneType' object is not iterable")
                common_type = py_object_type
                self.is_pycmp = True
        elif self.find_special_bool_compare_function(env):
            common_type = None # if coercion needed, the method call above has already done it
            self.is_pycmp = False # result is bint
            self.is_temp = True # must check for error return
        else:
            common_type = self.find_common_type(env, self.operator, self.operand1)
            self.is_pycmp = common_type.is_pyobject

        if common_type is not None and not common_type.is_error:
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

    def analyse_cpp_comparison(self, env):
        type1 = self.operand1.type
        type2 = self.operand2.type
        entry = env.lookup_operator(self.operator, [self.operand1, self.operand2])
        if entry is None:
            error(self.pos, "Invalid types for '%s' (%s, %s)" %
                (self.operator, type1, type2))
            self.type = PyrexTypes.error_type
            self.result_code = "<error>"
            return
        func_type = entry.type
        if func_type.is_ptr:
            func_type = func_type.base_type
        if len(func_type.args) == 1:
            self.operand2 = self.operand2.coerce_to(func_type.args[0].type, env)
        else:
            self.operand1 = self.operand1.coerce_to(func_type.args[0].type, env)
            self.operand2 = self.operand2.coerce_to(func_type.args[1].type, env)
        self.type = func_type.return_type

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
        elif self.is_c_string_contains():
            if self.operand2.type is unicode_type:
                if self.uchar_test_type is PyrexTypes.c_py_unicode_type:
                    method = "__Pyx_UnicodeContains"
                else:
                    method = "__Pyx_UnicodeContainsUCS4"
            else:
                method = "__Pyx_BytesContains"
            if self.operator == "not_in":
                negation = "!"
            else:
                negation = ""
            return "(%s%s(%s, %s))" % (
                negation,
                method,
                self.operand2.result(),
                self.operand1.result())
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

    def has_constant_result(self):
        return self.constant_result is not constant_value_not_set and \
               self.constant_result is not not_a_constant

    def analyse_types(self, env):
        self.operand2.analyse_types(env)
        if self.cascade:
            self.cascade.analyse_types(env)

    def has_python_operands(self):
        return self.operand2.type.is_pyobject

    def coerce_operands_to_pyobjects(self, env):
        self.operand2 = self.operand2.coerce_to_pyobject(env)
        if self.operand2.type is dict_type and self.operator in ('in', 'not_in'):
            self.operand2 = self.operand2.as_none_safe_node("'NoneType' object is not iterable")
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

def binop_node(pos, operator, operand1, operand2, inplace=False):
    # Construct binop node of appropriate class for
    # given operator.
    return binop_node_classes[operator](pos,
        operator = operator,
        operand1 = operand1,
        operand2 = operand2,
        inplace = inplace)

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

    def may_be_none(self):
        return self.arg.may_be_none()

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

    def may_be_none(self):
        if self.notnone:
            return False
        return self.arg.may_be_none()

    def is_simple(self):
        return self.arg.is_simple()

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

    def may_be_none(self):
        return False

    def is_simple(self):
        return self.arg.is_simple()

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
        if type is py_object_type:
            # be specific about some known types
            if arg.type.is_string:
                self.type = bytes_type
            elif arg.type.is_unicode_char:
                self.type = unicode_type
            elif arg.type.is_complex:
                self.type = Builtin.complex_type
        else:
            # FIXME: check that the target type and the resulting type are compatible
            pass

    gil_message = "Converting to Python object"

    def may_be_none(self):
        # FIXME: is this always safe?
        return False

    def coerce_to_boolean(self, env):
        arg_type = self.arg.type
        if (arg_type == PyrexTypes.c_bint_type or
            (arg_type.is_pyobject and arg_type.name == 'bool')):
            return self.arg.coerce_to_temp(env)
        else:
            return CoerceToBooleanNode(self, env)

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


class CoerceIntToBytesNode(CoerceToPyTypeNode):
    #  This node is used to convert a C int type to a Python bytes
    #  object.

    is_temp = 1

    def __init__(self, arg, env):
        arg = arg.coerce_to_simple(env)
        CoercionNode.__init__(self, arg)
        self.type = Builtin.bytes_type

    def generate_result_code(self, code):
        arg = self.arg
        arg_result = arg.result()
        if arg.type not in (PyrexTypes.c_char_type,
                            PyrexTypes.c_uchar_type,
                            PyrexTypes.c_schar_type):
            if arg.type.signed:
                code.putln("if ((%s < 0) || (%s > 255)) {" % (
                    arg_result, arg_result))
            else:
                code.putln("if (%s > 255) {" % arg_result)
            code.putln('PyErr_Format(PyExc_OverflowError, '
                       '"value too large to pack into a byte"); %s' % (
                           code.error_goto(self.pos)))
            code.putln('}')
        temp = None
        if arg.type is not PyrexTypes.c_char_type:
            temp = code.funcstate.allocate_temp(PyrexTypes.c_char_type, manage_ref=False)
            code.putln("%s = (char)%s;" % (temp, arg_result))
            arg_result = temp
        code.putln('%s = PyBytes_FromStringAndSize(&%s, 1); %s' % (
            self.result(),
            arg_result,
            code.error_goto_if_null(self.result(), self.pos)))
        if temp is not None:
            code.funcstate.release_temp(temp)
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

    _special_builtins = {
        Builtin.list_type    : 'PyList_GET_SIZE',
        Builtin.tuple_type   : 'PyTuple_GET_SIZE',
        Builtin.bytes_type   : 'PyBytes_GET_SIZE',
        Builtin.unicode_type : 'PyUnicode_GET_SIZE',
        }

    def __init__(self, arg, env):
        CoercionNode.__init__(self, arg)
        if arg.type.is_pyobject:
            self.is_temp = 1

    def nogil_check(self, env):
        if self.arg.type.is_pyobject and self._special_builtins.get(self.arg.type) is None:
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
        if not self.is_temp:
            return
        test_func = self._special_builtins.get(self.arg.type)
        if test_func is not None:
            code.putln("%s = (%s != Py_None) && (%s(%s) != 0);" % (
                       self.result(),
                       self.arg.py_result(),
                       test_func,
                       self.arg.py_result()))
        else:
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
        self.constant_result = self.arg.constant_result
        self.is_temp = 1
        if self.type.is_pyobject:
            self.result_ctype = py_object_type

    gil_message = "Creating temporary Python reference"

    def analyse_types(self, env):
        # The arg is always already analysed
        pass

    def coerce_to_boolean(self, env):
        self.arg = self.arg.coerce_to_boolean(env)
        if self.arg.is_simple():
            return self.arg
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

    def is_simple(self):
        return True # result is always in a temp (or a name)

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

    def may_be_none(self):
        return False

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
        code.putln('%s = __Pyx_GetAttrString(%s, "__doc__"); %s' % (
            self.result(), self.body.result(),
            code.error_goto_if_null(self.result(), self.pos)))
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
    if (!result) {
        if (dict != %(BUILTINS)s) {
            PyErr_Clear();
            result = PyObject_GetAttr(%(BUILTINS)s, name);
        }
        if (!result) {
            PyErr_SetObject(PyExc_NameError, name);
        }
    }
    return result;
}
""" % {'BUILTINS' : Naming.builtins_cname})

#------------------------------------------------------------------------------------

import_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list, long level); /*proto*/
""",
impl = """
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list, long level) {
    PyObject *py_import = 0;
    PyObject *empty_list = 0;
    PyObject *module = 0;
    PyObject *global_dict = 0;
    PyObject *empty_dict = 0;
    PyObject *list;
    py_import = __Pyx_GetAttrString(%(BUILTINS)s, "__import__");
    if (!py_import)
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
    #if PY_VERSION_HEX >= 0x02050000
    {
        PyObject *py_level = PyInt_FromLong(level);
        if (!py_level)
            goto bad;
        module = PyObject_CallFunctionObjArgs(py_import,
            name, global_dict, empty_dict, list, py_level, NULL);
        Py_DECREF(py_level);
    }
    #else
    if (level>0) {
        PyErr_SetString(PyExc_RuntimeError, "Relative import is not supported for Python <=2.4.");
        goto bad;
    }
    module = PyObject_CallFunctionObjArgs(py_import,
        name, global_dict, empty_dict, list, NULL);
    #endif
bad:
    Py_XDECREF(empty_list);
    Py_XDECREF(py_import);
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

find_py2_metaclass_utility_code = UtilityCode(
proto = '''
static PyObject *__Pyx_FindPy2Metaclass(PyObject *bases); /*proto*/
''',
impl = '''
static PyObject *__Pyx_FindPy2Metaclass(PyObject *bases) {
    PyObject *metaclass;
    /* Default metaclass */
#if PY_MAJOR_VERSION < 3
    if (PyTuple_Check(bases) && PyTuple_GET_SIZE(bases) > 0) {
        PyObject *base = PyTuple_GET_ITEM(bases, 0);
        metaclass = PyObject_GetAttrString(base, (char *)"__class__");
        if (!metaclass) {
            PyErr_Clear();
            metaclass = (PyObject*) Py_TYPE(base);
        }
    } else {
        metaclass = (PyObject *) &PyClass_Type;
    }
#else
    if (PyTuple_Check(bases) && PyTuple_GET_SIZE(bases) > 0) {
        PyObject *base = PyTuple_GET_ITEM(bases, 0);
        metaclass = (PyObject*) Py_TYPE(base);
    } else {
        metaclass = (PyObject *) &PyType_Type;
    }
#endif
    Py_INCREF(metaclass);
    return metaclass;
}
''')

create_class_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name,
                                   PyObject *modname); /*proto*/
""",
impl = """
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name,
                                   PyObject *modname) {
    PyObject *result;
    PyObject *metaclass;

    if (PyDict_SetItemString(dict, "__module__", modname) < 0)
        return NULL;

    /* Python2 __metaclass__ */
    metaclass = PyDict_GetItemString(dict, "__metaclass__");
    if (metaclass) {
        Py_INCREF(metaclass);
    } else {
        metaclass = __Pyx_FindPy2Metaclass(bases);
    }
    result = PyObject_CallFunctionObjArgs(metaclass, name, bases, dict, NULL);
    Py_DECREF(metaclass);
    return result;
}
""",
requires = [find_py2_metaclass_utility_code])

#------------------------------------------------------------------------------------

create_py3class_utility_code = UtilityCode(
proto = """
static PyObject *__Pyx_Py3MetaclassGet(PyObject *bases, PyObject *mkw); /*proto*/
static PyObject *__Pyx_Py3MetaclassPrepare(PyObject *metaclass, PyObject *bases, PyObject *name, PyObject *mkw, PyObject *modname, PyObject *doc); /*proto*/
static PyObject *__Pyx_Py3ClassCreate(PyObject *metaclass, PyObject *name, PyObject *bases, PyObject *dict, PyObject *mkw); /*proto*/
""",
impl = """
PyObject *__Pyx_Py3MetaclassGet(PyObject *bases, PyObject *mkw) {
    PyObject *metaclass = PyDict_GetItemString(mkw, "metaclass");
    if (metaclass) {
        Py_INCREF(metaclass);
        if (PyDict_DelItemString(mkw, "metaclass") < 0) {
            Py_DECREF(metaclass);
            return NULL;
        }
        return metaclass;
    }
    return __Pyx_FindPy2Metaclass(bases);
}

PyObject *__Pyx_Py3MetaclassPrepare(PyObject *metaclass, PyObject *bases, PyObject *name, PyObject *mkw,
                                    PyObject *modname, PyObject *doc) {
    PyObject *prep;
    PyObject *pargs;
    PyObject *ns;
    PyObject *str;

    prep = PyObject_GetAttrString(metaclass, (char *)"__prepare__");
    if (!prep) {
        if (!PyErr_ExceptionMatches(PyExc_AttributeError))
            return NULL;
        PyErr_Clear();
        return PyDict_New();
    }
    pargs = PyTuple_New(2);
    if (!pargs) {
        Py_DECREF(prep);
        return NULL;
    }

    Py_INCREF(name);
    Py_INCREF(bases);
    PyTuple_SET_ITEM(pargs, 0, name);
    PyTuple_SET_ITEM(pargs, 1, bases);

    ns = PyObject_Call(prep, pargs, mkw);

    Py_DECREF(prep);
    Py_DECREF(pargs);

    if (ns == NULL)
        return NULL;

    /* Required here to emulate assignment order */
    /* XXX: use consts here */
    #if PY_MAJOR_VERSION >= 3
    str = PyUnicode_FromString("__module__");
    #else
    str = PyString_FromString("__module__");
    #endif
    if (!str) {
        Py_DECREF(ns);
        return NULL;
    }

    if (PyObject_SetItem(ns, str, modname) < 0) {
        Py_DECREF(ns);
        Py_DECREF(str);
        return NULL;
    }
    Py_DECREF(str);
    if (doc) {
        #if PY_MAJOR_VERSION >= 3
        str = PyUnicode_FromString("__doc__");
        #else
        str = PyString_FromString("__doc__");
        #endif
        if (!str) {
            Py_DECREF(ns);
            return NULL;
        }
        if (PyObject_SetItem(ns, str, doc) < 0) {
            Py_DECREF(ns);
            Py_DECREF(str);
            return NULL;
        }
        Py_DECREF(str);
    }
    return ns;
}

PyObject *__Pyx_Py3ClassCreate(PyObject *metaclass, PyObject *name, PyObject *bases, PyObject *dict, PyObject *mkw) {
    PyObject *result;
    PyObject *margs = PyTuple_New(3);
    if (!margs)
        return NULL;
    Py_INCREF(name);
    Py_INCREF(bases);
    Py_INCREF(dict);
    PyTuple_SET_ITEM(margs, 0, name);
    PyTuple_SET_ITEM(margs, 1, bases);
    PyTuple_SET_ITEM(margs, 2, dict);
    result = PyObject_Call(metaclass, margs, mkw);
    Py_DECREF(margs);
    return result;
}
""",
requires = [find_py2_metaclass_utility_code])

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
  } catch (const std::invalid_argument& exn) {
    // Catch a handful of different errors here and turn them into the
    // equivalent Python errors.
    // Change invalid_argument to ValueError
    PyErr_SetString(PyExc_ValueError, exn.what());
  } catch (const std::out_of_range& exn) {
    // Change out_of_range to IndexError
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

pyerr_occurred_withgil_utility_code= UtilityCode(
proto = """
static CYTHON_INLINE int __Pyx_ErrOccurredWithGIL(void); /* proto */
""",
impl = """
static CYTHON_INLINE int __Pyx_ErrOccurredWithGIL(void) {
  int err;
  #ifdef WITH_THREAD
  PyGILState_STATE _save = PyGILState_Ensure();
  #endif
  err = !!PyErr_Occurred();
  #ifdef WITH_THREAD
  PyGILState_Release(_save);
  #endif
  return err;
}
"""
)

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

#------------------------------------------------------------------------------------

getitem_dict_utility_code = UtilityCode(
proto = """
#if PY_MAJOR_VERSION >= 3
static PyObject *__Pyx_PyDict_GetItem(PyObject *d, PyObject* key) {
    PyObject *value;
    if (unlikely(d == Py_None)) {
        __Pyx_RaiseNoneIndexingError();
        return NULL;
    }
    value = PyDict_GetItemWithError(d, key);
    if (unlikely(!value)) {
        if (!PyErr_Occurred())
            PyErr_SetObject(PyExc_KeyError, key);
        return NULL;
    }
    Py_INCREF(value);
    return value;
}
#else
    #define __Pyx_PyDict_GetItem(d, key) PyObject_GetItem(d, key)
#endif
""",
requires = [raise_noneindex_error_utility_code])

#------------------------------------------------------------------------------------

getitem_int_pyunicode_utility_code = UtilityCode(
proto = '''
#define __Pyx_GetItemInt_Unicode(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \\
                                               __Pyx_GetItemInt_Unicode_Fast(o, i) : \\
                                               __Pyx_GetItemInt_Unicode_Generic(o, to_py_func(i)))

static CYTHON_INLINE Py_UNICODE __Pyx_GetItemInt_Unicode_Fast(PyObject* ustring, Py_ssize_t i) {
    if (likely((0 <= i) & (i < PyUnicode_GET_SIZE(ustring)))) {
        return PyUnicode_AS_UNICODE(ustring)[i];
    } else if ((-PyUnicode_GET_SIZE(ustring) <= i) & (i < 0)) {
        i += PyUnicode_GET_SIZE(ustring);
        return PyUnicode_AS_UNICODE(ustring)[i];
    } else {
        PyErr_SetString(PyExc_IndexError, "string index out of range");
        return (Py_UNICODE)-1;
    }
}

static CYTHON_INLINE Py_UNICODE __Pyx_GetItemInt_Unicode_Generic(PyObject* ustring, PyObject* j) {
    Py_UNICODE uchar;
    PyObject *uchar_string;
    if (!j) return (Py_UNICODE)-1;
    uchar_string = PyObject_GetItem(ustring, j);
    Py_DECREF(j);
    if (!uchar_string) return (Py_UNICODE)-1;
    uchar = PyUnicode_AS_UNICODE(uchar_string)[0];
    Py_DECREF(uchar_string);
    return uchar;
}
''')

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
#define __Pyx_GetItemInt_%(type)s(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_GetItemInt_%(type)s_Fast(o, i) : \\
                                                    __Pyx_GetItemInt_Generic(o, to_py_func(i)))

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_%(type)s_Fast(PyObject *o, Py_ssize_t i) {
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
    return __Pyx_GetItemInt_Generic(o, PyInt_FromSsize_t(i));
}
""" % {'type' : type_name} for type_name in ('List', 'Tuple')
]) + """

#define __Pyx_GetItemInt(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_GetItemInt_Fast(o, i) : \\
                                                    __Pyx_GetItemInt_Generic(o, to_py_func(i)))

static CYTHON_INLINE PyObject *__Pyx_GetItemInt_Fast(PyObject *o, Py_ssize_t i) {
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
        r = __Pyx_GetItemInt_Generic(o, PyInt_FromSsize_t(i));
    }
    return r;
}
""",
impl = """
""")



#------------------------------------------------------------------------------------

setitem_int_utility_code = UtilityCode(
proto = """
#define __Pyx_SetItemInt(o, i, v, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_SetItemInt_Fast(o, i, v) : \\
                                                    __Pyx_SetItemInt_Generic(o, to_py_func(i), v))

static CYTHON_INLINE int __Pyx_SetItemInt_Generic(PyObject *o, PyObject *j, PyObject *v) {
    int r;
    if (!j) return -1;
    r = PyObject_SetItem(o, j, v);
    Py_DECREF(j);
    return r;
}

static CYTHON_INLINE int __Pyx_SetItemInt_Fast(PyObject *o, Py_ssize_t i, PyObject *v) {
    if (PyList_CheckExact(o) && ((0 <= i) & (i < PyList_GET_SIZE(o)))) {
        Py_INCREF(v);
        Py_DECREF(PyList_GET_ITEM(o, i));
        PyList_SET_ITEM(o, i, v);
        return 1;
    }
    else if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_ass_item && (likely(i >= 0)))
        return PySequence_SetItem(o, i, v);
    else {
        PyObject *j = PyInt_FromSsize_t(i);
        return __Pyx_SetItemInt_Generic(o, j, v);
    }
}
""",
impl = """
""")

#------------------------------------------------------------------------------------

delitem_int_utility_code = UtilityCode(
proto = """
#define __Pyx_DelItemInt(o, i, size, to_py_func) (((size) <= sizeof(Py_ssize_t)) ? \\
                                                    __Pyx_DelItemInt_Fast(o, i) : \\
                                                    __Pyx_DelItem_Generic(o, to_py_func(i)))

static CYTHON_INLINE int __Pyx_DelItem_Generic(PyObject *o, PyObject *j) {
    int r;
    if (!j) return -1;
    r = PyObject_DelItem(o, j);
    Py_DECREF(j);
    return r;
}

static CYTHON_INLINE int __Pyx_DelItemInt_Fast(PyObject *o, Py_ssize_t i) {
    if (Py_TYPE(o)->tp_as_sequence && Py_TYPE(o)->tp_as_sequence->sq_ass_item && likely(i >= 0))
        return PySequence_DelItem(o, i);
    else {
        PyObject *j = PyInt_FromSsize_t(i);
        return __Pyx_DelItem_Generic(o, j);
    }
}
""",
impl = """
""")

#------------------------------------------------------------------------------------

raise_too_many_values_to_unpack = UtilityCode(
proto = """
static CYTHON_INLINE void __Pyx_RaiseTooManyValuesError(Py_ssize_t expected);
""",
impl = '''
static CYTHON_INLINE void __Pyx_RaiseTooManyValuesError(Py_ssize_t expected) {
    PyErr_Format(PyExc_ValueError,
        #if PY_VERSION_HEX < 0x02050000
            "too many values to unpack (expected %d)", (int)expected);
        #else
            "too many values to unpack (expected %zd)", expected);
        #endif
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
      __Pyx_RaiseTooManyValuesError(index);
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
""",
requires = [raise_need_more_values_to_unpack]
)

iternext_unpacking_end_utility_code = UtilityCode(
proto = """
static int __Pyx_IternextUnpackEndCheck(PyObject *retval, Py_ssize_t expected); /*proto*/
""",
impl = """
static int __Pyx_IternextUnpackEndCheck(PyObject *retval, Py_ssize_t expected) {
    if (unlikely(retval)) {
        Py_DECREF(retval);
        __Pyx_RaiseTooManyValuesError(expected);
        return -1;
    } else if (PyErr_Occurred()) {
        if (likely(PyErr_ExceptionMatches(PyExc_StopIteration))) {
            PyErr_Clear();
            return 0;
        } else {
            return -1;
        }
    }
    return 0;
}
""",
requires = [raise_too_many_values_to_unpack]
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
static int __Pyx_cdivision_warning(const char *, int); /* proto */
""",
impl="""
static int __Pyx_cdivision_warning(const char *filename, int lineno) {
    return PyErr_WarnExplicit(PyExc_RuntimeWarning,
                              "division with oppositely signed operands, C and Python semantics differ",
                              filename,
                              lineno,
                              __Pyx_MODULE_NAME,
                              NULL);
}
""")

# from intobject.c
division_overflow_test_code = UtilityCode(
proto="""
#define UNARY_NEG_WOULD_OVERFLOW(x)    \
        (((x) < 0) & ((unsigned long)(x) == 0-(unsigned long)(x)))
""")


binding_cfunc_utility_code = UtilityCode(
proto="""
#define %(binding_cfunc)s_USED 1

typedef struct {
    PyCFunctionObject func;
} %(binding_cfunc)s_object;

static PyTypeObject %(binding_cfunc)s_type;
static PyTypeObject *%(binding_cfunc)s = NULL;

static PyObject *%(binding_cfunc)s_NewEx(PyMethodDef *ml, PyObject *self, PyObject *module); /* proto */
#define %(binding_cfunc)s_New(ml, self) %(binding_cfunc)s_NewEx(ml, self, NULL)

static int %(binding_cfunc)s_init(void); /* proto */
""" % Naming.__dict__,
impl="""

static PyObject *%(binding_cfunc)s_NewEx(PyMethodDef *ml, PyObject *self, PyObject *module) {
    %(binding_cfunc)s_object *op = PyObject_GC_New(%(binding_cfunc)s_object, %(binding_cfunc)s);
    if (op == NULL)
        return NULL;
    op->func.m_ml = ml;
    Py_XINCREF(self);
    op->func.m_self = self;
    Py_XINCREF(module);
    op->func.m_module = module;
    PyObject_GC_Track(op);
    return (PyObject *)op;
}

static void %(binding_cfunc)s_dealloc(%(binding_cfunc)s_object *m) {
    PyObject_GC_UnTrack(m);
    Py_XDECREF(m->func.m_self);
    Py_XDECREF(m->func.m_module);
    PyObject_GC_Del(m);
}

static PyObject *%(binding_cfunc)s_descr_get(PyObject *func, PyObject *obj, PyObject *type) {
    if (obj == Py_None)
            obj = NULL;
    return PyMethod_New(func, obj, type);
}

static int %(binding_cfunc)s_init(void) {
    %(binding_cfunc)s_type = PyCFunction_Type;
    %(binding_cfunc)s_type.tp_name = __Pyx_NAMESTR("cython_binding_builtin_function_or_method");
    %(binding_cfunc)s_type.tp_dealloc = (destructor)%(binding_cfunc)s_dealloc;
    %(binding_cfunc)s_type.tp_descr_get = %(binding_cfunc)s_descr_get;
    if (PyType_Ready(&%(binding_cfunc)s_type) < 0) {
        return -1;
    }
    %(binding_cfunc)s = &%(binding_cfunc)s_type;
    return 0;

}
""" % Naming.__dict__)

generator_utility_code = UtilityCode(
proto="""
static PyObject *__Pyx_Generator_Next(PyObject *self);
static PyObject *__Pyx_Generator_Send(PyObject *self, PyObject *value);
static PyObject *__Pyx_Generator_Close(PyObject *self);
static PyObject *__Pyx_Generator_Throw(PyObject *gen, PyObject *args, CYTHON_UNUSED PyObject *kwds);

typedef PyObject *(*__pyx_generator_body_t)(PyObject *, PyObject *);
""",
impl="""
static CYTHON_INLINE void __Pyx_Generator_ExceptionClear(struct __pyx_Generator_object *self)
{
    Py_XDECREF(self->exc_type);
    Py_XDECREF(self->exc_value);
    Py_XDECREF(self->exc_traceback);

    self->exc_type = NULL;
    self->exc_value = NULL;
    self->exc_traceback = NULL;
}

static CYTHON_INLINE PyObject *__Pyx_Generator_SendEx(struct __pyx_Generator_object *self, PyObject *value)
{
    PyObject *retval;

    if (self->is_running) {
        PyErr_SetString(PyExc_ValueError,
                        "generator already executing");
        return NULL;
    }

    if (self->resume_label == 0) {
        if (value && value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
                            "can't send non-None value to a "
                            "just-started generator");
            return NULL;
        }
    }

    if (self->resume_label == -1) {
        PyErr_SetNone(PyExc_StopIteration);
        return NULL;
    }


    if (value)
        __Pyx_ExceptionSwap(&self->exc_type, &self->exc_value, &self->exc_traceback);
    else
        __Pyx_Generator_ExceptionClear(self);

    self->is_running = 1;
    retval = self->body((PyObject *) self, value);
    self->is_running = 0;

    if (retval)
        __Pyx_ExceptionSwap(&self->exc_type, &self->exc_value, &self->exc_traceback);
    else
        __Pyx_Generator_ExceptionClear(self);

    return retval;
}

static PyObject *__Pyx_Generator_Next(PyObject *self)
{
    return __Pyx_Generator_SendEx((struct __pyx_Generator_object *) self, Py_None);
}

static PyObject *__Pyx_Generator_Send(PyObject *self, PyObject *value)
{
    return __Pyx_Generator_SendEx((struct __pyx_Generator_object *) self, value);
}

static PyObject *__Pyx_Generator_Close(PyObject *self)
{
    struct __pyx_Generator_object *generator = (struct __pyx_Generator_object *) self;
    PyObject *retval;
#if PY_VERSION_HEX < 0x02050000
    PyErr_SetNone(PyExc_StopIteration);
#else
    PyErr_SetNone(PyExc_GeneratorExit);
#endif
    retval = __Pyx_Generator_SendEx(generator, NULL);
    if (retval) {
        Py_DECREF(retval);
        PyErr_SetString(PyExc_RuntimeError,
                        "generator ignored GeneratorExit");
        return NULL;
    }
#if PY_VERSION_HEX < 0x02050000
    if (PyErr_ExceptionMatches(PyExc_StopIteration))
#else
    if (PyErr_ExceptionMatches(PyExc_StopIteration)
        || PyErr_ExceptionMatches(PyExc_GeneratorExit))
#endif
    {
        PyErr_Clear();          /* ignore these errors */
        Py_INCREF(Py_None);
        return Py_None;
    }
    return NULL;
}

static PyObject *__Pyx_Generator_Throw(PyObject *self, PyObject *args, CYTHON_UNUSED PyObject *kwds)
{
    struct __pyx_Generator_object *generator = (struct __pyx_Generator_object *) self;
    PyObject *typ;
    PyObject *tb = NULL;
    PyObject *val = NULL;

    if (!PyArg_UnpackTuple(args, (char *)"throw", 1, 3, &typ, &val, &tb))
        return NULL;
    __Pyx_Raise(typ, val, tb, NULL);
    return __Pyx_Generator_SendEx(generator, NULL);
}
""",
proto_block='utility_code_proto_before_types',
requires=[Nodes.raise_utility_code, Nodes.swap_exception_utility_code],
)
