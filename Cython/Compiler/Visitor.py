#
#   Tree visitor and transform framework
#
import inspect
import Nodes
import ExprNodes
import Naming
from Cython.Utils import EncodedString

class BasicVisitor(object):
    """A generic visitor base class which can be used for visiting any kind of object."""
    # Note: If needed, this can be replaced with a more efficient metaclass
    # approach, resolving the jump table at module load time rather than per visitor
    # instance.
    def __init__(self):
        self.dispatch_table = {}
     
    def visit(self, obj):
        pattern = "visit_%s"
        cls = obj.__class__
        mname = pattern % cls.__name__
        m = self.dispatch_table.get(mname)
        if m is None:
            # Must resolve, try entire hierarchy
            mro = inspect.getmro(cls)
            for cls in mro:
                m = getattr(self, pattern % cls.__name__, None)
                if m is not None:
                    break
            else:
                raise RuntimeError("Visitor does not accept object: %s" % obj)
            self.dispatch_table[mname] = m
        return m(obj)

class TreeVisitor(BasicVisitor):
    """
    Base class for writing visitors for a Cython tree, contains utilities for
    recursing such trees using visitors. Each node is
    expected to have a child_attrs iterable containing the names of attributes
    containing child nodes or lists of child nodes. Lists are not considered
    part of the tree structure (i.e. contained nodes are considered direct
    children of the parent node).
    
    visit_children visits each of the children of a given node (see the visit_children
    documentation). When recursing the tree using visit_children, an attribute
    access_path is maintained which gives information about the current location
    in the tree as a stack of tuples: (parent_node, attrname, index), representing
    the node, attribute and optional list index that was taken in each step in the path to
    the current node.
    
    Example:
    
    >>> class SampleNode:
    ...     child_attrs = ["head", "body"]
    ...     def __init__(self, value, head=None, body=None):
    ...         self.value = value
    ...         self.head = head
    ...         self.body = body
    ...     def __repr__(self): return "SampleNode(%s)" % self.value
    ...
    >>> tree = SampleNode(0, SampleNode(1), [SampleNode(2), SampleNode(3)])
    >>> class MyVisitor(TreeVisitor):
    ...     def visit_SampleNode(self, node):
    ...         print "in", node.value, self.access_path
    ...         self.visitchildren(node)
    ...         print "out", node.value
    ...
    >>> MyVisitor().visit(tree)
    in 0 []
    in 1 [(SampleNode(0), 'head', None)]
    out 1
    in 2 [(SampleNode(0), 'body', 0)]
    out 2
    in 3 [(SampleNode(0), 'body', 1)]
    out 3
    out 0
    """
    
    def __init__(self):
        super(TreeVisitor, self).__init__()
        self.access_path = []

    def visitchild(self, child, parent, attrname, idx):
        self.access_path.append((parent, attrname, idx))
        result = self.visit(child)
        self.access_path.pop()
        return result

    def visitchildren(self, parent, attrs=None):
        """
        Visits the children of the given parent. If parent is None, returns
        immediately (returning None).
        
        The return value is a dictionary giving the results for each
        child (mapping the attribute name to either the return value
        or a list of return values (in the case of multiple children
        in an attribute)).
        """

        if parent is None: return None
        result = {}
        for attr in parent.child_attrs:
            if attrs is not None and attr not in attrs: continue
            child = getattr(parent, attr)
            if child is not None:
                if isinstance(child, list):
                    childretval = [self.visitchild(x, parent, attr, idx) for idx, x in enumerate(child)]
                else:
                    childretval = self.visitchild(child, parent, attr, None)
                result[attr] = childretval
        return result


class VisitorTransform(TreeVisitor):
    """
    A tree transform is a base class for visitors that wants to do stream
    processing of the structure (rather than attributes etc.) of a tree.
    
    It implements __call__ to simply visit the argument node.
    
    It requires the visitor methods to return the nodes which should take
    the place of the visited node in the result tree (which can be the same
    or one or more replacement). Specifically, if the return value from
    a visitor method is:
    
    - [] or None; the visited node will be removed (set to None if an attribute and
    removed if in a list)
    - A single node; the visited node will be replaced by the returned node.
    - A list of nodes; the visited nodes will be replaced by all the nodes in the
    list. This will only work if the node was already a member of a list; if it
    was not, an exception will be raised. (Typically you want to ensure that you
    are within a StatListNode or similar before doing this.)
    """
    def visitchildren(self, parent, attrs=None):
        result = super(VisitorTransform, self).visitchildren(parent, attrs)
        for attr, newnode in result.iteritems():
            if not isinstance(newnode, list):
                setattr(parent, attr, newnode)
            else:
                # Flatten the list one level and remove any None
                newlist = []
                for x in newnode:
                    if x is not None:
                        if isinstance(x, list):
                            newlist += x
                        else:
                            newlist.append(x)
                setattr(parent, attr, newlist)
        return result        
    
    def __call__(self, root):
        return self.visit(root)

class CythonTransform(VisitorTransform):
    """
    Certain common conventions and utilitues for Cython transforms.
    """
    def __init__(self, context):
        super(CythonTransform, self).__init__()
        self.context = context

    def visit_Node(self, node):
        self.visitchildren(node)
        return node


# Utils
def ensure_statlist(node):
    if not isinstance(node, Nodes.StatListNode):
        node = Nodes.StatListNode(pos=node.pos, stats=[node])
    return node

def replace_node(ptr, value):
    """Replaces a node. ptr is of the form used on the access path stack
    (parent, attrname, listidx|None)
    """
    parent, attrname, listidx = ptr
    if listidx is None:
        setattr(parent, attrname, value)
    else:
        getattr(parent, attrname)[listidx] = value

tmpnamectr = 0
def temp_name_handle(description):
    global tmpnamectr
    tmpnamectr += 1
    return EncodedString(Naming.temp_prefix + u"%d_%s" % (tmpnamectr, description))

def get_temp_name_handle_desc(handle):
    if not handle.startswith(u"__cyt_"):
        return None
    else:
        idx = handle.find(u"_", 6)
        return handle[idx+1:]
    
class PrintTree(TreeVisitor):
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

    def __call__(self, tree, phase=None):
        print("Parse tree dump at phase '%s'" % phase)

    # Don't do anything about process_list, the defaults gives
    # nice-looking name[idx] nodes which will visually appear
    # under the parent-node, not displaying the list itself in
    # the hierarchy.
    def visit_Node(self, node):
        if len(self.access_path) == 0:
            name = "(root)"
        else:
            parent, attr, idx = self.access_path[-1]
            if idx is not None:
                name = "%s[%d]" % (attr, idx)
            else:
                name = attr
        print("%s- %s: %s" % (self._indent, name, self.repr_of(node)))
        self.indent()
        self.visitchildren(node)
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()
