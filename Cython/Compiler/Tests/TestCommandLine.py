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
import multiprocessing

from Cython.TestUtils import CythonTest
from Cython.Compiler.CmdLine import parse_command_line

import Cython.Compiler.Options as Options
import Cython.Compiler.DebugFlags as DebugFlags

def parse(string):
    return parse_command_line(string.split())

def parser_return_code(string):
    '''Return code of Cython, if it had been invoked with <string> as cline.'''
    p = multiprocessing.Process(target=parse_command_line, args=[string.split()])
    p.start()
    p.join()
    return p.exitcode

FAILURE = 2

class TestCommandLine(CythonTest):
    def test_source_recognition(self):
        opt, src = parse('-z test -t -f -I. source.pyx')
        self.assertEqual(src, ['source.pyx'])
        opt, src = parse('-z=test -t -f -I. sourceXX.pyx')
        self.assertEqual(src, ['sourceXX.pyx'])
        opt, src = parse('-I. source.pyx source2.pyx -f -D')
        self.assertEqual(src, ['source.pyx', 'source2.pyx'])
        #opt, src = parse('-I. source.pyx -f -D source2.pyx')
        #self.assertEqual(src, ['source.pyx', 'source2.pyx'])
        opt, src = parse('-I. -f -D source.pyx source2.pyx')
        self.assertEqual(src, ['source.pyx', 'source2.pyx'])

    def test_embed_recognition(self):
        opt, src = parse('--embed --gdb -2  test.pyx')
        self.assertEqual(Options.embed, 'main')
        self.assertEqual(src, ['test.pyx'])
        opt, src = parse('--gdb -2 --embed -- test.pyx')
        self.assertEqual(Options.embed, 'main')
        self.assertEqual(src, ['test.pyx'])
        opt, src = parse('--gdb -2 --embed test.pyx')
        self.assertEqual(Options.embed, 'main')
        self.assertEqual(src, ['test.pyx'])
        opt, src = parse('--fast-fail --embed mainX -f --gdb s.py')
        self.assertEqual(Options.embed, 'mainX')
        #XXX should not be used
        #opt, src = parse('--fast-fail -f --gdb s.py --embed mainZ')
        #self.assertEqual(src, ['s.py'])
        #self.assertEqual(Options.embed, 'mainZ')
        self.assertEqual(
            parser_return_code('--fast-fail -f --embed a.pyx b.py'),
            FAILURE)
        self.assertEqual(
            parser_return_code('--fast-fail -f --embed a.pyx b.py c.py'),
            FAILURE)

    def test_embed_explicit_recognition(self):
        try:
            from Cython.Compiler.CmdLine import argparse
        except ImportError:
            self.skipTest('--embed <name> is parseable only by newer argparse')
        opt, src = parse('--fast-fail -f --embed=mainY --gdb s.py')
        self.assertEqual(Options.embed, 'mainY')
        self.assertEqual(
            parser_return_code('--fast-fail -f --embed=mainY --gdb'),
            FAILURE)
        self.assertEqual(
            parser_return_code('--fast-fail -f --embed=mainY --gdb a.pyx b.py'),
            FAILURE)

    def test_include_recognition(self):
        opt, src = parse('-v -r -Igreedy -w x test.pyx')
        self.assertEqual(opt['include_path'], ['greedy'])
        self.assertEqual(src, ['test.pyx'])
        opt, src = parse('-I/usr/include/mistery/dot test.pyx')
        self.assertEqual(opt['include_path'], ['/usr/include/mistery/dot'])
        opt, src = parse('-I /usr/include/mistery/dot test.pyx')
        self.assertEqual(opt['include_path'], ['/usr/include/mistery/dot'])

    def test_directive_options(self):
        def issubset(universe, dic):
            '''True if <dic> is a subset of <universe>'''
            for k, v in dic.iteritems():
                try:
                    if universe[k] != v:
                        return False
                except KeyError:
                    return False
            return True

        opt, src = parse('-Xboundscheck=False test.pyx')
        self.failIf(opt['compiler_directives']['boundscheck'])
        opt, src = parse('-Xnonecheck=True test.pyx')
        self.failUnless(opt['compiler_directives']['nonecheck'])
        opt, src = parse('-Xcdivision=True test.pyx')
        self.failUnless(opt['compiler_directives']['cdivision'])
        opt, src = parse('-Xlanguage_level=2,profile=True test.pyx')
        self.failUnless(issubset(opt['compiler_directives'],
            {'profile': True, 'language_level': 2}))
        opt, src = parse('--directive callspec=False,final=True test.pyx')
        self.failUnless(issubset(opt['compiler_directives'],
            {'callspec': False, 'final': True}))
        opt, src = parse('-Xauto_cpdef=True,profile=True -I. -Xinternal=True test.pyx')
        self.failUnless(issubset(opt['compiler_directives'],
            {'profile': True, 'internal': True, 'auto_cpdef': True} ))

    def test_output_options(self):
        opt, src = parse('-I. -I /usr -o mytestexec test.pyx')
        self.assertEqual(opt['output_file'], 'mytestexec')
        opt, src = parse('-I. -o2mytestexec -I /usr test.pyx')
        self.assertEqual(opt['output_file'], '2mytestexec')

    def test_if_arguments_are_required_correctly(self):
        self.assertEqual(parser_return_code('-I'), FAILURE)
        self.assertEqual(parser_return_code(''), FAILURE)
        self.assertEqual(parser_return_code('-X source.py'), FAILURE)

    def test_debug_options(self):
        opt, src = parse('-I. --debug-temp-code-comments test.pyx')
        self.failUnless(DebugFlags.debug_temp_code_comments)
        opt, src = parse('--debug-trace-code-generation test.pyx')
        self.failUnless(DebugFlags.debug_trace_code_generation)
        opt, src = parse('--debug-verbose-pipeline test.pyx')
        self.failUnless(DebugFlags.debug_verbose_pipeline)

    @classmethod
    def tearDownClass(cls):
        # Clean up permanent options XXX
        reload(Options)

if __name__ == '__main__':
    import unittest
    unittest.main()
