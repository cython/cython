from Cython.StringIOTree import StringIOTree
from cStringIO import StringIO

INDENT = "  "

class CodeWriter(object):

    def __init__(self, level, writer=None, **kwargs):
        if writer is None:
            self.sit = StringIOTree(**kwargs)
        else:
            self.sit = writer
        self.level = level

    def putln(self, line):
        self.sit.write(INDENT*self.level+line+"\n")

    def put(self, chunk, indent=False):
        if indent:
            chunk = ('\n'+INDENT*self.level).join(chunk.split('\n'))
        self.sit.write(chunk)

    def insertion_point(self, level=None):
        if level is None:
            level = self.level
        return CodeWriter(level, writer=self.sit.insertion_point())

    def __getattr__(self, attr):
        return getattr(self.sit, attr)


class UtilityCode(object):

    def __init__(self, level=0):
        self.level = level
        self.root = CodeWriter(level)

    def copyto(self, target):
        self.root.copyto(target)

class CompositeBlock(object):
    '''
    Base class for all Module, SubProgram (functions/subroutines) & program
    code blocks.
    '''

    def __init__(self, level=0):
        self.level = level
        self.has_subprogs = False
        self.root = CodeWriter(level)
        self.top = self.root.insertion_point(level)
        self.block_start = self.root.insertion_point(level)
        self.use_stmts = self.root.insertion_point(level+1)
        self.implicit_none = self.root.insertion_point(level+1)
        self.declarations = self.root.insertion_point(level+1)
        self.executable_stmts = self.root.insertion_point(level+1)
        self.subprograms = self.root.insertion_point(level+1)
        self.block_end = self.root.insertion_point(level)
        self.bottom = self.root.insertion_point(level)

        self.implicit_none.putln("implicit none")

    def add_subprogram_block(self, subp):
        if not self.has_subprogs:
            self.has_subprogs = True
            self.subprograms.putln("contains")
        self.subprograms.insert(subp.root)

    def add_declaration_block(self, dec):
        self.declarations.insert(dec.root)

    def getvalue(self):
        return self.root.getvalue()

    def copyto(self, target):
        self.root.copyto(target)

class ModuleCode(CompositeBlock):

    block_type_str = "module"

class SubProgramCode(CompositeBlock):
    pass

class FunctionCode(SubProgramCode):

    block_type_str = "function"

class SubroutineCode(SubProgramCode):

    block_type_str = "subroutine"

class ProgramCode(CompositeBlock):

    block_type_str = "program"
