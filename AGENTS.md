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
- **Cross-module `super().method()` uses vtable dispatch**: `_handle_simple_base_method_call` (`Optimize.py:1808`) optimizes `super().method()` in `@cclass`. Same-module target → direct `__pyx_f_<Owner>_<method>(self, …, 0)` call. Cross-module target (base class in another module, e.g. `A(B)` with `A` in `a.pyx`, `B` in `b.pyx`) must NOT bail to the Python `super()` + `FastCallMethod` fallback — the target C function is `static` in its own module. Instead dispatch through the base type's exported vtable pointer (imported via `__Pyx_GetVtable`), mirroring the `is_cproperty` branch of `_handle_simple_base_property_access`: `vtable_call = "%s->%s" % (base_type.vtabptr_cname, base_entry.cname)` wrapped in a `RawCNameExprNode(type=base_entry.type, cname=vtable_call)`. Use `base_type.scope.lookup(attr)` (not `lookup_here`) so the entry's `cname` matches the (prefix-stripped) vtable struct member name (e.g. `__pyx___init__`). `skip_dispatch=0` is appended automatically and is safe for cclasses (the dispatch guard `tp_dictoffset != 0 || HEAPTYPE` is false for static extension types). This applies to `__init__` and any cdef/cpdef method; `tests/build/embed_modules_optimize.srctree`'s `check_codegen.py` asserts no `FastCallMethod(...__pyx_n_u_init` survives.
- **Deleting Code.so enables python-mode**: Should delete all .so or .pyd files under `Cython/` otherwise we end up using stale code.
- **@final property getters get final_func_cname**: `PropertyScope.declare_cfunction` (`Symtab.py:3072`) must set `is_final_cmethod=True` and `final_func_cname=func_cname` when `parent_type.is_final_type`, mirroring `ClassScope.declare_cfunction`. In `c_call_code`, check `not func_entry.final_func_cname` to skip vtable dispatch for final types.
- **`.py` tests** get `import cython` auto-injected when `add_cython_import=True`
- **CFLAGS `-O0` or `-Og`** cuts test suite runtime by ~2x
- **Tree path assertions** (`@cython.test_assert_path_exists`, `@cython.test_fail_if_path_exists`) test that optimizations fire. They use XPath-like `TreePath` expressions.
- **NEVER LET TEST FAILING JUST BECAUSE THEY ARE PRE-EXISTING ISSUES**: Just fix the compiler, I don't care if you don't introduced the issue. It is not acceptable to leave the repository without a clean test run of the test suite: `python3.13 runtests.py --no-code-style -x Debugger -x tag:cpp20 -x tag:cpp17 -x tag:cpp11 -x tag:pythran -x tag:numpy --backends=c,cpp -j32`

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
