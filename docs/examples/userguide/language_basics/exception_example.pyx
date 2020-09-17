# >>> c.a_cpdef_wo_py_retval()
# Exception: a_cpdef_wo_py_retval: This Exception will cause a return of 0
# Exception ignored in: 'cython_exception_example.a_cpdef_wo_py_retval'
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# Exception: a_cpdef_wo_py_retval: This Exception will cause a return of 0
# 0

cpdef int a_cpdef_wo_py_retval():
	# NB: defined as cpdef
	# This function returns an int which is not a Python
	# object. Hence the function has no way of signalling
	# an Exception, and will return a default Exception
	# indicator of 0 instead.
	raise Exception(
		'a_cpdef_wo_py_retval: This Exception '
		'will cause a return of 0')
	# As the return type is int, the 
	# Exception will cause a return of the default value 0
	pass
	print('Not running any longer, you will not see this...')
	return 1  # will not return 1 here, has already returned 0

cdef int a_cdef_wo_py_retval():
	# NB: defined as cdef, to show the behaviour is
	# identical to cpdef
	# This function returns an int which is not a Python
	# object. Hence the function has no way of signalling
	# an Exception, and will return a default Exception
	# indicator of 0 instead.
	raise Exception(
		'a_cdef_wo_py_retval: This Exception '
		'will cause a return of 0')
	# As return type is int, the 
	# Exception will cause a return of default value 0
	pass
	print('Not running any longer, you will not see this...')
	return 1  # will not return 1 here, has already returned 0

# >>> c.a_cpdef_w_py_retval()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "cython_exception_example.pyx", line 48, in cython_exception_example.a_cpdef_w_py_retval
#     cpdef a_cpdef_w_py_retval():
#   File "cython_exception_example.pyx", line 51, in cython_exception_example.a_cpdef_w_py_retval
#     raise Exception('This exception will bubble up to caller')
# Exception: This exception will bubble up to caller
# >>>

cpdef a_cpdef_w_py_retval():
	# NB: no return type -> returning a Python object
	# This Exception will bubble up to caller
	raise Exception('This exception will bubble up to caller')
	print('Not running any longer, you will not see this...')
	return 1  # will not return 1 here, Exception has been raised

cdef a_cdef_w_py_retval():
	# NB: no return type -> returning a Python object
	# This Exception will bubble up to caller
	raise Exception('This exception will bubble up to caller')
	print('Not running any longer, you will not see this...')
	return 1  # will not return 1 here, Exception has been raised


# >>> c.a_cpfdef_wo_py_retval_wrapped_cpdef()
# Traceback (most recent call last):
#   File "cython_exception_example.pyx", line 51, in cython_exception_example.a_cpdef_w_py_retval
#     # This Exception will bubble up to caller
# Exception: This exception will bubble up to caller
# Exception ignored in: 'cython_exception_example.a_cpfdef_wo_py_retval_wrapped_cpdef'
# Traceback (most recent call last):
#   File "cython_exception_example.pyx", line 51, in cython_exception_example.a_cpdef_w_py_retval
#     # This Exception will bubble up to caller
# Exception: This exception will bubble up to caller
# 0
cpdef int a_cpfdef_wo_py_retval_wrapped_cpdef():
	# Example of when an Exception of a wrapped cpdef
	# becomes effectively ignored because this function
	# does not return a Python type
	val = a_cpdef_w_py_retval()
	# ^ Exception is raised in a_cpdef_w_py_retval(),
	# which is detected here,
	# but because the current function does not return
	# a Python object, it will not bubble up any further
	# Instead we will return 0 here ("ignoring" it)
	pass  # keep for better stack trace
	print('Not running any longer, you will not see this...')
	return 1  # Nope: has already returned 0

# >>> c.a_cpfdef_wo_py_retval_wrapped_cdef()
# Traceback (most recent call last):
#   File "cython_exception_example.pyx", line 58, in cython_exception_example.a_cdef_w_py_retval
#     # This Exception will bubble up to caller
# Exception: This exception will bubble up to caller
# Exception ignored in: 'cython_exception_example.a_cpfdef_wo_py_retval_wrapped_cdef'
# Traceback (most recent call last):
#   File "cython_exception_example.pyx", line 58, in cython_exception_example.a_cdef_w_py_retval
#     # This Exception will bubble up to caller
# Exception: This exception will bubble up to caller
# 0
cpdef int a_cpfdef_wo_py_retval_wrapped_cdef():
	# Example of when an Exception of a wrapped cdef
	# becomes effectively ignored because this function
	# does not return a Python type
	val = a_cdef_w_py_retval()
	# ^ Exception is raised in a_cdef_w_py_retval(),
	# which is detected here,
	# but because the current function does not return
	# a Python object, it will not bubble up any further
	# Instead we will return 0 here ("ignoring" it)
	pass  # keep for better stack trace
	print('Not running any longer, you will not see this...')
	return 1  # Nope: has already returned 0
