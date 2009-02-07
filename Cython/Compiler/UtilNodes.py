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
    # handle   TempHandle

    def generate_assignment_code(self, rhs, code):
        pass

    def generate_execution_code(self, code):
        if self.type.is_pyobject:
            code.put_decref_clear(self.result(), self.type)
            self.handle.needs_cleanup = False

class TempsBlockNode(Node):
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

    def analyse_types(self, env):
        self.type = self.expression.type

    def result(self):
        return self.result_code

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

    def free_temps(self, code):
        pass


class EvalWithTempExprNode(ExprNodes.NewTempExprNode):
    # A wrapper around a subexpression that moves an expression into a
    # temp variable and provides it to the subexpression.

    subexprs = ['temp_expression', 'subexpression']

    def __init__(self, lazy_temp, subexpression):
        self.pos = subexpression.pos
        self.lazy_temp = lazy_temp
        self.temp_expression = lazy_temp.expression
        self.subexpression = subexpression

    def result(self):
        return self.subexpression.result()

    def analyse_types(self, env):
        self.temp_expression.analyse_types(env)
        self.subexpression.analyse_types(env)
        self.type = self.subexpression.type

    def generate_evaluation_code(self, code):
        self.temp_expression.generate_evaluation_code(code)
        result_in_temp = self.temp_expression.result_in_temp()
        temp_type = self.temp_expression.type
        if result_in_temp:
            temp = self.temp_expression.result()
        else:
            self.temp_expression.make_owned_reference(code)
            temp = code.funcstate.allocate_temp(
                temp_type, manage_ref=True)
            code.putln("%s = %s;" % (temp, self.temp_expression.result()))
        self.lazy_temp.result_code = temp
        self.subexpression.generate_evaluation_code(code)
        if not result_in_temp:
            if temp_type.is_pyobject:
                code.put_decref_clear(temp, temp_type)
            code.funcstate.release_temp(temp)
