"""
Defines a pyx_library() macros corresponding to py_library.

Uses Cython to compile .pyx files (and .py files with corresponding .pxd
files) to Python extension modules.

Example:

# Assuming Cython is mapped to "cython" in your workspace.
load("@cython//Tools:rules.bzl", "pyx_library")

pyx_library(name = 'mylib',
            srcs = ['a.pyx', 'a.pxd', 'b.py', 'pkg/__init__.py', 'pkg/c.pyx'],
            # python library deps passed to py_library
            deps = ['//py_library/dep']
)

The __init__.py file must be in your srcs list so that Cython can resolve
cimports using the package layout.
"""

load("@rules_cc//cc:defs.bzl", "cc_binary")
load("@rules_python//python:defs.bzl", "py_library")

def pyx_library(
        name,
        cc_deps = [],
        py_deps = [],
        srcs = [],
        copts = None,
        defines = None,
        **kwargs):
    """Compiles a group of .pyx / .pxd / .py files.

    First runs Cython to create .cpp files for each input .pyx or .py + .pxd
    pair. Then builds a shared object for each, passing "cc_deps" to each cc_binary
    rule (includes Python headers by default). Finally, creates a py_library rule
    with the shared objects and any pure Python "srcs", with py_deps as its
    dependencies; the shared objects can be imported like normal Python files.

    Args:
      name: Name for the rule.
      cc_deps: C/C++ dependencies of the Cython (e.g. Numpy headers).
      py_deps: Pure Python dependencies of the final library.
      srcs: .py, .pyx, or .pxd files to either compile or pass through.
      copts: List of copts to pass to cc rules.
      defines: List of defines to pass to cc rules.
      **kwargs: Extra keyword arguments passed to the py_library.
    """

    # First filter out files that should be run compiled vs. passed through.
    py_srcs = []
    pyx_srcs = []
    pxd_srcs = []
    for src in srcs:
        if src.endswith(".pyx") or (src.endswith(".py") and
                                    src[:-3] + ".pxd" in srcs):
            pyx_srcs.append(src)
        elif src.endswith(".py"):
            py_srcs.append(src)
        else:
            pxd_srcs.append(src)
        if src.endswith("__init__.py"):
            pxd_srcs.append(src)

    # Invoke cython to produce the shared object libraries.
    for filename in pyx_srcs:
        native.genrule(
            name = filename + "_cython_translation",
            srcs = [filename],
            outs = [filename.split(".")[0] + ".cpp"],
            # Optionally use PYTHON_BIN_PATH on Linux platforms so that python 3
            # works. Windows has issues with cython_binary so skip PYTHON_BIN_PATH.
            cmd = "PYTHONHASHSEED=0 $(execpath %s) --cplus $(SRCS) --output-file $(OUTS)" % Label("//:cython_binary"),
            testonly = kwargs.get("testonly"),
            tools = [Label("//:cython_binary")] + pxd_srcs,
        )

    shared_objects = []
    for src in pyx_srcs:
        stem = src.split(".")[0]
        shared_object_name = stem + ".so"
        cc_binary(
            name = shared_object_name,
            srcs = [stem + ".cpp"],
            deps = cc_deps + [
                "@rules_python//python/cc:current_py_cc_headers",
                "@rules_python//python/cc:current_py_cc_libs",
            ],
            defines = defines,
            linkshared = 1,
            testonly = kwargs.get("testonly"),
            copts = copts,
        )
        shared_objects.append(shared_object_name)

    # Now create a py_library with these shared objects as data.
    data = shared_objects + kwargs.pop("data", [])
    py_library(
        name = name,
        srcs = py_srcs,
        deps = py_deps,
        data = data,
        **kwargs
    )
