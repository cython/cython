# mode: error
# tag: fstring

def incorrect_fstrings(x):
    return [
        f"""{}""",
        f"{}",
        f"{x!}",
        f"{x!q}",
        f"{{}}}",
        # This last one is a bit tricky now because newlines are allowed
        # in fstring bodies. Thus it has to go last because it confuses everything
        # else.
        f"{",
        f"",
    ]


_ERRORS = """
6:12: empty expression not allowed in f-string
7:10: empty expression not allowed in f-string
8:12: missing conversion character
9:12: invalid conversion character 'q'
10:14: f-string: single '}' is not allowed
11:10: FIXME
"""
