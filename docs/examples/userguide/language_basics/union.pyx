cdef union Food:
    char *spam
    f32 *eggs

def main():
    cdef f32 *arr = [1.0, 2.0]
    cdef Food spam = Food(spam='b')
    cdef Food eggs = Food(eggs=arr)
    print(spam.spam, eggs.eggs[0])
