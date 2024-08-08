# mode: run
# tag: pure3.7

import cython


def test_module_getattr_pointers():
    pint: cython.p_int
    ppint: cython.pp_int
    pppint: cython.ppp_int

    ppppint: cython.pppp_int  # dynamic attr generation
    ppppppppppppppppppppppint: cython.pppppppppppppppppppppp_int

    # test on another type
    pppppppppppppppppfloat: cython.ppppppppppppppppp_float


def test_module_getattr_import_pointers():
    # test direct import
    from cython import pppp_int
