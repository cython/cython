# mode: run
# ticket: t731
# tag: locals, vars, dir

cimport cython

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
    >>> [n for n in klass.names if n not in {"__qualname__", "__annotations__"}]
    ['__module__', 'visible']
    """
    not_visible = 1234
    class Foo:
        visible = 4321
        names = dir()
        locs = locals()
    return Foo


@cython.test_fail_if_path_exists('//SortedDictKeysNode')
def test_class_dir_contains():
    """
    >>> klass = test_class_dir_contains()
    True
    False
    True
    False
    True
    False
    True
    True
    True
    """
    not_visible = 1234
    class Foo:
        visible = 4321
        print('visible' in dir())
        print('not_visible' in dir())
        print('not_visible' not in dir())
        print('locs' in dir())
        print('visible' in locals())
        print('locs' in locals())
        locs = locals()
        print('visible' in dir())
        print('locs' in dir())
        print('locs' in locals())
    return Foo
