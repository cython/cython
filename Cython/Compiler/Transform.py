#
#   Tree transform framework
#
import Nodes
import ExprNodes

class Transform(object):
    #  parent_stack [Node]       A stack providing information about where in the tree
    #                            we currently are. Nodes here should be considered
    #                            read-only.

    # Transforms for the parse tree should usually extend this class for convenience.
    # The caller of a transform will only first call initialize and then process_node on
    # the root node, the rest are utility functions and conventions.
    
    # Transformations usually happens by recursively filtering through the stream.
    # process_node is always expected to return a new node, however it is ok to simply
    # return the input node untouched. Returning None will remove the node from the
    # parent.
    
    def __init__(self):
        self.parent_stack = []
    
    def initialize(self, phase, **options):
        pass

    def process_children(self, node):
        """For all children of node, either process_list (if isinstance(node, list))
        or process_node (otherwise) is called."""
        if node == None: return
        
        self.parent_stack.append(node)
        for childacc in node.get_child_accessors():
            child = childacc.get()
            if isinstance(child, list):
                newchild = self.process_list(child, childacc.name())
                if not isinstance(newchild, list): raise Exception("Cannot replace list with non-list!")
            else:
                newchild = self.process_node(child, childacc.name())
                if newchild is not None and not isinstance(newchild, Nodes.Node):
                    raise Exception("Cannot replace Node with non-Node!")
            childacc.set(newchild)
        self.parent_stack.pop()

    def process_list(self, l, name):
        """Calls process_node on all the items in l, using the name one gets when appending
        [idx] to the name. Each item in l is transformed in-place by the item process_node
        returns, then l is returned."""
        # Comment: If moving to a copying strategy, it might makes sense to return a
        # new list instead.
        for idx in xrange(len(l)):
            l[idx] = self.process_node(l[idx], "%s[%d]" % (name, idx))
        return l

    def process_node(self, node, name):
        """Override this method to process nodes. name specifies which kind of relation the
        parent has with child. This method should always return the node which the parent
        should use for this relation, which can either be the same node, None to remove
        the node, or a different node."""
        raise NotImplementedError("Not implemented")

class PrintTree(Transform):
    """Prints a representation of the tree to standard output.
    Subclass and override repr_of to provide more information
    about nodes. """
    def __init__(self):
        Transform.__init__(self)
        self._indent = ""

    def indent(self):
        self._indent += "  "
    def unindent(self):
        self._indent = self._indent[:-2]

    def initialize(self, phase, **options):
        print("Parse tree dump at phase '%s'" % phase)

    # Don't do anything about process_list, the defaults gives
    # nice-looking name[idx] nodes which will visually appear
    # under the parent-node, not displaying the list itself in
    # the hierarchy.
    
    def process_node(self, node, name):
        print("%s- %s: %s" % (self._indent, name, self.repr_of(node)))
        self.indent()
        self.process_children(node)
        self.unindent()
        return node

    def repr_of(self, node):
        if node is None:
            return "(none)"
        else:
            result = node.__class__.__name__
            if isinstance(node, ExprNodes.ExprNode):
                t = node.type
                result += "(type=%s)" % repr(t)
            return result


PHASES = [
    'before_analyse_function', # run in FuncDefNode.generate_function_definitions
    'after_analyse_function'   # run in FuncDefNode.generate_function_definitions
]

class TransformSet(dict):
    def __init__(self):
        for name in PHASES:
            self[name] = []
    def run(self, name, node, **options):
        assert name in self
        for transform in self[name]:
            transform.initialize(phase=name, **options)
            transform.process_node(node, "(root)")


