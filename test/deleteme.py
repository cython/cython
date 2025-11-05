# cython: infer_types=True
import cython

def main1() -> None:
    a: list[str] = ["meh"]
    b: list[str] = ["meh"]
    print(a[0] + b[0])

def main2() -> None:
    a: list[cython.int] = [1]
    b: list[cython.int] = [2]
    c = a[0] + b[0]
    print(c)

def main3() -> None:
    b: cython.int = 1
    a: list[cython.int] = [2]
    for c in a:
        print(b + c)


# NEGATIVE SC

# def main() -> None:
    # c: list[cython.float] = [5.0]
    # e: cython.int = c[0]

# def main() -> None:
#     a: cython.float = 5.0
#     b: cython.int = a
#     print(b)
# 
#     c: list[cython.float] = [5.0]
#     # c: list[cython.float] = [5.0]
#     d: list[cython.int] = c # This must fail
#     # d: list[cython.int] = [5.0] # This must fail
#     x = c[0]
#     print(x)

main1()
main2()
main3()
