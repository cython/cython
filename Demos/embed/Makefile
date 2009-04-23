# Makefile for creating our standalone Cython program
PYVERSION=2.3
PYPREFIX=/usr
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
	@rm -f *~ *.o *.so core core.* *.c embedded
