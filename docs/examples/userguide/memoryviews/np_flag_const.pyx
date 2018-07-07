import numpy as np

cdef const double[:] myslice   # const item type => read-only view

a = np.linspace(0, 10, num=50)
a.setflags(write=False)
myslice = a
