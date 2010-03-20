# Makefile for creating our standalone Cython program
PYTHON=python
PYVERSION=$(shell $(PYTHON) -c "import sys; print(sys.version[:3])")
PYPREFIX=$(shell $(PYTHON) -c "import sys; print(sys.prefix)")
LINKFORSHARED=$(shell $(PYTHON) -c "import distutils.sysconfig; print(distutils.sysconfig.get_config_var('LINKFORSHARED'))")
INCLUDES=-I$(PYPREFIX)/include/python$(PYVERSION)

embedded: embedded.o
	gcc -o $@ $^ $(LINKFORSHARED) -lpython$(PYVERSION) -lm -lpthread -ldl -lutil -L$(PYPREFIX)/lib

embedded.o: embedded.c
	gcc -c $^ $(INCLUDES)

embedded.c: embedded.pyx
	@$(PYTHON) ../../cython.py --embed embedded.pyx

all: embedded

clean:
	@echo Cleaning Demos/embed
	@rm -f *~ *.o *.so core core.* *.c embedded test.output

test: clean all
	./embedded > test.output
	$(PYTHON) assert_equal.py embedded.output test.output
