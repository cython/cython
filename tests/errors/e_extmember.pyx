cdef class Spam:
	cdef public Spam e
_ERRORS = u"""
/Local/Projects/D/Pyrex/Source/Tests/Errors1/e_extmember.pyx:2:18: Non-generic Python attribute cannot be exposed for writing from Python
"""
