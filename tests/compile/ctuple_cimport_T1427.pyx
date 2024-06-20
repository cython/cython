# ticket: 1427
# mode: compile

cimport ctuple_cimport

# Verify same tuple defined in multiple pxd not redeclared
ctypedef (int, double) int_double

ctuple_cimport.get_a_ctuple()
