from __future__ import unicode_literals

import unittest
from io import StringIO

from Cython.Compiler import Scanning
from Cython.Compiler.Symtab import ModuleScope
from Cython.Compiler.TreeFragment import StringParseContext
from Cython.Compiler.Errors import init_thread

# generate some fake code - just a bunch of lines of the form "a0 a1 ..."
code = []
for ch in range(ord("a"), ord("z")):
    line = " ".join(["%s%s" % (chr(ch), n) for n in range(10)])
    code.append(line)
code = "\n".join(code)

init_thread()


class TestScanning(unittest.TestCase):
    def make_scanner(self):
        source = Scanning.StringSourceDescriptor("fake code", code)
        buf = StringIO(code)
        context = StringParseContext("fake context")
        scope = ModuleScope("fake_module", None, None)

        return Scanning.PyrexScanner(buf, source, scope=scope, context=context)

    def test_put_back_positions(self):
        scanner = self.make_scanner()

        self.assertEqual(scanner.sy, "IDENT")
        self.assertEqual(scanner.systring, "a0")
        scanner.next()
        self.assertEqual(scanner.sy, "IDENT")
        self.assertEqual(scanner.systring, "a1")
        a1pos = scanner.position()
        self.assertEqual(a1pos[1:], (1, 3))
        a2peek = scanner.peek()  # shouldn't mess up the position
        self.assertEqual(a1pos, scanner.position())
        scanner.next()
        self.assertEqual(a2peek, (scanner.sy, scanner.systring))

        # find next line
        while scanner.sy != "NEWLINE":
            scanner.next()

        line_sy = []
        line_systring = []
        line_pos = []

        scanner.next()
        while scanner.sy != "NEWLINE":
            line_sy.append(scanner.sy)
            line_systring.append(scanner.systring)
            line_pos.append(scanner.position())
            scanner.next()

        for sy, systring, pos in zip(
            line_sy[::-1], line_systring[::-1], line_pos[::-1]
        ):
            scanner.put_back(sy, systring, pos)

        n = 0
        while scanner.sy != "NEWLINE":
            self.assertEqual(scanner.sy, line_sy[n])
            self.assertEqual(scanner.systring, line_systring[n])
            self.assertEqual(scanner.position(), line_pos[n])
            scanner.next()
            n += 1

        self.assertEqual(n, len(line_pos))

    def test_tentatively_scan(self):
        scanner = self.make_scanner()
        with Scanning.tentatively_scan(scanner) as errors:
            while scanner.sy != "NEWLINE":
                scanner.next()
        self.assertFalse(errors)

        scanner.next()
        self.assertEqual(scanner.systring, "b0")
        pos = None
        with Scanning.tentatively_scan(scanner) as errors:
            while scanner.sy != "NEWLINE":
                scanner.next()
                if not pos:
                    # record position of first tentatively scanned part
                    pos = scanner.position()
                if scanner.systring == "b7":
                    scanner.error("Oh no not b7!")
                    break
        self.assertTrue(errors)
        self.assertEqual(scanner.systring, "b1")  # state has been restored
        self.assertEqual(scanner.position(), pos)
        scanner.next()
        self.assertEqual(scanner.systring, "b2")  # and we can keep going again
        scanner.next()
        self.assertEqual(scanner.systring, "b3")  # and we can keep going again


if __name__ == "__main__":
    unittest.main()
