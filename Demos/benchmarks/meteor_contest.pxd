cimport cython

cdef list rotate(list ido, dict rd=*)

cdef list flip(list ido, dict fd=*)

cdef list permute(list ido, list r_ido)

@cython.locals(n_i_min=long)
cpdef solve(long n, long i_min, free, list curr_board, list pieces_left, list solutions,
            list fps=*, list se_nh=*, bisect=*)
