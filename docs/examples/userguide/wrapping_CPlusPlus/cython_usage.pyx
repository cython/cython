# distutils: language = c++

from Rectangle cimport Rectangle

def main():
    rec_ptr = new Rectangle(1, 2, 3, 4)  # Instantiate a Rectangle object on the heap
    try:
        rec_area = rec_ptr.getArea()
    finally:
        del rec_ptr  # delete heap allocated object

    cdef Rectangle rec_stack  # Instantiate a Rectangle object on the stack
