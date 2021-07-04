# mode: run
# tag: cpp, cpp11

from libcpp.functional cimport function
cimport cpp_function_lib

def test_simple_function():
    '''
    >>> test_simple_function()
    6.0
    '''
    return cpp_function_lib.add_one(2.0, 3)


def test_AddAnotherFunctor(n):
    '''
    >>> test_AddAnotherFunctor(5.0)
    10.0
    '''
    return cpp_function_lib.AddAnotherFunctor(5.0).call(2.0, 3)


cdef class FunctionKeeper:
    """
    >>> fk = FunctionKeeper('add_one')
    >>> fk(2.0, 3)
    6.0
    >>> fk = FunctionKeeper('add_two')
    >>> fk(2.0, 3)
    7.0
    >>> fk = FunctionKeeper('AddAnotherFunctor5')
    >>> fk(2.0, 3)
    10.0
    >>> fk = FunctionKeeper('default')
    >>> bool(fk)
    False
    >>> fk(2.0, 3)
    Traceback (most recent call last):
    ...
    RuntimeError: Trying to call undefined function!
    >>> fk.set_function('AddAnotherFunctor5')
    >>> fk(2.0, 3)
    10.0
    >>> bool(fk)
    True
    >>> fk.set_function('NULL')
    >>> bool(fk)
    False
    """
    cdef cpp_function_lib.FunctionKeeper* function_keeper
    
    cdef function[double(double, int)]* _get_function_ptr_from_name(self, function_name):
        cdef function[double(double, int)] *f
        
        if function_name == 'add_one':
            f = new function[double(double, int)](cpp_function_lib.add_one)
        elif function_name == 'add_two':
            f = new function[double(double, int)](cpp_function_lib.add_two)
        elif function_name == 'AddAnotherFunctor5':
            f = new function[double(double, int)]()
            f[0] = cpp_function_lib.AddAnotherFunctor(5.0)
        elif function_name == 'NULL':
            f = new function[double(double, int)](NULL)
        elif function_name == 'default':
            f = new function[double(double, int)]()
            
        return f
   
    def __cinit__(self, function_name):
        cdef function[double(double, int)] *f = self._get_function_ptr_from_name(function_name)
        self.function_keeper = new cpp_function_lib.FunctionKeeper(f[0])
        del f

    def __dealloc__(self):
        del self.function_keeper

    def __call__(self, a, b):
        return self.function_keeper.call_function(a, b)

    def __bool__(self):
        return <bint> self.function_keeper.get_function()

    def set_function(self, function_name):
        cdef function[double(double, int)] *f = self._get_function_ptr_from_name(function_name)
        self.function_keeper.set_function(f[0])
        del f
