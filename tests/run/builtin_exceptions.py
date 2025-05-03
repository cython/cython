# mode: run
# tag: exception


NEWER_EXCEPTIONS = {
    'PythonFinalizationError': (3, 10),
    'ExceptionGroup': (3, 11),
    'BaseExceptionGroup': (3, 11),
    'PythonFinalizationError': (3, 13),
}

CALL_ARGS = {
    'UnicodeError'
}

def _type_name(obj):
    return type(obj).__name__


def gen_tests():
    import builtins
    from collections import defaultdict

    with open(__file__, encoding='utf8') as test_file:
        test_code = test_file.readlines()

    # Note: the following strings must not contain the marker lines!
    original_end_code = test_code[test_code.index("##### " + "END GENERATED TESTS\n"):]
    del test_code[test_code.index("##### " + "BEGIN GENERATED TESTS\n") + 1:]

    subclasses = defaultdict(list)
    for exc_name, exc_type in vars(builtins).items():
        if not isinstance(exc_type, type) or not issubclass(exc_type, BaseException):
            continue
        if exc_name in NEWER_EXCEPTIONS:
            continue
        try:
            exc_type()
        except TypeError:
            # Needs arguments - ignore.
            continue
        for base_type in exc_type.__mro__:
            subclasses[base_type.__name__].append(exc_name)
            if base_type.__name__ == 'BaseException':
                break

    for exc_name, subclass_names in sorted(subclasses.items()):
        test_code.append("\n")
        test_code.append(f"def accept_{exc_name}(exc: {exc_name}):\n")

        func_code = []
        func_code.append('"""')
        for subclass_name in subclass_names:
            func_code.append(f">>> accept_{exc_name}({subclass_name}())")
        func_code.append('"""')
        func_code.append(f"assert isinstance(exc, BaseException)")
        func_code.append(f"assert {exc_name} in type(exc).__mro__")
        func_code.append(f"assert isinstance(exc, {exc_name})")

        # indent and insert
        test_code.extend(f"    {line}\n" for line in func_code)

    test_code.append("\n")
    test_code += original_end_code
    test_code_str = ''.join(test_code)

    with open(__file__, encoding='utf8', mode='w') as test_file:
        test_file.write(test_code_str)

##### BEGIN GENERATED TESTS

def accept_ArithmeticError(exc: ArithmeticError):
    """
    >>> accept_ArithmeticError(ArithmeticError())
    >>> accept_ArithmeticError(FloatingPointError())
    >>> accept_ArithmeticError(OverflowError())
    >>> accept_ArithmeticError(ZeroDivisionError())
    """
    assert isinstance(exc, BaseException)
    assert ArithmeticError in type(exc).__mro__
    assert isinstance(exc, ArithmeticError)

def accept_AssertionError(exc: AssertionError):
    """
    >>> accept_AssertionError(AssertionError())
    """
    assert isinstance(exc, BaseException)
    assert AssertionError in type(exc).__mro__
    assert isinstance(exc, AssertionError)

def accept_AttributeError(exc: AttributeError):
    """
    >>> accept_AttributeError(AttributeError())
    """
    assert isinstance(exc, BaseException)
    assert AttributeError in type(exc).__mro__
    assert isinstance(exc, AttributeError)

def accept_BaseException(exc: BaseException):
    """
    >>> accept_BaseException(BaseException())
    >>> accept_BaseException(Exception())
    >>> accept_BaseException(GeneratorExit())
    >>> accept_BaseException(KeyboardInterrupt())
    >>> accept_BaseException(SystemExit())
    >>> accept_BaseException(ArithmeticError())
    >>> accept_BaseException(AssertionError())
    >>> accept_BaseException(AttributeError())
    >>> accept_BaseException(BufferError())
    >>> accept_BaseException(EOFError())
    >>> accept_BaseException(ImportError())
    >>> accept_BaseException(LookupError())
    >>> accept_BaseException(MemoryError())
    >>> accept_BaseException(NameError())
    >>> accept_BaseException(OSError())
    >>> accept_BaseException(ReferenceError())
    >>> accept_BaseException(RuntimeError())
    >>> accept_BaseException(StopAsyncIteration())
    >>> accept_BaseException(StopIteration())
    >>> accept_BaseException(SyntaxError())
    >>> accept_BaseException(SystemError())
    >>> accept_BaseException(TypeError())
    >>> accept_BaseException(ValueError())
    >>> accept_BaseException(Warning())
    >>> accept_BaseException(FloatingPointError())
    >>> accept_BaseException(OverflowError())
    >>> accept_BaseException(ZeroDivisionError())
    >>> accept_BaseException(BytesWarning())
    >>> accept_BaseException(DeprecationWarning())
    >>> accept_BaseException(EncodingWarning())
    >>> accept_BaseException(FutureWarning())
    >>> accept_BaseException(ImportWarning())
    >>> accept_BaseException(PendingDeprecationWarning())
    >>> accept_BaseException(ResourceWarning())
    >>> accept_BaseException(RuntimeWarning())
    >>> accept_BaseException(SyntaxWarning())
    >>> accept_BaseException(UnicodeWarning())
    >>> accept_BaseException(UserWarning())
    >>> accept_BaseException(BlockingIOError())
    >>> accept_BaseException(ChildProcessError())
    >>> accept_BaseException(ConnectionError())
    >>> accept_BaseException(FileExistsError())
    >>> accept_BaseException(FileNotFoundError())
    >>> accept_BaseException(InterruptedError())
    >>> accept_BaseException(IsADirectoryError())
    >>> accept_BaseException(NotADirectoryError())
    >>> accept_BaseException(PermissionError())
    >>> accept_BaseException(ProcessLookupError())
    >>> accept_BaseException(TimeoutError())
    >>> accept_BaseException(IndentationError())
    >>> accept_BaseException(IndexError())
    >>> accept_BaseException(KeyError())
    >>> accept_BaseException(ModuleNotFoundError())
    >>> accept_BaseException(NotImplementedError())
    >>> accept_BaseException(RecursionError())
    >>> accept_BaseException(UnboundLocalError())
    >>> accept_BaseException(UnicodeError())
    >>> accept_BaseException(BrokenPipeError())
    >>> accept_BaseException(ConnectionAbortedError())
    >>> accept_BaseException(ConnectionRefusedError())
    >>> accept_BaseException(ConnectionResetError())
    >>> accept_BaseException(TabError())
    >>> accept_BaseException(EnvironmentError())
    >>> accept_BaseException(IOError())
    """
    assert isinstance(exc, BaseException)
    assert BaseException in type(exc).__mro__
    assert isinstance(exc, BaseException)

def accept_BlockingIOError(exc: BlockingIOError):
    """
    >>> accept_BlockingIOError(BlockingIOError())
    """
    assert isinstance(exc, BaseException)
    assert BlockingIOError in type(exc).__mro__
    assert isinstance(exc, BlockingIOError)

def accept_BrokenPipeError(exc: BrokenPipeError):
    """
    >>> accept_BrokenPipeError(BrokenPipeError())
    """
    assert isinstance(exc, BaseException)
    assert BrokenPipeError in type(exc).__mro__
    assert isinstance(exc, BrokenPipeError)

def accept_BufferError(exc: BufferError):
    """
    >>> accept_BufferError(BufferError())
    """
    assert isinstance(exc, BaseException)
    assert BufferError in type(exc).__mro__
    assert isinstance(exc, BufferError)

def accept_BytesWarning(exc: BytesWarning):
    """
    >>> accept_BytesWarning(BytesWarning())
    """
    assert isinstance(exc, BaseException)
    assert BytesWarning in type(exc).__mro__
    assert isinstance(exc, BytesWarning)

def accept_ChildProcessError(exc: ChildProcessError):
    """
    >>> accept_ChildProcessError(ChildProcessError())
    """
    assert isinstance(exc, BaseException)
    assert ChildProcessError in type(exc).__mro__
    assert isinstance(exc, ChildProcessError)

def accept_ConnectionAbortedError(exc: ConnectionAbortedError):
    """
    >>> accept_ConnectionAbortedError(ConnectionAbortedError())
    """
    assert isinstance(exc, BaseException)
    assert ConnectionAbortedError in type(exc).__mro__
    assert isinstance(exc, ConnectionAbortedError)

def accept_ConnectionError(exc: ConnectionError):
    """
    >>> accept_ConnectionError(ConnectionError())
    >>> accept_ConnectionError(BrokenPipeError())
    >>> accept_ConnectionError(ConnectionAbortedError())
    >>> accept_ConnectionError(ConnectionRefusedError())
    >>> accept_ConnectionError(ConnectionResetError())
    """
    assert isinstance(exc, BaseException)
    assert ConnectionError in type(exc).__mro__
    assert isinstance(exc, ConnectionError)

def accept_ConnectionRefusedError(exc: ConnectionRefusedError):
    """
    >>> accept_ConnectionRefusedError(ConnectionRefusedError())
    """
    assert isinstance(exc, BaseException)
    assert ConnectionRefusedError in type(exc).__mro__
    assert isinstance(exc, ConnectionRefusedError)

def accept_ConnectionResetError(exc: ConnectionResetError):
    """
    >>> accept_ConnectionResetError(ConnectionResetError())
    """
    assert isinstance(exc, BaseException)
    assert ConnectionResetError in type(exc).__mro__
    assert isinstance(exc, ConnectionResetError)

def accept_DeprecationWarning(exc: DeprecationWarning):
    """
    >>> accept_DeprecationWarning(DeprecationWarning())
    """
    assert isinstance(exc, BaseException)
    assert DeprecationWarning in type(exc).__mro__
    assert isinstance(exc, DeprecationWarning)

def accept_EOFError(exc: EOFError):
    """
    >>> accept_EOFError(EOFError())
    """
    assert isinstance(exc, BaseException)
    assert EOFError in type(exc).__mro__
    assert isinstance(exc, EOFError)

def accept_EncodingWarning(exc: EncodingWarning):
    """
    >>> accept_EncodingWarning(EncodingWarning())
    """
    assert isinstance(exc, BaseException)
    assert EncodingWarning in type(exc).__mro__
    assert isinstance(exc, EncodingWarning)

def accept_Exception(exc: Exception):
    """
    >>> accept_Exception(Exception())
    >>> accept_Exception(ArithmeticError())
    >>> accept_Exception(AssertionError())
    >>> accept_Exception(AttributeError())
    >>> accept_Exception(BufferError())
    >>> accept_Exception(EOFError())
    >>> accept_Exception(ImportError())
    >>> accept_Exception(LookupError())
    >>> accept_Exception(MemoryError())
    >>> accept_Exception(NameError())
    >>> accept_Exception(OSError())
    >>> accept_Exception(ReferenceError())
    >>> accept_Exception(RuntimeError())
    >>> accept_Exception(StopAsyncIteration())
    >>> accept_Exception(StopIteration())
    >>> accept_Exception(SyntaxError())
    >>> accept_Exception(SystemError())
    >>> accept_Exception(TypeError())
    >>> accept_Exception(ValueError())
    >>> accept_Exception(Warning())
    >>> accept_Exception(FloatingPointError())
    >>> accept_Exception(OverflowError())
    >>> accept_Exception(ZeroDivisionError())
    >>> accept_Exception(BytesWarning())
    >>> accept_Exception(DeprecationWarning())
    >>> accept_Exception(EncodingWarning())
    >>> accept_Exception(FutureWarning())
    >>> accept_Exception(ImportWarning())
    >>> accept_Exception(PendingDeprecationWarning())
    >>> accept_Exception(ResourceWarning())
    >>> accept_Exception(RuntimeWarning())
    >>> accept_Exception(SyntaxWarning())
    >>> accept_Exception(UnicodeWarning())
    >>> accept_Exception(UserWarning())
    >>> accept_Exception(BlockingIOError())
    >>> accept_Exception(ChildProcessError())
    >>> accept_Exception(ConnectionError())
    >>> accept_Exception(FileExistsError())
    >>> accept_Exception(FileNotFoundError())
    >>> accept_Exception(InterruptedError())
    >>> accept_Exception(IsADirectoryError())
    >>> accept_Exception(NotADirectoryError())
    >>> accept_Exception(PermissionError())
    >>> accept_Exception(ProcessLookupError())
    >>> accept_Exception(TimeoutError())
    >>> accept_Exception(IndentationError())
    >>> accept_Exception(IndexError())
    >>> accept_Exception(KeyError())
    >>> accept_Exception(ModuleNotFoundError())
    >>> accept_Exception(NotImplementedError())
    >>> accept_Exception(RecursionError())
    >>> accept_Exception(UnboundLocalError())
    >>> accept_Exception(UnicodeError())
    >>> accept_Exception(BrokenPipeError())
    >>> accept_Exception(ConnectionAbortedError())
    >>> accept_Exception(ConnectionRefusedError())
    >>> accept_Exception(ConnectionResetError())
    >>> accept_Exception(TabError())
    >>> accept_Exception(EnvironmentError())
    >>> accept_Exception(IOError())
    """
    assert isinstance(exc, BaseException)
    assert Exception in type(exc).__mro__
    assert isinstance(exc, Exception)

def accept_FileExistsError(exc: FileExistsError):
    """
    >>> accept_FileExistsError(FileExistsError())
    """
    assert isinstance(exc, BaseException)
    assert FileExistsError in type(exc).__mro__
    assert isinstance(exc, FileExistsError)

def accept_FileNotFoundError(exc: FileNotFoundError):
    """
    >>> accept_FileNotFoundError(FileNotFoundError())
    """
    assert isinstance(exc, BaseException)
    assert FileNotFoundError in type(exc).__mro__
    assert isinstance(exc, FileNotFoundError)

def accept_FloatingPointError(exc: FloatingPointError):
    """
    >>> accept_FloatingPointError(FloatingPointError())
    """
    assert isinstance(exc, BaseException)
    assert FloatingPointError in type(exc).__mro__
    assert isinstance(exc, FloatingPointError)

def accept_FutureWarning(exc: FutureWarning):
    """
    >>> accept_FutureWarning(FutureWarning())
    """
    assert isinstance(exc, BaseException)
    assert FutureWarning in type(exc).__mro__
    assert isinstance(exc, FutureWarning)

def accept_GeneratorExit(exc: GeneratorExit):
    """
    >>> accept_GeneratorExit(GeneratorExit())
    """
    assert isinstance(exc, BaseException)
    assert GeneratorExit in type(exc).__mro__
    assert isinstance(exc, GeneratorExit)

def accept_ImportError(exc: ImportError):
    """
    >>> accept_ImportError(ImportError())
    >>> accept_ImportError(ModuleNotFoundError())
    """
    assert isinstance(exc, BaseException)
    assert ImportError in type(exc).__mro__
    assert isinstance(exc, ImportError)

def accept_ImportWarning(exc: ImportWarning):
    """
    >>> accept_ImportWarning(ImportWarning())
    """
    assert isinstance(exc, BaseException)
    assert ImportWarning in type(exc).__mro__
    assert isinstance(exc, ImportWarning)

def accept_IndentationError(exc: IndentationError):
    """
    >>> accept_IndentationError(IndentationError())
    >>> accept_IndentationError(TabError())
    """
    assert isinstance(exc, BaseException)
    assert IndentationError in type(exc).__mro__
    assert isinstance(exc, IndentationError)

def accept_IndexError(exc: IndexError):
    """
    >>> accept_IndexError(IndexError())
    """
    assert isinstance(exc, BaseException)
    assert IndexError in type(exc).__mro__
    assert isinstance(exc, IndexError)

def accept_InterruptedError(exc: InterruptedError):
    """
    >>> accept_InterruptedError(InterruptedError())
    """
    assert isinstance(exc, BaseException)
    assert InterruptedError in type(exc).__mro__
    assert isinstance(exc, InterruptedError)

def accept_IsADirectoryError(exc: IsADirectoryError):
    """
    >>> accept_IsADirectoryError(IsADirectoryError())
    """
    assert isinstance(exc, BaseException)
    assert IsADirectoryError in type(exc).__mro__
    assert isinstance(exc, IsADirectoryError)

def accept_KeyError(exc: KeyError):
    """
    >>> accept_KeyError(KeyError())
    """
    assert isinstance(exc, BaseException)
    assert KeyError in type(exc).__mro__
    assert isinstance(exc, KeyError)

def accept_KeyboardInterrupt(exc: KeyboardInterrupt):
    """
    >>> accept_KeyboardInterrupt(KeyboardInterrupt())
    """
    assert isinstance(exc, BaseException)
    assert KeyboardInterrupt in type(exc).__mro__
    assert isinstance(exc, KeyboardInterrupt)

def accept_LookupError(exc: LookupError):
    """
    >>> accept_LookupError(LookupError())
    >>> accept_LookupError(IndexError())
    >>> accept_LookupError(KeyError())
    """
    assert isinstance(exc, BaseException)
    assert LookupError in type(exc).__mro__
    assert isinstance(exc, LookupError)

def accept_MemoryError(exc: MemoryError):
    """
    >>> accept_MemoryError(MemoryError())
    """
    assert isinstance(exc, BaseException)
    assert MemoryError in type(exc).__mro__
    assert isinstance(exc, MemoryError)

def accept_ModuleNotFoundError(exc: ModuleNotFoundError):
    """
    >>> accept_ModuleNotFoundError(ModuleNotFoundError())
    """
    assert isinstance(exc, BaseException)
    assert ModuleNotFoundError in type(exc).__mro__
    assert isinstance(exc, ModuleNotFoundError)

def accept_NameError(exc: NameError):
    """
    >>> accept_NameError(NameError())
    >>> accept_NameError(UnboundLocalError())
    """
    assert isinstance(exc, BaseException)
    assert NameError in type(exc).__mro__
    assert isinstance(exc, NameError)

def accept_NotADirectoryError(exc: NotADirectoryError):
    """
    >>> accept_NotADirectoryError(NotADirectoryError())
    """
    assert isinstance(exc, BaseException)
    assert NotADirectoryError in type(exc).__mro__
    assert isinstance(exc, NotADirectoryError)

def accept_NotImplementedError(exc: NotImplementedError):
    """
    >>> accept_NotImplementedError(NotImplementedError())
    """
    assert isinstance(exc, BaseException)
    assert NotImplementedError in type(exc).__mro__
    assert isinstance(exc, NotImplementedError)

def accept_OSError(exc: OSError):
    """
    >>> accept_OSError(OSError())
    >>> accept_OSError(BlockingIOError())
    >>> accept_OSError(ChildProcessError())
    >>> accept_OSError(ConnectionError())
    >>> accept_OSError(FileExistsError())
    >>> accept_OSError(FileNotFoundError())
    >>> accept_OSError(InterruptedError())
    >>> accept_OSError(IsADirectoryError())
    >>> accept_OSError(NotADirectoryError())
    >>> accept_OSError(PermissionError())
    >>> accept_OSError(ProcessLookupError())
    >>> accept_OSError(TimeoutError())
    >>> accept_OSError(BrokenPipeError())
    >>> accept_OSError(ConnectionAbortedError())
    >>> accept_OSError(ConnectionRefusedError())
    >>> accept_OSError(ConnectionResetError())
    >>> accept_OSError(EnvironmentError())
    >>> accept_OSError(IOError())
    """
    assert isinstance(exc, BaseException)
    assert OSError in type(exc).__mro__
    assert isinstance(exc, OSError)

def accept_OverflowError(exc: OverflowError):
    """
    >>> accept_OverflowError(OverflowError())
    """
    assert isinstance(exc, BaseException)
    assert OverflowError in type(exc).__mro__
    assert isinstance(exc, OverflowError)

def accept_PendingDeprecationWarning(exc: PendingDeprecationWarning):
    """
    >>> accept_PendingDeprecationWarning(PendingDeprecationWarning())
    """
    assert isinstance(exc, BaseException)
    assert PendingDeprecationWarning in type(exc).__mro__
    assert isinstance(exc, PendingDeprecationWarning)

def accept_PermissionError(exc: PermissionError):
    """
    >>> accept_PermissionError(PermissionError())
    """
    assert isinstance(exc, BaseException)
    assert PermissionError in type(exc).__mro__
    assert isinstance(exc, PermissionError)

def accept_ProcessLookupError(exc: ProcessLookupError):
    """
    >>> accept_ProcessLookupError(ProcessLookupError())
    """
    assert isinstance(exc, BaseException)
    assert ProcessLookupError in type(exc).__mro__
    assert isinstance(exc, ProcessLookupError)

def accept_RecursionError(exc: RecursionError):
    """
    >>> accept_RecursionError(RecursionError())
    """
    assert isinstance(exc, BaseException)
    assert RecursionError in type(exc).__mro__
    assert isinstance(exc, RecursionError)

def accept_ReferenceError(exc: ReferenceError):
    """
    >>> accept_ReferenceError(ReferenceError())
    """
    assert isinstance(exc, BaseException)
    assert ReferenceError in type(exc).__mro__
    assert isinstance(exc, ReferenceError)

def accept_ResourceWarning(exc: ResourceWarning):
    """
    >>> accept_ResourceWarning(ResourceWarning())
    """
    assert isinstance(exc, BaseException)
    assert ResourceWarning in type(exc).__mro__
    assert isinstance(exc, ResourceWarning)

def accept_RuntimeError(exc: RuntimeError):
    """
    >>> accept_RuntimeError(RuntimeError())
    >>> accept_RuntimeError(NotImplementedError())
    >>> accept_RuntimeError(RecursionError())
    """
    assert isinstance(exc, BaseException)
    assert RuntimeError in type(exc).__mro__
    assert isinstance(exc, RuntimeError)

def accept_RuntimeWarning(exc: RuntimeWarning):
    """
    >>> accept_RuntimeWarning(RuntimeWarning())
    """
    assert isinstance(exc, BaseException)
    assert RuntimeWarning in type(exc).__mro__
    assert isinstance(exc, RuntimeWarning)

def accept_StopAsyncIteration(exc: StopAsyncIteration):
    """
    >>> accept_StopAsyncIteration(StopAsyncIteration())
    """
    assert isinstance(exc, BaseException)
    assert StopAsyncIteration in type(exc).__mro__
    assert isinstance(exc, StopAsyncIteration)

def accept_StopIteration(exc: StopIteration):
    """
    >>> accept_StopIteration(StopIteration())
    """
    assert isinstance(exc, BaseException)
    assert StopIteration in type(exc).__mro__
    assert isinstance(exc, StopIteration)

def accept_SyntaxError(exc: SyntaxError):
    """
    >>> accept_SyntaxError(SyntaxError())
    >>> accept_SyntaxError(IndentationError())
    >>> accept_SyntaxError(TabError())
    """
    assert isinstance(exc, BaseException)
    assert SyntaxError in type(exc).__mro__
    assert isinstance(exc, SyntaxError)

def accept_SyntaxWarning(exc: SyntaxWarning):
    """
    >>> accept_SyntaxWarning(SyntaxWarning())
    """
    assert isinstance(exc, BaseException)
    assert SyntaxWarning in type(exc).__mro__
    assert isinstance(exc, SyntaxWarning)

def accept_SystemError(exc: SystemError):
    """
    >>> accept_SystemError(SystemError())
    """
    assert isinstance(exc, BaseException)
    assert SystemError in type(exc).__mro__
    assert isinstance(exc, SystemError)

def accept_SystemExit(exc: SystemExit):
    """
    >>> accept_SystemExit(SystemExit())
    """
    assert isinstance(exc, BaseException)
    assert SystemExit in type(exc).__mro__
    assert isinstance(exc, SystemExit)

def accept_TabError(exc: TabError):
    """
    >>> accept_TabError(TabError())
    """
    assert isinstance(exc, BaseException)
    assert TabError in type(exc).__mro__
    assert isinstance(exc, TabError)

def accept_TimeoutError(exc: TimeoutError):
    """
    >>> accept_TimeoutError(TimeoutError())
    """
    assert isinstance(exc, BaseException)
    assert TimeoutError in type(exc).__mro__
    assert isinstance(exc, TimeoutError)

def accept_TypeError(exc: TypeError):
    """
    >>> accept_TypeError(TypeError())
    """
    assert isinstance(exc, BaseException)
    assert TypeError in type(exc).__mro__
    assert isinstance(exc, TypeError)

def accept_UnboundLocalError(exc: UnboundLocalError):
    """
    >>> accept_UnboundLocalError(UnboundLocalError())
    """
    assert isinstance(exc, BaseException)
    assert UnboundLocalError in type(exc).__mro__
    assert isinstance(exc, UnboundLocalError)

def accept_UnicodeError(exc: UnicodeError):
    """
    >>> accept_UnicodeError(UnicodeError())
    """
    assert isinstance(exc, BaseException)
    assert UnicodeError in type(exc).__mro__
    assert isinstance(exc, UnicodeError)

def accept_UnicodeWarning(exc: UnicodeWarning):
    """
    >>> accept_UnicodeWarning(UnicodeWarning())
    """
    assert isinstance(exc, BaseException)
    assert UnicodeWarning in type(exc).__mro__
    assert isinstance(exc, UnicodeWarning)

def accept_UserWarning(exc: UserWarning):
    """
    >>> accept_UserWarning(UserWarning())
    """
    assert isinstance(exc, BaseException)
    assert UserWarning in type(exc).__mro__
    assert isinstance(exc, UserWarning)

def accept_ValueError(exc: ValueError):
    """
    >>> accept_ValueError(ValueError())
    >>> accept_ValueError(UnicodeError())
    """
    assert isinstance(exc, BaseException)
    assert ValueError in type(exc).__mro__
    assert isinstance(exc, ValueError)

def accept_Warning(exc: Warning):
    """
    >>> accept_Warning(Warning())
    >>> accept_Warning(BytesWarning())
    >>> accept_Warning(DeprecationWarning())
    >>> accept_Warning(EncodingWarning())
    >>> accept_Warning(FutureWarning())
    >>> accept_Warning(ImportWarning())
    >>> accept_Warning(PendingDeprecationWarning())
    >>> accept_Warning(ResourceWarning())
    >>> accept_Warning(RuntimeWarning())
    >>> accept_Warning(SyntaxWarning())
    >>> accept_Warning(UnicodeWarning())
    >>> accept_Warning(UserWarning())
    """
    assert isinstance(exc, BaseException)
    assert Warning in type(exc).__mro__
    assert isinstance(exc, Warning)

def accept_ZeroDivisionError(exc: ZeroDivisionError):
    """
    >>> accept_ZeroDivisionError(ZeroDivisionError())
    """
    assert isinstance(exc, BaseException)
    assert ZeroDivisionError in type(exc).__mro__
    assert isinstance(exc, ZeroDivisionError)

##### END GENERATED TESTS


if __name__ == '__main__':
    gen_tests()
