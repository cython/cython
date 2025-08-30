# mode: run
# tag: closures

# Cython version of Knuth's "man or boy" test -- "It separates the man
# Algol 60 compilers from the boy Algol 60 compilers." Here's the
# original (from wikipedia):
#
# begin
#   real procedure A (k, x1, x2, x3, x4, x5);
#   value k; integer k;
#   begin
#     real procedure B;
#     begin k:= k - 1;
#           B:= A := A (k, B, x1, x2, x3, x4);
#     end;
#     if k <= 0 then A:= x4 + x5 else B;
#   end;
#   outreal (A (10, 1, -1, -1, 1, 0));
# end;
#
# and a table of values:
#
#   k           A
#   0           1
#   1           0
#   2   	-2
#   3   	0
#   4   	1
#   5   	0
#   6   	1
#   7   	-1
#   8   	-10
#   9   	-30
#   10   	-67
#
# Past 10 or so, we blow the C stack -- can't just set a higher recursion limit
# to get around that one.
#

def compute(val):
    if isinstance(val, int):
        return val
    else:
        return val()

def a(in_k, x1, x2, x3, x4, x5):
    """
    >>> import sys
    >>> old_limit = sys.getrecursionlimit()
    >>> sys.setrecursionlimit(1350 if not getattr(sys, 'pypy_version_info', None) else 2700)

    >>> a(10, 1, -1, -1, 1, 0)
    -67

    >>> sys.setrecursionlimit(old_limit)
    """
    k = [in_k]
    def b():
        k[0] -= 1
        return a(k[0], b, x1, x2, x3, x4)
    return compute(x4) + compute(x5) if k[0] <= 0 else b()

