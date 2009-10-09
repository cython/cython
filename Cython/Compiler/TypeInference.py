import ExprNodes
from PyrexTypes import py_object_type, unspecified_type, spanning_type
from Visitor import CythonTransform

try:
    set
except NameError:
    # Python 2.3
    from sets import Set as set


class TypedExprNode(ExprNodes.ExprNode):
    # Used for declaring assignments of a specified type whithout a known entry.
    def __init__(self, type):
        self.type = type

object_expr = TypedExprNode(py_object_type)

class MarkAssignments(CythonTransform):
    
    def mark_assignment(self, lhs, rhs):
        if isinstance(lhs, ExprNodes.NameNode):
            if lhs.entry is None:
                # TODO: This shouldn't happen...
                # It looks like comprehension loop targets are not declared soon enough.
                return
            lhs.entry.assignments.append(rhs)
        elif isinstance(lhs, ExprNodes.SequenceNode):
            for arg in lhs.args:
                self.mark_assignment(arg, object_expr)
        else:
            # Could use this info to infer cdef class attributes...
            pass
    
    def visit_SingleAssignmentNode(self, node):
        self.mark_assignment(node.lhs, node.rhs)
        self.visitchildren(node)
        return node

    def visit_CascadedAssignmentNode(self, node):
        for lhs in node.lhs_list:
            self.mark_assignment(lhs, node.rhs)
        self.visitchildren(node)
        return node
    
    def visit_InPlaceAssignmentNode(self, node):
        self.mark_assignment(node.lhs, node.create_binop_node())
        self.visitchildren(node)
        return node

    def visit_ForInStatNode(self, node):
        # TODO: Remove redundancy with range optimization...
        is_range = False
        sequence = node.iterator.sequence
        if isinstance(sequence, ExprNodes.SimpleCallNode):
            function = sequence.function
            if sequence.self is None and \
                    isinstance(function, ExprNodes.NameNode) and \
                    function.name in ('range', 'xrange'):
                is_range = True
                self.mark_assignment(node.target, sequence.args[0])
                if len(sequence.args) > 1:
                    self.mark_assignment(node.target, sequence.args[1])
                    if len(sequence.args) > 2:
                        self.mark_assignment(node.target, 
                                 ExprNodes.binop_node(node.pos,
                                                      '+',
                                                      sequence.args[0],
                                                      sequence.args[2]))
        if not is_range:
            self.mark_assignment(node.target, object_expr)
        self.visitchildren(node)
        return node

    def visit_ForFromStatNode(self, node):
        self.mark_assignment(node.target, node.bound1)
        if node.step is not None:
            self.mark_assignment(node.target,
                    ExprNodes.binop_node(node.pos, 
                                         '+', 
                                         node.bound1, 
                                         node.step))
        self.visitchildren(node)
        return node

    def visit_ExceptClauseNode(self, node):
        if node.target is not None:
            self.mark_assignment(node.target, object_expr)
        self.visitchildren(node)
        return node
    
    def visit_FromCImportStatNode(self, node):
        pass # Can't be assigned to...

    def visit_FromImportStatNode(self, node):
        for name, target in node.items:
            if name != "*":
                self.mark_assignment(target, object_expr)
        self.visitchildren(node)
        return node


class PyObjectTypeInferer:
    """
    If it's not declared, it's a PyObject.
    """
    def infer_types(self, scope):
        """
        Given a dict of entries, map all unspecified types to a specified type.
        """
        for name, entry in scope.entries.items():
            if entry.type is unspecified_type:
                entry.type = py_object_type

class SimpleAssignmentTypeInferer:
    """
    Very basic type inference.
    """
    # TODO: Implement a real type inference algorithm.
    # (Something more powerful than just extending this one...)
    def infer_types(self, scope):
        dependancies_by_entry = {} # entry -> dependancies
        entries_by_dependancy = {} # dependancy -> entries
        ready_to_infer = []
        for name, entry in scope.entries.items():
            if entry.type is unspecified_type:
                all = set()
                for expr in entry.assignments:
                    all.update(expr.type_dependencies(scope))
                if all:
                    dependancies_by_entry[entry] = all
                    for dep in all:
                        if dep not in entries_by_dependancy:
                            entries_by_dependancy[dep] = set([entry])
                        else:
                            entries_by_dependancy[dep].add(entry)
                else:
                    ready_to_infer.append(entry)
        def resolve_dependancy(dep):
            if dep in entries_by_dependancy:
                for entry in entries_by_dependancy[dep]:
                    entry_deps = dependancies_by_entry[entry]
                    entry_deps.remove(dep)
                    if not entry_deps and entry != dep:
                        del dependancies_by_entry[entry]
                        ready_to_infer.append(entry)
        # Try to infer things in order...
        while True:
            while ready_to_infer:
                entry = ready_to_infer.pop()
                types = [expr.infer_type(scope) for expr in entry.assignments]
                if types:
                    entry.type = reduce(spanning_type, types)
                else:
                    # List comprehension?
                    # print "No assignments", entry.pos, entry
                    entry.type = py_object_type
                resolve_dependancy(entry)
            # Deal with simple circular dependancies...
            for entry, deps in dependancies_by_entry.items():
                if len(deps) == 1 and deps == set([entry]):
                    types = [expr.infer_type(scope) for expr in entry.assignments if expr.type_dependencies(scope) == ()]
                    if types:
                        entry.type = reduce(spanning_type, types)
                        types = [expr.infer_type(scope) for expr in entry.assignments]
                        entry.type = reduce(spanning_type, types) # might be wider...
                        resolve_dependancy(entry)
                        del dependancies_by_entry[entry]
                        if ready_to_infer:
                            break
            if not ready_to_infer:
                break
                    
        # We can't figure out the rest with this algorithm, let them be objects.
        for entry in dependancies_by_entry:
            entry.type = py_object_type

def get_type_inferer():
    return SimpleAssignmentTypeInferer()
