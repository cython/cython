cdef:
	extern from "cpp_source.h":
		cppclass testclass:
			testclass()
			void a()
			void a(unsigned int i)
	cppclass testclass2(testclass): # a() is dropped
		testclass2()

	testclass t1 = testclass()
	testclass2 t2 = testclass2()


t1.a()
t1.a(1)

t2.a() # Call with wrong number of arguments (expected 1, got 0)
t2.a(2)
