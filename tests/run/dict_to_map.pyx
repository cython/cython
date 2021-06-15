from libcpp.map cimport map

cdef:
	extern from "cpp_source.h":
		void test(map[unsigned int, unsigned int] m)

d = {1: 3}
test(d) # works fine

test({1: 1}) # generation error
