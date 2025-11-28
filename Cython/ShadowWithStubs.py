# This file contains types that still require type stubs because
# the implementation differs significantly from the nominal
# typing.

# Emulated types

class CythonMetaType(type):

    def __getitem__(type, ix):
        return array(type, ix)

CythonTypeObject = CythonMetaType('CythonTypeObject', (object,), {})

class CythonType(CythonTypeObject):

    def _pointer(self, n=1):
        for i in range(n):
            self = pointer(self)
        return self

class PointerType(CythonType):

    def __init__(self, value=None):
        if isinstance(value, (ArrayType, PointerType)):
            self._items = [cast(self._basetype, a) for a in value._items]
        elif isinstance(value, list):
            self._items = [cast(self._basetype, a) for a in value]
        elif value is None or value == 0:
            self._items = []
        else:
            raise ValueError

    def __getitem__(self, ix):
        if ix < 0:
            raise IndexError("negative indexing not allowed in C")
        return self._items[ix]

    def __setitem__(self, ix, value):
        if ix < 0:
            raise IndexError("negative indexing not allowed in C")
        self._items[ix] = cast(self._basetype, value)

    def __eq__(self, value):
        if value is None and not self._items:
            return True
        elif type(self) != type(value):
            return False
        else:
            return not self._items and not value._items

    def __repr__(self):
        return f"{self._basetype} *"


class ArrayType(PointerType):

    def __init__(self, value=None):
        if value is None:
            self._items = [None] * self._n
        else:
            super().__init__(value)


class StructType(CythonType):

    def __init__(self, *posargs, **data):
        if not (posargs or data):
            return
        if posargs and data:
            raise ValueError('Cannot accept both positional and keyword arguments.')

        # Allow 'cast_from' as single positional or keyword argument.
        if data and len(data) == 1 and 'cast_from' in data:
            cast_from = data.pop('cast_from')
        elif len(posargs) == 1 and type(posargs[0]) is type(self):
            cast_from, posargs = posargs[0], ()
        elif posargs:
            for key, arg in zip(self._members, posargs):
                setattr(self, key, arg)
            return
        else:
            for key, value in data.items():
                if key not in self._members:
                    raise ValueError("Invalid struct attribute for %s: %s" % (
                        self.__class__.__name__, key))
                setattr(self, key, value)
            return

        # do cast
        if data:
            raise ValueError('Cannot accept keyword arguments when casting.')
        if type(cast_from) is not type(self):
            raise ValueError('Cannot cast from %s' % cast_from)
        for key, value in cast_from.__dict__.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if key in self._members:
            self.__dict__[key] = cast(self._members[key], value)
        else:
            raise AttributeError("Struct has no member '%s'" % key)


class UnionType(CythonType):

    def __init__(self, cast_from=_Unspecified, **data):
        if cast_from is not _Unspecified:
            # do type cast
            if len(data) > 0:
                raise ValueError('Cannot accept keyword arguments when casting.')
            if isinstance(cast_from, dict):
                datadict = cast_from
            elif type(cast_from) is type(self):
                datadict = cast_from.__dict__
            else:
                raise ValueError('Cannot cast from %s' % cast_from)
        else:
            datadict = data
        if len(datadict) > 1:
            raise AttributeError("Union can only store one field at a time.")
        for key, value in datadict.items():
            setattr(self, key, value)

    def __setattr__(self, key, value):
        if key == '__dict__':
            CythonType.__setattr__(self, key, value)
        elif key in self._members:
            self.__dict__ = {key: cast(self._members[key], value)}
        else:
            raise AttributeError("Union has no member '%s'" % key)


class pointer(PointerType):
    # Implemented as class to support both 'pointer(int)' and 'pointer[int]'.
    def __new__(cls, basetype):
        class PointerInstance(PointerType):
            _basetype = basetype
        return PointerInstance

    def __class_getitem__(cls, basetype):
        return cls(basetype)


class array(ArrayType):
    # Implemented as class to support both 'array(int, 5)' and 'array[int, 5]'.
    def __new__(cls, basetype, n):
        class ArrayInstance(ArrayType):
            _basetype = basetype
            _n = n
        return ArrayInstance

    def __class_getitem__(cls, item):
        basetype, n = item
        return cls(basetype, item)


class typedef(CythonType):

    def __init__(self, type, name=None):
        self._basetype = type
        self.name = name

    def __call__(self, *arg):
        from .Shadow import cast
        value = cast(self._basetype, *arg)
        return value

    def __repr__(self):
        return self.name or str(self._basetype)

    def __getitem__(self, item):
        from .Shadow import index_type
        return index_type(self, item)
