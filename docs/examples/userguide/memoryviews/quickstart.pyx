from cython.view cimport array as cvarray
import numpy as np

# Memoryview on a NumPy array
narr = np.arange(27, dtype=np.dtype("i")).reshape((3, 3, 3))
cdef int [:, :, :] narr_view = narr

# Memoryview on a C array
cdef int carr[3][3][3]
cdef int [:, :, :] carr_view = carr

# Memoryview on a Cython array
cyarr = cvarray(shape=(3, 3, 3), itemsize=sizeof(int), format="i")
cdef int [:, :, :] cyarr_view = cyarr

# Show the sum of all the arrays before altering it
print("NumPy sum of the NumPy array before assignments: %s" % narr.sum())

# We can copy the values from one memoryview into another using a single
# statement, by either indexing with ... or (NumPy-style) with a colon.
carr_view[...] = narr_view
cyarr_view[:] = narr_view
# NumPy-style syntax for assigning a single value to all elements.
narr_view[:, :, :] = 3

# Just to distinguish the arrays
carr_view[0, 0, 0] = 100
cyarr_view[0, 0, 0] = 1000

# Assigning into the memoryview on the NumPy array alters the latter
print("NumPy sum of NumPy array after assignments: %s" % narr.sum())

# A function using a memoryview does not usually need the GIL
cpdef int sum3d(int[:, :, :] arr) nogil:
    cdef size_t i, j, k, I, J, K
    cdef int total = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total

# A function accepting a memoryview knows how to use a NumPy array,
# a C array, a Cython array...
print("Memoryview sum of NumPy array is %s" % sum3d(narr))
print("Memoryview sum of C array is %s" % sum3d(carr))
print("Memoryview sum of Cython array is %s" % sum3d(cyarr))
# ... and of course, a memoryview.
print("Memoryview sum of C memoryview is %s" % sum3d(carr_view))
