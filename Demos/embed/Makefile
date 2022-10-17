# Makefile for creating our standalone Cython program
PYTHON := python
PYVERSION := $(shell $(PYTHON) -c "import sys; print(sys.version[:3])")
PYPREFIX := $(shell $(PYTHON) -c "import sys; print(sys.prefix)")

INCDIR := $(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_python_inc())")
PLATINCDIR := $(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_python_inc(plat_specific=True))")
LIBDIR1 := $(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_config_var('LIBDIR'))")
LIBDIR2 := $(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_config_var('LIBPL'))")
PYLIB := $(shell $(PYTHON) -c "from distutils import sysconfig; print(sysconfig.get_config_var('LIBRARY')[3:-2])")

CC := $(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('CC'))")
LINKCC := $(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('LINKCC'))")
LINKFORSHARED := $(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('LINKFORSHARED'))")
LIBS := $(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('LIBS'))")
SYSLIBS :=  $(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('SYSLIBS'))")

.PHONY: paths all clean test

paths:
	@echo "PYTHON=$(PYTHON)"
	@echo "PYVERSION=$(PYVERSION)"
	@echo "PYPREFIX=$(PYPREFIX)"
	@echo "INCDIR=$(INCDIR)"
	@echo "PLATINCDIR=$(PLATINCDIR)"
	@echo "LIBDIR1=$(LIBDIR1)"
	@echo "LIBDIR2=$(LIBDIR2)"
	@echo "PYLIB=$(PYLIB)"
	@echo "CC=$(CC)"
	@echo "LINKCC=$(LINKCC)"
	@echo "LINKFORSHARED=$(LINKFORSHARED)"
	@echo "LIBS=$(LIBS)"
	@echo "SYSLIBS=$(SYSLIBS)"

embedded: embedded.o
	$(LINKCC) -o $@ $^ -L$(LIBDIR1) -L$(LIBDIR2) -l$(PYLIB) $(LIBS) $(SYSLIBS) $(LINKFORSHARED)

embedded.o: embedded.c
	$(CC) -c $^ -I$(INCDIR) -I$(PLATINCDIR)

CYTHON := ../../cython.py
embedded.c: embedded.pyx
	@$(PYTHON) $(CYTHON) --embed embedded.pyx

all: embedded

clean:
	@echo Cleaning Demos/embed
	@rm -f *~ *.o *.so core core.* *.c embedded test.output

test: clean all
	LD_LIBRARY_PATH=$(LIBDIR1):$$LD_LIBRARY_PATH ./embedded > test.output
	$(PYTHON) assert_equal.py embedded.output test.output
