import numpy as np


array = np.arange(20, dtype=np.intc).reshape((2, 10))

cdef i32[:, ::1] c_contig = array
cdef i32[::1, :] f_contig = c_contig.T
