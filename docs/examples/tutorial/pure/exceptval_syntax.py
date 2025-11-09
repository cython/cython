from cython import exceptval
@exceptval(-1)
def func_a():
    pass
@exceptval(-1, check=False)
def func_b():
    pass
@exceptval(check=True)
def func_c():
    pass   
@exceptval(-1, check=True)
def func_d():
    pass
@exceptval(check=False)
def func_e():
    pass
