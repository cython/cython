# Cython – Agent Guide

## Quick start (no install needed)

```bash
python cython.py file.pyx           # compile pyx -> C
python cythonize.py -if file.pyx    # compile + build .so
python runtests.py test_name        # run one test
```

Editable install (optional, for using `cython`/`cythonize` CLI):
`NO_CYTHON_COMPILE=true pip install -e .`

Build Cython's own compiled extensions: `python setup.py build_ext --inplace -j5`

## Test infrastructure

**Run a single test:** `python runtests.py -vv run.with_gil`

Test name = `{directory}.{filename_without_ext}` — e.g. `tests/run/with_gil.pyx` → `run.with_gil`.

**Key flags:**
| Flag | Purpose |
|------|---------|
| `--no-cleanup` | Keep generated C/C++ files in `TEST_TMP/` |
| `--no-cleanup-failures` | Keep workdir only for failed tests |
| `--backends=c,cpp` | Select language backends (default: both) (do not apply for srctree tests) |
| `--cython-only` | Stop after pyx→c generation (skip compilation/run) |
| `--limited-api [VER]` | Test with CPython Limited API |
| `--no-code-style` | Skip PEP8 checks (auto-implied when passing test selectors) |
| `-x PATTERN` | Exclude tests matching pattern |
| `tag:cpp` | Matcher that filter by tag |

**Test modes** (set via `# mode:` comment, default `run`):
- `run` — compile → build `.so` → run doctests
- `compile` — compile only, check C warnings/errors
- `error` — compile, match against `_ERRORS` section

**Tags** (`# tag: value`): `cpp`, `numpy`, `embed`, `werror`, `tracback`, `no-cpp`, `cerror`, etc.

**`# distutils:` directives:** Pass options to extension builder (`language=c++`, `sources=helper.c`, etc.)

**`.srctree` end-to-end tests:** Embedded files separated by `######## filename ########`. Header lines before the first separator are shell commands. Substitution vars: `PYTHON` → `sys.executable`, `CYTHON` → `python cython.py`, `CD path`, `UNSET VAR`.

**Test file extensions recognized:** `.pyx`, `.py`, `.srctree` only.

**`test_` prefix matters:** Files in `mode: run` named `test_*.pyx` get `CythonUnitTestCase` (loads unittest from module); otherwise `CythonRunTestCase` (doctests only).

**Bug exclusion files:** `tests/{bugs,cygwin_bugs,graal_bugs,limited_api_bugs,pypy_bugs,windows_bugs,...}.txt` — regex patterns for known-failing tests per platform.

The best test case to run is:

```
python runtests.py --no-code-style -x Debugger --backends=c --no-cleanup embed_modules_optimize
```

Then you can check the generated file in: `TEST_TMP/build/embed_modules_optimize/`

## Development quirks & conventions

- **No reinstall needed:** `runtests.py` uses the local source tree directly (`sys.path.insert(0, ...)`)
- **Cython is self-compiling:** It's a Python-to-C compiler written partly in Cython. `setup.py build_ext` compiles the hot modules (scanner, parser, codegen) to C for speed. Run this before `--coverage` runs.
- **`# tag: embed`** tests are excluded under Limited API and Py_DEBUG (builds with `Py_DEBUG` defined)
- **Properties on `@cclass`** generate `getset_descriptor` objects (not Python `property`). Use `descr.__set__(obj, val)` not `descr.fset(obj, val)` — `fset`/`fget`/`fdel` don't exist on `getset_descriptor`.
- **`auto_cpdef=True`** makes `cpdef` functions importable as function pointers (`__pyx_f_...`). Used by embed-module optimization.
- **auto_cpdef + `__init__` in cclasses**: `__init__` can be promoted inside `@cclass` via auto_cpdef. The promoted entry gets `is_special=1` set in `CClassScope.declare_cfunction` (`Symtab.py`) so the `tp_init` slot is assigned. The slot must use the `__pyx_pw_` wrapper (returns `int` for `initproc`), not the `__pyx_f_` function (returns `PyObject*`). This is handled by `MethodSlot._get_slot_function` (`TypeSlots.py`) which prefers `as_variable.func_cname` for cfunction entries. Signature conflicts across inheritance are suppressed with an `elif name in ('__init__', '<init>')` branch in `declare_cfunction`.
- **auto_cpdef blocks other dunders in cclasses**: `__add__`, `__eq__`, `__repr__` etc. are NOT promoted inside cclasses because cpdef promotion adds `int __pyx_skip_dispatch` to the C signature, but the synthesized slot wrappers (richcompare, nb_add, getattro, etc.) call `entry.func_cname` with the fixed CPython slot argument count. Only `__init__` is exempt because its slot (`tp_init`) goes through `MethodSlot.slot_code` which we patch. To enable other dunders, update every slot wrapper generator in `ModuleNode.py` (6-7 sites) to pass `, 1` for overridable entries.
- **`lto=True`** (Link-Together Optimization): El modo LTO asume que los modulos que estan siendo compilados seran tambien enlazados juntos por lo tanto no depende de la carga dinamica de modulos de Python que estan siendo compilados juntos. Se activa con `-X lto=True`.
- **Property accessor capsule names**: Multiple classes per module sharing property names cause `__get__`/`__set__` capsule name collisions in function export/import (`ModuleNode.py:_get_function_export_name`). Qualified as `{ClassName}.{prop_name}.{entry.name}`.
- **Inherited entry cname prefix stripping**: When inheriting cpdef entries from base scopes, `CClassScope.declare_cfunction` (`Symtab.py:2823`) now strips leading `__pyx_base.` prefix from `cname` for inherited entries to prevent accumulation through multiple inheritance levels (e.g., `__pyx_base.__pyx_base.__pyx___init__` → `__pyx___init__`).
- **auto_cpdef properties are cproperties**: With `auto_cpdef=True`, `@property` getters get `inline` modifier, which sets both `is_cproperty=True` and `is_overridable=True` (`PropertyNode.analyse_declarations`, `Nodes.py:6208-6214`). The vtable dispatch vs Python attribute fallback is controlled by whether `vtabstruct_cname` is set, not by `is_cproperty`.
- **Vtable allocation for property-only types**: `allocate_vtable_names` (`Symtab.py:1916`) only checks `cfunc_entries` when deciding whether to allocate a vtable struct. Property accessor entries live in `PropertyScope`, not the class scope. If a cclass only has `@property` accessors and no `cdef` methods, add an `elif` for `property_entries` with `is_cproperty=True` to allocate the vtable. Skip extern types (`entry.visibility == 'extern'`) to avoid breaking `cpython/datetime` and similar pxd wrappers.
- **Property vtable overrides must patch all ancestors**: When overriding a property, `generate_exttype_vtable_init_code` (`ModuleNode.py:4435`) patches ancestor vtable slots. Use a `base_path` string that accumulates `.__pyx_base` suffixes (one per inheritance level) instead of a single `Naming.obj_base_cname`, and do NOT `break` after the first match — patch every ancestor's slot so dispatch through any base-class pointer resolves correctly.
- **LTO super().prop uses RawCNameExprNode**: The LTO path in `_handle_simple_base_property_access` (`Optimize.py:1889`) must use `RawCNameExprNode` (not `NameNode`) so `c_call_code` (`ExprNodes.py:6689`) doesn't re-enter vtable dispatch for the direct call.
- **RawCNameExprNode has no `.entry`**: `c_call_code` (`ExprNodes.py:6753`) calls `self.function.entry.is_unbound_cmethod` to decide skip_dispatch. When `self.function` is a `RawCNameExprNode` (from LTO path), it has no `.entry` attribute. Use `getattr(self.function, 'entry', None)` guard: `func_entry = getattr(self.function, 'entry', None); skip_dispatch = func_entry.is_unbound_cmethod if func_entry else False`
- **C trampolines for incompatible cpdef overrides** (`ParseTreeTransforms.AnalyseDeclarationsTransform._create_cpdef_method_trampolines`, `Nodes.CFuncDefNode._analyse_trampoline_declarations`). When a `def` in a cclass overrides an inherited cpdef method but cannot itself be promoted to cpdef (closure or generator), instead of erroring it synthesises a C "trampoline" `CFuncDefNode` that fills the inherited vtable slot and dispatches to the Python body. The trampoline carries the same `OverrideCheckNode` as a normal cpdef, so pure-Python subclasses that further override the method are still reached through C dispatch. A generator body is called directly via `pyfunc_cname`; the return value (a `PyObject*`) is coerced to the slot's return type. Coverage: `tests/run/auto_cpdef_classes.py::test_method_trampoline`, `tests/run/auto_cpdef_trampoline_cross_module.srctree`.
- **Regular cclass methods are auto_cpdef-promoted so `super().method()` optimizes**: the block in `AdjustDefByDirectives` (`ParseTreeTransforms.py` ~3281) now only blocks *dunders* (`name.startswith('__') and name.endswith('__') and name != '__init__'`), not all non-`__init__` methods. This lets regular methods like `_make_hit_box` become cpdef (get an `__pyx_f_` + vtable slot) so the `super()` optimizer fires. A method that can't be cpdef (generator/closure → `is_cdef_func_compatible()` is False) overriding a now-promoted base method raises a clear error (`Nodes.py` ~3674) telling you to `@cython.no_ccall` the *base* method. **Opt-out pattern**: decorate the base-class definition (the first in the hierarchy) with `@cython.no_ccall`; the whole family then stays a plain Python `def`. The full c+cpp suite stays green; crop-chronicles needed only `IFocusManager.start_text_input/stop_text_input` annotated.
- **`@no_ccall` was a silent no-op (now fixed)**: `no_ccall` is a marker directive whose bare decorator stores value `None`. `AdjustDefByDirectives` read it with `self.directives.get('no_ccall')` (falsy → ignored) instead of presence (`'no_ccall' in self.directives`, like `ccall`/`cfunc`). Fixed in `ParseTreeTransforms.py` ~3254. Without this, the promotion opt-out does nothing.
- **Promoting more methods exposed two latent codegen bugs (both fixed)** — these only fire once regular methods are cpdef, so the unit suite never hit them; crop-chronicles did:
  1. **`cfunc.to_py` utility inherits `auto_cpdef` → `'wrap redeclared'`**: `CFuncType.create_to_py_utility_code` (`PyrexTypes.py` ~3766) loaded the converter with `dict(env.global_scope().directives)`, so the utility's internal `def wrap` got auto-promoted and redeclared. Fixed by forcing `utility_directives['auto_cpdef'] = False`. (The FIXME there about leaking directives is the root smell.)
  2. **Inherited cpdef method referenced as a value → broken `to_py` of the vtable pointer**: e.g. `self._cb` passed as a callback (`TextButton(..., self._show_credits)`). Inherited cmethod entries have `as_variable = None`, so `AttributeNode.coerce_to` (`ExprNodes.py` ~7919) skipped the cpdef→cyfunction branch and coerced the raw vtable pointer; its signature carries `__pyx_skip_dispatch`, which doesn't match the generated `object (*)(T)` converter → g++ "no matching function". Fixed by adding a branch: an overridable cmethod coerced to `py_object` resolves via `analyse_as_python_attribute` (`GetAttr` → bound cyfunction) even when `as_variable` is None. Regression test: `tests/run/auto_cpdef_classes.py::use_inherited_method_ref`.
- **`super().method()` / `super().property` optimization in `@cclass`** (`_handle_simple_base_method_call`, `_handle_simple_base_property_access`, `Optimize.py:1808`+). Final design, after several wrong turns documented below:
  - **Same-module target** → direct `__pyx_f_<Owner>_<method>(self, …)` call via `RawCNameExprNode(type=resolved_fn.type, cname=origin)`, where `resolved_fn`/`origin` come from the `lookup_here` ancestor walk + `_find_owning_cname`. Declared in the same TU, so a direct call is fine.
  - **Cross-module target** → **VTABLE dispatch through `base_type.vtabptr_cname`** (cimported via `__Pyx_GetVtable`, so *always declared*). Build `"%s->%s" % (base_type.vtabptr_cname, base_entry.cname)` where `base_entry = base_type.scope.lookup(attr)` — its `cname` already encodes the nested `__pyx_base...` path (e.g. `__pyx_base._make_hit_box`) and its `type` is the real `CFuncType`. Wrap in `RawCNameExprNode(type=base_entry.type, …)`, and set `call_node.wrapper_call = True` so `skip_dispatch=1` is passed (a `RawCNameExprNode` has no `.entry`, so it would otherwise default to 0 — and `super()` must call the base method itself, never re-dispatch to a Python-subclass override).
  - **Properties are NOT copied into subclass scopes** (unlike cmethods), so `base_type.scope.lookup(prop)` returns None when only inherited. Walk `base_type.base_type` to the defining class counting levels, then build `vtabptr->` + `"__pyx_base." * depth` + `getter_entry.cname`. Property getters have no `skip_dispatch` arg.
  - **`__init__` is the exception**: cpdef `__init__` entries are *copied* into every subclass scope with a cname that mislocates the slot when the class only inherits it. So optimize `__init__` only when `base_type` *directly* defines it: `e = base_type.scope.lookup_here('__init__'); if not (e and e.is_cmethod and not getattr(e,'is_inherited',False)): return node`. Else leave it as Python `super()` MRO dispatch (always correct). Reproducing MRO chaining for *inherited* cross-module `__init__` is the larger constructor rewrite's job.
  - **Why NOT a direct cross-module `__pyx_f_` call** (an earlier attempt via an unbound-cmethod `AttributeNode` that resolved to the LTO direct form): the calling module never emits the extern `__pyx_f_` proto → g++ `use of undeclared identifier` across many modules. The vtable pointer is the only thing the cimport reliably declares.
  - **Bugs this caused along the way (all now avoided):** a hand-built vtable string using the wrong entry's `.type` (`py_object` variable form) made `SimpleCallNode` emit a Python `FastCall` on a raw function pointer → garbage args (`OverflowError: value too large to convert to int` far away); and the deep `RootGameNode → IGameScreenController → … → GameNode` `super().__init__()` resolving to the WRONG nested slot (cast to an unrelated `SpriteBase*` via 6×`__pyx_base`) so base `__init__` never ran → `AttributeError: 'NoneType' object has no attribute 'add_many'`.
  - **Coverage**: `tests/build/embed_modules_optimize.srctree`'s `check_codegen.py` covers the base-directly-defines case (no `FastCallMethod(...__pyx_n_u_init` survives). The **inherited** cross-module case is only validated by the crop-chronicles project — the unit suite has no deep cross-module inheritance, so always rebuild crop-chronicles too.
  - **Payoff (validated, consistent across ≥4 runs):** crop-chronicles `test_fps_benchmark` ~84 FPS (Python `super()`) → **~225 (level 6-2) / ~409 (overworld)** with vtable dispatch. `super().update()/.draw()/._make_hit_box()` run every frame per node, so making them vtable calls is a ~2.7–4.8× win. (FPS is noisy run-to-run; compare ≥3 runs of each build, not single readings.)
- **Closure (non-generator) `@property` getters now become C getters / cproperties** (`ParseTreeTransforms.py` `_convert_property_to_cfunc`, ~1979). The auto_cpdef property→`CFuncDefNode` conversion used to bail on **any** `needs_closure` getter, leaving it Python-only (`__pyx_pf_`/`__pyx_getprop_`, no `__pyx_f_`, no vtable slot). That meant a getter like `return all(e.is_fulfilled for e in self.entries)` could NOT override an inherited cproperty's vtable slot, so a statically-typed-base access (`self._order.is_fulfilled` where `_order: IOrder`, and `IOrder.is_fulfilled` is an abstract cproperty) dispatched to the **base** (abstract) getter → `NotImplementedError` swallowed as `Exception ignored in: 'IOrder.is_fulfilled.__get__'`. The fix narrows the bail to **`node.is_generator`** only: a generator getter (the body itself uses `yield`, e.g. `for x in …: yield x`) genuinely cannot be a plain C getter (it must build a generator object) — converting one crashes (the C getter runs the generator body as a normal function; observed as `EXC_BAD_ACCESS` in `PyTraceBack_Here` while building the traceback of the resulting exception). A *generator expression / comprehension / lambda inside* the body is NOT `is_generator` and is fine — Cython compiles those closures inside cdef/cpdef functions and the C getter fills the vtable slot. **Key distinction: `is_generator` (getter yields) ≠ `needs_closure` (getter has an inner closure).**
- **Generator-property-getter trampolines now fill inherited cproperty vtable slots** (`ParseTreeTransforms.AnalyseDeclarationsTransform._create_property_getter_trampolines`, `Nodes.CFuncDefNode._analyse_property_trampoline_declarations`). When a cclass overrides an inherited cproperty with a *generator* getter (`yield` in body), the getter stays Python-only but a C "trampoline" inline function is synthesised and registered in `cfunc_entries` with the inherited vtable slot cname, so `generate_exttype_vtable_init_code` fills the slot. A statically-typed base access (e.g. `base_ref.puddles` where the base declares `puddles` as a cproperty) then correctly dispatches to the override's generator rather than the abstract base getter. The trampoline body calls `pydef.entry.pyfunc_cname` (the Python generator function). Coverage: `tests/run/auto_cpdef_classes.py::use_generator_property_getter` and the `IThing/Thing.items` example.
- **Optional-arg methods are now auto_cpdef-promotable**: `is_cdef_func_compatible` (`Nodes.py:3579`) no longer rejects methods whose `num_required_args < len(args)` (i.e. methods with default arguments). `*args` and `**kwargs` remain blocked. `@cython.ccall` already supported optional args through the same `as_cfunction` path, so removing the restriction is safe.
- **Constructor optimization now applies to all expression contexts** (`OptimizeExtTypeConstructorCalls`, `Optimize.py:~4696`). The transform has two paths:
  1. **Statement-level split** (`visit_SingleAssignmentNode` + `_maybe_split_ctor`): for `var = T(args)` with a simple-name LHS — avoids an extra temp variable. The synthesised `NameNode` for the self arg sets `cf_maybe_null = False` to suppress the redundant unbound-local null check that control-flow analysis would otherwise emit after tp_new.
  2. **Expression-level transform** (`visit_SimpleCallNode` + `_maybe_transform_ctor_expr`): for all other contexts (`return T(args)`, `func(T(args))`, standalone `T(args)`). Uses `UtilNodes.TempResultFromStatNode(result_ref, [tp_new→result_ref, __init__(result_ref)])`. `result_ref.type = py_object_type` so the allocated temp is `PyObject *` (matching `allocate_temp_result`); `TempResultFromStatNode.type` is overridden to `ext_type` so callers see the precise type without a `PyTypeTestNode`.
  - **CloneNode sync bug**: `SimpleCallNode.analyse_types` clones `self.self` into `function.obj` and `coerced_self` via `CloneNode`. When `visitchildren` transforms `node.self`, the CloneNodes still point to the untransformed original — whose `temp_code = None` (class default), generating literal `None` in C. Fix: after `visitchildren`, sync `CloneNode.arg` to the new `node.self` for both `function.obj` and `coerced_self`.
  - **C++ self-type fix**: `_build_init_call_stat` uses `formal_self_type` (not always `ext_type`) to avoid C++ pointer-type errors. The actual self type of the C function is determined by comparing `func_cname` against what `ext_type.scope.mangle(Naming.func_prefix, '__init__')` produces: if they match, the function is `ext_type`'s own init (takes `ext_type *`); otherwise (inherited init from a base class), use `orig_type.args[0].type`. `is_inherited` alone is not a reliable indicator — due to `copy.copy` in `handle_already_declared_name`, a class's own `__init__` entry can have `is_inherited = True` while still being the class's own function.
  - Same-module: `func_cname` (`__pyx_f_…`) is declared in the same TU → `PythonCapiCallNode(func_cname, …)`.
  - Cross-module: use `ext_type.vtabptr_cname->init_entry.cname(…)`. `has_vtable` flag controls which path is taken.
  - When some optional args are passed positionally, `call.has_optional_args = True` activates the `__pyx_opt_args_*` struct machinery in `generate_result_code`.
  - `call_type` uses `is_overridable=True` so `c_call_code` inserts `__pyx_skip_dispatch` before the opt-args struct pointer (the correct ABI order). `wrapper_call=True` fixes the skip-dispatch value to 1.
  - Coverage: `tests/run/auto_cpdef_optargs_methods.py`, `tests/build/embed_modules_optimize.srctree`.
- **`_handle_simple_base_method_call` optional-arg fix** (`Optimize.py:~1808`): post-analysis synthesised `SimpleCallNode` instances (from the super() optimiser) bypass `analyse_c_function_call`, which would normally set `has_optional_args`. The helper `_set_optional_args_flag` (module-level) sets it manually when `len(actual_args) > expected_nargs`. Without this, `c_call_code` tries to reference `self.opt_arg_struct` before it is allocated.
- **Constructor optimization for `@dataclass` cdef classes** (`Dataclass.py:handle_cclass_dataclass`, `Symtab.py:CClassScope.declare_pyfunction`): `generate_init_code` always emits `def __init__` in text (valid for all kw_only/non-kw_only forms), then `handle_cclass_dataclass` upgrades the resulting `DefNode` to `CFuncDefNode` via `stat.as_cfunction(overridable=True)` — this is the same tree-level promotion path as `auto_cpdef`, bypassing the parser's rejection of `*` inside `cpdef` syntax. Only done when `stat.is_cdef_func_compatible()` returns True; the one rejected case is a required kw-only arg after an optional kw-only arg (e.g. `*, a=1, b`), which `CFuncDeclaratorNode.analyse` can't represent. Two companion fixes needed: (1) After visiting the generated code, call `node.entry.scope.allocate_vtable_names(node.entry)` — `allocate_vtable_names` ran before the cpdef was added to `cfunc_entries`, leaving `vtabptr_cname=None` and producing `None->__pyx___init__` in the `__pyx_pf_` body for optional-arg cpdef methods. (2) `CClassScope.declare_pyfunction` (`Symtab.py:~2636`) generated a spurious level-0 `'<name>' redeclared` warning (visible at `runtests.py`'s `LEVEL=0`) when `declare_cpdef_wrapper` called `declare_pyfunction` on an already-registered cfunction — fix: use `visibility='ignore'` when `not allow_redefine` (wrapper path) and an existing cfunction entry is found; `allow_redefine=True` (user def overriding cpdef) keeps the warning. Coverage: `tests/run/cdef_class_dataclass.pyx` (`make_dataclass_ctor_opt`, `make_dataclass_ctor_opt_expr` with `@cython.test_fail_if_path_exists("//SimpleCallNode")`).
- **Dataclass opt_args struct C-type fix** (`Dataclass.py:handle_cclass_dataclass`, ~line 384): The generated `def __init__` is wrapped in `CompilerDirectivesNode(annotation_typing=False)` so that optional args accept any Python object (needed for `_HAS_DEFAULT_FACTORY` sentinel with `default_factory` fields). Side-effect: `CArgDeclNode.analyse` skips annotation-based type injection, so optional args remain `PyObject *` in the opt_args struct even when the field has a C type (e.g. `y: float` → `PyObject *y` instead of `float y`). Fix: after `as_cfunction`, iterate over `cfunc.declarator.args`; for each optional arg (`arg.default is not None`) whose field has a plain default (`field.default_factory is MISSING`) and a non-pyobject class-scope entry type, pre-set `arg.name_declarator = arg.declarator` and `arg.type = field_entry.type`. The early-exit `if self.type is not None` in `CArgDeclNode.analyse` then uses the pre-set type, bypassing the disabled annotation typing. `default_factory` fields are left as `PyObject *` intentionally. `name_declarator` must be set alongside `type` or the early-return produces a `(None, type)` pair that crashes `CFuncDeclaratorNode.analyse` on `name_declarator.name`.
- **Deleting Code.so enables python-mode**: Should delete all .so or .pyd files under `Cython/` otherwise we end up using stale code.
- **@final property getters get final_func_cname**: `PropertyScope.declare_cfunction` (`Symtab.py:3072`) must set `is_final_cmethod=True` and `final_func_cname=func_cname` when `parent_type.is_final_type`, mirroring `ClassScope.declare_cfunction`. In `c_call_code`, check `not func_entry.final_func_cname` to skip vtable dispatch for final types.
- **`.py` tests** get `import cython` auto-injected when `add_cython_import=True`
- **CFLAGS `-O0` or `-Og`** cuts test suite runtime by ~2x
- **Tree path assertions** (`@cython.test_assert_path_exists`, `@cython.test_fail_if_path_exists`) test that optimizations fire. They use XPath-like `TreePath` expressions.
- **`python_subclassing` directive** (`Options.py`, `Nodes.py`, `ModuleNode.py`, `TypeSlots.py`): When set to `False` on a `cdef class`, suppresses `OverrideCheckNode` generation for all `cpdef` methods (including trampolines and cpdef property getters) and injects an `__init_subclass__` classmethod that raises `TypeError` when a pure Python class tries to subclass the extension type. Default `True` (preserves all existing behaviour). Settable at module level (`# cython: python_subclassing=False`) or per-class (`@cython.python_subclassing(False)`). In `Shadow.py` the decorator is a no-op `_EmptyDecoratorAndManager()`.
  - **`immediate_decorator_directives` + scope attribute pattern**: `python_subclassing` is in `immediate_decorator_directives`, which means `visit_with_directives` wraps the class body in a `CompilerDirectivesNode(old_directives)` that resets `env.directives` before method `analyse_declarations` runs. Do NOT read `env.directives.get('python_subclassing')` inside `declare_cpdef_wrapper` — it will always see the pre-decorator default. Instead, store `scope.python_subclassing = scope.directives.get('python_subclassing', True)` on the scope object during `CClassDefNode.analyse_declarations` BEFORE `body.analyse_declarations()` runs, then read `getattr(env, 'python_subclassing', True)` at gate sites. Any future `immediate_decorator_directives` entry that controls method-analysis-time behaviour must follow this same pattern.
  - **Pure Python subclass discriminator**: The `__init_subclass__` C function uses `tp_dictoffset != 0 || Py_TPFLAGS_MANAGED_DICT` to distinguish pure Python classes from Cython heap types. `Py_TPFLAGS_MANAGED_DICT` is set by `type.__new__` (pure Python) but NOT by `PyType_FromSpec` (`CYTHON_USE_TYPE_SPECS` Cython types). `tp_dictoffset != 0` is the Python < 3.12 fallback. Do NOT use `Py_TPFLAGS_HEAPTYPE` or `Py_TPFLAGS_HAVE_GC` — Cython spec types set both.
  - **Compile-time error**: `PyClassDefNode._check_python_subclassing` fires during `analyse_declarations` for Python classes in `.pyx` files and raises an `error()` if any base name resolves to a `cdef class` scope with `python_subclassing=False`. Guard with `hasattr(self.bases, 'args')` — star-expression bases are `AsTupleNode` with `.arg` (singular), not `.args`.
  - **`MethodTableSlot.slot_code`** emits the method table cname (not `"0"`) when `_init_subclass_func_cname` is set even if `pyfunc_entries` is empty.
  - Coverage: `tests/run/python_subclassing_directive.pyx`, `tests/run/python_subclassing_module.pyx`, `tests/errors/python_subclassing_error.pyx`.
- **`python_subclassing` inheritance-lock**: `@python_subclassing(True)` starts a lock on any class where it causes a **False→True value transition** (whether via explicit decorator or ambient module default overriding a base's explicit `False`). All descendants automatically inherit `True` (silently overriding any module-level ambient `False`). An explicit `@python_subclassing(False)` decorator on a locked descendant is a compile-time error — but only if the decorator *changes* the ambient value; if module-default is already `False`, the `_extract_directives` filter silently skips it (same-value decorator is not reported). Lock detection implemented via `scope.python_subclassing_locked`; set whenever the effective value transitions from `False` in the base to `True` in the current class.
  - **"Late enable" requires two injections**: (1) Inheritance trampolines for inherited cpdef/ccall methods not explicitly overridden — synthesised in `AnalyseDeclarationsTransform._create_inheritance_trampolines`; (2) A **permissive** `__init_subclass__` that overrides the blocking one from the False ancestor — generated via `generate_init_subclass_function(scope, code, permissive=True)` in `ModuleNode`. Without (2), Python classes inherit the base's TypeError-raising `__init_subclass__` and still cannot subclass the re-enabled class.
  - **`_MinimalPyFuncRef`** (Nodes.py): lightweight stub carrying `.entry`, `.fused_py_func=None`, `.is_module_scope=False` so `OverrideCheckNode` can use the inherited Python-wrapper Entry without a real `DefNode`. The comparison in `generate_execution_code` uses `Base.__pyx_pw_` as the "expected" function; Python subclasses that override will differ → dispatch fires.
  - **Forward call avoids vtable cycle**: the trampoline fills `Derived.vtable.__pyx_base.slot`; calling through `self->vtab->slot` would re-enter the trampoline. Instead the body calls through `defining_base.vtabptr_cname->slot` (the static vtabptr for the class that originally defines the method, always pointing to the un-trampolined implementation).
  - Coverage: `tests/run/python_subclassing_inheritance.pyx`, `tests/errors/python_subclassing_lock_error.pyx`.
- **Required kw-only args after optional ones block cpdef promotion** (`Nodes.py:is_cdef_func_compatible`): `def f(self, *, a=1, b)` (required kw-only after optional) cannot be a C function (C requires all required args before optional). Return `False` from `is_cdef_func_compatible` for this case; the method stays as a plain `def`. Coverage: `tests/run/auto_cpdef_kwonly_required.py`.
- **cpdef method called with kw-only gap falls back to Python dispatch** (`ExprNodes.py:GeneralCallNode.analyse_types`, `map_to_simple_call_node`): When a cpdef method is called with keyword args that skip an optional arg (`self.f(layer, grid_rect=r)` where `f(layer, *, grid_position=None, grid_rect=None)`), `map_to_simple_call_node` detects the gap and returns `self`. Then `GeneralCallNode.analyse_types` calls `coerce_to_pyobject` on the function, which via `AttributeNode.coerce_to` (`is_cmethod and is_overridable`) calls `analyse_as_python_attribute`, setting `is_py_attr=1`. **Bug fixed**: `AttributeNode.infer_type` was calling `self.analyse_attribute(env)` (which resets `is_py_attr=0`) after this setup — triggered by `ForInStatNode`'s loop-variable type inference chain. Fix: early-return `py_object_type` in `infer_type` when `is_py_attr` is already set. **Performance note**: the gap call falls back to Python dispatch, losing the C-call speedup for that method. A future optimization could fill the opt_args struct with `NULL` for the missing args and do a direct C call.
- **Same-module `super().method()` was missing `wrapper_call=True`** (`Optimize.py:_handle_simple_base_method_call`, ~1919): The cross-module path (line 1911) correctly set `wrapper_call=True` (→ `skip_dispatch=1`). The same-module path did NOT, generating `skip_dispatch=0`. This caused cpdef `__init__` dispatch checks to call the subclass's `__init__` (e.g. `LevelHUD.__init__`) with wrong args when a base `__init__` (e.g. `PresentationHostNode.__init__`) ran its override check. Fix: add `call_node.wrapper_call = True` to the same-module path too.
- **wrapper_call controls skip_dispatch**: `c_call_code` (`ExprNodes.py`) inserts `__pyx_skip_dispatch=1` when `self.wrapper_call=True`, `0` otherwise. Any synthesised C call that should call the target directly (not re-dispatch) must set `wrapper_call=True`.
- **wrapper/trampoline functions and opt_arg_struct override** (`Nodes.py:generate_function_header`, `generate_wrapper_functions`): When a child class overrides a parent cpdef method that had optional args but the child has none, the wrapper must declare the parent's opt_arg_struct as `CYTHON_UNUSED` in its header to match the vtable slot signature. `generate_function_header` takes an `opt_arg_struct` override parameter; `generate_wrapper_functions` passes `entry.type.op_arg_struct` when `entry.type.optional_arg_count > 0 and not self.type.optional_arg_count`.
- **NEVER LET TEST FAILING JUST BECAUSE THEY ARE PRE-EXISTING ISSUES**: Just fix the compiler, I don't care if you don't introduced the issue. It is not acceptable to leave the repository without a clean test run of the test suite. The canonical full CI command (all backends including cpp11/17/20) is: `CXX=clang++-mp-21 python runtests.py --no-code-style -x Debugger --backends=c,cpp -j32`. clang++-mp-21 (LLVM 21, installed at `/opt/local/libexec/llvm-21/bin/`) is required because older toolchains lack support for cpp17/cpp20 features. Set it via the `CXX` env var.
- **C++ template specialization cname uses function pointer type** (`PyrexTypes.py:best_match`, `ExprNodes.py:IndexNode.calculate_result_code`): When building the specialization cname for a C++ template function (e.g. `std::next_permutation<iter, Compare>`), `CFuncType` template arguments must be emitted as function pointer types (`bool (*)(char, char)`) not function types (`bool (char, char)`). libc++ 21 changed `__comp_ref_type<Compare>` = `Compare&`, so instantiating `Compare = bool(char,char)` produces `bool(char,char)&` which can't bind a function pointer. Fix is in `PyrexTypes.py:best_match` (`_tmpl_arg` helper) and `ExprNodes.py:IndexNode.calculate_result_code` (`_template_arg_code` helper): call `t.declaration_code("*")` instead of `t.empty_declaration_code()` when `t.is_cfunction`.
- **C++20 sync primitives require macOS 11.0** (`runtests.py`): `std::barrier`, `std::semaphore`, `std::stop_token`, `std::jthread`, and related C++20 concurrency types are marked unavailable by libc++ when `-mmacosx-version-min` < 11.0. The general `update_cpp20_extension` uses `min_macos_version="10.13"` (sufficient for most C++20 syntax features). Tests that use these sync primitives must carry `# tag: cpp20_sync` (in addition to `cpp20`), which resolves to `update_cpp20_sync_extension` with `min_macos_version="11.0"`. Currently tagged: `libcpp_stop_token`, `libcpp_threadsync_cpp20`, `cpp_condition_variables_cpp20`.
- **`tests/macos_cpp_bugs.txt`** excludes tests that cannot pass on macOS with libc++ regardless of clang version. Applied unconditionally on macOS (not just in CI). Currently contains only `cpp_stl_cmath_cpp17` (libc++ does not implement C++17 mathematical special functions `std::beta`, `std::legendre`, etc.; they are in libstdc++ but not libc++). All other tests that were previously in this file now pass with clang++-mp-21.

## Architecture

```
Cython/Compiler/   # The compiler pipeline — Main.py, Nodes.py, ExprNodes.py, Code.py, ...
Cython/Utility/    # C utility code templates bundled into generated .c files
Cython/Runtime/    # Runtime support (refnanny)
Cython/Build/      # cythonize, Dependencies
Cython/Includes/   # Standard .pxd files
tests/
  run/        # mode: run (1065 files — main test area)
  compile/    # mode: compile
  errors/     # mode: error
  build/      # srctree end-to-end tests
  broken/     # excluded from normal runs
```

**Console scripts** (from `setup.py`): `cython = Cython.Compiler.Main:setuptools_main`, `cythonize = Cython.Build.Cythonize:main`, `cygdb = Cython.Debugger.Cygdb:main`.

## Install test deps

```bash
pip install -r test-requirements.txt
pip install -r test-requirements-cpython.txt    # CPython only
pip install -r test-requirements-313.txt        # Python 3.13+
```

## CI command (runtests invocation)

```bash
python runtests.py --no-code-style -x Debugger --backends=c,cpp -j32
```

## Real-world validation project: crop-chronicles

`/Users/jairo/repos/crop-chronicles` is a real (non-trivial) game project used to validate that
Cython changes work beyond the unit test suite. The `embed_modules_optimize` work has broken it
before while passing the test suite, so check it for regressions on the constructor/super
optimization work.

- **Build pipeline:** Poetry + scons. The project's own pipeline transpiles pure-Python `.py` into
  `.pyx`, then runs Cython to compile them. **Focus on the Cython behavior only** — the transpile
  pipeline is correct.
- **Generated `.pyx` to inspect:** `build/lib.macos-desktop-clang/cython/` (these are the inputs to
  Cython; debug Cython codegen here, e.g. the generated `.c`).
- **Build output:** `build/lib.macos-desktop-clang/bundle/`.
- **Canonical build command (fish):**
  `poetry run pip uninstall -y Cython ;and poetry lock ;and poetry install --sync ;and poetry run scons bundle mode=local_debug test_runner=1`
- **⚠️ Do NOT run the poetry command from this Cython dev environment** — we are already in an
  activated venv for Cython development, and running poetry as above would corrupt that venv. It is
  listed only for reference / for the user to run.
- **Run the embedded game test runner:**
  `./farm_rush.exe --test-runner test/manual/test_fps_benchmark.py` (from the `bundle/` dir).
- **⚠️ The full build + test runner is slow and produces huge logs.** Always redirect stdout+stderr
  to a file (e.g. `> /tmp/cc_build.log 2>&1`) and run it in the background; never re-run it without
  an intervening code change.
- **Not every crop-chronicles failure is a Cython bug.** The `test_fps_benchmark` runner had TWO
  independent failures: (1) the cross-module `super().__init__()` regression above (a real Cython
  bug — fixed in `Optimize.py`); and (2) an `OverflowError: value too large to convert to int` in
  `tile_map_data.get_static_tile_desc`, which was a **source** bug: `tile_id: int` (= `cython.int`,
  declared via `from cython import int`) is too narrow for raw Tiled GIDs, whose high bits encode
  flip flags (value up to `0xFFFFFFFF`, from the pure-Python `pytiled_parser`). Fixed source-side by
  widening the GID-receiving params to `cython.uint` (`get_static_tile_desc`, `get_tile_by_id`,
  `get_tile_desc`, `is_tile_flipped_horizontally/_vertically` in
  `farm_rush/engine/tilemap/tile_map_data.py` — edit the `.py`, the `.pyx` is generated). Lesson:
  to tell whether a failure is a compiler regression, regenerate the failing `.cpp` with the Cython
  at a known-good commit (e.g. one tagged "Green … compiling project too") via a `git worktree` and
  diff the relevant codegen — if it's byte-identical, the cause is source/data, not Cython.
- **`python_subclassing=False` is set globally** in `builder/native_codegen.py:DEFAULT_CYTHON_COMPILER_DIRECTIVES`. Known classes in crop-chronicles that still need fixing: `IObservableGroup` in `farm_rush/engine/i_game_node.py:91` (pure Python class inheriting from `IGroup` cclass — needs `@cclass`); `KeyFrameAnimationFloat` and `KeyFrameAnimationVector2` inherit from `AnimationValueBase` and override `_compute_value` — since `python_subclassing=False` suppresses dispatch, those overrides are never called via C; they too need `@cclass` or their base needs `@cython.python_subclassing(True)`.
- **Fast codegen check (no full build):** to verify Cython output for a single generated `.pyx`
  without the multi-minute scons build, run `Cython.Compiler.Main.compile` directly from a tiny
  driver: `chdir` into `build/lib.macos-desktop-clang/cython/`, set `Options.cimport_from_pyx=True`,
  pass `--cplus --no-docstrings --fast-fail`, the directives from
  `builder/native_codegen.py:DEFAULT_CYTHON_COMPILER_DIRECTIVES` (`auto_cpdef=True`, `lto=True`,
  `language_level=3`, `python_subclassing=False`, …), `--include-dir .` **and** `--include-dir <crop-chronicles repo root>`
  (some `.pxd` like `sdl2_capi.pxd` live in the source tree, not the generated dir), and
  `--output-file /tmp/foo.cpp` so you don't clobber the build cache. Then grep the `.cpp` for the
  codegen of interest.
- **Updating the dev Cython without a full reinstall:** crop-chronicles consumes Cython as the local
  wheel `dist/cython-3.3.0a0-cp313-cp313-macosx_15_0_arm64.whl` (pinned by exact filename in
  `pyproject.toml`). `Optimize.py` (and most `Compiler/*.py`) ship as **pure `.py`** inside that
  wheel, so you can swap the fixed file into the existing wheel (preserving filename/tag/compiled
  `.so`s) and regenerate the `.dist-info/RECORD` line for it, rather than rebuilding the wheel.
  Run the build with `env -u VIRTUAL_ENV -u PYTHONPATH poetry …` so Poetry uses its own managed venv
  (`~/Library/Caches/pypoetry/virtualenvs/farm-rush-*`) instead of the active Cython dev venv —
  otherwise `poetry install --sync` corrupts the Cython dev venv.
- **⚠️ There are multiple Poetry venvs for farm-rush — always identify the active one first.**
  `ls ~/Library/Caches/pypoetry/virtualenvs/ | grep farm` lists them all (there may be 5+). The
  active one for the current lock file is given by `cd /Users/jairo/repos/crop-chronicles && poetry
  env info --path`. Copy compiler files into THAT venv's `lib/python3.13/site-packages/Cython/Compiler/`
  and delete `__pycache__/*.pyc` for the changed files — stale bytecode will shadow your edits.
- **⚠️ TWO caches will silently serve stale output when the Cython *version* is unchanged
  (`3.3.0a0`); both bit me hard:**
  1. **Poetry/pip won't reinstall** a same-version path wheel even after `pip uninstall` + `poetry
     lock` + `poetry install` — the venv keeps the OLD `Optimize.py`. **Verify** with
     `grep <your-change> <poetry-venv>/lib/python3.13/site-packages/Cython/Compiler/Optimize.py`.
     The reliable fix is to copy your edited `Optimize.py` **directly** into that site-packages dir
     (then run scons only — do NOT re-run `poetry install`, which would overwrite it with the stale
     wheel).
  2. **The Cython compile cache** at `/Users/jairo/Library/Caches/cython` (`--cache` is passed by the
     pipeline) is keyed on source+directives+Cython *version*, not the compiler's file contents, so
     it returns `.cpp` generated by the previous compiler. `rm -rf /Users/jairo/Library/Caches/cython`
     before rebuilding. Also delete the already-generated `.cpp`/`.o` under
     `build/lib.macos-desktop-clang/cython/` (keep `.pyx`/`.pxd`) to force scons to regenerate.
- **Validating trampolines in crop-chronicles codegen:** after a successful build, check
  `build/lib.macos-desktop-clang/cython/farm_rush/engine/nodes/game_node2d.cpp` (or any other
  generated `.cpp`). Two things to grep:
  1. `grep -oE "__pyx_f_[a-zA-Z0-9_]*hit_test_point[a-zA-Z0-9_]*" game_node2d.cpp | sort -u` —
     must show `__pyx_f_..._GameNode2D_hit_test_point` (the C trampoline body). If only `__pyx_pf_`
     and `__pyx_pw_` appear, the trampoline did not fire.
  2. `grep "hit_test_point" game_node2d.cpp | grep vtable` — must show
     `__pyx_vtable_...GameNode2D.__pyx_base.hit_test_point = (cast)__pyx_f_..._GameNode2D_hit_test_point`.
     The `.__pyx_base.hit_test_point` confirms the inherited vtable slot (not a new one) is filled.
- **crop-chronicles source change (trampoline-related):** `@no_ccall` was removed from
  `hit_test_point` in `farm_rush/engine/nodes/game_node.py` (the base, which has a cpdef-compatible
  body `raise NotImplementedError()`). The override in `game_node2d.py` is a generator (`yield self`)
  and gets a C trampoline automatically. This lets all `b.hit_test_point(pointer)` calls where
  `b: IGameNode2D` use vtable dispatch instead of Python. The corresponding generated `.pyx` at
  `build/lib.macos-desktop-clang/cython/farm_rush/engine/nodes/game_node.pyx` was also updated
  to remove `@no_ccall` (scons will regenerate it from source on the next full build anyway).
