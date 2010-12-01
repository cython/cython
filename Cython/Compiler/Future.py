def _get_feature(name):
    import __future__
    try:
        return getattr(__future__, name)
    except AttributeError:
        # unique fake object for earlier Python versions
        return object()

unicode_literals = _get_feature("unicode_literals")
with_statement = _get_feature("with_statement")
division = _get_feature("division")
print_function = _get_feature("print_function")
nested_scopes = _get_feature("nested_scopes")  # dummy

del _get_feature
