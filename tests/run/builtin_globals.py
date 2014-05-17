# mode: run
# tag: allow_unknown_names

assert "NEW" not in globals()

globals().update(NEW=True)

assert "NEW" in globals()


def default_args(value=NEW):
    """
    >>> default_args()
    True
    """
    return value
