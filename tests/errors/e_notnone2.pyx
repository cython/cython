# mode: error

def eggs(int x not None, char* y not None):
	pass
_ERRORS = u"""
3: 9: Only Python type arguments can have 'not None'
3:25: Only Python type arguments can have 'not None'
"""
