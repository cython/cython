"""
NoexceptInference.py -- Infer noexcept for provably non-raising cpdef functions.

Three passes:
  _CollectCFuncDefs   - record every CFuncDefNode in the module tree.
  _BodyRaiseAnalysis  - memoized per-function body raise analysis.
  InferNoexcept       - orchestrator transform (inserted in Pipeline.py).
"""

from .Visitor import CythonTransform, TreeVisitor
from . import Nodes, ExprNodes, PyrexTypes, Options, UtilNodes


# ---------------------------------------------------------------------------
# Cross-module facts (LTO / cimport_from_pyx multi-source compilation)
#
# When several modules are compiled in one invocation (compile_multiple), a
# first frontend-only phase collects, per module, which functions were proven
# never-raising.  Consumers cimporting those modules from .pyx only re-analyse
# *declarations* (create_pyx_as_pxd_pipeline stops at
# AnalyseDeclarationsTransform), so they cannot re-derive the inference — the
# facts are injected instead and applied to the cimported entries, making
# cross-module call sites (vtabptr dispatch, direct LTO calls) check-free.
#
# Fact keys (all name-based, stable across compilations of the same source):
#   ('f', func_name)                          module-level function
#   ('m', class_name, method_name)            final method of a cdef class
#   ('p', class_name, prop_name, accessor)    final-class property accessor
# ---------------------------------------------------------------------------

_external_facts = {}  # {module_name: {fact_key: True}}


def set_external_facts(facts):
    """Install the cross-module facts for this (worker) process."""
    global _external_facts
    _external_facts = facts or {}


def _external_fact_for_entry(entry):
    """Return the cross-module fact ('entry' | 'direct') recorded for this
    (consumer-side, cimported) entry, or None."""
    if not _external_facts or entry is None:
        return None
    key = _fact_key_for_entry(entry)
    if key is None:
        return None
    scope = entry.scope
    while scope is not None and not scope.is_module_scope:
        scope = scope.outer_scope
    if scope is None:
        return None
    facts = _external_facts.get(scope.qualified_name)
    if not facts:
        return None
    return facts.get(key)


def _fact_key_for_entry(entry):
    scope = entry.scope
    if scope is None:
        return None
    if scope.is_module_scope:
        return ('f', entry.name)
    if getattr(scope, 'is_property_scope', False):
        parent_type = getattr(scope, 'parent_type', None)
        type_scope = getattr(parent_type, 'scope', None) if parent_type is not None else None
        if type_scope is None:
            return None
        return ('p', type_scope.name, scope.name, entry.name)
    if getattr(scope, 'is_c_class_scope', False):
        return ('m', scope.name, entry.name)
    return None


# ---------------------------------------------------------------------------
# Phase 1: collect all CFuncDefNode instances
# ---------------------------------------------------------------------------

class _CollectCFuncDefs(CythonTransform):
    """Walk the module recording every CFuncDefNode.

    Results:
      by_entry  : {id(entry): CFuncDefNode}
      by_cname  : {func_cname: CFuncDefNode}  (only entries with a plain cname)
      func_directives : {id(node): directives-dict}
    """

    def __init__(self, context):
        super().__init__(context)
        self.by_entry = {}
        self.by_cname = {}
        self.func_directives = {}

    def visit_CFuncDefNode(self, node):
        entry = node.entry
        if entry is not None:
            self.by_entry[id(entry)] = node
            # Index only by func_cname (the actual unique C symbol name).
            # entry.cname for cmethods is the short vtable member name (e.g.
            # 'get_x'), which collides across classes and is never what a
            # direct-call function node carries.
            func_cname = getattr(entry, 'func_cname', None)
            if func_cname and '->' not in func_cname:
                self.by_cname[func_cname] = node
        self.func_directives[id(node)] = self.current_directives
        self.visitchildren(node)
        return node

    def visit_Node(self, node):
        self.visitchildren(node)
        return node


# ---------------------------------------------------------------------------
# Phase 2: conservative body raise analysis
# ---------------------------------------------------------------------------

_IN_PROGRESS = object()  # cycle sentinel


class _BodyRaiseAnalysis(TreeVisitor):
    """Memoized body-cannot-raise analysis.

    visit_Node fallback returns False (unsafe).  Each handler must check
    that all conditions hold and recurse into safe sub-nodes explicitly.
    """

    def __init__(self, by_entry, by_cname, func_directives, module_directives):
        super().__init__()
        self._memo = {}          # id(funcdef) -> bool | _IN_PROGRESS
        self.by_entry = by_entry
        self.by_cname = by_cname
        self.func_directives = func_directives
        self.module_directives = module_directives

    # ------------------------------------------------------------------
    # Public entry-point
    # ------------------------------------------------------------------

    def body_cannot_raise(self, funcdef):
        key = id(funcdef)
        cached = self._memo.get(key, None)
        if cached is _IN_PROGRESS:
            return False   # cycle → conservatively unsafe
        if cached is not None:
            return cached
        self._memo[key] = _IN_PROGRESS
        result = self._analyse_body(funcdef)
        self._memo[key] = result
        return result

    def _analyse_body(self, funcdef):
        # Profiling/linetrace inject trace hooks that can raise, regardless of
        # the body's own statements.  Gate on the directives in effect at the
        # function's definition (a per-function @cython.profile(True) is not
        # visible inside funcdef.body).
        directives = self.func_directives.get(id(funcdef), self.module_directives)
        if directives.get('profile') or directives.get('linetrace'):
            return False
        body = funcdef.body
        if body is None:
            return True
        # Identify the override statement to skip.
        override = getattr(funcdef, 'override', None)
        if override is not None:
            # Body should be StatListNode([override, original_body]).
            # Analyse only the non-override stats.
            from .Nodes import StatListNode
            if isinstance(body, StatListNode):
                for stat in body.stats:
                    if stat is override:
                        continue
                    if not self._node_safe(stat):
                        return False
                return True
            # Unexpected structure; fall through to normal analysis.
        return self._node_safe(body)

    # ------------------------------------------------------------------
    # Internal visit dispatching (returns bool: safe=True / unsafe=False)
    # ------------------------------------------------------------------

    def _node_safe(self, node):
        if node is None:
            return True
        # Use the cpdef `visit` entry point: `_visit` is a cdef method of the
        # compiled TreeVisitor and is not visible from Python subclasses.
        return self.visit(node)

    def _children_safe(self, node, attrs=None):
        """Return True iff all children in attrs (or all child_attrs) are safe."""
        if attrs is None:
            attrs = node.child_attrs or []
        for attr in attrs:
            child = getattr(node, attr, None)
            if child is None:
                continue
            if isinstance(child, list):
                for item in child:
                    if item is not None and not self._node_safe(item):
                        return False
            else:
                if not self._node_safe(child):
                    return False
        return True

    # ------------------------------------------------------------------
    # visit_Node: fallback — unsafe (conservative)
    # ------------------------------------------------------------------

    def visit_Node(self, node):
        return False

    # ------------------------------------------------------------------
    # Safe statements
    # ------------------------------------------------------------------

    def visit_StatListNode(self, node):
        for stat in (node.stats or []):
            if stat is not None and not self._node_safe(stat):
                return False
        return True

    def visit_PassStatNode(self, node):
        return True

    def visit_BreakStatNode(self, node):
        return True

    def visit_ContinueStatNode(self, node):
        return True

    def visit_ExprStatNode(self, node):
        return self._node_safe(node.expr)

    def visit_SingleAssignmentNode(self, node):
        return (self._node_safe(node.rhs) and
                self._safe_assignment_target(node.lhs))

    def visit_CascadedAssignmentNode(self, node):
        if not self._node_safe(node.rhs):
            return False
        for lhs in (node.lhs_list or []):
            if not self._safe_assignment_target(lhs):
                return False
        return True

    def visit_ParallelAssignmentNode(self, node):
        for stat in (node.stats or []):
            if stat is not None and not self._node_safe(stat):
                return False
        return True

    def visit_InPlaceAssignmentNode(self, node):
        # ExpandInplaceOperators (which runs earlier in the pipeline) expands
        # every in-place assignment into SingleAssignmentNode + binop (with
        # the proper overflow/zerodivision flags, which we check there) EXCEPT
        # C++ class lhs (operator op= may throw) and buffer indexing.  Both
        # leftovers are unsafe, so any surviving InPlaceAssignmentNode is.
        return False

    def visit_ReturnStatNode(self, node):
        if node.value is None:
            return True
        return self._node_safe(node.value)

    def visit_IfStatNode(self, node):
        for clause in (node.if_clauses or []):
            cond = clause.condition
            if cond is None or cond.type.is_pyobject:
                return False
            if not self._node_safe(cond):
                return False
            if not self._node_safe(clause.body):
                return False
        if node.else_clause is not None:
            if not self._node_safe(node.else_clause):
                return False
        return True

    def visit_WhileStatNode(self, node):
        cond = node.condition
        if cond is None or cond.type.is_pyobject:
            return False
        if not self._node_safe(cond):
            return False
        if not self._node_safe(node.body):
            return False
        if node.else_clause is not None:
            if not self._node_safe(node.else_clause):
                return False
        return True

    def visit_ForFromStatNode(self, node):
        # Safe only for C-typed bounds and target.
        if getattr(node, 'is_py_target', False):
            return False
        for attr in ('target', 'bound1', 'bound2', 'step'):
            child = getattr(node, attr, None)
            if child is not None:
                if child.type.is_pyobject:
                    return False
                if not self._node_safe(child):
                    return False
        if not self._node_safe(node.body):
            return False
        if node.else_clause is not None:
            if not self._node_safe(node.else_clause):
                return False
        return True

    def visit_CriticalSectionStatNode(self, node):
        # Freethreading critical section (frozen-dataclass __init__ wraps its
        # field stores in one).  __Pyx_PyCriticalSection_Begin/End and
        # PyMutex_Lock/Unlock cannot raise; only the args evaluation and the
        # body can.  The finally clauses contain CriticalSectionExitNode(s),
        # vetted like any other statement.
        for arg in (node.args or []):
            if not self._node_safe(arg):
                return False
        return (self._node_safe(node.body) and
                self._node_safe(node.finally_clause) and
                self._node_safe(node.finally_except_clause))

    def visit_CriticalSectionExitNode(self, node):
        return True

    def visit_CompilerDirectivesNode(self, node):
        directives = node.directives
        if directives.get('profile') or directives.get('linetrace'):
            return False
        if directives.get('cdivision_warnings'):
            return False
        # Recurse with these directives in effect (analysis already baked in).
        return self._node_safe(node.body)

    # ------------------------------------------------------------------
    # Safe expressions
    # ------------------------------------------------------------------

    def _visit_ConstNode(self, node):
        return True

    visit_IntNode = _visit_ConstNode
    visit_FloatNode = _visit_ConstNode
    visit_BoolNode = _visit_ConstNode
    visit_NoneNode = _visit_ConstNode
    visit_NullNode = _visit_ConstNode
    visit_CharNode = _visit_ConstNode
    # Pre-built module-level constants: BytesNode, UnicodeNode, StringNode
    visit_BytesNode = _visit_ConstNode
    visit_UnicodeNode = _visit_ConstNode
    visit_StringNode = _visit_ConstNode

    def visit_NameNode(self, node):
        entry = node.entry
        if entry is None:
            return False
        # Python globals / builtins always raise.
        if entry.is_pyglobal or entry.is_builtin:
            return False
        # C globals without cpp_optional are fine.
        if entry.is_cglobal:
            if entry.is_cpp_optional and getattr(node, 'initialized_check', False):
                return False
            return True
        # Local/closure/memslice: raise iff maybe-null + pyobject/memslice.
        if entry.is_local or entry.in_closure or entry.from_closure or entry.type.is_memoryviewslice:
            raise_unbound = (
                (getattr(node, 'cf_maybe_null', False) or getattr(node, 'cf_is_null', False))
                and not getattr(node, 'allow_null', False))
            memslice_check = entry.type.is_memoryviewslice and getattr(node, 'initialized_check', False)
            optional_cpp_check = getattr(entry, 'is_cpp_optional', False) and getattr(node, 'initialized_check', False)
            if raise_unbound and (entry.type.is_pyobject or memslice_check or optional_cpp_check):
                return False
            return True
        # C arguments, C globals, etc.
        return True

    def visit_AttributeNode(self, node):
        if node.is_py_attr:
            return False
        # cproperty reads are converted to SimpleCallNode.for_cproperty_get at
        # analyse time; any surviving cproperty AttributeNode is unexpected —
        # its codegen would call the getter with an error check.
        if node.entry is not None and getattr(node.entry, 'is_cproperty', False):
            return False
        # obj must be safe.
        if not self._node_safe(node.obj):
            return False
        # Reject memoryviewslice or cpp_optional initialized-check branches.
        if node.type.is_memoryviewslice:
            return False
        if getattr(node.entry, 'is_cpp_optional', False) and getattr(node, 'initialized_check', False):
            return False
        return True

    def visit_TypecastNode(self, node):
        # Safe for C↔C casts (no pyobject involved in the cast itself).
        if node.type.is_pyobject and node.operand.type.is_pyobject:
            # pyobject-to-pyobject: safe (no allocation).
            return self._node_safe(node.operand)
        if node.type.is_pyobject or node.operand.type.is_pyobject:
            # C↔Python coercion via cast syntax: unsafe.
            return False
        return self._node_safe(node.operand)

    def visit_NumBinopNode(self, node):
        if node.type.is_pyobject:
            return False
        if getattr(node, 'overflow_check', False):
            return False
        return self._children_safe(node, ['operand1', 'operand2'])

    def visit_DivNode(self, node):
        if node.type.is_pyobject:
            return False
        if getattr(node, 'overflow_check', False):
            return False
        if getattr(node, 'zerodivision_check', False):
            return False
        if self.module_directives.get('cdivision_warnings', False):
            return False
        return self._children_safe(node, ['operand1', 'operand2'])

    visit_ModNode = visit_DivNode

    def _visit_UnopNode(self, node):
        if node.type.is_pyobject:
            return False
        if getattr(node, 'overflow_check', False):
            return False
        return self._children_safe(node, ['operand'])

    visit_UnaryMinusNode = _visit_UnopNode
    visit_UnaryPlusNode = _visit_UnopNode
    visit_TildeNode = _visit_UnopNode
    visit_NotNode = _visit_UnopNode

    def visit_BoolBinopNode(self, node):
        if node.type.is_pyobject:
            return False
        return self._children_safe(node, ['operand1', 'operand2'])

    def visit_CondExprNode(self, node):
        if node.type.is_pyobject:
            return False
        return self._children_safe(node, ['test', 'true_val', 'false_val'])

    def visit_PrimaryCmpNode(self, node):
        if node.type.is_pyobject:
            return False
        # Reject comparisons of pyobject operands.
        if node.operand1.type.is_pyobject or node.operand2.type.is_pyobject:
            return False
        return self._children_safe(node, ['operand1', 'operand2'])

    def visit_IndexNode(self, node):
        # Safe only for plain C pointer/array indexing.  Subclasses
        # (buffer/memoryview indexing, with their boundscheck/None-check
        # codegen) are rejected by the exact-type check.
        if node.__class__ is not ExprNodes.IndexNode:
            return False
        if node.type.is_pyobject:
            return False
        base_type = node.base.type if node.base is not None else None
        if base_type is None or not (base_type.is_ptr or base_type.is_array):
            return False
        return self._children_safe(node, ['base', 'index'])

    def visit_TupleNode(self, node):
        # A C-tuple result is a plain struct build (no allocation) — safe iff
        # every component is safe.  A Python-tuple result allocates (PyTuple_New
        # can raise MemoryError and gets a NULL check), so it stays unsafe.
        if not node.type.is_ctuple:
            return False
        return self._children_safe(node, ['args'])

    def visit_DictNode(self, node):
        # A value_type constructor `Vec2(...)` lowers to a DictNode coerced to
        # the value-class struct: pure member stores (no allocation, no
        # __init__ dispatch), so it cannot raise iff every value is safe.  A
        # Python-dict result allocates (PyDict_New can raise) and stays unsafe.
        if not getattr(node.type, 'is_value_class', False):
            return False
        for item in node.key_value_pairs:
            if not self._node_safe(item.value):
                return False
        return True

    # Coercion nodes that are safe:
    def visit_CoerceToTempNode(self, node):
        return self._node_safe(node.arg)

    def visit_CloneNode(self, node):
        # CloneNode just re-uses an already-evaluated temp.
        return True

    def visit_RawCNameExprNode(self, node):
        # A raw C name reference emits no evaluation code.
        return True

    def visit_ProxyNode(self, node):
        return self._node_safe(node.arg)

    def visit_CoerceToBooleanNode(self, node):
        # Safe only when the argument is C-typed.
        if node.arg.type.is_pyobject:
            return False
        return self._node_safe(node.arg)

    # Explicitly unsafe coercions:
    def visit_CoerceToPyTypeNode(self, node):
        return False

    def visit_CoerceFromPyTypeNode(self, node):
        return False

    def visit_NoneCheckNode(self, node):
        return False

    def visit_PyTypeTestNode(self, node):
        return False

    # PowNode: unsafe in v1.
    def visit_PowNode(self, node):
        return False

    # ------------------------------------------------------------------
    # Call nodes
    # ------------------------------------------------------------------

    def _visit_call_node(self, node):
        func_type = node.function_type() if hasattr(node, 'function_type') else getattr(node.function, 'type', None)
        if func_type is None:
            return False
        if not func_type.is_cfunction:
            return False
        if func_type.exception_check == '+':
            return False
        if getattr(func_type, 'return_type', None) is not None and func_type.return_type.is_memoryviewslice:
            return False
        # All argument expressions must be safe.
        for arg in (node.args or []):
            if not self._node_safe(arg):
                return False
        # Function expression must be safe.  NameNode / RawCNameExprNode /
        # PythonCapiFunctionNode call targets emit no evaluation code beyond
        # the C symbol itself.  An AttributeNode target (cmethod) evaluates
        # its object expression, so it goes through the full handler.
        func_node = node.function
        if not isinstance(func_node, (ExprNodes.NameNode,
                                      ExprNodes.RawCNameExprNode,
                                      ExprNodes.PythonCapiFunctionNode)):
            if not self._node_safe(func_node):
                return False
        # If already proven never-raising, we're done.
        if func_type.never_raises:
            return True
        # For non-pyobject returns that are already noexcept:
        if not func_type.return_type.is_pyobject:
            if not func_type.exception_check and func_type.exception_value is None:
                return True

        # Try to resolve the callee body.
        target_node = self._resolve_call_target(node, func_type)
        if target_node is None:
            # Cross-module target: no local body.  For direct calls
            # (skip_dispatch=1, executes exactly the defining body), trust a
            # cross-module fact recorded by the target module's own analysis.
            if getattr(node, 'wrapper_call', False):
                entry = (getattr(node.function, 'entry', None)
                         or getattr(func_type, 'entry', None))
                if _external_fact_for_entry(entry) in ('entry', 'direct'):
                    return True
            return False

        target_entry = target_node.entry
        if target_entry is None:
            return False

        # Dispatch safety for recursion:
        wrapper_call = getattr(node, 'wrapper_call', False)
        if not (target_entry.is_final_cmethod or
                (hasattr(target_entry, 'scope') and
                 getattr(target_entry.scope, 'is_module_scope', False)) or
                wrapper_call):
            return False

        # Recurse into target body.
        return self.body_cannot_raise(target_node)

    visit_SimpleCallNode = _visit_call_node
    visit_PythonCapiCallNode = _visit_call_node

    def _resolve_call_target(self, node, func_type):
        """Return the CFuncDefNode for the callee, or None if not resolvable."""
        func_node = node.function

        # Try by entry first (most reliable).
        entry = getattr(func_node, 'entry', None)
        if entry is not None:
            target = self.by_entry.get(id(entry))
            if target is not None:
                return target

        # Try by cname (for RawCNameExprNode / PythonCapiFunctionNode).
        cname = getattr(func_node, 'cname', None)
        if cname and '->' not in cname:
            return self.by_cname.get(cname)

        return None

    # ------------------------------------------------------------------
    # Assignment target helper
    # ------------------------------------------------------------------

    def _safe_assignment_target(self, node):
        if node is None:
            return True
        node_type = getattr(node, 'type', None)
        if node_type is None:
            return False
        # C++ class targets invoke operator= (may throw); memoryview targets
        # do acquisition/initialized bookkeeping.
        if node_type.is_cpp_class or node_type.is_memoryviewslice:
            return False
        if isinstance(node, ExprNodes.NameNode):
            entry = node.entry
            if entry is None:
                return False
            if entry.is_pyglobal:
                return False
            # Local, arg, or C global: plain store (+ incref/decref for
            # pyobject locals, which never raises).
            return True
        if isinstance(node, UtilNodes.CPropertySetNode):
            # cproperty assignment: routed through the setter call, which the
            # call handler vets (dispatch safety + setter body analysis).
            return self._node_safe(node.call_node)
        if isinstance(node, ExprNodes.AttributeNode):
            # C field store (including PyObject-typed ext-type fields:
            # incref/decref don't raise).
            if node.is_py_attr:
                return False
            if node.entry is not None and getattr(node.entry, 'is_cproperty', False):
                return False
            return self._node_safe(node.obj)
        if type(node) is ExprNodes.IndexNode:
            # Plain C pointer/array element store only (not pyobject subscript
            # — PyObject_SetItem raises — and not buffer/memview subclasses,
            # excluded by the exact-type check).
            base_type = node.base.type if node.base is not None else None
            if base_type is None or not (base_type.is_ptr or base_type.is_array):
                return False
            if node_type.is_pyobject:
                return False
            return (self._node_safe(node.base) and self._node_safe(node.index))
        return False


def _mark_cfunc_type(t):
    """Apply the noexcept inference mark to a CFuncType in place."""
    t.never_raises = True
    return_type = t.return_type
    if return_type is not None and not return_type.is_pyobject:
        t.exception_value = None
        t.exception_check = False


class ApplyCrossModuleNoexceptFacts(CythonTransform):
    """Mark cimported entries using facts from the other modules of this
    compilation batch (set via set_external_facts).

    The consumer only re-analysed the dependency's *declarations*
    (create_pyx_as_pxd_pipeline stops at AnalyseDeclarationsTransform), so the
    body analysis cannot run here; the producer's own compilation derived the
    facts from the identical source with identical directives.  Tier-1 facts
    are restricted to final methods/accessors and module-level functions, so
    no override (and therefore no exception spec inheritance) can ever
    observe these marks.

    Must run BEFORE OptimizeBuiltinCalls / OptimizeExtTypeConstructorCalls:
    the constructor optimizer snapshots the callee's exception spec into a
    fresh per-call CFuncType, so marks applied later would not reach the
    synthesized cross-module __init__ calls.
    """

    def visit_ModuleNode(self, node):
        if not _external_facts:
            return node
        if not node.directives.get('infer_noexcept', True):
            return node
        modules = getattr(self.context, 'modules', None)
        if not modules:
            return node
        own_scope = node.scope
        for mod_name, facts in _external_facts.items():
            if not facts:
                continue
            mod_scope = self._resolve_module_scope(modules, mod_name)
            if mod_scope is None or mod_scope is own_scope:
                continue
            for key, fact_kind in facts.items():
                if fact_kind != 'entry':
                    # 'direct' facts are only honored per-call-site (tier 2);
                    # the entry may be reachable through overriding vtable
                    # slots, so entry-wide marking would be unsound.
                    continue
                entry = self._resolve_fact_entry(mod_scope, key)
                if entry is not None:
                    self._mark_external_entry(entry, key[0])
        return node

    @staticmethod
    def _resolve_module_scope(modules, dotted_name):
        # context.modules is keyed by TOP-LEVEL package name only; dotted
        # submodules hang off it via lookup_submodule.
        parts = dotted_name.split('.')
        scope = modules.get(parts[0])
        for part in parts[1:]:
            if scope is None:
                return None
            scope = scope.lookup_submodule(part)
        return scope

    @staticmethod
    def _resolve_fact_entry(mod_scope, key):
        kind = key[0]
        if kind == 'f':
            return mod_scope.lookup_here(key[1])
        class_entry = mod_scope.lookup_here(key[1])
        if class_entry is None or not class_entry.is_type:
            return None
        class_scope = getattr(class_entry.type, 'scope', None)
        if class_scope is None:
            return None
        if kind == 'm':
            return class_scope.lookup_here(key[2])
        if kind == 'p':
            prop_entry = class_scope.lookup_here(key[2])
            if prop_entry is None:
                return None
            prop_scope = getattr(prop_entry, 'scope', None)
            if prop_scope is None or not getattr(prop_scope, 'is_property_scope', False):
                return None
            return prop_scope.lookup_here(key[3])
        return None

    @staticmethod
    def _mark_external_entry(entry, kind):
        func_type = entry.type
        if func_type is None or not func_type.is_cfunction:
            return
        if (getattr(func_type, 'has_explicit_exc_clause', False)
                and not getattr(func_type, 'synthesized_exc_clause', False)):
            return
        if func_type.exception_check == '+':
            return
        return_type = func_type.return_type
        if return_type is None or return_type.is_memoryviewslice:
            return
        if func_type.never_raises:
            return
        # Tier-1 facts only cover dispatch-safe entries; verify the consumer's
        # parse agrees (guards against name collisions or source skew).
        if kind == 'f':
            if entry.scope is None or not entry.scope.is_module_scope:
                return
        elif not getattr(entry, 'is_final_cmethod', False):
            return
        _mark_cfunc_type(func_type)


# ---------------------------------------------------------------------------
# Phase 3: orchestrator / tier-2 transform
# ---------------------------------------------------------------------------

class InferNoexcept(CythonTransform):
    """Orchestrator for noexcept inference.

    Phase 1: collect all CFuncDefNode instances.
    Phase 2 (tier 1): mark entry-level candidates whose body cannot raise.
    Phase 3 (tier 2): replace function.type on wrapper_call SimpleCallNodes.
    """

    def __call__(self, node):
        # Initialise current_directives via the parent __call__ machinery.
        from .ModuleNode import ModuleNode
        if isinstance(node, ModuleNode):
            self.current_directives = node.directives
        return super().__call__(node)

    def visit_ModuleNode(self, node):
        module_directives = node.directives
        self.collected_facts = {}

        # Gate: skip entire module when profile/linetrace is on.
        if module_directives.get('profile') or module_directives.get('linetrace'):
            return node

        # Phase 1: collect.
        collector = _CollectCFuncDefs(self.context)
        collector(node)

        by_entry = collector.by_entry
        by_cname = collector.by_cname
        func_directives = collector.func_directives

        # Phase 2: tier-1 marking.
        analysis = _BodyRaiseAnalysis(by_entry, by_cname, func_directives, module_directives)

        for entry_id, funcdef in by_entry.items():
            entry = funcdef.entry

            # --- Candidate filter ---
            if funcdef.body is None:
                continue
            if entry is None:
                continue

            directives = func_directives.get(id(funcdef), module_directives)
            if not directives.get('infer_noexcept', True):
                continue
            if directives.get('profile') or directives.get('linetrace'):
                continue

            func_type = funcdef.type
            if func_type is None:
                continue

            if (getattr(func_type, 'has_explicit_exc_clause', False)
                    and not getattr(func_type, 'synthesized_exc_clause', False)):
                continue

            if funcdef.visibility == 'extern':
                continue

            if getattr(func_type, 'is_fused', False) or getattr(func_type, 'has_fused_arguments', False):
                continue

            # Skip synthesized trampolines.
            if (getattr(funcdef, 'is_cpdef_trampoline', False) or
                    getattr(funcdef, 'is_cpdef_property_trampoline', False) or
                    getattr(funcdef, 'is_cpdef_inheritance_trampoline', False)):
                continue

            # Skip closures (scope allocation can raise).
            from .Nodes import FuncDefNode
            if funcdef.needs_closure and funcdef.needs_closure != FuncDefNode.NeedsClosure.NO_CLOSURE:
                continue

            return_type = func_type.return_type
            if return_type is not None and return_type.is_memoryviewslice:
                continue

            if func_type.exception_check == '+':
                continue

            # Skip if already marked.
            if func_type.never_raises:
                continue
            if not return_type.is_pyobject:
                if not func_type.exception_check and func_type.exception_value is None:
                    continue  # already noexcept (e.g. cdef void)

            # Dispatch safety: entry-level marking only for final methods or
            # module-scope functions (their entries are never reachable through
            # an overriding vtable slot).  Non-final class methods cannot be
            # entry-marked, but their body analysis still yields a 'direct'
            # fact: synthesized direct calls (super()/ctor, skip_dispatch=1)
            # execute exactly this body, so per-call-site patching is sound.
            scope = getattr(entry, 'scope', None)
            is_module_scope = scope is not None and getattr(scope, 'is_module_scope', False)
            is_final = getattr(entry, 'is_final_cmethod', False)
            is_class_method = scope is not None and getattr(scope, 'is_c_class_scope', False)

            if is_module_scope:
                # Module-scope: safe when lookup_module_cpdef is False (no vtable override possible).
                if func_type.is_overridable and Options.lookup_module_cpdef:
                    continue
                entry_safe = True
            elif is_final:
                # funcdef.override must be None (invariant: no OverrideCheckNode for finals).
                entry_safe = getattr(funcdef, 'override', None) is None
            elif is_class_method:
                entry_safe = False  # 'direct' fact only
            else:
                continue

            # --- Body analysis (always skips funcdef.override) ---
            if not analysis.body_cannot_raise(funcdef):
                continue

            fact_key = _fact_key_for_entry(entry)
            if entry_safe:
                # --- Mutate in place ---
                # Mutate funcdef.type and entry.type (may be distinct objects).
                _mark_cfunc_type(func_type)
                if entry.type is not func_type:
                    _mark_cfunc_type(entry.type)
                # Propagate the mark to the cpdef Python wrapper node so its own
                # generated code (e.g. the __hash__ -1->-2 coercion) drops the
                # now-dead PyErr_Occurred() guard.  The wrapper's type is the
                # shared py_object_type, so we cannot mutate it — flag the nodes.
                funcdef.inferred_noexcept = True
                py_func = getattr(funcdef, 'py_func', None)
                if py_func is not None:
                    py_func.inferred_noexcept = True
                if fact_key is not None:
                    self.collected_facts[fact_key] = 'entry'
            else:
                if fact_key is not None:
                    self.collected_facts[fact_key] = 'direct'

        # Phase 3: tier-2 — walk the tree and replace function.type on
        # wrapper_call SimpleCallNodes whose callee is proven safe.
        self._analysis = analysis
        self._by_cname = by_cname
        self._module_directives = module_directives
        self.visitchildren(node)
        return node

    def visit_SimpleCallNode(self, node):
        self.visitchildren(node)
        self._try_tier2(node)
        return node

    def visit_PythonCapiCallNode(self, node):
        self.visitchildren(node)
        self._try_tier2(node)
        return node

    def _try_tier2(self, node):
        if not getattr(node, 'wrapper_call', False):
            return

        # Must be the infer_noexcept directive active at this call site.
        if not self.current_directives.get('infer_noexcept', True):
            return

        func_node = node.function
        if func_node is None:
            return

        func_type = getattr(func_node, 'type', None)
        if func_type is None or not func_type.is_cfunction:
            return
        if func_type.exception_check == '+':
            return
        if (getattr(func_type, 'has_explicit_exc_clause', False)
                and not getattr(func_type, 'synthesized_exc_clause', False)):
            return  # user-written exception spec is sacred
        if func_type.return_type.is_memoryviewslice:
            return
        if func_type.never_raises:
            return  # already marked

        # Resolve cname.  RawCNameExprNode / PythonCapiFunctionNode store it
        # directly.  NameNodes (produced from AttributeNode.as_name_node for
        # unbound-cmethod calls) carry it on their entry.
        cname = getattr(func_node, 'cname', None)
        if cname is None:
            entry = getattr(func_node, 'entry', None)
            if entry is not None:
                # Prefer func_cname (the actual C symbol) for by_cname lookup.
                cname = getattr(entry, 'func_cname', None) or getattr(entry, 'cname', None)

        target_node = None
        if cname and '->' not in cname:
            target_node = self._by_cname.get(cname)

        if target_node is not None:
            if not self._analysis.body_cannot_raise(target_node):
                return
        else:
            # Cross-module direct call (e.g. `vtabptr->__pyx___init__` from the
            # super()/ctor optimizers): trust the target module's own analysis
            # via the injected facts.  skip_dispatch=1 guarantees the executed
            # code is exactly the analysed body.
            entry = (getattr(func_node, 'entry', None)
                     or getattr(func_type, 'entry', None))
            if _external_fact_for_entry(entry) not in ('entry', 'direct'):
                return

        # Replace the function node's type with a noexcept copy (never mutate the shared entry type).
        func_node.type = func_type.with_noexcept_spec()

    def visit_Node(self, node):
        self.visitchildren(node)
        return node
