CC = gcc
CYTHON = ./../bin/cython
CYTHON_FREEZE = ../../bin/cython_freeze.py

CFLAGS = -fPIC -g -O2 -Wall -Wextra
CPPFLAGS = -I /usr/include/python2.6
LDFLAGS = -Xlinker -export-dynamic -Wl,-O1 -Wl,-Bsymbolic-functions
LDLIBS = /usr/lib/python2.6/config/libpython2.6.a \
	-lm -ldl -pthread -lutil -lz


# Name of executable
TARGET = nCr

# List of Cython source files, with main module first.
CYTHON_SOURCE = combinatorics.pyx cmath.pyx


all : $(TARGET)

$(TARGET) : $(TARGET).o $(CYTHON_SOURCE:.pyx=.o)

$(TARGET).c :
	$(CYTHON_FREEZE) $(CYTHON_SOURCE:.pyx=) > $@

%.c : %.pyx
	$(CYTHON) $(CYTHONFLAGS) $^

clean:
	$(RM) *.o *.c $(TARGET)

.PHONY: clean
.SECONDARY: $(CYTHON_SOURCE:.pyx=.c)
