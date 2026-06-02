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
- **Cross-module `super().method()` → unbound C-method call, NOT a hand-built vtable string**: `_handle_simple_base_method_call` (`Optimize.py:1808`) optimizes `super().method()` in `@cclass`. Same-module target → direct `__pyx_f_<Owner>_<method>(self, …)` call (via `RawCNameExprNode(type=resolved_fn.type, …)` where `resolved_fn` comes from the `lookup_here` ancestor walk — a real `CFuncType`). Cross-module target (base class in another module) must NOT bail to the Python `super()` + `FastCallMethod` fallback, but must also NOT hand-build the vtable access string. **Do not** write `"%s->%s" % (base_type.vtabptr_cname, entry.cname)`: (1) when `base_type` only *inherits* the method (doesn't define it), the member is nested under `__pyx_base` in its vtable struct, so a top-level `vtabptr->method` member often doesn't exist; and (2) `base_type.scope.lookup(attr)` on such a class returns the **Python (variable) form** whose `.type` is `py_object`, which makes `SimpleCallNode` emit a Python `FastCall` on a raw C function pointer → garbage args (observed as `OverflowError: value too large to convert to int` deep in unrelated code). Instead, emit an **unbound C-method call** `BaseClass.method(self, …)` via `AttributeNode(obj=NameNode(base_type.name), attribute=resolved_fn.name, needs_none_check=False)` — but **only when `base_type` *directly defines* the method**, so it owns a top-level vtable slot and attribute analysis emits a simple unambiguous dispatch (e.g. `__pyx_vtabptr_1b_B->__pyx___init__(self, 1)`). Otherwise `return node` and let Python `super()` MRO dispatch handle it (always correct). Two guards are needed: `if not method_scope.lookup(base_type.name): return node`, AND a "base defines it directly" check. **Gotcha:** `resolved_type is base_type` and `base_type.scope.lookup_here(attr)` are NOT sufficient — cpdef `__init__` entries are *copied* into every subclass scope, so `lookup_here` returns an entry even when the class doesn't define the method in source. Require a non-inherited entry: `e = base_type.scope.lookup_here(attr); if not (e and e.is_cmethod and not getattr(e, 'is_inherited', False)): return node`. Without this, a deep chain like `RootGameNode → IGameScreenController → … → GameNode` resolves `super().__init__()` to the WRONG nested vtable slot (observed: cast to an unrelated `SpriteBase*` via 6×`__pyx_base`), so the real base `__init__` never runs and its fields stay `None` (e.g. `AttributeError: 'NoneType' object has no attribute 'add_many'`). `tests/build/embed_modules_optimize.srctree`'s `check_codegen.py` asserts no `FastCallMethod(...__pyx_n_u_init` survives there (base `B` *does* define `__init__`, so the vtable optimization fires). The unit tests do NOT cover deep cross-module inheritance — always validate against the crop-chronicles project. Fully reproducing Python MRO chaining for *inherited* cross-module methods is the job of the larger constructor rewrite, not this pass.
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
- **Fast codegen check (no full build):** to verify Cython output for a single generated `.pyx`
  without the multi-minute scons build, run `Cython.Compiler.Main.compile` directly from a tiny
  driver: `chdir` into `build/lib.macos-desktop-clang/cython/`, set `Options.cimport_from_pyx=True`,
  pass `--cplus --no-docstrings --fast-fail`, the directives from
  `builder/native_codegen.py:DEFAULT_CYTHON_COMPILER_DIRECTIVES` (`auto_cpdef=True`, `lto=True`,
  `language_level=3`, …), `--include-dir .` **and** `--include-dir <crop-chronicles repo root>`
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
