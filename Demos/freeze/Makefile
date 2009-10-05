CC = gcc
CYTHON = ../../bin/cython
CYTHON_FREEZE = ../../bin/cython_freeze
PYTHON = python

PY_LDFLAGS = $(shell $(PYTHON) -c 'from distutils.sysconfig import get_config_var as g; print " ".join([g("LINKFORSHARED"), "-L"+g("LIBPL")])')
PY_CPPFLAGS = $(shell $(PYTHON) -c 'from distutils.sysconfig import *; print "-I"+get_python_inc()')
PY_LDLIBS = $(shell $(PYTHON) -c 'from distutils.sysconfig import get_config_var as g; print " ".join(["-lpython"+g("VERSION"), g("SYSLIBS"), g("LIBS"), g("LOCALMODLIBS")])')

CFLAGS = -fPIC -g -O2 -Wall -Wextra
CPPFLAGS = $(PY_CPPFLAGS)
LDFLAGS = $(PY_LDFLAGS)
LDLIBS = $(PY_LDLIBS)


# Name of executable
TARGETS = nCr python

# List of Cython source files, with main module first.
CYTHON_SOURCE = combinatorics.pyx cmath.pyx
CYTHON_SECONDARY = $(CYTHON_SOURCE:.pyx=.c) $(TARGETS:=.c)


all : $(TARGETS)

$(TARGETS) : % : %.o $(CYTHON_SOURCE:.pyx=.o)

nCr.c :
	$(CYTHON_FREEZE) $(CYTHON_SOURCE:.pyx=) > $@

python.c :
	$(CYTHON_FREEZE) --pymain $(CYTHON_SOURCE:.pyx=) > $@

%.c : %.pyx
	$(CYTHON) $(CYTHONFLAGS) $^

clean:
	$(RM) *.o $(CYTHON_SECONDARY) $(TARGETS)

.PHONY: clean
.SECONDARY: $(CYTHON_SECONDARY)
