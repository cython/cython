# mode: run
# tag: datetime
# cython: freethreading_compatible=True

from cpython.datetime cimport date, datetime, time, timedelta, tzinfo

import subprocess
import sys
import textwrap


cdef class NativeDatetime(datetime):
    cdef object payload


class SubDatetime(NativeDatetime):
    pass


def make_datetime():
    cdef NativeDatetime value = SubDatetime(2024, 1, 1)
    value.payload = value
    return value


def get_types():
    return date, datetime, time, timedelta, tzinfo


def test_patched_datetime_module():
    """
    Native datetime types must not bind to Python replacements at import time.

    >>> test_patched_datetime_module()
    """
    code = textwrap.dedent("""
        import datetime
        import gc
        import importlib.util
        import sys
        import weakref

        sys.path[:0] = sys.argv[3:]
        names = ('date', 'datetime', 'time', 'timedelta', 'tzinfo')
        original_types = tuple(getattr(datetime, name) for name in names)
        if sys.implementation.name == 'cpython':
            import _datetime
            for name, original in zip(names, original_types):
                replacement = type('Fake' + name, (original,), {})
                setattr(datetime, name, replacement)
                setattr(_datetime, name, replacement)

        spec = importlib.util.spec_from_file_location(sys.argv[1], sys.argv[2])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        value = module.make_datetime()
        reference = weakref.ref(value)
        del value
        gc.collect()
        assert reference() is None
        assert module.get_types() == original_types
    """)
    result = subprocess.run(
        [sys.executable, '-c', code, __name__, __file__, *sys.path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode('utf8', 'replace')


def test_invalid_datetime_c_api():
    """
    A failed C API import must propagate the exception without using a null pointer.

    >>> test_invalid_datetime_c_api()
    """
    if sys.implementation.name != 'cpython':
        return
    code = textwrap.dedent("""
        import datetime
        import importlib.util
        import sys

        sys.path[:0] = sys.argv[3:]
        datetime.datetime_CAPI = None
        spec = importlib.util.spec_from_file_location(sys.argv[1], sys.argv[2])
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except AttributeError as exc:
            assert 'datetime.datetime_CAPI' in str(exc), str(exc)
        else:
            raise AssertionError('Import succeeded with an invalid datetime C API')
    """)
    result = subprocess.run(
        [sys.executable, '-c', code, __name__, __file__, *sys.path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert result.returncode == 0, result.stderr.decode('utf8', 'replace')
