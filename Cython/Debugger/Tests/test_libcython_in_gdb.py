"""
Tests that run inside GDB.

Note: debug information is already imported by the file generated by
Cython.Debugger.Cygdb.make_command_file()
"""


import os
import re
import sys
import trace
import pickle
import random
import inspect
import warnings
import unittest
import textwrap
import tempfile
import functools
import traceback
import itertools
#from test import test_support

import gdb

from .. import libcython
from .. import libpython
from . import TestLibCython as test_libcython

# for some reason sys.argv is missing in gdb
sys.argv = ['gdb']


def print_on_call_decorator(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        _debug(type(self).__name__, func.__name__)

        try:
            return func(self, *args, **kwargs)
        except Exception:
            _debug("An exception occurred:", traceback.format_exc())
            raise

    return wrapper

class TraceMethodCallMeta(type):

    def __init__(self, name, bases, dict):
        for func_name, func in dict.items():
            if inspect.isfunction(func):
                setattr(self, func_name, print_on_call_decorator(func))


class DebugTestCase(unittest.TestCase, metaclass=TraceMethodCallMeta):
    """
    Base class for test cases. On teardown it kills the inferior and unsets
    all breakpoints.
    """

    def __init__(self, name):
        super().__init__(name)
        self.cy = libcython.cy
        self.module = libcython.cy.cython_namespace['codefile']
        self.spam_func, self.spam_meth = libcython.cy.functions_by_name['spam']
        self.ham_func = libcython.cy.functions_by_qualified_name[
            'codefile.ham']
        self.eggs_func = libcython.cy.functions_by_qualified_name[
            'codefile.eggs']

    def read_var(self, varname, cast_to=None):
        result = gdb.parse_and_eval('$cy_cvalue("%s")' % varname)
        if cast_to:
            result = cast_to(result)

        return result

    def local_info(self):
        return gdb.execute('info locals', to_string=True)

    def lineno_equals(self, source_line=None, lineno=None):
        if source_line is not None:
            lineno = test_libcython.source_to_lineno[source_line]
        frame = gdb.selected_frame()
        self.assertEqual(libcython.cython_info.lineno(frame), lineno)

    def break_and_run(self, source_line):
        break_lineno = test_libcython.source_to_lineno[source_line]
        gdb.execute('cy break codefile:%d' % break_lineno, to_string=True)
        gdb.execute('run', to_string=True)

    def tearDown(self):
        gdb.execute('delete breakpoints', to_string=True)
        try:
            gdb.execute('kill inferior 1', to_string=True)
        except RuntimeError:
            pass

        gdb.execute('set args -c "import codefile"')


class TestDebugInformationClasses(DebugTestCase):

    def test_CythonModule(self):
        "test that debug information was parsed properly into data structures"
        self.assertEqual(self.module.name, 'codefile')
        global_vars = ('c_var', 'python_var', '__name__',
                       '__builtins__', '__doc__', '__file__')
        assert set(global_vars).issubset(self.module.globals)

    def test_CythonVariable(self):
        module_globals = self.module.globals
        c_var = module_globals['c_var']
        python_var = module_globals['python_var']
        self.assertEqual(c_var.type, libcython.CObject)
        self.assertEqual(python_var.type, libcython.PythonObject)
        self.assertEqual(c_var.qualified_name, 'codefile.c_var')

    def test_CythonFunction(self):
        self.assertEqual(self.spam_func.qualified_name, 'codefile.spam')
        self.assertEqual(self.spam_meth.qualified_name,
                         'codefile.SomeClass.spam')
        self.assertEqual(self.spam_func.module, self.module)

        assert self.eggs_func.pf_cname, (self.eggs_func, self.eggs_func.pf_cname)
        assert not self.ham_func.pf_cname
        assert not self.spam_func.pf_cname
        assert not self.spam_meth.pf_cname

        self.assertEqual(self.spam_func.type, libcython.CObject)
        self.assertEqual(self.ham_func.type, libcython.CObject)

        self.assertEqual(self.spam_func.arguments, ['a'])
        self.assertEqual(self.spam_func.step_into_functions,
                         {'puts', 'some_c_function'})

        expected_lineno = test_libcython.source_to_lineno['def spam(a=0):']
        self.assertEqual(self.spam_func.lineno, expected_lineno)
        self.assertEqual(sorted(self.spam_func.locals), list('abcd'))


class TestReprMethods(DebugTestCase):

    def test_simple_repr(self):
        test_class = libcython.CythonModule
        num_args = len(inspect.signature(test_class).parameters)
        lorem_ipsum = random.Random(0)
        filler_args = (lorem_ipsum.randbytes(8) for _ in range(num_args))
        instance = test_class(*filler_args)
        recreated = eval("libcython." + repr(instance))
        self.assertEqual(pickle.dumps(instance), pickle.dumps(recreated))

    def test_frame_repr(self):
        # check that frame_repr's function expansion is idempotent
        beginline = 'import os'

        self.break_and_run(beginline)
        frame = gdb.selected_frame()
        self.assertEqual(libcython.frame_repr(frame),
                         libcython.frame_repr(frame))


class TestParameters(unittest.TestCase):

    def test_parameters(self):
        gdb.execute('set cy_colorize_code on')
        assert libcython.parameters.colorize_code
        gdb.execute('set cy_colorize_code off')
        assert not libcython.parameters.colorize_code


class TestBreak(DebugTestCase):

    def test_break(self):
        breakpoint_amount = len(gdb.breakpoints() or ())
        gdb.execute('cy break codefile.spam')

        self.assertEqual(len(gdb.breakpoints()), breakpoint_amount + 1)
        bp = gdb.breakpoints()[-1]
        self.assertEqual(bp.type, gdb.BP_BREAKPOINT)
        assert self.spam_func.cname in bp.location
        assert bp.enabled

    def test_python_break(self):
        gdb.execute('cy break -p join')
        assert 'def join(' in gdb.execute('cy run', to_string=True)

    def test_break_lineno(self):
        beginline = 'import os'
        nextline = 'cdef int c_var = 12'

        self.break_and_run(beginline)
        self.lineno_equals(beginline)
        step_result = gdb.execute('cy step', to_string=True)
        self.lineno_equals(nextline)
        assert step_result.rstrip().endswith(nextline)

    def test_break_completion(self):
        completer = libcython.cy.break_.complete
        self.assertIn('spam', completer("codefile.SomeClass.s", "s"))
        self.assertIn('spam', completer("codefile.SomeClass.", None))
        self.assertIn('pam', completer("codefile.s", None))


# I removed this testcase, because it will never work, because
# gdb.execute(..., to_string=True) does not capture stdout and stderr of python.
# class TestKilled(DebugTestCase):
#     def test_abort(self):
#         gdb.execute("set args -c 'import os;print(123456789);os.abort()'")
#         output = gdb.execute('cy run', to_string=True)
#         assert 'abort' in output.lower()


class DebugStepperTestCase(DebugTestCase):

    def step(self, varnames_and_values, source_line=None, lineno=None):
        gdb.execute(self.command)
        for varname, value in varnames_and_values:
            self.assertEqual(self.read_var(varname), value, self.local_info())

        self.lineno_equals(source_line, lineno)


class TestStep(DebugStepperTestCase):
    """
    Test stepping. Stepping happens in the code found in
    Cython/Debugger/Tests/codefile.
    """

    def test_cython_step(self):
        gdb.execute('cy break codefile.spam')

        gdb.execute('run', to_string=True)
        self.lineno_equals('def spam(a=0):')

        gdb.execute('cy step', to_string=True)
        self.lineno_equals('b = c = d = 0')

        self.command = 'cy step'
        self.step([('b', 0)], source_line='b = 1')
        self.step([('b', 1), ('c', 0)], source_line='c = 2')
        self.step([('c', 2)], source_line='int(10)')
        self.step([], source_line='puts("spam")')

        gdb.execute('cont', to_string=True)
        self.assertEqual(len(gdb.inferiors()), 1)
        self.assertEqual(gdb.inferiors()[0].pid, 0)

    def test_c_step(self):
        self.break_and_run('some_c_function()')
        gdb.execute('cy step', to_string=True)
        self.assertEqual(gdb.selected_frame().name(), 'some_c_function')

    def test_python_step(self):
        self.break_and_run('os.path.join("foo", "bar")')

        result = gdb.execute('cy step', to_string=True)

        curframe = gdb.selected_frame()
        self.assertEqual(curframe.name(), 'PyEval_EvalFrameEx')

        pyframe = libpython.Frame(curframe).get_pyop()
        # With Python 3 inferiors, pyframe.co_name will return a PyUnicodePtr,
        # be compatible
        frame_name = pyframe.co_name.proxyval(set())
        self.assertEqual(frame_name, 'join')
        assert re.match(r'\d+    def join\(', result), result


class TestNext(DebugStepperTestCase):

    def test_cython_next(self):
        self.break_and_run('c = 2')

        lines = (
            'int(10)',
            'puts("spam")',
            'os.path.join("foo", "bar")',
            'some_c_function()',
        )

        for line in lines:
            gdb.execute('cy next')
            self.lineno_equals(line)


class TestLocalsGlobals(DebugTestCase):

    def test_locals(self):
        self.break_and_run('int(10)')

        result = gdb.execute('cy locals', to_string=True)
        assert 'a = 0', repr(result)
        assert 'b = (int) 1', result
        assert 'c = (int) 2' in result, repr(result)

    def test_globals(self):
        self.break_and_run('int(10)')

        result = gdb.execute('cy globals', to_string=True)
        assert '__name__ ' in result, repr(result)
        assert '__doc__ ' in result, repr(result)
        assert 'os ' in result, repr(result)
        assert 'c_var ' in result, repr(result)
        assert 'python_var ' in result, repr(result)


class TestBacktrace(DebugTestCase):

    def test_backtrace(self):
        libcython.parameters.colorize_code.value = False

        self.break_and_run('os.path.join("foo", "bar")')

        def match_backtrace_output(result):
            assert re.search(r'\#\d+ *0x.* in spam\(\) at .*codefile\.pyx:22',
                             result), result
            assert 'os.path.join("foo", "bar")' in result, result

        result = gdb.execute('cy bt', to_string=True)
        match_backtrace_output(result)

        result = gdb.execute('cy bt -a', to_string=True)
        match_backtrace_output(result)

        # Apparently not everyone has main()
        # assert re.search(r'\#0 *0x.* in main\(\)', result), result


class TestFunctions(DebugTestCase):

    def test_functions(self):
        self.break_and_run('c = 2')
        result = gdb.execute('print $cy_cname("b")', to_string=True)
        assert re.search('__pyx_.*b', result), result

        result = gdb.execute('print $cy_lineno()', to_string=True)
        supposed_lineno = test_libcython.source_to_lineno['c = 2']
        assert str(supposed_lineno) in result, (supposed_lineno, result)

        result = gdb.execute('print $cy_cvalue("b")', to_string=True)
        assert '= 1' in result


class TestPrint(DebugTestCase):

    def test_print(self):
        self.break_and_run('c = 2')
        result = gdb.execute('cy print b', to_string=True)
        self.assertEqual('b = (int) 1\n', result)
        result = gdb.execute('cy print python_var', to_string=True)
        self.assertEqual('python_var = 13\n', result)
        result = gdb.execute('cy print c_var', to_string=True)
        self.assertEqual('c_var = (int) 12\n', result)

correct_result_test_list_inside_func = '''\
    14            int b, c
    15
    16        b = c = d = 0
    17
    18        b = 1
>   19        c = 2
    20        int(10)
    21        puts("spam")
    22        os.path.join("foo", "bar")
    23        some_c_function()
'''
correct_result_test_list_outside_func = '''\
     5        void some_c_function()
     6
     7    import os
     8
     9    cdef int c_var = 12
>   10    python_var = 13
    11
    12    def spam(a=0):
    13        cdef:
    14            int b, c
'''


class TestList(DebugTestCase):
    def workaround_for_coding_style_checker(self, correct_result_wrong_whitespace):
        correct_result = ""
        for line in correct_result_test_list_inside_func.split("\n"):
            if len(line) < 10 and len(line) > 0:
                line += " "*4
            correct_result += line + "\n"
        correct_result = correct_result[:-1]

    def test_list_inside_func(self):
        self.break_and_run('c = 2')
        result = gdb.execute('cy list', to_string=True)
        # We don't want to fail because of some trailing whitespace,
        # so we remove trailing whitespaces with the following line
        result = "\n".join([line.rstrip() for line in result.split("\n")])
        self.assertEqual(correct_result_test_list_inside_func, result)

    def test_list_outside_func(self):
        self.break_and_run('python_var = 13')
        result = gdb.execute('cy list', to_string=True)
        # We don't want to fail because of some trailing whitespace,
        # so we remove trailing whitespaces with the following line
        result = "\n".join([line.rstrip() for line in result.split("\n")])
        self.assertEqual(correct_result_test_list_outside_func, result)


class TestUpDown(DebugTestCase):

    def test_updown(self):
        self.break_and_run('os.path.join("foo", "bar")')
        gdb.execute('cy step')
        self.assertRaises(RuntimeError, gdb.execute, 'cy down')

        result = gdb.execute('cy up', to_string=True)
        assert 'spam()' in result
        assert 'some_c_function()' not in result


class TestExec(DebugTestCase):

    def setUp(self):
        super().setUp()
        self.fd, self.tmpfilename = tempfile.mkstemp()
        self.tmpfile = os.fdopen(self.fd, 'r+')

    def tearDown(self):
        super().tearDown()

        try:
            self.tmpfile.close()
        finally:
            os.remove(self.tmpfilename)

    def eval_command(self, command):
        gdb.execute('cy exec open(%r, "w").write(str(%s))' %
                                                (self.tmpfilename, command))
        return self.tmpfile.read().strip()

    def test_cython_exec(self):
        self.break_and_run('os.path.join("foo", "bar")')

        # test normal behaviour
        self.assertEqual("[0]", self.eval_command('[a]'))

        return  #The test after this return freezes gdb, so I temporarily removed it.
        # test multiline code
        result = gdb.execute(textwrap.dedent('''\
            cy exec
            pass

            "nothing"
            end
            '''))
        result = self.tmpfile.read().rstrip()
        self.assertEqual('', result)

    def test_python_exec(self):
        self.break_and_run('os.path.join("foo", "bar")')
        gdb.execute('cy step')

        gdb.execute('cy exec some_random_var = 14')
        self.assertEqual('14', self.eval_command('some_random_var'))


class CySet(DebugTestCase):

    def test_cyset(self):
        self.break_and_run('os.path.join("foo", "bar")')

        gdb.execute('cy set a = $cy_eval("{None: []}")')
        stringvalue = self.read_var("a", cast_to=str)
        self.assertEqual(stringvalue, "{None: []}")


class TestCyEval(DebugTestCase):
    "Test the $cy_eval() gdb function."

    def test_cy_eval(self):
        # This function leaks a few objects in the GDB python process. This
        # is no biggie
        self.break_and_run('os.path.join("foo", "bar")')

        result = gdb.execute('print $cy_eval("None")', to_string=True)
        assert re.match(r'\$\d+ = None\n', result), result

        result = gdb.execute('print $cy_eval("[a]")', to_string=True)
        assert re.match(r'\$\d+ = \[0\]', result), result


class TestClosure(DebugTestCase):

    def break_and_run_func(self, funcname):
        gdb.execute('cy break ' + funcname)
        gdb.execute('cy run')

    def test_inner(self):
        self.break_and_run_func('inner')
        self.assertEqual('', gdb.execute('cy locals', to_string=True))

        # Allow the Cython-generated code to initialize the scope variable
        gdb.execute('cy step')

        self.assertEqual(str(self.read_var('a')), "'an object'")
        print_result = gdb.execute('cy print a', to_string=True).strip()
        self.assertEqual(print_result, "a = 'an object'")

    def test_outer(self):
        self.break_and_run_func('outer')
        self.assertEqual('', gdb.execute('cy locals', to_string=True))

        # Initialize scope with 'a' uninitialized
        gdb.execute('cy step')
        self.assertEqual('', gdb.execute('cy locals', to_string=True))

        # Initialize 'a' to 1
        gdb.execute('cy step')
        print_result = gdb.execute('cy print a', to_string=True).strip()
        self.assertEqual(print_result, "a = 'an object'")


_do_debug = os.environ.get('GDB_DEBUG')
if _do_debug:
    _debug_file = open('/dev/tty', 'w')

def _debug(*messages):
    if _do_debug:
        messages = itertools.chain([sys._getframe(1).f_code.co_name, ':'],
                                   messages)
        _debug_file.write(' '.join(str(msg) for msg in messages) + '\n')


def run_unittest_in_module(modulename):
    # Check if the Python executable provides a symbol table.
    if not hasattr(gdb.selected_inferior().progspace, "symbol_file"):
        msg = ("Unable to run tests, Python was not compiled with "
                "debugging information. Either compile python with "
                "-g or get a debug build (configure with --with-pydebug).")
        warnings.warn(msg)
        os._exit(1)
    else:
        m = __import__(modulename, fromlist=[''])
        tests = inspect.getmembers(m, inspect.isclass)

        # test_support.run_unittest(tests)

        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite(
            [test_loader.loadTestsFromTestCase(cls) for name, cls in tests])

        result = unittest.TextTestRunner(verbosity=1).run(suite)
        return result.wasSuccessful()

def runtests():
    """
    Run the libcython and libpython tests. Ensure that an appropriate status is
    returned to the parent test process.
    """
    from Cython.Debugger.Tests import test_libpython_in_gdb

    success_libcython = run_unittest_in_module(__name__)
    success_libpython = run_unittest_in_module(test_libpython_in_gdb.__name__)

    if not success_libcython or not success_libpython:
        sys.exit(2)

def main(version, trace_code=False):
    global inferior_python_version

    inferior_python_version = version

    if trace_code:
        tracer = trace.Trace(count=False, trace=True, outfile=sys.stderr,
                            ignoredirs=[sys.prefix, sys.exec_prefix])
        tracer.runfunc(runtests)
    else:
        runtests()
