import cython


@cython.locals(counts=cython.int[10], digit=cython.int)
def count_digits(digits):
    """
    >>> digits = '01112222333334445667788899'
    >>> count_digits(map(int, digits))
    [1, 3, 4, 5, 3, 1, 2, 2, 3, 2]
    """
    counts = [0] * 10
    for digit in digits:
        assert 0 <= digit <= 9
        counts[digit] += 1
    return counts
