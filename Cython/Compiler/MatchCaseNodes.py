# Nodes for structural pattern matching.
#
# In a separate file because they're unlikely to be useful
# for much else

from .Nodes import Node, StatNode
from .Errors import error, local_errors, report_error
from . import Nodes, ExprNodes, PyrexTypes, Builtin, Options
from .Code import UtilityCode

class MatchNode(StatNode):
    """
    subject  ExprNode    The expression to be matched
    cases    [MatchCaseBaseNode]  list of cases

    sequence_mapping_temp  None or AssignableTempNode  an int temp to store result of sequence/mapping tests
    """

    child_attrs = ["subject", "cases"]

    subject_clonenode = None  # set to a value if we require a temp
    sequence_mapping_temp = None

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
                assignments = c.pattern.generate_target_assignments(subject, None)
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
        for c in self.cases:
            c.analyse_case_declarations(self.subject_clonenode, env)

    def analyse_expressions(self, env):
        sequence_mapping_count = 0
        for c in self.cases:
            if c.is_sequence_or_mapping():
                sequence_mapping_count += 1
        if sequence_mapping_count >= 2:
            self.sequence_mapping_temp = AssignableTempNode(self.pos, PyrexTypes.c_uint_type)
            self.sequence_mapping_temp.is_addressable = lambda: True

        self.subject = self.subject.analyse_expressions(env)
        assert isinstance(self.subject, ExprNodes.ProxyNode)
        if not self.subject.arg.is_literal:
            self.subject.arg = self.subject.arg.coerce_to_temp(env)
        subject = self.subject_clonenode.analyse_expressions(env)
        self.cases = [c.analyse_case_expressions(subject, env, self.sequence_mapping_temp) for c in self.cases]
        self.cases = [c for c in self.cases if c is not None]
        return self

    def generate_execution_code(self, code):
        if self.sequence_mapping_temp:
            self.sequence_mapping_temp.allocate(code)
            code.putln("%s = 0; /* sequence/mapping test temp */" 
                        % self.sequence_mapping_temp.result())
        end_label = self.end_label = code.new_label()
        if self.subject_clonenode:
            self.subject.generate_evaluation_code(code)
        for c in self.cases:
            c.generate_execution_code(code, end_label)
        if self.sequence_mapping_temp:
            self.sequence_mapping_temp.release(code)
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

    def is_sequence_or_mapping(self):
        return isinstance(self.pattern, (MatchSequencePatternNode, MatchMappingPatternNode))

    def analyse_case_declarations(self, subject_node, env):
        self.pattern.analyse_declarations(env)
        self.target_assignments = self.pattern.generate_target_assignments(subject_node, env)
        if self.target_assignments:
            self.target_assignments.analyse_declarations(env)
        if self.guard:
            self.guard.analyse_declarations(env)
        self.body.analyse_declarations(env)

    def analyse_case_expressions(self, subject_node, env, sequence_mapping_temp):
        with local_errors(True) as errors:
            self.pattern = self.pattern.analyse_pattern_expressions(subject_node, env, sequence_mapping_temp)
        if self.pattern.comp_node and self.pattern.comp_node.is_literal:
            self.pattern.comp_node.calculate_constant_result()
            if not self.pattern.comp_node.constant_result:
                # we know this pattern can't succeed. Ignore any errors and return None
                return None
        for error in errors:
            report_error(error)
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
        self.pattern.allocate_subject_temps(code)
        self.pattern.generate_comparison_evaluation_code(code)

        end_of_case_label = code.new_label()

        code.putln("if (!%s) { /* pattern */" % self.pattern.comparison_result())
        self.pattern.dispose_of_subject_temps(code)  # failed, don't need the subjects
        code.put_goto(end_of_case_label)

        code.putln("} else { /* pattern */")
        self.pattern.generate_comparison_disposal_code(code)
        self.pattern.free_comparison_temps(code)
        if self.target_assignments:
            self.target_assignments.generate_execution_code(code)
        self.pattern.dispose_of_subject_temps(code)
        self.pattern.release_subject_temps(code)  # we're done with the subjects here
        if self.guard:
            self.guard.generate_evaluation_code(code)
            code.putln("if (%s) { /* guard */" % self.guard.result())
            self.guard.generate_disposal_code(code)
            self.guard.free_temps(code)
        #body_insertion_point = code.insertion_point()
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
    DW decided that PatternNode shouldn't be an expression because
    it does several things (evalutating a boolean expression,
    assignment of targets), and they need to be done at different
    times.

    as_targets   [NameNode]    any target assign by "as"

    Generated in analysis:
    comp_node   ExprNode     node to evaluate for the pattern
    """
    # useful for type tests
    is_match_value_pattern = False

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

    def analyse_pattern_expressions(self, subject_node, env, sequence_mapping_temp):
        error(self.pos, "This type of pattern is not currently supported %s" % self)
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

    def generate_target_assignments(self, subject_node, env):
        # Generates the assignment code needed to initialize all the targets.
        # Returns either a StatListNode or None
        assignments = []
        for target in self.as_targets:
            if (
                self.is_match_value_pattern
                and self.value
                and self.value.is_simple()
            ):
                # in this case we can optimize slightly and just take the value
                subject_node = self.value.clone_node()
            assignments.append(
                Nodes.SingleAssignmentNode(
                    target.pos, lhs=target.clone_node(), rhs=subject_node
                )
            )
        assignments.extend(self.generate_main_pattern_assignment_list(subject_node, env))
        if assignments:
            return Nodes.StatListNode(self.pos, stats=assignments)
        else:
            return None

    def generate_main_pattern_assignment_list(self, subject_node, env):
        # generates assignments for everything except the "as_target".
        # Override in subclasses.
        # Returns a list of Nodes
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

    initial_child_attrs = PatternNode.initial_child_attrs + ["value"]

    is_is_check = False

    def get_main_pattern_targets(self):
        return set()

    def is_simple_value_comparison(self):
        return True

    def get_comparison_node(self, subject_node, env):
        op = "is" if self.is_is_check else "=="
        return ExprNodes.PrimaryCmpNode(
            self.pos, operator=op, operand1=subject_node, operand2=self.value
        )

    def get_simple_comparison_node(self, subject_node):
        # for this node the comparison and "simple" comparison are the same
        return self.get_comparison_node(subject_node, None)

    def analyse_declarations(self, env):
        super(MatchValuePatternNode, self).analyse_declarations(env)
        if self.value:
            self.value.analyse_declarations(env)

    def analyse_pattern_expressions(self, subject_node, env, sequence_mapping_temp):
        if self.value:
            self.value = self.value.analyse_expressions(env)
        self.comp_node = self.get_comparison_node(subject_node, env).analyse_expressions(env)
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
        return True

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
        return self.get_comparison_node(subject_node, None)
        
    def get_comparison_node(self, subject_node, env):
        return ExprNodes.BoolNode(self.pos, value=True)

    def generate_main_pattern_assignment_list(self, subject_node, env):
        if self.target:
            return [
                Nodes.SingleAssignmentNode(
                    self.pos, lhs=self.target.clone_node(), rhs=subject_node
                )
            ]
        else:
            return []

    def analyse_pattern_expressions(self, subject_node, env, sequence_mapping_temp):
        if self.is_star and False:
            # TODO investigate?
            return super(MatchAndAssignPatternNode, self).analyse_pattern_expressions(
                subject_node, env
            )
        else:
            self.comp_node = self.get_comparison_node(
                subject_node, env
            ).analyse_expressions(env)

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

    def get_comparison_node(self, subject_node, env, sequence_mapping_temp):
        error(self.pos, "'or' cases aren't fully implemented yet")
        return ExprNodes.BoolNode(self.pos, value=False)

    def analyse_declarations(self, env):
        super(OrPatternNode, self).analyse_declarations(env)
        for a in self.alternatives:
            a.analyse_declarations(env)

    def analyse_pattern_expressions(self, subject_node, env, sequence_mapping_temp):
        self.alternatives = [
            a.analyse_pattern_expressions(subject_node, env, None) for a in self.alternatives
        ]
        self.comp_node = self.get_comparison_node(
            subject_node, env
        ).analyse_temp_boolean_expression(env)
        return self

    def generate_main_pattern_assignment_list(self, subject_node, env):
        assignments = []
        for a in self.alternatives:
            a_assignment = a.generate_target_assignments(subject_node, env)
            if a_assignment:
                # Switch code paths depending on which node gets assigned
                error(self.pos, "Need to handle assignments in or nodes correctly")
                assignments.append(a_assignment)
        return assignments


class MatchSequencePatternNode(PatternNode):
    """
    patterns   list of PatternNodes

    generated: 
    subjects    [TrackTypeTempNode]  individual subsubjects can be assigned to these
    """
    subjects = None
    needs_length_temp = False

    initial_child_attrs = PatternNode.initial_child_attrs + ["patterns"]

    Pyx_sequence_check_type = PyrexTypes.CFuncType(
        PyrexTypes.c_bint_type, [
            PyrexTypes.CFuncTypeArg("o", PyrexTypes.py_object_type, None),
            PyrexTypes.CFuncTypeArg("sequence_mapping_temp", PyrexTypes.c_ptr_type(PyrexTypes.c_uint_type), None)
        ],
        exception_value="-1")

    def __init__(self, pos, **kwds):
        super(MatchSequencePatternNode, self).__init__(pos, **kwds)
        self.length_temp = AssignableTempNode(self.pos, PyrexTypes.c_py_ssize_t_type)

    def get_main_pattern_targets(self):
        targets = set()
        star_count = 0
        for p in self.patterns:
            if isinstance(p, MatchAndAssignPatternNode) and p.is_star:
                star_count += 1
            self.update_targets_with_targets(targets, p.get_targets())
        if star_count > 1:
            error(self.pos,  "multiple starred names in sequence pattern")
        return targets

    def get_comparison_node(self, subject_node, env, sequence_mapping_temp=None):
        from .UtilNodes import TempResultFromStatNode, ResultRefNode

        test = None
        assert getattr(self, "subject_temps", None) is not None
        for n, pattern in enumerate(self.patterns):
            p_test = pattern.get_comparison_node(self.subject_temps[n], env)
            if test is not None:
                p_test = ExprNodes.BoolBinopNode(self.pos,
                    operator = "and",
                    operand1 = test,
                    operand2 = p_test
                )
            if not pattern.get_targets() and pattern.is_irrefutable():
                test = p_test
                # the subject isn't actually needed, don't evaluate it
                self.subject_temps[n] = None
                continue  
                
            result_ref = ResultRefNode(pos=self.pos, type=PyrexTypes.c_bint_type)
            subject_assignment = Nodes.SingleAssignmentNode(
                self.pos,
                lhs = self.subject_temps[n],  # the temp node
                rhs = self.subjects[n]  # the regular node
            )
            test_assignment = Nodes.SingleAssignmentNode(
                self.pos,
                lhs = result_ref,
                rhs = p_test
            )
            stats = Nodes.StatListNode(
                self.pos,
                stats = [ subject_assignment, test_assignment ]
            )
            test = TempResultFromStatNode(result_ref, stats)

        seq_test = self.make_sequence_check(subject_node, sequence_mapping_temp)
        if isinstance(seq_test, ExprNodes.BoolNode) and not seq_test.value:
            return seq_test  # no point in proceeding further!
        has_star = False
        for pattern in self.patterns:
            if isinstance(pattern, MatchAndAssignPatternNode) and pattern.is_star:
                has_star = True
                self.needs_length_temp = True
                break
        len_test = len(self.patterns)
        if has_star:
            len_test -= 1
        # check whether we need a length call...
        if not (self.patterns and len(self.patterns) == 1 and has_star):
            length_call = self.make_length_call_node(subject_node)

            if (length_call.is_literal and 
                    ((has_star and len_test < length_call.constant_result) or
                    (not has_star and len_test != length_call.constant_result))):
                # definitely failed!
                return ExprNodes.BoolNode(self.pos, value=False)
            seq_len_test = ExprNodes.BoolBinopNode(
                self.pos,
                operator = "and",
                operand1 = seq_test,
                operand2 = ExprNodes.PrimaryCmpNode(
                    self.pos,
                    operator = ">=" if has_star else "==",
                    operand1 = length_call,
                    operand2 = ExprNodes.IntNode(
                        self.pos,
                        value = str(len_test)
                    ),
                )
            )
        else:
            self.needs_length_temp = False
            seq_len_test = seq_test
        if test is None:
            test = seq_len_test
        else:
            test = ExprNodes.BoolBinopNode(
                self.pos,
                operator = "and",
                operand1 = seq_len_test,
                operand2 = test
            )            
        return test

    def generate_subjects(self, subject_node, env):
        assert self.subjects is None  # not called twice

        star_idx = None
        for n, pattern in enumerate(self.patterns):
            if isinstance(pattern, MatchAndAssignPatternNode) and pattern.is_star:
                star_idx = n
        if star_idx is None:
            idxs = list(range(len(self.patterns)))
        else:
            fwd_idxs = list(range(star_idx))
            backward_idxs = list(range(star_idx-len(self.patterns)+1, 0))
            star_idx = (
                fwd_idxs[-1]+1 if fwd_idxs else None,
                backward_idxs[0] if backward_idxs else None
            )
            idxs = fwd_idxs + [star_idx] + backward_idxs
            
        subjects = []
        for pattern, idx in zip(self.patterns, idxs):
            indexer = self.make_indexing_node(pattern, subject_node, idx, env)
            subjects.append(ExprNodes.ProxyNode(indexer) if indexer else None)
        self.subjects = subjects
        self.subject_temps = [ TrackTypeTempNode(self.pos, s) for s in self.subjects ]

    def generate_main_pattern_assignment_list(self, subject_node, env):
        assignments = []
        self.generate_subjects(subject_node, env)
        for subject, pattern in zip(self.subject_temps, self.patterns):
            p_assignments = pattern.generate_target_assignments(subject, env)
            if p_assignments:
                assignments.extend(p_assignments.stats)
        return assignments

    def make_sequence_check(self, subject_node, sequence_mapping_temp):
        # Note: the sequence check code is very quick on Python 3.10+
        # but potentially quite slow on lower versions (although should
        # be medium quick for common types). It'd be nice to cache the
        # results of it where it's been called on the same object
        # multiple times.
        # DW has decided that that's too complicated to implement 
        # for now.
        utility_code = UtilityCode.load_cached(
            "IsSequence",
            "MatchCase.c"
        )
        if sequence_mapping_temp is not None:
            sequence_mapping_temp = ExprNodes.AmpersandNode(
                self.pos, operand=sequence_mapping_temp
            )
        else:
            sequence_mapping_temp = ExprNodes.NullNode(self.pos)
        call = ExprNodes.PythonCapiCallNode(
            self.pos, "__Pyx_MatchCase_IsSequence", self.Pyx_sequence_check_type,
            utility_code= utility_code, args=[subject_node, sequence_mapping_temp]
        )
        def type_check(type):
            # type-check need not be perfect, it's an optimization
            if type in [ Builtin.list_type, Builtin.tuple_type ]:
                return True
            if type.is_memoryviewslice or type.is_ctuple:
                return True
            if type in [ Builtin.str_type, Builtin.bytes_type,
                         Builtin.unicode_type, Builtin.bytearray_type,
                         Builtin.dict_type, Builtin.set_type ]:
                # non-exhaustive list at this stage, but returning "False" is
                # an optimization so it's allowed to be non-exchaustive
                return False
            if type.is_numeric or type.is_struct or type.is_enum:
                # again, not exhaustive
                return False
            return None
        return StaticTypeCheckNode(
            self.pos,
            arg = subject_node,
            fallback = call,
            check = type_check
        )

    def make_length_call_node(self, subject_node):
        len_entry = Builtin.builtin_scope.lookup("len")
        if subject_node.type.is_memoryviewslice:
            len_call = ExprNodes.IndexNode(
                self.pos,
                base = ExprNodes.AttributeNode(
                    self.pos,
                    obj = subject_node,
                    attribute = "shape"
                ),
                index = ExprNodes.IntNode(
                    self.pos,
                    value = "0"
                )
            )
        elif subject_node.type.is_ctuple:
            len_call = ExprNodes.IntNode(
                self.pos,
                value = str(len(subject_node.type.components))
            )
        else:
            len_call = ExprNodes.SimpleCallNode(
                self.pos,
                function = ExprNodes.NameNode(self.pos, name="len", entry=len_entry),
                args = [ subject_node ]
            )
        if self.needs_length_temp:
            return ExprNodes.AssignmentExpressionNode(
                self.pos,
                lhs = self.length_temp,
                rhs = len_call
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
                int_node = ExprNodes.IntNode(pattern.pos, value = str(i))
                if i >= 0:
                    return int_node
                else:
                    self.needs_length_temp = True
                    return ExprNodes.binop_node(
                        pattern.pos,
                        operator="+",
                        operand1=self.length_temp,
                        operand2=int_node)

        if isinstance(idx, tuple):
            start = get_index_from_int(idx[0])
            stop = get_index_from_int(idx[1])
            indexer = ExprNodes.MergedSequenceNode(
                pattern.pos,
                args = [ExprNodes.SliceIndexNode(
                    pattern.pos,
                    base = subject_node,
                    start = start,
                    stop = stop
                )],
                type = Builtin.list_type
            )
        else:
            indexer = ExprNodes.IndexNode(
                pattern.pos,
                base = subject_node,
                index = get_index_from_int(idx),
                force_boundscheck_off = True,
                force_wraparound_off = True,
            )

        return indexer

    def analyse_declarations(self, env):
        for p in self.patterns:
            p.analyse_declarations(env)
        return super(MatchSequencePatternNode, self).analyse_declarations(env)

    def analyse_pattern_expressions(self, subject_node, env, sequence_mapping_temp):
        for n in range(len(self.subjects)):
            if self.subjects[n]:
                self.subjects[n] = self.subjects[n].analyse_types(env)
        for n in range(len(self.patterns)):
            self.patterns[n] = self.patterns[n].analyse_pattern_expressions(
                self.subject_temps[n], env, None
            )
        self.comp_node = self.get_comparison_node(
            subject_node, env, sequence_mapping_temp)
        if not self.comp_node.is_literal:
            self.comp_node = self.comp_node.analyse_temp_boolean_expression(env)
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


class StaticTypeCheckNode(ExprNodes.ExprNode):
    """
    Useful for structural pattern matching, where we
    can skip the "is_seqeunce/is_mapping" checks if
    we know the type in advantage (or reduce it to a
    None check).

    This should optimize itself out at the analyse_expressions
    stage

    arg        ExprNode
    fallback   ExprNode   Function to be called if the static 
                            typecheck isn't optimized out
    check      callable   Returns True, False, or None (for "can't tell")
    """
    child_attrs = ['fallback']  # arg in not included since it's in "fallback"

    def analyse_types(self, env):
        check = self.check(self.arg.type)
        if check:
            if self.arg.may_be_none():
                return ExprNodes.PrimaryCmpNode(
                    self.pos,
                    operand1 = self.arg,
                    operand2 = ExprNodes.NoneNode(self.pos),
                    operator = "is_not"
                ).analyse_expressions(env)
            else:
                return ExprNodes.BoolNode(
                    pos = self.pos,
                    value = True
                ).analyse_expressions(env)
        elif check is None:
            return self.fallback.analyse_expressions(env)
        else:
            return ExprNodes.BoolNode(
                pos = self.pos,
                value = False
            ).analyse_expressions(env)


class AssignableTempNode(ExprNodes.TempNode):
    lhs_of_first_assignment = True  # assume it can be assigned to once
    _assigned_twice = False

    def infer_type(self, env):
        return self.type 

    def generate_assignment_code(self, rhs, code, overloaded_assignment=False):
        assert not self._assigned_twice  # if this happens it's not a disaster but it needs a refactor
        self._assigned_twice = True
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
    
    def generate_post_assignment_code(self, code):
        code.put_incref(self.result(), self.type)


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


