"""
Initial cleanup and 'calibration':
>>> _ = gc.collect()
>>> old_unreachable = len(gc.garbage)

Test:
>>> x = SimpleGarbage()
SimpleGarbage(1) __cinit__
>>> del x
SimpleGarbage(1) __dealloc__
Collector.__dealloc__

Make sure nothing changed in the environment:
>>> new_unreachable = get_new_unreachable()
>>> new_unreachable == old_unreachable or (old_unreachable, new_unreachable)
True
"""

import gc

cdef Py_ssize_t new_unreachable = 0

def get_new_unreachable():
    return new_unreachable

cdef int counter = 0
cdef int next_counter():
    global counter
    counter += 1
    return counter

cdef class Collector:
    # Indirectly trigger garbage collection in SimpleGarbage deallocation.
    # The __dealloc__ method of SimpleGarbage won't trigger the bug as the
    # refcount is artificially inflated for the duration of that function.
    def __dealloc__(self):
        print "Collector.__dealloc__"
        global new_unreachable
        gc.collect()
        new_unreachable = len(gc.garbage)

cdef class SimpleGarbage:
    cdef Collector c  # to participate in garbage collection
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
