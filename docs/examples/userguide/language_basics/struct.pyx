cdef struct Grail:
    int age
    float volume

def main():
    cdef Grail grail = Grail(5, 3.0)
    print(grail.age, grail.volume)
