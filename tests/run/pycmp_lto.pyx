# mode: run
# tag: comparison,int,pylong,float,total_ordering,gh7908
# distutils: extra_compile_args = -O3 -flto=auto

# -flto=auto made this test fail in GCC.
# See https://github.com/cython/cython/issues/7908

include "pycmp.pyx"
