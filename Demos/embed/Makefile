# Makefile for creating our standalone Cython program
PYVERSION=$(shell python -c "import sys; print sys.version[:3]")
PYPREFIX=$(shell python -c "import sys; print sys.prefix")
INCLUDES=-I$(PYPREFIX)/include/python$(PYVERSION)

embedded: embedded.o
	gcc -o $@ $^ -lpython$(PYVERSION)

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
