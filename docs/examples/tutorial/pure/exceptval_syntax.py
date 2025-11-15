from cython import exceptval, cfunc, int as cython_int

@exceptval(-1)
@cfunc
def func_a() -> cython_int:
    return 0

@exceptval(-1, check=False)
@cfunc
def func_b() -> cython_int:
    return 0

@exceptval(check=True)
@cfunc
def func_c() -> cython_int:
    return 0

@exceptval(-1, check=True)
@cfunc
def func_d() -> cython_int:
    return 0

@exceptval(check=False)
@cfunc
def func_e() -> cython_int:
    return 0
