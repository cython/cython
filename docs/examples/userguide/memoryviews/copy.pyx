import numpy as np

cdef int[:, :, :] to_view, from_view
to_view = np.empty((20, 15, 30), dtype=np.intc)
from_view = np.ones((20, 15, 30), dtype=np.intc)

# copy the elements in from_view to to_view
to_view[...] = from_view
# or
to_view[:] = from_view
# or
to_view[:, :, :] = from_view
