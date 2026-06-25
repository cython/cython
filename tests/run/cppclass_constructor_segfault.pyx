pyo = "test"

cdef:
	cppclass test:
		test():
			global pyo # Does not cause segfault

			# Causes segfault
			#[1, 2, 3]
			#i = 1000000000000000000000
			#int(123)
			#print(123)
			#hi = "test"
			#pyo
			#str("test")
			#import os
			#hex(40)
			#chr(40)
			#bin(40)
			#range(40)
			#5 / 0

			# No segfault, no error
			#"test"
			#str()
			#2 ** 900
			#None
			#False
			#u"Test"
			#ord(b't')
			#abs(40)
			#type(40)
			#bool(40)

			# Fatal Python error: PyEval_SaveThread: NULL tstate
			#with nogil:
			#	pass

			# Fatal Python error: PyThreadState_Get: no current thread
			#bytearray()
			#bytes()

	test t = test()
