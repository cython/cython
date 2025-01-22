# mode: run
# tag: condexpr
# ticket: 5197

cimport cython

cdef class Foo:
    cdef dict data

    def __repr__(self):
        return '<Foo>'


cpdef test_type_cast(Foo obj, cond):
    """
    # Regression test: obj must be cast to (PyObject *) here
    >>> test_type_cast(Foo(), True)
    [<Foo>]
    >>> test_type_cast(Foo(), False)
    <Foo>
    """
    return [obj] if cond else obj


cdef func(Foo foo, dict data):
    return foo, data


@cython.test_fail_if_path_exists('//PyTypeTestNode')
def test_cpp_pyobject_cast(Foo obj1, Foo obj2, cond):
    """
    >>> test_cpp_pyobject_cast(Foo(), Foo(), True)
    (<Foo>, None)
    """
    return func(obj1 if cond else obj2, obj1.data if cond else obj2.data)


def test_charptr_coercion(x):
    """
    >>> print(test_charptr_coercion(True))
    abc
    >>> print(test_charptr_coercion(False))
    def
    """
    cdef char* s = b'abc' if x else b'def'
    return s.decode('ascii')


def test_syntax():
    """
    >>> test_syntax()
    (0, 0, 0)
    """
    # Py3 allows the 'else' keyword to directly follow a number
    x = 0 if 1else 1
    y = 0 if 1.0else 1
    z = 0 if 1.else 1
    return x, y, z


from libc cimport math

def test_cfunc_ptrs(double x, bint round_down):
    """
    >>> test_cfunc_ptrs(2.5, round_down=True)
    2.0
    >>> test_cfunc_ptrs(2.5, round_down=False)
    3.0
    """
    return (math.floor if round_down else math.ceil)(x)


def performance_gh5197(patternsList):
    """
    >>> performance_gh5197([])  # do not actually run anything, just see that things work at all
    """
    # Coercing the types in nested conditional expressions used to slow down exponentially.
    # See https://github.com/cython/cython/issues/5197
    import re
    matched=[]
    for _ in range(len(patternsList)):
        try:
            matched.append(patternsList[_].split('|')[-1].split('/')[-1] + 'pattr1' if re.search('^SomeString.*EndIng$')\
                else patternsList[_].split('|a')[-1].split('/a')[-1] + 'pattr2' if re.search('^SomeOtherString.?Number.*EndIng$')\
                    else patternsList[_].split('|a')[-1].split('/a')[-1] + 'pattr2' if re.search('^SomeOtherString.?Number.*EndIng$')\
                        else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                            else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                    else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                        else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                            else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                    else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                        else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                            else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                    else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                        else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                            else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                    else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                        else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                            else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                    else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                        # else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                        #     else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                        #         else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                        #             else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                        #                 else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                        #                     else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                        #                         else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1] if re.search('^SomeOtherString.?Number.*EndIng$')\
                                                                                                                                    else patternsList[_].split('|b')[-1].split('/b')[-1] + 'pattr2' + patternsList[_].split('/')[-1].split('//')[-1]  )
        except Exception as e:
            matched.append('Error at Index:%s-%s' %(_, patternsList[_]))

cdef accept_int(int x):
    return x

def test_mixed_int_bool_coercion(x):
    """
    https://github.com/cython/cython/issues/5731

    >>> test_mixed_int_bool_coercion(None)
    0
    >>> test_mixed_int_bool_coercion(5)
    5
    """
    return accept_int(False if x is None else x)
