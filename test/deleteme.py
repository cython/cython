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

def main4() -> None:
    # a: list[list[cython.int]] = [[1]]
    a: list[tuple[cython.int]] = [(1,)]
    b: list[list[cython.int]] = [[1]]
    c: cython.int = 5
    print(c + a[0][0])
    print(c + b[0][0])


# NEGATIVE SC

# def negative_tests() -> None:
#     # a = [5.0]
#     # b: cython.int = a[0]
#     # print(b)
# 
#     c: list[cython.float] = [5.0]
#     d: list[cython.int] = c # This must fail
#     d: list[cython.int] = [5.0]
#     # x = d[0]
#     # print(x)
# negative_tests()

main1()
main2()
main3()
main4()
