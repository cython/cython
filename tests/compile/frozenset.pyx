#mode: compile

def f():
    a = frozenset((1,2,3)) | {2,3,4}
    b = {3,4,5} | frozenset((1,2,3))
