cimport cython

fn list rotate(list ido, dict rd=*)

fn list flip(list ido, dict fd=*)

fn list permute(list ido, list r_ido)

@cython.locals(n_i_min=i64)
cpdef solve(i64 n, i64 i_min, free, list curr_board, list pieces_left, list solutions,
            list fps=*, list se_nh=*, bisect=*)
