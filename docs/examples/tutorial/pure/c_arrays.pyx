def count_digits(digits):
    cdef int[10] counts = [0] * 10

    cdef int digit

    for digit in digits:
        assert 0 <= digit <= 9
        counts[digit] += 1
    
    return list(counts)
