.. _tempita:


Tempita templating language
===========================

This document describes the Tempita Templating Engine.
It was originally developed by Ian Bicking.
The original version of Tempita is available on `PyPI <https://pypi.org/project/Tempita/>`_ and documentation can be found at https://github.com/TurboGears/tempita/blob/main/README.rst.

Tempita is used internally in Cython for non-trivial code-generation purposes.
It is also available to users as a public API for generating or customizing code when building a Cython module.


Overview
********

Tempita is a simple templating language, similar to Jinja.
Basic usage is as follows:

.. code-block:: python

    from Cython.Tempita import Template

    tmpl1 = Template(template_string)       # load from string
    tmpl2 = Template.from_filename(path)    # load template from file

    tmpl1.substitute(**kwargs)     # pass parameters as named arguments.
    tmpl2.sub_vars(mapping)        # pass an argument as dict-like mapping.

Tempita also provides a shortcut function:

.. code-block:: python

    from Cython.Tempita import sub
    sub(template_string, **kwargs)


Templating Syntax
*****************

Below are the different directive types and expression forms supported.


Simple Expression Substitution
------------------------------

Write expressions as ``{{ ... }}``, which are evaluated in the template context.

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

You can specify a default value for a variable using the ``default`` keyword,
and overwrite it by passing it as argument to the template substitution:

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

Arbitrary Python statements can be inserted inline with ``{{py: ...}}``.
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


Custom delimiter characters
---------------------------

In cases where the double braces that Tempita normally uses as delimiters (``{{...}}``) get in the way,
you can replace them with other characters:

.. code-block:: python

    >>> sub("Show literal braces: {{<<name>>}}", delimiters=['<<', '>>'], name="x")
    'Show literal braces: {{x}}'

.. note:: The ``delimiters`` can also be passed as an argument to the ``Template`` class,
thus keeping them together with the template definition that uses them,
rather than needing to remember them later in the substitution step.

   ``Template("...", delimiters=['((', '))'])``


Filters
-------

You can post-process the result of an expression before it is written into the template.
Below, the ``filtername`` refers to a callable (function) that will be called by the template engine
and receives the result of the preceding expression as argument.
Whatever it outputs will then be written into the templating result.

.. code-block:: python

    {{ expression | filtername }}

Example:

.. code-block:: python

    >>> sub("Lowercase: {{ name | lower }}", name="ALICE", lower=lambda x: x.lower())
    'Lowercase: alice'


Control Blocks
**************

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

You may also unpack tuples or iterate with multiple variables, as known from Python for-loops.

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


.. note:: As known from Python's for-loop, Tempita ``for`` blocks also support ``{{break}}`` and ``{{continue}}`` statements.


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

- Templates preserve whitespace exactly as written around directives.
- Newlines in templates become newlines in outputs.
- Indentation is preserved, so control block bodies should be indented
  meaningfully by the template author if you want nice output.


Examples
********

Here are consolidated examples showing most of the available syntax in use:

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
*********************

- Templates are evaluated when they are substituted, rather than when they are created; errors show up when calling
  :meth:`substitute`.
- There is no sandbox: template code can execute arbitrary Python expressions.
