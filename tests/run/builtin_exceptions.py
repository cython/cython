# mode: run
# tag: exception


# This test file is generated based on the known builtin exceptions.
# To regenerate the tests from a newer Python version, run the file:
#
#    python3 tests/run/builtin_exceptions.py


NEWER_EXCEPTIONS = {
    # Remove when increasing minimal supported Python version.
    'PythonFinalizationError': (3, 10),
    'EncodingWarning': (3, 10),
    'ExceptionGroup': (3, 11),
    'BaseExceptionGroup': (3, 11),
}

CALL_ARGS = {
    'UnicodeError'
}


def gen_tests():
    import builtins
    import sys
    from collections import defaultdict

    with open(__file__, encoding='utf8') as test_file:
        test_code = test_file.readlines()

    # Note: the following strings must not contain the marker lines!
    original_end_code = test_code[test_code.index("##### " + "END GENERATED TESTS\n"):]
    del test_code[test_code.index("##### " + "BEGIN GENERATED TESTS\n") + 1:]

    test_code.append(f"# generated from the builtin exceptions in Python {tuple(sys.version_info)}\n")

    # Construct the list of all exception subtypes.
    subclasses = defaultdict(list)
    for exc_name, exc_type in vars(builtins).items():
        if not isinstance(exc_type, type) or not issubclass(exc_type, BaseException):
            continue
        if exc_name in NEWER_EXCEPTIONS:
            # Ignore recent exceptions for now.
            continue

        try:
            exc_type("message")
        except TypeError:
            # Needs arguments - ignore.
            continue
        for base_type in exc_type.__mro__:
            subclasses[base_type.__name__].append(exc_name)
            if base_type.__name__ == 'BaseException':
                break

    # Generate tests that pass all subtypes into a typed base type argument.
    for exc_name, subclass_names in sorted(subclasses.items()):
        test_code.append("\n")
        test_code.append(f"def accept_{exc_name}(exc: {exc_name}):\n")

        func_code = []
        func_code.append('"""')
        for subclass_name in subclass_names:
            func_code.append(f">>> accept_{exc_name}({subclass_name}('message'))")
            func_code.append(f">>> class MyExceptionSubtype_{subclass_name}({subclass_name}): pass")
            func_code.append(f">>> accept_{exc_name}(MyExceptionSubtype_{subclass_name}('message'))")
        func_code.append('"""')
        func_code.append(f"exc_var: {exc_name} = {{exc}}.pop()")  # untype the RHS
        func_code.append(f"assert isinstance(exc, BaseException)")
        func_code.append(f"assert {exc_name} in type(exc).__mro__")
        func_code.append(f"assert isinstance(exc, {exc_name})")
        func_code.append(f"assert exc.args == ('message',)")

        # indent and insert test function body
        test_code.extend(f"    {line}\n" for line in func_code)

    test_code.append("\n")
    test_code += original_end_code
    test_code_str = ''.join(test_code)

    with open(__file__, encoding='utf8', mode='w') as test_file:
        test_file.write(test_code_str)

##### BEGIN GENERATED TESTS
# generated from the builtin exceptions in Python (3, 12, 3, 'final', 0)

def accept_ArithmeticError(exc: ArithmeticError):
    """
    >>> accept_ArithmeticError(ArithmeticError('message'))
    >>> class MyExceptionSubtype_ArithmeticError(ArithmeticError): pass
    >>> accept_ArithmeticError(MyExceptionSubtype_ArithmeticError('message'))
    >>> accept_ArithmeticError(FloatingPointError('message'))
    >>> class MyExceptionSubtype_FloatingPointError(FloatingPointError): pass
    >>> accept_ArithmeticError(MyExceptionSubtype_FloatingPointError('message'))
    >>> accept_ArithmeticError(OverflowError('message'))
    >>> class MyExceptionSubtype_OverflowError(OverflowError): pass
    >>> accept_ArithmeticError(MyExceptionSubtype_OverflowError('message'))
    >>> accept_ArithmeticError(ZeroDivisionError('message'))
    >>> class MyExceptionSubtype_ZeroDivisionError(ZeroDivisionError): pass
    >>> accept_ArithmeticError(MyExceptionSubtype_ZeroDivisionError('message'))
    """
    exc_var: ArithmeticError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ArithmeticError in type(exc).__mro__
    assert isinstance(exc, ArithmeticError)
    assert exc.args == ('message',)

def accept_AssertionError(exc: AssertionError):
    """
    >>> accept_AssertionError(AssertionError('message'))
    >>> class MyExceptionSubtype_AssertionError(AssertionError): pass
    >>> accept_AssertionError(MyExceptionSubtype_AssertionError('message'))
    """
    exc_var: AssertionError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert AssertionError in type(exc).__mro__
    assert isinstance(exc, AssertionError)
    assert exc.args == ('message',)

def accept_AttributeError(exc: AttributeError):
    """
    >>> accept_AttributeError(AttributeError('message'))
    >>> class MyExceptionSubtype_AttributeError(AttributeError): pass
    >>> accept_AttributeError(MyExceptionSubtype_AttributeError('message'))
    """
    exc_var: AttributeError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert AttributeError in type(exc).__mro__
    assert isinstance(exc, AttributeError)
    assert exc.args == ('message',)

def accept_BaseException(exc: BaseException):
    """
    >>> accept_BaseException(BaseException('message'))
    >>> class MyExceptionSubtype_BaseException(BaseException): pass
    >>> accept_BaseException(MyExceptionSubtype_BaseException('message'))
    >>> accept_BaseException(Exception('message'))
    >>> class MyExceptionSubtype_Exception(Exception): pass
    >>> accept_BaseException(MyExceptionSubtype_Exception('message'))
    >>> accept_BaseException(GeneratorExit('message'))
    >>> class MyExceptionSubtype_GeneratorExit(GeneratorExit): pass
    >>> accept_BaseException(MyExceptionSubtype_GeneratorExit('message'))
    >>> accept_BaseException(KeyboardInterrupt('message'))
    >>> class MyExceptionSubtype_KeyboardInterrupt(KeyboardInterrupt): pass
    >>> accept_BaseException(MyExceptionSubtype_KeyboardInterrupt('message'))
    >>> accept_BaseException(SystemExit('message'))
    >>> class MyExceptionSubtype_SystemExit(SystemExit): pass
    >>> accept_BaseException(MyExceptionSubtype_SystemExit('message'))
    >>> accept_BaseException(ArithmeticError('message'))
    >>> class MyExceptionSubtype_ArithmeticError(ArithmeticError): pass
    >>> accept_BaseException(MyExceptionSubtype_ArithmeticError('message'))
    >>> accept_BaseException(AssertionError('message'))
    >>> class MyExceptionSubtype_AssertionError(AssertionError): pass
    >>> accept_BaseException(MyExceptionSubtype_AssertionError('message'))
    >>> accept_BaseException(AttributeError('message'))
    >>> class MyExceptionSubtype_AttributeError(AttributeError): pass
    >>> accept_BaseException(MyExceptionSubtype_AttributeError('message'))
    >>> accept_BaseException(BufferError('message'))
    >>> class MyExceptionSubtype_BufferError(BufferError): pass
    >>> accept_BaseException(MyExceptionSubtype_BufferError('message'))
    >>> accept_BaseException(EOFError('message'))
    >>> class MyExceptionSubtype_EOFError(EOFError): pass
    >>> accept_BaseException(MyExceptionSubtype_EOFError('message'))
    >>> accept_BaseException(ImportError('message'))
    >>> class MyExceptionSubtype_ImportError(ImportError): pass
    >>> accept_BaseException(MyExceptionSubtype_ImportError('message'))
    >>> accept_BaseException(LookupError('message'))
    >>> class MyExceptionSubtype_LookupError(LookupError): pass
    >>> accept_BaseException(MyExceptionSubtype_LookupError('message'))
    >>> accept_BaseException(MemoryError('message'))
    >>> class MyExceptionSubtype_MemoryError(MemoryError): pass
    >>> accept_BaseException(MyExceptionSubtype_MemoryError('message'))
    >>> accept_BaseException(NameError('message'))
    >>> class MyExceptionSubtype_NameError(NameError): pass
    >>> accept_BaseException(MyExceptionSubtype_NameError('message'))
    >>> accept_BaseException(OSError('message'))
    >>> class MyExceptionSubtype_OSError(OSError): pass
    >>> accept_BaseException(MyExceptionSubtype_OSError('message'))
    >>> accept_BaseException(ReferenceError('message'))
    >>> class MyExceptionSubtype_ReferenceError(ReferenceError): pass
    >>> accept_BaseException(MyExceptionSubtype_ReferenceError('message'))
    >>> accept_BaseException(RuntimeError('message'))
    >>> class MyExceptionSubtype_RuntimeError(RuntimeError): pass
    >>> accept_BaseException(MyExceptionSubtype_RuntimeError('message'))
    >>> accept_BaseException(StopAsyncIteration('message'))
    >>> class MyExceptionSubtype_StopAsyncIteration(StopAsyncIteration): pass
    >>> accept_BaseException(MyExceptionSubtype_StopAsyncIteration('message'))
    >>> accept_BaseException(StopIteration('message'))
    >>> class MyExceptionSubtype_StopIteration(StopIteration): pass
    >>> accept_BaseException(MyExceptionSubtype_StopIteration('message'))
    >>> accept_BaseException(SyntaxError('message'))
    >>> class MyExceptionSubtype_SyntaxError(SyntaxError): pass
    >>> accept_BaseException(MyExceptionSubtype_SyntaxError('message'))
    >>> accept_BaseException(SystemError('message'))
    >>> class MyExceptionSubtype_SystemError(SystemError): pass
    >>> accept_BaseException(MyExceptionSubtype_SystemError('message'))
    >>> accept_BaseException(TypeError('message'))
    >>> class MyExceptionSubtype_TypeError(TypeError): pass
    >>> accept_BaseException(MyExceptionSubtype_TypeError('message'))
    >>> accept_BaseException(ValueError('message'))
    >>> class MyExceptionSubtype_ValueError(ValueError): pass
    >>> accept_BaseException(MyExceptionSubtype_ValueError('message'))
    >>> accept_BaseException(Warning('message'))
    >>> class MyExceptionSubtype_Warning(Warning): pass
    >>> accept_BaseException(MyExceptionSubtype_Warning('message'))
    >>> accept_BaseException(FloatingPointError('message'))
    >>> class MyExceptionSubtype_FloatingPointError(FloatingPointError): pass
    >>> accept_BaseException(MyExceptionSubtype_FloatingPointError('message'))
    >>> accept_BaseException(OverflowError('message'))
    >>> class MyExceptionSubtype_OverflowError(OverflowError): pass
    >>> accept_BaseException(MyExceptionSubtype_OverflowError('message'))
    >>> accept_BaseException(ZeroDivisionError('message'))
    >>> class MyExceptionSubtype_ZeroDivisionError(ZeroDivisionError): pass
    >>> accept_BaseException(MyExceptionSubtype_ZeroDivisionError('message'))
    >>> accept_BaseException(BytesWarning('message'))
    >>> class MyExceptionSubtype_BytesWarning(BytesWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_BytesWarning('message'))
    >>> accept_BaseException(DeprecationWarning('message'))
    >>> class MyExceptionSubtype_DeprecationWarning(DeprecationWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_DeprecationWarning('message'))
    >>> accept_BaseException(FutureWarning('message'))
    >>> class MyExceptionSubtype_FutureWarning(FutureWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_FutureWarning('message'))
    >>> accept_BaseException(ImportWarning('message'))
    >>> class MyExceptionSubtype_ImportWarning(ImportWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_ImportWarning('message'))
    >>> accept_BaseException(PendingDeprecationWarning('message'))
    >>> class MyExceptionSubtype_PendingDeprecationWarning(PendingDeprecationWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_PendingDeprecationWarning('message'))
    >>> accept_BaseException(ResourceWarning('message'))
    >>> class MyExceptionSubtype_ResourceWarning(ResourceWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_ResourceWarning('message'))
    >>> accept_BaseException(RuntimeWarning('message'))
    >>> class MyExceptionSubtype_RuntimeWarning(RuntimeWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_RuntimeWarning('message'))
    >>> accept_BaseException(SyntaxWarning('message'))
    >>> class MyExceptionSubtype_SyntaxWarning(SyntaxWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_SyntaxWarning('message'))
    >>> accept_BaseException(UnicodeWarning('message'))
    >>> class MyExceptionSubtype_UnicodeWarning(UnicodeWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_UnicodeWarning('message'))
    >>> accept_BaseException(UserWarning('message'))
    >>> class MyExceptionSubtype_UserWarning(UserWarning): pass
    >>> accept_BaseException(MyExceptionSubtype_UserWarning('message'))
    >>> accept_BaseException(BlockingIOError('message'))
    >>> class MyExceptionSubtype_BlockingIOError(BlockingIOError): pass
    >>> accept_BaseException(MyExceptionSubtype_BlockingIOError('message'))
    >>> accept_BaseException(ChildProcessError('message'))
    >>> class MyExceptionSubtype_ChildProcessError(ChildProcessError): pass
    >>> accept_BaseException(MyExceptionSubtype_ChildProcessError('message'))
    >>> accept_BaseException(ConnectionError('message'))
    >>> class MyExceptionSubtype_ConnectionError(ConnectionError): pass
    >>> accept_BaseException(MyExceptionSubtype_ConnectionError('message'))
    >>> accept_BaseException(FileExistsError('message'))
    >>> class MyExceptionSubtype_FileExistsError(FileExistsError): pass
    >>> accept_BaseException(MyExceptionSubtype_FileExistsError('message'))
    >>> accept_BaseException(FileNotFoundError('message'))
    >>> class MyExceptionSubtype_FileNotFoundError(FileNotFoundError): pass
    >>> accept_BaseException(MyExceptionSubtype_FileNotFoundError('message'))
    >>> accept_BaseException(InterruptedError('message'))
    >>> class MyExceptionSubtype_InterruptedError(InterruptedError): pass
    >>> accept_BaseException(MyExceptionSubtype_InterruptedError('message'))
    >>> accept_BaseException(IsADirectoryError('message'))
    >>> class MyExceptionSubtype_IsADirectoryError(IsADirectoryError): pass
    >>> accept_BaseException(MyExceptionSubtype_IsADirectoryError('message'))
    >>> accept_BaseException(NotADirectoryError('message'))
    >>> class MyExceptionSubtype_NotADirectoryError(NotADirectoryError): pass
    >>> accept_BaseException(MyExceptionSubtype_NotADirectoryError('message'))
    >>> accept_BaseException(PermissionError('message'))
    >>> class MyExceptionSubtype_PermissionError(PermissionError): pass
    >>> accept_BaseException(MyExceptionSubtype_PermissionError('message'))
    >>> accept_BaseException(ProcessLookupError('message'))
    >>> class MyExceptionSubtype_ProcessLookupError(ProcessLookupError): pass
    >>> accept_BaseException(MyExceptionSubtype_ProcessLookupError('message'))
    >>> accept_BaseException(TimeoutError('message'))
    >>> class MyExceptionSubtype_TimeoutError(TimeoutError): pass
    >>> accept_BaseException(MyExceptionSubtype_TimeoutError('message'))
    >>> accept_BaseException(IndentationError('message'))
    >>> class MyExceptionSubtype_IndentationError(IndentationError): pass
    >>> accept_BaseException(MyExceptionSubtype_IndentationError('message'))
    >>> accept_BaseException(IndexError('message'))
    >>> class MyExceptionSubtype_IndexError(IndexError): pass
    >>> accept_BaseException(MyExceptionSubtype_IndexError('message'))
    >>> accept_BaseException(KeyError('message'))
    >>> class MyExceptionSubtype_KeyError(KeyError): pass
    >>> accept_BaseException(MyExceptionSubtype_KeyError('message'))
    >>> accept_BaseException(ModuleNotFoundError('message'))
    >>> class MyExceptionSubtype_ModuleNotFoundError(ModuleNotFoundError): pass
    >>> accept_BaseException(MyExceptionSubtype_ModuleNotFoundError('message'))
    >>> accept_BaseException(NotImplementedError('message'))
    >>> class MyExceptionSubtype_NotImplementedError(NotImplementedError): pass
    >>> accept_BaseException(MyExceptionSubtype_NotImplementedError('message'))
    >>> accept_BaseException(RecursionError('message'))
    >>> class MyExceptionSubtype_RecursionError(RecursionError): pass
    >>> accept_BaseException(MyExceptionSubtype_RecursionError('message'))
    >>> accept_BaseException(UnboundLocalError('message'))
    >>> class MyExceptionSubtype_UnboundLocalError(UnboundLocalError): pass
    >>> accept_BaseException(MyExceptionSubtype_UnboundLocalError('message'))
    >>> accept_BaseException(UnicodeError('message'))
    >>> class MyExceptionSubtype_UnicodeError(UnicodeError): pass
    >>> accept_BaseException(MyExceptionSubtype_UnicodeError('message'))
    >>> accept_BaseException(BrokenPipeError('message'))
    >>> class MyExceptionSubtype_BrokenPipeError(BrokenPipeError): pass
    >>> accept_BaseException(MyExceptionSubtype_BrokenPipeError('message'))
    >>> accept_BaseException(ConnectionAbortedError('message'))
    >>> class MyExceptionSubtype_ConnectionAbortedError(ConnectionAbortedError): pass
    >>> accept_BaseException(MyExceptionSubtype_ConnectionAbortedError('message'))
    >>> accept_BaseException(ConnectionRefusedError('message'))
    >>> class MyExceptionSubtype_ConnectionRefusedError(ConnectionRefusedError): pass
    >>> accept_BaseException(MyExceptionSubtype_ConnectionRefusedError('message'))
    >>> accept_BaseException(ConnectionResetError('message'))
    >>> class MyExceptionSubtype_ConnectionResetError(ConnectionResetError): pass
    >>> accept_BaseException(MyExceptionSubtype_ConnectionResetError('message'))
    >>> accept_BaseException(TabError('message'))
    >>> class MyExceptionSubtype_TabError(TabError): pass
    >>> accept_BaseException(MyExceptionSubtype_TabError('message'))
    >>> accept_BaseException(EnvironmentError('message'))
    >>> class MyExceptionSubtype_EnvironmentError(EnvironmentError): pass
    >>> accept_BaseException(MyExceptionSubtype_EnvironmentError('message'))
    >>> accept_BaseException(IOError('message'))
    >>> class MyExceptionSubtype_IOError(IOError): pass
    >>> accept_BaseException(MyExceptionSubtype_IOError('message'))
    """
    exc_var: BaseException = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert BaseException in type(exc).__mro__
    assert isinstance(exc, BaseException)
    assert exc.args == ('message',)

def accept_BlockingIOError(exc: BlockingIOError):
    """
    >>> accept_BlockingIOError(BlockingIOError('message'))
    >>> class MyExceptionSubtype_BlockingIOError(BlockingIOError): pass
    >>> accept_BlockingIOError(MyExceptionSubtype_BlockingIOError('message'))
    """
    exc_var: BlockingIOError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert BlockingIOError in type(exc).__mro__
    assert isinstance(exc, BlockingIOError)
    assert exc.args == ('message',)

def accept_BrokenPipeError(exc: BrokenPipeError):
    """
    >>> accept_BrokenPipeError(BrokenPipeError('message'))
    >>> class MyExceptionSubtype_BrokenPipeError(BrokenPipeError): pass
    >>> accept_BrokenPipeError(MyExceptionSubtype_BrokenPipeError('message'))
    """
    exc_var: BrokenPipeError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert BrokenPipeError in type(exc).__mro__
    assert isinstance(exc, BrokenPipeError)
    assert exc.args == ('message',)

def accept_BufferError(exc: BufferError):
    """
    >>> accept_BufferError(BufferError('message'))
    >>> class MyExceptionSubtype_BufferError(BufferError): pass
    >>> accept_BufferError(MyExceptionSubtype_BufferError('message'))
    """
    exc_var: BufferError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert BufferError in type(exc).__mro__
    assert isinstance(exc, BufferError)
    assert exc.args == ('message',)

def accept_BytesWarning(exc: BytesWarning):
    """
    >>> accept_BytesWarning(BytesWarning('message'))
    >>> class MyExceptionSubtype_BytesWarning(BytesWarning): pass
    >>> accept_BytesWarning(MyExceptionSubtype_BytesWarning('message'))
    """
    exc_var: BytesWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert BytesWarning in type(exc).__mro__
    assert isinstance(exc, BytesWarning)
    assert exc.args == ('message',)

def accept_ChildProcessError(exc: ChildProcessError):
    """
    >>> accept_ChildProcessError(ChildProcessError('message'))
    >>> class MyExceptionSubtype_ChildProcessError(ChildProcessError): pass
    >>> accept_ChildProcessError(MyExceptionSubtype_ChildProcessError('message'))
    """
    exc_var: ChildProcessError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ChildProcessError in type(exc).__mro__
    assert isinstance(exc, ChildProcessError)
    assert exc.args == ('message',)

def accept_ConnectionAbortedError(exc: ConnectionAbortedError):
    """
    >>> accept_ConnectionAbortedError(ConnectionAbortedError('message'))
    >>> class MyExceptionSubtype_ConnectionAbortedError(ConnectionAbortedError): pass
    >>> accept_ConnectionAbortedError(MyExceptionSubtype_ConnectionAbortedError('message'))
    """
    exc_var: ConnectionAbortedError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ConnectionAbortedError in type(exc).__mro__
    assert isinstance(exc, ConnectionAbortedError)
    assert exc.args == ('message',)

def accept_ConnectionError(exc: ConnectionError):
    """
    >>> accept_ConnectionError(ConnectionError('message'))
    >>> class MyExceptionSubtype_ConnectionError(ConnectionError): pass
    >>> accept_ConnectionError(MyExceptionSubtype_ConnectionError('message'))
    >>> accept_ConnectionError(BrokenPipeError('message'))
    >>> class MyExceptionSubtype_BrokenPipeError(BrokenPipeError): pass
    >>> accept_ConnectionError(MyExceptionSubtype_BrokenPipeError('message'))
    >>> accept_ConnectionError(ConnectionAbortedError('message'))
    >>> class MyExceptionSubtype_ConnectionAbortedError(ConnectionAbortedError): pass
    >>> accept_ConnectionError(MyExceptionSubtype_ConnectionAbortedError('message'))
    >>> accept_ConnectionError(ConnectionRefusedError('message'))
    >>> class MyExceptionSubtype_ConnectionRefusedError(ConnectionRefusedError): pass
    >>> accept_ConnectionError(MyExceptionSubtype_ConnectionRefusedError('message'))
    >>> accept_ConnectionError(ConnectionResetError('message'))
    >>> class MyExceptionSubtype_ConnectionResetError(ConnectionResetError): pass
    >>> accept_ConnectionError(MyExceptionSubtype_ConnectionResetError('message'))
    """
    exc_var: ConnectionError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ConnectionError in type(exc).__mro__
    assert isinstance(exc, ConnectionError)
    assert exc.args == ('message',)

def accept_ConnectionRefusedError(exc: ConnectionRefusedError):
    """
    >>> accept_ConnectionRefusedError(ConnectionRefusedError('message'))
    >>> class MyExceptionSubtype_ConnectionRefusedError(ConnectionRefusedError): pass
    >>> accept_ConnectionRefusedError(MyExceptionSubtype_ConnectionRefusedError('message'))
    """
    exc_var: ConnectionRefusedError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ConnectionRefusedError in type(exc).__mro__
    assert isinstance(exc, ConnectionRefusedError)
    assert exc.args == ('message',)

def accept_ConnectionResetError(exc: ConnectionResetError):
    """
    >>> accept_ConnectionResetError(ConnectionResetError('message'))
    >>> class MyExceptionSubtype_ConnectionResetError(ConnectionResetError): pass
    >>> accept_ConnectionResetError(MyExceptionSubtype_ConnectionResetError('message'))
    """
    exc_var: ConnectionResetError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ConnectionResetError in type(exc).__mro__
    assert isinstance(exc, ConnectionResetError)
    assert exc.args == ('message',)

def accept_DeprecationWarning(exc: DeprecationWarning):
    """
    >>> accept_DeprecationWarning(DeprecationWarning('message'))
    >>> class MyExceptionSubtype_DeprecationWarning(DeprecationWarning): pass
    >>> accept_DeprecationWarning(MyExceptionSubtype_DeprecationWarning('message'))
    """
    exc_var: DeprecationWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert DeprecationWarning in type(exc).__mro__
    assert isinstance(exc, DeprecationWarning)
    assert exc.args == ('message',)

def accept_EOFError(exc: EOFError):
    """
    >>> accept_EOFError(EOFError('message'))
    >>> class MyExceptionSubtype_EOFError(EOFError): pass
    >>> accept_EOFError(MyExceptionSubtype_EOFError('message'))
    """
    exc_var: EOFError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert EOFError in type(exc).__mro__
    assert isinstance(exc, EOFError)
    assert exc.args == ('message',)

def accept_Exception(exc: Exception):
    """
    >>> accept_Exception(Exception('message'))
    >>> class MyExceptionSubtype_Exception(Exception): pass
    >>> accept_Exception(MyExceptionSubtype_Exception('message'))
    >>> accept_Exception(ArithmeticError('message'))
    >>> class MyExceptionSubtype_ArithmeticError(ArithmeticError): pass
    >>> accept_Exception(MyExceptionSubtype_ArithmeticError('message'))
    >>> accept_Exception(AssertionError('message'))
    >>> class MyExceptionSubtype_AssertionError(AssertionError): pass
    >>> accept_Exception(MyExceptionSubtype_AssertionError('message'))
    >>> accept_Exception(AttributeError('message'))
    >>> class MyExceptionSubtype_AttributeError(AttributeError): pass
    >>> accept_Exception(MyExceptionSubtype_AttributeError('message'))
    >>> accept_Exception(BufferError('message'))
    >>> class MyExceptionSubtype_BufferError(BufferError): pass
    >>> accept_Exception(MyExceptionSubtype_BufferError('message'))
    >>> accept_Exception(EOFError('message'))
    >>> class MyExceptionSubtype_EOFError(EOFError): pass
    >>> accept_Exception(MyExceptionSubtype_EOFError('message'))
    >>> accept_Exception(ImportError('message'))
    >>> class MyExceptionSubtype_ImportError(ImportError): pass
    >>> accept_Exception(MyExceptionSubtype_ImportError('message'))
    >>> accept_Exception(LookupError('message'))
    >>> class MyExceptionSubtype_LookupError(LookupError): pass
    >>> accept_Exception(MyExceptionSubtype_LookupError('message'))
    >>> accept_Exception(MemoryError('message'))
    >>> class MyExceptionSubtype_MemoryError(MemoryError): pass
    >>> accept_Exception(MyExceptionSubtype_MemoryError('message'))
    >>> accept_Exception(NameError('message'))
    >>> class MyExceptionSubtype_NameError(NameError): pass
    >>> accept_Exception(MyExceptionSubtype_NameError('message'))
    >>> accept_Exception(OSError('message'))
    >>> class MyExceptionSubtype_OSError(OSError): pass
    >>> accept_Exception(MyExceptionSubtype_OSError('message'))
    >>> accept_Exception(ReferenceError('message'))
    >>> class MyExceptionSubtype_ReferenceError(ReferenceError): pass
    >>> accept_Exception(MyExceptionSubtype_ReferenceError('message'))
    >>> accept_Exception(RuntimeError('message'))
    >>> class MyExceptionSubtype_RuntimeError(RuntimeError): pass
    >>> accept_Exception(MyExceptionSubtype_RuntimeError('message'))
    >>> accept_Exception(StopAsyncIteration('message'))
    >>> class MyExceptionSubtype_StopAsyncIteration(StopAsyncIteration): pass
    >>> accept_Exception(MyExceptionSubtype_StopAsyncIteration('message'))
    >>> accept_Exception(StopIteration('message'))
    >>> class MyExceptionSubtype_StopIteration(StopIteration): pass
    >>> accept_Exception(MyExceptionSubtype_StopIteration('message'))
    >>> accept_Exception(SyntaxError('message'))
    >>> class MyExceptionSubtype_SyntaxError(SyntaxError): pass
    >>> accept_Exception(MyExceptionSubtype_SyntaxError('message'))
    >>> accept_Exception(SystemError('message'))
    >>> class MyExceptionSubtype_SystemError(SystemError): pass
    >>> accept_Exception(MyExceptionSubtype_SystemError('message'))
    >>> accept_Exception(TypeError('message'))
    >>> class MyExceptionSubtype_TypeError(TypeError): pass
    >>> accept_Exception(MyExceptionSubtype_TypeError('message'))
    >>> accept_Exception(ValueError('message'))
    >>> class MyExceptionSubtype_ValueError(ValueError): pass
    >>> accept_Exception(MyExceptionSubtype_ValueError('message'))
    >>> accept_Exception(Warning('message'))
    >>> class MyExceptionSubtype_Warning(Warning): pass
    >>> accept_Exception(MyExceptionSubtype_Warning('message'))
    >>> accept_Exception(FloatingPointError('message'))
    >>> class MyExceptionSubtype_FloatingPointError(FloatingPointError): pass
    >>> accept_Exception(MyExceptionSubtype_FloatingPointError('message'))
    >>> accept_Exception(OverflowError('message'))
    >>> class MyExceptionSubtype_OverflowError(OverflowError): pass
    >>> accept_Exception(MyExceptionSubtype_OverflowError('message'))
    >>> accept_Exception(ZeroDivisionError('message'))
    >>> class MyExceptionSubtype_ZeroDivisionError(ZeroDivisionError): pass
    >>> accept_Exception(MyExceptionSubtype_ZeroDivisionError('message'))
    >>> accept_Exception(BytesWarning('message'))
    >>> class MyExceptionSubtype_BytesWarning(BytesWarning): pass
    >>> accept_Exception(MyExceptionSubtype_BytesWarning('message'))
    >>> accept_Exception(DeprecationWarning('message'))
    >>> class MyExceptionSubtype_DeprecationWarning(DeprecationWarning): pass
    >>> accept_Exception(MyExceptionSubtype_DeprecationWarning('message'))
    >>> accept_Exception(FutureWarning('message'))
    >>> class MyExceptionSubtype_FutureWarning(FutureWarning): pass
    >>> accept_Exception(MyExceptionSubtype_FutureWarning('message'))
    >>> accept_Exception(ImportWarning('message'))
    >>> class MyExceptionSubtype_ImportWarning(ImportWarning): pass
    >>> accept_Exception(MyExceptionSubtype_ImportWarning('message'))
    >>> accept_Exception(PendingDeprecationWarning('message'))
    >>> class MyExceptionSubtype_PendingDeprecationWarning(PendingDeprecationWarning): pass
    >>> accept_Exception(MyExceptionSubtype_PendingDeprecationWarning('message'))
    >>> accept_Exception(ResourceWarning('message'))
    >>> class MyExceptionSubtype_ResourceWarning(ResourceWarning): pass
    >>> accept_Exception(MyExceptionSubtype_ResourceWarning('message'))
    >>> accept_Exception(RuntimeWarning('message'))
    >>> class MyExceptionSubtype_RuntimeWarning(RuntimeWarning): pass
    >>> accept_Exception(MyExceptionSubtype_RuntimeWarning('message'))
    >>> accept_Exception(SyntaxWarning('message'))
    >>> class MyExceptionSubtype_SyntaxWarning(SyntaxWarning): pass
    >>> accept_Exception(MyExceptionSubtype_SyntaxWarning('message'))
    >>> accept_Exception(UnicodeWarning('message'))
    >>> class MyExceptionSubtype_UnicodeWarning(UnicodeWarning): pass
    >>> accept_Exception(MyExceptionSubtype_UnicodeWarning('message'))
    >>> accept_Exception(UserWarning('message'))
    >>> class MyExceptionSubtype_UserWarning(UserWarning): pass
    >>> accept_Exception(MyExceptionSubtype_UserWarning('message'))
    >>> accept_Exception(BlockingIOError('message'))
    >>> class MyExceptionSubtype_BlockingIOError(BlockingIOError): pass
    >>> accept_Exception(MyExceptionSubtype_BlockingIOError('message'))
    >>> accept_Exception(ChildProcessError('message'))
    >>> class MyExceptionSubtype_ChildProcessError(ChildProcessError): pass
    >>> accept_Exception(MyExceptionSubtype_ChildProcessError('message'))
    >>> accept_Exception(ConnectionError('message'))
    >>> class MyExceptionSubtype_ConnectionError(ConnectionError): pass
    >>> accept_Exception(MyExceptionSubtype_ConnectionError('message'))
    >>> accept_Exception(FileExistsError('message'))
    >>> class MyExceptionSubtype_FileExistsError(FileExistsError): pass
    >>> accept_Exception(MyExceptionSubtype_FileExistsError('message'))
    >>> accept_Exception(FileNotFoundError('message'))
    >>> class MyExceptionSubtype_FileNotFoundError(FileNotFoundError): pass
    >>> accept_Exception(MyExceptionSubtype_FileNotFoundError('message'))
    >>> accept_Exception(InterruptedError('message'))
    >>> class MyExceptionSubtype_InterruptedError(InterruptedError): pass
    >>> accept_Exception(MyExceptionSubtype_InterruptedError('message'))
    >>> accept_Exception(IsADirectoryError('message'))
    >>> class MyExceptionSubtype_IsADirectoryError(IsADirectoryError): pass
    >>> accept_Exception(MyExceptionSubtype_IsADirectoryError('message'))
    >>> accept_Exception(NotADirectoryError('message'))
    >>> class MyExceptionSubtype_NotADirectoryError(NotADirectoryError): pass
    >>> accept_Exception(MyExceptionSubtype_NotADirectoryError('message'))
    >>> accept_Exception(PermissionError('message'))
    >>> class MyExceptionSubtype_PermissionError(PermissionError): pass
    >>> accept_Exception(MyExceptionSubtype_PermissionError('message'))
    >>> accept_Exception(ProcessLookupError('message'))
    >>> class MyExceptionSubtype_ProcessLookupError(ProcessLookupError): pass
    >>> accept_Exception(MyExceptionSubtype_ProcessLookupError('message'))
    >>> accept_Exception(TimeoutError('message'))
    >>> class MyExceptionSubtype_TimeoutError(TimeoutError): pass
    >>> accept_Exception(MyExceptionSubtype_TimeoutError('message'))
    >>> accept_Exception(IndentationError('message'))
    >>> class MyExceptionSubtype_IndentationError(IndentationError): pass
    >>> accept_Exception(MyExceptionSubtype_IndentationError('message'))
    >>> accept_Exception(IndexError('message'))
    >>> class MyExceptionSubtype_IndexError(IndexError): pass
    >>> accept_Exception(MyExceptionSubtype_IndexError('message'))
    >>> accept_Exception(KeyError('message'))
    >>> class MyExceptionSubtype_KeyError(KeyError): pass
    >>> accept_Exception(MyExceptionSubtype_KeyError('message'))
    >>> accept_Exception(ModuleNotFoundError('message'))
    >>> class MyExceptionSubtype_ModuleNotFoundError(ModuleNotFoundError): pass
    >>> accept_Exception(MyExceptionSubtype_ModuleNotFoundError('message'))
    >>> accept_Exception(NotImplementedError('message'))
    >>> class MyExceptionSubtype_NotImplementedError(NotImplementedError): pass
    >>> accept_Exception(MyExceptionSubtype_NotImplementedError('message'))
    >>> accept_Exception(RecursionError('message'))
    >>> class MyExceptionSubtype_RecursionError(RecursionError): pass
    >>> accept_Exception(MyExceptionSubtype_RecursionError('message'))
    >>> accept_Exception(UnboundLocalError('message'))
    >>> class MyExceptionSubtype_UnboundLocalError(UnboundLocalError): pass
    >>> accept_Exception(MyExceptionSubtype_UnboundLocalError('message'))
    >>> accept_Exception(UnicodeError('message'))
    >>> class MyExceptionSubtype_UnicodeError(UnicodeError): pass
    >>> accept_Exception(MyExceptionSubtype_UnicodeError('message'))
    >>> accept_Exception(BrokenPipeError('message'))
    >>> class MyExceptionSubtype_BrokenPipeError(BrokenPipeError): pass
    >>> accept_Exception(MyExceptionSubtype_BrokenPipeError('message'))
    >>> accept_Exception(ConnectionAbortedError('message'))
    >>> class MyExceptionSubtype_ConnectionAbortedError(ConnectionAbortedError): pass
    >>> accept_Exception(MyExceptionSubtype_ConnectionAbortedError('message'))
    >>> accept_Exception(ConnectionRefusedError('message'))
    >>> class MyExceptionSubtype_ConnectionRefusedError(ConnectionRefusedError): pass
    >>> accept_Exception(MyExceptionSubtype_ConnectionRefusedError('message'))
    >>> accept_Exception(ConnectionResetError('message'))
    >>> class MyExceptionSubtype_ConnectionResetError(ConnectionResetError): pass
    >>> accept_Exception(MyExceptionSubtype_ConnectionResetError('message'))
    >>> accept_Exception(TabError('message'))
    >>> class MyExceptionSubtype_TabError(TabError): pass
    >>> accept_Exception(MyExceptionSubtype_TabError('message'))
    >>> accept_Exception(EnvironmentError('message'))
    >>> class MyExceptionSubtype_EnvironmentError(EnvironmentError): pass
    >>> accept_Exception(MyExceptionSubtype_EnvironmentError('message'))
    >>> accept_Exception(IOError('message'))
    >>> class MyExceptionSubtype_IOError(IOError): pass
    >>> accept_Exception(MyExceptionSubtype_IOError('message'))
    """
    exc_var: Exception = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert Exception in type(exc).__mro__
    assert isinstance(exc, Exception)
    assert exc.args == ('message',)

def accept_FileExistsError(exc: FileExistsError):
    """
    >>> accept_FileExistsError(FileExistsError('message'))
    >>> class MyExceptionSubtype_FileExistsError(FileExistsError): pass
    >>> accept_FileExistsError(MyExceptionSubtype_FileExistsError('message'))
    """
    exc_var: FileExistsError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert FileExistsError in type(exc).__mro__
    assert isinstance(exc, FileExistsError)
    assert exc.args == ('message',)

def accept_FileNotFoundError(exc: FileNotFoundError):
    """
    >>> accept_FileNotFoundError(FileNotFoundError('message'))
    >>> class MyExceptionSubtype_FileNotFoundError(FileNotFoundError): pass
    >>> accept_FileNotFoundError(MyExceptionSubtype_FileNotFoundError('message'))
    """
    exc_var: FileNotFoundError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert FileNotFoundError in type(exc).__mro__
    assert isinstance(exc, FileNotFoundError)
    assert exc.args == ('message',)

def accept_FloatingPointError(exc: FloatingPointError):
    """
    >>> accept_FloatingPointError(FloatingPointError('message'))
    >>> class MyExceptionSubtype_FloatingPointError(FloatingPointError): pass
    >>> accept_FloatingPointError(MyExceptionSubtype_FloatingPointError('message'))
    """
    exc_var: FloatingPointError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert FloatingPointError in type(exc).__mro__
    assert isinstance(exc, FloatingPointError)
    assert exc.args == ('message',)

def accept_FutureWarning(exc: FutureWarning):
    """
    >>> accept_FutureWarning(FutureWarning('message'))
    >>> class MyExceptionSubtype_FutureWarning(FutureWarning): pass
    >>> accept_FutureWarning(MyExceptionSubtype_FutureWarning('message'))
    """
    exc_var: FutureWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert FutureWarning in type(exc).__mro__
    assert isinstance(exc, FutureWarning)
    assert exc.args == ('message',)

def accept_GeneratorExit(exc: GeneratorExit):
    """
    >>> accept_GeneratorExit(GeneratorExit('message'))
    >>> class MyExceptionSubtype_GeneratorExit(GeneratorExit): pass
    >>> accept_GeneratorExit(MyExceptionSubtype_GeneratorExit('message'))
    """
    exc_var: GeneratorExit = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert GeneratorExit in type(exc).__mro__
    assert isinstance(exc, GeneratorExit)
    assert exc.args == ('message',)

def accept_ImportError(exc: ImportError):
    """
    >>> accept_ImportError(ImportError('message'))
    >>> class MyExceptionSubtype_ImportError(ImportError): pass
    >>> accept_ImportError(MyExceptionSubtype_ImportError('message'))
    >>> accept_ImportError(ModuleNotFoundError('message'))
    >>> class MyExceptionSubtype_ModuleNotFoundError(ModuleNotFoundError): pass
    >>> accept_ImportError(MyExceptionSubtype_ModuleNotFoundError('message'))
    """
    exc_var: ImportError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ImportError in type(exc).__mro__
    assert isinstance(exc, ImportError)
    assert exc.args == ('message',)

def accept_ImportWarning(exc: ImportWarning):
    """
    >>> accept_ImportWarning(ImportWarning('message'))
    >>> class MyExceptionSubtype_ImportWarning(ImportWarning): pass
    >>> accept_ImportWarning(MyExceptionSubtype_ImportWarning('message'))
    """
    exc_var: ImportWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ImportWarning in type(exc).__mro__
    assert isinstance(exc, ImportWarning)
    assert exc.args == ('message',)

def accept_IndentationError(exc: IndentationError):
    """
    >>> accept_IndentationError(IndentationError('message'))
    >>> class MyExceptionSubtype_IndentationError(IndentationError): pass
    >>> accept_IndentationError(MyExceptionSubtype_IndentationError('message'))
    >>> accept_IndentationError(TabError('message'))
    >>> class MyExceptionSubtype_TabError(TabError): pass
    >>> accept_IndentationError(MyExceptionSubtype_TabError('message'))
    """
    exc_var: IndentationError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert IndentationError in type(exc).__mro__
    assert isinstance(exc, IndentationError)
    assert exc.args == ('message',)

def accept_IndexError(exc: IndexError):
    """
    >>> accept_IndexError(IndexError('message'))
    >>> class MyExceptionSubtype_IndexError(IndexError): pass
    >>> accept_IndexError(MyExceptionSubtype_IndexError('message'))
    """
    exc_var: IndexError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert IndexError in type(exc).__mro__
    assert isinstance(exc, IndexError)
    assert exc.args == ('message',)

def accept_InterruptedError(exc: InterruptedError):
    """
    >>> accept_InterruptedError(InterruptedError('message'))
    >>> class MyExceptionSubtype_InterruptedError(InterruptedError): pass
    >>> accept_InterruptedError(MyExceptionSubtype_InterruptedError('message'))
    """
    exc_var: InterruptedError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert InterruptedError in type(exc).__mro__
    assert isinstance(exc, InterruptedError)
    assert exc.args == ('message',)

def accept_IsADirectoryError(exc: IsADirectoryError):
    """
    >>> accept_IsADirectoryError(IsADirectoryError('message'))
    >>> class MyExceptionSubtype_IsADirectoryError(IsADirectoryError): pass
    >>> accept_IsADirectoryError(MyExceptionSubtype_IsADirectoryError('message'))
    """
    exc_var: IsADirectoryError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert IsADirectoryError in type(exc).__mro__
    assert isinstance(exc, IsADirectoryError)
    assert exc.args == ('message',)

def accept_KeyError(exc: KeyError):
    """
    >>> accept_KeyError(KeyError('message'))
    >>> class MyExceptionSubtype_KeyError(KeyError): pass
    >>> accept_KeyError(MyExceptionSubtype_KeyError('message'))
    """
    exc_var: KeyError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert KeyError in type(exc).__mro__
    assert isinstance(exc, KeyError)
    assert exc.args == ('message',)

def accept_KeyboardInterrupt(exc: KeyboardInterrupt):
    """
    >>> accept_KeyboardInterrupt(KeyboardInterrupt('message'))
    >>> class MyExceptionSubtype_KeyboardInterrupt(KeyboardInterrupt): pass
    >>> accept_KeyboardInterrupt(MyExceptionSubtype_KeyboardInterrupt('message'))
    """
    exc_var: KeyboardInterrupt = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert KeyboardInterrupt in type(exc).__mro__
    assert isinstance(exc, KeyboardInterrupt)
    assert exc.args == ('message',)

def accept_LookupError(exc: LookupError):
    """
    >>> accept_LookupError(LookupError('message'))
    >>> class MyExceptionSubtype_LookupError(LookupError): pass
    >>> accept_LookupError(MyExceptionSubtype_LookupError('message'))
    >>> accept_LookupError(IndexError('message'))
    >>> class MyExceptionSubtype_IndexError(IndexError): pass
    >>> accept_LookupError(MyExceptionSubtype_IndexError('message'))
    >>> accept_LookupError(KeyError('message'))
    >>> class MyExceptionSubtype_KeyError(KeyError): pass
    >>> accept_LookupError(MyExceptionSubtype_KeyError('message'))
    """
    exc_var: LookupError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert LookupError in type(exc).__mro__
    assert isinstance(exc, LookupError)
    assert exc.args == ('message',)

def accept_MemoryError(exc: MemoryError):
    """
    >>> accept_MemoryError(MemoryError('message'))
    >>> class MyExceptionSubtype_MemoryError(MemoryError): pass
    >>> accept_MemoryError(MyExceptionSubtype_MemoryError('message'))
    """
    exc_var: MemoryError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert MemoryError in type(exc).__mro__
    assert isinstance(exc, MemoryError)
    assert exc.args == ('message',)

def accept_ModuleNotFoundError(exc: ModuleNotFoundError):
    """
    >>> accept_ModuleNotFoundError(ModuleNotFoundError('message'))
    >>> class MyExceptionSubtype_ModuleNotFoundError(ModuleNotFoundError): pass
    >>> accept_ModuleNotFoundError(MyExceptionSubtype_ModuleNotFoundError('message'))
    """
    exc_var: ModuleNotFoundError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ModuleNotFoundError in type(exc).__mro__
    assert isinstance(exc, ModuleNotFoundError)
    assert exc.args == ('message',)

def accept_NameError(exc: NameError):
    """
    >>> accept_NameError(NameError('message'))
    >>> class MyExceptionSubtype_NameError(NameError): pass
    >>> accept_NameError(MyExceptionSubtype_NameError('message'))
    >>> accept_NameError(UnboundLocalError('message'))
    >>> class MyExceptionSubtype_UnboundLocalError(UnboundLocalError): pass
    >>> accept_NameError(MyExceptionSubtype_UnboundLocalError('message'))
    """
    exc_var: NameError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert NameError in type(exc).__mro__
    assert isinstance(exc, NameError)
    assert exc.args == ('message',)

def accept_NotADirectoryError(exc: NotADirectoryError):
    """
    >>> accept_NotADirectoryError(NotADirectoryError('message'))
    >>> class MyExceptionSubtype_NotADirectoryError(NotADirectoryError): pass
    >>> accept_NotADirectoryError(MyExceptionSubtype_NotADirectoryError('message'))
    """
    exc_var: NotADirectoryError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert NotADirectoryError in type(exc).__mro__
    assert isinstance(exc, NotADirectoryError)
    assert exc.args == ('message',)

def accept_NotImplementedError(exc: NotImplementedError):
    """
    >>> accept_NotImplementedError(NotImplementedError('message'))
    >>> class MyExceptionSubtype_NotImplementedError(NotImplementedError): pass
    >>> accept_NotImplementedError(MyExceptionSubtype_NotImplementedError('message'))
    """
    exc_var: NotImplementedError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert NotImplementedError in type(exc).__mro__
    assert isinstance(exc, NotImplementedError)
    assert exc.args == ('message',)

def accept_OSError(exc: OSError):
    """
    >>> accept_OSError(OSError('message'))
    >>> class MyExceptionSubtype_OSError(OSError): pass
    >>> accept_OSError(MyExceptionSubtype_OSError('message'))
    >>> accept_OSError(BlockingIOError('message'))
    >>> class MyExceptionSubtype_BlockingIOError(BlockingIOError): pass
    >>> accept_OSError(MyExceptionSubtype_BlockingIOError('message'))
    >>> accept_OSError(ChildProcessError('message'))
    >>> class MyExceptionSubtype_ChildProcessError(ChildProcessError): pass
    >>> accept_OSError(MyExceptionSubtype_ChildProcessError('message'))
    >>> accept_OSError(ConnectionError('message'))
    >>> class MyExceptionSubtype_ConnectionError(ConnectionError): pass
    >>> accept_OSError(MyExceptionSubtype_ConnectionError('message'))
    >>> accept_OSError(FileExistsError('message'))
    >>> class MyExceptionSubtype_FileExistsError(FileExistsError): pass
    >>> accept_OSError(MyExceptionSubtype_FileExistsError('message'))
    >>> accept_OSError(FileNotFoundError('message'))
    >>> class MyExceptionSubtype_FileNotFoundError(FileNotFoundError): pass
    >>> accept_OSError(MyExceptionSubtype_FileNotFoundError('message'))
    >>> accept_OSError(InterruptedError('message'))
    >>> class MyExceptionSubtype_InterruptedError(InterruptedError): pass
    >>> accept_OSError(MyExceptionSubtype_InterruptedError('message'))
    >>> accept_OSError(IsADirectoryError('message'))
    >>> class MyExceptionSubtype_IsADirectoryError(IsADirectoryError): pass
    >>> accept_OSError(MyExceptionSubtype_IsADirectoryError('message'))
    >>> accept_OSError(NotADirectoryError('message'))
    >>> class MyExceptionSubtype_NotADirectoryError(NotADirectoryError): pass
    >>> accept_OSError(MyExceptionSubtype_NotADirectoryError('message'))
    >>> accept_OSError(PermissionError('message'))
    >>> class MyExceptionSubtype_PermissionError(PermissionError): pass
    >>> accept_OSError(MyExceptionSubtype_PermissionError('message'))
    >>> accept_OSError(ProcessLookupError('message'))
    >>> class MyExceptionSubtype_ProcessLookupError(ProcessLookupError): pass
    >>> accept_OSError(MyExceptionSubtype_ProcessLookupError('message'))
    >>> accept_OSError(TimeoutError('message'))
    >>> class MyExceptionSubtype_TimeoutError(TimeoutError): pass
    >>> accept_OSError(MyExceptionSubtype_TimeoutError('message'))
    >>> accept_OSError(BrokenPipeError('message'))
    >>> class MyExceptionSubtype_BrokenPipeError(BrokenPipeError): pass
    >>> accept_OSError(MyExceptionSubtype_BrokenPipeError('message'))
    >>> accept_OSError(ConnectionAbortedError('message'))
    >>> class MyExceptionSubtype_ConnectionAbortedError(ConnectionAbortedError): pass
    >>> accept_OSError(MyExceptionSubtype_ConnectionAbortedError('message'))
    >>> accept_OSError(ConnectionRefusedError('message'))
    >>> class MyExceptionSubtype_ConnectionRefusedError(ConnectionRefusedError): pass
    >>> accept_OSError(MyExceptionSubtype_ConnectionRefusedError('message'))
    >>> accept_OSError(ConnectionResetError('message'))
    >>> class MyExceptionSubtype_ConnectionResetError(ConnectionResetError): pass
    >>> accept_OSError(MyExceptionSubtype_ConnectionResetError('message'))
    >>> accept_OSError(EnvironmentError('message'))
    >>> class MyExceptionSubtype_EnvironmentError(EnvironmentError): pass
    >>> accept_OSError(MyExceptionSubtype_EnvironmentError('message'))
    >>> accept_OSError(IOError('message'))
    >>> class MyExceptionSubtype_IOError(IOError): pass
    >>> accept_OSError(MyExceptionSubtype_IOError('message'))
    """
    exc_var: OSError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert OSError in type(exc).__mro__
    assert isinstance(exc, OSError)
    assert exc.args == ('message',)

def accept_OverflowError(exc: OverflowError):
    """
    >>> accept_OverflowError(OverflowError('message'))
    >>> class MyExceptionSubtype_OverflowError(OverflowError): pass
    >>> accept_OverflowError(MyExceptionSubtype_OverflowError('message'))
    """
    exc_var: OverflowError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert OverflowError in type(exc).__mro__
    assert isinstance(exc, OverflowError)
    assert exc.args == ('message',)

def accept_PendingDeprecationWarning(exc: PendingDeprecationWarning):
    """
    >>> accept_PendingDeprecationWarning(PendingDeprecationWarning('message'))
    >>> class MyExceptionSubtype_PendingDeprecationWarning(PendingDeprecationWarning): pass
    >>> accept_PendingDeprecationWarning(MyExceptionSubtype_PendingDeprecationWarning('message'))
    """
    exc_var: PendingDeprecationWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert PendingDeprecationWarning in type(exc).__mro__
    assert isinstance(exc, PendingDeprecationWarning)
    assert exc.args == ('message',)

def accept_PermissionError(exc: PermissionError):
    """
    >>> accept_PermissionError(PermissionError('message'))
    >>> class MyExceptionSubtype_PermissionError(PermissionError): pass
    >>> accept_PermissionError(MyExceptionSubtype_PermissionError('message'))
    """
    exc_var: PermissionError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert PermissionError in type(exc).__mro__
    assert isinstance(exc, PermissionError)
    assert exc.args == ('message',)

def accept_ProcessLookupError(exc: ProcessLookupError):
    """
    >>> accept_ProcessLookupError(ProcessLookupError('message'))
    >>> class MyExceptionSubtype_ProcessLookupError(ProcessLookupError): pass
    >>> accept_ProcessLookupError(MyExceptionSubtype_ProcessLookupError('message'))
    """
    exc_var: ProcessLookupError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ProcessLookupError in type(exc).__mro__
    assert isinstance(exc, ProcessLookupError)
    assert exc.args == ('message',)

def accept_RecursionError(exc: RecursionError):
    """
    >>> accept_RecursionError(RecursionError('message'))
    >>> class MyExceptionSubtype_RecursionError(RecursionError): pass
    >>> accept_RecursionError(MyExceptionSubtype_RecursionError('message'))
    """
    exc_var: RecursionError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert RecursionError in type(exc).__mro__
    assert isinstance(exc, RecursionError)
    assert exc.args == ('message',)

def accept_ReferenceError(exc: ReferenceError):
    """
    >>> accept_ReferenceError(ReferenceError('message'))
    >>> class MyExceptionSubtype_ReferenceError(ReferenceError): pass
    >>> accept_ReferenceError(MyExceptionSubtype_ReferenceError('message'))
    """
    exc_var: ReferenceError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ReferenceError in type(exc).__mro__
    assert isinstance(exc, ReferenceError)
    assert exc.args == ('message',)

def accept_ResourceWarning(exc: ResourceWarning):
    """
    >>> accept_ResourceWarning(ResourceWarning('message'))
    >>> class MyExceptionSubtype_ResourceWarning(ResourceWarning): pass
    >>> accept_ResourceWarning(MyExceptionSubtype_ResourceWarning('message'))
    """
    exc_var: ResourceWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ResourceWarning in type(exc).__mro__
    assert isinstance(exc, ResourceWarning)
    assert exc.args == ('message',)

def accept_RuntimeError(exc: RuntimeError):
    """
    >>> accept_RuntimeError(RuntimeError('message'))
    >>> class MyExceptionSubtype_RuntimeError(RuntimeError): pass
    >>> accept_RuntimeError(MyExceptionSubtype_RuntimeError('message'))
    >>> accept_RuntimeError(NotImplementedError('message'))
    >>> class MyExceptionSubtype_NotImplementedError(NotImplementedError): pass
    >>> accept_RuntimeError(MyExceptionSubtype_NotImplementedError('message'))
    >>> accept_RuntimeError(RecursionError('message'))
    >>> class MyExceptionSubtype_RecursionError(RecursionError): pass
    >>> accept_RuntimeError(MyExceptionSubtype_RecursionError('message'))
    """
    exc_var: RuntimeError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert RuntimeError in type(exc).__mro__
    assert isinstance(exc, RuntimeError)
    assert exc.args == ('message',)

def accept_RuntimeWarning(exc: RuntimeWarning):
    """
    >>> accept_RuntimeWarning(RuntimeWarning('message'))
    >>> class MyExceptionSubtype_RuntimeWarning(RuntimeWarning): pass
    >>> accept_RuntimeWarning(MyExceptionSubtype_RuntimeWarning('message'))
    """
    exc_var: RuntimeWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert RuntimeWarning in type(exc).__mro__
    assert isinstance(exc, RuntimeWarning)
    assert exc.args == ('message',)

def accept_StopAsyncIteration(exc: StopAsyncIteration):
    """
    >>> accept_StopAsyncIteration(StopAsyncIteration('message'))
    >>> class MyExceptionSubtype_StopAsyncIteration(StopAsyncIteration): pass
    >>> accept_StopAsyncIteration(MyExceptionSubtype_StopAsyncIteration('message'))
    """
    exc_var: StopAsyncIteration = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert StopAsyncIteration in type(exc).__mro__
    assert isinstance(exc, StopAsyncIteration)
    assert exc.args == ('message',)

def accept_StopIteration(exc: StopIteration):
    """
    >>> accept_StopIteration(StopIteration('message'))
    >>> class MyExceptionSubtype_StopIteration(StopIteration): pass
    >>> accept_StopIteration(MyExceptionSubtype_StopIteration('message'))
    """
    exc_var: StopIteration = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert StopIteration in type(exc).__mro__
    assert isinstance(exc, StopIteration)
    assert exc.args == ('message',)

def accept_SyntaxError(exc: SyntaxError):
    """
    >>> accept_SyntaxError(SyntaxError('message'))
    >>> class MyExceptionSubtype_SyntaxError(SyntaxError): pass
    >>> accept_SyntaxError(MyExceptionSubtype_SyntaxError('message'))
    >>> accept_SyntaxError(IndentationError('message'))
    >>> class MyExceptionSubtype_IndentationError(IndentationError): pass
    >>> accept_SyntaxError(MyExceptionSubtype_IndentationError('message'))
    >>> accept_SyntaxError(TabError('message'))
    >>> class MyExceptionSubtype_TabError(TabError): pass
    >>> accept_SyntaxError(MyExceptionSubtype_TabError('message'))
    """
    exc_var: SyntaxError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert SyntaxError in type(exc).__mro__
    assert isinstance(exc, SyntaxError)
    assert exc.args == ('message',)

def accept_SyntaxWarning(exc: SyntaxWarning):
    """
    >>> accept_SyntaxWarning(SyntaxWarning('message'))
    >>> class MyExceptionSubtype_SyntaxWarning(SyntaxWarning): pass
    >>> accept_SyntaxWarning(MyExceptionSubtype_SyntaxWarning('message'))
    """
    exc_var: SyntaxWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert SyntaxWarning in type(exc).__mro__
    assert isinstance(exc, SyntaxWarning)
    assert exc.args == ('message',)

def accept_SystemError(exc: SystemError):
    """
    >>> accept_SystemError(SystemError('message'))
    >>> class MyExceptionSubtype_SystemError(SystemError): pass
    >>> accept_SystemError(MyExceptionSubtype_SystemError('message'))
    """
    exc_var: SystemError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert SystemError in type(exc).__mro__
    assert isinstance(exc, SystemError)
    assert exc.args == ('message',)

def accept_SystemExit(exc: SystemExit):
    """
    >>> accept_SystemExit(SystemExit('message'))
    >>> class MyExceptionSubtype_SystemExit(SystemExit): pass
    >>> accept_SystemExit(MyExceptionSubtype_SystemExit('message'))
    """
    exc_var: SystemExit = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert SystemExit in type(exc).__mro__
    assert isinstance(exc, SystemExit)
    assert exc.args == ('message',)

def accept_TabError(exc: TabError):
    """
    >>> accept_TabError(TabError('message'))
    >>> class MyExceptionSubtype_TabError(TabError): pass
    >>> accept_TabError(MyExceptionSubtype_TabError('message'))
    """
    exc_var: TabError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert TabError in type(exc).__mro__
    assert isinstance(exc, TabError)
    assert exc.args == ('message',)

def accept_TimeoutError(exc: TimeoutError):
    """
    >>> accept_TimeoutError(TimeoutError('message'))
    >>> class MyExceptionSubtype_TimeoutError(TimeoutError): pass
    >>> accept_TimeoutError(MyExceptionSubtype_TimeoutError('message'))
    """
    exc_var: TimeoutError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert TimeoutError in type(exc).__mro__
    assert isinstance(exc, TimeoutError)
    assert exc.args == ('message',)

def accept_TypeError(exc: TypeError):
    """
    >>> accept_TypeError(TypeError('message'))
    >>> class MyExceptionSubtype_TypeError(TypeError): pass
    >>> accept_TypeError(MyExceptionSubtype_TypeError('message'))
    """
    exc_var: TypeError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert TypeError in type(exc).__mro__
    assert isinstance(exc, TypeError)
    assert exc.args == ('message',)

def accept_UnboundLocalError(exc: UnboundLocalError):
    """
    >>> accept_UnboundLocalError(UnboundLocalError('message'))
    >>> class MyExceptionSubtype_UnboundLocalError(UnboundLocalError): pass
    >>> accept_UnboundLocalError(MyExceptionSubtype_UnboundLocalError('message'))
    """
    exc_var: UnboundLocalError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert UnboundLocalError in type(exc).__mro__
    assert isinstance(exc, UnboundLocalError)
    assert exc.args == ('message',)

def accept_UnicodeError(exc: UnicodeError):
    """
    >>> accept_UnicodeError(UnicodeError('message'))
    >>> class MyExceptionSubtype_UnicodeError(UnicodeError): pass
    >>> accept_UnicodeError(MyExceptionSubtype_UnicodeError('message'))
    """
    exc_var: UnicodeError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert UnicodeError in type(exc).__mro__
    assert isinstance(exc, UnicodeError)
    assert exc.args == ('message',)

def accept_UnicodeWarning(exc: UnicodeWarning):
    """
    >>> accept_UnicodeWarning(UnicodeWarning('message'))
    >>> class MyExceptionSubtype_UnicodeWarning(UnicodeWarning): pass
    >>> accept_UnicodeWarning(MyExceptionSubtype_UnicodeWarning('message'))
    """
    exc_var: UnicodeWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert UnicodeWarning in type(exc).__mro__
    assert isinstance(exc, UnicodeWarning)
    assert exc.args == ('message',)

def accept_UserWarning(exc: UserWarning):
    """
    >>> accept_UserWarning(UserWarning('message'))
    >>> class MyExceptionSubtype_UserWarning(UserWarning): pass
    >>> accept_UserWarning(MyExceptionSubtype_UserWarning('message'))
    """
    exc_var: UserWarning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert UserWarning in type(exc).__mro__
    assert isinstance(exc, UserWarning)
    assert exc.args == ('message',)

def accept_ValueError(exc: ValueError):
    """
    >>> accept_ValueError(ValueError('message'))
    >>> class MyExceptionSubtype_ValueError(ValueError): pass
    >>> accept_ValueError(MyExceptionSubtype_ValueError('message'))
    >>> accept_ValueError(UnicodeError('message'))
    >>> class MyExceptionSubtype_UnicodeError(UnicodeError): pass
    >>> accept_ValueError(MyExceptionSubtype_UnicodeError('message'))
    """
    exc_var: ValueError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ValueError in type(exc).__mro__
    assert isinstance(exc, ValueError)
    assert exc.args == ('message',)

def accept_Warning(exc: Warning):
    """
    >>> accept_Warning(Warning('message'))
    >>> class MyExceptionSubtype_Warning(Warning): pass
    >>> accept_Warning(MyExceptionSubtype_Warning('message'))
    >>> accept_Warning(BytesWarning('message'))
    >>> class MyExceptionSubtype_BytesWarning(BytesWarning): pass
    >>> accept_Warning(MyExceptionSubtype_BytesWarning('message'))
    >>> accept_Warning(DeprecationWarning('message'))
    >>> class MyExceptionSubtype_DeprecationWarning(DeprecationWarning): pass
    >>> accept_Warning(MyExceptionSubtype_DeprecationWarning('message'))
    >>> accept_Warning(FutureWarning('message'))
    >>> class MyExceptionSubtype_FutureWarning(FutureWarning): pass
    >>> accept_Warning(MyExceptionSubtype_FutureWarning('message'))
    >>> accept_Warning(ImportWarning('message'))
    >>> class MyExceptionSubtype_ImportWarning(ImportWarning): pass
    >>> accept_Warning(MyExceptionSubtype_ImportWarning('message'))
    >>> accept_Warning(PendingDeprecationWarning('message'))
    >>> class MyExceptionSubtype_PendingDeprecationWarning(PendingDeprecationWarning): pass
    >>> accept_Warning(MyExceptionSubtype_PendingDeprecationWarning('message'))
    >>> accept_Warning(ResourceWarning('message'))
    >>> class MyExceptionSubtype_ResourceWarning(ResourceWarning): pass
    >>> accept_Warning(MyExceptionSubtype_ResourceWarning('message'))
    >>> accept_Warning(RuntimeWarning('message'))
    >>> class MyExceptionSubtype_RuntimeWarning(RuntimeWarning): pass
    >>> accept_Warning(MyExceptionSubtype_RuntimeWarning('message'))
    >>> accept_Warning(SyntaxWarning('message'))
    >>> class MyExceptionSubtype_SyntaxWarning(SyntaxWarning): pass
    >>> accept_Warning(MyExceptionSubtype_SyntaxWarning('message'))
    >>> accept_Warning(UnicodeWarning('message'))
    >>> class MyExceptionSubtype_UnicodeWarning(UnicodeWarning): pass
    >>> accept_Warning(MyExceptionSubtype_UnicodeWarning('message'))
    >>> accept_Warning(UserWarning('message'))
    >>> class MyExceptionSubtype_UserWarning(UserWarning): pass
    >>> accept_Warning(MyExceptionSubtype_UserWarning('message'))
    """
    exc_var: Warning = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert Warning in type(exc).__mro__
    assert isinstance(exc, Warning)
    assert exc.args == ('message',)

def accept_ZeroDivisionError(exc: ZeroDivisionError):
    """
    >>> accept_ZeroDivisionError(ZeroDivisionError('message'))
    >>> class MyExceptionSubtype_ZeroDivisionError(ZeroDivisionError): pass
    >>> accept_ZeroDivisionError(MyExceptionSubtype_ZeroDivisionError('message'))
    """
    exc_var: ZeroDivisionError = {exc}.pop()
    assert isinstance(exc, BaseException)
    assert ZeroDivisionError in type(exc).__mro__
    assert isinstance(exc, ZeroDivisionError)
    assert exc.args == ('message',)

##### END GENERATED TESTS


if __name__ == '__main__':
    gen_tests()
