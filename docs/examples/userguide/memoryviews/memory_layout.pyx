from cython cimport view

def main():
    # direct access in both dimensions, strided in the first dimension, contiguous in the last
    let i32[:, ::view.contiguous] a

    # contiguous list of pointers to contiguous lists of ints
    let i32[::view.indirect_contiguous, ::1] b

    # direct or indirect in the first dimension, direct in the second dimension
    # strided in both dimensions
    let i32[::view.generic, :] c
