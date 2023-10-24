import numpy as np

cdef const f64[:] myslice   # const item type => read-only view

a = np.linspace(0, 10, num=50)
a.setflags(write=false)
myslice = a
