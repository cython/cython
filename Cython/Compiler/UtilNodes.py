#
# Nodes used as utilities and support for transforms etc.
# These often make up sets including both Nodes and ExprNodes
# so it is convenient to have them in a seperate module.
#

import Nodes
import ExprNodes
from Nodes import Node
from ExprNodes import AtomicExprNode

class TempHandle(object):
    # THIS IS DEPRECATED, USE LetRefNode instead
    temp = None
    needs_xdecref = False
    def __init__(self, type):
        self.type = type
        self.needs_cleanup = type.is_pyobject

    def ref(self, pos):
        return TempRefNode(pos, handle=self, type=self.type)

    def cleanup_ref(self, pos):
        return CleanupTempRefNode(pos, handle=self, type=self.type)

class TempRefNode(AtomicExprNode):
    # THIS IS DEPRECATED, USE LetRefNode instead
    # handle   TempHandle

    def analyse_types(self, env):
        assert self.type == self.handle.type
    
    def analyse_target_types(self, env):
        assert self.type == self.handle.type

    def analyse_target_declaration(self, env):
        pass

    def calculate_result_code(self):
        result = self.handle.temp
        if result is None: result = "<error>" # might be called and overwritten
        return result

    def generate_result_code(self, code):
        pass

    def generate_assignment_code(self, rhs, code):
        if self.type.is_pyobject:
            rhs.make_owned_reference(code)
            # TODO: analyse control flow to see if this is necessary
            code.put_xdecref(self.result(), self.ctype())
        code.putln('%s = %s;' % (self.result(), rhs.result_as(self.ctype())))
        rhs.generate_post_assignment_code(code)
        rhs.free_temps(code)

class CleanupTempRefNode(TempRefNode):
    # THIS IS DEPRECATED, USE LetRefNode instead
    # handle   TempHandle

    def generate_assignment_code(self, rhs, code):
        pass

    def generate_execution_code(self, code):
        if self.type.is_pyobject:
            code.put_decref_clear(self.result(), self.type)
            self.handle.needs_cleanup = False

class TempsBlockNode(Node):
    # THIS IS DEPRECATED, USE LetNode instead
    
    """
    Creates a block which allocates temporary variables.
    This is used by transforms to output constructs that need
    to make use of a temporary variable. Simply pass the types
    of the needed temporaries to the constructor.
    
    The variables can be referred to using a TempRefNode
    (which can be constructed by calling get_ref_node).
    """

    # temps   [TempHandle]
    # body    StatNode
    
    child_attrs = ["body"]

    def generate_execution_code(self, code):
        for handle in self.temps:
            handle.temp = code.funcstate.allocate_temp(
                handle.type, manage_ref=handle.needs_cleanup)
        self.body.generate_execution_code(code)
        for handle in self.temps:
            if handle.needs_cleanup:
                if handle.needs_xdecref:
                    code.put_xdecref_clear(handle.temp, handle.type)
                else:
                    code.put_decref_clear(handle.temp, handle.type)
            code.funcstate.release_temp(handle.temp)

    def analyse_control_flow(self, env):
        self.body.analyse_control_flow(env)

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)
    
    def analyse_expressions(self, env):
        self.body.analyse_expressions(env)
    
    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)
            
    def annotate(self, code):
        self.body.annotate(code)


class ResultRefNode(AtomicExprNode):
    # A reference to the result of an expression.  The result_code
    # must be set externally (usually a temp name).

    subexprs = []

    def __init__(self, expression):
        self.pos = expression.pos
        self.expression = expression
        if hasattr(expression, "type"):
            self.type = expression.type

    def analyse_types(self, env):
        self.type = self.expression.type

    def infer_type(self, env):
        return self.expression.infer_type(env)

    def result(self):
        return self.result_code

    def generate_evaluation_code(self, code):
        pass

    def generate_result_code(self, code):
        pass
        
    def generate_disposal_code(self, code):
        pass
                
    def generate_assignment_code(self, rhs, code):
        if self.type.is_pyobject:
            rhs.make_owned_reference(code)
            code.put_decref(self.result(), self.ctype())
        code.putln('%s = %s;' % (self.result(), rhs.result_as(self.ctype())))
        rhs.generate_post_assignment_code(code)
        rhs.free_temps(code)

    def allocate_temps(self, env):
        pass
        
    def release_temp(self, env):
        pass

    def free_temps(self, code):
        pass


class LetNodeMixin:
    def set_temp_expr(self, lazy_temp):
        self.lazy_temp = lazy_temp
        self.temp_expression = lazy_temp.expression

    def setup_temp_expr(self, code):
        self.temp_expression.generate_evaluation_code(code)
        self._result_in_temp = self.temp_expression.result_in_temp()
        self.temp_type = self.temp_expression.type
        if self._result_in_temp:
            self.temp = self.temp_expression.result()
        else:
            self.temp_expression.make_owned_reference(code)
            self.temp = code.funcstate.allocate_temp(
                self.temp_type, manage_ref=True)
            code.putln("%s = %s;" % (self.temp, self.temp_expression.result()))
        self.lazy_temp.result_code = self.temp

    def teardown_temp_expr(self, code):
       if not self._result_in_temp:
            if self.temp_type.is_pyobject:
                code.put_decref_clear(self.temp, self.temp_type)
            code.funcstate.release_temp(self.temp)

class EvalWithTempExprNode(ExprNodes.ExprNode, LetNodeMixin):
    # A wrapper around a subexpression that moves an expression into a
    # temp variable and provides it to the subexpression.

    subexprs = ['temp_expression', 'subexpression']

    def __init__(self, lazy_temp, subexpression):
        self.set_temp_expr(lazy_temp)
        self.pos = subexpression.pos
        self.subexpression = subexpression
        # if called after type analysis, we already know the type here
        self.type = self.subexpression.type

    def infer_type(self, env):
        return self.subexpression.infer_type(env)

    def result(self):
        return self.subexpression.result()

    def analyse_types(self, env):
        self.temp_expression.analyse_types(env)
        self.subexpression.analyse_types(env)
        self.type = self.subexpression.type

    def generate_evaluation_code(self, code):
        self.setup_temp_expr(code)
        self.subexpression.generate_evaluation_code(code)
        self.teardown_temp_expr(code)
 
LetRefNode = ResultRefNode

class LetNode(Nodes.StatNode, LetNodeMixin):
    # Implements a local temporary variable scope. Imagine this
    # syntax being present:
    # let temp = VALUE:
    #     BLOCK (can modify temp)
    #     if temp is an object, decref
    #
    # To be used after analysis phase, does no analysis.

    child_attrs = ['temp_expression', 'body']

    def __init__(self, lazy_temp, body):
        self.set_temp_expr(lazy_temp)
        self.pos = body.pos
        self.body = body

    def generate_execution_code(self, code):
        self.setup_temp_expr(code)
        self.body.generate_execution_code(code)
        self.teardown_temp_expr(code)
