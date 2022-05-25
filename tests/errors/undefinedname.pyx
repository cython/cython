# mode: error

i = _this_global_name_does_not_exist_

def test(i):
    return _this_local_name_does_not_exist_

_ERRORS = u"""
3:4:undeclared name not builtin: _this_global_name_does_not_exist_
6:11:undeclared name not builtin: _this_local_name_does_not_exist_
"""
