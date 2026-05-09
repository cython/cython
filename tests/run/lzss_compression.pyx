# mode: run
# tag: lzss, compression, string_compression

# cython: language_level=3
# distutils: define_macros=CYTHON_COMPRESS_STRINGS=90

import difflib
from itertools import count

from Cython.LZSS import lzss_compress

import cython
from libc.stdint cimport uint8_t

cdef extern from *:
    """
    static size_t __pyx_lzss_decompress (const uint8_t *src, uint8_t *dst, size_t dst_len);
    """
    size_t lzss_decompress "__pyx_lzss_decompress" (const uint8_t *src, uint8_t *dst, size_t dst_len)


MAKE_SURE_THERE_IS_SOMETHING_TO_COMPRESS = b'''
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
'''


def decompress_py(compressed: bytes):
    uncompressed = bytearray()
    iter_bytes = iter(compressed)
    eight_bits = list(range(0, 8))

    try:
        for flags in iter_bytes:
            for i in eight_bits:
                if flags & (1 << i):
                    c = next(iter_bytes)
                    uncompressed.append(c)
                    yield c
                else:
                    lo = next(iter_bytes)
                    hi = next(iter_bytes)
                    if (lo & 0x80) == 0:
                        p = lo
                        ml = hi
                    elif (hi & 0x80) == 0:
                        p = ((hi << 2) & 0x180) | (lo & 0x7F)
                        ml = hi & 0x1F
                    else:
                        p = (hi & 0x7F) << 7 | (lo & 0x7F)
                        ml = next(iter_bytes)

                    ml += 3;
                    copy = uncompressed[-p - ml : len(uncompressed) - p]
                    uncompressed.extend(copy)
                    yield from copy

    except StopIteration:
        pass


def _compare(b1: bytes, b2: bytes) -> str:
    return ''.join(difflib.ndiff(b1.decode('latin1'), b2.decode('latin1')))


def _print_start(prefix, s: bytes, cut=25):
    print(prefix, s[:cut] + (b'...' if len(s) > cut else b''))


def test(data: bytes) -> None:
    """
    # Decompressing very short or empty bytes is deliberately undefined behaviour.
    >>> test(b'a' * 3)
    SIZE: 3 -> 4
    >>> test(b'a' * 4)
    SIZE: 4 -> 5
    >>> test(b'a' * 5)
    SIZE: 5 -> 6
    >>> test(b'a' * 6)
    SIZE: 6 -> 6
    >>> test(b'a' * 7)
    SIZE: 7 -> 7
    >>> test(b'a' * 20)
    SIZE: 20 -> 10
    >>> test(b'a' * 197)
    SIZE: 197 -> 19
    >>> test(b'a' * 317)
    SIZE: 317 -> 19
    >>> test(b'avx' * 317)
    SIZE: 951 -> 27
    >>> test(b'\\0')
    SIZE: 1 -> 2
    >>> test(b'\\0' * 21)
    SIZE: 21 -> 10
    >>> test(b'\\0' * 463)
    SIZE: 463 -> 22
    >>> test(b'0123456789')
    SIZE: 10 -> 12
    >>> test(b'0123456789' * 21)
    SIZE: 210 -> 22
    >>> test(b'0123456789' * 463)
    SIZE: 4630 -> 74

    # Test cutoff at max offset (7+7 bits):
    >>> test(b'0123456789' + b'x' * ((1 << 14) - 4) + b'234569')
    SIZE: 16396 -> 227
    >>> test(b'0123456789' + b'x' * ((1 << 14) - 3) + b'234569')
    SIZE: 16397 -> 231

    >>> len(MAKE_SURE_THERE_IS_SOMETHING_TO_COMPRESS)
    1717
    >>> MAKE_SURE_THERE_IS_SOMETHING_TO_COMPRESS == b'\\n' + (b'a' * 77 + b'\\n') * 22
    True
    """
    uncompressed_length = len(data)

    compressed = lzss_compress(data)

    assert compressed if data else not compressed

    py_decomp = bytes(list(decompress_py(compressed)))  # GraalPy can't construct bytes from generators.

    if py_decomp != data:
        _print_start('I', data)
        _print_start('C', compressed)
        _print_start('P', py_decomp)

        for i, c, dec in zip(count(), data, py_decomp):
            if c != dec:
                print(f"PYTHON: …{data[max(0, i-5):i].decode('latin1')}[{chr(c)} != {chr(dec)}]{data[i+1:i+6].decode('latin1')}…")
                break

    output = bytearray(uncompressed_length + 4000)  # safety buffer
    compressed_length = <Py_ssize_t> lzss_decompress(compressed, output, uncompressed_length)

    assert compressed_length == len(compressed), (compressed[:20], compressed_length, len(compressed))

    output = bytes(output[:uncompressed_length])

    if output != data:
        _print_start('I', data)
        _print_start('C', compressed)
        _print_start('O', output)
        print(_compare(data, output))

    print(f"SIZE: {uncompressed_length} -> {compressed_length}")
