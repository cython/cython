# mode: run
# ticket: 561
# ticket: 3

# The patch in #561 changes code generation for most special methods
# to remove the Cython-generated wrapper and let PyType_Ready()
# generate its own wrapper.  (This wrapper would be used, for instance,
# when using the special method as a bound method.)

# To test this, we go through and verify that each affected special
# method works as a bound method.

# Special methods that are treated the same under Python 2 and 3 are
# tested here; see also special_methods_T561_py2.pyx and
# special_methods_T561_py3.pyx for tests of the differences between
# Python 2 and 3.

# Regarding ticket 3, we should additionally test that unbound method
# calls to these special methods (e.g. ExtType.__init__()) do not use
# a runtime lookup indirection.

import sys

__doc__ = u"""
    >>> # If you define either setitem or delitem, you get wrapper objects
    >>> # for both methods.  (This behavior is unchanged by #561.)
    >>> si_setitem = SetItem().__setitem__
    >>> si_setitem('foo', 'bar')
    SetItem setitem 'foo' 'bar'
    >>> si_delitem = SetItem().__delitem__
    >>> si_delitem('foo')
    Traceback (most recent call last):
    ...
    NotImplementedError: Subscript deletion not supported by special_methods_T561.SetItem
    >>> di_setitem = DelItem().__setitem__
    >>> di_setitem('foo', 'bar')
    Traceback (most recent call last):
    ...
    NotImplementedError: Subscript assignment not supported by special_methods_T561.DelItem
    >>> di_delitem = DelItem().__delitem__
    >>> di_delitem('foo')
    DelItem delitem 'foo'
    >>> sdi_setitem = SetDelItem().__setitem__
    >>> sdi_setitem('foo', 'bar')
    SetDelItem setitem 'foo' 'bar'
    >>> sdi_delitem = SetDelItem().__delitem__
    >>> sdi_delitem('foo')
    SetDelItem delitem 'foo'
    >>> g01 = object.__getattribute__(GetAttr(), '__getattribute__')
    >>> g01('attr')
    GetAttr getattr 'attr'
    >>> g10 = object.__getattribute__(GetAttribute(), '__getattr__')
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561.GetAttribute' object has no attribute '__getattr__'
    >>> g11 = object.__getattribute__(GetAttribute(), '__getattribute__')
    >>> g11('attr')
    GetAttribute getattribute 'attr'
    >>> # If you define either setattr or delattr, you get wrapper objects
    >>> # for both methods.  (This behavior is unchanged by #561.)
    >>> sa_setattr = SetAttr().__setattr__
    >>> sa_setattr('foo', 'bar')
    SetAttr setattr 'foo' 'bar'
    >>> sa_delattr = SetAttr().__delattr__
    >>> sa_delattr('foo')
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561.SetAttr' object has no attribute 'foo'
    >>> da_setattr = DelAttr().__setattr__
    >>> da_setattr('foo', 'bar')
    Traceback (most recent call last):
    ...
    AttributeError: 'special_methods_T561.DelAttr' object has no attribute 'foo'
    >>> da_delattr = DelAttr().__delattr__
    >>> da_delattr('foo')
    DelAttr delattr 'foo'
    >>> sda_setattr = SetDelAttr().__setattr__
    >>> sda_setattr('foo', 'bar')
    SetDelAttr setattr 'foo' 'bar'
    >>> sda_delattr = SetDelAttr().__delattr__
    >>> sda_delattr('foo')
    SetDelAttr delattr 'foo'
    >>> # If you define either set or delete, you get wrapper objects
    >>> # for both methods.  (This behavior is unchanged by #561.)
    >>> s_set = Set().__set__
    >>> s_set('instance', 'val')
    Set set 'instance' 'val'
    >>> s_delete = Set().__delete__
    >>> s_delete('instance')
    Traceback (most recent call last):
    ...
    NotImplementedError: __delete__
    >>> d_set = Delete().__set__
    >>> d_set('instance', 'val')
    Traceback (most recent call last):
    ...
    NotImplementedError: __set__
    >>> d_delete = Delete().__delete__
    >>> d_delete('instance')
    Delete delete 'instance'
    >>> sd_set = SetDelete().__set__
    >>> sd_set('instance', 'val')
    SetDelete set 'instance' 'val'
    >>> sd_delete = SetDelete().__delete__
    >>> sd_delete('instance')
    SetDelete delete 'instance'
    >>> # If you define __long__, you get a wrapper object for __int__.
    >>> # (This behavior is unchanged by #561.)
    >>> Li = Long().__int__
    >>> Li()
    Long __long__
"""
if sys.version_info >= (2,5):
    __doc__ += u"""\
    >>> vs0 = VerySpecial(0)
    VS __init__ 0
    >>> vs0_index = vs0.__index__
    >>> vs0_index()
    VS __index__ 0
"""

cdef class VerySpecial:
    """
    >>> vs0 = VerySpecial(0)
    VS __init__ 0
    >>> vs1 = VerySpecial(1)
    VS __init__ 1

    >>> vs0_add = vs0.__add__
    >>> vs0_add(vs1)
    VS __add__ 0 1
    >>> vs0_sub = vs0.__sub__
    >>> vs0_sub(vs1)
    VS __sub__ 0 1
    >>> vs0_mul = vs0.__mul__
    >>> vs0_mul(vs1)
    VS __mul__ 0 1
    >>> vs0_mod = vs0.__mod__
    >>> vs0_mod(vs1)
    VS __mod__ 0 1
    >>> vs0_divmod = vs0.__divmod__
    >>> vs0_divmod(vs1)
    VS __divmod__ 0 1
    >>> vs0_pow = vs0.__pow__
    >>> vs0_pow(vs1)
    VS __pow__ pow(0, 1, None)
    >>> vs0_pow(vs1, 13)
    VS __pow__ pow(0, 1, 13)
    >>> vs0_neg = vs0.__neg__
    >>> vs0_neg()
    VS __neg__ 0
    >>> vs0_pos = vs0.__pos__
    >>> vs0_pos()
    VS __pos__ 0
    >>> vs0_abs = vs0.__abs__
    >>> vs0_abs()
    VS __abs__ 0
    >>> vs0_invert = vs0.__invert__
    >>> vs0_invert()
    VS __invert__ 0
    >>> vs0_lshift = vs0.__lshift__
    >>> vs0_lshift(vs1)
    VS __lshift__ 0 << 1
    >>> vs0_rshift = vs0.__rshift__
    >>> vs0_rshift(vs1)
    VS __rshift__ 0 >> 1
    >>> vs0_and = vs0.__and__
    >>> vs0_and(vs1)
    VS __and__ 0 & 1
    >>> vs0_xor = vs0.__xor__
    >>> vs0_xor(vs1)
    VS __xor__ 0 ^ 1
    >>> vs0_or = vs0.__or__
    >>> vs0_or(vs1)
    VS __or__ 0 | 1
    >>> vs0_int = vs0.__int__
    >>> vs0_int()
    VS __int__ 0
    >>> vs0_float = vs0.__float__
    >>> vs0_float()
    VS __float__ 0
    >>> vs0_iadd = vs0.__iadd__
    >>> vs0_iadd(vs1)
    VS __iadd__ 0 += 1
    >>> vs0_isub = vs0.__isub__
    >>> vs0_isub(vs1)
    VS __isub__ 0 -= 1
    >>> vs0_imul = vs0.__imul__
    >>> vs0_imul(vs1)
    VS __imul__ 0 *= 1
    >>> vs0_imod = vs0.__imod__
    >>> vs0_imod(vs1)
    VS __imod__ 0 %= 1
    >>> vs0_ipow = vs0.__ipow__
    >>> vs0_ipow(vs1)
    VS __ipow__ 0 1
    >>> vs0_ilshift = vs0.__ilshift__
    >>> vs0_ilshift(vs1)
    VS __ilshift__ 0 <<= 1
    >>> vs0_irshift = vs0.__irshift__
    >>> vs0_irshift(vs1)
    VS __irshift__ 0 >>= 1
    >>> vs0_iand = vs0.__iand__
    >>> vs0_iand(vs1)
    VS __iand__ 0 &= 1
    >>> vs0_ixor = vs0.__ixor__
    >>> vs0_ixor(vs1)
    VS __ixor__ 0 ^= 1
    >>> vs0_ior = vs0.__ior__
    >>> vs0_ior(vs1)
    VS __ior__ 0 |= 1
    >>> vs0_floordiv = vs0.__floordiv__
    >>> vs0_floordiv(vs1)
    VS __floordiv__ 0 / 1
    >>> vs0_truediv = vs0.__truediv__
    >>> vs0_truediv(vs1)
    VS __truediv__ 0 / 1
    >>> vs0_ifloordiv = vs0.__ifloordiv__
    >>> vs0_ifloordiv(vs1)
    VS __ifloordiv__ 0 /= 1
    >>> vs0_itruediv = vs0.__itruediv__
    >>> vs0_itruediv(vs1)
    VS __itruediv__ 0 /= 1

    # If you define an arithmetic method, you get wrapper objects for
    # the reversed version as well.  (This behavior is unchanged by #561.)
    >>> vs0_radd = vs0.__radd__
    >>> vs0_radd(vs1)
    VS __add__ 1 0
    >>> vs0_rsub = vs0.__rsub__
    >>> vs0_rsub(vs1)
    VS __sub__ 1 0
    >>> vs0_rmul = vs0.__rmul__
    >>> vs0_rmul(vs1)
    VS __mul__ 1 0
    >>> vs0_rmod = vs0.__rmod__
    >>> vs0_rmod(vs1)
    VS __mod__ 1 0
    >>> vs0_rdivmod = vs0.__rdivmod__
    >>> vs0_rdivmod(vs1)
    VS __divmod__ 1 0
    >>> vs0_rpow = vs0.__rpow__
    >>> vs0_rpow(vs1)
    VS __pow__ pow(1, 0, None)
    >>> vs0_rlshift = vs0.__rlshift__
    >>> vs0_rlshift(vs1)
    VS __lshift__ 1 << 0
    >>> vs0_rrshift = vs0.__rrshift__
    >>> vs0_rrshift(vs1)
    VS __rshift__ 1 >> 0
    >>> vs0_rand = vs0.__rand__
    >>> vs0_rand(vs1)
    VS __and__ 1 & 0
    >>> vs0_rxor = vs0.__rxor__
    >>> vs0_rxor(vs1)
    VS __xor__ 1 ^ 0
    >>> vs0_ror = vs0.__ror__
    >>> vs0_ror(vs1)
    VS __or__ 1 | 0
    >>> vs0_rfloordiv = vs0.__rfloordiv__
    >>> vs0_rfloordiv(vs1)
    VS __floordiv__ 1 / 0
    >>> vs0_rtruediv = vs0.__rtruediv__
    >>> vs0_rtruediv(vs1)
    VS __truediv__ 1 / 0
    >>> vs0_getitem = vs0.__getitem__
    >>> vs0_getitem('foo')
    VS __getitem__ 0['foo']
    >>> vs0_contains = vs0.__contains__
    >>> vs0_contains(vs1)
    VS __contains__ 0 1
    False
    >>> vs0_len = vs0.__len__
    >>> vs0_len()
    VS __len__ 0
    0
    >>> vs0_repr = vs0.__repr__
    >>> vs0_repr()
    VS __repr__ 0
    >>> vs0_hash = vs0.__hash__
    >>> vs0_hash()
    VS __hash__ 0
    1000
    >>> vs0_call = vs0.__call__
    >>> vs0_call(vs1)
    VS __call__ 0(1)
    >>> vs0_str = vs0.__str__
    >>> vs0_str()
    VS __str__ 0

    # If you define __richcmp__, you get all of __lt__, __le__,
    # __eq__, __ne__, __gt__, __ge__ (this behavior is unchanged by #561).
    # (you don't get a __richcmp__ method, because it doesn't have a
    # Python signature)
    >>> vs0_lt = vs0.__lt__
    >>> vs0_lt(vs1)
    VS richcmp 0 1 (kind=0)
    >>> vs0_le = vs0.__le__
    >>> vs0_le(vs1)
    VS richcmp 0 1 (kind=1)
    >>> vs0_eq = vs0.__eq__
    >>> vs0_eq(vs1)
    VS richcmp 0 1 (kind=2)
    >>> vs0_ne = vs0.__ne__
    >>> vs0_ne(vs1)
    VS richcmp 0 1 (kind=3)
    >>> vs0_gt = vs0.__gt__
    >>> vs0_gt(vs1)
    VS richcmp 0 1 (kind=4)
    >>> vs0_ge = vs0.__ge__
    >>> vs0_ge(vs1)
    VS richcmp 0 1 (kind=5)
    >>> vs0_iter = vs0.__iter__
    >>> vs0_iter()
    VS __iter__ 0
    >>> vs0_next = vs0.__next__
    >>> vs0_next()
    VS next/__next__ 0

    >>> vs0_get = vs0.__get__
    >>> vs0_get('instance', 'owner')
    VS __get__ 0 'instance' 'owner'
    >>> vs0_init = vs0.__init__
    >>> vs0_init(0)
    VS __init__ 0
    """
    cdef readonly int value

    def __init__(self, v):
        self.value = v
        print "VS __init__ %d" % self.value

    def __add__(self, other):
        print "VS __add__ %d %d" % (self.value, other.value)

    def __sub__(self, other):
        print "VS __sub__ %d %d" % (self.value, other.value)

    def __mul__(self, other):
        print "VS __mul__ %d %d" % (self.value, other.value)

    def __div__(self, other):
        print "VS __div__ %d %d" % (self.value, other.value)

    def __mod__(self, other):
        print "VS __mod__ %d %d" % (self.value, other.value)

    def __divmod__(self, other):
        print "VS __divmod__ %d %d" % (self.value, other.value)

    def __pow__(self, other, mod):
        print "VS __pow__ pow(%d, %d, %r)" % (self.value, other.value, mod)

    def __lshift__(self, other):
        print "VS __lshift__ %d << %d" % (self.value, other.value)

    def __rshift__(self, other):
        print "VS __rshift__ %d >> %d" % (self.value, other.value)

    def __and__(self, other):
        print "VS __and__ %d & %d" % (self.value, other.value)

    def __xor__(self, other):
        print "VS __xor__ %d ^ %d" % (self.value, other.value)

    def __or__(self, other):
        print "VS __or__ %d | %d" % (self.value, other.value)

    def __floordiv__(self, other):
        print "VS __floordiv__ %d / %d" % (self.value, other.value)

    def __truediv__(self, other):
        print "VS __truediv__ %d / %d" % (self.value, other.value)

    def __neg__(self):
        print "VS __neg__ %d" % self.value

    def __pos__(self):
        print "VS __pos__ %d" % self.value

    def __abs__(self):
        print "VS __abs__ %d" % self.value

    def __nonzero__(self):
        print "VS __nonzero__ %d" % self.value

    def __invert__(self):
        print "VS __invert__ %d" % self.value

    def __int__(self):
        print "VS __int__ %d" % self.value

    def __long__(self):
        print "VS __long__ %d" % self.value

    def __float__(self):
        print "VS __float__ %d" % self.value

    def __oct__(self):
        print "VS __oct__ %d" % self.value

    def __hex__(self):
        print "VS __hex__ %d" % self.value

    def __iadd__(self, other):
        print "VS __iadd__ %d += %d" % (self.value, other.value)

    def __isub__(self, other):
        print "VS __isub__ %d -= %d" % (self.value, other.value)

    def __imul__(self, other):
        print "VS __imul__ %d *= %d" % (self.value, other.value)

    def __idiv__(self, other):
        print "VS __idiv__ %d /= %d" % (self.value, other.value)

    def __imod__(self, other):
        print "VS __imod__ %d %%= %d" % (self.value, other.value)

    def __ipow__(self, other):
        # We must declare mod as an argument, but we must not touch it
        # or we'll get a segfault.  See #562
        print "VS __ipow__ %d %d" % (self.value, other.value)

    def __ilshift__(self, other):
        print "VS __ilshift__ %d <<= %d" % (self.value, other.value)

    def __irshift__(self, other):
        print "VS __irshift__ %d >>= %d" % (self.value, other.value)

    def __iand__(self, other):
        print "VS __iand__ %d &= %d" % (self.value, other.value)

    def __ixor__(self, other):
        print "VS __ixor__ %d ^= %d" % (self.value, other.value)

    def __ior__(self, other):
        print "VS __ior__ %d |= %d" % (self.value, other.value)

    def __ifloordiv__(self, other):
        print "VS __ifloordiv__ %d /= %d" % (self.value, other.value)

    def __itruediv__(self, other):
        print "VS __itruediv__ %d /= %d" % (self.value, other.value)

    def __index__(self):
        print "VS __index__ %d" % self.value

    def __getitem__(self, index):
        print "VS __getitem__ %d[%r]" % (self.value, index)

    def __contains__(self, other):
        print "VS __contains__ %d %d" % (self.value, other.value)

    def __len__(self):
        print "VS __len__ %d" % (self.value)

    def __cmp__(self, other):
        print "VS __cmp__ %d %d" % (self.value, other.value)

    def __repr__(self):
        print "VS __repr__ %d" % self.value

    def __hash__(self):
        print "VS __hash__ %d" % self.value
        return self.value + 1000

    def __call__(self, other):
        print "VS __call__ %d(%d)" % (self.value, other.value)

    def __str__(self):
        print "VS __str__ %d" % self.value

    def __richcmp__(self, other, kind):
        print "VS richcmp %d %d (kind=%r)" % (self.value, other.value, kind)

    def __iter__(self):
        print "VS __iter__ %d" % self.value

    def __next__(self):
        print "VS next/__next__ %d" % self.value

    def __get__(self, inst, own):
        print "VS __get__ %d %r %r" % (self.value, inst, own)

cdef class SetItem:
    def __setitem__(self, index, value):
        print "SetItem setitem %r %r" % (index, value)

cdef class DelItem:
    def __delitem__(self, index):
        print "DelItem delitem %r" % index

cdef class SetDelItem:
    def __setitem__(self, index, value):
        print "SetDelItem setitem %r %r" % (index, value)

    def __delitem__(self, index):
        print "SetDelItem delitem %r" % index

cdef class GetAttr:
    def __getattr__(self, attr):
        print "GetAttr getattr %r" % attr

cdef class GetAttribute:
    def __getattribute__(self, attr):
        print "GetAttribute getattribute %r" % attr

cdef class SetAttr:
    def __setattr__(self, attr, val):
        print "SetAttr setattr %r %r" % (attr, val)

cdef class DelAttr:
    def __delattr__(self, attr):
        print "DelAttr delattr %r" % attr

cdef class SetDelAttr:
    def __setattr__(self, attr, val):
        print "SetDelAttr setattr %r %r" % (attr, val)

    def __delattr__(self, attr):
        print "SetDelAttr delattr %r" % attr

cdef class Set:
    def __set__(self, inst, val):
        print "Set set %r %r" % (inst, val)

cdef class Delete:
    def __delete__(self, inst):
        print "Delete delete %r" % inst

cdef class SetDelete:
    def __set__(self, inst, val):
        print "SetDelete set %r %r" % (inst, val)

    def __delete__(self, inst):
        print "SetDelete delete %r" % inst

cdef class Long:
    def __long__(self):
        print "Long __long__"

cdef class GetAttrGetItemRedirect:
    """
    >>> o = GetAttrGetItemRedirect()

    >>> assert o.item == o['item']
    >>> source, item_value = o.item
    >>> assert source == 'item', source

    >>> assert o['attr'] == o.attr
    >>> source, attr_value = o['attr']
    >>> assert source == 'attr', source

    >>> assert item_value is attr_value, repr((item_value, attr_value))
    """
    cdef object obj
    def __cinit__(self):
        self.obj = object()

    def __getattr__(self, name):
        if name == 'item':
            return self[name]
        return ('attr', self.obj)

    def __getitem__(self, key):
        if key == 'attr':
            return getattr(self, key)
        return ('item', self.obj)


# test unbound method usage in subtypes

cdef class VerySpecialSubType(VerySpecial):
    """
    >>> vs0 = VerySpecialSubType(0)
    VS __init__ 0
    >>> vs1 = VerySpecialSubType(1)
    VS __init__ 1

    >>> vs0_add = vs0.__add__
    >>> vs0_add(vs1)
    VS __add__ 0 1
    >>> vs0_sub = vs0.__sub__
    >>> vs0_sub(vs1)
    VS __sub__ 0 1
    >>> vs0_mul = vs0.__mul__
    >>> vs0_mul(vs1)
    VS __mul__ 0 1
    >>> vs0_mod = vs0.__mod__
    >>> vs0_mod(vs1)
    VS __mod__ 0 1
    >>> vs0_divmod = vs0.__divmod__
    >>> vs0_divmod(vs1)
    VS __divmod__ 0 1
    >>> vs0_pow = vs0.__pow__
    >>> vs0_pow(vs1)
    VS __pow__ pow(0, 1, None)
    >>> vs0_pow(vs1, 13)
    VS __pow__ pow(0, 1, 13)
    >>> vs0_neg = vs0.__neg__
    >>> vs0_neg()
    VS __neg__ 0
    >>> vs0_pos = vs0.__pos__
    >>> vs0_pos()
    VS __pos__ 0
    >>> vs0_abs = vs0.__abs__
    >>> vs0_abs()
    VS __abs__ 0
    >>> vs0_invert = vs0.__invert__
    >>> vs0_invert()
    VS __invert__ 0
    >>> vs0_lshift = vs0.__lshift__
    >>> vs0_lshift(vs1)
    VS __lshift__ 0 << 1
    >>> vs0_rshift = vs0.__rshift__
    >>> vs0_rshift(vs1)
    VS __rshift__ 0 >> 1
    >>> vs0_and = vs0.__and__
    >>> vs0_and(vs1)
    VS __and__ 0 & 1
    >>> vs0_xor = vs0.__xor__
    >>> vs0_xor(vs1)
    VS __xor__ 0 ^ 1
    >>> vs0_or = vs0.__or__
    >>> vs0_or(vs1)
    VS __or__ 0 | 1
    >>> vs0_int = vs0.__int__
    >>> vs0_int()
    VS __int__ 0
    >>> vs0_float = vs0.__float__
    >>> vs0_float()
    VS __float__ 0
    >>> vs0_iadd = vs0.__iadd__
    >>> vs0_iadd(vs1)
    VS __iadd__ 0 += 1
    >>> vs0_isub = vs0.__isub__
    >>> vs0_isub(vs1)
    VS __isub__ 0 -= 1
    >>> vs0_imul = vs0.__imul__
    >>> vs0_imul(vs1)
    VS __imul__ 0 *= 1
    >>> vs0_imod = vs0.__imod__
    >>> vs0_imod(vs1)
    VS __imod__ 0 %= 1
    >>> vs0_ipow = vs0.__ipow__
    >>> vs0_ipow(vs1)
    VS __ipow__ 0 1
    >>> vs0_ilshift = vs0.__ilshift__
    >>> vs0_ilshift(vs1)
    VS __ilshift__ 0 <<= 1
    >>> vs0_irshift = vs0.__irshift__
    >>> vs0_irshift(vs1)
    VS __irshift__ 0 >>= 1
    >>> vs0_iand = vs0.__iand__
    >>> vs0_iand(vs1)
    VS __iand__ 0 &= 1
    >>> vs0_ixor = vs0.__ixor__
    >>> vs0_ixor(vs1)
    VS __ixor__ 0 ^= 1
    >>> vs0_ior = vs0.__ior__
    >>> vs0_ior(vs1)
    VS __ior__ 0 |= 1
    >>> vs0_floordiv = vs0.__floordiv__
    >>> vs0_floordiv(vs1)
    VS __floordiv__ 0 / 1
    >>> vs0_truediv = vs0.__truediv__
    >>> vs0_truediv(vs1)
    VS __truediv__ 0 / 1
    >>> vs0_ifloordiv = vs0.__ifloordiv__
    >>> vs0_ifloordiv(vs1)
    VS __ifloordiv__ 0 /= 1
    >>> vs0_itruediv = vs0.__itruediv__
    >>> vs0_itruediv(vs1)
    VS __itruediv__ 0 /= 1

    # If you define an arithmetic method, you get wrapper objects for
    # the reversed version as well.  (This behavior is unchanged by #561.)
    >>> vs0_radd = vs0.__radd__
    >>> vs0_radd(vs1)
    VS __add__ 1 0
    >>> vs0_rsub = vs0.__rsub__
    >>> vs0_rsub(vs1)
    VS __sub__ 1 0
    >>> vs0_rmul = vs0.__rmul__
    >>> vs0_rmul(vs1)
    VS __mul__ 1 0
    >>> vs0_rmod = vs0.__rmod__
    >>> vs0_rmod(vs1)
    VS __mod__ 1 0
    >>> vs0_rdivmod = vs0.__rdivmod__
    >>> vs0_rdivmod(vs1)
    VS __divmod__ 1 0
    >>> vs0_rpow = vs0.__rpow__
    >>> vs0_rpow(vs1)
    VS __pow__ pow(1, 0, None)
    >>> vs0_rlshift = vs0.__rlshift__
    >>> vs0_rlshift(vs1)
    VS __lshift__ 1 << 0
    >>> vs0_rrshift = vs0.__rrshift__
    >>> vs0_rrshift(vs1)
    VS __rshift__ 1 >> 0
    >>> vs0_rand = vs0.__rand__
    >>> vs0_rand(vs1)
    VS __and__ 1 & 0
    >>> vs0_rxor = vs0.__rxor__
    >>> vs0_rxor(vs1)
    VS __xor__ 1 ^ 0
    >>> vs0_ror = vs0.__ror__
    >>> vs0_ror(vs1)
    VS __or__ 1 | 0
    >>> vs0_rfloordiv = vs0.__rfloordiv__
    >>> vs0_rfloordiv(vs1)
    VS __floordiv__ 1 / 0
    >>> vs0_rtruediv = vs0.__rtruediv__
    >>> vs0_rtruediv(vs1)
    VS __truediv__ 1 / 0
    >>> vs0_getitem = vs0.__getitem__
    >>> vs0_getitem('foo')
    VS __getitem__ 0['foo']
    >>> vs0_contains = vs0.__contains__
    >>> vs0_contains(vs1)
    VS __contains__ 0 1
    False
    >>> vs0_len = vs0.__len__
    >>> vs0_len()
    VS __len__ 0
    0
    >>> vs0_repr = vs0.__repr__
    >>> vs0_repr()
    VS __repr__ 0
    >>> vs0_hash = vs0.__hash__
    >>> vs0_hash()
    VS __hash__ 0
    1000
    >>> vs0_call = vs0.__call__
    >>> vs0_call(vs1)
    VS __call__ 0(1)
    >>> vs0_str = vs0.__str__
    >>> vs0_str()
    VS __str__ 0
    >>> vs0_lt = vs0.__lt__
    >>> vs0_lt(vs1)
    VS richcmp 0 1 (kind=0)
    >>> vs0_le = vs0.__le__
    >>> vs0_le(vs1)
    VS richcmp 0 1 (kind=1)
    >>> vs0_eq = vs0.__eq__
    >>> vs0_eq(vs1)
    VS richcmp 0 1 (kind=2)
    >>> vs0_ne = vs0.__ne__
    >>> vs0_ne(vs1)
    VS richcmp 0 1 (kind=3)
    >>> vs0_gt = vs0.__gt__
    >>> vs0_gt(vs1)
    VS richcmp 0 1 (kind=4)
    >>> vs0_ge = vs0.__ge__
    >>> vs0_ge(vs1)
    VS richcmp 0 1 (kind=5)
    >>> vs0_iter = vs0.__iter__
    >>> vs0_iter()
    VS __iter__ 0
    >>> vs0_next = vs0.__next__
    >>> vs0_next()
    VS next/__next__ 0
    >>> vs0_get = vs0.__get__
    >>> vs0_get('instance', 'owner')
    VS __get__ 0 'instance' 'owner'
    >>> vs0_init = vs0.__init__
    >>> vs0_init(0)
    VS __init__ 0
    """
    def __init__(self, v):
        VerySpecial.__init__(self, v)

    def __add__(self, other):
        return VerySpecial.__add__(self, other)

    def __sub__(self, other):
        return VerySpecial.__sub__(self, other)

    def __mul__(self, other):
        return VerySpecial.__mul__(self, other)

    def __div__(self, other):
        return VerySpecial.__div__(self, other)

    def __mod__(self, other):
        return VerySpecial.__mod__(self, other)

    def __divmod__(self, other):
        return VerySpecial.__divmod__(self, other)

    def __pow__(self, other, mod):
        return VerySpecial.__pow__(self, other, mod)

    def __lshift__(self, other):
        return VerySpecial.__lshift__(self, other)

    def __rshift__(self, other):
        return VerySpecial.__rshift__(self, other)

    def __and__(self, other):
        return VerySpecial.__and__(self, other)

    def __xor__(self, other):
        return VerySpecial.__xor__(self, other)

    def __or__(self, other):
        return VerySpecial.__or__(self, other)

    def __floordiv__(self, other):
        return VerySpecial.__floordiv__(self, other)

    def __truediv__(self, other):
        return VerySpecial.__truediv__(self, other)

    def __neg__(self):
        return VerySpecial.__neg__(self)

    def __pos__(self):
        return VerySpecial.__pos__(self)

    def __abs__(self):
        return VerySpecial.__abs__(self)

    def __nonzero__(self):
        return VerySpecial.__nonzero__(self)

    def __invert__(self):
        return VerySpecial.__invert__(self)

    def __int__(self):
        return VerySpecial.__int__(self)

    def __long__(self):
        return VerySpecial.__long__(self)

    def __float__(self):
        return VerySpecial.__float__(self)

    def __oct__(self):
        return VerySpecial.__oct__(self)

    def __hex__(self):
        return VerySpecial.__hex__(self)

    def __iadd__(self, other):
        return VerySpecial.__iadd__(self, other)

    def __isub__(self, other):
        return VerySpecial.__isub__(self, other)

    def __imul__(self, other):
        return VerySpecial.__imul__(self, other)

    def __idiv__(self, other):
        return VerySpecial.__idiv__(self, other)

    def __imod__(self, other):
        return VerySpecial.__imod__(self, other)

    def __ipow__(self, other):
        return VerySpecial.__ipow__(self, other)

    def __ilshift__(self, other):
        return VerySpecial.__ilshift__(self, other)

    def __irshift__(self, other):
        return VerySpecial.__irshift__(self, other)

    def __iand__(self, other):
        return VerySpecial.__iand__(self, other)

    def __ixor__(self, other):
        return VerySpecial.__ixor__(self, other)

    def __ior__(self, other):
        return VerySpecial.__ior__(self, other)

    def __ifloordiv__(self, other):
        return VerySpecial.__ifloordiv__(self, other)

    def __itruediv__(self, other):
        return VerySpecial.__itruediv__(self, other)

    def __index__(self):
        return VerySpecial.__index__(self)

    def __getitem__(self, index):
        return VerySpecial.__getitem__(self, index)

    def __contains__(self, other):
        return VerySpecial.__contains__(self, other)

    def __len__(self):
        return VerySpecial.__len__(self)

    def __cmp__(self, other):
        return VerySpecial.__cmp__(self, other)

    def __repr__(self):
        return VerySpecial.__repr__(self)

    def __hash__(self):
        return VerySpecial.__hash__(self)

    def __call__(self, arg):
        return VerySpecial.__call__(self, arg)

    def __str__(self):
        return VerySpecial.__str__(self)

# there is no __richcmp__ at the Python level
#    def __richcmp__(self, other, kind):
#        return VerySpecial.__richcmp__(self, other, kind)

    def __iter__(self):
        return VerySpecial.__iter__(self)

    def __next__(self):
        return VerySpecial.__next__(self)

    def __get__(self, inst, own):
        return VerySpecial.__get__(self, inst, own)
