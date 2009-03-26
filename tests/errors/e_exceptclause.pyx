
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
8:0: default 'except:' must be last
10:0: default 'except:' must be last
"""
