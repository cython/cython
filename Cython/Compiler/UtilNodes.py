#
# Nodes used as utilities and support for transforms etc.
# These often make up sets including both Nodes and ExprNodes
# so it is convenient to have them in a separate module.
#

from __future__ import absolute_import

from . import Nodes
from . import ExprNodes
from .Nodes import Node
from .ExprNodes import AtomicExprNode
from .PyrexTypes import c_ptr_type, c_bint_type


class TempHandle(object):
    # THIS IS DEPRECATED, USE LetRefNode instead
    temp = None
    needs_xdecref = False
    def __init__(self, type, needs_cleanup=None):
        self.type = type
        if needs_cleanup is None:
            self.needs_cleanup = type.is_pyobject
        else:
            self.needs_cleanup = needs_cleanup

    def ref(self, pos):
        return TempRefNode(pos, handle=self, type=self.type)


class TempRefNode(AtomicExprNode):
    # THIS IS DEPRECATED, USE LetRefNode instead
    # handle   TempHandle

    def analyse_types(self, env):
        assert self.type == self.handle.type
        return self

    def analyse_target_types(self, env):
        assert self.type == self.handle.type
        return self

    def analyse_target_declaration(self, env):
        pass

    def calculate_result_code(self):
        result = self.handle.temp
        if result is None: result = "<error>"  # might be called and overwritten
        return result

    def generate_result_code(self, code):
        pass

    def generate_assignment_code(self, rhs, code, overloaded_assignment=False):
        if self.type.is_pyobject:
            rhs.make_owned_reference(code)
            # TODO: analyse control flow to see if this is necessary
            code.put_xdecref(self.result(), self.ctype())
        code.putln('%s = %s;' % (
            self.result(),
            rhs.result() if overloaded_assignment else rhs.result_as(self.ctype()),
        ))
        rhs.generate_post_assignment_code(code)
        rhs.free_temps(code)


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

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)

    def analyse_expressions(self, env):
        self.body = self.body.analyse_expressions(env)
        return self

    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)

    def annotate(self, code):
        self.body.annotate(code)


class ResultRefNode(AtomicExprNode):
    # A reference to the result of an expression.  The result_code
    # must be set externally (usually a temp name).

    subexprs = []
    lhs_of_first_assignment = False

    def __init__(self, expression=None, pos=None, type=None, may_hold_none=True, is_temp=False):
        self.expression = expression
        self.pos = None
        self.may_hold_none = may_hold_none
        if expression is not None:
            self.pos = expression.pos
            self.type = getattr(expression, "type", None)
        if pos is not None:
            self.pos = pos
        if type is not None:
            self.type = type
        if is_temp:
            self.is_temp = True
        assert self.pos is not None

    def clone_node(self):
        # nothing to do here
        return self

    def type_dependencies(self, env):
        if self.expression:
            return self.expression.type_dependencies(env)
        else:
            return ()

    def update_expression(self, expression):
        self.expression = expression
        type = getattr(expression, "type", None)
        if type:
            self.type = type

    def analyse_target_declaration(self, env):
        pass  # OK - we can assign to this

    def analyse_types(self, env):
        if self.expression is not None:
            if not self.expression.type:
                self.expression = self.expression.analyse_types(env)
            self.type = self.expression.type
        return self

    def infer_type(self, env):
        if self.type is not None:
            return self.type
        if self.expression is not None:
            if self.expression.type is not None:
                return self.expression.type
            return self.expression.infer_type(env)
        assert False, "cannot infer type of ResultRefNode"

    def may_be_none(self):
        if not self.type.is_pyobject:
            return False
        return self.may_hold_none

    def _DISABLED_may_be_none(self):
        # not sure if this is safe - the expression may not be the
        # only value that gets assigned
        if self.expression is not None:
            return self.expression.may_be_none()
        if self.type is not None:
            return self.type.is_pyobject
        return True  # play it safe

    def is_simple(self):
        return True

    def result(self):
        try:
            return self.result_code
        except AttributeError:
            if self.expression is not None:
                self.result_code = self.expression.result()
        return self.result_code

    def generate_evaluation_code(self, code):
        pass

    def generate_result_code(self, code):
        pass

    def generate_disposal_code(self, code):
        pass

    def generate_assignment_code(self, rhs, code, overloaded_assignment=False):
        if self.type.is_pyobject:
            rhs.make_owned_reference(code)
            if not self.lhs_of_first_assignment:
                code.put_decref(self.result(), self.ctype())
        code.putln('%s = %s;' % (
            self.result(),
            rhs.result() if overloaded_assignment else rhs.result_as(self.ctype()),
        ))
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
        self.temp_type = self.temp_expression.type
        if self.temp_type.is_array:
            self.temp_type = c_ptr_type(self.temp_type.base_type)
        self._result_in_temp = self.temp_expression.result_in_temp()
        if self._result_in_temp:
            self.temp = self.temp_expression.result()
        else:
            if self.temp_type.is_memoryviewslice:
                self.temp_expression.make_owned_memoryviewslice(code)
            else:
                self.temp_expression.make_owned_reference(code)
            self.temp = code.funcstate.allocate_temp(
                self.temp_type, manage_ref=True)
            code.putln("%s = %s;" % (self.temp, self.temp_expression.result()))
            self.temp_expression.generate_disposal_code(code)
            self.temp_expression.free_temps(code)
        self.lazy_temp.result_code = self.temp

    def teardown_temp_expr(self, code):
        if self._result_in_temp:
            self.temp_expression.generate_disposal_code(code)
            self.temp_expression.free_temps(code)
        else:
            if self.temp_type.needs_refcounting:
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

    def may_be_none(self):
        return self.subexpression.may_be_none()

    def result(self):
        return self.subexpression.result()

    def analyse_types(self, env):
        self.temp_expression = self.temp_expression.analyse_types(env)
        self.lazy_temp.update_expression(self.temp_expression)  # overwrite in case it changed
        self.subexpression = self.subexpression.analyse_types(env)
        self.type = self.subexpression.type
        return self

    def free_subexpr_temps(self, code):
        self.subexpression.free_temps(code)

    def generate_subexpr_disposal_code(self, code):
        self.subexpression.generate_disposal_code(code)

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
    # Usually used after analysis phase, but forwards analysis methods
    # to its children

    child_attrs = ['temp_expression', 'body']

    def __init__(self, lazy_temp, body):
        self.set_temp_expr(lazy_temp)
        self.pos = body.pos
        self.body = body

    def analyse_declarations(self, env):
        self.temp_expression.analyse_declarations(env)
        self.body.analyse_declarations(env)

    def analyse_expressions(self, env):
        self.temp_expression = self.temp_expression.analyse_expressions(env)
        self.body = self.body.analyse_expressions(env)
        return self

    def generate_execution_code(self, code):
        self.setup_temp_expr(code)
        self.body.generate_execution_code(code)
        self.teardown_temp_expr(code)

    def generate_function_definitions(self, env, code):
        self.temp_expression.generate_function_definitions(env, code)
        self.body.generate_function_definitions(env, code)


class TempResultFromStatNode(ExprNodes.ExprNode):
    # An ExprNode wrapper around a StatNode that executes the StatNode
    # body.  Requires a ResultRefNode that it sets up to refer to its
    # own temp result.  The StatNode must assign a value to the result
    # node, which then becomes the result of this node.

    subexprs = []
    child_attrs = ['body']

    def __init__(self, result_ref, body):
        self.result_ref = result_ref
        self.pos = body.pos
        self.body = body
        self.type = result_ref.type
        self.is_temp = 1

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)

    def analyse_types(self, env):
        self.body = self.body.analyse_expressions(env)
        return self

    def may_be_none(self):
        return self.result_ref.may_be_none()

    def generate_result_code(self, code):
        self.result_ref.result_code = self.result()
        self.body.generate_execution_code(code)

    def generate_function_definitions(self, env, code):
        self.body.generate_function_definitions(env, code)


class HasGilNode(AtomicExprNode):
    """
    Simple node that evaluates to 0 or 1 depending on whether we're
    in a nogil context
    """
    type = c_bint_type

    def analyse_types(self, env):
        return self

    def generate_result_code(self, code):
        self.has_gil = code.funcstate.gil_owned

    def calculate_result_code(self):
        return "1" if self.has_gil else "0"
    

class StarExceptHelperNode(Nodes.StatListNode):
    """
    Like a stat list node, but also handles some of
    the temporary variables that its children will need
    """

    def __init__(self, pos, except_clauses):
        from . import Builtin, PyrexTypes

        get_exception_type = PyrexTypes.CFuncType(
            PyrexTypes.py_object_type, [])
        prep_star_type = PyrexTypes.CFuncType(
            PyrexTypes.py_object_type,
            [PyrexTypes.CFuncTypeArg("orig", PyrexTypes.py_object_type, None),
             PyrexTypes.CFuncTypeArg("excs", PyrexTypes.py_object_type, None),]
        )
        set_handled_exception_type = PyrexTypes.CFuncType(
            PyrexTypes.c_void_type,
            [PyrexTypes.CFuncTypeArg("exc", PyrexTypes.py_object_type, None)]
        )

        super(StarExceptHelperNode, self).__init__(pos, stats=[])

        self.in_progress_exception_group = ExprNodes.PyTempNode(self.pos, None)
        self.original_exception_group = ExprNodes.PyTempNode(self.pos, None)
        self.matched_exception_group = ExprNodes.PyTempNode(self.pos, None)
        self.exception_list = ExprNodes.TempNode(self.pos, Builtin.list_type)
        self.exception_list.may_be_none = lambda: False

        #get_exception_as_exception_group_call = ExprNodes.PythonCapiCallNode(
        #    self.pos, function_name="__Pyx_GetExceptionAsExceptionGroup",
        #    func_type=get_exception_type,
        #    args=[]
        #)
        #self.stats.append(Nodes.SingleAssignmentNode(
        #    self.pos,
        #    lhs=self.in_progress_exception_group,
        #    rhs=get_exception_as_exception_group_call
        #))

        for clause in except_clauses:
            append_to_list = Nodes.ExprStatNode(
                clause.pos,
                expr=ExprNodes.SimpleCallNode(
                    clause.pos,
                    function=ExprNodes.AttributeNode(
                        clause.pos, obj=self.exception_list, attribute="append"
                    ),
                    args=[
                        # Py3.11 only C API (but that's OK - nothing else works on earlier versions)
                        ExprNodes.PythonCapiCallNode(
                            clause.pos, function_name="PyErr_GetHandledException",
                            func_type=get_exception_type,
                            args=[]
                        )
                    ]
                )
            )
            on_exception_raised_in_body = Nodes.ExceptClauseNode(
                clause.pos, pattern=[], body=append_to_list, target=None
            )

            star_except_test_setup = StarExceptTestSetupNode(
                clause.pos,
                pattern=clause.pattern,
                in_progress_exception_group=self.in_progress_exception_group,
                matched_exception_group=self.matched_exception_group,
            )

            this_clause_stats = [
                star_except_test_setup
            ]

            if_clause = Nodes.IfClauseNode(
                clause.pos,
                condition = ExprNodes.PrimaryCmpNode(
                    clause.pos,
                    operator='is_not',
                    operand1=ExprNodes.CloneNode(self.matched_exception_group),
                    operand2=ExprNodes.NoneNode(clause.pos)
                ),
                body=Nodes.StatListNode(
                    clause.pos, stats=[
                        # Set the wrapped exception group to be the "handled exception"
                        Nodes.ExprStatNode(
                            clause.pos,
                            expr=ExprNodes.PythonCapiCallNode(
                                clause.pos, function_name="PyErr_SetHandledException",
                                func_type=set_handled_exception_type,
                                args=[ExprNodes.CloneNode(self.matched_exception_group)]
                            )
                        )
                    ]
                )  # fill in stats fully later
            )
            if_statement = Nodes.IfStatNode(
                clause.pos,
                if_clauses=[if_clause],
                else_clause=None
            )

            this_clause_stats.append(if_statement)

            if clause.target:
                assert clause.is_except_as
                if_clause.body.stats.append(
                    # Not using a Clone node here skips a bit of reference counting
                    # so is actually desirable
                    Nodes.SingleAssignmentNode(
                        clause.pos, lhs=clause.target, rhs=self.matched_exception_group
                    )
                )

                # make sure we clean up the target
                if_clause.body.stats.append(Nodes.TryFinallyStatNode(
                    clause.pos,
                    body=clause.body,
                    finally_clause=Nodes.StatListNode(
                        clause.pos,
                        stats=[
                            Nodes.DelStatNode(
                                clause.pos,
                                args=[ExprNodes.NameNode(
                                    clause.target.pos, name=clause.target.name)],
                                    ignore_nonexisting=True)
                        ]
                    )
                ))
            else:
                if_clause.body.append(clause.body)

            try_except = Nodes.TryExceptStatNode(
                clause.pos,
                body=Nodes.StatListNode(clause.pos, stats=this_clause_stats),
                except_clauses=[on_exception_raised_in_body],
                else_clause=None,
            )

            self.stats.append(try_except)
        
        #self.stats.append(
        #    StarExceptHelperTempCleanupNode(self.pos)
        #)

        # unfortunately it doesn't seem possible to do this without
        # using this internal API (or reimplementing a lot)
        wrapped_exception = ExprNodes.PythonCapiCallNode(
            self.pos, function_name="_PyExc_PrepReraiseStar",
            func_type=prep_star_type,
            args=[ExprNodes.CloneNode(self.original_exception_group), ExprNodes.CloneNode(self.exception_list)]
        )
        

        self.stats.append(
            Nodes.IfStatNode(
                self.pos,
                if_clauses = [Nodes.IfClauseNode(
                    self.pos,
                    condition=ExprNodes.CloneNode(self.exception_list),
                    body=Nodes.StatListNode(
                        self.pos,
                        stats=[
                            Nodes.RaiseStatNode(
                                self.pos,
                                exc_type=wrapped_exception,
                                exc_value=None,
                                exc_tb=None,
                                cause=None
                            )
                        ]
                    )
                )],
                else_clause=None
            )
        )

    def generate_execution_code(self, code):
        temps = [self.in_progress_exception_group, self.original_exception_group, self.matched_exception_group, self.exception_list]
        for t in temps:
            t.allocate(code)
        code.putln("#if PY_VERSION_HEX < 0x030B0000")
        code.putln('#error "Starred exceptions require runtime support so only work on Python 3.11 or later"')
        code.putln("#endif")
        code.put_error_if_neg(self.pos, "(%s = PyList_New(0))" % self.exception_list.result())
        code.putln("%s = %s = PyErr_GetHandledException();" % (
            self.original_exception_group.result(),
            self.in_progress_exception_group.result()
        ))
        code.putln("%s = NULL;" % self.matched_exception_group.result())
        super(StarExceptHelperNode, self).generate_execution_code(code)
        for t in temps:
            if t is self.matched_exception_group:
                code.put_xdecref_clear(t.result(), t.type)
            else:
                code.put_decref_clear(t.result(), t.type)
            t.release(code)


class StarExceptHelperTempCleanupNode(Nodes.StatNode):
    pass


class StarExceptTestSetupNode(Nodes.StatNode):
    child_attrs = ["pattern"]

    def analyse_declarations(self, env):
        for p in self.pattern:
            p.analyse_declarations(env)

    def analyse_expressions(self, env):
        self.pattern = [ p.analyse_expressions(env) for p in self.pattern ]
        return self
    
    def generate_execution_code(self, code):
        from . import Code
        code.globalstate.use_utility_code(
            Code.UtilityCode.load_cached("ExceptStar", "Exceptions.c")
        )

        for p in self.pattern:
            code.putln(code.error_goto_if("__Pyx_ValidateStarCatchPattern(%s)" % p.result(), self.pos))
        match_result_found_label = code.new_label()

        # if the in progress exception is None (i.e. it's already been handled, completely),
        # then it definitely won't match any of the patterns, so skip
        code.putln("if (%s == Py_None) {" % self.in_progress_exception_group.result())
        code.put_goto(match_result_found_label)
        code.putln("}")
        for p in self.pattern:
            code.putln(code.error_goto_if("__Pyx_ExceptionGroupMatch(%s, &%s, &%s)" % (
                p.result(),
                self.in_progress_exception_group.result(),
                self.matched_exception_group.result()), self.pos))
            code.put("if (%s != Py_None)" % self.matched_exception_group.result())
            code.put_goto(match_result_found_label)
        code.put_label(match_result_found_label)

def make_except_star_handler_body(pos, except_clauses):
    # The except* behaviour is fairly complicated, and best encapsulated by
    # generated nodes rather than having a dedicated node of its own.
    # The advantage of this is that it can be handled by the existing
    # flow control structures

    return StarExceptHelperNode(pos, except_clauses=except_clauses)