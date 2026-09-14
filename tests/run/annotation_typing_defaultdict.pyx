# mode: run
# tag: pep484
# cython: language_level=3, annotation_typing=False

from collections import defaultdict


def default_dict_annotation_typing_disabled():
    """
    >>> default_dict_annotation_typing_disabled()
    [defaultdict(<class 'int'>, {'severity': 1})]
    """
    values: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    values["target"]["severity"] += 1
    return [counts for _, counts in values.items()]
