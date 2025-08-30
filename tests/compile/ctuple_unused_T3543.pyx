# ticket: 3543
# mode: compile

# Views define unused ctuples, including (long,)
from cython cimport view

# Implicitly generate a ctuple (long,)
obj = None
obj or (1,)
