# mode: compile

def f(a, b):
    global g
    del g
    del a[b]
    del a[b][42]
    del a.spam
    del a.spam.eggs
