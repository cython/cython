cdef struct Grail:
    i32 age
    f32 volume

def main():
    let Grail grail = Grail(5, 3.0)
    print(grail.age, grail.volume)
