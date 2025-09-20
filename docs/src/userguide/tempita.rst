.. _tempita:

Tempita templating language
===========================

This document describes template syntax features supported by Tempita - expressions, control blocks, escaping, filters, etc.

Overview
--------

A Tempita is a simple templating language Cython built-in similar to Jinja. Basic usage
is as follows:

.. code-block:: python

    from Cython.Tempita import Template

    tmpl1 = Template(template_string)       # load from string
    tmpl2 = Template.from_filename(path)    # load template from file

    tmpl1.substitute(**kwargs)     # pass parameters as named arguments.
    tmpl2.sub_vars(mapping)        # pass an argument as dict-like mapping.

Tempita supports also shortcut function:

.. code-block:: python

    from Cython.Tempita import sub
    sub(template_string, **kwargs)

Templating Syntax
-----------------

Below are the different directive types and expression forms supported.

Simple Expression Substitution
------------------------------

Surround expression with ``{{ ... }}``, which is evaluated in the template
context.

Example:

.. code-block:: python

    >>> sub("Hello {{name}}!", name="World")
    'Hello World!'

Expressions can be any valid Python expression: arithmetic, attribute access,
indexing, function calls etc.:

.. code-block:: python

    >>> sub("2 * 3 = {{2 * 3}}")
    '2 * 3 = 6'
    >>> class User:
    ...     name = 'Mark'
    ...
    >>> sub("User: {{ user.name }}", user=User())
    'User: Mark'
    >>> sub("Hex: {{ hex(num) }}", num=10)
    'Hex: 0xa'
    >>> sub("Number: {{ func(num) }}", func=abs, num=-10)
    'Number: 10'
    >>> sub("List[0] = {{ mylist[0] }}", mylist=[10,20,30])
    'List[0] = 10'
    >>> sub("Dist['name'] = {{ mydict['name'] }}", mydict={'name': 'Miss Islington'})
    "Dist['name'] = Miss Islington"
    >>> sub("Uppercase {{ string.upper() }}", string="hello")
    'Uppercase HELLO'

Default Values
--------------

You can specify a default value for a variable using ``default`` keyword:

.. code-block:: python

    >>> tmpl = Template("""
    ... {{default name = "Sir Lancelot the Brave"}}
    ... My name is {{name}}.
    ... """
    ... )
    >>> tmpl.substitute()
    'My name is Sir Lancelot the Brave.\n'
    >>> tmpl.substitute(name="Sir Bedevere the Wise")
    'My name is Sir Bedevere the Wise.\n'


Inline Python Code
------------------

Arbitrary python statements can be inserted inline with ``{{py: ...}}``.
These do not emit output directly but can modify the template context.

.. code-block:: python

    >>> tmpl = Template("""
    ... {{py: x = 5}}
    ... Value of x: {{x}}
    ... """)
    >>> tmpl.substitute()
    'Value of x: 5\n'

Comments
--------

Comments are introduced with ``{{# ... }}``. They are completely removed
from output.

.. code-block:: python

    >>> sub("Hello {{# This is a comment }}World.")
    'Hello World.'

Custom delimiters
-----------------

If you want literal text that looks like a directive (e.g. `{{...}}`), you
can use custom delimiters:

.. code-block:: python

    >>> sub("Show literal braces: {{((name))}}", delimiters=['((', '))'], name="x")
    'Show literal braces: {{x}}'

.. note:: Parameter `delimiters` can be also passed to ``Template`` class as an argument:

   ``Template("...", delimiters=['((', '))'])``

Filters
-------

You can pass callable which will be automatically called with expression as parameter:

.. code-block:: python

    {{ expression | filtername }}

Example:

.. code-block:: python

    >>> sub("Lowercase: {{ name | lower }}", name="ALICE", lower=lambda x: x.lower())
    'Lowercase: alice'

Control Blocks
==============

Tempita supports Python-like control flow directives.
These are evaluated at runtime and allow conditional rendering and iteration.

Each block has an explicit *closing directive* such as ``endif`` or ``endfor``.

``if`` / ``elif`` / ``else`` block
----------------------------------

Conditional execution based on an expression.

**Syntax**::

    {{if condition}}
      ... content if true ...
    {{elif other_condition}}
      ... content if elif is true ...
    {{else}}
      ... content if all above are false ...
    {{endif}}

**Example**:

.. code-block:: python

    >>> tmpl = Template("""
    ... {{if x > 0}}
    ... Positive
    ... {{elif x == 0}}
    ... Zero
    ... {{else}}
    ... Negative
    ... {{endif}}
    ... """)
    >>> tmpl.substitute(x=-5)
    'Negative\n'

``for`` block
-------------

Iterate over a sequence and render the body for each element.

**Syntax**::

    {{for var in iterable}}
      ... body using {{var}} ...
    {{endfor}}

You may also unpack tuples or iterate with multiple variables.

**Example**:

.. code-block:: python

    >>> tmpl = Template("""
    ... {{for name, score in scores}}
    ... {{name}}: {{score}}
    ... {{endfor}}
    ... """)
    >>> print(tmpl.substitute(scores=[("Alice", 95), ("Bob", 88)]))
    Alice: 95
    Bob: 88


.. note:: Tempita ``for`` block supports also ``{{break}}`` and ``{{continue}}`` statements.

Nesting Blocks
--------------

Blocks can be nested arbitrarily.

.. code-block:: python

    >>> tmpl = Template("""
    ... {{for item in items}}
    ...   {{if item < 0}}
    ...   {{continue}}
    ...   {{elif item % 2 == 0}}
    ...   {{item}} is even
    ...   {{else}}
    ...   {{item}} is odd
    ...   {{endif}}
    ... {{endfor}}
    ... """)
    >>> print(tmpl.substitute(items=[-1, 1, 2, 3]))
      1 is odd
      2 is even
      3 is odd

Indentation, Whitespace, and Newlines
-------------------------------------

- The template preserves whitespace exactly as written around directives.
- Newlines in the template become newlines in output.
- Indentation is preserved, so control block bodies should be indented
  meaningfully by the template author if you want nice output.

Examples
--------

Here are consolidated examples showing most syntax in use:

.. code-block:: python

    from Cython.Tempita import Template

    tmpl = Template("""
    Header
    {{# This is a comment }}

    {{if user["is_admin"]}}
      Welcome, Admin {{user["name"]}}!
    {{else}}
      Hello, {{user["name"] or 'Guest'}}.
    {{endif}}

    {{for item in items}}
      * {{item["name"]}}: {{item["value"]}}
    {{endfor}}

    {{py: x = 1 + 2}}
    Inline code result: {{x}}

    Expression: 1 + 2 = {{1 + 2}}

    """)

    print(tmpl.substitute(user={'name': 'Bob', 'is_admin': False},
                          items=[{'name':'A','value':10},
                                 {'name':'B','value':20}]))

Output::

    Header
      Hello, Bob.

      * A: 10
      * B: 20

    Expression: 1 + 2 = 3

Notes and Limitations
---------------------

- Templates are evaluated at runtime; errors show up when calling
  :meth:`substitute`.
- There is no sandbox: template code can execute arbitrary Python expressions.
