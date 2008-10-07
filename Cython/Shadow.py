compiled = False

def empty_decorator(x):
    return x

def locals(**arg_types):
    return empty_decorator


# Emulated language constructs

def cast(type, arg):
    if callable(type):
        return type(arg)
    else:
        return arg

def sizeof(arg):
    return 1
    
def address(arg):
    return pointer(type(arg))([arg])
    
def declare(type=None, value=None, **kwds):
    if type and callable(type):
        if value:
            return type(value)
        else:
            return type()
    else:
        return value

# Emulated types

class CythonType(object):

    def _pointer(self, n=1):
        for i in range(n):
            self = pointer(self)
        return self

    def __getitem__(self, ix):
        return array(self, ix)


class PointerType(CythonType):

    def __init__(self, value=None):
        if isinstance(value, ArrayType):
            self._items = [cast(self._basetype, a) for a in value._items]
        elif isinstance(value, list):
            self._items = [cast(self._basetype, a) for a in value]
        elif value is None:
            self._items = []
        else:
            raise ValueError
            
    def __getitem__(self, ix):
        if ix < 0:
            raise IndexError, "negative indexing not allowed in C"
        return self._items[ix]
        
    def __setitem__(self, ix, value):
        if ix < 0:
            raise IndexError, "negative indexing not allowed in C"
        self._items[ix] = cast(self._basetype, value)
        
class ArrayType(PointerType):
    
    def __init__(self):
        self._items = [None] * self._n


class StructType(CythonType):
    
    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)
            
    def __setattr__(self, key, value):
        if key in self._members:
            self.__dict__[key] = cast(self._members[key], value)
        else:
            raise AttributeError, "Struct has no member '%s'" % key
    

class UnionType(CythonType):

    def __init__(self, **data):
        if len(data) > 0:
            raise AttributeError, "Union can only store one field at a time."
        for key, value in data.items():
            setattr(self, key, value)
            
    def __setattr__(self, key, value):
        if key in '__dict__':
            CythonType.__setattr__(self, key, value)
        elif key in self._members:
            self.__dict__ = {key: cast(self._members[key], value)}
        else:
            raise AttributeError, "Union has no member '%s'" % key

def pointer(basetype):
    class PointerInstance(PointerType):
        _basetype = basetype
    return PointerInstance

def array(basetype, n):
    class ArrayInstance(ArrayType):
        _basetype = basetype
        _n = n
    return ArrayInstance

def struct(**members):
    class StructInstance(StructType):
        _members = members
    for key in members.keys():
        setattr(StructInstance, key, None)
    return StructInstance

def union(**members):
    class UnionInstance(UnionType):
        _members = members
    for key in members.keys():
        setattr(UnionInstance, key, None)
    return UnionInstance

class typedef(CythonType):

    def __init__(self, type):
        self._basetype = type
    
    def __call__(self, value=None):
        if value is not None:
            value = cast(self._basetype, value)
        return value
        


py_int = int
py_long = long
py_float = float


# Predefined types

int_types = ['char', 'short', 'int', 'long', 'longlong', 'Py_ssize_t'] 
float_types = ['double', 'float']
other_types = ['bint', 'Py_ssize_t', 'void']
gs = globals()

for name in int_types:
    gs[name] = typedef(py_int)
    gs['u'+name] = typedef(py_int)
    
double = float = typedef(py_float)
bint = typedef(bool)
void = typedef(int)

for t in int_types + float_types + other_types:
    for i in range(1, 4):
        gs["%s_%s" % ('p'*i, t)] = globals()[t]._pointer(i)

void = typedef(None)
NULL = None
