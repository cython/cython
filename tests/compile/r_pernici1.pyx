# mode: compile

__doc__ = u"""
>>> main()
3.14159265358979323846
3.14159265358979323846
3.14159265358979323846
"""

cdef extern from "math.h":
  double M_PI

#cdef unsigned long int n1
#n1 = 4293858116

cdef double pi
pi = 3.14159265358979323846

def main():
  #print n1
  print "%.18f" % M_PI
  print "%.18f" % (<float> M_PI)
  print "%.18f" % pi
