# Nodes for structural pattern matching.
#
# In a separate file because they're unlikely to be useful
# for much else

from .Nodes import Node, StatNode
from . import Nodes
from .Errors import error
from . import ExprNodes


class MatchNode(StatNode):
    """
    subject  ExprNode    The expression to be matched
    cases    [MatchCaseBaseNode]  list of cases
    """

    child_attrs = ["subject", "cases"]

    subject_clonenode = None  # set to a value if we require a temp

    def validate_irrefutable(self):
        found_irrefutable_case = None
        for c in self.cases:
            if found_irrefutable_case:
                error(
                    found_irrefutable_case.pos,
                    (
                        "%s makes remaining patterns unreachable"
                        % found_irrefutable_case.pattern.irrefutable_message()
                    ),
                )
                break
            if c.is_irrefutable():
                found_irrefutable_case = c
            c.validate_irrefutable()

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
                body = SubstitutedIfStatListNode(
                    c.body.pos,
                    stats = c.body.stats,
                    match_node = self
                )
                if_clause = Nodes.IfClauseNode(
                    c.pos,
                    condition=c.pattern.get_simple_comparison_node(subject),
                    body=body,
                )
                assignments = c.pattern.generate_target_assignments(subject)
                if assignments:
                    if_clause.body.stats.insert(0, assignments)
                if not current_if_statement:
                    current_if_statement = Nodes.IfStatNode(
                        c.pos, if_clauses=[], else_clause=None
                    )
                current_if_statement.if_clauses.append(if_clause)
                self.cases[n] = None  # remove case
            elif current_if_statement:
                # this cannot be simplified, but previous case(s) were
                self.cases[n - 1] = SubstitutedMatchCaseNode(
                    current_if_statement.pos, body = current_if_statement
                )
                current_if_statement = None
        # eliminate optimized cases
        self.cases = [c for c in self.cases if c is not None]

    def analyse_declarations(self, env):
        self.subject.analyse_declarations(env)
        subject = self.get_or_setup_clonenode()
        for c in self.cases:
            c.analyse_case_declarations(subject, env)

    def analyse_expressions(self, env):
        self.subject = self.subject.analyse_expressions(env)
        assert isinstance(self.subject, ExprNodes.ProxyNode)
        if not self.subject.arg.is_literal:
            self.subject.arg = self.subject.arg.coerce_to_temp(env)
        subject = self.subject_clonenode
        self.cases = [c.analyse_case_expressions(subject, env) for c in self.cases]
        return self

    def generate_execution_code(self, code):
        end_label = self.end_label = code.new_label()
        if self.subject_clonenode:
            self.subject.generate_evaluation_code(code)
        for c in self.cases:
            c.generate_execution_code(code, end_label)
        if code.label_used(end_label):
            code.put_label(end_label)
        if self.subject_clonenode:
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
    original_pattern  PatternNode  (not coerced to temp)
    target_assignments  [ SingleAssignmentNodes ]
    """

    target_assignments = None
    child_attrs = ["pattern", "target_assignments", "guard", "body"]

    def is_irrefutable(self):
        return self.pattern.is_irrefutable() and not self.guard

    def is_simple_value_comparison(self):
        if self.guard:
            return False
        return self.pattern.is_simple_value_comparison()

    def validate_targets(self):
        self.pattern.get_targets()

    def validate_irrefutable(self):
        self.pattern.validate_irrefutable()

    def analyse_case_declarations(self, subject_node, env):
        self.pattern.analyse_declarations(env)
        self.target_assignments = self.pattern.generate_target_assignments(subject_node)
        if self.target_assignments:
            self.target_assignments.analyse_declarations(env)
        if self.guard:
            self.guard.analyse_declarations(env)
        self.body.analyse_declarations(env)

    def analyse_case_expressions(self, subject_node, env):
        self.pattern = self.pattern.analyse_pattern_expressions(subject_node, env)
        self.original_pattern = self.pattern
        self.pattern.comp_node = self.pattern.comp_node.coerce_to_boolean(
            env
        ).coerce_to_simple(env)
        if self.target_assignments:
            self.target_assignments = self.target_assignments.analyse_expressions(env)
        if self.guard:
            self.guard = self.guard.analyse_temp_boolean_expression(env)
        self.body = self.body.analyse_expressions(env)
        return self

    def generate_execution_code(self, code, end_label):
        self.pattern.generate_comparison_evaluation_code(code)
        code.putln("if (%s) { /* pattern */" % self.pattern.comparison_result())
        self.pattern.generate_comparison_disposal_code(code)
        self.pattern.free_comparison_temps(code)
        if self.target_assignments:
            self.target_assignments.generate_execution_code(code)
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


class SubstitutedMatchCaseNode(MatchCaseBaseNode):
    # body  - Node -  The (probably) if statement that it's replaced with
    child_attrs = ["body"]

    def analyse_case_declarations(self, subject_node, env):
        self.analyse_declarations(env)

    def analyse_declarations(self, env):
        self.body.analyse_declarations(env)

    def analyse_case_expressions(self, subject_node, env):
        self.body = self.body.analyse_expressions(env)
        return self

    def generate_execution_code(self, code, end_label):
        self.body.generate_execution_code(code)


class PatternNode(Node):
    """
    DW decided that PatternNode shouldn't be an expression because
    it does several things (evalutating a boolean expression,
    assignment of targets), and they need to be done at different
    times.

    as_targets   [NameNode]    any target assign by "as"

    Generated in analysis:
    comp_node   ExprNode     node to evaluate for the pattern
    """

    as_target = None
    comp_node = None

    # When pattern nodes are analysed it changes which children are important.
    # Therefore have two different list of child_attrs and switch
    initial_child_attrs = ["as_targets"]
    post_analysis_child_attrs = ["comp_node"]

    def __init__(self, pos, **kwds):
        super(PatternNode, self).__init__(pos, **kwds)
        if not hasattr(self, "as_targets"):
            self.as_targets = []

    @property
    def child_attrs(self):
        if self.comp_node is None:
            return self.initial_child_attrs
        else:
            return self.post_analysis_child_attrs

    def is_irrefutable(self):
        return False

    def get_targets(self):
        targets = self.get_main_pattern_targets()
        for t in self.as_targets:
            self.add_target_to_targets(targets, t.name)
        return targets

    def update_targets_with_targets(self, targets, other_targets):
        intersection = targets.intersection(other_targets)
        for i in intersection:
            error(self.pos, "multiple assignments to name '%s' in pattern" % i)
        targets.update(other_targets)

    def add_target_to_targets(self, targets, target):
        if target in targets:
            error(self.pos, "multiple assignments to name '%s in pattern" % target)
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
            if isinstance(child, PatternNode):
                child.validate_irrefutable()

    def analyse_pattern_expressions(self, subject_node, env):
        error(self.pos, "This type of pattern is not currently supported")
        return self

    def calculate_result_code(self):
        return self.comp_node.result()

    def generate_result_code(self, code):
        pass

    def generate_comparison_evaluation_code(self, code):
        self.comp_node.generate_evaluation_code(code)

    def comparison_result(self):
        return self.comp_node.result()

    def generate_comparison_disposal_code(self, code):
        self.comp_node.generate_disposal_code(code)

    def free_comparison_temps(self, code):
        self.comp_node.free_temps(code)

    def generate_target_assignments(self, subject_node):
        # Generates the assignment code needed to initialize all the targets.
        # Returns either a StatListNode or None
        assignments = []
        if self.as_target:
            if (
                isinstance(self, MatchValuePatternNode)
                and self.value
                and self.value.is_simple()
            ):
                # in this case we can optimize slightly and just take the value
                subject_node = self.value.clone_node()
            assignments.append(
                Nodes.SingleAssignmentNode(
                    self.pos, lhs=self.as_target.clone_node(), rhs=subject_node
                )
            )
        assignments.extend(self.generate_main_pattern_assignment_list(subject_node))
        if assignments:
            return Nodes.StatListNode(self.pos, stats=assignments)
        else:
            return None

    def generate_main_pattern_assignment_list(self, subject_node):
        # generates assignments for everything except the "as_target".
        # Override in subclasses.
        # Returns a list of Nodes
        return []


class MatchValuePatternNode(PatternNode):
    """
    value   ExprNode
    is_is_check   bool     Picks "is" or equality check
    """

    initial_child_attrs = PatternNode.initial_child_attrs + ["value"]

    is_is_check = False

    def get_main_pattern_targets(self):
        return set()

    def is_simple_value_comparison(self):
        return True

    def get_comparison_node(self, subject_node):
        op = "is" if self.is_is_check else "=="
        return ExprNodes.PrimaryCmpNode(
            self.pos, operator=op, operand1=subject_node, operand2=self.value
        )

    def get_simple_comparison_node(self, subject_node):
        # for this node the comparison and "simple" comparison are the same
        return self.get_comparison_node(subject_node)

    def analyse_declarations(self, env):
        super(MatchValuePatternNode, self).analyse_declarations(env)
        if self.value:
            self.value.analyse_declarations(env)

    def analyse_pattern_expressions(self, subject_node, env):
        if self.value:
            self.value = self.value.analyse_expressions(env)
        self.comp_node = self.get_comparison_node(subject_node).analyse_expressions(env)
        return self


class MatchAndAssignPatternNode(PatternNode):
    """
    target   NameNode or None  the target to assign to (None = wildcard)
    is_star  bool
    """

    target = None
    is_star = False

    initial_child_attrs = PatternNode.initial_child_attrs + ["target"]

    def is_irrefutable(self):
        return not self.is_star

    def irrefutable_message(self):
        if self.target:
            return "name capture '%s'" % self.target.name
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

    def get_comparison_node(self, subject_node):
        return self.get_simple_comparison_node(subject_node)

    def generate_main_pattern_assignment_list(self, subject_node):
        if self.target:
            return [
                Nodes.SingleAssignmentNode(
                    self.pos, lhs=self.target.clone_node(), rhs=subject_node
                )
            ]
        else:
            return []

    def analyse_pattern_expressions(self, subject_node, env):
        if self.is_star:
            return super(MatchAndAssignPatternNode, self).analyse_pattern_expressions(
                subject_node, env
            )
        else:
            self.comp_node = self.get_comparison_node(subject_node).analyse_expressions(
                env
            )
            return self


class OrPatternNode(PatternNode):
    """
    alternatives   list of PatternNodes
    """

    initial_child_attrs = PatternNode.initial_child_attrs + ["alternatives"]

    def get_first_irrefutable(self):
        for a in self.alternatives:
            if a.is_irrefutable():
                return a
        return None

    def is_irrefutable(self):
        return self.get_first_irrefutable() is not None

    def irrefutable_message(self):
        return self.get_first_irrefutable().irrefutable_message()

    def get_main_pattern_targets(self):
        child_targets = None
        for ch in self.alternatives:
            ch_targets = ch.get_targets()
            if child_targets is not None and child_targets != ch_targets:
                error(self.pos, "alternative patterns bind different names")
            child_targets = ch_targets
        return child_targets

    def validate_irrefutable(self):
        super(OrPatternNode, self).validate_irrefutable()
        found_irrefutable_case = None
        for a in self.alternatives:
            if found_irrefutable_case:
                error(
                    found_irrefutable_case.pos,
                    (
                        "%s makes remaining patterns unreachable"
                        % found_irrefutable_case.irrefutable_message()
                    ),
                )
                break
            if a.is_irrefutable():
                found_irrefutable_case = a
            a.validate_irrefutable()

    def is_simple_value_comparison(self):
        return all(a.is_simple_value_comparison() for a in self.alternatives)

    def get_simple_comparison_node(self, subject_node):
        assert self.is_simple_value_comparison()
        assert len(self.alternatives) >= 2, self.alternatives
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

    def analyse_declarations(self, env):
        super(OrPatternNode, self).analyse_declarations(env)
        for a in self.alternatives:
            a.analyse_declarations(env)

    def analyse_pattern_expressions(self, subject_node, env):
        self.alternatives = [
            a.analyse_pattern_expressions(subject_node, env) for a in self.alternatives
        ]
        self.comp_node = self.get_comparison_node(
            subject_node
        ).analyse_temp_boolean_expression(env)
        return self

    def generate_main_pattern_assignment_list(self, subject_node):
        assignments = []
        for a in self.alternatives:
            a_assignment = a.generate_target_assignments(subject_node)
            if a_assignment:
                # Switch code paths depending on which node gets assigned
                error(self.pos, "Need to handle assignments in or nodes correctly")
                assignments.append(a_assignment)
        return assignments


class MatchSequencePatternNode(PatternNode):
    """
    patterns   list of PatternNodes
    """

    initial_child_attrs = PatternNode.initial_child_attrs + ["patterns"]

    def get_main_pattern_targets(self):
        targets = set()
        for p in self.patterns:
            self.update_targets_with_targets(targets, p.get_targets())
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

    initial_child_attrs = PatternNode.initial_child_attrs + [
        "keys",
        "value_patterns",
        "double_star_capture_target",
    ]

    def get_main_pattern_targets(self):
        targets = set()
        for p in self.value_patterns:
            self.update_targets_with_targets(targets, p.get_targets())
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

    initial_child_attrs = PatternNode.initial_child_attrs + [
        "class_",
        "positional_patterns",
        "keyword_pattern_names",
        "keyword_pattern_patterns",
    ]

    def get_main_pattern_targets(self):
        targets = set()
        for p in self.positional_patterns + self.keyword_pattern_patterns:
            self.update_targets_with_targets(targets, p.get_targets())
        return targets


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

