# Nodes for structural pattern matching.
#
# In a separate file because they're unlikely to be useful for much else.

from .Nodes import Node, StatNode, ErrorNode
from . import Nodes
from .Errors import error
from . import ExprNodes
from . import PyrexTypes


class MatchNode(StatNode):
    """
    subject  ExprNode    The expression to be matched
    cases    [MatchCaseBaseNode]  list of cases

    subject_clonenode  CloneNode of subject
    """

    child_attrs = ["subject", "cases"]

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
        for n, c in enumerate(self.cases + [None]):  # The None is dummy at the end
            if c is not None and c.is_simple_value_comparison():
                if_clause = Nodes.IfClauseNode(
                    c.pos,
                    condition=c.pattern.get_simple_comparison_node(subject),
                    body=c.body,
                )
                for t in c.pattern.get_targets():
                    # generate an assignment at the start of the body
                    if_clause.body.stats.insert(
                        0,
                        Nodes.SingleAssignmentNode(
                            c.pos, lhs=NameNode(c.pos, name=t), rhs=subject
                        ),
                    )
                if not current_if_statement:
                    current_if_statement = Nodes.IfStatNode(
                        c.pos, if_clauses=[], else_clause=None
                    )
                current_if_statement.if_clauses.append(if_clause)
                self.cases[n] = None  # remove case
            elif current_if_statement:
                # this cannot be simplified, but previous case(s) were
                self.cases[n - 1] = SubstitutedMatchCaseNode(
                    current_if_statement.pos, body=current_if_statement
                )
                current_if_statement = None
        # eliminate optimized cases
        self.cases = [c for c in self.cases if c is not None]

    def analyse_declarations(self, env):
        self.subject.analyse_declarations(env)
        for c in self.cases:
            c.analyse_declarations(env)

    def analyse_expressions(self, env):
        self.subject = self.subject.analyse_expressions(env)
        assert isinstance(self.subject, ExprNodes.ProxyNode)
        if not self.subject.arg.is_literal:
            self.subject.arg = self.subject.arg.coerce_to_temp(env)
        subject = self.subject_clonenode
        self.cases = [c.analyse_case_expressions(subject, env) for c in self.cases]
        return self

    def generate_execution_code(self, code):
        self.subject.generate_evaluation_code(code)
        for c in self.cases:
            c.generate_execution_code(code)
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
    """

    child_attrs = ["pattern", "body", "guard"]

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

    def analyse_declarations(self, env):
        self.pattern.analyse_declarations(env)
        if self.guard:
            self.guard.analyse_declarations(env)
        self.body.analyse_declarations(env)

    def analyse_case_expressions(self, subject_node, env):
        if self.guard:
            error(self.pos, "Cases with guards are currently not supported")
            return self
        error(self.pos, "This case statement is not yet supported")
        return self

    def generate_execution_code(self, code):
        error(self.pos, "This case statement is not yet supported")


class SubstitutedMatchCaseNode(MatchCaseBaseNode):
    # body  - Node -  The (probably) if statement that it's replaced with
    child_attrs = ["body"]

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)

    def analyse_case_expressions(self, subject_node, env):
        self.body = self.body.analyse_expressions(env)
        return self

    def generate_execution_code(self, code):
        self.body.generate_execution_code(code)


class PatternNode(Node):
    """
    PatternNode is not an expression because
    it does several things (evaluating a boolean expression,
    assignment of targets), and they need to be done at different
    times.

    as_targets   [NameNode]    any target assign by "as"
    """

    child_attrs = ["as_targets"]

    def __init__(self, pos, **kwds):
        if "as_targets" not in kwds:
            kwds["as_targets"] = []
        super(PatternNode, self).__init__(pos, **kwds)

    def is_irrefutable(self):
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

    def validate_irrefutable(self):
        for attr in self.child_attrs:
            child = getattr(self, attr)
            if child is not None and isinstance(child, PatternNode):
                child.validate_irrefutable()


class MatchValuePatternNode(PatternNode):
    """
    value   ExprNode
    is_is_check   bool     Picks "is" or equality check
    """

    child_attrs = PatternNode.child_attrs + ["value"]
    is_is_check = False

    def get_main_pattern_targets(self):
        return set()

    def is_simple_value_comparison(self):
        return True

    def get_simple_comparison_node(self, subject_node):
        op = "is" if self.is_is_check else "=="
        return MatchValuePrimaryCmpNode(
            self.pos, operator=op, operand1=subject_node, operand2=self.value
        )


class MatchAndAssignPatternNode(PatternNode):
    """
    target   NameNode or None  the target to assign to (None = wildcard)
    is_star  bool
    """

    target = None
    is_star = False

    child_atts = PatternNode.child_attrs + ["target"]

    def is_irrefutable(self):
        return not self.is_star

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
        return ExprNodes.BoolNode(self.pos, value=True)


class OrPatternNode(PatternNode):
    """
    alternatives   list of PatternNodes
    """

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

    def get_simple_comparison_node(self, subject_node):
        assert self.is_simple_value_comparison()
        assert len(self.alternatives) >= 2
        binop = ExprNodes.BoolBinopNode(
            self.pos,
            operator="or",
            operand1=self.alternatives[0].get_simple_comparison_node(subject_node),
            operand2=self.alternatives[1].get_simple_comparison_node(subject_node),
        )
        for a in self.alternatives[2:]:
            binop = ExprNodes.BoolBinopNode(
                self.pos,
                operator="or",
                operand1=binop,
                operand2=a.get_simple_comparison_node(subject_node),
            )
        return binop


class MatchSequencePatternNode(PatternNode):
    """
    patterns   list of PatternNodes
    """

    child_attrs = PatternNode.child_attrs + ["patterns"]

    def get_main_pattern_targets(self):
        targets = set()
        for pattern in self.patterns:
            self.update_targets_with_targets(targets, pattern.get_targets())
        return targets


class MatchMappingPatternNode(PatternNode):
    """
    keys   list of NameNodes
    value_patterns  list of PatternNodes of equal length to keys
    double_star_capture_target  NameNode or None
    """

    keys = []
    value_patterns = []
    double_star_capture_target = None

    child_attrs = PatternNode.child_attrs + [
        "keys",
        "value_patterns",
        "double_star_capture_target",
    ]

    def get_main_pattern_targets(self):
        targets = set()
        for pattern in self.value_patterns:
            self.update_targets_with_targets(targets, pattern.get_targets())
        if self.double_star_capture_target:
            self.add_target_to_targets(targets, self.double_star_capture_target.name)
        return targets


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

    child_attrs = PatternNode.child_attrs + [
        "class_",
        "positional_patterns",
        "keyword_pattern_names",
        "keyword_pattern_patterns",
    ]

    def get_main_pattern_targets(self):
        targets = set()
        for pattern in self.positional_patterns + self.keyword_pattern_patterns:
            self.update_targets_with_targets(targets, pattern.get_targets())
        return targets


class MatchValuePrimaryCmpNode(ExprNodes.PrimaryCmpNode):
    """
    Overrides PrimaryCmpNode to be a little more restrictive
    that normal. Specifically, Cython normally allows:
      int(1) is True
    Here, True should only match an exact Python object, or
    a bint(True).
    """
    def __init__(self, pos, **kwds):
        super().__init__(pos, **kwds)
        # operand1 should be the match subject
        assert isinstance(self.operand1, ExprNodes.CloneNode)
        assert self.operator in ["==", "is"]

    def analyse_types(self, env):
        if (self.operator == "is" and
                isinstance(self.operand2, ExprNodes.BoolNode)):
            # because operand1 is a CloneNode its type should already be known
            op1_type = self.operand1.arg.type
            if not (op1_type.is_pyobject or op1_type is PyrexTypes.c_bint_type):
                return ExprNodes.BoolNode(self.pos, value=False).analyse_expressions(env)

        return super().analyse_types(env)