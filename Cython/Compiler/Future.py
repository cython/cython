def _get_feature(name):
    import __future__
    try:
        return getattr(__future__, name)
    except AttributeError:
        # unique fake object for earlier Python versions
        return object()

unicode_literals = _get_feature("unicode_literals")

del _get_feature
