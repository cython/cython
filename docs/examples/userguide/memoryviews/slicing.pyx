import numpy as np

exporting_object = np.empty((15, 10, 20), dtype=np.intc)

cdef int[:, :, :] my_view = exporting_object

# These are all equivalent
my_view[10]
my_view[10, :, :]
my_view[10, ...]
