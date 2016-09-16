# Bazel build file for inclusion as external dependency.
#
# Most useful is the pyx_library rule from //Tools:rules.bzl
# which mirrors py_library but compiles .pyx files.

py_library(
    name = "cython_lib",
    srcs = glob(
        ["Cython/**/*.py"],
        exclude = [
            "**/Tests/*.py",
        ],
    ) + ["cython.py"],
    data = glob([
        "Cython/**/*.pyx",
        "Cython/Utility/*.*",
        "Cython/Includes/**/*.pxd",
    ]),
    visibility = ["//visibility:public"],
)

py_binary(
    name = "cythonize",
    srcs = ["cythonize.py"],
    visibility = ["//visibility:public"],
    deps = ["cython_lib"],
)

py_binary(
    name = "cython",
    srcs = ["cython.py"],
    visibility = ["//visibility:public"],
    deps = ["cython_lib"],
)
