# mode: error
# tag: cpp

from libcpp cimport bool as bool_t

cdef:
	struct S1:
		int i

	struct S2:
		int i

	extern from "cpp_source.h":
		cppclass testclass:
			testclass()
			void a()
			void a(unsigned int i)

	cppclass testclass2(testclass):
		testclass2()

	cppclass testclass3(testclass):
		testclass3()
		void a(S1 v)

	cppclass testclass4(testclass):
		testclass4()
		void a(S2 v)

	testclass t1 = testclass()
	testclass2 t2 = testclass2()
	testclass3 t3 = testclass3()
	testclass4 t4 = testclass4()

cdef S1 s1
cdef S2 s2

testclass4().a(s1)
testclass3().a(s2)
testclass2().a(s1)
testclass2().a(s2)
testclass().a(s1)
testclass().a(s2)


_ERRORS = """
38:14: no suitable method found
39:14: no suitable method found
40:15: Cannot assign type 'S1' to 'unsigned int'
41:15: Cannot assign type 'S2' to 'unsigned int'
42:14: Cannot assign type 'S1' to 'unsigned int'
43:14: Cannot assign type 'S2' to 'unsigned int'
"""
