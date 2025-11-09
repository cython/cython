@cython.locals(
    counts=cython.int[10],
    digit=cython.int)

def count_digits(digits):
    counts = [0] * 10
    
    for digit in digits:
        assert 0 <= digit <= 9
        counts[digit] += 1
    
    return counts