from Cython.Compiler.Visitor import VisitorTransform, CythonTransform, TreeVisitor
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.Nodes import *
from Cython.Compiler.ExprNodes import *
from Cython.Compiler.UtilNodes import *
from Cython.Compiler.TreeFragment import TreeFragment, TemplateTransform
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Errors import CompileError
try:
    set
except NameError:
    from sets import Set as set
import copy


class NameNodeCollector(TreeVisitor):
    """Collect all NameNodes of a (sub-)tree in the ``name_nodes``
    attribute.
    """
    def __init__(self):
        super(NameNodeCollector, self).__init__()
        self.name_nodes = []

    visit_Node = TreeVisitor.visitchildren

    def visit_NameNode(self, node):
        self.name_nodes.append(node)


class SkipDeclarations:
    """
    Variable and function declarations can often have a deep tree structure, 
    and yet most transformations don't need to descend to this depth. 
    
    Declaration nodes are removed after AnalyseDeclarationsTransform, so there 
    is no need to use this for transformations after that point. 
    """
    def visit_CTypeDefNode(self, node):
        return node
    
    def visit_CVarDefNode(self, node):
        return node
    
    def visit_CDeclaratorNode(self, node):
        return node
    
    def visit_CBaseTypeNode(self, node):
        return node
    
    def visit_CEnumDefNode(self, node):
        return node

    def visit_CStructOrUnionDefNode(self, node):
        return node


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

    def visit_CDeclaratorNode(self, node):
        return node    


class PostParseError(CompileError): pass

# error strings checked by unit tests, so define them
ERR_CDEF_INCLASS = 'Cannot assign default value to fields in cdef classes, structs or unions'
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
        self.scope_node = node
        self.visitchildren(node)
        return node

    def visit_scope(self, node, scope_type):
        prev = self.scope_type, self.scope_node
        self.scope_type = scope_type
        self.scope_node = node
        self.visitchildren(node)
        self.scope_type, self.scope_node = prev
        return node
    
    def visit_ClassDefNode(self, node):
        return self.visit_scope(node, 'class')

    def visit_FuncDefNode(self, node):
        return self.visit_scope(node, 'function')

    def visit_CStructOrUnionDefNode(self, node):
        return self.visit_scope(node, 'struct')

    # cdef variables
    def handle_bufferdefaults(self, decl):
        if not isinstance(decl.default, DictNode):
            raise PostParseError(decl.pos, ERR_BUF_DEFAULTS)
        self.scope_node.buffer_defaults_node = decl.default
        self.scope_node.buffer_defaults_pos = decl.pos

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
                        if self.scope_type in ('class', 'struct'):
                            if isinstance(self.scope_node, CClassDefNode):
                                handler = self.specialattribute_handlers.get(decl.name)
                                if handler:
                                    if decl is not declbase:
                                        raise PostParseError(decl.pos, ERR_INVALID_SPECIALATTR_TYPE)
                                    handler(decl)
                                    continue # Remove declaration
                            raise PostParseError(decl.pos, ERR_CDEF_INCLASS)
                        first_assignment = self.scope_type != 'module'
                        stats.append(SingleAssignmentNode(node.pos,
                            lhs=NameNode(node.pos, name=declbase.name),
                            rhs=declbase.default, first=first_assignment))
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

class PxdPostParse(CythonTransform, SkipDeclarations):
    """
    Basic interpretation/validity checking that should only be
    done on pxd trees.

    A lot of this checking currently happens in the parser; but
    what is listed below happens here.

    - "def" functions are let through only if they fill the
    getbuffer/releasebuffer slots
    
    - cdef functions are let through only if they are on the
    top level and are declared "inline"
    """
    ERR_INLINE_ONLY = "function definition in pxd file must be declared 'cdef inline'"
    ERR_NOGO_WITH_INLINE = "inline function definition in pxd file cannot be '%s'"

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
        err = self.ERR_INLINE_ONLY

        if (isinstance(node, DefNode) and self.scope_type == 'cclass'
            and node.name in ('__getbuffer__', '__releasebuffer__')):
            err = None # allow these slots
            
        if isinstance(node, CFuncDefNode):
            if u'inline' in node.modifiers and self.scope_type == 'pxd':
                node.inline_in_pxd = True
                if node.visibility != 'private':
                    err = self.ERR_NOGO_WITH_INLINE % node.visibility
                elif node.api:
                    err = self.ERR_NOGO_WITH_INLINE % 'api'
                else:
                    err = None # allow inline function
            else:
                err = self.ERR_INLINE_ONLY

        if err:
            self.context.nonfatal_error(PostParseError(node.pos, err))
            return None
        else:
            return node
    
class InterpretCompilerDirectives(CythonTransform, SkipDeclarations):
    """
    After parsing, options can be stored in a number of places:
    - #cython-comments at the top of the file (stored in ModuleNode)
    - Command-line arguments overriding these
    - @cython.optionname decorators
    - with cython.optionname: statements

    This transform is responsible for interpreting these various sources
    and store the option in two ways:
    - Set the directives attribute of the ModuleNode for global directives.
    - Use a CompilerDirectivesNode to override directives for a subtree.

    (The first one is primarily to not have to modify with the tree
    structure, so that ModuleNode stay on top.)

    The directives are stored in dictionaries from name to value in effect.
    Each such dictionary is always filled in for all possible directives,
    using default values where no value is given by the user.

    The available directives are controlled in Options.py.

    Note that we have to run this prior to analysis, and so some minor
    duplication of functionality has to occur: We manually track cimports
    and which names the "cython" module may have been imported to.
    """
    special_methods = set(['declare', 'union', 'struct', 'typedef', 'sizeof', 'cast', 'address', 'pointer', 'compiled', 'NULL'])

    def __init__(self, context, compilation_option_overrides):
        super(InterpretCompilerDirectives, self).__init__(context)
        self.compilation_option_overrides = compilation_option_overrides
        self.cython_module_names = set()
        self.option_names = {}

    # Set up processing and handle the cython: comments.
    def visit_ModuleNode(self, node):
        options = copy.copy(Options.option_defaults)
        options.update(node.option_comments)
        options.update(self.compilation_option_overrides)
        self.options = options
        node.directives = options
        self.visitchildren(node)
        node.cython_module_names = self.cython_module_names
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
                if (name in Options.option_types or 
                        name in self.special_methods or
                        PyrexTypes.parse_basic_type(name)):
                    if as_name is None:
                        as_name = name
                    self.option_names[as_name] = name
                    if kind is not None:
                        self.context.nonfatal_error(PostParseError(pos,
                            "Compiler option imports must be plain imports"))
                else:
                    newimp.append((pos, name, as_name, kind))
            if not newimp:
                return None
            node.imported_names = newimp
        return node
        
    def visit_FromImportStatNode(self, node):
        if node.module.module_name.value == u"cython":
            newimp = []
            for name, name_node in node.items:
                if (name in Options.option_types or 
                        name in self.special_methods or
                        PyrexTypes.parse_basic_type(name)):
                    self.option_names[name_node.name] = name
                else:
                    newimp.append((name, name_node))
            if not newimp:
                return None
            node.items = newimp
        return node

    def visit_SingleAssignmentNode(self, node):
        if (isinstance(node.rhs, ImportNode) and
                node.rhs.module_name.value == u'cython'):
            node = CImportStatNode(node.pos, 
                                   module_name = u'cython',
                                   as_name = node.lhs.name)
            self.visit_CImportStatNode(node)
        else:
            self.visitchildren(node)
        return node
            
    def visit_NameNode(self, node):
        if node.name in self.cython_module_names:
            node.is_cython_module = True
        else:
            node.cython_attribute = self.option_names.get(node.name)
        return node

    def try_to_parse_option(self, node):
        # If node is the contents of an option (in a with statement or
        # decorator), returns (optionname, value).
        # Otherwise, returns None
        optname = None
        if isinstance(node, CallNode):
            self.visit(node.function)
            optname = node.function.as_cython_attribute()

        if optname:
            optiontype = Options.option_types.get(optname)
            if optiontype:
                args, kwds = node.explicit_args_kwds()
                if optiontype is bool:
                    if kwds is not None or len(args) != 1 or not isinstance(args[0], BoolNode):
                        raise PostParseError(dec.function.pos,
                            'The %s option takes one compile-time boolean argument' % optname)
                    return (optname, args[0].value)
                elif optiontype is dict:
                    if len(args) != 0:
                        raise PostParseError(dec.function.pos,
                            'The %s option takes no prepositional arguments' % optname)
                    return optname, dict([(key.value, value) for key, value in kwds.key_value_pairs])
                else:
                    assert False

        return None

    def visit_with_options(self, body, options):
        oldoptions = self.options
        newoptions = copy.copy(oldoptions)
        newoptions.update(options)
        self.options = newoptions
        assert isinstance(body, StatListNode), body
        retbody = self.visit_Node(body)
        directive = CompilerDirectivesNode(pos=retbody.pos, body=retbody,
                                           directives=newoptions)
        self.options = oldoptions
        return directive
 
    # Handle decorators
    def visit_FuncDefNode(self, node):
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
            if realdecs and isinstance(node, CFuncDefNode):
                raise PostParseError(realdecs[0].pos, "Cdef functions cannot take arbitrary decorators.")
            else:
                node.decorators = realdecs
        
        if options:
            optdict = {}
            options.reverse() # Decorators coming first take precedence
            for option in options:
                name, value = option
                optdict[name] = value
            body = StatListNode(node.pos, stats=[node])
            return self.visit_with_options(body, optdict)
        else:
            return self.visit_Node(node)
    
    def visit_CVarDefNode(self, node):
        if node.decorators:
            for dec in node.decorators:
                option = self.try_to_parse_option(dec.decorator)
                if option is not None and option[0] == u'locals':
                    node.directive_locals = option[1]
                else:
                    raise PostParseError(dec.pos, "Cdef functions can only take cython.locals() decorator.")
        return node
                                   
    # Handle with statements
    def visit_WithStatNode(self, node):
        option = self.try_to_parse_option(node.manager)
        if option is not None:
            if node.target is not None:
                raise PostParseError(node.pos, "Compiler option with statements cannot contain 'as'")
            name, value = option
            return self.visit_with_options(node.body, {name:value})
        else:
            return self.visit_Node(node)

class WithTransform(CythonTransform, SkipDeclarations):

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
                EXCINFO = None
                BODY
            except:
                EXC = False
                if not EXIT(*EXCINFO):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
    """, temps=[u'MGR', u'EXC', u"EXIT"],
    pipeline=[NormalizeTree(None)])

    template_with_target = TreeFragment(u"""
        MGR = EXPR
        EXIT = MGR.__exit__
        VALUE = MGR.__enter__()
        EXC = True
        try:
            try:
                EXCINFO = None
                TARGET = VALUE
                BODY
            except:
                EXC = False
                if not EXIT(*EXCINFO):
                    raise
        finally:
            if EXC:
                EXIT(None, None, None)
            MGR = EXIT = VALUE = EXC = None
            
    """, temps=[u'MGR', u'EXC', u"EXIT", u"VALUE"],
    pipeline=[NormalizeTree(None)])

    def visit_WithStatNode(self, node):
        # TODO: Cleanup badly needed
        TemplateTransform.temp_name_counter += 1
        handle = "__tmpvar_%d" % TemplateTransform.temp_name_counter
        
        self.visitchildren(node, ['body'])
        excinfo_temp = NameNode(node.pos, name=handle)#TempHandle(Builtin.tuple_type)
        if node.target is not None:
            result = self.template_with_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                u'TARGET' : node.target,
                u'EXCINFO' : excinfo_temp
                }, pos=node.pos)
        else:
            result = self.template_without_target.substitute({
                u'EXPR' : node.manager,
                u'BODY' : node.body,
                u'EXCINFO' : excinfo_temp
                }, pos=node.pos)

        # Set except excinfo target to EXCINFO
        try_except = result.stats[-1].body.stats[-1]
        try_except.except_clauses[0].excinfo_target = NameNode(node.pos, name=handle)
#            excinfo_temp.ref(node.pos))

#        result.stats[-1].body.stats[-1] = TempsBlockNode(
#            node.pos, temps=[excinfo_temp], body=try_except)

        return result
        
    def visit_ExprNode(self, node):
        # With statements are never inside expressions.
        return node
        

class ComprehensionTransform(VisitorTransform):
    """Prevent the target of list/set/dict comprehensions from leaking by
    moving it into a temp variable.  This mimics the behaviour of all
    comprehensions in Py3 and of generator expressions in Py2.x.

    This must run before the IterationTransform, which might replace
    for-loops with while-loops.  We only handle for-loops here.
    """
    def visit_ModuleNode(self, node):
        self.comprehension_targets = {}
        self.visitchildren(node)
        return node

    visit_Node = VisitorTransform.recurse_to_children

    def visit_ComprehensionNode(self, node):
        if type(node.loop) not in (Nodes.ForInStatNode,
                                   Nodes.ForFromStatNode):
            # this should not happen!
            self.visitchildren(node)
            return node

        outer_comprehension_targets = self.comprehension_targets
        self.comprehension_targets = outer_comprehension_targets.copy()

        # find all NameNodes in the loop target
        target_name_collector = NameNodeCollector()
        target_name_collector.visit(node.loop.target)
        targets = target_name_collector.name_nodes

        # create a temp variable for each target name
        temps = []
        for target in targets:
            handle = TempHandle(target.type)
            temps.append(handle)
            self.comprehension_targets[target.entry.cname] = handle.ref(node.pos)

        # replace name references in the loop code by their temp node
        self.visitchildren(node, ['loop'])

        loop = node.loop
        if type(loop) is Nodes.ForFromStatNode and loop.target.type.is_numeric:
            loop.loopvar_node = loop.target

        node.loop = TempsBlockNode(node.pos, body=node.loop, temps=temps)
        self.comprehension_targets = outer_comprehension_targets
        return node

    def visit_NameNode(self, node):
        if node.entry:
            replacement = self.comprehension_targets.get(node.entry.cname)
            if replacement is not None:
                return replacement
        return node


class DecoratorTransform(CythonTransform, SkipDeclarations):

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
        for var, type_node in node.directive_locals.items():
            if not lenv.lookup_here(var):   # don't redeclare args
                type = type_node.analyse_as_type(lenv)
                if type:
                    lenv.declare_var(var, type, type_node.pos)
                else:
                    error(type_node.pos, "Not a type")
        node.body.analyse_declarations(lenv)
        self.env_stack.append(lenv)
        self.visitchildren(node)
        self.env_stack.pop()
        return node
    
    # Some nodes are no longer needed after declaration
    # analysis and can be dropped. The analysis was performed
    # on these nodes in a seperate recursive process from the
    # enclosing function or module, so we can simply drop them.
    def visit_CDeclaratorNode(self, node):
        return node
    
    def visit_CTypeDefNode(self, node):
        return node

    def visit_CBaseTypeNode(self, node):
        return None
    
    def visit_CEnumDefNode(self, node):
        return None

    def visit_CStructOrUnionDefNode(self, node):
        return None

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
        
class AlignFunctionDefinitions(CythonTransform):
    """
    This class takes the signatures from a .pxd file and applies them to 
    the def methods in a .py file. 
    """
    
    def visit_ModuleNode(self, node):
        self.scope = node.scope
        self.directives = node.directives
        self.visitchildren(node)
        return node
    
    def visit_PyClassDefNode(self, node):
        pxd_def = self.scope.lookup(node.name)
        if pxd_def:
            if pxd_def.is_cclass:
                return self.visit_CClassDefNode(node.as_cclass(), pxd_def)
            else:
                error(node.pos, "'%s' redeclared" % node.name)
                error(pxd_def.pos, "previous declaration here")
                return None
        else:
            return node
        
    def visit_CClassDefNode(self, node, pxd_def=None):
        if pxd_def is None:
            pxd_def = self.scope.lookup(node.class_name)
        if pxd_def:
            outer_scope = self.scope
            self.scope = pxd_def.type.scope
        self.visitchildren(node)
        if pxd_def:
            self.scope = outer_scope
        return node
        
    def visit_DefNode(self, node):
        pxd_def = self.scope.lookup(node.name)
        if pxd_def:
            if pxd_def.is_cfunction:
                node = node.as_cfunction(pxd_def)
            else:
                error(node.pos, "'%s' redeclared" % node.name)
                error(pxd_def.pos, "previous declaration here")
                return None
        elif self.scope.is_module_scope and self.directives['auto_cpdef']:
            node = node.as_cfunction(scope=self.scope)
        # Enable this when internal def functions are allowed. 
        # self.visitchildren(node)
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
        

class EnvTransform(CythonTransform):
    """
    This transformation keeps a stack of the environments. 
    """
    def __call__(self, root):
        self.env_stack = [root.scope]
        return super(EnvTransform, self).__call__(root)        
    
    def visit_FuncDefNode(self, node):
        self.env_stack.append(node.local_scope)
        self.visitchildren(node)
        self.env_stack.pop()
        return node


class TransformBuiltinMethods(EnvTransform):

    def visit_SingleAssignmentNode(self, node):
        if node.declaration_only:
            return None
        else:
            self.visitchildren(node)
            return node
    
    def visit_AttributeNode(self, node):
        return self.visit_cython_attribute(node)

    def visit_NameNode(self, node):
        return self.visit_cython_attribute(node)
        
    def visit_cython_attribute(self, node):
        attribute = node.as_cython_attribute()
        if attribute:
            if attribute == u'compiled':
                node = BoolNode(node.pos, value=True)
            elif attribute == u'NULL':
                node = NullNode(node.pos)
            elif not PyrexTypes.parse_basic_type(attribute):
                error(node.pos, u"'%s' not a valid cython attribute or is being used incorrectly" % attribute)
        return node

    def visit_SimpleCallNode(self, node):

        # locals builtin
        if isinstance(node.function, ExprNodes.NameNode):
            if node.function.name == 'locals':
                pos = node.pos
                lenv = self.env_stack[-1]
                items = [ExprNodes.DictItemNode(pos, 
                                                key=ExprNodes.IdentifierStringNode(pos, value=var),
                                                value=ExprNodes.NameNode(pos, name=var)) for var in lenv.entries]
                return ExprNodes.DictNode(pos, key_value_pairs=items)

        # cython.foo
        function = node.function.as_cython_attribute()
        if function:
            if function == u'cast':
                if len(node.args) != 2:
                    error(node.function.pos, u"cast takes exactly two arguments")
                else:
                    type = node.args[0].analyse_as_type(self.env_stack[-1])
                    if type:
                        node = TypecastNode(node.function.pos, type=type, operand=node.args[1])
                    else:
                        error(node.args[0].pos, "Not a type")
            elif function == u'sizeof':
                if len(node.args) != 1:
                    error(node.function.pos, u"sizeof takes exactly one argument" % function)
                else:
                    type = node.args[0].analyse_as_type(self.env_stack[-1])
                    if type:
                        node = SizeofTypeNode(node.function.pos, arg_type=type)
                    else:
                        node = SizeofVarNode(node.function.pos, operand=node.args[0])
            elif function == 'address':
                if len(node.args) != 1:
                    error(node.function.pos, u"sizeof takes exactly one argument" % function)
                else:
                    node = AmpersandNode(node.function.pos, operand=node.args[0])
            else:
                error(node.function.pos, u"'%s' not a valid cython language construct" % function)
        
        self.visitchildren(node)
        return node
