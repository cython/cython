from Cython.Compiler.Visitor import VisitorTransform, temp_name_handle, CythonTransform
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.TreeFragment import TreeFragment
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Errors import CompileError
try:
    set
except NameError:
    from sets import Set as set
import copy

class NormalizeTree(CythonTransform):
    """
    This transform fixes up a few things after parsing
    in order to make the parse tree more suitable for
    transforms.

    a) After parsing, blocks with only one statement will
    be represented by that statement, not by a StatListNode.
    When doing transforms this is annoying and inconsistent,
    as one cannot in general remove a statement in a consistent
    way and so on. This transform wraps any single statements
    in a StatListNode containing a single statement.

    b) The PassStatNode is a noop and serves no purpose beyond
    plugging such one-statement blocks; i.e., once parsed a
`    "pass" can just as well be represented using an empty
    StatListNode. This means less special cases to worry about
    in subsequent transforms (one always checks to see if a
    StatListNode has no children to see if the block is empty).
    """

    def __init__(self, context):
        super(NormalizeTree, self).__init__(context)
        self.is_in_statlist = False
        self.is_in_expr = False

    def visit_ExprNode(self, node):
        stacktmp = self.is_in_expr
        self.is_in_expr = True
        self.visitchildren(node)
        self.is_in_expr = stacktmp
        return node

    def visit_StatNode(self, node, is_listcontainer=False):
        stacktmp = self.is_in_statlist
        self.is_in_statlist = is_listcontainer
        self.visitchildren(node)
        self.is_in_statlist = stacktmp
        if not self.is_in_statlist and not self.is_in_expr:
            return StatListNode(pos=node.pos, stats=[node])
        else:
            return node

    def visit_StatListNode(self, node):
        self.is_in_statlist = True
        self.visitchildren(node)
        self.is_in_statlist = False
        return node

    def visit_ParallelAssignmentNode(self, node):
        return self.visit_StatNode(node, True)
    
    def visit_CEnumDefNode(self, node):
        return self.visit_StatNode(node, True)

    def visit_CStructOrUnionDefNode(self, node):
        return self.visit_StatNode(node, True)

    # Eliminate PassStatNode
    def visit_PassStatNode(self, node):
        if not self.is_in_statlist:
            return StatListNode(pos=node.pos, stats=[])
        else:
            return []


class PostParseError(CompileError): pass

# error strings checked by unit tests, so define them
ERR_CDEF_INCLASS = 'Cannot assign default value to cdef class attributes'
ERR_BUF_LOCALONLY = 'Buffer types only allowed as function local variables'
ERR_BUF_DEFAULTS = 'Invalid buffer defaults specification (see docs)'
ERR_INVALID_SPECIALATTR_TYPE = 'Special attributes must not have a type declared'
class PostParse(CythonTransform):
    """
    Basic interpretation of the parse tree, as well as validity
    checking that can be done on a very basic level on the parse
    tree (while still not being a problem with the basic syntax,
    as such).

    Specifically:
    - Default values to cdef assignments are turned into single
    assignments following the declaration (everywhere but in class
    bodies, where they raise a compile error)
    
    - Interpret some node structures into Python runtime values.
    Some nodes take compile-time arguments (currently:
    CBufferAccessTypeNode[args] and __cythonbufferdefaults__ = {args}),
    which should be interpreted. This happens in a general way
    and other steps should be taken to ensure validity.

    Type arguments cannot be interpreted in this way.

    - For __cythonbufferdefaults__ the arguments are checked for
    validity.

    CBufferAccessTypeNode has its options interpreted:
    Any first positional argument goes into the "dtype" attribute,
    any "ndim" keyword argument goes into the "ndim" attribute and
    so on. Also it is checked that the option combination is valid.
    - __cythonbufferdefaults__ attributes are parsed and put into the
    type information.

    Note: Currently Parsing.py does a lot of interpretation and
    reorganization that can be refactored into this transform
    if a more pure Abstract Syntax Tree is wanted.
    """

    # Track our context.
    scope_type = None # can be either of 'module', 'function', 'class'

    def __init__(self, context):
        super(PostParse, self).__init__(context)
        self.specialattribute_handlers = {
            '__cythonbufferdefaults__' : self.handle_bufferdefaults
        }

    def visit_ModuleNode(self, node):
        self.scope_type = 'module'
        self.visitchildren(node)
        return node
    
    def visit_ClassDefNode(self, node):
        prev = self.scope_type
        self.scope_type = 'class'
        self.classnode = node
        self.visitchildren(node)
        self.scope_type = prev
        del self.classnode
        return node

    def visit_FuncDefNode(self, node):
        prev = self.scope_type
        self.scope_type = 'function'
        self.visitchildren(node)
        self.scope_type = prev
        return node

    # cdef variables
    def handle_bufferdefaults(self, decl):
        if not isinstance(decl.default, DictNode):
            raise PostParseError(decl.pos, ERR_BUF_DEFAULTS)
        self.classnode.buffer_defaults_node = decl.default
        self.classnode.buffer_defaults_pos = decl.pos

    def visit_CVarDefNode(self, node):
        # This assumes only plain names and pointers are assignable on
        # declaration. Also, it makes use of the fact that a cdef decl
        # must appear before the first use, so we don't have to deal with
        # "i = 3; cdef int i = i" and can simply move the nodes around.
        try:
            self.visitchildren(node)
            stats = [node]
            newdecls = []
            for decl in node.declarators:
                declbase = decl
                while isinstance(declbase, CPtrDeclaratorNode):
                    declbase = declbase.base
                if isinstance(declbase, CNameDeclaratorNode):
                    if declbase.default is not None:
                        if self.scope_type == 'class':
                            if isinstance(self.classnode, CClassDefNode):
                                handler = self.specialattribute_handlers.get(decl.name)
                                if handler:
                                    if decl is not declbase:
                                        raise PostParseError(decl.pos, ERR_INVALID_SPECIALATTR_TYPE)
                                    handler(decl)
                                    continue # Remove declaration
                            raise PostParseError(decl.pos, ERR_CDEF_INCLASS)
                        stats.append(SingleAssignmentNode(node.pos,
                            lhs=NameNode(node.pos, name=declbase.name),
                            rhs=declbase.default, first=True))
                        declbase.default = None
                newdecls.append(decl)
            node.declarators = newdecls
            return stats
        except PostParseError, e:
            # An error in a cdef clause is ok, simply remove the declaration
            # and try to move on to report more errors
            self.context.nonfatal_error(e)
            return None

    def visit_CBufferAccessTypeNode(self, node):
        if not self.scope_type == 'function':
            raise PostParseError(node.pos, ERR_BUF_LOCALONLY)
        return node

class PxdPostParse(CythonTransform):
    """
    Basic interpretation/validity checking that should only be
    done on pxd trees.

    A lot of this checking currently happens in the parser; but
    what is listed below happens here.

    - "def" functions are let through only if they fill the
    getbuffer/releasebuffer slots
    """
    ERR_FUNCDEF_NOT_ALLOWED = 'function definition not allowed here'

    def __call__(self, node):
        self.scope_type = 'pxd'
        return super(PxdPostParse, self).__call__(node)

    def visit_CClassDefNode(self, node):
        old = self.scope_type
        self.scope_type = 'cclass'
        self.visitchildren(node)
        self.scope_type = old
        return node

    def visit_FuncDefNode(self, node):
        # FuncDefNode always come with an implementation (without
        # an imp they are CVarDefNodes..)
        ok = False

        if (isinstance(node, DefNode) and self.scope_type == 'cclass'
            and node.name in ('__getbuffer__', '__releasebuffer__')):
            ok = True

        if not ok:
            self.context.nonfatal_error(PostParseError(node.pos,
                self.ERR_FUNCDEF_NOT_ALLOWED))
            return None
        else:
            return node

class ResolveOptions(CythonTransform):
    """
    After parsing, options can be stored in a number of places:
    - #cython-comments at the top of the file (stored in ModuleNode)
    - Command-line arguments overriding these
    - @cython.optionname decorators
    - with cython.optionname: statements

    This transform is responsible for annotating each node with an
    "options" attribute linking it to a dict containing the exact
    options that are in effect for that node. Any corresponding decorators
    or with statements are removed in the process.

    Note that we have to run this prior to analysis, and so some minor
    duplication of functionality has to occur: We manually track cimports
    to correctly intercept @cython... and with cython...
    """

    def __init__(self, context, compilation_option_overrides):
        super(ResolveOptions, self).__init__(context)
        self.compilation_option_overrides = compilation_option_overrides
        self.cython_module_names = set()
        self.option_names = {}

    def visit_ModuleNode(self, node):
        options = copy.copy(Options.option_defaults)
        options.update(node.option_comments)
        options.update(self.compilation_option_overrides)
        self.options = options
        node.options = options
        self.visitchildren(node)
        return node

    # Track cimports of the cython module.
    def visit_CImportStatNode(self, node):
        if node.module_name == u"cython":
            if node.as_name:
                modname = node.as_name
            else:
                modname = u"cython"
            self.cython_module_names.add(modname)
        return node
    
    def visit_FromCImportStatNode(self, node):
        if node.module_name == u"cython":
            newimp = []
            for pos, name, as_name, kind in node.imported_names:
                if name in Options.option_types:
                    self.option_names[as_name] = name
                    if kind is not None:
                        self.context.nonfatal_error(PostParseError(pos,
                            "Compiler option imports must be plain imports"))
                    return None
                else:
                    newimp.append((pos, name, as_name, kind))
            node.imported_names = newimpo
        return node

    def visit_Node(self, node):
        node.options = self.options
        self.visitchildren(node)
        return node

    def try_to_parse_option(self, node):
        # If node is the contents of an option (in a with statement or
        # decorator), returns (optionname, value).
        # Otherwise, returns None
        optname = None
        if isinstance(node, SimpleCallNode):
            if (isinstance(node.function, AttributeNode) and
                  isinstance(node.function.obj, NameNode) and
                  node.function.obj.name in self.cython_module_names):
                optname = node.function.attribute
            elif (isinstance(node.function, NameNode) and
                  node.function.name in self.option_names):
                optname = self.option_names[node.function.name]

        if optname:
            optiontype = Options.option_types.get(optname)
            if optiontype:
                args = node.args
                if optiontype is bool:
                    if len(args) != 1 or not isinstance(args[0], BoolNode):
                        raise PostParseError(dec.function.pos,
                            'The %s option takes one compile-time boolean argument' % optname)
                    return (optname, args[0].value)
                else:
                    assert False

        return None

    def visit_with_options(self, node, options):
        oldoptions = self.options
        newoptions = copy.copy(oldoptions)
        newoptions.update(options)
        self.options = newoptions
        node = self.visit_Node(node)
        self.options = oldoptions
        return node  
 
    # Handle decorators
    def visit_DefNode(self, node):
        options = []
        
        if node.decorators:
            # Split the decorators into two lists -- real decorators and options
            realdecs = []
            for dec in node.decorators:
                option = self.try_to_parse_option(dec.decorator)
                if option is not None:
                    options.append(option)
                else:
                    realdecs.append(dec)
            node.decorators = realdecs

        if options:
            optdict = {}
            options.reverse() # Decorators coming first take precedence
            for option in options:
                name, value = option
                optdict[name] = value
            return self.visit_with_options(node, optdict)
        else:
            return self.visit_Node(node)
                                   
    # Handle with statements
    def visit_WithStatNode(self, node):
        option = self.try_to_parse_option(node.manager)
        if option is not None:
            if node.target is not None:
                raise PostParseError(node.pos, "Compiler option with statements cannot contain 'as'")
            name, value = option
            self.visit_with_options(node.body, {name:value})
            return node.body.stats
        else:
            return self.visit_Node(node)

class WithTransform(CythonTransform):

    # EXCINFO is manually set to a variable that contains
    # the exc_info() tuple that can be generated by the enclosing except
    # statement.
    template_without_target = TreeFragment(u"""
        MGR = EXPR
        EXIT = MGR.__exit__
        MGR.__enter__()
        EXC = True
        try:
            try:
                BODY
            except:
                EXC = False
                if not EXIT(*EXCINFO):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
    """, temps=[u'MGR', u'EXC', u"EXIT", u"SYS)"],
    pipeline=[NormalizeTree(None)])

    template_with_target = TreeFragment(u"""
        MGR = EXPR
        EXIT = MGR.__exit__
        VALUE = MGR.__enter__()
        EXC = True
        try:
            try:
                TARGET = VALUE
                BODY
            except:
                EXC = False
                if not EXIT(*EXCINFO):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
    """, temps=[u'MGR', u'EXC', u"EXIT", u"VALUE", u"SYS"],
    pipeline=[NormalizeTree(None)])

    def visit_WithStatNode(self, node):
        excinfo_name = temp_name_handle('EXCINFO')
        excinfo_namenode = NameNode(pos=node.pos, name=excinfo_name)
        excinfo_target = NameNode(pos=node.pos, name=excinfo_name)
        if node.target is not None:
            result = self.template_with_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                u'TARGET' : node.target,
                u'EXCINFO' : excinfo_namenode
                }, pos = node.pos)
            # Set except excinfo target to EXCINFO
            result.stats[4].body.stats[0].except_clauses[0].excinfo_target = excinfo_target
        else:
            result = self.template_without_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                u'EXCINFO' : excinfo_namenode
                }, pos = node.pos)
            # Set except excinfo target to EXCINFO
            result.stats[4].body.stats[0].except_clauses[0].excinfo_target = excinfo_target
        
        return result.stats

class DecoratorTransform(CythonTransform):

    def visit_DefNode(self, func_node):
        if not func_node.decorators:
            return func_node

        decorator_result = NameNode(func_node.pos, name = func_node.name)
        for decorator in func_node.decorators[::-1]:
            decorator_result = SimpleCallNode(
                decorator.pos,
                function = decorator.decorator,
                args = [decorator_result])

        func_name_node = NameNode(func_node.pos, name = func_node.name)
        reassignment = SingleAssignmentNode(
            func_node.pos,
            lhs = func_name_node,
            rhs = decorator_result)
        return [func_node, reassignment]

class AnalyseDeclarationsTransform(CythonTransform):

    basic_property = TreeFragment(u"""
property NAME:
    def __get__(self):
        return ATTR
    def __set__(self, value):
        ATTR = value
    """, level='c_class')

    def __call__(self, root):
        self.env_stack = [root.scope]
        return super(AnalyseDeclarationsTransform, self).__call__(root)        
    
    def visit_ModuleNode(self, node):
        node.analyse_declarations(self.env_stack[-1])
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        lenv = node.create_local_scope(self.env_stack[-1])
        node.body.analyse_control_flow(lenv) # this will be totally refactored
        node.declare_arguments(lenv)
        node.body.analyse_declarations(lenv)
        self.env_stack.append(lenv)
        self.visitchildren(node)
        self.env_stack.pop()
        return node
        
    # Some nodes are no longer needed after declaration
    # analysis and can be dropped. The analysis was performed
    # on these nodes in a seperate recursive process from the
    # enclosing function or module, so we can simply drop them.
    def visit_CVarDefNode(self, node):
        if node.need_properties:
            # cdef public attributes may need type testing on 
            # assignment, so we create a property accesss
            # mechanism for them. 
            stats = []
            for entry in node.need_properties:
                property = self.create_Property(entry)
                property.analyse_declarations(node.dest_scope)
                self.visit(property)
                stats.append(property)
            return StatListNode(pos=node.pos, stats=stats)
        else:
            return None
            
    def create_Property(self, entry):
        property = self.basic_property.substitute({
                u"ATTR": AttributeNode(pos=entry.pos,
                                       obj=NameNode(pos=entry.pos, name="self"), 
                                       attribute=entry.name),
            }, pos=entry.pos).stats[0]
        property.name = entry.name
        return property

class AnalyseExpressionsTransform(CythonTransform):
    def visit_ModuleNode(self, node):
        node.body.analyse_expressions(node.scope)
        self.visitchildren(node)
        return node
        
    def visit_FuncDefNode(self, node):
        node.body.analyse_expressions(node.local_scope)
        self.visitchildren(node)
        return node

class MarkClosureVisitor(CythonTransform):
    
    needs_closure = False
    
    def visit_FuncDefNode(self, node):
        self.needs_closure = False
        self.visitchildren(node)
        node.needs_closure = self.needs_closure
        self.needs_closure = True
        return node
        
    def visit_ClassDefNode(self, node):
        self.visitchildren(node)
        self.needs_closure = True
        return node
        
    def visit_YieldNode(self, node):
        self.needs_closure = True
        
class CreateClosureClasses(CythonTransform):
    # Output closure classes in module scope for all functions
    # that need it. 
    
    def visit_ModuleNode(self, node):
        self.module_scope = node.scope
        self.visitchildren(node)
        return node

    def create_class_from_scope(self, node, target_module_scope):
        as_name = temp_name_handle("closure")
        func_scope = node.local_scope

        entry = target_module_scope.declare_c_class(name = as_name,
            pos = node.pos, defining = True, implementing = True)
        class_scope = entry.type.scope
        for entry in func_scope.entries.values():
            class_scope.declare_var(pos=node.pos,
                                    name=entry.name,
                                    cname=entry.cname,
                                    type=entry.type,
                                    is_cdef=True)
            
    def visit_FuncDefNode(self, node):
        self.create_class_from_scope(node, self.module_scope)
        return node
        

