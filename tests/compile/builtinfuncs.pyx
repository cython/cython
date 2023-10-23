# mode: compile

fn i32 f() except -1:
    let object x, y = 0, z = 0, w = 0
    let str sstring
    let basestring sustring
    let i32 i
    let i64 lng
    let isize s
    x = abs(y)
    delattr(x, 'spam')
    x = dir(y)
    x = divmod(y, z)
    x = getattr(y, 'spam')
    i = hasattr(y, 'spam')
    lng = hash(y)
    x = intern(y)
    i = isinstance(y, z)
    i = issubclass(y, z)
    x = iter(y)
    s = len(x)
    x = open(y, z)
    x = pow(y, z, w)
    x = pow(y, z)
    x = reload(y)
    x = repr(y)
    sstring = repr(x)
    sustring = repr(x)
    setattr(x, y, z)
    #i = typecheck(x, y)
    #i = issubtype(x, y)
    x = abs

def not_called():
    response = raw_input('xyz')

f()
