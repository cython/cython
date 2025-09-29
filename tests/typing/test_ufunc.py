from _cython_local import ufunc

@ufunc
def square(x: int) -> int:
    return x * x

reveal_type(square)  # E: Revealed type is "def (x: builtins.int) -> builtins.int"
