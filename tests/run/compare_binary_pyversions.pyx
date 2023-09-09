# mode: run
# tag: internal

cdef extern from *:
    int check_binary_version "__Pyx_check_binary_version" (unsigned long ct_version, unsigned long rt_version, int allow_newer) except -1
    unsigned long get_runtime_version "__Pyx_get_runtime_version" ()
    unsigned long PY_VERSION_HEX


def test_get_runtime_version():
    """
    >>> test_get_runtime_version()
    True
    """
    cdef unsigned long rt_version = get_runtime_version()
    return PY_VERSION_HEX & ~0xFF == rt_version or  (hex(PY_VERSION_HEX), hex(rt_version))


def iter_hex_versions():
    cdef long major, minor, dot
    for major in range(0, 20):
        for minor in range(0, 20, 3):
            for dot in range(0, 20, 3):
                yield ((major * 16 + minor) * 16 + dot) * 16


def test_compare_binary_versions_exact():
    """
    >>> import warnings
    >>> warnings.simplefilter("error")
    >>> test_compare_binary_versions_exact()
    >>> warnings.resetwarnings()
    """
    cdef long major_and_minor = 0xFFFF0000
    cdef long rt_version, ct_version

    versions = list(iter_hex_versions())
    for ct_version in versions:
        for rt_version in versions:
            if rt_version & major_and_minor == ct_version & major_and_minor:
                assert check_binary_version(ct_version, rt_version, 0) == 0, (hex(rt_version), hex(ct_version))
            else:
                try:
                    check_binary_version(ct_version, rt_version, 0)
                except Warning as exc:
                    assert "does not match runtime version" in str(exc), exc
                else:
                    assert not "raised", (hex(rt_version), hex(ct_version))


def test_compare_binary_versions_minimum():
    """
    >>> import warnings
    >>> warnings.simplefilter("error")
    >>> test_compare_binary_versions_minimum()
    >>> warnings.resetwarnings()
    """
    cdef long major_and_minor = 0xFFFF0000
    cdef long rt_version, ct_version

    versions = list(iter_hex_versions())
    for ct_version in versions:
        for rt_version in versions:
            if rt_version & major_and_minor >= ct_version & major_and_minor:
                result = check_binary_version(ct_version, rt_version, 1)
                if rt_version & major_and_minor > ct_version & major_and_minor:
                    assert result == 1, (hex(rt_version), hex(ct_version))
                else:
                    assert result == 0, (hex(rt_version), hex(ct_version))
            else:
                try:
                    check_binary_version(ct_version, rt_version, 1)
                except Warning as exc:
                    if rt_version & major_and_minor < ct_version & major_and_minor:
                        assert "was newer than runtime version" in str(exc), exc
                    else:
                        assert "does not match runtime version" in str(exc), exc
                else:
                    assert not "raised", (hex(rt_version), hex(ct_version))
