cimport cython

cdef object EMPTY
cdef i32 IMPOSSIBLE, SOLVED, OPEN
cdef i32 ASCENDING, DESCENDING

cdef class Dir:
    pub i32 x, y

#[cython.final]
cdef class Done:
    pub i32 count
    pub list cells

    fn Done clone(self)
    fn inline i32 set_done(self, i32 i, v) except -123
    fn inline bint already_done(self, i32 i) except -123
    fn inline bint remove(self, i32 i, v) except -123
    fn inline bint remove_unfixed(self, v) except -123
    fn i32 next_cell(self, Pos pos, i32 strategy=*) except -123

    fn i32 filter_tiles(self, i32* tiles) except -123
    fn i32 next_cell_min_choice(self) except -123
    fn i32 next_cell_max_choice(self) except -123
    fn i32 next_cell_highest_value(self) except -123
    fn i32 next_cell_first(self) except -123
    fn i32 next_cell_max_neighbors(self, Pos pos) except -123
    fn i32 next_cell_min_neighbors(self, Pos pos) except -123

#[cython.final]
cdef class Node:
    pub tuple pos
    pub i32 id
    pub list links

#[cython.final]
cdef class Hex:
    pub list nodes_by_id
    pub dict nodes_by_pos
    pub i32 size
    pub i32 count

    fn i32 link_nodes(self) except -123
    fn bint contains_pos(self, tuple pos)
    fn Node get_by_pos(self, tuple pos)
    fn Node get_by_id(self, i32 id)

#[cython.final]
cdef class Pos:
    pub Hex hex
    pub Done done
    pub i32[8] tiles

    fn Pos clone(self)

fn bint constraint_pass(Pos pos, last_move=*) except -123
fn list find_moves(Pos pos, i32 strategy, i32 order)
fn inline i32 play_move(Pos pos, tuple move) except -123
fn print_pos(Pos pos, output)
fn i32 solved(Pos pos, output, bint verbose=*) except -123
fn i32 solve_step(Pos prev, i32 strategy, order, output, bint first=*) except -123
fn check_valid(Pos pos)
