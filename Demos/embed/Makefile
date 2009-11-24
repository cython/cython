# Makefile for creating our standalone Cython program
PYVERSION=$(shell python -c "import sys; print sys.version[:3]")
PYPREFIX=$(shell python -c "import sys; print sys.prefix")
LINKFORSHARED=$(shell python -c "import distutils.sysconfig; print distutils.sysconfig.get_config_var('LINKFORSHARED')")
INCLUDES=-I$(PYPREFIX)/include/python$(PYVERSION)

embedded: embedded.o
	gcc -o $@ $^ $(LINKFORSHARED) -lpython$(PYVERSION) -lm -lpthread -ldl -lutil

embedded.o: embedded.c
	gcc -c $^ $(INCLUDES)

embedded.c: embedded.pyx
	@python ../../cython.py --embed embedded.pyx

all: embedded

clean:
	@echo Cleaning Demos/embed
	@rm -f *~ *.o *.so core core.* *.c embedded test.output

test: clean all
	./embedded > test.output
	python assert_equal.py embedded.output test.output
