u'''
>>> test_is_contiguous()
1 1
0 1
1 0
1 0
<BLANKLINE>
0 1
1 0
>>> call()
1000 2000 3000
1000
2000 3000
3000
1 1 1000
>>> two_dee()
1 2 3 4
-4 -4
1 2 3 -4
1 2 3 -4
>>> fort_two_dee()
1 2 3 4
-4 -4
1 2 3 -4
1 3 2 -4
1 2 3 -4
>>> test_nonecheck1()
Traceback (most recent call last):
  ...
AttributeError: 'NoneType' object has no attribute 'is_c_contig'
>>> test_nonecheck2()
Traceback (most recent call last):
  ...
AttributeError: 'NoneType' object has no attribute 'is_f_contig'
>>> test_nonecheck3()
Traceback (most recent call last):
  ...
AttributeError: 'NoneType' object has no attribute 'copy'
>>> test_nonecheck4()
Traceback (most recent call last):
  ...
AttributeError: 'NoneType' object has no attribute 'copy_fortran'
>>> test_nonecheck5()
Traceback (most recent call last):
  ...
AttributeError: 'NoneType' object has no attribute '_data'
'''

# from cython.view cimport memoryview
cimport cython
from cython cimport array

@cython.nonecheck(True)
def test_nonecheck1():
    cdef int[:,:,:] uninitialized
    print uninitialized.is_c_contig()

@cython.nonecheck(True)
def test_nonecheck2():
    cdef int[:,:,:] uninitialized
    print uninitialized.is_f_contig()

@cython.nonecheck(True)
def test_nonecheck3():
    cdef int[:,:,:] uninitialized
    uninitialized.copy()

@cython.nonecheck(True)
def test_nonecheck4():
    cdef int[:,:,:] uninitialized
    uninitialized.copy_fortran()

@cython.nonecheck(True)
def test_nonecheck5():
    cdef int[:,:,:] uninitialized
    uninitialized._data

def test_is_contiguous():
    cdef int[::1, :, :] fort_contig = array((1,1,1), sizeof(int), 'i', mode='fortran')
    print fort_contig.is_c_contig() , fort_contig.is_f_contig()
    fort_contig = array((200,100,100), sizeof(int), 'i', mode='fortran')
    print fort_contig.is_c_contig(), fort_contig.is_f_contig()
    fort_contig = fort_contig.copy()
    print fort_contig.is_c_contig(), fort_contig.is_f_contig()
    cdef int[:,:,:] strided = fort_contig
    print strided.is_c_contig(), strided.is_f_contig()
    print 
    fort_contig = fort_contig.copy_fortran()
    print fort_contig.is_c_contig(), fort_contig.is_f_contig()
    print strided.is_c_contig(), strided.is_f_contig()


def call():
    cdef int[::1] mv1, mv2, mv3
    cdef array arr = array((3,), sizeof(int), 'i')
    mv1 = arr
    cdef int *data
    data = <int*>arr.data
    data[0] = 1000
    data[1] = 2000
    data[2] = 3000

    print (<int*>mv1._data)[0] , (<int*>mv1._data)[1] , (<int*>mv1._data)[2]

    mv2 = mv1.copy()

    print (<int*>mv2._data)[0]


    print (<int*>mv2._data)[1] , (<int*>mv2._data)[2]

    mv3 = mv2

    cdef int *mv3_data = <int*>mv3._data

    print (<int*>mv1._data)[2]

    mv3_data[0] = 1

    print (<int*>mv3._data)[0] , (<int*>mv2._data)[0] , (<int*>mv1._data)[0]

def two_dee():
    cdef long[:,::1] mv1, mv2, mv3
    cdef array arr = array((2,2), sizeof(long), 'l')

    cdef long *arr_data
    arr_data = <long*>arr.data

    mv1 = arr

    arr_data[0] = 1
    arr_data[1] = 2
    arr_data[2] = 3
    arr_data[3] = 4

    print (<long*>mv1._data)[0] , (<long*>mv1._data)[1] , (<long*>mv1._data)[2] , (<long*>mv1._data)[3]

    mv2 = mv1

    arr_data = <long*>mv2._data

    arr_data[3] = -4

    print (<long*>mv2._data)[3] , (<long*>mv1._data)[3]

    mv3 = mv2.copy()

    print (<long*>mv2._data)[0] , (<long*>mv2._data)[1] , (<long*>mv2._data)[2] , (<long*>mv2._data)[3]

    print (<long*>mv3._data)[0] , (<long*>mv3._data)[1] , (<long*>mv3._data)[2] , (<long*>mv3._data)[3]

def fort_two_dee():
    cdef array arr = array((2,2), sizeof(long), 'l', mode='fortran')
    cdef long[::1,:] mv1, mv2, mv3

    cdef long *arr_data
    arr_data = <long*>arr.data

    mv1 = arr

    arr_data[0] = 1
    arr_data[1] = 2
    arr_data[2] = 3
    arr_data[3] = 4

    print (<long*>mv1._data)[0], (<long*>mv1._data)[1], (<long*>mv1._data)[2], (<long*>mv1._data)[3]

    mv2 = mv1

    arr_data = <long*>mv2._data

    arr_data[3] = -4

    print (<long*>mv2._data)[3], (<long*>mv1._data)[3]

    mv3 = mv2.copy()

    print (<long*>mv2._data)[0], (<long*>mv2._data)[1], (<long*>mv2._data)[2], (<long*>mv2._data)[3]

    print (<long*>mv3._data)[0], (<long*>mv3._data)[1], (<long*>mv3._data)[2], (<long*>mv3._data)[3]

    mv3 = mv3.copy_fortran()

    print (<long*>mv3._data)[0], (<long*>mv3._data)[1], (<long*>mv3._data)[2], (<long*>mv3._data)[3]
