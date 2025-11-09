def count_digits(digits):
    cdef int counts[10]  
    cdef int digit

    for i in range(10):
        counts[i] = 0

    for digit in digits:
        assert 0 <= digit <= 9
        counts[digit] += 1
    
    return list(counts)