# delorean.pyx

cdef public struct Vehicle:
    int speed
    float power

cdef api void activate(Vehicle *v):
    if v.speed >= 88 and v.power >= 1.21:
        print("Time travel achieved")