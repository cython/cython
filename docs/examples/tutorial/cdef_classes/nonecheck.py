# cython: nonecheck=True
#        ^^^ Turns on nonecheck globally

import cython

@cython.cclass
class MyClass:
    pass

# Turn off nonecheck locally for the function
@cython.nonecheck(False)
def func():
    obj: MyClass = None
    try:
        # Turn nonecheck on again for a block
        with cython.nonecheck(True):
            print(obj.myfunc())  # Raises exception
    except AttributeError:
        pass
    print(obj.myfunc())  # Hope for a crash!
