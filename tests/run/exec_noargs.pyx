# mode: run
# tag: exec

exec "GLOBAL = 1234"

def exec_module_scope():
    """
    >>> globals()['GLOBAL']
    1234
    """

def exec_func_scope():
    """
    >>> sorted(exec_func_scope().items())
    [('G', 1234), ('a', 'b')]
    """
    d = {}
    exec "d['a'] = 'b'; d['G'] = GLOBAL"
    return d

def exec_pyclass_scope():
    """
    >>> obj = exec_pyclass_scope()
    >>> obj.a
    'b'
    >>> obj.G
    1234
    """
    class TestExec:
        exec "a = 'b'; G = GLOBAL"
    return TestExec
