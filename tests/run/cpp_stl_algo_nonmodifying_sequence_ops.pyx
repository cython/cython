# mode: run
# tag: cpp, werror, cpp11

from cython.operator cimport dereference as deref

from libcpp cimport bool
from libcpp.algorithm cimport all_of, any_of, none_of, for_each, count, count_if, mismatch, find, find_if, find_if_not
from libcpp.algorithm cimport find_end, find_first_of, adjacent_find, search, search_n
from libcpp.iterator cimport distance
from libcpp.string cimport string
from libcpp.vector cimport vector


cdef bool is_odd(int i):
    return i % 2


def all_odd(vector[int] values):
    """
    Test all_of with is_odd predicate.

    >>> all_odd([3, 5, 7, 11, 13, 17, 19, 23])
    True
    >>> all_odd([3, 4])
    False
    """
    return all_of(values.begin(), values.end(), is_odd)


def any_odd(vector[int] values):
    """
    Test any_of with is_odd predicate.

    >>> any_odd([1, 2, 3, 4])
    True
    >>> any_odd([2, 4, 6, 8])
    False
    """
    return any_of(values.begin(), values.end(), is_odd)


def none_odd(vector[int] values):
    """
    Test none_of with is_odd predicate.

    >>> none_odd([2, 4, 6, 8])
    True
    >>> none_odd([1, 2, 3, 4])
    False
    """
    return none_of(values.begin(), values.end(), is_odd)


def count_ones(vector[int] values):
    """
    Test count.

    >>> count_ones([1, 2, 1, 2])
    2
    """
    return count(values.begin(), values.end(), 1)


cdef void add_one(int &i):
    # https://github.com/cython/cython/issues/1863
    (&i)[0] += 1


def increment_ints(vector[int] values):
    """
    Test for_each.

    >>> increment_ints([3, 4, 2, 8, 15, 267])
    [4, 5, 3, 9, 16, 268]
    """
    for_each(values.begin(), values.end(), &add_one)
    return values


def count_odd(vector[int] values):
    """
    Test count_if with is_odd predicate.

    >>> count_odd([1, 2, 3, 4])
    2
    >>> count_odd([2, 4, 6, 8])
    0
    """
    return count_if(values.begin(), values.end(), is_odd)


def mirror_ends(string data):
    """
    Test mismatch using cppreference example.

    This program determines the longest substring that is simultaneously found at the very beginning of the given string
    and at the very end of it, in reverse order (possibly overlapping).

    >>> print(mirror_ends(b'abXYZba').decode('ascii'))
    ab
    >>> print(mirror_ends(b'abca').decode('ascii'))
    a
    >>> print(mirror_ends(b'aba').decode('ascii'))
    aba
    """
    return string(data.begin(), mismatch(data.begin(), data.end(), data.rbegin()).first)


def mismatch_ints(vector[int] values1, vector[int] values2):
    """
    Test mismatch(first1, last1, first2).

    >>> mismatch_ints([1, 2, 3], [1, 2, 3])
    >>> mismatch_ints([1, 2], [1, 2, 3])
    >>> mismatch_ints([1, 3], [1, 2, 3])
    (3, 2)
    """
    result = mismatch(values1.begin(), values1.end(), values2.begin())
    if result.first == values1.end():
        return
    return deref(result.first), deref(result.second)


def is_int_in(vector[int] values, int target):
    """
    Test find.

    >>> is_int_in(range(5), 3)
    True
    >>> is_int_in(range(5), 10)
    False
    """
    return find(values.begin(), values.end(), target) != values.end()


def find_odd(vector[int] values):
    """
    Test find_if using is_odd predicate.

    >>> find_odd([2, 3, 4])
    3
    >>> find_odd([2, 4, 6])
    """
    result = find_if(values.begin(), values.end(), is_odd)
    if result != values.end():
        return deref(result)
    else:
        return None


def find_even(vector[int] values):
    """
    Test find_if_not using is_odd predicate.

    >>> find_even([3, 4, 5])
    4
    >>> find_even([1, 3, 5])
    """
    result = find_if_not(values.begin(), values.end(), is_odd)
    if result != values.end():
        return deref(result)
    else:
        return None


def find_last_int_sequence(vector[int] values, vector[int] target):
    """
    Test find_end.

    >>> find_last_int_sequence([1, 2, 3, 1, 2, 3], [2, 3])
    4
    >>> find_last_int_sequence([1, 2, 3], [4, 5])
    """
    result = find_end(values.begin(), values.end(), target.begin(), target.end())
    if result != values.end():
        return distance(values.begin(), result)
    else:
        return None


cdef bool is_equal(int lhs, int rhs):
    return lhs == rhs


def find_last_int_sequence2(vector[int] values, vector[int] target):
    """
    Test find_end (using is_equal predicate).

    >>> find_last_int_sequence2([1, 2, 3, 1, 2, 3], [2, 3])
    4
    >>> find_last_int_sequence2([1, 2, 3], [4, 5])
    """
    result = find_end(values.begin(), values.end(), target.begin(), target.end(), &is_equal)
    if result != values.end():
        return distance(values.begin(), result)
    else:
        return None


def find_first_int_in_set(values, target):
    """
    Test find_first_of.

    >>> find_first_int_in_set([1, 2, 3, 4, 5], [3, 5])
    2
    >>> find_first_int_in_set([1, 2, 3], [4, 5])
    """
    cdef vector[int] v = values
    cdef vector[int] t = target
    result = find_first_of(v.begin(), v.end(), t.begin(), t.end())
    if result != v.end():
        return distance(v.begin(), result)
    else:
        return None


def find_first_int_in_set2(vector[int] values, vector[int] target):
    """
    Test find_first_of with is_equal predicate.

    >>> find_first_int_in_set2([1, 2, 3, 4, 5], [3, 5])
    2
    >>> find_first_int_in_set2([1, 2, 3], [4, 5])
    """
    result = find_first_of(values.begin(), values.end(), target.begin(), target.end(), is_equal)
    if result != values.end():
        return distance(values.begin(), result)
    else:
        return None


def find_adjacent_int(vector[int] values):
    """
    Test adjacent_find.

    >>> find_adjacent_int([0, 1, 2, 3, 40, 40, 41, 41, 5])
    4
    >>> find_adjacent_int(range(5))
    """
    result = adjacent_find(values.begin(), values.end())
    if result != values.end():
        return distance(values.begin(), result)
    else:
        return None


def find_adjacent_int2(vector[int] values):
    """
    Test find_adjacent with is_equal predicate.

    >>> find_adjacent_int2([0, 1, 2, 3, 40, 40, 41, 41, 5])
    4
    >>> find_adjacent_int2(range(5))
    """
    result = adjacent_find(values.begin(), values.end(), is_equal)
    if result != values.end():
        return distance(values.begin(), result)
    else:
        return None


def in_quote(string quote, string word):
    """
    Test search using cppreference example.

    >>> in_quote(b"why waste time learning, when ignorance is instantaneous?", b"learning")
    True
    >>> in_quote(b"why waste time learning, when ignorance is instantaneous?", b"lemming")
    False
    """
    return search(quote.begin(), quote.end(), word.begin(), word.end()) != quote.end()


def in_quote2(string quote, string word):
    """
    Test search using cppreference example (with is_equal predicate).

    >>> in_quote2(b"why waste time learning, when ignorance is instantaneous?", b"learning")
    True
    >>> in_quote2(b"why waste time learning, when ignorance is instantaneous?", b"lemming")
    False
    """
    return search(quote.begin(), quote.end(), word.begin(), word.end(), &is_equal) != quote.end()


def consecutive_values(string c, int count, char v):
    """
    Test search_n using cppreference example (without std::begin and std::end).

    >>> consecutive_values(b"1001010100010101001010101", 4, ord("0"))
    False
    >>> consecutive_values(b"1001010100010101001010101", 3, ord("0"))
    True
    """
    return search_n(c.begin(), c.end(), count, v) != c.end()


def consecutive_values2(string c, int count, char v):
    """
    Test search_n using cppreference example (with is_equal predicate).

    >>> consecutive_values2(b"1001010100010101001010101", 4, ord("0"))
    False
    >>> consecutive_values2(b"1001010100010101001010101", 3, ord("0"))
    True
    """
    return search_n(c.begin(), c.end(), count, v, &is_equal) != c.end()
