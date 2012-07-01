# tag: numpy
# tag: openmp
# mode: run

include "utils.pxi"

ctypedef fused _dtype_t:
    double
    object

_dtype = np.double

m = np.arange(4 * 8, dtype=_dtype).reshape(4, 8)

def test_strided():
    """
    Test strided layouts. See the actual tests below

    >>> order = {{ORDER}}
    >>> test_strided(m.copy(order=order), m.copy(order=order))
    array([[   0.,    2.,    6.,   12.,   20.,   30.,   42.,   56.],
           [  72.,   90.,  110.,  132.,  156.,  182.,  210.,  240.],
           [ 272.,  306.,  342.,  380.,  420.,  462.,  506.,  552.],
           [ 600.,  650.,  702.,  756.,  812.,  870.,  930.,  992.]])
    >>> test_strided(m.copy(order=order)[::2], m.copy(order=order)[1::2])
    array([[   0.,   10.,   22.,   36.,   52.,   70.,   90.,  112.],
           [ 400.,  442.,  486.,  532.,  580.,  630.,  682.,  736.]])
    >>> test_strided(m.copy(order=order)[::2, ::-2], m.copy(order=order)[1::2, ::-2])
    array([[ 112.,   70.,   36.,   10.],
           [ 736.,  630.,  532.,  442.]])
    """

@testcase_like_sub(test_strided, {'{{ORDER}}': '"C"'})
def test_strided_c(_dtype_t[:, :] m1, _dtype_t[:, :] m2):
    m1[:] = m1 + m2 * m1
    return np.asarray(m1)

@testcase_like_sub(test_strided, {'{{ORDER}}': '"F"'})
def test_strided_f(_dtype_t[:, :] m1, _dtype_t[:, :] m2):
    m1[:] = m1 + m2 * m1
    return np.asarray(m1)


def test_contig():
    """
    >>> order1, order2 = {{ORDER1}}, {{ORDER2}}
    >>> test_contig(m.copy(order=order1), m.copy(order=order2))
    array([[   0.,    2.,    6.,   12.,   20.,   30.,   42.,   56.],
           [  72.,   90.,  110.,  132.,  156.,  182.,  210.,  240.],
           [ 272.,  306.,  342.,  380.,  420.,  462.,  506.,  552.],
           [ 600.,  650.,  702.,  756.,  812.,  870.,  930.,  992.]])
    """

@testcase_like_sub(test_contig, {'{{ORDER1}}': '"C"', '{{ORDER2}}': '"F"'})
def test_contig_cf(_dtype_t[:, ::1] m1, _dtype_t[::1, :] m2):
    m1[:] = m1 + m2 * m1
    return np.asarray(m1)

@testcase_like_sub(test_contig, {'{{ORDER1}}': '"F"', '{{ORDER2}}': '"C"'})
def test_contig_fc(_dtype_t[::1, :] m1, _dtype_t[:, ::1] m2):
    m1[:] = m1 + m2 * m1
    return np.asarray(m1)

@testcase_like_sub(test_contig, {'{{ORDER1}}': '"C"', '{{ORDER2}}': '"C"'})
def test_contig_cc(_dtype_t[:, ::1] m1, _dtype_t[:, ::1] m2):
    m1[:] = m1 + m2 * m1
    return np.asarray(m1)

@testcase_like_sub(test_contig, {'{{ORDER1}}': '"F"', '{{ORDER2}}': '"F"'})
def test_contig_ff(_dtype_t[::1, :] m1, _dtype_t[::1, :] m2):
    m1[:] = m1 + m2 * m1
    return np.asarray(m1)

@testcase
def test_tiling(double[:, :] m1, double[:, :] m2):
    """
    >>> result = test_tiling(m.copy(), m.copy(order='F'))
    >>> result
    array([[   0.,    2.,    6.,   12.,   20.,   30.,   42.,   56.],
           [  72.,   90.,  110.,  132.,  156.,  182.,  210.,  240.],
           [ 272.,  306.,  342.,  380.,  420.,  462.,  506.,  552.],
           [ 600.,  650.,  702.,  756.,  812.,  870.,  930.,  992.]])
    >>> np.all(test_tiling(m.copy(order='F'), m.copy()) == result)
    True

    >>> result = test_tiling(m.copy()[::2], m.copy(order='F')[::2])
    >>> result
    array([[   0.,    2.,    6.,   12.,   20.,   30.,   42.,   56.],
           [ 272.,  306.,  342.,  380.,  420.,  462.,  506.,  552.]])
    >>> np.all(test_tiling(m.copy(order='F')[::2], m.copy()[::2]) == result)
    True
    """
    m1[:] = m1 + m2 * m1
    return np.asarray(m1)


