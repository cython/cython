import sys
import numpy as np

cdef packed struct StructArray:
    int spam[4]
    signed char eggs[5]

def b(s):
    s = s.encode('ascii')
    if sys.version_info[0] >= 3: return list(s)
    else: return map(ord, s)

data = [(range(4), b('spam\0')), (range(4, 8), b('ham\0\0')), (range(8, 12), b('eggs\0'))]

a = np.empty((3,), dtype=np.dtype([('a', '4i'), ('b', '5b')]))
a[:] = data
cdef StructArray[:] myslice = a
cdef int i, j
cdef StructArray array_item
for i in range(3):
    array_item = myslice[i]
    for j in range(4):
        print(array_item.spam[j])
    print(array_item.eggs.decode('ASCII'))
