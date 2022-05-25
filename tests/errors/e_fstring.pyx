# mode: error
# tag: fstring

def incorrect_fstrings(x):
    return [
        f"{x}{'\\'}'{x+1}",
        f"""{}""",
        f"{}",
        f"{x!}",
        f"{",
        f"{{}}}",
    ]


_ERRORS = """
6:16: backslashes not allowed in f-strings
7:14: empty expression not allowed in f-string
8:12: empty expression not allowed in f-string
9:14: missing '}' in format string expression, found '!'
10:12: empty expression not allowed in f-string
10:12: missing '}' in format string expression
11:15: f-string: single '}' is not allowed
"""
