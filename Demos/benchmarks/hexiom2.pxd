cimport cython

cdef object EMPTY
cdef int IMPOSSIBLE, SOLVED, OPEN
cdef int ASCENDING, DESCENDING

cdef class Dir:
    cdef public int x, y


@cython.final
cdef class Done:
    cdef public int count
    cdef public list cells

    cdef Done clone(self)
    cdef inline int set_done(self, int i, v) except -123
    cdef inline bint already_done(self, int i) except -123
    cdef inline bint remove(self, int i, v) except -123
    cdef inline bint remove_unfixed(self, v) except -123
    cdef int next_cell(self, Pos pos, int strategy=*) except -123

    cdef int filter_tiles(self, int* tiles) except -123
    cdef int next_cell_min_choice(self) except -123
    cdef int next_cell_max_choice(self) except -123
    cdef int next_cell_highest_value(self) except -123
    cdef int next_cell_first(self) except -123
    cdef int next_cell_max_neighbors(self, Pos pos) except -123
    cdef int next_cell_min_neighbors(self, Pos pos) except -123


@cython.final
cdef class Node:
    cdef public tuple pos
    cdef public int id
    cdef public list links


@cython.final
cdef class Hex:
    cdef public list nodes_by_id
    cdef public dict nodes_by_pos
    cdef public int size
    cdef public int count

    cdef int link_nodes(self) except -123
    cdef bint contains_pos(self, tuple pos)
    cdef Node get_by_pos(self, tuple pos)
    cdef Node get_by_id(self, int id)


@cython.final
cdef class Pos:
    cdef public Hex hex
    cdef public Done done
    cdef public int[8] tiles

    cdef Pos clone(self)


cdef bint constraint_pass(Pos pos, last_move=*) except -123
cdef list find_moves(Pos pos, int strategy, int order)
cdef inline int play_move(Pos pos, tuple move) except -123
cdef print_pos(Pos pos, output)
cdef int solved(Pos pos, output, bint verbose=*) except -123
cdef int solve_step(Pos prev, int strategy, order, output, bint first=*) except -123
cdef check_valid(Pos pos)
