.. highlight:: cython

.. _overview-label:

********
Overview
********

A language for writing Python extension modules

What is Cython all about?
=========================

Cython is a language specially designed for writing Python extension modules.
It's designed to bridge the gap between the nice, high-level, easy-to-use
world of Python and the messy, low-level world of C.

You may be wondering why anyone would want a special language for this. Python
is really easy to extend using C or C++, isn't it? Why not just write your
extension modules in one of those languages?

Well, if you've ever written an extension module for Python, you'll know that
things are not as easy as all that. First of all, there is a fair bit of
boilerplate code to write before you can even get off the ground. Then you're
faced with the problem of converting between Python and C data types. For the
basic types such as numbers and strings this is not too bad, but anything more
elaborate and you're into picking Python objects apart using the Python/C API
calls, which requires you to be meticulous about maintaining reference counts,
checking for errors at every step and cleaning up properly if anything goes
wrong. Any mistakes and you have a nasty crash that's very difficult to debug.

Various tools have been developed to ease some of the burdens of producing
extension code, of which perhaps SWIG is the best known. SWIG takes a
definition file consisting of a mixture of C code and specialised
declarations, and produces an extension module. It writes all the boilerplate
for you, and in many cases you can use it without knowing about the Python/C
API. But you need to use API calls if any substantial restructuring of the
data is required between Python and C.

What's more, SWIG gives you no help at all if you want to create a new
built-in Python type. It will generate pure-Python classes which wrap (in a
slightly unsafe manner) pointers to C data structures, but creation of true
extension types is outside its scope.

Another notable attempt at making it easier to extend Python is PyInline ,
inspired by a similar facility for Perl. PyInline lets you embed pieces of C
code in the midst of a Python file, and automatically extracts them and
compiles them into an extension. But it only converts the basic types
automatically, and as with SWIG,  it doesn't address the creation of new
Python types.

Cython aims to go far beyond what any of these previous tools provides. Cython
deals with the basic types just as easily as SWIG, but it also lets you write
code to convert between arbitrary Python data structures and arbitrary C data
structures, in a simple and natural way, without knowing anything about the
Python/C API. That's right -- nothing at all! Nor do you have to worry about
reference counting or error checking -- it's all taken care of automatically,
behind the scenes, just as it is in interpreted Python code. And what's more,
Cython lets you define new built-in Python types just as easily as you can
define new classes in Python.

Future Plans
============
Cython is not finished. Substantial tasks remaining. See
:ref:`cython-limitations-label` for a current list. 

