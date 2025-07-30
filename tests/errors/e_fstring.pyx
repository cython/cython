# mode: error
# tag: fstring

def incorrect_fstrings(x):
    return [
        f"""{}""",
        f"{}",
        f"{x!}",
        f"{x!q}",
        f"{",
        f"{{}}}",
    ]


_ERRORS = """
6:12: empty expression not allowed in f-string
7:10: empty expression not allowed in f-string
8:13: missing conversion character
9:13: invalid conversion character 'q'
10:14: f-string: single '}' is not allowed
11:15: FIXME
"""
