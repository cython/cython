def empty_decorator(x):
    return x

def locals(**arg_types):
    return empty_decorator

def cast(type, arg):
    # can/should we emulate anything here?
    return arg

py_int = int
py_long = long
py_float = float

# They just have to exist...
int = long = char = bint = uint = ulong = longlong = ulonglong = Py_ssize_t = float = double = None
