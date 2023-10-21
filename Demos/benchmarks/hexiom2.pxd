cimport cython

cdef object EMPTY
cdef i32 IMPOSSIBLE, SOLVED, OPEN
cdef i32 ASCENDING, DESCENDING

cdef class Dir:
    cdef public i32 x, y

@cython.final
cdef class Done:
    cdef public i32 count
    cdef public list cells

    cdef Done clone(self)
    cdef inline i32 set_done(self, i32 i, v) except -123
    cdef inline bint already_done(self, i32 i) except -123
    cdef inline bint remove(self, i32 i, v) except -123
    cdef inline bint remove_unfixed(self, v) except -123
    cdef i32 next_cell(self, Pos pos, i32 strategy=*) except -123

    cdef i32 filter_tiles(self, i32* tiles) except -123
    cdef i32 next_cell_min_choice(self) except -123
    cdef i32 next_cell_max_choice(self) except -123
    cdef i32 next_cell_highest_value(self) except -123
    cdef i32 next_cell_first(self) except -123
    cdef i32 next_cell_max_neighbors(self, Pos pos) except -123
    cdef i32 next_cell_min_neighbors(self, Pos pos) except -123

@cython.final
cdef class Node:
    cdef public tuple pos
    cdef public i32 id
    cdef public list links

@cython.final
cdef class Hex:
    cdef public list nodes_by_id
    cdef public dict nodes_by_pos
    cdef public i32 size
    cdef public i32 count

    cdef i32 link_nodes(self) except -123
    cdef bint contains_pos(self, tuple pos)
    cdef Node get_by_pos(self, tuple pos)
    cdef Node get_by_id(self, i32 id)

@cython.final
cdef class Pos:
    cdef public Hex hex
    cdef public Done done
    cdef public i32[8] tiles

    cdef Pos clone(self)

cdef bint constraint_pass(Pos pos, last_move=*) except -123
cdef list find_moves(Pos pos, i32 strategy, i32 order)
cdef inline i32 play_move(Pos pos, tuple move) except -123
cdef print_pos(Pos pos, output)
cdef i32 solved(Pos pos, output, bint verbose=*) except -123
cdef i32 solve_step(Pos prev, i32 strategy, order, output, bint first=*) except -123
cdef check_valid(Pos pos)
