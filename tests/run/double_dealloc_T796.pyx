"""
>>> x = SimpleGarbage()
SimpleGarbage(1) __cinit__
>>> del x
SimpleGarbage(1) __dealloc__
Collector.__dealloc__
collect 0
"""

import gc, sys, weakref

cdef int counter = 0
cdef int next_counter():
    global counter
    counter += 1
    return counter

cdef class Collector:
    # Indirectly trigger garbage collection in SimpleGarbage deallocation.
    # The __dealloc__ method of SimpleGarbage won't trigger the bug as the
    # refcount is artifitially inflated for the durration of that function.
    def __dealloc__(self):
        print "Collector.__dealloc__"
        print "collect", gc.collect()

cdef class SimpleGarbage:
    cdef Collector c # to particpate in garbage collection
    cdef int index
    cdef bint deallocated
    def __cinit__(self):
        self.index = next_counter()
        self.c = Collector()
        print self, "__cinit__"
    def __dealloc__(self):
        print self, "__dealloc__"
        if self.deallocated:
            print "Double dealloc!"
        self.deallocated = True
        gc.collect()
    def __str__(self):
        return "SimpleGarbage(%s)" % self.index
    def __repr__(self):
        return "SimpleGarbage(%s)" % self.index
