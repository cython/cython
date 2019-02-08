"""
Python Lexical Analyser

Exception classes
"""


class PlexError(Exception):
    message = ""


class PlexTypeError(PlexError, TypeError):
    pass


class PlexValueError(PlexError, ValueError):
    pass


class InvalidRegex(PlexError):
    pass


class InvalidToken(PlexError):
    def __init__(self, token_number, message):
        msg = ("Token number {number}: {message}"
               .format(number=token_number, message=message))
        PlexError.__init__(self, msg)


class InvalidScanner(PlexError):
    pass


class AmbiguousAction(PlexError):
    message = "Two tokens with different actions can match the same string"

    def __init__(self):
        pass


class UnrecognizedInput(PlexError):
    scanner = None
    position = None
    state_name = None

    def __init__(self, scanner, state_name):
        self.scanner = scanner
        self.position = scanner.get_position()
        self.state_name = state_name

    def __str__(self):
        pos, line, char = self.position
        msg = ("'{pos}', line {line}, char {char}: Token not recognised in "
               "state {state}"
               .format(pos=pos, line=line, char=char, state=self.state_name))
        return msg
