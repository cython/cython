"""
LZSS-like compressor.

See decompression function in StringTools.c, "DecompressString_LZSS".
"""

from __future__ import annotations

from collections import defaultdict

import cython

PRINT_STATS = False


def lzss_compress(data: bytes) -> bytes:
    """
    LZSS-like compressor.

    Uses a byte triplet dict for fast match finding.
    Outputs a bit stream with small overhead.

    Args:
        data: Input bytes to compress

    Returns:
        Compressed bytes (no header/metadata, decompressor must know output size)
    """
    if not data:
        return b''

    # Hash table: maps 3-byte sequences to a list of positions starting with that sequence.
    hash_table = defaultdict(list)

    def find_longest_match(pos: cython.Py_ssize_t) -> tuple[cython.Py_ssize_t, cython.Py_ssize_t]:
        """Find longest match in sliding window. Returns (offset, length)."""
        if pos + 3 > len(data):
            return (0, 0)

        # 14-bit offset (max 16KiB lookback)
        WINDOW_SIZE: cython.long = 1 << 14
        # 8-bit length + 3, allowing up to 258 bytes.
        MAX_MATCH: cython.long = min(255 + 3, len(data) - pos)

        best_len: cython.Py_ssize_t = 0
        best_offset: cython.Py_ssize_t = 0
        window_start: cython.Py_ssize_t = max(0, pos - WINDOW_SIZE - MAX_MATCH)

        prev_pos: cython.Py_ssize_t
        match_len: cython.long
        max_len: cython.long

        # Check all positions starting with the same 3-byte sequence.
        key = data[pos:pos+3]
        if key not in hash_table:
            return (0, 0)

        for prev_pos in hash_table[key]:
            if prev_pos < window_start or prev_pos >= pos:
                continue

            # Extend match as far as possible.
            match_len = 3
            max_len = min(MAX_MATCH, pos - prev_pos)
            while match_len < max_len and data[prev_pos + match_len] == data[pos + match_len]:
                match_len += 1

            # Prefer longer matches, break ties by preferring closer offsets.
            if match_len > best_len:
                best_len = match_len
                best_offset = pos - prev_pos

        # Lazy matching: check if next position has a better match.
        next_key = data[pos + 1:pos + 4]
        if 0 < best_len < MAX_MATCH and next_key in hash_table and pos + best_len + 1 < len(data):
            next_best_len: cython.Py_ssize_t = 0
            window_start = max(0, pos + 1 - WINDOW_SIZE - MAX_MATCH)

            for prev_pos in hash_table[next_key]:
                if prev_pos < window_start:
                    continue

                match_len = 3
                max_len = min(MAX_MATCH, pos - prev_pos)
                while match_len < max_len and data[prev_pos + match_len] == data[pos + 1 + match_len]:
                    match_len += 1

                if match_len > next_best_len:
                    next_best_len = match_len

            # If the next position has a significantly better match, ignore this one.
            if next_best_len > best_len + 1:
                best_offset = best_len = 0

        return (best_offset, best_len)

    # Build output as bit stream.
    output = bytearray(b'\0')
    pos: cython.Py_ssize_t = 0
    flags_pos: cython.Py_ssize_t = 0
    flags: cython.int = 0xFF0000

    stats = [0, 0, 0, 0]

    while pos < len(data):
        offset, length = find_longest_match(pos)

        #if offset > 0:
        #    assert data[pos:pos+length] == data[pos-offset:pos-offset+length], (
        #        data[pos:pos+3], data[pos-offset:pos-offset+length])

        # Update hash table for current position.
        key = data[pos:pos+3]
        hash_table[key].append(pos)

        flag = 0
        offset -= length  # offset >= length if interesting, so remove redundancy.

        # See if the match is worth it and store a single literal byte otherwise.

        if length > 2 and 0 <= offset <= 0x7F:
            # Store 7 bit offset and length as two bytes.
            output.append(offset)
            #assert output[-1] & 0x80 == 0
            output.append(length - 3)
            stats[1] += 1
        elif length > 2 and length - 3 <= 0x1F and 0 <= offset <= 0x1FF:
            # Store a longer 7+2 bit offset at the cost of a shorter 5 bit length.
            output.append((offset & 0x7F) | 0x80)
            output.append(((offset & 0x180) >> 2) | (length - 3))
            #assert output[-1] & 0x80 == 0
            stats[2] += 1
        elif length > 3 and 0 <= offset < (1 << 14):
            # Store a 7+7 bit offset with a separate 8 bit length.
            output.append(offset & 0x7F | 0x80)
            output.append((offset >> 7) & 0x7F | 0x80)
            output.append(length - 3)
            stats[3] += 1
        else:
            # Encode 8 bit literal + 1 bit flag.
            flag = 1
            length = 1
            output.append(data[pos])
            stats[0] += 1

        pos += length

        flags = (flag << 7) | (flags >> 1)
        if flags < 0x10000:
            output[flags_pos] = flags & 0xFF
            flags_pos = len(output)
            output.append(0)  # next flags
            flags = 0xFF0000

    if flags_pos == len(output) - 1:
        output.pop()
    else:
        # Pad flags with empty non-literals
        # - decompressor must stop at the end of the output buffer !
        while flags >= 0x10000:
            flags >>= 1
        output[flags_pos] = flags & 0xFF

    if PRINT_STATS:
        print("BYTES:", len(data), "->", len(output))
        print("ENCODINGS:", stats)

    return bytes(output)
