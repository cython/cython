# mode: run
# ticket: 731
# tags: locals, vars, dir

LOCALS = locals()
GLOBALS = globals()
DIR_SAME = sorted(dir()) == sorted(globals().keys())

def test_module_locals_and_dir():
    """
    >>> LOCALS is GLOBALS
    True
    >>> DIR_SAME
    True
    """

def test_class_locals_and_dir():
    """
    >>> klass = test_class_locals_and_dir()
    >>> 'visible' in klass.locs and 'not_visible' not in klass.locs
    True
    >>> klass.names
    ['visible']
    """
    not_visible = 1234
    class Foo:
        visible = 4321
        names = dir()
        locs = locals()
    return Foo
