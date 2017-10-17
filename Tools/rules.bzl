"""
Defines a pyx_library() macros corresponding to py_library.

Uses Cython to compile .pyx files (and .py files with corresponding .pxd
files) to Python extension modules.

Example:

# Assuming Cython is mapped to "cython" in your workspace.
load("@cython//Tools:rules.bzl", "pyx_library")

pyx_library(name = 'mylib',
            srcs = ['a.pyx', 'a.pxd', 'b.py', 'pkg/__init__.py', 'pkg/c.pyx'],
            py_deps = ['//py_library/dep'],
            data = ['//other/data'],
)

The __init__.py file must be in your srcs list so that Cython can resolve
cimports using the package layout.
"""

def pyx_library(
        name,
        deps=[],
        srcs=[],
        cython_directives=[],
        cython_options=[],
        **kwargs):
    # First filter out files that should be run compiled vs. passed through.
    py_srcs = []
    pyx_srcs = []
    pxd_srcs = []
    for src in srcs:
        if src.endswith('.pyx') or (src.endswith('.py')
                                    and src[:-3] + '.pxd' in srcs):
            pyx_srcs.append(src)
        elif src.endswith('.py'):
            py_srcs.append(src)
        else:
            pxd_srcs.append(src)
        if src.endswith('__init__.py'):
            # TODO(robertwb): Infer __init__.py files/package root?
            pxd_srcs.append(src)

    # Invoke cythonize to produce the shared object libraries.
    outs = [src.split('.')[0] + '.so' for src in pyx_srcs]
    extra_flags = " ".join(["-X '%s=%s'" % x for x in cython_directives] +
                           ["-s '%s=%s'" % x for x in cython_options])
    # TODO(robertwb): It might be better to only generate the C files,
    # letting cc_library (or similar) handle the rest, but there isn't yet
    # support compiling Python C extensions from bazel.
    native.genrule(
        name = name + "_cythonize",
        srcs = pyx_srcs,
        outs = outs,
        cmd = "PYTHONHASHSEED=0 $(location @cython//:cythonize) -k -i %s $(SRCS)" % extra_flags
              # Rename outputs to expected location.
              # TODO(robertwb): Add an option to cythonize itself to do this.
              + """ && python -c 'import os, sys; n = len(sys.argv); [os.rename(src.split(".")[0] + ".so", dst) for src, dst in zip(sys.argv[1:], sys.argv[1+n//2:])]' $(SRCS) $(OUTS)""",
        tools = ["@cython//:cythonize"] + pxd_srcs,
    )

    # Now create a py_library with these shared objects as data.
    native.py_library(
        name=name,
        srcs=py_srcs,
        deps=deps,
        data=outs + pyx_srcs + pxd_srcs,
        **kwargs
    )
