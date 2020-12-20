# functions to transform a c class into a dataclass

from collections import OrderedDict

from .Errors import error, warning
from . import ExprNodes, Nodes, PyrexTypes
from .Code import UtilityCode, TempitaUtilityCode
from .Visitor import VisitorTransform
from . import UtilNodes, Builtin, Naming
from .StringEncoding import BytesLiteral, EncodedString
from .TreeFragment import TreeFragment
from .ParseTreeTransforms import (NormalizeTree, SkipDeclarations, AnalyseDeclarationsTransform,
                                  MarkClosureVisitor)

def _make_module_callnode_and_utilcode(pos, name, py_code):
    loader_utilitycode = TempitaUtilityCode.load_cached("SpecificModuleLoader", "Dataclasses.c",
                                                        context={'name': name, 'py_code': py_code})
    return (ExprNodes.PythonCapiCallNode(pos, "__Pyx_Load_%s_Module" % name,
                                PyrexTypes.CFuncType(PyrexTypes.py_object_type, []),
                                utility_code = loader_utilitycode,
                                args=[]),
            loader_utilitycode)

def make_dataclasses_module_callnode_and_utilcode(pos):
    python_utility_code = UtilityCode.load_cached("Dataclasses_fallback", "Dataclasses.py")
    python_utility_code = EncodedString(python_utility_code.impl)
    return _make_module_callnode_and_utilcode(pos, "dataclasses", python_utility_code.as_c_string_literal())
def make_dataclasses_module_callnode(pos):
    return make_dataclasses_module_callnode_and_utilcode(pos)[0]
def make_typing_module_callnode(pos):
    python_utility_code = UtilityCode.load_cached("Typing_fallback", "Dataclasses.py")
    python_utility_code = EncodedString(python_utility_code.impl)
    return _make_module_callnode_and_utilcode(pos, "typing", python_utility_code.as_c_string_literal())[0]

_INTERNAL_DEFAULTSHOLDER_NAME = EncodedString('__pyx_dataclass_defaults')

def make_common_utilitycode(scope):
    scope.global_scope().use_utility_code(make_dataclasses_module_callnode_and_utilcode(None)[1])


class RemoveAssignments(VisitorTransform, SkipDeclarations):
    def __init__(self, names):
        super(RemoveAssignments, self).__init__()
        self.names = names
        self.removed_assignments = {}

    def visit_CClassNode(self, node):
        self.visitchildren(node)
        return node

    def visit_PyClassNode(self, node):
        return node  # go no further

    def visit_FuncDefNode(self, node):
        return node  # go no further

    def visit_SingleAssignmentNode(self, node):
        if node.lhs.is_name and node.lhs.name in self.names:
            if node.lhs.name in self.removed_assignments:
                warning(node.pos, ("Multiple assignments for '%s' in dataclass; "
                                   "using most recent") % node.lhs.name, 1)
            self.removed_assignments[node.lhs.name] = node.rhs
            return []
        return node

    # I believe cascaded assignment is always a syntax error with decorators
    # so can be ignored

    def visit_Node(self, node):
        self.visitchildren(node)
        return node

class _MISSING_TYPE:
    pass
MISSING = _MISSING_TYPE()

def process_class_get_fields(node):
    _TrueNode = ExprNodes.BoolNode(node.pos, value=True)
    _FalseNode = ExprNodes.BoolNode(node.pos, value=False)
    _NoneNode = ExprNodes.NoneNode(node.pos)

    class Field:
        """
        Field is based on the dataclasses.field class from the standard library module.
        It is used internally during the generation of Cython dataclasses to keep track
        of the settings for individual attributes.

        Attributes of this class are stored as nodes so they can be used in code construction
        more readily (i.e. we store BoolNode rather than bool)
        The class (+ _TrueNode, _FalseNode and _NoneNode) are defined inside a function
        that when _TrueNode (etc) are used as default arguments they can have a useful pos
        """
        default = MISSING
        default_factory = MISSING
        private = False
        def __init__(self, default=MISSING, default_factory=MISSING,
                        repr=_TrueNode, hash=_NoneNode, init=_TrueNode,
                        compare=_TrueNode, metadata=_NoneNode,
                        is_initvar=False):
            if default is not MISSING:
                self.default = default
            if default_factory is not MISSING:
                self.default_factory = default_factory
            self.repr = repr
            self.hash = hash
            self.init = init
            self.compare = compare
            self.metadata = metadata
            self.is_initvar = is_initvar

            for field_name in ("repr", "hash", "init", "compare", "metadata"):
                field_value = getattr(self, field_name)
                if not field_value.is_literal:
                    error(field_value.pos, "cython.dataclasses.field parameter '%s' must be a literal value"
                            % field_name)

    var_entries = node.scope.var_entries
    # order of definition is used in the dataclass
    var_entries = sorted(var_entries, key=lambda entry: entry.pos)
    var_names = [ entry.name for entry in var_entries ]

    # remove assignments for stat_list
    transform = RemoveAssignments(var_names)
    transform(node)

    if node.base_type and node.base_type.dataclass_fields:
        fields = node.base_type.dataclass_fields.copy()
    else:
        fields = OrderedDict()
    for entry in var_entries:
        name = entry.name
        is_initvar = entry.type.is_dataclasses_initvar
        if name in transform.removed_assignments:
            assignment = transform.removed_assignments[name]
            if (isinstance(assignment, ExprNodes.CallNode)
                    and assignment.function.as_cython_attribute() == "dataclasses.field"):
                # I believe most of this is well-enforced when it's treated as a directive
                # but it doesn't hurt to make sure
                if (not isinstance(assignment, ExprNodes.GeneralCallNode)
                        or not isinstance(assignment.positional_args, ExprNodes.TupleNode)
                        or assignment.positional_args.args
                        or not isinstance(assignment.keyword_args, ExprNodes.DictNode)):
                    error(assignment.pos, "Call to 'cython.dataclasses.field' must only consist "
                          "of compile-time keyword arguments")
                    continue
                keyword_args = { k.value: v for k, v in assignment.keyword_args.key_value_pairs }
                if 'default' in keyword_args and 'default_factory' in keyword_args:
                    error(assignment.pos, "You cannot specify both 'default' and 'default_factory'"
                          " for a dataclass member")
                    continue
                field = Field(**keyword_args)
            else:
                if isinstance(assignment, ExprNodes.CallNode):
                    func = assignment.function
                    if ((func.is_name and func.name == "field")
                            or (isinstance(func, ExprNodes.AttributeNode)
                                and func.attribute == "field")):
                        warning(assignment.pos, "Do you mean cython.dataclasses.field instead?", 1)
                if assignment.type in [Builtin.list_type,
                                    Builtin.dict_type,
                                    Builtin.set_type]:
                    # The standard library module generates a TypeError at runtime
                    # in this situation
                    error(assignment.pos, "Mutable default passed argument for '{0}' - "
                          "use 'default_factory' instead".format(name))

                field = Field(default=assignment)
        else:
            field = Field()
        field.is_initvar = is_initvar
        if entry.visibility == "private":
            field.private = True
        fields[name] = field
    node.entry.type.dataclass_fields = fields
    return fields

def handle_cclass_dataclass(node, dataclass_args, analyse_decs_transform):
    from .ExprNodes import (AttributeNode, TupleNode, NameNode,
                            GeneralCallNode, DictNode,
                            IdentifierStringNode, BoolNode, DictItemNode)
    # default argument values from https://docs.python.org/3/library/dataclasses.html
    kwargs = dict(init=True, repr=True, eq=True,
                  order=False, unsafe_hash=False, frozen=False)
    if dataclass_args is not None:
        if dataclass_args[0]:
            error(node.pos, "cython.dataclasses.dataclass takes no positional arguments")
        for k, v in dataclass_args[1].items():
            if k not in kwargs:
                error(node.pos,
                      "Unrecognised keyword argument '{0}' to cython.dataclasses.dataclass".format(k))
            if not isinstance(v, ExprNodes.BoolNode):
                error(node.pos,
                      "Arguments to cython.dataclasses.dataclass must be True or False")
            kwargs[k] = v

    dataclass_scope = make_common_utilitycode(node.scope)
    fields = process_class_get_fields(node)

    dataclass_module = make_dataclasses_module_callnode(node.pos)

    # create __dataclass_params__ attribute
    dataclass_params_func = AttributeNode(node.pos, obj=dataclass_module,
                                            attribute=EncodedString("_DataclassParams"))
    dataclass_params_keywords = DictNode.from_pairs(node.pos,
            [ (IdentifierStringNode(node.pos, value=EncodedString(k)),
                BoolNode(node.pos, value=v))
                for k, v in kwargs.items() ])
    dataclass_params = GeneralCallNode(node.pos,
                                    function = dataclass_params_func,
                                    positional_args = TupleNode(node.pos, args=[]),
                                    keyword_args = dataclass_params_keywords)
    dataclass_params_assignment = \
        Nodes.SingleAssignmentNode(node.pos,
                        lhs = NameNode(node.pos,
                                        name=EncodedString("__dataclass_params__")),
                        rhs = dataclass_params)

    dataclass_fields_stats = _setup_dataclass_fields(node, fields, dataclass_module)

    stats = Nodes.StatListNode(node.pos,
                               stats=[dataclass_params_assignment]
                                    + dataclass_fields_stats)

    init_stats = generate_init_code(kwargs['init'], node, fields)
    repr_stats = generate_repr_code(kwargs['repr'], node, fields)
    eq_stats = generate_eq_code(kwargs['eq'], node, fields)
    order_stats = generate_order_code(kwargs['order'], node, fields)
    hash_stats = generate_hash_code(kwargs['unsafe_hash'], kwargs['eq'], kwargs['frozen'],
                       node, fields)

    stats.stats = stats.stats + init_stats + repr_stats + eq_stats + order_stats + hash_stats

    # turn off annotation typing, so all arguments to __init__ are accepted as
    # generic objects and thus can accept _HAS_DEFAULT_FACTORY
    # type conversion comes later
    comp_directives = Nodes.CompilerDirectivesNode(node.pos,
        directives = node.scope.directives.copy(),
        body=stats)
    comp_directives.directives['annotation_typing'] = False

    comp_directives.analyse_declarations(node.scope)
    # probably already in this scope, but it doesn't hurt to make sure
    analyse_decs_transform.enter_scope(node, node.scope)
    analyse_decs_transform.visit(comp_directives)
    analyse_decs_transform.exit_scope()

    RemoveDontAnalyseDeclarations()(comp_directives)
    node.body.stats.append(comp_directives)

def generate_init_code(init, node, fields):
    if not init or node.scope.lookup_here("__init__"):
        return []
    # selfname behaviour copied from the cpython module
    selfname = "__dataclass_self__" if "self" in fields else "self"
    args = [selfname]

    placeholders = {}
    placeholder_count = [0]

    # create a temp to get _HAS_DEFAULT_FACTORY
    dataclass_module = make_dataclasses_module_callnode(node.pos)
    has_default_factory = ExprNodes.AttributeNode(node.pos,
                                        obj = dataclass_module,
                                        attribute = EncodedString("_HAS_DEFAULT_FACTORY"))

    def get_placeholder_name():
        while True:
            name = "PLACEHOLDER_%s" % placeholder_count[0]
            if (name not in placeholders
                    and name not in fields):
                # make sure name isn't already used and doesn't
                # conflict with a variable name (which is unlikely but possible)
                break
            placeholder_count[0] += 1
        return name

    default_factory_placeholder = get_placeholder_name()
    placeholders[default_factory_placeholder] = has_default_factory

    seen_default = False
    for name, field in fields.items():
        if not field.init.value:
            continue
        entry = node.scope.lookup(name)
        annotation = entry.pep563_annotation
        if annotation:
            annotation = u": %s" % annotation
        else:
            annotation = u""
        assignment = u''
        if field.default is not MISSING or field.default_factory is not MISSING:
            seen_default = True
            if field.default_factory is not MISSING:
                ph_name = default_factory_placeholder
            else:
                ph_name = get_placeholder_name()
                placeholders[ph_name] = field.default  # should be node
            assignment = u" = %s" % ph_name
        elif seen_default:
            error(entry.pos, ("non-default argument %s follows default argument "
                             "in dataclass __init__") % name)
            return []

        args.append(u"%s%s%s" % (name, annotation, assignment))
    args = u", ".join(args)
    func_call = u"def __init__(%s):" % args

    code_lines = [func_call,
                  "    pass",  # just in-case it's an empty body
                  ]
    for name, field in fields.items():
        if field.is_initvar:
            continue
        if field.default_factory is MISSING:
            if field.init.value:
                code_lines.append(u"    %s.%s = %s" % (selfname, name, name))
        else:
            ph_name = get_placeholder_name()
            placeholders[ph_name] = field.default_factory
            if field.init.value:
                code_lines.append(u"    if %s is %s:"
                                % (name, default_factory_placeholder))
                code_lines.append(u"        %s.%s = %s()"
                                % (selfname, name, ph_name))
                code_lines.append(u"    else:")
                code_lines.append(u"        %s.%s = %s" % (selfname, name, name))
            else:
                # still need to use the default factory to initialize
                code_lines.append(u"    %s.%s = %s()"
                                  % (selfname, name, ph_name))
    if node.scope.lookup("__post_init__"):
        post_init_vars = ", ".join(name for name, field in fields.items()
                                    if field.is_initvar)
        code_lines.append("    %s.__post_init__(%s)" % (selfname, post_init_vars))
    code_lines = u"\n".join(code_lines)

    code_tree = TreeFragment(code_lines, level='c_class',
                             pipeline=[NormalizeTree(node.scope),
                                       ]
                              ).substitute(placeholders)

    return code_tree.stats


def generate_repr_code(repr, node, fields):
    if not repr or node.scope.lookup("__repr__"):
        return []
    code_lines = ["def __repr__(self):"]
    strs = [ u"%s={self.%s}" % (name, name)
            for name, field in fields.items() if field.repr.value and not field.is_initvar ]
    format_string = u", ".join(strs)
    code_lines.append(u"    return f'{type(self).__name__}(%s)'" % format_string)
    code_lines = u"\n".join(code_lines)

    code_tree = TreeFragment(code_lines,
                              level='c_class', pipeline=[NormalizeTree(None)]
                              ).substitute({})
    return code_tree.stats

def generate_cmp_code(op, funcname, node, fields):
    if node.scope.lookup_here(funcname):
        return []  # already exists

    names = [ name for name, field in fields.items()
                if (field.compare.value and not field.is_initvar) ]

    if not names:
        return []  # no comparable types

    code_lines = ["def %s(self, other):" % funcname,
                  "    cdef %s other_cast" % node.class_name,
                  "    try:",
                  "        other_cast = other",
                  "    except TypeError:",
                  "        return NotImplemented"]

    for name in names:
        shared = "if not (self.%s == other_cast.%s):" % (name, name)
        if op == "==":
            code_lines.append("    %s return False" % shared)
        else:
            code_lines.append("    %s return self.%s %s other_cast.%s" %
                              (shared, name, op, name))

    if "=" in op:
        code_lines.append("    return True")
    else:
        code_lines.append("    return False")

    code_lines = u"\n".join(code_lines)

    code_tree = TreeFragment(code_lines,
                              level='c_class', pipeline=[NormalizeTree(None)]
                              ).substitute({})
    return code_tree.stats

def generate_eq_code(eq, node, fields):
    if not eq:
        return []
    return generate_cmp_code("==", "__eq__", node, fields)

def generate_order_code(order, node, fields):
    if not order:
        return []
    stats = []
    for op, name in [("<", "__lt__"),
                     ("<=", "__le__"),
                     (">", "__gt__"),
                     (">=", "__ge__")]:
        stats.extend(generate_cmp_code(op, name, node, fields))
    return stats

def generate_hash_code(unsafe_hash, eq, frozen, node, fields):
    hash_entry = node.scope.lookup_here("__hash__")
    if hash_entry:
        # TODO ideally assignment of __hash__ to None shouldn't trigger this
        # but difficult to get the right information here
        if unsafe_hash:
            error(node.pos, "Request for dataclass unsafe_hash when a '__hash__' function"
                  " already exists")
        return []
    if not unsafe_hash:
        if eq and not frozen:
            return [Nodes.SingleAssignmentNode(node.pos,
                                        lhs = ExprNodes.NameNode(node.pos, name=EncodedString("__hash__")),
                                        rhs = ExprNodes.NoneNode(node.pos))]
        if not eq:
            return []

    names = [ name for name, field in fields.items()
                if (not field.is_initvar and
                    (field.compare.value if field.hash.value is None else field.hash.value)) ]
    if not names:
        return []  # nothing to hash

    # make a tuple of the hashes
    tpl = u", ".join(u"hash(self.%s)" % name for name in names )

    # if we're here we want to generate a hash
    code_lines = u"""def __hash__(self):
    return hash((%s))
""" % tpl
    code_tree = TreeFragment(code_lines,
                              level='c_class', pipeline=[NormalizeTree(None)]
                              ).substitute({})
    return code_tree.stats


class GetTypeNode(ExprNodes.ExprNode):
    # Tries to return a pytype_type if possible. However contains
    # some fallback provision if it turns out not to resolve to a Python object
    # Initialize with "entry"

    subexprs = []

    def __init__(self, entry):
        super(GetTypeNode, self).__init__(entry.pos, entry=entry)

    def analyse_types(self, env):
        type = self.entry.type

        if type.is_extension_type or type.is_builtin_type:
            return ExprNodes.RawCNameExprNode(self.pos, Builtin.type_type,
                                                type.typeptr_cname).analyse_types(env)
        else:
            names = None
            py_name = type.py_type_name()
            # int types can return "(int, long)"
            if py_name:
                names = py_name.split(",")
                names = [ n.strip("() ") for n in names ]
            if names:
                for name in names:
                    name = EncodedString(name)
                    nn = ExprNodes.NameNode(self.pos, name=name)
                    # try to set the entry now to prevent the user accidentally shadowing
                    # the name
                    nn.entry = env.builtin_scope().lookup(name)
                    if not nn.entry:
                        try:
                            nn.entry = env.declare_builtin(name, self.pos)
                        except:
                            pass  # not convinced a failure means much
                    if nn.entry:
                        return nn.analyse_types(env)

        # otherwise we're left to return a string
        s = self.entry.pep563_annotation
        if not s:
            s = self.entry.type.declaration_code("", for_display=1)
        return ExprNodes.StringNode(self.pos, value=s).analyse_types(env)

class DontAnalyseDeclarationsNode(ExprNodes.ExprNode):
    # arg    ExprNode
    #
    # This is designed to wrap stuff that's already been analysed
    # so that lambdas aren't redeclared for example
    # and then immediately be replaced

    subexprs = []

    def analyse_declarations(self, env):
        return

class RemoveDontAnalyseDeclarations(VisitorTransform):
    def visit_DontAnalyseDeclarationsNode(self, node):
        return node.arg

    def visit_Node(self, node):
        self.visitchildren(node)
        return node


class FieldsValueNode(ExprNodes.ExprNode):
    # largely just forwards arg. Allows it to be coerced to a Python object
    # if possible, and if not then generates a sensible backup string
    subexprs = ['arg']

    def __init__(self, pos, arg):
        super(FieldsValueNode, self).__init__(pos, arg=arg)

    def analyse_types(self, env):
        self.arg.analyse_types(env)
        self.type = self.arg.type
        return self

    def coerce_to_pyobject(self, env):
        if self.arg.type.can_coerce_to_pyobject(env):
            return self.arg.coerce_to_pyobject(env)
        else:
            # A string representation of the code that gave the field seems like a reasonable
            # fallback. This'll mostly happen for "default" and "default_factory" where the
            # type may be a C-type that can't be converted to Python.
            return self._make_string()

    def _make_string(self):
        from .AutoDocTransforms import AnnotationWriter
        writer = AnnotationWriter(description="Dataclass field")
        string = writer.write(self.arg)
        return ExprNodes.StringNode(self.pos, value=EncodedString(string))

    def generate_evaluation_code(self, code):
        return self.arg.generate_evaluation_code(code)


def _setup_dataclass_fields(node, fields, dataclass_module):
    from .ExprNodes import (AttributeNode, TupleNode, NameNode,
                            GeneralCallNode, DictNode,
                            IdentifierStringNode, BoolNode, DictItemNode,
                            CloneNode)

    # For defaults and default_factories containing things like lambda,
    # they're already declared in the class scope, and it creates a big
    # problem if multiple copies are floating around in both the __init__
    # function, and in the __dataclass_fields__ structure.
    # Therefore, create module-level constants holding these values and
    # pass those around instead
    variables_assignment_stats = []
    for name, field in fields.items():
        if field.private:
            continue  # doesn't appear in the public interface
        for attrname in [ "default", "default_factory" ]:
            f_def = getattr(field, attrname)
            if f_def is MISSING or f_def.is_literal or f_def.is_name:
                # some simple cases where we don't need to set up
                # the variable as a module-level constant
                continue
            global_scope = node.scope.global_scope()
            module_field_name = global_scope.mangle(global_scope.mangle(
                                    Naming.dataclass_field_default_cname,
                                    node.class_name), name)
            # create an entry in the global scope for this variable to live
            nn = NameNode(f_def.pos, name=EncodedString(module_field_name))
            nn.entry = global_scope.declare_var(nn.name, type=f_def.type or PyrexTypes.unspecified_type,
                                                pos=f_def.pos, cname=nn.name, is_cdef=1)
            # replace the field so that future users just receive the namenode
            setattr(field, attrname, nn)

            variables_assignment_stats.append(
                Nodes.SingleAssignmentNode(f_def.pos,
                                           lhs = nn,
                                           rhs = DontAnalyseDeclarationsNode(f_def.pos, arg=f_def)))

    placeholders = {}
    field_func = AttributeNode(node.pos, obj = dataclass_module,
                                    attribute=EncodedString("field"))
    dc_fields = DictNode(node.pos, key_value_pairs=[])
    dc_fields_namevalue_assignments = []
    for name, field in fields.items():
        if field.private:
            continue  # doesn't appear in the public interface
        placeholder_name = "PLACEHOLDER_%s" % name
        placeholders[placeholder_name] = GetTypeNode(node.scope.entries[name])

        if field.is_initvar:
            continue

        dc_field_keywords = DictNode.from_pairs(node.pos,
            [ (IdentifierStringNode(node.pos, value=EncodedString(k)),
               FieldsValueNode(node.pos, arg=v))
                for k, v in field.__dict__.items() if k not in ["is_initvar", "private"] ])
        dc_field_call = GeneralCallNode(node.pos, function = field_func,
                                    positional_args = TupleNode(node.pos, args=[]),
                                    keyword_args = dc_field_keywords)
        dc_fields.key_value_pairs.append(
            DictItemNode(node.pos,
                key=IdentifierStringNode(node.pos, value=EncodedString(name)),
                value=dc_field_call))
        dc_fields_namevalue_assignments.append(
            u"""
__dataclass_fields__[{0!r}].name = {0!r}
__dataclass_fields__[{0!r}].type = {1}
""".format(name, placeholder_name))

    dataclass_fields_assignment = \
        Nodes.SingleAssignmentNode(node.pos,
                        lhs = ExprNodes.NameNode(node.pos,
                                        name=EncodedString("__dataclass_fields__")),
                        rhs = dc_fields)

    dc_fields_namevalue_assignments = u"\n".join(dc_fields_namevalue_assignments)
    dc_fields_namevalue_assignments = TreeFragment(dc_fields_namevalue_assignments,
                                                   level="c_class",
                                                   pipeline=[NormalizeTree(None)])
    dc_fields_namevalue_assignments = dc_fields_namevalue_assignments.substitute(placeholders)

    return (variables_assignment_stats
            + [dataclass_fields_assignment]
            + dc_fields_namevalue_assignments.stats)
