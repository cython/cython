__doc__ = u"""
>>> a
2
>>> b
3
>>> exc[0].__class__.__name__
'AttributeError'
>>> exc[1].__class__.__name__
'KeyError'
>>> exc[2].__class__.__name__
'IndexError'
>>> exc[3].__class__.__name__
'ValueError'
>>> exc[3] is val
True

>>> except_as_deletes   # Py2 behaviour
False
>>> no_match_does_not_touch_target
True
"""

a = 0

try:
    raise KeyError
except AttributeError:
    a = 1
except KeyError:
    a = 2
except:
    a = 3

b = 0

try:
    raise IndexError
except AttributeError:
    b = 1
except KeyError:
    b = 2
except:
    b = 3

exc = [None]*4

try:
    raise AttributeError
except AttributeError as e:
    exc[0] = e
except KeyError       as e:
    exc[0] = e
except IndexError     as e:
    exc[0] = e
except:
    exc[0] = 'SOMETHING ELSE'

e = None
try:
    raise KeyError
except AttributeError as e:
    exc[1] = e
except KeyError       as e:
    exc[1] = e
except IndexError     as e:
    exc[1] = e
except:
    exc[1] = 'SOMETHING ELSE'

try:
    e
except NameError:
    except_as_deletes = True
else:
    except_as_deletes = False

e = 123
try:
    raise TypeError
except NameError as e:
    pass
except TypeError:
    pass
no_match_does_not_touch_target = (e == 123)

try:
    raise IndexError
except AttributeError as e:
    exc[2] = e
except KeyError       as e:
    exc[2] = e
except IndexError     as e:
    exc[2] = e
except:
    exc[2] = 'SOMETHING ELSE'

val = None
try:
    try:
        try:
            raise ValueError
        except AttributeError as e:
            exc[3] = e
        except KeyError       as e:
            exc[3] = e
        except IndexError     as e:
            exc[3] = e
        except:
            raise
    except (AttributeError,
            KeyError,
            IndexError,
            ValueError) as e:
        val = e
        raise e
except Exception as e:
    exc[3] = e
