#
#   Pyrex - Parse tree nodes for expressions
#

from string import join

from Errors import error, InternalError
import Naming
from Nodes import Node
import PyrexTypes
from PyrexTypes import py_object_type, c_long_type, typecast
import Symtab
import Options

from Pyrex.Debugging import print_call_chain
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
    #      calculate_result_code
    #        - Return a C code fragment evaluating to
    #          the result. This is only called when the
    #          result is not a temporary.
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
    #        is provided which uses the following abstract method:
    #
    #          generate_result_code
    #            - Generate any C statements necessary to calculate
    #              the result of this node from the results of its
    #              sub-expressions.
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
    
    def result_as(self, type = None):
        #  Return the result code cast to the specified C type.
        return typecast(type, self.ctype(), self.result_code)
    
    def py_result(self):
        #  Return the result code cast to PyObject *.
        return self.result_as(py_object_type)
    
    def ctype(self):
        #  Return the native C type of the result (i.e. the
        #  C type of the result_code expression).
        return self.result_ctype or self.type
    
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
    
    def analyse_as_extension_type(self, env):
        # If this node can be interpreted as a reference to an
        # extension type, return its type, else None.
        return None
    
    def analyse_types(self, env):
        self.not_implemented("analyse_types")
    
    def analyse_target_types(self, env):
        self.analyse_types(env)
    
    def check_const(self):
        self.not_const()
    
    def not_const(self):
        error(self.pos, "Not allowed in a constant expression")
    
    def check_const_addr(self):
        self.addr_not_const()
    
    def addr_not_const(self):
        error(self.pos, "Address is not constant")
    
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
            print self, "Allocating target temps"
        self.allocate_subexpr_temps(env)
        self.result_code = self.target_code()
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
            print self, "Allocating temps"
        self.allocate_subexpr_temps(env)
        self.allocate_temp(env, result)
        if self.is_temp:
            self.release_subexpr_temps(env)
    
    def allocate_subexpr_temps(self, env):
        #  Allocate temporary variables for all sub-expressions
        #  of this node.
        if debug_temp_alloc:
            print self, "Allocating temps for:", self.subexprs
        for node in self.subexpr_nodes():
            if node:
                if debug_temp_alloc:
                    print self, "Allocating temps for", node
                node.allocate_temps(env)
    
    def allocate_temp(self, env, result = None):
        #  If this node requires a temporary variable for its
        #  result, allocate one, otherwise set the result to
        #  a C code fragment. If a result is specified,
        #  this must be a temp node and the specified variable
        #  is used as the result instead of allocating a new
        #  one.
        if debug_temp_alloc:
            print self, "Allocating temp"
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
                print self, "Allocated result", self.result_code
        else:
            self.result_code = self.calculate_result_code()
    
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
                print self, "Releasing result", self.result_code
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
            code.put_incref(self.result_code, self.ctype())
    
    def generate_evaluation_code(self, code):
        #  Generate code to evaluate this node and
        #  its sub-expressions, and dispose of any
        #  temporary results of its sub-expressions.
        self.generate_subexpr_evaluation_code(code)
        self.generate_result_code(code)
        if self.is_temp:
            self.generate_subexpr_disposal_code(code)
    
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
                code.put_decref_clear(self.result_code, self.ctype())
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
                code.putln("%s = 0;" % self.result_code)
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
            if not dst_type.assignable_from(src_type):
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
            if not type.is_int:
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


class AtomicExprNode(ExprNode):
    #  Abstract base class for expression nodes which have
    #  no sub-expressions.
    
    subexprs = []


class PyConstNode(AtomicExprNode):
    #  Abstract base class for constant Python values.
    
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
    

class EllipsisNode(PyConstNode):
    #  '...' in a subscript list.
    
    value = "Py_Ellipsis"


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


class NullNode(ConstNode):
    type = PyrexTypes.c_null_ptr_type
    value = "NULL"


class CharNode(ConstNode):
    type = PyrexTypes.c_char_type
    
    def calculate_result_code(self):
        return "'%s'" % self.value


class IntNode(ConstNode):
    type = PyrexTypes.c_long_type


class FloatNode(ConstNode):
    type = PyrexTypes.c_double_type


class StringNode(ConstNode):
    #  entry   Symtab.Entry
    
    type = PyrexTypes.c_char_ptr_type
    
    def analyse_types(self, env):
        self.entry = env.add_string_const(self.value)
    
    def coerce_to(self, dst_type, env):
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
        return StringNode(self.pos, entry = entry, type = py_object_type)
            
    def calculate_result_code(self):
        if self.type.is_pyobject:
            return self.entry.pystring_cname
        else:
            return self.entry.cname


class LongNode(AtomicExprNode):
    #  Python long integer literal
    #
    #  value   string
    
    def analyse_types(self, env):
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_evaluation_code(self, code):
        code.putln(
            '%s = PyLong_FromString("%s", 0, 0); if (!%s) %s' % (
                self.result_code,
                self.value,
                self.result_code,
                code.error_goto(self.pos)))	


class ImagNode(AtomicExprNode):
    #  Imaginary number literal
    #
    #  value   float    imaginary part
    
    def analyse_types(self, env):
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_evaluation_code(self, code):
        code.putln(
            "%s = PyComplex_FromDoubles(0.0, %s); if (!%s) %s" % (
                self.result_code,
                self.value,
                self.result_code,
                code.error_goto(self.pos)))


class NameNode(AtomicExprNode):
    #  Reference to a local or global variable name.
    #
    #  name            string    Python name of the variable
    #  entry           Entry     Symbol table entry
    
    is_name = 1
    
    def analyse_as_module(self, env):
        # Try to interpret this as a reference to a cimported module.
        # Returns the module scope, or None.
        entry = env.lookup(self.name)
        if entry and entry.as_module:
            return entry.as_module
        return None
    
    def analyse_as_extension_type(self, env):
        # Try to interpret this as a reference to an extension type.
        # Returns the extension type, or None.
        entry = env.lookup(self.name)
        if entry and entry.is_type and entry.type.is_extension_type:
                return entry.type
        return None
    
    def analyse_target_declaration(self, env):
        self.entry = env.lookup_here(self.name)
        if not self.entry:
            #print "NameNode.analyse_target_declaration:", self.name ###
            #print "...declaring as py_object_type" ###
            self.entry = env.declare_var(self.name, py_object_type, self.pos)
    
    def analyse_types(self, env):
        self.entry = env.lookup(self.name)
        if not self.entry:
            self.entry = env.declare_builtin(self.name, self.pos)
        self.analyse_entry(env)
        
    def analyse_entry(self, env):
        self.check_identifier_kind()
        entry = self.entry
        self.type = entry.type
        if entry.is_declared_generic:
            self.result_ctype = py_object_type
        ## Reference to C array turns into pointer to first element.
        #while self.type.is_array:
        #	self.type = self.type.element_ptr_type()
        if entry.is_pyglobal or entry.is_builtin:
            assert self.type.is_pyobject, "Python global or builtin not a Python object"
            self.is_temp = 1
            if Options.intern_names:
                env.use_utility_code(get_name_interned_utility_code)
            else:
                env.use_utility_code(get_name_utility_code)
    
    def analyse_target_types(self, env):
        self.check_identifier_kind()
        if self.is_lvalue():
            self.type = self.entry.type
        else:
            error(self.pos, "Assignment to non-lvalue '%s'"
                % self.name)
            self.type = PyrexTypes.error_type
    
    def check_identifier_kind(self):
        #print "NameNode.check_identifier_kind:", self.entry.name ###
        entry = self.entry
        entry.used = 1
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
        if not (entry.is_const or entry.is_cfunction):
            self.not_const()
    
    def check_const_addr(self):
        entry = self.entry
        if not (entry.is_cglobal or entry.is_cfunction):
            self.addr_not_const()

    def is_lvalue(self):
        return self.entry.is_variable and \
            not self.entry.type.is_array and \
            not self.entry.is_readonly
    
    def is_ephemeral(self):
        #  Name nodes are never ephemeral, even if the
        #  result is in a temporary.
        return 0

    def calculate_result_code(self):
        if self.entry is None:
            return "<error>" # There was an error earlier
        return self.entry.cname
    
    def generate_result_code(self, code):
        if not hasattr(self, 'entry'):
            error(self.pos, "INTERNAL ERROR: NameNode has no entry attribute during code generation")
        entry = self.entry
        if entry is None:
            return # There was an error earlier
        if entry.is_pyglobal or entry.is_builtin:
            if entry.is_builtin:
                namespace = Naming.builtins_cname
            else: # entry.is_pyglobal
                namespace = entry.namespace_cname
            if Options.intern_names:
                #assert entry.interned_cname is not None
                code.putln(
                    '%s = __Pyx_GetName(%s, %s); if (!%s) %s' % (
                    self.result_code,
                    namespace, 
                    entry.interned_cname,
                    self.result_code, 
                    code.error_goto(self.pos)))		
            else:
                code.putln(
                    '%s = __Pyx_GetName(%s, "%s"); if (!%s) %s' % (
                    self.result_code,
                    namespace, 
                    self.entry.name,
                    self.result_code, 
                    code.error_goto(self.pos)))		

    def generate_assignment_code(self, rhs, code):
        entry = self.entry
        if entry is None:
            return # There was an error earlier
        if entry.is_pyglobal:
            namespace = self.entry.namespace_cname
            if Options.intern_names:
                code.putln(
                    'if (PyObject_SetAttr(%s, %s, %s) < 0) %s' % (
                        namespace, 
                        entry.interned_cname,
                        rhs.py_result(), 
                        code.error_goto(self.pos)))
            else:
                code.putln(
                    'if (PyObject_SetAttrString(%s, "%s", %s) < 0) %s' % (
                        namespace, 
                        entry.name,
                        rhs.py_result(), 
                        code.error_goto(self.pos)))
            if debug_disposal_code:
                print "NameNode.generate_assignment_code:"
                print "...generating disposal code for", rhs
            rhs.generate_disposal_code(code)
        else:
            if self.type.is_pyobject:
                #print "NameNode.generate_assignment_code: to", self.name ###
                #print "...from", rhs ###
                #print "...LHS type", self.type, "ctype", self.ctype() ###
                #print "...RHS type", rhs.type, "ctype", rhs.ctype() ###
                rhs.make_owned_reference(code)
                code.put_decref(self.result_code, self.ctype())
            code.putln('%s = %s;' % (self.result_code, rhs.result_as(self.ctype())))
            if debug_disposal_code:
                print "NameNode.generate_assignment_code:"
                print "...generating post-assignment code for", rhs
            rhs.generate_post_assignment_code(code)
    
    def generate_deletion_code(self, code):
        if self.entry is None:
            return # There was an error earlier
        if not self.entry.is_pyglobal:
            error(self.pos, "Deletion of local or C global name not supported")
            return
        code.putln(
            'if (PyObject_DelAttrString(%s, "%s") < 0) %s' % (
                Naming.module_cname,
                self.entry.name,
                code.error_goto(self.pos)))
            

class BackquoteNode(ExprNode):
    #  `expr`
    #
    #  arg    ExprNode
    
    subexprs = ['arg']
    
    def analyse_types(self, env):
        self.arg.analyse_types(env)
        self.arg = self.arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln(
            "%s = PyObject_Repr(%s); if (!%s) %s" % (
                self.result_code,
                self.arg.py_result(),
                self.result_code,
                code.error_goto(self.pos)))


class ImportNode(ExprNode):
    #  Used as part of import statement implementation.
    #  Implements result = 
    #    __import__(module_name, globals(), None, name_list)
    #
    #  module_name   StringNode         dotted name of module
    #  name_list     ListNode or None   list of names to be imported
    
    subexprs = ['module_name', 'name_list']

    def analyse_types(self, env):
        self.module_name.analyse_types(env)
        self.module_name = self.module_name.coerce_to_pyobject(env)
        if self.name_list:
            self.name_list.analyse_types(env)
        self.type = py_object_type
        self.is_temp = 1
        env.use_utility_code(import_utility_code)
    
    def generate_result_code(self, code):
        if self.name_list:
            name_list_code = self.name_list.py_result()
        else:
            name_list_code = "0"
        code.putln(
            "%s = __Pyx_Import(%s, %s); if (!%s) %s" % (
                self.result_code,
                self.module_name.py_result(),
                name_list_code,
                self.result_code,
                code.error_goto(self.pos)))


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
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln(
            "%s = PyObject_GetIter(%s); if (!%s) %s" % (
                self.result_code,
                self.sequence.py_result(),
                self.result_code,
                code.error_goto(self.pos)))


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
        code.putln(
            "%s = PyIter_Next(%s);" % (
                self.result_code,
                self.iterator.py_result()))
        code.putln(
            "if (!%s) {" %
                self.result_code)
        code.putln(
                "if (PyErr_Occurred()) %s" %
                    code.error_goto(self.pos))
        code.putln(
                "break;")
        code.putln(
            "}")
        

class ExcValueNode(AtomicExprNode):
    #  Node created during analyse_types phase
    #  of an ExceptClauseNode to fetch the current
    #  exception value.
    
    def __init__(self, pos, env):
        ExprNode.__init__(self, pos)
        self.type = py_object_type
        self.is_temp = 1
        env.use_utility_code(get_exception_utility_code)
    
    def generate_result_code(self, code):
        code.putln(
            "%s = __Pyx_GetExcValue(); if (!%s) %s" % (
                self.result_code,
                self.result_code,
                code.error_goto(self.pos)))


class TempNode(AtomicExprNode):
    #  Node created during analyse_types phase
    #  of some nodes to hold a temporary value.
    
    def __init__(self, pos, type, env):
        ExprNode.__init__(self, pos)
        self.type = type
        if type.is_pyobject:
            self.result_ctype = py_object_type
        self.is_temp = 1
    
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
    
    subexprs = ['base', 'index']
    
    def is_ephemeral(self):
        return self.base.is_ephemeral()
    
    def analyse_target_declaration(self, env):
        pass
    
    def analyse_types(self, env):
        self.base.analyse_types(env)
        self.index.analyse_types(env)
        if self.base.type.is_pyobject: 
            self.index = self.index.coerce_to_pyobject(env)
            self.type = py_object_type
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
                    PyrexTypes.c_int_type, env)
            if not self.index.type.is_int:
                error(self.pos,
                    "Invalid index type '%s'" %
                        self.index.type)
    
    def check_const_addr(self):
        self.base.check_const_addr()
        self.index.check_const()
    
    def is_lvalue(self):
        return 1
    
    def calculate_result_code(self):
        return "(%s[%s])" % (
            self.base.result_code, self.index.result_code)
    
    def generate_result_code(self, code):
        if self.type.is_pyobject:
            code.putln(
                "%s = PyObject_GetItem(%s, %s); if (!%s) %s" % (
                    self.result_code,
                    self.base.py_result(),
                    self.index.py_result(),
                    self.result_code,
                    code.error_goto(self.pos)))
    
    def generate_assignment_code(self, rhs, code):
        self.generate_subexpr_evaluation_code(code)
        if self.type.is_pyobject:
            code.putln(
                "if (PyObject_SetItem(%s, %s, %s) < 0) %s" % (
                    self.base.py_result(),
                    self.index.py_result(),
                    rhs.py_result(),
                    code.error_goto(self.pos)))
        else:
            code.putln(
                "%s = %s;" % (
                    self.result_code, rhs.result_code))
        self.generate_subexpr_disposal_code(code)
        rhs.generate_disposal_code(code)
    
    def generate_deletion_code(self, code):
        self.generate_subexpr_evaluation_code(code)
        code.putln(
            "if (PyObject_DelItem(%s, %s) < 0) %s" % (
                self.base.py_result(),
                self.index.py_result(),
                code.error_goto(self.pos)))
        self.generate_subexpr_disposal_code(code)


class SliceIndexNode(ExprNode):
    #  2-element slice indexing
    #
    #  base      ExprNode
    #  start     ExprNode or None
    #  stop      ExprNode or None
    
    subexprs = ['base', 'start', 'stop']
    
    def analyse_target_declaration(self, env):
        pass

    def analyse_types(self, env):
        self.base.analyse_types(env)
        if self.start:
            self.start.analyse_types(env)
        if self.stop:
            self.stop.analyse_types(env)
        self.base = self.base.coerce_to_pyobject(env)
        c_int = PyrexTypes.c_int_type
        if self.start:
            self.start = self.start.coerce_to(c_int, env)
        if self.stop:
            self.stop = self.stop.coerce_to(c_int, env)
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln(
            "%s = PySequence_GetSlice(%s, %s, %s); if (!%s) %s" % (
                self.result_code,
                self.base.py_result(),
                self.start_code(),
                self.stop_code(),
                self.result_code,
                code.error_goto(self.pos)))
    
    def generate_assignment_code(self, rhs, code):
        self.generate_subexpr_evaluation_code(code)
        code.putln(
            "if (PySequence_SetSlice(%s, %s, %s, %s) < 0) %s" % (
                self.base.py_result(),
                self.start_code(),
                self.stop_code(),
                rhs.result_code,
                code.error_goto(self.pos)))
        self.generate_subexpr_disposal_code(code)
        rhs.generate_disposal_code(code)

    def generate_deletion_code(self, code):
        self.generate_subexpr_evaluation_code(code)
        code.putln(
            "if (PySequence_DelSlice(%s, %s, %s) < 0) %s" % (
                self.base.py_result(),
                self.start_code(),
                self.stop_code(),
                code.error_goto(self.pos)))
        self.generate_subexpr_disposal_code(code)
    
    def start_code(self):
        if self.start:
            return self.start.result_code
        else:
            return "0"
    
    def stop_code(self):
        if self.stop:
            return self.stop.result_code
        else:
            return "0x7fffffff"
    
    def calculate_result_code(self):
        # self.result_code is not used, but this method must exist
        return "<unused>"
    

class SliceNode(ExprNode):
    #  start:stop:step in subscript list
    #
    #  start     ExprNode
    #  stop      ExprNode
    #  step      ExprNode
    
    subexprs = ['start', 'stop', 'step']
    
    def analyse_types(self, env):
        self.start.analyse_types(env)
        self.stop.analyse_types(env)
        self.step.analyse_types(env)
        self.start = self.start.coerce_to_pyobject(env)
        self.stop = self.stop.coerce_to_pyobject(env)
        self.step = self.step.coerce_to_pyobject(env)
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln(
            "%s = PySlice_New(%s, %s, %s); if (!%s) %s" % (
                self.result_code,
                self.start.py_result(), 
                self.stop.py_result(), 
                self.step.py_result(),
                self.result_code,
                code.error_goto(self.pos)))


class SimpleCallNode(ExprNode):
    #  Function call without keyword, * or ** args.
    #
    #  function       ExprNode
    #  args           [ExprNode]
    #  arg_tuple      ExprNode or None     used internally
    #  self           ExprNode or None     used internally
    #  coerced_self   ExprNode or None     used internally
    
    subexprs = ['self', 'coerced_self', 'function', 'args', 'arg_tuple']
    
    self = None
    coerced_self = None
    arg_tuple = None
    
    def analyse_types(self, env):
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
            if self.args:
                self.arg_tuple = TupleNode(self.pos, args = self.args)
                self.arg_tuple.analyse_types(env)
            else:
                self.arg_tuple = None
            self.args = None
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
        expected_nargs = len(func_type.args)
        actual_nargs = len(self.args)
        if actual_nargs < expected_nargs \
            or (not func_type.has_varargs and actual_nargs > expected_nargs):
                expected_str = str(expected_nargs)
                if func_type.has_varargs:
                    expected_str = "at least " + expected_str
                error(self.pos, 
                    "Call with wrong number of arguments (expected %s, got %s)"
                        % (expected_str, actual_nargs))
                self.args = None
                self.type = PyrexTypes.error_type
                self.result_code = "<error>"
                return
        # Coerce arguments
        for i in range(expected_nargs):
            formal_type = func_type.args[i].type
            self.args[i] = self.args[i].coerce_to(formal_type, env)
        for i in range(expected_nargs, actual_nargs):
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
    
    def calculate_result_code(self):
        return self.c_call_code()
    
    def c_call_code(self):
        func_type = self.function_type()
        if self.args is None or not func_type.is_cfunction:
            return "<error>"
        formal_args = func_type.args
        arg_list_code = []
        for (formal_arg, actual_arg) in \
            zip(formal_args, self.args):
                arg_code = actual_arg.result_as(formal_arg.type)
                arg_list_code.append(arg_code)
        for actual_arg in self.args[len(formal_args):]:
            arg_list_code.append(actual_arg.result_code)
        result = "%s(%s)" % (self.function.result_code,
            join(arg_list_code, ","))
        return result
    
    def generate_result_code(self, code):
        func_type = self.function_type()
        if func_type.is_pyobject:
            if self.arg_tuple:
                arg_code = self.arg_tuple.py_result()
            else:
                arg_code = "0"
            code.putln(
                "%s = PyObject_CallObject(%s, %s); if (!%s) %s" % (
                    self.result_code,
                    self.function.py_result(),
                    arg_code,
                    self.result_code,
                    code.error_goto(self.pos)))
        elif func_type.is_cfunction:
            exc_checks = []
            if self.type.is_pyobject:
                exc_checks.append("!%s" % self.result_code)
            else:
                exc_val = func_type.exception_value
                exc_check = func_type.exception_check
                if exc_val is not None:
                    exc_checks.append("%s == %s" % (self.result_code, exc_val))
                if exc_check:
                    exc_checks.append("PyErr_Occurred()")
            if self.is_temp or exc_checks:
                rhs = self.c_call_code()
                if self.result_code:
                    lhs = "%s = " % self.result_code
                    if self.is_temp and self.type.is_pyobject:
                        #return_type = self.type # func_type.return_type
                        #print "SimpleCallNode.generate_result_code: casting", rhs, \
                        #	"from", return_type, "to pyobject" ###
                        rhs = typecast(py_object_type, self.type, rhs)
                else:
                    lhs = ""
                code.putln(
                    "%s%s; if (%s) %s" % (
                        lhs,
                        rhs,
                        " && ".join(exc_checks),
                        code.error_goto(self.pos)))
    

class GeneralCallNode(ExprNode):
    #  General Python function call, including keyword,
    #  * and ** arguments.
    #
    #  function         ExprNode
    #  positional_args  ExprNode          Tuple of positional arguments
    #  keyword_args     ExprNode or None  Dict of keyword arguments
    #  starstar_arg     ExprNode or None  Dict of extra keyword args
    
    subexprs = ['function', 'positional_args', 'keyword_args', 'starstar_arg']

    def analyse_types(self, env):
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
        self.is_temp = 1
        
    def generate_result_code(self, code):
        if self.keyword_args and self.starstar_arg:
            code.putln(
                "if (PyDict_Update(%s, %s) < 0) %s" % (
                    self.keyword_args.py_result(), 
                    self.starstar_arg.py_result(),
                    code.error_goto(self.pos)))
            keyword_code = self.keyword_args.py_result()
        elif self.keyword_args:
            keyword_code = self.keyword_args.py_result()
        elif self.starstar_arg:
            keyword_code = self.starstar_arg.py_result()
        else:
            keyword_code = None
        if not keyword_code:
            call_code = "PyObject_CallObject(%s, %s)" % (
                self.function.py_result(),
                self.positional_args.py_result())
        else:
            call_code = "PyEval_CallObjectWithKeywords(%s, %s, %s)" % (
                self.function.py_result(),
                self.positional_args.py_result(),
                keyword_code)
        code.putln(
            "%s = %s; if (!%s) %s" % (
                self.result_code,
                call_code,
                self.result_code,
                code.error_goto(self.pos)))


class AsTupleNode(ExprNode):
    #  Convert argument to tuple. Used for normalising
    #  the * argument of a function call.
    #
    #  arg    ExprNode
    
    subexprs = ['arg']
    
    def analyse_types(self, env):
        self.arg.analyse_types(env)
        self.arg = self.arg.coerce_to_pyobject(env)
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln(
            "%s = PySequence_Tuple(%s); if (!%s) %s" % (
                self.result_code,
                self.arg.py_result(),
                self.result_code,
                code.error_goto(self.pos)))
    

class AttributeNode(ExprNode):
    #  obj.attribute
    #
    #  obj          ExprNode
    #  attribute    string
    #
    #  Used internally:
    #
    #  is_py_attr           boolean   Is a Python getattr operation
    #  member               string    C name of struct member
    #  is_called            boolean   Function call is being done on result
    #  entry                Entry     Symbol table entry of attribute
    #  interned_attr_cname	string    C name of interned attribute name
    
    is_attribute = 1
    subexprs = ['obj']
    
    type = PyrexTypes.error_type
    result = "<error>"
    entry = None
    is_called = 0

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
                self.mutate_into_name_node(env, ubcm_entry, None)
                return 1
        return 0
    
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
            NameNode.analyse_entry(self, env)
    
    def analyse_as_ordinary_attribute(self, env, target):
        self.obj.analyse_types(env)
        self.analyse_attribute(env)
        if self.entry and self.entry.is_cmethod and not self.is_called:
            error(self.pos, "C method can only be called")
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
        if obj_type.is_ptr:
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
            else:
                error(self.pos, 
                    "Cannot select attribute of incomplete type '%s'" 
                    % obj_type)
                obj_type = PyrexTypes.error_type
            self.entry = entry
            if entry:
                if obj_type.is_extension_type and entry.name == "__weakref__":
                    error(self.pos, "Illegal use of special attribute __weakref__")
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
        if obj_type.is_pyobject:
            self.type = py_object_type
            self.is_py_attr = 1
            if Options.intern_names:
                self.interned_attr_cname = env.intern(self.attribute)
        else:
            if not obj_type.is_error:
                error(self.pos, 
                    "Object of type '%s' has no attribute '%s'" %
                    (obj_type, self.attribute))
        
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
        #print "...obj node =", self.obj, "code", self.obj.result_code ###
        #print "...obj type", self.obj.type, "ctype", self.obj.ctype() ###
        obj = self.obj
        obj_code = obj.result_as(obj.type)
        #print "...obj_code =", obj_code ###
        if self.entry and self.entry.is_cmethod:
            return "((struct %s *)%s%s%s)->%s" % (
                obj.type.vtabstruct_cname, obj_code, self.op, 
                obj.type.vtabslot_cname, self.member)
        else:
            return "%s%s%s" % (obj_code, self.op, self.member)
    
    def generate_result_code(self, code):
        if self.is_py_attr:
            if Options.intern_names:
                code.putln(
                    '%s = PyObject_GetAttr(%s, %s); if (!%s) %s' % (
                        self.result_code,
                        self.obj.py_result(),
                        self.interned_attr_cname,
                        self.result_code,
                        code.error_goto(self.pos)))
            else:
                code.putln(
                    '%s = PyObject_GetAttrString(%s, "%s"); if (!%s) %s' % (
                        self.result_code,
                        self.objpy_result(),
                        self.attribute,
                        self.result_code,
                        code.error_goto(self.pos)))
    
    def generate_assignment_code(self, rhs, code):
        self.obj.generate_evaluation_code(code)
        if self.is_py_attr:
            if Options.intern_names:
                code.putln(
                    'if (PyObject_SetAttr(%s, %s, %s) < 0) %s' % (
                        self.obj.py_result(),
                        self.interned_attr_cname,
                        rhs.py_result(),
                        code.error_goto(self.pos)))
            else:
                code.putln(
                    'if (PyObject_SetAttrString(%s, "%s", %s) < 0) %s' % (
                        self.obj.py_result(),
                        self.attribute,
                        rhs.py_result(),
                        code.error_goto(self.pos)))
            rhs.generate_disposal_code(code)
        else:
            select_code = self.result_code
            if self.type.is_pyobject:
                rhs.make_owned_reference(code)
                code.put_decref(select_code, self.ctype())
            code.putln(
                "%s = %s;" % (
                    select_code,
                    rhs.result_as(self.ctype())))
                    #rhs.result_code))
            rhs.generate_post_assignment_code(code)
        self.obj.generate_disposal_code(code)
    
    def generate_deletion_code(self, code):
        self.obj.generate_evaluation_code(code)
        if self.is_py_attr:
            if Options.intern_names:
                code.putln(
                    'if (PyObject_DelAttr(%s, %s) < 0) %s' % (
                        self.obj.py_result(),
                        self.interned_attr_cname,
                        code.error_goto(self.pos)))
            else:
                code.putln(
                    'if (PyObject_DelAttrString(%s, "%s") < 0) %s' % (
                        self.obj.py_result(),
                        self.attribute,
                        code.error_goto(self.pos)))
        else:
            error(self.pos, "Cannot delete C attribute of extension type")
        self.obj.generate_disposal_code(code)

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
    
    def analyse_target_declaration(self, env):
        for arg in self.args:
            arg.analyse_target_declaration(env)

    def analyse_types(self, env):
        for i in range(len(self.args)):
            arg = self.args[i]
            arg.analyse_types(env)
            self.args[i] = arg.coerce_to_pyobject(env)
        self.type = py_object_type
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
        if rhs:
            rhs.release_temp(env)
        for arg, node in zip(self.args, self.coerced_unpacked_items):
            node.allocate_temps(env)
            arg.allocate_target_temps(env, node)
            #arg.release_target_temp(env)
            #node.release_temp(env)
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
            "%s = PyObject_GetIter(%s); if (!%s) %s" % (
                self.iterator.result_code,
                rhs.py_result(),
                self.iterator.result_code,
                code.error_goto(self.pos)))
        rhs.generate_disposal_code(code)
        for i in range(len(self.args)):
            item = self.unpacked_items[i]
            unpack_code = "__Pyx_UnpackItem(%s)" % (
                self.iterator.py_result())
            code.putln(
                "%s = %s; if (!%s) %s" % (
                    item.result_code,
                    typecast(item.ctype(), py_object_type, unpack_code),
                    item.result_code,
                    code.error_goto(self.pos)))
            value_node = self.coerced_unpacked_items[i]
            value_node.generate_evaluation_code(code)
            self.args[i].generate_assignment_code(value_node, code)
        code.putln(
            "if (__Pyx_EndUnpack(%s) < 0) %s" % (
                self.iterator.py_result(),
                code.error_goto(self.pos)))
        if debug_disposal_code:
            print "UnpackNode.generate_assignment_code:"
            print "...generating disposal code for", rhs
        self.iterator.generate_disposal_code(code)


class TupleNode(SequenceNode):
    #  Tuple constructor.

    def generate_operation_code(self, code):
        code.putln(
            "%s = PyTuple_New(%s); if (!%s) %s" % (
                self.result_code,
                len(self.args),
                self.result_code,
                code.error_goto(self.pos)))
        for i in range(len(self.args)):
            arg = self.args[i]
            if not arg.result_in_temp():
                code.put_incref(arg.result_code, arg.ctype())
            code.putln(
                "PyTuple_SET_ITEM(%s, %s, %s);" % (
                    self.result_code,
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
    
    def generate_operation_code(self, code):
        code.putln("%s = PyList_New(%s); if (!%s) %s" %
            (self.result_code,
            len(self.args),
            self.result_code,
            code.error_goto(self.pos)))
        for i in range(len(self.args)):
            arg = self.args[i]
            #if not arg.is_temp:
            if not arg.result_in_temp():
                code.put_incref(arg.result_code, arg.ctype())
            code.putln("PyList_SET_ITEM(%s, %s, %s);" %
                (self.result_code,
                i,
                arg.py_result()))
                
    def generate_subexpr_disposal_code(self, code):
        # We call generate_post_assignment_code here instead
        # of generate_disposal_code, because values were stored
        # in the list using a reference-stealing operation.
        for arg in self.args:
            arg.generate_post_assignment_code(code)		


class DictNode(ExprNode):
    #  Dictionary constructor.
    #
    #  key_value_pairs  [(ExprNode, ExprNode)]
    
    def analyse_types(self, env):
        new_pairs = []
        for key, value in self.key_value_pairs:
            key.analyse_types(env)
            value.analyse_types(env)
            key = key.coerce_to_pyobject(env)
            value = value.coerce_to_pyobject(env)
            new_pairs.append((key, value))
        self.key_value_pairs = new_pairs
        self.type = py_object_type
        self.is_temp = 1
    
    def allocate_temps(self, env, result = None):
        #  Custom method used here because key-value
        #  pairs are evaluated and used one at a time.
        self.allocate_temp(env, result)
        for key, value in self.key_value_pairs:
            key.allocate_temps(env)
            value.allocate_temps(env)
            key.release_temp(env)
            value.release_temp(env)
    
    def generate_evaluation_code(self, code):
        #  Custom method used here because key-value
        #  pairs are evaluated and used one at a time.
        code.putln(
            "%s = PyDict_New(); if (!%s) %s" % (
                self.result_code,
                self.result_code,
                code.error_goto(self.pos)))
        for key, value in self.key_value_pairs:
            key.generate_evaluation_code(code)
            value.generate_evaluation_code(code)
            code.putln(
                "if (PyDict_SetItem(%s, %s, %s) < 0) %s" % (
                    self.result_code,
                    key.py_result(),
                    value.py_result(),
                    code.error_goto(self.pos)))
            key.generate_disposal_code(code)
            value.generate_disposal_code(code)
    

class ClassNode(ExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a class object given
    #  a name, tuple of bases and class dictionary.
    #
    #  name         ExprNode           Name of the class
    #  bases        ExprNode           Base class tuple
    #  dict         ExprNode           Class dict (not owned by this node)
    #  doc          ExprNode or None   Doc string
    #  module_name  string             Name of defining module
    
    subexprs = ['name', 'bases', 'doc']
    
    def analyse_types(self, env):
        self.name.analyse_types(env)
        self.name = self.name.coerce_to_pyobject(env)
        self.bases.analyse_types(env)
        if self.doc:
            self.doc.analyse_types(env)
            self.doc = self.doc.coerce_to_pyobject(env)
        self.module_name = env.global_scope().qualified_name
        self.type = py_object_type
        self.is_temp = 1
        env.use_utility_code(create_class_utility_code);
    
    def generate_result_code(self, code):
        if self.doc:
            code.putln(
                'if (PyDict_SetItemString(%s, "__doc__", %s) < 0) %s' % (
                    self.dict.py_result(),
                    self.doc.py_result(),
                    code.error_goto(self.pos)))
        code.putln(
            '%s = __Pyx_CreateClass(%s, %s, %s, "%s"); if (!%s) %s' % (
                self.result_code,
                self.bases.py_result(),
                self.dict.py_result(),
                self.name.py_result(),
                self.module_name,
                self.result_code,
                code.error_goto(self.pos)))


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
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln(
            "%s = PyMethod_New(%s, 0, %s); if (!%s) %s" % (
                self.result_code,
                self.function.py_result(),
                self.class_cname,
                self.result_code,
                code.error_goto(self.pos)))


class PyCFunctionNode(AtomicExprNode):
    #  Helper class used in the implementation of Python
    #  class definitions. Constructs a PyCFunction object
    #  from a PyMethodDef struct.
    #
    #  pymethdef_cname   string   PyMethodDef structure
    
    def analyse_types(self, env):
        self.type = py_object_type
        self.is_temp = 1
    
    def generate_result_code(self, code):
        code.putln(
            "%s = PyCFunction_New(&%s, 0); if (!%s) %s" % (
                self.result_code,
                self.pymethdef_cname,
                self.result_code,
                code.error_goto(self.pos)))

#-------------------------------------------------------------------
#
#  Unary operator nodes
#
#-------------------------------------------------------------------

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
    
    def analyse_types(self, env):
        self.operand.analyse_types(env)
        if self.is_py_operation():
            self.coerce_operand_to_pyobject(env)
            self.type = py_object_type
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
            "%s = %s(%s); if (!%s) %s" % (
                self.result_code, 
                function, 
                self.operand.py_result(),
                self.result_code,
                code.error_goto(self.pos)))
        
    def type_error(self):
        if not self.operand.type.is_error:
            error(self.pos, "Invalid operand type for '%s' (%s)" %
                (self.operator, self.operand.type))
        self.type = PyrexTypes.error_type


class NotNode(ExprNode):
    #  'not' operator
    #
    #  operand   ExprNode
    
    subexprs = ['operand']
    
    def analyse_types(self, env):
        self.operand.analyse_types(env)
        self.operand = self.operand.coerce_to_boolean(env)
        self.type = PyrexTypes.c_int_type
    
    def calculate_result_code(self):
        return "(!%s)" % self.operand.result_code
    
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
        return self.operand.result_code


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
        return "(-%s)" % self.operand.result_code


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
        return "(~%s)" % self.operand.result_code


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
        return "(&%s)" % self.operand.result_code

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
    return unop_node_classes[operator](pos, 
        operator = operator, 
        operand = operand)


class TypecastNode(ExprNode):
    #  C type cast
    #
    #  base_type    CBaseTypeNode
    #  declarator   CDeclaratorNode
    #  operand      ExprNode
    
    subexprs = ['operand']
    
    def analyse_types(self, env):
        base_type = self.base_type.analyse(env)
        _, self.type = self.declarator.analyse(base_type, env)
        self.operand.analyse_types(env)
        to_py = self.type.is_pyobject
        from_py = self.operand.type.is_pyobject
        if from_py and not to_py and self.operand.is_ephemeral():
            error(self.pos, "Casting temporary Python object to non-Python type")
        if to_py and not from_py:
            self.result_ctype = py_object_type
            self.is_temp = 1			
    
    def check_const(self):
        self.operand.check_const()
    
    def calculate_result_code(self):
        opnd = self.operand
        result_code = self.type.cast_code(opnd.result_code)
        return result_code
    
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
                    self.result_code,
                    self.operand.result_code))
            code.put_incref(self.result_code, self.ctype())


class SizeofNode(ExprNode):
    #  Abstract base class for sizeof(x) expression nodes.

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
    
    def analyse_types(self, env):
        base_type = self.base_type.analyse(env)
        _, arg_type = self.declarator.analyse(base_type, env)
        self.arg_type = arg_type
        if arg_type.is_pyobject:
            error(self.pos, "Cannot take sizeof Python object")
        elif arg_type.is_void:
            error(self.pos, "Cannot take sizeof void")
        elif not arg_type.is_complete():
            error(self.pos, "Cannot take sizeof incomplete type '%s'" % arg_type)
        self.type = PyrexTypes.c_int_type
        
    def calculate_result_code(self):
        arg_code = self.arg_type.declaration_code("")
        return "(sizeof(%s))" % arg_code
    

class SizeofVarNode(SizeofNode):
    #  C sizeof function applied to a variable
    #
    #  operand   ExprNode
    
    subexprs = ['operand']
    
    def analyse_types(self, env):
        self.operand.analyse_types(env)
        self.type = PyrexTypes.c_int_type
    
    def calculate_result_code(self):
        return "(sizeof(%s))" % self.operand.result_code
    
    def generate_result_code(self, code):
        pass


#-------------------------------------------------------------------
#
#  Binary operator nodes
#
#-------------------------------------------------------------------

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
                "%s = %s(%s, %s%s); if (!%s) %s" % (
                    self.result_code, 
                    function, 
                    self.operand1.py_result(),
                    self.operand2.py_result(),
                    extra_args,
                    self.result_code,
                    code.error_goto(self.pos)))
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
        self.type = self.compute_c_result_type(type1, type2)
        if not self.type:
            self.type_error()
    
    def compute_c_result_type(self, type1, type2):
        if self.c_types_okay(type1, type2):
            return PyrexTypes.widest_numeric_type(type1, type2)
        else:
            return None
    
    def c_types_okay(self, type1, type2):
        return type1.is_numeric and type2.is_numeric

    def calculate_result_code(self):
        return "(%s %s %s)" % (
            self.operand1.result_code, 
            self.operator, 
            self.operand2.result_code)
    
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
        "/":		"PyNumber_Divide",
        "%":		"PyNumber_Remainder",
        "**":   "PyNumber_Power"
    }


class IntBinopNode(NumBinopNode):
    #  Binary operation taking integer arguments.
    
    def c_types_okay(self, type1, type2):
        return type1.is_int and type2.is_int

    
class AddNode(NumBinopNode):
    #  '+' operator.
    
    def is_py_operation(self):
        if self.operand1.type.is_string \
            and self.operand2.type.is_string:
                return 1
        else:
            return NumBinopNode.is_py_operation(self)

    def compute_c_result_type(self, type1, type2):
        if type1.is_ptr and type2.is_int:
            return type1
        elif type1.is_int and type2.is_ptr:
            return type2
        else:
            return NumBinopNode.compute_c_result_type(
                self, type1, type2)


class SubNode(NumBinopNode):
    #  '-' operator.
    
    def compute_c_result_type(self, type1, type2):
        if type1.is_ptr and type2.is_int:
            return type1
        elif type1.is_ptr and type2.is_ptr:
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


class ModNode(IntBinopNode):
    #  '%' operator.
    
    def is_py_operation(self):
        return (self.operand1.type.is_string
            or self.operand2.type.is_string
            or IntBinopNode.is_py_operation(self))


class PowNode(NumBinopNode):
    #  '**' operator.
    
    def analyse_types(self, env):
        env.pow_function_used = 1
        NumBinopNode.analyse_types(self, env)
    
    def compute_c_result_type(self, type1, type2):
        if self.c_types_okay(type1, type2):
            return PyrexTypes.c_double_type
        else:
            return None
    
    def calculate_result_code(self):
        return "pow(%s, %s)" % (
            self.operand1.result_code, self.operand2.result_code)
            

class BoolBinopNode(ExprNode):
    #  Short-circuiting boolean operation.
    #
    #  operator     string
    #  operand1     ExprNode
    #  operand2     ExprNode
    #  temp_bool    ExprNode     used internally
    
    temp_bool = None
    
    subexprs = ['operand1', 'operand2', 'temp_bool']
    
    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        if self.operand1.type.is_pyobject or \
                self.operand2.type.is_pyobject:
            self.operand1 = self.operand1.coerce_to_pyobject(env)
            self.operand2 = self.operand2.coerce_to_pyobject(env)
            self.temp_bool = TempNode(self.pos,
                PyrexTypes.c_int_type, env)
            self.type = py_object_type
        else:
            self.operand1 = self.operand1.coerce_to_boolean(env)
            self.operand2 = self.operand2.coerce_to_boolean(env)
            self.type = PyrexTypes.c_int_type
        # For what we're about to do, it's vital that
        # both operands be temp nodes.
        self.operand1 = self.operand1.coerce_to_temp(env) #CTT
        self.operand2 = self.operand2.coerce_to_temp(env)
        # coerce_to_simple does not seem to be sufficient
        #self.operand1 = self.operand1.coerce_to_simple(env)
        #self.operand2 = self.operand2.coerce_to_simple(env)
        self.is_temp = 1
    
    def allocate_temps(self, env, result_code = None):
        #  We don't need both operands at the same time, and
        #  one of the operands will also be our result. So we
        #  use an allocation strategy here which results in
        #  this node and both its operands sharing the same
        #  result variable. This allows us to avoid some 
        #  assignments and increfs/decrefs that would otherwise
        #  be necessary.
        self.allocate_temp(env, result_code)
        self.operand1.allocate_temps(env, self.result_code)
        if self.temp_bool:
            self.temp_bool.allocate_temp(env)
            self.temp_bool.release_temp(env)
        self.operand2.allocate_temps(env, self.result_code)
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
            self.operand1.result_code,
            self.py_to_c_op[self.operator],
            self.operand2.result_code)
    
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
            test_result = self.temp_bool.result_code
            code.putln(
                "%s = PyObject_IsTrue(%s); if (%s < 0) %s" % (
                    test_result,
                    self.operand1.py_result(),
                    test_result,
                    code.error_goto(self.pos)))
        else:
            test_result = self.operand1.result_code
        return test_result


class CmpNode:
    #  Mixin class containing code common to PrimaryCmpNodes
    #  and CascadedCmpNodes.
    
    def is_python_comparison(self):
        return (self.has_python_operands()
            or (self.cascade and self.cascade.is_python_comparison())
            or self.operator in ('in', 'not_in'))

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
            return 0

    def generate_operation_code(self, code, result_code, 
            operand1, op , operand2):
        if op == 'in' or op == 'not_in':
            code.putln(
                "%s = PySequence_Contains(%s, %s); if (%s < 0) %s" % (
                    result_code, 
                    operand2.py_result(), 
                    operand1.py_result(), 
                    result_code,
                    code.error_goto(self.pos)))
            if op == 'not_in':
                code.putln(
                    "%s = !%s;" % (
                        result_code, result_code))
        elif (operand1.type.is_pyobject
            and op not in ('is', 'is_not')):
                code.putln(
                    "if (PyObject_Cmp(%s, %s, &%s) < 0) %s" % (
                        operand1.py_result(), 
                        operand2.py_result(), 
                        result_code,
                        code.error_goto(self.pos)))
                code.putln(
                    "%s = %s %s 0;" % (
                        result_code, result_code, op))
        else:
            code.putln("%s = %s %s %s;" % (
                result_code, 
                operand1.result_code, 
                self.c_operator(op), 
                operand2.result_code))
    
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
    
    cascade = None
    
    def analyse_types(self, env):
        self.operand1.analyse_types(env)
        self.operand2.analyse_types(env)
        if self.cascade:
            self.cascade.analyse_types(env, self.operand2)
        self.is_pycmp = self.is_python_comparison()
        if self.is_pycmp:
            self.coerce_operands_to_pyobjects(env)
        if self.cascade:
            #self.operand2 = self.operand2.coerce_to_temp(env) #CTT
            self.operand2 = self.operand2.coerce_to_simple(env)
            self.cascade.coerce_cascaded_operands_to_temp(env)
        self.check_operand_types(env)
        self.type = PyrexTypes.c_int_type
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
            self.operand1.result_code,
            self.c_operator(self.operator),
            self.operand2.result_code)
    
    def generate_evaluation_code(self, code):
        self.operand1.generate_evaluation_code(code)
        self.operand2.generate_evaluation_code(code)
        if self.is_temp:
            self.generate_operation_code(code, self.result_code, 
                self.operand1, self.operator, self.operand2)
            if self.cascade:
                self.cascade.generate_evaluation_code(code,
                    self.result_code, self.operand2)
            self.operand1.generate_disposal_code(code)
            self.operand2.generate_disposal_code(code)
    
    def generate_subexpr_disposal_code(self, code):
        #  If this is called, it is a non-cascaded cmp,
        #  so only need to dispose of the two main operands.
        self.operand1.generate_disposal_code(code)
        self.operand2.generate_disposal_code(code)


class CascadedCmpNode(Node, CmpNode):
    #  A CascadedCmpNode is not a complete expression node. It 
    #  hangs off the side of another comparison node, shares 
    #  its left operand with that node, and shares its result 
    #  with the PrimaryCmpNode at the head of the chain.
    #
    #  operator      string
    #  operand2      ExprNode
    #  cascade       CascadedCmpNode

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
            print self, "Coercing", self.arg


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
        assert dst_type.is_extension_type, "PyTypeTest on non extension type"
        CoercionNode.__init__(self, arg)
        self.type = dst_type
        self.result_ctype = arg.ctype()
        env.use_utility_code(type_test_utility_code)
    
    def result_in_temp(self):
        return self.arg.result_in_temp()
    
    def is_ephemeral(self):
        return self.arg.is_ephemeral()
    
    def calculate_result_code(self):
        return self.arg.result_code
    
    def generate_result_code(self, code):
        if self.type.typeobj_is_available():
            code.putln(
                "if (!__Pyx_TypeTest(%s, %s)) %s" % (
                    self.arg.py_result(),
                    self.type.typeptr_cname,
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
        self.is_temp = 1
        if not arg.type.to_py_function:
            error(arg.pos,
                "Cannot convert '%s' to Python object" % arg.type)
    
    def generate_result_code(self, code):
        function = self.arg.type.to_py_function
        code.putln('%s = %s(%s); if (!%s) %s' % (
            self.result_code, 
            function, 
            self.arg.result_code, 
            self.result_code, 
            code.error_goto(self.pos)))


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
    
    def generate_result_code(self, code):
        function = self.type.from_py_function
        operand = self.arg.py_result()
        rhs = "%s(%s)" % (function, operand)
        if self.type.is_enum:
            rhs = typecast(self.type, c_long_type, rhs)
        code.putln('%s = %s; if (PyErr_Occurred()) %s' % (
            self.result_code, 
            rhs, 
            code.error_goto(self.pos)))


class CoerceToBooleanNode(CoercionNode):
    #  This node is used when a result needs to be used
    #  in a boolean context.
    
    def __init__(self, arg, env):
        CoercionNode.__init__(self, arg)
        self.type = PyrexTypes.c_int_type
        if arg.type.is_pyobject:
            self.is_temp = 1
    
    def check_const(self):
        if self.is_temp:
            self.not_const()
        self.arg.check_const()
    
    def calculate_result_code(self):
        return "(%s != 0)" % self.arg.result_code

    def generate_result_code(self, code):
        if self.arg.type.is_pyobject:
            code.putln(
                "%s = PyObject_IsTrue(%s); if (%s < 0) %s" % (
                    self.result_code, 
                    self.arg.py_result(), 
                    self.result_code,
                    code.error_goto(self.pos)))


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
    
    def generate_result_code(self, code):
        #self.arg.generate_evaluation_code(code) # Already done
        # by generic generate_subexpr_evaluation_code!
        code.putln("%s = %s;" % (
            self.result_code, self.arg.result_as(self.ctype())))
        if self.type.is_pyobject:
            code.put_incref(self.result_code, self.ctype())


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
        self.type = arg.type
        self.result_ctype = arg.result_ctype
    
    def calculate_result_code(self):
        return self.arg.result_code
    
    #def result_as_extension_type(self):
    #	return self.arg.result_as_extension_type()
    
    def generate_evaluation_code(self, code):
        pass

    def generate_result_code(self, code):
        pass
    
#------------------------------------------------------------------------------------
#
#  Runtime support code
#
#------------------------------------------------------------------------------------

get_name_utility_code = [
"""
static PyObject *__Pyx_GetName(PyObject *dict, char *name); /*proto*/
""","""
static PyObject *__Pyx_GetName(PyObject *dict, char *name) {
    PyObject *result;
    result = PyObject_GetAttrString(dict, name);
    if (!result)
        PyErr_SetString(PyExc_NameError, name);
    return result;
}
"""]

get_name_interned_utility_code = [
"""
static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/
""","""
static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name) {
    PyObject *result;
    result = PyObject_GetAttr(dict, name);
    if (!result)
        PyErr_SetObject(PyExc_NameError, name);
    return result;
}
"""]

#------------------------------------------------------------------------------------

import_utility_code = [
"""
static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/
""","""
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
}]

#------------------------------------------------------------------------------------

get_exception_utility_code = [
"""
static PyObject *__Pyx_GetExcValue(void); /*proto*/
""","""
static PyObject *__Pyx_GetExcValue(void) {
    PyObject *type = 0, *value = 0, *tb = 0;
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
    Py_XDECREF(tstate->exc_type);
    Py_XDECREF(tstate->exc_value);
    Py_XDECREF(tstate->exc_traceback);
    tstate->exc_type = type;
    tstate->exc_value = value;
    tstate->exc_traceback = tb;
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
"""]

#------------------------------------------------------------------------------------

unpacking_utility_code = [
"""
static PyObject *__Pyx_UnpackItem(PyObject *); /*proto*/
static int __Pyx_EndUnpack(PyObject *); /*proto*/
""","""
static void __Pyx_UnpackError(void) {
    PyErr_SetString(PyExc_ValueError, "unpack sequence of wrong size");
}

static PyObject *__Pyx_UnpackItem(PyObject *iter) {
    PyObject *item;
    if (!(item = PyIter_Next(iter))) {
        if (!PyErr_Occurred())
            __Pyx_UnpackError();
    }
    return item;
}

static int __Pyx_EndUnpack(PyObject *iter) {
    PyObject *item;
    if ((item = PyIter_Next(iter))) {
        Py_DECREF(item);
        __Pyx_UnpackError();
        return -1;
    }
    else if (!PyErr_Occurred())
        return 0;
    else
        return -1;
}
"""]

#------------------------------------------------------------------------------------

type_test_utility_code = [
"""
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type); /*proto*/
""","""
static int __Pyx_TypeTest(PyObject *obj, PyTypeObject *type) {
    if (!type) {
        PyErr_Format(PyExc_SystemError, "Missing type object");
        return 0;
    }
    if (obj == Py_None || PyObject_TypeCheck(obj, type))
        return 1;
    PyErr_Format(PyExc_TypeError, "Cannot convert %s to %s",
        obj->ob_type->tp_name, type->tp_name);
    return 0;
}
"""]

#------------------------------------------------------------------------------------

create_class_utility_code = [
"""
static PyObject *__Pyx_CreateClass(PyObject *bases, PyObject *dict, PyObject *name, char *modname); /*proto*/
""","""
static PyObject *__Pyx_CreateClass(
    PyObject *bases, PyObject *dict, PyObject *name, char *modname)
{
    PyObject *py_modname;
    PyObject *result = 0;
    
    py_modname = PyString_FromString(modname);
    if (!py_modname)
        goto bad;
    if (PyDict_SetItemString(dict, "__module__", py_modname) < 0)
        goto bad;
    result = PyClass_New(bases, dict, name);
bad:
    Py_XDECREF(py_modname);
    return result;
}
"""]

#------------------------------------------------------------------------------------
