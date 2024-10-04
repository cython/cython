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
    python_cmd = """
import os
import sys

n = len(sys.argv)
for src, dst in zip(sys.argv[1:], sys.argv[1+n//2:]):
    src_file_name = src.split(".")[0]
    src = src_file_name + ".so"
    try:
        os.rename(src, dst)
    except Exception as e:
        print("Failed to rename: " + src + " to " + dst)
        dir = os.path.dirname(src_file_name)
        renamed_candidate = False
        for file_name in os.listdir(dir):
            file, ext = os.path.splitext(file_name)
            if ext != ".so":
                continue
            if not file.startswith(os.path.basename(src_file_name)):
                continue
            file_dot_split = file.split(".")
            if len(file_dot_split) >= 2 and ".".join(file_dot_split[:-2]) == src_file_name:
                potential_src_file_name = os.path.join(dir, file_name)
                try:
                    os.rename(potential_src_file_name, dst)
                    renamed_candidate = True
                except Exception as e2:
                    print("Failed to rename: " + potential_src_file_name + " to " + dst)
                    raise e2
        if not renamed_candidate:
            raise e
"""
    native.genrule(
        name = name + "_cythonize",
        srcs = pyx_srcs,
        outs = outs,
        cmd = "PYTHONHASHSEED=0 $(location @cython//:cythonize) -k -i %s $(SRCS)" % extra_flags
              # Rename outputs to expected location.
              # TODO(robertwb): Add an option to cythonize itself to do this.
              + """ && python -c '%s' $(SRCS) $(OUTS)""" % python_cmd,
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
