# mode: compile

cdef int i, j, k
cdef object a, b, x

for i from 0 <= i < 10:
    pass
for i from 0 < i <= 10:
    pass
for i from 10 >= i > 0:
    pass
for i from 10 > i >= 0:
    pass

for x from 0 <= x <= 10:
    pass

for i from a <= i <= b:
    pass

for i from k <= i <= j:
    pass

for i from k * 42 <= i <= j / 18:
    pass

while j:
    for i from 0 <= i <= 10:
        continue
        break
    else:
        continue
        break

