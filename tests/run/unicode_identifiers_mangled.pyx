# -*- coding: utf-8 -*-
# distutils: language = c++
# mode: run
# tag: cpp11

#cnames should be mangled for ΣtructnameInternal but not for ΣtructnamePublic
cdef struct ΣtructnameInternal:
    int α

cdef public struct ΣtructnamePublic:
    int α

from libcpp cimport bool

# use C template tricks to check the existance of an α attribute
cdef extern from *:
    r"""
    template <typename T>
    int has_alpha_impl(decltype(T::\u03b1)*) {
        return true;
    }
    template <typename T>
    int has_alpha_impl(...) {
        return false;
    }

    template <typename T>
    bool has_alpha() {
        return has_alpha_impl<T>(nullptr);
    }

    // a compile-time assertion that (sigma)tructnamePublic exists
    //  (the "internal" varient would fail)
    void name_exists(struct \u03a3tructnamePublic* ) {}
    """
    bool has_alpha[T]()


def internal_has_alpha():
    """
    >>> internal_has_alpha()
    False
    """
    return has_alpha[ΣtructnameInternal]()

def public_has_alpha():
    """
    >>> public_has_alpha()
    True
    """
    return has_alpha[ΣtructnamePublic]()

