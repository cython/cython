# mode: error

try:
    raise KeyError
except KeyError:
    pass
except:
    pass
except:
    pass
except AttributeError:
    pass

_ERRORS = u"""
9:0: default 'except:' must be last
11:0: default 'except:' must be last
"""
