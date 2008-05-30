#
# TreeFragments - parsing of strings to trees
#

import re
from cStringIO import StringIO
from Scanning import PyrexScanner, StringSourceDescriptor
from Symtab import BuiltinScope, ModuleScope
from Visitor import VisitorTransform
from Nodes import Node
from ExprNodes import NameNode
import Parsing
import Main

"""
Support for parsing strings into code trees.
"""

class StringParseContext(Main.Context):
    def __init__(self, include_directories, name):
        Main.Context.__init__(self, include_directories)
        self.module_name = name
        
    def find_module(self, module_name, relative_to = None, pos = None, need_pxd = 1):
        if module_name != self.module_name:
            raise AssertionError("Not yet supporting any cimports/includes from string code snippets")
        return ModuleScope(module_name, parent_module = None, context = self)
        
def parse_from_strings(name, code, pxds={}):
    """
    Utility method to parse a (unicode) string of code. This is mostly
    used for internal Cython compiler purposes (creating code snippets
    that transforms should emit, as well as unit testing).
    
    code - a unicode string containing Cython (module-level) code
    name - a descriptive name for the code source (to use in error messages etc.)
    """

    # Since source files carry an encoding, it makes sense in this context
    # to use a unicode string so that code fragments don't have to bother
    # with encoding. This means that test code passed in should not have an
    # encoding header.
    assert isinstance(code, unicode), "unicode code snippets only please"
    encoding = "UTF-8"

    module_name = name
    initial_pos = (name, 1, 0)
    code_source = StringSourceDescriptor(name, code)

    context = StringParseContext([], name)
    scope = context.find_module(module_name, pos = initial_pos, need_pxd = 0)

    buf = StringIO(code.encode(encoding))

    scanner = PyrexScanner(buf, code_source, source_encoding = encoding,
                     type_names = scope.type_names, context = context)
    tree = Parsing.p_module(scanner, 0, module_name)
    return tree

class TreeCopier(VisitorTransform):
    def visit_Node(self, node):
        if node is None:
            return node
        else:
            c = node.clone_node()
            self.visitchildren(c)
            return c

class ApplyPositionAndCopy(TreeCopier):
    def __init__(self, pos):
        super(ApplyPositionAndCopy, self).__init__()
        self.pos = pos
        
    def visit_Node(self, node):
        copy = super(ApplyPositionAndCopy, self).visit_Node(node)
        copy.pos = self.pos
        return copy

class TemplateTransform(VisitorTransform):
    """
    Makes a copy of a template tree while doing substitutions.
    
    A dictionary "substitutions" should be passed in when calling
    the transform; mapping names to replacement nodes. Then replacement
    happens like this:
     - If an ExprStatNode contains a single NameNode, whose name is
       a key in the substitutions dictionary, the ExprStatNode is
       replaced with a copy of the tree given in the dictionary.
       It is the responsibility of the caller that the replacement
       node is a valid statement.
     - If a single NameNode is otherwise encountered, it is replaced
       if its name is listed in the substitutions dictionary in the
       same way. It is the responsibility of the caller to make sure
       that the replacement nodes is a valid expression.
    
    Each replacement node gets the position of the substituted node
    recursively applied to every member node.
    """
    def visit_Node(self, node):
        if node is None:
            return node
        else:
            c = node.clone_node()
            self.visitchildren(c)
            return c
    
    def try_substitution(self, node, key):
        sub = self.substitutions.get(key)
        if sub is None:
            return self.visit_Node(node) # make copy as usual
        else:
            return ApplyPositionAndCopy(node.pos)(sub)
    
    def visit_NameNode(self, node):
        return self.try_substitution(node, node.name)

    def visit_ExprStatNode(self, node):
        # If an expression-as-statement consists of only a replaceable
        # NameNode, we replace the entire statement, not only the NameNode
        if isinstance(node.expr, NameNode):
            return self.try_substitution(node, node.expr.name)
        else:
            return self.visit_Node(node)
    
    def __call__(self, node, substitutions):
        self.substitutions = substitutions
        return super(TemplateTransform, self).__call__(node)

def copy_code_tree(node):
    return TreeCopier()(node)

INDENT_RE = re.compile(ur"^ *")
def strip_common_indent(lines):
    "Strips empty lines and common indentation from the list of strings given in lines"
    lines = [x for x in lines if x.strip() != u""]
    minindent = min(len(INDENT_RE.match(x).group(0)) for x in lines)
    lines = [x[minindent:] for x in lines]
    return lines
    
class TreeFragment(object):
    def __init__(self, code, name, pxds={}):
        if isinstance(code, unicode):
            def fmt(x): return u"\n".join(strip_common_indent(x.split(u"\n"))) 
            
            fmt_code = fmt(code)
            fmt_pxds = {}
            for key, value in pxds.iteritems():
                fmt_pxds[key] = fmt(value)
                
            self.root = parse_from_strings(name, fmt_code, fmt_pxds)
        elif isinstance(code, Node):
            if pxds != {}: raise NotImplementedError()
            self.root = code
        else:
            raise ValueError("Unrecognized code format (accepts unicode and Node)")

    def copy(self):
        return copy_code_tree(self.root)

    def substitute(self, nodes={}):
        return TemplateTransform()(self.root, substitutions = nodes)




