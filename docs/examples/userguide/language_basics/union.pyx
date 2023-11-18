cdef union Food:
    char *spam
    float *eggs

def main():
    cdef float *arr = [1.0, 2.0]
    cdef Food spam = Food(spam='b')
    cdef Food eggs = Food(eggs=arr)
    print(spam.spam, eggs.eggs[0])
