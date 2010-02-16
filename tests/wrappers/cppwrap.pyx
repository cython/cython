
cimport cppwrap_lib

cdef class DoubleKeeper:
    cdef cppwrap_lib.DoubleKeeper* keeper

    def __cinit__(self, double number):
        self.keeper = new cppwrap_lib.DoubleKeeper(number)

    def __dealloc__(self):
        del self.keeper

    def set_number(self, double number):
        self.keeper.set_number(number)

    def get_number(self):
        return self.keeper.get_number()

    def transmogrify(self, double value):
        return self.keeper.transmogrify(value)


def voidfunc():
    cppwrap_lib.voidfunc()

def doublefunc(double x, double y, double z):
    return cppwrap_lib.doublefunc(x, y, z)

def transmogrify_from_cpp(DoubleKeeper obj not None, double value):
    return cppwrap_lib.transmogrify_from_cpp(obj.keeper, value)
