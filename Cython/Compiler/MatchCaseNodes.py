# Nodes for structural pattern matching.
#
# In a separate file because they're unlikely to be useful for much else.

import enum

from .Nodes import Node, StatNode, ErrorNode
from .Errors import error, local_errors, report_error
from . import Nodes, ExprNodes, PyrexTypes, Builtin
from .Code import UtilityCode, TempitaUtilityCode
from .Options import copy_inherited_directives


class MatchNode(StatNode):
    """
    subject  ExprNode    The expression to be matched
    cases    [MatchCaseBaseNode]  list of cases

    sequence_mapping_temp  None or AssignableTempNode  an int temp to store result of sequence/mapping tests
            sequence_mapping_temp is an optimization because determining whether something is a sequence or mapping
            is slow on Python <3.10, the Limited API (in principle, although in practice we're able to retrieve
            the flags at runtime), and PyPy. It should be deleted once no longer required.
    """

    child_attrs = ["subject", "cases"]

    sequence_mapping_temp = None

    def validate_irrefutable(self):
        found_irrefutable_case = None
        for case in self.cases:
            if isinstance(case, ErrorNode):
                # This validation happens before error nodes have been
                # transformed into actual errors, so we need to ignore them
                continue
            if found_irrefutable_case:
                error(
                    found_irrefutable_case.pos,
                    f"{found_irrefutable_case.pattern.irrefutable_message()} makes remaining patterns unreachable"
                )
                break
            if case.is_irrefutable():
                found_irrefutable_case = case
            case.validate_irrefutable()

    def refactor_cases(self):
        # An early transform - changes cases that can be represented as
        # a simple if/else statement into them (giving them maximum chance
        # to be optimized by the existing mechanisms). Leaves other cases
        # unchanged
        from .ExprNodes import CloneNode, ProxyNode, NameNode

        self.subject = ProxyNode(self.subject)
        subject = self.subject_clonenode = CloneNode(self.subject)
        current_if_statement = None
        new_cases = []
        for c in self.cases:
            if c is not None and c.is_simple_value_comparison():
                body = SubstitutedIfStatListNode(
                    c.body.pos,
                    stats=c.body.stats,
                    match_node=self
                )
                if_clause = Nodes.IfClauseNode(
                    c.pos,
                    condition=c.pattern.get_simple_comparison_node(subject),
                    body=body,
                )
                # Passing None for env is safe only because we know it's a simple value comparison.
                assignments = c.pattern.create_target_assignments(subject, env=None)
                if assignments:
                    if_clause.body.stats.insert(0, assignments)
                if current_if_statement is None:
                    current_if_statement = Nodes.IfStatNode(
                        c.pos, if_clauses=[], else_clause=None
                    )
                current_if_statement.if_clauses.append(if_clause)
            else:
                if current_if_statement:
                    # this cannot be simplified, but previous case(s) were
                    new_cases.append(SubstitutedMatchCaseNode(
                        current_if_statement.pos, body=current_if_statement
                    ))
                    current_if_statement = None
                if c is not None:
                    new_cases.append(c)
        if current_if_statement:
            # this cannot be simplified, but previous case(s) were
            new_cases.append(SubstitutedMatchCaseNode(
                current_if_statement.pos, body=current_if_statement
            ))
        self.cases = new_cases

    def analyse_declarations(self, env):
        self.subject.analyse_declarations(env)
        for c in self.cases:
            c.analyse_case_declarations(self.subject_clonenode, env)

    def analyse_expressions(self, env):
        sequence_mapping_count = 0
        for c in self.cases:
            if c.is_sequence_or_mapping():
                sequence_mapping_count += 1
        if sequence_mapping_count >= 2:
            self.sequence_mapping_temp = AssignableTempNode(
                self.pos, PyrexTypes.c_uint_type,
                is_addressable=True
            )

        self.subject = self.subject.analyse_expressions(env)
        assert isinstance(self.subject, ExprNodes.ProxyNode)
        if not self.subject.arg.is_literal:
            self.subject.arg = self.subject.arg.coerce_to_temp(env)
        subject = self.subject_clonenode.analyse_expressions(env)
        analysed_cases = []
        for c in self.cases:
            c = c.analyse_case_expressions(subject, env, self.sequence_mapping_temp)
            if c is not None:
                analysed_cases.append(c)
        self.cases = analysed_cases
        return self

    def generate_execution_code(self, code):
        if self.sequence_mapping_temp:
            self.sequence_mapping_temp.allocate(code)
            code.putln(f"{self.sequence_mapping_temp.result()} = 0; /* sequence/mapping test temp */")
            # For things that are a sequence at compile-time it's difficult
            # to avoid generating the sequence mapping temp. Therefore, silence
            # an "unused error".
            code.putln(f"(void){self.sequence_mapping_temp.result()};")
        end_label = self.end_label = code.new_label()
        self.subject.generate_evaluation_code(code)
        for c in self.cases:
            c.generate_execution_code(code, end_label)
        if self.sequence_mapping_temp:
            self.sequence_mapping_temp.release(code)
        if code.label_used(end_label):
            code.put_label(end_label)
        self.subject.generate_disposal_code(code)
        self.subject.free_temps(code)


class MatchCaseBaseNode(Node):
    """
    Common base for a MatchCaseNode and a
    substituted node
    """

    pass


class MatchCaseNode(Node):
    """
    pattern    PatternNode
    body       StatListNode
    guard      ExprNode or None

    generated:
    target_assignments  [ SingleAssignmentNodes ]
    comp_node  ExprNode that evaluates to bool
    """

    target_assignments = None
    comp_node = None
    child_attrs = ["pattern", "target_assignments", "comp_node", "guard", "body"]

    def is_irrefutable(self):
        if isinstance(self.pattern, ErrorNode):
            return True  # value doesn't really matter
        return self.pattern.is_irrefutable() and not self.guard

    def is_simple_value_comparison(self):
        if self.guard:
            return False
        return self.pattern.is_simple_value_comparison()

    def validate_targets(self):
        if isinstance(self.pattern, ErrorNode):
            return
        self.pattern.get_targets()

    def validate_irrefutable(self):
        if isinstance(self.pattern, ErrorNode):
            return
        self.pattern.validate_irrefutable()

    def is_sequence_or_mapping(self):
        return self.pattern.is_sequence_or_mapping()

    def analyse_case_declarations(self, subject_node, env):
        self.pattern.analyse_declarations(env)
        self.target_assignments = self.pattern.create_target_assignments(subject_node, env)
        if self.target_assignments:
            self.target_assignments.analyse_declarations(env)
        if self.guard:
            self.guard.analyse_declarations(env)
        self.body.analyse_declarations(env)

    def analyse_case_expressions(self, subject_node, env, sequence_mapping_temp):
        with local_errors(True) as errors:
            self.pattern = self.pattern.analyse_pattern_expressions(env, sequence_mapping_temp)
            self.comp_node = self.pattern.get_comparison_node(subject_node, sequence_mapping_temp)
            self.comp_node = self.comp_node.analyse_types(env)

        if self.comp_node and isinstance(self.comp_node, ExprNodes.BoolNode):
            if not self.comp_node.value:
                # We know this pattern can't succeed. Ignore any errors and return None.
                return None
        for error in errors:
            report_error(error)

        # coerce_to_boolean.coerce_to_simple is taken from analyse_temp_boolean_expression
        # and ensures that self.comp_node.generate_disposal_code is trivial and so
        # it doesn't matter if it's skipped in one branch. IfClauseNode relies on the same mechanism.
        self.comp_node = self.comp_node.coerce_to_boolean(env).coerce_to_simple(env)

        if self.target_assignments:
            self.target_assignments = self.target_assignments.analyse_expressions(env)
        if self.guard:
            # analyse_temp_boolean_expression ensures that self.guard.generate_disposal_code is trivial
            # and so it doesn't matter if it's skipped in one branch.
            self.guard = self.guard.analyse_temp_boolean_expression(env)
        self.body = self.body.analyse_expressions(env)
        return self

    def generate_execution_code(self, code, end_label):
        self.pattern.allocate_subject_temps(code)
        self.comp_node.generate_evaluation_code(code)

        end_of_case_label = code.new_label()

        code.putln(f"if (!{self.comp_node.result()}) ""{ /* !pattern */")
        self.pattern.dispose_of_subject_temps(code)  # failed, don't need the subjects
        code.put_goto(end_of_case_label)

        code.putln("} else { /* pattern */")
        self.comp_node.generate_disposal_code(code)
        self.comp_node.free_temps(code)
        if self.target_assignments:
            self.target_assignments.generate_execution_code(code)
        self.pattern.dispose_of_subject_temps(code)
        self.pattern.release_subject_temps(code)  # we're done with the subjects here
        if self.guard:
            self.guard.generate_evaluation_code(code)
            code.putln("if (%s) { /* guard */" % self.guard.result())
            self.guard.generate_disposal_code(code)
            self.guard.free_temps(code)
        self.body.generate_execution_code(code)
        if not self.body.is_terminator:
            code.put_goto(end_label)
        if self.guard:
            code.putln("} /* guard */")
        code.putln("} /* pattern */")
        code.put_label(end_of_case_label)


class SubstitutedMatchCaseNode(MatchCaseBaseNode):
    # body  - Node -  The (probably) if statement that it's replaced with
    child_attrs = ["body"]

    def is_sequence_or_mapping(self):
        return False

    def analyse_case_declarations(self, subject_node, env):
        self.analyse_declarations(env)

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)

    def analyse_case_expressions(self, subject_node, env, sequence_mapping_temp):
        self.body = self.body.analyse_expressions(env)
        return self

    def generate_execution_code(self, code, end_label):
        self.body.generate_execution_code(code)


class PatternNode(Node):
    """
    PatternNode is not an expression because
    it does several things (evaluating a boolean expression,
    assignment of targets), and they need to be done at different
    times.

    as_targets   [NameNode]    any target assign by "as"

    Generated in analysis:
    comp_node   ExprNode     node to evaluate for the pattern

    ----------------------------------------
    How these nodes are processed:
    1. During "analyse_declarations", "PatternNode.create_target_assignments()"
       is called on the main "PatternNode" of the case. This calls its
       sub-patterns ".create_target_assignments()" recursively.
       This creates a "StatListNode" that is held by the "MatchCaseNode".
    2. In the "analyse_expressions" phases, the "MatchCaseNode" calls
       "PatternNode.analyse_pattern_expressions", which calls its sub-pattern recursively.
    3. At the end of the "analyse_expressions" stage, the "MatchCaseNode"
       class "PatternNode.get_comparison_node()" (which calls
       "PatternNode.get_comparison_node()" for its sub-patterns).
       This returns an ExprNode which can be evaluated to determine if the
       pattern has matched.
       While generating the comparison we try quite hard not to
       analyse it until right at the end, because otherwise it'll lead
       to a lot of repeated work for deeply nested patterns.
    4. In the code generation stage, "PatternNodes" hardly generate any
       code themselves. However, they do set up whatever temps they need
       (mainly for sub-pattern subjects), with "allocate_subject_temps",
       "release_subject_temps", and "dispose_of_subject_temps" (which
       they also call recursively on their sub-patterns).
    """

    # useful for type tests
    is_match_value_pattern = False
    is_match_and_assign_pattern = False

    child_attrs = ["as_targets"]

    def __init__(self, pos, **kwds):
        if "as_targets" not in kwds:
            kwds["as_targets"] = []
        super(PatternNode, self).__init__(pos, **kwds)

    def is_irrefutable(self):
        return False

    def is_sequence_or_mapping(self):
        """
        Used for determining whether to allocate a sequence_mapping_temp.

        An OrPattern containing at least one also returns True
        """
        return False

    def get_targets(self):
        targets = self.get_main_pattern_targets()
        for target in self.as_targets:
            self.add_target_to_targets(targets, target.name)
        return targets

    def update_targets_with_targets(self, targets, other_targets):
        for name in targets.intersection(other_targets):
            error(self.pos, f"multiple assignments to name '{name}' in pattern")
        targets.update(other_targets)

    def add_target_to_targets(self, targets, target):
        if target in targets:
            error(self.pos, f"multiple assignments to name '{target}' in pattern")
        targets.add(target)

    def get_main_pattern_targets(self):
        # exclude "as" target
        raise NotImplementedError

    def is_simple_value_comparison(self):
        # Can this be converted to an "if ... elif: ..." statement?
        # Only worth doing to take advantage of things like SwitchTransform
        # so there's little benefit on doing it too widely
        return False

    def get_simple_comparison_node(self):
        """
        Returns an ExprNode that can be used as the case in an if-statement

        Should only be called if is_simple_value_comparison() is True
        """
        raise NotImplementedError

    def get_comparison_node(self, subject_node, sequence_mapping_temp=None):
        error(self.pos, f"This type of pattern is not currently supported: {self}")
        raise NotImplementedError

    def validate_irrefutable(self):
        for attr in self.child_attrs:
            child = getattr(self, attr)
            if child is not None and isinstance(child, PatternNode):
                child.validate_irrefutable()

    def analyse_pattern_expressions(self, env, sequence_mapping_temp):
        error(self.pos, f"This type of pattern is not currently supported {self}")
        raise NotImplementedError

    def generate_result_code(self, code):
        pass

    def create_target_assignments(self, subject_node, env):
        # Generates the assignment code needed to initialize all the targets.
        # Returns either a StatListNode or None.
        #
        # env may be None only if self.is_simple_value_comparison().
        # In which case there is no main_pattern_assignment_list.
        assignments = []
        for target in self.as_targets:
            if (
                self.is_match_value_pattern and
                self.value and
                self.value.is_simple()
            ):
                # in this case we can optimize slightly and just take the value
                subject_node = self.value.clone_node()
            assignments.append(
                Nodes.SingleAssignmentNode(
                    target.pos, lhs=target.clone_node(), rhs=subject_node
                )
            )
        assert env or self.is_simple_value_comparison()
        assignments.extend(self.create_main_pattern_assignment_list(subject_node, env))
        if assignments:
            return Nodes.StatListNode(self.pos, stats=assignments)
        else:
            return None

    def create_main_pattern_assignment_list(self, subject_node, env):
        # Generates assignments for everything except the "as_targets".
        # Override in subclasses.
        # Returns a list of Nodes.
        return []

    def allocate_subject_temps(self, code):
        pass  # Implement in nodes that need it

    def release_subject_temps(self, code):
        pass  # Implement in nodes that need it

    def dispose_of_subject_temps(self, code):
        pass  # Implement in nodes that need it


class MatchValuePatternNode(PatternNode):
    """
    value   ExprNode
    is_is_check   bool     Picks "is" or equality check
    """

    is_match_value_pattern = True

    child_attrs = PatternNode.child_attrs + ["value"]

    is_is_check = False

    def get_main_pattern_targets(self):
        return set()

    def is_simple_value_comparison(self):
        return True

    def get_comparison_node(self, subject_node, sequence_mapping_temp=None):
        # for this node the comparison and "simple" comparison are the same
        return LazyCoerceToBool(self.pos,
            arg=self.get_simple_comparison_node(subject_node)
        )

    def get_simple_comparison_node(self, subject_node):
        op = "is" if self.is_is_check else "=="
        return MatchValuePrimaryCmpNode(
            self.pos, operator=op, operand1=subject_node, operand2=self.value
        )

    def analyse_declarations(self, env):
        super(MatchValuePatternNode, self).analyse_declarations(env)
        if self.value:
            self.value.analyse_declarations(env)

    def analyse_pattern_expressions(self, env, sequence_mapping_temp):
        if self.value:
            self.value = self.value.analyse_expressions(env)
        return self


class MatchAndAssignPatternNode(PatternNode):
    """
    target   NameNode or None  the target to assign to (None = wildcard)
    is_star  bool
    """

    target = None
    is_star = False
    is_match_and_assign_pattern = True

    child_attrs = PatternNode.child_attrs + ["target"]

    def is_irrefutable(self):
        return True

    def irrefutable_message(self):
        if self.target:
            return f"name capture '{self.target.name}'"
        else:
            return "wildcard"

    def get_main_pattern_targets(self):
        if self.target:
            return {self.target.name}
        else:
            return set()

    def is_simple_value_comparison(self):
        return self.is_irrefutable()  # the comparison is to "True"

    def get_simple_comparison_node(self, subject_node):
        assert self.is_simple_value_comparison()
        return self.get_comparison_node(subject_node)

    def get_comparison_node(self, subject_node, sequence_mapping_temp=None):
        return ExprNodes.BoolNode(self.pos, value=True)

    def create_main_pattern_assignment_list(self, subject_node, env):
        if not self.target:
            return []
        return [Nodes.SingleAssignmentNode(self.pos, lhs=self.target.clone_node(), rhs=subject_node)]

    def analyse_pattern_expressions(self, env, sequence_mapping_temp):
        return self  # nothing to analyse


class OrPatternNode(PatternNode):
    """
    alternatives   list of PatternNodes

    generated:
    which_alternative_temp  - an integer temp node. 0 for failed; 1, 2... 
                              identify the alternative that succeeded
    """
    which_alternative_temp = None
    sequence_mapping_temp = None  # used in a similar way to MatchCaseNode,
                # to avoid recalcutating if we're a sequence or mapping

    child_attrs = PatternNode.child_attrs + ["alternatives"]

    def get_first_irrefutable(self):
        for alternative in self.alternatives:
            if alternative.is_irrefutable():
                return alternative
        return None

    def is_irrefutable(self):
        return self.get_first_irrefutable() is not None

    def irrefutable_message(self):
        return self.get_first_irrefutable().irrefutable_message()

    def is_sequence_or_mapping(self):
        # this affects if the caller generates a temp for it. If so the
        # this node can forward the temp to the relevant alternative
        for a in self.alternatives:
            if a.is_sequence_or_mapping():
                return True
        return False

    def get_main_pattern_targets(self):
        child_targets = None
        for alternative in self.alternatives:
            alternative_targets = alternative.get_targets()
            if child_targets is not None and child_targets != alternative_targets:
                error(self.pos, "alternative patterns bind different names")
            child_targets = alternative_targets
        return child_targets

    def validate_irrefutable(self):
        super(OrPatternNode, self).validate_irrefutable()
        found_irrefutable_case = None
        for alternative in self.alternatives:
            if found_irrefutable_case:
                error(
                    found_irrefutable_case.pos,
                    f"{found_irrefutable_case.irrefutable_message()} makes remaining patterns unreachable"
                )
                break
            if alternative.is_irrefutable():
                found_irrefutable_case = alternative
            alternative.validate_irrefutable()

    def is_simple_value_comparison(self):
        return all(
            # it turns out to be hard to generate correct assignment code
            # for or patterns with targets
            a.is_simple_value_comparison() and not a.get_targets()
            for a in self.alternatives
        )

    def is_really_simple_value_comparison(self):
        # like is_simple_value_comparison but also doesn't have any targets
        return (self.is_simple_value_comparison() and
                all(not a.get_targets() for a in self.alternatives))

    def get_simple_comparison_node(self, subject_node):
        assert self.is_simple_value_comparison()
        assert len(self.alternatives) >= 2, self.alternatives
        checks = []
        for a in self.alternatives:
            checks.append(a.get_simple_comparison_node(subject_node))
        if any(isinstance(ch, ExprNodes.BoolNode) and ch.value for ch in checks):
            # handle the obvious very simple case
            return ExprNodes.BoolNode(self.pos, value=True)
        return generate_binop_tree_from_list(self.pos, "or", checks)

    def get_comparison_node(self, subject_node, sequence_mapping_temp=None):
        if self.is_really_simple_value_comparison():
            return self.get_simple_comparison_node(subject_node)

        cond_exprs = []
        for n, a in enumerate(self.alternatives, start=1):
            a_test = a.get_comparison_node(subject_node, sequence_mapping_temp)
            a_value = ExprNodes.IntNode(a.pos, value=str(n))
            if isinstance(a_test, ExprNodes.BoolNode) and a_test.value:
                cond_exprs.append(a_value)
                break  # no point in going further
            else:
                cond_exprs.append(
                    ExprNodes.CondExprNode(
                        self.pos,
                        test = a_test,
                        true_val = a_value,
                        false_val = ExprNodes.IntNode(self.pos, value="0")
                    )
                )
        
        expr = generate_binop_tree_from_list(self.pos, "or", cond_exprs)

        if self.which_alternative_temp:
            expr = ExprNodes.AssignmentExpressionNode(
                self.pos,
                lhs = self.which_alternative_temp,
                rhs = expr
            )
        return LazyCoerceToBool(expr.pos, arg=expr)

    def analyse_declarations(self, env):
        super(OrPatternNode, self).analyse_declarations(env)
        for a in self.alternatives:
            a.analyse_declarations(env)

    def analyse_pattern_expressions(self, env, sequence_mapping_temp):
        self.alternatives = [
            a.analyse_pattern_expressions(env, sequence_mapping_temp)
            for a in self.alternatives
        ]
        if not sequence_mapping_temp:
            sequence_mapping_count = 0
            for a in self.alternatives:
                if a.is_sequence_or_mapping():
                    sequence_mapping_count += 1
            if sequence_mapping_count >= 2:
                self.sequence_mapping_temp = AssignableTempNode(
                    self.pos, PyrexTypes.c_uint_type,
                    is_addressable=True
                )
                sequence_mapping_temp = self.sequence_mapping_temp
        return self

    def create_main_pattern_assignment_list(self, subject_node, env):
        ifclauses = []
        for n, a in enumerate(self.alternatives, start=1):
            a_assignment = a.create_target_assignments(subject_node, env)
            if a_assignment:
                if not self.which_alternative_temp:
                    self.which_alternative_temp = AssignableTempNode(self.pos, PyrexTypes.c_int_type)
                # Switch code paths depending on which node gets assigned
                ifclause = Nodes.IfClauseNode(
                    a.pos,
                    condition=ExprNodes.PrimaryCmpNode(
                        a.pos,
                        operator="==",
                        operand1=self.which_alternative_temp,
                        operand2=ExprNodes.IntNode(a.pos, value=str(n))
                    ),
                    body = a_assignment
                )
                ifclauses.append(ifclause)
        if ifclauses:
            return [
                Nodes.IfStatNode(
                    self.pos,
                    if_clauses=ifclauses,
                    else_clause=None
                )
            ]
        return []

    def allocate_subject_temps(self, code):
        if self.sequence_mapping_temp:
            self.sequence_mapping_temp.allocate(code)
            code.putln(
                "%s = 0; /* sequence/mapping test temp */"
                % self.sequence_mapping_temp.result()
            )
            # For things that are a sequence at compile-time it's difficult
            # to avoid generating the sequence mapping temp. Therefore, silence
            # an "unused error"
            code.putln("(void)%s;" % self.sequence_mapping_temp.result())
        if self.which_alternative_temp:
            self.which_alternative_temp.allocate(code)
        for a in self.alternatives:
            a.allocate_subject_temps(code)

    def release_subject_temps(self, code):
        if self.sequence_mapping_temp:
            self.sequence_mapping_temp.release(code)
        if self.which_alternative_temp:
            self.which_alternative_temp.release(code)
        for a in self.alternatives:
            a.release_subject_temps(code)

    def dispose_of_subject_temps(self, code):
        if self.which_alternative_temp:
            self.which_alternative_temp.generate_disposal_code(code)
        if self.sequence_mapping_temp:
            self.sequence_mapping_temp.generate_disposal_code(code)
        for a in self.alternatives:
            a.dispose_of_subject_temps(code)


class MatchSequencePatternNode(PatternNode):
    """
    patterns   list of PatternNodes

    generated:
    subjects    [TrackTypeTempNode]  individual subsubjects can be assigned to these
    """

    subjects = None
    needs_length_temp = False

    child_attrs = PatternNode.child_attrs + ["patterns"]

    Pyx_sequence_check_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type,
        [
            PyrexTypes.CFuncTypeArg("o", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg(
                "sequence_mapping_temp",
                PyrexTypes.c_ptr_type(PyrexTypes.c_uint_type),
                None,
            ),
        ],
        exception_value="-1",
    )

    def is_sequence_or_mapping(self):
        return True

    def __init__(self, pos, **kwds):
        super(MatchSequencePatternNode, self).__init__(pos, **kwds)
        self.length_temp = AssignableTempNode(self.pos, PyrexTypes.c_py_ssize_t_type)

    def get_main_pattern_targets(self):
        targets = set()
        star_count = 0
        for pattern in self.patterns:
            if pattern.is_match_and_assign_pattern and pattern.is_star:
                star_count += 1
            self.update_targets_with_targets(targets, pattern.get_targets())
        if star_count > 1:
            error(self.pos, "multiple starred names in sequence pattern")
        return targets

    def get_comparison_node(self, subject_node, sequence_mapping_temp=None):
        from .UtilNodes import TempResultFromStatNode, ResultRefNode

        test = None
        assert getattr(self, "subject_temps", None) is not None

        seq_test = self.make_sequence_check(subject_node, sequence_mapping_temp)
        if isinstance(seq_test, ExprNodes.BoolNode) and not seq_test.value:
            return seq_test  # no point in proceeding further!

        has_star = False
        all_tests = [seq_test]
        pattern_tests = []
        for n, pattern in enumerate(self.patterns):
            if isinstance(pattern, MatchAndAssignPatternNode) and pattern.is_star:
                has_star = True
                self.needs_length_temp = True

            if self.subject_temps[n] is None:
                # The subject has been identified as unneeded, so don't evaluate it
                continue
            p_test = pattern.get_comparison_node(self.subject_temps[n])

            result_ref = ResultRefNode(pos=self.pos, type=PyrexTypes.c_bint_type)
            subject_assignment = Nodes.SingleAssignmentNode(
                self.pos,
                lhs=self.subject_temps[n],  # the temp node
                rhs=self.subjects[n],  # the regular node
            )
            test_assignment = Nodes.SingleAssignmentNode(
                self.pos, lhs=result_ref, rhs=p_test
            )
            stats = Nodes.StatListNode(
                self.pos, stats=[subject_assignment, test_assignment]
            )
            pattern_tests.append(TempResultFromStatNode(result_ref, stats))

        min_length = len(self.patterns)
        if has_star:
            min_length -= 1
        # check whether we need a length call...
        if not (self.patterns and len(self.patterns) == 1 and has_star):
            length_call = self.make_length_call_node(subject_node)

            if length_call.is_literal and (
                (has_star and min_length < length_call.constant_result)
                or (not has_star and min_length != length_call.constant_result)
            ):
                # definitely failed!
                return ExprNodes.BoolNode(self.pos, value=False)
            seq_len_test = ExprNodes.PrimaryCmpNode(
                self.pos,
                operator=">=" if has_star else "==",
                operand1=length_call,
                operand2=ExprNodes.IntNode.for_size(self.pos, min_length),
            )
            all_tests.append(seq_len_test)
        else:
            self.needs_length_temp = False
        all_tests.extend(pattern_tests)
        test = generate_binop_tree_from_list(self.pos, "and", all_tests)
        return LazyCoerceToBool(test.pos, arg=test)

    def generate_subjects(self, subject_node, env):
        assert self.subjects is None  # not called twice

        star_idx = None
        for n, pattern in enumerate(self.patterns):
            if pattern.is_match_and_assign_pattern and pattern.is_star:
                star_idx = n
        if star_idx is None:
            idxs = list(range(len(self.patterns)))
        else:
            fwd_idxs = list(range(star_idx))
            backward_idxs = list(range(star_idx - len(self.patterns) + 1, 0))
            star_idx = (
                fwd_idxs[-1] + 1 if fwd_idxs else None,
                backward_idxs[0] if backward_idxs else None,
            )
            idxs = fwd_idxs + [star_idx] + backward_idxs

        subjects = []
        for pattern, idx in zip(self.patterns, idxs):
            indexer = self.make_indexing_node(pattern, subject_node, idx, env)
            subjects.append(ExprNodes.ProxyNode(indexer) if indexer else None)
        self.subjects = subjects
        self.subject_temps = [
            None if p.is_irrefutable() else TrackTypeTempNode(self.pos, s)
            for s, p in zip(self.subjects, self.patterns)
        ]

    def create_main_pattern_assignment_list(self, subject_node, env):
        assignments = []
        self.generate_subjects(subject_node, env)
        for subject_temp, subject, pattern in zip(
            self.subject_temps, self.subjects, self.patterns
        ):
            needs_result_ref = False
            if subject_temp is not None:
                subject = subject_temp
            else:
                if subject is None:
                    assert not pattern.get_targets()
                    continue
                elif not subject.is_literal or subject.is_temp:
                    from .UtilNodes import ResultRefNode, LetNode

                    subject = ResultRefNode(subject)
                    needs_result_ref = True
            p_assignments = pattern.create_target_assignments(subject, env)
            if needs_result_ref:
                p_assignments = LetNode(subject, p_assignments)
            else:
                p_assignments = p_assignments
            if p_assignments:
                assignments.append(p_assignments)
        return assignments

    def make_sequence_check(self, subject_node, sequence_mapping_temp):
        # Note: the sequence check code is very quick on Python 3.10+
        # but potentially quite slow on lower versions (although should
        # be medium quick for common types). It'd be nice to cache the
        # results of it where it's been called on the same object
        # multiple times.
        # DW has decided that that's too complicated to implement
        # for now.
        utility_code = UtilityCode.load_cached("IsSequence", "MatchCase.c")
        if sequence_mapping_temp is not None:
            sequence_mapping_temp = ExprNodes.AmpersandNode(
                self.pos, operand=sequence_mapping_temp
            )
        else:
            sequence_mapping_temp = ExprNodes.NullNode(self.pos)
        call = ExprNodes.PythonCapiCallNode(
            self.pos,
            "__Pyx_MatchCase_IsSequence",
            self.Pyx_sequence_check_type,
            utility_code=utility_code,
            args=[subject_node, sequence_mapping_temp],
        )

        def type_check(type):
            # type-check need not be perfect, it's an optimization
            if type.is_pylist_type or type.is_pytuple_type:
                return True
            if type.is_memoryviewslice or type.is_ctuple:
                return True
            if (
                type.is_bytes_or_str_or_bytearray or
                type.is_pyanydict_type or
                type.is_pyanyset_type
            ):
                # non-exhaustive list at this stage, but returning "False" is
                # an optimization so it's allowed to be non-exchaustive
                return False
            if type.is_numeric or type.is_struct or type.is_enum:
                # again, not exhaustive
                return False
            return None

        return StaticTypeCheckNode(
            self.pos, arg=subject_node, fallback=call, check=type_check
        )

    def make_length_call_node(self, subject_node):
        len_entry = Builtin.builtin_scope.lookup("len")
        if subject_node.type.is_memoryviewslice:
            len_call = ExprNodes.IndexNode(
                self.pos,
                base=ExprNodes.AttributeNode(
                    self.pos, obj=subject_node, attribute="shape"
                ),
                index=ExprNodes.IntNode.for_size(self.pos, 0),
            )
        elif subject_node.type.is_ctuple:
            len_call = ExprNodes.IntNode.for_size(
                self.pos, len(subject_node.type.components))
        else:
            len_call = ExprNodes.SimpleCallNode(
                self.pos,
                function=ExprNodes.NameNode(self.pos, name="len", entry=len_entry),
                args=[subject_node],
            )
        if self.needs_length_temp:
            return ExprNodes.AssignmentExpressionNode(
                self.pos, lhs=self.length_temp, rhs=len_call
            )
        else:
            return len_call

    def make_indexing_node(self, pattern, subject_node, idx, env):
        if pattern.is_irrefutable() and not pattern.get_targets():
            # Nothing to do - index isn't used
            return None

        def get_index_from_int(i):
            if i is None:
                return None
            else:
                int_node = ExprNodes.IntNode.for_size(pattern.pos, i)
                if i >= 0:
                    return int_node
                else:
                    self.needs_length_temp = True
                    return ExprNodes.binop_node(
                        pattern.pos,
                        operator="+",
                        operand1=self.length_temp,
                        operand2=int_node,
                    )

        if isinstance(idx, tuple):
            start = get_index_from_int(idx[0])
            stop = get_index_from_int(idx[1])
            indexer = SliceToListNode(
                pattern.pos,
                base=subject_node,
                start=start,
                stop=stop,
                length_node=self.length_temp if self.needs_length_temp else None,
            )
        else:
            indexer = ExprNodes.CompilerDirectivesExprNode(
                arg=ExprNodes.IndexNode(
                    pattern.pos, base=subject_node, index=get_index_from_int(idx)
                ),
                directives=copy_inherited_directives(
                    env.directives, boundscheck=False, wraparound=False
                ),
            )
        return indexer

    def analyse_declarations(self, env):
        for p in self.patterns:
            p.analyse_declarations(env)
        return super(MatchSequencePatternNode, self).analyse_declarations(env)

    def analyse_pattern_expressions(self, env, sequence_mapping_temp):
        for n in range(len(self.subjects)):
            if self.subjects[n]:
                self.subjects[n] = self.subjects[n].analyse_types(env)
        for n in range(len(self.patterns)):
            self.patterns[n] = self.patterns[n].analyse_pattern_expressions(env, None)
        return self

    def allocate_subject_temps(self, code):
        if self.needs_length_temp:
            self.length_temp.allocate(code)
        for temp in self.subject_temps:
            if temp is not None:
                temp.allocate(code)
        for pattern in self.patterns:
            pattern.allocate_subject_temps(code)

    def release_subject_temps(self, code):
        if self.needs_length_temp:
            self.length_temp.release(code)
        for temp in self.subject_temps:
            if temp is not None:
                temp.release(code)
        for pattern in self.patterns:
            pattern.release_subject_temps(code)

    def dispose_of_subject_temps(self, code):
        if self.needs_length_temp:
            code.put_xdecref_clear(self.length_temp.result(), self.length_temp.type)
        for temp in self.subject_temps:
            if temp is not None:
                code.put_xdecref_clear(temp.result(), temp.type)
        for pattern in self.patterns:
            pattern.dispose_of_subject_temps(code)


class MatchMappingPatternNode(PatternNode):
    """
    keys   list of Literals or AttributeNodes
    value_patterns  list of PatternNodes of equal length to keys
    double_star_capture_target  NameNode or None

    needs_runtime_keycheck  - bool  - are there any keys which can only be resolved at runtime
    subjects    [temp nodes or None]  individual subsubjects can be assigned to these
    """

    keys = []
    value_patterns = []
    double_star_capture_target = None
    subject_temps = None
    double_star_temp = None

    needs_runtime_keycheck = False

    child_attrs = PatternNode.child_attrs + [
        "keys",
        "value_patterns",
        "double_star_capture_target",
    ]

    Pyx_mapping_check_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type,
        [
            PyrexTypes.CFuncTypeArg("o", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg(
                "sequence_mapping_temp",
                PyrexTypes.c_ptr_type(PyrexTypes.c_uint_type),
                None,
            ),
        ],
        exception_value="-1",
    )
    # lie about the types of keys for simplicity
    Pyx_mapping_check_duplicates_type = PyrexTypes.CFuncType(
        PyrexTypes.c_int_type,
        [
            PyrexTypes.CFuncTypeArg("keys", PyrexTypes.c_void_ptr_type, None),
            PyrexTypes.CFuncTypeArg("nKeys", PyrexTypes.c_py_ssize_t_type, None),
        ],
        exception_value="-1",
    )
    # lie about the types of keys and subjects for simplicity
    Pyx_mapping_extract_subjects_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type,
        [
            PyrexTypes.CFuncTypeArg("mapping", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("keys", PyrexTypes.c_void_ptr_type, None),
            PyrexTypes.CFuncTypeArg("nKeys", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("subjects", PyrexTypes.c_void_ptr_ptr_type, None),
        ],
        exception_value="-1",
    )
    Pyx_mapping_doublestar_type = PyrexTypes.CFuncType(
        Builtin.dict_type,
        [
            PyrexTypes.CFuncTypeArg("mapping", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("keys", PyrexTypes.c_void_ptr_type, None),
            PyrexTypes.CFuncTypeArg("nKeys", PyrexTypes.c_py_ssize_t_type, None),
        ],
    )

    def is_sequence_or_mapping(self):
        return True

    def get_main_pattern_targets(self):
        targets = set()
        for pattern in self.value_patterns:
            self.update_targets_with_targets(targets, pattern.get_targets())
        if self.double_star_capture_target:
            self.add_target_to_targets(targets, self.double_star_capture_target.name)
        return targets

    def validate_keys(self):
        # called after constant folding
        literal_keys = set()
        for k in self.keys:
            if k.has_constant_result():
                value = k.constant_result
                # Note that "set" equality behaviour is intentional. e.g. 0.0 and 0 are duplicates.
                if value in literal_keys:
                    error(k.pos, "mapping pattern checks duplicate key (%s)" % value)
                literal_keys.add(value)
            else:
                self.needs_runtime_keycheck = True

        if literal_keys and self.keys:
            # it's very useful to sort keys early so the literal keys
            # come first
            sorted_keys = sorted(
                zip(self.keys, self.value_patterns),
                key=lambda kvp: (not kvp[0].is_literal),
            )
            self.keys, self.value_patterns = [list(l) for l in zip(*sorted_keys)]

    def analyse_declarations(self, env):
        super(MatchMappingPatternNode, self).analyse_declarations(env)
        self.validate_keys()
        for k in self.keys:
            k.analyse_declarations(env)
        for vp in self.value_patterns:
            vp.analyse_declarations(env)
        if self.double_star_capture_target:
            self.double_star_capture_target.analyse_declarations(env)

    def generate_subjects(self, subject_node, env):
        assert self.subject_temps is None  # already calculated
        subject_temps = []
        for pattern in self.value_patterns:
            if pattern.is_match_and_assign_pattern and not pattern.target:
                subject_temps.append(None)
            else:
                subject_temps.append(
                    AssignableTempNode(pattern.pos, PyrexTypes.py_object_type)
                )
        self.subject_temps = subject_temps

    def create_main_pattern_assignment_list(self, subject_node, env):
        self.generate_subjects(subject_node, env)
        assignments = []
        for subject, pattern in zip(self.subject_temps, self.value_patterns):
            p_assignments = pattern.create_target_assignments(subject, env)
            if p_assignments:
                assignments.extend(p_assignments.stats)
        if self.double_star_capture_target:
            self.double_star_temp = AssignableTempNode(self.pos, Builtin.dict_type)
            assignments.append(
                Nodes.SingleAssignmentNode(
                    self.double_star_temp.pos,
                    lhs=self.double_star_capture_target,
                    rhs=self.double_star_temp,
                )
            )
        return assignments

    class DictCheckResult(enum.IntEnum):
        NotAMapping = enum.auto()
        NotADict = enum.auto()  # but might be another mapping
        MightBeAnAnyDict = enum.auto()
        ExactDict = enum.auto()
        ExactFrozenDict = enum.auto()

    def is_dict_type_check(self, type):
        # Returns a DictCheckResult to summarize what we know about types dictness.
        # We need to get ExactDict, ExactFrozenDict, and NotAMapping right. The other
        # two cases are optimizations so can be wrong.
        if type.is_pydict_type:
            return self.DictCheckResult.ExactDict
        if type.is_pyfrozendict_type:
            return self.DictCheckResult.ExactFrozenDict
        if type.is_builtin_type:
            # All other builtin types that Cython knows of are not mappings
            # (DictProxyType is, but Cython doesn't know about that).
            return self.DictCheckResult.NotAMapping
        if not type.is_pyobject:
            # for now any non-pyobject type isn't treated as a mapping
            return self.DictCheckResult.NotAMapping
        if type.is_extension_type:
            # An external extension type might actually be a dict, but that's fine:
            # it just ends up on a slightly slower code path.
            return self.DictCheckResult.NotADict
        return self.DictCheckResult.MightBeAnAnyDict

    def make_mapping_check(self, subject_node, sequence_mapping_temp):
        # Note: the mapping check code is very quick on Python 3.10+
        # but potentially quite slow on lower versions (although should
        # be medium quick for common types). It'd be nice to cache the
        # results of it where it's been called on the same object
        # multiple times.
        # DW has decided that that's too complicated to implement
        # for now.
        utility_code = UtilityCode.load_cached("IsMapping", "MatchCase.c")
        if sequence_mapping_temp is not None:
            sequence_mapping_temp = ExprNodes.AmpersandNode(
                self.pos, operand=sequence_mapping_temp
            )
        else:
            sequence_mapping_temp = ExprNodes.NullNode(self.pos)
        call = ExprNodes.PythonCapiCallNode(
            self.pos,
            "__Pyx_MatchCase_IsMapping",
            self.Pyx_mapping_check_type,
            utility_code=utility_code,
            args=[subject_node, sequence_mapping_temp],
        )

        def type_check(type):
            res = self.is_dict_type_check(type)
            if res is self.DictCheckResult.ExactDict or res is self.DictCheckResult.ExactFrozenDict:
                return True
            if res is self.DictCheckResult.NotAMapping:
                return False
            return None

        return StaticTypeCheckNode(
            self.pos, arg=subject_node, fallback=call, check=type_check
        )

    def make_duplicate_keys_check(self, n_fixed_keys):
        utility_code = UtilityCode.load_cached("MappingKeyCheck", "MatchCase.c")
        if n_fixed_keys == len(self.keys):
            return None  # nothing to check
        if n_fixed_keys == 0 and len(self.keys) <= 1:
            return None  # nothing to check

        return Nodes.ExprStatNode(
            self.pos,
            expr=ExprNodes.PythonCapiCallNode(
                self.pos,
                "__Pyx_MatchCase_CheckMappingDuplicateKeys",
                self.Pyx_mapping_check_duplicates_type,
                utility_code=utility_code,
                args=[
                    EvaluateWithKeysAndSubjectsArrays.make_keys_node(self.pos),
                    ExprNodes.IntNode.for_size(self.pos, n_fixed_keys),
                    ExprNodes.IntNode.for_size(self.pos, len(self.keys)),
                ],
            ),
        )

    def check_all_keys(self, subject_node):
        # It's debatable here whether to go for individual unpacking or a function.
        # Current implementation is a function that's loosely copied from CPython.
        # For small numbers of keys it might be better to generate the code instead.
        # There's three versions depending on if we know that the type is exactly
        # a dict, definitely not a dict, or unknown.
        # The advantages of generating a function are:
        # * more compact code
        # * can potentially be extracted into the shared utility module
        # * easier to check the type once then branch the implementation
        # * faster in the cases that are more likely to fail due to wrong keys being
        #    present than due to the values not matching the patterns
        if not self.keys:
            return ExprNodes.BoolNode(self.pos, value=True)

        is_dict = self.is_dict_type_check(subject_node.type)
        if is_dict is self.DictCheckResult.ExactDict or is_dict is self.DictCheckResult.ExactFrozenDict:
            util_code = UtilityCode.load_cached("ExtractExactDict", "MatchCase.c")
            func_name = "__Pyx_MatchCase_Mapping_ExtractDict"
        elif is_dict is self.DictCheckResult.MightBeAnAnyDict:
            util_code = UtilityCode.load_cached("ExtractGeneric", "MatchCase.c")
            func_name = "__Pyx_MatchCase_Mapping_Extract"
        else:
            util_code = UtilityCode.load_cached("ExtractNonDict", "MatchCase.c")
            func_name = "__Pyx_MatchCase_Mapping_ExtractNonDict"

        return ExprNodes.PythonCapiCallNode(
            self.pos,
            func_name,
            self.Pyx_mapping_extract_subjects_type,
            utility_code=util_code,
            args=[
                subject_node,
                EvaluateWithKeysAndSubjectsArrays.make_keys_node(self.pos),
                ExprNodes.IntNode.for_size(self.pos, len(self.keys)),
                EvaluateWithKeysAndSubjectsArrays.make_subjects_node(self.pos),
            ],
        )

    def make_double_star_capture(self, subject_node, test_result):
        # test_result being the variable that holds "case check passed until now"
        is_dict = self.is_dict_type_check(subject_node.type)
        if is_dict is self.DictCheckResult.ExactDict:
            tag = "ExactDict"
        elif is_dict is self.DictCheckResult.ExactFrozenDict:
            tag = "ExactFrozenDict"
        elif is_dict is self.DictCheckResult.MightBeAnAnyDict:
            tag = ""
        else:
            tag = "NotDict"
        utility_code = TempitaUtilityCode.load_cached(
            "DoubleStarCapture", "MatchCase.c", context={"tag": tag}
        )
        func = ExprNodes.PythonCapiCallNode(
            self.double_star_capture_target.pos,
            "__Pyx_MatchCase_DoubleStarCapture" + tag,
            self.Pyx_mapping_doublestar_type,
            utility_code=utility_code,
            args=[
                subject_node,
                EvaluateWithKeysAndSubjectsArrays.make_keys_node(self.pos),
                ExprNodes.IntNode.for_size(self.pos, len(self.keys)),
            ],
        )
        assignment = Nodes.SingleAssignmentNode(
            self.double_star_capture_target.pos, lhs=self.double_star_temp, rhs=func
        )
        if_clause = Nodes.IfClauseNode(
            self.double_star_capture_target.pos, condition=test_result, body=assignment
        )
        return Nodes.IfStatNode(
            self.double_star_capture_target.pos,
            if_clauses=[if_clause],
            else_clause=None,
        )

    def get_comparison_node(self, subject_node, sequence_mapping_temp=None):
        from . import UtilNodes

        var_keys = []
        n_literal_keys = 0
        for k in self.keys:
            if not k.is_literal:
                var_keys.append(k)
            else:
                n_literal_keys += 1

        all_tests = []
        all_tests.append(self.make_mapping_check(subject_node, sequence_mapping_temp))
        all_tests.append(self.check_all_keys(subject_node))

        if any(isinstance(test, ExprNodes.BoolNode) and not test.value for test in all_tests):
            # identify automatic-failure
            return ExprNodes.BoolNode(self.pos, value=False)

        for pattern, subject in zip(self.value_patterns, self.subject_temps):
            if pattern.is_irrefutable():
                continue
            assert subject
            all_tests.append(pattern.get_comparison_node(subject))

        body = all_tests_node = generate_binop_tree_from_list(self.pos, "and", all_tests)
        duplicate_check = self.make_duplicate_keys_check(n_literal_keys)

        if duplicate_check or self.double_star_capture_target:
            stats = []
            if duplicate_check:
                stats.append(duplicate_check)
            test_result = UtilNodes.ResultRefNode(pos=self.pos, type=PyrexTypes.c_bint_type)
            stats.append(
                Nodes.SingleAssignmentNode(self.pos, lhs=test_result, rhs=all_tests_node))
            if self.double_star_capture_target:
                assert self.double_star_temp
                stats.append(
                    # make_double_star_capture wraps itself in an if
                    self.make_double_star_capture(subject_node, test_result)
                )
            body = UtilNodes.TempResultFromStatNode(test_result, Nodes.StatListNode(self.pos, stats=stats))
        if self.keys or self.double_star_capture_target:
            body = EvaluateWithKeysAndSubjectsArrays(
                body.pos,
                arg=LazyCoerceToBool(body.pos, arg=body),
                keys_array=self.keys,
                subjects_array=self.subject_temps
            )
        return LazyCoerceToBool(body.pos, arg=body)

    def analyse_pattern_expressions(self, env, sequence_mapping_temp):
        def to_temp_or_literal(node):
            return node if node.is_literal else node.coerce_to_temp(env)

        self.keys = [
            to_temp_or_literal(k.analyse_expressions(env))
            for k in self.keys
        ]

        self.value_patterns = [ p.analyse_pattern_expressions(env, None) for p in self.value_patterns ]
        return self

    def allocate_subject_temps(self, code):
        for temp in self.subject_temps:
            if temp is not None:
                temp.allocate(code)
        for pattern in self.value_patterns:
            pattern.allocate_subject_temps(code)
        if self.double_star_temp:
            self.double_star_temp.allocate(code)

    def release_subject_temps(self, code):
        for temp in self.subject_temps:
            if temp is not None:
                temp.release(code)
        for pattern in self.value_patterns:
            pattern.release_subject_temps(code)
        if self.double_star_temp:
            self.double_star_temp.release(code)

    def dispose_of_subject_temps(self, code):
        for temp in self.subject_temps:
            if temp is not None:
                code.put_xdecref_clear(temp.result(), temp.type)
        for pattern in self.value_patterns:
            pattern.dispose_of_subject_temps(code)
        if self.double_star_temp:
            code.put_xdecref_clear(
                self.double_star_temp.result(), self.double_star_temp.type
            )


class ClassPatternNode(PatternNode):
    """
    class_  NameNode or AttributeNode
    positional_patterns  list of PatternNodes
    keyword_pattern_names    list of NameNodes
    keyword_pattern_patterns    list of PatternNodes
                                (same length as keyword_pattern_names)
    """

    class_ = None
    positional_patterns = []
    keyword_pattern_names = []
    keyword_pattern_patterns = []

    # as with the mapping functions, lie a little about some of the types for
    # ease of declaration
    Pyx_positional_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type,
        [
            PyrexTypes.CFuncTypeArg("subject", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("type", Builtin.type_type, None),
            PyrexTypes.CFuncTypeArg("fixed_names", PyrexTypes.c_void_ptr_type, None),
            PyrexTypes.CFuncTypeArg("n_fixed", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("match_self", PyrexTypes.c_int_type, None),
            PyrexTypes.CFuncTypeArg("subjects", PyrexTypes.c_void_ptr_ptr_type, None),
            PyrexTypes.CFuncTypeArg("n_subjects", PyrexTypes.c_int_type, None),
        ],
        exception_value="-1",
    )

    Pyx_typeguard_type = PyrexTypes.CFuncType(
        Builtin.type_type,
        [
            PyrexTypes.CFuncTypeArg("type", PyrexTypes.py_object_type, None),
        ],
    )

    child_attrs = PatternNode.child_attrs + [
        "class_",
        "positional_patterns",
        "keyword_pattern_patterns",
        # keyword_pattern_names are deliberately excluded. They're only NameNodes as a
        # convenient way of storing a name and a pos. There's nothing to be gained from
        # processing them
    ]

    def generate_subjects(self, subject_node):
        assert not hasattr(self, "keyword_subject_temps")

        if self.class_known_type:
            # maximizes type inference
            subject_node = ExprNodes.TypecastNode(
                subject_node.pos,
                operand=subject_node,
                type=self.class_known_type,
                typecheck=False,
            )

        self.keyword_subject_temps = []
        self.keyword_subject_attrs = []
        for p, p_name in zip(self.keyword_pattern_patterns, self.keyword_pattern_names):
            # The attribute lookups are calculated here to maximize chance of type interference
            attr_lookup = ExprNodes.AttributeNode(
                p_name.pos, obj=subject_node, attribute=p_name.name, mangle_private_names=False
            )
            self.keyword_subject_attrs.append(attr_lookup)
            if not p.get_targets() and p.is_irrefutable():
                self.keyword_subject_temps.append(None)
            else:
                # Hopefully the type can be assigned later
                self.keyword_subject_temps.append(TrackTypeTempNode(p.pos, attr_lookup))

        self.positional_subject_temps = []
        for p in self.positional_patterns:
            if not p.get_targets() and p.is_irrefutable():
                self.positional_subject_temps.append(None)
            else:
                self.positional_subject_temps.append(
                    AssignableTempNode(p.pos, PyrexTypes.py_object_type)
                )

    def get_main_pattern_targets(self):
        targets = set()
        for pattern in self.positional_patterns + self.keyword_pattern_patterns:
            self.update_targets_with_targets(targets, pattern.get_targets())
        return targets

    def create_main_pattern_assignment_list(self, subject_node, env):
        self.generate_subjects(subject_node)
        assignments = []
        patterns = self.keyword_pattern_patterns + self.positional_patterns
        temps = self.keyword_subject_temps + self.positional_subject_temps
        for pattern, temp in zip(patterns, temps):
            pattern_assignments = pattern.create_target_assignments(temp, env)
            if pattern_assignments:
                assignments.extend(pattern_assignments.stats)
        return assignments

    def make_typecheck_call(self, subject_node, class_node):
        if not subject_node.type.is_pyobject:
            with local_errors(True) as errors:
                # TODO - it'd be nice to be able to match up simple c types
                # e.g. "int" to "int", "double" to "double"
                # without having to go through this
                subject_node = LazyCoerceToPyObject(subject_node.pos, arg=subject_node)
            if errors:
                return ExprNodes.BoolNode(self.pos, value=False)
        if self.class_known_type:
            if not self.class_known_type.is_pyobject:
                error(self.pos, "class must be a Python object")
                return ExprNodes.BoolNode(self.pos, value=False)

            if subject_node.type.subtype_of_resolved_type(self.class_known_type):
                if subject_node.may_be_none():
                    return ExprNodes.PrimaryCmpNode(
                        self.pos,
                        operator="is_not",
                        operand1=subject_node,
                        operand2=ExprNodes.NoneNode(self.pos),
                    )
                else:
                    return ExprNodes.BoolNode(self.pos, value=True)
            # if subject_node.type is not PyrexTypes.py_object_type
            # I suspect the value is false, but possibly can't prove it

        return ExprNodes.SimpleCallNode(
            self.pos,
            function=ExprNodes.NameNode(
                self.pos,
                name="isinstance",
                entry=Builtin.builtin_scope.lookup("isinstance"),
            ),
            args=[subject_node, class_node],
        )

    def make_keyword_pattern_lookups(self):
        # These are always looking up fixed names.
        # Therefore, get best efficiency by letting Cython do the lookup
        # and so infer the types
        assert self.keyword_pattern_names

        from .UtilNodes import ResultRefNode, TempResultFromStatNode

        passed_rr = ResultRefNode(pos=self.pos, type=PyrexTypes.c_bint_type)
        stats = []
        for pattern_name, subject_temp, lookup in zip(
            self.keyword_pattern_names,
            self.keyword_subject_temps,
            self.keyword_subject_attrs,
        ):
            if subject_temp:
                subject_temp.arg = lookup  # it should now know the type
                stat = Nodes.SingleAssignmentNode(
                    pattern_name.pos, lhs=subject_temp, rhs=lookup
                )
            else:
                stat = Nodes.ExprStatNode(pattern_name.pos, expr=lookup)
            stats.append(stat)
        except_clause = Nodes.ExceptClauseNode(
            self.pos,
            pattern=[
                ExprNodes.NameNode(
                    self.pos,
                    name="AttributeError",
                    entry=Builtin.builtin_scope.lookup("AttributeError"),
                )
            ],
            body=Nodes.StatListNode(
                self.pos,
                stats=[
                    Nodes.SingleAssignmentNode(
                        self.pos,
                        lhs=passed_rr,
                        rhs=ExprNodes.BoolNode(self.pos, value=False),
                    )
                ],
            ),
            target=None,
        )
        else_clause = Nodes.SingleAssignmentNode(
            self.pos, lhs=passed_rr, rhs=ExprNodes.BoolNode(self.pos, value=True)
        )
        try_except = Nodes.TryExceptStatNode(
            self.pos,
            body=Nodes.StatListNode(self.pos, stats=stats),
            except_clauses=[except_clause],
            else_clause=else_clause,
        )
        return TempResultFromStatNode(passed_rr, try_except)

    def _calculate_match_self(self):
        # -1 is "unknown", 0 is false, 1 is true
        if len(self.positional_patterns) != 1 or self.keyword_pattern_names:
            return 0
        if self.class_known_type:
            for type_attr in [
                "is_pytuple_type",
                "is_pylist_type",
                "is_pyanydict_type",
                "is_pyanyset_type",
                "is_bytes_or_str_or_bytearray",
            ]:
                if getattr(self.class_known_type, type_attr):
                    return 1
            for t in [
                Builtin.bool_type,
                Builtin.float_type,
                Builtin.int_type,
            ]:
                if self.class_known_type.subtype_of_resolved_type(t):
                    return 1
            if self.class_known_type.is_extension_type:
                tp = self.class_known_type
                while tp:
                    if (not tp.is_extension_type or
                        tp.is_external
                        or not self.class_known_type.scope.method_table_cname
                    ):  # effectively extern visibility:
                        return -1
                    tp = tp.base_type
                # We know enough about the type's provinence to know it can't match a self argument
                return 0
        return -1


    def make_positional_args_call(self, subject_node, class_node):
        assert self.positional_patterns
        util_code = UtilityCode.load_cached("ClassPositionalPatterns", "MatchCase.c")
        keynames = [
            ExprNodes.UnicodeNode(n.pos, value=n.name)
            for n in self.keyword_pattern_names
        ]

        match_self = ExprNodes.IntNode(self.pos, value=str(self._calculate_match_self()))
        n_subjects = ExprNodes.IntNode(self.pos, value=str(len(self.positional_patterns)))
        return EvaluateWithKeysAndSubjectsArrays(
            self.pos,
            arg=ExprNodes.PythonCapiCallNode(
                self.pos,
                "__Pyx_MatchCase_ClassPositional",
                self.Pyx_positional_type,
                utility_code=util_code,
                args=[
                    subject_node,
                    class_node,
                    EvaluateWithKeysAndSubjectsArrays.make_keys_node(self.pos),
                    ExprNodes.IntNode(self.pos, value=str(len(keynames))),
                    match_self,
                    EvaluateWithKeysAndSubjectsArrays.make_subjects_node(self.pos),
                    n_subjects,
                ]
            ),
            subjects_array=self.positional_subject_temps,
            keys_array=keynames,
        )

    def make_subpattern_checks(self):
        patterns = self.keyword_pattern_patterns + self.positional_patterns
        temps = self.keyword_subject_temps + self.positional_subject_temps
        checks = []
        for temp, pattern in zip(temps, patterns):
            if temp:
                checks.append(pattern.get_comparison_node(temp))
        return checks

    def get_comparison_node(self, subject_node, sequence_mapping_temp=None):
        from .UtilNodes import ResultRefNode, EvalWithTempExprNode

        if self.class_known_type:
            class_node = self.class_.clone_node()
            class_node.entry = self.class_known_type.entry
        else:
            if self.class_.type is not Builtin.type_type:
                util_code = UtilityCode.load_cached("MatchClassTypeGuard", "MatchCase.c")
                class_node = ExprNodes.PythonCapiCallNode(
                    self.pos,
                    "__Pyx_MatchCase_TypeGuard",
                    self.Pyx_typeguard_type,
                    utility_code=util_code,
                    args=[self.class_],
                )
            class_node = ResultRefNode(class_node)

        all_checks = []
        all_checks.append(self.make_typecheck_call(subject_node, class_node))

        if self.class_known_type:
            # From this point on we know the type of the subject
            subject_node = ExprNodes.TypecastNode(
                self.class_.pos,
                operand=subject_node,
                type=self.class_known_type,
                typecheck=False,
            )
        if self.positional_patterns:
            all_checks.append(self.make_positional_args_call(subject_node, class_node))
        if self.keyword_pattern_names:
            all_checks.append(self.make_keyword_pattern_lookups())

        all_checks.extend(self.make_subpattern_checks())

        if any(isinstance(ch, ExprNodes.BoolNode) and not ch.value for ch in all_checks):
            # handle any obvious failures
            return ExprNodes.BoolNode(self.pos, value=False)

        all_checks = generate_binop_tree_from_list(self.pos, "and", all_checks)

        if isinstance(class_node, ResultRefNode) and not all_checks.is_literal:
            return LazyCoerceToBool(class_node.pos, arg=EvalWithTempExprNode(class_node, all_checks))
        else:
            return LazyCoerceToBool(all_checks.pos, arg=all_checks)

    def analyse_declarations(self, env):
        self.validate_keywords()
        # Try to work out the type early
        self.class_.analyse_declarations(env)
        self.class_known_type = self.class_.analyse_as_extension_type(env)
        for p in self.positional_patterns:
            p.analyse_declarations(env)
        for p_name, p in zip(self.keyword_pattern_names, self.keyword_pattern_patterns):
            p_name.analyse_declarations(env)
            p.analyse_declarations(env)
        super(ClassPatternNode, self).analyse_declarations(env)

    def analyse_pattern_expressions(self, env, sequence_mapping_temp):
        self.class_ = self.class_.analyse_types(env)

        self.keyword_subject_attrs = [ a.analyse_types(env) for a in self.keyword_subject_attrs ]
        self.keyword_pattern_patterns = [ p.analyse_pattern_expressions(env, None) for p in self.keyword_pattern_patterns ]
        self.positional_patterns = [ p.analyse_pattern_expressions(env, None) for p in self.positional_patterns ]

        return self

    def allocate_subject_temps(self, code):
        for temp in self.keyword_subject_temps + self.positional_subject_temps:
            if temp is not None:
                temp.allocate(code)
        for pattern in self.keyword_pattern_patterns + self.positional_patterns:
            pattern.allocate_subject_temps(code)

    def release_subject_temps(self, code):
        for temp in self.keyword_subject_temps + self.positional_subject_temps:
            if temp is not None:
                temp.release(code)
        for pattern in self.keyword_pattern_patterns + self.positional_patterns:
            pattern.release_subject_temps(code)

    def dispose_of_subject_temps(self, code):
        for temp in self.keyword_subject_temps + self.positional_subject_temps:
            if temp is not None:
                code.put_xdecref_clear(temp.result(), temp.type)
        for pattern in self.keyword_pattern_patterns + self.positional_patterns:
            pattern.dispose_of_subject_temps(code)

    def validate_keywords(self):
        seen = set()
        for kw in self.keyword_pattern_names:
            if kw.name in seen:
                error(
                    self.pos,
                    f"attribute name repeated in class pattern: '{kw.name}'"
                )
            seen.add(kw.name)


class MatchValuePrimaryCmpNode(ExprNodes.PrimaryCmpNode):
    """
    Overrides PrimaryCmpNode to be a little more restrictive
    than normal. Specifically, Cython normally allows:
      int(1) is True
    Here, True should only match an exact Python object, or
    a bint(True).
    """
    def __init__(self, pos, **kwds):
        super().__init__(pos, **kwds)
        # operand1 should be the match subject
        assert isinstance(self.operand1, (ExprNodes.CloneNode, TrackTypeTempNode, AssignableTempNode)), type(self.operand1)
        assert self.operator in ["==", "is"]

    def analyse_types(self, env):
        if (self.operator == "is" and
                isinstance(self.operand2, ExprNodes.BoolNode)):
            # operand1's type should already be known
            op1_type = self.operand1.type
            if not (op1_type.is_pyobject or op1_type is PyrexTypes.c_bint_type):
                return ExprNodes.BoolNode(self.pos, value=False).analyse_expressions(env)

        return super().analyse_types(env)


class SubstitutedIfStatListNode(Nodes.StatListNode):
    """
    Like StatListNode but with a "goto end of match" at the
    end of it

    match_node   - the enclosing match statement
    """

    def generate_execution_code(self, code):
        super(SubstitutedIfStatListNode, self).generate_execution_code(code)
        if not self.is_terminator:
            code.put_goto(self.match_node.end_label)


class StaticTypeCheckNode(ExprNodes.ExprNode):
    """
    Useful for structural pattern matching, where we
    can skip the "is_seqeunce/is_mapping" checks if
    we know the type in advance (or reduce it to a
    None check).

    This should optimize itself out at the analyse_expressions
    stage

    arg        ExprNode
    fallback   ExprNode   Function to be called if the static
                            typecheck isn't optimized out
    check      callable   Returns True, False, or None (for "can't tell")
    """

    child_attrs = ["fallback"]  # arg in not included since it's in "fallback"

    def analyse_types(self, env):
        check = self.check(self.arg.type)
        if check:
            if self.arg.may_be_none():
                return ExprNodes.PrimaryCmpNode(
                    self.pos,
                    operand1=self.arg,
                    operand2=ExprNodes.NoneNode(self.pos),
                    operator="is_not",
                ).analyse_expressions(env)
            else:
                return ExprNodes.BoolNode(pos=self.pos, value=True).analyse_expressions(
                    env
                )
        elif check is None:
            return self.fallback.analyse_expressions(env)
        else:
            return ExprNodes.BoolNode(pos=self.pos, value=False).analyse_expressions(
                env
            )


class AssignableTempNode(ExprNodes.TempNode):
    lhs_of_first_assignment = True  # assume it can be assigned to once
    _assigned_twice = False

    def __init__(self, pos, *args, is_addressable=False, **kwds):
        self._is_addressable = is_addressable
        super().__init__(pos, *args, **kwds)

    def is_addressable(self):
        return self._is_addressable

    def infer_type(self, env):
        return self.type

    def generate_assignment_code(self, rhs, code, overloaded_assignment=False):
        assert (
            not self._assigned_twice
        )  # if this happens it's not a disaster but it needs a refactor
        self._assigned_twice = True
        if self.type.is_pyobject:
            rhs.make_owned_reference(code)
            if not self.lhs_of_first_assignment:
                code.put_decref(self.result(), self.ctype())
        code.putln(
            "%s = %s;"
            % (
                self.result(),
                rhs.result() if overloaded_assignment else rhs.result_as(self.ctype()),
            )
        )
        rhs.generate_post_assignment_code(code)
        rhs.free_temps(code)

    def generate_post_assignment_code(self, code):
        code.put_incref(self.result(), self.type)

    def generate_disposal_code(self, code):
        pass  # handled elsewhere - we expect to use this temp multiple times

    def clone_node(self):
        return self  # temps break if you make a copy!


class TrackTypeTempNode(AssignableTempNode):
    #  Like a temp node, but type is set from arg

    lhs_of_first_assignment = True  # assume it can be assigned to once
    _assigned_twice = False

    @property
    def type(self):
        return getattr(self.arg, "type", None)

    def __init__(self, pos, arg):
        ExprNodes.ExprNode.__init__(self, pos)  # skip a level
        self.arg = arg

    def infer_type(self, env):
        return self.arg.infer_type(env)


class SliceToListNode(ExprNodes.ExprNode):
    """
    Used as a brief temporary node to optimize
    case [..., *_, ...].
    Always reduces to something else after analyse_types
    """

    subexprs = ["base", "start", "stop", "length_node"]

    type = Builtin.list_type

    Pyx_iterable_to_list_type = PyrexTypes.CFuncType(
        Builtin.list_type,
        [
            PyrexTypes.CFuncTypeArg("iterable", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("start", PyrexTypes.c_py_ssize_t_type, None),
            PyrexTypes.CFuncTypeArg("stop", PyrexTypes.c_py_ssize_t_type, None),
        ],
    )

    def generate_via_slicing(self, env):
        # for any more complicated type that doesn't have a specialized path
        # we can simply slice it and copy it to list
        res = ExprNodes.CompilerDirectivesExprNode(
            arg=ExprNodes.SliceIndexNode(
                self.pos, base=self.base, start=self.start, stop=self.stop
            ),
            directives=copy_inherited_directives(
                env.directives, boundcheck=False, wraparound=False
            ),
        )
        res = ExprNodes.SimpleCallNode(
            self.pos,
            function=ExprNodes.NameNode(
                self.pos,
                name="list",
                entry=Builtin.builtin_scope.lookup("list"),
            ),
            args=[res],
        )
        return res

    def get_stop(self):
        if not self.stop:
            if self.length_node:
                return self.length_node
            else:
                return ExprNodes.SimpleCallNode(
                    self.pos,
                    function=ExprNodes.NameNode(
                        self.pos, name="len", entry=Builtin.builtin_scope.lookup("len")
                    ),
                    args=[self.base],
                )
        else:
            return self.stop

    def generate_for_memoryview(self, env):
        # Requires Cython code generation...
        # A list comprehension with indexing turns out to be a good option
        from .UtilityCode import CythonUtilityCode

        suffix = self.base.type.specialization_suffix()
        util_code = CythonUtilityCode.load(
            "MemoryviewSliceToList",
            "MatchCase_Cy.pyx",
            context={
                "decl_code": self.base.type.empty_declaration_code(pyrex=True),
                "suffix": suffix,
            },
        )
        func_type = PyrexTypes.CFuncType(
            Builtin.list_type,
            [
                PyrexTypes.CFuncTypeArg("x", self.base.type, None),
                PyrexTypes.CFuncTypeArg("start", PyrexTypes.c_py_ssize_t_type, None),
                PyrexTypes.CFuncTypeArg("stop", PyrexTypes.c_py_ssize_t_type, None),
            ],
        )
        env.use_utility_code(
            util_code
        )  # attaching it to the call node doesn't seem enough
        return ExprNodes.PythonCapiCallNode(
            self.pos,
            "__Pyx_MatchCase_SliceMemoryview_%s" % suffix,
            func_type,
            utility_code=util_code,
            args=[
                self.base,
                self.start if self.start else ExprNodes.IntNode.for_size(self.pos, 0),
                self.get_stop(),
            ],
        )

    def generate_for_pyobject(self):
        util_code_name = None
        func_name = None
        if self.base.type.is_pytuple_type:
            util_code_name = "TupleSliceToList"
        elif self.base.type.is_pylist_type:
            func_name = "PyList_GetSlice"
        elif (
            self.base.type.is_pyobject
            and self.base.type is not PyrexTypes.py_object_type
        ):
            # some specialized type that almost certainly isn't a list. Just go straight
            # to the "other" version of it
            util_code_name = "OtherSequenceSliceToList"
        else:
            util_code_name = "UnknownTypeSliceToList"
        if not func_name:
            func_name = "__Pyx_MatchCase_%s" % util_code_name
        if util_code_name:
            util_code = UtilityCode.load_cached(
                util_code_name,
                "MatchCase.c"
            )
        else:
            util_code = None
        start = self.start if self.start else ExprNodes.IntNode.for_size(self.pos, 0)
        stop = self.get_stop()
        return ExprNodes.PythonCapiCallNode(
            self.pos,
            func_name,
            self.Pyx_iterable_to_list_type,
            utility_code=util_code,
            args=[self.base, start, stop],
        )

    def analyse_types(self, env):
        self.base = self.base.analyse_types(env)
        if self.base.type.is_memoryviewslice:
            result = self.generate_for_memoryview(env)
        elif self.base.type.is_pyobject:
            result = self.generate_for_pyobject()
        else:
            # Some other type (probably a ctuple).
            # Just slice it, copy it to a list and hope it works
            result = self.generate_via_slicing(env)
        return result.analyse_types(env)


class LazyCoerceToPyObject(ExprNodes.ExprNode):
    """
    Just calls "self.arg.coerce_to_pyobject" when it's analysed,
    so doesn't need 'env' when it's created
    arg  - ExprNode
    """
    subexprs = ["arg"]
    type = PyrexTypes.py_object_type

    def analyse_types(self, env):
        return self.arg.analyse_types(env).coerce_to_pyobject(env)


class LazyCoerceToBool(ExprNodes.ExprNode):
    """
    Just calls "self.arg.analyse_boolean_expression"
    when it's analysed, so doesn't need 'env' when it's created
    arg  - ExprNode
    """
    subexprs = ["arg"]
    type = PyrexTypes.c_bint_type

    def analyse_types(self, env):
        return self.arg.analyse_boolean_expression(env)

def generate_binop_tree_from_list(pos, operator, list_of_tests):
    """
    Given a list of operands generates a roughly balanced tree:
    (test1 op test2) op (test3 op test4)
    This is better than (((test1 op test2) op test3) op test4)
    because it generates a shallower tree of nodes so is
    less likely to overflow the compiler
    """
    len_tests = len(list_of_tests)
    if len_tests == 1:
        return list_of_tests[0]
    else:
        split_idx = len_tests // 2
        operand1 = generate_binop_tree_from_list(
            pos, operator, list_of_tests[:split_idx]
        )
        operand2 = generate_binop_tree_from_list(
            pos, operator, list_of_tests[split_idx:]
        )
        return ExprNodes.binop_node(
            pos,
            operator=operator,
            operand1=operand1,
            operand2=operand2
        )


class EvaluateWithKeysAndSubjectsArrays(ExprNodes.ExprNode):
    """
    This is responsible for setting up up the arrays of
    subjects and keys that are used in
    the function calls that handle these types of patterns
    (mapping and class patterns).
    Essentially 'arg' is evaluated with the keys and subjects
    arrays.
    """
    subexprs = ["keys_array", "arg"]

    keys_array_cname = "__pyx_match_mapping_keys"
    subjects_array_cname = "__pyx_match_mapping_subjects"

    is_temp = True

    @property
    def type(self):
        return self.arg.type

    @classmethod
    def make_keys_node(cls, pos):
        return ExprNodes.RawCNameExprNode(
            pos,
            type=PyrexTypes.c_void_ptr_type,
            cname=cls.keys_array_cname
        )

    @classmethod
    def make_subjects_node(cls, pos):
        return ExprNodes.RawCNameExprNode(
            pos,
            type=PyrexTypes.c_void_ptr_ptr_type,
            cname=cls.subjects_array_cname
        )

    def analyse_types(self, env):
        self.arg = self.arg.analyse_types(env)
        assert self.arg.type is PyrexTypes.c_bint_type
        self.keys_array = [
            key.analyse_types(env).coerce_to_pyobject(env).coerce_to_simple(env)
            for key in self.keys_array
        ]
        return self

    def generate_evaluation_code(self, code):
        for k in self.keys_array:
            k.generate_evaluation_code(code)

        code.mark_pos(self.pos)
        if self.is_temp:
            self.allocate_temp_result(code)

        code.putln("{")
        keys_str = ", ".join(k.result() for k in self.keys_array)
        if not keys_str:
            # GCC gets worried about overflow if we pass
            # a genuinely empty array
            keys_str = "NULL"
        code.putln("PyObject *%s[] = {%s};" % (
            EvaluateWithKeysAndSubjectsArrays.keys_array_cname,
            keys_str,
        ))
        subjects_str = ", ".join(
            "&"+subject.result() if subject is not None else "NULL" for subject in self.subjects_array
        )
        if not subjects_str:
            # GCC gets worried about overflow if we pass
            # a genuinely empty array
            subjects_str = "NULL"
        code.putln("PyObject **%s[] = {%s};" % (
            EvaluateWithKeysAndSubjectsArrays.subjects_array_cname,
            subjects_str
        ))

        self.arg.generate_evaluation_code(code)
        code.putln(f"{self.result()} = {self.arg.result()};")

        code.putln("}")
        self.generate_subexpr_disposal_code(code)
        self.free_subexpr_temps(code)
