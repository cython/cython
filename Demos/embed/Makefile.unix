PYVERSION = 2.2
PYHOME = $(HOME)/pkg/python/$(PYVERSION)
PYARCH = $(PYHOME)/$(ARCH)
PYINCLUDE = \
	-I$(PYHOME)/include/python$(PYVERSION) \
	-I$(PYARCH)/include/python$(PYVERSION)
PYLIB = -L$(PYARCH)/lib/python$(PYVERSION)/config \
	-lpython$(PYVERSION) \
	-ldl -lpthread -lutil -lm

%.c:	%.pyx
	../../bin/pyrexc $<

%.o:	%.c
	gcc -c -fPIC $(PYINCLUDE) $<

#%.so:	%.o
#	gcc -shared $< -lm -o $@

all:	main

main:	main.o embedded.o
	gcc main.o embedded.o $(PYLIB) -o main

clean:
	@echo Cleaning Demos/embed
	@rm -f *~ *.o *.so core core.* embedded.h embedded.c main

embedded.h:	embedded.c
main.o:		embedded.h
