seq = [1, [2, 3]]

def f():
    a, (b, c) = [1, [2, 3]]
    print a
    print b
    print c

def g():
    a, b, c = seq

def h():
    a, = seq
