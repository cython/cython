#
#   Copyright 2011 Stefano Sanfilippo <satufk on GitHub>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os

from Cython.TestUtils import CythonTest
from Cython.Compiler.CmdLine import parse_command_line

import Cython.Compiler.Options as Options
import Cython.Compiler.DebugFlags as DebugFlags

def parse(string):
    return parse_command_line(string.split())

#FIXME very time consuming
def parser_return_code(string):
    '''Return code of Cython, if it had been invoked with <string> as cline.'''
    return os.system("""python -c \"from Cython.Compiler.CmdLine import \
        parse_command_line as p\np('%s'.split())\" &> /dev/null""" % string)

FAILURE = 512

class TestCommandLine(CythonTest):
    def test_source_recognition(self):
        opt, src = parse('--embed=test -t -f -I. source.pyx')
        self.failUnlessEqual(src, ['source.pyx'])
        opt, src = parse('-I. source.pyx source2.pyx -f -D')
        self.failUnlessEqual(src, ['source.pyx', 'source2.pyx'])

    def test_embed_recognition(self):
        opt, src = parse('--fast-fail -f --embed mainX --gdb s.py')
        self.failUnlessEqual(Options.embed, 'mainX')
        opt, src = parse('--fast-fail -f --embed=mainY --gdb s.py')
        self.failUnlessEqual(Options.embed, 'mainY')
        opt, src = parse('--embed --gdb -2  test.pyx')
        self.failUnlessEqual(Options.embed, 'main')
        self.failUnlessEqual(src, ['test.pyx'])

    def test_include_recognition(self):
        opt, src = parse('-v -r -Igreedy --embed=x test.pyx')
        self.failUnless(opt['include_path'] == ['greedy'] and src == ['test.pyx'])
        opt, src = parse('-I/usr/include/mistery/dot test.pyx')
        self.failUnlessEqual(opt['include_path'], ['/usr/include/mistery/dot'])

    def test_directive_options(self):
        opt, src = parse('-Xboundscheck=False test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], {'boundscheck': False})
        opt, src = parse('-Xnonecheck=True test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], {'nonecheck': True})
        opt, src = parse('-Xcdivision=True test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], {'cdivision': True})
        opt, src = parse('-Xlanguage_level=2,profile=True test.pyx')
        self.failUnlessEqual(opt['compiler_directives'],
            {'profile': True, 'language_level': 2})
        opt, src = parse('--directive callspec=False,final=True test.pyx')
        self.failUnlessEqual(opt['compiler_directives'],
            {'callspec': 'False', 'final': True})
        opt, src = parse('-Xauto_cpdef=True,profile=True -I. -Xinternal=True test.pyx')
        self.failUnlessEqual(opt['compiler_directives'],
            {'profile': True, 'internal': True, 'auto_cpdef': True} )

    def test_debug_options(self):
        opt, src = parse('-I. --debug temp_code_comments test.pyx')
        self.failUnless(DebugFlags.debug_temp_code_comments)
        # Let's try - instead of _
        opt, src = parse('--debug=trace-code-generation test.pyx')
        self.failUnless(DebugFlags.debug_trace_code_generation)
        opt, src = parse('-dverbose_pipeline test.pyx')
        self.failUnless(DebugFlags.debug_verbose_pipeline)

    def test_output_options(self):
        opt, src = parse('-I. -I /usr -o mytestexec test.pyx')
        self.failUnlessEqual(opt['output_file'], 'mytestexec')
        opt, src = parse('-I. -o2mytestexec -I /usr test.pyx')
        self.failUnlessEqual(opt['output_file'], '2mytestexec')

    def test_if_arguments_are_required_correctly(self):
        self.failUnless(parser_return_code('-I') == FAILURE)
        self.failUnless(parser_return_code('') == FAILURE)
        self.failUnless(parser_return_code('-X source.py') == FAILURE)

if __name__ == '__main__':
    import unittest
    unittest.main()
