from lcmath import add
from lcmath import sub

@cython.ccall
def add_one(a: cython.int):
    print(add(a, 1))

@cython.ccall
def sub_one(a: cython.int):
    print(sub(a, 1))

if __name__ == "__main__":
    add_one(5)
    sub_one(3)
