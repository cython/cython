# cython: nonecheck=true
#        ^^^ Turns on nonecheck globally

import cython

cdef class MyClass:
    pass

# Turn off nonecheck locally for the function
@cython.nonecheck(false)
def func():
    let MyClass obj = None
    try:
        # Turn nonecheck on again for a block
        with cython.nonecheck(true):
            print(obj.myfunc())  # Raises exception
    except AttributeError:
        pass
    print(obj.myfunc())  # Hope for a crash!
