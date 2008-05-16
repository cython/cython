#
#   Tree transform framework
#
import Nodes
import ExprNodes
import inspect

class Transform(object):
    # parent_stack [Node]   A stack providing information about where in the tree
    #                       we currently are. Nodes here should be considered
    #                       read-only.
    #
    # attr_stack   [(string,int|None)]
    #                       A stack providing information about the attribute names
    #                       followed to get to the current location in the tree.
    #                       The first tuple item is the attribute name, the second is
    #                       the index if the attribute is a list, or None otherwise.
    #                           
    #
    # Additionally, any keyword arguments to __call__ will be set as fields while in
    # a transformation.

    # Transforms for the parse tree should usually extend this class for convenience.
    # The caller of a transform will only first call initialize and then process_node on
    # the root node, the rest are utility functions and conventions.
    
    # Transformations usually happens by recursively filtering through the stream.
    # process_node is always expected to return a new node, however it is ok to simply
    # return the input node untouched. Returning None will remove the node from the
    # parent.
    
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
                self.attr_stack.append((childacc.name(), None))
                newchild = self.process_node(child)
                if newchild is not None and not isinstance(newchild, Nodes.Node):
                    raise Exception("Cannot replace Node with non-Node!")
                self.attr_stack.pop()
            childacc.set(newchild)
        self.parent_stack.pop()

    def process_list(self, l, attrname):
        """Calls process_node on all the items in l. Each item in l is transformed
        in-place by the item process_node returns, then l is returned. If process_node
        returns None, the item is removed from the list."""
        for idx in xrange(len(l)):
            self.attr_stack.append((attrname, idx))
            l[idx] = self.process_node(l[idx])
            self.attr_stack.pop()
        return [x for x in l if x is not None]

    def process_node(self, node):
        """Override this method to process nodes. name specifies which kind of relation the
        parent has with child. This method should always return the node which the parent
        should use for this relation, which can either be the same node, None to remove
        the node, or a different node."""
        raise NotImplementedError("Not implemented")

    def __call__(self, root, **params):
        self.parent_stack = []
        self.attr_stack = []
        for key, value in params.iteritems():
            setattr(self, key, value)
        root = self.process_node(root)
        for key, value in params.iteritems():
            delattr(self, key)
        del self.parent_stack
        del self.attr_stack
        return root


class VisitorTransform(Transform):

    # Note: If needed, this can be replaced with a more efficient metaclass
    # approach, resolving the jump table at module load time.
    
    def __init__(self, readonly=False, **kw):
        """readonly - If this is set to True, the results of process_node
        will be discarded (so that one can return None without changing
        the tree)."""
        super(VisitorTransform, self).__init__(**kw)
        self.visitmethods = {'process_' : {}, 'pre_' : {}, 'post_' : {}}
        self.attrname = ""
        self.readonly = readonly
     
    def get_visitfunc(self, prefix, cls):
        mname = prefix + cls.__name__
        m = self.visitmethods[prefix].get(mname)
        if m is None:
            # Must resolve, try entire hierarchy
            for cls in inspect.getmro(cls):
                m = getattr(self, prefix + cls.__name__, None)
                if m is not None:
                    break
            if m is None: raise RuntimeError("Not a Node descendant: " + cls.__name__)
            self.visitmethods[prefix][mname] = m
        return m

    def process_node(self, node, name="_"):
        # Pass on to calls registered in self.visitmethods
        self.attrname = name
        if node is None:
            return None
        result = self.get_visitfunc("process_", node.__class__)(node)
        if self.readonly:
            return node
        else:
            return result
    
    def process_Node(self, node):
        descend = self.get_visitfunc("pre_", node.__class__)(node)
        if descend:
            self.process_children(node)
            self.get_visitfunc("post_", node.__class__)(node)
        return node

    def pre_Node(self, node):
        return True

    def post_Node(self, node):
        pass


# Utils
def ensure_statlist(node):
    if not isinstance(node, Nodes.StatListNode):
        node = Nodes.StatListNode(pos=node.pos, stats=[node])
    return node


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

    def __call__(self, tree, phase=None, **params):
        print("Parse tree dump at phase '%s'" % phase)
        super(PrintTree, self).__call__(tree, phase=phase, **params)

    # Don't do anything about process_list, the defaults gives
    # nice-looking name[idx] nodes which will visually appear
    # under the parent-node, not displaying the list itself in
    # the hierarchy.
    
    def process_node(self, node):
        if len(self.attr_stack) == 0:
            name = "(root)"
        else:
            attr, idx = self.attr_stack[-1]
            if idx is not None:
                name = "%s[%d]" % (attr, idx)
            else:
                name = attr
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
            if isinstance(node, ExprNodes.NameNode):
                result += "(type=%s, name=\"%s\")" % (repr(node.type), node.name)
            elif isinstance(node, Nodes.DefNode):
                result += "(name=\"%s\")" % node.name
            elif isinstance(node, ExprNodes.ExprNode):
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
        assert name in self, "Transform phase %s not defined" % name
        for transform in self[name]:
            transform(node, phase=name, **options)


