
import cython
cython.declare(PyrexTypes=object, Naming=object, ExprNodes=object, Nodes=object,
               Options=object, UtilNodes=object, ModuleNode=object,
               LetNode=object, LetRefNode=object, TreeFragment=object,
               TemplateTransform=object, EncodedString=object,
               error=object, warning=object, copy=object)

import PyrexTypes
import Naming
import ExprNodes
import Nodes
import Options

from Cython.Compiler.Visitor import VisitorTransform, TreeVisitor
from Cython.Compiler.Visitor import CythonTransform, EnvTransform, ScopeTrackingTransform
from Cython.Compiler.ModuleNode import ModuleNode
from Cython.Compiler.UtilNodes import LetNode, LetRefNode
from Cython.Compiler.TreeFragment import TreeFragment, TemplateTransform
from Cython.Compiler.StringEncoding import EncodedString
from Cython.Compiler.Errors import error, warning, CompileError, InternalError

import copy


class NameNodeCollector(TreeVisitor):
    """Collect all NameNodes of a (sub-)tree in the ``name_nodes``
    attribute.
    """
    def __init__(self):
        super(NameNodeCollector, self).__init__()
        self.name_nodes = []

    def visit_NameNode(self, node):
        self.name_nodes.append(node)

    def visit_Node(self, node):
        self._visitchildren(node, None)


class SkipDeclarations(object):
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
            return Nodes.StatListNode(pos=node.pos, stats=[node])
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
            return Nodes.StatListNode(pos=node.pos, stats=[])
        else:
            return []

    def visit_CDeclaratorNode(self, node):
        return node


class PostParseError(CompileError): pass

# error strings checked by unit tests, so define them
ERR_CDEF_INCLASS = 'Cannot assign default value to fields in cdef classes, structs or unions'
ERR_BUF_DEFAULTS = 'Invalid buffer defaults specification (see docs)'
ERR_INVALID_SPECIALATTR_TYPE = 'Special attributes must not have a type declared'
class PostParse(ScopeTrackingTransform):
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
    TemplatedTypeNode[args] and __cythonbufferdefaults__ = {args}),
    which should be interpreted. This happens in a general way
    and other steps should be taken to ensure validity.

    Type arguments cannot be interpreted in this way.

    - For __cythonbufferdefaults__ the arguments are checked for
    validity.

    TemplatedTypeNode has its directives interpreted:
    Any first positional argument goes into the "dtype" attribute,
    any "ndim" keyword argument goes into the "ndim" attribute and
    so on. Also it is checked that the directive combination is valid.
    - __cythonbufferdefaults__ attributes are parsed and put into the
    type information.

    Note: Currently Parsing.py does a lot of interpretation and
    reorganization that can be refactored into this transform
    if a more pure Abstract Syntax Tree is wanted.
    """

    def __init__(self, context):
        super(PostParse, self).__init__(context)
        self.specialattribute_handlers = {
            '__cythonbufferdefaults__' : self.handle_bufferdefaults
        }

    def visit_ModuleNode(self, node):
        self.lambda_counter = 1
        return super(PostParse, self).visit_ModuleNode(node)

    def visit_LambdaNode(self, node):
        # unpack a lambda expression into the corresponding DefNode
        lambda_id = self.lambda_counter
        self.lambda_counter += 1
        node.lambda_name = EncodedString(u'lambda%d' % lambda_id)

        body = Nodes.ReturnStatNode(
            node.result_expr.pos, value = node.result_expr)
        node.def_node = Nodes.DefNode(
            node.pos, name=node.name, lambda_name=node.lambda_name,
            args=node.args, star_arg=node.star_arg,
            starstar_arg=node.starstar_arg,
            body=body)
        self.visitchildren(node)
        return node

    # cdef variables
    def handle_bufferdefaults(self, decl):
        if not isinstance(decl.default, ExprNodes.DictNode):
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
                while isinstance(declbase, Nodes.CPtrDeclaratorNode):
                    declbase = declbase.base
                if isinstance(declbase, Nodes.CNameDeclaratorNode):
                    if declbase.default is not None:
                        if self.scope_type in ('cclass', 'pyclass', 'struct'):
                            if isinstance(self.scope_node, Nodes.CClassDefNode):
                                handler = self.specialattribute_handlers.get(decl.name)
                                if handler:
                                    if decl is not declbase:
                                        raise PostParseError(decl.pos, ERR_INVALID_SPECIALATTR_TYPE)
                                    handler(decl)
                                    continue # Remove declaration
                            raise PostParseError(decl.pos, ERR_CDEF_INCLASS)
                        first_assignment = self.scope_type != 'module'
                        stats.append(Nodes.SingleAssignmentNode(node.pos,
                            lhs=ExprNodes.NameNode(node.pos, name=declbase.name),
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

    # Split parallel assignments (a,b = b,a) into separate partial
    # assignments that are executed rhs-first using temps.  This
    # restructuring must be applied before type analysis so that known
    # types on rhs and lhs can be matched directly.  It is required in
    # the case that the types cannot be coerced to a Python type in
    # order to assign from a tuple.

    def visit_SingleAssignmentNode(self, node):
        self.visitchildren(node)
        return self._visit_assignment_node(node, [node.lhs, node.rhs])

    def visit_CascadedAssignmentNode(self, node):
        self.visitchildren(node)
        return self._visit_assignment_node(node, node.lhs_list + [node.rhs])

    def _visit_assignment_node(self, node, expr_list):
        """Flatten parallel assignments into separate single
        assignments or cascaded assignments.
        """
        if sum([ 1 for expr in expr_list if expr.is_sequence_constructor ]) < 2:
            # no parallel assignments => nothing to do
            return node

        expr_list_list = []
        flatten_parallel_assignments(expr_list, expr_list_list)
        temp_refs = []
        eliminate_rhs_duplicates(expr_list_list, temp_refs)

        nodes = []
        for expr_list in expr_list_list:
            lhs_list = expr_list[:-1]
            rhs = expr_list[-1]
            if len(lhs_list) == 1:
                node = Nodes.SingleAssignmentNode(rhs.pos,
                    lhs = lhs_list[0], rhs = rhs)
            else:
                node = Nodes.CascadedAssignmentNode(rhs.pos,
                    lhs_list = lhs_list, rhs = rhs)
            nodes.append(node)

        if len(nodes) == 1:
            assign_node = nodes[0]
        else:
            assign_node = Nodes.ParallelAssignmentNode(nodes[0].pos, stats = nodes)

        if temp_refs:
            duplicates_and_temps = [ (temp.expression, temp)
                                     for temp in temp_refs ]
            sort_common_subsequences(duplicates_and_temps)
            for _, temp_ref in duplicates_and_temps[::-1]:
                assign_node = LetNode(temp_ref, assign_node)

        return assign_node

def eliminate_rhs_duplicates(expr_list_list, ref_node_sequence):
    """Replace rhs items by LetRefNodes if they appear more than once.
    Creates a sequence of LetRefNodes that set up the required temps
    and appends them to ref_node_sequence.  The input list is modified
    in-place.
    """
    seen_nodes = cython.set()
    ref_nodes = {}
    def find_duplicates(node):
        if node.is_literal or node.is_name:
            # no need to replace those; can't include attributes here
            # as their access is not necessarily side-effect free
            return
        if node in seen_nodes:
            if node not in ref_nodes:
                ref_node = LetRefNode(node)
                ref_nodes[node] = ref_node
                ref_node_sequence.append(ref_node)
        else:
            seen_nodes.add(node)
            if node.is_sequence_constructor:
                for item in node.args:
                    find_duplicates(item)

    for expr_list in expr_list_list:
        rhs = expr_list[-1]
        find_duplicates(rhs)
    if not ref_nodes:
        return

    def substitute_nodes(node):
        if node in ref_nodes:
            return ref_nodes[node]
        elif node.is_sequence_constructor:
            node.args = list(map(substitute_nodes, node.args))
        return node

    # replace nodes inside of the common subexpressions
    for node in ref_nodes:
        if node.is_sequence_constructor:
            node.args = list(map(substitute_nodes, node.args))

    # replace common subexpressions on all rhs items
    for expr_list in expr_list_list:
        expr_list[-1] = substitute_nodes(expr_list[-1])

def sort_common_subsequences(items):
    """Sort items/subsequences so that all items and subsequences that
    an item contains appear before the item itself.  This is needed
    because each rhs item must only be evaluated once, so its value
    must be evaluated first and then reused when packing sequences
    that contain it.

    This implies a partial order, and the sort must be stable to
    preserve the original order as much as possible, so we use a
    simple insertion sort (which is very fast for short sequences, the
    normal case in practice).
    """
    def contains(seq, x):
        for item in seq:
            if item is x:
                return True
            elif item.is_sequence_constructor and contains(item.args, x):
                return True
        return False
    def lower_than(a,b):
        return b.is_sequence_constructor and contains(b.args, a)

    for pos, item in enumerate(items):
        key = item[1] # the ResultRefNode which has already been injected into the sequences
        new_pos = pos
        for i in xrange(pos-1, -1, -1):
            if lower_than(key, items[i][0]):
                new_pos = i
        if new_pos != pos:
            for i in xrange(pos, new_pos, -1):
                items[i] = items[i-1]
            items[new_pos] = item

def flatten_parallel_assignments(input, output):
    #  The input is a list of expression nodes, representing the LHSs
    #  and RHS of one (possibly cascaded) assignment statement.  For
    #  sequence constructors, rearranges the matching parts of both
    #  sides into a list of equivalent assignments between the
    #  individual elements.  This transformation is applied
    #  recursively, so that nested structures get matched as well.
    rhs = input[-1]
    if not rhs.is_sequence_constructor or not sum([lhs.is_sequence_constructor for lhs in input[:-1]]):
        output.append(input)
        return

    complete_assignments = []

    rhs_size = len(rhs.args)
    lhs_targets = [ [] for _ in xrange(rhs_size) ]
    starred_assignments = []
    for lhs in input[:-1]:
        if not lhs.is_sequence_constructor:
            if lhs.is_starred:
                error(lhs.pos, "starred assignment target must be in a list or tuple")
            complete_assignments.append(lhs)
            continue
        lhs_size = len(lhs.args)
        starred_targets = sum([1 for expr in lhs.args if expr.is_starred])
        if starred_targets > 1:
            error(lhs.pos, "more than 1 starred expression in assignment")
            output.append([lhs,rhs])
            continue
        elif lhs_size - starred_targets > rhs_size:
            error(lhs.pos, "need more than %d value%s to unpack"
                  % (rhs_size, (rhs_size != 1) and 's' or ''))
            output.append([lhs,rhs])
            continue
        elif starred_targets:
            map_starred_assignment(lhs_targets, starred_assignments,
                                   lhs.args, rhs.args)
        elif lhs_size < rhs_size:
            error(lhs.pos, "too many values to unpack (expected %d, got %d)"
                  % (lhs_size, rhs_size))
            output.append([lhs,rhs])
            continue
        else:
            for targets, expr in zip(lhs_targets, lhs.args):
                targets.append(expr)

    if complete_assignments:
        complete_assignments.append(rhs)
        output.append(complete_assignments)

    # recursively flatten partial assignments
    for cascade, rhs in zip(lhs_targets, rhs.args):
        if cascade:
            cascade.append(rhs)
            flatten_parallel_assignments(cascade, output)

    # recursively flatten starred assignments
    for cascade in starred_assignments:
        if cascade[0].is_sequence_constructor:
            flatten_parallel_assignments(cascade, output)
        else:
            output.append(cascade)

def map_starred_assignment(lhs_targets, starred_assignments, lhs_args, rhs_args):
    # Appends the fixed-position LHS targets to the target list that
    # appear left and right of the starred argument.
    #
    # The starred_assignments list receives a new tuple
    # (lhs_target, rhs_values_list) that maps the remaining arguments
    # (those that match the starred target) to a list.

    # left side of the starred target
    for i, (targets, expr) in enumerate(zip(lhs_targets, lhs_args)):
        if expr.is_starred:
            starred = i
            lhs_remaining = len(lhs_args) - i - 1
            break
        targets.append(expr)
    else:
        raise InternalError("no starred arg found when splitting starred assignment")

    # right side of the starred target
    for i, (targets, expr) in enumerate(zip(lhs_targets[-lhs_remaining:],
                                            lhs_args[-lhs_remaining:])):
        targets.append(expr)

    # the starred target itself, must be assigned a (potentially empty) list
    target = lhs_args[starred].target # unpack starred node
    starred_rhs = rhs_args[starred:]
    if lhs_remaining:
        starred_rhs = starred_rhs[:-lhs_remaining]
    if starred_rhs:
        pos = starred_rhs[0].pos
    else:
        pos = target.pos
    starred_assignments.append([
        target, ExprNodes.ListNode(pos=pos, args=starred_rhs)])


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

        if (isinstance(node, Nodes.DefNode) and self.scope_type == 'cclass'
            and node.name in ('__getbuffer__', '__releasebuffer__')):
            err = None # allow these slots

        if isinstance(node, Nodes.CFuncDefNode):
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
    After parsing, directives can be stored in a number of places:
    - #cython-comments at the top of the file (stored in ModuleNode)
    - Command-line arguments overriding these
    - @cython.directivename decorators
    - with cython.directivename: statements

    This transform is responsible for interpreting these various sources
    and store the directive in two ways:
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
    unop_method_nodes = {
        'typeof': ExprNodes.TypeofNode,

        'operator.address': ExprNodes.AmpersandNode,
        'operator.dereference': ExprNodes.DereferenceNode,
        'operator.preincrement' : ExprNodes.inc_dec_constructor(True, '++'),
        'operator.predecrement' : ExprNodes.inc_dec_constructor(True, '--'),
        'operator.postincrement': ExprNodes.inc_dec_constructor(False, '++'),
        'operator.postdecrement': ExprNodes.inc_dec_constructor(False, '--'),

        # For backwards compatability.
        'address': ExprNodes.AmpersandNode,
    }

    binop_method_nodes = {
        'operator.comma'        : ExprNodes.c_binop_constructor(','),
    }

    special_methods = cython.set(['declare', 'union', 'struct', 'typedef', 'sizeof',
                                  'cast', 'pointer', 'compiled', 'NULL'])
    special_methods.update(unop_method_nodes.keys())

    def __init__(self, context, compilation_directive_defaults):
        super(InterpretCompilerDirectives, self).__init__(context)
        self.compilation_directive_defaults = {}
        for key, value in compilation_directive_defaults.items():
            self.compilation_directive_defaults[unicode(key)] = value
        self.cython_module_names = cython.set()
        self.directive_names = {}

    def check_directive_scope(self, pos, directive, scope):
        legal_scopes = Options.directive_scopes.get(directive, None)
        if legal_scopes and scope not in legal_scopes:
            self.context.nonfatal_error(PostParseError(pos, 'The %s compiler directive '
                                        'is not allowed in %s scope' % (directive, scope)))
            return False
        else:
            return True

    # Set up processing and handle the cython: comments.
    def visit_ModuleNode(self, node):
        for key, value in node.directive_comments.items():
            if not self.check_directive_scope(node.pos, key, 'module'):
                self.wrong_scope_error(node.pos, key, 'module')
                del node.directive_comments[key]

        directives = copy.copy(Options.directive_defaults)
        directives.update(self.compilation_directive_defaults)
        directives.update(node.directive_comments)
        self.directives = directives
        node.directives = directives
        self.visitchildren(node)
        node.cython_module_names = self.cython_module_names
        return node

    # The following four functions track imports and cimports that
    # begin with "cython"
    def is_cython_directive(self, name):
        return (name in Options.directive_types or
                name in self.special_methods or
                PyrexTypes.parse_basic_type(name))

    def visit_CImportStatNode(self, node):
        if node.module_name == u"cython":
            self.cython_module_names.add(node.as_name or u"cython")
        elif node.module_name.startswith(u"cython."):
            if node.as_name:
                self.directive_names[node.as_name] = node.module_name[7:]
            else:
                self.cython_module_names.add(u"cython")
            # if this cimport was a compiler directive, we don't
            # want to leave the cimport node sitting in the tree
            return None
        return node

    def visit_FromCImportStatNode(self, node):
        if (node.module_name == u"cython") or \
               node.module_name.startswith(u"cython."):
            submodule = (node.module_name + u".")[7:]
            newimp = []
            for pos, name, as_name, kind in node.imported_names:
                full_name = submodule + name
                if self.is_cython_directive(full_name):
                    if as_name is None:
                        as_name = full_name
                    self.directive_names[as_name] = full_name
                    if kind is not None:
                        self.context.nonfatal_error(PostParseError(pos,
                            "Compiler directive imports must be plain imports"))
                else:
                    newimp.append((pos, name, as_name, kind))
            if not newimp:
                return None
            node.imported_names = newimp
        return node

    def visit_FromImportStatNode(self, node):
        if (node.module.module_name.value == u"cython") or \
               node.module.module_name.value.startswith(u"cython."):
            submodule = (node.module.module_name.value + u".")[7:]
            newimp = []
            for name, name_node in node.items:
                full_name = submodule + name
                if self.is_cython_directive(full_name):
                    self.directive_names[name_node.name] = full_name
                else:
                    newimp.append((name, name_node))
            if not newimp:
                return None
            node.items = newimp
        return node

    def visit_SingleAssignmentNode(self, node):
        if (isinstance(node.rhs, ExprNodes.ImportNode) and
                node.rhs.module_name.value == u'cython'):
            node = Nodes.CImportStatNode(node.pos,
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
            node.cython_attribute = self.directive_names.get(node.name)
        return node

    def try_to_parse_directives(self, node):
        # If node is the contents of an directive (in a with statement or
        # decorator), returns a list of (directivename, value) pairs.
        # Otherwise, returns None
        if isinstance(node, ExprNodes.CallNode):
            self.visit(node.function)
            optname = node.function.as_cython_attribute()
            if optname:
                directivetype = Options.directive_types.get(optname)
                if directivetype:
                    args, kwds = node.explicit_args_kwds()
                    directives = []
                    key_value_pairs = []
                    if kwds is not None and directivetype is not dict:
                        for keyvalue in kwds.key_value_pairs:
                            key, value = keyvalue
                            sub_optname = "%s.%s" % (optname, key.value)
                            if Options.directive_types.get(sub_optname):
                                directives.append(self.try_to_parse_directive(sub_optname, [value], None, keyvalue.pos))
                            else:
                                key_value_pairs.append(keyvalue)
                        if not key_value_pairs:
                            kwds = None
                        else:
                            kwds.key_value_pairs = key_value_pairs
                        if directives and not kwds and not args:
                            return directives
                    directives.append(self.try_to_parse_directive(optname, args, kwds, node.function.pos))
                    return directives
        elif isinstance(node, (ExprNodes.AttributeNode, ExprNodes.NameNode)):
            self.visit(node)
            optname = node.as_cython_attribute()
            if optname:
                directivetype = Options.directive_types.get(optname)
                if directivetype is bool:
                    return [(optname, True)]
                elif directivetype is None:
                    return [(optname, None)]
                else:
                    raise PostParseError(
                        node.pos, "The '%s' directive should be used as a function call." % optname)
        return None

    def try_to_parse_directive(self, optname, args, kwds, pos):
        directivetype = Options.directive_types.get(optname)
        if len(args) == 1 and isinstance(args[0], ExprNodes.NoneNode):
            return optname, Options.directive_defaults[optname]
        elif directivetype is bool:
            if kwds is not None or len(args) != 1 or not isinstance(args[0], ExprNodes.BoolNode):
                raise PostParseError(pos,
                    'The %s directive takes one compile-time boolean argument' % optname)
            return (optname, args[0].value)
        elif directivetype is str:
            if kwds is not None or len(args) != 1 or not isinstance(args[0], (ExprNodes.StringNode,
                                                                              ExprNodes.UnicodeNode)):
                raise PostParseError(pos,
                    'The %s directive takes one compile-time string argument' % optname)
            return (optname, str(args[0].value))
        elif directivetype is dict:
            if len(args) != 0:
                raise PostParseError(pos,
                    'The %s directive takes no prepositional arguments' % optname)
            return optname, dict([(key.value, value) for key, value in kwds.key_value_pairs])
        elif directivetype is list:
            if kwds and len(kwds) != 0:
                raise PostParseError(pos,
                    'The %s directive takes no keyword arguments' % optname)
            return optname, [ str(arg.value) for arg in args ]
        else:
            assert False

    def visit_with_directives(self, body, directives):
        olddirectives = self.directives
        newdirectives = copy.copy(olddirectives)
        newdirectives.update(directives)
        self.directives = newdirectives
        assert isinstance(body, Nodes.StatListNode), body
        retbody = self.visit_Node(body)
        directive = Nodes.CompilerDirectivesNode(pos=retbody.pos, body=retbody,
                                                 directives=newdirectives)
        self.directives = olddirectives
        return directive

    # Handle decorators
    def visit_FuncDefNode(self, node):
        directives = self._extract_directives(node, 'function')
        if not directives:
            return self.visit_Node(node)
        body = Nodes.StatListNode(node.pos, stats=[node])
        return self.visit_with_directives(body, directives)

    def visit_CVarDefNode(self, node):
        if not node.decorators:
            return node
        for dec in node.decorators:
            for directive in self.try_to_parse_directives(dec.decorator) or ():
                if directive is not None and directive[0] == u'locals':
                    node.directive_locals = directive[1]
                else:
                    self.context.nonfatal_error(PostParseError(dec.pos,
                        "Cdef functions can only take cython.locals() decorator."))
        return node

    def visit_CClassDefNode(self, node):
        directives = self._extract_directives(node, 'cclass')
        if not directives:
            return self.visit_Node(node)
        body = Nodes.StatListNode(node.pos, stats=[node])
        return self.visit_with_directives(body, directives)

    def visit_PyClassDefNode(self, node):
        directives = self._extract_directives(node, 'class')
        if not directives:
            return self.visit_Node(node)
        body = Nodes.StatListNode(node.pos, stats=[node])
        return self.visit_with_directives(body, directives)

    def _extract_directives(self, node, scope_name):
        if not node.decorators:
            return {}
        # Split the decorators into two lists -- real decorators and directives
        directives = []
        realdecs = []
        for dec in node.decorators:
            new_directives = self.try_to_parse_directives(dec.decorator)
            if new_directives is not None:
                for directive in new_directives:
                    if self.check_directive_scope(node.pos, directive[0], scope_name):
                        directives.append(directive)
            else:
                realdecs.append(dec)
        if realdecs and isinstance(node, (Nodes.CFuncDefNode, Nodes.CClassDefNode)):
            raise PostParseError(realdecs[0].pos, "Cdef functions/classes cannot take arbitrary decorators.")
        else:
            node.decorators = realdecs
        # merge or override repeated directives
        optdict = {}
        directives.reverse() # Decorators coming first take precedence
        for directive in directives:
            name, value = directive
            if name in optdict:
                old_value = optdict[name]
                # keywords and arg lists can be merged, everything
                # else overrides completely
                if isinstance(old_value, dict):
                    old_value.update(value)
                elif isinstance(old_value, list):
                    old_value.extend(value)
                else:
                    optdict[name] = value
            else:
                optdict[name] = value
        return optdict

    # Handle with statements
    def visit_WithStatNode(self, node):
        directive_dict = {}
        for directive in self.try_to_parse_directives(node.manager) or []:
            if directive is not None:
                if node.target is not None:
                    self.context.nonfatal_error(
                        PostParseError(node.pos, "Compiler directive with statements cannot contain 'as'"))
                else:
                    name, value = directive
                    if name == 'nogil':
                        # special case: in pure mode, "with nogil" spells "with cython.nogil"
                        node = Nodes.GILStatNode(node.pos, state = "nogil", body = node.body)
                        return self.visit_Node(node)
                    if self.check_directive_scope(node.pos, name, 'with statement'):
                        directive_dict[name] = value
        if directive_dict:
            return self.visit_with_directives(node.body, directive_dict)
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
        excinfo_temp = ExprNodes.NameNode(node.pos, name=handle)#TempHandle(Builtin.tuple_type)
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
        try_except.except_clauses[0].excinfo_target = ExprNodes.NameNode(node.pos, name=handle)
#            excinfo_temp.ref(node.pos))

#        result.stats[-1].body.stats[-1] = TempsBlockNode(
#            node.pos, temps=[excinfo_temp], body=try_except)

        return result

    def visit_ExprNode(self, node):
        # With statements are never inside expressions.
        return node


class DecoratorTransform(CythonTransform, SkipDeclarations):

    def visit_DefNode(self, func_node):
        self.visitchildren(func_node)
        if not func_node.decorators:
            return func_node
        return self._handle_decorators(
            func_node, func_node.name)

    def visit_CClassDefNode(self, class_node):
        # This doesn't currently work, so it's disabled.
        #
        # Problem: assignments to cdef class names do not work.  They
        # would require an additional check anyway, as the extension
        # type must not change its C type, so decorators cannot
        # replace an extension type, just alter it and return it.

        self.visitchildren(class_node)
        if not class_node.decorators:
            return class_node
        error(class_node.pos,
              "Decorators not allowed on cdef classes (used on type '%s')" % class_node.class_name)
        return class_node
        #return self._handle_decorators(
        #    class_node, class_node.class_name)

    def visit_ClassDefNode(self, class_node):
        self.visitchildren(class_node)
        if not class_node.decorators:
            return class_node
        return self._handle_decorators(
            class_node, class_node.name)

    def _handle_decorators(self, node, name):
        decorator_result = ExprNodes.NameNode(node.pos, name = name)
        for decorator in node.decorators[::-1]:
            decorator_result = ExprNodes.SimpleCallNode(
                decorator.pos,
                function = decorator.decorator,
                args = [decorator_result])

        name_node = ExprNodes.NameNode(node.pos, name = name)
        reassignment = Nodes.SingleAssignmentNode(
            node.pos,
            lhs = name_node,
            rhs = decorator_result)
        return [node, reassignment]


class AnalyseDeclarationsTransform(CythonTransform):

    basic_property = TreeFragment(u"""
property NAME:
    def __get__(self):
        return ATTR
    def __set__(self, value):
        ATTR = value
    """, level='c_class')
    basic_pyobject_property = TreeFragment(u"""
property NAME:
    def __get__(self):
        return ATTR
    def __set__(self, value):
        ATTR = value
    def __del__(self):
        ATTR = None
    """, level='c_class')
    basic_property_ro = TreeFragment(u"""
property NAME:
    def __get__(self):
        return ATTR
    """, level='c_class')

    def __call__(self, root):
        self.env_stack = [root.scope]
        # needed to determine if a cdef var is declared after it's used.
        self.seen_vars_stack = []
        return super(AnalyseDeclarationsTransform, self).__call__(root)

    def visit_NameNode(self, node):
        self.seen_vars_stack[-1].add(node.name)
        return node

    def visit_ModuleNode(self, node):
        self.seen_vars_stack.append(cython.set())
        node.analyse_declarations(self.env_stack[-1])
        self.visitchildren(node)
        self.seen_vars_stack.pop()
        return node

    def visit_LambdaNode(self, node):
        node.analyse_declarations(self.env_stack[-1])
        self.visitchildren(node)
        return node

    def visit_ClassDefNode(self, node):
        self.env_stack.append(node.scope)
        self.visitchildren(node)
        self.env_stack.pop()
        return node

    def visit_CClassDefNode(self, node):
        node = self.visit_ClassDefNode(node)
        if node.scope and node.scope.implemented:
            stats = []
            for entry in node.scope.var_entries:
                if entry.needs_property:
                    property = self.create_Property(entry)
                    property.analyse_declarations(node.scope)
                    self.visit(property)
                    stats.append(property)
            if stats:
                node.body.stats += stats
        return node

    def visit_FuncDefNode(self, node):
        self.seen_vars_stack.append(cython.set())
        lenv = node.local_scope
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
        self.seen_vars_stack.pop()
        return node

    def visit_ScopedExprNode(self, node):
        env = self.env_stack[-1]
        node.analyse_declarations(env)
        # the node may or may not have a local scope
        if node.has_local_scope:
            self.seen_vars_stack.append(cython.set(self.seen_vars_stack[-1]))
            self.env_stack.append(node.expr_scope)
            node.analyse_scoped_declarations(node.expr_scope)
            self.visitchildren(node)
            self.env_stack.pop()
            self.seen_vars_stack.pop()
        else:
            node.analyse_scoped_declarations(env)
            self.visitchildren(node)
        return node

    def visit_TempResultFromStatNode(self, node):
        self.visitchildren(node)
        node.analyse_declarations(self.env_stack[-1])
        return node

    # Some nodes are no longer needed after declaration
    # analysis and can be dropped. The analysis was performed
    # on these nodes in a seperate recursive process from the
    # enclosing function or module, so we can simply drop them.
    def visit_CDeclaratorNode(self, node):
        # necessary to ensure that all CNameDeclaratorNodes are visited.
        self.visitchildren(node)
        return node

    def visit_CTypeDefNode(self, node):
        return node

    def visit_CBaseTypeNode(self, node):
        return None

    def visit_CEnumDefNode(self, node):
        if node.visibility == 'public':
            return node
        else:
            return None

    def visit_CStructOrUnionDefNode(self, node):
        return None

    def visit_CNameDeclaratorNode(self, node):
        if node.name in self.seen_vars_stack[-1]:
            entry = self.env_stack[-1].lookup(node.name)
            if entry is None or entry.visibility != 'extern':
                warning(node.pos, "cdef variable '%s' declared after it is used" % node.name, 2)
        self.visitchildren(node)
        return node

    def visit_CVarDefNode(self, node):
        # to ensure all CNameDeclaratorNodes are visited.
        self.visitchildren(node)
        return None

    def create_Property(self, entry):
        if entry.visibility == 'public':
            if entry.type.is_pyobject:
                template = self.basic_pyobject_property
            else:
                template = self.basic_property
        elif entry.visibility == 'readonly':
            template = self.basic_property_ro
        property = template.substitute({
                u"ATTR": ExprNodes.AttributeNode(pos=entry.pos,
                                                 obj=ExprNodes.NameNode(pos=entry.pos, name="self"),
                                                 attribute=entry.name),
            }, pos=entry.pos).stats[0]
        property.name = entry.name
        # ---------------------------------------
        # XXX This should go to AutoDocTransforms
        # ---------------------------------------
        if (Options.docstrings and
            self.current_directives['embedsignature']):
            attr_name = entry.name
            type_name = entry.type.declaration_code("", for_display=1)
            default_value = ''
            if not entry.type.is_pyobject:
                type_name = "'%s'" % type_name
            elif entry.type.is_extension_type:
                type_name = entry.type.module_name + '.' + type_name
            if entry.init is not None:
                default_value = ' = ' + entry.init
            elif entry.init_to_none:
                default_value = ' = ' + repr(None)
            docstring = attr_name + ': ' + type_name + default_value
            property.doc = EncodedString(docstring)
        # ---------------------------------------
        return property

class AnalyseExpressionsTransform(CythonTransform):

    def visit_ModuleNode(self, node):
        node.scope.infer_types()
        node.body.analyse_expressions(node.scope)
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        node.local_scope.infer_types()
        node.body.analyse_expressions(node.local_scope)
        self.visitchildren(node)
        return node

    def visit_ScopedExprNode(self, node):
        if node.has_local_scope:
            node.expr_scope.infer_types()
            node.analyse_scoped_expressions(node.expr_scope)
        self.visitchildren(node)
        return node

class ExpandInplaceOperators(EnvTransform):

    def visit_InPlaceAssignmentNode(self, node):
        lhs = node.lhs
        rhs = node.rhs
        if lhs.type.is_cpp_class:
            # No getting around this exact operator here.
            return node
        if isinstance(lhs, ExprNodes.IndexNode) and lhs.is_buffer_access:
            # There is code to handle this case.
            return node

        env = self.current_env()
        def side_effect_free_reference(node, setting=False):
            if isinstance(node, ExprNodes.NameNode):
                return node, []
            elif node.type.is_pyobject and not setting:
                node = LetRefNode(node)
                return node, [node]
            elif isinstance(node, ExprNodes.IndexNode):
                if node.is_buffer_access:
                    raise ValueError, "Buffer access"
                base, temps = side_effect_free_reference(node.base)
                index = LetRefNode(node.index)
                return ExprNodes.IndexNode(node.pos, base=base, index=index), temps + [index]
            elif isinstance(node, ExprNodes.AttributeNode):
                obj, temps = side_effect_free_reference(node.obj)
                return ExprNodes.AttributeNode(node.pos, obj=obj, attribute=node.attribute), temps
            else:
                node = LetRefNode(node)
                return node, [node]
        try:
            lhs, let_ref_nodes = side_effect_free_reference(lhs, setting=True)
        except ValueError:
            return node
        dup = lhs.__class__(**lhs.__dict__)
        binop = ExprNodes.binop_node(node.pos,
                                     operator = node.operator,
                                     operand1 = dup,
                                     operand2 = rhs,
                                     inplace=True)
        # Manually analyse types for new node.
        lhs.analyse_target_types(env)
        dup.analyse_types(env)
        binop.analyse_operation(env)
        node = Nodes.SingleAssignmentNode(
            node.pos,
            lhs = lhs,
            rhs=binop.coerce_to(lhs.type, env))
        # Use LetRefNode to avoid side effects.
        let_ref_nodes.reverse()
        for t in let_ref_nodes:
            node = LetNode(t, node)
        return node

    def visit_ExprNode(self, node):
        # In-place assignments can't happen within an expression.
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
            if not pxd_def.is_cfunction:
                error(node.pos, "'%s' redeclared" % node.name)
                error(pxd_def.pos, "previous declaration here")
                return None
            node = node.as_cfunction(pxd_def)
        elif self.scope.is_module_scope and self.directives['auto_cpdef']:
            node = node.as_cfunction(scope=self.scope)
        # Enable this when internal def functions are allowed.
        # self.visitchildren(node)
        return node


class MarkClosureVisitor(CythonTransform):

    def visit_ModuleNode(self, node):
        self.needs_closure = False
        self.visitchildren(node)
        return node

    def visit_FuncDefNode(self, node):
        self.needs_closure = False
        self.visitchildren(node)
        node.needs_closure = self.needs_closure
        self.needs_closure = True
        return node

    def visit_CFuncDefNode(self, node):
        self.visit_FuncDefNode(node)
        if node.needs_closure:
            error(node.pos, "closures inside cdef functions not yet supported")
        return node

    def visit_LambdaNode(self, node):
        self.needs_closure = False
        self.visitchildren(node)
        node.needs_closure = self.needs_closure
        self.needs_closure = True
        return node

    def visit_ClassDefNode(self, node):
        self.visitchildren(node)
        self.needs_closure = True
        return node


class CreateClosureClasses(CythonTransform):
    # Output closure classes in module scope for all functions
    # that really need it.

    def __init__(self, context):
        super(CreateClosureClasses, self).__init__(context)
        self.path = []
        self.in_lambda = False

    def visit_ModuleNode(self, node):
        self.module_scope = node.scope
        self.visitchildren(node)
        return node

    def get_scope_use(self, node):
        from_closure = []
        in_closure = []
        for name, entry in node.local_scope.entries.items():
            if entry.from_closure:
                from_closure.append((name, entry))
            elif entry.in_closure and not entry.from_closure:
                in_closure.append((name, entry))
        return from_closure, in_closure

    def create_class_from_scope(self, node, target_module_scope, inner_node=None):
        from_closure, in_closure = self.get_scope_use(node)
        in_closure.sort()

        # Now from the begining
        node.needs_closure = False
        node.needs_outer_scope = False

        func_scope = node.local_scope
        cscope = node.entry.scope
        while cscope.is_py_class_scope or cscope.is_c_class_scope:
            cscope = cscope.outer_scope

        if not from_closure and (self.path or inner_node):
            if not inner_node:
                if not node.assmt:
                    raise InternalError, "DefNode does not have assignment node"
                inner_node = node.assmt.rhs
            inner_node.needs_self_code = False
            node.needs_outer_scope = False
        # Simple cases
        if not in_closure and not from_closure:
            return
        elif not in_closure:
            func_scope.is_passthrough = True
            func_scope.scope_class = cscope.scope_class
            node.needs_outer_scope = True
            return

        as_name = '%s_%s' % (target_module_scope.next_id(Naming.closure_class_prefix), node.entry.cname)

        entry = target_module_scope.declare_c_class(name = as_name,
            pos = node.pos, defining = True, implementing = True)
        func_scope.scope_class = entry
        class_scope = entry.type.scope
        class_scope.is_internal = True
        class_scope.directives = {'final': True}

        if from_closure:
            assert cscope.is_closure_scope
            class_scope.declare_var(pos=node.pos,
                                    name=Naming.outer_scope_cname,
                                    cname=Naming.outer_scope_cname,
                                    type=cscope.scope_class.type,
                                    is_cdef=True)
            node.needs_outer_scope = True
        for name, entry in in_closure:
            class_scope.declare_var(pos=entry.pos,
                                    name=entry.name,
                                    cname=entry.cname,
                                    type=entry.type,
                                    is_cdef=True)
        node.needs_closure = True
        # Do it here because other classes are already checked
        target_module_scope.check_c_class(func_scope.scope_class)

    def visit_LambdaNode(self, node):
        was_in_lambda = self.in_lambda
        self.in_lambda = True
        self.create_class_from_scope(node.def_node, self.module_scope, node)
        self.visitchildren(node)
        self.in_lambda = was_in_lambda
        return node

    def visit_FuncDefNode(self, node):
        if self.in_lambda:
            self.visitchildren(node)
            return node
        if node.needs_closure or self.path:
            self.create_class_from_scope(node, self.module_scope)
            self.path.append(node)
            self.visitchildren(node)
            self.path.pop()
        return node


class GilCheck(VisitorTransform):
    """
    Call `node.gil_check(env)` on each node to make sure we hold the
    GIL when we need it.  Raise an error when on Python operations
    inside a `nogil` environment.
    """
    def __call__(self, root):
        self.env_stack = [root.scope]
        self.nogil = False
        return super(GilCheck, self).__call__(root)

    def visit_FuncDefNode(self, node):
        self.env_stack.append(node.local_scope)
        was_nogil = self.nogil
        self.nogil = node.local_scope.nogil
        if self.nogil and node.nogil_check:
            node.nogil_check(node.local_scope)
        self.visitchildren(node)
        self.env_stack.pop()
        self.nogil = was_nogil
        return node

    def visit_GILStatNode(self, node):
        env = self.env_stack[-1]
        if self.nogil and node.nogil_check: node.nogil_check()
        was_nogil = self.nogil
        self.nogil = (node.state == 'nogil')
        self.visitchildren(node)
        self.nogil = was_nogil
        return node

    def visit_Node(self, node):
        if self.env_stack and self.nogil and node.nogil_check:
            node.nogil_check(self.env_stack[-1])
        self.visitchildren(node)
        return node


class TransformBuiltinMethods(EnvTransform):

    def visit_SingleAssignmentNode(self, node):
        if node.declaration_only:
            return None
        else:
            self.visitchildren(node)
            return node

    def visit_AttributeNode(self, node):
        self.visitchildren(node)
        return self.visit_cython_attribute(node)

    def visit_NameNode(self, node):
        return self.visit_cython_attribute(node)

    def visit_cython_attribute(self, node):
        attribute = node.as_cython_attribute()
        if attribute:
            if attribute == u'compiled':
                node = ExprNodes.BoolNode(node.pos, value=True)
            elif attribute == u'NULL':
                node = ExprNodes.NullNode(node.pos)
            elif attribute in (u'set', u'frozenset'):
                node = ExprNodes.NameNode(node.pos, name=EncodedString(attribute),
                                          entry=self.current_env().builtin_scope().lookup_here(attribute))
            elif not PyrexTypes.parse_basic_type(attribute):
                error(node.pos, u"'%s' not a valid cython attribute or is being used incorrectly" % attribute)
        return node

    def visit_SimpleCallNode(self, node):

        # locals builtin
        if isinstance(node.function, ExprNodes.NameNode):
            if node.function.name == 'locals':
                lenv = self.current_env()
                entry = lenv.lookup_here('locals')
                if entry:
                    # not the builtin 'locals'
                    return node
                if len(node.args) > 0:
                    error(self.pos, "Builtin 'locals()' called with wrong number of args, expected 0, got %d" % len(node.args))
                    return node
                pos = node.pos
                items = [ ExprNodes.DictItemNode(pos,
                                                 key=ExprNodes.StringNode(pos, value=var),
                                                 value=ExprNodes.NameNode(pos, name=var))
                          for var in lenv.entries ]
                return ExprNodes.DictNode(pos, key_value_pairs=items)

        # cython.foo
        function = node.function.as_cython_attribute()
        if function:
            if function in InterpretCompilerDirectives.unop_method_nodes:
                if len(node.args) != 1:
                    error(node.function.pos, u"%s() takes exactly one argument" % function)
                else:
                    node = InterpretCompilerDirectives.unop_method_nodes[function](node.function.pos, operand=node.args[0])
            elif function in InterpretCompilerDirectives.binop_method_nodes:
                if len(node.args) != 2:
                    error(node.function.pos, u"%s() takes exactly two arguments" % function)
                else:
                    node = InterpretCompilerDirectives.binop_method_nodes[function](node.function.pos, operand1=node.args[0], operand2=node.args[1])
            elif function == u'cast':
                if len(node.args) != 2:
                    error(node.function.pos, u"cast() takes exactly two arguments")
                else:
                    type = node.args[0].analyse_as_type(self.current_env())
                    if type:
                        node = ExprNodes.TypecastNode(node.function.pos, type=type, operand=node.args[1])
                    else:
                        error(node.args[0].pos, "Not a type")
            elif function == u'sizeof':
                if len(node.args) != 1:
                    error(node.function.pos, u"sizeof() takes exactly one argument")
                else:
                    type = node.args[0].analyse_as_type(self.current_env())
                    if type:
                        node = ExprNodes.SizeofTypeNode(node.function.pos, arg_type=type)
                    else:
                        node = ExprNodes.SizeofVarNode(node.function.pos, operand=node.args[0])
            elif function == 'cmod':
                if len(node.args) != 2:
                    error(node.function.pos, u"cmod() takes exactly two arguments")
                else:
                    node = ExprNodes.binop_node(node.function.pos, '%', node.args[0], node.args[1])
                    node.cdivision = True
            elif function == 'cdiv':
                if len(node.args) != 2:
                    error(node.function.pos, u"cdiv() takes exactly two arguments")
                else:
                    node = ExprNodes.binop_node(node.function.pos, '/', node.args[0], node.args[1])
                    node.cdivision = True
            elif function == u'set':
                node.function = ExprNodes.NameNode(node.pos, name=EncodedString('set'))
            else:
                error(node.function.pos, u"'%s' not a valid cython language construct" % function)

        self.visitchildren(node)
        return node


class DebugTransform(CythonTransform):
    """
    Create debug information and all functions' visibility to extern in order
    to enable debugging.
    """

    def __init__(self, context, options, result):
        super(DebugTransform, self).__init__(context)
        self.visited = cython.set()
        # our treebuilder and debug output writer
        # (see Cython.Debugger.debug_output.CythonDebugWriter)
        self.tb = self.context.gdb_debug_outputwriter
        #self.c_output_file = options.output_file
        self.c_output_file = result.c_file

        # Closure support, basically treat nested functions as if the AST were
        # never nested
        self.nested_funcdefs = []

        # tells visit_NameNode whether it should register step-into functions
        self.register_stepinto = False

    def visit_ModuleNode(self, node):
        self.tb.module_name = node.full_module_name
        attrs = dict(
            module_name=node.full_module_name,
            filename=node.pos[0].filename,
            c_filename=self.c_output_file)

        self.tb.start('Module', attrs)

        # serialize functions
        self.tb.start('Functions')
        # First, serialize functions normally...
        self.visitchildren(node)

        # ... then, serialize nested functions
        for nested_funcdef in self.nested_funcdefs:
            self.visit_FuncDefNode(nested_funcdef)

        self.register_stepinto = True
        self.serialize_modulenode_as_function(node)
        self.register_stepinto = False
        self.tb.end('Functions')

        # 2.3 compatibility. Serialize global variables
        self.tb.start('Globals')
        entries = {}

        for k, v in node.scope.entries.iteritems():
            if (v.qualified_name not in self.visited and not
                v.name.startswith('__pyx_') and not
                v.type.is_cfunction and not
                v.type.is_extension_type):
                entries[k]= v

        self.serialize_local_variables(entries)
        self.tb.end('Globals')
        # self.tb.end('Module') # end Module after the line number mapping in
        # Cython.Compiler.ModuleNode.ModuleNode._serialize_lineno_map
        return node

    def visit_FuncDefNode(self, node):
        self.visited.add(node.local_scope.qualified_name)

        if getattr(node, 'is_wrapper', False):
            return node

        if self.register_stepinto:
            self.nested_funcdefs.append(node)
            return node

        # node.entry.visibility = 'extern'
        if node.py_func is None:
            pf_cname = ''
        else:
            pf_cname = node.py_func.entry.func_cname

        attrs = dict(
            name=node.entry.name,
            cname=node.entry.func_cname,
            pf_cname=pf_cname,
            qualified_name=node.local_scope.qualified_name,
            lineno=str(node.pos[1]))

        self.tb.start('Function', attrs=attrs)

        self.tb.start('Locals')
        self.serialize_local_variables(node.local_scope.entries)
        self.tb.end('Locals')

        self.tb.start('Arguments')
        for arg in node.local_scope.arg_entries:
            self.tb.start(arg.name)
            self.tb.end(arg.name)
        self.tb.end('Arguments')

        self.tb.start('StepIntoFunctions')
        self.register_stepinto = True
        self.visitchildren(node)
        self.register_stepinto = False
        self.tb.end('StepIntoFunctions')
        self.tb.end('Function')

        return node

    def visit_NameNode(self, node):
        if (self.register_stepinto and
            node.type.is_cfunction and
            getattr(node, 'is_called', False) and
            node.entry.func_cname is not None):
            # don't check node.entry.in_cinclude, as 'cdef extern: ...'
            # declared functions are not 'in_cinclude'.
            # This means we will list called 'cdef' functions as
            # "step into functions", but this is not an issue as they will be
            # recognized as Cython functions anyway.
            attrs = dict(name=node.entry.func_cname)
            self.tb.start('StepIntoFunction', attrs=attrs)
            self.tb.end('StepIntoFunction')

        self.visitchildren(node)
        return node

    def serialize_modulenode_as_function(self, node):
        """
        Serialize the module-level code as a function so the debugger will know
        it's a "relevant frame" and it will know where to set the breakpoint
        for 'break modulename'.
        """
        name = node.full_module_name.rpartition('.')[-1]

        cname_py2 = 'init' + name
        cname_py3 = 'PyInit_' + name

        py2_attrs = dict(
            name=name,
            cname=cname_py2,
            pf_cname='',
            # Ignore the qualified_name, breakpoints should be set using
            # `cy break modulename:lineno` for module-level breakpoints.
            qualified_name='',
            lineno='1',
            is_initmodule_function="True",
        )

        py3_attrs = dict(py2_attrs, cname=cname_py3)

        self._serialize_modulenode_as_function(node, py2_attrs)
        self._serialize_modulenode_as_function(node, py3_attrs)

    def _serialize_modulenode_as_function(self, node, attrs):
        self.tb.start('Function', attrs=attrs)

        self.tb.start('Locals')
        self.serialize_local_variables(node.scope.entries)
        self.tb.end('Locals')

        self.tb.start('Arguments')
        self.tb.end('Arguments')

        self.tb.start('StepIntoFunctions')
        self.register_stepinto = True
        self.visitchildren(node)
        self.register_stepinto = False
        self.tb.end('StepIntoFunctions')

        self.tb.end('Function')

    def serialize_local_variables(self, entries):
        for entry in entries.values():
            if entry.type.is_pyobject:
                vartype = 'PythonObject'
            else:
                vartype = 'CObject'

            if entry.from_closure:
                # We're dealing with a closure where a variable from an outer
                # scope is accessed, get it from the scope object.
                cname = '%s->%s' % (Naming.cur_scope_cname,
                                    entry.outer_entry.cname)

                qname = '%s.%s.%s' % (entry.scope.outer_scope.qualified_name,
                                      entry.scope.name,
                                      entry.name)
            elif entry.in_closure:
                cname = '%s->%s' % (Naming.cur_scope_cname,
                                    entry.cname)
                qname = entry.qualified_name
            else:
                cname = entry.cname
                qname = entry.qualified_name

            if not entry.pos:
                # this happens for variables that are not in the user's code,
                # e.g. for the global __builtins__, __doc__, etc. We can just
                # set the lineno to 0 for those.
                lineno = '0'
            else:
                lineno = str(entry.pos[1])

            attrs = dict(
                name=entry.name,
                cname=cname,
                qualified_name=qname,
                type=vartype,
                lineno=lineno)

            self.tb.start('LocalVar', attrs)
            self.tb.end('LocalVar')

