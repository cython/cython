Cython internals
================

The parse tree (AST)
--------------------

As pretty much any compiler, Cython parses source code into a parse tree or Abstract Syntax Tree.
Tree nodes represent a specific syntax or language feature, such as a try-finally statement
or a binary plus operation. Some of them also represent compiler internal tree state or operations
that are needed by Cython's code generation.

Statement nodes live in the ``Nodes.py`` module, whereas expression nodes (names, values and any
operation that has a result) live in ``ExprNodes.py``. The main base classes
``Node`` (in `Nodes.py <https://github.com/cython/cython/blob/master/Cython/Compiler/Nodes.py>`_) and
ExprNode (in `ExprNodes.py <https://github.com/cython/cython/blob/master/Cython/Compiler/ExprNodes.py>`_)
have some comments about their inner workings and the main analysis transforms:
declaration analysis and expression/types analysis.

Except for these two phases (which directly traverse and modify the tree via the
``.analyse_declarations()`` and ``.analyse_expressions()`` / ``.analyse_types()`` methods),
all tree modifications use tree visitor transforms. A transform
(see `ParseTreeTransforms.py <https://github.com/cython/cython/blob/master/Cython/Compiler/ParseTreeTransforms.py>`_)
is a class that uses the visitor pattern
(see `Visitor.py <https://github.com/cython/cython/blob/master/Cython/Compiler/Visitor.py>`_)
to traverse the tree and intercept on specific nodes that it can process.
The node matching uses a method naming pattern ``.visit_SomeNode``, where ``SomeNode``
is a specific node class (or a node base class). When a node is found whose class type
matches one of the visitor methods, the method is called with that node as argument,
and whatever it returns (the original node or something else) is then injected into
the tree to replace the original node. This makes it easy for a transform to apply tree modifications.

The AST can be inspected at various stages of the pipeline by adding ``PrintTree()`` into the pipeline.
``PrintTree()(some_node)`` can be a useful tool for debugging the state of a node
anywhere in the code that handles nodes (it need not only be used from the pipeline).

How to add a new attribute to an AST node
-----------------------------------------

Tree nodes have two types of attributes: simple node data and state, and child nodes.
There is nothing special about the state of a node. In that regard, it's just a Python object with attributes.

Child nodes, however, need to be integrated with the tree traversal. The traversal is
external to the node, and implemented in the visitor and transform base classes.
In order to let them know which attributes are tree child nodes, they are listed in the child_attrs attribute,
a Python list of attribute names. Note that children are traversed in the order
in which they are listed here. That is often important when it comes to execution
order or semantic dependencies between children.

As mentioned before, the analysis of declarations and expressions do not follow the visitor pattern
(at least inside of the main module code, classes and functions). They have their own traversal
and tree modification mechanism, by explicitly calling the respective methods of their child nodes.
This is done because they need a lot of control over

a. the order in which child nodes are processed and 
b. the way in which their children are analysed, modified and replaced.

The most complex decisions in Cython are taking during expression/types analysis.
Thus, the ``.analyse_expressions()`` call chain (or its slightly simpler fallback ``.analyse_types()``)
has a transform-like mechanism that returns the modified node, so that
the caller can further process it and/or replace its original child with it.

When adding a new child to a tree node, all three places need to be modified:
the ``child_attrs`` list, the ``.analyse_declarations()`` method,
and the ``.analyse_expressions()`` or ``.analyse_types()`` method of the parent node,
so that the new child is correctly traversed and processed by all tree analysis and modification phases.

Utility Code
------------

C code that is included directly into Cython modules is stored in ``Cython/Utility`` and is
included using the ``UtilityCode`` classes.  There are a few points of customization:

* ``PYIDENT("some_name")`` is replaced with cached and interned string while ``PYUNICODE``
  is replaced with a cached string.
* ``CALL_UNBOUND_METHOD(type, "method_name"[, args])`` produces an optimized (and cached)
  call to a method of a builtin type.
* ``#substitute: naming`` allows you to refer to variables in the ``Cython.Compiler.Naming``
  module using ``$varname``.
* ``EMPTY(tuple)`` (or ``bytes`` or ``unicode``) is a quick way of getting access to an
  empty immutable container..
* ``CGLOBAL(varname)`` looks up ``varname`` in the module state structure. 
  ``NAMED_CGLOBAL(named_varname)`` looks up the result of ``Cython.Compiler.Naming.named_varname``
  in the module state structure.
* "Tempita" is a more advanced templating language vendored into Cython
  (but `originally written by Ian Bicking outside Cython <https://github.com/TurboGears/tempita>`_)
  which can be used for more advanced code-generation.

Naming conventions
------------------

* Modules use ``CamelCase`` naming for historical reasons (the code base predates PEP-8, and of course
  PEP-8 is only *required* for the Python standard library and other code can choose to adopt it or not).
* To avoid naming collisions in C space, global C names are "always" prefixed with ``__pyx_``,
  internal function names and types with ``__Pyx_``, internal upper-case macros with ``__PYX_``.
  Exceptions to this rule are exceptions to this rule.
* User definable/overridable macros (e.g. feature switches) are prefixed with ``CYTHON_``.
