# -*- coding: utf-8 -*-
#
# Cython documentation build configuration file, created by
# sphinx-quickstart on Fri Apr 25 12:49:32 2008.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed automatically).
#
# All configuration values have a default value; values that are commented out
# serve to show the default value.

import sys
import re
import os.path

# If your extensions are in another directory, add it here.
sys.path.append('sphinxext')

# Import support for ipython console session syntax highlighting (lives
# in the sphinxext directory defined above)
import ipython_console_highlighting

# General configuration
# ---------------------

# Use cython as the default syntax highlighting language, as python is a subset
# this does the right thing
highlight_language = 'cython'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['ipython_console_highlighting', 'cython_highlighting', 'sphinx.ext.pngmath', 'sphinx.ext.todo', 'sphinx.ext.intersphinx']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

exclude_patterns = ['py*', 'build']

# General substitutions.
project = 'Cython'
copyright = '2011, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al.'

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The full version, including alpha/beta/rc tags.
release = '0.15'
try:
    _match_version = re.compile(r'^\s*_*version\s*_*\s*=\s*["\']([^"\']+)["\'].*').match
    with open(os.path.join(os.path.dirname(__file__), '..', 'Cython', '__init__.py')) as _f:
        for line in _f:
            _m = _match_version(line)
            if _m:
                release = _m.group(1)
                break
except:
    pass
# The short X.Y version.
version = re.sub('^([0-9]+[.][0-9]+).*', '\g<1>', release)

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%B %d, %Y'

# List of documents that shouldn't be included in the build.
#unused_docs = []

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Options for HTML output
# -----------------------

# suffix for generated files
html_file_suffix = '.html'

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_style = 'default.css'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# Include the Cython logo in the sidebar
html_logo = '_static/cython-logo-light.png'

# used a favicon!
html_favicon = '_static/favicon.ico'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Content template for the index page.
#html_index = ''

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = False

# Don't generate and index
html_use_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
#html_copy_source = True

# Output file base name for HTML help builder.
htmlhelp_basename = 'Cythondoc'


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
#latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class [howto/manual]).
#_stdauthor = r'Greg Ewig\\ Gabriel Gellner, editor'
_stdauthor = r'Stefan Behnel, Robert Bradshaw, William Stein\\ Gary Furnish, Dag Seljebotn, Greg Ewing\\ Gabriel Gellner, editor'
latex_documents = [
    ('src/reference/index', 'reference.tex',
     'Cython Reference Guide', _stdauthor, 'manual'),
    ('src/tutorial/index', 'tutorial.tex',
     'Cython Tutorial', _stdauthor, 'manual')
]

# Additional stuff for the LaTeX preamble.
#latex_preamble = ''

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_use_modindex = True

# todo
todo_include_todos = True

# intersphinx for standard :keyword:s (def, for, etc.)
intersphinx_mapping = {'python': ('http://docs.python.org/3.2', None)}
