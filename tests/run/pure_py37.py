# mode: run
# tag: pure3.7

import cython


def test_module_getattr_pointers:
    cython.p_int
    cython.pp_int
    cython.ppp_int   # < py3.7 limit in interpreted mode

    cython.pppp_int  # dynamic attr generation
    cython.pppppppppppppppppppppp_int

    # test on another type
    cython.ppppppppppppppppp_float


def test_module_getattr_import_pointers:
    # test direct import
    from cython import pppp_int
