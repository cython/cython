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

def parse(string):
    return parse_command_line(string.split())

def parser_return_code(string):
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
        opt, src = parse('-Xfake test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], ['fake'])
        opt, src = parse('-Xwooofake test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], ['wooofake'])
        opt, src = parse('-Xfake=2 test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], ['fake=2'])
        opt, src = parse('-Xfake=2,sub=1 test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], ['fake=2,sub=1'])
        opt, src = parse('--directive fake=2,sub=1 test.pyx')
        self.failUnlessEqual(opt['compiler_directives'], ['fake=2,sub=1'])

    def test_debug_options(self):
        opt, src = parse('-I. --debug fake1 test.pyx')
        self.failUnlessEqual(opt['debug_flags'], ['fake1'])
        opt, src = parse('--debug=fake2 test.pyx')
        self.failUnlessEqual(opt['debug_flags'], ['fake2'])
        opt, src = parse('-dfake3 test.pyx')
        self.failUnlessEqual(opt['debug_flags'], ['fake3'])

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
