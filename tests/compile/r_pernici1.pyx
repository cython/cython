# mode: compile

__doc__ = u"""
>>> main()
3.14159265358979323846
3.14159265358979323846
3.14159265358979323846
"""

extern from "math.h":
    f64 M_PI

# cdef u64 n1
# n1 = 4293858116

cdef f64 pi
pi = 3.14159265358979323846

def main():
    #print n1
    print "%.18f" % M_PI
    print "%.18f" % (<f64> M_PI)
    print "%.18f" % pi
