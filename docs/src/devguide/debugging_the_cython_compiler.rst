Getting started
^^^^^^^^^^^^^^^

  or: where does that C code come from?

Most often, when you are new to Cython development, you have an idea about the Cython code you want to debug.
So, looking at the generated C code, your main question will be: »where is that C code generated?«.

Luckily, the Cython compiler has a couple of debug features that you can use
to pin-point the relevant code sections.  They can be enabled in
the module `Cython.Compiler.DebugFlags <https://github.com/cython/cython/blob/master/Cython/Compiler/DebugFlags.py>`_.
Read the comments in that file, enable the relevant debug features
(usually ``debug_trace_code_generation`` to get started), and then read
the C code that Cython generates to find out what is going on.

One trick to identify the origin of *a specific line* of C code is
to use the Python debugger to stop when that specific line is written by adding
``if s.find("your line of code") != -1: import pdb; pdb.set_trace()`` to the
`CCodeWriter.write function in Code.py <https://github.com/cython/cython/blob/b9cecd602878334173aa9f6ed635d48739bfa2b1/Cython/Compiler/Code.py#L1820>`_.

It's usually best to write a test case for the code you want to debug. See the next section on how to do this.

To get a general idea about the different `code modules <https://github.com/cython/cython/tree/master/Cython/Compiler>_`
of the Cython compiler, you might want to skip through
`Josh Kantor's Cython notes <https://web.archive.org/web/20170511222231/https://wstein.org/wiki/attachments/2008(2f)sageseminar(2f)kantor/slides.pdf>`_.
