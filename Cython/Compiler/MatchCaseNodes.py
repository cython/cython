# Nodes for structural pattern matching.
#
# In a separate file because they're unlikely to be useful
# for much else

from .Nodes import Node, StatNode
from .Errors import error


class MatchNode(StatNode):
    """
    subject  ExprNode    The expression to be matched
    cases    [MatchCaseNode]  list of cases
    """

    child_attrs = ["subject", "cases"]

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

    def analyse_expressions(self, env):
        error(self.pos, "Structural pattern match is not yet implemented")
        return self


class MatchCaseNode(Node):
    """
    pattern    PatternNode
    body       StatListNode
    guard      ExprNode or None
    """

    child_attrs = ["pattern", "body", "guard"]

    def is_irrefutable(self):
        return self.pattern.is_irrefutable() and not self.guard

    def validate_targets(self):
        self.pattern.get_targets()

    def validate_irrefutable(self):
        self.pattern.validate_irrefutable()


class PatternNode(Node):
    """
    DW decided that PatternNode shouldn't be an expression because
    it does several things (evalutating a boolean expression,
    assignment of targets), and they need to be done at different
    times.

    as_target   None or NameNode    any target assign by "as"
    """

    as_target = None

    child_attrs = ["as_target"]

    def is_irrefutable(self):
        return False

    def get_targets(self):
        targets = self.get_main_pattern_targets()
        if self.as_target:
            self.add_target_to_targets(targets, self.as_target.name)
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

    def validate_irrefutable(self):
        for attr in self.child_attrs:
            child = getattr(self, attr)
            if isinstance(child, PatternNode):
                child.validate_irrefutable()


class MatchValuePatternNode(PatternNode):
    """
    value   ExprNode        # todo be more specific
    is_check   bool     Picks "is" or equality check
    """

    child_attrs = PatternNode.child_attrs + ["value"]
    is_is_check = False

    def get_main_pattern_targets(self):
        return set()


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
            return "name capture '%s'" % self.target.name
        else:
            return "wildcard"

    def get_main_pattern_targets(self):
        if self.target:
            return {self.target.name}
        else:
            return set()


class OrPatternNode(PatternNode):
    """
    alternatives   list of PatternNodes
    """

    child_attrs = PatternNode.child_attrs + ["alternatives"]

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


class MatchSequencePatternNode(PatternNode):
    """
    patterns   list of PatternNodes
    """

    child_attrs = PatternNode.child_attrs + ["patterns"]

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

    child_atts = PatternNode.child_attrs + [
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

    child_attrs = PatternNode.child_attrs + [
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
