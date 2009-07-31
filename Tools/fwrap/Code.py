from Cython.StringIOTree import StringIOTree
from cStringIO import StringIO

INDENT = "  "
LINE_LENGTH = 79
BREAK_CHARS = (' ', '\t', ',', '!')
COMMENT_CHAR = '!'

def break_line(line, level, max_len):

    line = INDENT*level+line

    if len(line) <= max_len:
        return [line, '']

    # break up line.
    in_comment = False
    in_string = False
    in_escape = False
    last_break_pos = -1
    for idx, ch in enumerate(line):
        if idx+1 > max_len:
            if last_break_pos < 0:
                raise RuntimeError("line too long and unable to break it up.")
            return [line[:last_break_pos]] + break_line(line[last_break_pos:], level, max_len)

        if ch in BREAK_CHARS and not in_comment and not in_string:
            last_break_pos = idx

        if ch == COMMENT_CHAR and not in_comment and not in_string:
            in_comment = True
        elif ch in ('"', "'") and not in_string and not in_comment:
            in_string = True
        elif ch in ('"', "'") and in_string and not in_escape and not in_comment:
            in_string = False

        if ch == '\\' and not in_escape:
            in_escape = True
        elif in_escape:
            in_escape = False

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
        return type(self)(level, writer=self.sit.insertion_point())

    def insert(self, writer):
        self.sit.insert(writer.sit)

    def tell(self):
        return self.sit.stream.tell()

    def __getattr__(self, attr):
        return getattr(self.sit, attr)

class FortranCodeWriter(CodeWriter):

    def putln(self, line, max_len=LINE_LENGTH):

        if len(line) <= max_len:
            self.sit.write(INDENT*self.level+line+"\n")
        else:
            multiline = "&\n".join([ln for ln in break_line(line, self.level, max_len) if ln])
            self.sit.write(multiline+'\n')

class CompositeCodeBase(object):

    def __init__(self, level=0, writer=CodeWriter):
        self.level = level
        self.root = writer(level)

    def copyto(self, target):
        self.root.copyto(target)

    def getvalue(self):
        return self.root.getvalue()

class UtilityCode(CompositeCodeBase):
    pass

class InterfaceCode(CompositeCodeBase):

    def __init__(self, level=0):
        CompositeCodeBase.__init__(self, level, writer=FortranCodeWriter)
        self.has_subprogs = False
        self.top = self.root.insertion_point(level)
        self.block_start = self.root.insertion_point(level)
        self.use_stmts = self.root.insertion_point(level+1)
        self.declarations = self.root.insertion_point(level+1)
        self.block_end = self.root.insertion_point(level)
        self.bottom = self.root.insertion_point(level)

class CompositeBlock(CompositeCodeBase):
    '''
    Base class for all Module, SubProgram (functions/subroutines) & program
    code blocks.
    '''

    def __init__(self, level=0):
        CompositeCodeBase.__init__(self, level, writer=FortranCodeWriter)
        self.has_subprogs = False
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

class CySuiteCode(CompositeCodeBase):

    def __init__(self, level=0):
        CompositeCodeBase.__init__(self, level)
        self.suite_start = self.root.insertion_point(level)
        self.suite_body = self.root.insertion_point(level+1)
