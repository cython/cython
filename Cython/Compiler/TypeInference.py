from Errors import error, warning, message, warn_once, InternalError
import ExprNodes
import Nodes
import Builtin
import PyrexTypes
from Cython import Utils
from PyrexTypes import py_object_type, unspecified_type
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
        if isinstance(lhs, (ExprNodes.NameNode, Nodes.PyArgDeclNode)):
            if lhs.entry is None:
                # TODO: This shouldn't happen...
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
        is_special = False
        sequence = node.iterator.sequence
        if isinstance(sequence, ExprNodes.SimpleCallNode):
            function = sequence.function
            if sequence.self is None and function.is_name:
                if function.name in ('range', 'xrange'):
                    is_special = True
                    for arg in sequence.args[:2]:
                        self.mark_assignment(node.target, arg)
                    if len(sequence.args) > 2:
                        self.mark_assignment(
                            node.target,
                            ExprNodes.binop_node(node.pos,
                                                 '+',
                                                 sequence.args[0],
                                                 sequence.args[2]))
        if not is_special:
            # A for-loop basically translates to subsequent calls to
            # __getitem__(), so using an IndexNode here allows us to
            # naturally infer the base type of pointers, C arrays,
            # Python strings, etc., while correctly falling back to an
            # object type when the base type cannot be handled.
            self.mark_assignment(node.target, ExprNodes.IndexNode(
                node.pos,
                base = sequence,
                index = ExprNodes.IntNode(node.pos, value = '0')))
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

    def visit_DefNode(self, node):
        # use fake expressions with the right result type
        if node.star_arg:
            self.mark_assignment(
                node.star_arg, TypedExprNode(Builtin.tuple_type))
        if node.starstar_arg:
            self.mark_assignment(
                node.starstar_arg, TypedExprNode(Builtin.dict_type))
        self.visitchildren(node)
        return node

class MarkOverflowingArithmetic(CythonTransform):

    # It may be possible to integrate this with the above for
    # performance improvements (though likely not worth it).

    might_overflow = False

    def __call__(self, root):
        self.env_stack = []
        self.env = root.scope
        return super(MarkOverflowingArithmetic, self).__call__(root)

    def visit_safe_node(self, node):
        self.might_overflow, saved = False, self.might_overflow
        self.visitchildren(node)
        self.might_overflow = saved
        return node

    def visit_neutral_node(self, node):
        self.visitchildren(node)
        return node

    def visit_dangerous_node(self, node):
        self.might_overflow, saved = True, self.might_overflow
        self.visitchildren(node)
        self.might_overflow = saved
        return node

    def visit_FuncDefNode(self, node):
        self.env_stack.append(self.env)
        self.env = node.local_scope
        self.visit_safe_node(node)
        self.env = self.env_stack.pop()
        return node

    def visit_NameNode(self, node):
        if self.might_overflow:
            entry = node.entry or self.env.lookup(node.name)
            if entry:
                entry.might_overflow = True
        return node

    def visit_BinopNode(self, node):
        if node.operator in '&|^':
            return self.visit_neutral_node(node)
        else:
            return self.visit_dangerous_node(node)

    visit_UnopNode = visit_neutral_node

    visit_UnaryMinusNode = visit_dangerous_node

    visit_InPlaceAssignmentNode = visit_dangerous_node

    visit_Node = visit_safe_node

    def visit_assignment(self, lhs, rhs):
        if (isinstance(rhs, ExprNodes.IntNode)
                and isinstance(lhs, ExprNodes.NameNode)
                and Utils.long_literal(rhs.value)):
            entry = lhs.entry or self.env.lookup(lhs.name)
            if entry:
                entry.might_overflow = True

    def visit_SingleAssignmentNode(self, node):
        self.visit_assignment(node.lhs, node.rhs)
        self.visitchildren(node)
        return node

    def visit_CascadedAssignmentNode(self, node):
        for lhs in node.lhs_list:
            self.visit_assignment(lhs, node.rhs)
        self.visitchildren(node)
        return node

class PyObjectTypeInferer(object):
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

class SimpleAssignmentTypeInferer(object):
    """
    Very basic type inference.
    """
    # TODO: Implement a real type inference algorithm.
    # (Something more powerful than just extending this one...)
    def infer_types(self, scope):
        enabled = not scope.is_closure_scope and scope.directives['infer_types']
        verbose = scope.directives['infer_types.verbose']
        if enabled == True:
            spanning_type = aggressive_spanning_type
        elif enabled is None: # safe mode
            spanning_type = safe_spanning_type
        else:
            for entry in scope.entries.values():
                if entry.type is unspecified_type:
                    entry.type = py_object_type
            return

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
                    entry.type = spanning_type(types, entry.might_overflow)
                else:
                    # FIXME: raise a warning?
                    # print "No assignments", entry.pos, entry
                    entry.type = py_object_type
                if verbose:
                    message(entry.pos, "inferred '%s' to be of type '%s'" % (entry.name, entry.type))
                resolve_dependancy(entry)
            # Deal with simple circular dependancies...
            for entry, deps in dependancies_by_entry.items():
                if len(deps) == 1 and deps == set([entry]):
                    types = [expr.infer_type(scope) for expr in entry.assignments if expr.type_dependencies(scope) == ()]
                    if types:
                        entry.type = spanning_type(types, entry.might_overflow)
                        types = [expr.infer_type(scope) for expr in entry.assignments]
                        entry.type = spanning_type(types, entry.might_overflow) # might be wider...
                        resolve_dependancy(entry)
                        del dependancies_by_entry[entry]
                        if ready_to_infer:
                            break
            if not ready_to_infer:
                break

        # We can't figure out the rest with this algorithm, let them be objects.
        for entry in dependancies_by_entry:
            entry.type = py_object_type
            if verbose:
                message(entry.pos, "inferred '%s' to be of type '%s' (default)" % (entry.name, entry.type))

def find_spanning_type(type1, type2):
    if type1 is type2:
        result_type = type1
    elif type1 is PyrexTypes.c_bint_type or type2 is PyrexTypes.c_bint_type:
        # type inference can break the coercion back to a Python bool
        # if it returns an arbitrary int type here
        return py_object_type
    else:
        result_type = PyrexTypes.spanning_type(type1, type2)
    if result_type in (PyrexTypes.c_double_type, PyrexTypes.c_float_type,
                       Builtin.float_type):
        # Python's float type is just a C double, so it's safe to
        # use the C type instead
        return PyrexTypes.c_double_type
    return result_type

def aggressive_spanning_type(types, might_overflow):
    result_type = reduce(find_spanning_type, types)
    if result_type.is_reference:
        result_type = result_type.ref_base_type
    return result_type

def safe_spanning_type(types, might_overflow):
    result_type = reduce(find_spanning_type, types)
    if result_type.is_reference:
        result_type = result_type.ref_base_type
    if result_type.is_pyobject:
        # In theory, any specific Python type is always safe to
        # infer. However, inferring str can cause some existing code
        # to break, since we are also now much more strict about
        # coercion from str to char *. See trac #553.
        if result_type.name == 'str':
            return py_object_type
        else:
            return result_type
    elif result_type is PyrexTypes.c_double_type:
        # Python's float type is just a C double, so it's safe to use
        # the C type instead
        return result_type
    elif result_type is PyrexTypes.c_bint_type:
        # find_spanning_type() only returns 'bint' for clean boolean
        # operations without other int types, so this is safe, too
        return result_type
    elif result_type.is_ptr and not (result_type.is_int and result_type.rank == 0):
        # Any pointer except (signed|unsigned|) char* can't implicitly
        # become a PyObject.
        return result_type
    elif result_type.is_cpp_class:
        # These can't implicitly become Python objects either.
        return result_type
    elif result_type.is_struct:
        # Though we have struct -> object for some structs, this is uncommonly
        # used, won't arise in pure Python, and there shouldn't be side
        # effects, so I'm declaring this safe.
        return result_type
    # TODO: double complex should be OK as well, but we need
    # to make sure everything is supported.
    elif result_type.is_int and not might_overflow:
        return result_type
    return py_object_type


def get_type_inferer():
    return SimpleAssignmentTypeInferer()
